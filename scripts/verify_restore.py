"""python scripts/verify_restore.py BACKUP_DIR NEW_RESTORE_DIR. Never overwrites."""
from pathlib import Path
import argparse
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from content.services.backups import restore

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('backup_directory')
    parser.add_argument('new_restore_directory')
    args = parser.parse_args()
    print(json.dumps(restore(args.backup_directory, args.new_restore_directory)))
