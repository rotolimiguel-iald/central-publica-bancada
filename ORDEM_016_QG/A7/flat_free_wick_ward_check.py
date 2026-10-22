"""Exact free covariance and Euler conditions for a BRST-compatible Wick map.

This constructs a flat candidate, not a curved state or a new normalization
of the already measured composite time-ordered insertions.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, time, uuid
import sympy as s
from position_metric_bubble_engine import BASIS, LABELS

H=Path(__file__).resolve().parent
D=H/'flat_free_wick_ward'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):
    assert not p.exists(),p
    b=json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b); assert t.read_bytes()==b; t.replace(p)
def main():
    D.mkdir(exist_ok=False)
    put(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
        target='Free matrix identities sufficient for equivariant flat Wick ordering',
        signatures=[[1,1,1,1],[-1,1,1,1]],
        field_order='h_lower symmetric10,b_lower4,c_lower4,barc_lower4',
        variables='p is a formal derivative symbol; physical Fourier derivatives require p=i*k consistently',
        candidate='Hplus=N(partial)*fplus, where fplus is a scalar massless bisolution',
        exclusions=['No curved bisolution/state construction','No positivity on gauge field space',
            'No composite Euler normalization','No Q2 or gate conclusion'],
        script_sha256=sha(Path(__file__)),
        sources=[dict(path=str(p),sha256=sha(p)) for p in
            [H/'free_euler_insertion_contact_check.py',H/'position_metric_bubble_engine.py']]))
    start=time.process_time();p=s.symbols('p0:4');kap=s.symbols('kappa',nonzero=True)
    checks=[];outputs=[]
    def matrix_eq(label,A,B):
        diff=(A-B).applyfunc(s.expand)
        assert diff==s.zeros(*diff.shape),(label,diff)
        checks.append(dict(label=label,shape=list(diff.shape),zero=True))
    for sig in [(1,1,1,1),(-1,1,1,1)]:
        eta=s.diag(*sig);p2=sum(sig[i]*p[i]**2 for i in range(4))
        gram=s.diag(*[(1 if i==j else 2)*sig[i]*sig[j] for i,j in LABELS])
        tr=s.Matrix([sig[i]*int(i==j) for i,j in LABELS])
        g=s.Matrix([sig[i]*int(i==j) for i,j in LABELS])
        reverse=s.eye(10)-g*tr.T/2
        S=reverse*gram.inv()
        G=s.Matrix(10,4,lambda A,r:p[LABELS[A][0]]*int(LABELS[A][1]==r)
            +p[LABELS[A][1]]*int(LABELS[A][0]==r))
        C=s.Matrix(4,10,lambda r,A:sum(sig[m]*p[m]*BASIS[A][4*m+r] for m in range(4))
            -p[r]*sum(sig[i]*BASIS[A][4*i+i] for i in range(4))/2)
        E=-p2*reverse+reverse*G*C
        P=s.zeros(22);N=s.zeros(22);Q=s.zeros(22)
        P[:10,:10]=gram*E/(4*kap)
        P[:10,10:14]=-C.T*eta
        P[10:14,:10]=eta*C
        P[10:14,10:14]=-2*kap*eta
        P[14:18,18:22]=-p2*eta
        P[18:22,14:18]=p2*eta
        N[:10,:10]=-4*kap*S
        N[:10,10:14]=G*eta
        N[10:14,:10]=-eta*G.T
        N[14:18,18:22]=eta
        N[18:22,14:18]=-eta
        Q[:10,14:18]=G
        Q[18:22,10:14]=-s.eye(4)
        grading=s.diag(*([1]*14+[-1]*8))
        neg=lambda M:M.subs(dict(zip(p,[-v for v in p])),simultaneous=True)
        label=str(sig)
        matrix_eq(label+' P*N',P*N,p2*s.eye(22))
        matrix_eq(label+' N*P',N*P,p2*s.eye(22))
        matrix_eq(label+' Q^2',Q*Q,s.zeros(22))
        matrix_eq(label+' graded Ward',Q*N+grading*N*neg(Q).T,s.zeros(22))
        # Both ghost entries are odd; all mixed even/odd entries vanish.
        exchange=neg(N).T
        exchange[14:22,14:22]=-exchange[14:22,14:22]
        matrix_eq(label+' graded exchange',N,exchange)
        Pformal=neg(P).T
        Pformal[14:22,14:22]=-Pformal[14:22,14:22]
        matrix_eq(label+' graded Euler adjoint',P,Pformal)
        broken=N.copy();broken[:10,10:14]=s.zeros(10,4);broken[10:14,:10]=s.zeros(4,10)
        witness=(Q*broken+grading*broken*neg(Q).T).applyfunc(s.expand)
        assert witness!=s.zeros(22)
        checks.append(dict(label=label+' omission rejected',zero=False,
                           witness_h00_barc0=str(witness[0,18])))
        outputs.append(dict(signature=sig,p_squared=str(p2),
            ward_zero=True,euler_bisolution_mod_p_squared=True,
            omission_witness=str(witness[0,18])))
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),
        cpu_seconds=time.process_time()-start,matrix_checks=checks,signatures=outputs,
        conclusion='If the flat scalar covariance is an exact bisolution, this numerator yields the field Ward relation and Euler covariance zero; these are sufficient for free BV equivariance of Wick ordering.',
        A1_scope='A1=0 for the explicitly equivariant flat Wick prescription, not automatically for earlier unspecified T1 or curved parametrix',
        chosen_for_curved_model=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result)
    put(D/'manifest.json',dict(artifacts=[dict(path=str(q),sha256=sha(q)) for q in
        [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']],full_Q2=False,gate_changed=False))
    print(json.dumps({k:v for k,v in result.items() if k!='matrix_checks'},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
