"""Reconstruct verified public PDFs locally, or verify locally exported PDFs.

This retrieves recorded original sources, not a cloud-workspace download URL.
It never logs in, imports cookies, disables TLS, or substitutes an unverified PDF.
"""
from pathlib import Path
import argparse,csv,hashlib,json,os,tempfile,time,urllib.request

def digest(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--manifest',type=Path,default=Path(__file__).resolve().parent/'audit/scansci_verified_pdf_manifest_utf8.csv')
 ap.add_argument('--out',type=Path,default=Path('ad-oxygen-fulltexts'))
 ap.add_argument('--verify-only',action='store_true',help='Only verify files already copied/exported locally; no network')
 args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
 with args.manifest.open(encoding='utf-8-sig',newline='')as f:rows=list(csv.DictReader(f))
 passed=0;missing=[]
 for row in rows:
  id=row['原记录ID'];name=row['PDF文件名'];expected=row['SHA256'];dest=args.out/Path(name).name
  if dest.exists()and digest(dest)==expected:passed+=1;print(id,'已有文件SHA256一致');continue
  if args.verify_only:missing.append(id);print(id,'缺少文件或校验不一致');continue
  urls=[]
  actual=row['实际PDF来源URL（下载或历史记录明确）']
  if actual:urls.append(actual)
  urls+=json.loads(row['公开PDF候选URL（非下载URL绑定实录）']or'[]')
  urls=list(dict.fromkeys(u for u in urls if u.startswith(('https://','http://'))))
  ok=False
  for url in urls:
   temp=None
   try:
    req=urllib.request.Request(url,headers={'User-Agent':'Academic PDF manifest retrieval/1.0'})
    with urllib.request.urlopen(req,timeout=45)as res:
     with tempfile.NamedTemporaryFile(delete=False,dir=args.out,suffix='.part')as f:
      temp=Path(f.name)
      while True:
       chunk=res.read(1024*1024)
       if not chunk:break
       f.write(chunk)
    if digest(temp)!=expected:print(id,'此来源字节与已验证SHA不同；保留原文件并尝试下一记录来源');continue
    with temp.open('rb')as f:assert f.read(1024).lstrip().startswith(b'%PDF')
    temp.replace(dest);passed+=1;ok=True;print(id,'已从原来源重取，SHA256一致');break
   except Exception as ex:print(id,'来源未成功',type(ex).__name__)
   finally:
    if temp and temp.exists():temp.unlink()
   time.sleep(2)
  if not ok:missing.append(id);print(id,'需从记录中的官方文章/仓储入口手动获取；不会改用未知来源')
 print('已恢复/验证',passed,'/',len(rows),'；尚未恢复',len(missing))
 if missing:print('ID：',', '.join(missing))
 return 0 if not missing else 1

if __name__=='__main__':raise SystemExit(main())
