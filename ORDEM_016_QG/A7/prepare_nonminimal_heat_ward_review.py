"""Prepare an independent review of the newly measured mixed Ward jet."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid,subprocess,sys
H=Path(__file__).resolve().parent
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
D=H/'orchestration_nonminimal_heat_ward'
PROMPT=r'''ORDEM016 A7.b: uma NOVA unidade cética delimitada, não repetir a revisão antiga
de Leibniz/descida 6309. A bancada construiu os jatos abaixo e pede auditoria
independente, não concordância. Memória científica comum obrigatória. Nenhum
arquivo será modificado; não alegue execução de CAS. Prazo2026-09-25T20:32Z.

Pergunta única: o coeficiente337/10 da expressão normalizada A1(Faf) abaixo
segue destes dados e desta prescrição, ou há erro de sinal/fator/tipo/parte
suave no encadeamento? Dê um contraexemplo ou uma reconstrução independente,
nomeando hipóteses ausentes; não afirmar Q2 completa ou continuação lorentziana.

Prescrição AUXILIAR EUCLIDIANA em espaço-forma4D de curvatura constante K.
S^2T*: Itr=I-2P_tr, dimTL9, dimtr1. Lh=nabla²+K(-2P_TL+6P_tr),
Lq=nabla²+3K. Calor exp(tL): (4pi t)^-2 exp(-z/(4t))*sum U_n t^n,
z=dist². Parametrix escolhido Hr=U0/z-U1 log(z/l²)/4+U2 z log(z/l²)/16+...
sem parte suave acrescentada. Covariância comum leading1/z; não foi aplicado
normalizador físico/Feynman. Coeficientes coincidentes conhecidos:
[U1h]=8K P_tr; [U1q]=5K I4;
[U2h]=K²(-7/5 P_TL+479/15 P_tr); [U2q]=K²179/15 I4.
Resto Euler já calculado [Lr Hr]=3[U2r]/4.

Gauge K_g v=2sym nabla v, K_g^*=-2div, C=div Itr,
C^*=-sym nabla+g div/2=-Itr K_g/2, ell=1/(2kappa).
Hessian H0 K_g=0, D=H0+ell C^*C=-Itr Lh/(4kappa), Q=C K_g=Lq.
Logo Lh K_g=K_g Q, div Lh=Q div. Assume-se o entrelaçamento formal dos
coeficientes de calor por unicidade de transporte, sem construir estado global.
HD=-4kappa Hh Itr, HQ=Hq. Parametrix graduado candidato na ordem(h,b,c,barc):
Hfull=[[HD,K_g HQ,0,0],[HQ K_g^*,0,0,0],[0,0,0,HQ],[0,0,-HQ,0]].
P=[[H0,C^*,0,0],[C,-ell^-1,0,0],[0,0,0,-Q],[0,0,Q,0]].
S=ell C HD-HQ K_g^*. Multiplicação de blocos:
(PHfull)_hh=D HD-C^*S; (PHfull)_bh=S/ell;
(PHfull)_bb=Q HQ; (PHfull)_cc=(PHfull)_barcbarc=Q HQ; hb=0.

Em índices covariantes, defina
B_n=div_x U_h,n + sym(nabla_y U_q,n),
A_n=(nabla_x z) contraído U_h,n + sym((nabla_y z)U_q,n).
O heat Ward dá A0=0 e B_n=A_(n+1)/4. Na derivada do parametrix:
B0/z - A0/z² - B1 logz/4 - A1/(4z)
 + B2 z logz/16 + A2(logz+1)/16 = A2/16 + O(r³ log r).
Portanto S=-2(div_x Hh+sym nabla_y Hq) tem primeiro jato -nabla A2/8.
Para entrada tensorial h, [nabla_x,lambda A2]_nu(h)=
2(U2h h)_lambda,nu -2*(179/15)K²*h_lambda,nu.
Conclusão proposta:
[nabla_x,lambda S_nu](h)=K²[-25/12*g_lambda,nu*trh +10/3*h_lambda,nu].
Ou r=-25K²/12,s=5K²/3 em r*g*g+s*(g*g+g*g).
[C^*S]=K²(-10/3 P_TL-5P_tr).

Controle independente do heat Ward, SEM presumir esse jato:
Para cada feixe, Omega_ij é a representação de E_ij-E_ji; E_h=-2TL+6tr,
E_q=3I. Os jatos ordenados U1, com K² retirado, são
xx_ij=(E/2+29I/30)*delta_ij +sum_k{Omega_ik,Omega_jk}/12
      +Omega_ij*(E+2I)/2.
O jato MISTO DO CALOR U1 é -xx_ji por Synge (não o jato Green a2/2-xx_ji).
Verificados16 componentes de
sum_mu (xx_h,lambda,mu h)_mu,nu
-sum_alpha,beta (xx_q,alpha,lambda)_nu,beta h_alpha,beta
= (U2h h)_lambda,nu/2 -(179/30)h_lambda,nu.

Convenção BV já adotada pela bancada: qh=K_g c,qbarc=-b,qb=qc=0;
qhdagger=+H0 h+C^*b; qcdagger=-Q barc-K_g^*hdagger.
Contração com c dá Jc0=+Q HQ porque H_barc,c=-HQ.
Então Jh0=K²(137/60 P_TL+579/20 P_tr), Jc0=K²179/20 I4.
Os jatos seguintes Jh1(rank5),Jc1(rank3) zeram por isotropia/paridade.

Faf=int chi[hdagger Lie_c h+cdagger_i c^j nabla_j c^i].
Com diferencial quântico livre fixado numa representação G equivarante,
W=G-Hfull e N_H=N_G exp(i hbar C_W), A1=i hbar[q,C_W].
Nas coordenadas simétricas independentes h_A e antifields duais:
A1(Faf)/(i hbar)=int chi[ tr(M(nabla c)Jh0)+Jc0[i,j]nabla_j c^i],
tr(M P_TL)=9 divc/2,tr(M P_tr)=divc/2.
Daí (9*137/120+579/40+179/20)K² int chi divc
=(337/10)K² int chi divc. Primitiva ALGÉBRICA=(337/20)K² int chi trh.
Não se adotou contratermo físico: realidade, Lorentz e admissibilidade pendentes.
Sem o termo C^*S sairia81/5; diferença35/2. Não confundir expressão normalizada
euclidiana, representante de primeira ordem, classe de anomalia e Q2 completa.
O qhat não pode ser redefinido por conjugação de H para forçar zero.
'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,x):
    assert not p.exists(),p
    b=json.dumps(x,ensure_ascii=False,indent=2).encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
def main():
    D.mkdir(exist_ok=False);rid=str(uuid.uuid4())
    constraints=dict(mission_id='ORDEM_016',branch_id='A-7.b',
        lemma_id='nonminimal_heat_ward_first_jet_coefficient',role='skeptic',
        required_provider='deepseek',max_calls=1,max_cost_usd=None,max_output_tokens=393216)
    source=H/'nonminimal_wick_heat_ward_check.py'
    prompt=PROMPT+'\nProveniência: script científico local '+source.name+' SHA256='+sha(source)+'. Dados acima extraídos explicitamente, não dependem de acesso remoto ao arquivo.\n'
    payload=D/'deepseek_nonminimal_heat_ward_submit.json'
    put(payload,dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=constraints))
    put(D/(rid+'_origin.json'),dict(at=datetime.now(timezone.utc).isoformat(),
        thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',request_id=rid,
        payload=str(payload),payload_sha256=sha(payload),status='PREPARED_NOT_SUBMITTED',
        original_house='Central de Patentes',mission_bench=str(H)))
    run=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'transport_cli.py')],
        input=json.dumps(dict(operation='preview_execution',prompt=prompt,execution_constraints=constraints)),
        capture_output=True,text=True,encoding='utf-8',cwd=BASE)
    response=json.loads(run.stdout);preview=D/(rid+'_preview.json')
    put(preview,dict(returncode=run.returncode,response=response))
    assert run.returncode==0 and response.get('selected')=='deepseek'
    units=[dict(provider='deepseek',request_id=rid,payload=str(payload),payload_sha256=sha(payload),
        lemma=constraints['lemma_id'],selected=response['selected'],preview=str(preview),
        status='PREPARED_NOT_SUBMITTED',dispatch_deadline='2026-09-25T20:32:00Z')]
    put(D/'prepared_units.json',units)
    print(json.dumps(units,ensure_ascii=False))
if __name__=='__main__':main()
