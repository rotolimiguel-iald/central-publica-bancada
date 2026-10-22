"""Independent algebraic/Kronecker reproduction; writes only this review directory."""
from pathlib import Path
import ast, datetime, hashlib, json, math, re, sys, time
import numpy as np

B=Path(__file__).resolve().parent
P=B.parent
def pin(p):
    p=Path(p);raw=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
def put(p,value):
    raw=value.encode('utf-8')
    with p.open('xb') as f:f.write(raw)
    assert p.read_bytes()==raw
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
start=now();tick=time.perf_counter()
pre=json.loads((P/'PREREGISTRO_OH_SECTOR_R2.json').read_text(encoding='utf-8'))
freeze=json.loads((P/'FREEZE_OH_SECTOR_R2.json').read_text(encoding='utf-8'))
original=json.loads((P/'RESULTADO_OH_SECTOR_R2.json').read_text(encoding='utf-8'))
oldpre=json.loads((P/'PREREGISTRO_OH_SECTOR_R1.json').read_text(encoding='utf-8'))
assert {k:v for k,v in pre.items() if k not in {'created_utc','runner'}}=={k:v for k,v in oldpre.items() if k not in {'created_utc','runner'}}
assert datetime.datetime.fromisoformat(pre['created_utc'])<datetime.datetime.fromisoformat(freeze['created_utc'])<datetime.datetime.fromisoformat(original['start_utc'])
pins=[freeze['preregistration'],freeze['runner'],original['freeze'],original['runner'],*pre['source_pins'].values()]
for x in pins:assert pin(x['path'])==x
assert original['source_pins_after']==pre['source_pins']
assert original['passed'] and original['checks_total']==original['checks_passed']==30
assert all(x['passed'] for x in original['checks'])
tol=pre['numeric_policy']['relative_tolerance'];negative=pre['numeric_policy']['negative_min_relative_residual']
assert tol==1e-12 and negative==0.1

# Read constants as data, never import production code or execute the author's runner.
tree=ast.parse(Path(pre['source_pins']['alpha_source']['path']).read_text(encoding='utf-8'))
const={n.targets[0].id:ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in {'ALPHA_FINE_CODATA_2018','_SEALED_ALPHA_CODATA_2018'}}
alpha=const['ALPHA_FINE_CODATA_2018'];assert not isinstance(alpha,bool) and math.isfinite(alpha) and alpha==const['_SEALED_ALPHA_CODATA_2018']
beta=alpha*math.sqrt(math.e)
tex=Path(pre['source_pins']['superconductor']['path']).read_text(encoding='utf-8')
block=tex.split(r'\label{eq:hamiltonian}',1)[1].split(r'\subsubsection',1)[0]
parts=re.findall(r'([0-9]+(?:\.[0-9]+)*)\{,\}([0-9]+)\$~MHz',block)
assert len(parts)==1
MHz=float(parts[0][0].replace('.','')+'.'+parts[0][1]);omega=2*math.pi*MHz*10**6
hbar=6.62607015e-34/(2*math.pi);energy=hbar*omega;V0=energy/2
gamma=beta*energy/(2*hbar);rate=gamma/2
physical=Path(pre['source_pins']['physical_parameters']['path']).read_text(encoding='utf-8')
assert 'hbar_J_s = 6.62607015e-34 / (2.0 * math.pi)' in physical
assert 'gamma=beta/(2*hbar)*(sqrt(Eref+V0)-sqrt(Eref-V0))**2' in physical

# Column-major vec: vec(A X B)=(B^T tensor A)vec(X).
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.]).astype(complex)
def dissipator(j):
    q=j.conj().T@j
    return np.kron(j.conj(),j)-(np.kron(I,q)+np.kron(q.T,I))/2
def commutator(h):return -1j*(np.kron(I,h)-np.kron(h.T,I))/hbar
H=np.diag([0.,energy]);J=np.diag([0.,math.sqrt(beta*energy/hbar)])
root=dissipator(J);other=rate*dissipator(Z);ham=commutator(H);L=root+ham
E=np.diag([1.,0.,0.,1.]);checks=[]
def equal(name,a,b,scale):
    err=float(np.linalg.norm(a-b)/scale)
    checks.append({'name':name,'relative_residual':err,'passed':bool(math.isfinite(err) and err<=tol)})
def different(name,a,b,scale):
    err=float(np.linalg.norm(a-b)/scale)
    checks.append({'name':name,'relative_residual':err,'passed':bool(math.isfinite(err) and err>=negative)})
equal('root_vs_sigma_z_dissipator',root,other,gamma)
equal('complete_Liouvillian',L,ham+other,omega)
equal('root_is_gamma_pinch_minus_id',root,gamma*(E-np.eye(4)),gamma)
equal('coherence_eigenvalue',L[:,2],np.array([0,0,-gamma+1j*omega,0]),omega)
equal('reading_preserved_generator',E@L,np.zeros((4,4)),omega)
C=(I+1j*X)/math.sqrt(2);Q=np.kron(C.conj(),C)
equal('basis_unitary',C@C.conj().T,I,1)
equal('Hg_exact_R9',C@(H-V0*I)@C.conj().T,-V0*Y,V0)
equal('joint_operator_covariance',Q@L@Q.conj().T,commutator(C@H@C.conj().T)+dissipator(C@J@C.conj().T),omega)
for u in pre['numeric_policy']['channel_scaled_times']:
    t=u/gamma;q=math.exp(-u);U=np.diag([1,np.exp(-1j*omega*t)])
    A=math.sqrt((1+q)/2)*U;Bop=math.sqrt((1-q)/2)*U@Z
    channel=np.kron(A.conj(),A)+np.kron(Bop.conj(),Bop)
    analytical=np.diag([1,np.exp(-u-1j*omega*t),np.exp(-u+1j*omega*t),1])
    equal(f'channel_generator_at_{u}',channel,analytical,1)
    equal(f'Kraus_trace_preserving_at_{u}',A.conj().T@A+Bop.conj().T@Bop,I,1)
    equal(f'reading_at_{u}',E@channel,E,1)
    a=A.reshape(4,order='F');b=Bop.reshape(4,order='F')
    choi=np.outer(a,a.conj())+np.outer(b,b.conj())
    eig=float(np.linalg.eigvalsh(choi).min())
    checks.append({'name':f'Choi_positive_at_{u}','min_eigenvalue':eig,'passed':bool(math.isfinite(eig) and eig>=-tol)})
old=json.loads(Path(pre['source_pins']['old_device_spec']['path']).read_text(encoding='utf-8'))['model']
old_gamma=beta*old['omega_OH']/2
different('old_dimensionless_rate_control',dissipator(np.diag([0.,math.sqrt(beta*old['omega_OH'])])),old['gamma_dephasing']*dissipator(Z),old_gamma)
Hr=V0*(I+X);Jr=math.sqrt(beta*omega)*(I+X)/2
different('Rabi_sigma_z_is_not_root_H',dissipator(Jr),other,gamma)
different('Rabi_noncommuting_jump',Hr@Z-Z@Hr,np.zeros((2,2)),V0)
Hs=H+energy*I;Js=np.diag(np.sqrt(beta*np.diag(Hs)/hbar))
equal('shift_keeps_commutator',commutator(Hs),ham,omega)
different('shift_changes_root_dissipation',dissipator(Js),root,gamma)
ev=np.linalg.eigvalsh(H-V0*I)
checks.append({'name':'centered_Hg_not_positive','eigenvalues_J':ev.tolist(),'passed':bool(np.all(np.isfinite(ev)) and ev[0]<0)})
assert len(checks)==30 and all(c['passed'] for c in checks)
assert [x['name'] for x in checks]==[x['name'] for x in original['checks']]
for name,value in {'alpha':alpha,'beta_runtime':beta,'frequency_source_MHz':MHz,'omega_OH_s_inv':omega,'hbar_J_s':hbar,'V0_J':V0,'Eref_J':V0,'gamma_root_s_inv':gamma,'gamma_phi_matching_s_inv':rate}.items():
    assert math.isclose(value,original['parameters'][name],rel_tol=tol,abs_tol=0)
# Independent exact expressions for the three nontrivial negative-control residuals.
lookup={x['name']:x for x in checks}
for name,value in {'Rabi_sigma_z_is_not_root_H':math.sqrt(2),'Rabi_noncommuting_jump':2*math.sqrt(2),'shift_changes_root_dissipation':4-2*math.sqrt(2)}.items():
    assert math.isclose(lookup[name]['relative_residual'],value,rel_tol=tol)
for item in pins:assert pin(item['path'])==item
result={'unit':'F1.FECHO_20261015','claim_event':845,'reviewer':'/root/atrator_skeptic','verdict':'PASSA_NO_MODELO_FINITO_CONFIGURADO','start_utc':start,'end_utc':now(),'seconds':time.perf_counter()-tick,'command':[sys.executable,'-B','-X','utf8',str(Path(__file__).resolve())],'script':pin(__file__),'inputs':[pin(P/n) for n in ['RESULTADO_OH_SECTOR_R2.json','PREREGISTRO_OH_SECTOR_R2.json','FREEZE_OH_SECTOR_R2.json','ATTEMPT_OH_R1_REFUSAL.json','verify_oh_sector_r1.py','verify_oh_sector_r2.py']],'source_pins_unchanged':pre['source_pins'],'parameters':{'alpha':alpha,'beta_runtime':beta,'frequency_MHz':MHz,'omega_s_inv':omega,'gamma_root_s_inv':gamma,'gamma_phi_input_s_inv':rate},'checks':checks,'checks_total':30,'checks_passed':30,'preregistration_policy_unchanged_after_parser_fix':True,'method':'Independent Kronecker superoperators and explicit analytical eigenvalues/channel; no import/execution of production or original runner. Original check names/thresholds retained.','material_findings':[],'limits':['gamma_phi=beta*omega/4 is configured INPUT required for equality; this is not a measured dephasing rate or an independently derived full-device prediction.','The effective OH excitation Hamiltonian is positive with its stated energy zero. Center removal is valid for its commutator only, not for its square-root dissipator.','The prior device rate in its dimensionless clock fails matching, Rabi noncommuting jump fails matching, and shifting energy zero changes root dissipation as required.','The R1 refusal preceded matrix construction; R2 changed the source extraction window and output names, not numeric criteria or parameters.','This reproduces finite-model identities, not hardware, observed data, thermal calibration, kappa or nature confirmation. No production, memory or gate modified.']}
put(B/'REVISAO_OH_R1.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
lines=['# Revisão independente do setor OH','','[REAL] PASSA no modelo finito configurado: 30/30 verificações reproduzidas. Nenhum achado material.','',f'β calculado em runtime: {beta!r}; ω = {omega!r} s⁻¹; γ_raiz = {gamma!r} s⁻¹; γ_φ = {rate!r} s⁻¹.', '', 'A reprodução usa superoperadores por produtos de Kronecker, autovalores e canal analíticos. As tolerâncias do pré-registro foram preservadas (1e-12 e controles negativos ≥0,1). Os pinos e a cronologia local do congelamento conferem; a correção do parser R1→R2 não alterou a política numérica.','']+['- '+s for s in result['limits']]+['','Recibo, hashes e valores: REVISAO_OH_R1.json.']
put(B/'REVISAO_OH_R1.md','\n'.join(lines)+'\n')
print(json.dumps({'verdict':result['verdict'],'json':pin(B/'REVISAO_OH_R1.json'),'md':pin(B/'REVISAO_OH_R1.md')},ensure_ascii=False))
