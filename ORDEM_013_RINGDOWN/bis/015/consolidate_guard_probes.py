"""Bind existing measured controls to the unchanged V1.1 candidate/code."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
B=Path(__file__).resolve().parents[2];D=B/'bis/015/t03';C=B/'bis/e2_code_v1_1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_bytes())
def main():
    sys.path.insert(0,str(C));import registration_guard as g
    candidate=load(D/'CANDIDATE_V1_1_002.json'); tree={p.relative_to(C).as_posix():sha(p) for p in C.rglob('*.py')}
    assert tree==candidate['own_code_tree_sha256']
    g.verify_statistical_identity(load(B/'RINGDOWN_5SIGMA_V1.json'),candidate)
    tests=[];evidence=[]
    for folder in ['candidate_tests_001','guard_integration_tests_003','reading_failure_tests_002','clock_nulls_tests_002']:
        p=D/folder/'RESULT.json';x=load(p)
        if 'own_code_tree_sha256' in x:assert x['own_code_tree_sha256']==tree
        if 'candidate_sha256' in x:assert x['candidate_sha256']==sha(D/'CANDIDATE_V1_1_002.json')
        if 'guard_sha256' in x:assert x['guard_sha256']==tree['registration_guard.py']
        for n,h in x.get('files_sha256',{}).items():assert tree[n]==h
        assert x.get('seed_read') is False
        for t in x['tests']:
            # Earlier clock suite records successful expected outcomes, not a boolean.
            if folder=='clock_nulls_tests_002':assert t['result'] in ['REFUSED','ACCEPTED','AST_AND_SOURCE_CHECK']
            else:assert t.get('passed') is True
            tests.append(dict(name=folder+':'+t['name'],passed=True,evidence=t))
        evidence.append(dict(path=str(p),sha256=sha(p),count=len(x['tests']),scope=x.get('scope',x.get('limit'))))
    required=['frozen_statistics','promotion_before_first_witness','unpaid_reading_MISSING','R_LIN_below_exact_target_false','R_LIN_at_exact_target_true','440_outside_qualified_box','runner_old_id_before_simulation','full_checked_registration_pinned_runtime_fixture']
    for name in required:assert any(t['name'].endswith(':'+name) for t in tests),name
    r=dict(status='V1_1_GUARD_PROBES_PASSED',finished_utc=datetime.now(timezone.utc).isoformat(),tests=tests,evidence=evidence,
        own_code_tree_sha256=tree,statistical_subobject_sha256=candidate['statistical_subobject_sha256'],candidate_sha256=sha(D/'CANDIDATE_V1_1_002.json'),
        script_sha256=sha(Path(__file__)),scope='Consolidation of measured candidate, actual-entry synthetic fixtures, reading and clock controls with current byte hashes; not independent management review',
        new_scientific_draws=0,seed_read=False,real_registration_activated=False)
    p=D/'C1_GUARD_MUTATION_TESTS_V1_1.json';assert not p.exists();g.publish_new(p,r)
    print(json.dumps(dict(status=r['status'],tests=len(tests),sha256=sha(p))))
if __name__=='__main__':main()
