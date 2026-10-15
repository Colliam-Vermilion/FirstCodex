"""Offline verification of TLS/proxy adapter; no HTTP request is sent."""
import json,os,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
# Harmless fake proxy is confined to a child process whose send function is captured.
child=r'''
import bootstrap,requests,json
captured={}
def capture(self,request,**kwargs):
 captured.update(kwargs);return kwargs
bootstrap._original_send=capture
from scansci_pdf.config import load_config
from scansci_pdf.network import _get_session
s=_get_session(load_config())
s.send(requests.Request('GET','https://example.invalid/').prepare(),verify=False,proxies={})
plain=requests.Session();plain.send(requests.Request('GET','https://example.invalid/').prepare(),verify=False,proxies=None)
result={'network_requests_sent':0,'fake_proxy_capture_only':True,
 'new_requests_sessions_use_explicit_proxy':plain.proxies.get('https')==bootstrap._proxy,
 'sdk_session_trust_env_disabled':s.trust_env is False,
 'verify_false_overridden':captured.get('verify')==bootstrap._verify and bool(captured.get('verify')),
 'empty_or_none_proxies_overridden':captured.get('proxies',{}).get('https')=='http://127.0.0.1:9',
 'configured_CA_exists':not bootstrap._ca or __import__('pathlib').Path(bootstrap._ca).is_file()}
assert all(v is True for k,v in result.items() if k!='network_requests_sent')
print(json.dumps(result))
'''
env=dict(os.environ)
for k in ['HTTP_PROXY','HTTPS_PROXY','http_proxy','https_proxy','SCANSCI_PDF_PROXY']:
    env[k]='http://127.0.0.1:9'
env['PYTHONPATH']=str(BASE)
proc=subprocess.run([sys.executable,'-c',child],env=env,cwd=BASE,text=True,capture_output=True,check=True)
result=json.loads(proc.stdout)
(BASE/'transport_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
