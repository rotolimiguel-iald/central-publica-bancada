"""Persist audited parallel reviews and the next admitted work without duplicate calls."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
H=Path(__file__).resolve().parent;OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
D=H/'parallel_adjoint_boundary_delivery';assert not D.exists();D.mkdir()
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,existing=False):
    if p.exists():
        assert existing,p
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
        assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(b);assert b and tmp.read_bytes()==b;tmp.replace(p)
def put(p,v,existing=False):write(p,json.dumps(v,indent=2,ensure_ascii=False).encode('utf-8'),existing)
def append(p,t):write(p,p.read_bytes()+t.encode('utf-8'),True)
folders=['mimo_opposite_endpoint_adjoint_review','deepseek_localized_boundary_review']
audits=[json.loads((H/f/'local_audit.json').read_bytes()) for f in folders]
checks=sum(a['checks'] for a in audits);cpu=sum(a['cpu_seconds'] for a in audits)
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[REAL — respostas recebidas e verificações locais; conclusões científicas com escopo limitado]

MiMo24ad e DeepSeek70e9 concluíram; recibos e respostas integrais preservados
na bancada e lançados UMA vez por execution_task_id no LEDGER_016.jsonl.

MiMo derivou o mesmo adjunto existente:
 A(I,J)=(-1)^|I|(d+lambda)^I(d-eta)^J.
Sua resposta mantém o sinal cX-barcY positivo, o sinal bX-hY negativo e a
multiplicidade2 dos termos de Leibniz para derivadas iguais. Nove controles
locais passaram, com produtos polinomiais não constantes, derivadas repetidas
e mistas e controles negativos de sinal/omissão. Não criamos outro motor.
Nas linhas de teste da resposta, o símbolo de adjunto precisa ser conservado:
derivada original e derivada adjunta não são literalmente o mesmo operador.

DeepSeek identificou corretamente W20/W02/W11 antes da integração por partes
e a representação com jatos até primeira ordem depois de mover a divergência
para o cutoff. Corrigimos a afirmação de que os jatos de segunda ordem estão
inteiramente numa superfície física: eles se reorganizam em derivadas do
cutoff mesmo quando o fluxo de superfície é zero. Controle com
chi=t²(1-t)²,B=t² em[0,1]: superfície0 e ambas integrais=-1/30.

No controle tensorial já especificado, b4=(15/4,9/8,-3/4,-15/8),
Q=(2,2,2,5). Os dois fatores i da divergência Fourier dão
Vraw_boundary=16 Q.b4=-18, logo o contato normalizado raw/16=-9/8.
Com momento total zero, Vraw_boundary=0 exatamente. O perfil com superfície
física não nula proposto na resposta muda o problema e não é o controle
Fourier pedido. Também se preserva a separação: metric_quartic_vertices
calcula GammaGamma; o termo EH completo exige somar o motor de fronteira.
Nove controles locais passaram. O resultado prévio de1321 controles continua
sendo a evidência mais ampla; não foi reexecutado nem substituído.

Nesta entrega: {checks} controles novos, CPU {cpu}s, rc0.
MiMo:356076tokens,419.479s,estimativaUSD0.1652913.
DeepSeek:268952tokens,171.033s,estimativa superiorUSD0.113241636.
Valores lidos dos recibos; não equivalem à fatura.

O coordenador preencheu as duas vagas: Kimi e710b704 no job
d41046ee-a069-4545-a6ba-9c322662af46; MiMo a369dc3e no job
5286ee12-8b8c-44d2-8af3-8dcd5562fe17. Ambos awaiting_dispatch na observação
recebida, não execução presumida. Kimi51c064fb continua próximo em staging.
Mantidos o prazo A7.b20:32UTC, cinco admitidos, uma execução por fornecedor
e três globais. Nenhum prompt independente foi contaminado pelos resultados.

Reprodução: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/audit_mimo_adjoint_deepseek_boundary.py. O script é de intake único;
uma repetição deve preservar recibos e não duplicar custos. Artefatos e log
estão custodiados no manifesto. Originais, kernel e gate intactos; Q2 OPEN.
Abertura sha256={opening}.
'''
write(D/'DERIVACAO.md',report.encode('utf-8'))
write(OUT/'ENTREGA_016_A7b_revisoes_paralelas_adjunto_fronteira.md',report.encode('utf-8'))
paths=[Path(__file__),D/'DERIVACAO.md',H/'audit_mimo_adjoint_deepseek_boundary.py',
 H/'audit_mimo_adjoint_deepseek_boundary_run.log']
for f in folders:paths.extend([H/f/'manifest.json',H/f/'local_audit.json',H/f/'INTAKE.json'])
put(D/'manifest.json',dict(at=now.isoformat(),opening_sha256=opening,checks=checks,cpu_seconds=cpu,
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],full_Q2=False,gate_changed=False))
ledger=OUT/'LEDGER_016.jsonl'
append(ledger,json.dumps(dict(at=now.isoformat(),event='PARALLEL_ADJOINT_BOUNDARY_LOCAL_AUDIT',
 target='A7.b',checks=checks,cpu_seconds=cpu,remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
cost=Decimal(0);seen=set()
for line in ledger.read_text('utf-8').splitlines():
    e=json.loads(line);v=e.get('cost_estimate_usd',e.get('cost_usd'))
    if v is None:continue
    key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id')
    if key and key in seen:continue
    if key:seen.add(key)
    cost+=Decimal(str(v))
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b PROGRESSO: MiMo24ad eDeepSeek70e9 auditados; adjunto existente mantido, fronteira corrigida;{checks}checks,CPU{cpu}s,custo conhecido parcialUSD{cost};Kimi/MiMo novos admitidos,Q2 OPEN. Abertura sha256={opening}.\n')
p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes())
state['parallel_adjoint_boundary_update']=dict(at=now.isoformat(),manifest=str(D/'manifest.json'),
 results='MiMo24ad accepted formal adjoint; DeepSeek70e9 jet order retained, boundary/normalization corrected',
 new_admitted_jobs={'kimi_e710b704':'d41046ee-a069-4545-a6ba-9c322662af46',
 'mimo_a369dc3e':'5286ee12-8b8c-44d2-8af3-8dcd5562fe17'},
 next_kimi_staged='51c064fb-7083-491c-aea0-5a4acea97f43',
 next='Read Kimi ee44/5e1/bd879 and BV reviews; derive compatible EOM normalization and global coefficients without refitting tau',
 own_processes=[],full_Q2=False,gate_changed=False)
put(p,state,True)
print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=checks,cpu_seconds=cpu,known_partial_cost_usd=str(cost))))
