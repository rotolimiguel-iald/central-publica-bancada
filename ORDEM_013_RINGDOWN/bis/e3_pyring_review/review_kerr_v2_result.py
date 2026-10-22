"""Read-only independent review of completed Kerr V2; no model or sampler import."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import time
import importlib.metadata
import sys

HERE = Path(__file__).resolve().parent
B = HERE.parents[1]
ROOT = B.parent
OUT = B / 'cache/E3_KERR220_CALIBRATION_V2'
RUN = OUT / 'public_psd'
checks, pins = [], {}
started, cpu = time.perf_counter(), time.process_time()


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''): h.update(chunk)
    result = h.hexdigest()
    pins[str(path)] = result
    return result


def load(path):
    def pairs(items):
        d = {}
        for k,v in items:
            if k in d: raise ValueError('duplicate key')
            d[k] = v
        return d
    def bad(v): raise ValueError('nonfinite JSON')
    sha(path)
    return json.loads(path.read_bytes(), object_pairs_hook=pairs, parse_constant=bad)


def check(name, ok):
    checks.append(dict(name=name, passed=bool(ok)))
    if not ok: raise ValueError('REVIEW_BLOCKED:' + name)


def close(a, b):
    return math.isclose(float(a), float(b), rel_tol=2e-12, abs_tol=2e-12)


def dt(value): return datetime.fromisoformat(value)


def quantile(a, p):
    ordered = sorted(map(float, a))
    position = (len(ordered)-1)*p
    low = math.floor(position); high = math.ceil(position)
    return ordered[low] + (ordered[high]-ordered[low])*(position-low)


def variance(a):
    mean = math.fsum(map(float,a))/len(a)
    return math.fsum((float(x)-mean)**2 for x in a)/(len(a)-1)


def covariance(a, b):
    ma = math.fsum(map(float,a))/len(a); mb = math.fsum(map(float,b))/len(b)
    cross = math.fsum((float(x)-ma)*(float(y)-mb) for x,y in zip(a,b))/(len(a)-1)
    return [[variance(a),cross],[cross,variance(b)]]


def ks(a, b):
    from bisect import bisect_right
    x, y = sorted(map(float,a)), sorted(map(float,b))
    return max(abs(bisect_right(x,v)/len(x)-bisect_right(y,v)/len(y)) for v in sorted(set(x+y)))


manifest_path=B/'bis/e3_kerr_continuation/MANIFEST.json'
manifest=load(manifest_path); cfg=load(manifest_path.with_name('CONFIG.json'))
review=load(HERE/'KERR_CONTINUATION_REVIEW.json')
check('closed_delta',review['status']=='KERR_CONTINUATION_DELTA_CLOSED' and review['blocking_findings']==[])
check('manifest_review_pin',sha(manifest_path)==review['manifest_sha256'])
for name, expected in manifest['code_sha256'].items():
    check('runtime_source:'+name,sha(manifest_path.parent/name)==expected)
for name, expected in manifest['source_and_config_pins'].items():
    path=ROOT/name
    check('confined_pin:'+name, path.resolve().is_relative_to(ROOT.resolve()))
    check('source_pin:'+name,sha(path)==expected)
runtime=load(B/'bis/E2_SCIENTIFIC_RUNTIME_MANIFEST.json')
check('python_executable_pin',sha(Path(runtime['python_executable']))==runtime['python_executable_sha256'])
for name, item in runtime['files'].items():
    check('installed_runtime_pin:'+name,sha(Path(name))==item['sha256'])
for name, version in runtime['distributions'].items():
    check('distribution:'+name,importlib.metadata.version(name)==version)

auth_path=B/'bis/E3_KERR_AUTHORIZATION_V2.json'
auth=load(auth_path); launch=load(B/'bis/E3_KERR_LAUNCH_V2.json')
env=load(OUT/'ENVELOPE.json'); cost=load(OUT/'COST.json')
context=load(RUN/'CONTEXT.json'); claim=load(RUN/'CLAIM.json')
controller=load(RUN/'CONTROLLER.json'); conv=load(RUN/'CONVERGENCE.json')
conditioning=load(RUN/'CONDITIONING.json')
check('authorizer_review_pin',sha(B/'refeito/activate_kerr_continuation_013bis.py')==review['authorizer_sha256']==auth['authorizer_sha256'])
check('review_auth_pin',auth['review_sha256']==sha(HERE/'KERR_CONTINUATION_REVIEW.json'))
check('authorization_receipts',sha(auth_path)==launch['authorization_sha256']==env['authorization_sha256'])
check('manifest_receipts',all(x['manifest_sha256']==sha(manifest_path) for x in (auth,env,cost,context,claim)))
check('claim_context',claim['context_sha256']==sha(RUN/'CONTEXT.json'))
check('claim_pid_group',claim['pid']==controller['cleanup']['pgid'])
check('registration',auth['E2_registration_sha256']==launch['registration_sha256']==sha(B/'RINGDOWN_5SIGMA_V1.json'))
old=B/'cache/E3_KERR220_CALIBRATION_V1'
oldenv=load(old/'ENVELOPE.json'); oldcost=load(old/'COST.json')
check('parent_auth',auth['parent_authorization_sha256']==sha(B/'bis/E3_KERR_AUTHORIZATION_V1.json'))
check('parent_cost',auth['parent_cost_sha256']==sha(old/'COST.json'))
check('parent_envelope',auth['original_envelope_sha256']==sha(old/'ENVELOPE.json'))
check('original_deadline',len({oldenv['stop_utc'],env['stop_utc'],auth['valid_until_utc'],launch['original_absolute_deadline'],manifest['original_envelope_stop_utc']})==1)
check('time_order',dt(auth['approved_utc'])<dt(env['started_utc'])<dt(launch['finished_utc'])<dt(context['stop_utc'])<=dt(env['stop_utc']))
check('variant_stop',abs((dt(context['stop_utc'])-dt(env['started_utc'])).total_seconds()-1800)<1)
check('one_completed_run',cost['runs']==[controller] and cost['cleanup']==controller['cleanup'])
check('runtime_wall_bound',0<controller['wall_seconds']<cfg['variant_wall_seconds']['public_psd'])
check('cost_order',0<conv['cost']['wall_seconds']<=controller['wall_seconds']<=cost['wall_seconds']<=launch['wall_seconds'])
from post_result_metadata_gate import evaluate
gate=evaluate(dict(launch=launch,controller=controller,convergence=conv,
                  failure_file_present=(RUN/'FAILURE.json').exists(),partial_status_file_present=(RUN/'STATUS.json').exists()),cfg['sampler'])
check('prepared_metadata_gate',gate['issues']==[])
check('conditioning_detectors',sorted(x['detector'] for x in conditioning['receipts'])==sorted(cfg['detectors']))
for rec in conditioning['receipts']:
    detector=rec['detector']
    check('condition_finite:'+detector,math.isfinite(rec['covariance_condition_number']) and 0<rec['covariance_condition_number']<1e12)
    check('conditioning_pins:'+detector,rec['onsource_sha256']==cfg['data'][detector]['onsource_sha256'] and rec['psd']['source_sha256']==cfg['public_psd'][detector]['sha256'])
    check('native_grid:'+detector,rec['sample_count']==819 and close(rec['sample_count_over_fs'],819/cfg['sample_rate_hz']) and 0<=rec['start_grid_residual_s']<1/cfg['sample_rate_hz'])

# Only now inspect HDF5 terminal/weights, before posterior samples.
import h5py
import numpy as np
h5path=RUN/'Kerr220_result.hdf5'; sha(h5path)
def safe(file,path):
    node=file
    for part in path.split('/'):
        check('hard_link:'+path+':'+part,isinstance(node.get(part,getlink=True),h5py.HardLink))
        node=node[part]
    check('infile_dataset:'+path,isinstance(node,h5py.Dataset) and not node.is_virtual and not node.external)
    return node
def scalar(file,path):
    node=safe(file,path); check('scalar:'+path,node.shape==())
    value=node[()]
    if isinstance(value,bytes):return value.decode('utf-8')
    return value.item() if hasattr(value,'item') else value

summary={}; borders={}
with h5py.File(h5path,'r') as h:
    terminal={key:scalar(h,'meta_data/e2_terminal/'+key) for key in ('before_add_live','delta_logz','ncall','status','threshold')}
    check('raw_terminal_pre_live',terminal['before_add_live'] is True)
    check('raw_terminal_status',terminal['status']=='DLOGZ_REACHED_REQUIRES_ESS')
    for key in ('delta_logz','ncall','threshold'):check('raw_terminal:'+key,terminal[key]==conv[key])
    check('raw_ncall',scalar(h,'num_likelihood_evaluations')==conv['ncall_reported'])
    for key in ('log_evidence','log_evidence_err'):check('raw_'+key,close(scalar(h,key),conv[key]))
    weights=np.asarray(safe(h,'nested_samples/weights')[...],float)
    check('weights_valid',weights.ndim==1 and len(weights)>0 and np.isfinite(weights).all() and (weights>=0).all() and weights.sum()>0)
    ess=math.fsum(map(float,weights))**2/math.fsum(float(x)**2 for x in weights)
    check('independent_ESS',close(ess,conv['ess']) and ess>=cfg['sampler']['minimum_effective_samples'])
    comparison=load(RUN/'COMPARISON.json'); npzpath=RUN/'PAIRED_POSTERIOR.npz'
    check('paired_hash',sha(npzpath)==comparison['posterior_sha256'])
    keys=list(cfg['priors'])
    check('comparison_parameter_order',comparison['parameter_order']==keys)
    with np.load(npzpath,allow_pickle=False) as archive:
        check('eight_paired_columns',set(archive.files)==set(keys) and len(archive.files)==8)
        own={k:archive[k].copy() for k in keys}
    for key,a in own.items():
        check('paired_shape:'+key,a.shape==(conv['posterior_samples'],) and np.isfinite(a).all())
        check('raw_pair_equality:'+key,np.array_equal(a,safe(h,'posterior/'+key)[...]))
        low,high=cfg['priors'][key]
        check('prior_support:'+key,((a>=low)&(a<=high)).all())
        borders[key]=dict(min=float(a.min()),max=float(a.max()),
                         fraction_lower_1pct=float(np.mean(a<low+.01*(high-low))),
                         fraction_upper_1pct=float(np.mean(a>high-.01*(high-low))),
                         boundary_diagnostic='Descriptive 1% of INPUT prior width; circular phases have identified endpoints')
    check('N_comparison',comparison['samples']==len(own['Mf'])==conv['posterior_samples'])
    rawmeta_keys=list(h['meta_data'].keys())
    rawpriors=json.loads(scalar(h,'priors'))
    for key in keys:
        parameters=rawpriors[key]['kwargs']
        check('raw_prior:'+key,parameters['minimum']==cfg['priors'][key][0] and parameters['maximum']==cfg['priors'][key][1])

reference=ROOT/cfg['reference_posterior_path']
check('reference_pin',sha(reference)==cfg['reference_posterior_sha256'])
ref=np.genfromtxt(reference,names=True,usecols=('Mf','af'))
check('reference_valid',ref.ndim==1 and len(ref)>1 and all(np.isfinite(ref[k]).all() for k in ('Mf','af')))
for key in ('Mf','af'):
    a,b=own[key],ref[key]
    qa=[quantile(a,p) for p in (.05,.5,.95)];qb=[quantile(b,p) for p in (.05,.5,.95)]
    sa,sb=math.sqrt(variance(a)),math.sqrt(variance(b))
    result=dict(own_05_50_95=qa,released_05_50_95=qb,own_std_ddof1=sa,released_std_ddof1=sb,
                median_difference=qa[1]-qb[1],difference_over_quadrature_width=(qa[1]-qb[1])/math.hypot(sa,sb),
                overlap_90pct=max(qa[0],qb[0])<=min(qa[2],qb[2]),marginal_KS_distance=ks(a,b))
    for field,value in result.items():
        expected=comparison['comparison'][key][field]
        valid=all(close(x,y) for x,y in zip(value,expected)) if isinstance(value,list) else (value==expected if isinstance(value,bool) else close(value,expected))
        check('independent_summary:'+key+':'+field,valid)
    summary[key]=result
for name,a,b in [('own',own['Mf'],own['af']),('reference',ref['Mf'],ref['af'])]:
    observed=covariance(a,b); expected=comparison[name+'_Mf_af_covariance_ddof1']
    check('covariance:'+name,all(close(observed[i][j],expected[i][j]) for i in range(2) for j in range(2)))
check('comparison_not_equivalence',comparison['equivalent_reproduction_paid'] is False and comparison['z_calibrated'] is None)
check('convergence_agrees_comparison',comparison['convergence']=={k:v for k,v in conv.items() if k!='cost'})
check('final_cost_order',conv['cost']['wall_seconds']<=comparison['cost']['wall_seconds']<=controller['wall_seconds'])
for path, expected in list(pins.items()):
    check('unchanged_during_review:'+path,sha(Path(path))==expected)
report=dict(status='KERR_V2_NONBLIND_CALIBRATION_REVIEWED_WITH_LIMITATIONS',blocking_findings=[],
            created_utc=datetime.now(timezone.utc).isoformat(),check_count=len(checks),checks=checks,
            input_hashes=pins,manifest_sha256=sha(manifest_path),authorizer_sha256=review['authorizer_sha256'],
            convergence_review=dict(reported=conv,raw_terminal=terminal,independent_ess=ess,nested_weight_count=len(weights)),
            conditioning_review=conditioning,
            cost_review=dict(launch_wall_seconds=launch['wall_seconds'],controller_wall_seconds=cost['wall_seconds'],
                             children_cpu_seconds=cost['children_cpu_seconds'],runner_final=comparison['cost'],
                             V1_plus_V2_controller_wall_seconds=oldcost['wall_seconds']+cost['wall_seconds'],
                             V1_plus_V2_children_cpu_seconds=oldcost['children_cpu_seconds']+cost['children_cpu_seconds'],
                             original_deadline=env['stop_utc'],finished_utc=launch['finished_utc'],cleanup=controller['cleanup']),
            posterior_analysis=dict(own_N=len(own['Mf']),reference_N=len(ref),comparison=summary,prior_boundary_diagnostics=borders,
                                    raw_hdf5_metadata_keys=rawmeta_keys,paired_npz_sha256=sha(npzpath),raw_hdf5_sha256=sha(h5path)),
            nonblocking_notes=[
                'HDF5 meta_data does not embed manifest/mode supplied at run_sampler; external custody chain plus exact eight-column equality binds it to NPZ. No embedded pin claimed.',
                'CONDITIONING status CONTROL_PSD_NOT_IDENTICAL_RELEASE is an operational label: identity UNKNOWN, not demonstrated physical inequivalence.',
                'Pre-live chronology rests on pinned hook and stored terminal, not a new independent sampler replay.',
                '512 live points and one seed do not independently certify all modes.',
                'Likelihood counter increments after deadline guard; not all frontier entries. Counters are not equated.'
            ],
            limitations=cfg['limitations']+['Same-event descriptive comparison only; no physical z, Bayes factor or independent evidence.',
                'V1 partial posterior not opened. Welch failure remains and PSD robustness is not closed.',
                'Strain/conditioning not recomputed; hash correspondence of receipt only for onsource data.',
                'Cleanup is witnessed by controller receipt, not a new live process survey.'],
            scientific_execution=False,accepted_sample_analysis=True,physical_confirmation=False,equivalent_reproduction_paid=False,
            review_wall_seconds=time.perf_counter()-started,review_cpu_seconds=time.process_time()-cpu,
            script_sha256=sha(Path(__file__)))
target=HERE/'KERR_V2_POST_RESULT_REVIEW.json'
with target.open('xb') as f:f.write((json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8'))
print(json.dumps(dict(status=report['status'],checks=len(checks),receipt_sha256=sha(target),comparison=summary,
                     review_wall_seconds=report['review_wall_seconds']),indent=2))
