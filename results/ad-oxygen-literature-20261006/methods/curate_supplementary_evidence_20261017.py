"""Correct navigation false positives and record explicitly stated data projects.

Project accessions below were reviewed in the downloaded article's own methods
or data availability statement. ENA queries retrieve byte-count metadata only;
no FASTQ or other database content is downloaded.
"""
import csv, io, re
from urllib.parse import urlencode, urlsplit
import recovery_20261017 as r
import continue_records_20261017 as c

REVIEWED={'R09236':'PRJNA1013451','R12985':'PRJNA1013451','R10492':'PRJNA1128434',
          'R13833':'PRJEB11469','R13911':'PRJNA1056946'}


def run():
    c.ready();report=r.load(r.RUN/'supplementary_check.json',{})
    rejected=r.load(r.RUN/'rejected_external_data_link_candidates.json',[])
    for id,record in report.items():
        valid=[]
        for item in record.get('external_data_links',[]):
            host=urlsplit(item['url'].strip()).hostname or ''
            if host in ['scholar.google.com','x.com','twitter.com','www.linkedin.com','www.facebook.com','www.reddit.com','www.mendeley.com','www.wef.org'] or item['url'].strip().startswith('javascript:'):
                evidence={'record_id':id,**item,'rejection_reason':'Reference, social sharing, navigation or global site promotion; not an article data/supplement declaration'}
                if not any(x['record_id']==id and x['url']==item['url'] for x in rejected):rejected.append(evidence)
            else:valid.append(item)
        record['external_data_links']=valid
    r.save(r.RUN/'rejected_external_data_link_candidates.json',rejected)
    out=r.ROOT/'original_files/repository_followups_20261017'
    worker=c.BoundedRetriever(r.ROOT,out,'external_dataset_metadata',workers=1)
    sizes={};links=[]
    for id,accession in REVIEWED.items():
        proof=[]
        for path in (r.ROOT/'papers'/id/'extracted').glob('*/chunks.jsonl'):
            for line in path.read_text().splitlines():
                chunk=r.json.loads(line)
                if accession in chunk['text']:
                    i=chunk['text'].index(accession)
                    proof.append({'source_sha256':chunk['source_sha256'],'location':chunk['location'],
                        'source_asset_id':chunk['asset_id'],'statement':chunk['text'][max(0,i-700):i+700]})
        assert proof,'Reviewed data statement is missing from current parsed sources'
        if accession not in sizes:
            cache=r.RUN/'external_data_size_probes'/(accession+'.tsv')
            query='https://www.ebi.ac.uk/ena/portal/api/filereport?'+urlencode({'accession':accession,'result':'read_run','fields':'run_accession,fastq_bytes','format':'tsv'})
            result=worker.get(id,query) if not cache.exists() else None
            if result and len(result[0])<2*1024*1024:
                cache.parent.mkdir(parents=True,exist_ok=True);cache.write_bytes(result[0])
            info={'size_bytes':None,'size_status':'Public total not established; no database files downloaded','size_metadata_url':query}
            if cache.exists():
                listing=list(csv.DictReader(io.StringIO(cache.read_text()),delimiter='\t'))
                if listing and 'fastq_bytes' in listing[0]:
                    numbers=[int(x) for row in listing for x in row.get('fastq_bytes','').split(';') if x.isdigit()]
                    if numbers:info.update(size_bytes=sum(numbers),size_status='Sum of public ENA FASTQ file byte counts for the full accession/project; may exceed the subset used by this paper',public_run_count=len(listing),size_metadata_path=str(cache.relative_to(r.ROOT)),size_metadata_sha256=r.sha(cache.read_bytes()))
            sizes[accession]=info
        item={'record_id':id,'accession':accession,'url':'https://www.ebi.ac.uk/ena/browser/view/'+accession,
            **sizes[accession],'downloaded':False,'kind':'external_sequencing_database_project',
            'association':'Reviewed own methods/data availability statement; not a reference citation',
            'article_statement_evidence':proof,'automatic_bulk_download_disabled':True}
        record=report[id]
        record['external_data_links']=[x for x in record['external_data_links'] if x.get('accession')!=accession]+[item]
        links.append(item);print(id,accession,item['size_bytes'],flush=True)
    r.save(r.RUN/'external_data_links_20261017.json',links)
    r.writecsv(r.RUN/'external_data_links_utf8.csv',links)
    r.save(r.RUN/'supplementary_check.json',report)
    c.reconcile_supplementary()
    c.checkpt('Preserve corrected supplementary evidence and external database size metadata')


if __name__=='__main__':run()
