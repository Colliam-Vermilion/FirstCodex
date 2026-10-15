"""Verify delivered originals after independently fetching the result branch.

This does not download from publishers. A manifest with no files is NOT a pass.
Paths are relative to the project directory, never an old cloud-machine path.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root = args.project.resolve()
    manifest = root / 'methods/audit/current_original_files_manifest_utf8.csv'
    with manifest.open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    results = []
    for row in rows:
        result = {'id': row['原记录ID'], 'role': row['文件角色（正文或SI）'], 'verified': False}
        relative = Path(row['相对保存路径'])
        path = (root / relative).resolve()
        if relative.is_absolute() or root not in path.parents:
            result['error'] = 'Manifest path must stay inside this project'
        elif not path.is_file():
            result['error'] = 'Original bytes missing'
        else:
            digest = hashlib.sha256()
            with path.open('rb') as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    digest.update(chunk)
            result['verified'] = digest.hexdigest() == row['SHA256'] and path.stat().st_size == int(row['字节数'])
            if not result['verified']:
                result['error'] = 'SHA256 or byte count mismatch'
        results.append(result)
    passed = sum(r['verified'] for r in results)
    report = {'manifest_files': len(rows), 'verified_files': passed,
              'original_bytes_available': bool(rows) and passed == len(rows),
              'checks': results, 'publisher_retrieval_performed': False}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if rows and passed == len(rows) else (2 if not rows else 1)


if __name__ == '__main__':
    raise SystemExit(main())
