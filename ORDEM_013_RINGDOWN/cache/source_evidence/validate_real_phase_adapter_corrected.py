"""Independent real-interpolation oracle and failed-source full-wave controls."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
from datetime import datetime, timezone
import copy
import json
import numpy as np
from scipy.special import logsumexp
import source_evidence as se
import peak_phase_coordinates as pc
import phase_marginal_source as pm
import real_fourier_phase as real
from phase_marginal_real_source import phase_marginal_loglikes

FOLDER = se.ROOT/'real_phase_adapter_validation_corrected'
FAILED = se.ROOT/'failed_phenom_phase_diagnostic'
PILOT = se.ROOT/'phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384'


def make_bank(data):
    n = len(data)
    return dict(n=n, orders=np.fft.fftfreq(n)*n, samples=data[None],
                coefficients=(np.fft.fft(data, axis=0)/n)[None])


def oracle():
    rng = np.random.default_rng(130950)
    phases = np.r_[.173, .619, 1.413, rng.uniform(-3, 9, 31)]
    rows = []
    for n in (16, 17):
        data = rng.normal(size=(n, 13, 2))
        bank = make_bank(data)
        angles = phases[:, None]-2*np.pi*np.arange(n)[None, :]/n
        kernel = np.ones_like(angles)
        for k in range(1, (n-1)//2+1):
            kernel += 2*np.cos(k*angles)
        if n % 2 == 0:
            kernel += np.cos(n*angles/2)
        exact = np.einsum('pk,ktj->ptj', kernel/n, data)
        got = real.evaluate_bank(bank, phases, 0)
        legacy_real = np.einsum('pk,ktj->ptj', np.exp(1j*np.outer(phases, bank['orders'])), bank['coefficients'][0]).real
        targets = rng.normal(size=(9, 13))
        independent = se.linear_statistics(exact, targets, 3.)[1]
        approximate = real.bank_loglikes(bank, phases, targets, 0)
        if independent.shape != approximate.shape:
            raise ValueError('Independent likelihood shapes differ')
        row = dict(n=n, cardinal_interpolation_error=float(np.max(np.abs(exact-got))),
            legacy_real_error=float(np.max(np.abs(legacy_real-got))),
            original_sample_error=float(np.max(np.abs(real.evaluate_bank(bank, 2*np.pi*np.arange(n)/n, 0)-data))),
            direct_amplitude_integral_error=float(np.max(np.abs(independent-approximate))))
        if max(v for k, v in row.items() if k != 'n') > 1e-10:
            raise ValueError('Independent real-Fourier oracle failed')
        rows.append(row)
    # A pure Nyquist cosine is legitimate real data, not imaginary leakage.
    data = ((-1.)**np.arange(16))[:, None, None]*np.ones((16, 3, 2))
    bank = make_bank(data)
    expected = np.cos(8*phases)[:, None, None]*np.ones((len(phases), 3, 2))
    nyquist_error = float(np.max(np.abs(real.evaluate_bank(bank, phases, 0)-expected)))
    try:
        pc.evaluate_bank(bank, [.173], 0)
    except ValueError as exc:
        old_rejection = str(exc)
    else:
        raise ValueError('Counterexample no longer reproduces old rejection')
    bad = copy.deepcopy(bank); bad['coefficients'][0, 3, 1, 0] += .01j
    mismatch = copy.deepcopy(bank); mismatch['samples'][0, 2, 0, 0] += .01
    refused = 0
    for b, phase in ((bad, [.2]), (mismatch, [.2]), (bank, [np.nan])):
        try:
            real.evaluate_bank(b, phase, 0)
        except ValueError:
            refused += 1
        else:
            raise ValueError('Corrupted real phase bank accepted')
    return dict(rows=rows, nyquist_error=nyquist_error, old_nyquist_rejection=old_rejection, invalid_banks_refused=refused)


def main():
    pm.check(); FOLDER.mkdir(exist_ok=False)
    names = ['validate_real_phase_adapter_corrected.py', 'REAL_PHASE_VALIDATION_CORRECTION.json', 'validate_real_phase_adapter.py', 'real_fourier_phase.py', 'phase_marginal_real_source.py',
             'REAL_PHASE_ADAPTER_PROVENANCE.json', 'phase_marginal_source.py', 'peak_phase_coordinates.py']
    se.write(FOLDER/'REGISTRATION.json', dict(status='REGISTERED_REAL_FOURIER_CORRECTION_CONTROL',
        date_utc=datetime.now(timezone.utc).isoformat(), seed=130950,
        limits=dict(algebra=1e-10, full_wave_relative=1e-6, full_logL=.001, phase_quadrature=1e-5),
        failed_point=15627, reuse_scope='Original real outputs unchanged algebraically; discarded imaginary Nyquist artifact replaced by real cosine with independent bank integrity checks',
        hashes={n: se.sha(se.ROOT/n) for n in names}))
    controls = oracle(); state = se.load_state()
    with np.load(PILOT/'PROPOSALS.npz') as f:
        u = f['unit_cube'].copy()
    rows = []
    for index in (15619, 15625, 15627):
        value, metadata = phase_marginal_loglikes('IMRPhenomXPHM', u[index], state)
        row = dict(index=index, controls=metadata)
        passing = FAILED/f'point_{index}_passing.npz'
        if passing.exists():
            with np.load(passing) as f:
                error = float(np.max(np.abs(value-f['components'])))
            if error > 1e-9:
                raise ValueError('Previously passing likelihood changed')
            row['previous_integral_error'] = error
        se.save_arrays(FOLDER/f'point_{index}.npz', components=value)
        rows.append(row)
        print(json.dumps(row), flush=True)
    x = pm.six_to_physical(u[15627])
    refinements = []
    for psd in ('O4', 'O5'):
        integrals = []
        for n in (16, 32, 64):
            bank = pc.phase_bank('IMRPhenomXPHM', x, state['times'], state[psd+'_white'], n=n)
            phases = 2*np.pi*np.arange(1024)/1024
            output = np.array([logsumexp(real.bank_loglikes(bank, phases, state[psd+'_targets'], a), axis=0)-np.log(len(phases)) for a in (0, 1)])
            integrals.append(output)
            se.save_arrays(FOLDER/f'failed_{psd}_bank{n}.npz', phase_integrals=output)
        differences = [float(np.max(np.abs(integrals[i]-integrals[-1]))) for i in (0, 1)]
        if max(differences) > .001:
            raise ValueError('Real phase bank disagrees under size refinement')
        refinements.append(dict(psd=psd, compared_to_n64_max_logL_errors=differences))
    result = dict(status='PASS_REAL_PHASE_ADAPTER', algebra=controls, source_rows=rows,
        failed_point_bank_refinement=refinements, failed_point_recovered=True,
        physical_prior_changed=False, full_wave_or_quadrature_tolerance_relaxed=False,
        imaginary_guard_replaced='Real Nyquist interpolation plus coefficient/sample and conjugate-symmetry checks; original imaginary comparison was not a valid real-interpolation test',
        scientific_acceptance=False, registration_sha256=se.sha(FOLDER/'REGISTRATION.json'))
    se.write(FOLDER/'RESULT.json', result)
    print(json.dumps({k: v for k, v in result.items() if k not in ('algebra', 'source_rows')}), flush=True)


if __name__ == '__main__':
    main()
