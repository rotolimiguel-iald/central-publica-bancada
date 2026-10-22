from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, sys
HERE=Path(__file__).resolve().parent
OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(HERE.parent/'A0'))
from auditar_axiomas import audita
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,raw):
    if p.exists():
        old=p.read_bytes();b=p.with_name(p.name+'.bak_'+stamp)
        with b.open('xb') as f:f.write(old)
        assert b.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+stamp)
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw and raw
    t.replace(p)
def dump(p,d):save(p,json.dumps(d,ensure_ascii=False,indent=2).encode())
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
proofs=[]
for src,label in [('RapidityJacobian_v2.lean','rapidity_jacobian_02'),('OrbitalRapidityMeasure_v4.lean','orbital_measure_04')]:
    s=HERE/src;l=HERE/(label+'.log');r=json.loads((HERE/(label+'.json')).read_text(encoding='utf8'))
    a=audita(str(s),str(l))
    assert r['rc']==0 and not r['newer_kernel_files'] and not r['scan_errors']
    assert r['source_sha256']==sha(s) and r['log_sha256']==sha(l) and a['auditoria']=='PASSA'
    proofs.append(dict(source=str(s),source_sha256=sha(s),log_sha256=sha(l),receipt=r,audit=a))
attempts=[]
for label in ['rapidity_jacobian_01','rapidity_jacobian_02','orbital_measure_01','orbital_measure_02','orbital_measure_02_access','orbital_measure_03','orbital_measure_04']:
    p=HERE/(label+'.json');r=json.loads(p.read_text(encoding='utf8'));attempts.append(dict(label=label,rc=r['rc'],wall_seconds=r['wall_seconds'],cpu_seconds=r['cpu_user_seconds']+r['cpu_kernel_seconds'],receipt_sha256=sha(p)))
units=[];events=[]
for provider in ['mimo','kimi']:
    p=HERE/f'{provider}_parallel_orbit_receipt.json';r=json.loads(p.read_text(encoding='utf8'))
    units.append(dict(provider=provider,request_id=r['request_id'],job_id=r['job_id'],stage='awaiting_dispatch',execution='NOT_STARTED_PENDING_SPECIFIC_EGRESS_APPROVAL',receipt_sha256=sha(p),source_hashes=r['sources']))
    events.append(dict(ts=now.isoformat(),event='dispatch_approval_pending',provedor=provider,request_id=r['request_id'],job_id=r['job_id'],provider_calls_observed=0,custo_usd=None,reason='Coordinator reported automatic review requires specific approval for scientific payload; question presented in coordinator task. No dispatch.'))
ledger=OUT/'LEDGER_016.jsonl'
save(ledger,ledger.read_bytes()+''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events).encode())
# Sum only explicit prices, once per job. Estimates are not an invoice.
latest={}
for line in ledger.read_text(encoding='utf8').splitlines():
    e=json.loads(line);key=e.get('job_id') or e.get('request_id')
    if not key:continue
    price=e.get('cost_estimate_usd')
    if price is None:price=e.get('custo_usd')
    if price is not None:
        try:latest[key]=Decimal(str(price))
        except Exception:pass
cost=dict(label='SUM_OF_EXPLICIT_JOB_ESTIMATES_NOT_INVOICE_NOT_ALL_UNKNOWN_COSTS',usd=str(sum(latest.values(),Decimal(0))),jobs_count=len(latest),values={k:str(v) for k,v in latest.items()})
manifest=dict(status='REAL',utc=now.isoformat(),opening_sha256=opening,proofs=proofs,attempts=attempts,units=units,cost=cost,pending='Physical orbit Hilbert-space transport, boost intertwining, helicity realization; A3.4 not fully paid.')
dump(HERE/'orbital_measure_and_distribution_manifest.json',manifest)
n=sum(x['audit']['n_declaracoes_auditadas'] for x in proofs)
wall=sum(x['wall_seconds'] for x in attempts);cpu=sum(x['cpu_seconds'] for x in attempts)
report=f'''[REAL — mudança de medida compilada; delegações registradas e pendentes de autorização de envio]

# ORDEM 016 — medida orbital e duas novas unidades

UTC {now.isoformat()}. ABERTURA sha256 `{opening}`.

**Construção local:** {n} declarações auditadas nos dois arquivos finais,
rc0 e axiomas somente propext/Classical.choice/Quot.sound; sem sorry ou
axioma novo. Cinco declarações tratam a mudança longitudinal; dez tratam a
medida produto, mensurabilidade e eixo excepcional. A integral ponderada
por 1/sqrt(m²+q₂²+q₃²+p₁²) coincide com a integral do pullback
p₁=sqrt(m²+q₂²+q₃²)sinh ξ. O eixo q=0 tem medida zero para Lebesgue
produto e para a medida ponderada. O enunciado vale para m real e funções
mensuráveis não negativas; o peso é definido pela convenção de inverso
de Lean. A identificação com a órbita física exclui o vértice nulo.

Tentativas preservadas: quatro versões da prova produto, mais uma recusa
de acesso às dependências que não chegou à análise Lean; duas versões do
jacobiano. Máquina total: {wall:.6f}s parede, {cpu:.6f}s CPU.
Nenhum arquivo do kernel original mudou nas compilações autorizadas.

**Limite:** não é ainda a identificação unitária completa dos espaços de
estados físicos, nem a construção da representação de helicidades ou H2.
Não paga A3.4 inteiro e não altera o gate.

**MiMo:** job `{units[0]['job_id']}`. Rascunho mínimo de ausência de
autovetores em L²(Q×R;E) com cociclo isométrico, sem postular gauge trivial.

**Kimi:** job `{units[1]['job_id']}`. Revisão cética da passagem da
fidelidade pontual já compilada para U(a)=I em L²: suporte pleno,
continuidade e testes de suporte finito, sem avaliar uma igualdade a.e.
em eixos nulos. A coordenadora reconciliou o alerta antigo de cota com a
validação Ultra; a nova prévia selecionou Kimi antes do registro.

Ambos mantêm required_provider e max_calls=1, memória comum e fontes com
hash/linhas. **Não enviados:** a revisão automática exigiu aprovação
específica dos pacotes científicos; a coordenadora já perguntou ao
operador. Nenhuma resposta é presumida. DeepSeek anterior segue cancelado,
sem execução, e a unidade antiga Kimi não foi reaberta.

Soma programática dos preços/estimativas explícitos do ledger, uma vez por
job: US$ {cost['usd']} ({cost['jobs_count']} jobs com preço explícito).
Não é fatura nem total completo: custos desconhecidos continuam desconhecidos.
Os dois novos pedidos não tiveram chamada observada.

Manifesto local: `A3/orbital_measure_and_distribution_manifest.json`.
Próximo: transporte L²/intertwining, aproveitando as respostas quando
autorizadas e efetivamente recebidas; revisão do modelo não substitui Lean.
'''
save(OUT/'ENTREGA_016_MEDIDA_A3_4_medida_e_distribuicao.md',report.encode())
p=OUT/'ENTREGA_016_PROGRESSO.md'
save(p,p.read_bytes()+f'\n{now.isoformat()} | A3.4 EM CURSO: mudança de medida e eixo nulo, {n} declarações auditadas rc0; {wall/3600:.6f}h máquina. MiMo/Kimi novos registrados, despacho bloqueado para aprovação específica; DeepSeek cancelado. Estimativas explícitas por job {cost["usd"]} USD, incompletas/não fatura. Gate intacto.\n'.encode())
print(json.dumps(dict(audit='PASSA',declarations=n,wall_seconds=wall,units=units,cost=cost),ensure_ascii=False))
