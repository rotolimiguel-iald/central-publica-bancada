"""Finalize an already counted package into a reviewable plan; never install it."""
from pathlib import Path
import json,sys
W=Path(__file__).resolve().parents[1];A=Path('C:/IALD/projetos_pyhton/IALD');S=W/'memory_stage'
sys.dont_write_bytecode=True;sys.path[:0]=[str(W/'app_patch'),str(A),str(W/'memory_build'),str(W)]
from transaction import digest,write_evidence
from package_native import finalize
from claude_memory_package import load_package
from iald_release_binding import load_release

def main():
    candidate=json.loads((W/'delta_app01/install_plan_candidate.json').read_bytes())
    if candidate['status']!='STATIC_CANDIDATE_NOT_ACTIVATABLE':raise ValueError('Unexpected candidate')
    expected=json.loads((W/'COUNT_PLAN.json').read_bytes())['prefix_sha256']
    finalize(W/'COUNT_RESULT.json',expected)
    release=load_release(S/'manifest_staged.json')
    package=load_package(S/'haiku_runtime',canonical_manifest=S/'manifest_staged.json',source_sha=release.identity['source_sha256'])
    if package.prefix.encode()!=(S/'haiku_prefix.md').read_bytes():raise ValueError('Changed native prefix')
    for item in candidate['files']:
        src,dst=Path(item['source']),Path(item['destination'])
        if digest(src.read_bytes())!=item['sha256']:raise ValueError('Changed reviewed stage')
        prior=digest(dst.read_bytes()) if dst.exists() else None
        if prior!=item['baseline']:raise ValueError('Changed production baseline')
    final=candidate['files'].pop()
    if Path(final['destination'])!=A/'iald_nucleo_fixo.json':raise ValueError('Manifest must switch last')
    prep=json.loads((S/'prepared.json').read_bytes())
    for name in ('prefix.md','manifest.json'):
        src,dst=S/'haiku_runtime'/name,A/'.iald_runtime/haiku'/name
        prior=digest(dst.read_bytes())
        if prior!=prep['protected_production_sha256'][str(dst)]:raise ValueError('Changed native baseline')
        candidate['files'].append({'source':str(src),'destination':str(dst),'sha256':digest(src.read_bytes()),'baseline':prior,'bytes':src.stat().st_size})
    candidate['files'].append(final);candidate['native_files_pending']=[]
    candidate['native_count']=json.loads((W/'COUNT_RESULT.json').read_bytes())
    candidate['status']='COMPLETE_PLAN_REQUIRES_INDEPENDENT_ROOT_REVIEW_AND_RELEASE'
    write_evidence(W/'install_plan.json',candidate)
    write_evidence(W/'validation/final_checks.json',{'passed':True,'scope':'LOCAL_PACKAGE_IDENTITY_AND_MEASURED_BUDGET','plan_sha256':digest((W/'install_plan.json').read_bytes()),'native_receipt_sha256':digest((W/'COUNT_RESULT.json').read_bytes()),'independent_review':'PENDING_ROOT_REVIEW_FINAL_JSON'})
    print(json.dumps({'status':candidate['status'],'files':len(candidate['files']),'plan_sha256':digest((W/'install_plan.json').read_bytes())}))
if __name__=='__main__':main()
