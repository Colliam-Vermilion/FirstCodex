"""Normalize complete returned pages, retain identity/provenance, never rescreen old 233."""
import json,hashlib,re,xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from prepare import T,read,dump,doi,title,now

def pm(a,path,origin):
 c=a.find('MedlineCitation');article=c.find('Article'); ids={x.get('IdType'):x.text for x in a.findall('./PubmedData/ArticleIdList/ArticleId')}
 return {'pmid':c.findtext('PMID'),'doi':doi(ids.get('doi')),'pmcid':ids.get('pmc'),'title':''.join(article.find('ArticleTitle').itertext()),'abstract':'\n'.join((x.get('Label','')+': ' if x.get('Label') else '')+''.join(x.itertext()) for x in article.findall('./Abstract/AbstractText')),'authors':[x.findtext('LastName','')+', '+x.findtext('ForeName',x.findtext('Initials','')) if x.find('LastName') is not None else x.findtext('CollectiveName','') for x in article.findall('./AuthorList/Author')], 'year':article.findtext('./Journal/JournalIssue/PubDate/Year') or article.findtext('./ArticleDate/Year'),'journal':article.findtext('./Journal/Title'),'publication_types':[x.text for x in article.findall('./PublicationTypeList/PublicationType')],'source':{'origin':origin,'raw_path':path,'record_locator':'PubmedArticle[PMID='+c.findtext('PMID')+']'},'abstract_kind':'complete official PubMed AbstractText fields; not full text'}
def oa(a,path,origin):
 inv=a.get('abstract_inverted_index') or {};words={i:w for w,idx in inv.items() for i in idx};abstract=' '.join(words[i] for i in sorted(words))
 return {'oa_id':a['id'],'doi':doi(a.get('doi')),'pmid':(a.get('ids',{}).get('pmid') or '').split('/')[-1],'title':a.get('title') or a.get('display_name') or '', 'abstract':abstract,'authors':[x.get('author',{}).get('display_name','') for x in a.get('authorships',[])],'year':a.get('publication_year'),'date':a.get('publication_date'),'journal':((a.get('primary_location') or {}).get('source') or {}).get('display_name'),'publication_types':[a.get('type')],'locations':a.get('locations',[]),'source':{'origin':origin,'raw_path':path,'record_locator':a['id']},'abstract_kind':'OpenAlex reconstructed complete supplied inverted index; may be absent'}

def main():
 records=[];counts={}
 for l in read(T/'online_search_log.json'):
  counts[l['query_id']]=l['retrieved_records']
  if l['database']=='PubMed':
   for f in l.get('fetches',[]):
    records.extend(pm(a,f['raw_path'],l['query_id']) for a in ET.parse(T/f['raw_path']).findall('.//PubmedArticle'))
  else:
   for page in l['pages']:
    records.extend(oa(a,page['raw_path'],l['query_id']) for a in read(T/page['raw_path'])['results'])
 for l in read(T/'online_citation_trace_log.json'):
  for page in l.get('pages',[]):records.extend(oa(a,page['raw_path'],l['seed_key']+'_'+l['direction']) for a in read(T/page['raw_path'])['results'])
 for l in read(T/'seed_pubmed_results.json'):
  records.extend(pm(a,l['metadata_path'],l['seed_key']) for a in ET.parse(T/l['metadata_path']).findall('.//PubmedArticle'))
 extra='raw/online/extra_EuropePMC/europepmc-response.json'
 for a in read(T/extra)['resultList']['result']:
  records.append({'pmid':a['id'] if a.get('source')=='MED' else '', 'doi':doi(a.get('doi')),'title':a.get('title',''),'abstract':re.sub('<[^>]+>',' ',a.get('abstractText','')),'authors':[a.get('authorString','')],'year':a.get('pubYear'),'journal':(a.get('journalInfo') or {}).get('journal',{}).get('title'),'source':{'origin':'extra_EuropePMC_broad_first25_of417','raw_path':extra,'record_locator':a.get('source','')+':'+a['id']},'abstract_kind':'complete returned EuropePMC core abstract field; absent if not supplied'})
 # Full prior 13,817-result library plus current mechanism+omics identity registry.
 snapshot=T/'checkpoints/pre_online_global_identity_registry.json'
 if snapshot.exists():global_old=read(snapshot)
 else:
  original=read(Path('/workspace/ad-oxygen-review/merged.json'));global_old=[{k:r.get(k) for k in ['id','doi','pmid','title']} for r in original];dump(snapshot,global_old)
 registry=read(T/'local_identity_registry.json');oldrows=read(T/'literature_master.json');oldids={x['id'] for x in oldrows}
 # repeated run must retain baseline 233 identities, independent of appended online rows
 baseline=[x['id'] for x in read(T/'checkpoints/pre_online_233_master.json')] if (T/'checkpoints/pre_online_233_master.json').exists() else read(T/'progress.json')['completed_initial_screen_ids'];oldids=set(baseline)
 identity={};index={};conflicts=[]
 for r in global_old+registry:
  identity[r['id']]=r
  for k,v in [('doi',doi(r.get('doi'))),('pmid',str(r.get('pmid') or '')),('title',title(r.get('title')))]:
   if v:index[k,v]=r['id'] # current canonical registry wins over older original IDs
 merged={};mapping=[]
 for r in records:
  keys=[('doi',doi(r.get('doi'))),('pmid',str(r.get('pmid') or '')),('title',title(r.get('title')))];target=None;basis=None
  for k,v in keys:
   if not v or (k,v) not in index:continue
   candidate=index[k,v];old=identity.get(candidate) or merged[candidate]
   if k=='title' and doi(old.get('doi')) and r.get('doi') and doi(old['doi'])!=r['doi']:
    conflicts.append({'incoming':r,'candidate_id':candidate,'reason':'same normalized title, conflicting DOI; do not merge by title'});continue
   target=candidate;basis=k;break
  if target is None:
   key=r.get('doi') or r.get('pmid') or title(r['title']) or r.get('oa_id');assert key,'record lacks a stable identity';target='SG-'+hashlib.sha256(key.encode()).hexdigest()[:12].upper();basis='new deterministic DOI/PMID/title hash'
  item=merged.setdefault(target,{'id':target,**{k:v for k,v in r.items() if k!='source'},'online_source_links':[],'existed_in_global_library':target in identity,'already_spatial_initial_screened':target in oldids})
  if r['source'] not in item['online_source_links']:item['online_source_links'].append(r['source'])
  # Prefer official PubMed complete abstract over OpenAlex when both available.
  if r.get('abstract') and (not item.get('abstract') or r['source']['raw_path'].endswith('.xml')):
   item['abstract']=r['abstract'];item['abstract_kind']=r['abstract_kind'];item['preferred_abstract_source']=r['source']
  for k in ['doi','pmid','pmcid','authors','year','journal','locations','oa_id']:
   if not item.get(k) and r.get(k):item[k]=r[k]
  mapping.append({'assigned_id':target,'matched_by':basis,'source':r['source']})
  for k,v in keys:
   if v:index[k,v]=target
 unique=list(merged.values());dump(T/'online_records.json',unique);dump(T/'online_dedup_mapping.json',mapping);dump(T/'online_identity_conflicts.json',conflicts)
 stats={'updated_utc':now(),'query_return_counts':counts,'original12_returned_total_with_duplicates':sum(counts.values()),'all_returned_records_including_citations_seeds_extra_with_duplicates':len(records),'unique_online_identities':len(unique),'matched_global_existing_identities':sum(r['existed_in_global_library'] for r in unique),'new_to_global_library':sum(not r['existed_in_global_library'] for r in unique),'matched_original233':sum(r['already_spatial_initial_screened'] for r in unique),'new_to_spatial_view':sum(not r['already_spatial_initial_screened'] for r in unique),'identity_conflicts':len(conflicts),'full_global_dedup_source':'prior 13817 merged.json plus 3752 current mechanism/omics identity registry; original exclusions not reversed','screening_complete':False}
 dump(T/'online_merge_summary.json',stats);print(json.dumps(stats,ensure_ascii=False))
 # Human/model reading packet: new PubMed topical records first, no status assigned by words.
 pack=[r for r in unique if not r['already_spatial_initial_screened'] and any(x['origin'] in ['Q01','Q02','Q03','Q04','Q05','Q06','Q07','Q08','S01','S03','S04','S05'] for x in r['online_source_links'])]
 dump(T/'online_pubmed_reading_packet.json',pack)
 print('new PubMed/seed packet',len(pack))
if __name__=='__main__':main()
