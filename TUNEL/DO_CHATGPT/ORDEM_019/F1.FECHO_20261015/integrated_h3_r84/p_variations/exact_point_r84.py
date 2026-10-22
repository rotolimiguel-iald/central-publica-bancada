from fractions import Fraction as F
from pathlib import Path
import json,hashlib,datetime
root=Path(__file__).resolve().parent
p=[F(1,2)]+[F(1,12)]*4+[F(1,6)]
g=[F(1),-F(2,3),-F(4,3),-F(2,3)]
ric=[F(3,4),F(1,6),F(4,3),F(2,3)]
t=[F(3,4),-F(1,6),-F(1,3),-F(1,6)]
squares=[[F(1),F(3,2),F(0),F(0)],[F(1),F(0),F(3,4),F(0)]]
quad=lambda a,v:sum(x*y for x,y in zip(a,v))
values=[{'g':str(quad(g,v)),'Ric':str(quad(ric,v)),'T_over_c':str(quad(t,v))} for v in squares]
assert sum(p)==1 and all(x>0 for x in p)
assert values==[{'g':'0','Ric':'1','T_over_c':'1/2'},{'g':'0','Ric':'7/4','T_over_c':'1/2'}]
assert F(1)/F(1,3)==F(2)/F(2,3)==3
r={'status':'PASS_EXACT_POINT_ALGEBRA','method':'fractions.Fraction; no float, no observed data, no Lean; differential derivation is in the note','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'probabilities':[str(x) for x in p],'contractions':values,'incompatible_C_times_c':['2','7/2'],'scope':'Checks algebra of tensors derived analytically; not an independent curvature differentiation.'}
with (root/'EXACT_POINT_RESULT_R84.json').open('xb') as f:f.write((json.dumps(r,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps(r,ensure_ascii=False))
