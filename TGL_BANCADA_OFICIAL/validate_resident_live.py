"""Measure the installed resident bench through HTTP; never modify source data."""
import json
import math
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
BASE='http://127.0.0.1:18765/api/universe/'

def api(path,body=None):
    request=urllib.request.Request(BASE+path,data=None if body is None else json.dumps(body).encode(),
        headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(request,timeout=70) as response:return json.load(response)

def main():
    started=time.monotonic();last=-1;history=[]
    while True:
        s=api('status')
        if s['loaded_files']!=last:
            print(json.dumps({k:s.get(k) for k in ('status','loaded_files','total_files','resident_bytes','worker_swap_bytes')}),flush=True)
            history.append({k:s.get(k) for k in ('status','loaded_files','total_files','resident_bytes','worker_rss_bytes','worker_swap_bytes')})
            last=s['loaded_files']
        if s['status'] in ('READY','PARTIAL','FAILED'):break
        if time.monotonic()-started>900:raise TimeoutError('Load has not finished; kept active')
        time.sleep(10)
    record={'measured_at':datetime.now(timezone.utc).isoformat(),'status':s,'load_observation_history':history,
            'scope':'COMPLETE_DECLARED_GWOSC_STRAIN_PROFILE_NOT_ALL_DOMAINS','views':[],'models':[]}
    if s['status'] not in ('READY','PARTIAL'):raise RuntimeError(s['message'])
    rec=next(r for r in s['series'] if r['finite_fraction']>.99)
    for duration in (1.,32.,rec['duration_s']):
        for fraction in (0.,.2,.5,.8):
            t=time.perf_counter()
            v=api('view?'+urllib.parse.urlencode({'id':rec['id'],'start_s':fraction*(rec['duration_s']-duration),
                                                'duration_s':duration,'bins':1600}))
            measured={k:v[k] for k in ('id','start_s','duration_s','window_rows','total_rows','read_source',
                                       'data_reads_since_load','elapsed_ms','load_id','generation','mixed_gap_bins')}
            measured['http_ms']=1000*(time.perf_counter()-t)
            assert v['data_reads_since_load']==0 and v['read_source']=='RESIDENT_RAM'
            assert v['load_id']==s['load_id']
            record['views'].append(measured)
    for reading in ('R-GLOBAL','R-A','R-B'):
        t=time.perf_counter()
        m=api('model',{'mass_source_solar':65,'spin':.7,'redshift':.1,'reading':reading,
                       'amplitude':1e-21,'phase':0,'duration_s':.08})
        difference=max(abs(a-b) for a,b in zip(m['gr'],m['tgl']))
        if reading=='R-GLOBAL':assert difference==0
        if reading=='R-B':assert difference>0 and m['prediction']['gamma_per_s']>0
        assert m['mass_detector_solar']==71.5
        record['models'].append({'reading':reading,'http_ms':1000*(time.perf_counter()-t),
             'max_abs_difference':difference,'prediction':m['prediction'],'source':m['source'],'scope':m['scope']})
    end=api('status');assert end['data_read_operations']==s['data_read_operations']
    record['final_memory']={k:end[k] for k in ('resident_bytes','worker_rss_bytes','worker_swap_bytes','data_read_operations')}
    record['sources_are_closed_after_load']=True # dataset contexts close in loader; not FD audit
    record['closed_handle_evidence']='CODE_CONTEXT_MANAGERS_AND_FIXTURE_DELETE_TEST_NOT_PROC_FD_AUDIT'
    values=sorted(v['http_ms'] for v in record['views'])
    record['view_http_p95_ms']=values[math.ceil(.95*len(values))-1]
    p=HERE/'state'/('validation_universe_v4_'+s['load_id']+'.json');p.parent.mkdir(parents=True,exist_ok=True)
    data=json.dumps(record,ensure_ascii=False,indent=2).encode();tmp=p.with_suffix('.new');tmp.write_bytes(data)
    assert tmp.stat().st_size==len(data);tmp.replace(p)
    print(json.dumps({'receipt':str(p),'status':s['status'],'files':s['loaded_files'],'total':s['total_files'],
                     'GiB':s['resident_bytes']/1024**3,'view_http_p95_ms':record['view_http_p95_ms'],
                     'swap_bytes':end['worker_swap_bytes'],'models':len(record['models'])}),flush=True)

if __name__=='__main__':main()
