"""Synthetic development content only. Never runs against application data."""
from pathlib import Path
import secrets
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from content.models import Topic, ContentBlock, TopicRelation, Quiz, Question, Choice, LearningResource
from content.services.publication import publish
from content.services.quiz import review_quiz
from content.services.resources import process_resource, approve_resource

LESSONS = [
    ('reading-evidence', 'Reading the past, one source at a time', 'Observation and inference', 'An observation describes what you can see in a source. An inference is an interpretation that needs supporting evidence.'),
    ('building-chronology', 'Putting events into perspective', 'Chronology and sequence', 'A chronology organizes events in sequence. Relative order and precise dates answer different questions; distinguish them in your notes.'),
    ('comparing-sources', 'When sources tell different stories', 'Comparing sources', 'Compare what each source claims, when it was produced and the evidence it offers. Agreement is useful, but does not automatically establish accuracy.'),
    ('reading-maps', 'Reading a landscape with care', 'Maps and scale', 'A map is a representation made for a purpose. Read the legend, orientation and scale before drawing conclusions from it.'),
    ('asking-questions', 'Better questions, deeper understanding', 'Questions and evidence', 'A useful study question is specific enough to answer using available evidence. Separate a factual question from a request for interpretation.'),
    ('connecting-ideas', 'Finding the thread between ideas', 'Relationships and context', 'Connect two lessons by naming the relationship between them. A prerequisite introduces an idea that a later lesson relies on.'),
    ('making-notes', 'Make notes that do more', 'Notes and source references', 'Keep a source reference beside an important claim. A short summary should preserve the meaning and uncertainty of the source.'),
    ('reflecting-learning', 'A thoughtful pause before moving on', 'Reflection and practice', 'Use practice feedback to return to a relevant passage. Explain why an answer is supported, then try the question again without a timer.'),
]


def demo_pdf(title):
    from io import BytesIO
    from pypdf import PdfWriter
    from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject
    writer = PdfWriter()
    for number in (1, 2):
        page = writer.add_blank_page(width=595, height=842)
        font = DictionaryObject({NameObject('/Type'): NameObject('/Font'), NameObject('/Subtype'): NameObject('/Type1'), NameObject('/BaseFont'): NameObject('/Helvetica')})
        page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/F1'): writer._add_object(font)})})
        lines = [title, f'Development edition / page {number}', 'SYNTHETIC MATERIAL - NOT AN APPROVED RPSC LESSON', '',
                 'A small field guide to thoughtful reading.', '', 'Observation describes what a source shows.', 'Inference is an interpretation to check against evidence.',
                 'A chronology places events in sequence.', 'Keep a reference beside each important claim.', '', 'Pause. Read the passage. Ask what supports the answer.', '',
                 'Created for Prepal interface and retrieval testing.', 'Original demonstration text; no third-party material.']
        stream = DecodedStreamObject()
        operations = ['BT /F1 14 Tf 48 770 Td']
        for i, line in enumerate(lines):
            escaped = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
            if i: operations.append('0 -30 Td')
            operations.append(f'({escaped}) Tj')
        operations.append('ET'); stream.set_data('\n'.join(operations).encode('ascii'))
        page[NameObject('/Contents')] = writer._add_object(stream)
    output = BytesIO(); writer.write(output); return output.getvalue()


class Command(BaseCommand):
    help = 'Create clearly labeled synthetic fixtures in the isolated demo database only.'

    def handle(self, *args, **options):
        expected = Path(settings.DEMO_ROOT) / 'demo.sqlite3'
        if (not settings.DEMO_MODE or settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3'
                or Path(settings.DATABASES['default']['NAME']).resolve() != expected.resolve()):
            raise CommandError('Refusing demo data outside the isolated demo database.')
        if Topic.objects.exists(): raise CommandError('Demo already contains topics; refusing overwrite. Keep the existing demo or select a separately reviewed reset.')
        password = secrets.token_urlsafe(24)
        editor = get_user_model().objects.create_superuser('demo-editor', password=password)
        credentials = Path(settings.DEMO_ROOT) / 'admin-credentials.txt'
        credentials.write_text(f'Local synthetic demo only\nUsername: demo-editor\nPassword: {password}\n')
        credentials.chmod(0o600)
        import json
        fixture_path = Path(__file__).resolve().parents[2] / 'fixtures' / 'syllabus_142.json'
        if fixture_path.exists():
            with open(fixture_path) as f:
                raw_topics = json.load(f)
            for item in raw_topics:
                Topic.objects.create(
                    id=item['id'],
                    title=item['title'],
                    slug=item['slug'],
                    parent_id=item['parent_id'],
                    order=item['order']
                )
            for root_id in [5, 54, 90, 107, 123]:
                t = Topic.objects.filter(id=root_id).first()
                if t: publish(t, editor)
            t6 = Topic.objects.filter(id=6).first()
            if t6:
                ContentBlock.objects.create(topic=t6, block_type='heading', content='Prehistoric Sites of Rajasthan', order=1, source_reference='Rajasthan State Archives / Archeological Survey')
                ContentBlock.objects.create(topic=t6, block_type='text', content='<p>Prehistoric human occupation in Rajasthan dates back from the Lower Palaeolithic period. The river valleys of Luni, Berach, and Banas have yielded rich assemblages of stone age implements.</p><p>Key sites such as Bagor (Bhilwara), Tilwara (Barmer), and Kalibangan (Hanumangarh) illustrate the transition from nomadic foraging to settled agro-pastoral communities.</p>', order=2, source_reference='Archeological Survey of India')
                publish(t6, editor)
            t7 = Topic.objects.filter(id=7).first()
            if t7:
                ContentBlock.objects.create(topic=t7, block_type='heading', content='Palaeolithic to Chalcolithic Transitions', order=1, source_reference='Rajasthan State Archives')
                ContentBlock.objects.create(topic=t7, block_type='text', content='<p>The Palaeolithic era in Rajasthan is characterized by Acheulian handaxes, cleavers, and flake tools found predominantly along the ancient Saraswati and Drishadvati river systems.</p><p>The subsequent Mesolithic phase is prominently documented at Bagor on the Kothari river, showing microlithic industries and early animal domestication.</p>', order=2, source_reference='Archeological Survey of India')
                publish(t7, editor)

        root5 = Topic.objects.filter(id=5).first()
        collection = Topic.objects.create(title='A toolkit for historical thinking', slug='historical-thinking', parent=root5, order=99)
        publish(collection, editor)
        # Retain rajasthan-history slug for gallery preview test compatibility
        history_alias = Topic.objects.create(title='Rajasthan · History & heritage overview', slug='rajasthan-history', parent=root5, order=98)
        publish(history_alias, editor)
        topics = []
        for index, (slug, title, concept, fact) in enumerate(LESSONS):
            topic = Topic.objects.create(title=title, slug=slug, parent=collection, order=index)
            topics.append(topic)
            blocks = [
                ('text', f'<p><strong>Development lesson.</strong> This original demonstration content tests the learning experience. It has not been reviewed against the RPSC syllabus.</p>'),
                ('heading', concept),
                ('text', f'<p>{fact}</p><p>Start by reading the passage slowly. Identify the central idea, ask what supports it, and distinguish the statement from your interpretation. This simple routine makes a complex reading task more manageable.</p><blockquote><p>Learning objective: explain the central idea in your own words and connect it to a specific source.</p></blockquote>'),
                ('heading', 'A closer look'),
                ('text', '<p>Consider a synthetic example: a study card shows two marks. “There are two marks” is an observation. “The marks had a special meaning” is an inference that would need additional evidence.</p><table><caption>A reading checklist</caption><thead><tr><th scope="col">Ask</th><th scope="col">Look for</th></tr></thead><tbody><tr><td>What does the source say?</td><td>A clear observation or claim</td></tr><tr><td>What supports the claim?</td><td>Evidence and a reference</td></tr><tr><td>What remains uncertain?</td><td>Limits and alternative explanations</td></tr></tbody></table>'),
                ('heading', 'Take it with you'),
                ('text', f'<ul><li>{fact}</li><li>Keep observation and interpretation distinct.</li><li>Use the connected lesson to build on this idea.</li></ul><p>Before moving on, explain the distinction to yourself. The practice questions below help you check the demonstration material without saving any personal result.</p>'),
            ]
            for order, (kind, text) in enumerate(blocks):
                ContentBlock.objects.create(topic=topic, block_type=kind, content=text, order=order, source_reference='Prepal original synthetic development material; no editorial approval')
            quiz = Quiz.objects.create(topic=topic, title=f'Practice · {concept}', time_limit_seconds=0)
            questions = [
                ('Which statement is supported by this lesson?', fact, 'A source always proves every interpretation.'),
                ('What should accompany an important claim?', 'A source reference and supporting evidence.', 'Only a confident tone.'),
                ('What describes an observation in the example?', 'The study card shows two marks.', 'The marks must have a special meaning.'),
                ('What should you do when the evidence is insufficient?', 'State what is uncertain and look for relevant evidence.', 'Invent the missing information.'),
                ('How can you use practice feedback?', 'Return to the relevant passage and explain the answer.', 'Treat a score as proof of complete mastery.'),
            ]
            for question, correct, wrong in questions:
                q = Question.objects.create(quiz=quiz, question_text=question, explanation=f'The demonstration notes support this answer: {correct}')
                Choice.objects.create(question=q, choice_text=correct[:255], is_correct=True)
                Choice.objects.create(question=q, choice_text=wrong)
            review_quiz(quiz, editor, 'Synthetic test approval only; not editorial approval for public launch')
            publish(topic, editor)
        for i, topic in enumerate(topics):
            target = topics[(i+1) % len(topics)]
            TopicRelation.objects.create(source=topic, target=target, kind='related', status='approved', reason='Continue the demonstration reading toolkit with this connected concept.')
        for number, title in enumerate(['The thoughtful reading field guide', 'A pocket guide to source questions']):
            resource = LearningResource(topic=topics[number], title=title, source_reference='Prepal original synthetic demonstration PDF', rights_note='Original fixture text created for development; no third-party material')
            resource.file.save(f'demonstration-guide-{number+1}.pdf', ContentFile(demo_pdf(title)), save=True)
            process_resource(resource.pk); resource.refresh_from_db()
            if resource.status != 'ready': raise CommandError(f'Demo PDF failed: {resource.error_code}')
            approve_resource(resource, editor)
        for topic in topics: publish(topic, editor)
        # Explicit synthetic editorial fixtures, never real-corpus approval.
        from content.models import Tag, TopicAlias, KeywordLinkProposal
        from content.services.connections import process_pending, decide
        tag = Tag.objects.create(name='Synthetic reading toolkit', is_public=True)
        TopicAlias.objects.create(topic=topics[0], name='Observation', status='approved')
        TopicAlias.objects.create(topic=topics[1], name='Chronology', status='approved')
        ContentBlock.objects.create(topic=topics[0], block_type='text', order=100, content='<p>Chronology places evidence in sequence.</p>', source_reference='Synthetic linking fixture; not real editorial content')
        for topic in topics[:2]:
            topic.tags.add(tag)
            publish(topic, editor)
        process_pending(200)
        for proposal in KeywordLinkProposal.objects.filter(source=topics[1], target=topics[0], phrase_key='observation'):
            decide(proposal, 'approved', editor)
        self.stdout.write('Created 8 synthetic lessons, 40 fixture MCQs and 2 original two-page PDFs. AI is mocked. Admin credentials are private in .local/demo/admin-credentials.txt.')
