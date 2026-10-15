"""Behavior tests for corrupt transfers, source throttling, review and ID/SHA merge.
Uses existing permissive article bytes plus temporary HTTP fixtures; no publisher requests.
"""
from pathlib import Path
from types import SimpleNamespace
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
import unittest,tempfile,json,hashlib,csv,shutil,zipfile,contextlib,io
import download_local as dl
import transfer_library as tr
from audit_library import dump,sha,write_csv
PROJECT=Path(__file__).resolve().parents[2]


class Workflow(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='文献 workflow ');self.base=Path(self.tmp.name);self.root=self.base/'local library';self.project=self.base/'project';self.root.mkdir();self.project.mkdir();(self.project/'inventory').mkdir()
        self.meta=json.loads((PROJECT/'papers/R03161/metadata.json').read_text());self.meta['assets']=[];dump(self.project/'papers/R03161/metadata.json',self.meta);dump(self.project/'inventory/assets.json',[])
        self.pdf=(PROJECT/'original_files/fulltext/R03161_2017_Effect_of_liquid_surface_area_on_hydrogen_sulfide_oxidation.pdf').read_bytes()
    def tearDown(self):self.tmp.cleanup()
    def args(self,**kwargs):
        defaults={'project':self.project,'root':self.root};defaults.update(kwargs);return SimpleNamespace(**defaults)
    def serve(self):
        data=self.pdf;seen=[]
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_GET(h):
                seen.append((h.path,h.headers.get('Range')))
                if h.path=='/rate.pdf':h.send_response(429);h.send_header('Retry-After','120');h.end_headers();return
                if h.path=='/login.pdf':raw=b'<!DOCTYPE html><html><title>Login</title></html>';h.send_response(200);h.send_header('Content-Type','application/pdf');h.end_headers();h.wfile.write(raw);return
                start=int(h.headers['Range'].split('=')[1].split('-')[0]) if h.headers.get('Range') and h.path!='/ignore.pdf' else 0
                raw=data[start:];h.send_response(206 if start else 200);h.send_header('ETag','"stable"');h.send_header('Content-Type','application/pdf');h.send_header('Content-Length',str(len(raw)))
                if start:h.send_header('Content-Range',f'bytes {start}-{len(data)-1}/{len(data)}')
                h.end_headers();h.wfile.write(raw)
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=Thread(target=server.serve_forever,daemon=True);thread.start();self.addCleanup(server.server_close);self.addCleanup(server.shutdown);return server.server_port,seen
    def download(self,rows,retry=False):
        queue=self.base/'queue.csv';write_csv(queue,rows)
        with contextlib.redirect_stdout(io.StringIO()):dl.download(self.args(queue=queue,delay=3,max_mib=100,retry_failed=retry))
        return json.loads((self.root/'intake/download_state.json').read_text())
    def test_login_html_never_counts_as_original(self):
        port,seen=self.serve();state=self.download([{'record_id':'R03161','role':'main','url':f'http://127.0.0.1:{port}/login.pdf'}]);self.assertNotIn('downloaded_pending_review',[x['status'] for x in state.values()])
    def test_range_resume_yields_exact_source_sha(self):
        port,seen=self.serve();url=f'http://127.0.0.1:{port}/main.pdf';key=hashlib.sha256(('R03161|main|'+url).encode()).hexdigest();folder=self.root/'intake/R03161/main';folder.mkdir(parents=True);part=folder/(key[:12]+'_main.pdf.part');part.write_bytes(self.pdf[:1000]);dump(part.with_suffix('.resume.json'),{'validator':'"stable"'})
        state=self.download([{'record_id':'R03161','role':'main','url':url}]);r=next(iter(state.values()));self.assertEqual(r['sha256'],hashlib.sha256(self.pdf).hexdigest());self.assertEqual(seen[0][1],'bytes=1000-');self.assertFalse(r['identity_verified'])
    def test_ignored_range_restarts_without_corrupt_append(self):
        port,seen=self.serve();url=f'http://127.0.0.1:{port}/ignore.pdf';key=hashlib.sha256(('R03161|main|'+url).encode()).hexdigest();folder=self.root/'intake/R03161/main';folder.mkdir(parents=True);part=folder/(key[:12]+'_ignore.pdf.part');part.write_bytes(self.pdf[:123]);dump(part.with_suffix('.resume.json'),{'validator':'"stable"'})
        state=self.download([{'record_id':'R03161','role':'main','url':url}]);self.assertEqual(next(iter(state.values()))['sha256'],hashlib.sha256(self.pdf).hexdigest())
    def test_retry_after_survives_resume_and_other_host_continues(self):
        another=dict(self.meta);another['record_id']='R06325';dump(self.project/'papers/R06325/metadata.json',another)
        port,seen=self.serve();rows=[{'record_id':'R03161','role':'main','url':f'http://127.0.0.1:{port}/rate.pdf'},{'record_id':'R06325','role':'main','url':f'http://localhost:{port}/main.pdf'}]
        self.download(rows);self.assertEqual(len(seen),2);self.download(rows,retry=True);self.assertEqual(len(seen),2)
    def test_same_candidate_not_downloaded_twice_and_reject_is_explicit(self):
        port,seen=self.serve();row={'record_id':'R03161','role':'main','url':f'http://127.0.0.1:{port}/main.pdf'};state=self.download([row]);self.download([row]);self.assertEqual(len(seen),1)
        path=Path(next(iter(state.values()))['path']);dl.reject(self.args(id='R03161',file=path,evidence='Fixture review: wrong article'));self.download([row],retry=True);self.assertEqual(len(seen),1)
    def test_explicit_none_requires_both_source_checks(self):
        with self.assertRaises(ValueError):dl.si_review(self.args(id='R03161',status='explicit_none',publisher_checked=True,repository_checked=False,evidence='no links',url=[]))
    def test_register_refuses_excluded(self):
        m=dict(self.meta);m['record_id']='R99999';m['included_for_download']=False;dump(self.project/'papers/R99999/metadata.json',m)
        with self.assertRaises(ValueError):dl.register(self.args(id='R99999',role='main',reviewed=True,evidence='x',version='publisher_version',file=self.base/'not_needed.pdf',url=''))
    def register_pdf(self):
        path=self.base/'原始 正文.pdf';path.write_bytes(self.pdf)
        with contextlib.redirect_stdout(io.StringIO()):dl.register(self.args(id='R03161',role='main',reviewed=True,evidence='Existing permissive paper PDF p1 title/authors and source DOI reviewed',version='publisher_version',file=path,url='https://example.org/article.pdf'))
    def test_private_return_roundtrip_merge_is_idempotent(self):
        self.register_pdf();out=self.base/'return.zip'
        with contextlib.redirect_stdout(io.StringIO()):tr.prepare_return(self.args(out=out))
        receipt=tr.verify_package(out);self.assertTrue(receipt['all_member_sha_verified']);other=self.base/'return readback'
        with contextlib.redirect_stdout(io.StringIO()):tr.hydrate(self.args(package=out,expected_sha256=receipt['package_sha256'],root=other))
        with contextlib.redirect_stdout(io.StringIO()):tr.merge(self.args(root=other));tr.merge(self.args(root=other))
        self.assertEqual(len(json.loads((self.project/'inventory/assets.json').read_text())),1);report=json.loads((self.project/'inventory/last_return_merge.json').read_text());self.assertEqual(len(report['duplicate_assets_skipped']),1)
    def test_sha_corruption_and_zip_path_traversal_rejected(self):
        path=self.base/'bad.zip'
        with zipfile.ZipFile(path,'w') as z:z.writestr('../escape.txt','x');z.writestr('transfer_manifest.json',json.dumps({'kind':'bad','files':[]}))
        with self.assertRaises(ValueError):tr.verify_package(path)
        with self.assertRaises(ValueError):tr.verify_package(path,'0'*64)
    def test_zip_attachment_preserves_nontext_and_parses_members_separately(self):
        path=self.base/'supp.zip'
        with zipfile.ZipFile(path,'w') as z:z.writestr('data/table.csv','field,value\noxygen,1\n');z.writestr('images/model.skp',b'model-byte-fixture')
        with contextlib.redirect_stdout(io.StringIO()):dl.register(self.args(id='R03161',role='supplementary',reviewed=True,association_reviewed=True,evidence='Fixture parent association explicit',version=None,file=path,url='https://example.org/supp.zip'))
        assets=json.loads((self.root/'intake/assets.json').read_text());self.assertEqual(len(assets),3);self.assertEqual(sum(a['official_attachment'] for a in assets),1);self.assertTrue(all(a['archive_parent_asset_id'] for a in assets if a['role']=='derived'))
    def test_merge_preflight_fails_without_partial_metadata_changes(self):
        self.register_pdf();assets=json.loads((self.root/'intake/assets.json').read_text());assets.append(dict(assets[0],asset_id='R03161.main.'+'0'*16,sha256='0'*64));dump(self.root/'inventory/returned_assets.json',assets);before=(self.project/'papers/R03161/metadata.json').read_bytes()
        with self.assertRaises(ValueError):tr.merge(self.args())
        self.assertEqual(before,(self.project/'papers/R03161/metadata.json').read_bytes())
    def test_review_only_return_without_downloads_is_mergeable(self):
        m=json.loads((self.project/'papers/R03161/metadata.json').read_text());m['supplementary_official_count']=0;dump(self.project/'papers/R03161/metadata.json',m)
        with contextlib.redirect_stdout(io.StringIO()):dl.si_review(self.args(id='R03161',status='explicit_none',publisher_checked=True,repository_checked=True,evidence='Unit fixture: both source scopes checked',url=[]))
        out=self.base/'review-only.zip'
        with contextlib.redirect_stdout(io.StringIO()):tr.prepare_return(self.args(out=out))
        other=self.base/'review readback'
        with contextlib.redirect_stdout(io.StringIO()):tr.hydrate(self.args(package=out,expected_sha256=sha(out),root=other));tr.merge(self.args(root=other))
        self.assertEqual(json.loads((self.project/'papers/R03161/metadata.json').read_text())['supplementary_status'],'explicit_none')
        self.assertEqual(json.loads((self.project/'inventory/assets.json').read_text()),[])
    def test_changed_package_never_overwrites_prior_delivery(self):
        source=self.base/'data.txt';source.write_text('initial bytes');output=self.base/'delivery.zip'
        tr.write_package(output,[('data.txt',source,'fixture')],'unit_fixture',{});before=sha(output);source.write_text('changed bytes')
        with self.assertRaises(FileExistsError):tr.write_package(output,[('data.txt',source,'fixture')],'unit_fixture',{})
        self.assertEqual(sha(output),before)
    def test_csv_quoted_multiline_fields_and_locator_are_preserved(self):
        from extract_search import extract_asset
        source=self.base/'table.csv';expected=[['编号','测量值','备注'],['1','0.25','含,逗号\n换行']]
        with source.open('w',encoding='utf-8-sig',newline='') as f:csv.writer(f).writerows(expected)
        digest=sha(source);a={'record_id':'R03161','asset_id':'R03161.supplementary.'+digest[:16],'role':'supplementary','resolved_source_path':str(source),'original_filename':'table.csv','canonical_path':'papers/R03161/supplementary/table.csv','sha256':digest,'format':'csv'}
        report=extract_asset((a,str(self.root),False));self.assertEqual(report['status'],'parsed');folder=Path(report['output_directory'])
        with (folder/'tables/table.csv').open(encoding='utf-8-sig',newline='') as f:self.assertEqual(list(csv.reader(f)),expected)
        chunks=[json.loads(x) for x in (folder/'chunks.jsonl').read_text().splitlines()];self.assertEqual(chunks[1]['location']['row'],2);self.assertIn('含,逗号\n换行',chunks[1]['text'])
    def test_secret_query_redaction_does_not_change_article_identity(self):
        url=tr.redact_url('https://user:pass@example.org/paper.pdf?doi=10.1%2Fx&X-Amz-Signature=secret')
        self.assertNotIn('secret',url);self.assertNotIn('pass',url);self.assertIn('doi=10.1%2Fx',url)


if __name__=='__main__':unittest.main(verbosity=2)
