"""Record a source-pinned inventory, not a new physical experiment or build."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

HERE = Path(__file__).resolve().parent
ORD = HERE.parents[1]
PHYS = ORD / 'F1.TEMPO.V394' / 'physical_contract'
OLD = json.loads((PHYS / 'SOURCE_CUSTODY_PHYSICAL_R1.json').read_text(encoding='utf-8'))

def pin(path):
    path = Path(path).resolve()
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

sources = {}
for key, record in OLD.items():
    current = pin(record['path'])
    current['matches_existing_custody'] = current['sha256'] == record['sha256']
    if not current['matches_existing_custody']:
        raise RuntimeError(f'Changed source: {key}')
    current['anchors'] = [{'start_line': x['start_line'], 'end_line': x['end_line']} for x in record.get('excerpts', [])]
    sources[key] = current

for name in ['CONTRATO_FISICO_DIMENSIONAL_R1.json', 'RESULTADO_PHYSICAL_R1.json', 'RESULTADO_KMS_ANCHOR_R2.json', 'physical_parameters.py', 'kms_root_anchor_r2.py']:
    sources[name] = pin(PHYS / name)
for name in ['RELATORIO_DEVICE_R1.md', 'PREREGISTRO_DEVICE_R1.json', 'run_finite_device.py']:
    sources['finite_device/' + name] = pin(ORD / 'F1.REDE' / 'finite_device' / name)
for directory, name in [('DISPOSITIVO_E_ESPECTRO_R7', 'CONTRATO_DISPOSITIVO_E_LEI_RAIZ_R7.txt'), ('FREQUENCIA_E_GRAVITON_R9', 'PONTE_FREQUENCIA_GRAVITON_R9.txt')]:
    sources[name] = pin(ORD / 'F1.TEMPO.LEITURA_20261015' / directory / name)

contract = json.loads((PHYS / 'CONTRATO_FISICO_DIMENSIONAL_R1.json').read_text(encoding='utf-8'))
principal = json.loads((PHYS / 'RESULTADO_PHYSICAL_R1.json').read_text(encoding='utf-8'))
kms = json.loads((PHYS / 'RESULTADO_KMS_ANCHOR_R2.json').read_text(encoding='utf-8'))

result = {
    'schema': 'physical-clock-reuse-inventory/v1',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'unit': 'F1.FECHO_20261015', 'claim_event': 845,
    'author': 'codex-gerente-tgl / delegated tempo_math_review',
    'status': 'DERIVED source-based algebra; REAL source pins and reuse inventory; no new numerical experiment or Lean build',
    'scope': {'production_changes': False, 'memory_changes': False, 'provider_calls': False, 'new_observed_data': False, 'gate_change': False},
    'sources': sources,
    'already_available': [
        {'source': 'Custo:14441-14483 and R9', 'content': 'Hlig=-V0 sigma_x; C=diag(1,i) gives Hg=-V0 sigma_y=i V0 genK. Omega=V0/hbar, coherence gap frequency=2Omega. The Custo V0 is an abstract parity coupling; its radiative reading V0=hbar omega is stated in the source, not a measured device value.'},
        {'source': 'CONTRATO_FISICO_DIMENSIONAL_R1.json/root_positive_contract', 'content': 'Hpos=Eref I+Hg >=0 with Eref>=V0>0; root rate gamma=beta/(2hbar)(sqrt(Eref+V0)-sqrt(Eref-V0))^2. Exact fixed-two-level quadratic matching tau_eff=hbar/(sqrt(Ehi)+sqrt(Elo))^2 is already implemented. It does not extend to arbitrary multilevel spectra with one universal tau.'},
        {'source': 'O16/ContractCalibrationReuse.lean:19-51,104-114; ContratoQG_v31_Teoremas.lean:401-438', 'content': 'Named observer N fixes kappa=1/refRadius(N) in natural units; changing N changes normalization. Existing H2 supplies KMS time P=2pi/kappa. SI conversion kappa_seconds=c/rho=a/c must be explicit. No Omega=kappa follows.'},
        {'source': 'CONTRATO_FISICO_DIMENSIONAL_R1.json/kms_common_clock and optional_density_anchor; FiniteTomita.lean:33-46,174-185', 'content': 'For a specifically chosen finite Gibbs state rho proportional to exp(-P Hg/hbar), sigma_s=alpha_(-Ps). K_rho=-log rho is positive; Hpos_Gibbs=(hbar/P)K_rho derives Eref=(hbar/P)log(2cosh(P Omega)) after V0 and kappa are specified. This bridge is already implemented; -log Delta is a distinct signed modular generator. Gibbs alone does not determine an arbitrary physical energy zero or select rho dynamically under dephasing.'}
    ],
    'device_identity': {
        'source': 'PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex:338-370',
        'hamiltonian': 'H/hbar=omega_c(n_in+n_out)+omega_OH sigma+sigma-+g_JC(a_in^dag sigma-+sigma+ a_in)+Omega_Rabi(sigma++sigma-)',
        'jump': 'J=a_out^dag sigma-+sigma+ a_in; coefficient beta gamma_Lambda multiplying D[J]',
        'frequency': 'Omega_Rabi is microwave pumping, not the EOM frequency. omega_OH=2pi times 1.667359 GHz is the stated source specification, not a new measurement.',
        'units': 'All Hamiltonian coefficients are s^-1 on the engineering clock; H and V0,Eref are joules. beta is dimensionless and remains runtime alpha(0)*sqrt(e).',
        'kappa_warning': 'Patent:377-383 kappa is cavity photon loss. H2 kappa is normalized Killing acceleration rate. Custo:14485-14500 also uses kappa for elastic boundary energy. Equal names, and in two cases equal units, do not establish equality.'
    },
    'restricted_bare_OH_bridge': {
        'status': 'DERIVED algebraic wiring of existing operators under explicit restrictions; not a device rate prediction',
        'hypotheses': ['omega_OH>0; choose bare excitation-energy zero at the OH ground level', 'g_JC=0 and Omega_Rabi=0', 'Cavity modes remain in their vacuum spectator sector', 'gamma_Lambda=0 and gamma_OH=0; retain only the existing sigma_z dephasing channel'],
        'equations': ['H_OH=hbar omega_OH n_e, with spectrum {0,hbar omega_OH}', 'V0=Eref=hbar omega_OH/2; after subtracting the identity center and a unitary eigenbasis map, Hg has the R9 form', '[H_OH,sigma_z]=0', 'gamma_root=beta omega_OH/2', 'gamma_phi D[sigma_z] has coherence rate 2gamma_phi', 'Exact matching requires gamma_phi=beta omega_OH/4'],
        'nonvacuity': 'The existing two-level OH matrices and cavity vacuum realize the restricted Hilbert sector. Equality of the measured conventional rate to the root rate remains an additional INPUT/test, not an outcome of the source.',
        'not_full_model': 'Relaxation, cavity exchange and the holographic J were explicitly removed. No inference about the complete driven device, latency or universal physical clock follows.'
    },
    'Rabi_scope_clarification': {
        'source': 'CONTRATO_FISICO_DIMENSIONAL_R1.json/device_comparison; finite_device/run_finite_device.py:169-172',
        'content': 'The isolated resonantly driven rotating-frame Hamiltonian H=hbar Omega_Rabi sigma_x supplies V0=hbar|Omega_Rabi|. But the separate conventional sigma_z jump does not commute with sigma_x. A common unitary basis change preserves the nonzero commutator. Therefore the existing dephasing-only matching sentence must not be composed into simultaneous root(H) equivalence of that driven Hamiltonian and its sigma_z dissipator. The bare OH restriction above provides a compatible alternative with explicitly named exclusions.'
    },
    'full_holographic_obstruction': {
        'status': 'DERIVED finite algebra, reused from R7',
        'equation': 'On a=|100>, b=|001>, c=|010>, J=|b><a|+|c><b| gives D[J](I)=|c><c|-|a><a| !=0.',
        'conclusion': 'The isolated holographic generator is nonunital; Hermitian root dephasing is unital. They cannot be equal by mere unitary conjugation. This does not prohibit a named effective sector, approximation or additional balancing terms.'
    },
    'old_echo_scope': {
        'source': 'tgl_echo_smatrix.py and R7, R9, physical contract',
        'existing_numeric_text': contract['echo_equivalence']['old_active_M2_no_go'],
        'branch_qualification': 'The numeric mismatch uses the source continuous frequency branch nu=w1=1.30 at dt=.35; sampled phase also permits nu_m=w1+2pi m/dt. The mismatch is not an impossibility theorem for every branch embedding.',
        'full_space': contract['echo_equivalence']['old_full_M16_no_go'],
        'existing_repair': contract['echo_equivalence']['matched_instance'],
        'scope': 'New matched synthetic step does not replace the old experiment or calibrate hardware.'
    },
    'existing_evidence_reused': {
        'physical_passed': principal['all_passed'], 'physical_checks': principal['checks_total'],
        'kms_passed': kms['all_passed'], 'kms_checks': kms['checks_total'],
        'new_execution': False,
        'origin': 'Pinned local result artifacts, not fresh measurements by this inventory.'
    },
    'remaining_typed_physical_identification': [
        'Select the actual physical sector, operating frame, excitation-energy reference and engineering clock; do not import dimensionless finite_device defaults as SI measurements.',
        'For bare OH, compare independently supplied gamma_phi with beta omega_OH/4; for the full J model construct an actual reduction or retain its distinct nonunital dynamics.',
        'If using the Gibbs/KMS anchor, identify the thermal state and observer normalization experimentally/theoretically in that sector; cavity loss kappa alone supplies neither.',
        'There is already a complete conditional finite spectral/clock construction. The remaining issue is the named physical identification and rates, not absence of an algebraic bridge.'
    ],
    'script': pin(__file__)
}

out = HERE / 'PHYSICAL_CLOCK_INVENTORY_R4.json'
if out.exists():
    raise FileExistsError(out)
data = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
tmp = out.with_suffix('.json.tmp')
with tmp.open('xb') as f:
    f.write(data)
if tmp.stat().st_size != len(data):
    raise RuntimeError('Short write')
tmp.rename(out)
print(json.dumps(pin(out), ensure_ascii=False))
