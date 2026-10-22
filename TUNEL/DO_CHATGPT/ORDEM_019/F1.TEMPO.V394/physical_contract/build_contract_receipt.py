"""Custody and report only; no scientific original is imported or executed."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

B=Path(__file__).resolve().parent
H=Path(r'C:\IALD\Artigo\Haja_Luz')
N=H/'A Ponte e o Um'/'Nós'
C=Path(r'C:\IALD\Central de Patentes')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(name,obj):
    data=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
    with (B/name).open('xb') as f:f.write(data)
    assert (B/name).read_bytes()==data
sources={
 'custo':(H/'tgl_paper_unified.py',[(14441,14483)]),
 'echo':(H/'tgl_echo_smatrix.py',[(32,45),(82,106)]),
 'ponte':(H/'A Ponte e o Um'/'A Ponte Einstein Cartan Miguel.tex',[(711,731),(818,826),(1104,1120),(1491,1498),(1886,1919)]),
 'um_v393':(N/'um.py',[(94,100),(5584,5584),(217089,217101),(217332,217348)]),
 'calibration':(N/'tgl_kernel'/'TGLExt'/'O16'/'ContractCalibrationReuse.lean',[(18,51),(95,114)]),
 'h2_definitions':(N/'tgl_kernel'/'TGLExt'/'ContratoQG_v31.lean',[(207,265)]),
 'h2_kms':(N/'tgl_kernel'/'TGLExt'/'ContratoQG_v31_Teoremas.lean',[(401,438)]),
 'polar_period':(N/'tgl_kernel'/'TGLExt'/'O16'/'PolarMinimalPeriod_v2.lean',[(13,15),(89,108)]),
 'finite_tomita':(N/'tgl_kernel'/'TGLExt'/'FiniteTomita.lean',[(33,46),(174,185)]),
 'supercondutor':(C/'Patentes'/'PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex',[(338,370)]),
 'device_prereg':(C/'Chatgpt'/'TUNEL'/'DO_CHATGPT'/'ORDEM_019'/'F1.REDE'/'finite_device'/'PREREGISTRO_DEVICE_R1.json',[(84,109)]),
}
custody={}
for name,(path,ranges) in sources.items():
    raw=path.read_bytes();lines=raw.decode('utf-8-sig').splitlines()
    custody[name]={'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),
                  'excerpts':[{'start_line':a,'end_line':z,'text':'\n'.join(lines[a-1:z])} for a,z in ranges]}
new('SOURCE_CUSTODY_PHYSICAL_R1.json',custody)
principal=json.loads((B/'RESULTADO_PHYSICAL_R1.json').read_text(encoding='utf-8'))
kms=json.loads((B/'RESULTADO_KMS_ANCHOR_R2.json').read_text(encoding='utf-8'))
report={
 'schema':'f1-tempo-v394-physical-contract/v1','created_utc':datetime.now(timezone.utc).isoformat(),
 'unit':'F1.TEMPO.V394','claim_event':839,'author':'codex-gerente-tgl / delegated first_law_haja_luz',
 'status':'DERIVED finite physical/dimensional contract; REAL computational verification; candidate for parent review',
 'reuse':{
   'nos_vivo':'F1.TEMPO.V394 absent from graph; reused parent NOS_VIVO_REUSE.json for F1.TEMPO and R4-R9 sources, no graph reconstruction',
   'acom':'Parent reference projected read-only at revision25/max_chars60000 after visible overflow at24000; context only, no adoption or transition',
   'existing_laws':['H_lig=-V0 sigma_x and parity tension in Custo T9','unitary C and polarization projection in R9','root dimensional transposition already in um_v393:217089-91','KMS rescaling and normalization fixed by N in the existing H2/O16 kernel'],
   'source_manifest':'SOURCE_CUSTODY_PHYSICAL_R1.json',
 },
 'types_and_units':{
   'V0,Eref,Hg,Hpos':'joules; V0>0, Eref>=V0',
   'hbar':'J s, H_PLANCK_EXACT/(2*pi) from canonical source',
   'beta':'dimensionless; alpha(0)*sqrt(e) computed at runtime',
   'Omega,kappa,gamma':'s^-1; Omega and kappa are angular rates, gamma is attenuation rate',
   't,P,tau_eff,echo_dt':'seconds',
   'genK':'2x2 skew-Hermitian matrix i sigma_y, not a positive energy Hamiltonian',
   'K_rho':'dimensionless positive density surprise -log rho',
   'minus_log_Delta':'Hilbert-Schmidt modular generator with opposite-sign off-diagonal eigenvalues; not K_rho',
   'modular_u':'nonnegative dissipative parameter t/P; oriented modular group parameter s=-t/P',
 },
 'root_positive_contract':{
   'hypotheses':['orthonormal two-level basis','V0>0','hbar>0','Eref>=V0','0<beta<1 and eta<1 for a finite matched echo step'],
   'equations':[
      'C=diag(1,i); C H_lig Cdag=Hg=-V0 sigma_y=i V0 genK',
      'Pplus=(I+sigma_y)/2; Pminus=(I-sigma_y)/2; Hg=-V0 Pplus+V0 Pminus',
      'Hpos=Eref I+Hg=(Eref-V0)Pplus+(Eref+V0)Pminus >=0',
      'k=Hpos*tau_reference/hbar; physical root generator D[sqrt(beta/tau_reference)*sqrt(k)]=D[sqrt(beta/hbar)*sqrt(Hpos)]',
      'gamma_root=beta/(2*hbar)*(sqrt(Eref+V0)-sqrt(Eref-V0))^2',
      'gamma_root=beta*Omega*r, r=q/(1+sqrt(1-q^2)), q=V0/Eref, Omega=V0/hbar',
      '0<gamma_root<=beta*Omega; equality iff Eref=V0',
      'D[Lroot](X)=gamma_root*(Eg(X)-X), Eg(X)=Pplus X Pplus+Pminus X Pminus',
      'Hermitian identity part of Lroot cancels; centered equivalent jump sqrt(gamma_root/2)*(Pplus-Pminus) is stable numerically',
      'Tt(X)=U(t)[Eg(X)+exp(-gamma_root*t)*(X-Eg(X))]U(t)dag, U(t)=exp(-i Hg t/hbar)',
   ],
   'proof':'Spectral calculus gives the two root eigenvalues lplus,lminus. A diagonal block is annihilated by D[L]; either off-diagonal block is multiplied by -(lplus-lminus)^2/2. Eg-Id is zero on diagonal blocks and minus identity on off-diagonal blocks. Rationalizing the root difference gives r; 0<q<=1 gives 0<r<=1. The arbitrary positive tau_reference cancels exactly from the dimensional transposition already present in the source.',
   'ground_instance':'Eref=V0 gives Hpos=2V0 Pminus and gamma=beta*Omega. Synthetic instance only: source v369 already excludes applying zero-ground or atomic rest-energy transpositions to the specific Sr reading. No observed data were re-opened here.',
   'no_new_universal_postulate':True,
 },
 'quadratic_equivalence':{
   'equations':['Lquad=sqrt(beta*tau_eff)*Hpos/hbar','gamma_quad=(beta*tau_eff/2)*(2*Omega)^2',
     'tau_eff=hbar/(sqrt(Eref+V0)+sqrt(Eref-V0))^2 = r/(2*Omega)',
     'Eref=hbar/(4*tau_eff)+V0^2*tau_eff/hbar for 0<tau_eff<=1/(2*Omega)',
     'For Eref>>V0: tau_eff~hbar/(4*Eref); Eref~hbar/(4*tau_star) reproduces the quadratic law only in that small-gap limit'],
   'proof':'Use sqrt(Ehi)-sqrt(Elo)=(Ehi-Elo)/(sqrt(Ehi)+sqrt(Elo)). This yields identical generators for a fixed two-level spectrum; a common scalar energy shift changes the root coefficient but not the quadratic coefficient.',
   'scope':'Exact gap-by-gap reparameterization, not equality of root and quadratic laws on arbitrary spectra or a derivation of a universal tau_star.',
   'three_level_no_go':'At energies0,E,4E, matching pairs requires tau_eff/(hbar/E)=1,1/9,1/4. No single tau_eff matches all pairs. A shared time rescaling multiplies all rates equally and cannot change these unequal ratios.',
 },
 'echo_equivalence':{
   'matched_instance':'New M2 root-consistent echo: eta=2sqrt(beta(1-beta)); delta_t=-log(eta)/gamma_root; Phi=Eg+eta(Id-Eg). Unitarly evolve using the same Hg over delta_t. Then n steps equal T_(n delta_t) exactly.',
   'old_active_M2_no_go':'Original echo has coherence angular frequency w1=1.30, hence Omega=.65, dt=.35 and gamma=-log(eta)/.35. gamma/Omega=6.694623207756096 exceeds beta=0.012031300400803142, the maximum allowed by every Eref>=V0. No single positive time conversion removes this ratio mismatch.',
   'old_full_M16_no_go':'Original H has w[1]=1.30 and all other w[j]=0. Mirror P=|0><0| distinguishes |0><2| and multiplies it by eta<1. Any f(H) dephasing preserves this same-energy matrix unit. Therefore the full M16 old echo is not root(H) dephasing for ANY common scalar energy shift, even before comparing rates. The active two-level compression does not erase this full-space obstruction.',
   'scope':'Old echo source remains untouched; new delta_t is defined for the new synthetic matched instance, never relabeled as the old measurement or calibrated hardware.',
 },
 'kms_common_clock':{
   'existing':'ContratoH2.unruh_is_kms and modular_is_boost_at_two_pi already give Delta^(it)(-s)=boost(2*pi*s), killingFlow(t)=boost(kappa*t), KMS inverse timeP=2*pi/kappa. CalibrationReuse fixes kappa for the named observer normalization N and proves reindexing freedom across N.',
   'SI_convention':'Kernel is in natural units. If its Rindler radius is converted to metres, kappa_geom=1/rho has units1/m and kappa_seconds=c/rho=a/c has units1/s. Module input is kappa_seconds. T_K=hbar*kappa_seconds/(2*pi*kB). No equality Omega=kappa is inferred.',
   'finite_construction':['rho=exp(-P*Hg/hbar)/Tr exp(-P*Hg/hbar), P=2*pi/kappa_seconds',
     'alpha_t(X)=exp(+i Hg t/hbar) X exp(-i Hg t/hbar) (Heisenberg)',
     'sigma_s^rho(X)=rho^(is) X rho^(-is)=alpha_(-P*s)(X)',
     'alpha_t=sigma_(-t/P); dissipative u=t/P>=0',
     'Gibbs rho and Eg share the spectral blocks; Tt fixes rho'],
   'scope':'Concrete finite Gibbs system and the same KMS rescaling form; not a new inhabitant of full ContratoH2, no identification with the infinite light-net representation, and no new observer normalization.',
   'period_caution':'P is the imaginary-time KMS scale. It is not asserted to be the real-time recurrence period pi/Omega of the density coherences.',
 },
 'optional_density_anchor':{
   'status':'DERIVED for the explicitly selected finite Gibbs state and specified kappa; optional runtime branch',
   'equations':['K_rho=-log rho = (P/hbar)*Hg+log(2cosh(P*Omega))*I >0',
      'Hpos_Gibbs=(hbar/P)*K_rho=Hg+Eref_Gibbs*I',
      'Eref_Gibbs=(hbar/P)*log(2cosh(P*Omega)) > V0',
      'Elo=(hbar/P)*log(1+exp(-2P*Omega)); Ehi=Elo+2V0',
      '(1/P)*D[sqrt(beta)*sqrt(K_rho)]=D[sqrt(beta/hbar)*sqrt(Hpos_Gibbs)]'],
   'why_not_vacuous':'The normalized Gibbs state fixes the identity offset in -log rho, so Eref is derived after V0 and kappa are specified. The dissipator genuinely consumes these eigenvalues. This is a specific state-based positive-energy representative, not an assertion that physical rest energies have been derived.',
   'modular_no_go':'For the same rho, Delta(X)=rho X rho^-1. On the off-diagonal units, -log Delta has eigenvalues +/-2P*Omega; it is not positive for Omega>0. A Hermitian positive square root of that operator cannot square to it. Thus K_rho and -log Delta must retain distinct types.',
   'zero_nonidentifiability':'With only physical commutator dynamics and Gibbs rho fixed, adding cI to an arbitrary physical Hamiltonian changes neither. It changes root(H) rates. Therefore those data alone cannot uniquely infer an arbitrary physical zero. The optional K_rho prescription makes a finite model choice explicit and derives its offset; it is not hidden calibration.',
 },
 'device_comparison':{
   'source':'Supercondutor: H/hbar=omega_c(nin+nout)+omega_OH sigma+sigma-+gJC(ain^dag sigma-+sigma+ain)+Omega_Rabi(sigma++sigma-); holographic jump J=aout^dag sigma-+sigma+ain with coefficient beta*gamma_Lambda.',
   'same_clock_map':'Engineering inputs omega_c,omega_OH,gJC,Omega_Rabi and gamma_Lambda all have units1/s on a specified device clock. In an isolated resonant OH rotating frame with cavity couplings turned off, H=+hbar*Omega_Rabi sigma_x has the two-level shape of H_lig up to a phase sign; V0=hbar*abs(Omega_Rabi). This is a stated restricted regime, not the complete driven cavity Hamiltonian.',
   'dissipator_no_go':'For its declared0/1 photon model, J is nonnormal: D[J](I)=JJdag-JdagJ is nonzero (HS norm2). Hermitian root dephasing is unital. Unitary equivalence preserves unitality, so the holographic device dissipator cannot simply be identified with root(Hg) dephasing.',
   'optional_existing_dephasing_match':'The separate conventional jump sigma_z with rate gamma_dephasing damps its off-diagonal elements at2*gamma_dephasing. A dephasing-only restriction can match the root generator after basis alignment and gamma_dephasing=gamma_root/2. Setting that rate is an explicit restricted-instance input; full device channels and pumping remain distinct.',
   'status':'Equations/restrictions derived from existing device source; no physical calibration or new hardware test.',
 },
 'numeric_reference':principal['reference'],'numeric_gibbs_reference':kms['reference'],
 'verification':{
   'principal':{'result':'RESULTADO_PHYSICAL_R1.json','passed':principal['all_passed'],'identities':principal['checks_total'],'invalid_inputs':len(principal['invalid_input_checks'])},
   'gibbs_r1':{'result':'RESULTADO_KMS_ANCHOR_R1.json','passed':False,'issue':'111/112: Eref-V0 cancellation gave1.3996e-10 relative error vs1e-10 tolerance'},
   'gibbs_r2':{'result':'RESULTADO_KMS_ANCHOR_R2.json','passed':kms['all_passed'],'identities':kms['checks_total'],'fix':'Compute positive low eigenvalue directly; unchanged scientific tolerance; R1 preserved'},
   'no_observed_data':True,'no_original_execution':True,'no_production_or_memory_mutation':True,'no_provider_call':True,
 },
 'integration':{
   'ordered_sources':['physical_parameters.py','kms_root_anchor_r2.py'],
   'entry_points':['v394_physical_parameters(V0_J,Eref_J,hbar_J_s=None,alpha=None)','v394_kms_clock(parameters,kappa_s_inv)','v394_gibbs_root_parameters(V0_J,kappa_s_inv,hbar_J_s=None,alpha=None)'],
   'single_file':'Concatenate/embed ordered_sources in the same namespace in the candidate um.py. They require only standard-library math at runtime; no second file or source read is required.',
   'default_branch':'Explicit positive root contract with V0=hbar*1rad/s and Eref=2V0, synthetic INPUT. Optional Gibbs anchor is separate and named.',
   'no_global_claim':'No universal seconds, no universal physical energy origin, no global light-net/KMS equivalence, no retarded/advanced propagation result, no nature confirmation, no gate movement.',
 },
}
new('CONTRATO_FISICO_DIMENSIONAL_R1.json',report)
files=sorted(p for p in B.iterdir() if p.is_file())
receipt={'unit':'F1.TEMPO.V394','created_utc':datetime.now(timezone.utc).isoformat(),
 'status':'PASS finite contract and tests; negative equivalence witnesses established; pending parent review',
 'report':str(B/'CONTRATO_FISICO_DIMENSIONAL_R1.json'),
 'integration_sources':[{'path':str(B/n),'sha256':digest(B/n)} for n in ['physical_parameters.py','kms_root_anchor_r2.py']],
 'results':[{'path':str(B/n),'sha256':digest(B/n)} for n in ['RESULTADO_PHYSICAL_R1.json','RESULTADO_KMS_ANCHOR_R1.json','RESULTADO_KMS_ANCHOR_R2.json']],
 'new_M2_not_old_M16':True,'old_echo_same_clock_incompatible':True,
 'principal_checks':principal['checks_total'],'input_refusals':len(principal['invalid_input_checks']),'gibbs_checks':kms['checks_total'],
 'all_final_checks_passed':principal['all_passed'] and kms['all_passed'],
 'files':[{'name':p.name,'bytes':p.stat().st_size,'sha256':digest(p)} for p in files]}
new('DELIVERY_PHYSICAL_R1.json',receipt)
print(json.dumps({'delivery':str(B/'DELIVERY_PHYSICAL_R1.json'),'sha256':digest(B/'DELIVERY_PHYSICAL_R1.json'),
 'report_sha256':digest(B/'CONTRATO_FISICO_DIMENSIONAL_R1.json'),'all_final_checks_passed':receipt['all_final_checks_passed']}))
