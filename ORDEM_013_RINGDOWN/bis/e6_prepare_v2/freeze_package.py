"""Freeze preparation pins/delta after metadata-only fixtures; not E6 execution."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def publish(name,raw):
    if len(raw)>25_000_000:raise ValueError('Size cap')
    p=HERE/name;t=p.with_name(p.name+'.pending')
    with t.open('xb') as f:f.write(raw)
    if t.stat().st_size!=len(raw):raise ValueError('Short write')
    os.link(t,p);t.unlink()


def main():
    old=HERE.parent/'e6_prepare'
    before={p.name:sha(p) for p in old.iterdir() if p.is_file()}
    if any(sha(HERE/'v1_snapshot'/name)!=digest for name,digest in before.items()):raise ValueError('V1 bytes differ')
    pins=json.loads((HERE/'SOURCE_PINS.json').read_bytes())
    for section in ('sources','document_pins'):
        for ref in pins[section].values():
            if sha(ROOT/ref['path'])!=ref['sha256']:raise ValueError('Frozen source changed: '+ref['path'])
    tests=json.loads((HERE/'FIXTURE_RESULTS_V2_001.json').read_bytes())
    if tests['negative_accepted'] or tests['failures'] or tests['passed']!=tests['total']:raise ValueError('Fixture failures remain')
    if tests['generator_sha256']!=sha(HERE/'generate_reach_table.py') or tests['fixture_script_sha256']!=sha(HERE/'test_metadata_v2.py'):
        raise ValueError('Tested code changed')
    review=HERE.parent/'e6_review/E6_INDEPENDENT_PREP_REVIEW_V1.md'
    delta=f'''# E6 V2 — delta e handoff para fechamento independente R

**READY_FOR_FOCUSED_REVIEW_NOT_AUTHORIZED.** Preparação congelada em nova árvore; V1 preservada byte a byte e copiada em v1_snapshot. Nenhuma montagem E6 real, autorização E6 real ou extração E7. As 180 células e mapeamento histórico permanecem; não mudou matemática, dados ou leitura escolhida.

Parecer que motivou a correção: `e6_review/E6_INDEPENDENT_PREP_REVIEW_V1.md`, SHA256 `{sha(review)}`.

| Achado | Delta concreto | Fixture focal |
|---|---|---|
| R1 | Recibo V2, predecessores com pin e evidência temporal separada da emissão; piso de ativação E2; sequência efetiva alocação→calibração→TEST; NO_EXECUTION com parede pinada | stage_before_E2_activation; TEST_before_allocation_and_calibration; pins divergentes; datas future/naive/malformed; paredes e GO preexistente positivos |
| R2 | z/lnB/razão física passam pelo mesmo gate; calibração não emite razão física de teste; UNDERPOWERED exige análise válida e insuficiência revisada sem limiar alto | red_gate_physical_ratio; unpaid_partial_NOT_FALSIFIED_UNDERPOWERED; E3.3 ratio; positivos underpowered com z dummy 0.2 e sem número físico |
| R3 | SEMANTIC_UNITS e contrato/schema por rota/campo; quantidades dimensionais, canais, informação, contagem, equivalentes e taxa não intercambiáveis | green_tau_gate_in_Hz; 220/440/IV cruzados; contagem/informação/equivalentes/base temporal; um binding válido por rota |
| R4 | Grupos futuros no contrato atual apenas projeção, dados=false, AWAITING_DATA e físicos null; sem exceção por booleano | future_ET_physical_test e demais grupos; projeções condicionais positivas |
| R5 | Fonte contraditória recusada: dados presentes red/OPEN somente INCONCLUSIVE_SYSTEMATICS; sem dados AWAITING_DATA | red_data_AWAITING_DATA; red_data_INCONCLUSIVE; no_data_OPEN |

[REAL — produtor, não fechamento independente] {tests['passed']}/{tests['total']} verificações finitas corresponderam às expectativas; negativos aceitos=0. O caso ET é exercitado tanto no grupo de regressão quanto na matriz futura. Harness AST exclui main, publicação e renderização; activate usa apenas arquivos fictícios dentro de fixtures_v2_001. A grade vazia é fictícia, não montagem de E0/E4. Evidence bindings em memória têm números dummy, não ciência. Partiais, bloqueados e indisponíveis não foram promovidos a completude.

Interfaces para R: `generate_reach_table.py` acrescenta `check_timeline`, constantes `SEMANTIC_UNITS`, `FUTURE_GROUPS`, `EVIDENCE_VERDICTS`; `check_metric` aceita terceiro argumento `route`. Adaptar namespace AST para incluir essas definições. Recibos/reviews precisam declarar timeline/predecessor do contrato V2. Não reutilizar dados temporais inventados como evidência real.

Não se afirma que hashes ou timestamps de fonte provem execução física ou independência organizacional. Não são pedidos novos GO ou alto poder: autorização histórica é admissível antes da ativação, mas atividade após ela; poder insuficiente continua veredito válido quando a análise é válida. Uma parede real não necessita timestamps de execução inexistente.

Pins finais estão no manifesto pareado. O principal deve encaminhar este delta e o manifesto a R para revisão focal R1–R5. V2 não está liberada por seus próprios testes. O próximo helper de paredes será outra árvore e não autoriza E6 nem fabrica recibos reais.
'''
    publish('DELTA_AND_HANDOFF_V2.md',delta.encode())
    package_names=('generate_reach_table.py','CONTRACT.json','SOURCE_PINS.json','OUTPUT_SCHEMA.json')
    files={}
    for p in sorted(HERE.rglob('*')):
        if not p.is_file():continue
        if p.stat().st_size>25_000_000:raise ValueError('Oversized file')
        files[p.relative_to(HERE).as_posix()]={'sha256':sha(p),'bytes':p.stat().st_size}
    manifest=dict(schema='E6_PREPARATION_MANIFEST_V2',status='FROZEN_AWAITING_INDEPENDENT_R1_R5_CLOSING',
        frozen_utc=datetime.now(timezone.utc).isoformat(),artifacts=files,
        predecessor_manifest_sha256=sha(old/'PREPARATION_MANIFEST.json'),v1_bytes_verified=before,
        activation_package_sha256={name:sha(HERE/name) for name in package_names},
        fixture_evidence_sha256=sha(HERE/'FIXTURE_RESULTS_V2_001.json'),cases=tests['total'],negative_accepted=[],
        main_not_called=True,actual_E6_executed=False,real_authorization_created=False,order_completed=False,
        independent_closing='OPEN_PENDING_R_OR_PRINCIPAL_RELAY',self_hash='external')
    publish('PREPARATION_MANIFEST_V2.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps(dict(status=manifest['status'],manifest_sha256=sha(HERE/'PREPARATION_MANIFEST_V2.json'),
        package=manifest['activation_package_sha256'],delta_sha256=sha(HERE/'DELTA_AND_HANDOFF_V2.md'),fixture_sha256=manifest['fixture_evidence_sha256'])))


if __name__=='__main__':main()
