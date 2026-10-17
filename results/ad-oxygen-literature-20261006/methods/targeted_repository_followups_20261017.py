"""Follow public file controls on already identified articles, without searching.

Only links exposed by the saved target article or its exact repository bitstream
are followed. New PDFs remain candidates until a separate identity/body review.
"""
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup
import json, re
import recovery_20261017 as r
import continue_records_20261017 as c


def run():
    c.ready()
    out=r.ROOT/'original_files/repository_followups_20261017'
    worker=c.BoundedRetriever(r.ROOT,out,'exact_item_followup',workers=1)
    assets=r.load(r.ASSETS,[])
    def metadata(id,url,label):
        result=worker.get(id,url)
        if not result:return None
        try:value=json.loads(result[0])
        except (ValueError,UnicodeDecodeError):return None
        r.save(r.RUN/(id+'_'+label+'.json'),{'source_url':r.safe_url(result[1]),'metadata':value})
        return value
    candidates=r.load(r.RUN/'repository_followup_candidates.json',{})
    # The publisher exposes this download form in the already verified page.
    for a in assets:
        if a['role']!='evidence_html' or a['record_id']!='R09240' or not r.present(a):continue
        if a['record_id'] in candidates:continue
        soup=BeautifulSoup(r.path_for(a).read_text(),'html.parser')
        forms=soup.select('form[action]')
        for form in forms:
            action=urljoin(a['source_url'],form['action'])
            if '/deliver/fulltext/' not in action or '.pdf' not in urlsplit(action).path:continue
            response=worker.get(a['record_id'],action)
            if response and response[0].lstrip().startswith(b'%PDF'):
                content,actual,mime=response
                dest=out/'pdf_candidates'/a['record_id']/(r.sha(content)+'.pdf');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(content)
                candidates[a['record_id']]={'path':str(dest.relative_to(r.ROOT)),'source_url':actual,'sha256':r.sha(content),'size_bytes':len(content),'status':'pending_manual_identity_and_version'}
            break
    # Inspect only the ORIGINAL bundle belonging to the exact held bitstream.
    for id in ['R10492','R10250','R10714','R13911']:
        source=next(a for a in assets if a['record_id']==id and a['role']=='main' and r.present(a))
        match=re.search(r'/bitstreams/([0-9a-f-]{36})',source['source_url'])
        if not match:continue
        base='https://dspace.lib.cranfield.ac.uk/server/api/core/bitstreams/'+match[1]
        bundle=metadata(id,base+'/bundle','repository_original_bundle')
        if not bundle:continue
        link=bundle.get('_links',{}).get('bitstreams',{}).get('href')
        if link:
            files=metadata(id,link,'repository_original_bundle_files')
            if files:print(id,'ORIGINAL bundle files',files.get('page',{}).get('totalElements'),flush=True)
    # These two records already point to these public item pages. Their scripts
    # explicitly expose Biblio/detailData/<the same item>, not a catalogue search.
    for id,bibid in [('R13968','77770'),('R13969','77766')]:
        page=next(a for a in assets if a['record_id']==id and a['role']=='evidence_html' and r.present(a))
        html=r.path_for(page).read_text()
        if 'Biblio/detailData/' not in html or bibid not in html:continue
        value=metadata(id,'https://digiverse.chula.ac.th/digital/api/Biblio/detailData/'+bibid,'public_item_metadata')
        if value:
            print(id,'public item metadata keys',list(value)[:20],flush=True)
            parts=[]
            previous=r.load(r.RUN/(id+'_multipart_downloads.json'),[])
            for item in value.get('digital',{}).get('file',[]):
                if item.get('ext')!='pdf' or item.get('is_link')!='0':continue
                old=next((x for x in previous if x['doc_id']==item['doc_id']),None)
                if old and (r.ROOT/old['path']).is_file() and r.sha((r.ROOT/old['path']).read_bytes())==old['sha256']:
                    parts.append(old);continue
                url='https://digiverse.chula.ac.th/digital/api/DownloadDigitalFile/dowload/'+item['doc_id']
                response=worker.get(id,url)
                if not response or not response[0].lstrip().startswith(b'%PDF'):continue
                data,actual,mime=response
                doc=r.fitz.open(stream=data,filetype='pdf');texts=[page.get_text() for page in doc]
                assert len(doc)==int(item['num_page']),'Public item PDF page count differs'
                name=id+'_'+Path(item['file_name_original']).name
                path=out/'pdf_candidates'/id/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
                parts.append({'record_id':id,'doc_id':item['doc_id'],'original_filename':item['file_name_original'],
                    'path':str(path.relative_to(r.ROOT)),'source_url':r.safe_url(actual),'sha256':r.sha(data),
                    'size_bytes':len(data),'pages':len(doc),'native_characters':sum(map(len,texts)),
                    'multipart_status':'candidate_part_pending_group_identity_review'})
                r.save(r.RUN/(id+'_multipart_downloads.json'),parts)
                print(id,'part downloaded',name,len(doc),flush=True)
            r.save(r.RUN/(id+'_multipart_downloads.json'),parts)
    r.save(r.RUN/'repository_followup_candidates.json',candidates)
    c.checkpt('Persist exact-item repository follow-ups and publisher download controls')


if __name__=='__main__':run()
