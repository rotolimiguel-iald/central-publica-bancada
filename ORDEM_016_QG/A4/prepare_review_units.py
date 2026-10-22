from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT.parent / 'IALD_ORQUESTRACAO_20260923'
DEST = HERE / 'orchestration_reviews_20260924'
DEST.mkdir(exist_ok=True)

def save(path, value):
    raw = json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if path.exists():
        before = path.read_bytes()
        backup = path.with_name(path.name + '.bak_' + stamp)
        with backup.open('xb') as stream:
            stream.write(before)
        assert backup.read_bytes() == before
    temp = path.with_name(path.name + '.tmp_' + stamp)
    with temp.open('xb') as stream:
        stream.write(raw)
    assert raw and temp.read_bytes() == raw
    temp.replace(path)

def excerpt(path, start=1, stop=None):
    raw = path.read_bytes()
    lines = raw.decode('utf-8-sig').splitlines()
    stop = min(stop or len(lines), len(lines))
    return (f'\nSOURCE {path.name}; sha256={hashlib.sha256(raw).hexdigest()}; '
            f'lines={start}-{stop}\n' + '\n'.join(
                f'{i}: {lines[i-1]}' for i in range(start, stop+1)))

units = [
    ('kimi_kms_strip_scope', 'kimi', 'skeptic', 'A-4k.4',
     'A pergunta única é: as três declarações compiladas abaixo fecham a condição KMS regional, '
     'ou somente transportam uma condição já assumida, e qual enunciado mínimo exato continua '
     'necessário para o mesmo par regional? Audite a definição vetorial KMSAt, sinais, duas bordas, '
     'limitação da faixa, reescala e identidade BW. Confronte com o resultado anterior: energia '
     'positiva orbital produz coeficiente analítico no semiplano superior, mas ainda não um vácuo '
     'normalizado fixo por boosts nem uma rede regional. Não refaça rescale nem invente rede, '
     'vacuum, Fock ou novos axiomas. Se houver um elo disponível nos trechos que remove uma '
     'hipótese, escreva a composição exata; caso contrário, identifique a hipótese sem chamar '
     'isso de impossibilidade matemática. Entrega: dependências explícitas e eventual contraexemplo '
     'à inferência excessiva, sem afirmar execução de ferramentas ou Lean.',
     [(HERE / 'KMSStripConditional.lean', 1, None),
      (ROOT / 'A1/minimal_imports/ContratoQG_v31_Minimal.lean', 133, 155)]),
    ('kimi_polar_geometry_scope', 'kimi', 'skeptic', 'A-4k.2',
     'A pergunta única é: o teorema polar_descends_injectively_iff demonstra exatamente o critério '
     'do alvo A-4k.2, e qual alcance geométrico ele NÃO estabelece por si? O alvo pede, para '
     'kappa!=0 e r>0, que (r,t)->(r*cos(kappa*t),r*sin(kappa*t)) desça a R/PZ e seja injetiva '
     'em t iff kappa*P=+-2pi, e a composição desse fator no boostSegmentDefect. Audite período '
     'mínimo, múltiplos inteiros, orientação, P=0, domínio r>0, relação de equivalência e '
     'hipóteses de positividade. Diferencie esse critério, regularidade métrica no vértice, '
     'periodicidade euclidiana e KMS lorentziano. NÃO amplie o alvo para provar toda geometria '
     'de cones, não rederive os mesmos lemas, não alegue kernel alterado. Dê parecer com '
     'linhas concretas e somente correções necessárias na interpretação ou enunciado.',
     [(HERE / 'PolarMinimalPeriod_v2.lean', 1, None),
      (HERE / 'PolarQuotientGeometry_v2.lean', 1, None),
      (HERE / 'PeriodHeatCalibration_v3.lean', 1, None)]),
    ('mimo_ten_readings_algebra', 'mimo', 'draft', 'A-4k.6',
     'A pergunta única é: sob a hipótese explicitamente nomeada H_tauStar_eq_KMS_period '
     '(tauStar=2pi/kappa_H), quais das dez leituras do registro coincidem identicamente com '
     'Gamma=beta*tauStar*omega^2/2, e sob quais hipóteses adicionais? Produza uma tabela das '
     'DEZ leituras sem escolher uma. Mostre R-MOD para Omega_H=0 e fator 8pi contra R-B '
     'em Schwarzschild kappa_H=c^3/(4GM). Distinga frequência física e co-rotante, expoente '
     'integrado e taxa, relógios fonte/detector e ocupação. Para números históricos, confira '
     'frações 887/I, N90 e fator de Bonferroni com k=4, sem transformar poder em detecção. '
     'Entregue expressões exatas e roteiro curto de verificações Sympy, sem alegar executá-las. '
     'Beta deve ficar simbólico; se houver cálculo numérico use alpha CODATA2018*sqrt(e), '
     'não literal beta. Não rode dados, não mude V1, não reabra relógios/eco como campanha, '
     'não declare 5sigma observado. Kay-Wald só permanece DECLARADO, pois nenhuma fonte '
     'primária foi enviada. Este é o ramo algébrico autorizado A4k.6, não Parte B pesada.',
     [(ROOT.parent / 'TUNEL/PARA_CHATGPT/ORDEM_016_INSUMOS/ESTADO_RINGDOWN_LEITURAS.json', 1, None)])
]

sys.path.insert(0, str(BASE))
from iald_orchestrator.runtime import Runtime
runtime = Runtime(recover=False)
save(DEST / 'runtime_status.json', runtime.status())
prepared = []
for slug, provider, role, branch, question, sources in units:
    payload_path = DEST / (slug + '_submit.json')
    if payload_path.exists():
        payload = json.loads(payload_path.read_bytes())
    else:
        prompt = ('ORDEM_016. Nova unidade A4 delimitada, solicitada pelo operador para ampliar '
                  'a distribuição com prioridade Kimi. Não repete unidades A3 em fila. '
                  'Use a memória científica comum anexada pelo transporte; os trechos abaixo '
                  'são a bancada atual. Resposta é DECLARADO até verificação local. '
                  'Nenhum original, kernel ou gate será alterado pelo modelo.\n' + question +
                  ''.join(excerpt(*spec) for spec in sources))
        constraints = dict(mission_id='ORDEM_016', branch_id=branch, lemma_id=slug,
                           role=role, required_provider=provider, max_calls=1)
        if provider == 'mimo':
            constraints.update(max_cost_usd=None, max_output_tokens=131072)
        payload = dict(operation='submit', request_id=str(uuid.uuid4()), prompt=prompt,
                       execution_constraints=constraints)
        save(payload_path, payload)
        save(DEST / (slug + '_receipt.json'), dict(
            request_id=payload['request_id'], provider=provider, branch=branch,
            origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',
            origin_directory=str(HERE), status='prepared_not_submitted',
            created_at=datetime.now(timezone.utc).isoformat(),
            prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),
            sources=[str(spec[0]) for spec in sources]))
    preview = runtime.preview(payload['prompt'], payload['execution_constraints'])
    save(DEST / (slug + '_preview.json'), preview)
    if preview.get('selected') != provider:
        raise RuntimeError('ROTA_NAO_DISPONIVEL: ' + slug)
    prepared.append(dict(slug=slug, provider=provider, branch=branch,
        request_id=payload['request_id'], selected=preview['selected'],
        prompt_chars=len(payload['prompt'])))
save(DEST / 'prepared_units.json', prepared)
print(json.dumps(prepared, ensure_ascii=False))
