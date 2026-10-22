"""Prepare one distinct skeptical review of the newly derived bilocal identity."""
from pathlib import Path
from datetime import datetime,timezone
import json,uuid,subprocess,sys
from prepare_curved_wick_defect_review import put,sha,H,BASE
D=H/'orchestration_bilocal_wick_transport'

QUESTION='''ORDEM016 A7.b, revisão independente de ALTA complexidade.
Uma pergunta precisa: a identidade bilocal abaixo transporta corretamente as
duas correções A1 para o termo de contato temporal, e qual é a fórmula EXATA
que resta quando se aplica a extensão radial R já fixada?

Não é nova tentativa do cálculo curvo6945 concluído, nem da mudança BV57e
em revisão MiMo. Não escolher tau para cancelar números. Não repetir parecer
genérico de anomalias. Revise a passagem algébrica e escreva a diferença
entre transportar antes/depois de estender, com sinais, fatores i*hbar e
simetrização. Se a identidade só vale para kernels suaves, localize essa
restrição exatamente. Não use aprovação do CAS como prova de distribuição.

q=s0 é derivação ímpar linear LIVRE, contrações somente de campos;
antifields sem propagador, mas q(hdag) contém Euler. t=i*hbar.
Nx=exp(t CWx), Ny=exp(t CWy), W=G-H suave. N_H=N_G exp(t CW).
A1=t[q,CW]. Na referência G, q é equivarante se o Green homogêneo completo
satisfaz a identidade livre, hipótese explícita. BF é contração Feynman
CRUZADA, BW contração W cruzada, BH=BF-BW.
No tensor graduado antes da multiplicação m:
RW,total=[q,CWx+CWy+BW], Rx=[q,CWx], Ry=[q,CWy].
(q+t RW,total)exp(t BH)-exp(t BH)(q+t Rx+t Ry)
  =t exp(t BH)([q,BH]+[q,BW])=t exp(t BH)[q,BF].
Os segundos comutadores com contrações constantes se anulam. A fonte à
direita independe de W, mas o fator exp(t BH) NÃO. Não afirmar invariância
total de A2 nem suprimir delta*propagador. Modelo finito é só controle de
sinais; texto e código originais seguem abaixo.

Para F,G pares, convenção de Fröb1803.10235v3 eq34-35,154-158:
S2=[T1(F)star T1(G)+T1(G)star T1(F)]/2,
Tc2=(i/hbar)(T2-S2)=-1/t*(T2-S2),
T1(A2)=qhat Tc2-Tc2((s0+A1)F,G)-Tc2(F,(s0+A1)G)-T1((F,G)).
Na ordem relevante V1 tem vértices EH cúbico, chi barc C Lie_c h e
chi[hdag Lie_c h+cdag c.nabla c] em coordenadas BV assinadas B;
qcdag=-Qbarc-Kg*hdag, qhdag=H0h+C*b. h e b completam a linha Euler.

Prescrição ordinária já fixada (auxiliar EUCLIDEANO 4D):
R(f)=FP_a[(1-a)mu^(2a) z^a f], z=|x-y|²;
CE=-4pi², q_i é símbolo de derivada de delta, NÃO momento Fourier.
Res[z^(a-n)]/CE=-(q²)^(n-2)/(4^(n-1)(n-1)!(n-2)!), n>=2.
C_w(f)=(R(D_w f)-D_w R(f))/CE.
C_ij(1/z)=-delta_ij/4, Delta R(1/z)=CE delta.
f_a=z^(tau a-1),g_a=z^((1-tau)a-1) tem produto ordinário fixo;
FP[(1-a)(Delta f_a)g_a]/CE=tau q²/8, outro=(1-tau)q²/8.
Isto só diagnostica alocação das inserções; tau NÃO escolhido. A soma e o
termo de gradientes cruzados dão3q²/8, conforme Leibniz. Não confundir
inserção Euler antes de multiplicar com derivada do produto completo.

Entregue uma derivação crítica: formule o representante A2 nesta convenção
em termos do COMUTADOR da extensão com o operador de Ward e do contato
composto, e diga quais parcelas já se compensam pela identidade acima.
Se R ordinário não fixa o contato composto, exponha o dado mínimo ainda
necessário; não invente cancelamento nem um teorema de impossibilidade.
Trabalho deve permanecer no alvo A7.b. Prazo2026-09-25T20:32:00Z.
Resposta DECLARADO até auditoria local. Memória científica comum obrigatória.
'''

def main():
    D.mkdir(exist_ok=False);rid=str(uuid.uuid4())
    paths=[H/'bilocal_wick_ward_transport/DERIVACAO.md',
           H/'bilocal_wick_ward_transport_check.py']
    prompt=QUESTION
    for p in paths:
        prompt+='\nFONTE CUSTODIADA '+str(p)+' SHA256='+sha(p)+'\n'+p.read_text('utf-8')
    ec=dict(mission_id='ORDEM_016',branch_id='A-7.b',lemma_id='bilocal_wick_ward_transport_and_extension_commutator',
            role='skeptic',required_provider='deepseek',max_calls=1,max_cost_usd=None,max_output_tokens=393216)
    payload=D/'deepseek_bilocal_wick_transport_submit.json'
    put(payload,dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=ec))
    put(D/(rid+'_origin.json'),dict(at=datetime.now(timezone.utc).isoformat(),
        thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',request_id=rid,
        payload=str(payload),payload_sha256=sha(payload),original_house='Central de Patentes',
        status='PREPARED_NOT_SUBMITTED'))
    run=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'transport_cli.py')],
        input=json.dumps(dict(operation='preview_execution',prompt=prompt,execution_constraints=ec)),
        capture_output=True,text=True,encoding='utf-8',cwd=BASE)
    response=json.loads(run.stdout);preview=D/(rid+'_preview.json')
    put(preview,dict(returncode=run.returncode,response=response))
    assert run.returncode==0 and response.get('selected')=='deepseek'
    units=[dict(provider='deepseek',request_id=rid,payload=str(payload),payload_sha256=sha(payload),
        lemma=ec['lemma_id'],selected=response['selected'],preview=str(preview),
        status='PREPARED_NOT_SUBMITTED',dispatch_deadline='2026-09-25T20:32:00Z')]
    put(D/'prepared_units.json',units)
    print(json.dumps(units,ensure_ascii=False))

if __name__=='__main__':main()
