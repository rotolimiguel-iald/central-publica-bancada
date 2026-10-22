from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, sys

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / 'TUNEL/DO_CHATGPT'
sys.path.insert(0, str(HERE.parent / 'A0'))
from auditar_axiomas import audita
now = datetime.now(timezone.utc)
stamp = now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, data):
    if p.exists():
        old = p.read_bytes(); backup = p.with_name(p.name+'.bak_'+stamp)
        with backup.open('xb') as f: f.write(old)
        assert backup.read_bytes() == old
    temp = p.with_name(p.name+'.tmp_'+stamp)
    with temp.open('xb') as f: f.write(data)
    assert data and temp.read_bytes() == data
    temp.replace(p)

opening = sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
units = [('OrbitalBoostCovariance_v2.lean', 'orbital_covariance_02'),
         ('PositiveEnergyIntegral_v4.lean', 'positive_energy_integral_04'),
         ('OrbitalPositiveEnergy_v3.lean', 'orbital_energy_01'),
         ('OrbitalStateAnalytic.lean', 'orbital_state_analytic_01'),
         ('OrbitalPositiveEnergyContract.lean', 'orbital_energy_contract_01'),
         ('OrbitalBoostContinuity_v2.lean', 'orbital_continuity_02'),
         ('OrbitalBoostUnitary_v2.lean', 'orbital_unitary_02')]
proofs = []
for name, label in units:
    source, log, rp = HERE/name, HERE/(label+'.log'), HERE/(label+'.json')
    receipt = json.loads(rp.read_text(encoding='utf8'))
    audit = audita(str(source), str(log))
    assert receipt['rc'] == 0 and not receipt['newer_kernel_files'] and not receipt['scan_errors']
    assert receipt['source_sha256'] == sha(source) and receipt['log_sha256'] == sha(log)
    assert audit['auditoria'] == 'PASSA', audit
    proofs.append(dict(source=str(source), source_sha256=sha(source), log_sha256=sha(log),
                       receipt_sha256=sha(rp), receipt=receipt, audit=audit))
attempts=[]
for prefix, count in [('orbital_covariance',2), ('positive_energy_integral',4),
    ('orbital_energy',1), ('orbital_state_analytic',1), ('orbital_energy_contract',1),
    ('orbital_continuity',2), ('orbital_unitary',2)]:
    for i in range(1,count+1):
        label=f'{prefix}_{i:02}'; p=HERE/(label+'.json')
        r=json.loads(p.read_text(encoding='utf8'))
        attempts.append(dict(label=label,sha256=sha(p),rc=r['rc'],wall=r['wall_seconds'],
            cpu=r['cpu_user_seconds']+r['cpu_kernel_seconds'],utc=r['utc']))

dependencies=[]
for name,label in [('OrbitalTranslationOperators_v2.lean','orbital_translation_02'),
    ('OrbitalBoostTransport.lean','orbital_boost_transport_01'),
    ('ProductOrbitalSpectrum_v3.lean','product_orbital_spectrum_03'),
    ('OrbitalMeasureSupport_v2.lean','orbital_support_02')]:
    p=HERE/name; rp=HERE/(label+'.json'); r=json.loads(rp.read_text(encoding='utf8'))
    assert r['rc']==0 and r['source_sha256']==sha(p)
    dependencies.append(dict(path=str(p),sha256=sha(p),receipt_sha256=sha(rp)))
p=HERE.parent/'A1/minimal_imports/ContratoQG_v31_Minimal.lean'
rp=p.parent/'v31_minimal_01.json';r=json.loads(rp.read_text(encoding='utf8'))
assert r['rc']==0 and r['source_sha256']==sha(p)
dependencies.append(dict(path=str(p),sha256=sha(p),receipt_sha256=sha(rp)))

# Record the coordinator's limited independent review of preceding deliveries.
reviews=[]
base=HERE.parents[1]/'IALD_ORQUESTRACAO_20260923/validation'
for name,manifest_name in [('sister_l2_boost_independent_custody.json','l2_boost_spectrum_manifest.json'),
    ('sister_translation_faithfulness_independent_custody.json','translation_operator_faithfulness_manifest.json')]:
    p=base/name; r=json.loads(p.read_text(encoding='utf8'))
    assert r['manifest_sha256']==sha(HERE/manifest_name)
    reviews.append(dict(path=str(p),sha256=sha(p),scope='PREVIOUS_DELIVERY_SOURCE_LOG_REVIEW_NO_FRESH_COMPILATION'))

prices={};unknown=set()
for line in (OUT/'LEDGER_016.jsonl').read_text(encoding='utf8').splitlines():
    item=json.loads(line);key=item.get('job_id') or item.get('request_id')
    if not key:continue
    value=item.get('cost_estimate_usd',item.get('custo_usd'))
    if value is not None:
        try:prices[key]=Decimal(str(value));unknown.discard(key)
        except Exception:pass
    elif item.get('desfecho')=='failed' or 'UNMETERED' in str(item):
        prices.pop(key,None);unknown.add(key)
key='bcacca23-9116-4043-8b69-ac7264009303';prices.pop(key,None);unknown.add(key)
cost=dict(known_explicit_estimates_usd=str(sum(prices.values(),Decimal(0))),
          unknown_jobs=sorted(unknown),scope='NOT_INVOICE_NOT_COMPLETE_TOTAL')
n=sum(p['audit']['n_declaracoes_auditadas'] for p in proofs)
wall=sum(a['wall'] for a in attempts);cpu=sum(a['cpu'] for a in attempts)
elapsed=(now-min(datetime.fromisoformat(a['utc']) for a in attempts)).total_seconds()
manifest=dict(status='REAL',utc=now.isoformat(),opening_sha256=opening,declarations=n,
    proofs=proofs,dependencies=dependencies,attempts=attempts,cost=cost,
    previous_independent_reviews=reviews,machine_wall_seconds=wall,machine_cpu_seconds=cpu,
    elapsed_since_first_compile_seconds=elapsed,
    paid_scope=['A3.2 analytic positive energy of constructed orbital translations',
                'A3.3 strongly continuous unitary wedge-boost group and boostMat translation covariance',
                'A3.5 no normalized boost-invariant one-particle vacuum'],
    not_claimed=['full physical helicity representation','AQFT net and reserved H2 witness',
                 'BW identification of modular group','Fock second quantization',
                 'failure of null_ergodic implication alone'])
save(HERE/'energy_covariance_manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2).encode())
report=f'''[REAL — energia positiva analítica e covariância do boost orbital compiladas]

# ORDEM 016 — A3.2–A3.3 e teste de vácuo A3.5

UTC {now.isoformat()}; ABERTURA sha256 `{opening}`.

**A3.2 PAGO para as translações construídas.** Para a no `forwardCone`
do contrato e todo vetor ψ do espaço orbital L², foi construída
F(z)=∫ exp(i z a·p) dμψ(p), com dμψ=‖ψ(p)‖² dμ(p).
A finitude dessa medida foi provada a partir de ψ∈L². O pareamento
(+---) é não negativo no cone futuro; isso foi demonstrado, não assumido
como campo de estrutura. F é holomorfa para Im z>0, contínua até a borda,
limitada por μψ(Ω), e F(t)=⟨ψ,U(ta)ψ⟩. O lema
`orbital_positive_energy_v31_shape` usa exatamente `forwardCone`,
`upperHalf` e a conclusão analítica do contrato v3.1. Não exige momento
de energia finito: no interior, a derivada tem majorante 1/δ.

**A3.3 PAGO no componente cinemático do boost.** A mudança de rapidez
é ligada à `TGLExt.boostMat` existente por igualdade de coordenadas.
O grupo orbital tem identidade, composição, inversa, norma preservada
e continuidade forte na topologia real. Foi empacotado como equivalência
isométrica complexa, com a igualdade de operadores no tipo do contrato:

    B_s.conjStarAlgEquiv(U(a)) = U(wedgeBoostMap(s,a)).

No raio nulo, a mesma matriz dá B_s U(r n) B_(-s)=U(r exp(s) n).
O sinal vem do transporte pelo boost inverso; não foi trocado por
convenção informal. Isto não identifica ainda B com o grupo modular
de uma álgebra regional, nem deriva o 2π de BW por uma nova definição.

**A3.5 — teste de vácuo:** todo vetor orbital fixo por todos os boosts
é zero; portanto não existe vácuo normalizado com essa invariância no
espaço de uma partícula. É o resultado que exige a etapa de Fock.
Precisão lógica: NÃO foi demonstrado que a implicação `null_ergodic`
isolada seja falsa; ela pode ser satisfeita sem um vácuo físico. O que
não se pode fornecer aqui é o conjunto de condições com vácuo normalizado
e invariância por boosts. Não foi fabricado habitante do tipo reservado.

**Escopo dos três ramos:** energia e translações escalares valem nas
órbitas sem massa e massiva; os lemas permitem fibras complexas. Usar
duas componentes não constrói por si o cociclo físico das helicidades
±1. Essa realização continua aberta; seu controle normativo condicional
está na entrega anterior e permanece com esse estatuto.

**Verificação:** {n} declarações auditadas em {len(proofs)} fontes finais;
{len(attempts)} compilações preservadas, máximo quatro versões compiladas
por módulo. rc0 final, cobertura integral de axiomas, somente o trio,
nenhuma admissão e kernel sem arquivos novos/modificados em cada rodada.
Máquina: {wall:.6f}s parede / {cpu:.6f}s CPU; intervalo desde primeira
compilação desta entrega: {elapsed/3600:.6f}h. Fontes, comandos, logs,
hashes e tentativas em `A3/energy_covariance_manifest.json`.

**Reutilização:** operadores de translação, equivalência L², jacobiano,
ausência de autovetores e a matriz da casa foram importados e ligados.
As duas conferências independentes da coordenadora sobre as entregas
anteriores foram vinculadas por hash no manifesto; eram revisões de
fontes/logs/custódia, sem recompilação, e não se estendem automaticamente
à presente entrega.

**Ainda não pago:** realização física completa das helicidades, rede
local AQFT, identificação modular BW e segunda quantização. Esta entrega
reduz essas pendências pela construção dos operadores e da condição
analítica; não altera `um.py`, originais, kernel, gate ou confirmação física.

Sem nova chamada externa. Estimativas deduplicadas conhecidas: US$
{cost['known_explicit_estimates_usd']}; {len(unknown)} jobs sem custo informado
permanecem desconhecidos. Não é total faturado. As duas unidades MiMo/Kimi
aguardam a confirmação específica de egress já pedida pela coordenação.
Nenhuma chamada foi repetida nem despachada por outra rota.
'''
save(OUT/'ENTREGA_016_A3_energia_covariancia_e_vacuo.md',report.encode())
p=OUT/'ENTREGA_016_PROGRESSO.md'
save(p,p.read_bytes()+f'\n{now.isoformat()} | A3.2 PAGO no setor orbital: holomorfia, borda e coeficiente real do vetor L2; A3.3 grupo unitário fortemente contínuo/covariância boostMat PAGO no componente cinemático; A3.5 ausência de vácuo normalizado boost-fixo medida, sem negar null_ergodic isolado. +{n} declarações auditadas. Máquina {wall/3600:.6f}h parede/{cpu/3600:.6f}h CPU, intervalo {elapsed/3600:.6f}h. Custos conhecidos {cost["known_explicit_estimates_usd"]} USD; desconhecidos preservados. Próximo: helicidades/BW/rede/Fock conforme árvore; gate intacto.\n'.encode())
print(json.dumps(dict(status='PASSA',declarations=n,wall_seconds=wall,cpu_seconds=cpu,
                      elapsed_since_first_compile_hours=elapsed/3600,cost=cost),ensure_ascii=False))
