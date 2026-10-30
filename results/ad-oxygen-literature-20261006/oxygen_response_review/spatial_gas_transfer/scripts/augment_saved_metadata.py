"""Reuse only already-linked, locally saved PubMed XML; zero API calls."""
import json,xml.etree.ElementTree as ET
from pathlib import Path
T=Path(__file__).resolve().parents[1];R=T.parents[3]
def main():
 p=T/'saved_author_sources.json';cache=json.loads(p.read_text())
 needed={r['pmid'] for r in json.loads((T/'candidate_records.json').read_text()) if r.get('pmid')}
 source_paths=sorted({r['source_path'] for r in cache.values()});added=[]
 for source in source_paths:
  root=ET.parse(R/source).getroot()
  for a in root.findall('.//PubmedArticle'):
   pmid=a.findtext('./MedlineCitation/PMID')
   if pmid not in needed or pmid in cache:continue
   names=[]
   for n in a.findall('./MedlineCitation/Article/AuthorList/Author'):
    if n.findtext('CollectiveName'):names.append(n.findtext('CollectiveName'))
    elif n.findtext('LastName'):names.append(n.findtext('LastName')+', '+(n.findtext('ForeName') or n.findtext('Initials') or ''))
   if not names:continue
   pmcid=next((n.text for n in a.findall('./PubmedData/ArticleIdList/ArticleId') if n.attrib.get('IdType')=='pmc'),None)
   cache[pmid]={'authors':names,'source_path':source,'pmcid':pmcid};added.append(pmid)
 p.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'already_saved_sources_parsed':len(source_paths),'author_entries_now':len(cache),'added_from_local_XML':len(added),'new_network_calls':0}))
if __name__=='__main__':main()
