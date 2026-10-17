"""Recover one declared missing attachment via its publisher's public CDN.

The article PII is from the preserved exact-DOI source audit; the attachment
filename is from its complete JATS. Accept only the historical original SHA256.
"""
import io, json, re, zipfile
from pathlib import Path
import recovery_20261017 as r
import continue_records_20261017 as c


def run():
    c.ready();id='R07238'
    expected=next(a for a in r.load(r.ASSETS,[]) if a['record_id']==id and a['role']=='supplementary' and a['original_filename']=='mmc1.docx')
    if r.present(expected):return
    audit=r.load(r.ROOT/'methods/audit/scansci_sourcewise_results.json')[id]
    pii=next(re.search(r'/pii/(S\d{16})/',u).group(1) for u in audit['visited'] if re.search(r'/pii/(S\d{16})/',u))
    declarations=r.load(r.RUN/'supplementary_check.json')[id]['declared_attachments']
    assert any(x['filename']=='mmc1.docx' for x in declarations)
    url='https://ars.els-cdn.com/content/image/1-s2.0-'+pii+'-mmc1.docx'
    out=r.ROOT/'original_files/repository_followups_20261017'
    worker=c.BoundedRetriever(r.ROOT,out,'exact_item_followup',workers=1)
    response=worker.get(id,url)
    result={'record_id':id,'source_url':url,'expected_sha256':expected['sha256'],'retrieved':False,'source':'Exact recorded PII plus explicitly declared attachment basename; official publisher CDN'}
    if response:
        data,actual,mime=response
        if r.sha(data)==expected['sha256'] and len(data)==int(expected['size_bytes']):
            with zipfile.ZipFile(io.BytesIO(data)) as z:assert z.testzip() is None
            c.store(id,'supplementary','mmc1.docx',data,actual,'Official publisher supplementary Word document; exact historical SHA256')
            result.update(retrieved=True,size_bytes=len(data),sha256=r.sha(data))
        else:result.update(response_is_expected_original=False,content_type=mime,response_bytes=len(data))
    r.save(r.RUN/'R07238_official_cdn_attachment_probe.json',result)
    c.reconcile_supplementary()
    c.checkpt('Persist declared attachment CDN recovery and exact historical-byte check')


if __name__=='__main__':run()
