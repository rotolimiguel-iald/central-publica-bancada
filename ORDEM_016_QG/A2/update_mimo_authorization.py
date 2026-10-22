from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os

root=Path(__file__).resolve().parents[1]
p=root/'A2/delegation_a23_core.json'
r=json.loads(p.read_bytes())
assert r['job_id'] is None and r['status']=='prepared_awaiting_enforced_controls'
old=r['prompt']
r['prompt']=old.replace(
 'Não executar sem executor MiMo fixado e reserva de custo dentro de US$0,50 no ramo e US$10 na missão.',
 'Usar executor MiMo fixado, em sua capacidade técnica máxima autorizada pelo operador em 24/09/2026, sem teto financeiro local. Manter sigilo e escopo científico.')
r['prompt']=r['prompt'].replace('Resposta em português, até 2500 palavras;', 'Resposta em português, com desenvolvimento suficiente da demonstração;')
r['prompt']=r['prompt'].replace('mantenha a projeção total <=20000 caracteres e bloqueie se não couber.',
 'use a capacidade de contexto disponível para os materiais científicos pertinentes, com recibo de cobertura real, sem alegar leitura de fontes não recebidas.')
assert r['prompt']!=old and 'US$0,50' not in r['prompt']
r['prompt_sha256']=hashlib.sha256(r['prompt'].encode()).hexdigest()
r['max_cost_usd']=None
r['authorization_update']={
 'verified_source_thread_id':'01a0ce2b-8c2f-71b0-a9a8-91b17715a569',
 'user_messages':['01a0d357-671a-7de1-ae66-192c6276126c','01a0d357-672b-7562-9640-79d7796a4c7c'],
 'quotes':['não dê limites ao MImo quero ele no máximo','o limite do Mimo é a própria TGL'],
 'verification':'read_thread: userMessage, not only assistant report',
 'scope':'MiMo only; other subscription quotas preserved; one logical unit, no automatic retry'}
r['status']='prepared_awaiting_provider_lock_schema'
stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
data=json.dumps(r,ensure_ascii=False,indent=2).encode()
for path in [p,root.parent/'IALD_ORQUESTRACAO_20260923/state/session_requests'/f"{r['request_id']}.json"]:
 backup=path.with_name(path.name+'.bak_'+stamp)
 with backup.open('xb') as f:f.write(path.read_bytes())
 tmp=path.with_name(path.name+'.tmp')
 with tmp.open('xb') as f:f.write(data)
 assert tmp.read_bytes()==data
 os.replace(tmp,path)
print(json.dumps({'request_id':r['request_id'],'status':r['status'],'prompt_chars':len(r['prompt'])}))
