"""Persistent scientific arrays in WSL RAM, controlled through JSON-lines."""
from __future__ import annotations
import gc
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import threading
import time
import uuid
import h5py
import numpy as np

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / 'models'))
sys.path.insert(0, str(HERE))

def available_bytes():
    values = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
    return int(values['MemAvailable'].split()[0]) * 1024

def scalar(x):
    if isinstance(x, bytes): return x.decode('utf-8', 'replace')
    if isinstance(x, np.generic): return scalar(x.item())
    if isinstance(x, (str, int, float, bool)) or x is None: return x
    return str(x)[:400]

def discover(source):
    arrays, meta, seen = [], {}, set()
    def visit(group, prefix='', depth=0):
        if depth > 12: raise ValueError('HDF5 nesting exceeds supported bound')
        for name in group:
            if not isinstance(group.get(name, getlink=True), h5py.HardLink):
                raise ValueError('Non-hard HDF5 link: explicit adapter required')
            obj=group[name]; path=prefix+'/'+name
            if obj.id in seen: continue
            seen.add(obj.id)
            if len(seen)>4096: raise ValueError('Too many HDF5 objects')
            if isinstance(obj,h5py.Group): visit(obj,path,depth+1)
            elif isinstance(obj,h5py.Dataset):
                if obj.is_virtual or obj.id.get_create_plist().get_external_count():
                    raise ValueError('External/virtual storage refused')
                if obj.dtype.kind in 'biufc' and obj.ndim<=2:
                    arrays.append((path,obj))
                elif obj.size<=64:
                    raw=obj[()]
                    meta[path]=scalar(raw) if np.ndim(raw)==0 else [scalar(v) for v in np.ravel(raw)]
                else: raise ValueError('Unsupported nonnumeric HDF5 content')
    visit(source)
    return arrays, meta

class ResidentDomain:
    def __init__(self):
        self.lock=threading.RLock();self.generation=0;self.thread=None
        self.stop=threading.Event();self.arrays={};self.records=[]
        self.state={'status':'IDLE','domain':None,'loaded_files':0,'total_files':0,
                    'resident_bytes':0,'errors':[],'series':[],'message':'Nenhum domínio residente.'}
        self.data_reads=0

    def status(self):
        with self.lock:
            proc=dict(line.split(':',1) for line in Path('/proc/self/status').read_text().splitlines() if ':' in line)
            return {**self.state,'errors':list(self.state['errors']),
                    'series':list(self.records),'worker_pid':os.getpid(),
                    'available_worker_bytes':available_bytes(),'generation':self.generation,
                    'data_read_operations':self.data_reads,
                    'storage':'OWNED_NUMPY_ARRAYS_NOT_MEMMAP',
                    'worker_rss_bytes':int(proc.get('VmRSS','0 kB').split()[0])*1024,
                    'worker_swap_bytes':int(proc.get('VmSwap','0 kB').split()[0])*1024,
                    'mask_policy':'QUALITY_ARRAYS_LOADED_NOT_AUTOMATICALLY_APPLIED'}

    def load(self,request):
        with self.lock:
            if self.thread and self.thread.is_alive():
                if self.state['status']=='LOADING' and self.state['domain']==request['domain']: return self.status()
                raise ValueError('A resident load/cancellation is already active')
            if self.arrays:
                if self.state['domain']==request['domain']: return self.status()
                raise ValueError('Release current domain before another load')
            sources=request['sources']
            if not sources: raise ValueError('No sources in selected domain')
            budget=int(request['budget_bytes'])
            if budget<=0: raise ValueError('No available memory budget')
            self.generation+=1; generation=self.generation;self.stop=threading.Event()
            self.state={'status':'LOADING','domain':request['domain'],'loaded_files':0,'load_id':str(uuid.uuid4()),
                        'total_files':len(sources),'resident_bytes':0,'errors':[],
                        'budget_bytes':budget,'series':[],'message':'Carregando arrays completos na RAM.'}
            self.thread=threading.Thread(target=self._load,args=(sources,budget,generation,self.stop),daemon=True)
            self.thread.start()
            return self.status()

    def _load(self,sources,budget,generation,stop):
        try:
            for item in sources:
                if stop.is_set(): break
                local={}; local_bytes=0
                try:
                    p=Path(item['path']); before=p.stat()
                    file_digest=None
                    if item.get('expected_sha256'):
                        with p.open('rb') as stream:
                            file_digest=hashlib.file_digest(stream,'sha256').hexdigest()
                        if file_digest!=item['expected_sha256']:
                            raise ValueError('Registered source hash mismatch')
                    with h5py.File(p,'r') as f:
                        found,meta=discover(f)
                        dataset_attrs={name:{k:scalar(v) for k,v in ds.attrs.items()} for name,ds in found}
                        if '/strain/Strain' not in {name for name,_ in found}: raise ValueError('No /strain/Strain')
                        d=f['/strain/Strain']
                        if d.ndim!=1 or d.dtype.kind not in 'fiu': raise ValueError('Invalid strain shape/dtype')
                        dt=float(d.attrs['Xspacing']); gps=float(d.attrs['Xstart'])
                        if not math.isfinite(dt) or dt<=0 or not math.isfinite(gps): raise ValueError('Invalid time metadata')
                        if scalar(d.attrs.get('Xunits','')) not in ('second','seconds','s'): raise ValueError('Time unit not seconds')
                        for name,dataset in found:
                            if stop.is_set(): break
                            size=int(dataset.size*dataset.dtype.itemsize)
                            used=self.state['resident_bytes']+local_bytes
                            if used+size>budget or size+2*1024**3>available_bytes():
                                raise MemoryError('Decoded arrays exceed resident memory budget')
                            array=dataset[()]
                            array=np.asarray(array)
                            if isinstance(array,np.memmap): raise ValueError('Memmap is not resident data')
                            array.flags.writeable=False
                            local[name]=array;local_bytes+=array.nbytes;self.data_reads+=1
                        strain=local.get('/strain/Strain')
                        if stop.is_set() or strain is None: break
                        finite=int(np.count_nonzero(np.isfinite(strain)))
                        digest=hashlib.sha256(memoryview(strain).cast('B')).hexdigest()
                        attrs={k:scalar(v) for k,v in d.attrs.items()}
                        rec={'id':item['id'],'name':item['name'],'detector':meta.get('/meta/Detector','UNKNOWN'),
                             'rows':len(strain),'dt_s':dt,'gps_start':gps,'duration_s':len(strain)*dt,
                             'finite_fraction':finite/max(1,len(strain)),'resident_bytes':local_bytes,
                             'numeric_datasets':len(local),'strain_array_sha256':digest,
                             'source_bytes':before.st_size,'source_mtime_ns':before.st_mtime_ns,
                             'attributes':attrs,'dataset_attributes':dataset_attrs,
                             'source_sha256':file_digest,'metadata':meta,'source':item['source'],
                             'source_path':str(p)}
                    after=p.stat()
                    if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):
                        raise ValueError('Source changed while loading')
                    with self.lock:
                        if generation!=self.generation or stop.is_set(): break
                        self.arrays[item['id']]=local;self.records.append(rec)
                        self.state['resident_bytes']+=local_bytes
                        self.state['loaded_files']+=1
                        self.state['message']='Residente: '+item['name']
                except Exception as exc:
                    with self.lock: self.state['errors'].append({'name':item['name'],'error':str(exc)[:200]})
                    if isinstance(exc,MemoryError): break
            with self.lock:
                if stop.is_set():
                    self.arrays.clear();self.records.clear();self.state.update(status='IDLE',resident_bytes=0,loaded_files=0,message='Domínio liberado.')
                else:
                    complete=self.state['loaded_files']==len(sources)
                    self.state['status']='READY' if complete else 'PARTIAL' if self.records else 'FAILED'
                    self.state['message']='Todos os arrays do domínio estão residentes.' if complete else 'Carga incompleta: conferir arquivos recusados.'
                    self.state['reads_after_load']=self.data_reads
                    manifest=HERE/'state'/'resident_runs'/(self.state['load_id']+'.json')
                    manifest.parent.mkdir(parents=True,exist_ok=True)
                    body=json.dumps(self.status(),ensure_ascii=False,allow_nan=False).encode('utf-8')
                    temp=manifest.with_suffix('.new');temp.write_bytes(body)
                    if temp.stat().st_size!=len(body):raise OSError('Incomplete resident manifest')
                    temp.replace(manifest)
                    self.state['manifest_path']=str(manifest)
        except Exception as exc:
            with self.lock: self.state.update(status='FAILED',message=str(exc)[:200])

    def release(self):
        with self.lock:
            self.stop.set()
            if self.thread and self.thread.is_alive():
                self.state.update(status='RELEASING',message='Cancelando carga e liberando arrays.')
            else:
                self.arrays.clear();self.records.clear();gc.collect()
                self.state.update(status='IDLE',resident_bytes=0,loaded_files=0,total_files=0,domain=None,message='Domínio liberado.')
            return self.status()

    def view(self,request):
        started=time.perf_counter()
        with self.lock:
            if self.state['status'] not in ('READY','PARTIAL'): raise ValueError('Domain load is not complete')
            rec=next((r for r in self.records if r['id']==request['id']),None)
            if rec is None: raise ValueError('Unknown resident series')
            values=self.arrays[rec['id']]['/strain/Strain']
            start=float(request.get('start_s',0));duration=float(request.get('duration_s',1));bins=int(request.get('bins',1600))
            if not all(math.isfinite(v) for v in (start,duration)) or start<0 or duration<=0 or not 16<=bins<=4096:
                raise ValueError('Invalid time window/resolution')
            lo=min(len(values),int(math.floor(start/rec['dt_s'])))
            hi=min(len(values),max(lo+1,int(math.ceil((start+duration)/rec['dt_s']))))
            if lo>=len(values): raise ValueError('Window outside observed data')
            window=values[lo:hi]; n=len(window);step=max(1,math.ceil(n/bins))
            # All samples contribute to finite min/max, including narrow peaks.
            points=[];finite_total=0;fractions=[]
            for offset in range(0,n,step):
                block=window[offset:min(n,offset+step)];valid=np.isfinite(block)
                count=int(np.count_nonzero(valid));finite_total+=count
                fractions.append(count/len(block))
                t=(lo+offset+(len(block)-1)/2)*rec['dt_s']
                points.append([t,float(np.min(block,where=valid,initial=np.inf)) if count else None,
                               float(np.max(block,where=valid,initial=-np.inf)) if count else None])
            result={'id':rec['id'],'start_s':lo*rec['dt_s'],'duration_s':n*rec['dt_s'],
                    'total_rows':rec['rows'],'window_rows':n,'resident_bytes':self.state['resident_bytes'],
                    'points':points,'units':{'x':'seconds since GPS '+str(rec['gps_start']),'y':'strain'},
                    'window_finite_fraction':finite_total/n,'read_source':'RESIDENT_RAM',
                    'data_reads_since_load':self.data_reads-self.state['reads_after_load'],
                    'generation':self.generation,'load_id':self.state['load_id'],
                    'valid_fraction_per_bin':fractions,
                    'mixed_gap_bins':sum(0<f<1 for f in fractions),
                    'render_method':'ALL_WINDOW_SAMPLES_MIN_MAX_ENVELOPE_NOT_SPECTRUM',
                    'elapsed_ms':1000*(time.perf_counter()-started),'gps_start':rec['gps_start']}
            return result

def verify_models():
    manifest=json.loads((HERE/'models'/'model_sources.json').read_text())
    for item in manifest['files']:
        if hashlib.sha256((HERE/'models'/item['copy']).read_bytes()).hexdigest()!=item['sha256']:
            raise ValueError('Scientific executor copy changed: review required')
    return manifest

def model(request):
    manifest=verify_models()
    from tgl_ringdown_prediction import prediction
    from tgl_ringdown_template import ringdown
    reading=request.get('reading')
    if reading not in ('R-A','R-B','R-RAIZ-0','R-GLOBAL'): raise ValueError('Select an explicit clock reading')
    mass=float(request.get('mass_source_solar',65));spin=float(request.get('spin',.7));z=float(request.get('redshift',.1))
    amp=float(request.get('amplitude',1e-21));phase=float(request.get('phase',0));duration=float(request.get('duration_s',.08))
    if not 0<duration<=100 or not 1<=mass<=1e10: raise ValueError('Invalid duration/mass')
    detector_mass=mass*(1+z)
    p=prediction(detector_mass,spin,reading,redshift=z)
    t=np.linspace(0,duration,4096)
    gr=ringdown(t,detector_mass,spin,reading,amp,phase=phase,deformation=0,redshift=z)['plus']
    tgl=ringdown(t,detector_mass,spin,reading,amp,phase=phase,deformation=1,redshift=z)['plus']
    source=HERE/'models'/'tgl_ringdown_prediction.py'
    return {'time_s':t.tolist(),'gr':gr.tolist(),'tgl':tgl.tolist(),'prediction':p,
            'mass_detector_solar':detector_mass,'scope':'CONDITIONAL_ENSEMBLE_NOT_EVENT_FIT',
            'parameters':request,
            'source':{'path':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'files':manifest['files']},
            'time_reference':{'detector_to_source':'t_source=t_detector/(1+z)',
                              't_mass_s':p['t_mass_s'],'tau_star_detector_s':p['tau_star_detector_s'],
                              'reading_scope':p['scope'],'playback_is_not_physical_evolution':True}}

def main():
    domain=ResidentDomain()
    for line in sys.stdin:
        request={}
        try:
            request=json.loads(line);op=request['operation']
            if op=='status': result=domain.status()
            elif op=='load': result=domain.load(request)
            elif op=='release': result=domain.release()
            elif op=='view': result=domain.view(request)
            elif op=='model': result=model(request)
            elif op=='event_manifest':
                from event_sources import build_event_manifest
                result=build_event_manifest(root=request['root'],inspect_hdf5=True)
            elif op=='event_view':
                from event_runtime import event_view
                result=event_view(domain,request,verify_models)
            else: raise ValueError('Unknown resident operation')
            print(json.dumps({'ok':True,'request_id':request.get('request_id'),'result':result},allow_nan=False),flush=True)
        except Exception as exc:
            print(json.dumps({'ok':False,'request_id':request.get('request_id'),'error':str(exc)[:500]}),flush=True)

if __name__=='__main__': main()
