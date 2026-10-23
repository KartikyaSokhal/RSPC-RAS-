"""Versioned demo corpus validation and read-only acceptance checks.

No runtime routes call this module. The existing publication, quiz and discovery
services remain the single implementation of student-facing behavior.
"""
from collections import Counter
from html import escape
import json
from pathlib import Path
from urllib.parse import urlparse

from django.core.management.base import CommandError

FIXTURES = Path(__file__).resolve().parents[1] / 'fixtures'


def load_corpus():
    return (json.loads((FIXTURES / 'sample_lessons_v1.json').read_text()),
            json.loads((FIXTURES / 'syllabus_142.json').read_text()))


def note_words(lesson):
    # Excludes headings, repeated demo notice, references and quiz questions.
    return sum(len(p.split()) for section in lesson['sections'] for p in section['paragraphs'])


def require(condition, message):
    if not condition:
        raise CommandError(message)


def validate_corpus(corpus, hierarchy):
    by_id = {row['id']: row for row in hierarchy}
    lessons = corpus['lessons']
    selected = {row['topic_id']: row for row in lessons}
    require(len(by_id) == 142 and len(lessons) == len(selected) == 15, 'Unexpected corpus size.')
    children = {row['parent_id'] for row in hierarchy}
    roots = Counter()
    questions = set()
    aliases = set()
    for lesson in lessons:
        pk = lesson['topic_id']
        require(pk in by_id and pk not in children, 'Lessons must use existing leaf topics.')
        node = by_id[pk]
        while node['parent_id']:
            node = by_id[node['parent_id']]
        roots[node['id']] += 1
        require(400 <= note_words(lesson) <= 600, f'Lesson {pk} must contain 400–600 note words.')
        require(2 <= len(set(lesson['tags'])) == len(lesson['tags']) <= 4, 'Use 2–4 distinct controlled tags.')
        alias = lesson['alias'].casefold()
        require(alias not in aliases, 'Ambiguous sample alias.')
        aliases.add(alias)
        require(lesson['sources'] and all(key in corpus['sources'] for key in lesson['sources']), 'Missing reference.')
        require(1 <= len(lesson['connections']) <= 6, 'Each sample needs meaningful connections.')
        targets = set()
        text = ' '.join(p for s in lesson['sections'] for p in s['paragraphs']).casefold()
        for edge in lesson['connections']:
            target = edge['target_id']
            require(target != pk and target in selected and target not in targets, 'Invalid connection target.')
            targets.add(target)
            require(selected[target]['alias'].casefold() in text and edge['reason'].strip(), 'Connection needs source phrase and rationale.')
        require(len(lesson['questions']) == 5, 'Each lesson needs five questions.')
        for item in lesson['questions']:
            require(item['question'].strip() and item['question'] not in questions, 'Duplicate or empty question.')
            questions.add(item['question'])
            require(len(item['choices']) == len(set(item['choices'])) == 4, 'Each question needs four distinct choices.')
            require(all(0 < len(c.strip()) <= 255 for c in item['choices']), 'Invalid choice text.')
            require(type(item['answer']) is int and 0 <= item['answer'] < 4 and item['explanation'].strip(), 'Missing answer or explanation.')
    require(roots == Counter({5: 3, 54: 3, 90: 3, 107: 3, 123: 3}), 'Expected three lessons per original subject.')
    for source in corpus['sources'].values():
        parsed = urlparse(source['url'])
        require(parsed.scheme == 'https' and parsed.netloc and source['title'], 'Invalid source link.')


def article_html(lesson, corpus):
    notice = 'Content-review draft — human editorial review pending.' if corpus.get('publication_status') == 'draft-human-review-required' else 'Local development sample — not production material.'
    html = [f'<p><strong>{notice}</strong> '
            'Source-checked demonstration notes; human editorial approval is still required before public release.</p>']
    for section in lesson['sections']:
        html.append(f"<h2>{escape(section['heading'])}</h2>")
        html.extend(f'<p>{escape(p)}</p>' for p in section['paragraphs'])
    html.append('<h2>References and further reading</h2><ul>')
    for key in lesson['sources']:
        source = corpus['sources'][key]
        html.append(f'<li><a href="{escape(source["url"], quote=True)}">{escape(source["title"])}</a></li>')
    html.append('</ul><p>Original explanatory text and practice questions. '
                f'References checked {escape(corpus.get("checked_on", "21 October 2026"))}; examples explicitly described as hypothetical are not historical or measured data.</p>')
    return ''.join(html)


def verify_sample(corpus=None, hierarchy=None):
    """No writes, republishing, analysis, provider calls or auto-repair."""
    from content.models import (Topic, ContentBlock, Quiz, Question, Choice, Tag, TopicAlias,
                                TopicRelation, KeywordLinkProposal, TopicPublication, QuizReview,
                                Bookmark, UserProgress, QuizAttempt, AiRequest)
    from .publication import visible_publications, detail, sanitize
    from .discovery import tag_page
    from .practice import preview, check
    from .quiz import is_reviewable, quiz_fingerprint
    corpus, hierarchy = (corpus, hierarchy) if corpus is not None else load_corpus()
    validate_corpus(corpus, hierarchy)
    actual = list(Topic.objects.order_by('pk').values('id', 'title', 'slug', 'parent_id', 'order'))
    require(actual == hierarchy, 'Syllabus differs from the original hierarchy.')
    pubs = visible_publications()
    report = {'topics': len(actual), 'subjects': 5, 'lessons': 15,
              'note_words': {str(row['topic_id']): note_words(row) for row in corpus['lessons']}}
    expected = {ContentBlock: 15, Quiz: 15, Question: 75, Choice: 300, QuizReview: 15,
                TopicAlias: 15, Bookmark: 0, UserProgress: 0, QuizAttempt: 0, AiRequest: 0}
    for model, count in expected.items():
        require(model.objects.count() == count, f'Unexpected {model.__name__} count.')
        report[model.__name__] = count
    all_ids = set()
    for lesson in corpus['lessons']:
        pk = lesson['topic_id']; pub = pubs.get(pk)
        require(pub is not None, f'Lesson {pk} is unavailable.')
        block = ContentBlock.objects.get(topic_id=pk)
        require(block.content == article_html(lesson, corpus), f'Unexpected draft change for {pk}.')
        require(pub.snapshot['blocks'][0]['content'] == sanitize(block.content), 'Released notes differ from sanitized draft.')
        data = detail(pub, pubs)
        targets = {edge['target_id'] for edge in lesson['connections']}
        links = data['keyword_links']
        require({link['target_id'] for link in links} == targets, f'Approved links missing for {pk}.')
        require(len(links) == len(targets) <= 8, 'Duplicate or excessive inline links.')
        related = [row['id'] for row in data['related']]
        require(targets.issubset(related) and len(related) == len(set(related)) and pk not in related, 'Related topics invalid.')
        require({tag['name'] for tag in data['tags']} == set(lesson['tags']), 'Published tags differ.')
        quiz = Quiz.objects.get(topic_id=pk)
        require(quiz.review.is_approved and is_reviewable(quiz) and quiz.review.fingerprint == quiz_fingerprint(quiz), 'Quiz review invalid.')
        questions = list(quiz.questions.order_by('pk').prefetch_related('choices', 'tags'))
        for question, item in zip(questions, lesson['questions'], strict=True):
            choices = list(question.choices.order_by('pk'))
            require(question.primary_topic_id == pk and question.question_text == item['question']
                    and question.explanation == item['explanation'], 'Question content or primary topic differs.')
            require([c.choice_text for c in choices] == item['choices'] and len(choices) == 4
                    and [i for i, c in enumerate(choices) if c.is_correct] == [item['answer']], 'Invalid answer key.')
        practice = preview(pub.topic.slug, 1)
        require(practice['count'] == 5, 'Lesson collection must contain five canonical questions.')
    pools = {}
    for root in Topic.objects.filter(parent=None).order_by('order', 'pk'):
        data = preview(root.slug, 1)
        ids = [q['id'] for q in data['questions']]
        require(data['count'] == len(ids) == len(set(ids)) == 15, 'Subject pool must contain 15 distinct questions.')
        require(not all_ids.intersection(ids), 'Question belongs to more than one sample subject pool.')
        all_ids.update(ids)
        answers = {str(c.question_id): c.pk for c in Choice.objects.filter(question_id__in=ids, is_correct=True)}
        payload = {k: data[k] for k in ('collection_id', 'page', 'revision_token')}
        payload['answers'] = answers
        first = check(root.slug, payload)
        require(first == check(root.slug, payload) and first['score'] == 15, 'Stateless scoring is not deterministic.')
        pools[root.slug] = len(ids)
    require(len(all_ids) == 75 and QuizAttempt.objects.count() == 0, 'Unexpected saved attempt or missing question.')
    for tag in Tag.objects.all():
        data = tag_page(tag.slug, pubs)
        expected_ids = {row['topic_id'] for row in corpus['lessons'] if tag.name in row['tags']}
        require({row['id'] for row in data['results']} == expected_ids, f'Tag {tag.slug} does not resolve correctly.')
    report.update(publications=TopicPublication.objects.count(), tags=Tag.objects.count(),
                  related_edges=TopicRelation.objects.count(),
                  approved_links=KeywordLinkProposal.objects.filter(status='approved').count(),
                  pending_links=KeywordLinkProposal.objects.filter(status='pending').count(), subject_pools=pools)
    return report
