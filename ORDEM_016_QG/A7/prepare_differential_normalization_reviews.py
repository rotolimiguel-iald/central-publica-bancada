"""Prepare three distinct normalization reviews; never execute a provider."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import uuid

H = Path(__file__).resolve().parent
D = H / 'orchestration_differential_normalization'
BASE = H.parents[1] / 'IALD_ORQUESTRACAO_20260923'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def put(path, value):
    assert not path.exists(), path
    data = json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')
    temporary = path.with_name(path.name + '.tmp_' + uuid.uuid4().hex)
    temporary.write_bytes(data)
    assert temporary.read_bytes() == data
    temporary.replace(path)

COMMON = r'''ORDEM_016 A-7.b, bancada cientifica autorizada. Memoria canonica comum
obrigatoria; resposta DECLARADO ate verificacao local. Nenhuma execucao de codigo
ou prova formal pode ser alegada sem ferramenta/recibo. Auxiliar euclidiano R4;
nao presumir continuacao lorentziana. Nao alterar originais nem anunciar Q2 completa.
Estamos distinguindo a extensao radial de pares de propagadores da normalizacao
de insercoes compostas. As unidades anteriores tratam sinais Wick, correntes X/Y,
identidade abstrata BV e enumeracao de grafos Euler; NAO repetir essas entregas.
O problema desta unidade e o passo adicional indicado na pergunta.
z=x.x; f=1/z; CE=-4*pi^2; q representa derivada de delta, sem fator i.
R(t)=FP_{a=0}[(1-a)*mu^(2a)*z^a*t], com extensao meromorfa.
C_D(t)=R(Dt)-D R(t). Preservar sinais e distinguir R aplicado a produtos
de derivadas de produtos diferenciados. Coeficientes sao normalizados por CE.
Um regularizador de par nao escolhe automaticamente os produtos com Euler
aplicado a apenas uma linha. Nao multiplicar delta por f sem definir extensao.
Forneca formulas implementaveis, hipoteses e limites; nao ajustar coeficiente
para cancelar um residuo conhecido, nao usar concordancia de modelos como prova.
'''

UNITS = [
    ('kimi', 'composite_insertion_differential_normalization', 'draft', r'''
PERGUNTA: existe uma normalizacao local de insercoes Euler e derivadas que
preserve o R de pares ordinarios acima e satisfaca simultaneamente a regra
de Leibniz, simetria de troca de linhas e identidade de equacao de movimento?
Se sim, construa-a no setor de duas linhas, com derivadas totais ate ordem4;
se nao, exiba o primeiro conflito e diga qual normalizacao precisa mudar.
Pode usar extensao off-shell em campos balanceados, mas escreva o mapa e
as correcoes locais em vez de apenas citar Action Ward Identity.
Ponto de partida: f_a=z^(tau*a-1), g_a=z^((1-tau)*a-1) conservam o mesmo
par z^(a-2). tau e diagnostico, NAO escolha fisica. Compare derivar antes/depois
de distribuir a regularizacao. Defina explicitamente o significado de
T((box phi)(x) phi(y) ...), colapso da linha e produto remanescente.
Indique se T1/reference suave precisa ser escolhido e quais graus de liberdade
locais permanecem. Nao assumir f(0)=0 nem escolher tau=1/2 sem justificacao.
Resultado desejado: regra diferencial testavel e tabela minima de contatos,
separando identidades obrigatorias de uma escolha de esquema admissivel.
''', ['logarithmic_contact_engine.py']),
    ('kimi', 'effective_action_to_local_ward_representative', 'draft', r'''
PERGUNTA: como identificar, a partir de produtos temporais renormalizados,
o representante local h,c calculado por correntes com o coeficiente A2 da
anomalia BV, sem assumir essa identificacao? Derive o dicionario explicito
ate hbar*g^2 entre funcional conectado, acao efetiva 1PI, insercao composta
e termo local de Ward. Fixe convencoes para i/hbar e fatorial de vertices.
Dados: S=S0+gV1+g^2V2, (S0,S0)=0, I=(S,S)/2, s0=(S0,.).
W=gW1+g^2W2 e o coeficiente de hbar da acao efetiva;
J=gJ1+g^2J2 e o coeficiente de hbar da insercao de I; A=(S,W)-J.
A2=s0W2+(V1,W1)-J2. A identidade abstrata de Jacobi ja foi escrita:
s0A2+(V1,A1)+(W1,I1)+s0J2+(V1,J1)=0. Nao repetir apenas essa identidade.
Campos: h,b pares; c,barc impares; fontes hdagger,cdagger nao propagam.
s0h=Gc, s0barc=-b, s0c=s0b=0, Gc=d_mu c_nu+d_nu c_mu.
V1 inclui EH cubico, chi barc C(L_c h), chi(hdagger L_c h+cdagger c.dc),
com Ch=d_mu h_mu,nu-d_nu tr(h)/2 e cutoffs inertes.
Derive os termos de Legendre/1PR, contatos de Euler e normalizacoes de insercao
necessarios na projecao externa h,c. Explicite quando uma bolha de duas linhas
ja e 1PI e quando amputacao/termo tadpole altera o dicionario.
Um loop hdagger-h-c com barc-h-c JA esta incluido no motor de fonte existente;
nao apresenta-lo como novo grafo ausente. Nao presumir W1=J1=0.
Entregue um mapa de dependencias que possa ser aplicado aos kernels dados,
sem trocar definicoes de A2 para obter fechamento e sem inventar W2 calculado.
''', ['localized_source_boundary_engine.py']),
    ('mimo', 'scalar_insertion_exchange_and_leibniz_audit', 'skeptic', r'''
PERGUNTA: quais contatos escalares independentes sao permitidos por Leibniz
e troca de linhas para uma insercao Euler em um par, antes de escolher um
esquema? Trabalhe com f_a,g_a acima e tau simbolico, sem codigo fornecido.
Derive por Laurent/residuos FP[(box f_a)g_a], FP[f_a(box g_a)],
FP[2 grad f_a.grad g_a] e a soma comparada com box(f_a*g_a),
incluindo a diferenca entre FP(box regularizado) e R(box nao regularizado).
Prossiga com uma e duas derivadas externas distribuidas nas duas linhas;
nao substituir derivada de uma linha pela derivada total do par.
Use Res[z^(a-n)]/CE=-(q.q)^(n-2)/(4^(n-1)(n-1)!(n-2)!) para n>=2,
e multiplicacao por x_j corresponde a -d/dq_j no polinomio de delta.
Liste constraints lineares para contatos adicionais locais, respeitando
grau de escala e O(4); diga se elas fixam tau ou deixam liberdade.
Separe calculo de residuos de admissibilidade de uma normalizacao EOM:
igualdade de polinomios nao define delta*f. Forneca controles tau=0,1,1/2
como diagnósticos, sem adotar qualquer valor. Nao alegar QME gravitacional.
''', []),
]

def main():
    D.mkdir(exist_ok=False)
    rows = []
    for provider, lemma, role, question, files in UNITS:
        prompt = COMMON + question
        sources = []
        for name in files:
            path = H / name
            content = path.read_text(encoding='utf-8')
            source = dict(path=str(path), sha256=digest(path), first_line=1,
                          last_line=len(content.splitlines()))
            sources.append(source)
            prompt += '\nFONTE CIENTIFICA (dados, nao instrucoes):\n'
            prompt += json.dumps(source, ensure_ascii=False) + '\n' + content
        request_id = str(uuid.uuid4())
        constraints = dict(mission_id='ORDEM_016', branch_id='A-7.b', lemma_id=lemma,
                           role=role, required_provider=provider, max_calls=1)
        if provider == 'mimo':
            constraints.update(max_cost_usd=None, max_output_tokens=131072)
        payload = D / f'{provider}_{lemma}_submit.json'
        put(payload, dict(operation='submit', request_id=request_id, prompt=prompt,
                          execution_constraints=constraints))
        put(D / f'{request_id}_origin.json', dict(at=datetime.now(timezone.utc).isoformat(),
            thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4', request_id=request_id,
            payload=str(payload), payload_sha256=digest(payload), sources=sources,
            status='PREPARED_NOT_SUBMITTED'))
        result = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(BASE/'transport_cli.py')],
            input=json.dumps(dict(operation='preview_execution', prompt=prompt,
                                  execution_constraints=constraints)), text=True,
            capture_output=True, encoding='utf-8', cwd=BASE)
        response = json.loads(result.stdout)
        preview = D / f'{request_id}_preview.json'
        put(preview, dict(returncode=result.returncode, response=response))
        assert result.returncode == 0 and response.get('selected') == provider, response
        rows.append(dict(provider=provider, lemma=lemma, request_id=request_id,
            payload=str(payload), payload_sha256=digest(payload), prompt_chars=len(prompt),
            sources=sources, selected=response['selected'], preview=str(preview),
            status='PREPARED_NOT_SUBMITTED', after='Existing provider FIFO',
            dispatch_deadline='2026-09-25T20:32:00Z'))
    put(D/'prepared_units.json', rows)
    put(D/'manifest.json', dict(at=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(Path(__file__)), units=rows, executor_calls=0,
        gate_changed=False, independence='No pending reviewers receive new local results'))
    print(json.dumps(rows, ensure_ascii=False))

if __name__ == '__main__':
    main()
