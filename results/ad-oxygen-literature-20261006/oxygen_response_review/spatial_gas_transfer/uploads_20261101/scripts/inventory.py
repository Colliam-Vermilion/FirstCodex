import fitz,hashlib,json,re
from pathlib import Path
R=Path('/workspace/FirstCodex');T=R/'results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer';P=T/'uploads_20261101';(P/'texts').mkdir(parents=True,exist_ok=True)
rows=[]
for p in sorted((R/'scientific_guide/NewPart1Articles').rglob('*')):
 if not p.is_file():continue
 h=hashlib.sha256(p.read_bytes()).hexdigest();z={'original_path':str(p.relative_to(R)),'original_filename':p.name,'sha256':h,'bytes':p.stat().st_size,'source':'user upload; branch 5910977','canonical_path':str(p.relative_to(R))}
 try:
  d=fitz.open(p);pages=[{'pdf_page':i+1,'text':x.get_text()} for i,x in enumerate(d)];z.update(pages=len(d),text_characters=sum(len(x['text']) for x in pages),metadata=d.metadata)
  (P/'texts'/f'{h[:16]}.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2));(P/'texts'/f'{h[:16]}.txt').write_text('\n'.join(f"\n===== PDF PAGE {x['pdf_page']} =====\n{x['text']}" for x in pages))
  z['text_path']=str((P/'texts'/f'{h[:16]}.json').relative_to(R));z['doi_candidates_first2pages']=list(dict.fromkeys(re.findall(r'10\.\d{4,9}/[^\s<>]+',' '.join(x['text'] for x in pages[:2]),re.I)))
 except Exception as e:z['error']=str(e)
 rows.append(z)
(P/'file_inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for i,z in enumerate(rows):print(i,z['original_filename'],z.get('pages'),z.get('doi_candidates_first2pages'),z.get('error',''))
