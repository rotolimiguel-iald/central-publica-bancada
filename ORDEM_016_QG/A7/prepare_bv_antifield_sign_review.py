"""One medium-complexity MiMo review, distinct from heat/Ward computation."""
from pathlib import Path
from datetime import datetime,timezone
import json,uuid,subprocess,sys
from prepare_curved_wick_defect_review import put,sha,H,BASE
D=H/'orchestration_bv_antifield_sign'
PROMPT=r'''ORDEM016 A7.b, unidade de MEDIA complexidade de conferência de convenções.
Uma pergunta, sem repetir o cálculo curvo6945 do DeepSeek ou a aridade1 geral87d.
Memória científica comum obrigatória. Não alegar acesso a arquivo ou execução.

Pergunta: a mudança de coordenadas de antifields abaixo é uma equivalência
canônica entre os dois contratos BV, preservando os sinais do vértice ghost e
da correção de Wick? Verifique em geradores e em um monômio com ghost;
se não for, dê o sinal exato que precisa mudar. Não redefinir qhat ou H.

Campos phi=(h,b,c,barc), paridades(0,0,1,1), antifields paridade oposta.
Derivadas esquerda/direita definidas por deltaF=deltaPhi*dL F=dR F*deltaPhi.
Contrato F, fórmula fornecida de Fröb1803.10235v3 eq98:
(F,G)_F=sum_A [(dR F/dphiA)(dL G/dfdagA)
              -(dR F/dfdagA)(dL G/dphiA)].
q_F=(S_F, .)_F, (phiA,fdagB)_F=deltaAB.

Contrato B que explicita os sinais implícitos usados na bancada:
(F,G)_B=sum_A epsilonA[(dR F/dphiA)(dL G/dbdagA)
                     -(dR F/dbdagA)(dL G/dphiA)], epsilonA=(-1)^paridadeA.
q_B=(S_B, .)_B. Suposta identificação fdagA=epsilonA*bdagA, campos iguais.

Operadores reais: H0 Kg=0, Q=C Kg=Q*, ell=1/(2kappa).
Sfree=1/2<h,H0 h>+<b,Ch>-<b,b>/(2ell)+<barc,Qc>.
S_B=Sfree+<hdagB,Kg c>-<barcdagB,b>.
Logo S_F proposto=Sfree+<hdagF,Kg c>+<barcdagF,b>.
Alvo geradores B: qh=Kg c, qbarc=-b, qc=qb=0,
qhdagB=H0h+C*b, qcdagB=-Qbarc-Kg*hdagB.
Alvo F: mesmos campos, qcdagF=+Qbarc+Kg*hdagF.

Interação antifield B: Faf_B=int chi[hdagB Lie_c h+cdagB_i c^j nabla_j c^i].
Transformação proposta Faf_F=int chi[hdagF Lie_c h-cdagF_i c^j nabla_j c^i].
No setor livre H_barc,c=-HQ,H_c,barc=+HQ; contração só de campos.
Se [QHQ]=d I e primeiro jato zero, o defeito estendido
D_H(cdagB_i,c^j)=+d delta_i^j, D_H(cdagF_i,c^j)=-d delta_i^j.
Consequentemente os sinais da variável antifield e do vértice mudariam
juntos e a contribuição d*div(c) para A1(Faf)/(i hbar) deveria ser a mesma.
Calcule isso com derivadas graduadas, não por analogia de nomes.

Controle extra: em uma dimensão, q1h=c h'+2h c', q1c=c c'.
q1 comuta com a derivada espacial e é derivação ímpar à esquerda.
Verifique q1²h=0 e mostre o que falha se só o sinal de q1c for invertido.
Este controle é álgebra local, não gravidade em1D. Não presumir que um
teste apenas com campo par fixa sinais ímpares. Não invocar uma nova
liberdade de renormalização para corrigir um dicionário de coordenadas.
Prazo2026-09-25T20:32:00Z; resposta DECLARADO até auditoria local.
'''
def main():
    D.mkdir(exist_ok=False);rid=str(uuid.uuid4())
    ec=dict(mission_id='ORDEM_016',branch_id='A-7.b',lemma_id='bv_signed_antifield_coordinate_dictionary',
        role='skeptic',required_provider='mimo',max_calls=1,max_cost_usd=None,max_output_tokens=131072)
    payload=D/'mimo_bv_antifield_sign_submit.json'
    put(payload,dict(operation='submit',request_id=rid,prompt=PROMPT,execution_constraints=ec))
    put(D/(rid+'_origin.json'),dict(at=datetime.now(timezone.utc).isoformat(),
        thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',request_id=rid,
        payload=str(payload),payload_sha256=sha(payload),original_house='Central de Patentes',
        status='PREPARED_NOT_SUBMITTED'))
    run=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'transport_cli.py')],
        input=json.dumps(dict(operation='preview_execution',prompt=PROMPT,execution_constraints=ec)),
        capture_output=True,text=True,encoding='utf-8',cwd=BASE)
    response=json.loads(run.stdout);preview=D/(rid+'_preview.json')
    put(preview,dict(returncode=run.returncode,response=response))
    assert run.returncode==0 and response.get('selected')=='mimo'
    units=[dict(provider='mimo',request_id=rid,payload=str(payload),payload_sha256=sha(payload),
        lemma=ec['lemma_id'],selected=response['selected'],preview=str(preview),
        status='PREPARED_NOT_SUBMITTED',dispatch_deadline='2026-09-25T20:32:00Z')]
    put(D/'prepared_units.json',units);print(json.dumps(units,ensure_ascii=False))
if __name__=='__main__':main()
