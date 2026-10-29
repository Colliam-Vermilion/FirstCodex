#!/usr/bin/env python3
"""Validate README navigation only; blanket replacement/folding is retired.

Since the 2026-10-25 correction this command NEVER writes a README.
Add future research to the corresponding visible stage or a new section.
The prior generator remains available in Git commit 9208deddd.
"""
from pathlib import Path
import re
P=Path(__file__).resolve().parents[1]
def run():
 project=re.sub(r'<details\b.*?</details\s*>','',(P/'README.md').read_text(),flags=re.I|re.S)
 for i in range(1,8):assert f'id="stage-{i}"' in project,f'missing stage {i}'
 assert 'results/ad-oxygen-literature-20261006/README.md' in re.sub(r'<details\b.*?</details\s*>','',(P.parents[1]/'README.md').read_text(),flags=re.I|re.S)
 print('README navigation valid; no files written. Seven research stages remain visible.')
if __name__=='__main__':
 import runpy
 migration=P/'branch_migration/oxygen_response_mechanisms_20261029/validate_migration.py'
 if migration.exists():runpy.run_path(str(migration),run_name='__main__')
 else:run()
