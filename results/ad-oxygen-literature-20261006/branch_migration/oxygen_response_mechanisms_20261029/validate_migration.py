#!/usr/bin/env python3
"""Read-only branch-migration checks; no search, result writes or paper rechecks.

Use --report PATH only to save a new migration report, never to overwrite study
results. Works in a sparse independent checkout by checking tracked link targets.
"""
import argparse,ast,csv,datetime,hashlib,json,re,subprocess,sys,zipfile
from pathlib import Path
from urllib.parse import unquote,urlsplit

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
REPO=PROJECT.parents[1]
PREFIX=PROJECT.relative_to(REPO).as_posix()+'/'
REVIEW=PROJECT/'oxygen_response_review'
BASE='2f952089deb28b2112ec90d0534dc7dff7e5e316'
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO,text=True)
def load(path):return json.loads(path.read_text(encoding='utf-8'))
def run():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report',type=Path);args=parser.parse_args()
 rows=list(csv.DictReader((HERE/'exclusive_files_utf8.csv').open(encoding='utf-8-sig')))
 expected={r['path'] for r in rows};assert len(rows)==len(expected)==1872
 # ls-tree reads only Git tree metadata, never shared paper contents.
 tracked=set(git('ls-tree','-r','--name-only','HEAD').splitlines())
 review_branch=REVIEW.exists();matched=0;baseline_unchanged=0
 if review_branch:
  assert {p for p in tracked if p.startswith(PREFIX+'oxygen_response_review/')}==expected
  for r in rows:
   b=(REPO/r['path']).read_bytes()
   assert len(b)==int(r['review_branch_bytes']) and hashlib.sha256(b).hexdigest()==r['review_branch_sha256'],r['path']
   matched+=1;baseline_unchanged+=r['review_branch_sha256']==r['baseline_sha256']
  assert len(load(REVIEW/'catalog.json'))==1536
  assert len(load(REVIEW/'screening.json'))==1536
  assert len(load(REVIEW/'all_pool/provisional_priorities.json'))==364
  assert len(load(REVIEW/'all_pool/pending_confirmation_queue.json'))==479
  assert len(load(REVIEW/'reading_queue35/source_conditions_audit.json'))==35
  assert len(load(REVIEW/'reading_queue35/other_in_scope_continuation_queue.json'))==312
  progress=load(REVIEW/'all_pool/progress.json')
  assert progress['new_semantic_screened']==1516 and progress['queue35_confirmed_core_records']==0
  with zipfile.ZipFile(REVIEW/'oxygen_response_review_cumulative.xlsx') as z:
   assert z.testzip() is None
   workbook=z.read('xl/workbook.xml').decode()
   assert all(t in workbook for t in ['优先精读','机制验证关联','评价口径'])
  from openpyxl import load_workbook
  wb=load_workbook(REVIEW/'oxygen_response_review_cumulative.xlsx',read_only=True)
  assert len(wb.sheetnames)>=3
  for ws in wb:
   assert next(ws.iter_rows(values_only=True),None) is not None,ws.title
  wb.close()
  ris=[]
  for p in REVIEW.rglob('*.ris'):
   s=p.read_text(encoding='utf-8-sig');n=len(re.findall(r'^TY  - ',s,re.M))
   assert n==len(re.findall(r'^ER  -',s,re.M)),str(p)
   ris.append({'path':p.relative_to(REPO).as_posix(),'records':n})
 else:
  assert not any(p.startswith(PREFIX+'oxygen_response_review/') for p in tracked)
  ris=[]
 # Independently usable dataset inputs: exact pinned objects, no current review
 # directory required. This imports a helper only, never a research script.
 sys.path.insert(0,str(PROJECT/'omics_dataset_discovery/scripts'))
 from review_dependency import review_bytes
 config=load(HERE/'dependency_sources.json')
 for f in config['files']:review_bytes(f)
 # Existing study tables, decisions, originals and progress outside the removed
 # directory must not have changed. This compares Git object identity, not PDFs.
 changed=git('diff','--name-only',BASE,'HEAD').splitlines()
 allowed={
  'README.md',PREFIX+'README.md',PREFIX+'method_audit/README.md',
  PREFIX+'method_audit/validate.py',PREFIX+'method_audit/update_readme_navigation.py',
  PREFIX+'method_audit/rebuild_appendices.py',PREFIX+'method_audit/readme_restoration/source_link_index.md',
  PREFIX+'method_audit/readme_restoration/chapter_map.md',
  PREFIX+'omics_dataset_discovery/README.md',PREFIX+'omics_dataset_discovery/methods/METHODS.md',
 }
 allowed.update(PREFIX+'omics_dataset_discovery/scripts/'+x for x in ['review_dependency.py','bootstrap.py','parse_discovery.py','link_papers.py','supplement_links.py','reuse_cached_methods.py','validate.py'])
 for p in changed:
  assert p in allowed or p.startswith(PREFIX+'branch_migration/') or p in expected,p
 # All three historical review artifacts actually modified are listed in manifest;
 # any scientific result mutation fails the destination byte checks above.
 project_text=(PROJECT/'README.md').read_text()
 assert all(f'id="stage-{i}"' in project_text for i in range(1,8))
 docs=[REPO/'README.md',PROJECT/'README.md',PROJECT/'omics_dataset_discovery/README.md',PROJECT/'method_audit/README.md']
 if review_branch:docs+=list(REVIEW.rglob('*.md'))
 docs+=list(HERE.glob('*.md'))
 links=0;errors=[]
 all_paths=set(tracked)
 all_paths.update(p.relative_to(REPO).as_posix() for p in HERE.rglob('*') if p.is_file())
 for doc in docs:
  if not doc.exists():continue
  for target in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)',doc.read_text()):
   u=urlsplit(target.strip('<>'))
   if u.scheme or not u.path:continue
   path=(doc.parent/unquote(u.path)).resolve()
   try:rel=path.relative_to(REPO).as_posix()
   except ValueError:errors.append([str(doc),target]);continue
   if path.exists() or rel in all_paths or any(x.startswith(rel.rstrip('/')+'/') for x in all_paths):links+=1
   else:errors.append([str(doc.relative_to(REPO)),target])
 assert not errors,errors
 for p in [*(PROJECT/'omics_dataset_discovery/scripts').glob('*.py'),*(PROJECT/'method_audit').glob('*.py'),*HERE.glob('*.py')]:ast.parse(p.read_text())
 result={'checked_Asia_Shanghai':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'commit':git('rev-parse','HEAD').strip(),'branch':git('branch','--show-current').strip(),'mode':'review' if review_branch else 'data','passed':True,'manifest_files':len(rows),'review_files_size_SHA_matched':matched,'review_files_unchanged_from_baseline':baseline_unchanged,'pinned_dependencies_readable':len(config['files']),'RIS_checks':ris,'local_links_resolved':links,'other_existing_study_results_unchanged':True,'shared_original_verification':'Git tree identity only; no PDF re-download or content rehash','new_searches':0,'new_screening':0,'paper_downloads':0}
 if args.report:args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':run()
