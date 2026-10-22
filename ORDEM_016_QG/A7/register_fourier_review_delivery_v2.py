"""Verify, ledger and publish the bounded Fourier audit."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT';D=H/'fourier_review_audit'
now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b):
 if p.exists():
  bak=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex)
  old=p.read_bytes();bak.write_bytes(old);assert bak.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def append(p,s):write(p,p.read_bytes()+s.encode())
m=D/'manifest.json';mf=json.loads(m.read_bytes())
for row in mf['artifacts']:assert sha(Path(row['path']))==row['sha256']
r=json.loads((D/'results.json').read_bytes());log=H/'fourier_review_audit_run.log'
assert json.loads(log.read_text('utf-8-sig').splitlines()[-1])=={k:v for k,v in r.items() if k!='phase_audit'}
receipt=json.loads((D/'RECEIPT.json').read_bytes())
prompt=H/'orchestration_nonlocal_followup/kimi_a7_meromorphic_fourier_high_harmonics_submit.json'
# Locate only the previously named prepared packet directory; require unique request match.
matches=[]
for p in (H/'orchestration_nonlocal_followup').glob('*submit.json'):
 if receipt['request_id'] in p.read_text('utf-8-sig'):matches.append(p)
assert len(matches)==1,matches
payload=json.loads(matches[0].read_bytes());assert 'prompt' in payload
receipt.update(prompt_sha256=hashlib.sha256(payload['prompt'].encode()).hexdigest(),
 at=now.isoformat(),provider='kimi',target='A7.b',event='RECEIVED_FOURIER_REVIEW_AUDITED',
 cost_status='SUBSCRIPTION_UNKNOWN_NOT_ZERO',remote_call=False)
ledger=O/'LEDGER_016.jsonl';rows=[json.loads(v) for v in ledger.read_text('utf-8-sig').splitlines() if v.strip()]
assert not any(v.get('execution_task_id')==receipt['execution_task_id'] for v in rows)
append(ledger,json.dumps(receipt,ensure_ascii=False)+'\n')
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
delivery=dict(at=now.isoformat(),opening_sha256=opening,scientific_manifest_sha256=sha(m),
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in [m,log,D/'DERIVACAO.md',matches[0],Path(__file__)]],
 checks=r['checks'],cpu_seconds=r['cpu_seconds'],rc=0,full_Q2=False)
p=D/'delivery_manifest.json';assert not p.exists();write(p,json.dumps(delivery,ensure_ascii=False,indent=2).encode())
note=f'''[DERIVED — parecer Fourier auditado; fase ímpar a rastrear na montagem]

{now.isoformat()}. Abertura SHA256 {opening}.

A fórmula Schwinger confirma um fator (-1)^l entre o motor e a
transformada exp(-ip.x) quando se separa C_E i^m. Não alterar o motor
antes de conferir as fases dos geradores e a orientação dos endpoints.

Correções ao parecer: m->m-j permanece válido para multiplicadores
angulares após recomposição; três constantes da tabela estavam erradas;
a fórmula intermediária repetia p^(-2a), e o termo cúbico Gamma tem sinal
negativo. Polinômios em p são visíveis em p²>0, embora locais em x.

Foram{r['checks']} controles exatos, CPU{r['cpu_seconds']}s, rc0:
A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/fourier_review_audit_check.py.
Log SHA256 {sha(log)}. Derivação: {D/'DERIVACAO.md'}.
Manifesto: {p}; SHA256 {sha(p)}.

Q2 permanece OPEN; nenhuma prescrição, fonte, kernel ou gate alterado.
O parecer recebido consumiu tokens registrados no ledger; custo da
assinatura desconhecido. Nenhuma chamada remota nova nesta auditoria.
'''
p=O/'ENTREGA_016_A7b_auditoria_fourier_fase_impar.md';assert not p.exists();write(p,note.encode())
append(O/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b PROGRESS: parecer Fourier auditado,57checks CPU8.8125s; fase ímpar identificada sob convenções fixas, impacto na montagem OPEN; nenhum custo remoto novo.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),fourier_review_delivery=str(D/'delivery_manifest.json'),
 next=['Trace odd Fourier phase through external generators before editing any engine','Audit DeepSeek cutoff reply against existing Hessian','A7b deadline20:32Z; A7c/d,A8,PartB,final still pending'])
write(p,json.dumps(c,ensure_ascii=False,indent=2).encode())
print(json.dumps(dict(checks=r['checks'],cpu_seconds=r['cpu_seconds'],delivery=str(D/'delivery_manifest.json'))))
