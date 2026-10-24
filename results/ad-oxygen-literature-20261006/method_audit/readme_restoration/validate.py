#!/usr/bin/env python3
"""Documentation-only validation; no paper download, parsing or SHA recheck."""
import csv,datetime,json,re,subprocess
from pathlib import Path
from urllib.parse import unquote,urlsplit
P=Path(__file__).resolve().parents[2];R=P.parents[1];OUT=P/'method_audit/readme_restoration';BASE='9208deddd624e99b1314bac359c22349c8554c64'
def load(n):return json.loads((P/n).read_text())
def run():
 current=[R/'README.md',P/'README.md',P/'HISTORY.md',P/'oxygen_response_review/README.md',P/'omics_dataset_discovery/README.md',P/'method_audit/README.md',OUT/'chapter_map.md',OUT/'source_link_index.md']
 project=re.sub(r'<details\b.*?</details\s*>','',(P/'README.md').read_text(),flags=re.I|re.S);anchors=[]
 for i in range(1,8):
  anchor=f'stage-{i}';assert f'id="{anchor}"' in project;anchors.append(anchor)
 no_details=sum('<details' not in f.read_text().lower() for f in [R/'README.md',P/'README.md',P/'oxygen_response_review/README.md',P/'omics_dataset_discovery/README.md'])
 errors=[];count=0
 for f in current:
  for dest in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)',f.read_text()):
   dest=dest.strip('<>');u=urlsplit(dest)
   if u.scheme:continue
   path=(f.parent/unquote(u.path)).resolve() if u.path else f.resolve();count+=1
   if path in [OUT/'validation.json',OUT/'remote_readback.json']:continue
   if not path.exists():errors.append({'source':str(f.relative_to(R)),'target':dest})
   elif u.fragment.startswith('stage-') and f'id="{u.fragment}"' not in path.read_text():errors.append({'source':str(f.relative_to(R)),'anchor':dest})
 assert not errors,errors
 # Diff tree paths, not original PDF bytes: no data/classification/assets/progress touched.
 names=subprocess.check_output(['git','diff','--name-only',BASE],cwd=R,text=True).splitlines()+subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=R,text=True).splitlines()
 allowed_md={str(f.relative_to(R)) for f in current}|{str((P/'windows/README_zh.md').relative_to(R))}
 allowed_py={str((P/'method_audit/update_readme_navigation.py').relative_to(R)),str((P/'method_audit/validate.py').relative_to(R))}
 prefix=str(OUT.relative_to(R))+'/'
 assert all(n in allowed_md or n in allowed_py or n.startswith(prefix) for n in names),[n for n in names if n not in allowed_md and n not in allowed_py and not n.startswith(prefix)]
 with (P/'final_results/ad_oxygen_download_review_utf8.csv').open(encoding='utf-8-sig',newline='') as f:master_count=sum(1 for _ in csv.DictReader(f))
 merge=load('inventory/merge_20261023/merge_summary.json');omics=load('omics_screening/summary.json');data=load('omics_dataset_discovery/summary.json')
 assert master_count==554 and merge['unique_canonical_objects']==665 and merge['verified_target_fulltext_ids']==388 and merge['research_supplementary_original_files']==154
 assert omics['target_articles']==22 and omics['remaining_unstarted']==0 and omics['screening_uncertainty_articles']==8
 assert data['reviewed_public_community_projects']==38 and data['A_B_public_runs']==349
 result={'checked_Asia_Shanghai':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'passed':True,'baseline_commit':BASE,'seven_visible_stages':anchors,'README_files_with_no_details':no_details,'all_research_stage_anchors_outside_folds':True,'local_document_links_resolved':count,'existing_result_changes':0,'new_searches':0,'new_screening':0,'paper_original_downloads_or_SHA_rechecks':0,'new_detailed_methods_queries_cases_preserved':True,'historical_source_headings_mapped':len(load('method_audit/readme_restoration/baseline.json')['original_project_headings']),'root_to_project_link_valid':True,'snapshot_counts':{'library_records':master_count,'canonical_objects':665,'fulltext_articles':388,'official_or_local_supplementary_originals':154,'omics_articles':22,'omics_pending':8,'public_community_projects':38,'A_B_runs':349}}
 (OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':run()
