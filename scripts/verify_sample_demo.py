"""Read-only validation of a prepared sample demo. No repair or live AI calls."""
import json
import os
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
demo = os.environ.get('PREPAL_DEMO_ROOT')
if not demo or not Path(demo).is_absolute():
    raise SystemExit('Set PREPAL_DEMO_ROOT to the absolute sample demo directory.')
marker = Path(demo) / '.sample-demo.json'
if not marker.is_file() or json.loads(marker.read_text()).get('state') != 'ready':
    raise SystemExit('Refusing verification outside a completed sample demo.')
os.environ.update(DJANGO_SETTINGS_MODULE='core.demo_settings', PYTHON_DOTENV_DISABLED='1',
                  GEMINI_API_KEY='', GOOGLE_API_KEY='')
sys.path.insert(0, str(root / 'backend'))
import django
django.setup()
from django.db import connection
from django.test import Client
from unittest.mock import patch
from content.services.sample_content import verify_sample

# An accidental future write in a verifier must fail rather than touch the demo.
with connection.cursor() as cursor:
    cursor.execute('PRAGMA query_only=ON')
    cursor.execute('PRAGMA integrity_check')
    assert cursor.fetchall() == [('ok',)]
    cursor.execute('PRAGMA foreign_key_check')
    assert cursor.fetchall() == []
with patch('google.genai.Client', side_effect=AssertionError('Paid AI forbidden')), \
        patch('socket.socket.connect', side_effect=AssertionError('Network forbidden')):
    report = verify_sample()
    from content.services.sample_content import load_corpus
    from content.models import Topic, Tag, Choice
    corpus, hierarchy = load_corpus()
    by_id = {row['id']: row for row in hierarchy}
    client = Client(enforce_csrf_checks=True)
    config = client.get('/api/config/').json()
    assert config['demo'] is True
    requests_checked = 1
    for lesson in corpus['lessons']:
        slug = by_id[lesson['topic_id']]['slug']
        for suffix in ('', 'context/', 'quiz/'):
            url = f'/api/topic/{slug}/{suffix}'
            first = client.get(url)
            assert first.status_code == 200, url
            # Signed tokens may have different timestamps; compare semantic IDs.
            if suffix == 'quiz/':
                second = client.get(url)
                assert second.status_code == 200
                assert [q['id'] for q in first.json()['questions']] == [q['id'] for q in second.json()['questions']]
                requests_checked += 1
            requests_checked += 1
    for tag in Tag.objects.all():
        assert client.get(f'/api/tags/{tag.slug}/').status_code == 200
        requests_checked += 1
    for subject in Topic.objects.filter(parent=None):
        url = f'/api/topic/{subject.slug}/practice/'
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        ids = [q['id'] for q in data['questions']]
        assert data['count'] == len(set(ids)) == 15
        answers = {str(c.question_id): c.pk for c in Choice.objects.filter(question_id__in=ids, is_correct=True)}
        payload = {key: data[key] for key in ('collection_id', 'page', 'revision_token')}
        payload['answers'] = answers
        result = client.post(url + 'check/', data=json.dumps(payload), content_type='application/json',
                             HTTP_X_CSRFTOKEN=config['csrf_token'])
        assert result.status_code == 200 and result.json()['score'] == 15
        requests_checked += 2
    for url in ('/api/bookmarks/', '/api/progress/', '/api/dashboard/', '/api/auth/status/'):
        assert client.get(url).status_code == 503
        requests_checked += 1
    assert client.get('/api/tags/nonexistent-sample-tag/').status_code == 404
    draft = client.get('/api/topic/a-mountains/').json()
    assert draft['status'] == 'coming_soon' and draft['blocks'] == [] and draft['is_published'] is False
    assert client.get('/api/topic/a-mountains/context/').status_code == 404
    report['http_requests_verified'] = requests_checked + 3
print(json.dumps(report, indent=2))
