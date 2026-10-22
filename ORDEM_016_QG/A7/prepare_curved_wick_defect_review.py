"""Prepare a distinct arity-one Wick/BV task; coordinator owns submission."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, uuid, subprocess, sys

H = Path(__file__).resolve().parent
BASE = H.parents[1] / 'IALD_ORQUESTRACAO_20260923'
D = H / 'orchestration_curved_wick_defect'

PROMPT = r'''ORDEM_016 A-7.b, unidade delimitada NOVA: defeito de Wick/BV de aridade UM.
Memoria cientifica comum obrigatoria, resposta DECLARADO ate auditoria local.
Nao modificar arquivos, nao alegar execucao de CAS ou acesso a caminhos externos.
Esta unidade nao repete o pedido escalar Leibniz/Euler a46, nem pede calcular
novamente grafos de duas insercoes. Nenhum fechamento Q2 deve ser presumido.

Objeto: campos livres phi=(h_ij simetrico,b_i,c_i,barc_i), paridades 14 pares/8
impares, e antifields de paridade oposta. BRST linear q phi=Q phi com
qh_ij=di c_j+dj c_i, qbarc_i=-b_i, qc=qb=0. q phi^dagger contem as equacoes
livres P phi e a acao adjunta nos antifields, com convencoes que VOCE deve
declarar antes de calcular. P e a Hessiana livre graduada. No fundo curvo
os operadores sao covariantes e suas identidades classicas devem ser mantidas.
Wick contrai somente campos, nao antifields, com um bidistribuicao H_AB.
H pode ser parametrix localmente covariante, NAO assumir bisolucao exata.
Defina separadamente os defeitos suaves E_AB=(P H)_AB e
D_AB=(Q_x H + epsilon H Q_y^T)_AB, epsilon_A=(-1)^paridade(phi_A),
declarando a convencao de derivadas transpostas/troca dos pontos.

Pergunta: derive a formula de primeira ordem em hbar de
qhat T1(F)-T1(qF)=T1(A1(F)) em termos de D,E e derivadas funcionais de F,
com fatores 1/2, sinais Grassmann e termos antifield-Euler explicitos.
Voce pode escolher uma convencao coerente T1=exp(hbar C_H), mas precisa
declarar C_H, qhat e a identificacao entre algebras; nao definir qhat por
conjugacao de T1 e depois anunciar A1=0 por construcao. Mostre onde um
defeito PH entra mesmo se QH+epsilon H Q^T=0. Separe mudanca de estado
por bisolucao suave, mudanca de parametrix por suave nao bisolucao e
liberdade de renormalizacao localmente covariante.

Aplique a formula, sem inventar H completo, a
F_af=int chi [h^dagger_ij (L_c h)_ij + c^dagger_i c^j nabla_j c^i],
(L_c h)_ij=c^k nabla_k h_ij+h_kj nabla_i c^k+h_ik nabla_j c^k.
Contracoes <hh>,<hb>,<bh>,<c barc>,<barc c> podem existir; <hc>,<cc>,
<h barc> sao zero. Indique quais termos de A1(F_af) podem sobreviver
apesar de C_H F_af=0, porque C_H(q F_af) nao precisa ser zero.
Se dependem de jatos desconhecidos, entregue-os simbolicamente, com tipos
e ordens de derivadas. Nao usar um traco de calor como substituto de A1.

Controles: pequeno algebra graduada de polinomios com um par antifield-Euler
para conferir manualmente o sinal de [q,C_H]; caso bisolucao equivarante
deve zerar; caso PH nao zero deve permitir testemunha nao nula. Explique
qual dado falta para aplicar a formula ao setor nao minimal completo22x22.
Resultado esperado: formula utilizavel de aridade1 e lista FINITA de jatos
necessarios para esta F_af, nao ensaio geral nem nova camada de motor.
Fontes conhecidas para situar convencoes: Frob arXiv1803.10235v3, identidade
de aridade1 qhat T1(F)=T1(s0F)+T1(A1(F)). Se nao tiver o texto, declare.
Prazo da bancada A7.b 2026-09-25T20:32:00Z; nao presumir aprovacao fisica.
'''

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def put(p, value):
    assert not p.exists(), p
    data = json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')
    temp = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    temp.write_bytes(data)
    assert temp.read_bytes() == data
    temp.replace(p)

def main():
    D.mkdir(exist_ok=False)
    rid = str(uuid.uuid4())
    constraints = dict(mission_id='ORDEM_016', branch_id='A-7.b',
        lemma_id='curved_wick_arity_one_antifield_euler_defect', role='draft',
        required_provider='mimo', max_calls=1, max_cost_usd=None,
        max_output_tokens=131072)
    payload = D / 'mimo_curved_wick_arity_one_submit.json'
    put(payload, dict(operation='submit', request_id=rid, prompt=PROMPT,
                     execution_constraints=constraints))
    origin = dict(at=datetime.now(timezone.utc).isoformat(),
        thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4', request_id=rid,
        payload=str(payload), payload_sha256=sha(payload),
        status='PREPARED_NOT_SUBMITTED', original_house='Central de Patentes',
        mission_bench=str(H), scientific_sources='Prompt mathematical data and canonical common memory')
    put(D / (rid + '_origin.json'), origin)
    result = subprocess.run([sys.executable, '-X', 'utf8', '-B',
        str(BASE / 'transport_cli.py')], input=json.dumps(dict(
        operation='preview_execution', prompt=PROMPT, execution_constraints=constraints)),
        capture_output=True, text=True, encoding='utf-8', cwd=BASE)
    response = json.loads(result.stdout)
    preview = D / (rid + '_preview.json')
    put(preview, dict(returncode=result.returncode, response=response))
    assert result.returncode == 0 and response.get('selected') == 'mimo'
    rows = [dict(provider='mimo', lemma=constraints['lemma_id'], request_id=rid,
        payload=str(payload), payload_sha256=sha(payload), prompt_chars=len(PROMPT),
        selected=response['selected'], preview=str(preview),
        status='PREPARED_NOT_SUBMITTED', after='MiMo a46; existing coordinator FIFO',
        dispatch_deadline='2026-09-25T20:32:00Z')]
    put(D / 'prepared_units.json', rows)
    put(D / 'manifest.json', dict(script_sha256=sha(Path(__file__)),
        units=rows, executor_calls=0, originals_modified=False, gate_changed=False))
    print(json.dumps(rows, ensure_ascii=False))

if __name__ == '__main__':
    main()
