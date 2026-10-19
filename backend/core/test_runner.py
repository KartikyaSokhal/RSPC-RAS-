"""Create disposable tables directly from models, without running migrations."""
from contextlib import ExitStack
from unittest.mock import patch

from django.apps import apps
from django.db import connections
from django.test.runner import DiscoverRunner


class NoMigrationRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        if self.parallel > 1 or self.keepdb:
            raise RuntimeError("P000 requires one disposable in-memory database")
        if set(connections) != {"default"}:
            raise RuntimeError("Unexpected test database alias")
        connection = connections["default"]
        if connection.vendor != "sqlite" or connection.settings_dict["NAME"] != ":memory:":
            raise RuntimeError("Refusing tests outside SQLite :memory:")
        connection.ensure_connection()
        with connection.schema_editor() as editor:
            for model in apps.get_models():
                if model._meta.managed and not model._meta.proxy:
                    editor.create_model(model)
        return None

    def teardown_databases(self, old_config, **kwargs):
        connection = connections["default"]
        # Normal SQLite close() deliberately preserves an in-memory database.
        if connection.connection is not None:
            connection.connection.close()
            connection.connection = None

    def run_tests(self, test_labels, **kwargs):
        with ExitStack() as stack:
            client = stack.enter_context(patch(
                "google.genai.Client", side_effect=AssertionError("Real AI clients forbidden in tests")
            ))
            stack.enter_context(patch("dotenv.load_dotenv"))
            network = stack.enter_context(patch(
                "socket.socket.connect", side_effect=AssertionError("Test network access forbidden")
            ))
            network_ex = stack.enter_context(patch(
                "socket.socket.connect_ex", side_effect=AssertionError("Test network access forbidden")
            ))
            failures = super().run_tests(test_labels, **kwargs)
            # Catch attempts even if application code swallows the exception.
            if client.call_count or network.call_count or network_ex.call_count:
                raise RuntimeError("Unexpected real provider/network attempt during tests")
            return failures
