#!/usr/bin/env python3
"""Map batch-one source documents to paragraph/page locators; keep originals."""
import hashlib,json,re,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PROJECT=ROOT.parent
PMIDS=['32301184','24222618','38129989','25706146','36083837','33326896','32515155','29725720','37918493','25398869','37382539','38953644','26431975','27663027','33147001','29312168','34409684','38580315','40057977','39608160']
THEMES=['M1_damage','M1_damage','M2_detox','M6_adaptation','M6_recovery','M2_detox','M4_interaction','M4_interaction','M5_spatial','M5_spatial','M2_detox','M2_detox','M3_metabolism','M3_metabolism','M6_recovery','M3_metabolism','M7_conditions','M2_detox','M3_metabolism','M4_interaction']
def run():
 import fitz
 cat=json.loads((ROOT/'catalog.json').read_text());assets=json.loads((PROJECT/'inventory/assets.json').read_text()); reg=[]; batch=[]
 out=ROOT/'evidence_sources';out.mkdir(exist_ok=True)
 for i,(pm,theme) in enumerate(zip(PMIDS,THEMES),1):
  r=next(z for z in cat if z.get('pmid')==pm);rid=r['id'];batch.append({'batch':'B001','order':i,'id':rid,'pmid':pm,'theme_stratum':theme,'selection_rule':'Different mechanisms and environments; mechanistic perturbation/physiology prioritized; includes old AD exclusion R11680 for independent reassessment','title':r['title']})
  f=ROOT/f'raw/pmc_fulltext/F{pm}_jats.xml'; pars=[];kind='abstract';src=r.get('raw_path','');sha=''
  full_xml=f.exists() and ET.fromstring(f.read_bytes()).find('.//body') is not None
  if full_xml:
   root=ET.fromstring(f.read_bytes());kind='JATS';src=str(f.relative_to(ROOT));sha=hashlib.sha256(f.read_bytes()).hexdigest()
   def walk(el,path,section):
    if el.tag=='sec':section='/'.join(x for x in [section,''.join(el.find('title').itertext()) if el.find('title') is not None else 'untitled'] if x)
    if el.tag in ['p','caption','table-wrap','ref']:
     pars.append({'locator':path,'section':section,'text':' '.join(''.join(el.itertext()).split()),'element_type':el.tag})
    counts={}
    for child in el:
     counts[child.tag]=counts.get(child.tag,0)+1;walk(child,path+'/'+child.tag+f'[{counts[child.tag]}]',section)
   walk(root,'/'+root.tag,'')
  elif r['old_library_ids']:
   candidates=[a for a in assets if a.get('record_id') in r['old_library_ids'] and a.get('role')=='fulltext' and a.get('verification_status')=='identity_and_body_structure_verified']
   if candidates:
    a=sorted(candidates,key=lambda a:a.get('canonical_path',''))[0];f=PROJECT/a['canonical_path'];src='../'+a['canonical_path'];sha=hashlib.sha256(f.read_bytes()).hexdigest();kind='PDF'
    with fitz.open(f) as doc:
     pars=[{'locator':f'PDF page {n+1}','section':'PDF page','text':p.get_text(sort=True),'element_type':'page'} for n,p in enumerate(doc)]
  if not pars:
   pubmed_source=next((z['raw_path'] for z in r['provenance'] if z['source']=='PubMed'),None)
   if pubmed_source:src=pubmed_source
   sf=ROOT/src
   if sf.exists() and sf.is_file():sha=hashlib.sha256(sf.read_bytes()).hexdigest()
   pars=[{'locator':z['location'],'section':z['label'] or 'Abstract','text':z['text'],'element_type':'abstract'} for z in r.get('abstract_sections',[]) ] or [{'locator':'Abstract','section':'Abstract','text':r.get('abstract',''),'element_type':'abstract'}]
  obj={'id':rid,'pmid':pm,'doi':r.get('doi',''),'source_kind':kind,'source_path':src,'source_sha256':sha,'official_url':f'https://pmc.ncbi.nlm.nih.gov/articles/{r["pmcid"]}/' if kind=='JATS' else r.get('url',''),'paragraphs':pars}
  dest=out/f'{rid}.json';dest.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8');reg.append({k:v for k,v in obj.items() if k!='paragraphs'})
 (ROOT/'batch_B001_selection.json').write_text(json.dumps(batch,ensure_ascii=False,indent=2));(ROOT/'source_document_register.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2));print([(r['id'],r['source_kind']) for r in reg])
if __name__=='__main__':run()
