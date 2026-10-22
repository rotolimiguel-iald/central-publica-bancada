"""Correct the two named F4 review findings beside immutable prior versions."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,copy
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(name,doc):
    p=ROOT/name
    if p.exists():raise FileExistsError(p)
    raw=(json.dumps(doc,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode();tmp=p.with_suffix('.tmp')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise ValueError('Write mismatch')
    tmp.replace(p);print(name,sha(p))
f=json.loads((ROOT/'C5_FISHER_v2.json').read_bytes())
f['same_source_R_B_linear_historical']=copy.deepcopy(f['same_source_R_B'])
for r in f['same_source_R_B']:
    matches=[s for s in f['records'] if s['psd']==r['psd'] and s['reading']=='R-B' and s['snr_ringdown']==40 and s['scenario']=='FREQUENCY_FREE_TAU_GR_FIXED']
    if len(matches)!=1:raise ValueError('Ambiguous Fisher reference')
    z=matches[0]['z_logdecay']*r['snr_ratio_to_O4']
    r.update(z_local=z,lnB_mean_if_reading=z*z/2,lnB_standard_deviation=z,convention='log1p(x)/sigma_log_decay; point hypotheses')
f.update(supersedes='C5_FISHER_v2.json',supersedes_sha256=sha(ROOT/'C5_FISHER_v2.json'),
 correction=dict(utc=datetime.now(timezone.utc).isoformat(),finding='F4-R1',builder_sha256=sha(Path(__file__)),review_sha256=sha(ROOT/'bis/F4_POWER_GATE_REVIEW.md')))
new('C5_FISHER_v3.json',f)
g=json.loads((ROOT/'PORTAO_DO_PODER_013.json').read_bytes())
norm=json.loads((ROOT/'bis/F4_GW250114_WINDOW_POWER_NORM.json').read_bytes())
bases=[b for b in g['bases'] if b['name']=='GW250114_MEASURED_NORM_10tM']
if len(bases)!=1:raise ValueError('Ambiguous measured base')
rho=bases[0]['rho']
for r in g['measured_psd_control']:
    r.update(rho_used=rho,rho_kind='NETWORK_NORM_APPLIED_TO_EACH_PSD_SCENARIO',scope='Separate PSD-shape scenarios at common network rho; not detector-specific measured z or combined network Fisher')
g.update(supersedes='PORTAO_DO_PODER_013.json',supersedes_sha256=sha(ROOT/'PORTAO_DO_PODER_013.json'),
 correction=dict(utc=datetime.now(timezone.utc).isoformat(),finding='F4-R2',builder_sha256=sha(Path(__file__)),review_sha256=sha(ROOT/'bis/F4_POWER_GATE_REVIEW.md')),
 current_fisher=dict(path='C5_FISHER_v3.json',sha256=sha(ROOT/'C5_FISHER_v3.json'),note='Original frozen dependency remains; current same-source auxiliary table corrected beside. Gate readings unchanged.'))
new('PORTAO_DO_PODER_013_v2.json',g)
