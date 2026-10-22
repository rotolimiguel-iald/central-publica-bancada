"""Measure all rank-two contacts with at most two ordered spectator-end jets."""
from pathlib import Path
from itertools import product
from datetime import datetime,timezone
import json,sys,time,ast
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'C6/tensor_yjets';H=ROOT/'A7'
sys.path[:0]=[str(ROOT/'C6'),str(H)]
import sympy as s
import tensor_euler_yjet_engine as E
import balanced_log_pair_engine as R
from deliver_nonminimal_wick_and_mimo_audit import sha,put

def main():
    D.mkdir(exist_ok=False);start=time.process_time()
    sources=[Path(__file__),ROOT/'C6/tensor_euler_yjet_engine.py',ROOT/'C6/tensor_euler_zerojet.py',H/'bilocal_covariant_jet_engine.py',H/'bilocal_first_curvature_engine.py',H/'balanced_log_pair_engine.py',H/'smooth_line_compatibility_check_v2.py']
    put(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),target='All ordered Y covariant jets with total degree at most two, X densitized Euler on first metric line',
        prescription='Existing partial R_bal and smooth-line completion',degree='First curvature; polynomial in derivatives of delta of degree len(u)+len(v)',
        expected_numeric_coefficients=None,vertices_included=False,full_Q2=False,sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
    inds=[(a,b,c,d) for a in range(4) for b in range(a,4) for c in range(4) for d in range(c,4)]
    words=[()]+[(i,) for i in range(4)]+list(product(range(4),repeat=2))
    pairs=[(u,v) for u,v in product(words,repeat=2) if len(u)+len(v)<=2]
    zero=json.loads((ROOT/'C6/tensor_zerojet/COEFFICIENTS.json').read_bytes())
    block_results=[];shape_checks=0;zero_checks=0
    for k,(u,v) in enumerate(pairs):
        coeff={};degree=len(u)+len(v)
        for ind in inds:
            a=E.first(ind,u,v);b=E.second(ind,u,v)
            for val in [a,b]:
                assert not val.free_symbols.difference(R.Q),(u,v,ind,val)
                assert all(sum(p)==degree for p,c in s.Poly(val,*R.Q).terms() if c),(u,v,ind,val)
                assert not val.has(s.Float)
                shape_checks+=1
            coeff[str(ind)]=[str(a),str(b)]
            if not u and not v:
                expected=zero[str(ind)][0]
                assert a==s.Rational(expected[0]) and b==s.Rational(expected[1])
                zero_checks+=2
        # These 200 coefficient polynomials generate all 10000 component pairs by bilinearity.
        p=D/f'block_{k:02d}.json';put(p,dict(u=u,v=v,coefficients=coeff))
        block_results.append(dict(path=str(p),sha256=sha(p),u=u,v=v))
        print(json.dumps(dict(block=k+1,total=len(pairs),u=u,v=v,cpu_seconds=time.process_time()-start)),flush=True)
    result=dict(at=datetime.now(timezone.utc).isoformat(),ordered_blocks=len(pairs),line_components=len(inds),
        component_pairs_represented=len(pairs)*len(inds)**2,coefficient_shape_checks=shape_checks,zerojet_regression_checks=zero_checks,
        cpu_seconds=time.process_time()-start,derivative_order_tested=2,first_curvature_only=True,
        independent_symmetry_audit_pending=True,full_Q2=False,gate_changed=False)
    put(D/'results.json',result);put(D/'manifest.json',dict(sources=[dict(path=str(p),sha256=sha(p)) for p in sources],blocks=block_results,results_sha256=sha(D/'results.json')))
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
