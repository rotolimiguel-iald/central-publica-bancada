"""Final candidate controls, no scientific draws, PE, seed read or real activation."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import copy, hashlib, json, os, sys, time
B = Path(__file__).resolve().parents[2]
ROOT = B.parent
C = B/'bis/e2_code_v1_1'
D = B/'bis/015/t03'
OUT = D/'candidate_tests_001'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_bytes())
def put(p, value):
    raw = value if isinstance(value, bytes) else (json.dumps(value, indent=2, allow_nan=False)+'\n').encode()
    p.parent.mkdir(parents=True, exist_ok=True)
    temp = p.with_name(p.name+'.tmp')
    with temp.open('xb') as f: f.write(raw)
    assert temp.stat().st_size == len(raw)
    os.replace(temp,p)
def main():
    wall=time.perf_counter();cpu=time.process_time();OUT.mkdir(exist_ok=False)
    sys.path.insert(0,str(C))
    import registration_guard as g, blinding as blind, pe_runner
    original=load(B/'RINGDOWN_5SIGMA_V1.json'); candidate=load(D/'CANDIDATE_V1_1_002.json')
    tree={p.relative_to(C).as_posix():sha(p) for p in C.rglob('*.py')}
    assert candidate['own_code_tree_sha256']==tree
    tests=[]
    def check(name, fn, refused=False):
        try: fn()
        except (ValueError,KeyError,FileNotFoundError) as e:
            if not refused: raise
            tests.append(dict(name=name,passed=True,observed='REFUSED',exception=type(e).__name__,message=str(e)));return
        if refused: raise AssertionError('Unexpected acceptance: '+name)
        tests.append(dict(name=name,passed=True,observed='ACCEPTED'))
    check('actual_candidate_statistics',lambda:g.verify_statistical_identity(original,candidate))
    for key in g.STATISTICAL_FIELDS:
        m=copy.deepcopy(candidate);m[key]={'single_byte_change':'x'}
        check('frozen_'+key,lambda:g.verify_statistical_identity(original,m),True)
    for key in ('seed_commitment_sha256','offset_half_range'):
        m=copy.deepcopy(candidate);m['blinding'][key]='x'
        check('frozen_blinding_'+key,lambda:g.verify_statistical_identity(original,m),True)
    m=copy.deepcopy(candidate);m['nulls']['cells']['NEW_CELL_IN_OLD_OBJECT']={}
    check('new_cell_in_frozen_nulls',lambda:g.verify_statistical_identity(original,m),True)
    m=copy.deepcopy(candidate);m['nulls_v1_1']['cells'][next(iter(original['nulls']['cells']))]={}
    check('old_id_in_new_nulls',lambda:g.new_null_cells(m),True)
    job=next(iter(candidate['pe_jobs'].values()))
    check('actual_job_R5_qualified',lambda:g.validate_job_qualification(candidate,job))
    check('actual_job_runner_validation',lambda:pe_runner.validate_config(job))
    m=copy.deepcopy(job);m['fixed_deformation_parameters']['dtau440']=1.1
    check('440_outside_qualified_box',lambda:g.validate_job_qualification(candidate,m),True)
    target=candidate['blinding']['minimum_information_to_unblind_by_reading']['R-LIN']
    def permission(reading,information,green=True):
        r=copy.deepcopy(candidate);r['blinding']['unblinding_dataset_sha256']=sha(D/'CANDIDATE_V1_1_002.json')
        receipt=dict(status='REGISTERED_UNBLINDING_GATE_MET',reading=reading,scope='per-reading',information=information,
            systematic_gate=green,independent_review_passed=True,dataset_sha256=r['blinding']['unblinding_dataset_sha256'],
            seed_commitment_sha256=r['blinding']['seed_commitment_sha256'],registration_id=r['registration_id'])
        return blind.unblinding_allowed(r,reading,information,green,receipt)
    def require(value):
        if value is not True: raise AssertionError(value)
    check('R_LIN_below_exact_target_false',lambda:require(permission('R-LIN',target-1e-6) is False))
    check('R_LIN_at_exact_target_true',lambda:require(permission('R-LIN',target) is True))
    check('R_LIN_7513_27_true',lambda:require(permission('R-LIN',7513.27) is True))
    check('red_systematics_false',lambda:require(permission('R-LIN',target,False) is False))
    for reading in ['MISSING']+[k for k,v in candidate['blinding']['minimum_information_to_unblind_by_reading'].items() if v is None]:
        check('unpaid_reading_'+reading,lambda:require(permission(reading,target) is False))
    # Actual candidate, isolated chain and witnesses. The source/statistics stay real.
    root=OUT/'fixture';base=root/'ORDEM_013_RINGDOWN';notes=root/'TUNEL/DO_CHATGPT'
    g.BASE=base;g.ROOT=root
    def contained(name,root=None):
        rt=g.ROOT if root is None else root;p=(rt/name).resolve()
        if not p.is_relative_to(rt.resolve()):raise ValueError('Outside fixture')
        return p
    g.contained=contained
    now=datetime.now(timezone.utc);issued=(now-timedelta(seconds=10)).isoformat()
    def witness(p,digest,when):
        put(p,('registro_sha256: '+digest+'\nregistered_utc: '+when+'\n').encode())
    op=base/'RINGDOWN_5SIGMA_V1.json';put(op,(B/'RINGDOWN_5SIGMA_V1.json').read_bytes())
    on=contained(original['witness_relative_to_Chatgpt']);put(on,(ROOT/original['witness_relative_to_Chatgpt']).read_bytes())
    reg=copy.deepcopy(candidate);reg.update(status='REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST',registered_utc=issued)
    cp=base/'RINGDOWN_5SIGMA_V1_1.json';cn=contained(reg['witness_relative_to_Chatgpt'])
    def publish(m):put(cp,m);witness(cn,sha(cp),issued)
    publish(reg);check('candidate_chain_valid',g.load_registration_chain_v1_1)
    m=copy.deepcopy(reg);m['conventions']['_tampered']='x';publish(m)
    check('candidate_chain_changed_statistics',g.load_registration_chain_v1_1,True)
    m=copy.deepcopy(reg);event=next(k for k,v in m['test_candidates'].items() if v.get('eligible') is not True)
    m['test_candidates'][event]['eligible']=True
    m['test_candidates_amendments'].append(dict(event=event,promotion=True,census_reviewed_utc=(now-timedelta(days=1)).isoformat()))
    publish(m);check('promotion_before_first_witness',g.load_registration_chain_v1_1,True)
    m=copy.deepcopy(reg);m['test_candidates'][event]['eligible']=True;publish(m)
    check('promotion_without_evidence',g.load_registration_chain_v1_1,True)
    publish(reg)
    assert not (B/'RINGDOWN_5SIGMA_V1_1.json').exists()
    assert not (B/'bis/PART_015_BUDGET_START.json').exists()
    for rt,pins in [(B/'bis/e2_code',original['own_code_tree_sha256'])]+[(ROOT/x['relative_to_Chatgpt'],x['files_sha256']) for x in original['extra_code_roots']]:
        assert {p.relative_to(rt).as_posix():sha(p) for p in rt.rglob('*.py')}==pins
    result=dict(status='CANDIDATE_CONTROLS_PASSED',finished_utc=datetime.now(timezone.utc).isoformat(),
        candidate_sha256=sha(D/'CANDIDATE_V1_1_002.json'),own_code_tree_sha256=tree,tests=tests,
        statistical_subobject_sha256=g.statistical_digest(original),cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall,
        seed_read=False,heavy_jobs=0,scope='Candidate and isolated synthetic chronology; no real publication')
    put(OUT/'RESULT.json',result)
    print(json.dumps(dict(status=result['status'],tests=len(tests),cpu_seconds=result['cpu_seconds'],wall_seconds=result['wall_seconds'])))
if __name__=='__main__':main()
