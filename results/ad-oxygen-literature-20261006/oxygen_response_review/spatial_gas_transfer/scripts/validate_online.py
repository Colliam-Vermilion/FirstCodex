"""Verify retrieval completeness, stable old identities, exports and old prose."""
import json,re,subprocess,hashlib,xml.etree.ElementTree as E,csv
from pathlib import Path
from openpyxl import load_workbook
from prepare import T,R,read,dump,now
BASE='ea021e273eaeb5957c979bf4d53ed5b651c5cdec'
def main():
 checks={};issues=[];qrows=[]
 for q in read(T/'online_search_log.json'):
  ids=[];counts=[]
  if q['database']=='PubMed':
   for f in q.get('fetches',[]):ids += [a.findtext('./MedlineCitation/PMID') for a in E.parse(T/f['raw_path']).findall('.//PubmedArticle')]
  else:
   for p in q['pages']:
    d=read(T/p['raw_path']);ids += [x['id'] for x in d['results']];counts.append(d['meta']['count'])
  valid=q['status']=='completed' and len(ids)==len(set(ids))==q['retrieved_records']==q['reported_count']
  qrows.append({'query_id':q['query_id'],'records':len(ids),'unique_ids':len(set(ids)),'reported_count':q['reported_count'],'all_page_reported_counts':counts,'complete_without_duplicate_or_cap':valid})
  if not valid:issues.append(q['query_id']+' completeness mismatch')
 checks['all12_complete']=len(qrows)==12 and all(q['complete_without_duplicate_or_cap'] for q in qrows)
 traces=[]
 for tr in read(T/'online_citation_trace_log.json'):
  ids=[r['id'] for p in tr.get('pages',[]) for r in read(T/p['raw_path'])['results']];ok=len(ids)==len(set(ids))==tr['retrieved_records']==tr['reported_count'] and tr['status']=='completed';traces.append({'seed_key':tr['seed_key'],'direction':tr['direction'],'records':len(ids),'valid':ok})
  if not ok:issues.append(str(tr))
 checks['all10_first_generation_citation_routes_complete']=len(traces)==10 and all(x['valid'] for x in traces)
 rows=read(T/'literature_master.json');C={r['id']:r for r in rows};base=read(T/'checkpoints/pre_online_233_master.json')
 checks['unique_cumulative_ids']=len(rows)==len(C)
 checks['original233_id_and_scope_decisions_preserved']=len(base)==233 and all(r['id'] in C and C[r['id']]['scope_decision']==r['scope_decision'] for r in base)
 checks['original233_no_new_initial_screenings']=not(set(r['id'] for r in base)&set(r['id'] for r in read(T/'online_screening.json')))
 with (T/'literature_master_utf8.csv').open(encoding='utf-8-sig') as f:cr=list(csv.DictReader(f))
 checks['csv_json_ids_match']={r['id'] for r in cr}==set(C)
 counts={}
 for name in ['spatial_gas_transfer_candidates.ris','spatial_gas_transfer_reviewed.ris']:
  t=(T/name).read_text();starts=t.count('TY  - ');ends=t.count('ER  -');counts[name]=starts;checks[name+'_balanced']=starts==ends
 checks['candidates_ris_count_matches']=counts['spatial_gas_transfer_candidates.ris']==len(rows)
 wb=load_workbook(T/'spatial_gas_transfer_cumulative.xlsx',read_only=True,data_only=True);checks['excel_master_count_matches']=wb['文献与专题筛选'].max_row-1==len(rows);wb.close()
 def old(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=R).decode()
 current=(R/'README.md').read_text().splitlines();pos=0;preserved=True
 for line in old('README.md').splitlines():
  if not line.strip():continue
  try:pos=current.index(line,pos)+1
  except ValueError:preserved=False;issues.append('old homepage line missing: '+line[:90]);break
 checks['every_prior_nonempty_homepage_line_preserved_in_order']=preserved
 for path in ['scientific_guide/literature_proposition_map.json','scientific_guide/propositions.json']:
  before=json.loads(old(path));after=read(R/path);aset={json.dumps(x,ensure_ascii=False,sort_keys=True) for x in after};checks[path+'_old_entries_preserved']=all(json.dumps(x,ensure_ascii=False,sort_keys=True) in aset for x in before)
 checks['all_seeds_verified']=len(read(T/'seed_audit.json'))==5 and all(x['external_verification_state']=='verified' and x['title_normalized_matches'] for x in read(T/'seed_audit.json'))
 checks['all_read_fulltexts_have_real_methods_and_results']=len(read(T/'online_fulltext_evidence.json'))==read(T/'online_increment_summary.json')['new_fulltexts_methods_results_verified'] and all(any('METHOD' in (s['heading'] or '').upper() for s in read(T/f['sections_path'])) and any('RESULT' in (s['heading'] or '').upper() for s in read(T/f['sections_path'])) for f in read(T/'online_fulltext_evidence.json'))
 for r in read(T/'online_original_file_register.json'):
  checks[r['pmcid']+'_canonical_original_hash_matches']=hashlib.sha256((R/r['path']).read_bytes()).hexdigest()==r['sha256']
 # Check only new local links; pre-existing sparse paths verified by tree membership.
 tree=set(subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=R).decode().splitlines());bad=[]
 for file in [R/'README.md',R/'scientific_guide/README.md',T/'README.md']+list((T/'evidence').glob('SG-*.md')):
  for target in re.findall(r'\]\(([^)\s]+)\)',file.read_text()):
   if target.startswith(('http:','https:','#','mailto:')):continue
   target=target.split('#')[0];dest=(file.parent/target).resolve()
   if dest.exists():continue
   try:rel=dest.relative_to(R).as_posix()
   except ValueError:bad.append({'file':str(file),'target':target});continue
   if rel not in tree:bad.append({'file':str(file.relative_to(R)),'target':target})
 checks['checked_markdown_links_resolve']=not bad
 errors=[k for k,v in checks.items() if not v];issues+=errors
 report={'updated_utc':now(),'base_commit':BASE,'checks':checks,'query_details':qrows,'citation_details':traces,'ris_counts':counts,'link_errors':bad,'issues':issues,'passed':not issues,'limits':'Does not substitute for scientific peer review or certify all unreviewed records. Original scope decisions preserved; S02 reading/parameter depth upgraded with provenance.'}
 dump(T/'online_validation.json',report);print(json.dumps(report,ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
if __name__=='__main__':main()
