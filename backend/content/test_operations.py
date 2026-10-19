"""Host/process boundaries, hostile files and production configuration."""
from io import BytesIO
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from pypdf import PdfWriter
from .services.pdf_extract import extract
from .validators import validate_pdf_upload, validate_image


class OperationsTests(SimpleTestCase):
    def test_production_refuses_unsafe_startup_and_accepts_explicit_safe_settings(self):
        base = {'PATH': os.defpath, 'PYTHON_DOTENV_DISABLED': '1', 'DJANGO_ENV': 'production'}
        command = [sys.executable, '-c', 'from core.settings import DEBUG; assert DEBUG is False']
        for extra in [{}, {'DEBUG': 'true'}, {'SECRET_KEY': 'short', 'ALLOWED_HOSTS': '*'}]:
            result = subprocess.run(command, env={**base, **extra}, capture_output=True, cwd=Path(__file__).resolve().parents[1])
            self.assertNotEqual(result.returncode, 0)
        safe = {**base, 'DEBUG': 'false', 'SECRET_KEY': 'synthetic-production-settings-test-8e5dbf3a750a4cf68ca70983574499c7', 'ALLOWED_HOSTS': 'example.invalid'}
        self.assertEqual(subprocess.run(command, env=safe, capture_output=True, cwd=Path(__file__).resolve().parents[1]).returncode, 0)

    def test_pdf_rejects_active_encrypted_oversized_page_count_and_reports_scans(self):
        with TemporaryDirectory() as directory:
            for kind in ['active', 'encrypted', 'scan', 'pages']:
                writer = PdfWriter(); writer.add_blank_page(width=200, height=200)
                if kind == 'active': writer.add_js('app.alert("fixture")')
                if kind == 'encrypted': writer.encrypt('fixture-only')
                if kind == 'pages': writer.add_blank_page(width=200, height=200)
                file = Path(directory) / f'{kind}.pdf'; writer.write(file)
                result = extract(str(file), max_pages=1)
                self.assertEqual(result.get('error') if kind != 'scan' else result['status'], {'active': 'active_pdf', 'encrypted': 'encrypted_pdf', 'scan': 'needs_ocr', 'pages': 'page_limit'}[kind])

    def test_upload_checks_reject_disguised_files_and_unsafe_images(self):
        for name, payload in [('fake.pdf', b'<html>not a pdf'), ('file.exe', b'%PDF-1.7')]:
            with self.assertRaises(ValidationError): validate_pdf_upload(SimpleUploadedFile(name, payload))
        for name, payload in [('image.svg', b'<svg onload="alert(1)"/>'), ('fake.png', b'not image bytes')]:
            with self.assertRaises(ValidationError): validate_image(SimpleUploadedFile(name, payload))
        from PIL import Image
        buffer = BytesIO(); Image.new('RGB', (20, 20)).save(buffer, format='PNG')
        validate_image(SimpleUploadedFile('fixture.png', buffer.getvalue()))

    def test_gemini_adapter_builds_bounded_request_without_live_client(self):
        import json
        from types import SimpleNamespace
        from unittest.mock import MagicMock, patch
        from django.test import override_settings
        from .services.providers import GeminiProvider
        client = MagicMock()
        client.__enter__.return_value.models.generate_content.return_value = SimpleNamespace(text=json.dumps({'answer': 'Mock', 'citations': ['b1'], 'insufficient': False}), usage_metadata=None)
        with override_settings(GEMINI_API_KEY='fixture-only', AI_MODEL='fixture-model'), patch('content.services.providers.genai.Client', return_value=client) as factory:
            result, _ = GeminiProvider().generate('bounded fixture', [])
            self.assertEqual(result['answer'], 'Mock')
            options = factory.call_args.kwargs['http_options']
            self.assertEqual(options.timeout, 30000); self.assertEqual(options.retry_options.attempts, 1)
            config = client.__enter__.return_value.models.generate_content.call_args.kwargs['config']
            self.assertEqual(config.max_output_tokens, 1000); self.assertEqual(config.thinking_config.thinking_budget, 0)
