from django.contrib import admin
from .models import Topic, ContentBlock, Quiz, Question, Choice, Bookmark, UserProgress, QuizAttempt


class ContentBlockInline(admin.TabularInline):
    model = ContentBlock
    extra = 1
    ordering = ("order",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "parent")
    list_filter = ("parent",)
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ContentBlockInline]


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ("topic", "block_type", "order")
    list_filter = ("block_type", "topic")
    search_fields = ("topic__title",)
    ordering = ("topic", "order")


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


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("topic", "created_at")


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ("topic", "is_completed", "last_read_at")
    list_filter = ("is_completed",)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("quiz", "score", "total_questions", "attempted_at")
