"""Prepare two distinct scientific reviews; previews only, no remote execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sys, uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT.parent / 'IALD_ORQUESTRACAO_20260923'
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')
AUDIT = ROOT.parent / 'AUDITORIA_V368_20260919'
CONTRACT = ROOT / 'A1/v31'

def create(path, data):
    assert not path.exists(), path
    raw = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
    temporary = path.with_name(path.name + '.tmp')
    with temporary.open('xb') as stream:
        stream.write(raw)
    assert temporary.read_bytes() == raw
    temporary.rename(path)

def excerpt(path, start=1, end=None):
    raw = path.read_bytes()
    lines = raw.decode('utf-8-sig').splitlines()
    end = len(lines) if end is None else min(end, len(lines))
    digest = hashlib.sha256(raw).hexdigest()
    meta = dict(path=str(path), sha256=digest, start_line=start, end_line=end)
    body = '\n'.join(f'{i}: {lines[i-1]}' for i in range(start, end+1))
    return meta, f'FONTE: {path.name}; SHA256 do arquivo inteiro: {digest}; linhas {start}-{end}\n{body}'

common = '''ORDEM_016, bancada A3, recuperação das construções existentes solicitada expressamente pelo operador. O operador autorizou novas tarefas distintas para Kimi e MiMo. Trabalhe sobre as fontes abaixo e a memória canônica comum acrescida pelo transporte. Não há acesso ao disco por esses caminhos: o conteúdo necessário está transcrito. Não execute ferramentas nem afirme compilação própria. Não altere kernel, um.py, gate ou escolha física. Não rederive a geometria lorentziana já existente. Não confunda declaração, hipótese recebida e conclusão provada; ausência no pacote não é ausência no acervo. Prefira localizar fornecedores e adaptação mínima a acrescentar camadas. A seleção da cunha/boost consta de PhysicalHorizonChange; não peça que o operador a escolha novamente. O contrato v3.1 é um alvo específico a comparar, não um axioma de que nada anterior foi demonstrado. Preserve a distinção entre matriz Lorentz, representação unitária no Hilbert e ação sobre a rede de álgebras. Estatutos e limitações locais precisam acompanhar conclusões.

Estado da bancada: WedgeDraggedFrame_v6 compilou e sete declarações têm auditoria de axiomas no trio; isso é evidência fornecida pela bancada, não execução sua. WedgeKillingNormalization_v4 é RASCUNHO NÃO COMPILADO, suspenso para procurar reaproveitamento. A auditoria de 19/09 já compilou ConexoesExistentes e três adaptadores: não refaça seus wrappers. Uma lista literal remaining em Python ou um comentário histórico não é prova de inexistência. Resposta em português com referências a arquivo/linha. Uma resposta de modelo será revisada localmente; não move gate nem confirma física.
'''

plans = {
 'kimi': {
  'lemma': 'existing_horizon_modular_H2_supplier_chain', 'role': 'skeptic',
  'task': '''TAREFA DE ALTA COMPLEXIDADE: rastrear a cadeia entre o horizonte físico já selecionado, o fluxo modular efetivamente construído na torre e os campos analíticos/representacionais de ContratoH2 v3.1. Produza um mapa fornecedor -> hipótese -> consumidor, sobretudo flow_implemented, kms, boost (V_translations/V_net), bw, translations_continuous/faithful, positive_energy, null_ergodic. Distingua: campos já fornecidos, adaptação de tipos, premissas efetivamente recebidas e lacunas somente neste pacote. Verifique se confundir a matriz 2x2 de boost com unitário causa uma falsa obstrução ou um falso fechamento. Identifique o PRIMEIRO elo exato ainda não conectado após máximo reaproveitamento, sem alegar ausência global. Se estiver conectado, escreva a composição e suas hipóteses, não apenas um veredito. Se necessário, proponha um único reparo mínimo com assinatura Lean ou argumento matemático verificável; não invente nomes de biblioteca. A comparação geométrica fina do frame/normalização está com MiMo: apenas indique dependências, não duplique essa tarefa.''',
  'sources': [(CONTRACT/'ContratoQG_v31.lean',90,260),
              (KERNEL/'ThePhysicalHorizon.lean',1,None),
              (KERNEL/'BisognanoWichmann.lean',1,None),
              (KERNEL/'TheModularFlowIsAHorizon.lean',1,None),
              (KERNEL/'TheMasterFires.lean',1,None),
              (AUDIT/'ConexoesExistentes.lean',1,None),
              (HERE/'WedgeDraggedFrame_v6.lean',1,None)]},
 'mimo': {
  'lemma': 'existing_frame_Killing_normalization_reuse_inventory', 'role': 'draft',
  'task': '''TAREFA DE MÉDIA COMPLEXIDADE: inventário de assinaturas e comparação delimitada dos campos GEOMÉTRICOS de ContratoH2 v3.1: kappa_pos, observer_unit, E, smooth_on, det_unit_on, dragged, fiducial_is_modular. Compare StrongFrame/theCurvedFrame, ConcreteFourFrame, StrongAssembly/qgStrongCertificate_frame, ConexoesExistentes, WedgeDraggedFrame_v6 e os lemas de normalização já presentes no contrato. Diga precisamente quais provas novas do rascunho WedgeKillingNormalization_v4 são redundantes, quais são simples adaptações e qual parte não é fornecida por esses arquivos. Use os dois teoremas frame_ne_curvedFrame para verificar a limitação daquele frame particular; não conclua que inexiste outro frame no acervo. Entregue tabela campo/fornecedor/tipo/hipóteses/compatibilidade e um plano mínimo de composição, incluindo uma proposta textual de código apenas quando necessária. Não resolva BW, energia positiva, teoria inteira nem representação de Wigner: isso é outra unidade. Não escolha ponto de referência N: trabalhe para N admissível arbitrário. Não confunda reutilizar um lema que exige ContratoH2 com construí-lo, pois isso poderia ser circular.''',
  'sources': [(CONTRACT/'ContratoQG_v31.lean',90,260),
              (CONTRACT/'ContratoQG_v31_Teoremas.lean',410,495),
              (CONTRACT/'ContratoQG_v31_Teoremas.lean',680,770),
              (KERNEL/'StrongFrame.lean',1,None),
              (KERNEL/'ConcreteFourFrame.lean',1,None),
              (KERNEL/'StrongAssembly.lean',1,None),
              (AUDIT/'ConexoesExistentes.lean',1,None),
              (HERE/'WedgeDraggedFrame_v6.lean',1,None),
              (HERE/'WedgeKillingNormalization_v4.lean',1,None)]}
}

sys.path.insert(0, str(BASE))
from iald_orchestrator.runtime import Runtime
runtime = Runtime(recover=False)
create(HERE/'reuse_provider_status.json', runtime.status())
summary = []
for provider, plan in plans.items():
    blocks = [excerpt(*entry) for entry in plan['sources']]
    prompt = common + '\n' + plan['task'] + '\n\n' + '\n\n'.join(b[1] for b in blocks)
    constraints = dict(mission_id='ORDEM_016', branch_id='A3.d', lemma_id=plan['lemma'],
                       role=plan['role'], required_provider=provider, max_calls=1)
    if provider == 'mimo':
        constraints.update(max_cost_usd=None, max_output_tokens=131072)
    request_id = str(uuid.uuid4())
    receipt = dict(request_id=request_id, job_id=None, status='prepared',
                   created_at=datetime.now(timezone.utc).isoformat(),
                   origin_thread='01a070fc-9484-7e13-a654-c6b5f61093a4',
                   origin_house='Central de Patentes', origin_folder=str(ROOT),
                   sources=[b[0] for b in blocks], execution_constraints=constraints,
                   prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest())
    payload = dict(operation='submit', request_id=request_id, prompt=prompt,
                   execution_constraints=constraints)
    create(HERE/f'reuse_{provider}_receipt.json', receipt)
    create(BASE/'state/session_requests'/f'{request_id}.json', receipt)
    create(HERE/f'reuse_{provider}_submit.json', payload)
    preview = runtime.preview(prompt, constraints)
    create(HERE/f'reuse_{provider}_preview.json', preview)
    assert preview.get('selected') == provider, (provider, preview.get('status'), preview.get('selected'))
    summary.append(dict(provider=provider, request_id=request_id, selected=preview['selected'],
                        status=preview['status'], prompt_chars=len(prompt),
                        canonical_memory=preview.get('canonical_memory')))
create(HERE/'reuse_dispatch_previews.json', summary)
print(json.dumps(summary, ensure_ascii=False))
