import json,hashlib,subprocess,re,os,csv
from pathlib import Path
from urllib.parse import unquote,urlsplit
from openpyxl import load_workbook
R=Path('/workspace/FirstCodex');T=R/'results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer';P=T/'uploads_20261101';BASE='591097727502b81b0e0a5bfa11d5ae07f05c7ca2'
read=lambda p:json.load(open(p))
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
M=read(T/'literature_master.json');old=json.loads(subprocess.check_output(['git','show',BASE+':'+str((T/'literature_master.json').relative_to(R))],cwd=R));C={r['id']:r for r in M};checks={};checks['unique_ids']=len(M)==len(C)
checks['prior_ids_and_manual_scope_preserved']=all(r['id'] in C and all(C[r['id']].get(k)==r.get(k)for k in ['scope_decision','existing_scope_decision_preserved','old_scope_judgment_changed'])for r in old)
checks['source_bytes_preserved']=all((R/r['canonical_path']).stat().st_size==r['bytes']and hashlib.sha256((R/r['canonical_path']).read_bytes()).hexdigest()==r['sha256']for r in read(P/'file_inventory.json'))
checks['compatibility_duplicate_hash']=all(hashlib.sha256((R/r['other_path']).read_bytes()).hexdigest()==r['sha256']for r in read(P/'duplicate_files.json'))
for f in [T/'spatial_gas_transfer_cumulative.xlsx',R/'scientific_guide/scientific_reading_guide.xlsx']:
 wb=load_workbook(f,read_only=True);checks[f.name+'_nine_fulltexts']=wb['上传全文精读'].max_row==10;checks[f.name+'_six_local']=wb['本轮现有候选补筛'].max_row==7
 if f.parent==T:checks['excel_master_count']=wb['文献与专题筛选'].max_row==len(M)+1
 wb.close()
s=(T/'spatial_gas_transfer_candidates.ris').read_text();checks['ris_count_balance']=s.count('TY  -')==s.count('ER  -')==len(M)
# Previously protected source catalogs and manual decisions have no diff.
protected=['catalog.json','screening.json','mechanism_evidence.json','reading_priority/evaluations.json','all_pool/progress.json','oxygen_response_review_cumulative.xlsx'];checks['original_mechanism_files_unchanged']=all(not subprocess.check_output(['git','diff',BASE,'--',str((T.parent/f).relative_to(R))],cwd=R)for f in protected)
docs=[R/'README.md',R/'scientific_guide/README.md',R/'scientific_guide/spatial_reading_map.md',T/'README.md',P/'README.md',*(P/'evidence').glob('*.md')];bad=[]
for f in docs:
 for target in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)',f.read_text()):
  u=urlsplit(target.strip('<>'))
  if u.scheme or not u.path:continue
  p=(f.parent/unquote(u.path)).resolve()
  if not p.exists():bad.append({'file':str(f.relative_to(R)),'target':target})
checks['all_current_document_links_exist']=not bad
checks['all_four_parts_visible']=all('## Part '+str(n)+'.' in (R/'README.md').read_text()for n in range(1,5))
dump(P/'validation.json',{'passed':all(checks.values()),'checks':checks,'bad_links':bad});print(json.dumps({'passed':all(checks.values()),'checks':checks,'bad_links':bad},ensure_ascii=False,indent=2));assert all(checks.values())
