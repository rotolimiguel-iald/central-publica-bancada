"""New MiMo unit: distribution identities only, no private engine files."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,sys,uuid
H=Path(__file__).resolve().parent;D=H/'orchestration_two_endpoint_source';BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923';D.mkdir(exist_ok=False)
def put(p,v):
 assert not p.exists();b=json.dumps(v,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
prompt='''ORDEM_016 A7.b. Unidade científica nova de revisão independente de
identidades distribucionais; memória canônica comum obrigatória. Nenhum
arquivo de código da bancada é anexado. Não executar ferramentas nem alegar
resultados computacionais. DECLARADO até verificação. Não substituir tarefas
Kimi, não reenviar tarefa MiMo terminal, não modificar a prescrição.

PERGUNTA ÚNICA: qual é o contato exato, com os sinais corretos, entre a
fonte bilocal localizada primeiro e sua extensão realizada depois, versus
a fonte estendida primeiro e localizada depois?

Dados suficientes: R=FP_a[(1-a)mu^(2a)z^a], z=(X-Y)^2 em4D euclidiano,
R comuta com multiplicação suave. E_X é o Einstein linearizado plano:
(Eh)_uv=-Box h_uv-partial_u partial_v trh
+partial_u partial_i h_iv+partial_v partial_i h_iu
+delta_uv(Box trh-partial_i partial_j h_ij).
E*=E em testes compactos. Defina C_D(f)=R(Df)-D R(f); não adicionar
contatos à adjunção de distribuições já estendidas.

A fonte sem cutoff é A_uv,r(X,Y)c^r(Y)+B^j_uv,r(X,Y)partialY_j c^r(Y).
C=A-divY B. Use cutoffs INDEPENDENTES chiX(X) e chiY(Y), suaves compactos.
Objeto efetivo:
 P=E_X {chiX [chiY R(A)-partialY_j(chiY R(B^j))]}.
Objeto de referência fora da diagonal estendido:
 Q=R {E_X [chiX (chiY C-(partialY_j chiY) B^j)]}.
Derive P-Q em termos de C_E e C_partialY. Preserve a ordem de E, os
dois cutoffs, suas derivadas e os produtos com derivadas de delta.
Separe a regra abstrata válida para qualquer fonte e o exemplo abaixo.

Para exemplo quantitativo, a fonte plana calculada tem
C_uv,r=[-12delta_uv x_r-30(delta_ur x_v+delta_vr x_u)]/z4
+96x_u x_v x_r/z5, x=X-Y.
B^j_uv,r é combinação de sete tensores, com coeficientes
(-2,-4,-4,16,-8,20,0), na base ordenada:
delta_jr delta_uv/z3;
(delta_ju delta_vr+delta_jv delta_ur)/z3;
delta_uv x_j x_r/z4;
delta_jr x_u x_v/z4;
(delta_ju x_v x_r+delta_jv x_u x_r)/z4;
(delta_ur x_j x_v+delta_vr x_j x_u)/z4;
x_j x_u x_v x_r/z5.
O valor CE=-4pi² é fator escalar, não o operador C_E.
Res(z^(a-n))/CE=-(q²)^(n-2)/[4^(n-1)(n-1)!(n-2)!] para n>=2;
multiplicar por x_i corresponde a -partial_qi no símbolo de delta.
q simboliza partial delta, NÃO momento Fourier sem fator i.

Calcule ao menos o contato R(divY B)-divY R(B) explicitamente para r=0
e dê uma componente verificável. Explique quando se pode e quando não
se pode substituir chiX partial^nu delta por chiX(Y) partial^nu delta.
Confronte o limite chiX=chiY=1 e a troca indevida E R=R E.
Não inferir que a soma das bolhas ou Q2 interagente completa se anula;
não introduzir estado físico, Lorentz, novo contratermo nem outro ramo.
'''
request=str(uuid.uuid4());constraints=dict(mission_id='ORDEM_016',branch_id='A-7.b',lemma_id='two_endpoint_localized_source_distribution_identity',role='skeptic',required_provider='mimo',max_calls=1,max_cost_usd=None,max_output_tokens=131072)
payload=dict(operation='submit',request_id=request,prompt=prompt,execution_constraints=constraints);p=D/'mimo_two_endpoint_source_submit.json';put(p,payload)
put(D/'origin_receipt.json',dict(at=datetime.now(timezone.utc).isoformat(),thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',request_id=request,payload=str(p),payload_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),status='PREPARED_NOT_SUBMITTED',content='Explicit mathematical equations; no attached private engine files'))
run=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'transport_cli.py')],input=json.dumps(dict(operation='preview_execution',prompt=prompt,execution_constraints=constraints),ensure_ascii=False),text=True,capture_output=True,encoding='utf-8',cwd=BASE)
r=json.loads(run.stdout);put(D/'preview.json',dict(returncode=run.returncode,response=r))
catalog=[dict(provider='mimo',request_id=request,lemma=constraints['lemma_id'],payload=str(p),payload_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),prompt_chars=len(prompt),selected=r.get('selected'),status='PREPARED_NOT_SUBMITTED')]
put(D/'prepared_units.json',catalog);print(json.dumps(catalog))
