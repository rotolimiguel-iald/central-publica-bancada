from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT.parent / 'IALD_ORQUESTRACAO_20260923'
DEST = HERE / 'orchestration_remaining_20260924'
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
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

def excerpt(path, start=1, stop=None):
    raw = path.read_bytes()
    lines = raw.decode('utf-8-sig').splitlines()
    stop = min(stop or len(lines), len(lines))
    return (f'\nSOURCE {path.name}; sha256={hashlib.sha256(raw).hexdigest()}; '
            f'lines={start}-{stop}\n' + '\n'.join(
                f'{i}: {lines[i-1]}' for i in range(start, stop+1)))

contract = ROOT / 'A1/minimal_imports/ContratoQG_v31_Minimal.lean'
probe = ROOT / 'A1/v31/ProbeResidualH3v31.lean'
common = (
    'ORDEM_016: pedido novo da bancada 01a070fc-9484-7e13-a654-c6b5f61093a4. '
    'Operador autorizou ampliar tarefas científicas, priorizando Kimi máximo. '
    'Memória científica comum obrigatória é anexada pelo transporte. Fontes abaixo delimitam a unidade. '
    'Sem ferramentas, sem edição de originais, sem afirmar compilação nem mover gate. '
    'Não repetir A3/A4, nem pesquisas gerais. Estatuto da contribuição: DECLARADO até revisão local. '
    'A5.b já construiu por integrais efetivas a NullSolution original sob continuidade e momentos '
    'absolutos de ordens zero e um nas caudas; 35 entradas de auditoria, 9 fontes finais rc0. '
    'H2 físico, tensor local T0 e elo modular não resultam dessa construção. '
    'Reutilize as provas existentes; uma hipótese nomeada não é hipótese descarregada. '
    'Não propor Fock/CCR nem nova rede fora da árvore. A bancada compila e verifica fontes primárias.\n')

units = [
    ('kimi_modular_charge_domain', 'kimi', 'A-5.c', 'skeptic',
     'Pergunta única: quais são os passos matemáticos mínimos, com domínios explícitos, para '
     'ligar o gerador de uma partícula B1=-i*d/dtheta à carga BILATERAL nullPlaneCharge deste '
     'contrato, e qual passo permanece independente dos dados de H2? Audite sinal na convenção '
     'Delta_it(t)=V(-2*pi*t), expectativa versus igualdade de operadores ilimitados, integral '
     'em todo lambda versus unilateral, regularidade Schwartz/domínios e tensor local versus '
     'funcional forjado. Separe o que segue por regra da cadeia do que precisa da identificação '
     'do tensor T0. Não definir T para ajustar a energia. Entregue diagrama de dependências '
     'enxuto e enunciados reutilizáveis, incluindo eventual hipótese ModularChargeLink T0. '
     'A referência CTT2017 é somente a alegação do comentário enviado, não texto primário '
     'verificado nesta unidade: não invente equações/citações nem certifique sua aplicabilidade.',
     [(contract, 150, 168), (contract, 260, 340)]),
    ('kimi_trace_extension_domain', 'kimi', 'A-5.c', 'skeptic',
     'Pergunta única: a extensão por infinito fora do cone positivo de um traço semifinito '
     'pode satisfazer o campo trace_tracial forall x y enviado, e que domínio legítimo permite '
     'a ponte sem confundir o leitor positivo com canonicalTrace? Já existe a prova enviada '
     'positiveTraceReader_not_cyclic para extensão por ZERO; não a refaça nem conclua '
     'impossibilidade de toda extensão. Examine o testemunho 2x2 X=[[1,1],[0,1]], '
     'Y=[[1,0],[0,0]], compare XY/YX, auto-adjunção, positividade e valores finitos versus '
     'infinito. Diga quais hipóteses de canto matricial realizam o argumento no core, e '
     'distinga tau(x*x)=tau(xx*) de tau(xy)=tau(yx) irrestrita. Nenhuma correção automática '
     'do contrato. Entregue argumento exato e um enunciado Lean candidato de escopo restrito.',
     [(KERNEL / 'TGL/ModularRealization.lean', 67, 85),
      (KERNEL / 'TGLExt/V354TraceReaderWall.lean', 1, None)]),
    ('mimo_two_body_first_order', 'mimo', 'A-5.d', 'draft',
     'Pergunta única: qual harness em aritmética exata demonstra primeira ordem não nula '
     'para carga unilateral e primeira ordem nula para carga bilateral em psi(epsilon) '
     'proporcional a Omega+epsilon*phi, com phi genuinamente de dois corpos? Comece pelo '
     'lema algébrico de normalização, Omega ortogonal phi, Kbil Omega=0, Aplus auto-adjunto '
     'e elemento cruzado Re<phi,Aplus Omega> não zero. Explique por que a identidade de '
     'primeira ordem é condicional a esse elemento cruzado e não garante phi físico. '
     'Proponha exemplo finito exatamente computável que distinga excitação de dois corpos '
     'de estado coerente, marque seus limites perante QFT contínua e jamais o venda como '
     'construção de Fock da rede. Forneça fórmulas/sugestão de script Sympy ou Lean, com '
     'controles negativos (elemento cruzado zero, normalização, sinal), sem execução alegada. '
     'Não inferir derivada de entropia física somente da definição windowEntropy.',
     [(contract, 155, 168), (contract, 276, 311)]),
    ('deepseek_import_h3_composition', 'deepseek', 'A-5.e', 'draft',
     'Pergunta única: qual composição Lean mínima reutiliza construct_null_solution e '
     'H3_of_null_solution para produzir o ContratoImportH3 exato, mantendo same_horizon '
     'e expondo TODOS os quantificadores? Atenção: produce recebe TODO h:ContratoH2, '
     'não apenas h2 fixado no índice. Mostre quais hipóteses modular_charge, não-trivialidade '
     'e tela plana precisam depender de h; não as assuma apenas para h2. Preserve T,G,A '
     'e os nomes já existentes; nada de tipo equivalente enfraquecido nem estrutura circular '
     'contendo H3 como campo. Há duplicação textual de NullSolution no módulo da bancada '
     'e no probe original: não importar ambos causando declaração duplicada; proponha '
     'reuso do corpo consumidor em módulo pequeno, sem recompilar kernel. Distinguir '
     'coincidência de estrutura textual, identidade de declaração e equivalência de tipos. '
     'Entregue termo/enunciado candidato e controle que mantém recusado o import vazio '
     '(não fabricar um H2 físico). Rascunho sem alegar compilação.',
     [(probe, 29, 138), (HERE / 'TeleologicalNullSolution_v2.lean', 1, None),
      (contract, 375, 383)]),
]

sys.path.insert(0, str(BASE))
from iald_orchestrator.runtime import Runtime
runtime = Runtime(recover=False)
status = runtime.status()
save(DEST / 'runtime_status.json', {
    'at': datetime.now(timezone.utc).isoformat(),
    'canonical_memory': status.get('canonical_memory'),
    'providers': [{k: p.get(k) for k in ('id','status','model','thinking_effort','context_budget')}
                  for p in status.get('providers', []) if p['id'] in ('kimi','mimo','deepseek')]
})
prepared = []
for slug, provider, branch, role, question, sources in units:
    payload_path = DEST / (slug + '_submit.json')
    if payload_path.exists():
        payload = json.loads(payload_path.read_bytes())
    else:
        prompt = common + question + ''.join(excerpt(*s) for s in sources)
        constraints = dict(mission_id='ORDEM_016', branch_id=branch, lemma_id=slug,
                           role=role, required_provider=provider, max_calls=1)
        if provider in ('mimo', 'deepseek'):
            constraints.update(max_cost_usd=None,
                               max_output_tokens=131072 if provider == 'mimo' else 393216)
        payload = dict(operation='submit', request_id=str(uuid.uuid4()), prompt=prompt,
                       execution_constraints=constraints)
        save(payload_path, payload)
        save(DEST / (slug + '_receipt.json'), dict(
            request_id=payload['request_id'], provider=provider, branch=branch,
            origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',
            origin_directory=str(HERE), status='PREPARED_NOT_SUBMITTED',
            at=datetime.now(timezone.utc).isoformat(),
            prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest()))
    preview = runtime.preview(payload['prompt'], payload['execution_constraints'])
    save(DEST / (slug + '_preview.json'), preview)
    if preview.get('selected') != provider:
        raise RuntimeError('ROTA_NAO_DISPONIVEL: ' + slug)
    prepared.append(dict(slug=slug, provider=provider, branch=branch,
        request_id=payload['request_id'], selected=preview['selected'],
        prompt_chars=len(payload['prompt']), payload=str(payload_path),
        payload_sha256=hashlib.sha256(payload_path.read_bytes()).hexdigest(),
        status='PREPARED_NOT_SUBMITTED'))
save(DEST / 'prepared_units.json', prepared)
print(json.dumps(prepared, ensure_ascii=False))
