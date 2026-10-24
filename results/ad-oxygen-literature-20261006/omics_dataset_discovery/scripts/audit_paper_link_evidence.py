"""Locate accession mentions; distinguish data-bank fields and cited datasets."""
import json,xml.etree.ElementTree as ET
from common import ROOT,dump
def run():
 papers=json.loads((ROOT/'new_associated_papers.json').read_text());ev=[]
 for p in papers:
  found=[]
  for raw in p.get('source_paths',[]):
   path=ROOT/raw
   if not path.exists():continue
   try:tree=ET.parse(path)
   except ET.ParseError:continue
   for article in tree.findall('.//PubmedArticle'):
    if article.findtext('./MedlineCitation/PMID')!=str(p.get('pmid')):continue
    def walk(n,loc):
     for acc in p.get('project_accessions',[]):
      if acc in (n.text or ''):found.append({'paper_id':p['paper_id'],'project_id':acc,'source_path':raw,'location':loc,'verbatim':n.text,'relation':'官方DataBank字段关联，研究产生/复用仍按方法' if '/DataBank/' in loc else '参考文献中的数据引用；不能据此认定本研究产生该项目' if '/ReferenceList/' in loc else '其他字段提及；研究归属待核'})
     for c in n:walk(c,loc+'/'+c.tag)
    walk(article,'PubmedArticle')
  if found:p['accession_mention_locations']=found;ev+=found
  if found and all('/ReferenceList/' in x['location'] for x in found):p['relation_caution']='仅定位数据参考文献；保留关联候选，不能据此将项目当本文独立产生或断定重复归档'
 dump(ROOT/'new_associated_papers.json',papers);dump(ROOT/'paper_project_mention_evidence.json',ev)
 print('exact accession fields',len(ev),'reference-only papers',sum(bool(p.get('relation_caution')) for p in papers))
if __name__=='__main__':run()
