import sys,json
from pathlib import Path
sys.path.insert(0,'/workspace/scansci-pdf-runtime');import bootstrap
from scansci_pdf.sources import download
P=Path('/workspace/FirstCodex/results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/uploads_20261101');f=P/'originals';f.mkdir(exist_ok=True)
r=download('10.1128/jb.178.24.7322-7325.1996',str(f),scihub_enabled=False,strategy='legal_only',rename=False,_institutional=False)
(P/'new_fulltext_attempt.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print('success',r.get('success'))
