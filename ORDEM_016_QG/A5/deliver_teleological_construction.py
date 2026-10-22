from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=ROOT.parent/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(ROOT/'A0'))
from auditar_axiomas import audita
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,b):
    if isinstance(b,str):b=b.encode('utf-8')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes();backup=p.with_name(p.name+'.bak_'+stamp)
        with backup.open('xb') as f:f.write(old)
        assert backup.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+stamp)
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b and b
    tmp.replace(p)
def dump(p,x):save(p,json.dumps(x,ensure_ascii=False,indent=2))

finals=[('TeleologicalTail_v3.lean','teleological_tail_03'),
    ('ScreenMetricAlgebra_v3.lean','screen_metric_03'),
    ('TeleologicalBoundary_v2.lean','teleological_boundary_02'),
    ('TeleologicalUniqueness.lean','teleological_uniqueness_01'),
    ('TeleologicalShift_v3.lean','teleological_shift_03'),
    ('NullRayResponse_v2.lean','null_ray_response_02'),
    ('TeleologicalMatrix_v3.lean','teleological_matrix_02'),
    ('TeleologicalContractBridge_v3.lean','teleological_contract_bridge_01'),
    ('TeleologicalNullSolution_v2.lean','teleological_null_solution_02')]
proofs=[]
for name,label in finals:
    src=HERE/name;log=HERE/(label+'.log');rp=HERE/(label+'.json')
    r=json.loads(rp.read_bytes());a=audita(str(src),str(log))
    assert r['rc']==0 and a['auditoria']=='PASSA'
    assert r['source_sha256']==sha(src) and r['log_sha256']==sha(log)
    assert not r['newer_kernel_files'] and not r['scan_errors']
    proofs.append(dict(source=str(src),source_sha256=sha(src),log=str(log),log_sha256=sha(log),
        receipt=r,receipt_sha256=sha(rp),audit=a))
attempts=[]
for pattern in ['teleological_tail_*.json','screen_metric_*.json','teleological_boundary_*.json',
    'teleological_uniqueness_*.json','teleological_shift_*.json','null_ray_response_*.json',
    'teleological_matrix_*.json','teleological_contract_bridge_*.json','teleological_null_solution_*.json',
    'null_propagator_geometry_*.json']:
    for p in HERE.glob(pattern):
        r=json.loads(p.read_bytes())
        if 'rc' not in r:continue
        attempts.append(dict(path=str(p),sha256=sha(p),receipt=r))
reuse=json.loads((HERE/'null_solution_reuse.json').read_bytes());origin=Path(reuse['source'])
assert sha(origin)==reuse['source_sha256']
lines=origin.read_text(encoding='utf-8-sig').splitlines()
block='\n'.join(lines[reuse['start_line']-1:reuse['end_line']]).rstrip()
assert hashlib.sha256(block.encode()).hexdigest()==reuse['block_sha256']
assert block in (HERE/'TeleologicalNullSolution_v2.lean').read_text(encoding='utf-8')
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
deps=[]
for p in [origin,ROOT/'A1/minimal_imports/ContratoQG_v31_Minimal.lean',
    ROOT.parent/'TUNEL/PARA_CHATGPT/ORDEM_016_a_gravidade_quantica_primeiro.md']:
    deps.append(dict(path=str(p),sha256=sha(p)))
wall=sum(x['receipt']['wall_seconds'] for x in attempts)
cpu=sum(x['receipt']['cpu_user_seconds']+x['receipt']['cpu_kernel_seconds'] for x in attempts)
count=sum(x['audit']['n_declaracoes_auditadas'] for x in proofs)
now=datetime.now(timezone.utc).isoformat()
manifest=dict(status='REAL_A5B_CONDITIONAL_CONSTRUCTION',at=now,opening_sha256=opening,
    proofs=proofs,attempts=attempts,dependencies=deps,reuse=reuse,entries=count,
    wall_seconds=wall,cpu_seconds=cpu,gate_changed=False,
    scope='Teleological NullSolution for supplied T,G,A under explicit continuity and zeroth/first absolute tail moments; no physical H2/T or modular-charge link selected.')
dump(HERE/'teleological_construction_manifest.json',manifest)

ledger=OUT/'LEDGER_016.jsonl';old=ledger.read_bytes();entries=[json.loads(s) for s in old.decode('utf-8-sig').splitlines()];add=[]
reviews=[]
for jid in ['cc64f514-586e-48c9-b6bb-e3b963d16bff','63b4e640-2b1a-4f7e-8213-76b2eb94d3e5']:
    p=HERE/(jid+'_received_response.json');d=json.loads(p.read_bytes());r=d['result']
    disposition=('Energy: accepts restricted no-hidden-first-moment audit; missing three dependency files noted; '
        'section6.2 claim that X<=-Y contradicts Y>=0 rejected (X=-2,Y=1 suffices). No new proof.'
        if jid.startswith('cc64') else
        'Helicity closure not accepted: inverse must be arsinh(p1/r), not artanh; frame lacks radial scaling; '
        'a.e. cocycle substitution t=xi-s lacks common representative justification; shift preserves transverse q; '
        'fiber U(1) action alone does not identify a fixed Lorentz subgroup representation. Draft contains admissions, no compilation.')
    reviews.append(dict(job_id=jid,response_sha256=hashlib.sha256(r['text'].encode()).hexdigest(),
        receipt_sha256=sha(p),usage=r['usage'],disposition=disposition,status='DECLARADO_WITH_LOCAL_REVIEW'))
    if not any(e.get('execution_id')==d['execution_id'] and e.get('event')=='executor_result_reviewed' for e in entries):
        add.append(dict(ts=now,event='executor_result_reviewed',provedor='kimi',alvo='A-3',
            job_id=jid,request_id=d['request_id'],execution_id=d['execution_id'],
            answer_sha256=hashlib.sha256(r['text'].encode()).hexdigest(),usage=r['usage'],
            custo_usd=None,desfecho=disposition))
req='036b85b4-b2cc-4ba6-8ccb-9a8f9a9d5db8';jid='3f2fb970-6b3b-4407-8bba-8b0fb1f67500'
if not any(e.get('job_id')==jid for e in entries):
    p=HERE/'orchestration_propagator_20260924/kimi_teleological_decay_uniqueness_submit.json';d=json.loads(p.read_bytes())
    add.append(dict(ts=now,event='coordination_registered_by_coordinator',provedor='kimi',alvo='A-5',ramo='A-5.b',
        request_id=req,job_id=jid,question_sha256=hashlib.sha256(d['prompt'].encode()).hexdigest(),
        custo_usd=None,desfecho='awaiting_dispatch'))
if add:save(ledger,old+''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in add).encode())
dump(HERE/'received_kimi_reviews.json',reviews)
prices={}
for e in entries+add:
    k=e.get('job_id') or e.get('request_id');v=e.get('cost_estimate_usd',e.get('custo_usd'))
    if k and v is not None:
        try:prices[k]=Decimal(str(v))
        except Exception:pass
cost=sum(prices.values(),Decimal(0))
report=f'''[REAL — compilação isolada; DERIVED sob hipóteses explícitas]
# A5.b — Propagador teleológico construído
Abertura SHA256 `{opening}`.

Para a fonte f=T_nn, c=8πG e cada gerador x+λn, construímos
θ(x)=c∫₀∞f(x+u n)du e a(x)=−c∫₀∞u f(x+u n)du.
Hipóteses nomeadas: continuidade da fonte no gerador, integrabilidade absoluta
da fonte e do primeiro momento em TODA cauda Ioi(λ). São suficientes;
não foram anunciadas necessárias nem verificadas para um tensor físico escolhido.

**Verificado:** a′=θ; θ′=−8πG f; a,θ→0 em +∞; duas soluções
da mesma fonte diferem por A+Bλ; impor ambos os limites nulos dá unicidade.
A mudança de variável de Ioi(0) para Ioi(λ) foi provada, ligando a análise
às fórmulas no espaço-tempo. A resposta h=diag(0,0,−a,−a) é simétrica,
satisfaz h n=0, tem densidade de área a, responde zero à fonte zero e é
covariante por translação para TODA fonte. A covariância é uma identidade
do integrando, inclusive fora do domínio de integrabilidade da integral totalizada;
a interpretação física e as derivadas permanecem restritas à classe admissível.

**Ligação paga ao contrato:** `TeleologicalContractBridge_v3.lean` identifica
por rfl a direção, T_nn e a densidade de área com as definições v3.1.
`construct_null_solution` habita o tipo ORIGINAL `ProbeResidual.NullSolution`
(estrutura reutilizada literalmente, hash/faixa no manifesto). Não é um
tipo mais fraco paralelo. Isso fornece o lado solução da equivalência
H3_iff_null_solution; o empacotamento em H3/import e o elo modular ainda são A5.c–e.

**Escopo:** componente nn linearizada numa direção n fixa. G e T são entradas;
nenhuma covariância de Lorentz completa, outras componentes de Einstein,
tensor local da rede, H2 físico ou modular_charge foram acrescentados.
Nenhum gate/original foi alterado.

**Auditoria:** {count} entradas em {len(proofs)} fontes finais, rc0 e apenas
propext/Classical.choice/Quot.sound; zero admissão nas fontes finais.
{len(attempts)} tentativas preservadas. As três falhas std::bad_alloc do módulo
integral com contrato completo foram superadas separando a compilação e
reutilizando provas num consumidor curto, que passou no mesmo limite de 8192 MiB.
Não se aumentou a memória nem se relaxou o contrato.
Máquina acumulada A5.b: {wall:.6f}s parede/{cpu:.6f}s CPU.
Estimativas monetárias explícitas da missão: US${cost}, incompletas e não fatura.

Manifesto `{HERE/'teleological_construction_manifest.json'}`,
SHA256 `{sha(HERE/'teleological_construction_manifest.json')}`.
As respostas Kimi de energia/helicidades foram recebidas e avaliadas em
`received_kimi_reviews.json`: a segunda NÃO fecha a identificação física alegada.
Kimi de contorno entrou na fila; as demais duas novas unidades aguardam vagas.
**Próximo: A5.c, elo modular_charge. Não move o gate.**
'''
save(OUT/'ENTREGA_016_A5b_propagador_teleologico.md',report)
p=OUT/'ENTREGA_016_PROGRESSO.md';tag='A5B_CONSTRUCTIVE_20260924'
if tag.encode() not in p.read_bytes():save(p,p.read_bytes()+f'\n- {now} — A5.b PAGO sob regularidade/momentos: {count} entradas/{len(proofs)} fontes, NullSolution original habitada; {len(attempts)} tentativas, máquina {wall/3600:.6f}h parede/{cpu/3600:.6f}h CPU. Tempo de bancada não exclusivo. Estimativas US${cost}, incompletas. Não move gate; próximo A5.c. [{tag}]\n'.encode())
print(json.dumps(dict(entries=count,sources=len(proofs),attempts=len(attempts),wall=wall,cpu=cpu,
    manifest=str(HERE/'teleological_construction_manifest.json'),report=str(OUT/'ENTREGA_016_A5b_propagador_teleologico.md'))))
