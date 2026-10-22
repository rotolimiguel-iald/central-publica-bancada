"""Custody and progress for measured A-1 controls; additive byte backups."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

root=Path(__file__).resolve().parents[1]
out=root.parent/'TUNEL/DO_CHATGPT'
stamp=datetime.datetime.now(datetime.timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def create(p,raw):
    assert not p.exists(),p
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw and raw
    tmp.rename(p)
def append(p,raw):
    before=p.read_bytes()
    backup=p.with_name(p.name+'.bak_'+stamp.strftime('%Y%m%d_%H%M%S_%f'))
    create(backup,before)
    content=before+raw
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(content)
    assert tmp.read_bytes()==content and content.startswith(before)
    tmp.replace(p)
    assert p.read_bytes()==content and backup.read_bytes()==before

source=root/'A1/probes/ProbeForgedStress_v2.lean'
log=source.parent/'forged_stress_02.log'
run=subprocess.run([sys.executable,'-X','utf8','-B',str(root/'A0/auditar_axiomas.py'),str(source),str(log)],capture_output=True)
assert run.returncode==0,run.stdout+run.stderr
create(source.parent/'forged_stress_axioms.json',run.stdout)
proof=json.loads(run.stdout)
assert proof[0]['auditoria']=='PASSA'
inspection=root/'A0/orchestration_fallback_inspection.json'
ins=json.loads(inspection.read_text(encoding='utf-8'))
selected=ins['preview']['selected']
assert selected=='claude'
entry={'ts':stamp.isoformat(),'alvo':'A-1','ramo':'A-1.b2','provedor':'local-preview',
       'modelo_informado':selected,'job_id':None,'tokens_in':0,'tokens_cache':0,'tokens_out':0,
       'custo_usd':0,'seconds':None,'question_sha256':ins['prompt_sha256'],
       'answer_sha256':sha(inspection),'turnos_fisica_coordenacao':0,
       'desfecho':'rota_nao_disponivel','reason':'Fallback now callable; preview selects Claude, forbidden by ORDEM 016. No submit, execute or provider request.'}
append(out/'LEDGER_016.jsonl',(json.dumps(entry,ensure_ascii=False)+'\n').encode())
opening=sha(out/'ENTREGA_016_ABERTURA_operador.md')
note=f'''[REAL] Fallback de orquestração disponível; rota da ORDEM 016 não satisfeita.

Abertura SHA256: {opening}
Recibo status/preview: {inspection}
Recibo SHA256: {sha(inspection)}

A instrução global recebida em 24/09/2026 autoriza Runtime(recover=False).status()/preview() quando o MCP não aparece. Ambas consultas responderam. O preview escolheu {selected}; a ORDEM 016 exige MiMo como primeiro rascunhista e proíbe Claude executor. Nenhum pedido foi submetido, nenhum worker adicional foi criado, nenhuma política da instalação foi alterada. Não houve leitura direta de credenciais nem solicitação de modelo. O ledger registra zero tokens e US$ 0 para esta consulta local, não consumo gratuito de uma inferência remota.

Próximo passo: prosseguir na prova local. A disponibilidade operacional anterior fica corrigida ao lado: o fallback funciona; o seletor vigente ainda não executa a rota permitida desta missão. Nada muda no gate ou nas hipóteses matemáticas.
'''
create(out/'ENTREGA_016_MEDIDA_orquestracao_rota_20260924.md',note.encode())
ledger=[json.loads(l) for l in (out/'LEDGER_016.jsonl').read_text(encoding='utf-8').splitlines() if l]
money=sum(float(r.get('custo_usd') or 0) for r in ledger)
tokens=sum(sum(int(r.get(k) or 0) for k in ['tokens_in','tokens_cache','tokens_out']) for r in ledger)
append(out/'ENTREGA_016_PROGRESSO.md',f'\n{stamp.isoformat()} | A-1.a | MEDIDA/NÃO PAGO por memória; dois rc 3221226505; 0.013858611 h parede Lean; 0.013046875 h CPU | A-1.b em curso.\nA-1.b2: controle algébrico independente compilado, 6 teoremas no trio; ligação ao contrato ainda NÃO PAGA. Orquestração: fallback responde, preview escolhe rota proibida; nenhuma chamada externa. Ledger somado: US$ {money}; tokens {tokens}.\n'.encode())
print(json.dumps({'proof_audit':'PASSA','declarations':proof[0]['n_declaracoes_auditadas'],'ledger_usd':money,'ledger_tokens':tokens,'opening_sha256':opening}))
