"""Recount frozen C5 results; no new calibration or promotion of old jobs."""
from pathlib import Path
from collections import defaultdict,Counter
from datetime import datetime,timezone
import hashlib,json,statistics
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
paths=[ROOT/n for n in ('C5_IMR_RECOVERY.json','C5_RECOLORED_FORECAST.json','C5_EMPIRICAL_IMR.json',
    'C5_EMPIRICAL_IMR_STARTS.json','C5_NONLINEAR_SOURCE_SUMMARY.json','C5_SOURCE_UNCERTAINTY_SUMMARY.json')]
imr,recolor,emp,starts,nonlinear,uncertainty=[json.loads(p.read_bytes()) for p in paths]
resolved={'R-B','R-RAIZ-0','R-LIN','R-MOD'}
groups=defaultdict(list)
for row in recolor['results']:
    if row['reading'] in resolved:
        key=tuple(row[k] for k in ('content','psd','recovery','reading','SNR'))
        groups[key].append(row)
group_counts=defaultdict(lambda:dict(total=0,passed=0))
for key,rows in groups.items():
    if len(rows)!=4 or len({(r['family'],r['injected_a']) for r in rows})!=4:
        raise ValueError('Incomplete two-family/two-injection group')
    group_counts[key[0]]['total']+=1
    group_counts[key[0]]['passed']+=int(all(r['status']=='CALIBRATED_CONDITIONAL_CELL' for r in rows))
opposite=[r for r in imr['results'] if r['reading'] in resolved and r['recovery'] in ('SEOBNRv4HM','IMRPhenomXPHM') and r['recovery']!=r['injection_family']]
joint=[r for r in imr['joint_mixture_criteria'] if r['reading'] in resolved]
low=[]
for reading in sorted(resolved):
    cells=[r for r in imr['results'] if r['reading']==reading and r['SNR']==40]
    for a in (0.,1.):
        matching=[r for r in cells if r['injected_a']==a and r['recovery']==r['injection_family']]
        vals=[r['lnB']['mean'] for r in matching]
        low.append(dict(reading=reading,injected_a=a,scope='Same-family fixed-source closed-set control; not calibration against model mismatch',
            mean_lnB_range=[min(vals),max(vals)],warning='Positive mean lnB at low SNR can be prior-volume/Occam effect; never convert it to sigma'))
result=dict(status='C5_CLOSED_AS_MEASURED_WALL__NO_NEW_CAMPAIGN',created_utc=datetime.now(timezone.utc).isoformat(),
    recolored_group_counts=dict(group_counts),opposite_family=dict(cells=len(opposite),
        calibrated=sum(r['status']=='CALIBRATED_CONDITIONAL_CELL' for r in opposite),
        median_absolute_bias=statistics.median(r['absolute_bias'] for r in opposite)),
    closed_set_mixture_groups=dict(total=len(joint),passed=sum(r['pass_all_four'] for r in joint),
        warning='Manufactured closure / inverse crime: truth lies inside recovery mixture, fixed source. High-SNR SEOB resolution unresolved.'),
    empirical_initial_status_counts=dict(Counter(r['status'] for r in emp['results'])),
    empirical_start_control_status_counts=dict(Counter(r['status'] for r in starts['results'])),
    low_snr_occam=low,nonlinear_RB_only=dict(same_family_residual_range=nonlinear['same_family_residual_range'],
        opposite_family_residual_range=nonlinear['opposite_family_residual_range'],
        source='C5_NONLINEAR_SOURCE_SUMMARY.json',scope='R-B, start10tM, nonblind local searches, not all readings.'),
    not_paid=['Source-marginalized bias/coverage at relevant SNR','Equivalent nonlinear-source campaign for other readings',
        'ET/CE full-IMR recovery','SEOB numerical resolution at SNR >=200'],
    optional_additional_nonlinear_search=dict(performed=False,machine_seconds_used=0,
        reason='Asymmetric rigor explicitly retained as permitted by F4; no new C5 campaign reopened. Zero is spent time, not a cost estimate or evidence that a search is expensive.'),
    stop_rule='Result, falsifier or measured wall closes C5. Old running jobs are diagnostic appendices excluded from gate and verdict. Part B is a separate route.',
    hashes={str(p.relative_to(ROOT)):sha(p) for p in paths})
out=ROOT/'bis/C5_WALL_COUNTS_013BIS.json'
if out.exists():raise FileExistsError(out)
raw=(json.dumps(result,indent=2,ensure_ascii=False)+'\n').encode();tmp=out.with_suffix('.tmp')
with tmp.open('xb') as f:f.write(raw)
if tmp.read_bytes()!=raw:raise RuntimeError('Write mismatch')
tmp.replace(out)
print(json.dumps({k:result[k] for k in ('recolored_group_counts','opposite_family','closed_set_mixture_groups','empirical_initial_status_counts')},indent=2))
print('sha256',sha(out))
