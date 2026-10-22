from pathlib import Path
import json,subprocess,hashlib,sys
B=Path(__file__).resolve().parent
REF=r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json'
def call(req,label):
 p=B/(label+'_REQUEST.json');p.write_text(json.dumps(req,ensure_ascii=False,indent=2),encoding='utf-8')
 r=subprocess.run([sys.executable,'-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\session_memory.py'],input=json.dumps(req),capture_output=True,text=True,encoding='utf-8')
 d=json.loads(r.stdout)
 with (B/(label+'_RESULT.json')).open('x',encoding='utf-8') as f:json.dump(d,f,ensure_ascii=False,indent=2)
 if r.returncode or not d.get('ok'):raise RuntimeError(d)
 return d['result']
s=call({'operation':'get','reference':REF},'GET')
p=B/'OPERADOR_VERBATIM.txt';h=hashlib.sha256(p.read_bytes()).hexdigest()
flow=dict(s['p']);flow['phase']='h3_universal_and_discriminant_priority';flow['next_action']='Ordem19out: ponte material OH-modos-reservatorio adiada pelo operador. Priorizar derivacao H3 universal (sem refazer H3 nulo fixo existente), formulacao da pergunta em quatro linguas e reavaliacao de canais discriminantes acima5sigma, sem prometer resultado nem abrir dado/gate por inferencia. Preservar R4/R5 como criterios abertos; nao usar OH como pre-requisito da exposicao matematica de um.py. Rebase formal dos requisitos e integracao final devem respeitar esta prioridade.'
r=call({'operation':'transition','reference':REF,'actor':{'id':'codex-gerente-tgl','kind':'agent'},'expected_revision':s['revision'],'event_id':'operator-20261019-defer-oh-prioritize-h3-and-discriminant','changes':{'records':[{'id':'operator-20261019-priority-h3','kind':'decision','statute':'INPUT','sources':[{'kind':'artifact','ref':str(p),'sha256':h}],'text':p.read_text(encoding='utf-8')}],'flow':flow}},'PRIORITY_TRANSITION')
print(json.dumps(r,ensure_ascii=False)[:1300])
