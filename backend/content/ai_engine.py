"""Compatibility boundaries. Live generation is available only through the tutor service."""
from .exceptions import ServiceError


def get_topic_context(topic):
    # Temporary bounded current-topic context; no arbitrary descendants or cycles.
    seen = set()
    node = topic
    for _ in range(32):
        if node.pk in seen:
            raise ServiceError("invalid_hierarchy", "Topic hierarchy is unavailable.", 409)
        seen.add(node.pk)
        if not node.parent_id:
            break
        node = node.parent
    else:
        raise ServiceError("invalid_hierarchy", "Topic hierarchy is unavailable.", 409)
    return "\n".join(topic.blocks.filter(block_type__in=["heading", "text"]).order_by("order", "pk").values_list("content", flat=True)[:100])[:24000]


def generate_mentor_response(topic, message, preset=None):
    raise ServiceError("ai_unavailable", "The tutor is temporarily unavailable. You can continue reading.", 503)


def generate_quiz_questions(*args, **kwargs):
    raise ServiceError("feature_unavailable", "Automatic question generation is disabled.", 503)


def generate_weakness_report(*args, **kwargs):
    raise ServiceError("learner_features_unavailable", "Personalized features are unavailable.", 503)
