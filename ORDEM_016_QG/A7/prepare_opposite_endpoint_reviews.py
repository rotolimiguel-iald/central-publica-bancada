"""Prepare complementary A7.b reviews; preview only, never dispatch."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, sys, uuid

H = Path(__file__).resolve().parent
D = H / 'orchestration_opposite_endpoint'
BASE = H.parents[1] / 'IALD_ORQUESTRACAO_20260923'
OUT = H.parents[1] / 'TUNEL' / 'DO_CHATGPT'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def put(p, value):
    assert not p.exists(), p
    raw = json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')
    tmp = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    tmp.write_bytes(raw)
    assert tmp.read_bytes() == raw
    tmp.replace(p)

COMMON = r'''ORDEM_016, A-7.b. Unidade científica delimitada; memória comum obrigatória.
Resultado DECLARADO até auditoria local. Não alterar arquivos, não inventar execução.
Esta unidade não repete as correntes situadas em Y: a corrente agora está em X,
com h externo em X, ghost INTERNO em X, e vértice ghost ordinário em Y com c externo.
Trabalhamos no auxiliar euclidiano plano R4: x=X-Y, f=1/(x.x), d=partial_x.
Derivadas reais: partial_X f=d f; partial_Y f=-d f.
C(h)_nu=partial_mu h_mu,nu-partial_nu tr(h)/2, Gc=partial_mu c_nu+partial_nu c_mu.
Z_mu,nu=L_c h_mu,nu=c^rho partial_rho h_mu,nu+h_rho,nu partial_mu c^rho
+h_mu,rho partial_nu c^rho; Zbar=Z-delta tr(Z)/2; w=c.dc.
s0h=Gc,s0c=0,s0barc=-b,s0b=0,s1h=Z,s1c=w.
Vgh_chi=integral chi barc C Z = -integral(chi d_mu barc_nu+d_mu chi barc_nu)Zbar_mu,nu.
Jb^mu=b_nu Zbar_mu,nu. Jghost has barc,c,c and no external h slot.
Conventions for free contractions, scalar normalization suppressed consistently:
<h_ab(X)h_cd(Y)>=-4 kappa S_ab,cd f, S=(delta_ac delta_bd+delta_ad delta_bc-delta_ab delta_cd)/2;
<h_ab(X)b_nu(Y)>=(delta_bn d_a+delta_an d_b)f;
<b_nu(X)h_ab(Y)>=-(delta_bn d_a+delta_an d_b)f;
<c_r(X)barc_nu(Y)>=delta_rnu f, reversed odd order has minus sign.
The stored EH Fourier polynomial has two derivative factors. Real density
S_EH=-integral chi sqrt(g)R/(2kappa) gives V3real=-V3stored/(16kappa).
The two-derivative current supplied below gives Cmetric_X=+(partial_mu chiX)Jraw^mu/(16kappa).
Treat this sign convention as explicit input; do not silently substitute the older raw=+16kappa real relation.
Jraw is the Hessian in its two h slots; Cmetric=1/2 J_AB,r h_A h_B c_r in component notation.
For Cb use +(partial_mu chiX)b_nu Zbar_mu,nu without a raw rescaling.
chiX=e^(lambda.X),chiY=e^(eta.Y) denote full local jets, not compact cutoffs globally.
Formal expansion exp(-V/hbar): first mean-current contribution is -<C V>_connected.
No desired residual or total-cancellation number is supplied. Do not fit weights.
Do not infer Q2, an anomaly, Lorentzian completion or full QME from one diagram.
'''

KIMI = r'''
PERGUNTA ÚNICA: qual é o coeficiente bilocal h_A(X)c_r(Y) da inserção
[Cmetric_X+Cb_X] Vgh_Y com DUAS contrações, incluindo as derivadas de ambos
os cutoffs, sinais graduados e pesos de Hessiana, antes e após adjunção externa?
Derive diretamente da ação e das contrações fornecidas, mantendo separado
<C V> do sinal posterior da identidade Ward. Jmetric tem h externo e h interno;
Cb tem h externo e b interno. Ghost da corrente é interno e contrai barc_Y.
O c de Y é externo. As duas escolhas do h externo da corrente métrica devem
ser contabilizadas, sem duplicar o fator 1/2 da Hessiana nem peso de base simétrica.
Base h_A possui dez componentes a<=b; E_ab tem duas entradas1 se a!=b.
Forneça algoritmo finito racional usando Jraw e matriz de jatos ghost W como entradas.
No W, linhas são c_Y e jatos, colunas barc_Y e jatos; h_Y e dh_Y são slots separados.
Retenha palavras externas de h_X até ordem2; não reduza prematuramente a ordem1.
Explique por que trocar X,Y em uma fórmula cuja perna externa está fixa não
substitui essa nova atribuição das pernas. Dê um controle finito com dados
arbitrários declarados, mais controles de lambda=0 e inversão de ordem ímpar.
Se o sinal/normalização não puder ser deduzido, exponha a hipótese faltante.
Entregue expressão/pseudocódigo verificável, nunca alegação de CAS executado.
'''

MIMO = r'''
PERGUNTA ÚNICA: qual operador adjunto reduz sem perda os jatos externos de
h_X (até ordem2) e c_Y (até ordem1) em cada kernel conectado da corrente em X,
incluindo sinais das duas contrações e distribuição de derivadas internas?
Esta auditoria é combinatória e de adjunção, não rederivação de EH nem revisão
das duas pernas c da corrente de três ghosts em Y (outra unidade já na fila).
Parta de integral chiX chiY (partial_X^I h_A)(partial_Y^J c_r)
F_IJ(X-Y), com campos teste compactos e palavras I,J ordenadas. Derive
as potências/composições de -(d+lambda) e +(d-eta), inclusive I=(i,i)
e I=(i,j), e exiba fatores de Leibniz nos produtos de dois propagadores.
Os coeficientes da corrente contêm lambda; não descartar derivadas do cutoff
ao adjuntar, nem confundir gradiente-only com jatos exponenciais completos.
Use a ordem C_X Vgh_Y para computar o sinal do produto c_X barc_Y c_Y,
com ghost externo à direita. No termo b_X h_Y preserve o sinal do propagador.
Dê testes polinomiais exatos por integração por partes (ou identidade formal
de operadores), incluindo multiplicidade2 para duas derivadas iguais e
comparação iterativa versus fórmula multinomial até ordem total3.
São esperados testes que detectem omissão de h'' e sinal errado no extremoY.
Não escolha fator a partir de um resíduo nem anuncie cancelamento total.
'''

def main():
    D.mkdir(exist_ok=False)
    units = []
    sources = [H/'classical_current_jet_engine.py', H/'ghost_direct_position_engine.py',
               H/'mixed_b_h_current_engine_v3.py', H/'real_density_fourier_vertex/results.json']
    provenance = [{'path': str(p), 'sha256': sha(p)} for p in sources]
    for provider, lemma, body in [('kimi','opposite_endpoint_metric_and_b_current',KIMI),
                                  ('mimo','opposite_endpoint_external_jet_adjoint_audit',MIMO)]:
        code = sources[0] if provider=='kimi' else sources[1]
        lines = code.read_text(encoding='utf-8').splitlines()
        excerpt = lines if provider=='kimi' else lines[:59]
        prompt = COMMON + body + '\nFONTE (dados):\n' + code.name + '\nsha256=' + sha(code)
        prompt += '\nlinhas1-' + str(len(excerpt)) + '\n' + '\n'.join(excerpt)
        rid = str(uuid.uuid4())
        constraints = dict(mission_id='ORDEM_016',branch_id='A-7.b',lemma_id=lemma,
                           role='draft' if provider=='kimi' else 'skeptic',required_provider=provider,max_calls=1)
        if provider=='mimo': constraints.update(max_cost_usd=None,max_output_tokens=131072)
        payload = D/f'{provider}_{lemma}_submit.json'
        put(payload,dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=constraints))
        put(D/f'{rid}_origin.json',dict(at=datetime.now(timezone.utc).isoformat(),
            thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',request_id=rid,
            payload=str(payload),payload_sha256=sha(payload),provenance=provenance,
            status='PREPARED_NOT_SUBMITTED'))
        p = subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'transport_cli.py')],
            input=json.dumps(dict(operation='preview_execution',prompt=prompt,execution_constraints=constraints)),
            text=True,capture_output=True,encoding='utf-8',cwd=BASE)
        response=json.loads(p.stdout)
        preview=D/f'{rid}_preview.json'
        put(preview,dict(returncode=p.returncode,response=response))
        assert p.returncode==0 and response.get('selected')==provider,response
        units.append(dict(provider=provider,lemma=lemma,request_id=rid,payload=str(payload),
            payload_sha256=sha(payload),prompt_chars=len(prompt),selected=response['selected'],
            preview=str(preview),status='PREPARED_NOT_SUBMITTED',after='Existing provider FIFO'))
    put(D/'prepared_units.json',units)
    put(D/'manifest.json',dict(at=datetime.now(timezone.utc).isoformat(),
        opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'),sources=provenance,
        preparation_sha256=sha(Path(__file__)),units=units,executor_calls=0,gate_changed=False))
    print(json.dumps(units,ensure_ascii=False))

if __name__=='__main__': main()
