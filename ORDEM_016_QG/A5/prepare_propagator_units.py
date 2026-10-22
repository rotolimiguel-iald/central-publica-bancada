from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT.parent / 'IALD_ORQUESTRACAO_20260923'
DEST = HERE / 'orchestration_propagator_20260924'
DEST.mkdir(exist_ok=True)

def save(path, value):
    raw = json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if path.exists():
        before = path.read_bytes()
        backup = path.with_name(path.name + '.bak_' + stamp)
        with backup.open('xb') as f:
            f.write(before)
        assert backup.read_bytes() == before
    temp = path.with_name(path.name + '.tmp_' + stamp)
    with temp.open('xb') as f:
        f.write(raw)
    assert temp.read_bytes() == raw and raw
    temp.replace(path)

def excerpt(path, start, stop):
    raw = path.read_bytes()
    lines = raw.decode('utf-8-sig').splitlines()
    stop = min(stop, len(lines))
    return (f'\nSOURCE {path.name}; sha256={hashlib.sha256(raw).hexdigest()}; '
            f'lines={start}-{stop}\n' + '\n'.join(
            f'{i}: {lines[i-1]}' for i in range(start, stop+1)))

contract = ROOT / 'A1/minimal_imports/ContratoQG_v31_Minimal.lean'
common = (
    'ORDEM_016, unidade nova A-5.b da bancada 01a070fc-9484-7e13-a654-c6b5f61093a4. '
    'Pedido atual do operador: distribuir mais trabalho, com prioridade ao Kimi em capacidade máxima. '
    'Memória científica comum vem anexada pelo transporte; estes trechos delimitam o alvo atual. '
    'Não repetir tarefas A3/A4, não executar ferramentas, não modificar kernel/gate/originais, '
    'não afirmar compilação. Resposta é DECLARADO até auditoria local. Não pesquisar literatura. '
    'O alvo autorizado é construir o propagador nulo, sob decaimento NOMEADO, mantendo G como INPUT '
    'e mesmo H2. Não construir Fock nem escolher tensor físico. A5.a já reutiliza toHorizonData '
    'a partir de um ContratoH3; não é existência H3 a partir de H2. '
    'Convenção: para f:R->R, c=8*pi*G, theta(l)=c*integral_(l,infty) f(u)du, '
    'a(l)=-c*integral_(l,infty)(u-l)f(u)du, logo a_prime=theta e theta_prime=-c*f. '
    'A5.b exige as integrais efetivas, não assumir essas derivadas como campos de um tipo.\n')

units = [
    ('kimi_teleological_decay_uniqueness', 'kimi', 'skeptic',
     'Pergunta única: quais hipóteses suficientes explícitas de regularidade e decaimento '
     'fazem essas fórmulas efetivamente resolver e selecionar a solução teleológica, sem esconder '
     'momento finito nem confundir ausência de fonte com ausência de condição de contorno? '
     'Audite sinais, diferenciação das integrais impróprias, termo de fronteira, limites a e theta '
     'em +infinito e diferença homogênea A+B*l. Compare condições necessárias versus suficientes; '
     'dê contraprova concreta quando remover hipótese material. Proponha enunciados exatos '
     'para a prova local e um exemplo não nulo admissível. Não rederive polar/KMS nem declare '
     'tensor local construído. A outra unidade Kimi cuida apenas do levantamento matricial/covariância.'),
    ('kimi_null_propagator_covariance', 'kimi', 'skeptic',
     'Pergunta única: a lei fixa que integra T_nn ao longo x+u*n e devolve uma perturbação '
     'diagonal de tela h22=h33=-a(x), demais entradas zero, satisfaz exatamente '
     'propagator_zero, propagator_covariant para TODA fonte, response_symm, lightcone_gauge '
     'e areaDensity=a do contrato enviado? Analise a propriedade forte forall f, inclusive '
     'f não integrável: a integral de Bochner totalizada em Lean vale zero fora do domínio, '
     'mas isso só é aceitável se a identidade por translação é extensional antes de integrar. '
     'Mostre a identidade (x+u*n)-b=(x-b)+u*n, sinais e fatores 1/2; diferencie covariância '
     'por translação demonstrada de covariância de Lorentz não pedida pelo tipo. Entregue '
     'composição enxuta e objeção concreta se falhar. Não supor que essa resposta especial '
     'resolve todas as componentes de Einstein. A outra unidade Kimi cuida da análise dos limites.'),
    ('mimo_improper_tail_lean_draft', 'mimo', 'draft',
     'Pergunta única: qual prova Lean enxuta, compatível com as integrais reais de Bochner da '
     'Mathlib, estabelece HasDerivAt theta (-c*f(l)) l e HasDerivAt a (theta(l)) l '
     'para f contínua e integrabilidade absoluta de f e u*f em cada cauda Ioi(l)? '
     'Use decomposição da cauda em integral fixa menos integral intervalar; não exigir '
     'derivada de f nem trocar integral imprópria por janela finita como resultado final. '
     'Dê rascunho de lemas/táticas e nomes de API apenas se conhecidos; qualquer nome incerto '
     'deve estar marcado como candidato a conferir. Não alegar execução Lean. Os revisores '
     'Kimi tratam separadamente unicidade/contorno e matriz/covariância; foque o termo de prova analítico.')
]

sys.path.insert(0, str(BASE))
from iald_orchestrator.runtime import Runtime
runtime = Runtime(recover=False)
save(DEST / 'runtime_status.json', runtime.status())
prepared = []
for slug, provider, role, question in units:
    payload_path = DEST / (slug + '_submit.json')
    if payload_path.exists():
        payload = json.loads(payload_path.read_bytes())
    else:
        prompt = common + question + excerpt(contract, 260, 405)
        constraints = dict(mission_id='ORDEM_016', branch_id='A-5.b', lemma_id=slug,
                           role=role, required_provider=provider, max_calls=1)
        if provider == 'mimo':
            constraints.update(max_cost_usd=None, max_output_tokens=131072)
        payload = dict(operation='submit', request_id=str(uuid.uuid4()), prompt=prompt,
                       execution_constraints=constraints)
        save(payload_path, payload)
        save(DEST / (slug + '_receipt.json'), dict(
            request_id=payload['request_id'], provider=provider, branch='A-5.b',
            origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',
            origin_directory=str(HERE), status='prepared_not_submitted_queue_full',
            at=datetime.now(timezone.utc).isoformat(),
            prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),
            source_sha256=hashlib.sha256(contract.read_bytes()).hexdigest()))
    preview = runtime.preview(payload['prompt'], payload['execution_constraints'])
    save(DEST / (slug + '_preview.json'), preview)
    if preview.get('selected') != provider:
        raise RuntimeError('ROTA_NAO_DISPONIVEL: ' + slug)
    prepared.append(dict(slug=slug, provider=provider, request_id=payload['request_id'],
        selected=preview['selected'], prompt_chars=len(payload['prompt']),
        payload=str(payload_path), status='prepared_not_submitted_queue_full'))
save(DEST / 'prepared_units.json', prepared)
print(json.dumps(prepared, ensure_ascii=False))
