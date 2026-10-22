"""R7 followed by the thirty registered null cells; bounded, no retries."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import os,sys,json,time,subprocess,signal,resource
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent; B=D.parents[1]; ROOT=B.parent
CODE=B/'bis/e2_code_v1_1_2'; OUT=ROOT/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(CODE))
from registration_guard import (load_registration_chain_v1_1,checked_registration,
    load_authorized_configuration,new_null_cells,sha,publish_new,check_witness)

def utc():return datetime.now(timezone.utc)
def text_new(path,text):
    raw=text.encode();temp=path.with_name(path.name+'.pending')
    with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert temp.read_bytes()==raw
    os.link(temp,path);temp.unlink()

def main():
    run=D/'nulls_campaign_001'; clock=B/'bis/PART_015_BUDGET_START.json'
    assert not run.exists() and not clock.exists(), 'Existing clock/run: inspect, never repeat'
    assert not list((ROOT/'TUNEL/PARA_CHATGPT').glob('RECIBO_016_FECHAMENTO_PARCIAL*.md')), 'Management review takes precedence'
    reg,digest,note=load_registration_chain_v1_1()
    try:checked_registration()
    except FileNotFoundError as e:
        assert str(clock) in str(e),str(e)
    else:raise AssertionError('R7 should still be absent')
    view=load_authorized_configuration(reg,digest)
    allocation=B/'ORCAMENTO_015_v1.json';a=json.loads(allocation.read_bytes())
    assert view['_allocation_sha256']==sha(allocation)
    seconds=next(x['allocated_machine_hours'] for x in a['items'] if x['item']=='T03_nulls_IV_and_t5')*3600
    assert seconds==3600
    cells=new_null_cells(reg)
    assert len(cells)==30 and sum(v['kind']=='route_IV' for v in cells.values())==6
    for name in cells:
        assert cells[name]['draws']==100_000_000
        for suffix in ('.json','_FAILURE.json'):
            assert not (B/'bis'/('RESULT_E2_NULL_'+name+suffix)).exists(), name
    run.mkdir()
    plan=dict(at=utc().isoformat(),registration_sha256=digest,code_directory=str(CODE),
        script_sha256=sha(Path(__file__)),allocation_sha256=sha(allocation),cell_ids=sorted(cells),
        max_child_processes=6,max_all_processes=7,allocated_seconds=seconds,retry=False,
        heavy_machine_accounting='UNION_OF_OWNED_CHILD_INTERVALS',blind_data=False)
    publish_new(run/'PLAN.json',plan)
    rule=reg['budget_rule_v1_1'];source=ROOT/rule['source_receipt_relative_to_Chatgpt']
    assert sha(source)==rule['source_receipt_sha256'] and rule.get('operator_reduction') is None
    release=ROOT/rule['machine_free_receipt_relative_to_Chatgpt']
    available=json.loads(source.read_bytes())['remaining_of_40_hours'];at=utc()
    budget=dict(start_utc=at.isoformat(),hard_deadline_utc=(at+timedelta(hours=168)).isoformat(),
        authorized_machine_hours=available,source_receipt_relative_to_Chatgpt=rule['source_receipt_relative_to_Chatgpt'],
        source_receipt_sha256=sha(source),recibo_maquina_livre_sha256=sha(release))
    publish_new(clock,budget)
    witness=ROOT/rule['witness_relative_to_Chatgpt']
    text_new(witness,f'''[REAL — relógio R7; nenhuma detecção física]

budget_sha256: {sha(clock)}
registered_utc: {at.isoformat()}

Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}
Registro corrente SHA256: {digest}
Horas autorizadas: {available!r}; relógio exclusivo por168h. Primeiro job: nulos T03; alocação1h, até6 filhos, sem dados cegos. Plano SHA256: {sha(run/'PLAN.json')}.
''')
    reg,checked=checked_registration();assert checked==digest
    queue=sorted(cells,key=lambda k:(cells[k]['kind']!='route_IV',k))
    active={};finished=[];attempts=[];fault=None;start=time.monotonic();last_report=0
    def terminate(signum,frame):raise InterruptedError('Controller signal '+str(signum))
    signal.signal(signal.SIGTERM,terminate);signal.signal(signal.SIGINT,terminate)
    try:
        while queue or active:
            if time.monotonic()-start>=seconds-10:raise TimeoutError('T03 allocated machine hour exhausted')
            while queue and len(active)<6:
                name=queue.pop(0);log=run/(name+'.log')
                record=dict(cell=name,start_utc=utc().isoformat(),command=[sys.executable,'-B',str(CODE/'null_runner.py'),'--cell',name])
                publish_new(run/(name+'_ATTEMPT.json'),record);attempts.append(record)
                stream=log.open('xb')
                child=subprocess.Popen(record['command'],stdout=stream,stderr=subprocess.STDOUT,
                    start_new_session=True,env={**os.environ,**{k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')}})
                record.update(pid=child.pid,monotonic_start=time.monotonic())
                active[name]=(child,stream,record)
                publish_new(run/(name+'_PROCESS.json'),record)
            for name,(child,stream,record) in list(active.items()):
                rc=child.poll()
                if rc is None:continue
                stream.close();del active[name]
                record.update(returncode=rc,end_utc=utc().isoformat(),wall_seconds=time.monotonic()-record['monotonic_start'],log_sha256=sha(run/(name+'.log')))
                path=B/'bis'/('RESULT_E2_NULL_'+name+'.json')
                if rc!=0 or not path.exists():
                    record['accepted']=False
                else:
                    value=json.loads(path.read_bytes())
                    record['accepted']=(value['registration_sha256']==digest and value['cell']==cells[name] and value['result']['draws']==cells[name]['draws'])
                    record.update(receipt_sha256=sha(path),cpu_seconds=value['cpu_seconds'])
                finished.append(record);publish_new(run/(name+'_FINISH.json'),record)
                print(json.dumps({'finished':len(finished),'total':30,'cell':name,'accepted':record['accepted'],'wall_seconds':record['wall_seconds']}),flush=True)
                if not record['accepted']:raise RuntimeError('Cell failed; no automatic retry: '+name)
            if time.monotonic()-last_report>=30:
                print(json.dumps({'status':'RUNNING','finished':len(finished),'active':list(active),'pending':len(queue),'elapsed_seconds':time.monotonic()-start}),flush=True)
                last_report=time.monotonic()
            time.sleep(1)
    except BaseException as e:
        fault={'type':type(e).__name__,'message':str(e)}
    finally:
        for child,stream,record in active.values():
            if child.poll() is None:os.killpg(child.pid,signal.SIGTERM)
        for name,(child,stream,record) in active.items():
            try:child.wait(timeout=3)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid,signal.SIGKILL);child.wait()
            stream.close();record.update(returncode=child.returncode,end_utc=utc().isoformat(),
                wall_seconds=time.monotonic()-record['monotonic_start'],accepted=False,stopped_by_controller=fault,log_sha256=sha(run/(name+'.log')))
            finished.append(record);publish_new(run/(name+'_FINISH.json'),record)
            failed=B/'bis'/('RESULT_E2_NULL_'+name+'_FAILURE.json')
            if not failed.exists() and not (B/'bis'/('RESULT_E2_NULL_'+name+'.json')).exists():
                publish_new(failed,dict(status='CONTROLLER_STOPPED_NO_TAIL_RESULT',cell_id=name,registration_sha256=digest,reason=fault))
        used=resource.getrusage(resource.RUSAGE_CHILDREN)
        intervals=sorted((datetime.fromisoformat(r['start_utc']).timestamp(),datetime.fromisoformat(r['end_utc']).timestamp()) for r in finished)
        union=0.;left=right=None
        for lo,hi in intervals:
            if left is None:left,right=lo,hi
            elif lo<=right:right=max(right,hi)
            else:union+=right-left;left,right=lo,hi
        if left is not None:union+=right-left
        result=dict(status='SYNTHETIC_NULLS_COMPLETED_NOT_PHYSICAL_5SIGMA' if fault is None else 'T03_MEDIDA_PARTIAL_NO_RETRY',
            registration_sha256=digest,clock_sha256=sha(clock),plan_sha256=sha(run/'PLAN.json'),
            finished=finished,not_started=queue,fault=fault,wall_seconds=time.monotonic()-start,
            child_cpu_seconds=used.ru_utime+used.ru_stime,machine_hours_union=union/3600,
            gate_changed=False,blind_data_read=False,seed_read=False,finished_utc=utc().isoformat())
        publish_new(run/'RESULT.json',result)
        print(json.dumps({k:result[k] for k in ('status','machine_hours_union','child_cpu_seconds','fault')}),flush=True)
    if fault:raise SystemExit(2)
if __name__=='__main__':main()
