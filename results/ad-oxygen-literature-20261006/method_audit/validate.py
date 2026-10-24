#!/usr/bin/env python3
"""Offline checks of methods, protected results, raw-query counts and local links."""
import ast,csv,datetime,hashlib,json,re,subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote,urlsplit
P=Path(__file__).resolve().parents[1];A=P/'method_audit';M=P/'oxygen_response_review';D=P/'omics_dataset_discovery'
def read(p):return json.loads(p.read_text())
def run():
 protected=read(A/'protected_sources.json')['files']
 for x in protected:assert hashlib.sha256((P/x['path']).read_bytes()).hexdigest()==x['sha256'],x['path']
 docs=[P/'README.md',M/'README.md',D/'README.md']+list((M/'methods').glob('*.md'))+list((D/'methods').glob('*.md'))+[A/'README.md']
 errors=[];links=0;external=[]
 for f in docs:
  if not f.exists():continue
  text=f.read_text().split('<!-- HISTORICAL_README_BEGIN -->')[0]
  # Current methods/navigation links; archived historical text deliberately preserved verbatim.
  for target in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)',text):
   target=target.strip('<>');u=urlsplit(target)
   if u.scheme in ['https','http','mailto']:external.append(target);continue
   dest=(f.parent/unquote(u.path)).resolve() if u.path else f.resolve();links+=1
   if dest==A/'validation.json':continue
   if not dest.exists():errors.append({'document':str(f.relative_to(P)),'target':target})
   elif u.fragment and dest.suffix=='.md' and u.fragment.startswith('query-'):
    if 'id="'+u.fragment+'"' not in dest.read_text():errors.append({'document':str(f.relative_to(P)),'missing_anchor':target})
 assert not errors,errors
 # Exact executed query counts and corresponding raw responses, not future API totals.
 for root,expected in [(M,25),(D,29)]:
  qs=read(root/'methods/queries.json');assert len(qs)==expected
  for q in qs:
   for raw in q['raw_paths']:assert (root/raw).is_file(),raw
   assert q['query_verbatim']
   n=0
   for raw in q['raw_paths']:
    path=root/raw
    if root==M:
     if q['database']=='PubMed' and '_fetch_' in raw:
      tree=ET.parse(path);n+=len(tree.findall('.//PubmedArticle'))+len(tree.findall('.//PubmedBookArticle'))
     elif q['database']=='Crossref':n+=len(read(path)['message']['items'])
     elif q['database']=='OpenAlex':n+=len(read(path).get('results',[]))
    elif q['query_id'].startswith('E'):n+=len(read(path))
    elif q['query_id'].startswith(('N','P')) and path.read_text().lstrip().startswith('<'):
     tree=ET.parse(path);n+=len(tree.findall('.//DocumentSummary')) if q['query_id'].startswith('N') else len(tree.findall('.//PubmedArticle'))+len(tree.findall('.//PubmedBookArticle'))
   if q['query_id']!='GSA-availability':assert n==q['retrieved_records'],(q['query_id'],n,q['retrieved_records'])
 if sum(q['retrieved_records'] for q in read(M/'methods/queries.json'))!=1147:raise AssertionError('mechanism returned rows')
 ds=read(D/'methods/queries.json');assert sum(q['retrieved_records'] for q in ds if q['query_id'].startswith('E'))==4291
 # Source registration confirms three later Europe PMC bodies despite old availability prose.
 ep=read(M/'methods/source_summary_discrepancy.json');assert len(ep['subsequent_saved_successes'])==3 and all(x['body_present'] for x in ep['subsequent_saved_successes'])
 for name,expected in [('flow_membership_utf8.csv',1536)]:
  with (M/'methods'/name).open(encoding='utf-8-sig',newline='') as f:assert len(list(csv.DictReader(f)))==expected
 for name,expected in [('selected60_provenance_utf8.csv',60),('project_pool_membership_utf8.csv',487),('already_audited_queue_overlap_utf8.csv',12)]:
  with (D/'methods'/name).open(encoding='utf-8-sig',newline='') as f:assert len(list(csv.DictReader(f)))==expected
 a=read(A/'audit_summary.json');s=read(D/'summary.json');f=a['mechanism_sets'];assert f['union_catalog']==1536 and f['priority364']==364 and f['pending479']==479
 assert s['reviewed_projects']==69 and s['reviewed_public_community_projects']==38 and s['A_B_public_runs']==349 and s['C_public_runs']==333
 assert s['potential_oxygen_control_comparison_records']==16 and s['confirmed_oxygen_control_comparisons']==12 and s['comparisons_metadata_only_pending_methods']==4
 assert len(read(D/'remaining_paper_queue.json'))==2228 and read(D/'methods/queue_identity_audit.json')['overlap_count']==12
 # Compile only the new offline audit scripts; never run original search/screen/render code.
 for script in A.glob('*.py'):ast.parse(script.read_text())
 for f in [P/'README.md',M/'README.md',D/'README.md']:
  original=subprocess.check_output(['git','show','0f9eeec20:'+str(f.relative_to(P.parents[1]))],cwd=P.parents[1],text=True)
  archived=f.read_text().split('<!-- HISTORICAL_README_BEGIN -->',1)[1].split('<!-- HISTORICAL_README_END -->',1)[0]
  assert original.strip()==archived.strip(),str(f)
 result={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':True,'new_database_queries':0,'new_screening_decisions':0,'protected_existing_result_files_unchanged':len(protected),'current_relative_links_resolved':links,'external_links_policy':'仅记录/核语法；本轮不重新请求数据库或出版商。GitHub文档另以认证API读回核验。','external_link_count':len(external),'mechanism_executed_queries':25,'dataset_executed_queries':28,'GSA_unexecuted_entry_test':1,'mechanism_returned_input_rows':1147,'ENA_returned_rows_with_cross_query_repeats':4291,'set_membership_verified':True,'saved_dataset_queue_overlap_old22':12,'existing_result_tables_and_progress_not_rewritten':True,'historical_READMEs':'原内容在相同文件折叠保留，相对链接不因搬迁改变；历史外链未重测'}
 (A/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':
 if 'id="stage-1"' in (P/'README.md').read_text():
  import runpy
  runpy.run_path(str(A/'readme_restoration/validate.py'),run_name='__main__')
 else:run()
