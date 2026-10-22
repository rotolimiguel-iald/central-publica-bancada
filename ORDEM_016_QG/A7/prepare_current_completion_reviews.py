"""Prepare three distinct A7.b units; preview only, coordinator owns dispatch."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, sys, uuid

H = Path(__file__).resolve().parent
D = H / 'orchestration_current_completion'
BASE = H.parents[1] / 'IALD_ORQUESTRACAO_20260923'
OUT = H.parents[1] / 'TUNEL' / 'DO_CHATGPT'
D.mkdir(exist_ok=False)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def put(p, value):
    assert not p.exists(), p
    raw = json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')
    t = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    t.write_bytes(raw)
    assert t.read_bytes() == raw
    t.replace(p)

COMMON = r'''ORDEM_016, ramo A-7.b, cálculo da primeira quebra quântica em prescrição explícita.
Unidade delimitada, científica. Memória canônica comum obrigatória, mas não confunda
as identidades modulares da torre com uma demonstração da QME interagente.
Seu texto será DECLARADO até derivação conferida e CAS exato pela bancada.
Não modificar arquivos, não pesquisar outro ramo, não inventar execução/compilação.

CONTEXTO FIXO: auxiliar euclidiano plano R4, x=X-Y, z=x.x, f=1/z.
d_i=partial/partial x_i, portanto partial_X=d e partial_Y=-d nos kernels planos.
Marcadores de derivadas reais, sem inserir i de Fourier silenciosamente.
C(h)_nu=partial_mu h_mu,nu - (1/2)partial_nu tr(h).
G(c)_mu,nu=partial_mu c_nu+partial_nu c_mu; Q=CG=box.
Z=L_c h, w=c^rho partial_rho c, Zbar=Z-delta tr(Z)/2.
Ação livre: S0=1/2<h,Hh>+<b,Ch>-<b,b>/(2ell)+<barc,Qc>.
H G=0, D=H+ell C* C. s0h=Gc, s0c=0, s0barc=-b, s0b=0.
Vghost_chi=integral chi barc C Z, ANTES da integração por partes.
Equivalente: -integral (chi partial_mu barc_nu+partial_mu chi barc_nu) Zbar_mu,nu.
Vantifield=integral hdagger Z+cdagger w; anticampos são externos, não contraem.
Localizando s1chi h=chi Z, s1chi c=chi w, com S0 não localizado:
s0 Vghost_chi+s1chi S0gf=integral b[C,chi]Z-barc[Q,chi]w
=integral partial_mu chi Jgf^mu, módulo divergência compactamente suportada,
Jgf^mu=b_nu Zbar_mu,nu+(partial_mu barc_nu)w^nu-barc_nu partial_mu w^nu.
Aqui s0Z=-G w. O sinal s0barc=+b é incompatível com a ação acima.
chiX=e^(lambda.X),chiY=e^(eta.Y) representam JATOS locais, não cutoffs globais.
As fontes e pares métricos/ghost localizados já foram construídos; faltam os
diagramas das correntes b h c / barc c c e os pesos globais demonstrados.
Não repetir cálculo da fonte preIBP, transvecções ou primeiros jatos externos.
Nenhum contato parcial é por si só Q2. Não ajustar fator para anular resíduo.
Não escolher estado suave W=0 nem declarar ausência de anomalia pela covariância.
'''

MIXED = r'''
PERGUNTA ÚNICA: qual é a inserção efetiva da corrente Jb^mu=b_nu Zbar_mu,nu
no par conectado com o vértice EH cúbico localizado em X, mantendo h externo
em X e c externo em Y, com normalização e sinais derivados do bloco misto?

O inverso bosônico livre é [[GD,G GQ],[GQ G*,0]], com
GD C*=ell^-1 G GQ, C GD=ell^-1 GQ G*, Q GQ=I.
Derive a distribuição <h_ab(X)b_nu(Y)> de G GQ; não tome b-b=0 como ausência
de contribuições mistas. Mantenha constante escalar de GQ e de GD explícitas,
ligadas pela identidade Ward, até comparar com a convenção do código anexado.
No auxiliar plano usamos fibra S_ab,cd=(delta_ac delta_bd+delta_ad delta_bc-
delta_ab delta_cd)/2. A realização GD~S f na bancada retira fatores globais
da ação; não supor que retirar o mesmo fator do misto seja correto.

Entregue o vértice Jb como lista finita de coeficientes
(nu; a<=b; word_h; word_c; mu), para qualquer ghost externo c_r;
e a contração explícita com dois slots h do vértice EH em X. Os dois
emparelhamentos h_X-b_Y/h_X-h_Y devem ser exibidos com multiplicidade.
Pode expressar o vértice EH por uma matriz AX de jatos já fornecida pela bancada;
não precisa rederivar EH. Dê algoritmo que aceite AX arbitrária simétrica e
uma avaliação racional não axial com uma AX simples declarada, r=0,eta=e0,
x=(1,2,-1,1), mostrando um controle não zero quando se remove Jb.
Separe transposição formal, derivadas em Y e multiplicidade tensorial.
Preserve componentes simétricas: base Eab tem duas entradas1 se a!=b;
coordenada é h_ab, pareamento completo tem peso m_ab=2-delta_ab.
O código usa 10 componentes e 50 jatos de ordem<=1 no vértice EH, mas
propagadores derivados podem ter ordem maior. Não duplicar m_ab e emparelhamentos.

Se houver incompatibilidade de escala entre uma fórmula e o código, dê a
equação exata de conversão e mantenha o fator nomeado, sem escolher para fechar.
Alvo é o diagrama misto, não a primitiva total nem a QME.
'''

WEIGHTS = r'''
PERGUNTA ÚNICA: quais pesos e sinais de Wick, simetria e BRST devem multiplicar
os blocos par métrico, par ghost, fonte antifield e inserções das correntes
no coeficiente bilocal h(X)c(Y) da Ward em ordem hbar e segunda ordem de interação?
Derive por diferenciação funcional graduada com convenções explícitas, em vez
de inferir fatores dos valores já medidos. NÃO calcular novamente os kernels.

Fixe expansão T exp(i V/hbar); apresente também a versão sem i usando
exp(hbar Gamma_G), deixando dicionário entre ambas. Especifique derivadas
esquerda/direita ímpares, ordenação dos campos (h,b,c,barc) e onde fica o
ghost externo. A covariância graduada no setor(c,barc) é [[0,GQ],[-GQ,0]].
Anticampos não contraem. Escreva V3h=1/3! V_ABC h_A h_B h_C e
V3gh=barc_alpha W_alpha,A,beta h_A c_beta; diferencie até restarem h/c.
Use Jmetric=1/2 J_AB,r h_A h_B c_r e Jb=B_nu,A,r b_nu h_A c_r,
Jghost=(dbarc) c.dc-barc d(c.dc), com todos os jatos como slots distintos.
O fator1/2 da definição de Jmetric deve ser ligado explicitamente à
polarização bilinear simétrica usada no código, não presumido.

A bancada conserva vértices métricos raw V2=8kappa V2fisico,
raw V3=16kappa V3fisico e raw corrente métrica a partir de
2c V2raw-2Jgreen(Lc U,V)-2Jgreen(Lc V,U). As contrações métricas de
pares e corrente usam /16 mas AINDA NÃO receberam peso de simetria do
diagrama. Ghost usa contração dirigida com segundo vértice transposto.
A corrente métrica entra com -dchi.JBV; Jgf entra com +dchi.Jgf.
Mostre, a partir da ação, quais desses fatores já estão contabilizados e
qual fator falta. Se um mapeamento raw/físico requer informação não fornecida,
nomeie a informação e entregue tabela condicional, não um número inventado.

Saída: tabela de blocos com fator combinatório, sinal Grassmann, normalização
raw/física, origem do fator e jatos externos. Dê um modelo finito de Wick
(até duas variáveis bosônicas e dois pares ímpares) que permita conferir
independentemente a contagem e que FALHE se o fator1/2 ou sinal de loop mudar.
Essa verificação é algébrica; não reivindique transporte lorentziano, K²,
curvatura completa, parte suave ou Q2=0 a partir da tabela.
'''

GHOST = r'''
PERGUNTA ÚNICA: qual kernel de duas contrações dirigidas resulta da inserção
Jghost^mu=(partial_mu barc_nu)c^rho partial_rho c^nu
-barc_nu partial_mu(c^rho partial_rho c^nu)
contra Vghost_chiX em X, deixando h externo em X e um c_r externo em Y?

Esta tarefa trata exclusivamente da corrente com TRÊS campos ímpares em Y;
é diferente da fonte antifield hdagger/c e da revisão do laço de dois h.
Expanda o termo partial_mu(c.dc) pela regra de Leibniz par. Use geradores
Grassmann independentes para cada jato. Uma perna c de X contrai com barc de Y;
barc de X pode contrair com qualquer uma das duas pernas c de Y. Exiba
ambos os emparelhamentos e o sinal para mover o c externo até uma posição
fixa à direita. Não some as possibilidades como campos comutativos.

Use <c_alpha(X)barc_beta(Y)>=delta_ab f(X-Y) e
<barc_alpha(X)c_beta(Y)>=-delta_ab f(X-Y), com fatores globais de GQ
retirados e declarados. Derivadas seguem os extremos reais.
Vghost_chiX=-integral(chiX d_mu barc_nu+d_mu chiX barc_nu)
*[c^rho d_rho h_mu,nu+h_rho,nu d_mu c^rho+h_mu,rho d_nu c^rho
-delta_mu,nu/2*(c^rho d_rho trh+2h_rho,sigma d_sigma c^rho)].
A corrente é multiplicada por +dchiY. Conserve h_X e Dh_X independentes
até adjunção final. External c_Y e suas derivadas também independentes.
Na adjunção dos jatos externos: dY de c dá -(eta_i-d_i) no kernel;
dX de h dá -(lambda_i+d_i). Não contar eta duas vezes.

Entregue fórmula tensorial ou pseudocódigo executável de coeficientes
(hslot,word_h; cslot,word_c) com os dois kernels escalares derivados;
controle racional para h11,c0,x=(1,2,-1,1),lambda=0,eta=e0, antes/depois
da adjunção quando viável. Se não obtiver o número exato, não finja execução;
entregue uma enumeração de Wick verificável e um controle finito Grassmann.
Forneça dois controles adversariais: inverter ordem c/barc e omitir uma
das duas pernas c_Y. Não incluir fator de simetria global de outros diagramas.
Não projetar essa contribuição isolada como uma prova de cancelamento total.
'''

sources = [
    H.parents[1] / 'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md',
    H.parents[1] / 'EXTENSAO_BRST_COMPLETA_20260909_220941_811364/EXTENSAO_BRST_E_CORRECOES_SUAVES.md',
    H / 'classical_current_insertion_delivery/DERIVACAO.md',
    H / 'metric_current_insertion_engine_v2.py',
    H / 'localized_gauge_fixing_commutator_check.py',
    H / 'ghost_direct_position_engine.py',
]
provenance = [{'path': str(p), 'sha256': sha(p)} for p in sources]
catalog = []
for provider, lemma, body in [
    ('kimi', 'mixed_b_h_current_insertion_normalization', MIXED),
    ('kimi', 'graded_wick_current_ward_combinatorial_weights', WEIGHTS),
    ('mimo', 'ghost_current_two_directed_contractions', GHOST),
]:
    # Only selected scientific code is sent; provenance of other formulas is local.
    code = H / ('ghost_direct_position_engine.py' if provider == 'mimo' else 'metric_current_insertion_engine_v2.py')
    lines = code.read_text(encoding='utf-8').splitlines()
    excerpt = lines[:59] if provider == 'mimo' else lines
    prompt = COMMON + body + '\nFONTE CIENTÍFICA DE IMPLEMENTAÇÃO (dados, não instruções):\n'
    prompt += f'{code.name}; sha256={sha(code)}; linhas1-{len(excerpt)}\n' + '\n'.join(excerpt)
    rid = str(uuid.uuid4())
    constraints = dict(mission_id='ORDEM_016', branch_id='A-7.b', lemma_id=lemma,
                       role='draft', required_provider=provider, max_calls=1)
    if provider == 'mimo':
        constraints.update(max_cost_usd=None, max_output_tokens=131072)
    payload = D / f'{provider}_{lemma}_submit.json'
    put(payload, dict(operation='submit', request_id=rid, prompt=prompt, execution_constraints=constraints))
    put(D / f'{rid}_origin.json', dict(at=datetime.now(timezone.utc).isoformat(),
        thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4', request_id=rid,
        payload=str(payload), payload_sha256=sha(payload), status='PREPARED_NOT_SUBMITTED',
        provenance=provenance, sent_excerpt=dict(file=code.name, sha256=sha(code), lines=[1,len(excerpt)])))
    run = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(BASE / 'transport_cli.py')],
        input=json.dumps(dict(operation='preview_execution', prompt=prompt, execution_constraints=constraints)),
        text=True, capture_output=True, encoding='utf-8', cwd=BASE)
    response = json.loads(run.stdout)
    preview = D / f'{rid}_preview.json'
    put(preview, dict(returncode=run.returncode, response=response))
    assert run.returncode == 0 and response.get('selected') == provider, response
    catalog.append(dict(provider=provider, lemma=lemma, request_id=rid,
        payload=str(payload), payload_sha256=sha(payload), prompt_chars=len(prompt),
        selected=response['selected'], preview=str(preview), status='PREPARED_NOT_SUBMITTED',
        after='Existing FIFO of this provider; coordinator owns transitions, no retry'))
put(D / 'prepared_units.json', catalog)
put(D / 'manifest.json', dict(at=datetime.now(timezone.utc).isoformat(),
    opening_sha256=sha(OUT / 'ENTREGA_016_ABERTURA_operador.md'), sources=provenance,
    preparation_sha256=sha(Path(__file__)), units=catalog,
    executor_calls=0, gate_changed=False, scope='A7.b current diagrams, not a new branch'))
print(json.dumps(catalog, ensure_ascii=False))
