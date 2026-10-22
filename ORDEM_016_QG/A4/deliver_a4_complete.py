from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib,json,sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=ROOT.parent/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(ROOT/'A0'))
from auditar_axiomas import audita

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,raw):
    if isinstance(raw,str):raw=raw.encode('utf-8')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes();backup=p.with_name(p.name+'.bak_'+stamp)
        with backup.open('xb') as f:f.write(old)
        assert backup.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+stamp)
    with tmp.open('xb') as f:f.write(raw)
    assert raw and tmp.read_bytes()==raw
    tmp.replace(p)
def dump(p,obj):save(p,json.dumps(obj,ensure_ascii=False,indent=2))

now=datetime.now(timezone.utc)
prior=json.loads((HERE/'wick_period_calibration_manifest.json').read_bytes())
proofs=[]
for entry in prior['proofs']:
    src=Path(entry['source']);log=Path(entry['audit']['log'])
    assert sha(src)==entry['source_sha256'] and sha(log)==entry['log_sha256']
    audit=audita(str(src),str(log))
    assert audit['auditoria']=='PASSA' and entry['receipt']['rc']==0
    proofs.append(entry)
attempts=list(prior['attempts'])
for srcname,label in [('KMSStripConditional.lean','kms_strip_01'),('GudermannSpectral.lean','gudermann_01')]:
    src=HERE/srcname;log=HERE/(label+'.log');rp=HERE/(label+'.json')
    r=json.loads(rp.read_bytes());audit=audita(str(src),str(log))
    assert r['rc']==0 and r['newer_kernel_files']==[] and r['scan_errors']==[]
    assert r['source_sha256']==sha(src) and r['log_sha256']==sha(log)
    assert audit['auditoria']=='PASSA'
    proofs.append(dict(source=str(src),source_sha256=sha(src),log_sha256=sha(log),
                       receipt_sha256=sha(rp),receipt=r,audit=audit))
    attempts.append(dict(path=str(rp),sha256=sha(rp),rc=r['rc'],utc=r['utc'],
                         wall=r['wall_seconds'],cpu=r['cpu_user_seconds']+r['cpu_kernel_seconds']))
for a in attempts:assert sha(Path(a['path']))==a['sha256']
algebra_path=HERE/'ten_readings_checked.json'
algebra=json.loads(algebra_path.read_bytes())
assert len(algebra['rows'])==10 and all(algebra['checks'].values())
assert algebra['selected_reading'] is None and not algebra['hypothesis_derived_here']
assert sha(HERE/'check_ten_readings.py')==algebra['script_sha256']
for p,h in algebra['input_hashes'].items():assert sha(Path(p))==h
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
assert opening==prior['opening_sha256']
kernel=Path(proofs[0]['receipt']['kernel'])
deps=list(prior['dependencies'])
for d in deps:assert sha(Path(d['path']))==d['sha256']
for rel in ['TGLExt/ContinuousModularZero.lean',
            '.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Trigonometric/Inverse.lean',
            '.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/StandardSubspace.lean',
            'TGLExt/HorizonBalanceControls.lean']:
    p=kernel/rel;deps.append(dict(path=str(p),sha256=sha(p)))

prices={};unknown=set()
for line in (OUT/'LEDGER_016.jsonl').read_text(encoding='utf-8-sig').splitlines():
    d=json.loads(line);key=d.get('job_id') or d.get('request_id')
    if not key:continue
    value=d.get('cost_estimate_usd',d.get('custo_usd'))
    if value is not None:
        try:prices[key]=Decimal(str(value));unknown.discard(key)
        except Exception:pass
    elif d.get('desfecho')=='failed' or 'UNMETERED' in str(d):
        prices.pop(key,None);unknown.add(key)
for key in ['bcacca23-9116-4043-8b69-ac7264009303','6cdeb9a0-20f7-45af-8b96-4bf5bb35c8f2']:
    prices.pop(key,None);unknown.add(key)
cost=dict(known_explicit_estimates_usd=str(sum(prices.values(),Decimal(0))),
          explicit_estimates_by_unit={k:str(v) for k,v in prices.items()},
          unknown_failed_jobs=sorted(unknown),
          scope='NOT_INVOICE_NOT_COMPLETE_TOTAL; subscriptions/running jobs not priced as zero')
sources=dict(kay_wald=dict(
    title='Theorems on the uniqueness and thermal properties of stationary, nonsingular, quasifree states on spacetimes with a bifurcate Killing horizon',
    doi='10.1016/0370-1573(91)90015-E',accessed_utc=now.isoformat(),
    author_repository='https://pure.york.ac.uk/portal/en/publications/theorems-on-the-uniqueness-and-thermal-properties-of-stationary-n/',
    publisher='https://www.sciencedirect.com/science/article/pii/037015739190015E',
    author_abstract_read=True,full_text_read=False,publisher_access='403',
    cern_access='timeout',
    scope='The author abstract concerns linear scalar fields and bifurcate horizons; it states a Kerr nonexistence result within its framework. Full theorem hypotheses not audited; no automatic application to TGL or observed remnants.'))
dump(HERE/'primary_source_scope.json',sources)
count=sum(p['audit']['n_declaracoes_auditadas'] for p in proofs)
assert count==50 and len(proofs)==8 and len(attempts)==13
wall=sum(a['wall'] for a in attempts)+algebra['elapsed_seconds']
cpu=sum(a['cpu'] for a in attempts)+algebra['cpu_seconds']
elapsed=(now-min(datetime.fromisoformat(a['utc']) for a in attempts)).total_seconds()
manifest=dict(status='REAL_A4_DELIVERED_WITH_KMS_NAMED_OPEN_HYPOTHESES',utc=now.isoformat(),
    opening_sha256=opening,proofs=proofs,declarations=count,attempts=attempts,dependencies=deps,
    parent_manifest_sha256=sha(HERE/'wick_period_calibration_manifest.json'),
    kms_manifest_sha256=sha(HERE/'kms_strip_manifest.json'),
    algebra_file=str(algebra_path),algebra_sha256=sha(algebra_path),
    table_sha256=sha(HERE/'ten_readings_table.md'),sources_sha256=sha(HERE/'primary_source_scope.json'),
    install_receipt_sha256=sha(HERE/'symbolic_runtime_install.json'),
    cost=cost,wall_seconds=wall,cpu_seconds=cpu,elapsed_since_first_A4_compile_seconds=elapsed,
    timing_scope='Compilation attempts plus algebra execution; install/setup and external inference excluded from measured CPU/wall sum. Elapsed interval is not exclusive attention.',
    disposition={'A-4k.1':'PAGO','A-4k.2':'PAGO_EXACT_QUOTIENT_CRITERION',
                 'A-4k.3':'PAGO_CALIBRATION_CONDITIONAL_H2',
                 'A-4k.4':'MEDIDA_NAMED_REGIONAL_KMS_AND_BW_HYPOTHESES',
                 'A-4k.5':'PAGO_PRINCIPAL_BRANCH_WITH_COUNTEREXAMPLE',
                 'A-4k.6':'PAGO_EXACT_ALGEBRA_NOT_PHYSICAL_CLOCK_IDENTIFICATION'},
    open=['Regional analytic KMS for the constructed same pair',
          'Identification tauStar=2pi/kappa_H for that physical horizon and normalization',
          'Kerr state hypotheses and physical sector identification'],
    gate_changed=False,next='A-5 H3 on the same horizon')
dump(HERE/'a4_complete_manifest.json',manifest)

measure=f'''[REAL — compilação condicional; OPEN — faixa KMS regional do par construído]

# ORDEM 016 — MEDIDA A4k.4

UTC {now.isoformat()}; abertura SHA256 `{opening}`.

A tentativa reutilizou exatamente o corpo `KMSAt.rescale` da v3.1 e compôs
dois teoremas: KMS em rapidez a 2π e KMS em tempo de Killing a 2π/κ.
São **condicionais** a `H_regional_modular_strip` e
`H_modular_equals_geometric`. A reescala não produz a função analítica nem
suas duas bordas a partir do círculo. A energia positiva orbital previamente
compilada tampouco fornece, sozinha, a rede e o vácuo regional.

Comando: `lake env lean -j1 -M8192 -R A4 -o A4/KMSStripConditional.olean A4/KMSStripConditional.lean`
(caminhos absolutos/LEAN_PATH e dependências no recibo `kms_strip_01.json`).
rc=0; três declarações auditadas, somente trio; corpo reutilizado comparado.
Log SHA256 `{sha(HERE/'kms_strip_01.log')}`.
Fonte SHA256 `{sha(HERE/'KMSStripConditional.lean')}`.
Tempo da tentativa {proofs[-2]['receipt']['wall_seconds']:.3f}s parede.

O TODO lido em `StandardSubspace.lean` confirma ausência dessa API pronta;
não é demonstração de impossibilidade. O controle `kms_with_incompatible_geometric_data`
do kernel é uma identidade KMS algébrica, não um contraexemplo a todo KMS analítico.
Não se declarou o teto de oito horas consumido: a ordem aceita MEDIDA com a
hipótese nomeada. A revisão Kimi permanece separada da evidência do compilador.
Nenhum gate/original alterado. Próximo ramo: A4k.5/6 (pagos nesta entrega), depois A-5.
'''
save(OUT/'ENTREGA_016_MEDIDA_KMS_faixa_regional.md',measure)
report=f'''[REAL/DERIVED — A4 entregue no escopo abaixo; KMS regional e relógio físico OPEN]

# ORDEM 016 — círculo, KMS e dez leituras

UTC {now.isoformat()}; abertura SHA256 `{opening}`.

**A4k.1–3 PAGO no escopo formal.** Wick liga o boost real complexificado à
rotação e aos três geradores existentes. A projeção polar descende
injetivamente ao quociente R/PZ sse κP=±2π. Para κ,P>0, P=2π/κ.
O coeficiente `rate/(2π)` de `boostSegmentDefect` foi conectado a 1/P;
a reescala e a calibração pelo mesmo N estão provadas. O quociente não
é um teorema geral de regularidade métrica no vértice, nem produz um estado KMS.

**A4k.4 MEDIDA.** Três declarações conectam uma faixa modular KMS assumida
e a identificação BW a KMS em rapidez 2π, depois em tempo de Killing 2π/κ.
`H_regional_modular_strip` e `H_modular_equals_geometric` permanecem explícitas.
Não há novo habitante regional H2. Detalhes em `ENTREGA_016_MEDIDA_KMS_faixa_regional.md`.

**A4k.5 PAGO com correção de domínio.** Definindo gd(x)=arcsin(tanh x),
provou-se qKappa(κ)=sin(gd(κ/2)) e alphaKappa(κ)=cos(gd(κ/2)).
O bicondicional com θ vale no ramo principal [-π/2,π/2]. O contraexemplo
κ=0,θ=2π também foi compilado, refutando o bicondicional irrestrito.
Esse κ é espectral adimensional; nenhuma identificação com κ_H foi feita.

**A4k.6 PAGO como álgebra, não como identificação física.** Sympy verificou
sete identidades exatas e cruzou todas as dez linhas com o C1 e o registro V1
originais, cujos hashes permaneceram iguais. Sob a hipótese nomeada
`H_tauStar_eq_KMS_period`, Γ=πβω²/κ coincide com R-MOD sem rotação.
Em Kerr, trocar ω por ω−mΩ_H exige a ponte física correspondente.
No Schwarzschild o período é 8π GM/c³: **R-B difere por 8π**.
As demais leituras e suas condições, incluindo taxa versus expoente de
propagação e inclinação inicial coerente, estão na tabela anexa das dez.

**Números rechecados, não nova detecção:** para GWTC5_31 e I histórico=887,
R-MOD tem I90=30209,424853; N90 ilustrativo=1055,613124 (teto 1056);
fração=2,936170%. R-B: 0,931566%; R-RAIZ-0: 3,178397%; R-LIN: 11,805783%.
Bonferroni k=4 dá z={algebra['statistics']['z_bonferroni']:.12f} e fator de
planejamento N90={algebra['statistics']['bonferroni_N_factor']:.12f}.
Uma leitura única registrada previamente poderia dispensar esse fator;
**nada aqui escolhe leitura, altera V1 ou demonstra significância observada**.
R-MOD continua `excluded_if_universal=true` no catálogo consultado; uma
partição não universal é decisão física do operador, não conclusão deste cálculo.

**Fonte primária nomeada:** o resumo autoral de Kay–Wald foi lido no
[repositório de York](https://pure.york.ac.uk/portal/en/publications/theorems-on-the-uniqueness-and-thermal-properties-of-stationary-n/).
Ele trata campos escalares lineares e horizontes bifurcados e anuncia uma
obstrução em Kerr dentro desse quadro. O texto integral não foi obtido (editora 403;
CERN timeout); hipóteses completas e aplicação à TGL/remanescentes não estão auditadas.
Não se usou essa referência como prova de ausência de qualquer estado físico em Kerr.

**Verificação e custo:** {count} entradas auditadas em oito fontes finais
(incluem definições e lemas reutilizados); 13 tentativas preservadas, rc0
em todas as finais, somente trio, sem escrita no kernel. {wall/3600:.6f}h
de máquina parede e {cpu/3600:.6f}h CPU nos comandos medidos. Intervalo desde
a primeira compilação A4: {elapsed/3600:.6f}h, não atenção exclusiva.
Sympy 1.14.0/mpmath 1.3.0 instalados em ambiente isolado A4; recibo com hashes.
Estimativas monetárias explícitas deduplicadas da missão:
US${cost['known_explicit_estimates_usd']}; consumo incompleto/assinaturas e
tentativas falhas sem medição não são zero nem fatura.

Manifesto: `{HERE/'a4_complete_manifest.json'}`
SHA256 `{sha(HERE/'a4_complete_manifest.json')}`.
Tabela completa: `{HERE/'ten_readings_table.md'}`
SHA256 `{sha(HERE/'ten_readings_table.md')}`.

**Não move o gate. Próximo: A-5 — H3 no mesmo horizonte.** Parte B pesada,
R7 e PE não foram iniciados por esta entrega; as revisões externas pendentes
serão confrontadas com estas provas, sem reimplementação automática.
'''
save(OUT/'ENTREGA_016_A4_circulo_KMS.md',report)
progress=OUT/'ENTREGA_016_PROGRESSO.md'
tag='A4_COMPLETE_SCOPED_20260924'
if tag.encode() not in progress.read_bytes():
    save(progress,progress.read_bytes()+(f'\n- {now.isoformat()} — A4 entregue: '
        f'k.1–3 PAGO, k.4 MEDIDA, k.5 PAGO no ramo principal, k.6 PAGO álgebra/tabela. '
        f'50 entradas auditadas/8 fontes, 13 tentativas. Máquina {wall/3600:.6f}h '
        f'parede; intervalo bancada {elapsed/3600:.6f}h (não exclusivo). '
        f'Estimativas explícitas acumuladas US${cost["known_explicit_estimates_usd"]}, '
        f'consumo incompleto. Não move gate; próximo A5. [{tag}]\n').encode('utf-8'))
print(json.dumps(dict(status=manifest['status'],declarations=count,wall_seconds=wall,
    cpu_seconds=cpu,cost=cost,report=str(OUT/'ENTREGA_016_A4_circulo_KMS.md')),ensure_ascii=False))
