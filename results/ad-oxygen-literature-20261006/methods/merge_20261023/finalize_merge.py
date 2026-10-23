import pathlib,json,csv,collections,shutil,hashlib
W=pathlib.Path('/workspace/work');B=W/'snapshot/results/ad-oxygen-literature-20261006';I=B/'inventory/merge_20261023'
def readcsv(p):return list(csv.DictReader(open(p,encoding='utf-8-sig')))
def writecsv(p,rows,fields=None):
 fields=fields or list(dict.fromkeys(k for r in rows for k in r))
 with open(p,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader()
  for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()})
R=readcsv(B/'final_results/ad_oxygen_download_review_utf8.csv');RM={r['稳定记录ID']:r for r in R};A=json.load(open(I/'unified_files.json'));M=readcsv(I/'source_path_mapping_utf8.csv');S=json.load(open(I/'paper_status.json'))
sha='d29034513104ea94ee48e59cc6ac7e4aec289b7ede54906d5cdeca1170efa9bc'
note='R13964与R13834上传同字节附件。附件为7种微污染物HPLC及GC-BID/GC-TCD色谱图、periods I–VII；与R13834实验对象/检测方法及Appendix A补充链接相符；R13964为H2S综述且不含该组实验。规范归R13834；R13964的错误来源关联保留，R13964不计此附件。'
for a in A:
 a['associated_record_ids']=a['source_record_ids'][:]
 if a['sha256']==sha:
  old=a['canonical_path'];new=old.replace('/R13964/','/R13834/');dest=B/new;dest.parent.mkdir(parents=True,exist_ok=True)
  if old!=new and (B/old).exists():shutil.move(B/old,dest)
  a.update(record_id='R13834',associated_record_ids=['R13834'],canonical_path=new,title=RM['R13834']['完整题名'],doi=RM['R13834']['DOI'],association_status='content_linkage_verified_misfile_resolved',verification_notes=note,verification_status='supplement_identity_resolved_by_content')
  a['github_path']='results/ad-oxygen-literature-20261006/'+new;a['github_url']='https://github.com/Colliam-Vermilion/FirstCodex/blob/results/ad-oxygen-literature-20261006/'+a['github_path']
  for m in M:
   if m['sha256']==sha:m.update(record_id='R13834',title=a['title'],doi=a['doi'],canonical_path=new,github_url=a['github_url'],association_status=a['association_status'],verification_notes=note,verification_status='misfiled_supplement_resolved' if m['source_record_id']=='R13964' else a['verification_status'])
 a['asset_id']=next((p['asset_id'] for p in a['prior_asset_evidence'] if p.get('asset_id')),f'{a["record_id"]}.{a["role"]}.{a["sha256"][:16]}');a['legacy_asset_ids']=list(dict.fromkeys(p.get('asset_id','') for p in a['prior_asset_evidence'] if p.get('asset_id')))
verified_si={'title_in_attachment_verified','doi_in_attachment_verified','existing_official_attachment_evidence_retained','content_linkage_verified_misfile_resolved'}
byid=collections.defaultdict(list)
for a in A:
 for rid in a['associated_record_ids']:byid[rid].append(a)
for s in S:
 rid=s['record_id'];fs=byid[rid];mains=[a for a in fs if a['role']=='fulltext'];mains.sort(key=lambda a:(int(next((x.get('multipart_part_index') for x in a['prior_asset_evidence'] if x.get('multipart_part_index')),0)), '接受稿' in a['version'],a['canonical_path']))
 si=[a for a in fs if a['role']=='supplementary'];pending=sum(a['association_status'] not in verified_si for a in si)
 s.update(main_paths=[a['canonical_path'] for a in mains],main_sha256=[a['sha256'] for a in mains],supplementary_count=len(si),supplementary_identity_pending_count=pending,supplementary_paths=[a['canonical_path'] for a in si],current_original_paths=[a['canonical_path'] for a in fs])
 s['supplementary_status']=f'已取得{len(si)}件原格式补充材料；其中{pending}件唯一关联待核实；完整性未确认' if si else '当前无补充材料原件；沿用既有缺失/无附件证据，不据此认定无附件'
 r=RM[rid];r['当前补充材料状态']=s['supplementary_status'];r['当前原件路径']='; '.join(s['current_original_paths']);r['当前正文全部原件路径']='; '.join(s['main_paths']);r['当前正文全部SHA256_JSON']=json.dumps(s['main_sha256']);r['当前原件SHA256']='; '.join(s['main_sha256']);r['本轮补充材料路径']='; '.join(s['supplementary_paths']);r['当前持久下载入口']='; '.join(a['github_url'] for a in mains)
 r['本地文件路径']=s['main_paths'][0] if mains else '';r['文件SHA256']=s['main_sha256'][0] if mains else '';r['文件大小（字节）']=mains[0]['size_bytes'] if mains else '';r['PDF页数']=mains[0].get('pages','') if mains else '';r['全文版本']='; '.join(dict.fromkeys(a['version'] for a in mains));r['SI状态']=s['supplementary_status']
 if rid in ['R13964','R13834']:r['本轮文件核验备注']+=' '+note
writecsv(I/'source_path_mapping_utf8.csv',M);writecsv(I/'unified_files_utf8.csv',A);json.dump(A,open(I/'unified_files.json','w'),ensure_ascii=False,indent=2)
writecsv(B/'final_results/ad_oxygen_download_review_utf8.csv',R);writecsv(B/'inventory/papers_utf8.csv',S);writecsv(B/'manual_review/current_environment_acquisition426_utf8.csv',[s for s in S if s['included_for_analysis']]);writecsv(B/'manual_review/current_environment_need_fulltext_utf8.csv',[s for s in S if s['included_for_analysis'] and not s['verified_fulltext']]);writecsv(B/'manual_review/supplementary_material_status_utf8.csv',S);json.dump(S,open(I/'paper_status.json','w'),ensure_ascii=False,indent=2)
writecsv(B/'inventory/assets_utf8.csv',[dict(a,role='main' if a['role']=='fulltext' else a['role'],source_repo_path=a['canonical_path'],availability='present_sha_verified') for a in A]);json.dump(A,open(B/'inventory/assets.json','w'),ensure_ascii=False,indent=2)
sumfile=I/'merge_summary.json';s=json.load(open(sumfile));s.update(supplementary_identity_pending=sum(a['role']=='supplementary' and a['association_status'] not in verified_si for a in A),resolved_misfiled_supplement_occurrences=1);json.dump(s,open(sumfile,'w'),ensure_ascii=False,indent=2)
print('finalized',len(A),'objects; supplemental pending',s['supplementary_identity_pending'])
