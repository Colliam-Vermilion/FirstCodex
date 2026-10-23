import pathlib,json,csv,hashlib,re,html,unicodedata,collections,shutil,zipfile,subprocess,os
from xml.etree import ElementTree as ET
from openpyxl import load_workbook
W=pathlib.Path('/workspace/work');B=W/'snapshot/results/ad-oxygen-literature-20261006';I=B/'inventory/merge_20261023';I.mkdir(parents=True,exist_ok=True)
A=json.load(open(W/'file_audit_initial.json'));R=list(csv.DictReader(open(W/'remote_master.csv',encoding='utf-8-sig')));RM={r['稳定记录ID']:r for r in R}
SCOPE={'1 直接向 AD 反应器或内部循环系统供氧','2 向厌氧水解或产酸阶段供氧','3 独立好氧或微好氧预处理','4 综述'}
def norm(s):
 for _ in range(3):s=html.unescape(s)
 return re.sub(r'[^a-z0-9\u4e00-\u9fff]','',unicodedata.normalize('NFKD',s).lower())
def writecsv(p,rows,fields=None):
 fields=fields or list(dict.fromkeys(k for r in rows for k in r))
 with open(p,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader()
  for row in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in row.items()})
wrong={
 'R04605':('Characteristics of ultra-fine bubble water and its trials on enhanced methane production from waste activated sludge','10.1016/j.biortech.2018.10.077','上传7页Bioresource Technology 273 (2019) 63–69期刊文章，不是目标Wang Di博士学位全文；同研究关联待核实，未另增文献ID'),
 'R03965':('Fate of sterols, polycyclic aromatic hydrocarbons, pharmaceuticals, ammonia and solids in single-stage anaerobic and sequential anaerobic/aerobic/anoxic sludge digestion','10.1016/j.wasman.2019.05.018','上传2019期刊文章，目标为2018会议文献；作者及主题关联，但题名和DOI不同，目标会议全文仍未取得'),
 'R13947':('Microaeration for Hydrogen Sulfide Removal in Biogas — Fact Sheet FS-xxx','', '上传3页University of Maryland Extension推广资料草稿，不是Iris Ramos Castaño目标学位论文'),
 'R13949':('Performance Enhancement Of Batch Anaerobic Digestion Of Napier Grass By Alkali Pre-Treatment','', '上传Int. J. ChemTech Research 5(2) 558–564 (2013)碱预处理文章；目标为好氧预处理会议论文，处理方法及题名不一致')}
manual={
 'R02239':'PDF pp.3–7为《微好氧水解酸化在石化废水预处理中的应用研究》，朱晨等，环境科学36(10),3738–3742 (2015)；含摘要、工程与方法、结果、结论及参考文献；pp.1–2及8–9为封面/目录，不以其无英文正文关键词否认完整正文。中文字体文字层乱码，核对中文题名及页序。',
 'R00608':'扫描PDF共5页，逐页OCR核对；第1页中英文题名、王佩超等作者、环境工程技术学报3(5),386–390 (2013)，末页含结论及参考文献。原件不改写，OCR作为派生核验依据。',
 'R13946':'上传整本Springer会议论文集207页。目标Chapter 5在PDF pp.46–53（印刷页35–42），该章节首有题名/Ziqi Fan/DOI，末有参考文献，PDF p.54开始第6章；按1篇已获完整章节计，不计为期刊论文。未把其他章节另增文献。',
 'R06611':'White Rose封面明确Accepted Version，题名、作者、DOI一致。PDF 48页的论文部分为图像文字；OCR抽查pp.2,4,11,21,31,41,47,48，覆盖题名、Introduction、Methods、Results、References、图表与电子附件入口，确认正文完整。',
 'R06152':'印尼文正文完整，英文题名及作者一致；pp.1–9覆盖ABSTRAK/ABSTRACT、方法、结果、结论及参考文献。',
 'R12483':'泰文全文20页，首页泰文/英文双语题名及作者、Thai Society of Agricultural Engineering Journal 31(2),40–59 (2025)、ISSN1685-408X；中文/英文关键词规则不适用，完整正文、结论及参考文献存在。'}
for a in A:
 p=B/a['source_path'];rid=a['record_id'];a['verification_notes']='';a['association_status']='';a['observed_title']='';a['observed_doi']=''
 if a['format']=='doc':
  t=(W/'texts'/f'{a["sha256"]}.antiword.txt').read_text();a['verification_status']='legacy_word_decoded_with_antiword';a['issues']=[x for x in a['issues'] if x!='legacy_doc_full_render_not_verified'];a['head_excerpt']=t[:5500];a['text_length']=len(t)
  a['association_text']=t
 elif a['format']=='docx':
  with zipfile.ZipFile(p) as z:
   root=ET.fromstring(z.read('word/document.xml'));t=' '.join(n.text or '' for n in root.iter() if n.tag.endswith('}t'))
  a['association_text']=t
 elif a.get('text_path'):a['association_text']=pathlib.Path('/workspace',a['text_path']).read_text()
 else:a['association_text']=''
 if a['format']=='xlsx':
  wb=load_workbook(p,read_only=True,data_only=False);a['workbook_sheets']=[{'name':s.title,'rows':s.max_row,'columns':s.max_column} for s in wb.worksheets];wb.close();a['verification_status']='xlsx_open_and_zip_crc_verified'
 if a['role']=='fulltext' and a['source']=='local_upload' and rid in wrong:
  a['role']='uncertain';a['verification_status']='identity_conflict_not_target_fulltext';a['observed_title'],a['observed_doi'],a['verification_notes']=wrong[rid];a['issues']=['identity_conflict_not_target_fulltext']
 elif a['role']=='fulltext':
  if rid in manual:a['verification_notes']=manual[rid];a['verification_status']='manual_identity_and_completeness_verified';a['issues']=[]
  elif rid in ['R13968','R13969']:
   prior=a['prior_assets'];assert prior and any(x.get('multipart_group_complete_and_reviewed')=='True' for x in prior)
   a['verification_notes']='七部分学位原件，沿用既有按题名/仓储ID/章节连续性人工核验；本轮全部7部分存在、SHA与页对象可读，组合计1篇，单个章节不单独计全文。';a['verification_status']='complete_multipart_thesis_group_verified';a['issues']=[]
  else:
   assert a['verification_status']=='identity_and_body_structure_verified',a['source_path']
   a['verification_notes']='首页/前两页题名作者或目标DOI核对，全部页面解析及正文结构检查；不据文件名判全文。'
  if '学位' in RM.get(rid,{}).get('文献类型','') or '学生' in RM.get(rid,{}).get('文献类型',''):a['version']='学位/学生报告原稿（分章节者按组）'
  if rid=='R13946':a['version']='出版版会议论文集（包含完整目标章节）'
  if rid=='R06611':a['version']='作者接受稿（White Rose明确Accepted Version）'
 if a['role']=='uncertain' and not a['verification_notes']:
  a['verification_status']='historical_candidate_not_target_fulltext';a['verification_notes']='历史候选抓取物：出版商目录/广告、期刊索引或检索页等，目标身份及正文不成立；原件保留，不计全文或科研补充材料。';a['issues']=['historical_non_target_candidate']
 if a['source_path']=='localdownload/R11773/supplementary.pdf':
  a['role']='administrative_attachment';a['verification_notes']='内容为Authorship change request（作者变更申请表）；有关联论文题名，但不是科研补充材料。';a['verification_status']='administrative_form_identified';a['issues']=['not_research_supplement']
 if a['role']=='supplementary':
  title=RM.get(rid,{}).get('完整题名','');t=a['association_text']
  if any(x.get('official_attachment')=='True' for x in a['prior_assets']):a['association_status']='existing_official_attachment_evidence_retained'
  elif len(norm(title))>25 and norm(title) in norm(t):a['association_status']='title_in_attachment_verified'
  elif a.get('expected_doi_in_head'):a['association_status']='doi_in_attachment_verified'
  else:a['association_status']='directory_and_content_consistent_identity_pending';a['verification_notes']+=' 文件可打开且内容为表格/数据/图等补充材料；缺题名/DOI等唯一关联凭据，仅保留目录及内容关联，不能声称已核实附件身份或已收齐全部附件。'
  if rid=='R03965' and a['source']=='local_upload':a['association_status']='related_journal_version_supplement_not_target_conference_verified';a['verification_notes']+=' 与该目录中的不同DOI期刊版相关，未核实属于目标会议文献。'
 if a['role']=='abstract':a['verification_status']='abstract_identity_verified_not_fulltext';a['verification_notes']='内容为会议摘要/展示材料，题名核对，仅摘要，不计已取得全文。'
 if a['role']=='poster':a['verification_status']='poster_identity_verified_not_fulltext';a['verification_notes']='研究海报，仅海报，不计论文全文。'
# Assert each multipart group is complete using actual current byte files.
for rid in ['R13968','R13969']:assert len([a for a in A if a['record_id']==rid and a['role']=='fulltext'])==7
# Archive lineage and previous inventories without changing their evidence.
for rel in ['inventory/assets_utf8.csv','inventory/assets.json','inventory/papers_utf8.csv','inventory/papers.json','original_files/ATTRIBUTION_utf8.csv']:
 p=B/rel
 if p.exists():shutil.copy2(p,I/('baseline_'+p.name))
shutil.copy2(W/'remote_master.csv',I/'baseline_master_utf8.csv')
shutil.copy2(W/'main_preservation_readback.json',I/'main_preservation_readback.json')
shutil.copy2(W/'main_preservation.json',I/'main_preservation_before_cleanup.json')
# One physical canonical object per SHA256; differing byte versions are retained.
groups=collections.defaultdict(list)
for a in A:groups[a['sha256']].append(a)
canonical=[];mapping=[];temp=B/'_canonical_staging';temp.mkdir(exist_ok=True)
for sha,items in sorted(groups.items()):
 a=items[0];rid=a['record_id'];role=a['role'];ext=a['format'];folder={'fulltext':'fulltext','supplementary':'supplementary','abstract':'abstract_poster','poster':'abstract_poster','derived':'derived','uncertain':'uncertain','administrative_attachment':'administrative','source_evidence':'evidence'}[role]
 rid=rid or '_project_evidence'
 version=''
 if role=='fulltext':version='__accepted' if '接受稿' in a['version'] else '__thesis' if '学位' in a['version'] else '__book_chapter' if a['record_id']=='R13946' else '__published' if '出版' in a['version'] else '__version_unverified'
 name=f'{role}{version}__{sha[:16]}.{ext}'
 path=f'original_files/{rid}/{folder}/{name}';dest=temp/pathlib.Path(path).relative_to('original_files');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(B/a['source_path'],dest)
 assert hashlib.sha256(dest.read_bytes()).hexdigest()==sha
 obj={k:v for k,v in a.items() if k not in ['association_text','head_excerpt','tail_excerpt','archive_members','prior_assets']};obj['canonical_path']=path;obj['source_paths']=[x['source_path'] for x in items];obj['sources']=list(dict.fromkeys(x['source'] for x in items));obj['original_filenames']=list(dict.fromkeys(x['original_filename'] for x in items));obj['source_record_ids']=list(dict.fromkeys(x['record_id'] for x in items));obj['prior_asset_evidence']=[p for x in items for p in x['prior_assets']];obj['archive_members']=a.get('archive_members',[])
 obj['github_path']='results/ad-oxygen-literature-20261006/'+path;obj['github_url']='https://github.com/Colliam-Vermilion/FirstCodex/blob/results/ad-oxygen-literature-20261006/'+obj['github_path'];obj['title']=RM.get(a['record_id'],{}).get('完整题名','');obj['doi']=RM.get(a['record_id'],{}).get('DOI','')
 canonical.append(obj)
 for x in items:
  x['canonical_path']=path
  mapping.append({'record_id':x['record_id'],'source_record_id':x['directory_id'],'title':RM.get(x['record_id'],{}).get('完整题名',''),'doi':RM.get(x['record_id'],{}).get('DOI',''),'role':x['role'],'version':x['version'],'original_filename':x['original_filename'],'source_path':x['source_path'],'source':x['source'],'canonical_path':path,'size_bytes':x['size_bytes'],'sha256':sha,'git_blob_oid':x['git_blob_oid'],'verification_status':x['verification_status'],'association_status':x['association_status'],'verification_notes':x['verification_notes'],'github_url':obj['github_url']})
shutil.rmtree(B/'original_files');temp.rename(B/'original_files')
shutil.rmtree(B/'localdownload');(B/'localdownload').mkdir();(B/'localdownload/README.md').write_text('# 上传目录已并入规范原件库\n\n2026-10-23按SHA256归并；439个上传文件均保留在 `../original_files/`。原路径与新路径逐件见 `../inventory/merge_20261023/source_path_mapping_utf8.csv`。历史上传原字节也可从提交022237df取回；本目录不再保留重复原件。\n')
# Store every original source association and every unique current object.
json.dump(canonical,open(I/'unified_files.json','w'),ensure_ascii=False,indent=2);writecsv(I/'unified_files_utf8.csv',canonical);writecsv(I/'source_path_mapping_utf8.csv',mapping)
json.dump([{k:v for k,v in a.items() if k!='association_text'} for a in A],open(I/'file_content_verification.json','w'),ensure_ascii=False,indent=2)
files_by_id=collections.defaultdict(list)
for a in canonical:
 for rid in a['source_record_ids']:files_by_id[rid].append(a)
statuses=[]
for r in R:
 rid=r['稳定记录ID'];fs=files_by_id[rid];mains=[a for a in fs if a['role']=='fulltext'];supp=[a for a in fs if a['role']=='supplementary'];abstracts=[a for a in fs if a['role']=='abstract'];posters=[a for a in fs if a['role']=='poster'];problems=[a for a in fs if a['role']=='uncertain' and a['verification_status']=='identity_conflict_not_target_fulltext']
 state='已取得核验全文' if mains else '仅摘要，未取得全文' if abstracts else '仅海报，未取得全文' if posters else '未取得全文（上传件身份错配/相关版本，目标正文缺失）' if problems else '未取得全文'
 pending=sum(a['association_status'] not in ['title_in_attachment_verified','doi_in_attachment_verified','existing_official_attachment_evidence_retained'] for a in supp)
 si=f'已取得{len(supp)}件原格式补充材料；其中{pending}件唯一关联待核实；完整性未确认' if supp else '当前无补充材料原件；沿用既有缺失/无附件证据，不据此认定无附件'
 s={'record_id':rid,'title':r['完整题名'],'doi':r['DOI'],'category_unchanged':r['最终分类'],'included_for_analysis':r['最终分类'] in SCOPE,'main_status':state,'verified_fulltext':bool(mains),'main_file_count':len(mains),'main_paths':[a['canonical_path'] for a in mains],'main_sha256':[a['sha256'] for a in mains],'supplementary_count':len(supp),'supplementary_identity_pending_count':pending,'supplementary_status':si,'supplementary_paths':[a['canonical_path'] for a in supp],'abstract_count':len(abstracts),'poster_count':len(posters),'identity_conflict_count':len(problems),'current_original_paths':[a['canonical_path'] for a in fs]};statuses.append(s)
 for field in ['全文获取状态','当前原件状态','当前正文核验状态']:r[field]=state
 r['新环境核查日期']='2026-10-23';r['当前补充材料状态']=si;r['当前原件路径']='; '.join(s['current_original_paths']);r['当前正文全部原件路径']='; '.join(s['main_paths']);r['当前正文全部SHA256_JSON']=json.dumps(s['main_sha256']);r['当前原件SHA256']='; '.join(s['main_sha256']);r['当前版本及限制']='; '.join(dict.fromkeys(a['version'] for a in mains));r['当前持久下载入口']='; '.join(a['github_url'] for a in mains);r['持久化及独立取回状态']='结果分支已保留原字节；本轮最终提交独立读回回执见inventory/merge_20261023/remote_readback.json';r['本轮文件核验备注']='; '.join(a['verification_notes'] for a in fs if a['role'] in ['fulltext','uncertain'] and a['verification_notes']);r['本轮补充材料路径']='; '.join(s['supplementary_paths']);r['本轮统一文件清单']='inventory/merge_20261023/unified_files_utf8.csv'
writecsv(B/'final_results/ad_oxygen_download_review_utf8.csv',R)
writecsv(B/'inventory/papers_utf8.csv',statuses);writecsv(B/'manual_review/current_environment_acquisition426_utf8.csv',[x for x in statuses if x['included_for_analysis']]);writecsv(B/'manual_review/current_environment_need_fulltext_utf8.csv',[x for x in statuses if x['included_for_analysis'] and not x['verified_fulltext']]);writecsv(B/'manual_review/supplementary_material_status_utf8.csv',statuses)
json.dump(statuses,open(I/'paper_status.json','w'),ensure_ascii=False,indent=2)
# Keep legacy asset evidence and IDs, and point original-byte references at the new canonical path.
legacy=json.load(open(I/'baseline_assets.json'));writecsv(B/'inventory/assets_utf8.csv',[dict(a,role='main' if a['role']=='fulltext' else a['role'],source_repo_path=a['canonical_path'],availability='present_sha_verified',storage_status='current_results_branch_original') for a in canonical]);json.dump(canonical,open(B/'inventory/assets.json','w'),ensure_ascii=False,indent=2)
scope=[s for s in statuses if s['included_for_analysis']];official=[a for a in canonical if a['role']=='supplementary']
summary={'baseline_commit':'022237df5e83e99711e7fa358ed2b4611d42bab1','preservation_commit':'b739c0e78507bc13db8d4a149ad7c34d07bfdbbf','main_cleanup_commit':'0bdf0b9933b1a628d8b49561fdf3e35bbc7f6223','total_records':len(R),'included_records':len(scope),'local_upload_files':sum(a['source']=='local_upload' for a in A),'local_upload_ids':len({a['record_id'] for a in A if a['source']=='local_upload'}),'cloud_existing_files':sum(a['source']=='cloud_existing' for a in A),'cloud_existing_fulltext_files':sum(a['source']=='cloud_existing' and a['role']=='fulltext' for a in A),'cloud_existing_fulltext_ids':len({a['record_id'] for a in A if a['source']=='cloud_existing' and a['role']=='fulltext'}),'local_verified_target_fulltext_ids':len({a['record_id'] for a in A if a['source']=='local_upload' and a['role']=='fulltext'}),'unique_canonical_objects':len(canonical),'duplicate_byte_occurrences':len(A)-len(canonical),'verified_target_fulltext_ids':sum(s['verified_fulltext'] for s in scope),'verified_target_fulltext_files':sum(a['role']=='fulltext' for a in canonical),'only_abstract_ids':sum(bool(s['abstract_count']) and not s['verified_fulltext'] for s in scope),'only_poster_ids':sum(bool(s['poster_count']) and not s['verified_fulltext'] for s in scope),'missing_fulltext_total':sum(not s['verified_fulltext'] for s in scope),'missing_without_abstract_or_poster':sum(not s['verified_fulltext'] and not s['abstract_count'] and not s['poster_count'] for s in scope),'local_identity_conflict_files':4,'historical_non_target_candidate_paths':sum(a['verification_status']=='historical_candidate_not_target_fulltext' for a in A),'historical_non_target_candidate_objects':sum(a['verification_status']=='historical_candidate_not_target_fulltext' for a in canonical),'administrative_forms':sum(a['role']=='administrative_attachment' for a in canonical),'damaged_or_password_required':sum(a['verification_status']=='unreadable' for a in canonical),'research_supplementary_original_files':len(official),'supplementary_formats':dict(collections.Counter(a['format'] for a in official)),'supplementary_identity_pending':sum(a['association_status'] not in ['title_in_attachment_verified','doi_in_attachment_verified','existing_official_attachment_evidence_retained'] for a in official),'zip_originals':sum(a['format']=='zip' for a in official),'derived_members_not_counted_as_original_supplements':sum(a['role']=='derived' for a in canonical),'source_evidence_objects_not_counted_as_fulltext_or_si':sum(a['role']=='source_evidence' for a in canonical),'canonical_bytes':sum(a['size_bytes'] for a in canonical)}
json.dump(summary,open(I/'merge_summary.json','w'),ensure_ascii=False,indent=2)
print(json.dumps(summary,ensure_ascii=False,indent=2))
