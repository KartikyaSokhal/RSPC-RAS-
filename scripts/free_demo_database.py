"""Explicit operator CLI. No startup hooks, resets, fallback or secret output."""
import argparse
import json
import os
import secrets
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'backend'))
from content.services.free_demo_database import prepare,apply_roles,grant_runtime,create_backup
from content.services.postgres_ops import load_environment, write_private
from content.services.free_demo_database import target


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=('prepare','roles','initialize','verify','grant-runtime','backup','student-credentials','student-login'))
    p.add_argument('--config',type=Path,required=True)
    p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--confirm-database',required=True)
    p.add_argument('--local-test',action='store_true')
    p.add_argument('--apply',action='store_true')
    p.add_argument('--output',type=Path)
    p.add_argument('--certificate',type=Path)
    p.add_argument('--pg-bin',type=Path)
    p.add_argument('--openssl',default='openssl')
    a=p.parse_args()
    try:
        cfg=load_environment(a.config)
        if cfg.get('POSTGRES_DB')!=a.confirm_database:raise ValueError('Target confirmation mismatch.')
        if a.action=='student-credentials':
            target(cfg,a.local_test)
            destination=a.directory.expanduser().resolve()
            if (a.directory.is_symlink() or destination.is_relative_to(ROOT)
                    or not destination.is_dir() or destination.stat().st_mode & 0o077):
                raise ValueError('Use an existing owner-only directory outside application Git.')
            write_private(destination/'student-credentials.json',json.dumps({'username':'prepal-demo-'+secrets.token_hex(12),'password':secrets.token_urlsafe(40)})+'\n')
            result={'private_credentials_prepared':True,'live_database_changed':False}
        elif a.action=='prepare':result=prepare(a.config,a.directory,a.local_test)
        elif a.action=='backup':result=create_backup(a.config,a.output,a.certificate,a.pg_bin,a.openssl,a.local_test)
        elif a.action in ('roles','grant-runtime'):
            if not a.apply:raise ValueError('Explicit --apply required for privilege writes.')
            result=apply_roles(a.config,a.directory,a.local_test) if a.action=='roles' else grant_runtime(a.directory,a.local_test)
        else:
            if a.action=='initialize' and not a.apply:raise ValueError('Explicit --apply required for schema/data writes.')
            # Clear inherited configuration; only the protected explicit file selects the DB.
            for k in list(os.environ):
                if k.startswith(('POSTGRES_','PG','PREPAL_','DJANGO_')) or k in ('DATABASE_ENGINE','DATABASE_URL','SECRET_KEY'):
                    os.environ.pop(k,None)
            os.environ.update(cfg,PYTHON_DOTENV_DISABLED='1',DJANGO_SETTINGS_MODULE='core.free_demo_ops_settings')
            if (cfg.get('PREPAL_FREE_DEMO_LOCAL_TEST')=='1')!=a.local_test:raise ValueError('Explicit local rehearsal confirmation mismatch.')
            import django
            django.setup()
            from django.core.management import call_command
            options={'confirm_database':a.confirm_database,'local_test':a.local_test}
            if a.action=='student-login':
                runtime=load_environment(a.directory/'runtime.env')
                if any(runtime[k]!=cfg[k] for k in ('POSTGRES_HOST','POSTGRES_PORT','POSTGRES_DB')):
                    raise ValueError('Runtime/operator target mismatch.')
                options.update(credentials_file=str(a.directory/'student-credentials.json'),runtime_role=runtime['POSTGRES_USER'],apply=a.apply)
                call_command('prepare_public_demo_login',**options)
                return
            if a.action=='initialize':options.update(apply=True,staff_password_file=str(a.directory/'staff-password.txt'))
            call_command('initialize_free_demo',**options)
            return
        print(json.dumps(result))
    except Exception:
        raise SystemExit('Free-demo operation refused/failed. No secrets emitted. Verify protected inputs, target identity, role permissions and empty/known state.') from None


if __name__=='__main__':main()
