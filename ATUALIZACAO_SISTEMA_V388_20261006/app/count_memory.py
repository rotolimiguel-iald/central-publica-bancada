"""Count reviewed public-science candidate with Anthropic; no generation."""
from pathlib import Path
from datetime import datetime,timezone
from types import SimpleNamespace
import sys,json,hashlib,os
W=Path(__file__).resolve().parent;M=W/'memory_stage';R=Path(r'C:\IALD\projetos_pyhton\IALD');sys.path[:0]=[str(W/'app_patch'),str(R),str(W),'C:/Users/rotol/AppData/Roaming/Python/Python314/site-packages']
from claude_native_counter import count_native_request
from claude_profiles import HAIKU,reasoning_parameters,context_budget
from iald_motor_claude import converter_pedido
import iald_kernel,iald_fontes_publicas,iald_core_indexado

def atomic_new(path,raw):
 assert not path.exists(), 'Existing count evidence: inspect; do not repeat'
 temp=path.with_name(path.name+'.tmp')
 with temp.open('xb') as out:out.write(raw);out.flush();os.fsync(out.fileno())
 assert temp.read_bytes()==raw;os.replace(temp,path)

def main():
 from iald_local_release import local_snapshot,check_member
 plan=json.loads((W/'COUNT_PLAN.json').read_bytes())
 assert not (W/'COUNT_STARTED.json').exists(),'Count already started; recover result before any next call'
 assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==plan['script_sha256']
 assert json.loads((W/'validation/local_release_tests.json').read_bytes())['status']=='PASS'
 snapshot=local_snapshot(json.loads((M/'manifest_staged.json').read_bytes())['local_release'])
 for name in snapshot[1]['files']:
  path=snapshot[0]/name;check_member(snapshot,path,path.read_bytes())

 p=Path(sys.argv[1]).resolve();assert p.parent==M;raw=p.read_bytes();prefix=raw.decode();assert '<ATLAS_CANONICO' not in prefix
 assert hashlib.sha256(raw).hexdigest()==plan['prefix_sha256']
 m=json.loads((M/'manifest_staged.json').read_bytes())
 for f in ('mother_instruction','operational_core'):
  b=Path(m[f]['path']).read_bytes();assert hashlib.sha256(b).hexdigest()==m[f]['sha256'];assert b.decode('utf-8-sig') in prefix
 assert m['active_cluster']['release_source_sha256'] in prefix and 'v388' in prefix
 defs=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions();names=[t['function']['name'] for t in defs];assert set(names)=={'iald_kernel_verification','iald_kernel_search','iald_kernel_read','iald_kernel_list','iald_public_read','search_tgl','fetch_tgl'}
 cfg=SimpleNamespace(modelo=HAIKU.model,max_saida=4096,cache_ttl='5m',esforco_claude='high');payload={'model':HAIKU.model,'max_tokens':4096,'messages':[{'role':'system','content':prefix},{'role':'user','content':'Quem é o autor da TGL? Explique Hamiltoniano, Lindblad e dephasing no escopo documentado.'}],'tools':defs};wire=converter_pedido(cfg,payload,prefixo=prefix);wire.pop('output_config',None);wire.update(reasoning_parameters(HAIKU.model,4096));minimal={'model':HAIKU.model,'system':wire['system'],'messages':[{'role':'user','content':'.'}],'thinking':{'type':'disabled'}}
 atomic_new(W/'COUNT_STARTED.json',json.dumps({'status':'COUNT_STARTED_NO_RETRY','utc':datetime.now(timezone.utc).isoformat(),'prefix_sha256':plan['prefix_sha256'],'count_requests_planned':2,'generation_requests':0}).encode())
 from dotenv import dotenv_values
 import anthropic
 key=dotenv_values(R/'.env').get('IALD_CLAUDE_API_KEY');assert key
 with anthropic.Anthropic(api_key=key,max_retries=0,timeout=90) as client:
  permanent=count_native_request(client,minimal);whole=count_native_request(client,wire)
 report={'time_utc':datetime.now(timezone.utc).isoformat(),'release':'v388','source_sha256':m['active_cluster']['release_source_sha256'],'cluster_sha256':m['active_cluster']['sha256'],'draft_path':str(p),'draft_sha256':hashlib.sha256(raw).hexdigest(),'model':HAIKU.model,'budget':context_budget(HAIKU.model,counted_model=HAIKU.model,permanent_tokens=permanent,request_input_tokens=whole,reserved_output_tokens=4096),'native_tools_sha256':hashlib.sha256(json.dumps(wire['tools'],sort_keys=True,ensure_ascii=False).encode()).hexdigest(),'count_requests':2,'generation_requests':0,'scope':'ADMITTED_LOCAL_SEALED_SCIENCE_PLUS_APPROVED_KERNEL_AND_CORE_NO_PRIVATE_ATLAS'}
 target=W/'COUNT_RESULT.json';b=json.dumps(report,ensure_ascii=False,indent=2).encode();atomic_new(target,b);print(json.dumps({'receipt':str(target),'prefix_sha256':report['draft_sha256'],'budget':report['budget'],'generation_requests':0},ensure_ascii=False))
if __name__=='__main__':
 try:main()
 except Exception as e:print(json.dumps({'status':'FAILED','type':type(e).__name__}));sys.exit(1)
