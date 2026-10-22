from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib,json,sys

HERE=Path(__file__).resolve().parent
OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(HERE.parent/'A0'))
from auditar_axiomas import audita
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,raw):
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes(); b=p.with_name(p.name+'.bak_'+stamp)
        with b.open('xb') as f:f.write(old)
        assert b.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+stamp)
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw and raw
    t.replace(p)

units=[('WickBoostRotation_v2.lean','wick_boost_02'),
       ('RotationGeneratorBridges.lean','rotation_bridges_01'),
       ('PolarMinimalPeriod_v2.lean','polar_period_02'),
       ('PolarQuotientGeometry_v2.lean','polar_quotient_02'),
       ('PeriodHeatCalibration_v3.lean','period_heat_03'),
       ('ContractCalibrationReuse.lean','contract_calibration_01')]
proofs=[]
for name,label in units:
    p=HERE/name;log=HERE/(label+'.log');rp=HERE/(label+'.json')
    r=json.loads(rp.read_text(encoding='utf8'));a=audita(str(p),str(log))
    assert r['rc']==0 and not r['newer_kernel_files'] and not r['scan_errors']
    assert r['source_sha256']==sha(p) and r['log_sha256']==sha(log)
    assert a['auditoria']=='PASSA',a
    proofs.append(dict(source=str(p),source_sha256=sha(p),log_sha256=sha(log),
                       receipt_sha256=sha(rp),receipt=r,audit=a))
attempts=[]
for prefix,count in [('wick_boost',2),('rotation_bridges',1),('polar_period',2),
                     ('polar_quotient',2),('period_heat',3),('contract_calibration',1)]:
    for i in range(1,count+1):
        p=HERE/(f'{prefix}_{i:02}.json');r=json.loads(p.read_text(encoding='utf8'))
        attempts.append(dict(path=str(p),sha256=sha(p),rc=r['rc'],utc=r['utc'],
            wall=r['wall_seconds'],cpu=r['cpu_user_seconds']+r['cpu_kernel_seconds']))
now=datetime.now(timezone.utc)
n=sum(x['audit']['n_declaracoes_auditadas'] for x in proofs)
wall=sum(a['wall'] for a in attempts);cpu=sum(a['cpu'] for a in attempts)
elapsed=(now-min(datetime.fromisoformat(a['utc']) for a in attempts)).total_seconds()
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
reuse=json.loads((HERE/'calibration_reuse_source.json').read_text(encoding='utf8'))
assert sha(Path(reuse['source']))==reuse['source_sha256']
prices={};unknown=set()
for line in (OUT/'LEDGER_016.jsonl').read_text(encoding='utf8').splitlines():
    d=json.loads(line);key=d.get('job_id') or d.get('request_id')
    if not key:continue
    v=d.get('cost_estimate_usd',d.get('custo_usd'))
    if v is not None:
        try:prices[key]=Decimal(str(v));unknown.discard(key)
        except Exception:pass
    elif d.get('desfecho')=='failed' or 'UNMETERED' in str(d):
        prices.pop(key,None);unknown.add(key)
old='bcacca23-9116-4043-8b69-ac7264009303';prices.pop(old,None);unknown.add(old)
cost=dict(known_explicit_estimates_usd=str(sum(prices.values(),Decimal(0))),unknown_jobs=sorted(unknown),
          scope='NOT_INVOICE_NOT_COMPLETE_TOTAL_LIVE_EXECUTION_NOT_YET_METERED')
kernel=Path(proofs[0]['receipt']['kernel'])
deps=[]
for rel in ['TGLExt/SMatrix.lean','TGLExt/BisognanoWichmann.lean','TGLExt/GeometryFluctuation.lean',
            'TGLExt/TheAngleIsTheProjection.lean','TGLExt/BoostHeatConstruction.lean',
            'TGLExt/PlaneWaveMatter.lean','lean-toolchain','lake-manifest.json']:
    p=kernel/rel;deps.append(dict(path=str(p),sha256=sha(p)))
for p in [HERE.parent/'A1/minimal_imports/ContratoQG_v31_Minimal.lean',Path(reuse['source'])]:
    deps.append(dict(path=str(p),sha256=sha(p)))
manifest=dict(status='REAL',utc=now.isoformat(),opening_sha256=opening,proofs=proofs,
              declarations=n,attempts=attempts,reused= reuse,dependencies=deps,cost=cost,
              wall_seconds=wall,cpu_seconds=cpu,elapsed_since_first_compile_seconds=elapsed,
              paid=['A-4k.1 Wick and named generator bridges',
                    'A-4k.2 injective polar quotient criterion and reciprocal period',
                    'A-4k.3 scale calibration and existing H2 conditional linkage'],
              open=['A-4k.4 analytic KMS for regional state','A-4k.5 optional','A-4k.6 ringdown table',
                    'physical identification of period with same-horizon thermal state'])
save(HERE/'wick_period_calibration_manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2).encode())
report=f'''[REAL — A4k.1–A4k.3 compilados no escopo geométrico e de composição]

# ORDEM 016 — Wick, período e calibração

UTC {now.isoformat()}; ABERTURA sha256 `{opening}`.

**A4k.1 PAGO.** A complexificação está ligada entrada a entrada ao boost real
existente. Para W=diag(1,-i), foi provado W⁻¹ B(iφ) W=exp(φGrot)=Smat(φ),
Smat(2π)=I e os lemas explícitos genK=Grot e complexificação(rotGen)=Grot.
Cada exponencial agora está ligada ao objeto existente; nenhum homônimo foi
substituído sem prova. O regime hiperbólico continua distinto da leitura circular.

**A4k.2 PAGO para o critério de quociente pedido.** Construímos o setóide
t~u sse t=u+nP, n inteiro, seu quociente efetivo e a projeção
polarPoint(r,κ,t)=r exp(iκt). Para r>0 e κ≠0, existe mapa F do quociente
para o plano complexo, injetivo e coincidente com essa projeção, SE E SOMENTE SE
κP=2π ou κP=-2π. A prova usa a periodicidade provada de Circle.exp e força
os números de voltas inversos a serem unidades inteiras, ±1. Não assume o
valor do período na definição da condição geométrica.

Para κ>0 e P>0, resulta P=2π/κ e 1/P=κ/(2π). Essa razão foi ligada à
função efetiva boostSegmentDefect: o coeficiente antes escrito como rate/(2π)
pode ser reescrito como 1/P sob o critério demonstrado. Não foi declarado um
teorema de regularidade de uma métrica arbitrária no vértice; o alcance é
exatamente a descida injetiva da projeção polar. A leitura T=1/P ainda depende
da identificação KMS do estado/região, separada em A4k.4.

**A4k.3 PAGO como calibração.** (κ,P)→(cκ,P/c) conserva a condição circular
para c≠0; a temperatura recíproca escala por c e κ/T permanece 2π.
O balanço quadrático do boost existente é equivalente antes/depois da escala,
por reutilização de boost_segment_quadratic_balance_iff. Do contrato v3.1,
foram reaproveitados sem alterar os corpos os teoremas κ=1/ρ(N), κ fixo dado N
e reindexação para qualquer N', condicionados a um habitante H2. Dois lemas
novos ligam o período angular a unruhTemperature e mostram igualdade de
períodos para o mesmo N. Nenhum habitante H2 foi criado por essa composição.

**Verificação:** {n} declarações auditadas em {len(proofs)} fontes finais;
{len(attempts)} compilações preservadas, no máximo três por módulo. rc0,
somente axiomas permitidos, sem admissão nem escrita no kernel. Máquina
{wall/3600:.6f} h parede / {cpu/3600:.6f} h CPU; intervalo de bancada desde
primeira compilação {elapsed/3600:.6f} h. A extração de calibração reutiliza
{len(reuse['reused_names'])} declarações, incluindo definições; não são anunciadas como
novos teoremas. Fontes, hashes, comandos, logs, falhas e origem do trecho
constam de `A4/wick_period_calibration_manifest.json`.

**Próximo:** A4k.4 (KMS de faixa), A4k.5 opcional e A4k.6 (dez leituras).
O período geométrico não determina sozinho um estado KMS, uma rede ou τ★ do
remanescente. A entrega completa A4_circulo_KMS ainda não foi emitida;
nenhuma PE cega da Parte B foi aberta aqui. Gate e originais intactos.

Orquestração: confirmação específica e delegação permanente recebidas;
primeira execução MiMo confirmada running, quatro unidades seguintes na fila.
Sem repetição. Estimativas já recebidas somam US$ {cost['known_explicit_estimates_usd']};
{len(unknown)} unidades anteriores sem custo informado e a execução viva ainda não
medida. Não é total faturado nem alegação de consumo zero.
'''
save(OUT/'ENTREGA_016_A4_Wick_periodo_e_calibracao.md',report.encode())
p=OUT/'ENTREGA_016_PROGRESSO.md'
line=f'\n{now.isoformat()} | A4k.1–3 PAGO no escopo: Wick/geradores existentes, quociente polar injetivo sse κP=±2π, coeficiente no defeito de calor e calibração. {n} declarações/{len(proofs)} fontes auditadas; máquina {wall/3600:.6f}h parede/{cpu/3600:.6f}h CPU; intervalo {elapsed/3600:.6f}h. KMS físico A4k.4 OPEN, segue árvore. Custo conhecido {cost["known_explicit_estimates_usd"]} USD incompleto; MiMo em execução, demais fila.\n'
save(p,p.read_bytes()+line.encode())
print(json.dumps(dict(status='PASSA',declarations=n,wall_seconds=wall,cpu_seconds=cpu,elapsed_hours=elapsed/3600)))
