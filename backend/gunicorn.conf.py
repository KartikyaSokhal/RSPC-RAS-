"""Private Django listener for PostgreSQL deployment behind a TLS reverse proxy."""
bind = '127.0.0.1:8000'
workers = 2
worker_class = 'sync'
timeout = 45
graceful_timeout = 45
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
errorlog = '-'
accesslog = None  # Proxy logs intentionally omit query strings and request bodies.
forwarded_allow_ips = '127.0.0.1'
limit_request_line = 4094
limit_request_fields = 50
