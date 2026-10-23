import pathlib,json,csv,hashlib,re,unicodedata,html,zipfile,collections,subprocess,concurrent.futures,difflib
import fitz
BASE=pathlib.Path('/workspace/work/snapshot/results/ad-oxygen-literature-20261006')
W=pathlib.Path('/workspace/work');(W/'texts').mkdir(exist_ok=True)
rs=list(csv.DictReader(open(W/'remote_master.csv',encoding='utf-8-sig')));records={r['稳定记录ID']:r for r in rs}
def norm(s):return re.sub(r'[^a-z0-9\u4e00-\u9fff]','',unicodedata.normalize('NFKD',html.unescape(s)).lower())
assets=list(csv.DictReader(open(BASE/'inventory/assets_utf8.csv',encoding='utf-8-sig')))
bysha=collections.defaultdict(list)
for a in assets:bysha[a['sha256']].append(a)
paths=[p for root in ['localdownload','original_files'] for p in (BASE/root).rglob('*') if p.is_file() and p.name not in ['README.md','ATTRIBUTION_utf8.csv']]
def inspect(p):
 data=p.read_bytes();sha=hashlib.sha256(data).hexdigest();rel=str(p.relative_to(BASE));ids=re.findall(r'R\d{5}',rel);rid=ids[0] if ids else ''
 a={'source_path':rel,'source':'local_upload' if rel.startswith('localdownload/') else 'cloud_existing','directory_id':rid,'record_id':rid,'original_filename':p.name,'size_bytes':len(data),'sha256':sha,'git_blob_oid':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),'format':p.suffix.lower().lstrip('.'),'prior_assets':bysha.get(sha,[]),'issues':[]}
 if rid not in records:a['issues'].append('unmatched_directory_id')
 declared=norm(p.stem)
 role=('fulltext' if declared in ['fulltext','fultext','fulltxt','fulltext1','fullpaper'] else 'abstract' if declared in ['abstract','abstarct','abtract'] else 'poster' if declared in ['poster','postar'] else 'supplementary') if a['source']=='local_upload' else ''
 if not role:
  pri=bysha.get(sha,[])
  proles={x.get('role') for x in pri}
  if 'derived' in proles or '/derived/' in rel:role='derived'
  elif 'main' in proles or rel.startswith('original_files/fulltext/'):role='fulltext'
  elif 'supplementary' in proles:role='supplementary'
  elif '/source_evidence/' in rel:role='source_evidence'
  elif '/candidates/' in rel:role='uncertain'
  else:role='source_evidence'
 a['declared_role']=role;a['role']=role;a['version']='';a['verification_status']='pending';head='';text=''
 try:
  if a['format']=='pdf':
   doc=fitz.open(stream=data,filetype='pdf');a['pages']=len(doc);a['encrypted']=bool(doc.needs_pass)
   if doc.needs_pass:raise ValueError('encrypted password required')
   # Every page is parsed; renderability is checked for first and last pages.
   texts=[page.get_text() for page in doc];text='\n'.join(texts);head='\n'.join(texts[:2]);a['page_text_lengths']=[len(t) for t in texts]
   a['first_page_size']=[doc[0].rect.width,doc[0].rect.height] if len(doc) else []
   if len(doc):doc[0].get_pixmap(matrix=fitz.Matrix(.15,.15));doc[-1].get_pixmap(matrix=fitz.Matrix(.15,.15))
   a['text_length']=len(text);a['repaired_pdf']=bool(doc.is_repaired)
   if doc.is_repaired:a['issues'].append('pdf_repair_needed')
   if len(text)<150:a['issues'].append('scan_or_no_extractable_text')
  elif a['format'] in ['docx','xlsx','zip']:
   with zipfile.ZipFile(p) as z:
    bad=z.testzip();a['archive_members']=[{'name':i.filename,'size':i.file_size,'encrypted':bool(i.flag_bits&1)} for i in z.infolist()]
    if bad:raise ValueError('ZIP CRC error '+bad)
    if a['format']=='docx':text=' '.join(re.sub('<[^>]+>',' ',z.read(n).decode('utf8')) for n in z.namelist() if n.startswith('word/') and n.endswith('.xml'));text=html.unescape(text)
    elif a['format']=='xlsx':text=' '.join(re.sub('<[^>]+>',' ',z.read(n).decode('utf8')) for n in z.namelist() if n in ['xl/sharedStrings.xml'] or n.startswith('xl/worksheets/sheet'));text=html.unescape(text)
    elif a['format']=='zip':text='\n'.join(i.filename for i in z.infolist())
   a['verification_status']='container_crc_verified'
  elif a['format'] in ['txt','xml','html','json','jsonl','csv']:text=data.decode('utf8',errors='replace');a['verification_status']='text_readable'
  elif a['format'] in ['jpg','jpeg','png']:
   from PIL import Image
   with Image.open(p) as im:a['image_size']=im.size;im.verify()
   a['verification_status']='image_decode_verified'
  elif a['format']=='doc':
   a['ole_signature_ok']=data.startswith(bytes.fromhex('d0cf11e0a1b11ae1'))
   text=subprocess.run(['strings','-el',str(p)],capture_output=True,text=True).stdout
   if not a['ole_signature_ok']:raise ValueError('not an OLE Word document')
   a['verification_status']='ole_signature_and_strings_only';a['issues'].append('legacy_doc_full_render_not_verified')
  else:a['verification_status']='format_not_validated';a['issues'].append('format_not_validated')
 except Exception as e:a['verification_status']='unreadable';a['issues'].append(str(e))
 if text:
  (W/'texts'/f'{sha}.txt').write_text(text)
  a['text_path']=f'work/texts/{sha}.txt'
  if not head:head=text[:10000]
 a['head_excerpt']=head[:5500];a['tail_excerpt']=text[-1000:];nh=norm(head);r=records.get(rid,{})
 title=r.get('完整题名','');doi=r.get('DOI','')
 a['expected_doi_in_head']=bool(doi and norm(doi) in nh)
 toks=set(re.findall(r'[a-z]{3,}',unicodedata.normalize('NFKD',html.unescape(title)).lower()))
 a['title_token_coverage']=round(len(toks&set(re.findall(r'[a-z]{3,}',head.lower())))/len(toks),3) if toks else 0
 a['title_compact_match']=len(norm(title))>25 and norm(title) in nh
 matches=[rr['稳定记录ID'] for rr in rs if rr['DOI'] and norm(rr['DOI']) in nh]
 a['head_doi_matching_ids']=matches
 if role in ['fulltext','abstract','poster'] and not (a['expected_doi_in_head'] or a['title_token_coverage']>=.7 or a['title_compact_match']):a['issues'].append('identity_requires_review')
 a['body_markers']=[k for k,patt in {'intro':r'\bintroduction\b','methods':r'\b(materials and methods|methodology|experimental|methods)\b','results':r'\bresults\b','conclusion':r'\bconclusions?\b','references':r'\b(references|bibliography)\b'}.items() if re.search(patt,text,re.I)]
 a['body_candidate_complete']=a.get('pages',0)>=3 and len(text)>5500 and len(a['body_markers'])>=3
 if role=='fulltext' and not a['body_candidate_complete']:a['issues'].append('body_completeness_requires_review')
 if role=='fulltext':
  v=[x['version'] for x in bysha.get(sha,[]) if x.get('version')]
  if v:a['version']='; '.join(dict.fromkeys(v))
  elif re.search(r'accepted manuscript|author.{0,3}s accepted|accepted version',head,re.I):a['version']='作者接受稿（文件文字）'
  elif re.search(r'Elsevier|Springer|Wiley|MDPI|Taylor & Francis|Published by|ACS Publications|Royal Society of Chemistry|©|Copyright',head,re.I):a['version']='出版版（版式及版权文字）'
  else:a['version']='版本待核实'
 if role=='fulltext' and a['body_candidate_complete'] and (a['expected_doi_in_head'] or a['title_token_coverage']>=.7 or a['title_compact_match']) and a['verification_status']!='unreadable':a['verification_status']='identity_and_body_structure_verified'
 elif a['format']=='pdf' and a['verification_status']=='pending':a['verification_status']='pdf_readable_requires_role_review'
 return a
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:out=list(pool.map(inspect,paths))
json.dump(out,open(W/'file_audit_initial.json','w'),ensure_ascii=False,indent=2)
print('paths',len(out),'unique hashes',len({a['sha256'] for a in out}),'roles',collections.Counter(a['role'] for a in out))
print('local issues')
for a in out:
 if a['source']=='local_upload' and a['issues']:print(a['source_path'],a.get('pages'),a['issues'],a['title_token_coverage'],a['head_doi_matching_ids'])
