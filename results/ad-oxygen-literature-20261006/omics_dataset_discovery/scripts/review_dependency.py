"""Read pinned legacy review inputs without a sibling worktree or network request.

No result files or paper copies are written. The pinned Git object exists in the
inherited full history. For shallow clones see branch_migration/.../README.md.
"""
import hashlib,json,subprocess
from pathlib import Path
PROJECT=Path(__file__).resolve().parents[2]
CONFIG=PROJECT/'branch_migration/oxygen_response_mechanisms_20261029/dependency_sources.json'
def review_bytes(relative):
 config=json.loads(CONFIG.read_text(encoding='utf-8'))
 if relative not in config['files']:raise ValueError('Unregistered review dependency: '+relative)
 path=config['path_prefix']+relative
 try:b=subprocess.check_output(['git','show',config['source_commit']+':'+path],cwd=PROJECT,stderr=subprocess.PIPE)
 except subprocess.CalledProcessError as exc:
  raise RuntimeError('Missing pinned Git history. Fetch the source commit in dependency_sources.json (see migration README); do not recreate or re-search the input.') from exc
 expected=config['files'][relative]
 if len(b)!=expected['bytes'] or hashlib.sha256(b).hexdigest()!=expected['sha256']:
  raise ValueError('Pinned dependency mismatch: '+path)
 return b
def review_json(relative):return json.loads(review_bytes(relative))
if __name__=='__main__':
 config=json.loads(CONFIG.read_text())
 for relative in config['files']:review_bytes(relative)
 print('All %d pinned review dependencies readable; no network, result writes or paper copies.'%len(config['files']))
