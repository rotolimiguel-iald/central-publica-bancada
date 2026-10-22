from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sys, uuid

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent / 'IALD_ORQUESTRACAO_20260923'
DEST = HERE / 'orchestration_reviews'
RECIPE = HERE.parent.parent / 'TUNEL/PARA_CHATGPT/ORDEM_016_INSUMOS/A6_EQUACAO_DA_VERDADE/A6_RECEITA__ADENDO_001_NUNCA_PUBLICADO.md'
DEST.mkdir(exist_ok=True)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, value):
    raw = json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')
    if path.exists():
        assert path.read_bytes() == raw, 'Immutable artifact differs: ' + str(path)
        return
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_bytes(raw)
    assert temp.read_bytes() == raw and raw
    temp.replace(path)

def excerpt(path, start=1, end=None):
    lines = path.read_text(encoding='utf-8-sig').splitlines()
    end = len(lines) if end is None else end
    assert 1 <= start <= end <= len(lines)
    return '\nSOURCE ' + path.name + '; sha256=' + sha(path) + f'; lines={start}-{end}\n' + '\n'.join(f'{i}: {lines[i-1]}' for i in range(start, end+1))

common = '''ORDEM_016; bancada 01a070fc-9484-7e13-a654-c6b5f61093a4. Unidade cientifica
autorizada pelo operador, com memoria canonica comum obrigatoria no adaptador. Apenas
texto/codigo candidato: nao alegar execucao, compilacao ou alteracao de arquivos. Resultado
DECLARADO ate verificacao local. Nao mover gate nem alterar escopo. Reutilizar provas existentes;
nao criar camadas redundantes. Distinguir teoria formal, hipoteses e verificacao numerica.
'''

units = [
    ('kimi_transposition_dependency_review', 'kimi', 'A-6.E', 'skeptic',
     '''Revise o plano de transposicao prescrito abaixo. A bancada tem duas variantes de base
com os MESMOS nomes globais: TheEquationOfTruth_T20 (46 originais + 7 extremos/leitura) e
TheEquationOfTruth_T20_v3 (esses 53 + 4 semigrupo/reciproca de tempo unico). As pontes
InscriptionBridge, PenaltyThreeLocksBridge_v2 e OperatorContourBridge_v2 importam a primeira;
FiniteGapRate_v2 importa a segunda. NAO podem ser importadas juntas sem unificar a base.
Os primeiros 28141 bytes da V3 original devem permanecer intactos como referencia. Uma
tentativa medida de acrescentar import no fim falhou: Lean exige imports no inicio.
Proponha o menor grafo de modulos e o procedimento de transposicao/recompilacao que evita
declaracoes duplicadas sem fingir cumprir a exigencia de monolito/prefixo. Distinga o que
depende de ratificacao da gerencia daquilo que e tecnicamente demonstravel. Entregue matriz
de riscos e verificacoes, nao novos teoremas nem valores presumidos de hashes/contagens.
B1d (limite forte em dimensao infinita) continua hipotese nomeada; nao promover a resultado.
Os controles e harness estao em andamento. Esta revisao e distinta dos pedidos de prova
de entropia, gap, tempo unico e limite infinito ja enviados ao Kimi.''',
     [(RECIPE, 444, 488)]),
    ('mimo_mutation_detection_review', 'mimo', 'A-6.C2', 'skeptic',
     '''Audite o script local e o contrato C2 abaixo: cada mutante realmente modifica uma
hipotese/conclusao pretendida? O teste distingue erro Lean, sorry, axioma e ausencia de print?
Procure falso positivo no criterio detected e incompatibilidade entre fonte, log e recibo.
Compare os criterios com o auditor anexado, sem alegar que executou. Liste apenas problemas
concretos com referencia de linha e impacto, ou diga que nao encontrou problema dentro do
escopo inspecionado. Nao refazer C1 (pedido separado), nao propor alterar kernel ou controles
para aprovar. A igualdade dos hashes contra a referencia e medida local, nao sua prova.''',
     [(RECIPE, 389, 413), (HERE/'C_controles/run_mutations.py', 1, None),
      (HERE.parent/'A0/auditar_axiomas.py', 1, None)]),
    ('deepseek_independent_harness_design', 'deepseek', 'A-6.D2', 'skeptic',
     '''Entregue um desenho verificavel do harness independente D2 especificado abaixo,
sobretudo dois pontos: (1) sinal da derivada entropica via mpmath.iv em >=64 pontos,
incluindo p=1/2,c!=0 e |c|^2=0.99 p(1-p), com intervalos estreitos e dominio r>0,r<1;
(2) identidade de entropia relativa pelo log matricial via autodecomposicao exata e avaliacao
50 digitos, tolerancia 1e-40. Explicite como impedir teste circular (usar a mesma formula
dos dois lados) e como tratar autovalores degenerados/kappa=0 separadamente. Proponha
codigo Python minimo candidato so para esses blocos, sem executar, sem usar resultados V1.
Nao assumir uma grade finita como prova universal. Nao derivar gravidade/5sigma desses checks.
Escolha de semente pertence a bancada e sera declarada antes da geracao, nao escolha agora.
Escopo de revisao numerica, distinto do pedido H3 anteriormente enviado ao DeepSeek.''',
     [(RECIPE, 415, 439)])
]

sys.path.insert(0, str(BASE))
from iald_orchestrator.runtime import Runtime
runtime = Runtime(recover=False)
status = runtime.status()
status_path = DEST / 'status_before_preparation.json'
if not status_path.exists():
    save(status_path, status)
catalog = []
for slug, provider, branch, role, question, sources in units:
    path = DEST / (slug + '_submit.json')
    if path.exists():
        payload = json.loads(path.read_bytes())
    else:
        prompt = common + question + ''.join(excerpt(*item) for item in sources)
        constraints = dict(mission_id='ORDEM_016', branch_id=branch, lemma_id=slug,
                           role=role, required_provider=provider, max_calls=1)
        if provider in ('mimo', 'deepseek'):
            constraints.update(max_cost_usd=None, max_output_tokens=131072 if provider == 'mimo' else 393216)
        payload = dict(operation='submit', request_id=str(uuid.uuid4()),
                       prompt=prompt, execution_constraints=constraints)
        save(path, payload)
        save(DEST/(slug+'_receipt.json'), dict(request_id=payload['request_id'],
             provider=provider, branch=branch, origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',
             origin_directory=str(HERE), status='PREPARED_NOT_SUBMITTED',
             at=datetime.now(timezone.utc).isoformat(), prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest()))
    preview = runtime.preview(payload['prompt'], payload['execution_constraints'])
    if not (DEST/(slug+'_preview.json')).exists():
        save(DEST/(slug+'_preview.json'), preview)
    assert preview.get('selected') == provider, (slug, preview.get('selected'))
    catalog.append(dict(slug=slug, provider=provider, branch=branch, request_id=payload['request_id'],
                        selected=preview['selected'], payload=str(path), payload_sha256=sha(path),
                        status='PREPARED_NOT_SUBMITTED'))
save(DEST/'prepared_units.json', catalog)
print(json.dumps(catalog, ensure_ascii=False))
