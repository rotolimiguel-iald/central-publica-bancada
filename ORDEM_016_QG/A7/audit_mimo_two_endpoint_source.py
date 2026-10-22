"""Audit received MiMo derivation; accept its contact and reject delta shortcut."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,time,uuid
import sympy as s
from logarithmic_contact_engine import contact,residue,Q

H=Path(__file__).resolve().parent;D=H/'mimo_two_endpoint_source_review';D.mkdir(exist_ok=False)
O=H.parents[1]/'TUNEL/DO_CHATGPT';BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b):
 if p.exists():
  old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex);bk.write_bytes(old);assert bk.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def dump(v):return json.dumps(v,ensure_ascii=False,indent=2).encode()
rp=BASE/'state/handoffs/f7f59797-7201-44a1-a4e5-25c7e748a01f_executor_receipt.json'
receipt=json.loads(rp.read_bytes());e=receipt['execution'];v=e['result']
assert e['status']=='result_ready' and receipt['request_id']=='d946bf96-9eaf-4263-bffb-fc8e1f7e688f'
write(D/'RECEIPT.json',rp.read_bytes());write(D/'RESPONSE.md',v['text'].encode())
sources=[Path(__file__),D/'RECEIPT.json',D/'RESPONSE.md',H/'logarithmic_contact_engine.py',H/'source_two_cutoff_assembly/manifest.json']
for row in json.loads((H/'source_two_cutoff_assembly/manifest.json').read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256']
write(D/'PRE_REGISTER.json',dump(dict(at=now.isoformat(),sources=[dict(path=str(p),sha256=sha(p)) for p in sources],target='Compare contact coefficients and disprove final-stage delta multiplication shortcut',full_Q2=False)))
start=time.process_time();checks=0
def eq(a,b):
 global checks
 assert s.expand(a-b)==0,(a,b);checks+=1
sig=(1,1,1,1);powers=(0,)*4
for n in range(1,5):
 for i in range(4):
  p=list(powers);p[i]+=1
  eq(contact(n,0,(i,)),-2*residue(n+1,tuple(p),sig))
  for j in range(4):
   pp=list(p);pp[j]+=1
   expected=-2*int(i==j)*residue(n+1,powers,sig)+(8*n+4)*residue(n+2,tuple(pp),sig)
   eq(contact(n,0,(i,j)),expected)
c=list(map(s.Rational,json.loads((H/'source_two_cutoff_assembly/results.json').read_bytes())['Y_contact_rank3_coefficients']))
q2=sum(q*q for q in Q)
for a in range(4):
 for b in range(4):
  for r in range(4):
   local=c[0]*int(a==b)*Q[r]*q2+c[1]*(int(a==r)*Q[b]+int(b==r)*Q[a])*q2+c[2]*Q[a]*Q[b]*Q[r]
   provider=s.Rational(-1,16)*int(a==b)*Q[r]*q2+s.Rational(1,6)*(int(a==r)*Q[b]+int(b==r)*Q[a])*q2
   eq(local,provider)
# A test function equal to these polynomials near zero suffices; append a bump.
x=s.Symbol('x');f=1+x;phi=sum((j+1)*x**j for j in range(7));counter=[]
for n in range(1,6):
 actual=(-1)**n*s.diff(f*phi,x,n).subs(x,0)
 rhs=sum((-1)**k*s.binomial(n,k)*s.diff(f,x,k).subs(x,0)*(-1)**(n-k)*s.diff(phi,x,n-k).subs(x,0) for k in range(n+1))
 naive=f.subs(x,0)*(-1)**n*s.diff(phi,x,n).subs(x,0)
 eq(actual,rhs);assert actual!=naive;checks+=1
 counter.append(dict(order=n,actual=str(actual),naive=str(naive),difference=str(actual-naive)))
elapsed=time.process_time()-start
proof=r'''[REAL/DERIVED — revisão local; parecer MiMo aceito parcialmente]

Lida a resposta integral. A fórmula P-Q=E_X(chiX K)-C_E(chiX U),
com U=chiY C-(dchiY)B, coincide com a derivação local anterior.
Também coincidem os coeficientes do contato Y, normalizados por CE=-4pi²:
(-1/16,1/6,0). As tabelas de primeira/segunda derivada sem log conferem
com o motor de contatos existente. Não foi calculada uma nova Q2 aqui.

ERRO na seção6 e no resumo8 do parecer: a igualdade
chiX(X) partial^nu delta(X-Y)=chiX(Y) partial^nu delta(X-Y)
é FALSA em geral, inclusive depois de todas as derivações. Suporte na
diagonal não apaga a sensibilidade de derivadas de delta aos jatos.
A regra correta é
f(X) partial_x^nu delta(x)=sum_{alpha<=nu} (-1)^|alpha|
 binom(nu,alpha) (partial^alpha f)(Y) partial_x^(nu-alpha) delta(x).
Contraexemplo mínimo: x delta'(x)=-delta(x), enquanto x(0)delta'=0.
Para f=1+x e teste phi=1+2x+3x²+... perto de0, as respostas são -3 e-2.
Os cinco controles conservam uma função bump idêntica a1 perto do suporte;
não dependem de testes não compactos. A simplificação só vale quando os
jatos adicionais relevantes se anulam, não por ser a etapa final.

A receita de resíduos simples conferida não deve ser estendida
automaticamente a amplitudes logarítmicas com polos duplos: nesses casos
é preciso conservar os fatores do esquema e todas as ordens de Laurent.
Essa ampliação não foi usada na aprovação parcial. O próprio parecer
não executou C_E aplicado à fonte componente a componente; a bancada já
tem esse cálculo anterior. Não refazê-lo nem promover esta revisão a
validação de todos os laços ou de uma prescrição causal completa.
'''
write(D/'REVISAO.md',proof.encode())
result=dict(at=now.isoformat(),checks=checks,cpu_seconds=elapsed,accepted=['Abstract source contact identity','Y contact rank3 coefficients','Nonlog scalar first and second derivative table'],
 rejected=['Final-stage replacement f(X) derivative(delta) by f(Y) derivative(delta)'],counterexamples=counter,full_Q2=False)
write(D/'results.json',dump(result))
usage=v['usage'];cached=usage['prompt_tokens_details']['cached_tokens'];calculated=(Decimal(usage['prompt_tokens']-cached)*Decimal('.435')+Decimal(cached)*Decimal('.0036')+Decimal(usage['completion_tokens'])*Decimal('.87'))/Decimal(1000000)
assert calculated==Decimal(v['cost_estimate_usd'])
write(D/'COST_RECONCILIATION.json',dump(dict(cache_aware_estimate_usd=str(calculated),conservative_accounting_usd=v['request_cost_accounting']['accounted_usd'],same_call_not_additive=True,invoice=False)))
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
manifest=dict(at=now.isoformat(),opening_sha256=opening,checks=checks,cpu_seconds=elapsed,artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'REVISAO.md',D/'results.json',D/'COST_RECONCILIATION.json']],full_Q2=False)
write(D/'delivery_manifest.json',dump(manifest))
ledger=O/'LEDGER_016.jsonl';prior=[json.loads(x) for x in ledger.read_text('utf-8-sig').splitlines() if x.strip()]
assert not any(t.get('execution_task_id')==e['id'] for t in prior)
event=dict(at=now.isoformat(),event='MIMO_TWO_ENDPOINT_SOURCE_REVIEW_RECEIVED_AND_AUDITED',provider='mimo',target='A7.b',request_id=receipt['request_id'],job_id=receipt['job_id'],execution_task_id=e['id'],usage=usage,cost_estimate_usd=str(calculated),conservative_alternative_not_additive_usd=v['request_cost_accounting']['accounted_usd'],response_sha256=sha(D/'RESPONSE.md'),prompt_sha256=hashlib.sha256(e['prompt'].encode()).hexdigest(),manifest_sha256=sha(D/'delivery_manifest.json'),checks=checks,cpu_seconds=elapsed)
write(ledger,ledger.read_bytes()+(json.dumps(event)+'\n').encode())
total=Decimal(0);seen=set()
for row in prior+[event]:
 key=row.get('execution_task_id') or row.get('job_id') or row.get('request_id');val=row.get('cost_estimate_usd',row.get('cost_usd'))
 if val is not None and (key is None or key not in seen):
  total+=Decimal(str(val))
  if key:seen.add(key)
note=f'''[REAL/DERIVED — revisão MiMo aceita parcialmente]

{now.isoformat()}. Abertura SHA256 {opening}.
Parecer f7f59797 lido integralmente. Identidade abstrata e coeficientes
da fonte conferem; rejeitada a regra da seção6 de substituir a função
pelo valor na diagonal ao multiplicar derivadas de delta, mesmo no final.
Contraexemplo x delta'=-delta. {checks} verificações locais; CPU{elapsed}s.
Manifesto {D/'delivery_manifest.json'}; SHA256 {sha(D/'delivery_manifest.json')}.
Uso330802entrada/95525saída/313728cache. Estimativa com cache US${calculated};
US${v['request_cost_accounting']['accounted_usd']} é alternativa conservadora da MESMA chamada, não soma.
Parcial conhecido US${total}. Nenhuma repetição remota nesta revisão.
Q2 completo OPEN; kernel, originais e gate intactos.
'''
p=O/'ENTREGA_016_A7b_revisao_MiMo_fonte_dois_cutoffs.md';assert not p.exists();write(p,note.encode())
p=O/'ENTREGA_016_PROGRESSO.md';write(p,p.read_bytes()+f'\n- {now.isoformat()} A7.b PROGRESS: MiMo fonte auditado,{checks}checks,CPU{elapsed}s; coeficientes aceitos,regra delta corrigida; custo chamadaUS${calculated},parcialUS${total}; Q2 OPEN.\n'.encode())
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c['completed_this_turn'].append('MiMo two-endpoint source review audited; delta multiplication shortcut refuted');c.update(at=now.isoformat(),mimo_two_endpoint_review_manifest=str(D/'delivery_manifest.json'),partial_metered_cost_usd=str(total),mimo_f7_received=True);write(p,dump(c))
print(json.dumps(dict(checks=checks,cpu_seconds=elapsed,partial_cost=str(total),manifest=str(D/'delivery_manifest.json'))))
