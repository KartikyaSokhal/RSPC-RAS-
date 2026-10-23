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
    response = public_json({'demo': settings.DEMO_MODE, 'ai_enabled': settings.AI_ENABLED and (settings.AI_GUEST_ENABLED or request.user.is_authenticated),
                            'support_email': settings.SUPPORT_EMAIL, 'student_features_enabled': settings.STUDENT_FEATURES_ENABLED, 'google_signin_enabled': bool(settings.STUDENT_FEATURES_ENABLED and settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET and settings.GOOGLE_REDIRECT_URI), 'csrf_token': get_token(request)})
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
@permission_classes([AllowAny])
@csrf_protect
def topic_chat(request, slug):
    serializer = ChatInputSerializer(data=request.data); serializer.is_valid(raise_exception=True)
    # Check disabled configuration before lookup or quota writes.
    if not settings.AI_ENABLED or (not request.user.is_authenticated and not settings.AI_GUEST_ENABLED):
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
    response = public_json(answer(slug, serializer.validated_data, visitor_key, ip_key, authenticated=request.user.is_authenticated))
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


from .student_auth import auth_register, auth_login, auth_logout, auth_status


from .student_views import learner_dashboard


from .student_views import user_bookmarks_list, user_progress_list, topic_bookmark, topic_progress


from .student_views import topic_quiz_submit, profile_weaknesses


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
