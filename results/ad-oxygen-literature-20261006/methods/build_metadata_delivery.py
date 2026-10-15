"""Build the metadata delivery ZIP; original binary files remain in the Git tree.

Run after updating all current tables and audits. GitHub's whole-branch Download ZIP
is the separate delivery that includes committed original files.
"""
from pathlib import Path
import hashlib
import json
import zipfile


def main():
    root = Path(__file__).resolve().parent.parent
    target = root / 'ad_oxygen_literature_final.zip'
    files = []
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path == target or '__pycache__' in path.parts or path.suffix == '.pyc':
            continue
        rel = path.relative_to(root)
        if rel.parts[0] == 'original_files' and rel.as_posix() not in ('original_files/README.md', 'original_files/ATTRIBUTION_utf8.csv'):
            continue
        files.append(path)
    temporary = target.with_suffix('.zip.tmp')
    with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as bundle:
        for path in files:
            bundle.write(path, path.relative_to(root).as_posix())
    with zipfile.ZipFile(temporary) as bundle:
        assert bundle.testzip() is None
        assert len(bundle.infolist()) == len(files)
        for path in files:
            assert hashlib.sha256(bundle.read(path.relative_to(root).as_posix())).digest() == hashlib.sha256(path.read_bytes()).digest()
    temporary.replace(target)
    print(json.dumps({'metadata_members': len(files), 'original_binary_members': 0,
                      'size_bytes': target.stat().st_size, 'each_member_sha_verified': True}))


if __name__ == '__main__':
    main()
