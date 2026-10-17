"""Inspect actual PDF hyperlinks; reject cited papers' SI as target attachments."""
from pathlib import Path
from urllib.parse import urlsplit
import io, re, zipfile
import recovery_20261017 as r
import continue_records_20261017 as c


def run():
    c.ready();assets=r.load(r.ASSETS,[]);links=[];seen=set()
    for a in assets:
        if a['role']!='main' or not r.present(a):continue
        doc=r.fitz.open(r.path_for(a))
        for n,page in enumerate(doc,1):
            for link in page.get_links():
                url=link.get('uri','')
                if not re.search(r'mmc\d|moesm|supplement|suppl_file|_si_|[-_]s00\d|figshare|zenodo|dataverse|datadryad',url,re.I):continue
                if (a['record_id'],url) in seen:continue
                seen.add((a['record_id'],url));links.append({'record_id':a['record_id'],'source_asset_id':a['asset_id'],'pdf_page':n,'url':r.safe_url(url),'link_bbox':list(link.get('from',[]))})
    report=r.load(r.RUN/'supplementary_check.json',{})
    out=r.ROOT/'original_files/repository_followups_20261017';worker=c.BoundedRetriever(r.ROOT,out,'pdf_declared_supplement',workers=1)
    for item in links:
        id=item['record_id'];meta=r.load(r.ROOT/'papers'/id/'metadata.json');url=item['url']
        match=re.search(r'/doi/suppl/(10\.[^/]+/.+?)/suppl_file/',url,re.I) or re.search(r'doi.org/(10\.[^/]+/.+?)/SUPPL_FILE/',url,re.I)
        if not match:continue
        if c.normalized(match[1])!=c.normalized(meta['doi']):
            item['association']='cited different DOI; not a target attachment';continue
        item['association']='Own article DOI matches explicit SI hyperlink embedded in verified main PDF'
        name=Path(urlsplit(url).path).name
        if any(a['record_id']==id and a['role']=='supplementary' and a['original_filename'].lower()==name.lower() and r.present(a) for a in assets):
            item['status']='existing_original_reused';continue
        if url.startswith('http://'):url='https://'+url[7:]
        record=report[id];record.setdefault('publisher_source_status',record['status'])
        record.setdefault('pdf_declared_attachments',[])
        if not any(x['filename']==name for x in record['pdf_declared_attachments']):record['pdf_declared_attachments'].append({'filename':name,'source_url':url,'source_pdf_sha256':next(a['sha256'] for a in assets if a['asset_id']==item['source_asset_id']),'pdf_page':item['pdf_page']})
        result=worker.get(id,url)
        if result and result[0].startswith(b'PK'):
            data,actual,mime=result
            with zipfile.ZipFile(io.BytesIO(data)) as z:assert z.testzip() is None
            path=out/'si_candidates'/id/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
            item.update(status='downloaded_candidate_requires_content_association_review',candidate_path=str(path.relative_to(r.ROOT)),sha256=r.sha(data),size_bytes=len(data),source_url=actual)
            record.update(status='identity_review_required',reason='Explicit own-PDF SI link downloaded; content association pending review')
        else:
            item['status']='access_failed';record.update(status='access_failed',reason='Explicit own-PDF SI hyperlink did not return verified attachment bytes')
        print(id,item['status'],flush=True)
    r.save(r.RUN/'pdf_embedded_supplement_link_candidates.json',links)
    r.save(r.RUN/'supplementary_check.json',report)
    c.checkpt('Persist exact supplementary links embedded in verified PDFs and source outcomes')


if __name__=='__main__':run()
