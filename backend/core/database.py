"""Explicit database selection; never silently fall back to valuable SQLite data."""
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured


def bounded(env, name, default, low, high):
    try:
        value = int(env.get(name, default))
        if not low <= value <= high: raise ValueError
    except (ValueError, TypeError):
        raise ImproperlyConfigured(f'{name} must be an integer from {low} to {high}.') from None
    return value

def database_config(env, *, production=False):
    engine = env.get('DATABASE_ENGINE', 'postgresql')
    if engine == 'sqlite':
        if production:
            raise ImproperlyConfigured('Production requires PostgreSQL.')
        name = env.get('DATABASE_PATH', '')
        if not name:
            raise ImproperlyConfigured('Explicit DATABASE_PATH is required for isolated SQLite use.')
        original = Path(__file__).resolve().parents[1] / 'db.sqlite3'
        if name != ':memory:' and Path(name).resolve() == original:
            raise ImproperlyConfigured('The original SQLite archive may only be accessed by read-only backup/inspection tools.')
        return {'ENGINE': 'django.db.backends.sqlite3', 'NAME': name, 'OPTIONS': {'timeout': 5}}
    if engine != 'postgresql':
        raise ImproperlyConfigured('DATABASE_ENGINE must be postgresql or sqlite.')
    required = ('POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_HOST')
    if any(not env.get(key, '').strip() for key in required):
        raise ImproperlyConfigured('Set POSTGRES_DB, POSTGRES_USER and POSTGRES_HOST; no SQLite fallback is allowed.')
    sslmode = env.get('POSTGRES_SSLMODE', 'verify-full' if production else 'prefer')
    if sslmode not in {'disable', 'allow', 'prefer', 'require', 'verify-ca', 'verify-full'}:
        raise ImproperlyConfigured('Invalid POSTGRES_SSLMODE.')
    if production and (not env.get('POSTGRES_PASSWORD') or sslmode != 'verify-full'):
        raise ImproperlyConfigured('Production requires POSTGRES_PASSWORD and POSTGRES_SSLMODE=verify-full.')
    try:
        port = int(env.get('POSTGRES_PORT', '5432'))
        if not 1 <= port <= 65535:
            raise ValueError
    except ValueError:
        raise ImproperlyConfigured('POSTGRES_PORT must be a valid port.') from None
    options = {'connect_timeout': bounded(env, 'POSTGRES_CONNECT_TIMEOUT', 5, 1, 30), 'sslmode': sslmode,
               'options': '-c statement_timeout={} -c lock_timeout={} -c idle_in_transaction_session_timeout={}'.format(
                   bounded(env, 'POSTGRES_STATEMENT_TIMEOUT_MS', 15000, 1000, 600000),
                   bounded(env, 'POSTGRES_LOCK_TIMEOUT_MS', 5000, 100, 60000),
                   bounded(env, 'POSTGRES_IDLE_TRANSACTION_TIMEOUT_MS', 60000, 1000, 600000))}
    if env.get('POSTGRES_SSLROOTCERT'):
        options['sslrootcert'] = str(Path(env['POSTGRES_SSLROOTCERT']).expanduser())
    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env['POSTGRES_DB'], 'USER': env['POSTGRES_USER'],
        'PASSWORD': env.get('POSTGRES_PASSWORD', ''), 'HOST': env['POSTGRES_HOST'],
        'PORT': str(port), 'CONN_MAX_AGE': bounded(env, 'POSTGRES_CONN_MAX_AGE', 0, 0, 300), 'CONN_HEALTH_CHECKS': True,
        'OPTIONS': options,
    }
