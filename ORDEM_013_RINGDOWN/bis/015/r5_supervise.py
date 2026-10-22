"""C04 attributable restarts with immutable per-child logs and a bounded CPU ledger."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,subprocess,time,resource,hashlib,collections
B=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN');ROOT=B/'bis/015';D=ROOT/'t03/R5'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,obj):
    with p.open('xb') as f:f.write((json.dumps(obj,indent=2)+'\n').encode())
def main():
    level=sys.argv[1];assert level in ['2048','4096'];out=D/('generation_'+level);out.mkdir(exist_ok=False)
    manifest=json.loads((D/'INPUT_MANIFEST.json').read_bytes())
    for n,pin in manifest['inputs'].items():assert sha(D/n)==pin
    for n,pin in manifest['source_tree'].items():assert sha(B/'bis/e2_code_v1_1'/n)==pin
    if level=='4096':
        previous=json.loads((D/'generation_2048/RESULT.json').read_bytes())
        assert previous['status_counts'].get('DOMAIN_RETURNED_NONE',0)>0,'Fallback only after measured EDOM'
    cfg=json.loads((D/('CONFIG_2048_INPUT.json' if level=='2048' else 'CONFIG_4096_RESERVED_INPUT.json')).read_bytes())
    items=json.loads((D/'ITEMS.json').read_bytes());bylabel={v['label']:i for i,v in enumerate(items)};assert len(bylabel)==len(items)
    index=0;records=[];crashes=[];results=[];start=time.perf_counter();cpu_start=resource.getrusage(resource.RUSAGE_CHILDREN)
    while index<len(items):
        folder=out/f'child_{len(records)+1:03d}';folder.mkdir();job=folder/'JOB.json';put(job,dict(config=cfg,items=items[index:]));log=folder/'CALLS.jsonl';t=time.perf_counter()
        usage=resource.getrusage(resource.RUSAGE_CHILDREN)
        with (folder/'NATIVE.log').open('xb') as stream:
            proc=subprocess.run([sys.executable,'-B',str(ROOT/'r5_child.py'),str(job),str(log)],stdout=stream,stderr=subprocess.STDOUT,timeout=880)
        end=resource.getrusage(resource.RUSAGE_CHILDREN);cpu=end.ru_utime+end.ru_stime-usage.ru_utime-usage.ru_stime
        lines=[json.loads(l) for l in log.read_text().splitlines()] if log.exists() else []
        returns=[r for r in lines if 'return_label' in r];results.extend(returns)
        record=dict(child=str(folder),rc=proc.returncode,wall_seconds=time.perf_counter()-t,cpu_seconds=cpu,returned=len(returns));records.append(record)
        if proc.returncode==0:break
        pre=[r['precall'] for r in lines if 'precall' in r];returned={r['return_label'] for r in returns}
        label=pre[-1] if pre and pre[-1] not in returned else None
        crashes.append(dict(rc=proc.returncode,label=label))
        if label is None:break # startup/transport failure is not an attributable native draw
        index=bylabel[label]+1
        if sum(r['cpu_seconds'] for r in records)>840:break
    counts=dict(collections.Counter(r['status'] for r in results));end=resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu=end.ru_utime+end.ru_stime-cpu_start.ru_utime-cpu_start.ru_stime
    passed=len(results)==len(items) and not crashes and counts.get('FINITE_WAVEFORM',0)==len(items)
    result=dict(at=datetime.now(timezone.utc).isoformat(),status='R5_SOURCE_ONLY_QUALIFIED' if passed else 'R5_NOT_QUALIFIED',generation_maximum_frequency_hz=int(level),n_items=len(items),returns=len(results),
      status_counts=counts,crashes=crashes,children=records,failures=[r for r in results if r['status']!='FINITE_WAVEFORM'],
      wall_seconds=time.perf_counter()-start,cpu_seconds=cpu,heavy_machine_hours=0,input_manifest_sha256=sha(D/'INPUT_MANIFEST.json'),
      child_script_sha256=sha(ROOT/'r5_child.py'),supervisor_script_sha256=sha(Path(__file__)),strain_read=False,blind_seed_read=False,PE_run=False)
    put(out/'RESULT.json',result);print(json.dumps({k:result[k] for k in ['status','generation_maximum_frequency_hz','n_items','returns','status_counts','crashes','wall_seconds','cpu_seconds']}))
if __name__=='__main__':main()
