"""Registered second-family source recovery with the native SEOB phase adapter.

The learned Phenom proposal is only a computational starting distribution. Its
density is transported using SEOB's own remnant map and Jacobian; it never
becomes the physical prior. Every target keeps its separate integral.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
from datetime import datetime,timezone
import argparse
import copy
import json
import multiprocessing as mp
import time
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
import transport_phase_source as tp
from importance_source_evidence import importance_statistics
from native_seob_source_likelihood import phase_marginal_loglikes

STAGE=se.ROOT/'phase_native_seob'


def check():
    pm.check()
    registration=json.loads((STAGE/'REGISTRATION.json').read_bytes())
    for name,h in registration['hashes'].items():
        if se.sha(se.ROOT/name)!=h:
            raise ValueError('Native source registration changed: '+name)
    return json.loads((STAGE/'PROPOSAL.json').read_bytes())


def register():
    pm.check()
    validation=json.loads((se.ROOT/'native_source_integral_validation/RESULT.json').read_bytes())
    if validation['status']!='PASS_NATIVE_SOURCE_INTEGRAL':
        raise ValueError('Source integral equivalence failed')
    for directory in ('native_source_integral_validation','native_seob_phase_validation'):
        reg=json.loads((se.ROOT/directory/'REGISTRATION.json').read_bytes())
        for name,h in reg['hashes'].items():
            if se.sha(se.ROOT/name)!=h:
                raise ValueError('Validated input changed: '+name)
    proposal=copy.deepcopy(json.loads((se.ROOT/'phase_ringdown_balanced/PROPOSAL.json').read_bytes()))
    proposal.update(family='SEOBNRv4HM',training_recovery_family='IMRPhenomXPHM',
        transferred_proposal_only=True,physical_prior_changed=False,
        caveat='Starting proposal transferred in frequency/damping coordinates. Its fit to SEOB posterior is unproven. SEOB map/Jacobian used at every draw.')
    STAGE.mkdir(exist_ok=False); se.write(STAGE/'PROPOSAL.json',proposal)
    names=['run_native_seob_source.py','native_seob_source_likelihood.py','native_seob_phase_source.py',
        'direct_seob_modes.py','stable_peak_phase_source.py','stable_peak_imr_model.py',
        'source_evidence.py','importance_source_evidence.py','transport_phase_source.py','ringdown_source_coordinates.py',
        'phase_marginal_source.py','phase_runs/REGISTRATION.json','native_source_integral_validation/REGISTRATION.json',
        'native_source_integral_validation/RESULT.json','RINGDOWN_COORDINATES_VALIDATION.json',
        'phase_ringdown_balanced/PROPOSAL.json','phase_native_seob/PROPOSAL.json','INJECTIONS.npz']
    reg=dict(status='REGISTERED_NATIVE_SEOB_SOURCE_INTEGRATION',date_utc=datetime.now(timezone.utc).isoformat(),
        family='SEOBNRv4HM',draws=2048,seed=130901,oracle_seed=130900,
        inherited_physical_prior_registration_sha256=se.sha(se.REG),
        source_parameters_integrated=7,source_parameters_sampled=6,shared_amplitudes_integrated=2,
        physical_prior_changed=False,physical_clock_selected=False,C6_changed=False,
        waveform_refinement='Phase-zero peak plus all native SEOB41 modes; every source point checked at three held-out phases against ORIGINAL complete waveform before phase quadrature',
        accuracy=dict(max_relative_waveform_error=1e-6,max_logL_interpolation_error=.001,max_phase_quadrature_error=1e-5),
        validation_max_logL_integral_error=validation['max_logL_integral_error'],
        validation_timing_caveat='Equivalence test calls the original first; cache can accelerate held-out controls afterward. Its timing is not a clean production speed benchmark.',
        acceptance='Component ESS100, maxweight.05, MCsdlnB.2, independent repetition, template-rate controls and continuous-strength bias/coverage; none waived',
        hashes={n:se.sha(se.ROOT/n) for n in names})
    se.write(STAGE/'REGISTRATION.json',reg)
    print(json.dumps({k:reg[k] for k in ('status','family','draws','seed','validation_max_logL_integral_error')}),flush=True)


def oracle():
    proposal=check(); s=tp.draw(proposal,32768,130900)
    w=np.zeros(len(s['inside'])); w[s['inside']]=np.exp(-s['logq'][s['inside']])
    u=s['unit_cube']; values=np.column_stack([w]+[w*u[:,i] for i in range(6)]+[w*u[:,i]**2 for i in range(6)])
    expected=np.array([1.]+[.5]*6+[1/3]*6)
    mean=values.mean(axis=0); sd=values.std(axis=0,ddof=1)/np.sqrt(len(w)); z=np.abs(mean-expected)/sd
    output=dict(status='PASS_TRANSPORT_PROPOSAL_MOMENTS' if z.max()<5 else 'PROPOSAL_MOMENTS_FAILED',
        seed=130900,draws=len(w),inside=int(s['inside'].sum()),family=proposal['family'],mean=mean.tolist(),
        expected=expected.tolist(),MC_standard_errors=sd.tolist(),max_standardized_error=float(z.max()),
        scientific_acceptance=False,registration_sha256=se.sha(STAGE/'REGISTRATION.json'))
    se.write(STAGE/'PROPOSAL_ORACLE.json',output); print(json.dumps(output),flush=True)
    if z.max()>=5:
        raise ValueError('Second-family proposal normalization failed')


def evaluate(item):
    index,u=item
    value,meta=phase_marginal_loglikes('SEOBNRv4HM',u,se._STATE)
    return index,value,meta


def run(args):
    proposal=check()
    oracle_result=json.loads((STAGE/'PROPOSAL_ORACLE.json').read_bytes())
    if oracle_result['status']!='PASS_TRANSPORT_PROPOSAL_MOMENTS':
        raise ValueError('Proposal is not validated')
    folder=STAGE/f"SEOBNRv4HM_seed{args.seed}_N{args.draws}"; folder.mkdir(exist_ok=False)
    s=tp.draw(proposal,args.draws,args.seed); se.save_arrays(folder/'PROPOSALS.npz',**s)
    se.write(folder/'START.json',dict(date_utc=datetime.now(timezone.utc).isoformat(),family='SEOBNRv4HM',
        seed=args.seed,draws=args.draws,processes=args.processes,transport_registration_sha256=se.sha(STAGE/'REGISTRATION.json'),
        inherited_phase_registration_sha256=se.sha(pm.REG),proposal_sha256=se.sha(STAGE/'PROPOSAL.json'),physical_prior_changed=False))
    jobs=[(int(i),s['unit_cube'][i]) for i in np.flatnonzero(s['inside'])]
    values=np.full((args.draws,2400),-np.inf); chunk=[]; metadata=[]; done=0; number=0; start=time.monotonic()
    with mp.get_context('fork').Pool(args.processes,initializer=se.initialize,initargs=('SEOBNRv4HM',)) as pool:
        for index,value,meta in pool.imap_unordered(evaluate,jobs,chunksize=1):
            values[index]=value; chunk.append((index,value)); metadata.append(dict(index=index,**meta)); done+=1
            if len(chunk)==16 or done==len(jobs):
                se.save_arrays(folder/f'chunk_{number:05d}.npz',indices=np.array([c[0] for c in chunk]),components=np.stack([c[1] for c in chunk]))
                chunk=[]; number+=1
                progress=dict(done=done,valid_draws=len(jobs),seconds=time.monotonic()-start,date_utc=datetime.now(timezone.utc).isoformat())
                se.write(folder/'PROGRESS.json',progress,replace=True); print(json.dumps(progress),flush=True)
    stats=importance_statistics(values,s['logq']); se.save_arrays(folder/'RESULT_ARRAYS.npz',**stats)
    good=(np.minimum(stats['ESS'][:1200],stats['ESS'][1200:])>=100)&(np.maximum(stats['max_weight'][:1200],stats['max_weight'][1200:])<=.05)&(stats['lnB_MC_sd']<=.2)
    labels=se.load_state()['labels']; rows=[]
    for label in labels:
        cell={k:label[k] for k in ('psd','source','injection_family','injection_a','snr')}
        if any(r['cell']==cell for r in rows):continue
        ids=np.array([i for i,l in enumerate(labels) if all(l[k]==v for k,v in cell.items())]); both=np.r_[ids,1200+ids]
        ll=stats['lnB'][ids]
        rows.append(dict(cell=cell,N=len(ids),lnB_mean=float(ll.mean()),lnB_sd_noise=float(ll.std(ddof=1)),
            lnB_quantiles=np.quantile(ll,[.05,.5,.95]).tolist(),min_component_ESS=float(stats['ESS'][both].min()),
            max_weight=float(stats['max_weight'][both].max()),max_lnB_MC_sd=float(stats['lnB_MC_sd'][ids].max()),draws_passing_precision=int(good[ids].sum())))
    output=dict(status='NATIVE_SEOB_SOURCE_PILOT_NOT_ACCEPTED',family='SEOBNRv4HM',seed=args.seed,
        draws=args.draws,evaluations=done,rows=rows,integration_controls=metadata,all_precision_pass=bool(good.all()),
        draws_passing_precision=int(good.sum()),ESS_range=[float(stats['ESS'].min()),float(stats['ESS'].max())],
        source_parameters_integrated=7,source_parameters_sampled=6,physical_prior_changed=False,original_C6_changed=False,
        registration_sha256=se.sha(pm.REG),transport_registration_sha256=se.sha(STAGE/'REGISTRATION.json'),
        waveform_revision='NATIVE_PHASE_ZERO_WITH_ORIGINAL_HELDOUT_CONTROLS',independent_repeat=False,
        scientific_acceptance=False,hashes={p.name:se.sha(p) for p in folder.glob('*.npz')})
    se.write(folder/'RESULT.json',output)
    print(json.dumps({k:output[k] for k in ('status','draws','evaluations','draws_passing_precision','ESS_range')}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['register','oracle','run'])
    p.add_argument('--draws',type=int,default=2048);p.add_argument('--seed',type=int,default=130901);p.add_argument('--processes',type=int,default=2)
    args=p.parse_args()
    if args.command=='register':register()
    elif args.command=='oracle':oracle()
    else:run(args)
