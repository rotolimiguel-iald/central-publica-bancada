"""Preregister and verify the configured OH restriction; no hardware measurement."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import argparse
import hashlib
import json
import math
import re
import sys
import time

HERE = Path(__file__).resolve().parent
ORD = HERE.parents[1]
DEVICE = ORD / 'F1.REDE' / 'finite_device'
PHYS = ORD / 'F1.TEMPO.V394' / 'physical_contract'

def now(): return datetime.now(timezone.utc).isoformat()
def pin(path):
    p = Path(path).resolve(); b = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
def save(name, data):
    p = HERE / name
    if p.exists(): raise FileExistsError(p)
    b = (json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode()
    tmp = p.with_suffix(p.suffix+'.tmp')
    with tmp.open('xb') as f: f.write(b)
    if tmp.stat().st_size != len(b): raise RuntimeError('Short write')
    tmp.rename(p)
    return pin(p)

def preregister():
    previous = json.loads((DEVICE/'PREREGISTRO_DEVICE_R1.json').read_text(encoding='utf-8'))
    sources = {k: pin(previous['source_pins'][k]['path']) for k in ['superconductor', 'alpha_source']}
    for k in sources:
        if sources[k]['sha256'] != previous['source_pins'][k]['sha256']:
            raise RuntimeError('Original source changed: '+k)
    sources['old_device_spec'] = pin(DEVICE/'PREREGISTRO_DEVICE_R1.json')
    sources['old_device_runner'] = pin(DEVICE/'run_finite_device.py')
    sources['physical_parameters'] = pin(PHYS/'physical_parameters.py')
    pre = {
        'unit': 'F1.FECHO_20261015', 'claim_event': 845, 'created_utc': now(),
        'status': 'INPUT test fixed before execution; DERIVED configured finite model, not physical measurement',
        'source_pins': sources, 'runner': pin(__file__),
        'units': {'primary': 'SI: H and V0,Eref in J, omega,gamma in s^-1, t in s', 'old_rate_control': 'Original dimensionless finite_device clock, omega_OH and gamma_dephasing retained together; never relabeled as SI'},
        'parameters': {'alpha': 'AST ALPHA_FINE_CODATA_2018, checked against _SEALED_ALPHA_CODATA_2018; beta=alpha*sqrt(e) at runtime', 'omega_OH': 'Parse source equation line367, Portuguese MHz formatting; omega=2pi*f_MHz*1e6', 'hbar': '6.62607015e-34/(2pi), exact SI Planck definition; same constant as pinned physical_parameters.py', 'V0_and_Eref': 'hbar*omega_OH/2', 'gamma_phi': 'beta*omega_OH/4'},
        'restrictions': ['g_JC=Omega_Rabi=gamma_Lambda=gamma_OH=0', 'cavity vacuum spectator sector', 'bare effective OH Hamiltonian H=hbar*omega_OH*|e><e|', 'only sigma_z conventional dephasing remains', 'The bare excitation zero belongs to this effective Hamiltonian, not a proof of absolute energy in nature'],
        'tests': ['Compare complete 4x4 Liouvillians and separate dissipators for root(H) and gamma_phi D[Z]', 'Verify unitary basis map into Hg=-V0 sigma_y and covariance of both operators', 'Verify coherent eigenvalue, reading preservation and CPTP channel identities at gamma*t in [0,0.1,1,5]', 'Negative: old finite_device rate with its old omega must mismatch', 'Negative: Rabi H proportional sigma_x with sigma_z jump must mismatch root(H)', 'Negative: H+cI leaves commutator unchanged but changes root rate; centered indefinite Hg cannot be used as positive H'],
        'numeric_policy': {'relative_tolerance': 1e-12, 'negative_min_relative_residual': 0.1, 'channel_scaled_times': [0.0,0.1,1.0,5.0], 'no_fit_or_parameter_search': True},
        'forbidden_claims': ['hardware measurement', 'full nonunital holographic J equals root dephasing', 'gamma_phi independently measured or predicted by source', 'universal energy zero or kappa clock calibration', 'nature confirmation or gate movement'],
        'new_observed_data': False
    }
    p = save('PREREGISTRO_OH_SECTOR_R1.json', pre)
    print(json.dumps(save('FREEZE_OH_SECTOR_R1.json', {'created_utc': now(), 'preregistration': p, 'runner': pin(__file__)})))

def run():
    import numpy as np
    start, timer = now(), time.perf_counter()
    freeze = json.loads((HERE/'FREEZE_OH_SECTOR_R1.json').read_text(encoding='utf-8'))
    for rec in [freeze['preregistration'], freeze['runner']]:
        if pin(rec['path'])['sha256'] != rec['sha256']: raise RuntimeError('Freeze pin mismatch')
    if datetime.fromisoformat(freeze['created_utc']) >= datetime.fromisoformat(start): raise RuntimeError('Late freeze')
    pre = json.loads(Path(freeze['preregistration']['path']).read_text(encoding='utf-8'))
    for rec in pre['source_pins'].values():
        if pin(rec['path'])['sha256'] != rec['sha256']: raise RuntimeError('Source pin mismatch')
    tree = ast.parse(Path(pre['source_pins']['alpha_source']['path']).read_text(encoding='utf-8'))
    alpha_names = {'ALPHA_FINE_CODATA_2018', '_SEALED_ALPHA_CODATA_2018'}
    const = {n.targets[0].id:ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in alpha_names}
    alpha = const['ALPHA_FINE_CODATA_2018']
    if isinstance(alpha,bool) or not math.isfinite(alpha) or alpha!=const['_SEALED_ALPHA_CODATA_2018']: raise ValueError('Bad alpha')
    beta = alpha*math.sqrt(math.e)
    text = Path(pre['source_pins']['superconductor']['path']).read_text(encoding='utf-8')
    matches = re.findall(r'= 2\\pi \\times ([0-9.]+)\{,\}([0-9]+)\$~MHz', text)
    if len(matches)!=1: raise ValueError('Frequency source ambiguous')
    f_MHz = float(matches[0][0].replace('.','')+'.'+matches[0][1]); omega=2*math.pi*f_MHz*1e6
    hbar=6.62607015e-34/(2*math.pi); V0=hbar*omega/2; Eref=V0; gamma=beta*omega/2; rate=gamma/2
    I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1.,-1.]).astype(complex)
    H=np.diag([0,hbar*omega]).astype(complex); root_jump=np.diag([0,math.sqrt(beta*omega)]).astype(complex)
    units=[np.outer(I[:,i],I[:,j]) for j in range(2) for i in range(2)]
    def op(fun): return np.column_stack([fun(a).reshape(4,order='F') for a in units])
    def D(j,a): return j@a@j.conj().T-(j.conj().T@j@a+a@j.conj().T@j)/2
    def Hcomm(h,a): return -1j*(h@a-a@h)/hbar
    def E(a): return np.diag(np.diag(a))
    dissip=op(lambda a:D(root_jump,a)); dz=op(lambda a:rate*D(Z,a)); ham=op(lambda a:Hcomm(H,a))
    Lroot=ham+dissip; Lz=ham+dz; checks=[]; tol=pre['numeric_policy']['relative_tolerance']; neg=pre['numeric_policy']['negative_min_relative_residual']
    def equal(name,a,b,scale):
        err=float(np.linalg.norm(a-b))/float(scale); checks.append({'name':name,'relative_residual':err,'threshold':tol,'passed':bool(math.isfinite(err) and err<=tol)})
    def different(name,a,b,scale):
        err=float(np.linalg.norm(a-b))/float(scale); checks.append({'name':name,'relative_residual':err,'minimum':neg,'passed':bool(math.isfinite(err) and err>=neg)})
    equal('root_vs_sigma_z_dissipator',dissip,dz,gamma)
    equal('complete_Liouvillian',Lroot,Lz,omega)
    equal('root_is_gamma_pinch_minus_id',dissip,op(lambda a:gamma*(E(a)-a)),gamma)
    equal('coherence_eigenvalue',Lroot[:,2],np.array([0,0,-gamma+1j*omega,0]),omega)
    equal('reading_preserved_generator',op(E)@Lroot,np.zeros((4,4)),omega)
    C=(I+1j*X)/math.sqrt(2)
    equal('basis_unitary',C@C.conj().T,I,1)
    equal('Hg_exact_R9',C@(H-Eref*I)@C.conj().T,-V0*Y,V0)
    equal('joint_operator_covariance',op(lambda a:C@(Hcomm(H,C.conj().T@a@C)+D(root_jump,C.conj().T@a@C))@C.conj().T),op(lambda a:Hcomm(C@H@C.conj().T,a)+D(C@root_jump@C.conj().T,a)),omega)
    for u in pre['numeric_policy']['channel_scaled_times']:
        t=u/gamma; U=np.diag([1,np.exp(-1j*omega*t)]); q=math.exp(-u)
        A=math.sqrt((1+q)/2)*U; B=math.sqrt((1-q)/2)*U@Z
        channel=op(lambda a:A@a@A.conj().T+B@a@B.conj().T)
        exact=np.diag(np.exp(np.diag(Lroot)*t))
        equal(f'channel_generator_at_{u}',channel,exact,1)
        equal(f'Kraus_trace_preserving_at_{u}',A.conj().T@A+B.conj().T@B,I,1)
        equal(f'reading_at_{u}',op(E)@channel,op(E),1)
        choi=sum(np.kron(a,A@a@A.conj().T+B@a@B.conj().T) for a in units)
        eig=float(np.linalg.eigvalsh(choi).min());checks.append({'name':f'Choi_positive_at_{u}','min_eigenvalue':eig,'threshold':-tol,'passed':bool(eig>=-tol)})
    old=json.loads(Path(pre['source_pins']['old_device_spec']['path']).read_text(encoding='utf-8'))['model']
    old_gamma_root=beta*old['omega_OH']/2
    old_root=op(lambda a:D(np.diag([0,math.sqrt(beta*old['omega_OH'])]),a))
    old_z=op(lambda a:old['gamma_dephasing']*D(Z,a))
    different('old_dimensionless_rate_control',old_root,old_z,old_gamma_root)
    H_rabi=V0*(I+X); J_rabi=math.sqrt(2*beta*V0/hbar)*(I+X)/2
    rabi_root=op(lambda a:D(J_rabi,a))
    different('Rabi_sigma_z_is_not_root_H',rabi_root,dz,gamma)
    different('Rabi_noncommuting_jump',H_rabi@Z-Z@H_rabi,np.zeros((2,2)),V0)
    Hshift=H+2*V0*I
    Jshift=np.diag(np.sqrt(beta*np.diag(Hshift).real/hbar))
    equal('shift_keeps_commutator',op(lambda a:Hcomm(Hshift,a)),ham,omega)
    different('shift_changes_root_dissipation',op(lambda a:D(Jshift,a)),dissip,gamma)
    centered_eig=np.linalg.eigvalsh(H-Eref*I).tolist()
    checks.append({'name':'centered_Hg_not_positive','eigenvalues_J':centered_eig,'passed':bool(centered_eig[0]<0)})
    result={'schema':'configured-OH-sector/v1','unit':pre['unit'],'claim_event':845,'start_utc':start,'end_utc':now(),'seconds':time.perf_counter()-timer,'command':[sys.executable,'-B','-X','utf8',str(Path(__file__).resolve()),'--run'],'python':sys.version,'numpy':np.__version__,'freeze':pin(HERE/'FREEZE_OH_SECTOR_R1.json'),'runner':pin(__file__),'source_pins_after':{k:pin(v['path']) for k,v in pre['source_pins'].items()},'parameters':{'alpha':alpha,'beta_runtime':beta,'frequency_source_MHz':f_MHz,'omega_OH_s_inv':omega,'hbar_J_s':hbar,'V0_J':V0,'Eref_J':Eref,'gamma_root_s_inv':gamma,'gamma_phi_matching_s_inv':rate,'old_clock_omega_OH':old['omega_OH'],'old_clock_gamma_phi':old['gamma_dephasing'],'old_clock_gamma_phi_matching':old_gamma_root/2},'checks':checks,'passed':all(x['passed'] for x in checks),'checks_total':len(checks),'checks_passed':sum(x['passed'] for x in checks),'statute':'REAL numerical identities in the configured finite model; matching gamma_phi is INPUT, not measurement or full-device prediction','scope':pre['restrictions'],'center_caution':'The identity center was removed only in the Hamiltonian commutator/basis comparison. The root jump always used H>=0 with its specified excitation zero.','gate_changed':False,'new_observed_data':False,'physical_measurement':False}
    result['exit_code']=0 if result['passed'] else 1
    output=save('RESULTADO_OH_SECTOR_R1.json',result)
    print(json.dumps({'passed':result['passed'],'checks':len(checks),'result':output}))
    raise SystemExit(result['exit_code'])

if __name__=='__main__':
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--preregister',action='store_true');g.add_argument('--run',action='store_true');a=p.parse_args()
    preregister() if a.preregister else run()
