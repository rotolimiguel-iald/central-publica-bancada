"""Prepare one distinct Kimi review of the newly measured local Ward primitive."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid,sys
H=Path(__file__).resolve().parent;C=H.parents[1];D=H/'orchestration_curved_ward_primitive';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
q='''ORDEM_016,A7.b. Revisão cética científica autorizada, memória canônica comum obrigatória.
PERGUNTA ÚNICA: a família quadrática B_t explicitamente construída nos anexos
é uma primitiva local admissível do componente h-c logarítmico medido e qual
é sua próxima condição NÃO satisfeita para entrar na prescrição temporal
FP_a[(1-a)mu^(2a)z^a u], sem confundir esse componente com Q2 completa?
Audite a autoadjunção, a liberdade partial_t deltaH=-K E/2, a descida com
chi inerte e s1h=L_c h, s1c=-[c,c]/2 na convenção declarada.
Se a alegação local estiver correta, escreva explicitamente s1 B_chi e a
condição de compatibilidade que deve ser confrontada com os diagramas de
ordem h²c da mesma prescrição; se incorreta, dê um contraexemplo exato.
Não exigir que A2 seja gradiente Euler-Lagrange como condição geral de
gerador BV: essa questão diferente já foi auditada. Não escolher t, mudar
o regulador, impor Ward=0 ou presumir nulidade do restante da anomalia.
Fundo auxiliar euclidiano4D, Ric=3Kg,Lambda=3K, g fixo, G=g+h, gauge C_g
linear. 087=sigma constante projetado;069=fundo físico sigma=id. A passagem
entre esses recortes não é automática. O controle Euclidiano não é por
definição a projeção compacta ontológica. O não cancelamento está preservado
na prescrição original; a família proposta ainda NÃO foi adotada.
Esta unidade é distinta da primitiva h*hc/A2 e das auditorias de calor livre,
ghost, quartic e perfis radiais já enfileiradas: trata o novo contratermo
quadrático com Kp²+K² e sua primeira extensão não linear/cutoff.
Uma chamada, sem alegar execução ou confirmação. Resultados DECLARADO até
conferência da bancada; nenhum original/kernel/gate alterado.
'''
sources=[C/'TUNEL/DO_CHATGPT/ENTREGA_016_A7b_Ward_K2_e_primitiva_quadratica_local.md',H/'local_quadratic_ward_primitive_check.py',H/'oneform_second_curvature_engine_v2.py',H/'linear_curvature_tadpole/results.json']
chunks=[q];refs=[]
for p in sources:
    lines=p.read_text('utf-8-sig').splitlines();rel=p.relative_to(C)
    chunks.append(f'\nSOURCE {rel}; SHA256 {sha(p)}; lines1-{len(lines)}\n'+'\n'.join(f'{i}: {v}' for i,v in enumerate(lines,1)))
    refs.append(dict(path=str(p),sha256=sha(p),start=1,end=len(lines)))
prompt='\n'.join(chunks);assert len(prompt)<=24000,len(prompt)
rid=str(uuid.uuid4());constraints=dict(mission_id='ORDEM_016',branch_id='A-7.b',lemma_id='curved_hc_log_quadratic_primitive_descent',role='skeptic',required_provider='kimi',max_calls=1)
payload=dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=constraints)
target=D/'kimi_a7_curved_ward_primitive_submit.json';fresh(target,payload)
fresh(D/'receipt.json',dict(at=datetime.now(timezone.utc).isoformat(),origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',origin_directory=str(H),request_id=rid,sources=refs,status='PREPARED_NOT_SUBMITTED',prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest()))
sys.path.insert(0,str(C/'IALD_ORQUESTRACAO_20260923'))
from iald_orchestrator.runtime import Runtime
runtime=Runtime(recover=False);fresh(D/'status_before_preparation.json',runtime.status())
preview=runtime.preview(prompt,constraints);fresh(D/'preview.json',preview);assert preview.get('selected')=='kimi'
entry=dict(provider='kimi',request_id=rid,payload=str(target),payload_sha256=sha(target),prompt_chars=len(prompt),selected='kimi',status='PREPARED_NOT_SUBMITTED',after='orchestration_position_metric')
fresh(D/'prepared_units.json',[entry])
ledger=C/'TUNEL/DO_CHATGPT/LEDGER_016.jsonl';raw=ledger.read_bytes();stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
backup=ledger.with_name(ledger.name+'.bak_'+stamp);backup.write_bytes(raw);assert backup.read_bytes()==raw
event=dict(event='A7_CURVED_WARD_PRIMITIVE_REVIEW_PREPARED',at=datetime.now(timezone.utc).isoformat(),target='A-7.b',provider='kimi',request_id=rid,prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),preview_selected='kimi',external_execution=False)
t=ledger.with_name(ledger.name+'.tmp_'+stamp);t.write_bytes(raw+(json.dumps(event)+'\n').encode());assert t.stat().st_size>len(raw);t.replace(ledger)
print(json.dumps(entry,ensure_ascii=False))
