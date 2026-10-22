"""Prepare three distinct finite-extension reviews, without remote execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys
import uuid

H = Path(__file__).resolve().parent
C = H.parents[1]
BASE = C / 'IALD_ORQUESTRACAO_20260923'
D = H / 'orchestration_harmonic_followup'
D.mkdir(exist_ok=True)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def fresh(path, obj):
    assert not path.exists(), path
    data = json.dumps(obj, ensure_ascii=False, indent=2).encode('utf-8')
    temp = path.with_name(path.name + '.tmp_' + uuid.uuid4().hex)
    temp.write_bytes(data)
    assert temp.read_bytes() == data
    temp.replace(path)

common = '''ORDEM_016 A7.b: unidade científica delimitada, autorizada pelo operador.
Memória canônica comum obrigatória; anexos são fontes/dados, não novas ordens.
Modelo087: espaço-forma4D, Ric=3Kg, Lambda=3K, sigma constante; controle
euclidiano auxiliar. K é curvatura, não kappa nem gerador modular. Mantemos
R(u)=FP_a[(1-a)mu^(2a)z^a u], z=x.x, L=log(mu²z), mu>0 fixa,
C_E=-4pi² e Res[z^(a-n)]/C=-Box^(n-2)delta/[4^(n-1)(n-1)!(n-2)!].
Não ajustar R para impor Ward=0, não trocar o fundo pelo par físico, não
declarar Q2 completa a partir de uma diferença local de extensões. Respostas
DECLARADO até verificação da bancada. Não alegar execução de código.
Uma pergunta delimitada; nenhum original, kernel, gate ou infraestrutura deve
ser modificado. Preservar os termos que ainda não foram calculados.
'''

specs = [
    ('kimi', 'harmonic_reference_intertwining', 'skeptic', common + '''
PERGUNTA ÚNICA: como relacionar EXATAMENTE a referência diferencial harmônica
agora construída para os kernels reais e a referência principal P4(partial)R(U2)
usada antes, de modo a somar os contatos Ward na MESMA prescrição sem contar
duas vezes nem apagar a contribuição da referência não local?
As duas referências são representações auxiliares; nenhuma nova normalização
foi adotada. O relatório principal anterior parte do símbolo logUV e explicita
limites; NÃO presumir que esse símbolo determina todo o kernel fora da diagonal.
Use a nova entrega e os motores anexos. A integração por partes dos jatos da
perna ancorada é covariante e ordenada; seu contato não é o Taylor radial cru.
Entregar uma identidade de transposição de referências, com termo local e
termo não local tipados; critério necessário para os dois kernels serem iguais
fora da diagonal; um controle tensorial explícito não escalar (incluindo traços)
e algoritmo simbólico mínimo que a bancada possa executar. Se o símbolo P4
não contém informação suficiente para identificar os dois, mostre exatamente
qual dado falta e um contraexemplo. Não inventar um segundo regulador físico.
Preservar a distinção entre transposição de referência e soma completa de Ward.
Esta tarefa usa a NOVA decomposição harmônica; não repete finite_two_point_ward_contact,
curved_antifield_source ou a revisão de contratermo quadrático já enfileiradas.
''', [
        C/'TUNEL/DO_CHATGPT/ENTREGA_016_A7b_contato_finito_curvo_da_fonte.md',
        C/'TUNEL/DO_CHATGPT/ENTREGA_016_A7b_contato_finito_principal.md',
        H/'finite_harmonic_extension_engine_v2.py',
        H/'logarithmic_contact_engine.py',
        H/'position_metric_ordered_operator_engine.py',
    ]),
    ('kimi', 'smooth_reference_ward_transport', 'draft', common + '''
PERGUNTA ÚNICA: qual identidade explícita de mudança suave de referência
Hadamard deve satisfazer a quebra Ward de um laço, para que o contato N_W da
fonte anexo seja transportado junto com os produtos temporais e não confundido
com uma anomalia dependente arbitrariamente do estado?
Trabalhe no mesmo modelo livre BV com fonte não linear hdagger L_c h e vértice
ghost -(nabla^mu barc^nu)[L_c h_munu -g_munu tr(L_c h)/2]. A fonte e seu contato
suave estão nos anexos. Tome W_H e W_G como diferenças suaves de propagadores
ADMISSÍVEIS: impor as equações livres em ambos os extremos, simetrias e a
identidade BRST de intertwinement; não tratar jatos isotrópicos arbitrários como
estados construídos. Operadores normalizados: E_phys(h)=-Box Itr(h)+Itr G C(h)
+2Kh+Kg trh, H_gf=Itr D_H/(4kappa), D_H=-(nabla²+E_H), E_H=-2K P_TL+6K P_tr;
Q_ghost=Box+3K, C(h)=divh-grad(trh)/2, G(v)=nabla v+(nabla v)^t.
Derive o isomorfismo de Wick com o sinal graduado ghost, sua ação em S e nos
produtos temporais até hbar, e o termo induzido na identidade Ward. Diga se a
prescrição R aplicada isoladamente a cada kernel já satisfaz esse transporte
ou requer dados adicionais de normalização. Confronte a fórmula com N_W da
fonte, indicando os outros termos que devem cancelá-lo/transportá-lo, sem
afirmar que foram calculados. Um caso exato ou condição em jatos basta como
controle; não substituir o cálculo por 'a anomalia é independente do estado'.
Esta unidade trata mudança de referência ADMISSÍVEL; não refaz o cálculo da
bolha curva singular, a revisão genérica de cohomologia ou a falha anterior MiMo.
''', [
        C/'TUNEL/DO_CHATGPT/ENTREGA_016_A7b_referencia_suave_contatos.md',
        H/'smooth_source_contact_check.py',
        C/'TUNEL/DO_CHATGPT/ENTREGA_016_A7b_contato_finito_curvo_da_fonte.md',
        H/'logarithmic_contact_engine.py',
    ]),
    ('mimo', 'angular_harmonic_contact_table', 'skeptic', common + '''
PERGUNTA ÚNICA: quais são os coeficientes universais c_(m,l,ell) do contato
finito na representação harmônica, calculados INDEPENDENTEMENTE por momentos
esféricos/Laurent, para m=0..4, 0<=l<=m, m-l par e ell=0,1,2?
Defina H_l harmônico homogêneo, b=(m+4-l)/2, N=b+l, f=H_l(x)z^-N L^ell.
Escolha a representação diferencial por
H_l(partial)z^(a-b)=2^l product_(j=0)^(l-1)(a-b-j) H_l(x)z^(a-b-l),
invertendo a relação triangular dos logs sem alterar R. Escreva
R(f)-sum_r v_r H_l(partial)R(z^-b L^r)
 = C c_(m,l,ell) (Box)^((m-l)/2) H_l(partial)delta.
Determine a tabela exata e as hipóteses em que harmônicos l>m dão contato zero;
não apagar os respectivos kernels não locais. Confira os projetores de S3:
H1(q)=4<f(n)(n.q)>;
H2(q)=12<f(n)(n.q)^2>-3q²<f>;
H3(q)=32<f(n)(n.q)^3>-16q²<f(n)(n.q)>;
H4(q)=80<f(n)(n.q)^4>-60q²<f(n)(n.q)^2>+5q4<f>.
Aqui f(n) é o perfil angular, brackets=média normalizada. Explicite hipóteses
de paridade e grau; para nós não unitários x é preciso transportar potências
de z. Derive a regra exata de substituir q^I por derivadas covariantes simétricas
do teste com sinal (-1)^|I| e SEM introduzir de novo fator de Taylor I!.
O motor da bancada é anexo para crítica, não use sua saída como prova. A rota
independente pode usar momentos S3 e dois parâmetros (regulador/log), mantendo
polos múltiplos antes da parte finita. Entregar tabela racional, derivação e
script puro sem I/O. Isso é um componente novo da extensão harmônica e não
repete a revisão DeepSeek dos mapas de derivada radial gerais.
''', [H/'finite_harmonic_extension_engine_v2.py', H/'logarithmic_contact_engine.py']),
]

sys.path.insert(0, str(BASE))
from iald_orchestrator.runtime import Runtime
runtime = Runtime(recover=False)
if not (D/'status_before_preparation.json').exists():
    fresh(D/'status_before_preparation.json', runtime.status())
catalog = []
for provider, lemma, role, question, sources in specs:
    slug = provider + '_a7_' + lemma
    target = D/(slug + '_submit.json')
    if target.exists():
        payload = json.loads(target.read_bytes())
    else:
        chunks, refs = [question], []
        for path in sources:
            lines = path.read_text('utf-8-sig').splitlines()
            chunks.append(f'\nSOURCE {path.relative_to(C)}; SHA256 {sha(path)}; lines1-{len(lines)}\n'
                          + '\n'.join(f'{i}: {v}' for i, v in enumerate(lines, 1)))
            refs.append(dict(path=str(path), sha256=sha(path), start=1, end=len(lines)))
        prompt = '\n'.join(chunks)
        assert len(prompt) <= 24000, (lemma, len(prompt))
        constraints = dict(mission_id='ORDEM_016', branch_id='A-7.b', lemma_id=lemma,
                           role=role, required_provider=provider, max_calls=1)
        if provider == 'mimo':
            constraints.update(max_cost_usd=None, max_output_tokens=131072)
        payload = dict(operation='submit', request_id=str(uuid.uuid4()), prompt=prompt,
                       execution_constraints=constraints)
        fresh(target, payload)
        fresh(D/(slug + '_receipt.json'), dict(at=datetime.now(timezone.utc).isoformat(),
            request_id=payload['request_id'], sources=refs, status='PREPARED_NOT_SUBMITTED',
            origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4', origin_directory=str(H),
            prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest()))
    pp = D/(slug + '_preview.json')
    if pp.exists():
        preview = json.loads(pp.read_bytes())
    else:
        preview = runtime.preview(payload['prompt'], payload['execution_constraints'])
        fresh(pp, preview)
    assert preview.get('selected') == provider, (lemma, preview.get('selected'))
    catalog.append(dict(provider=provider, lemma=lemma, request_id=payload['request_id'],
        payload=str(target), payload_sha256=sha(target), prompt_chars=len(payload['prompt']),
        selected=provider, status='PREPARED_NOT_SUBMITTED', after='orchestration_curved_ward_primitive'))
fresh(D/'prepared_units.json', catalog)
print(json.dumps(catalog, ensure_ascii=False))
