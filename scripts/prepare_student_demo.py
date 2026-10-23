"""Prepare a NEW isolated review environment; never migrate an existing database."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    args=parser.parse_args(); path=args.directory.expanduser().absolute()
    if path.exists() or path.is_symlink():
        parser.error('Choose a NEW nonsymlink absolute directory; existing destinations are preserved.')
    path=path.resolve()
    if path.exists(): parser.error('Existing destinations are preserved.')
    path.mkdir(parents=True,mode=0o700,exist_ok=False)
    for filename,kind in [('.student-demo.json','prepal-student-review-v2'),('.sample-demo.json','prepal-academic-sample-v1')]:
        marker=path/filename;marker.write_text(json.dumps({'kind':kind,'state':'preparing'}));marker.chmod(0o600)
    env={**os.environ,'PREPAL_DEMO_ROOT':str(path),'DJANGO_SETTINGS_MODULE':'core.student_demo_settings',
         'PYTHON_DOTENV_DISABLED':'1','GEMINI_API_KEY':'','GOOGLE_API_KEY':''}
    for command in [('migrate','--noinput'),('create_sample_content',),('create_review_content',)]:
        subprocess.run([sys.executable,'manage.py',*command],cwd=ROOT/'backend',env=env,check=True)
    print(f'Private student review demo ready: {path}. New academic content is NOT published. Mock Tutor only.')

if __name__=='__main__':main()
