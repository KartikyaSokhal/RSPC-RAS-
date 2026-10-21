"""Standalone bounded parser: executed with -I in a child, no Django/credentials."""
import hashlib
import json
import resource
import socket
import sys
from pypdf import PdfReader


def extract(path, max_pages=200):
    reader = PdfReader(path, strict=True)
    if reader.is_encrypted: return {'status': 'failed', 'error': 'encrypted_pdf'}
    if not 1 <= len(reader.pages) <= max_pages: return {'status': 'failed', 'error': 'page_limit'}
    forbidden = {'/JS', '/JavaScript', '/AA', '/OpenAction', '/Launch', '/EmbeddedFiles', '/RichMedia', '/XFA', '/AcroForm', '/SubmitForm', '/GoToR'}
    visited = set(); pending = [reader.trailer]; nodes = 0
    while pending:
        item = pending.pop(); nodes += 1
        if nodes > 100000: raise ValueError('object_limit')
        if hasattr(item, 'get_object'): item = item.get_object()
        key = id(item)
        if key in visited: continue
        visited.add(key)
        if isinstance(item, dict):
            if forbidden.intersection(item): return {'status': 'failed', 'error': 'active_pdf'}
            if str(item.get('/S', '')) in forbidden: return {'status': 'failed', 'error': 'active_pdf'}
            pending.extend(item.values())
        elif isinstance(item, (list, tuple)): pending.extend(item)
    pages = []
    for number, page in enumerate(reader.pages, 1):
        content = page.get_contents()
        if content and len(content.get_data()) > 10 * 1024 * 1024: raise ValueError('page_stream_limit')
        text = (page.extract_text() or '').strip()
        if len(text) > 50000: raise ValueError('page_text_limit')
        pages.append({'page_number': number, 'text': text, 'text_sha256': hashlib.sha256(text.encode()).hexdigest()})
    if sum(len(p['text']) for p in pages) > 2000000: raise ValueError('document_text_limit')
    return {'status': 'ready' if all(len(p['text']) >= 20 for p in pages) else 'needs_ocr', 'pages': pages}


if __name__ == '__main__':
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (45, 45))
        if sys.platform != 'darwin':
            resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024,) * 2)
        # macOS does not reliably enforce RLIMIT_AS/DATA; parent monitors RSS and kills the child.
        resource.setrlimit(resource.RLIMIT_FSIZE, (4 * 1024 * 1024,) * 2)
        # pypdf has no network requirement. Remove access even if parser behavior changes.
        def deny(*args, **kwargs): raise RuntimeError('network_disabled')
        socket.socket.connect = deny
        socket.socket.connect_ex = deny
        print(json.dumps(extract(sys.argv[1], int(sys.argv[2]))))
    except Exception:
        print(json.dumps({'status': 'failed', 'error': 'invalid_or_excessive_pdf'}))
        sys.exit(1)
