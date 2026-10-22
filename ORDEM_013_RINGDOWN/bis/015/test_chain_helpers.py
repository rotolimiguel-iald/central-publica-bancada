"""Actual V1 schema and synthetic parent/witness tests, no scientific activation."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,copy,hashlib,importlib.util,os,tempfile
B=Path(__file__).resolve().parents[2];D=B/'bis/015/t03/chain_tests_001';P=B/'bis/e2_code_v1_1/registration_guard.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    D.mkdir(exist_ok=False)
    raw=P.read_bytes();s=raw.decode();old="    old_ids=[c['id'] for c in original['nulls']['cells']]\n    new_ids=[c['id'] for c in candidate['nulls_v1_1']['cells']]"
    assert s.count(old)==1
    s=s.replace(old,"    old_cells=original['nulls']['cells'];new_cells=candidate['nulls_v1_1']['cells']\n    if not isinstance(old_cells,dict) or not isinstance(new_cells,dict):raise ValueError('Null cells require id-keyed mapping')\n    old_ids=list(old_cells);new_ids=list(new_cells)\n    if not all(isinstance(k,str) and k for k in new_ids):raise ValueError('Invalid null cell id')")
    with (D/'guard_before_schema_fix.py').open('xb') as f:f.write(raw)
    tmp=P.with_suffix('.pending')
    with tmp.open('xb') as f:f.write(s.encode())
    tmp.replace(P)
    spec=importlib.util.spec_from_file_location('candidate_guard',P);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    original=json.loads((B/'RINGDOWN_5SIGMA_V1.json').read_bytes());candidate=copy.deepcopy(original)
    candidate['statistical_subobject_sha256']=g.statistical_digest(original);candidate['nulls_v1_1']={'cells':{'R5_NEW_TEST':{}}}
    passed=[]
    def good(name,fn):fn();passed.append(name)
    def bad(name,fn):
        try:fn()
        except (ValueError,KeyError,FileNotFoundError):passed.append(name);return
        raise AssertionError('Expected refusal: '+name)
    good('real_V1_mapping_schema',lambda:g.verify_statistical_identity(original,candidate))
    c=copy.deepcopy(candidate);c['statistics']['T13_MUTATION']=True;bad('statistic_one_field_changed',lambda:g.verify_statistical_identity(original,c))
    c=copy.deepcopy(candidate);c['nulls']['cells']['ILLEGAL_NEW']={};bad('new_cell_inserted_in_frozen_V1_nulls',lambda:g.verify_statistical_identity(original,c))
    c=copy.deepcopy(candidate);c['nulls_v1_1']['cells']={next(iter(original['nulls']['cells'])):{}};bad('reused_V1_cell_id',lambda:g.verify_statistical_identity(original,c))
    c=copy.deepcopy(candidate);c['blinding']['offset_half_range']+=.0001;bad('offset_commitment_changed',lambda:g.verify_statistical_identity(original,c))
    c=copy.deepcopy(candidate);c['nulls_v1_1']['cells']=[{'id':'NEW'}];bad('wrong_nulls_container',lambda:g.verify_statistical_identity(original,c))
    bad('duplicate_json_key',lambda:g.strict_json('{"a":1,"a":2}'))
    bad('nonfinite_json',lambda:g.strict_json('{"a":NaN}'))
    root=D/'fixture';base=root/'ORDEM_013_RINGDOWN';notes=root/'TUNEL/DO_CHATGPT';base.mkdir(parents=True);notes.mkdir(parents=True)
    g.BASE=base;g.ROOT=root
    # contained's default was bound at import; explicitly rebind fixture-only resolution.
    def contained(name,root=None):
        rt=g.ROOT if root is None else root;p=(rt/name).resolve()
        if not p.is_relative_to(rt.resolve()):raise ValueError('outside fixture')
        return p
    g.contained=contained
    now=datetime.now(timezone.utc);t0=(now-timedelta(seconds=20)).isoformat();t1=(now-timedelta(seconds=15)).isoformat();t2=(now-timedelta(seconds=10)).isoformat()
    def put(p,obj):p.write_text(json.dumps(obj,sort_keys=True),'utf-8')
    def witness(p,digest,issued):
        p.write_text('registro_sha256: '+digest+'\nregistered_utc: '+issued+'\n','utf-8')
        stamp=datetime.fromisoformat(issued).timestamp();os.utime(p,(stamp,stamp))
    orig=copy.deepcopy(original);orig['registered_utc']=t0;orig['witness_relative_to_Chatgpt']='TUNEL/DO_CHATGPT/V1_TEST.md'
    op=base/'RINGDOWN_5SIGMA_V1.json';put(op,orig);witness(notes/'V1_TEST.md',sha(op),t0)
    c=copy.deepcopy(orig);c.update(parent_registration_sha256=sha(op),v1_witness_sha256=sha(notes/'V1_TEST.md'),
      statistical_subobject_sha256=g.statistical_digest(orig),registered_utc=t1,witness_relative_to_Chatgpt='TUNEL/DO_CHATGPT/ENTREGA_015_E2_REGISTRO_V1_1.md',
      nulls_v1_1={'cells':{'NEW_DIAGNOSTIC':{}}},pe_jobs={'NEW_JOB':{'fixed':1}},test_candidates_amendments=[])
    cp=base/'RINGDOWN_5SIGMA_V1_1.json';np=notes/'ENTREGA_015_E2_REGISTRO_V1_1.md'
    put(cp,c);witness(np,sha(cp),t1);good('valid_first_amendment',lambda:g.load_registration_chain_v1_1())
    second=copy.deepcopy(c);second.update(parent_registration_sha256=sha(cp),registered_utc=t2,witness_relative_to_Chatgpt='TUNEL/DO_CHATGPT/ENTREGA_015_E2_REGISTRO_V1_1_1.md')
    sp=base/'RINGDOWN_5SIGMA_V1_1_1.json';sn=notes/'ENTREGA_015_E2_REGISTRO_V1_1_1.md';put(sp,second);witness(sn,sha(sp),t2)
    good('valid_two_link_chain',lambda:g.load_registration_chain_v1_1())
    modified=copy.deepcopy(second);modified['parent_registration_sha256']='0'*64;put(sp,modified);witness(sn,sha(sp),t2);bad('wrong_parent',lambda:g.load_registration_chain_v1_1())
    modified=copy.deepcopy(second);modified['pe_jobs']['NEW_JOB']['fixed']=2;put(sp,modified);witness(sn,sha(sp),t2);bad('old_job_replacement',lambda:g.load_registration_chain_v1_1())
    modified=copy.deepcopy(second);modified['test_candidates_amendments']=[dict(promotion=True,event='TEST',census_reviewed_utc=t0)]
    put(sp,modified);witness(sn,sha(sp),t2);bad('promotion_review_before_V1_1',lambda:g.load_registration_chain_v1_1())
    put(sp,second);witness(sn,'f'*64,t2);bad('wrong_witness_hash',lambda:g.load_registration_chain_v1_1())
    # Rename within this isolated fixture only; no canonical files are involved.
    gap=base/'RINGDOWN_5SIGMA_V1_1_2.json';sp.rename(gap);bad('missing_chain_ordinal',lambda:g.load_registration_chain_v1_1())
    r=dict(status='CHAIN_HELPERS_CONTROLS_PASSED_NOT_WIRED',tests=passed,guard_sha256=sha(P),original_guard_sha256=sha(B/'bis/e2_code/registration_guard.py'),
      statistical_subobject_sha256=g.statistical_digest(original),fixture_only=True,activation_performed=False,seed_read=False,
      initial_schema_correction='V1 nulls.cells is an id-keyed dictionary, not a list; corrected before tests; pre-correction source preserved')
    with (D/'RESULT.json').open('xb') as f:f.write((json.dumps(r,indent=2)+'\n').encode())
    print(json.dumps(dict(status=r['status'],tests=len(passed),statistical_subobject_sha256=r['statistical_subobject_sha256'])))
if __name__=='__main__':main()
