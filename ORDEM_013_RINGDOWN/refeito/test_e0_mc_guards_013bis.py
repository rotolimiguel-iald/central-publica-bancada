"""Negative tests only, safe under -O; freeze current provenance without MC rerun."""
import json,copy,sys,hashlib
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import e0_mc_guarded_013bis as m
B=Path(__file__).resolve().parents[1]
def main():
    d=json.loads((B/'bis/E0_ROUTE_IV_POWER_v2.json').read_bytes())
    p=json.loads((B/'bis/E0_ROUTE_IV_PROVENANCE.json').read_bytes())
    rows=d['per_event'];sel=p['selected_events'];passed=[]
    def reject(name,fn):
        try:fn()
        except ValueError:passed.append(name)
        else:raise RuntimeError('Guard failed '+name)
    reject('unknown member',lambda:m.validate_population(rows,sel[:-1]+['UNKNOWN_EVENT']))
    reject('duplicate member',lambda:m.validate_population(rows,sel[:-1]+[sel[0]]))
    bad=copy.deepcopy(rows);bad[0]['sigma_df']=float('nan');reject('NaN width',lambda:m.validate_population(bad,sel))
    reject('NaN statistic',lambda:m.lrt([[2]],[[float('nan')]],[[1]],[1]))
    reject('inconsistent sums',lambda:m.lrt([[2]],[[4]],[[1]],[1]))
    reject('empty class nonzero',lambda:m.lrt([[0,2]],[[1,0]],[[1,1]],[1,1]))
    reject('NaN before counting',lambda:m.count_above([float('nan')]))
    reject('invalid N',lambda:m.sufficient(0,[1],0,1,1))
    reject('invalid variance',lambda:m.sufficient(2,[0],0,1,1))
    t,q=m.lrt([[3]],[[0]],[[1]],[1]);m.count_above(t)
    pops=m.frozen_populations()
    data={'status':'POSTHOC_GUARDS_AND_FROZEN_POPULATIONS__NO_MC_RERUN','utc':datetime.now(timezone.utc).isoformat(),
      'python_optimize':sys.flags.optimize,'negative_tests':passed,'populations':pops,
      'original_provenance_sha256':m.sha(B/'bis/E0_ROUTE_IV_PROVENANCE.json'),
      'new_guard_code_sha256':m.sha(B/'refeito/e0_mc_guarded_013bis.py'),
      'test_code_sha256':m.sha(Path(__file__)),
      'scope':'Future calls use explicit membership and finite-value guards; original published values unchanged and independently checked. Snapshot is posthoc, not a retroactive preregistration.'}
    with (B/'bis/E0_MC_GUARD_CLOSURE.json').open('x',encoding='utf-8') as f:json.dump(data,f,indent=2,allow_nan=False)
    print(json.dumps({'status':data['status'],'negative_tests':len(passed),'populations':{k:len(v['events']) for k,v in pops.items()}}))
if __name__=='__main__':main()
