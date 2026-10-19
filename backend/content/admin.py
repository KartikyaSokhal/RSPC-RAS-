from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.http import FileResponse, Http404
from django.utils.html import format_html
from .forms import TopicForm, ContentBlockForm, ResourceForm
from .services.publication import draft_snapshot, publish, republish_previous
from .services.resources import approve_resource
from .services.quiz import review_quiz, QuizServiceError
from .exceptions import ServiceError
from .models import TopicPublication, TopicRelation, LearningResource, ResourcePage, QuizReview
from .models import Topic, ContentBlock, Quiz, Question, Choice, Bookmark, UserProgress, QuizAttempt


class ContentBlockInline(admin.StackedInline):
    model = ContentBlock
    form = ContentBlockForm
    fields = ("block_type", "content", "file", "alt_text", "caption", "source_reference", "order")
    can_delete = False
    extra = 1
    ordering = ("order",)


class RelationInline(admin.TabularInline):
    model = TopicRelation
    fk_name = 'source'
    extra = 0
    autocomplete_fields = ('target',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    form = TopicForm
    list_display = ("title", "slug", "parent", "publication_state", "preview_link")
    actions = ["publish_selected", "withdraw_selected", "restore_previous"]
    list_filter = ("parent",)
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ContentBlockInline, RelationInline]

    def has_delete_permission(self, request, obj=None):
        return False

    def publication_state(self, obj):
        pub = TopicPublication.objects.filter(topic=obj).first()
        return f"Published · revision {pub.revision}" if pub and pub.is_published else "Draft / withdrawn"

    def preview_link(self, obj):
        return format_html('<a href="{}">Preview draft</a>', reverse('admin:content_topic_preview', args=[obj.pk]))

    def get_urls(self):
        return [path('<int:pk>/preview/', self.admin_site.admin_view(self.preview), name='content_topic_preview'),
                path('<int:pk>/draft-image/<int:block_id>/', self.admin_site.admin_view(self.draft_image), name='content_topic_draft_image')] + super().get_urls()

    def draft_image(self, request, pk, block_id):
        topic = self.get_object(request, str(pk))
        if topic is None or not self.has_view_permission(request, topic): raise PermissionDenied
        block = topic.blocks.filter(pk=block_id, block_type='image').first()
        if not block or not block.file: raise Http404
        from .validators import validate_image
        from PIL import Image
        from django.core.exceptions import ValidationError
        try:
            stream = block.file.open('rb'); validate_image(stream)
            image = Image.open(stream); content_type = Image.MIME[image.format]; stream.seek(0)
        except (OSError, ValidationError): raise Http404 from None
        response = FileResponse(stream, content_type=content_type)
        response['Cache-Control'] = 'private, no-store'
        return response

    def preview(self, request, pk):
        topic = self.get_object(request, str(pk))
        if topic is None or not self.has_view_permission(request, topic): raise PermissionDenied
        try: snapshot = draft_snapshot(topic); error = ''
        except (ServiceError, ValueError) as exc: snapshot = {'blocks': []}; error = str(exc)
        from django.utils.safestring import mark_safe
        for block in snapshot['blocks']:
            if block['block_type'] == 'text': block['safe_html'] = mark_safe(block['content'])
            if block['block_type'] == 'image': block['preview_url'] = reverse('admin:content_topic_draft_image', args=[topic.pk, block['id']])
        return TemplateResponse(request, 'admin/content/topic/preview.html', {
            **self.admin_site.each_context(request), 'title': f'Draft preview: {topic.title}', 'topic': topic, 'snapshot': snapshot, 'error': error,
        })

    @admin.action(description='Publish selected topics after editorial review', permissions=['change'])
    def publish_selected(self, request, queryset):
        for topic in queryset.order_by('pk'):
            try: publish(topic, request.user); self.log_change(request, topic, 'Published reviewed snapshot'); self.message_user(request, f'Published {topic.title}')
            except (ServiceError, ValueError) as exc: self.message_user(request, str(exc), level='ERROR')

    @admin.action(description='Withdraw selected topics (preserve all content)', permissions=['change'])
    def withdraw_selected(self, request, queryset):
        TopicPublication.objects.filter(topic__in=queryset).update(is_published=False)
        for topic in queryset: self.log_change(request, topic, 'Withdrew publication')
        self.message_user(request, 'Selected publications withdrawn, including public access to descendants.')

    @admin.action(description='Republish previous approved snapshot', permissions=['change'])
    def restore_previous(self, request, queryset):
        for pub in TopicPublication.objects.filter(topic__in=queryset):
            try: republish_previous(pub, request.user); self.log_change(request, pub.topic, 'Republished previous reviewed snapshot')
            except ServiceError as exc: self.message_user(request, str(exc), level='ERROR')


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    form = ContentBlockForm

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ("topic", "block_type", "order")
    list_filter = ("block_type", "topic")
    search_fields = ("topic__title",)
    ordering = ("topic", "order")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.topic and TopicPublication.objects.filter(topic=obj.topic, is_published=True).exists():
            try:
                publish(obj.topic, request.user)
            except Exception:
                pass


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "quiz")
    search_fields = ("question_text",)
    inlines = [ChoiceInline]


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "time_limit_seconds")
    list_filter = ("topic",)
    search_fields = ("title", "topic__title")
    inlines = [QuestionInline]


class UnavailableLearnerAdmin(admin.ModelAdmin):
    """P002 also blocks direct Admin URLs, including superusers, without deleting rows."""
    def get_queryset(self, request):
        return super().get_queryset(request).none()

    def history_view(self, request, object_id, extra_context=None):
        # Django otherwise redirects a missing queryset object before permission checks.
        raise PermissionDenied

    def has_module_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Bookmark)
class BookmarkAdmin(UnavailableLearnerAdmin):
    list_display = ("topic", "user", "created_at")


@admin.register(UserProgress)
class UserProgressAdmin(UnavailableLearnerAdmin):
    list_display = ("topic", "user", "is_completed", "last_read_at")
    list_filter = ("is_completed",)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(UnavailableLearnerAdmin):
    list_display = ("quiz", "user", "score", "total_questions", "attempted_at")



@admin.register(LearningResource)
class ResourceAdmin(admin.ModelAdmin):
    form = ResourceForm
    list_display = ('title', 'topic', 'status', 'page_count', 'reviewed_at')
    list_filter = ('status', 'topic')
    search_fields = ('title', 'source_reference')
    readonly_fields = ('preview_link', 'status', 'error_code', 'sha256', 'byte_count', 'page_count', 'attempts', 'reviewed_by', 'reviewed_at')
    actions = ['approve', 'withdraw']

    def has_delete_permission(self, request, obj=None): return False

    def preview_link(self, obj):
        if not obj.pk or obj.status not in ('ready', 'approved', 'needs_ocr', 'withdrawn'): return 'Process the uploaded candidate first.'
        return format_html('<a href="{}" target="_blank" rel="noopener">Inspect private source PDF</a> · <a href="{}?resource__id__exact={}">Review extracted pages</a>',
            reverse('admin:content_resource_preview', args=[obj.pk]), reverse('admin:content_resourcepage_changelist'), obj.pk)

    def get_urls(self):
        return [path('<int:pk>/preview/', self.admin_site.admin_view(self.preview), name='content_resource_preview')] + super().get_urls()

    def preview(self, request, pk):
        from .services.resources import file_digest
        obj = self.get_object(request, str(pk))
        if obj is None or not self.has_view_permission(request, obj): raise PermissionDenied
        if obj.status not in ('ready', 'approved', 'needs_ocr', 'withdrawn'): raise Http404
        try:
            if file_digest(obj) != obj.sha256: raise Http404
            response = FileResponse(obj.file.open('rb'), content_type='application/pdf')
        except OSError: raise Http404 from None
        response['Cache-Control'] = 'private, no-store'; response['Content-Security-Policy'] = "sandbox; default-src 'none'"
        return response

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status not in ('pending', 'failed'):
            return self.readonly_fields + ('topic', 'title', 'file', 'source_reference', 'rights_note')
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.file and obj.status in ('pending', 'failed'):
            from .services.resources import process_resource, approve_resource
            try:
                process_resource(obj.pk)
                obj.refresh_from_db()
                if obj.status == 'ready':
                    approve_resource(obj, request.user)
                if obj.topic and TopicPublication.objects.filter(topic=obj.topic, is_published=True).exists():
                    publish(obj.topic, request.user)
            except Exception:
                pass

    @admin.action(description='Approve selected resources after reviewing page text and rights', permissions=['change'])
    def approve(self, request, queryset):
        for resource in queryset:
            try: approve_resource(resource, request.user); self.log_change(request, resource, 'Approved extracted PDF and rights'); self.message_user(request, f'Approved {resource.title}; publish its topic to expose it.')
            except ServiceError as exc: self.message_user(request, str(exc), level='ERROR')

    @admin.action(description='Withdraw selected resources', permissions=['change'])
    def withdraw(self, request, queryset):
        for resource in queryset: self.log_change(request, resource, 'Withdrew resource')
        queryset.update(status='withdrawn')
        self.message_user(request, 'Resources withdrawn from viewing, search and tutor retrieval.')


@admin.register(ResourcePage)
class ResourcePageAdmin(admin.ModelAdmin):
    list_display = ('resource', 'page_number')
    list_filter = ('resource',)
    search_fields = ('text',)
    readonly_fields = ('resource', 'page_number', 'text', 'text_sha256')

    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False


@admin.register(QuizReview)
class QuizReviewAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'is_approved', 'reviewed_at', 'reviewed_by')
    fields = ('quiz', 'source_reference', 'is_approved', 'fingerprint', 'reviewed_by', 'reviewed_at')
    readonly_fields = ('is_approved', 'fingerprint', 'reviewed_by', 'reviewed_at')
    actions = ['approve', 'revoke']

    def has_delete_permission(self, request, obj=None): return False

    @admin.action(description='Approve selected quiz reviews after checking all answers and sources', permissions=['change'])
    def approve(self, request, queryset):
        for record in queryset:
            try: review_quiz(record.quiz, request.user, record.source_reference); self.message_user(request, 'Quiz reviewed. Later content changes invalidate this approval.')
            except QuizServiceError as exc: self.message_user(request, exc.message, level='ERROR')

    @admin.action(description='Revoke quiz approval', permissions=['change'])
    def revoke(self, request, queryset): queryset.update(is_approved=False)


admin.site.site_header = 'Prepal · Content studio'
admin.site.site_title = 'Prepal Admin'
admin.site.index_title = 'Author, review and publish'
