import ast
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
source = root / 'um_v368.py'
raw = source.read_bytes()
tree = ast.parse(raw.decode('utf-8-sig'))
node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'evaluate_quantum_gravity_closure')
namespace = {}
exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), 'exec'), namespace)
formal = dict.fromkeys(['concrete_aqft_core_constructed', 'concrete_breuer_corner_constructed', 'concrete_modular_four_frame_constructed', 'concrete_solder_field_constructed', 'concrete_emergent_einstein_proved', 'canonical_boundary_transport_witness_constructed'], True)
physics = dict.fromkeys(['massless_spin2_proved', 'exactly_two_helicities_proved', 'ghost_free_proved', 'stress_energy_conserved', 'relevant_anomalies_absent'], True)
experiment = dict.fromkeys(['independent_v3_profiles_unblinded', 'independent_v3_survey_mocks_passed', 'independent_v3_systematics_passed', 'independent_v3_powered_verdict_emitted'], True)
gate = namespace[node.name]
baseline = gate(formal, physics, experiment)
extended = dict(formal, gpf_H2_smooth_modular_four_frame_discharged=False, gpf_H3_local_horizon_equilibrium_discharged=False, gpi_H3_horizon_data_produced=False)
assert gate(extended, physics, experiment) == baseline
assert not gate({}, {}, {})['mathematical_model_constructed']
assert not gate(formal, dict(physics, massless_spin2_proved=False), experiment)['physical_quantum_gravity_constructed']
result = {'source_sha256': hashlib.sha256(raw).hexdigest(), 'function_line': node.lineno, 'scope': 'isolated existing function; no full um.py execution or Lean rebuild', 'tests_passed': 3, 'extra_H2_H3_flags_do_not_change_this_gate': True, 'baseline': baseline}
target = root / 'gate_verificado.json'
data = json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8')
temporary = target.with_suffix('.tmp')
temporary.write_bytes(data)
assert temporary.read_bytes() == data
temporary.replace(target)
print(json.dumps(result, ensure_ascii=False, indent=2))
