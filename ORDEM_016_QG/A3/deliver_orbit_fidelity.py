from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib,json,sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
BASE=ROOT.parent/'IALD_ORQUESTRACAO_20260923'
OUT=ROOT.parent/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(ROOT/'A0'))
from auditar_axiomas import audita
now=datetime.now(timezone.utc); stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,data):
    if path.exists():
        previous=path.read_bytes(); backup=path.with_name(path.name+'.bak_'+stamp)
        with backup.open('xb') as f:f.write(previous)
        assert backup.read_bytes()==previous
    temp=path.with_name(path.name+'.tmp_'+stamp)
    with temp.open('xb') as f:f.write(data)
    assert temp.read_bytes()==data and data
    temp.replace(path); assert path.read_bytes()==data

source=HERE/'OrbitTranslationFaithfulness_v2.lean'; log=HERE/'orbit_faithful_02.log'
receipt=json.loads((HERE/'orbit_faithful_02.json').read_text(encoding='utf8'))
assert receipt['rc']==0 and receipt['source_sha256']==sha(source) and receipt['log_sha256']==sha(log)
assert receipt['newer_kernel_files']==[] and receipt['scan_errors']==[]
audit=audita(str(source),str(log)); assert audit['auditoria']=='PASSA',audit
write(HERE/'orbit_faithfulness_axioms.json',json.dumps(audit,ensure_ascii=False,indent=2).encode())
attempts=[json.loads((HERE/f'orbit_faithful_0{i}.json').read_text(encoding='utf8')) for i in [1,2]]
wall=sum(x['wall_seconds'] for x in attempts)
cpu=sum(x['cpu_user_seconds']+x['cpu_kernel_seconds'] for x in attempts)
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')

ledger=OUT/'LEDGER_016.jsonl'; old=ledger.read_bytes()
rows=[json.loads(line) for line in old.decode('utf8').splitlines() if line.strip()]
events=[]
for provider in ['kimi','mimo']:
    request=json.loads((HERE/f'reuse_{provider}_submit_v2.json').read_text(encoding='utf8'))
    job=json.loads((HERE/f'reuse_{provider}_submission_result.json').read_text(encoding='utf8'))
    if not any(r.get('request_id')==request['request_id'] and r.get('event')=='coordination_registered' for r in rows):
        events.append(dict(ts=job['created_at'], recorded_at=now.isoformat(),event='coordination_registered',
                           alvo='A-3',ramo='A-3.d',provedor=provider,request_id=request['request_id'],
                           job_id=job['id'],question_sha256=hashlib.sha256(request['prompt'].encode()).hexdigest(),
                           desfecho='awaiting_dispatch',provider_calls_observed=0,custo_usd=None,
                           execution_constraints=request['execution_constraints']))
failed_path=BASE/'state/handoffs/bcd9cc68-075d-47a7-aee4-c9b24ac9fd34_failed.json'
failed=json.loads(failed_path.read_text(encoding='utf8'))
execution=failed['execution']; assert failed['stage']=='failed' and execution['result'] is None
events.append(dict(ts=failed['updated_at'],recorded_at=now.isoformat(),event='coordination_executor_failed',
                   alvo='A-3',ramo='A-3.d',provedor='kimi',request_id=failed['request_id'],job_id=failed['id'],
                   execution_task_id=execution['id'],desfecho='failed',error=execution['error'],
                   question_sha256=hashlib.sha256(failed['prompt'].encode()).hexdigest(),answer_sha256=None,
                   tokens_in=None,tokens_out=None,custo_usd=None,provider_calls_observed=1,
                   receipt_path=str(failed_path),receipt_sha256=sha(failed_path)))
write(ledger,old+b''.join((json.dumps(event,ensure_ascii=False)+'\n').encode() for event in events))
allrows=rows+events
costs={}
for row in allrows:
    cost=row.get('custo_usd',row.get('cost_usd'))
    if cost is not None:
        costs[row.get('request_id',row.get('job_id',str(len(costs))))]=Decimal(str(cost))
known=sum(costs.values(),Decimal(0))
manifest=dict(status='REAL',utc=now.isoformat(),opening_sha256=opening,source_sha256=sha(source),
              log_sha256=sha(log),audit=audit,attempts=attempts,wall_seconds=wall,cpu_seconds=cpu,
              known_external_cost_usd=str(known),ledger_sha256=sha(ledger),
              scope='Pointwise characters on full future mass shell; not yet the L2 operator bridge.')
write(HERE/'orbit_faithfulness_manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2).encode())
report=f'''[REAL — sete declarações compiladas e auditadas; fidelidade pontual nas órbitas]

# ORDEM 016 — A3, sub-alvo 1 nas três órbitas

UTC {now.isoformat()}. ABERTURA sha256 `{opening}`.

**PAGO no enunciado pontual prescrito:** se `exp(i a·p)=1` para TODO p na órbita
futura de massa zero, então a=0. O mesmo vale no hiperboloide de QUALQUER m>0.
Para o par de helicidades +1⊕−1, os dois caracteres escalares de translação têm
a mesma base nula; sua igualdade ao par identidade implica a mesma conclusão.
O emparelhamento está explícito na assinatura (+---).

O argumento usa toda a órbita contínua, não só a frase «ela gera R⁴».
No cone, seis raios axiais e variação positiva do módulo forçam a⁰±aʲ=0.
No caso massivo, momentos opostos com a mesma energia isolam as componentes
espaciais; energias m e m+r, r>0, isolam a componente temporal. Para qualquer
coeficiente não nulo, um parâmetro positivo produz fase −1, contradizendo fase 1.

**Limite explícito:** a representação unitária em L², sua medida invariante e a
passagem de igualdade quase em toda parte a igualdade pontual por continuidade
e suporte pleno não foram substituídas por este resultado. Não se declara
`W.U a = 1 → a=0` para uma rede W ainda não construída. O lema de helicidades
também não constrói a ação de Lorentz nem o cociclo de helicidade.

**Validação:** OrbitTranslationFaithfulness_v2.lean, rc0, 7 declarações no trio,
zero sorry/axiom novo; duas tentativas preservadas. Primeira falhou na redução
de Fin.cons e numa simplificação de índice, não num contraexemplo. A segunda
usa o mesmo vetor explicitado por componentes. Warnings são de táticas
redundantes, não erros nem provas admitidas. Nenhum arquivo do kernel alterado.
Manifesto com fontes/log/recibos: A3/orbit_faithfulness_manifest.json.
Máquina: {wall/3600:.6f}h parede, {cpu/3600:.6f}h CPU, trabalho comum contado uma vez
para as três órbitas. Teto do sub-alvo respeitado. Gasto externo conhecido somado
por request_id: US${known}; custos não informados continuam desconhecidos.

**Orquestração:** Kimi falhou por limite de consumo, sem resposta científica
e sem repetição. MiMo segue na unidade original conforme coordenação; resultado
ainda não recebido. IDs e falha foram acrescentados ao LEDGER_016, com backup.

**Move / não move:** não move gate; paga a separação dos caracteres na órbita,
insumo para a representação. Próximo passo prescrito: sub-alvo 4 nas três
órbitas, reutilizando o resultado de espectro contínuo da reta de rapidez e
verificando a extensão transversal. Depois vêm energia positiva e boosts.
'''
write(OUT/'ENTREGA_016_A3_1_fidelidade_das_orbitas.md',report.encode())
progress=OUT/'ENTREGA_016_PROGRESSO.md'
bench=(now-datetime.fromisoformat(attempts[0]['utc'])).total_seconds()/3600
write(progress,progress.read_bytes()+f'\n{now.isoformat()} | A3.1 PAGO pontualmente nas três órbitas: +7 declarações auditadas, duas tentativas; elo L2 ainda não alegado. Bancada mínima medida desde primeira compilação {bench:.6f}h; máquina comum {wall/3600:.6f}h parede/{cpu/3600:.6f}h CPU. Custo externo conhecido US${known}; Kimi failed por cota, sem repetição, MiMo pendente. Próximo A3.4.\n'.encode())
print(json.dumps(dict(audit='PASSA',declarations=7,wall_seconds=wall,cpu_seconds=cpu,known_cost=str(known)),ensure_ascii=False))
