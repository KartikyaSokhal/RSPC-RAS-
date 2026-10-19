from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from .models import Topic, ContentBlock, TopicRelation
from .ai_engine import get_topic_context
from .exceptions import ServiceError
from .services.publication import publish
from .services.retrieval import DatabaseRetrievalProvider
from .services.tutor import answer


class AIContainmentTests(TestCase):
    def setUp(self):
        self.editor = get_user_model().objects.create_superuser("ai-editor", password="test-only")
        self.topic = Topic.objects.create(title="Safety fixture", slug="safety")
        self.url = "/api/topic/safety/chat/"

    def test_valid_chat_is_disabled_without_any_provider(self):
        with patch("google.genai.Client") as provider:
            response = self.client.post(self.url, {"message": "Explain"}, content_type="application/json")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["error"]["code"], "ai_unavailable")
        provider.assert_not_called()

    def test_invalid_requests_are_predictable(self):
        for body in [[], {}, {"message": "x" * 2001}, {"message": True}, {"preset": "pyq_analysis"}, {"preset": "generate_mcqs"}, {"message": "Explain", "history": [{}]}, {"message": "Explain", "unexpected": 1}]:
            with self.subTest(body=str(body)[:50]):
                self.assertEqual(self.client.post(self.url, body, content_type="application/json").status_code, 400)

    def test_cyclic_hierarchy_fails_instead_of_looping(self):
        Topic.objects.filter(pk=self.topic.pk).update(parent=self.topic)
        self.topic.refresh_from_db()
        with self.assertRaises(ServiceError):
            get_topic_context(self.topic)

    @override_settings(AI_ENABLED=True, AI_GUEST_ENABLED=True, AI_MODEL="fixture-model", GEMINI_API_KEY="fixture-only", AI_DAILY_BUDGET_MICRO=100000, AI_INPUT_RATE_MICRO=1000000, AI_OUTPUT_RATE_MICRO=1000000)
    def test_unpublished_topic_returns_content_unavailable_without_calling_llm(self):
        # Topic exists in syllabus tree, but is not published (no TopicPublication snapshot)
        unpub = Topic.objects.create(title="Unpublished Curriculum Topic", slug="unpub-topic")
        with patch("content.services.providers.GeminiProvider.generate") as mock_generate:
            response = self.client.post(f"/api/topic/{unpub.slug}/chat/", {"message": "Tell me the facts"}, content_type="application/json")
            mock_generate.assert_not_called()

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "insufficient_context")
        self.assertEqual(data["citations"], [])
        self.assertIn("under editorial preparation", data["response"])

    @override_settings(AI_ENABLED=True, AI_GUEST_ENABLED=True, AI_MODEL="fixture-model", GEMINI_API_KEY="fixture-only", AI_DAILY_BUDGET_MICRO=100000, AI_INPUT_RATE_MICRO=1000000, AI_OUTPUT_RATE_MICRO=1000000)
    def test_empty_notes_topic_returns_insufficient_context_without_calling_llm(self):
        # Topic is published, but contains no text blocks or PDFs
        empty_topic = Topic.objects.create(title="Empty Notes Topic", slug="empty-topic")
        publish(empty_topic, self.editor)

        with patch("content.services.providers.GeminiProvider.generate") as mock_generate:
            response = self.client.post(f"/api/topic/{empty_topic.slug}/chat/", {"message": "What is the capital?"}, content_type="application/json")
            mock_generate.assert_not_called()

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "insufficient_context")
        self.assertEqual(data["citations"], [])
        self.assertIn("do not contain enough information", data["response"])

    def test_related_topic_scope_strictly_respects_relations_and_flag(self):
        # Topic A is connected to Topic B via TopicRelation. Topic C is separate and unrelated.
        topic_a = Topic.objects.create(title="Topic A", slug="topic-a")
        topic_b = Topic.objects.create(title="Topic B", slug="topic-b")
        topic_c = Topic.objects.create(title="Topic C", slug="topic-c")

        ContentBlock.objects.create(topic=topic_a, block_type="text", content="<p>Topic A fact about geography.</p>", source_reference="Source A", order=1)
        ContentBlock.objects.create(topic=topic_b, block_type="text", content="<p>Topic B fact about climate.</p>", source_reference="Source B", order=1)
        ContentBlock.objects.create(topic=topic_c, block_type="text", content="<p>Topic C fact about politics.</p>", source_reference="Source C", order=1)

        TopicRelation.objects.create(source=topic_a, target=topic_b)
        publish(topic_a, self.editor); publish(topic_b, self.editor); publish(topic_c, self.editor)

        provider = DatabaseRetrievalProvider()

        # 1. Without allow_related: only topic A evidence should be retrieved
        current, evidence_unallowed = provider.retrieve("topic-a", {"message": "fact", "allow_related": False})
        self.assertIsNotNone(current)
        topic_ids = {e["topic_id"] for e in evidence_unallowed}
        self.assertEqual(topic_ids, {topic_a.id})

        # 2. With allow_related: topic B is included, but unrelated topic C is strictly excluded
        current, evidence_allowed = provider.retrieve("topic-a", {"message": "fact", "allow_related": True})
        topic_ids_allowed = {e["topic_id"] for e in evidence_allowed}
        self.assertIn(topic_a.id, topic_ids_allowed)
        self.assertIn(topic_b.id, topic_ids_allowed)
        self.assertNotIn(topic_c.id, topic_ids_allowed)

    @override_settings(AI_ENABLED=True, AI_GUEST_ENABLED=True, AI_MODEL="fixture-model", GEMINI_API_KEY="fixture-only", AI_DAILY_BUDGET_MICRO=100000, AI_INPUT_RATE_MICRO=1000000, AI_OUTPUT_RATE_MICRO=1000000)
    def test_fabricated_citations_are_rejected_with_502(self):
        # A topic has genuine block b1. The AI model hallucinates a citation b99999.
        topic = Topic.objects.create(title="Grounded Lesson", slug="grounded-lesson")
        block = ContentBlock.objects.create(topic=topic, block_type="text", content="<p>Approved historical fact.</p>", source_reference="Source Fact", order=1)
        publish(topic, self.editor)

        # Mock model returning fabricated citation ID not in evidence
        def fake_model_response(*args, **kwargs):
            return {"answer": "A factual claim.", "citations": ["b99999"], "insufficient": False}, None

        with patch("content.services.providers.GeminiProvider.generate", side_effect=fake_model_response):
            response = self.client.post(f"/api/topic/{topic.slug}/chat/", {"message": "historical fact"}, content_type="application/json")

        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.json()["error"]["code"], "invalid_citation")

    @override_settings(AI_ENABLED=True, AI_GUEST_ENABLED=True, AI_MODEL="fixture-model", GEMINI_API_KEY="fixture-only", AI_DAILY_BUDGET_MICRO=100000, AI_INPUT_RATE_MICRO=1000000, AI_OUTPUT_RATE_MICRO=1000000)
    def test_external_urls_in_ai_answer_are_rejected_with_502(self):
        # If model hallucinates markdown links or external URLs
        topic = Topic.objects.create(title="Grounded Lesson Two", slug="grounded-lesson-two")
        block = ContentBlock.objects.create(topic=topic, block_type="text", content="<p>Approved historical fact.</p>", source_reference="Source Fact", order=1)
        publish(topic, self.editor)

        def hallucinated_link_response(*args, **kwargs):
            return {"answer": "Check this [source](https://external-unverified.com)", "citations": [f"b{block.id}"], "insufficient": False}, None

        with patch("content.services.providers.GeminiProvider.generate", side_effect=hallucinated_link_response):
            response = self.client.post(f"/api/topic/{topic.slug}/chat/", {"message": "historical fact"}, content_type="application/json")

        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.json()["error"]["code"], "invalid_citation")
