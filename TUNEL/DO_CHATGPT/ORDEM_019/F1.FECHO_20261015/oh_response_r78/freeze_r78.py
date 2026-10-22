"""Freeze pinned prepared code only after independent review; never run science."""
from pathlib import Path
import datetime as dt,hashlib,json
ROOT=Path(__file__).resolve().parent

def pin(p):
    p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def main():
    manifest=json.loads((ROOT/'PREEXEC_MANIFEST_R78.json').read_text(encoding='utf-8'))
    for row in manifest['files']:assert pin(row['path'])==row
    rp=ROOT/'PREEXEC_REVIEW_R78.json';review=json.loads(rp.read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!='codex-gerente-tgl'
    for name in ['consumer_r78.py','run_oh_response_r78.py','PLAN_R78.json','freeze_r78.py','PREEXEC_MANIFEST_R78.json']:
        assert pin(ROOT/name) in review['evidence']
    out={'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'files':manifest['files']+[pin(ROOT/'PREEXEC_MANIFEST_R78.json')],'review':pin(rp),'scientific_execution':False,'originals_unchanged':True}
    with (ROOT/'FREEZE_R78.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2,ensure_ascii=False)
    print(pin(ROOT/'FREEZE_R78.json'))
if __name__=='__main__':main()



