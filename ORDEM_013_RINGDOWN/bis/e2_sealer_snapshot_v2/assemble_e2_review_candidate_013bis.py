"""Merge reviewed packages into a candidate; no seed or registration created."""
from pathlib import Path
import argparse,json,hashlib,ast
from datetime import datetime,timezone
B=Path(__file__).resolve().parents[1];R=B.parent
SNAPSHOTS={}

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
    return h.hexdigest()
def captured(p):
    raw=p.read_bytes();pin=hashlib.sha256(raw).hexdigest()
    if p in SNAPSHOTS and SNAPSHOTS[p]!=pin:raise ValueError('Input changed during capture')
    SNAPSHOTS[p]=pin
    return raw,pin
def read(p):return json.loads(captured(p)[0])
def tree(root):
    result={}
    for p in sorted(root.rglob('*.py')):
        raw,pin=captured(p);ast.parse(raw.decode('utf-8-sig'));result[p.relative_to(root).as_posix()]=pin
    if not result:raise ValueError('Empty code tree')
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--draft',required=True);parser.add_argument('--tag',required=True);args=parser.parse_args()
    if not args.tag.isalnum():raise ValueError('Alphanumeric tag')
    draft=(B/'bis'/args.draft).resolve()
    if not draft.is_relative_to(B/'bis'):raise ValueError('Invalid draft path')
    reg=read(draft)
    if reg['status']!='DRAFT_NOT_REGISTERED__NO_EXECUTION_AUTHORIZATION':raise ValueError('Not a draft')
    fragment=read(B/'bis/e7_prepare/E2_INCLUDE_FINAL_v4.json')
    reg['e7']=fragment['e7'];reg['e7']['guard_sha256']=captured(B/'bis/e2_code/registration_guard.py')[1]
    reg['e7']['guard_pin_status']='READ_FROM_CURRENT_REVIEW_CANDIDATE__NOT_YET_REGISTERED'
    for n,pin in fragment['input_pins_relative_to_Chatgpt'].items():
        if sha(R/n)!=pin:raise ValueError('E7 input changed '+n)
        SNAPSHOTS[R/n]=pin
        if n in reg['input_pins_relative_to_Chatgpt'] and reg['input_pins_relative_to_Chatgpt'][n]!=pin:raise ValueError('Conflicting input pin')
        reg['input_pins_relative_to_Chatgpt'][n]=pin
    reg.pop('extra_code_trees',None)
    reg['own_code_tree_sha256']=tree(B/'bis/e2_code')
    roots=['ORDEM_013_RINGDOWN/bis/e7_prepare/producer','ORDEM_013_RINGDOWN/bis/e4_e5_prepare']
    reg['extra_code_roots']=[{'relative_to_Chatgpt':root,'files_sha256':tree(R/root)} for root in roots]
    if tree(R/reg['e7']['producer_directory'])!=reg['e7']['producer_tree_sha256']:raise ValueError('E7 fragment producer pins differ')
    e4=B/'bis/e4_e5_prepare'
    package={n:captured(e4/n)[1] for n in ['PLAN.json','INPUT_MANIFEST.json','SCHEMA.json','deterministic_e4_e5.py']}
    reg['e4_e5_preparation_pins']=package
    for n in package:reg['input_pins_relative_to_Chatgpt']['ORDEM_013_RINGDOWN/bis/e4_e5_prepare/'+n]=package[n]
    for item in read(e4/'INPUT_MANIFEST.json')['files']:
        p=(B/item['path']).resolve()
        if not p.is_relative_to(R) or sha(p)!=item['sha256']:raise ValueError('E4 input changed')
        SNAPSHOTS[p]=item['sha256']
        n=p.relative_to(R).as_posix();reg['input_pins_relative_to_Chatgpt'][n]=item['sha256']
    reg['registration_id']='RINGDOWN_5SIGMA_V1_013BIS'
    reg['review_candidate_provenance']={'draft':draft.relative_to(B).as_posix(),'draft_sha256':SNAPSHOTS[draft],
      'assembled_utc':datetime.now(timezone.utc).isoformat(),'assembler_sha256':captured(Path(__file__))[1],
      'E7_fragment_sha256':SNAPSHOTS[B/'bis/e7_prepare/E2_INCLUDE_FINAL_v4.json'],
      'scope':'Code/input snapshot only; no E2 witness, no seed, no execution yet'}
    out=B/'bis'/('E2_REVIEW_CANDIDATE_'+args.tag+'.json')
    for p,pin in SNAPSHOTS.items():
        if sha(p)!=pin:raise ValueError('Captured input changed before candidate publication')
    with out.open('x',encoding='utf-8') as f:json.dump(reg,f,indent=2,ensure_ascii=False,allow_nan=False)
    print(json.dumps({'candidate':out.name,'sha256':sha(out),'own_code_files':len(reg['own_code_tree_sha256']),
      'extra_code_files':sum(len(r['files_sha256']) for r in reg['extra_code_roots']),
      'calibration_identities':len(reg['calibration_event_ids']),
      'eligible_absent_in_scoped_census':sum(x['eligible'] is True and x['published_deformation_at_registration'] is False for x in reg['test_candidates'].values())}))

if __name__=='__main__':main()
