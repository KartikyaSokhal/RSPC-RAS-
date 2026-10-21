import uuid
from django.conf import settings
from django.core import signing
from django.http import FileResponse
from django.middleware.csrf import get_token
from django.utils.crypto import salted_hmac
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .exceptions import ServiceError
from .serializers import ChatInputSerializer, QuizSerializer
from .services.publication import visible_publications, resolve_publication, summary, detail, get_syllabus_tree
from .services.quiz import QuizServiceError, parse_quiz_id, select_reviewed_quiz, revision_token, check_answers
from .services.resources import authorized_resource, file_digest
from .services.tutor import answer
from .services.search import search


def public_json(data, status=200):
    return Response(data, status=status, headers={'Cache-Control': 'no-store'})


@api_view(['GET'])
def health(request):
    from .models import TopicPublication
    TopicPublication.objects.values_list('pk', flat=True).first()
    return public_json({'status': 'ok'})


@api_view(['GET'])
@ensure_csrf_cookie
def configuration(request):
    response = public_json({'demo': settings.DEMO_MODE, 'ai_enabled': settings.AI_ENABLED and settings.AI_GUEST_ENABLED,
                            'support_email': settings.SUPPORT_EMAIL, 'csrf_token': get_token(request)})
    try: request.get_signed_cookie('prepal_visitor', salt='visitor', max_age=86400)
    except (KeyError, signing.BadSignature):
        response.set_signed_cookie('prepal_visitor', uuid.uuid4().hex, salt='visitor', max_age=86400, httponly=True, secure=settings.PRODUCTION, samesite='Lax')
    return response


@api_view(['GET'])
def topic_root_list(request):
    published_only = request.query_params.get('published_only') == '1'
    include_tree = request.query_params.get('tree') == '1'
    return public_json(get_syllabus_tree(published_only=published_only, include_tree=include_tree, user=request.user))


@api_view(['GET'])
def topic_detail(request, slug):
    from .models import Topic
    pubs = visible_publications()
    pub = next((p for p in pubs.values() if p.snapshot.get('slug') == slug), None)
    if pub is not None:
        return public_json(detail(pub, pubs, user=request.user))

    topic = Topic.objects.filter(slug=slug).first()
    if topic is None:
        raise ServiceError('topic_not_found', 'This topic was not found.', 404)

    is_bookmarked = False
    is_completed = False

    breadcrumbs = []
    curr = topic
    while curr:
        curr_pub = pubs.get(curr.id)
        breadcrumbs.append({
            'id': curr.id,
            'title': curr_pub.title if curr_pub else curr.title,
            'slug': curr_pub.snapshot.get('slug', curr.slug) if curr_pub else curr.slug,
            'has_children': curr.children.exists(),
            'is_published': curr_pub is not None,
            'has_notes': bool(curr_pub and curr_pub.snapshot.get('blocks')),
        })
        curr = curr.parent
    breadcrumbs.reverse()

    user_bookmarks = set()
    user_completed = set()

    children = []
    for c in topic.children.all().order_by('order', 'id'):
        c_pub = pubs.get(c.id)
        children.append({
            'id': c.id,
            'title': c_pub.title if c_pub else c.title,
            'slug': c_pub.snapshot.get('slug', c.slug) if c_pub else c.slug,
            'has_children': c.children.exists(),
            'is_published': c_pub is not None,
            'has_notes': bool(c_pub and c_pub.snapshot.get('blocks')),
            'has_quiz': False,
            'has_resources': False,
            'is_bookmarked': c.id in user_bookmarks,
            'is_completed': c.id in user_completed,
        })

    return public_json({
        'id': topic.id,
        'title': topic.title,
        'slug': topic.slug,
        'revision': None,
        'is_published': False,
        'has_notes': False,
        'status': 'coming_soon',
        'blocks': [],
        'children': children,
        'breadcrumbs': breadcrumbs,
        'related': [],
        'resources': [],
        'has_quiz': False,
        'published_at': None,
        'is_bookmarked': is_bookmarked,
        'is_completed': is_completed,
        'message': 'Notes for this syllabus topic are currently under editorial preparation.',
    })



@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_protect
def topic_chat(request, slug):
    serializer = ChatInputSerializer(data=request.data); serializer.is_valid(raise_exception=True)
    # Check disabled configuration before lookup or quota writes.
    if not settings.AI_ENABLED or not settings.AI_GUEST_ENABLED:
        raise ServiceError('ai_unavailable', 'The tutor is temporarily unavailable. You can continue reading.', 503)
    if request.user.is_authenticated:
        visitor = f"user-{request.user.id}"
        need_cookie = False
    else:
        try:
            visitor = request.get_signed_cookie('prepal_visitor', salt='visitor', max_age=86400)
            need_cookie = False
        except (KeyError, signing.BadSignature):
            visitor = uuid.uuid4().hex
            need_cookie = True
    visitor_key = salted_hmac('visitor-quota', visitor).hexdigest()
    address = request.META.get('REMOTE_ADDR', 'unknown')
    if address in settings.TRUSTED_PROXY_IPS:
        from ipaddress import ip_address
        try: address = str(ip_address(request.META.get('HTTP_X_REAL_IP', '')))
        except ValueError: raise ServiceError('invalid_proxy', 'The request could not be validated.', 400) from None
    ip_key = salted_hmac('ip-quota', address).hexdigest()
    response = public_json(answer(slug, serializer.validated_data, visitor_key, ip_key))
    if need_cookie:
        response.set_signed_cookie('prepal_visitor', visitor, salt='visitor', max_age=86400, httponly=True, secure=settings.PRODUCTION, samesite='Lax')
    return response


@api_view(['GET'])
def topic_quiz(request, slug):
    try:
        ids = request.query_params.getlist('quiz_id')
        if len(ids) > 1: raise QuizServiceError(400, 'invalid_quiz_id', 'Expected one quiz_id.')
        quiz_id = parse_quiz_id(ids[0]) if ids else None
        resolve_publication(slug)
        quiz = select_reviewed_quiz(slug, quiz_id)
        return public_json({**QuizSerializer(quiz).data, 'revision_token': revision_token(quiz)})
    except QuizServiceError as error:
        return public_json(error.payload, error.status)
    except ServiceError as error:
        if error.status_code == 404:
            return public_json({'error': {'code': 'quiz_unavailable', 'message': 'No reviewed quiz is available for this topic.'}}, 404)
        raise


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_protect
def topic_quiz_check(request, slug):
    resolve_publication(slug)
    try: return public_json(check_answers(slug, request.data))
    except QuizServiceError as error: return public_json(error.payload, error.status)


@api_view(['GET'])
def search_results(request):
    query = request.query_params.get('q', '').strip()
    if len(query) > 200: raise ServiceError('invalid_query', 'Search queries must be at most 200 characters.')
    page = request.query_params.get('page', '1')
    if len(page) > 3 or not page.isascii() or not page.isdecimal() or not 1 <= int(page) <= 250:
        raise ServiceError('invalid_page', 'Choose a valid results page.')
    return public_json(search(query, int(page)))


@api_view(['GET'])
def resource_detail(request, resource_id):
    resource, pub = authorized_resource(resource_id)
    page = request.query_params.get('page', '1')
    if len(page) > 3 or not page.isascii() or not page.isdecimal() or not 1 <= int(page) <= resource.page_count:
        raise ServiceError('invalid_page', 'Choose a page in this document.')
    text = resource.pages.filter(page_number=int(page)).first()
    if text is None: raise ServiceError('resource_unavailable', 'Page text is unavailable.', 404)
    return public_json({'id': resource.pk, 'title': resource.title, 'page_count': resource.page_count,
        'source_reference': resource.source_reference, 'page': int(page), 'text': text.text, 'source_id': f'r{resource.pk}p{page}',
        'topic': summary(pub, {pub.topic_id: pub}), 'file_url': f'/api/resources/{resource.pk}/file/'})


@api_view(['GET'])
def resource_file(request, resource_id):
    resource, pub = authorized_resource(resource_id)
    try:
        valid = file_digest(resource) == resource.sha256
        stream = resource.file.open('rb') if valid else None
    except OSError:
        valid = False
    if not valid:
        raise ServiceError('resource_changed', 'This resource is temporarily unavailable.', 404)
    response = FileResponse(stream, content_type='application/pdf', as_attachment=False, filename='prepal-resource.pdf')
    response['Cache-Control'] = 'private, no-store'
    response['Content-Security-Policy'] = "sandbox; default-src 'none'"
    response['X-Content-Type-Options'] = 'nosniff'
    return response


@api_view(['GET'])
def topic_image(request, slug, block_id):
    import hashlib
    from django.core.files.storage import default_storage
    pub, pubs = resolve_publication(slug)
    block = next((b for b in pub.snapshot['blocks'] if b['id'] == block_id and b['block_type'] == 'image'), None)
    if not block or not block.get('file_name'): raise ServiceError('image_unavailable', 'Image unavailable.', 404)
    try:
        stream = default_storage.open(block['file_name'], 'rb')
        if hashlib.sha256(stream.read()).hexdigest() != block['file_hash']:
            stream.close(); raise ServiceError('image_unavailable', 'Image unavailable.', 404)
        stream.seek(0)
        from PIL import Image
        image = Image.open(stream); content_type = Image.MIME[image.format]; stream.seek(0)
    except OSError:
        raise ServiceError('image_unavailable', 'Image unavailable.', 404) from None
    response = FileResponse(stream, content_type=content_type)
    response['Cache-Control'] = 'private, no-store'; response['X-Content-Type-Options'] = 'nosniff'
    return response


@api_view(['POST'])
@csrf_protect
def auth_register(request):
    import re
    data = request.data
    username = str(data.get('username', '')).strip()
    password = str(data.get('password', ''))
    email = str(data.get('email', '')).strip()
    full_name = str(data.get('name', '')).strip()

    if len(username) < 3 or len(username) > 150 or not re.match(r'^[a-zA-Z0-9_.-]+$', username):
        raise ServiceError('invalid_username', 'Username must be 3-150 characters (letters, numbers, underscores).', 400)
    if len(password) < 8:
        raise ServiceError('invalid_password', 'Password must be at least 8 characters long.', 400)
    from django.contrib.auth.models import User
    from django.contrib import auth
    if User.objects.filter(username__iexact=username).exists():
        raise ServiceError('username_taken', 'This username is already registered.', 409)
    if email and User.objects.filter(email__iexact=email).exists():
        raise ServiceError('email_taken', 'An account with this email already exists.', 409)

    first_name = full_name.split()[0] if full_name else ''
    last_name = ' '.join(full_name.split()[1:]) if full_name and len(full_name.split()) > 1 else ''
    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
    auth.login(request, user)
    return public_json({
        'authenticated': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.get_full_name() or user.username,
        }
    })


@api_view(['POST'])
@csrf_protect
def auth_login(request):
    from django.contrib import auth
    data = request.data
    username = str(data.get('username', '')).strip()
    password = str(data.get('password', ''))
    if not username or not password:
        raise ServiceError('missing_credentials', 'Username and password are required.', 400)
    user = auth.authenticate(request, username=username, password=password)
    if user is None:
        return public_json({'error': {'code': 'invalid_credentials', 'message': 'Invalid username or password.'}}, 401)
    auth.login(request, user)
    return public_json({
        'authenticated': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.get_full_name() or user.username,
        }
    })


@api_view(['POST'])
@csrf_protect
def auth_logout(request):
    from django.contrib import auth
    auth.logout(request)
    return public_json({'authenticated': False, 'user': None})


@api_view(['GET'])
@ensure_csrf_cookie
def auth_status(request):
    if request.user.is_authenticated:
        return public_json({
            'authenticated': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'name': request.user.get_full_name() or request.user.username,
            }
        })
    return public_json({'authenticated': False, 'user': None})


@api_view(['GET'])
def learner_dashboard(request):
    if not request.user.is_authenticated:
        return public_json({'error': {'code': 'auth_required', 'message': 'Sign in to access your student dashboard.'}}, 401)
    from .models import Bookmark, UserProgress, QuizAttempt, Topic
    user = request.user
    bookmarks = list(Bookmark.objects.filter(user=user).select_related('topic').order_by('-created_at')[:50])
    completed_records = list(UserProgress.objects.filter(user=user, is_completed=True).select_related('topic').order_by('-last_read_at')[:100])
    recent_progress = list(UserProgress.objects.filter(user=user).select_related('topic').order_by('-last_read_at')[:10])
    attempts = list(QuizAttempt.objects.filter(user=user).select_related('quiz', 'quiz__topic').order_by('-attempted_at')[:20])

    total_topics = 152
    completed_count = len(completed_records)
    total_score = sum(a.score for a in attempts)
    total_possible = sum(a.total_questions for a in attempts)
    avg_accuracy = round((total_score / total_possible) * 100) if total_possible > 0 else None

    # Deterministic suggestion: find next topics that are uncompleted
    completed_ids = {p.topic_id for p in completed_records}
    suggested = []
    for t in Topic.objects.filter(parent__isnull=False).order_by('order', 'id'):
        if t.id not in completed_ids:
            suggested.append({'id': t.id, 'title': t.title, 'slug': t.slug})
            if len(suggested) >= 4:
                break

    return public_json({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.get_full_name() or user.username,
        },
        'stats': {
            'total_completed': completed_count,
            'total_topics': total_topics,
            'progress_percentage': round((completed_count / total_topics) * 100, 1),
            'total_bookmarks': len(bookmarks),
            'total_quizzes_taken': len(attempts),
            'average_quiz_accuracy': avg_accuracy,
        },
        'bookmarks': [
            {'id': b.id, 'topic_id': b.topic.id, 'title': b.topic.title, 'slug': b.topic.slug, 'created_at': b.created_at}
            for b in bookmarks
        ],
        'completed_topics': [
            {'topic_id': c.topic.id, 'title': c.topic.title, 'slug': c.topic.slug, 'last_read_at': c.last_read_at}
            for c in completed_records
        ],
        'recent_activity': [
            {'topic_id': p.topic.id, 'title': p.topic.title, 'slug': p.topic.slug, 'is_completed': p.is_completed, 'last_read_at': p.last_read_at}
            for p in recent_progress
        ],
        'quiz_attempts': [
            {
                'id': a.id,
                'quiz_id': a.quiz.id,
                'quiz_title': a.quiz.title,
                'topic_title': a.quiz.topic.title,
                'topic_slug': a.quiz.topic.slug,
                'score': a.score,
                'total_questions': a.total_questions,
                'percentage': round((a.score / a.total_questions) * 100) if a.total_questions else 0,
                'attempted_at': a.attempted_at,
            }
            for a in attempts
        ],
        'suggested_next': suggested,
    })


@api_view(['GET'])
def user_bookmarks_list(request):
    if not request.user.is_authenticated:
        return public_json({'error': {'code': 'auth_required', 'message': 'Sign in to view your bookmarks.'}}, 401)
    from .models import Bookmark
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('topic').order_by('-created_at')
    return public_json([
        {'id': b.id, 'topic_id': b.topic.id, 'title': b.topic.title, 'slug': b.topic.slug, 'created_at': b.created_at}
        for b in bookmarks
    ])


@api_view(['GET'])
def user_progress_list(request):
    if not request.user.is_authenticated:
        return public_json({'error': {'code': 'auth_required', 'message': 'Sign in to view your study progress.'}}, 401)
    from .models import UserProgress
    records = UserProgress.objects.filter(user=request.user).select_related('topic').order_by('-last_read_at')
    return public_json([
        {'id': p.id, 'topic_id': p.topic.id, 'title': p.topic.title, 'slug': p.topic.slug, 'is_completed': p.is_completed, 'last_read_at': p.last_read_at}
        for p in records
    ])


@api_view(['POST'])
@csrf_protect
def topic_bookmark(request, slug):
    if not request.user.is_authenticated:
        return public_json({'error': {'code': 'auth_required', 'message': 'Sign in to bookmark topics.'}}, 401)
    from .models import Bookmark, Topic
    topic = Topic.objects.filter(slug=slug).first()
    if not topic:
        pubs = visible_publications()
        pub = next((p for p in pubs.values() if p.snapshot.get('slug') == slug), None)
        if pub:
            topic = Topic.objects.filter(pk=pub.topic_id).first()
    if not topic:
        raise ServiceError('topic_not_found', 'Topic not found.', 404)
    bm = Bookmark.objects.filter(user=request.user, topic=topic).first()
    if bm:
        bm.delete()
        is_bookmarked = False
    else:
        Bookmark.objects.create(user=request.user, topic=topic)
        is_bookmarked = True
    return public_json({'is_bookmarked': is_bookmarked, 'topic_id': topic.id, 'slug': slug})


@api_view(['POST'])
@csrf_protect
def topic_progress(request, slug):
    if not request.user.is_authenticated:
        return public_json({'error': {'code': 'auth_required', 'message': 'Sign in to track progress.'}}, 401)
    from .models import UserProgress, Topic
    topic = Topic.objects.filter(slug=slug).first()
    if not topic:
        pubs = visible_publications()
        pub = next((p for p in pubs.values() if p.snapshot.get('slug') == slug), None)
        if pub:
            topic = Topic.objects.filter(pk=pub.topic_id).first()
    if not topic:
        raise ServiceError('topic_not_found', 'Topic not found.', 404)
    prog, created = UserProgress.objects.get_or_create(user=request.user, topic=topic)
    if 'is_completed' in request.data:
        prog.is_completed = bool(request.data['is_completed'])
    else:
        prog.is_completed = not prog.is_completed
    prog.save()
    return public_json({'is_completed': prog.is_completed, 'topic_id': topic.id, 'slug': slug})


@api_view(['POST'])
@csrf_protect
def topic_quiz_submit(request, slug):
    if not request.user.is_authenticated:
        return public_json({'error': {'code': 'auth_required', 'message': 'Sign in to record your quiz attempt.'}}, 401)
    resolve_publication(slug)
    try:
        result = check_answers(slug, request.data)
        from .models import Quiz, QuizAttempt
        quiz = Quiz.objects.get(pk=result['quiz_id'])
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=result['score'],
            total_questions=result['total']
        )
        incorrect_ids = [r['question_id'] for r in result['results'] if not r['is_correct']]
        if incorrect_ids:
            attempt.incorrect_questions.set(incorrect_ids)
        result['attempt_id'] = attempt.pk
        return public_json(result)
    except QuizServiceError as error:
        return public_json(error.payload, error.status)



@api_view(['GET'])
def profile_weaknesses(request):
    if not request.user.is_authenticated:
        return public_json({'error': {'code': 'auth_required', 'message': 'Sign in to view learning weaknesses.'}}, 401)
    from .models import QuizAttempt
    attempts = QuizAttempt.objects.filter(user=request.user).select_related('quiz', 'quiz__topic').order_by('-attempted_at')
    weakness_map = {}
    for att in attempts:
        for q in att.incorrect_questions.all():
            topic_id = att.quiz.topic_id
            weakness_map[topic_id] = weakness_map.get(topic_id, 0) + 1
    return public_json({'weaknesses': weakness_map, 'total_attempts': attempts.count()})



def discovery_page_number(request):
    values = request.query_params.getlist('page')
    value = values[0] if values else '1'
    if len(values) > 1 or len(value) > 3 or not value.isascii() or not value.isdecimal() or not 1 <= int(value) <= 250:
        raise ServiceError('invalid_page', 'Choose a page between 1 and 250.')
    return int(value)


@api_view(['GET'])
def tag_discovery(request, slug):
    from .services.discovery import tag_page
    return public_json(tag_page(slug, visible_publications(), discovery_page_number(request)))


@api_view(['GET'])
def practice_collection(request, slug):
    from .services.practice import preview
    return public_json(preview(slug, discovery_page_number(request)))


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_protect
def practice_collection_check(request, slug):
    from .services.practice import check
    try: return public_json(check(slug, request.data))
    except QuizServiceError as error: return public_json(error.payload, error.status)


@api_view(['GET'])
def topic_context(request, slug):
    from .services.discovery import article_card, description
    pub, publications = resolve_publication(slug)
    return public_json({**article_card(pub, publications), 'description': description(pub)})
