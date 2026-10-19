from django.conf import settings
from django.db import models

# class Topic(models.Model):
#     title = models.CharField(max_length=255)
#     slug = models.SlugField(unique=True)

#     parent = models.ForeignKey(
#         "self",
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="children"
#     )

#     def __str__(self):
#         return self.title
class Topic(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["title"]

    @property
    def has_children(self):
        return self.children.exists()

    def __str__(self):
        return self.title
# class Topic(models.Model):
#     title = models.CharField(max_length=255)
#     parent = models.ForeignKey(
#         "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
#     )

#     @property
#     def has_children(self):
#         return self.children.exists()


class ContentBlock(models.Model):
    BLOCK_TYPES = [
        ("heading", "Heading"),
        ("text", "Text"),
        ("pdf", "PDF"),
        ("image", "Image"),
    ]

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="blocks"
    )
    block_type = models.CharField(max_length=20, choices=BLOCK_TYPES)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to="content/", blank=True, null=True)
    order = models.PositiveIntegerField()

    alt_text = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=500, blank=True)
    source_reference = models.TextField(blank=True)

    def __str__(self):
        return f"{self.topic.title} - {self.block_type}"


class Quiz(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=255)
    time_limit_seconds = models.PositiveIntegerField(default=300)

    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return f"{self.topic.title} - {self.title}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    explanation = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.question_text[:50]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="bookmarks")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'topic'], name='unique_user_bookmark', condition=models.Q(user__isnull=False))
        ]

    def __str__(self):
        return f"Bookmark: {self.topic.title}"


class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="progress_records")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="progress_records")
    is_completed = models.BooleanField(default=False)
    last_read_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'topic'], name='unique_user_progress', condition=models.Q(user__isnull=False))
        ]

    def __str__(self):
        return f"Progress: {self.topic.title} - Completed: {self.is_completed}"


class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    score = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()
    attempted_at = models.DateTimeField(auto_now_add=True)
    incorrect_questions = models.ManyToManyField(Question, blank=True)

    def __str__(self):
        return f"Attempt: {self.quiz.title} - {self.score}/{self.total_questions}"


class TopicPublication(models.Model):
    topic = models.OneToOneField(Topic, on_delete=models.PROTECT, related_name='publication')
    revision = models.PositiveIntegerField(default=1)
    is_published = models.BooleanField(default=False, db_index=True)
    title = models.CharField(max_length=255)
    search_text = models.TextField(blank=True)
    snapshot = models.JSONField(default=dict)
    previous_snapshot = models.JSONField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    published_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)


class TopicRelation(models.Model):
    source = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='relations')
    target = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='incoming_relations')
    kind = models.CharField(max_length=20, choices=[('related', 'Related'), ('prerequisite', 'Prerequisite')])
    reason = models.CharField(max_length=300)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['source', 'target', 'kind'], name='unique_topic_relation')]

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.source_id == self.target_id:
            raise ValidationError('A topic cannot relate to itself.')


class LearningResource(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='resources')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='resources/%Y/%m/')
    sha256 = models.CharField(max_length=64, blank=True)
    byte_count = models.PositiveIntegerField(default=0)
    page_count = models.PositiveIntegerField(default=0)
    source_reference = models.TextField()
    rights_note = models.TextField()
    status = models.CharField(max_length=20, default='pending', choices=[(s, s.replace('_', ' ').title()) for s in ['pending', 'processing', 'ready', 'needs_ocr', 'failed', 'approved', 'withdrawn']])
    error_code = models.CharField(max_length=80, blank=True)
    attempts = models.PositiveIntegerField(default=0)
    processing_deadline = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ResourcePage(models.Model):
    resource = models.ForeignKey(LearningResource, on_delete=models.PROTECT, related_name='pages')
    page_number = models.PositiveIntegerField()
    text = models.TextField()
    text_sha256 = models.CharField(max_length=64)

    class Meta:
        ordering = ['page_number']
        constraints = [models.UniqueConstraint(fields=['resource', 'page_number'], name='unique_resource_page')]


class QuizReview(models.Model):
    quiz = models.OneToOneField(Quiz, on_delete=models.PROTECT, related_name='review')
    fingerprint = models.CharField(max_length=64)
    source_reference = models.TextField()
    reviewed_by = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL)
    reviewed_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)


class AiBudgetBucket(models.Model):
    key = models.CharField(max_length=120, unique=True)
    reserved_micro = models.PositiveBigIntegerField(default=0)
    requests = models.PositiveIntegerField(default=0)


class AiRequest(models.Model):
    request_id = models.UUIDField(primary_key=True)
    visitor_key = models.CharField(max_length=64, db_index=True)
    bucket_keys = models.JSONField(default=list)
    reserved_micro = models.PositiveBigIntegerField()
    actual_micro = models.PositiveBigIntegerField(null=True)
    state = models.CharField(max_length=20, default='reserved')
    model = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline_at = models.DateTimeField()
