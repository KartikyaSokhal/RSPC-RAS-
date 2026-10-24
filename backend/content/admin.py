import types
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.core.exceptions import PermissionDenied
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.http import FileResponse, Http404, HttpResponseRedirect
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.db.models import Count

from .forms import TopicForm, ContentBlockForm, ResourceForm, TopicResourceInlineForm, QuestionForm
from .services.publication import draft_snapshot, publish, republish_previous
from .services.resources import approve_resource, process_resource
from .services.quiz import review_quiz, QuizServiceError, is_reviewable, quiz_fingerprint
from .exceptions import ServiceError
from .models import TopicPublication, TopicRelation, LearningResource, ResourcePage, QuizReview, Tag, TopicAlias, KeywordLinkProposal, ConnectionScan
from .models import Topic, ContentBlock, Quiz, Question, Choice, Bookmark, UserProgress, QuizAttempt


def preparation_feedback(model_admin, request, resource):
    if resource.status == 'ready':
        message, level = 'PDF prepared. Review text and rights, approve, then publish its topic.', 'SUCCESS'
    elif resource.status in ('failed', 'needs_ocr'):
        message, level = 'PDF could not be prepared for approval. Inspect its processing state; it remains private.', 'ERROR'
    else:
        message, level = 'PDF is awaiting preparation and explicit review; it remains private.', 'WARNING'
    model_admin.message_user(request, message, level=level, fail_silently=True)


class ContentBlockInline(admin.StackedInline):
    model = ContentBlock
    form = ContentBlockForm
    fields = ("order", "block_type", "content", "file", "alt_text", "caption", "source_reference")
    can_delete = True
    extra = 1
    ordering = ("order",)


class LearningResourceInline(admin.StackedInline):
    """Allows uploading and inspecting PDF resources directly inside Topic editing."""
    model = LearningResource
    form = TopicResourceInlineForm
    fields = ("title", "file", "source_reference", "rights_note", "status_display")
    readonly_fields = ("status_display",)
    extra = 0

    def status_display(self, obj):
        if not obj or not obj.pk:
            return "Will process automatically upon saving."
        if obj.status == 'ready':
            return mark_safe('<span class="prepal-badge badge-draft">Ready · awaiting explicit review</span>')
        if obj.status == 'approved':
            return format_html('<span class="prepal-badge badge-published">✓ Approved ({})</span>', obj.status)
        if obj.status == 'failed':
            return format_html('<span class="prepal-badge badge-unreviewed">⚠️ Failed ({})</span>', obj.error_code or 'error')
        return format_html('<span class="prepal-badge badge-draft">⏳ {}</span>', obj.status)
    status_display.short_description = "Processing & Approval State"


class RelationInline(admin.TabularInline):
    model = TopicRelation
    fk_name = 'source'
    extra = 0
    autocomplete_fields = ('target',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_public')
    list_filter = ('is_public',)
    search_fields = ('name', 'normalized_name', 'slug')
    readonly_fields = ('normalized_name',)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TopicAlias)
class TopicAliasAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'topic__title')
    autocomplete_fields = ('topic',)
    readonly_fields = ('normalized_name',)

    def has_delete_permission(self, request, obj=None):
        return False


    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        from .services.connections import process_pending
        process_pending()
        pending = ConnectionScan.objects.filter(pending=True, publication__is_published=True).count()
        self.message_user(request, f'Alias saved. Published articles rechecked in a bounded batch; {pending} scans remain queued. Review new proposals before links become active.')


@admin.register(KeywordLinkProposal)
class KeywordLinkProposalAdmin(admin.ModelAdmin):
    list_display = ('phrase', 'source', 'target', 'context', 'status', 'source_revision')
    list_filter = ('status', 'source')
    search_fields = ('phrase', 'source__title', 'target__title')
    readonly_fields = ('source', 'target', 'phrase', 'phrase_key', 'context', 'source_hash', 'source_revision', 'occurrences', 'status', 'reviewed_by', 'reviewed_at')
    actions = ['approve_connections', 'reject_connections']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def review(self, request, queryset, status):
        from .services.connections import decide, vocabulary, refresh_link_plan
        from .services.publication import visible_publications
        pubs = visible_publications(); terms = vocabulary(pubs); affected = set()
        for proposal in queryset.select_related('source', 'target').order_by('pk'):
            try:
                decide(proposal, status, request.user, publications=pubs, terms=terms, refresh=False)
                affected.add(proposal.source_id)
                self.log_change(request, proposal, f'Keyword connection {status}')
                self.message_user(request, f'Connection {status}: {proposal.phrase}')
            except ServiceError as exc:
                self.message_user(request, str(exc), level='ERROR')

        for topic_id in affected:
            if topic_id in pubs: refresh_link_plan(pubs[topic_id], pubs)

    @admin.action(description='Approve selected phrase connections', permissions=['change'])
    def approve_connections(self, request, queryset):
        self.review(request, queryset, 'approved')

    @admin.action(description='Reject selected phrase connections', permissions=['change'])
    def reject_connections(self, request, queryset):
        self.review(request, queryset, 'rejected')


@admin.register(TopicRelation)
class TopicRelationAdmin(admin.ModelAdmin):
    list_display = ('source', 'target', 'kind', 'status')
    list_filter = ('kind', 'status')
    search_fields = ('source__title', 'target__title', 'reason')
    autocomplete_fields = ('source', 'target')

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    form = TopicForm
    change_form_template = 'admin/content/topic/change_form.html'
    change_list_template = 'admin/content/topic/change_list.html'

    list_display = ("title", "slug", "parent", "publication_state_badge", "content_overview", "preview_link")
    actions = ["publish_selected", "withdraw_selected", "restore_previous", "suggest_connections"]
    list_filter = ("editorial_status", "parent")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ContentBlockInline, LearningResourceInline, RelationInline]
    filter_horizontal = ("tags",)
    exclude = ("editorial_status",)

    def has_delete_permission(self, request, obj=None):
        # Safeguard against accidental topic deletion
        return False

    def publication_state(self, obj):
        """Preserved for backward compatibility."""
        pub = TopicPublication.objects.filter(topic=obj).first()
        return f"Published · revision {pub.revision}" if pub and pub.is_published else obj.get_editorial_status_display()

    def publication_state_badge(self, obj):
        pub = TopicPublication.objects.filter(topic=obj).first()
        if pub and pub.is_published:
            if obj.editorial_status == 'in_review':
                return format_html('<span class="prepal-badge badge-draft">Published · v{} · Awaiting review</span>', pub.revision)
            return format_html('<span class="prepal-badge badge-published">🟢 Published · v{}</span>', pub.revision)
        if obj.editorial_status == "in_review":
            return format_html('<span class="prepal-badge badge-draft">{}</span>', "Awaiting review")
        if obj.blocks.exists():
            return mark_safe('<span class="prepal-badge badge-draft">🟡 Draft</span>')
        return mark_safe('<span class="prepal-badge badge-unreviewed">⚪ Empty</span>')
    publication_state_badge.short_description = "Status"

    def content_overview(self, obj):
        b_count = obj.blocks.count()
        r_count = obj.resources.count()
        parts = [f"{b_count} notes"]
        if r_count:
            parts.append(f"{r_count} PDF{'s' if r_count != 1 else ''}")
        return " · ".join(parts)
    content_overview.short_description = "Content"

    def preview_link(self, obj):
        return format_html('<a href="{}" target="_blank" class="button">Preview draft</a>', reverse('admin:content_topic_preview', args=[obj.pk]))

    def get_urls(self):
        return [
            path('tree/', self.admin_site.admin_view(self.tree_view), name='content_topic_tree'),
            path('<int:pk>/preview/', self.admin_site.admin_view(self.preview), name='content_topic_preview'),
            path('<int:pk>/draft-image/<int:block_id>/', self.admin_site.admin_view(self.draft_image), name='content_topic_draft_image'),
        ] + super().get_urls()

    def tree_view(self, request):
        if not self.has_view_permission(request):
            raise PermissionDenied
        """Interactive Syllabus Tree Explorer for 152 topics."""
        topics = list(Topic.objects.all().order_by('order', 'title'))
        pubs = {p.topic_id: p for p in TopicPublication.objects.all()}
        b_counts = dict(ContentBlock.objects.values('topic_id').annotate(c=Count('id')).values_list('topic_id', 'c'))
        r_counts = dict(LearningResource.objects.values('topic_id').annotate(c=Count('id')).values_list('topic_id', 'c'))
        q_topics = set(Quiz.objects.values_list('topic_id', flat=True))

        nodes = {}
        for t in topics:
            pub = pubs.get(t.pk)
            nodes[t.pk] = {
                'id': t.pk,
                'title': t.title,
                'slug': t.slug,
                'parent_id': t.parent_id,
                'is_published': bool(pub and pub.is_published),
                'revision': pub.revision if pub else 1,
                'block_count': b_counts.get(t.pk, 0),
                'resource_count': r_counts.get(t.pk, 0),
                'has_quiz': t.pk in q_topics,
                'edit_url': reverse('admin:content_topic_change', args=[t.pk]),
                'preview_url': reverse('admin:content_topic_preview', args=[t.pk]),
                'add_child_url': reverse('admin:content_topic_add') + f'?parent={t.pk}',
                'children': [],
            }

        tree_data = []
        for t in topics:
            node = nodes[t.pk]
            if t.parent_id and t.parent_id in nodes:
                nodes[t.parent_id]['children'].append(node)
            else:
                tree_data.append(node)

        context = {
            **self.admin_site.each_context(request),
            'title': 'Syllabus Hierarchy Explorer',
            'tree_data': tree_data,
            'total_topics': len(topics),
        }
        return TemplateResponse(request, 'admin/content/topic/tree.html', context)

    def draft_image(self, request, pk, block_id):
        topic = self.get_object(request, str(pk))
        if topic is None or not self.has_view_permission(request, topic):
            raise PermissionDenied
        block = topic.blocks.filter(pk=block_id, block_type='image').first()
        if not block or not block.file:
            raise Http404
        from .validators import validate_image
        from PIL import Image
        from django.core.exceptions import ValidationError
        try:
            stream = block.file.open('rb')
            validate_image(stream)
            image = Image.open(stream)
            content_type = Image.MIME[image.format]
            stream.seek(0)
        except (OSError, ValidationError):
            raise Http404 from None
        response = FileResponse(stream, content_type=content_type)
        response['Cache-Control'] = 'private, no-store'
        return response

    def preview(self, request, pk):
        topic = self.get_object(request, str(pk))
        if topic is None or not self.has_view_permission(request, topic):
            raise PermissionDenied
        try:
            snapshot = draft_snapshot(topic)
            error = ''
        except (ServiceError, ValueError) as exc:
            snapshot = {'blocks': []}
            error = str(exc)
        from django.utils.safestring import mark_safe
        for block in snapshot['blocks']:
            if block['block_type'] == 'text':
                block['safe_html'] = mark_safe(block['content'])
            if block['block_type'] == 'image':
                block['preview_url'] = reverse('admin:content_topic_draft_image', args=[topic.pk, block['id']])
        return TemplateResponse(request, 'admin/content/topic/preview.html', {
            **self.admin_site.each_context(request),
            'title': f'Draft preview: {topic.title}',
            'topic': topic,
            'snapshot': snapshot,
            'error': error,
        })

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            obj = self.get_object(request, object_id)
            if obj and request.method == 'POST' and self.has_change_permission(request, obj):
                if '_submit_review' in request.POST and 'title' not in request.POST:
                    self.submit_review(request, obj)
                    return HttpResponseRedirect(request.path)
                if '_publish_now' in request.POST and not any(k.startswith('title') for k in request.POST):
                    try:
                        pub = publish(obj, request.user)
                        self.log_change(request, obj, f'Published live snapshot (revision {pub.revision})')
                        self.message_user(request, f"🚀 Published '{obj.title}' (Revision {pub.revision}) to the live platform!")
                    except (ServiceError, ValueError) as exc:
                        self.message_user(request, f"Publication error: {exc}", level='ERROR')
                    return HttpResponseRedirect(request.path)

                if '_withdraw_now' in request.POST and not any(k.startswith('title') for k in request.POST):
                    TopicPublication.objects.filter(topic=obj).update(is_published=False)
                    self.log_change(request, obj, 'Withdrew publication')
                    self.message_user(request, f"Publication withdrawn for '{obj.title}'. It is now saved as draft only.")
                    return HttpResponseRedirect(request.path)

                if '_restore_previous' in request.POST and not any(k.startswith('title') for k in request.POST):
                    pub = TopicPublication.objects.filter(topic=obj).first()
                    if pub:
                        try:
                            republish_previous(pub, request.user)
                            self.log_change(request, obj, 'Republished previous reviewed snapshot')
                            self.message_user(request, f"Restored previous approved snapshot for '{obj.title}'.")
                        except ServiceError as exc:
                            self.message_user(request, str(exc), level='ERROR')
                    return HttpResponseRedirect(request.path)

            pub = TopicPublication.objects.filter(topic_id=object_id).first()
            extra_context['publication_info'] = {
                'is_published': bool(pub and pub.is_published),
                'revision': pub.revision if pub else 1,
                'has_previous': bool(pub and pub.previous_snapshot),
            }
        return super().changeform_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        if "_submit_review" in request.POST:
            self.submit_review(request, obj)
            return HttpResponseRedirect(request.path)
        if '_publish_now' in request.POST:
            try:
                pub = publish(obj, request.user)
                self.log_change(request, obj, f'Published live snapshot (revision {pub.revision})')
                self.message_user(request, f"🚀 Published '{obj.title}' (Revision {pub.revision}) to the live platform!")
            except (ServiceError, ValueError) as exc:
                self.message_user(request, f"Publication error: {exc}", level='ERROR')
            return HttpResponseRedirect(request.path)

        if '_withdraw_now' in request.POST:
            TopicPublication.objects.filter(topic=obj).update(is_published=False)
            self.log_change(request, obj, 'Withdrew publication')
            self.message_user(request, f"Publication withdrawn for '{obj.title}'. It is now saved as draft only.")
            return HttpResponseRedirect(request.path)

        if '_restore_previous' in request.POST:
            pub = TopicPublication.objects.filter(topic=obj).first()
            if pub:
                try:
                    republish_previous(pub, request.user)
                    self.log_change(request, obj, 'Republished previous reviewed snapshot')
                    self.message_user(request, f"Restored previous approved snapshot for '{obj.title}'.")
                except ServiceError as exc:
                    self.message_user(request, str(exc), level='ERROR')
            return HttpResponseRedirect(request.path)

        return super().response_change(request, obj)

    def submit_review(self, request, obj):
        Topic.objects.filter(pk=obj.pk).update(editorial_status="in_review")
        self.log_change(request, obj, "Submitted draft for editorial review")
        self.message_user(request, "Draft submitted for review. Public content is unchanged.")

    def save_model(self, request, obj, form, change):
        obj.editorial_status = "draft"
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # Check newly uploaded or pending learning resources and process them
        for res in form.instance.resources.filter(status='pending'):
            if res.file:
                try:
                    process_resource(res.pk)
                    res.refresh_from_db()
                    preparation_feedback(self, request, res)
                except Exception:
                    self.message_user(request, "PDF preparation failed. The candidate remains private; inspect the resource before retrying.", level="ERROR", fail_silently=True)

    @admin.action(description='Suggest Connections', permissions=['change'])
    def suggest_connections(self, request, queryset):
        from .services.connections import suggest_connections
        for topic in queryset.order_by('pk'):
            try:
                count = suggest_connections(topic)
                self.message_user(request, f'{count} connection proposals for {topic.title}. Review each phrase, target and context in Keyword link proposals. Existing decisions were preserved.')
            except ServiceError as exc:
                self.message_user(request, str(exc), level='ERROR')

    @admin.action(description='Publish selected topics after editorial review', permissions=['change'])
    def publish_selected(self, request, queryset):
        for topic in queryset.order_by('pk'):
            try:
                publish(topic, request.user)
                self.log_change(request, topic, 'Published reviewed snapshot')
                self.message_user(request, f'Published {topic.title}')
            except (ServiceError, ValueError) as exc:
                self.message_user(request, str(exc), level='ERROR')

    @admin.action(description='Withdraw selected topics (preserve all content)', permissions=['change'])
    def withdraw_selected(self, request, queryset):
        TopicPublication.objects.filter(topic__in=queryset).update(is_published=False)
        for topic in queryset:
            self.log_change(request, topic, 'Withdrew publication')
        self.message_user(request, 'Selected publications withdrawn, including public access to descendants.')

    @admin.action(description='Republish previous approved snapshot', permissions=['change'])
    def restore_previous(self, request, queryset):
        for pub in TopicPublication.objects.filter(topic__in=queryset):
            try:
                republish_previous(pub, request.user)
                self.log_change(request, pub.topic, 'Republished previous reviewed snapshot')
            except ServiceError as exc:
                self.message_user(request, str(exc), level='ERROR')


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    form = ContentBlockForm
    autocomplete_fields = ("topic",)

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ("topic", "block_type", "order")
    list_filter = ("block_type", "topic")
    search_fields = ("topic__title",)
    ordering = ("topic", "order")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        Topic.objects.filter(pk=obj.topic_id).update(editorial_status="draft")
        self.message_user(request, "Content saved as draft. Preview and publish from its topic after review.")


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class SyllabusCollectionFilter(admin.SimpleListFilter):
    title = 'Syllabus question collection'
    parameter_name = 'collection'

    def lookups(self, request, model_admin):
        return list(Topic.objects.order_by('title').values_list('pk', 'title'))

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if not self.value().isascii() or not self.value().isdecimal() or len(self.value()) > 16:
            return queryset.none()
        topic = Topic.objects.filter(pk=self.value()).first()
        if topic is None:
            return queryset.none()
        from .services.collections import question_collection
        try:
            return queryset.filter(pk__in=question_collection(topic, reviewed_only=False).values('pk'))
        except ServiceError:
            return queryset.none()


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm
    autocomplete_fields = ("quiz", "primary_topic", "related_topics", "tags")
    list_filter = (SyllabusCollectionFilter, "primary_topic", "tags")
    list_display = ("question_text", "quiz", "choices_summary", "has_explanation")
    search_fields = ("question_text", "quiz__title")
    inlines = [ChoiceInline]

    def has_delete_permission(self, request, obj=None):
        return False

    def choices_summary(self, obj):
        total = obj.choices.count()
        correct = obj.choices.filter(is_correct=True).count()
        return f"{total} choices ({correct} correct)"
    choices_summary.short_description = "Choices"

    def has_explanation(self, obj):
        return bool(obj.explanation and obj.explanation.strip())
    has_explanation.boolean = True
    has_explanation.short_description = "Explanation"


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    form = QuestionForm
    fields = ('question_text', 'explanation', 'primary_topic', 'related_topics', 'tags', 'edit_choices_link')
    autocomplete_fields = ("primary_topic", "related_topics", "tags")
    readonly_fields = ('edit_choices_link',)

    def edit_choices_link(self, obj):
        if obj and obj.pk:
            url = reverse('admin:content_question_change', args=[obj.pk])
            count = obj.choices.count()
            has_correct = obj.choices.filter(is_correct=True).exists()
            status = "✓ Correct marked" if has_correct else "⚠️ No correct choice"
            return format_html('<a href="{}" target="_blank" class="button">Edit 4 Choices ({} choices, {})</a>', url, count, status)
        return "Save quiz to add/edit choices"
    edit_choices_link.short_description = "MCQ Choices"


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    change_form_template = 'admin/content/quiz/change_form.html'
    list_display = ("title", "topic", "question_count_display", "time_limit_seconds", "approval_badge", "quick_actions")
    list_filter = ("topic",)
    search_fields = ("title", "topic__title")
    inlines = [QuestionInline]
    actions = ["approve_selected", "revoke_selected"]

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def question_count_display(self, obj):
        return obj.questions.count()
    question_count_display.short_description = "Questions"

    def approval_badge(self, obj):
        is_app = False
        if is_reviewable(obj) and QuizReview.objects.filter(quiz=obj, is_approved=True, fingerprint=quiz_fingerprint(obj)).exists():
            is_app = True
        if is_app:
            return mark_safe('<span class="prepal-badge badge-published">🟢 Approved & Live</span>')
        return mark_safe('<span class="prepal-badge badge-unreviewed">🟡 Unreviewed Draft</span>')
    approval_badge.short_description = "Student Access"

    def quick_actions(self, obj):
        return format_html('<a href="{}" class="button">Edit & Review</a>', reverse('admin:content_quiz_change', args=[obj.pk]))
    quick_actions.short_description = "Actions"

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        is_app = False
        if object_id:
            obj = self.get_object(request, object_id)
            if obj and request.method == 'POST' and self.has_change_permission(request, obj):
                if '_approve_quiz' in request.POST and not any(k.startswith('title') for k in request.POST):
                    try:
                        review = review_quiz(obj, request.user, "Approved educational review")
                        self.message_user(request, f"✓ Successfully approved and published quiz '{obj.title}'! It is now live for students.")
                    except QuizServiceError as exc:
                        self.message_user(request, f"Approval rejected: {exc.message}", level='ERROR')
                    return HttpResponseRedirect(request.path)

                if '_revoke_quiz' in request.POST and not any(k.startswith('title') for k in request.POST):
                    QuizReview.objects.filter(quiz=obj).update(is_approved=False)
                    self.message_user(request, f"Approval revoked for quiz '{obj.title}'. It is now hidden from students.")
                    return HttpResponseRedirect(request.path)

            quiz = obj or Quiz.objects.filter(pk=object_id).first()
            if quiz and is_reviewable(quiz) and QuizReview.objects.filter(quiz=quiz, is_approved=True, fingerprint=quiz_fingerprint(quiz)).exists():
                is_app = True
        extra_context['quiz_approved'] = is_app
        return super().changeform_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        if '_approve_quiz' in request.POST:
            try:
                review = review_quiz(obj, request.user, "Approved educational review")
                self.message_user(request, f"✓ Successfully approved and published quiz '{obj.title}'! It is now live for students.")
            except QuizServiceError as exc:
                self.message_user(request, f"Approval rejected: {exc.message}", level='ERROR')
            return HttpResponseRedirect(request.path)

        if '_revoke_quiz' in request.POST:
            QuizReview.objects.filter(quiz=obj).update(is_approved=False)
            self.message_user(request, f"Approval revoked for quiz '{obj.title}'. It is now hidden from students.")
            return HttpResponseRedirect(request.path)

        return super().response_change(request, obj)

    @admin.action(description='Approve selected quizzes after reviewing all choices and explanations', permissions=['change'])
    def approve_selected(self, request, queryset):
        for quiz in queryset:
            try:
                review_quiz(quiz, request.user, "Approved educational review")
                self.message_user(request, f"Approved {quiz.title}")
            except QuizServiceError as exc:
                self.message_user(request, f"Could not approve {quiz.title}: {exc.message}", level='ERROR')

    @admin.action(description='Revoke approval for selected quizzes (hide from students)', permissions=['change'])
    def revoke_selected(self, request, queryset):
        QuizReview.objects.filter(quiz__in=queryset).update(is_approved=False)
        self.message_user(request, f"Revoked approval for {queryset.count()} quiz(zes).")


class UnavailableLearnerAdmin(admin.ModelAdmin):
    """P002 blocks direct Admin URLs, including superusers, without deleting rows."""
    def get_queryset(self, request):
        return super().get_queryset(request).none()

    def history_view(self, request, object_id, extra_context=None):
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

    def has_delete_permission(self, request, obj=None):
        return False

    def preview_link(self, obj):
        if not obj.pk or obj.status not in ('ready', 'approved', 'needs_ocr', 'withdrawn'):
            return 'Process the uploaded candidate first.'
        return format_html('<a href="{}" target="_blank" rel="noopener">Inspect private source PDF</a> · <a href="{}?resource__id__exact={}">Review extracted pages</a>',
            reverse('admin:content_resource_preview', args=[obj.pk]), reverse('admin:content_resourcepage_changelist'), obj.pk)

    def get_urls(self):
        return [path('<int:pk>/preview/', self.admin_site.admin_view(self.preview), name='content_resource_preview')] + super().get_urls()

    def preview(self, request, pk):
        from .services.resources import file_digest
        obj = self.get_object(request, str(pk))
        if obj is None or not self.has_view_permission(request, obj):
            raise PermissionDenied
        if obj.status not in ('ready', 'approved', 'needs_ocr', 'withdrawn'):
            raise Http404
        try:
            if file_digest(obj) != obj.sha256:
                raise Http404
            response = FileResponse(obj.file.open('rb'), content_type='application/pdf')
        except OSError:
            raise Http404 from None
        response['Cache-Control'] = 'private, no-store'
        response['Content-Security-Policy'] = "sandbox; default-src 'none'"
        return response

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status not in ('pending', 'failed'):
            return self.readonly_fields + ('topic', 'title', 'file', 'source_reference', 'rights_note')
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.file and obj.status in ('pending', 'failed'):
            from .services.resources import process_resource
            try:
                process_resource(obj.pk)
                obj.refresh_from_db()
                preparation_feedback(self, request, obj)
            except Exception:
                self.message_user(request, "PDF preparation failed. The candidate remains private; inspect the resource before retrying.", level="ERROR", fail_silently=True)

    @admin.action(description='Approve selected resources after reviewing page text and rights', permissions=['change'])
    def approve(self, request, queryset):
        for resource in queryset:
            try:
                approve_resource(resource, request.user)
                self.log_change(request, resource, 'Approved extracted PDF and rights')
                self.message_user(request, f'Approved {resource.title}; publish its topic to expose it.')
            except ServiceError as exc:
                self.message_user(request, str(exc), level='ERROR')

    @admin.action(description='Withdraw selected resources', permissions=['change'])
    def withdraw(self, request, queryset):
        for resource in queryset:
            self.log_change(request, resource, 'Withdrew resource')
        queryset.update(status='withdrawn')
        self.message_user(request, 'Resources withdrawn from viewing, search and tutor retrieval.')


@admin.register(ResourcePage)
class ResourcePageAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ('resource', 'page_number')
    list_filter = ('resource',)
    search_fields = ('text',)
    readonly_fields = ('resource', 'page_number', 'text', 'text_sha256')

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(QuizReview)
class QuizReviewAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    list_display = ('quiz', 'is_approved', 'reviewed_at', 'reviewed_by')
    fields = ('quiz', 'source_reference', 'is_approved', 'fingerprint', 'reviewed_by', 'reviewed_at')
    readonly_fields = ('is_approved', 'fingerprint', 'reviewed_by', 'reviewed_at')
    actions = ['approve', 'revoke']

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description='Approve selected quiz reviews after checking all answers and sources', permissions=['change'])
    def approve(self, request, queryset):
        for record in queryset:
            try:
                review_quiz(record.quiz, request.user, record.source_reference)
                self.message_user(request, 'Quiz reviewed. Later content changes invalidate this approval.')
            except QuizServiceError as exc:
                self.message_user(request, exc.message, level='ERROR')

    @admin.action(description='Revoke quiz approval', permissions=['change'])
    def revoke(self, request, queryset):
        queryset.update(is_approved=False)


# =========================================================================
# Section 3: Students Management & Progress Reporting
# =========================================================================

class StudentUserAdmin(UserAdmin):
    """
    Simplified, client-friendly Student Management interface for the educational business owner.
    Provides read-only progress reports and protects student personal data.
    """
    list_display = (
        "username", "email", "date_joined", "last_login",
        "is_staff", "is_active",
    )
    list_filter = ("is_staff", "is_active", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)

    # Preserve staff account administration; learner accounts/reports are outside MVP.
    add_fieldsets = UserAdmin.add_fieldsets + (("Administrative access", {'fields': ('is_staff',)}),)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=True)

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser and (obj is None or obj.is_staff)

    def has_change_permission(self, request, obj=None):
        return self.has_view_permission(request, obj)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def get_form(self, request, obj=None, **kwargs):
        base_form = super().get_form(request, obj, **kwargs)

        class StaffOnlyForm(base_form):
            def clean(self):
                data = super().clean()
                if not data.get('is_staff'):
                    self.add_error('is_staff', 'Only administrative staff accounts can be managed in this release.')
                return data

        return StaffOnlyForm

    def has_delete_permission(self, request, obj=None):
        # Safeguard: prevent accidental deletion of student accounts and study records
        return False

    def syllabus_progress_badge(self, obj):
        total = Topic.objects.count() or 1
        completed = obj.progress_records.filter(is_completed=True).count()
        pct = (completed / total) * 100
        pct_display = f"{pct:.1f}%"
        if completed > 0:
            return format_html('<span class="prepal-badge badge-published">{} / {} ({})</span>', completed, total, pct_display)
        return format_html('<span class="prepal-badge badge-unreviewed">0 / {}</span>', total)
    syllabus_progress_badge.short_description = "Syllabus Completed"

    def bookmarks_badge(self, obj):
        count = obj.bookmarks.count()
        return format_html('<span class="tree-meta-pill">🔖 {}</span>', count)
    bookmarks_badge.short_description = "Bookmarks"

    def quiz_performance_badge(self, obj):
        attempts = list(obj.attempts.all())
        if not attempts:
            return mark_safe('<span style="color:#94a3b8;font-size:12px;">No attempts</span>')
        scores = [a.score / a.total_questions * 100 for a in attempts if a.total_questions > 0]
        avg = (sum(scores) / len(scores)) if scores else 0.0
        avg_display = f"{avg:.0f}%"
        return format_html('<span class="prepal-badge badge-draft">{} tests · avg {}</span>', len(attempts), avg_display)
    quiz_performance_badge.short_description = "Quiz Performance"

    def view_report_btn(self, obj):
        url = reverse('admin:content_student_report', args=[obj.pk])
        return format_html('<a href="{}" class="button" style="padding:3px 8px;font-size:11px;">📊 Progress Report</a>', url)
    view_report_btn.short_description = "Report"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/report/', self.admin_site.admin_view(self.student_report_view), name='content_student_report'),
        ]
        return custom_urls + urls

    def student_report_view(self, request, pk):
        # Fixed release boundary applies to every identity, including superusers.
        raise PermissionDenied('Learner reports are unavailable in this content-first release.')
        student = self.get_object(request, str(pk))
        if student is None:
            raise Http404
        if not self.has_view_permission(request, student):
            raise PermissionDenied

        total_topics = Topic.objects.count()
        completed_topics = student.progress_records.filter(is_completed=True).select_related('topic', 'topic__parent').order_by('-last_read_at')
        completed_count = completed_topics.count()
        completion_pct = (completed_count / total_topics * 100.0) if total_topics else 0.0

        bookmarks = student.bookmarks.select_related('topic', 'topic__parent').order_by('-created_at')
        bookmarks_count = bookmarks.count()

        attempts = student.attempts.select_related('quiz', 'quiz__topic').order_by('-attempted_at')
        attempts_count = attempts.count()
        valid_scores = [a.score / a.total_questions * 100.0 for a in attempts if a.total_questions > 0]
        avg_accuracy = (sum(valid_scores) / len(valid_scores)) if valid_scores else 0.0

        context = {
            **self.admin_site.each_context(request),
            'title': f'Learner Report: {student.username}',
            'student': student,
            'total_topics': total_topics,
            'completed_topics': completed_topics,
            'completed_count': completed_count,
            'completion_percentage': completion_pct,
            'bookmarks': bookmarks,
            'bookmarks_count': bookmarks_count,
            'quiz_attempts': attempts,
            'attempts_count': attempts_count,
            'avg_accuracy': avg_accuracy,
            'now': timezone.now(),
        }
        return TemplateResponse(request, 'admin/content/student/report.html', context)


# Unregister standard User and Group, replace with StudentUserAdmin and RestrictedGroupAdmin
if admin.site.is_registered(User):
    admin.site.unregister(User)
admin.site.register(User, StudentUserAdmin)

class RestrictedGroupAdmin(GroupAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser

if admin.site.is_registered(Group):
    admin.site.unregister(Group)
admin.site.register(Group, RestrictedGroupAdmin)


# =========================================================================
# Simplified 3-Section Admin Navigation for Content Managers
# =========================================================================

original_get_app_list = admin.site.get_app_list

def prepal_get_app_list(self, request, app_label=None):
    raw_apps = original_get_app_list(request, app_label)
    models = {m['object_name']: m for app in raw_apps for m in app.get('models', [])}
    sections = []
    groups = [
        ('Topics', 'topics', ['Topic', 'TopicAlias', 'TopicRelation', 'KeywordLinkProposal']),
        ('Content', 'content_studio', ['ContentBlock', 'LearningResource', 'Tag']),
        ('Practice Questions', 'practice', ['Question', 'Quiz']),
    ]
    if request.user.is_superuser:
        groups.append(('Advanced maintenance (Superuser)', 'maintenance', ['ResourcePage', 'QuizReview', 'User', 'Group']))
    for title, label, names in groups:
        entries = [dict(models[n]) for n in names if n in models]
        if not entries:
            continue
        if label == 'topics' and 'Topic' in models:
            entries.append({'name': 'Syllabus tree', 'object_name': 'TopicTree',
                            'admin_url': reverse('admin:content_topic_tree'), 'add_url': None, 'view_only': True})
        sections.append({'name': title, 'app_label': label, 'app_url': entries[0].get('admin_url') or '#',
                         'has_module_perms': True, 'models': entries})
    return sections

admin.site.get_app_list = types.MethodType(prepal_get_app_list, admin.site)

admin.site.site_header = 'Prepal · Content Management Studio'
admin.site.site_title = 'Prepal Admin'
admin.site.index_title = 'Educational Content Management'
