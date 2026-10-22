"""Create an exact-arithmetic successor without changing cited v1 artifacts."""
from pathlib import Path
import hashlib,json,uuid
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,text):
    assert not p.exists(),p
    b=text.encode('utf-8');t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
p=H/'bilocal_metric_pair_engine.py'
text=p.read_text('utf-8')
old='frob(sandwich(U[e],AX[ex],V[ell-e]),BY)/16'
new='F(frob(sandwich(U[e],AX[ex],V[ell-e]),BY),16)'
assert text.count(old)==1
text=text.replace(old,new)
put(H/'bilocal_metric_pair_engine_v2.py',text)
p=H/'bilocal_metric_pair_check.py';text=p.read_text('utf-8')
text=text.replace('import bilocal_metric_pair_engine as E','import bilocal_metric_pair_engine_v2 as E')
text=text.replace("D=H/'bilocal_metric_pair'","D=H/'bilocal_metric_pair_v2'")
text=text.replace("H/'bilocal_metric_pair_engine.py'","H/'bilocal_metric_pair_engine_v2.py',H/'bilocal_metric_pair_engine.py'")
text=text.replace("cpu=time.process_time();checks=[];point=", "cpu=time.process_time();checks=[]\nassert isinstance(E.frob(E.empty(1),E.empty(1))/16,float)\nassert isinstance(F(E.frob(E.empty(1),E.empty(1)),16),F)\nchecks.append(('empty_sum_float_regression',))\npoint=")
text=text.replace("for o in (0,1):\n    for b in (1,2,3):", "for o in (0,1):\n    for row in values[o]:\n        for value in row:\n            assert isinstance(value,F),(o,value,type(value));checks.append(('exact_output_type',))\n    for b in (1,2,3):")
text=text.replace("status='METRIC_LOOP_Y_DIVERGENCE_POINT_MEASURED'", "status='METRIC_LOOP_Y_DIVERGENCE_POINT_EXACT_MEASURED'")
put(H/'bilocal_metric_pair_check_v2.py',text)
note=dict(status='V1_NUMERIC_NOT_EXACT_V2_PENDING',
 reason='frob of an empty contraction returns integer 0; division by 16 creates float and contaminates rational accumulation',
 correction='Fraction(frob(...),16) before accumulation; exact type assertions at output',
 v1_result_sha256=sha(H/'bilocal_metric_pair/results.json'),
 v1_engine_sha256=sha(H/'bilocal_metric_pair_engine.py'),
 v2_engine_sha256=sha(H/'bilocal_metric_pair_engine_v2.py'),
 v2_runner_sha256=sha(H/'bilocal_metric_pair_check_v2.py'),
 original_files_changed=False,gate_changed=False)
put(H/'METRIC_PAIR_EXACTNESS_ERRATUM.json',json.dumps(note,indent=2))
print(json.dumps(note))
