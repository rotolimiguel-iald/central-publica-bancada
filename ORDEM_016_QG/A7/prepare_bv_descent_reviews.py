"""Prepare independent BV descent units and preview routes, without execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, sys, uuid

H = Path(__file__).resolve().parent
D = H / 'orchestration_bv_descent'
BASE = H.parents[1] / 'IALD_ORQUESTRACAO_20260923'
OUT = H.parents[1] / 'TUNEL' / 'DO_CHATGPT'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def put(p, obj):
    assert not p.exists(), p
    data = json.dumps(obj, ensure_ascii=False, indent=2).encode('utf-8')
    tmp = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    tmp.write_bytes(data)
    assert tmp.read_bytes() == data
    tmp.replace(p)

COMMON = r'''ORDEM_016 A-7.b, no modelo truncado e na prescricao local de produtos temporais.
Unidade cientifica nova, uma pergunta; resultado DECLARADO ate auditoria local.
Memoria canonica comum obrigatoria. Nao alterar arquivos nem alegar executar CAS.
Auxiliar plano euclidiano R4; nenhuma identificacao automatica com a teoria lorentziana.
h simetrico par, b par, c e barc impares; antifields sao fontes sem propagadores.
G c = d_mu c_nu + d_nu c_mu; C h = d_mu h_mu,nu - d_nu tr(h)/2.
Z=L_c h, w=c.d c. s0h=Gc, s0c=0, s0barc=-b, s0b=0; s1h=Z,s1c=w.
s0Z=-G w. chi e um cutoff liso escalar inerte; exponenciais sao apenas marcadores de jatos.
S0=1/2<h,Hh>+<b,Ch>-<b,b>/(2ell)+<barc,Qc>.
Vgh_chi=integral chi barc C Z, antes de integracao por partes;
apos IBP = -integral (chi d_mu barc_nu+(d_mu chi)barc_nu) Zbar_mu,nu.
O Euler livre do h inclui o setor b: E_h=delta S0/delta h, nao apenas Hh.
Na convencao de fontes hdagger,cdagger adotada aqui:
Vaf_chi=integral chi(hdagger Z+cdagger w), s0hdagger=E_h,
s0cdagger|hdagger=-G* hdagger. Se usar antifields canonicos diferentes,
explicite a transformacao de sinal; nao a interprete como mudar um loop fisico.
Os kernels de contato atuais sao no setor externo h,c, com fontes postas a zero
APOS derivacoes. Nao foi demonstrado que este setor sozinho satisfaz consistencia
homogenea para chi variavel; nao anuncie obstrucao cohomologica por um residuo isolado.
Nao procurar uma resposta numerica desejada, nao refazer a corrente de campo em X/Y
nem o tadpole ordinario com referencia variavel (unidades diferentes ja em andamento).
Entregar hipoteses, signos, identidades verificaveis e lacunas especificas.
'''

UNITS = [
    ('kimi', 'localized_bv_inhomogeneous_ward_descent', 'draft', r'''
PERGUNTA UNICA: qual e a identidade de consistencia de ordem hbar para a quebra
Ward localizada, incluindo a insercao da quebra BV classica nao nula, antes de
projetar no setor h,c? Derive por antibracket graduado ou identidade de produtos
temporais, discriminando o que decorre de Jacobi daquilo que exige normalizacao
de insercoes compostas. Fixe I_chi=(S_chi,S_chi)/2 e Gamma=S_chi+hbar W+...;
nao imponha I_chi=0 quando chi varia. Escreva a identidade na ordem pertinente
em dois vertices e sua polarizacao chiX,chiY, com as ordens em acoplamento e
hbar explicitas. Verifique o papel de [G,chi]w e do termo de fonte necessario.
O resultado deve especificar exatamente que dado adicional, alem da matriz
local h,c, e preciso calcular para testar Wess-Zumino; nao basta citar QME.
Nao identificar W com uma acao efetiva calculada que nao foi fornecida.
'''),
    ('kimi', 'free_euler_contact_bv_graph_descent', 'draft', r'''
PERGUNTA UNICA: quais grafos e contatos locais efetivamente contribuem ao
descendente com insercao E_h [G,chi]w, ao nivel de dois vertices da identidade
Ward, quando E_h e o Euler LIVRE COMPLETO do sistema (h,b)? Use P G_F=I delta
para derivar o colapso de linha, mantendo separada a normalizacao de um produto
remanescente na diagonal. Comece pela contagem de campos de Vaf=hdagger h c,
cdagger c c e Vgh=barc h c: antifields nao contraem; explicite quais bubbles
de duas linhas sao impossiveis e quais aparecem somente apos variacao BV.
Liste campos externos, linhas internas, fator hbar, sinais impares e pesos
de vertices. Derive formula em termos de kernels livres e vertices dados,
sem inventar um propagador de antifield nem assumir que f(0)=0.
Diferencie normal ordering que elimina auto-contracoes de produto temporal
com EOM, e indique quais identidades de normalizacao sao compativeis ou ainda
precisam ser verificadas. Entregue uma receita finita implementavel e controles
de chi constante, sem prometer cancelar um residuo numerico nao fornecido.
'''),
    ('mimo', 'localized_hc_weighted_adjoint_criterion', 'skeptic', r'''
PERGUNTA UNICA: qual criterio de adjuncao formal testa corretamente a variacao
BRST do setor local h,c quando a quebra classica localizada e nao nula?
Considere A=integral exp(L.x) sum_{A,r} h_A a_Ar(D)c_r, A=(i<=j),
h_A e coordenada de matriz simetrica com ambas entradas quando i!=j.
s0h_ij=di c_j+dj c_i, s0c=0. Derive B_jr=-sum_i(D_i+L_i)a_(ij),r
com a multiplicidade diagonal explicitada, e o criterio graduado de anulacao
de integral c B c por B-B^dagger, B^dagger=B^T(-D-L).
Parta tambem de A(q) partial_X(delta(X-Y)) chiX chiY: derive, sem supor,
a substituicao entre q e D do operador local. Distingua sinal de IBP, peso
de base e derivadas do cutoff. Depois situe esse teste na identidade BV
inhomogenea de uma acao com I_chi=(S_chi,S_chi)/2 nao nula: o que uma falha
da matriz h,c pode e nao pode concluir? De dois contraexemplos polinomiais
pequenos: omissao de L e confusao entre simetria ordinaria e adjunta.
Nao escolha resultado por concordancia com calculos alheios.
'''),
]

def main():
    D.mkdir(exist_ok=False)
    source = H / 'localized_gauge_fixing_commutator_check.py'
    source_lines = source.read_text(encoding='utf-8').splitlines()
    # The existing input conventions are shared; new local result numbers are withheld.
    excerpt = '\n'.join(source_lines[:55])
    provenance = dict(path=str(source), sha256=sha(source), first_line=1,
                      last_line=min(55, len(source_lines)))
    rows=[]
    for provider, lemma, role, question in UNITS:
        prompt = COMMON+question+'\nFONTE LOCAL DE CONVENCOES (dados):\n'
        prompt += json.dumps(provenance,ensure_ascii=False)+'\n'+excerpt
        rid=str(uuid.uuid4())
        constraints=dict(mission_id='ORDEM_016',branch_id='A-7.b',lemma_id=lemma,
                         role=role,required_provider=provider,max_calls=1)
        if provider=='mimo':
            constraints.update(max_cost_usd=None,max_output_tokens=131072)
        payload=D/f'{provider}_{lemma}_submit.json'
        put(payload,dict(operation='submit',request_id=rid,prompt=prompt,
                         execution_constraints=constraints))
        put(D/f'{rid}_origin.json',dict(at=datetime.now(timezone.utc).isoformat(),
            thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',request_id=rid,
            payload=str(payload),payload_sha256=sha(payload),sources=[provenance],
            status='PREPARED_NOT_SUBMITTED'))
        result=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'transport_cli.py')],
            input=json.dumps(dict(operation='preview_execution',prompt=prompt,
                                  execution_constraints=constraints)),
            text=True,capture_output=True,encoding='utf-8',cwd=BASE)
        response=json.loads(result.stdout)
        preview=D/f'{rid}_preview.json'
        put(preview,dict(returncode=result.returncode,response=response))
        assert result.returncode==0 and response.get('selected')==provider,response
        rows.append(dict(provider=provider,lemma=lemma,request_id=rid,
            payload=str(payload),payload_sha256=sha(payload),prompt_chars=len(prompt),
            selected=response['selected'],preview=str(preview),
            status='PREPARED_NOT_SUBMITTED',after='Existing provider FIFO'))
    put(D/'prepared_units.json',rows)
    put(D/'manifest.json',dict(at=datetime.now(timezone.utc).isoformat(),
        opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'),sources=[provenance],
        preparation_sha256=sha(Path(__file__)),units=rows,executor_calls=0,gate_changed=False))
    print(json.dumps(rows,ensure_ascii=False))

if __name__=='__main__':
    main()
