"""Independent bounded review; no import/run of delivered scientific programs."""
from pathlib import Path
import json,math,hashlib,datetime,re,html
from audit_provenance import atomic,OUT,metadata
BASE=OUT.parent/'derivacoes'
spec=json.loads((BASE/'F2_FONTES_SHA256.json').read_text(encoding='utf-8'))
result=json.loads((BASE/'F2_CALCULOS_CONDICIONAIS.json').read_text(encoding='utf-8'))
records=[]
def record(path,expected=None,role='review input'):
    meta,raw=metadata(path)
    meta['role']=role
    if expected:meta['matches_delivery_hash']=meta['sha256']==expected
    records.append(meta)
    return raw
for name in ['NOTA_DERIVACOES_F2.md','f2_analysis.py','F2_CALCULOS_CONDICIONAIS.json','F2_FONTES_SHA256.json','MANIFESTO_F2.json','PLANO_F2_ANTES_DOS_CALCULOS.md']:
    record(BASE/name)
# Pin only canonical program and the two motors actually needed; do not mix a mutable Atlas update with source alteration.
excerpt_checks=[]
for item in spec['local']:
    if Path(item['path']).name not in ['um.py','motor.py','fundo_gpu.py']:continue
    raw=record(Path(item['path']),item['sha256'],'primary static reference')
    if Path(item['path']).name=='um.py':
        m=re.search(rb'^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)',raw,re.M)
        alpha=float(m.group(1))
    ex_path=BASE/item['excerpts_file']
    ex=json.loads(record(ex_path).decode('utf-8'))
    lines=raw.decode('utf-8').splitlines()
    for e in ex['excerpts']:
        excerpt_checks.append({'path':item['path'],'first_line':e['first_line'],'last_line':e['last_line'],'equal_to_source':e['text']=='\n'.join(lines[e['first_line']-1:e['last_line']])})
abstracts=[]
for item in spec['primary_web']:
    p=BASE/item['path']
    raw=record(p,item['sha256'],'archived primary web; no refetch')
    m=re.search(r'<meta name="citation_abstract" content="([^"]*)"',raw.decode('utf-8'))
    abstracts.append({'path':str(p),'abstract':html.unescape(m.group(1)) if m else None})
beta=alpha*math.sqrt(math.e)
def integrand(x,om,b,weighted):
    e=math.sqrt(1+om*((1+x)**3-1))
    return (math.exp((2*b/3)*math.log(e)) if weighted else 1)/e
def adaptive(f,a,b,eps=1e-12):
    mid=(a+b)/2
    fa,fm,fb=f(a),f(mid),f(b)
    s=(b-a)*(fa+4*fm+fb)/6
    def sub(a,b,fa,fm,fb,s,eps,depth):
        m=(a+b)/2;l=(a+m)/2;r=(m+b)/2
        fl,fr=f(l),f(r)
        sl=(m-a)*(fa+4*fl+fm)/6;sr=(b-m)*(fm+4*fr+fb)/6
        if depth<=0 or abs(sl+sr-s)<=15*eps:return sl+sr+(sl+sr-s)/15
        return sub(a,m,fa,fl,fm,sl,eps/2,depth-1)+sub(m,b,fm,fr,fb,sr,eps/2,depth-1)
    return sub(a,b,fa,fm,fb,s,eps,22)
delta=[]
for row in result['distance_rows']:
    om,z=row['om'],row['z']
    q=adaptive(lambda x:integrand(x,om,beta,True),0,z)/adaptive(lambda x:integrand(x,om,beta,False),0,z)
    endpoint=(1+om*((1+z)**3-1))**(beta/3)
    delta.append({'z':z,'om':om,'Q_abs_difference':abs(q-1-row['distance_ratio_Q_minus_1']),'k_abs_difference':abs(endpoint-1-row['endpoint_k_minus_1']),'magnitude_abs_difference':abs(5*math.log10(q)-row['magnitude_shift_vs_shadow'])})
mass=beta/math.sqrt(2)
tplanck=math.sqrt((6.62607015e-34/(2*math.pi))*6.67430e-11/299792458**5)
gamma=beta*tplanck*(2*math.pi*100)**2/2
review={
 'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Review delivered F2 only; excludes poder_forma and later forecasts; no canonical/author script execution, external call, fit or verdict.',
 'sources':records,'excerpt_checks':excerpt_checks,
 'arithmetic_checks':{'beta_match':beta==result['beta_runtime'],'Q_max_abs_difference':max(r['Q_abs_difference'] for r in delta),'endpoint_max_abs_difference':max(r['k_abs_difference'] for r in delta),'magnitude_max_abs_difference':max(r['magnitude_abs_difference'] for r in delta),'rows_checked':len(delta),'m2_abs_diff_eV':abs(mass-result['neutrino']['m2_eV']),'dm21_abs_diff_eV2':abs(mass*mass-result['neutrino']['dm21_eV2_given_m1_zero']),'S8_ratio_abs_diff':abs(math.sqrt(1+beta)-1-result['S8']['algebraic_ratio_minus_1_at_fixed_sigma8']),'clock_abs_diff_per_s':abs(gamma-result['clock']['Gamma_at_100_Hz_per_s_identity_only'])},
 'findings':[{'id':'F2-REV-01','severity':'P2_before_operational_lens_use','source':'NOTA_DERIVACOES_F2.md','issue':'f_phi direction not defined as a ratio. Under f_phi=Delta_phi_fit/Delta_phi_true, D_fit/D_bg=f_t*(f_l*f_s/f_ls)/f_phi, not multiplication. Product is valid if f_phi is explicitly defined inversely (true/fit).','impact':'Ambiguous inverse scaling for lens inference if f_phi differs from 1; illustrated f_phi=1 examples and JSON proxies unaffected.','remedy':'Define physical vs fitted potential factors by ratios and derive from Delta_t_obs and fitted equation before quantitative use.'}],
 'statutes':'Conditional derivations supported in examined scope; maps of duality/temperature/lensing/growth remain OPEN; angle sin45 POSTULATE,1eV NORM INPUT,m1=0 and NO conditions; sum not reopened.',
 'directions':{'S8_fixed_sigma8':'positive for beta>0, not a derived suppression of shear','m2':'m2>0 fixed; at fixed m2, dm21=m2^2-m1^2 decreases as m1 grows; adding m1 cannot raise dm21 toward a larger observation.'},
 'canonical_imports_executed':False,'author_script_executed':False,'observational_rite_repeated':False,'new_observational_verdict':False}
assert all(e['equal_to_source'] for e in excerpt_checks)
assert all(r.get('matches_delivery_hash',True) for r in records)
assert review['arithmetic_checks']['Q_max_abs_difference']<1e-10
atomic(OUT/'REVISAO_ADVERSARIAL_F2_FONTES.json',json.dumps(review,ensure_ascii=False,indent=2)+'\n')
atomic(OUT/'REVISAO_ADVERSARIAL_F2_ABSTRACTS.json',json.dumps(abstracts,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'sources':len(records),'excerpt_checks':len(excerpt_checks),'arithmetic_checks':review['arithmetic_checks'],'findings':review['findings']},ensure_ascii=False,indent=2))
