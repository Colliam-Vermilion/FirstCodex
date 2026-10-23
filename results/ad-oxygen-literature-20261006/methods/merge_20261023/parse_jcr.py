import pathlib,json,re,html,collections,unicodedata
out={};sources=[]
def norm(s):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',html.unescape(s)).lower())
for f in sorted(pathlib.Path('/workspace/work').glob('jcr_search_*.json')):
 d=json.load(f.open());raw='\n'.join(x.get('text','') for x in d.get('content',[]))
 for block in re.split(r'\n-{20,}\n',raw):
  url=re.search(r'\((https://topj\.lib\.whu\.edu\.cn/show\.asp[^)]+)\)',block)
  name=re.search(r'刊名全称[:：](.*?)\s+ISSN[:：]\s*([0-9Xx\-]*)',block)
  if not(url and name and '影响因子(2024)' in block):continue
  title=name[1].strip();issn=name[2].strip();part=block.split('JCR学科及分区：')
  if len(part)<2:continue
  cats=list(dict.fromkeys(re.findall(r'→(?:SCIE|SSCI|AHCI|ESCI|A&HCI)[:：]([^\n]+?)\((Q[1-4])\)',part[1].split('ESI期刊信息')[0])))
  if not cats:continue
  cats=[{'category':x.strip(),'quartile':q} for x,q in cats]
  entry={'journal':title,'issn':issn[:4]+'-'+issn[4:] if len(issn)==8 else issn,'jcr_metric_year':2024,'jcr_release_year':2025,'categories':cats,'source_url':html.unescape(url[1]),'verification':'机构JCR栏：搜索索引可核验；原页面直连未成功；非Clarivate账户导出','queried_at_date':'2026-10-23','snapshot_file':f.name}
  key=norm(title)
  if key in out and out[key]['categories']!=cats:
   sources.append({'conflict_key':key,'old':out[key],'new':entry})
   if len(out[key]['categories'])>=len(cats):continue
  out[key]=entry
for f in list(pathlib.Path('/workspace/work').glob('jcr_search_*.json'))+list(pathlib.Path('/workspace/work').glob('jcr_extra_*.json')):
 raw='\n'.join(x.get('text','') for x in json.load(f.open()).get('content',[]))
 for block in re.split(r'\n-{20,}\n',raw):
  url=re.search(r'\((https://topj\.lib\.whu\.edu\.cn/(?:search[^)]*)?)\)',block)
  if not url or '影响因子(2024)' not in block or 'JCR学科(分区)' not in block:continue
  chunks=re.split(r'(?m)^\s*(\d+)\s+\|',block)
  for i in range(2,len(chunks)-2,2):
   row=chunks[i];fields=row.split('|')
   if len(fields)<5:continue
   title=fields[1].strip();issn=fields[2].strip();key=norm(title)
   if key in out:continue
   catpart='|'.join(fields[4:])
   cats=list(dict.fromkeys(re.findall(r'(?:SCIE:|SSCI:|ESCI:)?([A-Z][A-Z, &\-]+)\((Q[1-4])\)',catpart)))
   if not cats or len(issn)!=8:continue
   out[key]={'journal':title,'issn':issn[:4]+'-'+issn[4:],'jcr_metric_year':2024,'jcr_release_year':2025,'categories':[{'category':x.strip(),'quartile':q} for x,q in cats],'source_url':html.unescape(url[1]),'verification':'机构2024年JCR列表栏：搜索索引可核验；原页直连未成功；仅统计已显示学科','queried_at_date':'2026-10-23','snapshot_file':f.name,'category_coverage':'displayed_verified_categories_only'}
json.dump(out,open('/workspace/work/jcr_verified.json','w'),ensure_ascii=False,indent=2)
json.dump(sources,open('/workspace/work/jcr_conflicts.json','w'),ensure_ascii=False,indent=2)
print('journals',len(out),'conflicts',len(sources));print('\n'.join(f'{v["journal"]}\t'+str([(x['category'],x['quartile']) for x in v['categories']]) for v in out.values()))
