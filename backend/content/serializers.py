from rest_framework import serializers
from .models import Topic, ContentBlock, Quiz, Question, Choice, Bookmark, UserProgress


class ContentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentBlock
        fields = ["block_type", "content", "file", "order"]


class ChildTopicSerializer(serializers.ModelSerializer):
    has_children = serializers.BooleanField(read_only=True)
    is_bookmarked = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ["title", "slug", "has_children", "is_bookmarked", "is_completed"]

    def get_is_bookmarked(self, obj):
        return Bookmark.objects.filter(topic=obj).exists()

    def get_is_completed(self, obj):
        return UserProgress.objects.filter(topic=obj, is_completed=True).exists()


class TopicDetailSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    blocks = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ["title", "slug", "children", "blocks", "is_bookmarked", "is_completed"]

    def get_children(self, obj):
        qs = obj.children.all().order_by("order")
        return ChildTopicSerializer(qs, many=True).data

    def get_blocks(self, obj):
        qs = obj.blocks.all().order_by("order")
        return ContentBlockSerializer(qs, many=True).data

    def get_is_bookmarked(self, obj):
        return Bookmark.objects.filter(topic=obj).exists()

    def get_is_completed(self, obj):
        return UserProgress.objects.filter(topic=obj, is_completed=True).exists()


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "choice_text"]


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "question_text", "choices"]


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "time_limit_seconds", "questions"]