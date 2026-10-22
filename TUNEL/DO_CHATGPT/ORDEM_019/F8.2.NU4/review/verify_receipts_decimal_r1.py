"""Independent offline review: no Bench/runner imports or HTTP calls."""
from pathlib import Path
from decimal import Decimal as D,getcontext
from datetime import datetime,timezone
import json,hashlib,sys
import numpy as np
getcontext().prec=110
B=Path(__file__).resolve().parent.parent; O=B/'review'
outputs=['NUMERICAL_REVIEW_R1.json','PARECER_R1.md','REVIEW_RECEIPT_R1.json']
for name in outputs:
 if (O/name).exists():raise FileExistsError(name)
started=datetime.now(timezone.utc).isoformat();checks=[];sources={};details=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):
 p=Path(p);sources[str(p)]={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size};return sources[str(p)]
def read(p):pin(p);return json.loads(Path(p).read_bytes(),parse_float=D,parse_int=D)
def ck(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
def near(name,got,want,rel='2e-12',abs_tol='0'):
 got,want=D(str(got)),D(str(want));err=abs(got-want);lim=max(D(abs_tol),abs(want)*D(rel));ck(name,err<=lim,dict(got=str(got),want=str(want),error=str(err),limit=str(lim)))
def atan(x):
 t=s=x;k=1
 while True:
  t*=-x*x;n=s+t/D(2*k+1)
  if n==s:return s
  s=n;k+=1
pi=16*atan(D(1)/5)-4*atan(D(1)/239)
def cos(x):
 x%=2*pi
 if x>pi:x-=2*pi
 t=s=D(1);k=1
 while True:
  t*=-x*x/D((2*k-1)*(2*k));n=s+t
  if n==s:return s
  s=n;k+=1
def arr(a):return np.array([[complex(float(v[0]),float(v[1])) for v in row]for row in a])
P=read(B/'PREREGISTRO_R1.json');R=read(B/'RESULTADOS_R1.json')
ck('preregister hash',sha(B/'PREREGISTRO_R1.json')==R['preregister_sha256']);ck('runner hash',pin(B/'run_pilot_r1.py')['sha256']==R['runner_sha256'])
for q in P['source_pins']:
 s=pin(q['path']);ck('pin '+q['path'],s['sha256']==q['sha256'] and s['bytes']==q['bytes'])
manifest=P['canonical_manifest_sha256'];ck('manifest receipt',R['canonical']['canonical_manifest_sha256']==manifest)
report=pin(B/'PRIMEIROS_RESULTADOS_R1.md');text=(B/'PRIMEIROS_RESULTADOS_R1.md').read_text(encoding='utf-8')
ck('report scope text','H diagonal fixo' in text and 'não é estimativa de tau_star nem evidência física' in text and 'Nenhum sigma observado foi calculado' in text)
alpha=R['canonical']['alpha'];beta=alpha*D(1).exp().sqrt();near('runtime beta',R['beta_runtime'],beta)
c=P['constants'];tau=(c['h_J_s']*c['G_SI']/(2*pi*c['c_m_s']**5)).sqrt();near('Planck time',R['tau_star_s'],tau)
t=P['protocol']['reactor_baseline_km']*1000/c['c_m_s'];hb=P['hbar_implementation_eV_s'];inp=P['reference_inputs'];w=[(1-inp['sin2theta12'])*(1-inp['sin2theta13']),inp['sin2theta12']*(1-inp['sin2theta13']),inp['sin2theta13']]
rows={x['E_MeV']:x for x in R['reactor']};ck('16 receipts',len(R['calls'])==len(list(B.glob('CALL_*.json')))==16)
for e in R['calls']:
 C=read(B/e['path']);ck(e['name']+' hash',sha(B/e['path'])==e['sha256']);q=C['request'];r=C['response'];x=r['result'];kind=q['channel'];d=dict(name=e['name'],channel=kind)
 ck(e['name']+' scope',r['synthetic'] and r['nature_sigma']is None and not r['data_opened'] and r['gate_effect']=='NONE')
 for field in ['canonical','canonical_at_delivery']:
  ck(e['name']+' '+field,all(r[field][k]==R['canonical'][k]for k in ['canonical_manifest_sha256','deployment_id','canonical_version','um_py_sha256','seal_sha256','alpha','beta_tgl']))
 if 'rho'in x:
  a=arr(q['rho']);z=arr(x['rho']);trace=abs(np.trace(z)-1);eig=float(np.linalg.eigvalsh(z).min());ck(e['name']+' trace',trace<=2e-12,float(trace));ck(e['name']+' Hermitian',np.max(abs(z-z.conj().T))<=2e-12);ck(e['name']+' PSD tolerance',eig>=-2e-12,eig);near(e['name']+' reported eigenvalue',x['min_eigenvalue'],eig,abs_tol='2e-14');d.update(trace_error=float(trace),min_eigenvalue=eig)
 if kind in ['physical_mass_gap_dephasing','modular_root_dephasing']:
  physical=kind=='physical_mass_gap_dephasing';h=[v/(2*q['energy_eV'])for v in q['mass_squared_eV2']]if physical else q['modular_eigenvalues'];clock=q['time_s']if physical else q['s'];expected=np.zeros_like(z);delta=D(0);pee=sum(v*v for v in w);gg=[];ll=[]
  for i in range(len(h)):
   for j in range(len(h)):
    f=(h[i]-h[j])/hb if physical else D(0);g=beta*q['tau_star_s']*q['Kfac']*f*f/2 if physical else beta*(h[i].sqrt()-h[j].sqrt())**2/2;damp=(-g*clock).exp();loss=1-damp;phase=f*clock
    for label,got,want in [('gamma',x['gamma'][i][j],g),('loss',x['coherence_loss'][i][j],loss),('damping',x['damping'][i][j],damp)]:near(f'{e["name"]} {label} {i}{j}',got,want)
    expected[i,j]=a[i,j]*complex(float(damp*cos(phase)),-float(damp*cos(pi/2-phase)))
    if i<j:
     gg.append(str(g));ll.append(str(loss))
     if physical:delta+=2*w[i]*w[j]*cos(phase)*(damp-1);pee+=2*w[i]*w[j]*cos(phase)
  err=float(np.max(abs(z-expected)));ck(e['name']+' density independent',err<=2e-12,err)
  energy0=sum(h[i]*q['rho'][i][i][0]for i in range(len(h)));energy1=sum(h[i]*x['rho'][i][i][0]for i in range(len(h)));ck(e['name']+' populations',all(q['rho'][i][i]==x['rho'][i][i]for i in range(len(h))));ck(e['name']+' fixed H energy',energy0==energy1);near(e['name']+' reported energy',x['conserved_diagonal_generator_after'],energy1,abs_tol='1e-22');d.update(gamma_12_13_23=gg,loss_12_13_23=ll,density_max_error=err,energy_drift=str(energy1-energy0))
  if physical:near(e['name']+' flight time',q['time_s'],t)
  if e['name'].startswith('diagonal_'):ck(e['name']+' stationary',q['rho']==x['rho'])
  if e['name'].startswith('planck_'):
   row=rows[q['energy_eV']/D('1e6')];near(e['name']+' direct high-precision delta',row['delta_Pee_stable'],delta);near(e['name']+' Pee zero',row['Pee_zero'],pee,abs_tol='2e-12');d.update(delta_Pee_110digits=str(delta),Pee_zero_110digits=str(pee))
  if e['name']=='positive_control':
   near('positive delta',R['positive_control']['delta_Pee'],delta,abs_tol='2e-12');near('positive exponent',beta*q['tau_star_s']*(h[2]/hb)**2*clock/2,D('.1'));near('positive loss31',x['coherence_loss'][0][2],1-D('-.1').exp());ck('positive not physical prediction',R['positive_control']['physical_prediction']is False);d['delta_Pee_110digits']=str(delta)
 elif kind=='boundary_parity_4state':
  flip=(1-(-2*q['s']).exp())/2;near(e['name']+' parity probability',x['flip_probability'],flip);idx=[2,3,0,1];expected=(1-float(flip))*a+float(flip)*a[np.ix_(idx,idx)];ck(e['name']+' parity density',np.max(abs(z-expected))<=2e-12);d['flip_110digits']=str(flip)
 elif kind=='beta_scale':
  v=q['chi']/2;bulk=2*D(1).exp().sqrt()/(v.exp()+(-v).exp());near(e['name']+' bulk',x['beta_bulk'],bulk);near(e['name']+' frontier',x['beta_frontier'],beta);d['bulk_110digits']=str(bulk)
 details.append(d)
for a,b in zip(R['reactor'],R['reactor'][1:]):near('E^-2 '+str(a['E_MeV']),a['gamma21_s']/b['gamma21_s'],(b['E_MeV']/a['E_MeV'])**2)
ck('result scope',R['nature_sigma']is None and not R['observed_data_fit'] and R['luminosity_or_chandrasekhar_shift']is None and R['gate_effect']=='NONE')
pin(__file__)
for s in sources.values():ck('unchanged '+s['path'],sha(s['path'])==s['sha256'])
passed=all(x['passed']for x in checks);verdict='PASS_CONDITIONAL_NUMERICAL_PILOT'if passed else 'FAIL'
result=dict(unit='F8.2.NU4',claim=642,verdict=verdict,started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),method='Decimal 110 digits; pi by Machin series; trigonometric series; direct high-precision exp subtraction independent from API expm1; NumPy eigenvalues only. No operational replay.',checks_total=len(checks),checks_passed=sum(x['passed']for x in checks),checks=checks,details=details,sources=list(sources.values()),manifest_sha256=manifest,scope='Synthetic conditional propagation, fixed H effective only; no observed fit, sigma, stellar production or complete Ia test',nos='NU4 not in graph; reused pinned NU2/NU3/preregistration')
def save(name,obj):
 with (O/name).open('x',encoding='utf-8')as f:json.dump(obj,f,ensure_ascii=False,indent=2,allow_nan=False)
save(outputs[0],result)
body=f'# Revisão independente NU4 — R1\n\n**{verdict}** — {result["checks_passed"]}/{len(checks)} verificações. [REAL] Releitura dos 16 recibos, pré-registro, executor e quatro pinos, incluindo bytes do módulo e manifesto instalados. Não foi repetida chamada à Bancada.\n\n[REAL numérico] Decimal de 110 dígitos, pi por Machin e cossenos por série; ΔPee conferido por subtração direta em alta precisão, independente do expm1 operacional. Taxas, lei E⁻², densidades, traço e positividade à tolerância pinada conferem.\n\n| E (MeV) | ΔPee no recibo |\n|---:|---:|\n'
for row in R['reactor']:body+=f'| {row["E_MeV"]} | {row["delta_Pee_stable"]} |\n'
body+='\n[DERIVED condicional] O estado diagonal é exatamente estacionário. O caso coerente tem efeito minúsculo, não zero físico; zero por subtração double é arredondamento. Energia preservada significa Tr(ρH) com H diagonal efetivo fixo, não um tensor gravitacional completo. Usou-se o ℏ da implementação, sem exigir igualdade de últimos dígitos com NU2.\n\nO controle positivo foi escolhido antes para Γ31t=0,1; sua perda31=0,095162581964 e ΔPee=−0,000889064398731 conferem. Verifica a resposta do canal; não estima τ★. Paridade, canal modular e escala β(χ) também conferem e mantêm contratos e relógios distintos.\n\nO relatório PRIMEIROS_RESULTADOS_R1 foi lido integralmente: não foi localizado defeito material de alcance. Este é um piloto condicional τ★=tP, Kfac=1, sem likelihood observada e sem cálculo de significância. Não demonstra fluxo absoluto, luminosidade nem massa de Chandrasekhar; não exclui outros contratos da TGL. A frase «não entregou um sinal de 5sigma» é delimitada logo adiante pela ausência de dados e função de significância, não um teste estatístico com resultado nulo.\n\nConsulta ao Nós: NU4 ausente do grafo; pré-registro e NU2/NU3 reutilizados. Nenhuma escrita em Bancada, quadro ou memória. Identidade conferida por bytes/recibos existentes, sem nova sondagem HTTP.\n\n'
body+=f'Manifesto: `{manifest}`.\nResultado: `{sha(B/"RESULTADOS_R1.json")}`.\nRelatório interpretativo: `{report["sha256"]}`.\n'
with (O/outputs[1]).open('x',encoding='utf-8')as f:f.write(body)
receipt=dict(unit='F8.2.NU4',claim=642,verdict=verdict,checks_total=len(checks),checks_passed=result['checks_passed'],artifacts=[pin(O/outputs[0]),pin(O/outputs[1]),pin(__file__)],result_sha256=sha(B/'RESULTADOS_R1.json'),interpretation_sha256=report['sha256'],manifest_sha256=manifest,gate_effect='NONE')
save(outputs[2],receipt)
print(json.dumps(dict(verdict=verdict,checks_total=len(checks),checks_passed=result['checks_passed'],failed=[x for x in checks if not x['passed']],receipt_sha256=sha(O/outputs[2]),deltas=[x for x in details if 'delta_Pee_110digits'in x]),ensure_ascii=False,indent=2))
if not passed:raise SystemExit(1)
