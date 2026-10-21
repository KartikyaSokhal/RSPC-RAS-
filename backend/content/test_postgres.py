"""Real PostgreSQL concurrency semantics on the disposable test DB; no providers."""
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest import skipUnless

from django.db import connection, connections
from django.test import TransactionTestCase, override_settings

from .exceptions import ServiceError
from .models import AiBudgetBucket, AiRequest
from .services.ai_budget import reserve, finish


@skipUnless(connection.vendor == 'postgresql', 'PostgreSQL concurrency checks require --postgres')
@override_settings(AI_DAILY_BUDGET_MICRO=4000, AI_INPUT_RATE_MICRO=1000000,
                   AI_OUTPUT_RATE_MICRO=1000000, AI_OUTPUT_TOKEN_LIMIT=1000, AI_MODEL='mock-only')
class PostgresConcurrencyTests(TransactionTestCase):
    def test_concurrent_reservations_cannot_exceed_global_cap(self):
        barrier = Barrier(8)
        def worker(index):
            try:
                barrier.wait(timeout=5)
                reserve(f'fixture-{index}', f'ip-{index}', 1000)
                return True
            except ServiceError as error:
                self.assertIn(error.status_code, (429, 503))
                return False
            finally:
                connections.close_all()
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(worker, range(8)))
        self.assertEqual(sum(results), 2)
        self.assertEqual(AiRequest.objects.count(), 2)
        self.assertEqual(AiBudgetBucket.objects.get(key__startswith='global:').reserved_micro, 4000)

    def test_simultaneous_finish_releases_unused_cost_once(self):
        request = reserve('fixture', 'fixture-ip', 1000)
        barrier = Barrier(2)
        def worker(_):
            try:
                barrier.wait(timeout=5)
                finish(request, actual_micro=1000)
            finally:
                connections.close_all()
        with ThreadPoolExecutor(max_workers=2) as pool:
            list(pool.map(worker, range(2)))
        request.refresh_from_db()
        self.assertEqual(request.state, 'completed')
        self.assertEqual(request.actual_micro, 1000)
        self.assertEqual(AiBudgetBucket.objects.get(key__startswith='global:').reserved_micro, 1000)
