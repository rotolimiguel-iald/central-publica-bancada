"""Bind the historical V1/witness and use the actual first witness time for promotions."""
from pathlib import Path
import json,hashlib,ast
B=Path(__file__).resolve().parents[2];D=B/'bis/015/t03';P=B/'bis/e2_code_v1_1/registration_guard.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    v1=B/'RINGDOWN_5SIGMA_V1.json';r=json.loads(v1.read_bytes());w=B.parent/r['witness_relative_to_Chatgpt']
    raw=P.read_bytes();s=raw.decode('utf-8');snap=D/'guard_before_anchor_fix.py'
    with snap.open('xb') as f:f.write(raw)
    anchor='# V1.1 statistical and chronology contract.'
    assert s.count(anchor)==1
    s=s.replace(anchor,'V1_PIN = '+repr(sha(v1))+'\nV1_WITNESS_PIN = '+repr(sha(w))+'\n\n'+anchor)
    anchor="    original=strict_json(original_path.read_bytes());parent=sha(original_path)"
    assert s.count(anchor)==1
    s=s.replace(anchor,anchor+"\n    if parent!=V1_PIN:raise ValueError('Historical V1 pin changed')")
    anchor="    v1_witness=check_witness(v1_note,parent,original['registered_utc'])"
    s=s.replace(anchor,anchor+"\n    if v1_witness!=V1_WITNESS_PIN:raise ValueError('Historical V1 witness pin changed')")
    assert s.count('if root_time is None:root_time=issued')==1
    s=s.replace('if root_time is None:root_time=issued','if root_time is None:root_time=witnessed')
    ast.parse(s);tmp=P.with_suffix('.pending')
    with tmp.open('xb') as f:f.write(s.encode())
    tmp.replace(P)
    result=dict(status='ANCHORS_TIGHTENED_PENDING_V2_TESTS',old=hashlib.sha256(raw).hexdigest(),new=sha(P),historical_registration=sha(v1),historical_witness=sha(w))
    with (D/'CHAIN_ANCHORS_PATCH_002.json').open('xb') as f:f.write((json.dumps(result,indent=2)+'\n').encode())
    # Reuse the existing focused test suite without repeating or overwriting its first fixtures/results.
    test=B/'bis/015/test_chain_helpers.py';text=test.read_text('utf-8')
    a=text.index('    raw=P.read_bytes();s=raw.decode();old=');z=text.index("    spec=importlib.util.spec_from_file_location",a)
    text=text[:a]+text[z:]
    text=text.replace("D=B/'bis/015/t03/chain_tests_001'","D=B/'bis/015/t03/chain_tests_002'")
    anchor="    op=base/'RINGDOWN_5SIGMA_V1.json';put(op,orig);witness(notes/'V1_TEST.md',sha(op),t0)"
    assert text.count(anchor)==1
    text=text.replace(anchor,anchor+"\n    g.V1_PIN=sha(op);g.V1_WITNESS_PIN=sha(notes/'V1_TEST.md')")
    anchor="    put(sp,second);witness(sn,'f'*64,t2);bad('wrong_witness_hash',lambda:g.load_registration_chain_v1_1())"
    replacement='''    put(sp,second);witness(sn,'f'*64,t2);bad('wrong_witness_hash',lambda:g.load_registration_chain_v1_1())
    put(sp,second);witness(sn,sha(sp),t2)
    first_late=(now-timedelta(seconds=12)).isoformat()
    witness(np,sha(cp),first_late)
    modified=copy.deepcopy(second);modified['test_candidates_amendments']=[dict(promotion=True,event='TEST',census_reviewed_utc=(now-timedelta(seconds=14)).isoformat())]
    put(sp,modified);witness(sn,sha(sp),t2)
    bad('promotion_between_issue_and_first_witness',lambda:g.load_registration_chain_v1_1())
    put(sp,second);witness(sn,sha(sp),t2);witness(np,sha(cp),t1)
    old_pin=g.V1_PIN;g.V1_PIN='0'*64;bad('historical_V1_pin',lambda:g.load_registration_chain_v1_1());g.V1_PIN=old_pin
    old_pin=g.V1_WITNESS_PIN;g.V1_WITNESS_PIN='0'*64;bad('historical_witness_pin',lambda:g.load_registration_chain_v1_1());g.V1_WITNESS_PIN=old_pin'''
    assert text.count(anchor)==1;text=text.replace(anchor,replacement);ast.parse(text)
    out=B/'bis/015/test_chain_helpers_v2.py'
    with out.open('xb') as f:f.write(text.encode())
    print(json.dumps(result))
if __name__=='__main__':main()
