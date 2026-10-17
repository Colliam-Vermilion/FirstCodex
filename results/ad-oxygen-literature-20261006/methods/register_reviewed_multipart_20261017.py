"""Register a manually reviewed, complete set of university thesis PDF parts.

An item is not complete because its cover alone downloaded. Each group requires
all source-declared parts, reviewed identities, expected page counts and SHA256.
No merged PDF is created; university supplied bytes remain the originals.
"""
from pathlib import Path
import recovery_20261017 as r
import continue_records_20261017 as c


def run():
    decisions=r.load(r.RUN/'multipart_identity_reviews_20261017.json',{})
    for id,decision in decisions.items():
        if not decision.get('manually_approved_complete_group'):continue
        parts=r.load(r.RUN/(id+'_multipart_downloads.json'),[])
        metadata=r.load(r.RUN/(id+'_public_item_metadata.json'))['metadata']
        expected=metadata['digital']['file']
        assert len(parts)==len(expected)==7
        assert {x['doc_id'] for x in parts}=={x['doc_id'] for x in expected}
        for part in parts:
            path=r.ROOT/part['path']
            if not path.exists():
                a=next(a for a in r.load(r.ASSETS,[]) if a['record_id']==id and a['sha256']==part['sha256'] and r.present(a))
                path=r.path_for(a)
            assert r.sha(path.read_bytes())==decision['approved_sha256_by_filename'][part['original_filename']]==part['sha256']
            doc=r.fitz.open(path)
            assert len(doc)==part['pages']
            assert all(page.get_text() is not None for page in doc)
        held=[]
        for n,part in enumerate(parts,1):
            existing=next((a for a in r.load(r.ASSETS,[]) if a['record_id']==id and a['sha256']==part['sha256'] and r.present(a)),None)
            if existing:held.append(existing);continue
            source=r.ROOT/part['path']
            a=c.store(id,'main',id+'_'+part['original_filename'],source.read_bytes(),part['source_url'],
                'University archived 2015 MSc thesis; complete set of 7 original PDF parts; use together in listed order',
                {'multipart_group':id+'.university_thesis.2015','multipart_part_index':n,'multipart_part_count':7,
                 'multipart_group_complete_and_reviewed':True,'identity_review_20261017':decision,
                 'original_filename':part['original_filename']})
            source.unlink();held.append(a)
        assets=r.load(r.ASSETS,[])
        for a in assets:
            if a['record_id']==id and a['role']=='main':a['preferred_for_record']=a['sha256']==parts[0]['sha256']
        r.save(r.ASSETS,assets)
        decision['applied_asset_ids']=[a['asset_id'] for a in held]
        print(id,'complete reviewed original parts',len(held),flush=True)
    r.save(r.RUN/'multipart_identity_reviews_20261017.json',decisions)
    c.reconcile_supplementary()
    c.checkpt('Register complete university thesis PDF sets and reconcile SI partial success')


if __name__=='__main__':run()
