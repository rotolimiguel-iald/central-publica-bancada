"""Registered, conditional model averaging after both source runs complete.

No new waveform is generated. Mock experiments remain separate. The result is
always a pilot until source convergence, repetition and calibration are paid.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
import argparse
from datetime import datetime, timezone
import json
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
from audit_phase_source import load_run
from source_family_mixture import mix_statistics, source_precision_mask

FOLDER = se.ROOT/'source_family_combination_real_repeat'
RUNS = {
    'IMRPhenomXPHM': 'phase_ringdown_real_continuation/IMRPhenomXPHM_seed130892_N16384',
    'SEOBNRv4HM': 'phase_native_repeat/SEOBNRv4HM_seed130942_N16384',
}


def register():
    pm.check()
    validation = json.loads((se.ROOT/'source_family_mixture_validation/RESULT.json').read_bytes())
    if validation['status'] != 'PASS_FAMILY_MIXTURE_ARITHMETIC':
        raise ValueError('Family mixture has not passed arithmetic controls')
    names = ['source_family_mixture.py', 'combine_source_families.py',
             'combine_continuation_families.py', 'CONTINUATION_FAMILY_MIXTURE_PROVENANCE.json',
             'source_family_mixture_validation/REGISTRATION.json',
             'source_family_mixture_validation/RESULT.json',
             'INJECTIONS.json', 'INJECTIONS.npz', 'REGISTRATION.json',
             'phase_runs/REGISTRATION.json', 'audit_phase_source.py']
    for name in RUNS.values():
        names += [name+'/START.json', name+'/PROPOSALS.npz',
                  name.rsplit('/', 1)[0]+'/REGISTRATION.json']
    FOLDER.mkdir(exist_ok=False)
    reg = dict(status='REGISTERED_NONBLIND_SOURCE_FAMILY_MIXTURE',
        date_utc=datetime.now(timezone.utc).isoformat(), runs=RUNS,
        family_prior={f: .5 for f in RUNS},
        prior_scope='Explicit equal model prior, conditional comparison only; same weights under a=0 and a=1. Consistent with earlier C5 family-mixture control, not derived from TGL.',
        formula='Z_a=sum_f pi_f Z_fa; lnB=lnZ_1-lnZ_0. Never average lnB_f and never multiply simulations.',
        error_scope='Centered family influence, paired within each family, independent between draws of different families; delta method invalid at low ESS.',
        acceptance='Individual family precision cannot be hidden by mixture. Independent repeats, rate controls and continuous-strength bias/coverage remain mandatory.',
        target_order='The frozen INJECTIONS.json label order, a=0 then a=1 component blocks',
        numerical_tests=dict(component_ESS_min=100, component_max_weight=.05, lnB_MC_sd_max=.2),
        reused_noise_intervals=50, mock_datasets=1200, physical_partition_selected=False,
        actual_event_strain_used=False, C6_changed=False,
        hashes={n: se.sha(se.ROOT/n) for n in names})
    se.write(FOLDER/'REGISTRATION.json', reg)
    print(json.dumps({k: reg[k] for k in ('status', 'runs', 'family_prior')}), flush=True)


def run():
    reg = json.loads((FOLDER/'REGISTRATION.json').read_bytes())
    if (FOLDER/'RESULT.json').exists() or (FOLDER/'RESULT_ARRAYS.npz').exists():
        raise FileExistsError('Preserve previous mixture result')
    for n, h in reg['hashes'].items():
        if se.sha(se.ROOT/n) != h:
            raise ValueError('Registered mixture input changed: '+n)
    # Check completion before loading any large arrays. A progress file is not
    # evidence of a completed run; missing output stays a visible failure.
    for name in reg['runs'].values():
        for required in ('RESULT.json', 'DENSITY_AUDIT.json'):
            if not (se.ROOT/name/required).is_file():
                raise FileNotFoundError('Mixture is not ready: '+name+'/'+required)
    results, stats_list, weight_list, logz_list, custody = [], [], [], [], {}
    seeds = []
    for family, name in reg['runs'].items():
        folder = se.ROOT/name
        stage_reg = json.loads((folder.parent/'REGISTRATION.json').read_bytes())
        for n, h in stage_reg['hashes'].items():
            if se.sha(se.ROOT/n) != h:
                raise ValueError('Source-stage registration changed: '+n)
        density = json.loads((folder/'DENSITY_AUDIT.json').read_bytes())
        if (density['status'] != 'PASS_TRANSPORT_DENSITY_NOT_PRECISION' or
                density['hashes']['RESULT.json'] != se.sha(folder/'RESULT.json')):
            raise ValueError('Missing matching source-density audit')
        result, u, logq, inside, values, stats = load_run(folder)
        if (result['family'] != family or
                result['transport_registration_sha256'] != se.sha(folder.parent/'REGISTRATION.json')):
            raise ValueError('Family/run registration mismatch')
        total = stats['logz']+np.log(len(u))
        values -= logq[:, None]
        values -= total[None, :]
        np.exp(values, out=values)
        # Each component sums to one. Outside-support rows remain exactly zero.
        if np.any(values[~inside] != 0):
            raise ValueError('A rejected proposal acquired nonzero target weight')
        weight_list.append(values)
        logz_list.append(stats['logz'])
        stats_list.append(stats)
        results.append(result)
        seeds.append(result['seed'])
        for n in ('RESULT.json', 'DENSITY_AUDIT.json', 'RESULT_ARRAYS.npz'):
            custody[name+'/'+n] = se.sha(folder/n)
        del u, logq, inside
    if len(set(seeds)) != len(seeds):
        raise ValueError('Independent family draws require distinct registered seeds')
    mixed = mix_statistics(np.asarray(logz_list), weight_list, list(reg['family_prior'].values()))
    masks = [source_precision_mask(s) for s in stats_list]
    labels = json.loads((se.ROOT/'INJECTIONS.json').read_bytes())['labels']
    if len(mixed['lnB']) != len(labels):
        raise ValueError('Label count differs from evidence components')
    rows = []
    noise_sets = []
    for label in labels:
        cell = {k: label[k] for k in ('psd', 'source', 'injection_family', 'injection_a', 'snr')}
        if any(r['cell'] == cell for r in rows):
            continue
        ids = np.array([i for i, v in enumerate(labels) if all(v[k] == x for k, x in cell.items())])
        noises = [labels[i]['noise_index'] for i in ids]
        if len(noises) != 50 or len(set(noises)) != 50:
            raise ValueError('Cell must contain the registered 50 separate noise intervals')
        noise_sets.append(set(noises))
        summaries = {}
        for name, stat in list(zip(reg['runs'], stats_list))+[('EQUAL_FAMILY_MIXTURE', mixed)]:
            values = stat['lnB'][ids]
            summaries[name] = dict(mean=float(values.mean()), sd_over_noise=float(values.std(ddof=1)),
                quantiles_05_50_95=np.quantile(values, [.05, .5, .95]).tolist(),
                max_delta_method_MC_sd=float(stat['lnB_MC_sd'][ids].max()))
        all_source = np.logical_and.reduce([m[ids] for m in masks])
        rows.append(dict(cell=cell, N=50, summaries=summaries,
            passing_individual_precision={f: int(m[ids].sum()) for f, m in zip(reg['runs'], masks)},
            passing_both_family_precision=int(all_source.sum()),
            passing_both_and_mixture_MC=int(np.sum(all_source & (mixed['lnB_MC_sd'][ids] <= .2))),
            accepted=False))
    if any(s != noise_sets[0] for s in noise_sets):
        raise ValueError('Unexpected noise-pairing mismatch')
    se.save_arrays(FOLDER/'RESULT_ARRAYS.npz', **mixed)
    output = dict(status='TWO_FAMILY_SOURCE_MIXTURE_PILOT_NOT_ACCEPTED',
        date_utc=datetime.now(timezone.utc).isoformat(), rows=rows,
        family_prior=reg['family_prior'], independent_noise_indices=sorted(noise_sets[0]),
        all_both_family_precision=bool(np.logical_and.reduce(masks).all()),
        scientific_acceptance=False, independent_repeat_complete=False,
        continuous_strength_calibration_complete=False,
        caveats=['Low-ESS delta-method errors are not reliable uncertainty estimates.',
                 '1200 mocks reuse 50 paired noise intervals; they are not 1200 events.',
                 'SNR40 is normalized separately for each PSD; this is not a fixed-distance O4/O5 yield forecast.',
                 'Equal-family mixture spans only these two approximants, not all waveform uncertainty.',
                 'No lnB-to-sigma conversion or physical clock selection.'],
        registration_sha256=se.sha(FOLDER/'REGISTRATION.json'),
        arrays_sha256=se.sha(FOLDER/'RESULT_ARRAYS.npz'), input_hashes=custody)
    se.write(FOLDER/'RESULT.json', output)
    print(json.dumps({k: v for k, v in output.items() if k not in ('rows', 'input_hashes')}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['register', 'run'])
    args = parser.parse_args()
    register() if args.command == 'register' else run()
