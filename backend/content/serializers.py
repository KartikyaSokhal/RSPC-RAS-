from rest_framework import serializers
from .models import Topic, ContentBlock, Quiz, Question, Choice


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
        # P002: never query or disclose ownerless learner records.
        return False

    def get_is_completed(self, obj):
        return False


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
        return False

    def get_is_completed(self, obj):
        return False


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


# IDs also travel through JavaScript; reject coercion, bools and unsafe integers.
MAX_SAFE_ID = 2**53 - 1


def is_valid_id(value):
    return type(value) is int and 0 < value <= MAX_SAFE_ID


class StrictIdField(serializers.Field):
    def to_internal_value(self, data):
        if not is_valid_id(data):
            raise serializers.ValidationError("Expected a positive integer ID.")
        return data


class AnswersField(serializers.Field):
    def to_internal_value(self, data):
        if type(data) is not dict:
            raise serializers.ValidationError("Expected an object mapping question IDs to choice IDs.")
        answers = {}
        for key, choice in data.items():
            # JSON object keys must be canonical decimal strings, not 01/+1/1.0.
            if (type(key) is not str or not key.isascii() or not key.isdecimal()
                    or len(key) > 16 or key.startswith("0") or not is_valid_id(int(key))
                    or not is_valid_id(choice)):
                raise serializers.ValidationError("Expected canonical question IDs and integer choice IDs.")
            answers[int(key)] = choice
        return answers


class QuizSubmissionSerializer(serializers.Serializer):
    """Internal grading input only. The HTTP submission endpoint stays P002-blocked."""
    quiz_id = StrictIdField(required=False)
    answers = AnswersField()

    def to_internal_value(self, data):
        if type(data) is not dict or set(data) - {"quiz_id", "answers"}:
            raise serializers.ValidationError({"non_field_errors": ["Expected only quiz_id and answers fields."]})
        return super().to_internal_value(data)


class HistoryMessageSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=["user", "assistant"])
    text = serializers.CharField(max_length=2000)


class SelectedTextSerializer(serializers.Serializer):
    source_id = serializers.CharField(max_length=100)
    revision = serializers.IntegerField(min_value=1)
    text = serializers.CharField(max_length=1000)


class ChatInputSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=2000, required=False, allow_blank=True)
    preset = serializers.ChoiceField(choices=["explain", "simplify", "summarize", "examples", "explain_beginner", "revision"], required=False)
    history = HistoryMessageSerializer(many=True, max_length=6, required=False)
    selected = SelectedTextSerializer(required=False)
    allow_related = serializers.BooleanField(default=False)

    def validate_allow_related(self, value):
        if value:
            raise serializers.ValidationError("Tutor scope is restricted to the current published lesson.")
        return False

    def validate(self, data):
        if not data.get("message") and not data.get("preset"):
            raise serializers.ValidationError("Enter a question or choose an action.")
        if sum(len(item["text"]) for item in data.get("history", [])) > 4000:
            raise serializers.ValidationError("Conversation context is too long.")
        return data

    def to_internal_value(self, data):
        if not isinstance(data, dict) or set(data) - set(self.fields):
            raise serializers.ValidationError({"non_field_errors": ["Unexpected request fields."]})
        return super().to_internal_value(data)
