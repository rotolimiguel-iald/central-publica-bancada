"""Run the registered starts/refinements and retain each separate result."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
from c6_engine import checked_registration
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def rows_by_key(doc):
    return {(r['reading'],r['amplitude_prior_sd_strain']):r for r in doc['results']}

def load_run(start,level,digest):
    path=ROOT/f'C6_STRAIN_{start:g}M_GRID_{level}.json'
    if not path.exists():
        result=subprocess.run([sys.executable,'-B',str(ROOT/'c6_engine.py'),'--start',str(start),'--level',str(level)],
            text=True,capture_output=True,check=False)
        if result.returncode:
            raise RuntimeError(f'C6 {start}M level {level} failed: {result.stderr[-4000:]}')
    doc=json.loads(path.read_bytes())
    if doc['registration_sha256']!=digest:raise ValueError('Stale C6 result')
    return path,doc

def main():
    reg,digest=checked_registration();results=[];checks=[];files=[]
    for start in reg['start_times_tM']:
        old=None
        for level in range(len(reg['quadrature_grids'])):
            path,doc=load_run(start,level,digest)
            files.append(dict(path=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
            current=rows_by_key(doc)
            if old is not None:
                differences={str(key):abs(value['lnB_vs_GR']-old[key]['lnB_vs_GR']) for key,value in current.items()}
                error=max(differences.values())
                passed=error<=reg['quadrature_convergence_abs_lnB']
                checks.append(dict(start_tM=start,levels=[level-1,level],max_abs_lnB_difference=error,passed=passed))
                if passed:break
            old=current
        for row in doc['results']:results.append(dict(start_tM=start,primary_start=start==reg['primary_start_tM'],**row))
        print(json.dumps(dict(start_tM=start,final_level=level,max_abs_lnB_difference=error,converged=passed,
            primary_prior_lnB={r['reading']:r['lnB_vs_GR'] for r in doc['results'] if abs(r['amplitude_prior_sd_strain']-reg['primary_amplitude_sd_scaled']*1e-21)<1e-30})),flush=True)
    atomic_json(ROOT/'C6_RESULTS.json',dict(status='INCONCLUSIVE_SYSTEMATICS',
        reason='Prespecified two-IMR-family calibration criterion was not met; no exclusion or confirmation is permitted',
        registration_sha256=digest,on_source_strain_read=True,convergence=checks,results=results,files=files,
        scope=reg['scope'],do_not_combine='These overlapping windows and all earlier posteriors use the same event; do not multiply their evidences',
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))

if __name__=='__main__':main()
