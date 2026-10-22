"""Conditional Poisson/calendar and O5 scaling scenarios; no schedule promise."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math
from scipy.stats import chi2
B=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
names=['bis/E0_SNR_INFORMATION_FIT.json','bis/e0_core/E0_CORE.json','bis/e0_metadata/GWOSC_INVENTORY.json','cache/e0_metadata/gwosc_runs.json','bis/e0_metadata/SCENARIOS_AND_SCHEDULES.json']
fit,core,inv,runs,scen=[json.loads((B/n).read_bytes()) for n in names]
out=B/'bis/E0_RATE_O5_SCENARIOS.json'
if out.exists():raise FileExistsError(out)
def poisson(n,years):
    return dict(N=n,exposure_years=years,rate_mle_per_year=n/years,rate_CI90_per_year=[float(chi2.ppf(.05,2*n)/(2*years)) if n else 0.,float(chi2.ppf(.95,2*(n+1))/(2*years))])
rr=[r for r in runs['results'] if r['name'] in ['O4a','O4b']]
if len(rr)!=2:raise ValueError('Missing archived run interval')
calendar=sum(r['gps_end']-r['gps_start'] for r in rr)/(365.25*86400)
chosen=next(r for r in fit['fits'] if r['population']=='GWTC5_31')['rows']
o4=[r for r in chosen if r['run'] in ['O4a','O4b']]
rare=inv['by_run']['O4a']['thresholds']['78']['events']+inv['by_run']['O4b']['thresholds']['78']['events']
exposures=[dict(years=1.45,status='INPUT_NOMINAL_ORDER_EXPOSURE__NOT_LIVE_TIME',definition='Nominal O4 duration used by management, retained for direct arithmetic comparison'),dict(years=calendar,status='DERIVED_ARCHIVE_CALENDAR_SPAN__NOT_LIVE_TIME',definition='Sum of GWOSC run gps_end-gps_start; archive boundaries can include engineering data and do not establish observing duty')]
rates=[];forecasts=[]
gains=[('O5_BBH_LOW',scen['o5_gain']['bbh_range_ratio'][0]),('O5_BBH_HIGH',scen['o5_gain']['bbh_range_ratio'][1]),('O5_C5_PSD',scen['o5_gain']['c5_ratio']),('BNS_ONLY_UPPER_CONTROL',scen['o5_gain']['bns_upper_only'])]
for exp in exposures:
    rp=poisson(len(rare),exp['years']);rc=poisson(len(o4),exp['years'])
    rates.append(dict(exposure=exp,rare_SNR_ge78=rp,rare_events=rare,calibration_O4_subset=rc,calibration_events=[r['event'] for r in o4],scope='Conditional stationary Poisson model for counts in this published universe; neither complete observing exposure nor pipeline selection efficiency measured'))
    for name,g in gains:
        n3=3*rc['rate_mle_per_year']*g**3
        n3band=[3*x*g**3 for x in rc['rate_CI90_per_year']]
        for reading,r in core['combinations']['GWTC5_31']['std_ddof1'].items():
            if reading=='GR_FALSE_FALSIFIER':continue
            z=r['z_comb'];N90=r['N90'];delta=r.get('delta_weighted')
            resolved=delta is not None and abs(delta)>=1e-12
            forecasts.append(dict(exposure_status=exp['status'],reading=reading,gain_label=name,gain=g,reference_population='GWTC5_31 spanning several runs, not pure O4',rate_population='O4 subset of the 31 published calibration events',count_expected_3_scenario_years=n3,count_CI90_from_Poisson_rate=n3band,z_optimistic_same_source_quality_plus_volume=(z*g*math.sqrt(n3/r['N_events'])) if z is not None else None,z_optimistic_CI90_rate_only=[z*g*math.sqrt(n/r['N_events']) for n in n3band] if z is not None else None,z_detection_threshold_quality_invariant_control=z*math.sqrt(n3/r['N_events']) if z is not None else None,N90_at_fixed_source_improved_sigma=N90/g**2 if N90 is not None and resolved else None,operational_information_target=r['I_tau_target90'] if resolved else None,systematic_gate='NOT_CALIBRATED_RED',test_verdict=None,scope='Illustrative assumptions only. Combining sigma/g with rate*g^3 supposes the added population retains the improved quality of fixed sources; selection/distance effects are not modeled. The rate-only control keeps detected quality invariant under a Euclidean threshold model. BNS factor never a BBH forecast.'))
doc=dict(status='NONBLIND_CONDITIONAL_RATE_AND_FORECAST__NO_CALENDAR_PROMISE',utc=datetime.now(timezone.utc).isoformat(),sources={n:sha(B/n) for n in names},code_sha256=sha(Path(__file__)),rates=rates,forecasts=forecasts,source_intervals=rr,limitations=['A source-calendar span is not network live time. True exposure/selection-normalized rates remain OPEN.','The rare definition SNR>=78 is a metadata proxy; it does not guarantee GW250114 damping precision or posterior width.','The 31 calibration products span older runs and O4. Calling this mixture pure O4 would be inaccurate.','No physical sigma significance or 5sigma reach follows with the systematic gate red. Numbers are prospective scaling diagnostics.','O5 is phased and historical range ratios are not a guaranteed sensitivity at its start.'])
with out.open('xb') as f:f.write((json.dumps(doc,indent=2,allow_nan=False)+'\n').encode())
print(json.dumps(dict(path=str(out),sha256=sha(out),rare_count=len(rare),O4_calibration_subset=len(o4),archive_calendar_years=calendar,nominal_rare_rate=rates[0]['rare_SNR_ge78'])))
