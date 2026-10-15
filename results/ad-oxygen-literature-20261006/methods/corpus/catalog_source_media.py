"""Map already-retained image members to XML references, without extracting copies."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib
from audit_library import dump,sha,write_csv


def catalog(p,root):
    assets=json.loads((p/'inventory/assets.json').read_text());rows=[];transport={a['record_id']:a for a in assets if a['role']=='transport_archive'}
    for a in assets:
        if a['role']!='evidence_xml':continue
        directory=root/'papers'/a['record_id']/'extracted'/a['asset_id'];media=json.loads((directory/'referenced_media.json').read_text());bundle=transport.get(a['record_id']);members=[]
        if bundle:members=json.loads((root/'papers'/a['record_id']/'extracted'/bundle['asset_id']/'archive_members.json').read_text())
        for ref in media:
            name=Path(ref.get('href') or '').name;matches=[m for m in members if Path(m['path']).name==name or Path(m['path']).stem==name or Path(m['path']).stem==Path(name).stem]
            rows.append({'record_id':a['record_id'],'source_xml_asset_id':a['asset_id'],'xpath':ref['xpath'],'declared_href':ref['href'],'binary_status':'stored_in_transport_archive' if matches else 'external_reference_not_cached','transport_asset_id':bundle['asset_id'] if matches else None,'matching_members':matches,'image_or_video_content_indexed':False})
    dump(p/'inventory/source_media_map.json',rows)
    # Physical acquisition files include duplicates, candidates and run evidence. They
    # are inventoried separately, never silently accepted as additional paper bodies.
    known={a['sha256']:a for a in assets};physical=[]
    old_reviews=json.loads((p/'methods/audit/current_extra_body_manual_validation_20261015.json').read_text());rejected={r.get('sha256') for r in old_reviews.get('manual_validations',[]) if str(r.get('decision','')).startswith('reject')}
    roots=[Path('/workspace/library-files/ad-oxygen-fulltexts'),Path('/workspace/library-files/ad-oxygen-current-run'),Path('/workspace/library-files/ad-oxygen-supplements'),p/'original_files']
    for base in roots:
        if not base.exists():continue
        for f in sorted(base.rglob('*')):
            if not f.is_file():continue
            digest=sha(f);a=known.get(digest);classification='accepted_asset_or_same_SHA_copy' if a else 'rejected_wrong_document_not_an_original' if digest in rejected else 'unverified_or_unselected_candidate' if f.suffix.lower() in ['.pdf','.docx','.xlsx','.zip','.skp'] else 'run_or_identity_evidence_not_counted_as_original'
            physical.append({'path':str(f),'size_bytes':f.stat().st_size,'sha256':digest,'classification':classification,'accepted_asset_id':a['asset_id'] if a else ''})
    write_csv(p/'inventory/physical_acquisition_files_utf8.csv',physical)
    report={'physical_files':len(physical),'physical_bytes_including_duplicates_and_run_evidence':sum(r['size_bytes'] for r in physical),'physical_classifications':dict(Counter(r['classification'] for r in physical)),'mapped_xml_graphic_references':len(rows),'graphic_reference_statuses':dict(Counter(r['binary_status'] for r in rows)),'transport_images_are_body_figures_not_automatically_official_SI':True,'no_new_network_or_file_copy':True}
    dump(p/'inventory/physical_and_media_audit.json',report);print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--project',type=Path,default=Path(__file__).resolve().parents[2]);ap.add_argument('--root',type=Path,required=True);a=ap.parse_args();catalog(a.project.resolve(),a.root.resolve())
