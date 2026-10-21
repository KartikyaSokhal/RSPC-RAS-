"""Validate local Markdown destinations in active docs (historical prose is not execution guidance)."""
from pathlib import Path
import re
from urllib.parse import unquote
import sys
root = Path(__file__).resolve().parents[1]
files = [root/'README.md', root/'AGENTS.md', root/'backend/README.md', *sorted((root/'docs').glob('*.md')), *sorted((root/'docs/design').glob('*.md'))]
missing = []
release = None
if '--release' in sys.argv:
    from release_manifest import release_paths
    release = set(release_paths(root))
    files = [p for p in files if str(p.relative_to(root)) in release]
for file in files:
    body = re.sub(r'```.*?```', '', file.read_text(), flags=re.S)
    for target in re.findall(r'\]\(([^)]+)\)', body):
        if target.startswith(('http:', 'https:', 'mailto:', '#')): continue
        path = unquote(target.split('#')[0]).strip('<>')
        if path:
            resolved = (file.parent/path).resolve()
            if not resolved.exists():
                missing.append(f'{file.relative_to(root)} -> {path}')
            elif release is not None and (not resolved.is_relative_to(root) or str(resolved.relative_to(root)) not in release):
                missing.append(f'{file.relative_to(root)} -> excluded release target: {path}')
if missing: raise SystemExit('\n'.join(missing))
print(f'Local Markdown destinations verified in {len(files)} active documents.')
