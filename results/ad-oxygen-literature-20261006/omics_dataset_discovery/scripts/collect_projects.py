"""Official ENA/SRA metadata only. Never downloads reads."""
import json,xml.etree.ElementTree as ET,time,sys,re
from common import ROOT,dump,now,fetch,getjson,url
ENA='https://www.ebi.ac.uk/ena/portal/api/';NCBI='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
def text(e,path):return ' '.join(e.findtext(path,default='').split())
def ena_fields():
 b,m=fetch(ENA+'returnFields?result=read_run','ENA');available={x.split('\t')[0] for x in b.decode().splitlines()[1:]}
 wanted='run_accession study_accession secondary_study_accession sample_accession secondary_sample_accession experiment_accession study_title sample_title sample_description experiment_title experiment_alias sample_alias scientific_name tax_id library_name library_strategy library_source library_selection library_layout instrument_platform instrument_model read_count base_count fastq_ftp fastq_bytes fastq_md5 submitted_ftp submitted_format submitted_bytes submitted_md5 sra_ftp sra_bytes sra_md5 first_public last_updated pubmed_id center_name'.split();return [x for x in wanted if x in available]
def parse_sra(b):
 root=ET.fromstring(b);rows=[]
 for pkg in root.findall('.//EXPERIMENT_PACKAGE'):
  exp=pkg.find('EXPERIMENT');sam=pkg.find('SAMPLE');study=pkg.find('STUDY')
  if exp is None or sam is None:continue
  ext={n.get('namespace'):n.text for n in sam.findall('./IDENTIFIERS/EXTERNAL_ID')};sid=sam.get('accession');bs=ext.get('BioSample') or sid
  aliases={n.get('namespace'):n.text for n in study.findall('./IDENTIFIERS/EXTERNAL_ID')} if study is not None else {};attributes=[{'tag':text(n,'TAG'),'value':text(n,'VALUE'),'units':text(n,'UNITS')} for n in sam.findall('./SAMPLE_ATTRIBUTES/SAMPLE_ATTRIBUTE')];layout=exp.find('./DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_LAYOUT');platform=exp.find('PLATFORM');platform_name=list(platform)[0].tag if platform is not None and len(platform) else None
  for run in pkg.findall('./RUN_SET/RUN'):
   files=[dict(x.attrib) for x in run.findall('.//SRAFile')]+[dict(x.attrib) for x in run.findall('.//SRA_FILES/SRA_FILE')]
   rows.append({'run_accession':run.get('accession'),'experiment_accession':exp.get('accession'),'sample_accession':bs,'secondary_sample_accession':sid,'sample_alias':sam.get('alias'),'sample_title':text(sam,'TITLE'),'scientific_name':text(sam,'SAMPLE_NAME/SCIENTIFIC_NAME'),'tax_id':text(sam,'SAMPLE_NAME/TAXON_ID'),'sample_attributes':attributes,'study_accession':aliases.get('BioProject'),'secondary_study_accession':study.get('accession') if study is not None else None,'study_title':text(study,'DESCRIPTOR/STUDY_TITLE') if study is not None else None,'study_description':text(study,'DESCRIPTOR/STUDY_ABSTRACT') if study is not None else None,'study_links':[dict(x.attrib,content=x.text) for x in study.findall('.//XREF_LINK/*')] if study is not None else [],'experiment_title':text(exp,'TITLE'),'library_name':text(exp,'DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_NAME'),'library_strategy':text(exp,'DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_STRATEGY'),'library_source':text(exp,'DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_SOURCE'),'library_selection':text(exp,'DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_SELECTION'),'library_layout':list(layout)[0].tag if layout is not None and len(layout) else None,'library_construction_protocol':text(exp,'DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_CONSTRUCTION_PROTOCOL'),'instrument_platform':platform_name,'instrument_model':text(platform,f'{platform_name}/INSTRUMENT_MODEL') if platform_name else None,'read_count':run.get('total_spots'),'base_count':run.get('total_bases'),'sra_run_bytes':run.get('size'),'sra_files':files,'run_published':run.get('published'),'run_is_public':run.get('is_public')})
 return rows
def collect(acc,fields=None):
 dest=ROOT/'project_cache'/acc;done=dest/'collection_status.json'
 if done.exists():return json.loads(done.read_text())
 fields=fields or ena_fields();status={'accession':acc,'checked_utc':now(),'ena_run_count':None,'ncbi_sra_count':None}
 j,m=getjson(url(ENA+'filereport',accession=acc,result='read_run',fields=','.join(fields),format='json',download='false'),'ENA');status['ena_request']=m
 if isinstance(j,list):dump(dest/'ena_runs.json',j);status['ena_run_count']=len(j)
 else:status['ena_parse_error']='not a JSON array'
 time.sleep(.4)
 j,m=getjson(url(NCBI+'esearch.fcgi',db='sra',term=acc,retmode='json',retmax=200,retstart=0),'NCBI');status['ncbi_search_request']=m;ids=[];packages=[]
 if j and 'esearchresult' in j:
  e=j['esearchresult'];count=int(e['count']);status['ncbi_sra_count']=count;ids=e.get('idlist',[])
  for off in range(200,count,200):
   time.sleep(.4);jj,mm=getjson(url(NCBI+'esearch.fcgi',db='sra',term=acc,retmode='json',retmax=200,retstart=off),'NCBI')
   if jj:ids+=jj.get('esearchresult',{}).get('idlist',[])
  status['ncbi_all_search_ids_retrieved']=len(ids)==count;dump(dest/'ncbi_sra_uids.json',ids)
  for off in range(0,len(ids),100):
   time.sleep(.4);b,mm=fetch(url(NCBI+'efetch.fcgi',db='sra',id=','.join(ids[off:off+100]),retmode='xml'),'NCBI')
   if b:
    try:packages+=parse_sra(b)
    except Exception as e:status.setdefault('sra_xml_parse_errors',[]).append(str(e))
  dump(dest/'ncbi_sra_packages.json',packages)
 b,m=fetch('https://www.ebi.ac.uk/ena/browser/api/xml/'+acc,'ENA');status['ena_project_xml_request']=m
 if b:
  (dest/'ena_project.xml').write_bytes(b)
  try:
   x=ET.fromstring(b);status['project_title']=' '.join(x.findtext('.//TITLE',default='').split());status['project_description']=' '.join(x.findtext('.//DESCRIPTION',default='').split());status['project_identifiers']=[{'tag':e.tag,**e.attrib,'value':e.text} for e in x.findall('.//IDENTIFIERS/*')];status['project_publication_fields']=[ET.tostring(e,encoding='unicode') for e in x.findall('.//PUBLICATIONS')+x.findall('.//PROJECT_LINKS')]
  except Exception as e:status['project_parse_error']=str(e)
 status['ncbi_run_count_parsed']=len(packages);dump(done,status);return status
if __name__=='__main__':
 a=sys.argv[1:];fields=ena_fields()
 if not a:a=sorted(json.loads((ROOT/'existing_project_links.json').read_text()))
 for acc in a:
  s=collect(acc,fields);print(acc,'ENA',s['ena_run_count'],'SRA experiments',s['ncbi_sra_count'],'parsed_runs',s.get('ncbi_run_count_parsed'),flush=True);time.sleep(.6)
