"""Single-worker staging baseline; increase only after memory/load measurement."""
import os
port = int(os.environ.get('PORT', '10000'))
if not 1 <= port <= 65535:
    raise ValueError('PORT outside valid range')
bind = f'0.0.0.0:{port}'
workers = 1
worker_class = 'sync'
timeout = 90  # Greater than the existing 60-second bounded PDF worker.
graceful_timeout = 90
keepalive = 2
accesslog = None  # No query strings, tokens, bodies or student identifiers.
errorlog = '-'
forwarded_allow_ips = '127.0.0.1'
