"""Independent post-extraction review. Requires a later explicit principal GO.

No production imports, extraction output, waveform, PE, fitting or Monte Carlo.
Reads the five registered HDF5 columns only after E6/GO custody checks.
"""
import os
for _key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[_key]='1'
import argparse
import hashlib
import json
import math
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
B=HERE.parents[1]
ROOT=B.parent
FIELDS=('df220','dtau220','Mfdet','af','z')
READINGS=('R-A','R-B','R-MOD','R-RAIZ-0','R-RAIZ-EP4','R-RAIZ-REST','R-RAIZ-COHERENT','R-LIN','R-GLOBAL','R-PROP')
STOP=None
CHECKS=[]

def tick():
    if STOP is not None and time.monotonic()>=STOP:raise TimeoutError('Independent review wall cap')
def ck(name,condition):
    tick();CHECKS.append({'name':name,'passed':bool(condition)})
    if not condition:raise ValueError(name)
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):tick();h.update(block)
    return h.hexdigest()
def strict(path):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('Duplicate JSON key')
            out[k]=v
        return out
    def invalid(value):raise ValueError('Nonfinite JSON')
    def number(value):
        out=float(value)
        if not math.isfinite(out):raise ValueError('Nonfinite numeric token')
        return out
    return json.loads(path.read_bytes(),object_pairs_hook=pairs,parse_constant=invalid,parse_float=number)
def contained(rel):
    if not isinstance(rel,str) or Path(rel).is_absolute():raise ValueError('Relative Chatgpt path required')
    p=ROOT/rel
    if p.is_symlink() or not p.resolve().is_relative_to(ROOT.resolve()):raise ValueError('Unconfined input')
    return p
def utc(text):
    out=datetime.fromisoformat(text)
    if out.tzinfo is None:raise ValueError('Aware UTC required')
    return out
def new(path,value):
    raw=(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    with path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
def near(name,actual,expected,rtol=3e-10,atol=2e-12):
    ck(name,math.isfinite(float(actual)) and math.isclose(float(actual),float(expected),rel_tol=rtol,abs_tol=atol))
def moments(values):
    n=len(values);mean=math.fsum(map(float,values))/n
    variance=math.fsum((float(v)-mean)**2 for v in values)/(n-1)
    return mean,math.sqrt(variance)
def quantile(values,q):
    v=sorted(map(float,values));position=(len(v)-1)*q;lo=int(position);hi=min(lo+1,len(v)-1)
    return v[lo]+(position-lo)*(v[hi]-v[lo])

def review(args):
    global STOP
    started=datetime.now(timezone.utc);start=time.monotonic();cpu=time.process_time()
    STOP=start+600
    ck('WSL existing runtime',os.name=='posix' and Path(sys.prefix).resolve()==Path('/opt/lal_env'))
    ck('GO pin',sha(args.go)==args.go_sha256)
    go=strict(args.go)
    ck('explicit principal GO',go['status']=='GO_E7_REVIEW_AFTER_E6')
    ck('reviewer code pin',go['verifier_sha256']==sha(Path(__file__)))
    ck('GO aware nonfuture',utc(go['created_utc'])<=started)
    regpath=B/'RINGDOWN_5SIGMA_V1.json';reg=strict(regpath);regsha=sha(regpath)
    ck('GO parent E2',go['registration_sha256']==regsha)
    spec=reg['e7']
    budget=strict(B/'ORCAMENTO_40H.json');shared=strict(B/'bis/PART_B_BUDGET_START.json')
    hard=min(utc(budget['wall_accounting']['finalization_stop_utc']),utc(shared['hard_deadline_utc']))
    remaining=(hard-started).total_seconds()-10
    ck('time before payload',remaining>30)
    STOP=min(STOP,start+remaining)
    def timed_out(signum,frame):raise TimeoutError('Bounded review alarm')
    signal.signal(signal.SIGALRM,timed_out);signal.setitimer(signal.ITIMER_REAL,max(1,STOP-time.monotonic()))
    names=('e6_result','e6_review','authorization','execution_receipt','posterior','e7_result')
    paths={name:contained(go['inputs'][name]['relative_to_Chatgpt']) for name in names}
    # Hashing payload bytes occurs only after GO and deadline checks; no arrays yet.
    for name,p in paths.items():ck(name+' pin',sha(p)==go['inputs'][name]['sha256'])
    e6=strict(paths['e6_result']);er=strict(paths['e6_review']);auth=strict(paths['authorization']);ex=strict(paths['execution_receipt'])
    ck('E6 independently approved',er['approved'] is True and er['e6_result_sha256']==go['inputs']['e6_result']['sha256'])
    ck('E6 parent and schema',e6['registration_sha256']==regsha and e6['schema']=='E6_REACH_TABLE_V2')
    ck('authorization E6 bindings',auth['e6_result_sha256']==go['inputs']['e6_result']['sha256'] and auth['e6_review_sha256']==go['inputs']['e6_review']['sha256'])
    ck('authorization approved chronology',auth['status']=='AUTHORIZED_BY_PRINCIPAL_AFTER_E2' and utc(reg['registered_utc'])<=utc(auth['registered_utc'])<=utc(go['created_utc']))
    ck('authorization custody',auth['registration_sha256']==regsha and auth['plan_sha256']==spec['plan_sha256'] and auth['producer_tree_sha256']==spec['producer_tree_sha256'])
    ck('authorization allocation',auth['allocation_sha256']==sha(B/'ORCAMENTO_40H.json'))
    ck('execution success',ex['status']=='E7_EXECUTED_NO_PHYSICAL_TEST' and ex['failure'] is None)
    ck('execution auth',ex['authorization_sha256']==go['inputs']['authorization']['sha256'])
    for name in ('posterior','e7_result'):ck('execution product '+name,ex['products'][paths[name].name]['sha256']==go['inputs'][name]['sha256'])
    for name in ('plan','nuisance','prediction_source'):ck('registered '+name,sha(contained(spec[name+'_path']))==spec[name+'_sha256'])
    producer=contained(spec['producer_directory'])
    ck('producer complete tree',{p.relative_to(producer).as_posix():sha(p) for p in producer.rglob('*.py')}==spec['producer_tree_sha256'])
    plan=strict(contained(spec['plan_path']));entries=plan['events']
    ck('33 unique calibration',len(entries)==33 and len({e['event_id'] for e in entries})==33 and all(e['role']=='calibration' for e in entries))
    payload=strict(paths['posterior']);result=strict(paths['e7_result'])
    ck('payload schema',payload['schema']=='POSTERIORES_PSEOB_V1')
    for obj in (payload,result):
        ck('payload/result parent',obj['registration_sha256']==regsha)
        ck('payload/result auth',obj['authorization_sha256']==go['inputs']['authorization']['sha256'])
        ck('payload/result plan',obj['plan_sha256']==spec['plan_sha256'])
    ck('result posterior binding',result['posterior_sha256']==go['inputs']['posterior']['sha256'])
    ck('result nuisance binding',result['nuisance_sha256']==spec['nuisance_sha256'])
    ck('full ordered population',[e['event_id'] for e in payload['events']]==[e['event_id'] for e in entries])
    ck('result honest scope',result['status']=='PREPARED_FAIL_CLOSED_NO_PHYSICAL_TEST' and result['calibration_events']==33 and result['test_events_added']==0 and result['lnB'] is None and result['z_physical'] is None)
    ck('twenty matrix cells',len(result['matrix'])==20 and {(r['reading'],r['mode_variant']) for r in result['matrix']}=={(r,m) for r in READINGS for m in ('220_only','220_plus_440_INPUT')})
    for r in result['matrix']:
        ck('matrix '+r['reading']+r['mode_variant'],r['verdict']=='AWAITING_DATA' and r['systematic_gate']=='red' and r['lnB'] is None and r['z_physical'] is None and r['correction_over_sigma_physical'] is None)
        ck('target '+r['reading']+r['mode_variant'],r['N_target_information']==spec['readings'][r['reading']]['N_target_information'])
    import numpy as np
    import h5py
    full=result['fullsample_diagnostics'];summaries=full['events']
    ck('summary event order',[e['event_id'] for e in summaries]==[e['event_id'] for e in entries])
    ck('density and physical summaries unpaid',all(full[k] is None for k in ('lnB','z_physical','LRT_IV','sigma_pop_calibrated','split_null_p')))
    archive_hashes={};source_hashes={};row_count=0;event_reports=[]
    for entry,event,summary in zip(entries,payload['events'],summaries):
        tick();eid=entry['event_id'];n=entry['N_source'];row_count+=n
        for key in ('role','source_path','source_sha256','tar_path','tar_sha256','dataset','model','mass_frame','mass_unit'):
            ck(eid+' '+key,event[key]==entry[key])
        ck(eid+' count and full thinning',event['N']==event['N_source']==n and event['thinning']=={'factor':1,'seed':None,'method':'none'} and event['sample_weights']=='equal_as_stored')
        ck(eid+' fields mapping',event['source_field_mapping']==entry['fields'] and set(event['samples'])==set(FIELDS))
        for stem,cache in (('tar',archive_hashes),('source',source_hashes)):
            p=contained(entry[stem+'_path'])
            if str(p) not in cache:cache[str(p)]=sha(p)
            ck(eid+' actual '+stem,cache[str(p)]==entry[stem+'_sha256'])
        p=contained(entry['source_path'])
        with h5py.File(p,'r') as h:
            prefix=''
            for part in entry['dataset'].strip('/').split('/'):
                prefix+='/'+part;ck(eid+' hardlink '+prefix,isinstance(h.get(prefix,getlink=True),h5py.HardLink))
            ds=h[entry['dataset']]
            ck(eid+' dataset schema',ds.ndim==1 and ds.shape==(n,) and bool(ds.dtype.names) and not ds.is_virtual and not ds.external)
            columns=[]
            for field in FIELDS:
                source=np.asarray(ds.fields(entry['fields'][field])[()],dtype=float)
                carried=np.asarray(event['samples'][field],dtype=float)
                ck(eid+' full exact '+field,source.shape==(n,) and np.isfinite(source).all() and np.array_equal(source,carried))
                columns.append(source)
                declarations=[]
                for priorpath in entry['prior_paths'][field]:
                    prefix=''
                    for part in priorpath.strip('/').split('/'):
                        prefix+='/'+part;ck(eid+' prior hardlink '+prefix,isinstance(h.get(prefix,getlink=True),h5py.HardLink))
                    node=h[priorpath];ck(eid+' prior ordinary '+field,not node.is_virtual and not node.external and 1<=node.size<=256 and h5py.check_string_dtype(node.dtype) is not None)
                    text=[v.decode('utf-8') if isinstance(v,bytes) else str(v) for v in np.asarray(node[()]).reshape(-1)]
                    declarations.append({'path':priorpath,'text':text})
                prior=event['priors'][field]
                ck(eid+' prior '+field,prior['declarations']==declarations and prior['density'] is None and prior['joint_factorization']=='OPEN')
                ck(eid+' prior status '+field,prior['status']==('DECLARADO_TEXT_NOT_NORMALIZED' if declarations else 'OPEN_DERIVED_PRIOR_NOT_DECLARED'))
        ck(eid+' source stable',sha(p)==entry['source_sha256'])
        calculated=[moments(x) for x in columns]
        ck(eid+' summary field order',tuple(summary['field_order'])==FIELDS and summary['N']==n)
        for i,(mu,sd) in enumerate(calculated):
            near(eid+' mean '+FIELDS[i],summary['mean'][i],mu)
            near(eid+' std '+FIELDS[i],summary['std_ddof1'][i],sd)
            for j in range(5):
                cov=math.fsum((float(a)-mu)*(float(b)-calculated[j][0]) for a,b in zip(columns[i],columns[j]))/(n-1)
                near(eid+' cov '+str(i)+str(j),summary['paired_covariance'][i][j],cov)
        event_reports.append({'event_id':eid,'N':n,'all_five_fields_exact':True,'moment_check':'fsum_two_pass_ddof1'})
    # Scalar summaries only; no new fit/density/draw or repeated algorithm campaign.
    widths=[r['std_ddof1'][1] for r in summaries];means=[r['mean'][1] for r in summaries]
    for key,index,power in [('tau_inverse_variance',1,2),('IV_inverse_fourth',0,4)]:
        v=[r['std_ddof1'][index]**(-power) for r in summaries];den=math.fsum(v);shares=[x/den for x in v]
        for i,x in enumerate(shares):near(key+str(i),full[key]['shares'][i],x)
        near(key+' maximum',full[key]['max_share'],max(shares))
        ck(key+' no filtering',full[key]['events_dropped']==0)
        ck(key+' cap flag',full[key]['dominates_cap']==(max(shares)>reg['statistics']['maximum_information_weight_INPUT']))
    inverse=[s**-2 for s in widths]
    near('weighted mean',full['descriptive_uncorrected_dtau_weighted_mean'],math.fsum(w*m for w,m in zip(inverse,means))/math.fsum(inverse))
    for i,row in enumerate(full['leave_one_out_descriptive_means']):
        ck('LOO identity'+str(i),row['omitted']==entries[i]['event_id'])
        near('LOO mean'+str(i),row['mean'],math.fsum(inverse[j]*means[j] for j in range(33) if j!=i)/math.fsum(inverse[j] for j in range(33) if j!=i))
    split=full['split_membership_only']
    ck('split partition only',len(split)==2 and sorted(split[0]+split[1])==sorted(e['event_id'] for e in entries) and len(set(split[0]+split[1]))==33)
    ck('all readings',set(result['conditional_readings'])==set(READINGS))
    for reading,block in result['conditional_readings'].items():
        ck(reading+' scoped',block['lnB'] is None and block['z_physical'] is None and block['physical_likelihood_status']=='OPEN')
        ck(reading+' IDs',[r['event_id'] for r in block['events']]==[e['event_id'] for e in entries])
        if reading in ('R-MOD','R-PROP','R-RAIZ-COHERENT'):
            ck(reading+' expected OPEN',all(r['status']=='OPEN' for r in block['events']))
    near('runtime beta',result['beta_runtime'],7.2973525693e-3*math.sqrt(math.e),rtol=2e-15,atol=0)
    # All payload/result hashes rechecked. Source files were also rehashed after each event.
    for name,p in paths.items():ck('final pin '+name,sha(p)==go['inputs'][name]['sha256'])
    return {'approved':True,'status':'E7_EXECUTION_INDEPENDENT_REVIEW_PASSED_WITH_DECLARED_SCOPE',
        'e7_result_sha256':go['inputs']['e7_result']['sha256'],'posterior_sha256':go['inputs']['posterior']['sha256'],
        'registration_sha256':regsha,'GO_sha256':args.go_sha256,'verifier_sha256':sha(Path(__file__)),
        'started_utc':started.isoformat(),'finished_utc':datetime.now(timezone.utc).isoformat(),
        'wall_seconds':time.monotonic()-start,'CPU_seconds':time.process_time()-cpu,'cap_seconds':600,
        'events':event_reports,'total_paired_rows':row_count,'exact_field_comparisons':row_count*5,
        'checks':CHECKS,'check_count':len(CHECKS),'blocking_findings':[],
        'scope':'Full extraction equality33x5, source/tar/prior custody, empirical moments/covariance, weights/LOO arithmetic and honest matrix. No independent repetition of all conditional prediction/geometry algorithms.',
        'density_scope':'E7 emits no KDE/marginal-density calculation. Prior densities, likelihood and physical evidence remain OPEN/null; density arithmetic not claimed verified or paid.',
        'inherited_algorithm_review':'Frozen baseline/unit/adversarial tests not rerun. Conditional prediction numeric algorithms and deterministic split permutation are not independently recomputed here; IDs/status and partition checked.',
        'physical_likelihood_approved':False,'new_PE':False,'producer_imported':False,
        'source_sha256':source_hashes,'archive_sha256':archive_hashes}

def main():
    global STOP
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--go',type=Path,required=True);parser.add_argument('--go-sha256',required=True)
    args=parser.parse_args();target=HERE/'E7_EXECUTION_INDEPENDENT_REVIEW.json'
    if target.exists():raise FileExistsError('Preserve prior review; explicit successor required')
    try:receipt=review(args)
    except BaseException as exc:
        receipt={'approved':False,'status':'E7_REVIEW_FAILED_VISIBLE','e7_result_sha256':None,
                 'error_type':type(exc).__name__,'error':str(exc),'checks':CHECKS,
                 'finished_utc':datetime.now(timezone.utc).isoformat(),'verifier_sha256':sha(Path(__file__)) if STOP is None or time.monotonic()<STOP else None}
    finally:
        if os.name=='posix':signal.setitimer(signal.ITIMER_REAL,0)
        STOP=None  # Only exclusive final receipt flush remains; no more source I/O.
    new(target,receipt)
    print(json.dumps({'approved':receipt['approved'],'receipt':str(target),'sha256':sha(target)}))
    if not receipt['approved']:raise SystemExit(1)

if __name__=='__main__':main()
