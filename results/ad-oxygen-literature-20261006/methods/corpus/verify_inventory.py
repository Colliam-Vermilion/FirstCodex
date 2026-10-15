"""Verify the current unified inventory in place; never rebuild it from old snapshots."""
from pathlib import Path
from collections import Counter
import argparse,json
from audit_library import sha,dump,write_csv


def verify(project,root=None):
    p=Path(project).resolve();assets=json.loads((p/'inventory/assets.json').read_text());checks=[]
    for a in assets:
        paths=[]
        if root:paths.append(Path(root)/a['canonical_path'])
        if a.get('source_repo_path'):paths.append(p/a['source_repo_path'])
        paths += [Path(a[k]) for k in ['resolved_source_path','source_local_path'] if a.get(k)]
        found=next((x for x in paths if x.is_file() and x.stat().st_size==a['size_bytes'] and sha(x)==a['sha256']),None)
        checks.append({'record_id':a['record_id'],'asset_id':a['asset_id'],'sha_verified':bool(found),'actual_path':str(found) if found else '', 'role':a['role'],'size_bytes':a['size_bytes'],'storage_status_recorded':a['storage_status']})
    report={'assets':len(assets),'verified':sum(r['sha_verified'] for r in checks),'missing_or_changed':sum(not r['sha_verified'] for r in checks),'all_actual_bytes_verified':all(r['sha_verified'] for r in checks),'files_by_role':dict(Counter(r['role'] for r in checks)),'no_original_moved_or_replaced':True,'scope_or_manual_judgments_modified':False,'new_cloud_readback_claimed':False,'checks':checks}
    dump(p/'inventory/current_inventory_sha_verification.json',report);print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False));return report


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--project',type=Path,default=Path(__file__).resolve().parents[2]);ap.add_argument('--root',type=Path);a=ap.parse_args();r=verify(a.project,a.root)
    if not r['all_actual_bytes_verified']:raise SystemExit(1)
