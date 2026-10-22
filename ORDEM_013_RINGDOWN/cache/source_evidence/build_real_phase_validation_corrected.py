"""Make a separate validator with an explicitly repaired comparison shape."""
import json
import source_evidence as se

original = se.ROOT/'validate_real_phase_adapter.py'
target = se.ROOT/'validate_real_phase_adapter_corrected.py'
diagnosis_path = se.ROOT/'real_phase_adapter_validation/ORACLE_FAILURE_DIAGNOSIS.json'
diagnosis = json.loads(diagnosis_path.read_bytes())
if diagnosis['original_validator_sha256'] != se.sha(original):
    raise ValueError('Original failed validator changed')
text = original.read_text()
changes = [
    ("FOLDER = se.ROOT/'real_phase_adapter_validation'", "FOLDER = se.ROOT/'real_phase_adapter_validation_corrected'"),
    ("independent = np.array([se.linear_statistics(v, targets, 3.)[1] for v in exact])",
     "independent = se.linear_statistics(exact, targets, 3.)[1]"),
    ("approximate = real.bank_loglikes(bank, phases, targets, 0)",
     "approximate = real.bank_loglikes(bank, phases, targets, 0)\n        if independent.shape != approximate.shape:\n            raise ValueError('Independent likelihood shapes differ')"),
    ("names = ['validate_real_phase_adapter.py'",
     "names = ['validate_real_phase_adapter_corrected.py', 'REAL_PHASE_VALIDATION_CORRECTION.json', 'validate_real_phase_adapter.py'"),
]
for before, after in changes:
    if text.count(before) != 1:
        raise ValueError('Expected exactly one validator edit: '+before)
    text = text.replace(before, after)
if target.exists():
    raise FileExistsError(target)
temp = target.with_suffix('.py.tmp')
raw = text.encode()
temp.write_bytes(raw)
if temp.read_bytes() != raw:
    raise ValueError('Invalid temporary copy')
temp.replace(target)
se.write(se.ROOT/'REAL_PHASE_VALIDATION_CORRECTION.json', dict(
    reason='Old singleton grid axis caused a phase-by-phase cross-comparison instead of a matched comparison',
    failed_validator_sha256=se.sha(original), corrected_validator_sha256=se.sha(target),
    diagnosis_sha256=se.sha(diagnosis_path), edits=changes,
    tolerance_changed=False, physical_algorithm_changed=False))
print('Separate corrected validator created; failed validator retained.', flush=True)
