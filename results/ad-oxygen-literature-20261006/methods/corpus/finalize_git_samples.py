"""Apply a completed independent Git readback receipt to sample persistence metadata."""
from pathlib import Path
from urllib.parse import quote
import argparse,json,re
from audit_library import dump,write_csv


def finalize(p):
    report=json.loads((p/'inventory/github_delivery_readback.json').read_text());commit=report['remote_commit']
    if not report['all_remote_payload_SHA_and_sizes_passed'] or not re.fullmatch(r'[0-9a-f]{40}',commit):raise ValueError('Verified immutable Git receipt required')
    files=json.loads((p/'inventory/extracted_files.json').read_text())
    for row in files:
        row['sample_git_commit']=commit if row['published_sample'] else ''
        row['download_url']='https://github.com/Colliam-Vermilion/FirstCodex/blob/'+commit+'/results/ad-oxygen-literature-20261006/'+quote(row['relative_path'],safe='/') if row['published_sample'] else ''
        if row['published_sample']:row['storage_status']='git_remote_SHA_readback_verified'
    dump(p/'inventory/extracted_files.json',files);write_csv(p/'inventory/extracted_files_utf8.csv',files)
    assets=json.loads((p/'inventory/assets.json').read_text())
    sample_ids={row['asset_id'] for row in files if row['published_sample']}
    for a in assets:
        if a['asset_id'] in sample_ids:a['extraction']['sample_git_readback_commit']=commit;a['extraction']['sample_storage_status']='git_remote_SHA_readback_verified'
    dump(p/'inventory/assets.json',assets);write_csv(p/'inventory/assets_utf8.csv',assets)
    for id in {row['record_id'] for row in files if row['published_sample']}:
        target=p/'papers'/id/'metadata.json';meta=json.loads(target.read_text());meta['assets']=[a for a in assets if a['record_id']==id];dump(target,meta)
    print(json.dumps({'new_sample_files_durable_verified':sum(r['published_sample'] for r in files),'readback_commit':commit,'old_54_original_status_unchanged':True}))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--project',type=Path,default=Path(__file__).resolve().parents[2]);finalize(ap.parse_args().project.resolve())
