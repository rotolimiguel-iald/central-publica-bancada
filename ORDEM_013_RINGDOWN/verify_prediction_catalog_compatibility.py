"""Check all saved point predictions survive API clarification for coherent fields."""
from pathlib import Path
import hashlib
import json
from tgl_ringdown_prediction import prediction
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def main():
    catalog=json.loads((ROOT/'C4_CATALOG_220.json').read_bytes());count=0;maxerr=0.
    for event in catalog['rows']:
        m,a,z=[event['quantiles'][key][1] for key in ['mass_detector','spin','redshift']]
        for row in event['rows']:
            old=row['median_prediction']
            # Reconstruct the dimensionless complex frequency stored in the point result.
            mode=complex(old['omega_mass'],-old['t_mass_s']/old['tau_gr_s'])
            new=prediction(m,a,row['reading'],redshift=z,
                           qnm_dimensionless=mode if row['reading']=='R-MOD' else None)
            for key in ['gamma_per_s','gamma_over_omega','delta_tau_ensemble_exact']:
                err=abs(new[key]-old[key])/max(abs(old[key]),1e-300)
                maxerr=max(maxerr,err);assert err<1e-12
            count+=1
    coherent=prediction(68.1,.68,'R-RAIZ-COHERENT',occupation=1e78)
    assert coherent['delta_tau'] is None and coherent['delta_tau_ensemble_exact'] is None
    out=dict(status='PASS',point_predictions_checked=count,max_relative_error=maxerr,
             current_prediction_sha256=hashlib.sha256((ROOT/'tgl_ringdown_prediction.py').read_bytes()).hexdigest(),
             prior_prediction_hashes=sorted(set(e['dependency_hashes']['tgl_ringdown_prediction.py'] for e in catalog['rows'])),
             scope='All 264 saved median predictions unchanged; coherent-field API no longer labels initial-slope proxy exact')
    atomic_json(ROOT/'C3_PREDICTION_COMPATIBILITY.json',out);print(json.dumps(out),flush=True)

if __name__=='__main__':main()
