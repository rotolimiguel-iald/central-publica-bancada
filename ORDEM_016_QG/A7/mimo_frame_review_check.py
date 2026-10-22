"""Independent bounded audit of frame-connection claims in a received review."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
from fractions import Fraction as F
import hashlib,json,time,uuid
import sympy as s
import bilocal_first_curvature_engine as B
import bilocal_covariant_jet_engine as E
import bilocal_ghost_pair_engine as G
from position_metric_bubble_engine import empty,frob

H=Path(__file__).resolve().parent;D=H/'mimo_frame_review';D.mkdir(exist_ok=True)
receipt_source=H.parents[1]/'IALD_ORQUESTRACAO_20260923/state/handoffs/c76366aa-33c2-4191-b56c-63ba0de3c8cc_delivery.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,b):
    p=D/n;assert not p.exists()
    if not isinstance(b,bytes):b=json.dumps(b,ensure_ascii=False,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
receipt=json.loads(receipt_source.read_bytes())
put('RECEIPT.json',receipt_source.read_bytes())
put('RESPONSE.md',receipt['result']['text'].encode())
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(receipt_source),
    tests=['frame2 from differentiation','tensor multiplicity and exact empty sum',
           'constant-frame vector covariant second jet versus frame-only claim',
           'source includes explicit connection contribution'],remote_call=False))
start=time.process_time();checks=0;nonzero_connection=0
def eq(a,b):
    global checks
    assert s.expand(a-b)==0,(a,b);checks+=1
y=B.y
def frame(a,b):return (sum(v*v for v in y)*B.d(a,b)-y[a]*y[b])/6
def at0(f):return f.subs(dict.fromkeys(y,0))
for i,j,a,b in product(range(4),repeat=4):
    q=s.diff(frame(a,b),y[i],y[j]);eq(q,G.frame2(i,j,a,b))
    eq(q,G.frame2(j,i,a,b))
    # For V^mu=e_b^mu and V^a_frame=delta^a_b, the second covariant
    # derivative in RNC is frame2 + dGamma, not frame2 alone.
    dg=s.diff(E.gamma(y,a,j,b),y[i])
    expected=(B.d(a,i)*B.d(j,b)-B.d(a,j)*B.d(i,b))/2
    eq(q+dg,expected)
    swapped=G.frame2(j,i,a,b)+s.diff(E.gamma(y,a,i,b),y[j])
    eq(q+dg-swapped,B.d(a,i)*B.d(j,b)-B.d(a,j)*B.d(i,b))
    if dg!=0:nonzero_connection+=1
for i,a,b in product(range(4),repeat=3):eq(at0(s.diff(frame(a,b),y[i])),0)
for a,b in product(range(4),repeat=2):
    h=G.tensor(a,b);eq(sum(v*v for v in h),G.multiplicity(a,b))
    if a==b:eq(h[4*a+a],1)
for a in range(4):eq(sum(G.frame2(a,j,j,a) for j in range(4)),F(-1,2))
zero=frob(empty(4),empty(4));eq(zero,0);assert type(zero) is int;checks+=1
source_counts={}
for name in ['bilocal_ghost_pair_engine.py','bilocal_metric_pair_engine_v2.py']:
    text=(H/name).read_text('utf-8')
    marker='F(8,3)*v1[ell]/m-F(2,3)*v2[ell]'
    assert text.count(marker)==1;checks+=1;source_counts[name]=text.count(marker)
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
    nonzero_connection_components=nonzero_connection,
    negative_control=dict(indices=[0,1,0,1],frame2='-1/6',dGamma='2/3',covariant_second_jet='1/2',
                          swapped_covariant_second_jet='-1/2',commutator='1'),
    diagonal_tensor_value=1,empty_sum_type=type(zero).__name__,explicit_connection_source_counts=source_counts,
    verdict='PARTIAL_REVIEW_CONNECTION_COMPLETENESS_AND_DIAGONAL_NORMALIZATION_CORRECTED',full_Q2=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
    [Path(__file__),H/'bilocal_ghost_pair_engine.py',H/'bilocal_metric_pair_engine_v2.py',
     H/'bilocal_covariant_jet_engine.py',H/'position_metric_bubble_engine.py',
     D/'PRE_REGISTER.json',D/'RECEIPT.json',D/'RESPONSE.md',D/'results.json']]))
print(json.dumps(result))
