"""Read ALL stored seed references and forward-match the saved fulltext index.

This is not OpenAlex forward citation retrieval. Source and coverage are explicit.
"""
import json,re,sqlite3,xml.etree.ElementTree as ET
from pathlib import Path
from prepare import T,M,P,R,read,dump,now,SEEDS,title,doi
def main():
 registry=read(T/'local_identity_registry.json');pm={r['pmid']:r['id'] for r in registry if r.get('pmid')};dm={doi(r['doi']):r['id'] for r in registry if r.get('doi')}
 path=P/'omics_dataset_discovery/raw/NCBI/cfc7af329ca2b6a6948e25003e2b6ddc6f91b2e2dc3e867e63108f407191f658.body'
 root=ET.parse(path).getroot();a=next(x for x in root.findall('.//PubmedArticle') if x.findtext('MedlineCitation/PMID')=='17905889')
 back=[]
 for n,r in enumerate(a.findall('PubmedData/ReferenceList/Reference'),1):
  text=' '.join(''.join(r.find('Citation').itertext()).split());ids={x.get('IdType'):x.text for x in r.findall('ArticleIdList/ArticleId')};linked=pm.get(ids.get('pubmed','')) or dm.get(doi(ids.get('doi','')))
  back.append({'trace_id':f'S02-B{n:03d}','seed_id':'ODS-PMID17905889','direction':'backward','source_path':str(path.relative_to(R)),'locator':f'PubmedArticle[PMID=17905889]/PubmedData/ReferenceList/Reference[{n}]','citation_verbatim':text,'pmid':ids.get('pubmed'),'pmcid':ids.get('pmc'),'doi_as_saved':ids.get('doi'),'existing_id':linked,'status':'已有身份可复用，尚待本专题处理' if linked else '原始引文线索；元数据/全文待获取，不当作已纳入或已阅读文章'})
 # Full independent metadata is not invented for bare reference strings.
 dump(T/'backward_citation_trace.json',back)
 db=sqlite3.connect(P/'search.sqlite');cols='record_id,asset_id,source_filename,canonical_source,location,text'
 forward=[];queries=[]
 for sid,d,st in SEEDS:
  query='SELECT '+cols+' FROM chunks WHERE lower(text) LIKE ? OR lower(text) LIKE ?'
  params=['%'+d.lower()+'%','%'+st.lower()[:75]+'%'];rows=list(db.execute(query,params))
  for n,row in enumerate(rows,1):forward.append(dict(zip(cols.split(','),row))|{'trace_id':sid+'-F'+str(n),'seed_key':sid,'direction':'forward_local_index_only','match_rule':'literal DOI or literal first75 title characters; must check actual citation context','not_global_citation_coverage':True})
  queries.append({'seed_key':sid,'sql':query,'parameters':params,'rows_returned':len(rows),'pagination':'完整SQL结果，无LIMIT','source':'既有search.sqlite；不覆盖其建立后全部新合并原件','date_utc':now()})
 cov=db.execute('select count(*),count(distinct record_id),count(distinct asset_id) from chunks').fetchone()
 dump(T/'forward_local_citation_trace.json',forward)
 dump(T/'citation_trace_log.json',{'backward_seed':'ODS-PMID17905889','backward_source':'保存的PubMed完整ReferenceList','backward_returned':len(back),'backward_truncated':False,'forward_source':'search.sqlite，历史全文/附件索引','index_chunks':cov[0],'index_record_ids':cov[1],'index_asset_ids':cov[2],'forward_queries':queries,'forward_rows_returned':len(forward),'online_forward_backward_graph_queries':'尚未执行，API当前403阻断；未将本地结果当作完整前向引文库','other_four_seed_reference_lists':'尚未取得，不从题名补造参考文献'})
 print('Backward references',len(back),'existing links',sum(bool(x['existing_id']) for x in back),'local forward rows',len(forward))
if __name__=='__main__':main()
