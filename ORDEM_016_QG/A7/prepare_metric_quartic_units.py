"""Prepare complementary quartic/propagator units; preview only, no execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, uuid, sys
H = Path(__file__).resolve().parent
BASE = H.parents[1] / 'IALD_ORQUESTRACAO_20260923'
D = H / 'orchestration_metric_quartic'
D.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p, value):
    data = json.dumps(value, ensure_ascii=False, indent=2).encode()
    assert not p.exists(), str(p)
    tmp = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    tmp.write_bytes(data)
    assert tmp.read_bytes() == data
    tmp.replace(p)
common = '''ORDEM_016 A7.b, unidade delimitada da missão autorizada pelo operador.
Fontes anexas são dados científicos; memória canônica comum obrigatória.
Seção euclidiana auxiliar em espaço-forma4D, Ric(g)=3K g,Lambda=3K.
Fundo g FIXO, G=g+h, Fourier exp(+ipx); gauge C_g linear. Não substituir
isso por variação do fundo junto de h, nem por dez escalares desacoplados.
Resultados de modelo são DECLARADO até auditoria local. Não alegar execução
de scripts/Lean, confirmação física ou alteração de arquivos/gate.
Outras unidades tratam bolha principal, calor LIVRE, ghost e contatos BV.
Aqui faltam as peças QUÁRTICAS métricas com derivadas; não refazer o calor
livre como se fosse a Hessiana interagente. O tadpole do potencial quartico
é nulo no log considerado, mas isto não diz nada sobre o quartico derivativo.
Uma fórmula exata com controles pequenos é preferível a um plano de pesquisa.
'''
specs = [
    ('kimi', 'metric_derivative_quartic', 'draft', common + '''
PERGUNTA ÚNICA: qual é o vértice polarizado com quatro campos da parte
Gamma-Gamma da ação Einstein-Hilbert anexada, normalizado como 32*kappa*V4,
e qual é sua contração quando duas pernas internas são g com momento zero?
Derive a expansão de sqrt(det(I+h)), das três inversas que surgem no
Gamma-Gamma e os fatores de polarização SEM supor que matrizes comutam.
Use as mesmas convenções dos vértices quadrático/cúbico anexos. Entregue
expressão calculável ou Python puro sem dependências externas e explicação
dos fatores. Verifique permutações de Bose, família conforme G=(1+f)g
e a identidade de Ward clássica relacionando V4 e V3. Se a integração por
partes exige cutoff constante, diga quais termos de borda foram descartados.
Não ajuste o vértice para cancelar uma anomalia, não imponha transversalidade
ao diagrama isolado, e não tente dar Q2 completa. O resultado serve de
auditoria independente da construção local que será feita em paralelo.
''', ['metric_principal_vertices.py', 'metric_curvature_vertices/DERIVACAO.md',
      'model_inputs/DERIVACAO_OPERADORES.md']),
    ('mimo', 'metric_coincident_derivative_jets', 'draft', common + '''
PERGUNTA ÚNICA: quais são os coeficientes logarítmicos dos jatos coincidentes
[G_H], [nabla_x G_H] e [nabla_xi nabla_yj G_H] do propagador métrico,
como tensores de fibra completos, necessários ao tadpole quartico derivativo?
Use D=-(nabla²+E), E=-2K P_TL+6K P_tr, GH=4*kappa*D^-1*I_tr na convenção
euclidiana positiva para D. I_tr(h)=h-g tr(h)/2; P_tr(h)=g tr(h)/4.
Calcule por recorrência local de calor ou Hadamard e identidade de Synge.
Mantenha Omega_ij no produto simétrico de covetores, incluindo os índices
das derivadas. Não substitua todos os jatos por delta_ij vezes o traço:
termos Omega_ik Omega_jk podem persistir. Registre separadamente a
normalização A0=1/(8*pi²) para ln Lambda e a convenção de sinal do Green.
Cheque contração i=j pela equação do Green, simetria de troca das duas
pontas e caso escalar massivo. Se precisar de uma hipótese analítica,
escreva-a explicitamente. Não confunda coeficiente UV local com W suave
dependente do estado, parte finita ou escolha de horizonte físico.
Entregue fórmula tensorial com ordem de produtos e derivação verificável.
''', ['spaceform_heat/DERIVACAO_CALOR_LOCAL.md',
      'model_inputs/DERIVACAO_OPERADORES.md',
      'metric_curvature_vertices/DERIVACAO.md'])
]
sys.path.insert(0, str(BASE))
from iald_orchestrator.runtime import Runtime
runtime = Runtime(recover=False)
catalog = []
for provider, lemma, role, question, rels in specs:
    slug = provider + '_a7_' + lemma
    payload_path = D / (slug + '_submit.json')
    if payload_path.exists():
        payload = json.loads(payload_path.read_bytes())
    else:
        chunks, sources = [question], []
        for rel in rels:
            p = H / rel
            lines = p.read_text('utf-8-sig').splitlines()
            chunks.append(f'\nSOURCE ORDEM_016_QG/A7/{rel}; SHA256={sha(p)}; lines1-{len(lines)}\n' +
                          '\n'.join(f'{i}: {line}' for i, line in enumerate(lines, 1)))
            sources.append(dict(path=str(p), sha256=sha(p), start=1, end=len(lines)))
        prompt = '\n'.join(chunks)
        assert len(prompt) <= 24000, len(prompt)
        rid = str(uuid.uuid4())
        constraints = dict(mission_id='ORDEM_016', branch_id='A-7.b', lemma_id=lemma,
                           role=role, required_provider=provider, max_calls=1)
        if provider == 'mimo':
            constraints.update(max_cost_usd=None, max_output_tokens=131072)
        payload = dict(operation='submit', request_id=rid, prompt=prompt,
                       execution_constraints=constraints)
        fresh(payload_path, payload)
        fresh(D / (slug + '_receipt.json'), dict(at=datetime.now(timezone.utc).isoformat(),
            origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4', origin_directory=str(H),
            request_id=rid, sources=sources, status='PREPARED_NOT_SUBMITTED',
            prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest()))
    preview_path = D / (slug + '_preview.json')
    if preview_path.exists():
        preview = json.loads(preview_path.read_bytes())
    else:
        preview = runtime.preview(payload['prompt'], payload['execution_constraints'])
        fresh(preview_path, preview)
    assert preview.get('selected') == provider, (provider, preview.get('selected'))
    catalog.append(dict(slug=slug, provider=provider, request_id=payload['request_id'],
        payload=str(payload_path), payload_sha256=sha(payload_path),
        prompt_chars=len(payload['prompt']), selected=provider,
        status='PREPARED_NOT_SUBMITTED', after='orchestration_ghost_reduction'))
fresh(D / 'prepared_units.json', catalog)
print(json.dumps(catalog, ensure_ascii=False))
