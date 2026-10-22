from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys
import uuid

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent / 'IALD_ORQUESTRACAO_20260923'
DEST = HERE / 'orchestration_additional'
DEST.mkdir(exist_ok=True)
RECIPE = HERE.parent.parent / 'TUNEL/PARA_CHATGPT/ORDEM_016_INSUMOS/A6_EQUACAO_DA_VERDADE/A6_RECEITA__ADENDO_001_NUNCA_PUBLICADO.md'
SOURCE = HERE / 'B_fechamentos/TheEquationOfTruth_T20_v3.lean'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, value):
    raw = json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if path.exists():
        old = path.read_bytes()
        backup = path.with_name(path.name + '.bak_' + stamp)
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temp = path.with_name(path.name + '.tmp_' + stamp)
    temp.write_bytes(raw)
    assert temp.read_bytes() == raw and len(raw) > 0
    temp.replace(path)

def excerpt(path, start, end):
    lines = path.read_text(encoding='utf-8-sig').splitlines()
    assert 1 <= start <= end <= len(lines)
    return ('\nSOURCE ' + path.name + '; sha256=' + digest(path) +
            f'; lines={start}-{end}\n' + '\n'.join(
                f'{n}: {lines[n-1]}' for n in range(start, end+1)))

COMMON = '''ORDEM_016, unidade A6 da bancada 01a070fc-9484-7e13-a654-c6b5f61093a4.
Nova unidade cientifica explicitamente autorizada pelo operador, que prioriza Kimi em capacidade maxima.
Receba a memoria canonica comum pelo adaptador. Entregue somente texto/provas/codigo candidato,
sem ferramentas, sem editar arquivos e sem alegar compilacao. Resultado DECLARADO ate verificacao
local. Nao promover resultado a gate ou confirmacao fisica. Nao criar novas camadas de funcoes:
reutilizar lemas existentes, expor hipoteses e eventual lacuna precisa. O fluxo dissipativo
exp(-sH) deste alvo nao e o fluxo modular unitario. Nomes de APIs nao consultados sao candidatos.
'''

UNITS = [
    ('kimi_qubit_entropy_scalar', 'kimi', 'A-6.B3a', 'draft',
     '''Entregue prova escrita completa e decomposicao minima em lemas Lean 4.31 para os cinco
itens ESCALARES de B3a transcritos abaixo. Inclua p=1/2, kappa=0 e s=0 nos dominios corretos.
Prefira monotonicidade/simetria de binEntropy, raiz e exponencial a derivacao se isso reduzir
dependencias. Mostre cada desigualdade necessaria, especialmente r<1 e S(s)<=binEntropy(p).
Nao assumir como hipoteses as conclusoes; nao identificar entropia binaria com entropia de
von Neumann sem decomposicao matricial, que e trabalho separado do harness. Derivada B3b
somente como observacao opcional, fora do escopo da entrega obrigatoria.''',
     [(RECIPE, 334, 343)]),
    ('kimi_finite_gap_norm_rate', 'kimi', 'A-6.B1b', 'draft',
     '''Demonstre ||T_s x-Px|| <= exp(-s*gamma)||x-Px|| para s>=0, gamma>0,
H limitado autoadjunto nao negativo em Hilbert real/complexo de dimensao finita, com cada
autovalor zero ou >=gamma. Reuse eigenvectorBasis e T_apply_eigen das fontes. Entregue prova
escrita e esqueleto Lean, especificando a hipotese do gap no mesmo objeto eigenvalues usado
pela base. Trate ker=top e dimensao zero sem forcar existencia de autovalor positivo.
Separar a desigualdade pontual da eventual igualdade de norma de operador: igualdade exige
gap atingido no complemento nao nulo. Nao usar mera soma das normas que perde a constante 1.
Nao expandir para dimensao infinita (outra unidade ja registrada).''',
     [(RECIPE, 350, 353), (SOURCE, 399, 504)]),
    ('mimo_negative_controls_audit', 'mimo', 'A-6.C1', 'skeptic',
     '''Audite os nove controles C1 abaixo, por calculo exato escrito, e entregue enunciados
Lean minimos candidatos. Identifique qualquer erro na formulacao em vez de ajustar o teste
para passar. Distinga contraexemplo matematico que compila de uma mutacao que nao compila.
Use indices Fin 2 (0 e 1) e declare qual coordenada decai; e2 no texto significa vetor (0,1).
C1.7 ja tem prova local equation_criterion_can_fail: indique reuso em vez de duplicar.
Nos exemplos de exponencial, derive o fluxo efetivo da matriz especificada, nao apenas
declare uma funcao sem liga-la ao gerador. Identifique hipoteses mantidas e retirada em cada
controle. Nao implementar C2 nem harness D; sao unidades separadas. Nao alegar execucao.''',
     [(RECIPE, 374, 388)])
]

sys.path.insert(0, str(BASE))
from iald_orchestrator.runtime import Runtime
runtime = Runtime(recover=False)
catalog = []
for slug, provider, branch, role, question, sources in UNITS:
    path = DEST / (slug + '_submit.json')
    if path.exists():
        payload = json.loads(path.read_bytes())
    else:
        prompt = COMMON + question + ''.join(excerpt(*item) for item in sources)
        constraints = dict(mission_id='ORDEM_016', branch_id=branch, lemma_id=slug,
                           role=role, required_provider=provider, max_calls=1)
        if provider == 'mimo':
            constraints.update(max_cost_usd=None, max_output_tokens=131072)
        payload = dict(operation='submit', request_id=str(uuid.uuid4()),
                       prompt=prompt, execution_constraints=constraints)
        save(path, payload)
        save(DEST / (slug + '_receipt.json'), dict(
            request_id=payload['request_id'], provider=provider, branch=branch,
            origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',
            origin_directory=str(HERE), status='PREPARED_NOT_SUBMITTED',
            at=datetime.now(timezone.utc).isoformat(),
            prompt_sha256=hashlib.sha256(prompt.encode('utf-8')).hexdigest()))
    preview = runtime.preview(payload['prompt'], payload['execution_constraints'])
    save(DEST / (slug + '_preview.json'), preview)
    assert preview.get('selected') == provider, (slug, preview.get('selected'))
    catalog.append(dict(slug=slug, provider=provider, branch=branch,
                        request_id=payload['request_id'], selected=preview['selected'],
                        payload=str(path), payload_sha256=digest(path),
                        status='PREPARED_NOT_SUBMITTED'))
save(DEST / 'prepared_units.json', catalog)
print(json.dumps(catalog, ensure_ascii=False))
