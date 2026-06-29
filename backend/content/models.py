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
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bookmark: {self.topic.title}"


class UserProgress(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="progress_records")
    is_completed = models.BooleanField(default=False)
    last_read_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Progress: {self.topic.title} - Completed: {self.is_completed}"


class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    score = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()
    attempted_at = models.DateTimeField(auto_now_add=True)
    incorrect_questions = models.ManyToManyField(Question, blank=True)

    def __str__(self):
        return f"Attempt: {self.quiz.title} - {self.score}/{self.total_questions}"