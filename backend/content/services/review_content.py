"""Versioned new academic drafts; never grants editorial or quiz approval."""
import hashlib
import json
from collections import Counter
from pathlib import Path
from .sample_content import load_corpus, note_words, require

PATH = Path(__file__).resolve().parents[1] / 'fixtures/student_lessons_v2.json'


def load_review():
    corpus = json.loads(PATH.read_text())
    base, hierarchy = load_corpus(); by_id = {row['id']: row for row in hierarchy}
    old = {row['topic_id'] for row in base['lessons']}; children = {row['parent_id'] for row in hierarchy}
    ids = {row['topic_id'] for row in corpus['lessons']}; roots = Counter(); questions = set(); paragraphs = set()
    require(len(ids) == len(corpus['lessons']) == 25 and not ids.intersection(old), 'Expected 25 genuinely new lessons.')
    for lesson in corpus['lessons']:
        pk = lesson['topic_id']; require(pk in by_id and pk not in children, 'Use existing leaf topic IDs only.')
        node = by_id[pk]
        while node['parent_id']: node = by_id[node['parent_id']]
        roots[node['id']] += 1
        require(400 <= note_words(lesson) <= 600, f'Invalid note length for {pk}.')
        require(2 <= len(set(lesson['tags'])) == len(lesson['tags']) <= 4, 'Use 2–4 controlled tags.')
        require(lesson['sources'] and all(key in corpus['sources'] for key in lesson['sources']), 'Missing academic reference.')
        for section in lesson['sections']:
            for paragraph in section['paragraphs']:
                require(paragraph not in paragraphs, 'Repeated paragraph in academic batch.'); paragraphs.add(paragraph)
        require(len(lesson['questions']) == 5, 'Each lesson needs five MCQs.')
        for item in lesson['questions']:
            require(item['question'] not in questions, 'Duplicate question.'); questions.add(item['question'])
            require(len(item['choices']) == len(set(item['choices'])) == 4 and all(0 < len(c) <= 255 for c in item['choices']), 'Four distinct valid choices required.')
            require(type(item['answer']) is int and 0 <= item['answer'] <= 3 and item['explanation'], 'One answer and explanation required.')
        require(all(e['target_id'] in ids and e['target_id'] != pk for e in lesson['connections']), 'Invalid proposed relationship.')
    require(roots == Counter({5:5,54:5,90:5,107:5,123:5}), 'Expected five new lessons per real subject.')
    return corpus, hierarchy


def corpus_hash():
    return hashlib.sha256(PATH.read_bytes()).hexdigest()
