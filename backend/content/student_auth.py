"""Session-based student identity. Provider calls are isolated for mocked verification."""
import base64
import hashlib
import re
import secrets
import time
import unicodedata
from urllib.parse import urlencode, urlparse

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.db.models import F
from django.http import HttpResponseRedirect
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.response import Response

from .exceptions import ServiceError
from .models import AuthRateWindow, StudentIdentity
from .permissions import student_endpoint


def reply(data, status=200):
    return Response(data, status=status, headers={'Cache-Control': 'no-store'})


def require_student(request):
    if getattr(settings, 'LEARNING_AUTH_REQUIRED', False):
        from core.public_demo_support import is_student
        if not is_student(request.user):
            raise ServiceError('auth_required', 'Sign in with a student account.', 401)
    if not request.user.is_authenticated or not request.user.is_active:
        raise ServiceError('auth_required', 'Sign in to access your learning records.', 401)
    return request.user


def body(request, fields):
    data = request.data
    if type(data) is not dict or set(data) - set(fields):
        raise ServiceError('invalid_request', 'Provide only the expected fields.', 400)
    return data


def text(data, key, maximum=254, required=True):
    value = data.get(key, '')
    if type(value) is not str or len(value) > maximum or (required and not value.strip()):
        raise ServiceError('invalid_request', f'Provide a valid {key.replace("_", " ")}.', 400)
    return value.strip() if key != 'password' else value


def normalized_email(value):
    from django.core.validators import validate_email
    value = unicodedata.normalize('NFKC', value).strip().casefold()
    try: validate_email(value)
    except ValidationError: raise ServiceError('invalid_email', 'Provide a valid email address.', 400) from None
    return value


def password_ok(password, user):
    try: validate_password(password, user)
    except ValidationError as error:
        raise ServiceError('invalid_password', ' '.join(error.messages), 400) from None


def rate_limit(scope, identifier, limit=10, seconds=900):
    key = salted_hmac('student-rate', f'{scope}:{int(time.time()) // seconds}:{identifier}', algorithm='sha256').hexdigest()
    with transaction.atomic():
        window, _ = AuthRateWindow.objects.get_or_create(key=key)
        if not AuthRateWindow.objects.filter(pk=window.pk, count__lt=limit).update(count=F('count') + 1):
            raise ServiceError('rate_limited', 'Too many requests. Please try again later.', 429)


def throttle(request, scope, identifier=''):
    address = request.META.get('REMOTE_ADDR', 'unknown')
    if address in settings.TRUSTED_PROXY_IPS:
        from ipaddress import ip_address
        try: address = str(ip_address(request.META.get('HTTP_X_REAL_IP', '')))
        except ValueError: raise ServiceError('invalid_proxy', 'The request could not be validated.', 400) from None
    rate_limit(scope + '-ip', address, 30)
    if identifier: rate_limit(scope + '-identity', identifier.casefold(), 8)


def user_data(user):
    return {'id': user.pk, 'username': user.username, 'email': user.email,
            'name': user.get_full_name() or user.username}


def login_response(request, user):
    auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
    return reply({'authenticated': True, 'user': user_data(user)})


@student_endpoint(['POST'])
def auth_register(request):
    if not getattr(settings, 'STUDENT_REGISTRATION_ENABLED', True):
        raise ServiceError('registration_disabled', 'Registration is unavailable in this synthetic demonstration. Use an assigned demo account; do not enter personal information.', 503)
    data = body(request, ['username', 'password', 'email', 'name'])
    username = unicodedata.normalize('NFKC', text(data, 'username', 150)).casefold()
    if not re.fullmatch(r'[a-z0-9_.-]{3,150}', username):
        raise ServiceError('invalid_username', 'Use 3–150 letters, numbers, dots, underscores or hyphens.', 400)
    email = normalized_email(text(data, 'email'))
    password = text(data, 'password', 256)
    name = text(data, 'name', 150, False)
    throttle(request, 'register', email)
    User = get_user_model()
    user = User(username=username, email=email, first_name=name)
    password_ok(password, user)
    try:
        with transaction.atomic():
            if User.objects.filter(username__iexact=username).exists() or User.objects.filter(email__iexact=email).exists():
                raise ServiceError('account_unavailable', 'An account with those details already exists. Sign in or reset its password.', 409)
            user.set_password(password); user.save()
            StudentIdentity.objects.create(user=user, email=email)
    except IntegrityError:
        raise ServiceError('account_unavailable', 'An account with those details already exists.', 409) from None
    return login_response(request, user)


@student_endpoint(['POST'])
def auth_login(request):
    data = body(request, ['username', 'password'])
    identifier = text(data, 'username', 254).casefold()
    password = text(data, 'password', 256)
    throttle(request, 'login', identifier)
    User = get_user_model()
    matches = User.objects.filter(email__iexact=identifier) if '@' in identifier else User.objects.filter(username__iexact=identifier)
    names = list(matches.values_list('username', flat=True)[:2])
    # authenticate even on a miss so Django performs its password-hasher timing work.
    user = auth.authenticate(request, username=names[0] if len(names) == 1 else identifier, password=password)
    from core.public_demo_support import is_student
    if user is None or len(names) != 1 or (getattr(settings, 'LEARNING_AUTH_REQUIRED', False) and not is_student(user)):
        raise ServiceError('invalid_credentials', 'Invalid sign-in details.', 401)
    return login_response(request, user)


@student_endpoint(['POST'])
def auth_logout(request):
    auth.logout(request)
    return reply({'authenticated': False, 'user': None})


@student_endpoint(['GET'])
def auth_status(request):
    from core.public_demo_support import is_student
    authenticated = request.user.is_authenticated and (not getattr(settings, 'LEARNING_AUTH_REQUIRED', False) or is_student(request.user))
    return reply({'authenticated': bool(authenticated),
                  'user': user_data(request.user) if authenticated else None})


@student_endpoint(['POST'])
def password_reset_request(request):
    data = body(request, ['email'])
    email = normalized_email(text(data, 'email'))
    throttle(request, 'password-reset', email)
    origin = settings.SITE_ORIGIN.rstrip('/')
    parsed = urlparse(origin)
    if not parsed.netloc or parsed.scheme not in ('https', 'http') or (settings.PRODUCTION and parsed.scheme != 'https'):
        # Configuration errors must have the same result for known and unknown email.
        raise ServiceError('email_unavailable', 'Password recovery is temporarily unavailable.', 503)
    User = get_user_model()
    users = list(User.objects.filter(email__iexact=email, is_active=True)[:2])
    if len(users) == 1 and users[0].has_usable_password():
        user = users[0]
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # Fragment keeps reset credentials out of HTTP access logs and Referer headers.
        link = f'{origin}/reset-password#uid={uid}&token={token}'
        try:
            send_mail('Reset your Prepal password', f'Use this link within 30 minutes:\n{link}\nIgnore this email if you did not request it.', settings.DEFAULT_FROM_EMAIL, [user.email])
        except Exception:
            # Same outward result avoids disclosing whether an account exists.
            pass
    return reply({'message': 'If a password account matches, recovery instructions will be emailed.'}, 202)


@student_endpoint(['POST'])
def password_reset_confirm(request):
    data = body(request, ['uid', 'token', 'password'])
    uid, token, password = text(data, 'uid', 100), text(data, 'token', 200), text(data, 'password', 256)
    throttle(request, 'password-confirm', uid)
    try: pk = force_str(urlsafe_base64_decode(uid))
    except (ValueError, UnicodeDecodeError): pk = None
    User = get_user_model()
    with transaction.atomic():
        user = User.objects.select_for_update().filter(pk=pk).first() if pk and pk.isdecimal() and len(pk) < 20 else None
        if not user or not user.is_active or not default_token_generator.check_token(user, token):
            raise ServiceError('invalid_reset', 'This recovery link is invalid or expired.', 400)
        password_ok(password, user)
        user.set_password(password); user.save(update_fields=['password'])
    auth.logout(request)
    return reply({'message': 'Password changed. Sign in with your new password.'})


def google_configured():
    return bool(settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET and settings.GOOGLE_REDIRECT_URI)


@student_endpoint(['POST'])
def google_start(request):
    throttle(request, 'google-start')
    if not google_configured():
        raise ServiceError('google_unavailable', 'Google sign-in is not configured. Use email and password.', 503)
    redirect = urlparse(settings.GOOGLE_REDIRECT_URI)
    if redirect.scheme != 'https' and not (not settings.PRODUCTION and redirect.scheme == 'http' and redirect.hostname in ('localhost', '127.0.0.1')):
        raise ServiceError('google_unavailable', 'Google sign-in configuration needs review.', 503)
    state, nonce, verifier = secrets.token_urlsafe(32), secrets.token_urlsafe(32), secrets.token_urlsafe(64)
    request.session['google_auth'] = {'state': state, 'nonce': nonce, 'verifier': verifier, 'started': time.time()}
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
    return reply({'url': 'https://accounts.google.com/o/oauth2/v2/auth?' + urlencode({
        'client_id': settings.GOOGLE_CLIENT_ID, 'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'response_type': 'code', 'scope': 'openid email profile', 'state': state, 'nonce': nonce,
        'code_challenge': challenge, 'code_challenge_method': 'S256', 'access_type': 'online',
    })})


def exchange_google(code, verifier):
    # No tokens are persisted; the only retained provider identifier is its stable sub.
    import requests
    from google.auth.transport.requests import Request
    from google.oauth2.id_token import verify_oauth2_token
    response = requests.post('https://oauth2.googleapis.com/token', data={
        'code': code, 'client_id': settings.GOOGLE_CLIENT_ID, 'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI, 'grant_type': 'authorization_code', 'code_verifier': verifier,
    }, timeout=10)
    response.raise_for_status()
    class BoundedRequest(Request):
        def __call__(self, *args, **kwargs):
            kwargs['timeout'] = 10
            return super().__call__(*args, **kwargs)
    return verify_oauth2_token(response.json()['id_token'], BoundedRequest(), settings.GOOGLE_CLIENT_ID)


@student_endpoint(['GET'])
def google_callback(request):
    state = request.session.pop('google_auth', None)
    throttle(request, 'google-callback')
    received = request.query_params.get('state', '')
    code = request.query_params.get('code', '')
    if (not google_configured() or not state or time.time() - state['started'] > 600
            or len(request.query_params.getlist('state')) != 1 or not constant_time_compare(state['state'], received)
            or not code or len(code) > 4096 or len(request.query_params.getlist('code')) != 1):
        raise ServiceError('invalid_oauth', 'Google sign-in expired or could not be verified. Start again.', 400)
    try: claims = exchange_google(code, state['verifier'])
    except Exception: raise ServiceError('invalid_oauth', 'Google could not verify this sign-in.', 400) from None
    if (claims.get('iss') not in ('accounts.google.com', 'https://accounts.google.com')
            or claims.get('aud') != settings.GOOGLE_CLIENT_ID or claims.get('email_verified') is not True
            or not isinstance(claims.get('sub'), str) or not 1 <= len(claims['sub']) <= 255
            or not isinstance(claims.get('nonce'), str) or not constant_time_compare(claims['nonce'], state['nonce'])
            or not isinstance(claims.get('exp'), (int, float)) or claims['exp'] <= time.time()):
        raise ServiceError('invalid_oauth', 'Google identity claims could not be verified.', 400)
    email = normalized_email(claims.get('email', '') if isinstance(claims.get('email'), str) else '')
    User = get_user_model()
    try:
        with transaction.atomic():
            identity = StudentIdentity.objects.select_related('user').filter(google_subject=claims['sub']).first()
            if identity:
                user = identity.user
                if not user.is_active or identity.email != email:
                    raise ServiceError('account_unavailable', 'This identity requires account support.', 403)
            else:
                if User.objects.filter(email__iexact=email).exists() or StudentIdentity.objects.filter(email=email).exists():
                    raise ServiceError('account_link_required', 'This email already has an account. Sign in with its existing method; automatic linking is disabled.', 409)
                user = User.objects.create_user(username='google_' + secrets.token_hex(16), email=email,
                    first_name=str(claims.get('name', ''))[:150])
                user.set_unusable_password(); user.save(update_fields=['password'])
                StudentIdentity.objects.create(user=user, email=email, google_subject=claims['sub'])
    except IntegrityError: raise ServiceError('account_unavailable', 'This identity requires account support.', 409) from None
    login_response(request, user)
    response = HttpResponseRedirect('/dashboard')
    response['Cache-Control'] = 'no-store'; response['Referrer-Policy'] = 'no-referrer'
    return response


@student_endpoint(['GET', 'POST'])
def account_deletion_readiness(request):
    """Non-destructive approval gate. No deletion path exists until retention is approved."""
    user = require_student(request)
    if request.method == 'POST':
        data = body(request, ['password', 'confirmation'])
        password = text(data, 'password', 256)
        throttle(request, 'deletion-reauth', str(user.pk))
        if not user.has_usable_password() or not user.check_password(password):
            raise ServiceError('reauthentication_required', 'Verify your current password to continue.', 403)
        if text(data, 'confirmation', 30) != 'DELETE MY ACCOUNT':
            raise ServiceError('confirmation_required', 'Explicit account deletion confirmation is required.', 400)
        raise ServiceError('deletion_policy_pending', 'Account deletion is not enabled. Retention and backup expiry require owner approval.', 409)
    from .models import Bookmark, UserProgress, QuizAttempt, StudyPlan, StudyTask
    return reply({'status': 'policy_approval_required', 'deletion_enabled': False,
                  'records': {'bookmarks': Bookmark.objects.filter(user=user).count(),
                              'progress': UserProgress.objects.filter(user=user).count(),
                              'attempts': QuizAttempt.objects.filter(user=user).count(),
                              'plans': StudyPlan.objects.filter(user=user).count(),
                              'tasks': StudyTask.objects.filter(plan__user=user).count()},
                  'message': 'No data will be deleted. Backup retention and session revocation policy await approval.'})
