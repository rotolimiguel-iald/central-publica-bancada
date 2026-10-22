"""Single persistent WSL scientific worker; original data remain read-only."""
from __future__ import annotations
import atexit
import json
from pathlib import Path
import queue
import subprocess
import threading
import time
import uuid
from functools import lru_cache
import data_lab
import hdf5_bridge

HERE=Path(__file__).resolve().parent
DOMAIN_GROUPS={'GWOSC: strain','GW: strain da bancada 013BIS'}

def sources():
    return [i for i in data_lab.catalog() if i['group'] in DOMAIN_GROUPS and i['format'] in ('.hdf5','.h5')]

def domains():
    files=sources()
    return {'domains':[
        {'id':'gw_strain','title':'Buracos negros · ondas gravitacionais',
         'description':'Strain GWOSC completo, sinais dos detectores e máscaras instaladas.',
         'files':len(files),'source_bytes':sum(i['bytes'] for i in files),'implemented':True,
         'scope':'Todos os arquivos GWOSC strain das caches 013/015; posteriores e outros formatos têm perfil separado.'},
        {'id':'cosmology','title':'Cosmologia · expansão e redshift','description':'BAO, SNe Ia, vazios e lenteamento.',
         'files':0,'source_bytes':0,'implemented':False,'scope':'Planejado; catálogo e executores a reunir.'},
        {'id':'particles','title':'Neutrinos · partículas','description':'Massas, oscilações e propagação.',
         'files':0,'source_bytes':0,'implemented':False,'scope':'Planejado; contratos de observáveis e unidades.'},
        {'id':'coherence','title':'Coerência · tempo e dephasing','description':'Leituras modulares, estados e evolução.',
         'files':0,'source_bytes':0,'implemented':False,'scope':'Planejado; fórmula do tempo e vínculo físico em auditoria de fonte.'}],
        'time_reference':{'status':'SOURCE_READ_WITH_HYPOTHESES','text':'Torre: tempo característico = índice = 1/peso de Markov (the_tower_is_time). Escala modular; segundos exigem relógio físico explícito. GPS, tempo fonte e reprodução preservam suas unidades.',
                          'source':'TIME_SOURCE_AUDIT.md','modular_killing':'t_mod = -kappa*t_Killing/(2*pi), sob ponte BW/KMS e normalização declarada.'}}

class Worker:
    def __init__(self):
        self.process=None;self.lock=threading.Lock();self.responses=queue.Queue()
    def start(self):
        if self.process is not None:
            if self.process.poll() is None:return
            raise ValueError('Scientific worker stopped; restart the bench to create a fresh session')
        log=HERE/'state'/'resident_worker.log';log.parent.mkdir(exist_ok=True,parents=True)
        with log.open('ab') as stderr:
            self.process=subprocess.Popen(['wsl.exe','-e',hdf5_bridge.ENV_PYTHON,'-u',
                hdf5_bridge.wsl_path(HERE/'adapters'/'resident_worker.py')],stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,stderr=stderr,text=True,encoding='utf-8',bufsize=1,
                creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        def reader():
            for line in self.process.stdout:
                try:self.responses.put(json.loads(line))
                except json.JSONDecodeError:self.responses.put({'error':'Worker returned invalid JSON'})
            self.responses.put({'error':'Worker output ended'})
        threading.Thread(target=reader,daemon=True).start()
    def call(self,payload):
        with self.lock:
            self.start();rid=str(uuid.uuid4())
            self.process.stdin.write(json.dumps({**payload,'request_id':rid})+'\n');self.process.stdin.flush()
            deadline=time.monotonic()+60
            while True:
                try:response=self.responses.get(timeout=max(.01,deadline-time.monotonic()))
                except queue.Empty:raise ValueError('Scientific operation timed out; no automatic repeat')
                if response.get('request_id') not in (rid,None):continue
                if not response.get('ok'):raise ValueError(response.get('error','Unknown worker failure'))
                return response['result']
    def close(self):
        if self.process and self.process.poll() is None:
            try:self.process.stdin.close()
            except OSError:pass

WORKER=Worker();atexit.register(WORKER.close)

def status():
    if WORKER.process is None:
        return {'status':'IDLE','domain':None,'loaded_files':0,'total_files':0,'resident_bytes':0,
                'errors':[],'series':[],'message':'Escolha um domínio para carregar os dados completos.'}
    return WORKER.call({'operation':'status'})

def load(domain):
    if domain!='gw_strain':raise ValueError('Domain adapter not implemented')
    files=sources();memory=data_lab.memory_status()
    budget=min(int(memory['available_bytes']*.50),96*1024**3)
    profile=event_profile()
    pins={v['name']:v['sha256'] for v in profile['sources'].values()}
    payload=[{'id':i['id'],'path':hdf5_bridge.wsl_path(Path(i['path'])),'source':i['path'],
              'name':i['name'],'expected_sha256':pins.get(i['name'])} for i in files]
    return WORKER.call({'operation':'load','domain':domain,'sources':payload,'budget_bytes':budget})

def view(params):
    return WORKER.call({'operation':'view','id':params.get('id',[''])[0],
                       'start_s':float(params.get('start_s',['0'])[0]),
                       'duration_s':float(params.get('duration_s',['1'])[0]),
                       'bins':int(params.get('bins',['1600'])[0])})

def model(payload):return WORKER.call({**payload,'operation':'model'})
def release():return WORKER.call({'operation':'release'})

@lru_cache(maxsize=1)
def event_profile():
    root=Path(r'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN')
    manifest=WORKER.call({'operation':'event_manifest','root':hdf5_bridge.wsl_path(root)})
    if not manifest.get('ready_for_source_use'):
        raise ValueError('Event source validation failed: '+json.dumps(manifest.get('errors',[]),ensure_ascii=False)[:1800])
    a=manifest['analysis']; sources={};noise={}
    for detector,info in manifest['detectors'].items():
        strain=manifest['sources'][info['strain']['source']]
        sources[detector]={'name':Path(strain['path']).name,'sha256':strain['sha256'],'path':strain['path']}
        n=manifest['sources'][info['noise']['source']]
        noise[detector]={'path':n['path'],'sha256':n['sha256']}
    return {'event':manifest['event'],'reference_peak_gps':manifest['reference_peak_gps'],
            'starts_tm':a['start_times_tM'],'primary_start_tm':a['primary_start_tM'],
            'reference_tM_seconds':a['reference_tM_seconds'],
            'reference_mass_detector_solar':a['reference_mass_detector_solar_for_start'],
            'redshift':manifest['reference_redshift'],'samples':a['interval_samples'],
            'sample_rate_hz':a['analysis_sample_rate_hz'],'stride':a['sample_stride'],
            'input_sample_rate_hz':a['analysis_sample_rate_hz']*a['sample_stride'],
            'required_dq':a['quality_required'],'required_injections':a['injection_flags_required'],
            'sources':sources,'noise_sources':noise,
            'physical_gate':{'status':manifest['scientific_status'],
                             'reason':manifest['model']['physical_gate']},
            'provenance':{'status':manifest['status'],'sources':manifest['sources'],
                          'reference_source':manifest['reference_source'],
                          'instrument_calibration':'NOT_MARGINALIZED_IN_THIS_INTERACTIVE_PREVIEW',
                          'c7_summary':manifest.get('c7_summary'),
                          'coverage':'ONE_REGISTERED_EVENT_NOT_ALL_EVENTS'}}

def event_metadata():
    return {k:v for k,v in event_profile().items() if k not in ('sources','noise_sources')}

def event_view(payload):
    allowed={'start_tm','reading','mass_source_solar','spin','redshift','detectors'}
    if set(payload)-allowed:raise ValueError('Unknown event parameter')
    return WORKER.call({**payload,'operation':'event_view','profile':event_profile()})
