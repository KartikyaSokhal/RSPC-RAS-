"""ID-preserving import into a newly migrated, disposable local PostgreSQL DB.

Uses concrete fields, including auto-created M2M models, rather than fixtures that
regenerate through-table IDs or auto_now timestamps. Never calls model save hooks.
"""
import datetime
import hashlib
import json
import uuid
from decimal import Decimal

from django.apps import apps
from django.db import connections, models, transaction
from django.db.migrations.recorder import MigrationRecorder


def transfer_models():
    tables = {model._meta.db_table: model for model in apps.get_models(include_auto_created=True)
              if model._meta.managed and not model._meta.proxy}
    tables['django_migrations'] = MigrationRecorder.Migration
    return dict(sorted(tables.items()))


def canonical(value):
    if isinstance(value, datetime.datetime):
        if value.tzinfo:
            value = value.astimezone(datetime.timezone.utc)
        return value.isoformat()
    if isinstance(value, (datetime.date, datetime.time, uuid.UUID, Decimal)):
        return str(value)
    if isinstance(value, (bytes, memoryview)):
        return bytes(value).hex()
    raise TypeError('Unsupported field type in transfer verification.')


def table_inventory(alias, table_models=None):
    result = {}
    for table, model in (table_models or transfer_models()).items():
        fields = model._meta.local_concrete_fields
        names = [field.attname for field in fields]
        digest = hashlib.sha256()
        count = 0
        for row in model._base_manager.using(alias).order_by('pk').values_list(*names).iterator():
            digest.update(json.dumps(row, default=canonical, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
            digest.update(b'\n')
            count += 1
        result[table] = {'count': count, 'sha256': digest.hexdigest(), 'columns': names}
    return result


def assert_disposable_target(connection):
    config = connection.settings_dict
    if (connection.vendor != 'postgresql' or not config['NAME'].startswith('prepal_rehearsal_')
            or config['HOST'] not in ('127.0.0.1', 'localhost', '::1')):
        raise ValueError('Refusing transfer outside a disposable local rehearsal database.')


def reset_and_verify_sequences(source_alias='source_copy', target_alias='default'):
    target = connections[target_alias]
    assert_disposable_target(target)
    with connections[source_alias].cursor() as source:
        source.execute('SELECT name, seq FROM sqlite_sequence')
        counters = dict(source.fetchall())
    verified = {}
    with target.cursor() as cursor:
        for table, model in transfer_models().items():
            if not isinstance(model._meta.pk, models.AutoField):
                continue
            high = max(counters.get(table, 0), model._base_manager.using(source_alias).aggregate(value=models.Max('pk'))['value'] or 0)
            cursor.execute('SELECT pg_get_serial_sequence(%s, %s)', [table, model._meta.pk.column])
            sequence = cursor.fetchone()[0]
            if not sequence:
                raise ValueError('Expected PostgreSQL identity sequence is missing.')
            cursor.execute('SELECT setval(%s::regclass, %s, %s)', [sequence, max(1, high), high > 0])
            cursor.execute('SELECT nextval(%s::regclass)', [sequence])
            if cursor.fetchone()[0] != high + 1:
                raise ValueError('PostgreSQL sequence would reuse an existing or historical ID.')
            cursor.execute('SELECT setval(%s::regclass, %s, %s)', [sequence, max(1, high), high > 0])
            verified[table] = high
    return verified


def verify_sequences(expected, target_alias='default'):
    """Read-only comparison, also usable after a native pg_dump/pg_restore rehearsal."""
    target = connections[target_alias]
    assert_disposable_target(target)
    table_models = transfer_models()
    with target.cursor() as cursor:
        for table, high in expected.items():
            cursor.execute('SELECT pg_get_serial_sequence(%s, %s)', [table, table_models[table]._meta.pk.column])
            sequence = cursor.fetchone()[0]
            cursor.execute('SELECT n.nspname, c.relname FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE c.oid=%s::regclass', [sequence])
            schema, name = cursor.fetchone()
            qualified = target.ops.quote_name(schema) + '.' + target.ops.quote_name(name)
            cursor.execute('SELECT last_value, is_called FROM ' + qualified)
            if cursor.fetchone() != (max(1, high), high > 0):
                raise ValueError('Restored PostgreSQL sequence differs from the verified source high-water mark.')
    return len(expected)


def transfer(source_alias='source_copy', target_alias='default'):
    source, target = connections[source_alias], connections[target_alias]
    assert_disposable_target(target)
    if source.vendor != 'sqlite' or '?mode=ro' not in str(source.settings_dict['NAME']):
        raise ValueError('Transfer source must be a read-only migrated SQLite copy.')
    source_history = MigrationRecorder(source).applied_migrations()
    target_history = MigrationRecorder(target).applied_migrations()
    if set(source_history) != set(target_history):
        raise ValueError('Source and target must have genuinely applied the same migrations.')
    table_models = transfer_models()
    before = table_inventory(source_alias, table_models)
    scaffold = {'auth_permission', 'django_content_type', 'django_migrations'}
    for table, model in table_models.items():
        if table not in scaffold and model._base_manager.using(target_alias).exists():
            raise ValueError('Refusing import into a populated target.')
    with transaction.atomic(using=target_alias), target.cursor() as cursor:
        cursor.execute('SET CONSTRAINTS ALL DEFERRED')
        # Only migration-generated metadata in a fresh isolated target is replaced.
        # Both DBs already ran migrations; preserve the source recorder IDs/dates.
        for table in ('auth_permission', 'django_content_type', 'django_migrations'):
            cursor.execute('DELETE FROM ' + target.ops.quote_name(table))
        for table, model in table_models.items():
            fields = model._meta.local_concrete_fields
            names = [field.attname for field in fields]
            columns = ', '.join(target.ops.quote_name(field.column) for field in fields)
            placeholders = ', '.join(['%s'] * len(fields))
            sql = f'INSERT INTO {target.ops.quote_name(table)} ({columns}) VALUES ({placeholders})'
            batch = []
            for row in model._base_manager.using(source_alias).order_by('pk').values_list(*names).iterator():
                batch.append([field.get_db_prep_save(value, connection=target) for field, value in zip(fields, row)])
                if len(batch) >= 250:
                    cursor.executemany(sql, batch)
                    batch.clear()
            if batch:
                cursor.executemany(sql, batch)
        target.check_constraints()
        after = table_inventory(target_alias, table_models)
        if before != after:
            raise ValueError('Transferred fields, records or primary keys do not match.')
    from django.contrib.contenttypes.models import ContentType
    ContentType.objects.clear_cache()
    return {'tables': before, 'rows': sum(table['count'] for table in before.values()),
            'sequences': reset_and_verify_sequences(source_alias, target_alias),
            'target_migrations_before_import': [
                {'app': record.app, 'name': record.name, 'applied': canonical(record.applied)}
                for _, record in sorted(target_history.items())
            ],
            'foreign_keys_verified': True, 'migration_history_preserved': True}
