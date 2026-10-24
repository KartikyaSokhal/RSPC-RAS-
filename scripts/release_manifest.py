"""Validate/export explicit release inputs without staging, committing or copying private data."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TOP = {
    '.env.example', '.gitignore', '.nvmrc', '.python-version', 'AGENTS.md', 'README.md',
    'index.html', 'package.json', 'package-lock.json', 'eslint.config.js',
    'vite.config.js', 'vitest.config.js', 'playwright.config.js',
    'playwright.integration.config.js', 'playwright.sample.config.js', 'playwright.student.config.js', 'prepal.code-workspace',
}
BACKEND = {
    '.env.example', '.gitignore', 'README.md', 'manage.py', 'run_tests.py', 'gunicorn.conf.py',
    'requirements.in', 'requirements.txt', 'requirements-dev.in', 'requirements-dev.txt',
}
TREES = ('src', 'public', 'e2e', 'e2e-integration', 'e2e-sample', 'e2e-student', 'scripts', 'deploy',
         '.github', 'backend/content', 'backend/core')
SKIP = {'__pycache__', 'node_modules', '.venv', 'env', '.local', '.git', '.pytest_cache'}
REQUIRED = {
    'backend/content/student_auth.py', 'backend/content/student_views.py',
    'backend/core/render_settings.py', 'backend/core/render_support.py',
    'backend/core/render_urls.py', 'backend/core/static_build_settings.py',
    'deploy/render-build.sh', 'deploy/render-start.sh', 'deploy/render-gunicorn.conf.py',
    'backend/content/test_render.py',
    'backend/core/free_demo_settings.py', 'backend/core/free_demo_support.py',
    'backend/core/free_demo_urls.py', 'backend/content/test_free_demo.py',
    'deploy/render-free-demo-start.sh',
    'backend/content/services/planner.py', 'backend/content/services/attempts.py',
    'backend/content/fixtures/student_lessons_v2.json', 'src/pages/plannerPage.jsx',
    'scripts/prepare_student_demo.py', 'e2e-student/platform.spec.js',
    'docs/AGENT_HANDOFF.md', 'docs/PROJECT_STATUS.md', 'docs/MVP_SCOPE.md',
    'docs/ADMIN_WORKFLOW.md', 'docs/AI_SYSTEM.md', 'docs/FEATURES.md',
    'src/pages/tagPage.jsx', 'src/pages/learnerUnavailablePage.jsx',
    'src/components/study/TopicPopup.jsx', 'src/hooks/useSyllabus.js',
    'backend/core/database.py', 'backend/content/signals.py',
    'backend/content/static/admin/js/prepal_wysiwyg.js',
    'backend/content/migrations/0007_tag_question_primary_topic_question_related_topics_and_more.py',
    'backend/content/migrations/0008_connectionscan_keywordlinkproposal_tag_is_public_and_more.py',
    'backend/content/fixtures/sample_lessons_v1.json', 'e2e-sample/content.spec.js',
}


def release_paths(root=ROOT):
    names = set(TOP) | {f'backend/{name}' for name in BACKEND} | {'.vscode/settings.json'}
    names.update(str(p.relative_to(root)) for p in (root / 'docs').glob('*.md'))
    for tree in TREES:
        names.update(str(p.relative_to(root)) for p in (root / tree).rglob('*') if p.is_file())
    result = []
    for name in sorted(names):
        p = root / name
        if SKIP.intersection(p.relative_to(root).parts) or p.name == '.DS_Store' or p.suffix in {'.pyc', '.log'}:
            continue
        if p.is_symlink() or not p.is_file():
            raise SystemExit(f'Missing or symlinked release input: {name}')
        if p.name == '.env' or '.sqlite3' in p.name or p.suffix in {'.db', '.pem', '.key'} or 'credentials' in p.name:
            raise SystemExit(f'Private artifact in release input: {name}')
        result.append(name)
    if not REQUIRED.issubset(result):
        raise SystemExit(f'Required inputs absent: {sorted(REQUIRED.difference(result))}')
    return result


def private_values(root):
    values = set()
    env = root / 'backend/.env'
    if env.exists():
        for line in env.read_text().splitlines():
            key, sep, value = line.partition('=')
            if sep and key.strip() in {'SECRET_KEY', 'GEMINI_API_KEY', 'GOOGLE_API_KEY', 'POSTGRES_PASSWORD', 'GOOGLE_CLIENT_SECRET', 'EMAIL_HOST_PASSWORD'}:
                value = value.strip().strip('\"\'')
                if len(value) >= 12:
                    values.add(value.encode())
    for p in (root / '.local').glob('*/admin-credentials.txt'):
        for line in p.read_text().splitlines():
            if line.startswith('Password: ') and len(line[10:]) >= 12:
                values.add(line[10:].encode())
    return values


def manifest(root=ROOT):
    paths = release_paths(root)
    secrets = private_values(root)
    files = {}
    for name in paths:
        content = (root / name).read_bytes()
        if any(value in content for value in secrets):
            raise SystemExit(f'Private credential found in release input: {name}')
        files[name] = {'sha256': hashlib.sha256(content).hexdigest(), 'bytes': len(content)}
    if (root / '.git').exists():
        ignored = subprocess.run(['git', 'check-ignore', '--stdin'], input='\n'.join(paths) + '\n',
                                 cwd=root, text=True, capture_output=True)
        if ignored.returncode not in (0, 1) or ignored.stdout.strip():
            raise SystemExit('Release inputs are ignored or Git check failed: ' + ignored.stdout.strip())
    return {'format': 1, 'files': files, 'private_artifacts': 0, 'known_private_values_found': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='New JSON manifest outside the release inputs.')
    parser.add_argument('--export', type=Path, help='New disposable release-copy directory.')
    args = parser.parse_args()
    report = manifest()
    if args.export:
        destination = args.export.expanduser().resolve()
        if destination.exists() or destination == ROOT or ROOT in destination.parents:
            raise SystemExit('Export requires a new destination outside the application checkout.')
        destination.mkdir(parents=True, mode=0o700)
        for name, expected in report['files'].items():
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, target)
            if hashlib.sha256(target.read_bytes()).hexdigest() != expected['sha256']:
                raise SystemExit(f'Export hash differs: {name}')
        (destination / '.release-manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    if args.output:
        with args.output.open('x') as stream:
            stream.write(json.dumps(report, indent=2) + '\n')
    print(f"Validated {len(report['files'])} release inputs; no private artifacts or known private credentials.")


if __name__ == '__main__':
    main()
