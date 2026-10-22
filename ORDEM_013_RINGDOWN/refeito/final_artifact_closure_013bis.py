"""Recheck hashes already declared by the delivered B3-B5 manifests."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, os
B=Path(__file__).resolve().parents[1];R=B.parent
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for x in iter(lambda:f.read(1048576),b''):h.update(x)
    return h.hexdigest()
def main():
    manifests=[B/'bis/B3_DELIVERY_MANIFEST.json',B/'bis/B4_TEST_DELIVERY_MANIFEST.json',B/'bis/B5_DELIVERY_MANIFEST.json']
    files={};checks=[]
    for p in manifests:
        d=json.loads(p.read_bytes())
        for name,entry in d['files'].items():
            path=(R/name).resolve()
            if not path.is_relative_to(R):raise ValueError('Unexpected artifact outside work root')
            actual=sha(path)
            if actual!=entry['sha256']:raise ValueError('Delivered artifact changed: '+name)
            if name in files and files[name]['sha256']!=actual:raise ValueError('Conflicting manifests')
            files[name]={'sha256':actual,'bytes':path.stat().st_size}
            checks.append({'manifest':p.relative_to(R).as_posix(),'artifact':name,'matches':True})
        files[p.relative_to(R).as_posix()]={'sha256':sha(p),'bytes':p.stat().st_size}
    extras=['bis/E6_ACTUAL_AUTHORIZATION_V1.json','bis/E6_ACTUAL_EXECUTION_V1.json',
        'bis/e6_actual_review/E6_EXECUTION_AND_MARKDOWN_REVIEW_001.json',
        'bis/e3_wall_stages/STAGE_CHAIN_FINAL_MANIFEST_V1.json',
        'bis/e3_wall_stages/STAGE_CHAIN_HANDOFF_V1.json',
        'bis/e6_review/FINAL_PUBLISHER_STATIC_CLOSING_V2.md',
        'refeito/publish_final_report_v2_013bis.py',
        'bis/e3_pilot_review/E3_WALL_BUDGET_ACTIVATION_V2_CLOSING_REVIEW.json',
        'bis/e3_pilot_review/DELIVERY_NOTES_V2_STATIC_CLOSING.json',
        'bis/e3_budget_wall_review/B3_V2_CLOSING_REVIEW.json',
        'bis/e3_budget_wall_review/SYMLINK_CLASSIFICATION.json']
    for name in extras:
        p=B/name;files[p.relative_to(R).as_posix()]={'sha256':sha(p),'bytes':p.stat().st_size}
    out=B/'bis/FINAL_ARTIFACT_CLOSURE.json'
    result={'status':'DELIVERED_B3_B4_TEST_B5_HASHES_RECHECKED','created_utc':datetime.now(timezone.utc).isoformat(),
        'files':files,'checks':checks,'scope':'Referenced delivered artifacts; transitive per-file custody remains in linked manifests',
        'script_sha256':sha(Path(__file__))}
    raw=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode();tmp=out.with_name(out.name+'.pending')
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.stat().st_size!=len(raw):raise OSError('Short closure write')
    os.link(tmp,out);tmp.unlink()
    print(json.dumps({'path':str(out),'sha256':sha(out),'checks':len(checks),'unique_files':len(files)}))
if __name__=='__main__':main()
