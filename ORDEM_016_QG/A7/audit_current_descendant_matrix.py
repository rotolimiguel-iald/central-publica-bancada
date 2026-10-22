"""Independent first-residue route and omission controls for current descent."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from full_loop_extension_engine import x,z,Q,terms
from logarithmic_contact_engine import residue
from position_metric_bubble_engine import LABELS

H=Path(__file__).resolve().parent;M=H/'current_distributional_descendant_matrix'
D=H/'current_descendant_matrix_independent_audit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):
    assert not p.exists(),p
    b=json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)
def parse(t):return s.sympify(t,locals={str(v):v for v in (*Q,*x,z)})
def matrix(rows):return s.Matrix([[parse(v) for v in row] for row in rows])

def main():
    result=json.loads((M/'results.json').read_bytes())
    D.mkdir(exist_ok=False)
    put(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
        method='Direct derivative of the regulator: C_i(F)=-2Res[x_i F/z], normalized by CE; no call to contact()',
        negative_controls=['Omit outer derivative contact','Reverse its sign'],
        no_loop_reexecution=True,script_sha256=sha(Path(__file__)),
        source_manifest_sha256=sha(M/'manifest.json')))
    start=time.process_time();checks=0;direct=[]
    def eq(a,b):
        nonlocal checks
        assert s.expand(a-b)==0,(a,b);checks+=1
    for order,eta in enumerate([(1,0,0,0),(1,-1,0,0)]):
        C=s.zeros(4)
        for a,(i,j) in enumerate(LABELS):
            for r in range(4):
                row=json.loads((M/f'component_{order}_{a}_{r}.json').read_bytes())
                F=parse(row['unextended_current'])
                for derivative,ghost in [(i,j),(j,i)]:
                    value=0
                    for n,powers,c in terms(F):
                        pp=list(powers);pp[derivative]+=1
                        value-=2*c*residue(n+1,tuple(pp),(1,1,1,1))
                    C[ghost,r]+=value
        direct.append(C.applyfunc(lambda v:s.expand(v.subs(
            dict(zip(Q,[Q[k]+eta[k] for k in range(4)])),simultaneous=True))))
    L=(2,-1,0,0)
    adj=lambda a:a.T.applyfunc(lambda v:s.expand(v.subs(dict(zip(Q,[-Q[k]-L[k] for k in range(4)])),simultaneous=True)))
    mean=(direct[0]+direct[1])/2
    independent=(mean-adj(mean)).applyfunc(s.expand)
    original=matrix(result['extra_derivative_extension_contact'])
    for a,b in zip(independent,original):eq(a,b)
    desc=matrix(result['distributional_current_descendant'])
    local=matrix(result['current_contact_variation'])
    difference=matrix(result['difference_full_minus_current'])
    for a,b in zip(desc,local+independent):eq(a,b)
    full=desc+difference
    omitted=(full-local).applyfunc(s.expand)
    reversed_sign=(full-local+independent).applyfunc(s.expand)
    assert omitted[0,0]!=0;checks+=1
    assert reversed_sign[0,0]!=0;checks+=1
    audit=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,
        cpu_seconds=time.process_time()-start,
        independent_residue_route_matches_all16=True,
        omitted_contact_nonzero_components=sum(v!=0 for v in omitted),
        reversed_sign_nonzero_components=sum(v!=0 for v in reversed_sign),
        zero_momentum_controls=dict(omitted00=str(omitted[0,0].subs(dict.fromkeys(Q,0))),
                                    reversed00=str(reversed_sign[0,0].subs(dict.fromkeys(Q,0)))),
        main_matrix_difference_nonzero_components=result['nonzero_difference_components'],
        main_bilocal_nonzero_components=result['bilocal_nonzero_components'],
        interpretation='Independent regulator derivative validates the added contact; mutation controls reject omission/sign reversal. No change of renormalization, full Q2 remains unestablished.',
        full_Q2=False,gate_changed=False)
    put(D/'results.json',audit)
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
        [Path(__file__),D/'PRE_REGISTER.json',D/'results.json',M/'manifest.json']],gate_changed=False))
    print(json.dumps(audit,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
