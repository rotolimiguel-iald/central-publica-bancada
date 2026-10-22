"""Independent checks; do not import production calculation or um.py."""
import hashlib, json, math, re
from decimal import Decimal, ROUND_CEILING, localcontext
from pathlib import Path
from statistics import NormalDist
from datetime import datetime, timezone

root=Path(__file__).resolve().parents[1]
output=Path(__file__).with_name('INDEPENDENT_CHECKS_R1.json')
if output.exists(): raise FileExistsError(output)
def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
result=json.loads((root/'CALCULOS_R2.json').read_text(encoding='utf-8'))
plan=json.loads((root/'PLANO_COMPLEMENTO_R2.json').read_text(encoding='utf-8'))
alpha_path=Path(result['alpha_source']['path'])
raw=alpha_path.read_bytes()
assert hashlib.sha256(raw).hexdigest()==result['alpha_source']['sha256']
matched=re.findall(rb'^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)\s*$',raw,re.M)
assert len(matched)==1
a=float(matched[0]);beta=a*math.exp(.5)
assert beta==result['beta0']
comparisons=[]
for item in result['known_Coulomb_sensitivity_NOT_TGL_PREDICTION']:
    z=item['Z']
    q=a*(8/6)*(-.895929255682)*math.pow(4/(9*math.pi),1/3)*math.pow(z,2/3)
    derivative=1.5*q/(1+q)
    assert math.isclose(q,item['q_Z'],rel_tol=2e-15)
    assert math.isclose(derivative,item['dlnM_dlnAlpha'],rel_tol=2e-15)
    changes={}
    for row in item['rows']:
        f=row['alpha_multiplier_INPUT']
        shift=math.expm1(1.5*(math.log1p(q*f)-math.log1p(q)))*100
        assert abs(shift-row['shift_percent'])<3e-14
        changes[str(f)]=shift
    comparisons.append({'Z':z,'q':q,'dlnM_dlnAlpha':derivative,'changes_percent':changes})
G=6.67430e-11;hbar=6.62607015e-34/(2*math.pi);c=299792458
curv=[]
for row in result['curvature_operator_SIZE_ONLY']['rows']:
    density=row['density_g_cm3_INPUT']*1e3
    # Expanded expression independent of the producer's intermediate lp2 and R.
    eps=8*math.pi*beta*hbar*G**2*density/c**5
    assert math.isclose(eps,row['epsilon_beta0'],rel_tol=1e-15)
    curv.append({'rho_g_cm3':density/1e3,'epsilon':eps})
power=[]
with localcontext() as ctx:
    ctx.prec=60
    for row in result['power_HYPOTHETICAL_ONLY']:
        signal=Decimal(str(row['signal_mag_INPUT']));sigma=Decimal(str(row['sigma_mag_INPUT']))
        n50=int(((5*sigma/signal)**2).to_integral_value(rounding=ROUND_CEILING))
        threshold=Decimal(5)+Decimal(str(NormalDist().inv_cdf(.9)))
        n90=int(((threshold*sigma/signal)**2).to_integral_value(rounding=ROUND_CEILING))
        assert n50==row['n_median_separation_5sigma']
        assert n90==row['n_90pct_power_one_sided_5sigma']
        power.append({'delta':float(signal),'n50':n50,'n90':n90})
# Check every matrix row from its spectral solution, without producer helpers.
deph=[]
for row in result['dephasing_FIXED_H_COMMUTING_JUMPS']['rows']:
    A=row['integrated_diffusion_INPUT'];energies=(0,1,2)
    rho=[[math.exp(-A*(ei-ej)**2)/3 for ej in energies] for ei in energies]
    energy=sum(energies[i]*rho[i][i] for i in range(3))
    purity=sum(rho[i][j]**2 for i in range(3) for j in range(3))
    assert energy==row['energy']==1
    assert math.isclose(purity,row['purity'],rel_tol=1e-15)
    deph.append({'A':A,'E':energy,'purity':purity})
literature=root/'literature'/'L01_chamel_2110_11038v1.html'
html=literature.read_text(encoding='utf-8')
equations={}
for number in (6,7,37,38):
    m=re.search(r'<table[^>]+id="[^"]*E'+str(number)+r'".*?</table>',html,re.S)
    assert m
    equations[str(number)]=re.findall('alttext="([^"]+)"',m.group(0))
treated=Path(plan['curvature']['source'])
lines=treated.read_text(encoding='utf-8').splitlines()
scope=[f'{i+1}: {lines[i]}' for i in range(574,585)]
files=[root/'CALCULOS_R2.json',root/'calculate_r2.py',root/'PLANO_CALCULO_R1.json',root/'PLANO_COMPLEMENTO_R2.json',root/'local_review'/'LOCAL_REUSE_NOTE_20261009.md',root/'local_review'/'LOCAL_NMC_RECONCILIATION_20261009.md',root/'literature'/'LEVANTAMENTO_EOS_FRACO_SN.md',literature,alpha_path,treated,Path(__file__)]
report=root/'RELATORIO_VIABILIDADE_R1.md'
if report.exists(): files.append(report)
payload={'unit':'F8.2.SN1','author':'codex/sn_skeptic','utc':datetime.now(timezone.utc).isoformat(),'verdict':'PASS_CONDITIONAL_CALCULATIONS_NO_PHYSICAL_SIGMA','independence':'Source equations and independent numerical expressions; producer module and um.py never imported or executed. No observed sample.','beta':beta,'Coulomb':comparisons,'curvature':curv,'power':power,'dephasing':deph,'source_equations':equations,'treated_lines':scope,'pins':[pin(p) for p in files]}
data=(json.dumps(payload,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')
with output.open('xb') as f: f.write(data)
print(json.dumps({'output':str(output),'sha256':hashlib.sha256(data).hexdigest(),'verdict':payload['verdict']},ensure_ascii=False))
