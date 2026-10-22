"""Deliver the ordered covariant source operator and its non-gauge residue."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    b=v if isinstance(v,bytes) else (v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)).encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bak=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'));bak.write_bytes(old);assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
r=json.loads((H/'covariant_source_operator/results.json').read_bytes())
a=json.loads((H/'covariant_source_operator_audit/results.json').read_bytes());cpu=r['cpu_seconds']+a['cpu_seconds']
report=f'''[DERIVED — operador logarítmico covariante de uma bolha, condicionado aos parametrices; REAL — CAS; OPEN — Q2 completa]
# A7.b — a fonte curva não é anulada separadamente pela Hessiana
Abertura SHA256 `{opening}`. UTC {now}.

Modelo087, K constante, primeira ordem K, setor sigma projetado, cálculo
euclidiano auxiliar. Mantidos os vértices069 e o transporte dos propagadores
e da densidade externa já verificados. O coeficiente abaixo é dividido por
A0=1/(8pi²), pela fase Fourier comum e pelos fatores globais da bolha
registrados na normalização relativa. Não é um resultado Lorentziano completo.

**Resultado.** Escreva K_gauge(v)_ab=nabla_a v_b+nabla_b v_a, distinto da
curvatura K. A contribuição logarítmica da bolha marcada, como operador local,
é

    R(v)=3/8 K_gauge(Box v)-1/2 Hess(div v)
           +K[-37/8 K_gauge(v)+2g div(v)]+O(K²)
        =K_gauge(3/8 Box v-1/4 grad(div v)-37K/8 v)
           +2K g div(v)+O(K²).

Em K=0, seu símbolo é exatamente
-(3/8)p²(pv^t+vp^t)+(1/2)pp^t(p·v), o calculado anteriormente.
A novidade é que o termo 2K g div(v) não pertence à parcela de puro gauge
exibida; não foi eliminado por um ajuste de coeficiente.

**Como as derivadas foram transportadas.** O núcleo plano foi mantido como
A_ab,r(x)v^r+B_ab,r^s(x)D_s v^r. Seu resíduo local antes de integrar por
partes contém

    <A x_i x_j x_k>/6 (nabla_(ijk)T^ab)v^r
      +<B^s x_i x_j>/2 (nabla_(ij)T^ab)(nabla_s v^r).

Os colchetes são médias angulares exatas. Adjungir a primeira parcela dá
-nabla_(ijk)v e a segunda +nabla_(ij)nabla_s v. Nenhuma comutação foi
presumida. No ponto normal, gamma^r_jb,i é a derivada da conexão dividida
por K; para v(x)=v exp(ipx),

    (nabla_i nabla_j nabla_k v)^r / i
      =-p_i p_j p_k v^r+K sum_b[
          gamma^r_kb,j p_i v^b+gamma^r_kb,i p_j v^b
          +gamma^r_jb,i p_k v^b-gamma^b_jk,i p_b v^r].

Essa fórmula foi conferida por recursão independente das derivadas
covariantes para todos os256 componentes, com p,v simbólicos. A parte K
explícita dos jatos de fonte, já derivada na entrega anterior, é somada
depois. Ajuste em três polarizações e teste denso não axial dão (-37/8,2)
na base residual K_gauge(v),g div(v). A Hessiana do escalar div(v) comuta
no controle, sem impor comutação às derivadas do vetor.

**Consequência medida.** A identidade clássica H_EH K_gauge=0 já consta
das fontes; não é provada novamente aqui. No normalizado E=4kappa H_EH,
a parte principal aplicada ao resto de primeira curvatura fornece

    E0[2K g div(v)] -> 4K(pp^t-gp²)(p·v),

com a mesma fase Fourier retirada. Para p=v=(1,0,0,0), componente11=-4K.
Assim o cancelamento separado da fonte plana não se estende a esta ordem.
A soma métrica e os demais termos da identidade devem ser calculados com
os mesmos pesos antes de concluir cancelamento ou quebra Ward.

Execuções rc0: {r['checks']}+{a['checks']}assertivas,CPU{cpu}s; logs e fontes
custodiados no manifesto. Componentes de um mesmo tensor não contam como
provas analíticas independentes. Esta é derivação escrita+CAS do resíduo
logarítmico de uma bolha. O contato finito dependente de W já foi separado;
faltam extensões finitas, cutoff variável e soma causal. Não há afirmação
de anomalia quântica completa, mudança de kernel, um.py ou gate.
'''
rp=O/'ENTREGA_016_A7b_operador_covarante_fonte_curva.md';save(rp,report)
save(H/'covariant_source_operator/DERIVACAO.md',report)
measure=f'''[REAL — medida CAS; DERIVED — primeiro termo curvo; OPEN — soma quântica]
# A7.b — não estender o cancelamento separado do caso plano
Abertura SHA256 `{opening}`. UTC {now}.

Tentativa: transportar a bolha h-dagger/c do perfil normal para um operador
covariante e testar a anulação isolada por Einstein, válida na ordem plana.
Comandos: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/covariant_source_operator_check.py e A7/covariant_source_operator_audit.py.
Ambos rc0. Logs SHA256:{sha(H/'covariant_source_operator_run.log')},
{sha(H/'covariant_source_operator_audit_run.log')}.

Identidade obtida: R=K_gauge(F)+2K g div(v)+O(K²),
F=3/8 Box v-1/4 grad(div v)-37K/8 v. Logo E0 do resto tem componente11
-4K em p=v=e0. O termo foi medido, não declarado uma anomalia.
Custo local CPU{cpu}s; zero novas chamadas externas nesta conta.
Próximo ramo dentro de A7.b: contribuição métrica curva com os mesmos
pesos e contatos; depois soma causal. Não encerrar Q2 pelo subresultado.
'''
mp=O/'ENTREGA_016_MEDIDA_fonte_curva_nao_puro_gauge.md';save(mp,measure)
files=[H/n for n in ['covariant_source_operator_check.py','covariant_source_operator_run.log',
 'covariant_source_operator/PRE_REGISTER.json','covariant_source_operator/results.json','covariant_source_operator/manifest.json',
 'covariant_source_operator/DERIVACAO.md','covariant_source_operator_audit.py','covariant_source_operator_audit_run.log',
 'covariant_source_operator_audit/PRE_REGISTER.json','covariant_source_operator_audit/results.json','covariant_source_operator_audit/manifest.json',
 'covariant_source_density/derivative_placements.json']]+[rp,mp,Path(__file__)]
save(H/'covariant_source_operator/delivery_manifest.json',dict(at=now,opening_sha256=opening,
 artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
ledger=O/'LEDGER_016.jsonl';marker='A7_COVARIANT_SOURCE_OPERATOR_NON_GAUGE_CURVATURE'
if marker.encode() not in ledger.read_bytes():
    ev=dict(event=marker,at=now,provider='local',target='A-7.b',cpu_seconds=cpu,checks=r['checks']+a['checks'],
      report_sha256=sha(rp),new_external_execution=False,full_Q2=False)
    save(ledger,ledger.read_bytes()+(json.dumps(ev,ensure_ascii=False)+'\n').encode())
rows=[json.loads(x) for x in ledger.read_text('utf-8-sig').splitlines() if x.strip()];par={}
def root(k):
    par.setdefault(k,k)
    if par[k]!=k:par[k]=root(par[k])
    return par[k]
def ids(r):return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
for row in rows:
    ix=ids(row)
    for k in ix[1:]:par[root(k)]=root(ix[0])
known={}
for row in rows:
    ix=ids(row);v=row.get('cost_estimate_usd',row.get('cost_usd',row.get('custo_usd')))
    if ix and v is not None:known[root(ix[0])]=Decimal(str(v))
total=sum(known.values(),Decimal(0))
save(H/'covariant_source_operator/COST_SNAPSHOT.json',dict(at=now,total_known_partial=str(total),
 ledger_sha256=sha(ledger),unknown_cost_not_zero=True,billing_not_verified=True))
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',
 covariant_source_operator_manifest=str(H/'covariant_source_operator/delivery_manifest.json'),
 next=['Compute/combine curved metric contribution against the now explicit first-K source operator; keep finite smooth-reference and cutoff contacts',
 'Receive pending independent reviews without editing their payloads',
 'A7.c only when24h exhausted;A7.d,A8,ORDEM015 PartB,full audit remain'])
c.setdefault('completed_this_turn',[]).append('Ordered covariant source operator derived:K_gauge(F)+2K gdivv;nonzero Einstein residual -4K measured')
save(p,c)
p=O/'ENTREGA_016_PROGRESSO.md';save(p,p.read_bytes()+f'\n- {now} — A7.b PROGRESSO/MEDIDA:fonte covarianteR=K_gauge(F)+2Kgdivv,Einstein resto11=-4K;{r["checks"]}+{a["checks"]}assertivas,CPU{cpu}s. SomaQ2OPEN. Custo parcialUS${total};abertura{opening};ledger{sha(ledger)}.\n'.encode())
print(json.dumps(dict(report=str(rp),measure=str(mp),cpu_seconds=cpu,status='ACTIVE_PROGRESS')))
