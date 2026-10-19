"""Validate local Markdown destinations in active docs (historical prose is not execution guidance)."""
from pathlib import Path
import re
from urllib.parse import unquote
root = Path(__file__).resolve().parents[1]
files = [root/'README.md', root/'AGENTS.md', root/'backend/README.md', *sorted((root/'docs').glob('*.md')), *sorted((root/'docs/design').glob('*.md'))]
missing = []
for file in files:
    body = re.sub(r'```.*?```', '', file.read_text(), flags=re.S)
    for target in re.findall(r'\]\(([^)]+)\)', body):
        if target.startswith(('http:', 'https:', 'mailto:', '#')): continue
        path = unquote(target.split('#')[0]).strip('<>')
        if path and not (file.parent/path).exists(): missing.append(f'{file.relative_to(root)} -> {path}')
if missing: raise SystemExit('\n'.join(missing))
print(f'Local Markdown destinations verified in {len(files)} active documents.')
