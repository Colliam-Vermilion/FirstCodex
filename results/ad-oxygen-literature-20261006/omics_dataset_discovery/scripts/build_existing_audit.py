import json,re,collections
from common import ROOT,dump,now
articles=json.loads((ROOT/'existing_target_articles.json').read_text());links=json.loads((ROOT/'existing_project_links.json').read_text());ev=json.loads((ROOT/'existing_target_evidence.json').read_text());ass=json.loads((ROOT/'project_assessments.json').read_text());rows=[]
for a in articles:
 ps=sorted(p for p,v in links.items() if any(d['record_id']==a['record_id'] for d in v));e=[x for x in ev if x['record_id']==a['record_id']];statements=[x for x in e if any(s in x['evidence_kind'] for s in ['数据声明','数据可用','可索取'])]
 code=None;availability=''
 if ps:code=min(ass[p]['availability_code'] for p in ps);availability='；'.join(ass[p]['availability'] for p in ps)
 elif a['record_id']=='R13274':code=4;availability='明确raw metatranscriptomic reads可索取；无公开编号，需用途说明/数据协议，未代联系'
 elif a['data_access_status'].startswith('5 '):code=5;availability='仅泛指数据可索取；是否包含raw reads未明确'
 elif a['record_id']=='R13817':availability='特殊限制：作者明确无权分享；不能认定可索取，尚无公开reads入口'
 elif a['record_id']=='R13904':availability='待确认：MG方法明确，但16S编号不能替代MG编号；末尾无数据声明与方法矛盾'
 else:availability='待确认：目标测序方法已确认，未定位目标reads编号或相关数据声明'
 rows.append({'paper_id':a['record_id'],'title':a['title'],'year':a['year'],'journal':a['journal'],'doi':a['doi'],'existing_literature_id':a['record_id'],'newly_discovered_paper':False,'project_accessions':ps,'omics':a['conclusion'].replace('确认',''),'availability_code':code,'availability':availability,'source_method_evidence_reused':a['method_summary'],'oxygen_supply':a['oxygen_supply'],'substrate':a['substrate'],'treatment_control':a['treatment_control'],'sequencing_sample_count_as_reported':a['sequencing_sample_count'],'biological_replicates_as_reported':a['biological_replicates'],'platform_as_reported':a['platform'],'evidence_ids':a['evidence_ids'],'source_locations':a['reviewed_locations'],'statements_with_locations':statements,'method_source_fulltext_previously_reviewed':True,'this_round_fulltext_redownloaded':False,'data_generation_mode':a.get('data_generation_mode') or ('既有数据再分析' if a['record_id']=='R12985' else '本研究产生')})
dump(ROOT/'existing_articles_availability_audit.json',rows)
print('audited',len(rows),'project_linked',sum(bool(r['project_accessions']) for r in rows),'no_project',sum(not r['project_accessions'] for r in rows))
