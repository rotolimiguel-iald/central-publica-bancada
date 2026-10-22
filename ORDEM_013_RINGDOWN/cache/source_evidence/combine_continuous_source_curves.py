"""Registered model averaging of COMPLETE continuous source integrals only."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
import argparse
from datetime import datetime, timezone
import json
import numpy as np
import source_evidence as se
import run_continuous_source_curves as curves
from continuous_source_calibration import read_curves
from continuous_family_mixture import mix_curves

STAGE=se.ROOT/'continuous_source_family_combination'
FAMILIES=('IMRPhenomXPHM','SEOBNRv4HM')


def register():
    validation_path=se.ROOT/'continuous_family_mixture_validation/RESULT.json'
    validation=json.loads(validation_path.read_bytes())
    if validation['status']!='PASS_CONTINUOUS_FAMILY_MIXTURE_ARITHMETIC':
        raise ValueError('Continuous mixture arithmetic is not validated')
    regpath=validation_path.parent/'REGISTRATION.json'
    if validation['registration_sha256']!=se.sha(regpath):
        raise ValueError('Wrong arithmetic validation registration')
    for name,digest in json.loads(regpath.read_bytes())['hashes'].items():
        if se.sha(se.ROOT/name)!=digest:
            raise ValueError('Validated mixture input changed')
    names=['combine_continuous_source_curves.py','continuous_family_mixture.py',
        'source_family_mixture.py','continuous_source_calibration.py','tgl_ringdown_likelihood.py',
        'continuous_family_mixture_validation/RESULT.json','continuous_family_mixture_validation/REGISTRATION.json',
        'run_continuous_source_curves.py','audit_continuous_endpoints.py','INJECTIONS.json','INJECTIONS.npz']
    inputs={}
    seeds=[]
    for family in FAMILIES:
        folder,reg=curves.check(family)
        inputs[family]=str(folder.relative_to(se.ROOT))
        source=se.ROOT/reg['source_run']
        source_start=json.loads((source/'START.json').read_bytes())
        seeds.append(source_start['seed'])
        names += [str((folder/'REGISTRATION.json').relative_to(se.ROOT)),
                  str((source/'PROPOSALS.npz').relative_to(se.ROOT)),
                  str((source/'START.json').relative_to(se.ROOT))]
    if len(set(seeds))!=len(seeds):
        raise ValueError('Different families require independent registered source draws')
    STAGE.mkdir(exist_ok=False)
    reg=dict(status='REGISTERED_CONTINUOUS_TWO_FAMILY_MIXTURE',date_utc=datetime.now(timezone.utc).isoformat(),
        runs=inputs,family_prior={family:.5 for family in FAMILIES},
        family_prior_scope='Same explicit equal conditional model prior at every strength; not derived from TGL',
        formula='Z(a)=sum_f prior(f)*Z_f(a). Reuse centered within-family paired covariance, independent between families.',
        strengths=curves.STRENGTHS.tolist(),strength_prior_selected=False,
        prerequisites=['Complete continuous results and hashed arrays',
            'Full binary/continuous endpoint audits for both families',
            'Parent proposal density audits pinned to completed binary results'],
        interpretation='Diagnostic LR90 intervals of nuisance-marginal model-averaged likelihood; empirical bias/coverage required',
        scope='R-B,SNR40,O4/O5;all1200 frozen mocks,50 reused noises. Other readings/SNR remain in full objective.',
        precision='Both individual families must pass at every strength; mixture MCsd<=0.2. No imprecise family may be hidden.',
        repeat_and_rate_scope='Not paid by arithmetic or averaging; independent continuous repeats and rate/grid controls still required',
        binomial_coverage='Do not treat1200 mocks as independent events; report cells separately by source/injection family/a/PSD/SNR',
        C6_changed=False,scientific_acceptance=False,
        hashes={n:se.sha(se.ROOT/n) for n in names})
    se.write(STAGE/'REGISTRATION.json',reg)
    print(json.dumps({k:reg[k] for k in ('status','runs','family_prior')}),flush=True)


def completed_endpoint_audit(folder,reg):
    candidates=[]
    for path in sorted((folder/'endpoint_audits').glob('*/RESULT.json')):
        report=json.loads(path.read_bytes())
        if report['status']=='PASS_FULL_ENDPOINT_COMPARISON' and report['full_comparison_complete']:
            candidates.append((path,report))
    if not candidates:
        raise FileNotFoundError('No full endpoint audit: '+str(folder))
    path,report=candidates[-1]
    source=se.ROOT/reg['source_run']
    if (report['continuous_registration_sha256']!=se.sha(folder/'REGISTRATION.json') or
            report['proposal_draws_sha256']!=se.sha(source/'PROPOSALS.npz') or
            report['matched_binary_points']!=reg['inside_draws'] or
            report['unmatched_points_pending'] or report['max_abs_logL_difference']>2e-5):
        raise ValueError('Full endpoint audit does not cover these runs')
    for name,digest in report['continuous_checkpoint_hashes'].items():
        if se.sha(folder/name)!=digest:
            raise ValueError('Continuous endpoint checkpoint changed')
    for name,digest in report['binary_checkpoint_hashes'].items():
        if se.sha(source/name)!=digest:
            raise ValueError('Binary endpoint checkpoint changed')
    return path


def run():
    reg=json.loads((STAGE/'REGISTRATION.json').read_bytes())
    if (STAGE/'RESULT.json').exists() or (STAGE/'RESULT_ARRAYS.npz').exists():
        raise FileExistsError('Preserve previous mixture result')
    for name,digest in reg['hashes'].items():
        if se.sha(se.ROOT/name)!=digest:
            raise ValueError('Registered mixture input changed: '+name)
    # Missing completed outputs are visible failures, before loading gigabytes.
    for name in reg['runs'].values():
        for required in ('RESULT.json','RESULT_ARRAYS.npz','CURVES.npy','EVALUATIONS_COMPLETE.json'):
            if not (se.ROOT/name/required).is_file():
                raise FileNotFoundError('Continuous mixture is not ready: '+name+'/'+required)
    data,qs,stats,custody=[],[],[],{}
    for family,name in reg['runs'].items():
        folder,own=curves.check(family)
        if str(folder.relative_to(se.ROOT))!=name:
            raise ValueError('Continuous family path changed')
        result=json.loads((folder/'RESULT.json').read_bytes())
        if (result['family']!=family or result['registration_sha256']!=se.sha(folder/'REGISTRATION.json') or
                result['arrays_sha256']!=se.sha(folder/'RESULT_ARRAYS.npz') or
                result['curves_sha256']!=se.sha(folder/'CURVES.npy') or
                result['complete_evaluations_sha256']!=se.sha(folder/'EVALUATIONS_COMPLETE.json')):
            raise ValueError('Continuous result custody changed')
        audit_path=completed_endpoint_audit(folder,own)
        source=se.ROOT/own['source_run']
        density=json.loads((source/'DENSITY_AUDIT.json').read_bytes())
        if (density['status']!='PASS_TRANSPORT_DENSITY_NOT_PRECISION' or
                density['hashes']['RESULT.json']!=se.sha(source/'RESULT.json')):
            raise ValueError('Matching proposal density audit required')
        array=np.load(folder/'CURVES.npy',mmap_mode='r')
        if array.shape!=(own['draws'],len(curves.STRENGTHS),own['targets']):
            raise ValueError('Continuous cube has wrong dimensions')
        with np.load(source/'PROPOSALS.npz') as archive:
            q,inside=archive['logq'].copy(),archive['inside'].copy()
        for first in range(0,len(inside),128):
            valid=inside[first:first+128]
            block=array[first:first+128]
            if not np.isneginf(block[~valid]).all() or not np.isfinite(block[valid]).all():
                raise ValueError('Cemetery/finite-integrand convention changed')
        with np.load(folder/'RESULT_ARRAYS.npz') as archive:
            if not np.array_equal(archive['strengths'],curves.STRENGTHS):
                raise ValueError('Family strength grid differs')
            statistics={k:archive[k].copy() for k in archive.files if k!='strengths'}
        data.append(array);qs.append(q);stats.append(statistics)
        for path in (folder/'RESULT.json',folder/'RESULT_ARRAYS.npz',folder/'CURVES.npy',
                     source/'DENSITY_AUDIT.json',audit_path):
            custody[str(path.relative_to(se.ROOT))]=se.sha(path)
    mixed=mix_curves(curves.STRENGTHS,data,qs,stats,list(reg['family_prior'].values()))
    report=read_curves(curves.STRENGTHS,mixed,se.load_state()['labels'])
    report.update(status='CONTINUOUS_TWO_FAMILY_CALIBRATION_DIAGNOSTIC',
        date_utc=datetime.now(timezone.utc).isoformat(),family_prior=reg['family_prior'],
        input_hashes=custody,registration_sha256=se.sha(STAGE/'REGISTRATION.json'),
        scientific_acceptance=False,independent_continuous_repeat=False,
        continuous_waveform_rate_audit=False,C6_changed=False)
    se.save_arrays(STAGE/'RESULT_ARRAYS.npz',strengths=curves.STRENGTHS,**mixed)
    report['arrays_sha256']=se.sha(STAGE/'RESULT_ARRAYS.npz')
    se.write(STAGE/'RESULT.json',report)
    print(json.dumps(dict(status=report['status'],usable_curves=sum(r['numerically_usable'] for r in report['curves']),
        local_calibration_cells=sum(r['numerical_and_local_calibration_pass'] for r in report['cells']))),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=('register','run'))
    args=parser.parse_args()
    register() if args.command=='register' else run()
