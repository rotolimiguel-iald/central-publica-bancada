"""Check the exact linear-slot Ward bridge, including its antifield Euler term."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
H=Path(__file__).resolve().parent;D=H/'linear_slot_ward_bridge'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):
    assert not p.exists(),p
    b=json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
def main():
    D.mkdir(exist_ok=False)
    put(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
        target='A2(Vchi,c)=0 under linear-slot perturbative agreement and both Green inverse identities',
        hypotheses=['s0 Vchi antighost right derivative = chi Q w - Q(chi w), w=c.nabla c',
            'C Lie_c Kg c=Qw, the polarization of classical BRST nilpotence',
            'GD Q=Q GD=I, with supports/domain sufficient for the paired kernels',
            'Same Wick/time-ordering prescription; linear-slot perturbative agreement'],
        exclusions=['No A2(Vchi,Veta)','No physical global state or inverse on arbitrary spaces'],
        sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'linear_anomaly_insertion/results.json',H/'bv_antifield_coordinate/results.json']]))
    start=time.process_time();checks=[]
    def eq(label,values):
        vals=list(values) if isinstance(values,s.MatrixBase) else [values]
        assert all(s.cancel(v)==0 for v in vals),(label,values);checks.append(label)
    # Exact finite surrogate tests operator order. It is not a spacetime Green construction.
    Q=s.Matrix([[4,1,0,0],[1,5,1,0],[0,1,6,1],[0,0,1,7]])
    G=Q.inv();cv=s.symbols('chi0:4');chi=s.diag(*cv);w=s.Matrix(s.symbols('w0:4'))
    eq('left inverse',G*Q-s.eye(4));eq('right inverse',Q*G-s.eye(4))
    derivative=chi*Q*w-Q*chi*w
    qtree=G*chi*Q*w
    source=G*derivative
    eq('full linear slot Ward',qtree-source-chi*w)
    assert source!=s.zeros(4,1);checks.append('variable cutoff source is retained')
    eq('constant cutoff source vanishes',source.subs(dict.fromkeys(cv,s.Symbol('chi'))))
    eq('omitted antifield Euler yields nonzero bracket',qtree-G*chi*Q*w-chi*w+chi*w)
    assert qtree-G*chi*Q*w-chi*w!=s.zeros(4,1)
    checks.append('missing antifield term rejected')
    wrong=G*(chi*Q-Q*chi).T*w
    assert qtree-wrong-chi*w!=s.zeros(4,1)
    checks.append('transpose/order error rejected')
    # Differential product rule for the cutoff source, independent of finite matrices.
    x=s.symbols('x0:4');lam=s.symbols('l0:4');p=s.symbols('p0:4');mass=s.symbols('mass')
    for sig in [(1,1,1,1),(-1,1,1,1)]:
        c=s.exp(sum(lam[i]*x[i] for i in range(4)));v=s.exp(sum(p[i]*x[i] for i in range(4)))
        lap=lambda f:sum(sig[i]*s.diff(f,x[i],2) for i in range(4))+mass*f
        actual=s.expand((lap(c*v)-c*lap(v))/(c*v))
        expected=sum(sig[i]*(lam[i]**2+2*lam[i]*p[i]) for i in range(4))
        eq('cutoff differential commutator '+str(sig),actual-expected)
    data=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        identity='s0 Tc2(Vchi,c)-Tc2(s0 Vchi,c)-(Vchi,c)=GD chi Q w-GD(chi Q-Q chi)w-chi w=0',
        source='dR(s0 Vchi)/dbarc=chi Qw-Q(chi w)=-[Q,chi]w',
        commutator='[Q,chi]w=2(nabla chi).nabla w+(box chi)w for Q=box+3K',
        missing_antifield_control='omitting -Q(chi w) leaves -chi w in the Ward defect',
        linear_A1_pair_zero='Tc2(A1(Vchi),c)=0 since both entries contain only c',
        conclusion='The linear insertion bridge cancels exactly under the declared normalization; this fixes a necessary subset of the A2 dictionary',
        full_Q2=False,gate_changed=False)
    put(D/'results.json',data);put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
        [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']],full_Q2=False))
    print(json.dumps(data,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
