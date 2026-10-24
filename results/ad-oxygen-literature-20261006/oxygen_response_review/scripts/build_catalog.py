#!/usr/bin/env python3
"""Build cumulative catalog without changing the AD library or human decisions."""
import csv, hashlib, html, json, re, unicodedata, xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parent

def normtitle(t):return ''.join(c for c in unicodedata.normalize('NFKD',html.unescape(t)).casefold() if c.isalnum())
def doi(x):return re.sub(r'^(?:https?://(?:dx\.)?doi.org/|doi\s*:\s*)','',x or '',flags=re.I).strip().lower().rstrip('.')
def text(e):return ''.join(e.itertext()) if e is not None else ''
def plain(s):return re.sub('<[^>]+>',' ',html.unescape(s or '')).strip()
def dump(path,obj):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def csvout(path,rows,fields=None):
 if not rows and not fields:return
 fields=fields or list(dict.fromkeys(k for r in rows for k in r))
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fields);w.writeheader()
  for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items() if k in fields})

def parse_pubmed(path):
 for a in ET.fromstring(path.read_bytes()).findall('PubmedArticle'):
  art=a.find('MedlineCitation/Article'); ids={x.attrib.get('IdType'):text(x) for x in a.findall('PubmedData/ArticleIdList/ArticleId')}
  ab=[{'label':x.attrib.get('Label',''),'text':text(x),'location':f'Abstract/AbstractText[{i+1}]'} for i,x in enumerate(art.findall('Abstract/AbstractText'))]
  pub=art.find('Journal/JournalIssue/PubDate'); yr=pub.findtext('Year') or (re.search(r'\d{4}',pub.findtext('MedlineDate') or '').group() if re.search(r'\d{4}',pub.findtext('MedlineDate') or '') else '')
  authors=[(x.findtext('LastName','')+', '+x.findtext('ForeName','')).strip(', ') or x.findtext('CollectiveName','') for x in art.findall('AuthorList/Author')]
  yield {'title':text(art.find('ArticleTitle')),'doi':doi(ids.get('doi','')),'pmid':a.findtext('MedlineCitation/PMID',''),'pmcid':ids.get('pmc',''),'year':yr,'journal':art.findtext('Journal/Title',''),'authors':authors,'publication_types':[text(x) for x in art.findall('PublicationTypeList/PublicationType')],'abstract':'\n'.join((x['label']+': ' if x['label'] else '')+x['text'] for x in ab),'abstract_sections':ab,'url':'https://pubmed.ncbi.nlm.nih.gov/'+a.findtext('MedlineCitation/PMID','')+'/','source':'PubMed','query_id':path.name.split('_')[0],'raw_path':str(path.relative_to(ROOT))}

def run():
 oldscreen={r['id']:r for r in json.loads((ROOT/'screening.json').read_text())} if (ROOT/'screening.json').exists() else {}
 master=list(csv.DictReader((PROJECT/'final_results/ad_oxygen_download_review_utf8.csv').open(encoding='utf-8-sig')))
 rows=[]
 for r in master:
  rows.append({'id':r['稳定记录ID'],'title':r['完整题名'],'doi':doi(r['DOI']),'pmid':r['PMID'],'year':r['正式发表年份'],'journal':r['期刊'],'authors':r['作者'].split('; '),'abstract':r['摘要'],'source':'Original AD library','query_id':'OLD554','old_library_ids':[r['稳定记录ID']],'old_ad_classification':r['最终分类'],'old_human_classification':r.get('人工最终分类',''),'raw_path':'../final_results/ad_oxygen_download_review_utf8.csv','url':r['文献链接'],'original_fulltext_paths':r.get('当前正文全部原件路径',''),'original_document_type':r.get('文献类型','')})
 for p in sorted((ROOT/'raw/pubmed').glob('*_fetch_*.xml')):rows.extend(parse_pubmed(p))
 # Trace/targeted records are kept apart from date-limited discovery.
 for p in sorted((ROOT/'raw/trace').glob('*_fetch_*.xml')):rows.extend(parse_pubmed(p))
 for p in sorted((ROOT/'raw/crossref').glob('C*_search.json')):
  for r in json.loads(p.read_text())['message']['items']:
   d=r.get('published',r.get('issued',{})).get('date-parts',[[]])[0]
   rows.append({'title':plain(' '.join(r.get('title',[]))),'doi':doi(r.get('DOI','')),'year':str(d[0]) if d else '', 'journal':' '.join(r.get('container-title',[])),'authors':[(a.get('family','')+', '+a.get('given','')).strip(', ') for a in r.get('author',[])],'abstract':plain(r.get('abstract','')),'publication_types':[r.get('type','')],'source':'Crossref','query_id':p.stem.split('_')[0],'raw_path':str(p.relative_to(ROOT)),'url':r.get('URL','')})
 for p in sorted((ROOT/'raw/openalex').glob('*_page_*.json')):
  for r in json.loads(p.read_text())['results']:
   inv=r.get('abstract_inverted_index') or {}; pos={i:w for w,ii in inv.items() for i in ii}
   rows.append({'title':r.get('display_name',''),'doi':doi(r.get('doi','')),'pmid':(r.get('ids',{}).get('pmid') or '').rstrip('/').split('/')[-1],'openalex_id':r['id'],'year':str(r.get('publication_year','')),'journal':((r.get('primary_location') or {}).get('source') or {}).get('display_name',''),'authors':[a['author']['display_name'] for a in r.get('authorships',[])],'abstract':' '.join(pos[i] for i in sorted(pos)),'publication_types':[r.get('type','')],'source':'OpenAlex','query_id':p.stem.split('_')[0],'raw_path':str(p.relative_to(ROOT)),'url':r.get('doi') or r['id']})
 catalog={}; indexes=defaultdict(dict); matching=[]; conflicts=[]
 for n,r in enumerate(rows,1):
  keys=[('doi',doi(r.get('doi',''))),('pmid',r.get('pmid','')),('title',normtitle(r.get('title','')))]
  match=set()
  for kind,key in keys:
   if key and key in indexes[kind]:
    candidate=indexes[kind][key]; c=catalog[candidate]
    if kind=='title' and c.get('doi') and r.get('doi') and c['doi']!=r['doi']:
     conflicts.append({'input':n,'candidate':candidate,'reason':'same normalized title, conflicting DOI','doi1':c['doi'],'doi2':r['doi']});continue
    if kind=='title' and c.get('year') and r.get('year') and abs(int(c['year'])-int(r['year']))>1:continue
    match.add(candidate)
  if r.get('id') and r['id'] not in catalog:
   target=r['id']
   catalog[target]={'id':target,'sources':[],'queries':[],'provenance':[],'old_library_ids':[],'screening_stage':'未开始','screening_decision':'未判断','screening_reason':'新范围尚未逐篇判断；旧AD排除结论不继承'}
   if match:conflicts.append({'input':n,'candidate':sorted(match),'preserved_existing_id':target,'reason':'pre-existing AD identity alias; both old IDs retained'})
  elif match:
   target=sorted(match,key=lambda x:(not x.startswith('R'),x))[0]
   if len(match)>1:conflicts.append({'input':n,'candidate':sorted(match),'reason':'multiple identity matches retained as aliases; not deleting existing AD IDs'})
  else:
   ident=next((kind+':'+key for kind,key in keys if key),'input:'+str(n))
   target=r.get('id') or 'OR-'+hashlib.sha256(ident.encode()).hexdigest()[:12].upper()
   catalog[target]={'id':target,'sources':[],'queries':[],'provenance':[],'old_library_ids':[],'screening_stage':'未开始','screening_decision':'未判断','screening_reason':'新范围尚未逐篇判断；旧AD排除结论不继承'}
  c=catalog[target]
  for k,v in r.items():
   if k in ('source','query_id','id','old_library_ids'):continue
   if v and not c.get(k):c[k]=v
  for field,val in [('sources',r['source']),('queries',r['query_id'])]:
   if val not in c[field]:c[field].append(val)
  for oldid in r.get('old_library_ids',[]):
   if oldid not in c['old_library_ids']:c['old_library_ids'].append(oldid)
  c['provenance'].append({'source':r['source'],'query_id':r['query_id'],'raw_path':r['raw_path'],'source_pmid':r.get('pmid',''),'source_doi':r.get('doi','')})
  if r.get('abstract_sections'):c['abstract_sections']=r['abstract_sections']
  for kind,key in keys:
   if key:indexes[kind].setdefault(key,target)
  matching.append({'input_index':n,'source':r['source'],'query_id':r['query_id'],'doi':r.get('doi',''),'pmid':r.get('pmid',''),'title':r.get('title',''),'assigned_id':target,'old_library_ids':c['old_library_ids'],'match_keys':[k for k,key in keys if key and indexes[k].get(key)==target],'raw_path':r['raw_path']})
 for c in catalog.values():
  c['early_key_study']= bool(c.get('year') and c['year'].isdigit() and int(c['year'])<2012)
  if c['id'] in oldscreen:c.update(oldscreen[c['id']])
 values=sorted(catalog.values(),key=lambda x:x['id'])
 dump(ROOT/'catalog.json',values);csvout(ROOT/'literature_master_utf8.csv',values)
 csvout(ROOT/'dedup_input_mapping_utf8.csv',matching);dump(ROOT/'identity_conflicts.json',conflicts)
 dump(ROOT/'dedup_summary.json',{'original_master_records':len(master),'source_input_rows_including_old':len(rows),'retrieval_input_rows':len(rows)-len(master),'unique_catalog_records':len(values),'unique_returned_records':sum(any(q!='OLD554' for q in c['queries']) for c in values),'original_ids_linked_to_returns':sum(bool(c['old_library_ids']) and any(q!='OLD554' for q in c['queries']) for c in values),'conflicts_for_review':len(conflicts),'old_records_preserved_in_source':True})
 print(json.dumps(json.loads((ROOT/'dedup_summary.json').read_text()),ensure_ascii=False))

if __name__=='__main__':run()
