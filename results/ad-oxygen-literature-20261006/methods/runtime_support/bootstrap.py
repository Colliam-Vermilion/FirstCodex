"""Current-environment HTTPS proxy and trust adapter for scansci-pdf 1.18.0.

No proxy address or credentials are embedded. Do not use without a trusted CA.
This deliberately restores TLS verification for upstream verify=False paths.
"""
import os
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent
os.environ.setdefault('SCANSCI_PDF_DATA_DIR', str(RUNTIME / 'data'))
_platform_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
if _platform_proxy:
    os.environ.setdefault('SCANSCI_PDF_PROXY', _platform_proxy)
_proxy = os.environ.get('SCANSCI_PDF_PROXY', '')
_ca = os.environ.get('REQUESTS_CA_BUNDLE') or os.environ.get('SSL_CERT_FILE')
if _ca and not Path(_ca).is_file():
    raise RuntimeError('Configured trusted CA bundle does not exist')
_verify = _ca or True

import requests
_original_init = requests.sessions.Session.__init__
_original_send = requests.sessions.Session.send

def _init(self, *args, **kwargs):
    _original_init(self, *args, **kwargs)
    self.trust_env = False
    self.verify = _verify
    if _proxy:
        self.proxies.update({'http': _proxy, 'https': _proxy})

def _send(self, request, **kwargs):
    kwargs['verify'] = _verify
    if _proxy:
        kwargs['proxies'] = {'http': _proxy, 'https': _proxy}
    return _original_send(self, request, **kwargs)

requests.sessions.Session.__init__ = _init
requests.sessions.Session.send = _send
