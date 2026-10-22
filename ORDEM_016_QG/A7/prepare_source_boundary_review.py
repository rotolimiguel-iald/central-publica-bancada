"""Prepare a distinct source boundary review; no executor call here."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,uuid,subprocess,sys
H=Path(__file__).resolve().parent;D=H/'orchestration_source_boundary';D.mkdir(exist_ok=False)
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
def put(p,o):
 assert not p.exists();b=json.dumps(o,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
prompt=r'''ORDEM_016 A7.b. Uma revisão independente específica da FONTE hstar/c
com a fronteira ghost pré-integração por partes restaurada. Não é repetição
da fonte antiga A.c+B.dc: naquela o vértice ghost já era -dbarc.Z e apenas
os multiplicadores dos extremos eram localizados. Aqui o novo dado é
integral chiY barc divZ=-integral(chiY dbarc+dchiY barc)Z.
Memória canônica comum obrigatória; resposta DECLARADO até auditoria.

PERGUNTA ÚNICA: qual contato de extensão a fonte completa produz quando
incluímos também dchiY.bar c.Z, e qual mudança concreta ela faz em relação
à fonte antiga? Derive a partir das contrações abaixo, sem supor resultado.

Espaço euclidiano plano R4, x=X-Y,z=sum x_i², f=1/z. d_i é derivada em x.
Delta é Kronecker. S_ce,mn=(delta_cm delta_en+delta_cn delta_em-
delta_ce delta_mn)/2; Sbar_ce,mn=(delta_cm delta_en+delta_cn delta_em)/2.
chiX=e^(lambda.X),chiY=e^(eta.Y) como jatos locais, não cutoffs globais.
A contração ghost nu=m elimina a soma nu. Para cada m,mu=0..3 e cada
(c,e,xi,gxi) em {(u,v,m,-1),(u,m,-1,v),(v,m,-1,u)}, onde d_-1=id,
defina g=(-d_mu+eta_mu)d_gxi f.
Então Aeta_uv,r=-sum g*(-d_r d_xi f)*Sbar_ce,mu,m.
B_eta^j_uv,r=-sum g*(d_xi f)*[delta_jmu S_ce,r,m+
delta_jm S_ce,mu,r-delta_mum S_ce,j,r].
Esses são coeficientes do campo ghost externo e de sua primeira derivada.
Heta=Aeta+sum_j(d_j-eta_j)B_eta^j. A mudança eta no próprio A/B é a
fronteira que falta se apenas multiplicarmos a fonte antiga por chiY.
Com eta=0 deve recuperar C_uv,r=[-12delta_uv x_r-
30(delta_ur x_v+delta_vr x_u)]/z^4+96x_u x_v x_r/z^5.

O operador Einstein linear não fixado por gauge é
E(h)_uv=-box h_uv-d_u d_v trh+d_u d_i h_iv+d_v d_i h_iu+
delta_uv(box trh-d_i d_j h_ij). Multiplicidades de tensores simétricos
são as de componentes completos, não adicione um fator2 arbitrário.
R=FP_a[(1-a)mu_scale^(2a) z^a(.)], CE=-4pi²;
C_D=R D-D R. O comparador específico desta fonte é
P=E_X{chiX[chiY R(Aeta)-divY(chiY R(Beta))]},
Q=R E_X{chiX chiY Heta}.
Verifique o sinal e a validade de
P-Q=-C_E(chiX chiY Heta)+E_X[chiX chiY C_divY(Beta)].
O valor de eta já está nos coeficientes Aeta,Beta; não o conte duas vezes.
No segundo contato, divY dos kernels é -sum d_j; o termo eta_j
é multiplicação e comuta com R.

Para obter números sem qualquer ferramenta externa:
Res(z^(a-n))/CE=-(q²)^(n-2)/[4^(n-1)(n-1)!(n-2)!] para n>=2.
Multiplicação por x_i corresponde a -partial_qi. q_i é derivada de delta.
Antes de extrair resíduo, o operador E_X atua com derivada
d_i+lambda_i+2a x_i/z. A diferença regulada usa
E_shift(Heta+a*2sum x_j Beta^j/z)-E_lambda(Heta).
Só o coeficiente linear em a contribui para estes polos simples, sem logs.
Depois aplique q -> q-lambda para mover chiX à diagonal, incluindo TODOS
os jatos; f(X)partial delta não pode ser trocado por f(Y)partial delta.

Entregue: (1) A/B de fronteira em forma tensorial ou algoritmo explícito;
(2) contato P-Q para u=v=1,r=0, avaliado em q=(2,1,0,0), nos casos
(lambda,eta)=(0,0),(0,e0),(e0-e1,e0); (3) pelo menos um controle que muda
se omitimos a fronteira, com significado preciso. Se não calcular algum
número, declare a lacuna; não invente execução ou prova Lean.
Não concluir Q2=0: laços métricos/ghost, inserções da corrente clássica,
curvatura, suavidade, aridades superiores e causalidade são outros dados.
Não pesquisar novo ramo nem reinterpretar o cutoff como horizonte físico.
'''
rid=str(uuid.uuid4());constraints=dict(mission_id='ORDEM_016',branch_id='A-7.b',lemma_id='source_preIBP_ghost_boundary_contact',role='skeptic',required_provider='mimo',max_calls=1,max_cost_usd=None,max_output_tokens=131072)
p=D/'mimo_source_boundary_submit.json';put(p,dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=constraints))
sh=hashlib.sha256(p.read_bytes()).hexdigest()
put(D/'origin_receipt.json',dict(at=datetime.now(timezone.utc).isoformat(),thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',request_id=rid,payload=str(p),payload_sha256=sh,status='PREPARED_NOT_SUBMITTED',attachments=[],scope='Scientific equations only, source boundary not old localization unit'))
run=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'transport_cli.py')],input=json.dumps(dict(operation='preview_execution',prompt=prompt,execution_constraints=constraints),ensure_ascii=False),text=True,capture_output=True,encoding='utf-8',cwd=BASE)
r=json.loads(run.stdout);put(D/'preview.json',dict(returncode=run.returncode,response=r));assert run.returncode==0 and r.get('selected')=='mimo'
c=[dict(provider='mimo',lemma=constraints['lemma_id'],request_id=rid,payload=str(p),payload_sha256=sh,prompt_chars=len(prompt),selected=r['selected'],status='PREPARED_NOT_SUBMITTED',after='MiMo4d500ad2; coordinator single owner and existing FIFO')]
put(D/'prepared_units.json',c);print(json.dumps(c,ensure_ascii=False))
