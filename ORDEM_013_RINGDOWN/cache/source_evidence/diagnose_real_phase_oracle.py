"""Record the failed validator's actual local arrays without changing it."""
import json
import numpy as np
import validate_real_phase_adapter as old
import source_evidence as se

try:
    old.oracle()
except ValueError as exc:
    tb = exc.__traceback__
    while tb.tb_next is not None:
        tb = tb.tb_next
    data = tb.tb_frame.f_locals
    independent = data['independent']
    approximate = data['approximate']
    if independent.shape != (len(approximate), 1, approximate.shape[1]):
        raise ValueError('Unexpected failed-oracle shape') from exc
    direct = se.linear_statistics(data['exact'], data['targets'], 3.)[1]
    result = dict(status='DIAGNOSED_ORACLE_BROADCASTING_ERROR',
        original_validator_sha256=se.sha(se.ROOT/'validate_real_phase_adapter.py'),
        original_error=str(exc), original_row=data['row'],
        old_direct_shape=independent.shape, approximate_shape=approximate.shape,
        unintended_comparison_shape=(independent-approximate).shape,
        corrected_direct_shape=direct.shape,
        corrected_error=float(np.max(np.abs(direct-approximate))),
        corrected_vs_squeezed_error=float(np.max(np.abs(direct-independent[:, 0, :]))))
    se.write(se.ROOT/'real_phase_adapter_validation/ORACLE_FAILURE_DIAGNOSIS.json', result)
    print(json.dumps(result), flush=True)
else:
    raise RuntimeError('Original oracle no longer fails')
