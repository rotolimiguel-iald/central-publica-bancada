"""Independent invariant reduction and curved-trace control of the C6 table."""
from pathlib import Path
from itertools import product
from datetime import datetime, timezone
import ast, json, sys, time
import sympy as s
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'C6'; H=ROOT/'A7'
sys.path[:0]=[str(D),str(H)]
from deliver_nonminimal_wick_and_mimo_audit import sha,put,write,OUT,append
import tensor_euler_zerojet as T
from smooth_line_compatibility_check_v2 import multiply

def main():
    started=time.process_time(); checks=[]
    data=json.loads((D/'tensor_zerojet/COEFFICIENTS.json').read_bytes())
    rows={ast.literal_eval(k): [[s.Rational(a),s.Rational(b)] for a,b in v] for k,v in data.items()}
    def tr(i):return T.delta(i[0],i[1])*T.delta(i[2],i[3])
    def eq(name,a,b):
        assert s.expand(a-b)==0,(name,a,b)
        checks.append(name)
    for ind, sides in rows.items():
        for side,(a,b) in enumerate(sides):
            eq('first '+str((ind,side)),a,-s.Rational(3,16)*T.S(ind)-tr(ind)/2)
            eq('second '+str((ind,side)),b,s.Rational(1,16)*T.S(ind)+tr(ind)/2)
    for i,j in product(rows,repeat=2):
        ci=-T.S(i)*T.S(j)/8+(T.S(i)*tr(j)-tr(i)*T.S(j))/2
        cj=-T.S(i)*T.S(j)/8+(T.S(j)*tr(i)-tr(j)*T.S(i))/2
        for side in (0,1):
            actual=T.S(j)*rows[i][side][0]+T.S(i)*rows[j][side][1]
            eq('invariant '+str((i,j,side)),actual,ci)
        eq('line swap sum '+str((i,j)),ci+cj,-T.S(i)*T.S(j)/4)
    # A tensor trace uses the metric at each endpoint, not four frozen deltas.
    # The flat derivative contact multiplied by the first metric jet contributes.
    frozen=sum(-T.S((a,a,c,c))*T.S((e,e,g,g))/8+
        (T.S((a,a,c,c))*tr((e,e,g,g))-tr((a,a,c,c))*T.S((e,e,g,g)))/2
        for a,c,e,g in product(range(4),repeat=4))
    eq('frozen double trace misses metric jets',frozen,-2)
    radius=T.xx
    traced_flat_line=-4
    traced_metric_jet=-sum(-T.B.gX1[a,b]*T.delta(a,b) for a,b in product(range(4),repeat=2))
    eq('one line traced metric jet',traced_metric_jet,-radius)
    multiplier=2*traced_flat_line*traced_metric_jet
    correction=multiply(multiplier,s.Rational(3,32)*sum(t*t for t in T.x))
    # Distribution polynomials in the existing engine encode derivatives of delta.
    eq('metric-jet contact',correction,6)
    eq('covariant full trace equals sixteen scalar contacts',frozen+correction,4)
    # Independently contract the actual bilocal parametrix BEFORE anchoring.
    trace0=sum(T.raw(0,(a,a,c,c)) for a,c in product(range(4),repeat=2))
    trace1=sum(T.raw(1,(a,a,c,c)) for a,c in product(range(4),repeat=2))
    trace1-=sum(T.B.gX1[a,b]*T.raw(0,(a,b,c,c)) for a,b,c in product(range(4),repeat=3))
    trace1-=sum(T.B.gY1[c,d]*T.raw(0,(a,a,c,d)) for a,c,d in product(range(4),repeat=3))
    z=sum((T.x[i]-T.y[i])**2 for i in range(4))
    target=-4*((T.xx*T.yy-T.xy**2)/(3*z*z)+s.Rational(1,4)-2*s.log(z))
    assert s.cancel(trace0+4/z)==0
    assert s.cancel(trace1-target)==0
    checks.extend(['bilocal traced principal profile','bilocal trace potential lambda=6'])
    # Nonvacuous controls: density omission and wrong connection sign.
    ind=(0,0,0,0); flat=T.S(ind)**2*s.Rational(3,32)*sum(t*t for t in T.x)
    density=multiply(-radius/2,flat)
    eq('omitting density leaves endpoint difference',-density,s.Rational(3,32))
    f0=T.raw(0,ind); coords=T.x
    connections=sum(2*g*s.diff(T.raw(0,replaced),coords[i])+s.diff(g,coords[i])*T.raw(0,replaced)
        for i in range(4) for g,replaced in T.connection_lines(ind,0,i))
    wrong=s.cancel((-2*connections).subs(T.zero))
    assert wrong!=0
    checks.append('wrong tensor connection sign rejected')
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-started,
        first='-3*S/16-T/2',second='S/16+T/2',
        tensor_contact='CE*K*[-S_i*S_j/8+(S_i*T_j-T_i*S_j)/2]*delta',
        both_line_sum='-CE*K*S_i*S_j*delta/4',
        frozen_double_trace=str(frozen),metric_jet_correction=str(correction),covariant_double_trace='4',
        wrong_connection_residual=str(wrong),density_omission_difference='3/32',
        full_Q2=False,gate_changed=False)
    put(D/'tensor_zerojet/INVARIANT_AUDIT.json',result)
    put(D/'tensor_zerojet/INVARIANT_MANIFEST.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'tensor_zerojet/COEFFICIENTS.json',D/'tensor_zerojet/INVARIANT_AUDIT.json',H/'smooth_line_compatibility_check_v2.py']]))
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
