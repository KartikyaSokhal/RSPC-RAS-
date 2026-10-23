"""Append the new draft batch only inside a newly prepared isolated student demo."""
import json
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from content.models import Topic, ContentBlock, Quiz, Question, Choice, Tag, TopicAlias, TopicRelation, TopicPublication, normalized_label
from content.services.review_content import load_review, corpus_hash
from content.services.sample_content import article_html, note_words


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not settings.DEMO_MODE or not getattr(settings, 'DEMO_ROOT', None):
            raise CommandError('This command requires a NEW isolated student-review environment.')
        root = Path(settings.DEMO_ROOT)
        marker = root / '.student-demo.json'
        if not settings.DEMO_MODE or not marker.is_file() or json.loads(marker.read_text()).get('kind') != 'prepal-student-review-v2':
            raise CommandError('This command requires a NEW isolated student-review environment.')
        corpus, hierarchy = load_review(); digest = corpus_hash()
        state = json.loads(marker.read_text())
        if state.get('state') == 'ready':
            if state.get('corpus_sha256') != digest: raise CommandError('Prepared corpus differs; choose a new destination.')
            for lesson in corpus['lessons']:
                if not ContentBlock.objects.filter(topic_id=lesson['topic_id'], content=article_html(lesson, corpus)).exists():
                    raise CommandError('Review drafts were edited; preserving all changes.')
            self.stdout.write('Existing unchanged review corpus verified; no writes.'); return
        if list(Topic.objects.order_by('pk').values('id','title','slug','parent_id','order')) != hierarchy:
            raise CommandError('Canonical syllabus or base demo missing.')
        selected = {l['topic_id'] for l in corpus['lessons']}
        if ContentBlock.objects.filter(topic_id__in=selected).exists() or Quiz.objects.filter(topic_id__in=selected).exists():
            raise CommandError('Destination contains review work; refusing to overwrite it.')
        inventory = []
        with transaction.atomic():
            for lesson in corpus['lessons']:
                topic = Topic.objects.get(pk=lesson['topic_id'])
                refs = [corpus['sources'][key] for key in lesson['sources']]
                reference = '\n'.join(f"{r['title']}: {r['url']}" for r in refs)
                tags=[]
                for name in lesson['tags']:
                    tag,_=Tag.objects.get_or_create(normalized_name=normalized_label(name), defaults={'name':name})
                    tags.append(tag)
                topic.tags.set(tags); topic.editorial_status='in_review'; topic.save(update_fields=['editorial_status'])
                TopicAlias.objects.create(topic=topic, name=lesson['alias'], status='draft')
                ContentBlock.objects.create(topic=topic, block_type='text', order=1, content=article_html(lesson,corpus), source_reference=reference)
                quiz=Quiz.objects.create(topic=topic, title=f'Editorial draft · {topic.title}', time_limit_seconds=0)
                for item in lesson['questions']:
                    question=Question.objects.create(quiz=quiz, primary_topic=topic, question_text=item['question'], explanation=item['explanation'])
                    question.tags.set(tags)
                    Choice.objects.bulk_create([Choice(question=question,choice_text=text,is_correct=i==item['answer']) for i,text in enumerate(item['choices'])])
                for edge in lesson['connections']:
                    relation=TopicRelation(source=topic,target_id=edge['target_id'],kind='related',status='draft',reason=edge['reason'])
                    relation.full_clean(); relation.save()
                node=topic; path=[]
                while node: path.append(node.title); node=node.parent
                inventory.append({'topic_id':topic.pk,'title':topic.title,'slug':topic.slug,'syllabus_path':list(reversed(path)),
                    'words':note_words(lesson),'mcqs':5,'choices':20,'tags':[t.name for t in tags],
                    'sources':refs,'publication_status':'unpublished draft, awaiting human review',
                    'quiz_status':'unapproved','alias_status':'draft','relationships':lesson['connections']})
            if TopicPublication.objects.filter(topic_id__in=selected,is_published=True).exists():
                raise CommandError('Review material must not be automatically published.')
        report={'kind':'prepal-student-review-v2','state':'ready','corpus_sha256':digest,'new_lessons':25,'new_questions':125,'new_choices':500,
                'production_approved':False,'lessons':inventory}
        for name in ('review-inventory.json','.student-demo.json'):
            target=root/name; target.write_text(json.dumps(report,ensure_ascii=False,indent=2)); target.chmod(0o600)
        self.stdout.write('25 new unpublished drafts, 125 unapproved MCQs and 500 choices; human review required. Inventory is private.')
