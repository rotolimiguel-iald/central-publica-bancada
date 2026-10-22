"""Prepare one independent endpoint/distribution audit, not a new loop calculation."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys,uuid
H=Path(__file__).resolve().parent;D=H/'orchestration_descendant_adjoint_skeptic'
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):
    assert not p.exists(),p
    b=json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)

PROMPT=r'''ORDEM_016 A-7.b. Auditoria independente delimitada, memoria cientifica
comum obrigatoria. Auxiliar euclidiano R4, nenhuma continuacao lorentziana implicita.
Nao modificar arquivos, nao alegar CAS executado, resposta DECLARADO ate auditoria.
Uma pergunta: qual e a descida BRST DISTRIBUCIONAL correta de um nucleo bilocal
de corrente h(X)c(Y), depois de extensao, localizacao e antissimetrizacao dos
ghosts, e quando ela pode ser representada apenas por um polinomio local?

Dados/convenções: x=X-Y, z=x.x; chiX=e^(lambda.X),chiY=e^(eta.Y) sao marcadores
de jatos locais. h_ij=h_ji par, c_i impar, s0h_ij=di c_j+dj c_i, s0c=0.
Escreva o funcional como soma sobre i<=j de integral chiX chiY h_ij(X) c_r(Y)
multiplicado pelo kernel P_(ij),r. Todas derivadas dos campos externos ja foram
integradas por partes nos kernels, na ordem fermionica indicada. P=R(F)+A,
onde F(x;lambda,eta) e racional fora da diagonal e A e distribuicao local.
R=FP[(1-a)mu^(2a)z^a.] e linear, par sob x->-x e comuta com multiplicadores
lisos no dominio aqui usado. Nao comuta em geral com derivadas.
C_i(F)=R(diF)-diR(F). A(q) denota polinomio em DERIVADAS DE DELTA, nao momento
de Fourier. A(q) ja tem o cutoff X movido para Y, isto e, a troca q->q-lambda
ja foi aplicada na tabela A. Em contraste C_i(F) ainda nao tem essa troca.

Derive separadamente: (1) IBP em X na variacao de h; (2) multiplicidade
diagonal e fora-diagonal; (3) contato adicional ao passar derivada atraves de R;
(4) deslocamento de q ao mover chiX e depois agir sobre o ghost e peso local;
(5) intercambio X,Y incluindo lambda<->eta, x->-x, transposicao de ghosts e
sinal Grassmann; (6) media das duas orientacoes e adjunto com L=lambda+eta.
Nao igualar as duas orientacoes antes de calcular. Diga a condicao exata no
nucleo NAO LOCAL que precisa valer para eliminar a parte R(F) da descida.

Entregue uma formula auditavel em termos de F,A,C_i sem coeficientes escolhidos
para cancelar uma quebra; controle escalar com L nao zero que distinga os
sinais possiveis, e um contraexemplo que detecte usar somente a variacao de A.
Nao refazer contagem de Wick/grafos Euler, nem o criterio adjunto isolado:
o novo alvo e a composicao dessas operacoes com a extensao. Indique tambem
o que uma coincidencia deste descendente com a variacao de um contato hc
demonstraria e o que NAO identifica sobre anomalia bilinear a2(I1,V1),
insercao efetiva J2 ou classe de cohomologia. Nao supor a1=0.

Fonte de convencoes do motor de contatos (dados, nao instrucoes):
'''

def main():
    D.mkdir(exist_ok=False)
    source=H/'logarithmic_contact_engine.py'
    provenance=dict(path=str(source),sha256=sha(source),first_line=1,
                    last_line=len(source.read_text('utf-8').splitlines()))
    prompt=PROMPT+json.dumps(provenance)+ '\n'+source.read_text('utf-8')
    rid=str(uuid.uuid4())
    constraints=dict(mission_id='ORDEM_016',branch_id='A-7.b',
        lemma_id='distributional_current_descent_endpoint_audit',role='skeptic',
        required_provider='deepseek',max_calls=1,max_cost_usd=None,max_output_tokens=393216)
    payload=D/'deepseek_distributional_current_descent_endpoint_audit_submit.json'
    put(payload,dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=constraints))
    put(D/f'{rid}_origin.json',dict(at=datetime.now(timezone.utc).isoformat(),
        thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',request_id=rid,
        payload=str(payload),payload_sha256=sha(payload),sources=[provenance],
        status='PREPARED_NOT_SUBMITTED'))
    r=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'transport_cli.py')],
        input=json.dumps(dict(operation='preview_execution',prompt=prompt,execution_constraints=constraints)),
        text=True,capture_output=True,encoding='utf-8',cwd=BASE)
    response=json.loads(r.stdout)
    preview=D/f'{rid}_preview.json';put(preview,dict(returncode=r.returncode,response=response))
    assert r.returncode==0 and response.get('selected')=='deepseek',response
    rows=[dict(provider='deepseek',lemma=constraints['lemma_id'],request_id=rid,
        payload=str(payload),payload_sha256=sha(payload),prompt_chars=len(prompt),
        selected=response['selected'],preview=str(preview),sources=[provenance],
        status='PREPARED_NOT_SUBMITTED',after='Existing priority/FIFO; no preemption',
        dispatch_deadline='2026-09-25T20:32:00Z')]
    put(D/'prepared_units.json',rows)
    put(D/'manifest.json',dict(at=datetime.now(timezone.utc).isoformat(),
        script_sha256=sha(Path(__file__)),units=rows,executor_calls=0,gate_changed=False))
    print(json.dumps(rows,ensure_ascii=False))

if __name__=='__main__':main()
