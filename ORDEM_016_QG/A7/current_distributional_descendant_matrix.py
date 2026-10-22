"""Full 4x4 counterpart of the corrected actual-current descendant probe."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from current_distributional_descendant_probe import expression
from full_loop_extension_engine import x,z,Q,dx,contact
from position_metric_bubble_engine import LABELS

H=Path(__file__).resolve().parent
D=H/'current_distributional_descendant_matrix'
OLD=H/'current_distributional_descendant_probe'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):
    assert not p.exists(),p
    b=json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)
def parse(t):return s.sympify(t,locals={str(v):v for v in (*Q,*x,z)})

def main():
    D.mkdir(exist_ok=False)
    put(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
       target='All16 components of distributional current descent, both ordered cutoff jets',
       cutoffs=[[1,-1,0,0],[1,0,0,0]],
       method='Reuse five current engines; R(F)+local-contact; compute additional C_di(F) from outer BRST variation; antisymmetrize both ghosts',
       reused_rows='8 unextended kernels of probe v1; no use of its incorrect local subtotal',
       stored_weight='parts.Ymetric already includes1/2; sum parts directly',
       comparison='full hc defect minus distributional descendant of currents; preserve nonzero',
       scope='Fixed cutoff jets, full tensor/ghost basis; no all-cutoff theorem, no complete quantum anomaly',
       no_fit=True,stop_on_nonzero=False,script_sha256=sha(Path(__file__))))
    start=time.process_time();raw=[];locals_current=[];corrections=[];targets=[]
    checks=0
    def eq(a,b):
        nonlocal checks
        assert s.expand(a-b)==0,(a,b);checks+=1
    for order,filename in enumerate(['full_current_contact_matrix/results.json',
                                    'full_current_contact_matrix_swapped/results.json']):
        data=json.loads((H/filename).read_bytes())
        lam=data['lambda_x'];eta=data['eta_y'];L=[a+b for a,b in zip(lam,eta)]
        f=s.zeros(4);C=s.zeros(4);local=s.zeros(4)
        for a,(i,j) in enumerate(LABELS):
            for r in range(4):
                cached=OLD/f'row_{order}_{j}.json' if i==0 and r==0 else None
                if cached is not None:
                    F=parse(json.loads(cached.read_bytes())['unextended_current'])
                else:
                    F=expression(a,r,lam,eta)
                # Two assignments coincide for diagonal h; no hidden tensor weight.
                for derivative,ghost in [(i,j),(j,i)]:
                    f[ghost,r]-=dx(F,derivative)+lam[derivative]*F
                    C[ghost,r]+=contact(F,(derivative,))
                row=next(v for v in data['rows'] if v['a']==a and v['c']==r)
                parts={k:parse(v) for k,v in row['parts'].items()}
                eq(sum(parts.values()),parse(row['polynomial']))
                A=sum(parts[k] for k in ['Ymetric','Ymixed','Yghost','Xmetric','Xmixed'])
                A=A.subs(dict(zip(Q,[Q[k]+L[k] for k in range(4)])),simultaneous=True)
                for derivative,ghost in [(i,j),(j,i)]:
                    local[ghost,r]-=(Q[derivative]+L[derivative])*A
                record=dict(order=order,a=a,h=[i,j],c=r,unextended_current=str(F),
                            reused=str(cached) if cached else None,cpu_seconds=time.process_time()-start)
                put(D/f'component_{order}_{a}_{r}.json',record)
                print(json.dumps(dict(order=order,h=[i,j],c=r,reused=bool(cached),
                      cpu_seconds=record['cpu_seconds'])),flush=True)
        raw.append(f.applyfunc(s.expand));locals_current.append(local.applyfunc(s.expand))
        corrections.append(C.applyfunc(lambda v:s.expand(v.subs(
             dict(zip(Q,[Q[k]+eta[k] for k in range(4)])),simultaneous=True))))
        targets.append(s.Matrix([[parse(v) for v in row] for row in data['graded_adjoint_defect']]))
    radial=sum(v*v for v in x)
    bilocal=(raw[0]-raw[1].T.applyfunc(lambda v:v.subs(dict(zip(x,[-t for t in x])),simultaneous=True)))
    bilocal=bilocal.applyfunc(lambda v:s.cancel(v.subs(z,radial)))
    L=(2,-1,0,0)
    adj=lambda M:M.T.applyfunc(lambda v:s.expand(v.subs(dict(zip(Q,[-Q[k]-L[k] for k in range(4)])),simultaneous=True)))
    local=(locals_current[0]+locals_current[1])/2
    extra=(corrections[0]+corrections[1])/2
    desc=(local-adj(local)+extra-adj(extra)).applyfunc(s.expand)
    target=(targets[0]+targets[1])/2
    difference=(target-desc).applyfunc(s.expand)
    for v in (difference+adj(difference)).applyfunc(s.expand):eq(v,0)
    old=json.loads((H/'current_distributional_descendant_probe_v2/results.json').read_bytes())
    eq(desc[0,0],parse(old['distributional_current_descendant']))
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,
      cpu_seconds=time.process_time()-start,reused_kernel_rows=8,new_kernel_rows=72,
      bilocal_antisymmetric_remainder=[[str(v) for v in row] for row in bilocal.tolist()],
      bilocal_nonzero_components=sum(v!=0 for v in bilocal),
      current_contact_variation=[[str(v) for v in row] for row in (local-adj(local)).applyfunc(s.expand).tolist()],
      extra_derivative_extension_contact=[[str(v) for v in row] for row in (extra-adj(extra)).applyfunc(s.expand).tolist()],
      distributional_current_descendant=[[str(v) for v in row] for row in desc.tolist()],
      difference_full_minus_current=[[str(v) for v in row] for row in difference.tolist()],
      nonzero_difference_components=sum(v!=0 for v in difference),
      interpretation='Purely local descendant interpretation requires bilocal_nonzero_components=0; exact agreement requires nonzero_difference_components=0. Neither is assumed.',
      scope='Fixed pair of cutoff jets, 40 h/c components, 16 two-ghost components; no general-cutoff or curved-space result',
      normalization_selected=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result)
    paths=[Path(__file__),D/'PRE_REGISTER.json',D/'results.json']+sorted(D.glob('component_*.json'))
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],full_Q2=False))
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v,list)},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
