"""Concurrent SQLite budget proof with a fresh temporary database and no provider."""
import json
import os
from pathlib import Path
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))

with tempfile.TemporaryDirectory(prefix='prepal-budget-') as directory:
    os.environ.update(PYTHON_DOTENV_DISABLED='1', DJANGO_SETTINGS_MODULE='core.settings', DJANGO_ENV='development', DATABASE_ENGINE='sqlite', DATABASE_PATH=str(Path(directory) / 'isolated.sqlite3'), AI_ENABLED='false', GEMINI_API_KEY='', GOOGLE_API_KEY='')
    import django
    django.setup()
    from django.core.management import call_command
    from django.db import connections
    from django.test import override_settings
    from content.services.ai_budget import reserve, finish
    from content.models import AiBudgetBucket, AiRequest
    from content.exceptions import ServiceError
    call_command('migrate', verbosity=0)
    with override_settings(AI_DAILY_BUDGET_MICRO=4000, AI_INPUT_RATE_MICRO=1000000, AI_OUTPUT_RATE_MICRO=1000000, AI_MODEL='mock-race', AI_MINUTE_LIMIT=100, AI_VISITOR_DAILY_LIMIT=100, AI_IP_DAILY_LIMIT=100):
        barrier = threading.Barrier(8)
        def contender(number):
            barrier.wait()
            try:
                row = reserve(str(number), 'fixture-ip', 1000)
                finish(row)
                return 'reserved'
            except ServiceError as error: return str(error.detail['code'])
            finally: connections.close_all()
        with ThreadPoolExecutor(max_workers=8) as pool: results = list(pool.map(contender, range(8)))
        # A SQLite lock loser may fail closed; safely consume any remaining room sequentially.
        for n in range(2):
            try: finish(reserve(f'fill-{n}', 'fixture-ip', 1000))
            except ServiceError: pass
        total = AiBudgetBucket.objects.get(key__startswith='global:').reserved_micro
        assert total == 4000 and AiRequest.objects.count() == 2
        try: reserve('over-cap', 'fixture-ip', 1)
        except ServiceError: pass
        else: raise AssertionError('Budget ceiling bypassed')
        print(json.dumps({'parallel_requests': 8, 'outcomes': results, 'charged_micro': total, 'ceiling_micro': 4000, 'successful_reservations': 2, 'over_cap_rejected': True}))
    connections.close_all()
