"""Correct stored-weight reading; reuse v1 raw kernels without redoing loops."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, time, uuid
import sympy as s
from full_loop_extension_engine import x,z,Q,dx,contact
from position_metric_bubble_engine import LABELS

H=Path(__file__).resolve().parent
OLD=H/'current_distributional_descendant_probe'
D=H/'current_distributional_descendant_probe_v2'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):
    assert not p.exists(),p
    b=json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)
def parse(t):return s.sympify(t,locals={str(v):v for v in (*Q,*x,z)})

def main():
    assert (OLD/'results.json').exists(),'Wait for the existing process; do not repeat it.'
    D.mkdir(exist_ok=False)
    put(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
        supersedes=str(OLD/'results.json'),predecessor_sha256=sha(OLD/'results.json'),
        correction='Stored parts.Ymetric already includes 1/2. V1 applied that factor again only in the local-contact subtotal. Raw kernels and outer contacts are reusable.',
        no_loop_reexecution=True,no_fit=True,scope='00 component, both cutoff orderings'))
    start=time.process_time();checks=0
    def eq(a,b):
        nonlocal checks
        assert s.expand(a-b)==0,(a,b);checks+=1
    raw=[];corrections=[];locals_current=[];targets=[]
    for order,filename in enumerate(['full_current_contact_matrix/results.json',
                                    'full_current_contact_matrix_swapped/results.json']):
        data=json.loads((H/filename).read_bytes())
        lam=data['lambda_x'];eta=data['eta_y'];L=[a+b for a,b in zip(lam,eta)]
        f=s.Integer(0);C=s.Integer(0);local=s.Integer(0)
        for i in range(4):
            saved=json.loads((OLD/f'row_{order}_{i}.json').read_bytes())
            F=parse(saved['unextended_current']);mult=1+int(i==0)
            outer=parse(saved['outer_contact'])
            eq(outer,mult*contact(F,(i,)))
            C+=outer;f-=mult*(dx(F,i)+lam[i]*F)
            a=LABELS.index((0,i))
            row=next(v for v in data['rows'] if v['a']==a and v['c']==0)
            parts={k:parse(v) for k,v in row['parts'].items()}
            eq(sum(parts.values()),parse(row['polynomial']))
            A=sum(parts[k] for k in ['Ymetric','Ymixed','Yghost','Xmetric','Xmixed'])
            A=A.subs(dict(zip(Q,[Q[j]+L[j] for j in range(4)])),simultaneous=True)
            local-=mult*(Q[i]+L[i])*A
        raw.append(s.expand(f));locals_current.append(s.expand(local))
        corrections.append(s.expand(C.subs(dict(zip(Q,[Q[j]+eta[j] for j in range(4)])),simultaneous=True)))
        targets.append(parse(data['graded_adjoint_defect'][0][0]))
    radial=sum(v*v for v in x)
    bilocal=s.cancel((raw[0]-raw[1].subs(dict(zip(x,[-v for v in x])),simultaneous=True)).subs(z,radial))
    previous=json.loads((OLD/'results.json').read_bytes())
    eq(bilocal,parse(previous['current_bilocal_antisymmetric_remainder']))
    L=(2,-1,0,0)
    adj=lambda f:s.expand(f.subs(dict(zip(Q,[-Q[j]-L[j] for j in range(4)])),simultaneous=True))
    local=s.expand(sum(locals_current)/2)
    extra=s.expand(sum(corrections)/2)
    localdef=s.expand(local-adj(local));extradef=s.expand(extra-adj(extra))
    desc=s.expand(localdef+extradef);target=s.expand(sum(targets)/2)
    diff=s.expand(target-desc)
    eq(diff+adj(diff),0)
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,
        cpu_seconds=time.process_time()-start,loop_reexecuted=False,
        bilocal_antisymmetric_remainder=str(bilocal),bilocal_closed_off_diagonal=bool(bilocal==0),
        current_contact_variation=str(localdef),extra_derivative_extension_contact=str(extradef),
        distributional_current_descendant=str(desc),full_hc_defect_00_polarized=str(target),
        difference_full_minus_current=str(diff),comparison_zero=bool(diff==0),
        control_at_q_zero=dict(current=str(desc.subs(dict.fromkeys(Q,0))),
                              full=str(target.subs(dict.fromkeys(Q,0))),
                              difference=str(diff.subs(dict.fromkeys(Q,0)))),
        interpretation='If the bilocal remainder vanishes, desc is the whole 00 descendant of these five field-current blocks in this prescription. Equality with the full hc defect is measured, not imposed.',
        scope='Two fixed cutoff jets, component00; not full J2 normalization, not full Q2',
        normalization_selected=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result)
    paths=[Path(__file__),D/'PRE_REGISTER.json',D/'results.json',OLD/'results.json']+sorted(OLD.glob('row_*.json'))
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],full_Q2=False))
    print(json.dumps(result,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
