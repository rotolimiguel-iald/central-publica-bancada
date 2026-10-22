"""Publish the insertion-normalization diagnostic and explicit ordered descendant."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
D=H/'free_euler_descent_delivery';D.mkdir(exist_ok=False)
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,existing=False):
 if p.exists():
  assert existing;old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
  assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
 assert b and t.read_bytes()==b;t.replace(p)
def put(p,v,existing=False):write(p,json.dumps(v,indent=2,ensure_ascii=False).encode('utf-8'),existing)
def append(p,text):write(p,p.read_bytes()+text.encode('utf-8'),True)
folders=['free_euler_insertion_contact','free_euler_leibniz_contact','euler_ghost_descendant_contact']
results={f:json.loads((H/f/'results.json').read_bytes()) for f in folders}
audit=json.loads((H/'mimo_directed_ghost_current_review/local_audit.json').read_bytes())
checks=sum(v['checks'] for v in results.values())+audit['checks']
cpu=sum(v['cpu_seconds'] for v in results.values())+audit['cpu_seconds']
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[DERIVED — inserção Euler condicionada à normalização; Q2 completa OPEN]

No auxiliar plano e na prescrição radial existente, a linha do Euler completo
obedece P_hh N_hh+P_hb N_bh=box I10 como identidade polinomial, para qualquer
kernel escalar. O termo de b é necessário: omiti-lo deixa uma matriz não nula.
Isso explica por que substituir E_h por apenas a Hessiana EH seria incorreto.

Para precisar a normalização de inserções, mantivemos o MESMO produto
z^(a-2)=f_a g_a, com f_a=z^(tau*a-1),g_a=z^((1-tau)*a-1), z>0.
tau é uma alocação diagnóstica do regulador, não parâmetro da TGL nem escolha
de estado. Ele não foi ajustado ao resíduo. Dividindo contatos por CE=-4pi²,
o polo simples da prescrição já existente fornece:

 FP[(1-a)(box f_a)g_a] = tau*q²/8;
 FP[(1-a)f_a(box g_a)] = (1-tau)*q²/8.

Aqui box f_a=4*tau*a*(tau*a-1)z^(tau*a-2), e o resíduo normalizado de
z^(a-3) é -q²/32. Só o coeficiente linear ema contribui nestes termos.
Para derivada em uma linha: (box f_a)d_j g_a dá tau*q_j*q²/24;
(d_j box f_a)g_a dá tau*q_j*q²/12. A soma é a derivada do primeiro contato.

Não se alterou a extensão do produto ordinário. A correção dos gradientes
cruzados na regra de Leibniz é q²/4; somada aos contatos Euler q²/8 dá
3q²/8, exatamente -C_box(z^-2) do motor radial existente. O total independe
de tau. Este cálculo mostra uma liberdade na normalização da inserção
diferenciada antes da multiplicação; não estabelece qual normalização de
produtos temporais satisfaz todas as identidades BV. Não se definiu delta*f
por multiplicação de distribuições nem se adotou f(0)=0.

A contagem de campos distingue corrente e vértice de anticampo. A corrente
hdagger*c*c não tem bubble de DUAS linhas com barc*h*c, pois hdagger não
contrai. Após s0hdagger=E_h, existem dois emparelhamentos com duas linhas,
deixando dois ghosts externos; h e b devem compor a linha Euler completa.
Já o VÉRTICE hdagger*h*c admite duas linhas, deixando hdagger e c externos.
Logo não se pode excluir todo o setor de anticampo pela contagem da corrente.

Foi calculado também o contato ORDENADO I_E,X Vghost,Y, onde
I_E=sum_A E_A[G,chiX]w_A e Vghost mantém a forma anterior à IBP como origem
dos sinais. Ambos os emparelhamentos de w=c.dc foram retidos, com sinais-,+.
Para lambda=e0-e1,eta=e0, foram852 termos; ordem de cutoffs trocada,532.
As16 entradas B_ur(D) e a parte B-B^dagger estão nos resultados. O adjunto
ponderado usa B^dagger=B^T(-D-lambda-eta). No controle q=0, a entrada01 é
-187*tau/192. Este é um candidato explícito na família declarada, SEM fator
global Ward/ação efetiva, SEM soma automática dos cutoffs e SEM seleção de
tau. Portanto não foi somado ao resíduo anterior para anunciar cancelamento.
A necessidade seguinte é derivar a normalização EOM compatível e o peso
global da descida, incluindo o setor de fontes e a identidade inhomogênea.

Recebido e auditado MiMo6307. Sua proposta de cancelamento é refutada pela
regra da cadeia (d_X f(Y-X)=d_X f(X-Y)), pelo cálculo exterior(-,+), pelo
vértice Lie_c h que foi indevidamente reduzido ah, e pelo controle pedido:
2357/117649+314/117649=2671/117649, não zero. A resposta e o recibo foram
preservados; nenhum engine foi alterado para acomodá-la. Uso medido365857
tokens; custo estimadoUSD0.17379642, não fatura; ledger uma única vez.

{checks}controles locais,CPU{cpu}s, quatro comandos rc0 com logs custodiados.
Alcance: contatos racionais auxiliares e diagnóstico de normalização.
Q2 integral, normalização lorentziana e gate permanecem sem fechamento novo.
Abertura sha256={opening}.
'''
write(D/'DERIVACAO.md',report.encode('utf-8'))
write(OUT/'ENTREGA_016_A7b_contatos_Euler_e_descendente.md',report.encode('utf-8'))
paths=[Path(__file__),D/'DERIVACAO.md',H/'euler_ghost_descendant_contact_engine.py']
for f in folders:paths.extend([H/f/'results.json',H/f/'manifest.json'])
paths.extend(H/f for f in ['free_euler_insertion_contact_check.py','free_euler_leibniz_contact_check.py',
 'euler_ghost_descendant_contact_check.py','free_euler_insertion_contact_run.log',
 'free_euler_leibniz_contact_run.log','euler_ghost_descendant_contact_run.log',
 'audit_mimo_directed_ghost_current.py','audit_mimo_directed_ghost_current_run.log',
 'mimo_directed_ghost_current_review/local_audit.json','mimo_directed_ghost_current_review/manifest.json'])
manifest=dict(at=now.isoformat(),opening_sha256=opening,checks=checks,cpu_seconds=cpu,
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],full_Q2=False,gate_changed=False)
put(D/'manifest.json',manifest)
ledger=OUT/'LEDGER_016.jsonl'
append(ledger,json.dumps(dict(at=now.isoformat(),event='FREE_EULER_INSERTION_AND_ORDERED_DESCENDANT',
 target='A7.b',checks=checks,cpu_seconds=cpu,remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
seen=set();cost=Decimal(0)
for line in ledger.read_text('utf-8').splitlines():
 e=json.loads(line);v=e.get('cost_estimate_usd',e.get('cost_usd'))
 if v is None:continue
 key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id')
 if key and key in seen:continue
 if key:seen.add(key)
 cost+=Decimal(str(v))
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b PROGRESSO:contatos Euler,Leibniz e descendente ordenado calculados;MiMo6307 auditado/refutado no controle;{checks}checks,CPU{cpu}s,custo conhecido parcialUSD{cost},assinaturas desconhecidas;Q2 OPEN,gate intacto. Abertura sha256={opening}.\n')
p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes())
state['free_euler_descent_update']=dict(at=now.isoformat(),manifest=str(D/'manifest.json'),
 next='Derive compatible time-ordered EOM normalization and global inhomogeneous Ward coefficient before combining ordered descendant with h/c matrix',
 symbolic_allocation_not_selected=True,ordered_cc_defect_01='-187*tau/192',
 mimo_6307='Received, ledgered, local counterexamples reject proposed zero',own_processes=[],full_Q2=False,gate_changed=False)
put(p,state,True)
for item in manifest['artifacts']:assert sha(Path(item['path']))==item['sha256']
print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=checks,cpu_seconds=cpu,known_partial_cost_usd=str(cost))))
