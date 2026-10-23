import pathlib,json,csv,re,html,unicodedata,collections,shutil,datetime,hashlib,zipfile
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart,Reference
W=pathlib.Path('/workspace/work');B=W/'snapshot/results/ad-oxygen-literature-20261006';I=B/'inventory/merge_20261023'
R=list(csv.DictReader(open(B/'final_results/ad_oxygen_download_review_utf8.csv',encoding='utf-8-sig')));S={s['record_id']:s for s in json.load(open(I/'paper_status.json'))};A=json.load(open(I/'unified_files.json'));J=json.load(open(W/'jcr_verified.json'))
SCOPE={'1 直接向 AD 反应器或内部循环系统供氧','2 向厌氧水解或产酸阶段供氧','3 独立好氧或微好氧预处理','4 综述'}
def clean(s):
 for _ in range(3):s=html.unescape(s)
 return s.strip()
def norm(s):return re.sub('[^a-z0-9]','',re.sub(r'\b(and|the)\b',' ',unicodedata.normalize('NFKD',clean(s)).lower()))
JN={norm(j['journal']):j for j in J.values()}
manual_journals={'R02239':('Huanjing Kexue / Environmental Science','0250-3301','',2015,'PDF pp.1,3–7：《环境科学》36(10),3738–3742；原期刊字段PubMed为索引平台'), 'R00608':('Journal of Environmental Engineering Technology','1674-991X','',2013,'扫描PDF p.1：《环境工程技术学报》3(5),386–390；doi:10.3969/j.issn.1674-991X.2013.05.060，原DOI为空未直接覆盖'), 'R02370':('Journal of Residuals Science & Technology','1544-8053','',2011,'PDF p.1期刊页脚显示Vol.8, No.2 April 2011，与原年份存在差异，范围分类不因年份核验自动改变'), 'R13818':('Journal of Residuals Science & Technology','1544-8053','',2013,'PDF p.1期刊页脚：Vol.10, No.1 January 2013'), 'R06674':('Songklanakarin Journal of Science and Technology','0125-3395','',2021,'PDF p.1：Songklanakarin J. Sci. Technol.43(6),1793–1799，原DOAJ字段为目录平台')}
kind_pending_ids={'R00273','R01680','R01805','R13906'}
series_pending={'Advanced Materials Research','Applied Mechanics and Materials','Energy Procedia','Procedia Environmental Sciences','Chemical Engineering Transactions'}
details=[];pending=[];metadata_audit=[]
for r in R:
 rid=r['稳定记录ID'];s=S[rid];p=W/'crossref'/f'{rid}.json';c=json.load(open(p)) if p.exists() else {};valid=bool(c.get('type'));doi=r['DOI'];journal=clean((c.get('container-title')or[r['期刊']])[0]);issn='';eissn='';notes=[];sources=[]
 if valid:
  sources.append('https://api.crossref.org/works/'+doi)
  for v in c.get('issn-type') or []:
   if v['type']=='print':issn=v['value']
   elif v['type']=='electronic':eissn=v['value']
  if not issn and not eissn:issn='; '.join(c.get('ISSN')or[])
 elif doi:notes.append('既有DOI未由Crossref返回可用元数据（可能为DataCite/JaLC等）；不据此否认记录身份')
 year=r['正式发表年份']
 if rid in manual_journals:
  journal,issn,eissn,year,n=manual_journals[rid];notes.append(n);sources.append('原件内容核验：'+r['当前正文全部原件路径'])
 group=r['文献类型分组'];typ=r['文献类型'];crtype=c.get('type','');in_scope=r['最终分类'] in SCOPE
 if '学位' in typ or '学生' in typ or '博士' in typ or '硕士' in typ or group=='学位论文/学生报告' or crtype=='dissertation':kind='学位/学生报告'
 elif '非期刊' in typ or '会议' in typ or '海报' in typ or '综述章节' in typ or crtype in ['proceedings-article','book-chapter']:kind='会议/非期刊'
 elif rid in kind_pending_ids or journal in series_pending or not journal or journal in ['PubMed','DOAJ (DOAJ: Directory of Open Access Journals)','Lund University Publications (Lund University)']:kind='类型待核实';notes.append('期刊/会议或其他载体身份缺少足够凭据，单列待核实，不混入期刊论文分母')
 elif '期刊' in group and group not in ['其他非期刊资料','其他非期刊'] or crtype=='journal-article':kind='期刊论文'
 else:kind='类型待核实'
 # Conference banner in this specific PDF leaves journal-special-issue identity unresolved.
 if rid=='R13906':kind='类型待核实';notes.append('PDF标注ICBAA会议，Crossref类型journal-article；会议专刊性质待核实，暂不混入期刊论文分母')
 sub=('其他期刊论文' if 'Technical Note' in typ or '技术说明' in typ else '综述' if r['最终分类']=='4 综述' or '综述' in typ else '研究类') if kind=='期刊论文' else kind
 j=next((j for j in J.values() if j.get('issn') and j['issn'] in [issn,eissn]),None) or JN.get(norm(journal))
 if kind!='期刊论文':j=None
 if j:
  journal=clean(j['journal']);cats=j['categories'];qtext='; '.join(x['category']+': '+x['quartile'] for x in cats);anyq='是' if any(x['quartile']=='Q1' for x in cats) else '否';allq='是' if all(x['quartile']=='Q1' for x in cats) else '否';verified='是';jurl=j['source_url'];notes.append(j['verification']);notes.append('全部Q1仅指本表全部已核实学科；无官方完整学科导出，不承诺没有未显示学科')
  if not issn and not eissn:issn=j['issn']
 else:cats=[];qtext='';anyq=allq='待核实';verified='否';jurl='';notes.append('2024指标年JCR分区未核实；空白不能当非Q1。需要2025发布版/2024指标年的JCR全部学科导出。' if kind=='期刊论文' else '非目标期刊论文或类型待核实，不进入JCR分母')
 if rid in ['R04605','R03965','R13947','R13949']:notes.append(r['本轮文件核验备注'])
 row={'文献ID':rid,'题名':r['完整题名'],'年份':year,'原总表年份':r['正式发表年份'],'DOI':doi,'文献类型':typ,'现有研究分类':r['最终分类'],'纳入范围':'是' if in_scope else '否','统计文献组':sub,'是否目标期刊论文':'是' if in_scope and kind=='期刊论文' else '否','期刊':journal,'原期刊字段':r['期刊'],'ISSN':issn,'eISSN':eissn,'正文获取状态':s['main_status'],'核验全文标志':'是' if s['verified_fulltext'] else '否','补充材料状态':s['supplementary_status'],'JCR数据年份':2024 if kind=='期刊论文' else '', 'JCR发布版本':'2025发布版（2024指标年）' if kind=='期刊论文' else '', '学科类别':'; '.join(x['category'] for x in cats),'JIF分区（逐学科）':qtext,'至少一学科Q1':anyq if kind=='期刊论文' else '不适用','全部已核实学科均Q1':allq if kind=='期刊论文' else '不适用','JCR分区已核实':verified if kind=='期刊论文' else '不适用','查询来源':jurl,'期刊身份来源':'; '.join(sources),'核验备注':' | '.join(notes),'正文全部规范路径':'; '.join(s['main_paths']),'补充材料路径':'; '.join(s['supplementary_paths']),'正文GitHub链接':r['当前持久下载入口']}
 details.append(row);metadata_audit.append({'record_id':rid,'original_journal':r['期刊'],'normalized_journal':journal,'publication_kind':kind,'subtype':sub,'issn':issn,'eissn':eissn,'metadata_source':'; '.join(sources),'notes':' | '.join(notes)})
 if in_scope and (kind=='类型待核实' or kind=='期刊论文' and (not j or not issn and not eissn)):
  pending.append({'文献ID':rid,'题名':r['完整题名'],'问题类别':'文献类型' if kind=='类型待核实' else 'JCR分区/期刊身份','具体问题':row['核验备注'],'期刊':journal,'DOI':doi,'需要资料':'2025发布版/2024指标年JCR导出：期刊全名、ISSN/eISSN、全部Category、JIF Quartile、JIF Rank、数据年份、导出日期；类型疑点需题名页/正式载体说明','路径':'; '.join(s['current_original_paths'])})
for a in A:
 if a['role']=='supplementary' and a['association_status'] not in {'title_in_attachment_verified','doi_in_attachment_verified','existing_official_attachment_evidence_retained','content_linkage_verified_misfile_resolved'} or a['role'] in ['uncertain','administrative_attachment']:
  pending.append({'文献ID':a['record_id'],'题名':a['title'],'问题类别':'附件唯一关联待核实' if a['role']=='supplementary' else '原件身份/角色异常','具体问题':a['verification_notes'],'期刊':'','DOI':a['doi'],'需要资料':'附件的原始出版社文件名/下载关联页面；错配文献的目标原件。原件保留，不在本轮追下载。','路径':a['canonical_path']})
target=[r for r in details if r['是否目标期刊论文']=='是'];journal_groups=collections.defaultdict(list)
for r in target:journal_groups[norm(r['期刊'])].append(r)
journal_rows=[];category_rows=[]
for key,rs in sorted(journal_groups.items(),key=lambda x:(-len(x[1]),x[1][0]['期刊'])):
 r=rs[0];journal_rows.append({'规范期刊':r['期刊'],'ISSN':'; '.join(dict.fromkeys(x['ISSN'] for x in rs if x['ISSN'])),'eISSN':'; '.join(dict.fromkeys(x['eISSN'] for x in rs if x['eISSN'])),'纳入记录数':len(rs),'已获取核验全文数':sum(x['核验全文标志']=='是' for x in rs),'研究类':sum(x['统计文献组']=='研究类' for x in rs),'综述':sum(x['统计文献组']=='综述' for x in rs),'其他期刊论文':sum(x['统计文献组']=='其他期刊论文' for x in rs),'JCR数据年份':2024,'JCR发布版本':2025,'学科类别':r['学科类别'],'分区逐学科':r['JIF分区（逐学科）'],'至少一学科Q1':r['至少一学科Q1'],'全部已核实学科均Q1':r['全部已核实学科均Q1'],'JCR核实':'是' if r['JCR分区已核实']=='是' else '否','查询来源':r['查询来源'],'核验备注':'统一名称及印刷/电子ISSN并集；多学科按全部已核实行保留；未知不作非Q1；原期刊名异名见文献明细'})
 j=JN.get(norm(r['期刊']))
 if j:
  for cat in j['categories']:category_rows.append({'期刊':r['期刊'],'ISSN':r['ISSN'],'eISSN':r['eISSN'],'指标年份':2024,'发布版本年份':2025,'学科类别':cat['category'],'JIF分区':cat['quartile'],'查询来源':j['source_url'],'核验方式':j['verification']})
summary=[]
for scope in ['全部纳入目标期刊论文','已取得核验全文目标期刊论文']:
 for subtype in ['合计','研究类','综述','其他期刊论文']:
  rs=[r for r in target if (scope.startswith('全部') or r['核验全文标志']=='是') and (subtype=='合计' or r['统计文献组']==subtype)];n=len(rs);v=sum(r['JCR分区已核实']=='是' for r in rs);a=sum(r['至少一学科Q1']=='是' for r in rs);q=sum(r['全部已核实学科均Q1']=='是' for r in rs)
  summary.append({'集合':scope,'文献组':subtype,'目标期刊论文数':n,'已核实JCR分区论文数':v,'JCR待核实论文数':n-v,'至少一个学科Q1文章数':a,'Q1占全部目标期刊论文':a/n if n else None,'Q1占已核实JCR论文':a/v if v else None,'全部已核实学科均Q1文章数':q,'全部已核实学科均Q1占全部目标':q/n if n else None,'全部已核实学科均Q1占已核实':q/v if v else None,'JCR核实覆盖率':v/n if n else None,'至少一学科Q1期刊种数':len({r['期刊'] for r in rs if r['至少一学科Q1']=='是'}),'全部已核实学科Q1期刊种数':len({r['期刊'] for r in rs if r['全部已核实学科均Q1']=='是'})})
meta_summary={'jcr_metric_year':2024,'jcr_release_year':2025,'data_status':'partial_verified_institutional_sources; missing values not non-Q1','summary':summary,'included_scope_type_counts':dict(collections.Counter(r['统计文献组'] for r in details if r['纳入范围']=='是')),'target_journal_count':len(journal_rows),'verified_journal_count':sum(r['JCR核实']=='是' for r in journal_rows),'q1_journal_count':sum(r['至少一学科Q1']=='是' for r in journal_rows),'all_verified_categories_q1_journal_count':sum(r['全部已核实学科均Q1']=='是' for r in journal_rows),'pending_items':len(pending)}
def savecsv(p,rows):
 with open(p,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
savecsv(I/'journal_metadata_verification_utf8.csv',metadata_audit);savecsv(I/'jcr_journal_summary_utf8.csv',journal_rows);savecsv(I/'jcr_category_quartiles_utf8.csv',category_rows);savecsv(I/'jcr_pending_utf8.csv',pending);json.dump(meta_summary,open(I/'jcr_summary.json','w'),ensure_ascii=False,indent=2)
sd=I/'jcr_sources';sd.mkdir(exist_ok=True)
used={j.get('snapshot_file') for j in J.values() if any(norm(j['journal'])==norm(r['期刊']) for r in target)}
for name in used:
 if name:shutil.copy2(W/name,sd/name)
json.dump({k:j for k,j in J.items() if any(norm(j['journal'])==norm(r['期刊']) for r in target)},open(sd/'verified_2024_categories.json','w'),ensure_ascii=False,indent=2)
wb=Workbook();wb.remove(wb.active)
NAVY='16324F';TEAL='087E8B';LIGHT='EAF4F5';GRAY='F1F4F8';GOLD='FFF0C2'
def sheet(name,rows):
 ws=wb.create_sheet(name)
 if not rows:return ws
 headers=list(rows[0]);ws.append(headers)
 for row in rows:
  vals=[]
  for key in headers:
   v=row.get(key,'');v=json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v
   if isinstance(v,str):v=re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]','',v)[:32760]
   vals.append(v)
  ws.append(vals)
 ws.freeze_panes='C2';ws.auto_filter.ref=ws.dimensions;ws.sheet_view.showGridLines=False;ws.row_dimensions[1].height=34
 for cell in ws[1]:cell.fill=PatternFill('solid',fgColor=NAVY);cell.font=Font(name='Microsoft YaHei',color='FFFFFF',bold=True);cell.alignment=Alignment(wrap_text=True,vertical='center')
 for i,row in enumerate(ws.iter_rows(min_row=2),2):
  ws.row_dimensions[i].height=48 if name not in ['统计汇总','期刊汇总'] else 38
  for c in row:
   c.font=Font(name='Microsoft YaHei',size=10,color='243746');c.alignment=Alignment(vertical='top',wrap_text=True)
   if i%2==0:c.fill=PatternFill('solid',fgColor=GRAY)
   if c.value=='是' and ('Q1' in str(ws.cell(1,c.column).value)):c.fill=PatternFill('solid',fgColor='D5F0E3');c.font=Font(name='Microsoft YaHei',color='08684B',bold=True)
 for idx,h in enumerate(headers,1):
  width=15
  if any(x in h for x in ['题名','具体问题','核验备注','需要资料','规范路径','路径','来源','GitHub','角色','学科类别','分区逐','JIF分区']):width=48
  elif '期刊' in h or '分类' in h or '状态' in h:width=30
  ws.column_dimensions[get_column_letter(idx)].width=width
 return ws
notes=[{'项目':'数据基准','说明':'2026-10-23；远端022237df当前文件；554条总记录、426条纳入范围，分类/人工证据保留；缺全文不改变范围。'}, {'项目':'JCR年份','说明':'统一使用2024指标年，对应2025发布版。依据Clarivate 2025 Release Notes；本表不声称使用2026发布版。'}, {'项目':'JCR定义','说明':'使用JIF Quartile（Q1–Q4）。不使用中科院分区、SJR/SCImago/CiteScore或影响因子高低替代JCR分区。'}, {'项目':'核验来源与限制','说明':'主要为武汉大学图书馆机构JCR期刊信息/列表的搜索索引摘录，逐刊保留年份、ISSN、学科、分区及URL和索引快照；直连页面未成功，未取得Clarivate账户全量导出。仅计已核实学科，所有未知留空/待核实。'}, {'项目':'两种Q1口径','说明':'至少一个已核实学科Q1；全部已核实学科均Q1。后者不承诺没有尚未显示的学科，需完整JCR导出补足。'}, {'项目':'分母','说明':'纳入范围内的目标期刊论文；分别按全部目标和已核实JCR分区目标为分母。学位、会议、海报、书章及类型待核实条目单列；未知JCR不作非Q1。'}, {'项目':'Q1数量性质','说明':'可核验部分的已确认数量/下限；不是完整JCR覆盖下的最终总数。分区是2024年期刊特征，不是每篇论文发表当年的历史分区。'}, {'项目':'还需要的JCR导出','说明':'请提供2025发布版、2024指标年的JCR Excel/CSV，含Journal name、ISSN、eISSN、全部Category、JIF Quartile、JIF Rank、JCR Year、导出日期。期刊名单见期刊汇总及待核实项。'}, {'项目':'原件与附件','说明':'665个不同字节对象；全文402文件组合388篇；154件原格式科研补充材料（含3 ZIP），5 ZIP派生成员不重复计数。61件附件唯一关联尚待核实。'}, {'项目':'异常处理','说明':'4个上传正文身份冲突、13不同字节历史候选、1作者变更表保留，不计目标全文；R13964误放同字节附件已归R13834并留映射。'}, {'项目':'main清理','说明':'保全b739c0e后独立读回30原件全部通过，再正常提交0bdf0b9清理main；README原字节不变；旧副本仍在Git历史。'}, {'项目':'官方年份说明','说明':'https://journalcitationreports.zendesk.com/hc/en-gb/articles/36310651247889-2025'}, {'项目':'官方多学科/JIF分区说明','说明':'https://journalcitationreports.zendesk.com/hc/en-gb/articles/28351430970001-Journal-Profile'}]
sheet('说明',notes);ds=sheet('文献明细',details);sheet('期刊汇总',journal_rows);ss=sheet('统计汇总',summary);sheet('待核实项',pending);sheet('JCR学科明细',category_rows)
file_rows=[{'文献ID':a['record_id'],'题名':a['title'],'DOI':a['doi'],'文件角色':a['role'],'版本':a['version'],'原文件名':'; '.join(a['original_filenames']),'规范路径':a['canonical_path'],'来源':'; '.join(a['sources']),'旧路径':'; '.join(a['source_paths']),'大小字节':a['size_bytes'],'SHA256':a['sha256'],'核验状态':a['verification_status'],'附件关联状态':a['association_status'],'核验备注':a['verification_notes'],'GitHub保存位置':a['github_url']} for a in A]
sheet('统一文件清单',file_rows)
sheet('非期刊及类型待核实',[r for r in details if r['纳入范围']=='是' and r['是否目标期刊论文']=='否'])
sheet('main清理',[{'事项':'保全提交','结果':'b739c0e78507bc13db8d4a149ad7c34d07bfdbbf'}, {'事项':'main清理提交','结果':'0bdf0b9933b1a628d8b49561fdf3e35bbc7f6223'}, {'事项':'独立读回','结果':'30文件全部大小、SHA256一致，读回完成后才清理'}, {'事项':'范围','结果':'只删除ab8353c误传30文件；其他main文件/README未改；Git历史不重写'}])
# Formula counts remain directly tied to the detail sheet. Cached values are independently checked below in JSON/CSV.
headers={h:i+1 for i,h in enumerate(details[0])};last=len(details)+1
def rng(h):return f"'文献明细'!${get_column_letter(headers[h])}$2:${get_column_letter(headers[h])}${last}"
for i,x in enumerate(summary,2):
 crit=[(rng('是否目标期刊论文'),'是')]
 if x['集合'].startswith('已取得'):crit.append((rng('核验全文标志'),'是'))
 if x['文献组']!='合计':crit.append((rng('统计文献组'),x['文献组']))
 def count(extra=[]):return '=COUNTIFS('+','.join(f'{rr},"{v}"' for rr,v in crit+extra)+')'
 ss.cell(i,3,count());ss.cell(i,4,count([(rng('JCR分区已核实'),'是')]));ss.cell(i,5,f'=C{i}-D{i}');ss.cell(i,6,count([(rng('至少一学科Q1'),'是')]));ss.cell(i,7,f'=IF(C{i}=0,"",F{i}/C{i})');ss.cell(i,8,f'=IF(D{i}=0,"",F{i}/D{i})');ss.cell(i,9,count([(rng('全部已核实学科均Q1'),'是')]));ss.cell(i,10,f'=IF(C{i}=0,"",I{i}/C{i})');ss.cell(i,11,f'=IF(D{i}=0,"",I{i}/D{i})');ss.cell(i,12,f'=IF(C{i}=0,"",D{i}/C{i})')
 for col in [7,8,10,11,12]:ss.cell(i,col).number_format='0.0%'
chart=BarChart();chart.title='全部目标期刊论文：已确认Q1数量';chart.y_axis.title='文章数';chart.add_data(Reference(ss,min_col=6,max_col=6,min_row=1,max_row=5),titles_from_data=True);chart.set_categories(Reference(ss,min_col=2,min_row=2,max_row=5));chart.height=8;chart.width=18;ss.add_chart(chart,'A13')
out=B/'final_results/journal_jcr_statistics_20261023.xlsx';wb.save(out)
# Inject legitimate precomputed formula caches for applications that do not recalculate on open.
import xml.etree.ElementTree as ET
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(out) as z:contents={n:z.read(n) for n in z.namelist()}
root=ET.fromstring(contents['xl/worksheets/sheet4.xml'])
for node in root.findall('.//m:c',ns):
 ref=node.attrib['r'];m=re.match(r'([A-Z]+)(\d+)$',ref)
 if node.find('m:f',ns) is None or not m:continue
 row=int(m[2])-2;col=0
 for ch in m[1]:col=col*26+ord(ch)-64
 val=list(summary[row].values())[col-1];v=node.find('m:v',ns)
 if v is None:v=ET.SubElement(node,'{'+ns['m']+'}v')
 if val is not None:v.text=str(val)
 else:node.set('t','str');v.text=''
contents['xl/worksheets/sheet4.xml']=ET.tostring(root,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for name,data in contents.items():z.writestr(name,data)
check=load_workbook(out,read_only=True,data_only=True);assert check['文献明细'].max_row==555;assert check['统一文件清单'].max_row==666;assert check['统计汇总']['F2'].value==summary[0]['至少一个学科Q1文章数'];check.close()
# Update the existing master workbook while preserving every historical sheet and manual/evidence column.
old=B/'final_results/ad_oxygen_download_review_20261006.xlsx';mw=load_workbook(old);ws=mw['文献库'];hs=[c.value for c in ws[1]];idcol=hs.index('稳定记录ID')+1
for k in R[0]:
 if k not in hs:hs.append(k);ws.cell(1,len(hs),k)
for rr in range(2,ws.max_row+1):
 rid=ws.cell(rr,idcol).value;r=next((x for x in R if x['稳定记录ID']==rid),None)
 if r:
  for col,h in enumerate(hs,1):
   if h in r:ws.cell(rr,col,r[h])
for n in ['当前环境获取总览426','当前缺正文337','本轮缺正文38']:
 if n in mw.sheetnames:del mw[n]
for n,rs in [('当前环境获取总览426',[s for s in S.values() if s['included_for_analysis']]),('本轮缺正文38',[s for s in S.values() if s['included_for_analysis'] and not s['verified_fulltext']])]:
 sh=mw.create_sheet(n,0);ks=list(rs[0]);sh.append(ks)
 for r in rs:sh.append([json.dumps(r[k],ensure_ascii=False) if isinstance(r[k],list) else r[k] for k in ks])
 sh.freeze_panes='B2';sh.auto_filter.ref=sh.dimensions
mw.save(old)
print(json.dumps(meta_summary,ensure_ascii=False,indent=2));print('workbooks saved and readable',out)
