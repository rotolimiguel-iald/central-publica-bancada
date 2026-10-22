"""Apply only ROOT-reviewed snapshot plan; no providers, scientific code or index writes."""
from pathlib import Path
import argparse,hashlib,json,os,sys
W=Path(__file__).resolve().parent;BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.dont_write_bytecode=True;sys.path.insert(0,str(BASE))
from iald_orchestrator.safe_files import replace_bytes,save_json
sha=lambda b:hashlib.sha256(b).hexdigest()
def main(review_path):
    if (W/'INSTALL_STARTED.json').exists():raise ValueError('Prior attempt exists; inspect, no automatic repeat')
    manifest_raw=(W/'REVIEW_MANIFEST.json').read_bytes();review=json.loads(Path(review_path).read_bytes())
    if review.get('status')!='PASS' or review.get('review_manifest_sha256')!=sha(manifest_raw):raise ValueError('ROOT review missing or differs')
    for item in json.loads(manifest_raw)['members']:
        p=Path(item['path']);raw=p.read_bytes()
        if len(raw)!=item['bytes'] or sha(raw)!=item['sha256']:raise ValueError('Reviewed artifact changed')
    plan=json.loads((W/'INSTALL_PLAN.json').read_bytes());prep=json.loads((W/'PREPARATION.json').read_bytes())
    index=BASE/'state/canonical_memory/index.sqlite3';catalog=BASE/'project_fisica/MANIFESTO_LOCAL.json'
    if sha(index.read_bytes())!=plan['index_sha256'] or sha(catalog.read_bytes())!=prep['historical_catalog_sha256']:raise ValueError('Index/catalog baseline changed')
    target=Path(prep['snapshot_target']);expected=BASE/'state/canonical_memory/snapshots'/('v388_'+plan['generation'][:16])
    if target!=expected or target.exists():raise ValueError('Snapshot target exists or differs; inspect identity first')
    old={};new={}
    for item in plan['files']:
        src,dst=Path(item['source']),Path(item['destination'])
        if not src.resolve().is_relative_to(W) or not dst.resolve().is_relative_to(BASE):raise ValueError('Plan path escaped')
        if dst not in (BASE/'iald_orchestrator/canonical_memory.py',BASE/'state/canonical_memory/manifest.json') and dst.parent!=target:raise ValueError('Destination not allowed')
        raw=src.read_bytes();prior=dst.read_bytes() if dst.exists() else None
        if sha(raw)!=item['sha256'] or (sha(prior) if prior is not None else None)!=item['baseline_sha256']:raise ValueError('CAS mismatch before install')
        old[dst]=prior;new[dst]=raw
    save_json(W/'INSTALL_STARTED.json',{'status':'STARTED_NO_AUTOMATIC_RETRY','review_manifest_sha256':sha(manifest_raw),'files':len(new)})
    written=[]
    try:
        for item in plan['files']:
            dst=Path(item['destination'])
            if (dst.read_bytes() if dst.exists() else None)!=old[dst]:raise ValueError('Concurrent edit')
            written.append(dst);replace_bytes(dst,new[dst])
            if item['mtime_ns'] is not None:
                os.utime(dst,ns=(item['mtime_ns'],item['mtime_ns']))
                if dst.stat().st_mtime_ns!=item['mtime_ns']:raise ValueError('Snapshot mtime preservation failed')
            if dst.read_bytes()!=new[dst]:raise ValueError('Installed bytes differ')
        if sha(index.read_bytes())!=plan['index_sha256'] or sha(catalog.read_bytes())!=prep['historical_catalog_sha256']:raise ValueError('Untouched index/catalog drift')
    except BaseException:
        for dst in reversed(written):
            if old[dst] is not None and dst.exists() and dst.read_bytes()==new[dst]:replace_bytes(dst,old[dst])
        raise
    report={'status':'INSTALLED_NEW_PROCESS_VERIFICATION_REQUIRED','generation':plan['generation'],'index_sha256':sha(index.read_bytes()),'files':{str(p):sha(b) for p,b in new.items()},'mtimes_preserved':True,'index_written':False,'catalog_written':False,'clients_restarted':0,'providers_called':0,'hot_reload_claimed':False}
    save_json(W/'INSTALL_RECEIPT.json',report);print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--review',required=True);a=p.parse_args();main(a.review)
