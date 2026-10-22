"""Replay already measured bounds through shared helper with scalar mocks."""
from pathlib import Path
import sys,json,hashlib,ast
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;B=HERE.parents[1];CODE=B/'bis/e2_code'
sys.path.insert(0,str(CODE))
from temporal_contract import validate_time_contract
from registration_guard import publish_new
import lalsimulation as ls
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
measured=HERE/'TEMPORAL_REMNANT_SCALAR_TEST.json'
rows=json.loads(measured.read_text())['temporal']['rows']
names=('SimInspiralChirpTimeBound','SimInspiralMergeTimeBound','SimInspiralFinalBlackHoleSpinBound','SimInspiralRingdownTimeBound')
originals={n:getattr(ls,n) for n in names};results=[]
try:
    for row in rows:
        ls.SimInspiralChirpTimeBound=lambda *a:row['inspiral_s']
        ls.SimInspiralMergeTimeBound=lambda *a:row['merger_s']
        ls.SimInspiralFinalBlackHoleSpinBound=lambda *a:.9
        ls.SimInspiralRingdownTimeBound=lambda *a:row['tail_with_max_dtau_s']/5
        for start,duration in ((1420878135.,8.),(1420878129.,16.)):
            margins=[row['earliest_GPS']-(start+.2),start+duration-.2-row['latest_GPS']]
            expected=min(margins)>=0
            try:
                out=validate_time_contract(row['mass_1'],row['mass_2'],row['chi_1'],row['chi_2'],20.,row['trigger'],dict(start_GPS=start,duration_s=duration,roll_off_s=.2),2.,4.)
            except RuntimeError:
                if expected:raise
                passed=False
            else:
                if not expected or max(abs(a-b) for a,b in zip(out['margins_s'],margins))>1e-7:raise RuntimeError('Shared helper changed margin')
                passed=True
            results.append(dict(duration_s=duration,accepted=passed,expected=expected))
finally:
    for n,f in originals.items():setattr(ls,n,f)
tree=ast.parse((CODE/'pseob_source.py').read_text())
calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='validate_time_contract']
if len(calls)!=1 or len(calls[0].args)!=9:raise RuntimeError('Shared source delegation missing')
out=dict(created_utc=datetime.now(timezone.utc).isoformat(),status='MOCK_REPLAY_ONLY_NO_LAL_BOUND_OR_WAVEFORM_EXECUTION',
  checks=len(results),results=results,source_delegation='One call, nine positional arguments including dtau220/440',
  source_sha256={str(p):sha(p) for p in (Path(__file__),measured,CODE/'pseob_source.py',CODE/'temporal_contract.py')})
publish_new(HERE/'SHARED_TEMPORAL_REPLAY.json',out)
print(json.dumps(dict(checks=len(results),all_expected=True,source_sha256=out['source_sha256'])))
