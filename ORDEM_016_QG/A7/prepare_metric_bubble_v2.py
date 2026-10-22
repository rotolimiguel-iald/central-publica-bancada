"""Make an explicit additive correction of the metric bubble contraction."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent
source=root/'metric_bubble_check.py'
dest=root/'metric_bubble_check_v2.py'
assert not dest.exists()
text=source.read_text('utf-8')
changes={
    "DEST=HERE/'metric_bubble'":"DEST=HERE/'metric_bubble_v2'",
    "numerator='Tr(S0 W_A S0 W_B)/16; W=16*kappa*V3'":
        "numerator='Tr(S0 W_A S0 transpose(W_B))/16; W=16*kappa*V3',\n    correction='Internal lines pair i with k and j with l; fixed-routing cubic matrices are not symmetric',\n    supersedes_sha256='"+hashlib.sha256(source.read_bytes()).hexdigest()+"'",
    "return [S*C for C in cs]":"return cs",
    "cache=[coefficients(H) for H in bs]":"""cache=[coefficients(H) for H in bs]
left_cache=[[S*C*S for C in cs] for cs in cache]
# Independent explicit four-index Wick contraction at a nonzero integer node.
metric=s.Matrix(10,10,lambda i,j:sum(bs[i][k]*bs[j][k] for k in range(16))
    -s.Rational(1,2)*sum(bs[i][5*k] for k in range(4))*sum(bs[j][5*k] for k in range(4)))
assert metric.inv()==S
checks.append('inverse_fiber_pairing_from_basis')
wa=W(bs[0],(2,-1,1,3));wb=W(bs[4],(2,-1,1,3))
direct=sum(wa[i,j]*wb[k,l]*S[i,k]*S[j,l]
    for i in range(10) for j in range(10) for k in range(10) for l in range(10))
check('four_index_Wick_matches_transposed_trace',direct,s.trace(S*wa*S*wb.T))
assert direct!=s.trace(S*wa*S*wb), 'negative control requires non-symmetric routing'
checks.append('old_untransposed_contraction_rejected')
""",
    "for m,A in zip(mons,cache[a]):":"for m,A in zip(mons,left_cache[a]):",
    "val=sum(A[i,j]*B[j,i] for i in range(10) for j in range(10))":
        "val=sum(A[i,j]*B[i,j] for i in range(10) for j in range(10))",
    "neg=[]":"neg=['old_untransposed_contraction_vs_direct_Wick']",
    "assert sum(x*y for x,y in zip(wrong,invariants(*fit[-1])))!=0":
        "assert sum(x*y for x,y in zip(wrong,invariants(*fit[-1])))!=0\nassert sum(x*y for x,y in zip(combined,invariants(*fit[-1])))==0",
}
for old,new in changes.items():
    assert text.count(old)==1,(old,text.count(old))
    text=text.replace(old,new)
raw=text.encode('utf-8');tmp=dest.with_name(dest.name+'.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and raw;tmp.replace(dest)
print(dest)
