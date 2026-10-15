"""Merge authorized contact and safe source defaults into private local config."""
import json,os
from pathlib import Path
import bootstrap
from scansci_pdf.config import CONFIG_FILE,load_config,save_config
cfg=load_config()
contact=os.environ.get('SCANSCI_CONTACT_EMAIL') or cfg.get('email','')
if not contact or '@' not in contact or contact.endswith('.invalid'):
    raise RuntimeError('Set SCANSCI_CONTACT_EMAIL in environment settings; never place it in a committed file')
cfg.update(email=contact,download_strategy='legal_only',scihub_enabled=False,
    scihub_domains=[],use_tor_for_scihub=False,scihub_direct=False,
    scihub_turnstile_click=False,scihub_browser_first=False,auto_relogin=False,
    ezproxy_enabled=False,vpnsci_enabled=False,carsi_enabled=False,
    parallel_sources=False,parallel_probes=False,batch_workers=1,
    institutional_workers=1,fixed_request_delay_enabled=True,
    request_delay_min=5.,request_delay_max=12.,proxy_pool='',direct_domains=[],
    download_si=True,progress_bar_auto=False)
save_config(cfg)
os.chmod(CONFIG_FILE,0o600)
print(json.dumps({'private_config_saved':True,'legal_only':True,'gray_sources_disabled':True,
    'contact_present':True,'credentials_values_not_exported':True}))
