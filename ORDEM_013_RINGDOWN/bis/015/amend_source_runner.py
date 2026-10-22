"""First authorized V1.1 patch: generation grid, overflow refusal, EDOM custody."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,ast
B=Path(__file__).resolve().parents[2];C=B/'bis/e2_code_v1_1';D=B/'bis/015/t03'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def replace(s,a,b):
    if s.count(a)!=1:raise ValueError('Anchor not unique: '+a[:100])
    return s.replace(a,b)
def main():
    snap=D/'source_runner_before_001';snap.mkdir(exist_ok=False)
    receipt=json.loads((D/'COPY_RECEIPT.json').read_bytes());rows=[]
    for n in ['pseob_source.py','pe_runner.py']:
        p=C/n;raw=p.read_bytes();assert sha(p)==receipt['copy_tree_sha256'][n]
        with (snap/n).open('xb') as f:f.write(raw)
    p=C/'pseob_source.py';s=p.read_text('utf-8')
    s=replace(s,'import time','import time\nimport os,json\nfrom pathlib import Path\nfrom datetime import datetime,timezone')
    s=replace(s,'COST_COUNTER = None','COST_COUNTER = None\nEDOM_LOG = None')
    s=replace(s,'    COST_COUNTER=counter','    if len(counter)!=3:raise ValueError("Source counter requires calls, seconds, EDOM")\n    COST_COUNTER=counter')
    marker='\ndef validate_polarizations('
    funcs='''
def set_edom_log(path):
    global EDOM_LOG
    path=Path(path)
    if path.name!='EDOM_LOG.jsonl' or path.is_symlink():raise ValueError('Explicit job EDOM log required')
    with path.open('xb'):pass
    EDOM_LOG=path


def generation_grid(frequency_array, generation_maximum, generation_rate, analysis_maximum):
    f=np.asarray(frequency_array,dtype=float)
    if f.ndim!=1 or len(f)<2 or not np.isfinite(f).all() or f[0]!=0 or not np.all(np.diff(f)>0):raise ValueError('Invalid uniform zero-origin grid')
    df=f[1]-f[0]
    if not np.allclose(f,np.arange(len(f))*df,rtol=0,atol=1e-9):raise ValueError('Nonuniform data frequency bins')
    if generation_rate not in (4096,8192) or not np.isfinite([generation_maximum,analysis_maximum]).all():raise ValueError('Unsupported generation sampling')
    if not 0<analysis_maximum<=generation_maximum<=generation_rate/2 or f[-1]>generation_rate/2:raise ValueError('Generation bandwidth does not contain data grid')
    # SimInspiralFD infers its time step from f_max. These qualified pairs remove ambiguity.
    if generation_maximum!=generation_rate/2:raise ValueError('Qualified generation requires fmax=fs/2')
    bins=int(round((generation_rate/2)/df))
    if not np.isclose(bins*df,generation_rate/2,rtol=0,atol=1e-9):raise ValueError('Generation Nyquist is off grid')
    g=np.arange(bins+1,dtype=float)*df
    if not np.allclose(g[:len(f)],f,rtol=0,atol=1e-9):raise ValueError('Incompatible generation/data bins')
    return g


def record_edom(parameters,generation_maximum):
    if EDOM_LOG is None or COST_COUNTER is None:raise RuntimeError('EDOM logging was not configured; no silent prior rejection')
    raw=(json.dumps(dict(at=datetime.now(timezone.utc).isoformat(),parameters=parameters,
         generation_maximum_frequency_hz=generation_maximum,status='DOMAIN_RETURNED_NONE'),allow_nan=False)+'\\n').encode()
    with COST_COUNTER.get_lock():
        fd=os.open(EDOM_LOG,os.O_WRONLY|os.O_APPEND)
        try:
            if os.write(fd,raw)!=len(raw):raise OSError('Short EDOM record')
        finally:os.close(fd)
        COST_COUNTER[2]+=1

'''
    s=replace(s,marker,'\n'+funcs+marker)
    anchor="    # Conservative LAL temporal bounds; failure aborts PE, never trims the prior."
    s=replace(s,anchor,"    if 1+dtau440>2*max(1.,1+dtau220):raise ValueError('NATIVE_RINGDOWN_BUFFER_BOUND_REFUSED_BEFORE_LAL')\n    generation_maximum=kwargs.pop('generation_maximum_frequency_hz')\n    generation_rate=kwargs.pop('generation_sample_rate_hz')\n    generated_grid=generation_grid(frequency_array,generation_maximum,generation_rate,kwargs['maximum_frequency'])\n"+anchor)
    s=replace(s,"options=dict(kwargs,waveform_approximant='pSEOBNRv4HM_PA',lal_waveform_dictionary=dictionary)","options=dict(kwargs,waveform_approximant='pSEOBNRv4HM_PA',lal_waveform_dictionary=dictionary)\n    options['maximum_frequency']=generation_maximum")
    s=replace(s,'result=lal_binary_black_hole(frequency_array,mass_1,mass_2,','result=lal_binary_black_hole(generated_grid,mass_1,mass_2,')
    anchor="    return validate_polarizations(result,frequency_array,kwargs['minimum_frequency'],kwargs['maximum_frequency'])"
    s=replace(s,anchor,"    if result is None:\n        record_edom(dict(mass_1=float(mass_1),mass_2=float(mass_2),chi_1=float(chi_1),chi_2=float(chi_2)),generation_maximum)\n        return None\n    validate_polarizations(result,generated_grid,kwargs['minimum_frequency'],generation_maximum)\n    # Exact common Fourier bins; no interpolation, aliasing or change to the data sample grid.\n    result={k:np.asarray(result[k])[:len(frequency_array)].copy() for k in ('plus','cross')}\n"+anchor)
    ast.parse(s);tmp=p.with_suffix('.pending')
    with tmp.open('xb') as f:f.write(s.encode())
    assert tmp.stat().st_size>0;tmp.replace(p);rows.append(dict(file=p.name,before=sha(snap/p.name),after=sha(p)))
    p=C/'pe_runner.py';s=p.read_text('utf-8')
    anchor="    if 2*config['onsource_roll_off_s']>=config['duration_s']:"
    add="""    rate=config['generation_sample_rate_hz'];gmax=config['generation_maximum_frequency_hz']
    if isinstance(rate,bool) or rate not in (4096,8192) or isinstance(gmax,bool):raise ValueError('Generation settings')
    positive(gmax,'generation maximum')
    if not config['maximum_frequency_hz']<=gmax or gmax!=rate/2 or config['sample_rate_hz']>rate:raise ValueError('Separated generation/data frequency contract')
"""
    s=replace(s,anchor,add+anchor)
    s=replace(s,'def main():','''def edom_posterior_status(path,posterior,counter):
    import numpy as np
    bounds={k:np.quantile(np.asarray(posterior[k],dtype=float),[.005,.995]).tolist() for k in ('mass_1','mass_2','chi_1','chi_2')}
    if any(not np.isfinite(v).all() for v in bounds.values()):raise ValueError('Nonfinite posterior EDOM region')
    inside=count=0
    with Path(path).open(encoding='utf-8') as stream:
        for line in stream:
            r=json.loads(line);params=r['parameters'];count+=1
            if all(bounds[k][0]<=params[k]<=bounds[k][1] for k in bounds):inside+=1
    with counter.get_lock():calls=int(counter[0]);measured=int(counter[2])
    if count!=measured or count>calls:raise ValueError('EDOM counter/log disagreement')
    return dict(status='FAILED_EDOM_INSIDE_POSTERIOR_REGION' if inside else 'NO_EDOM_INSIDE_POSTERIOR_REGION',
                inside=inside,edom=count,source_calls=calls,fraction=count/calls if calls else None,
                quantile_region=bounds,log_sha256=sha(path))


def main():''')
    s=replace(s,'parameter_conversion,set_deadline,set_cost_counter','parameter_conversion,set_deadline,set_cost_counter,set_edom_log')
    s=replace(s,"source_counter=multiprocessing.Array('d',[0.,0.],lock=True)","source_counter=multiprocessing.Array('d',[0.,0.,0.],lock=True)")
    s=replace(s,'set_cost_counter(source_counter);set_deadline(',"set_cost_counter(source_counter);set_edom_log(outdir/'EDOM_LOG.jsonl');set_deadline(")
    anchor="          reference_frequency=cfg['reference_frequency_hz'],catch_waveform_errors=True))"
    s=replace(s,anchor,"          generation_maximum_frequency_hz=cfg['generation_maximum_frequency_hz'],\n          generation_sample_rate_hz=cfg['generation_sample_rate_hz'],\n"+anchor)
    anchor="        state=convergence(result,cfg['sampler']);time_guard(reg)"
    s=replace(s,anchor,anchor+"\n        edom=edom_posterior_status(outdir/'EDOM_LOG.jsonl',result.posterior,source_counter)\n        if edom['inside']:\n            state.update(status='FAILED_EDOM_INSIDE_POSTERIOR_REGION',accepted_for_analysis=False)\n        publish_new(outdir/'EDOM_SUMMARY.json',edom)")
    s=replace(s,"          source_calls=int(source_counter[0]),source_total_wall_seconds=float(source_counter[1]),", "          edom=edom,source_calls=int(source_counter[0]),source_total_wall_seconds=float(source_counter[1]),")
    ast.parse(s);tmp=p.with_suffix('.pending')
    with tmp.open('xb') as f:f.write(s.encode())
    assert tmp.stat().st_size>0;tmp.replace(p);rows.append(dict(file=p.name,before=sha(snap/p.name),after=sha(p)))
    value=dict(at=datetime.now(timezone.utc).isoformat(),status='SOURCE_RUNNER_AMENDED_NOT_QUALIFIED',rows=rows,
        scope='Generation FFT bins, pre-LAL overflow refusal, atomic EDOM append under shared counter lock, posterior-region veto',
        pending=['R5 native qualification','negative/control tests','V1.1 guard/statistics/blinding','injection adapter explicit generation path at its authorized later stage'],originals_unchanged=all(sha(B/'bis/e2_code'/n)==v for n,v in receipt['original_tree_sha256'].items()))
    assert value['originals_unchanged']
    with (D/'SOURCE_RUNNER_PATCH_001.json').open('xb') as f:f.write((json.dumps(value,indent=2)+'\n').encode())
    print(json.dumps(value))
if __name__=='__main__':main()
