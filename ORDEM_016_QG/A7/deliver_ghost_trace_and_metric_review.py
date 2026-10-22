"""Deliver trace-channel calculation, review corrections, and dispatch receipts."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
 b=v if isinstance(v,bytes) else (v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)).encode()
 if p.exists():
  old=p.read_bytes()
  if old==b:return
  bak=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
  bak.write_bytes(old);assert bak.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
r=json.loads((H/'ghost_conformal_curvature/results.json').read_bytes())
a=json.loads((H/'kimi_metric_review_audit/results.json').read_bytes())
report=f'''[DERIVED — canal de traço do resíduo ghost; REAL — CAS; OPEN — Q2 causal]
# A7.b — primeiro operador curvo no canal de traço ghost
Abertura SHA256 `{opening}`. UTC {now}.

Partimos da redução em fundo fixo de ghost_minimal_heat/DERIVACAO.md,
SHA256 `{sha(H/'ghost_minimal_heat/DERIVACAO.md')}`. Suas condições analíticas
continuam explícitas: resíduo local de calor/ciclicidade de símbolos, h pequeno
como série formal, resultado integrado módulo divergências. Não é parte finita.

Para h=f g, defina v=df, S=Hess f e d=box f. No referencial ortonormal,

    C=-df, A_mu=v_mu I-v e_mu^t, B=-S, D=B-box h=-S-d I,
    F_mu,nu=-S[:,mu]e_nu^t+S[:,nu]e_mu^t.

As contrações matriciais, verificadas para v e S simbólicos arbitrários, são

    tr sum A_mu A^mu=3v²,
    tr D²=tr S²+6d²,
    tr sum F_mu,nu F^mu,nu=2tr S²-2d²,
    tr sum Omega0_mu,nu[A^mu,A^nu]=-6K v².

Portanto, ponto a ponto para esta representante do resíduo,

    a4_2(f g)=|Hess f|²/6+17(box f)²/24+5K f box f-4K|df|².

Com f compacto, integral f box f=-integral|df|². A outra redução não pode
ser feita como se as derivadas comutassem sobre df. Por integração por partes,
integral|Hess f|²=-integral df·(grad box f+Ric(df)); Ric=3K g. Logo

    integral|Hess f|²=integral(box f)²-3K integral|df|²,
    integral a4_2(f g)=integral[7(box f)²/8-(19K/2)|df|²].

Sua Hessiana no canal f, com o fator angular da bolha retirado, é

    **H_ghost,trace = (7/4)box²+19K box.**

O termo K² f² é zero neste canal. Isso é compatível com f constante:
Q(f)=(1+f)Q(0), cujo fator multiplicativo não tem resíduo log nas condições
declaradas. Não há alegação de igualdade dos determinantes finitos.
Em K=0, a polarização identidade/identidade no resultado antigo dá7p⁴/4,
o mesmo coeficiente, sem ajuste. Omitir o comutador de conexão muda a ação
por -K|df|²/4; omitir Ric na identidade integrada muda por -K|df|²/2.

{r['checks']} checks,3 negativos,rc0,CPU {r['cpu_seconds']}s. Não é a Hessiana
tensorial hh completa nem sua soma com o setor métrico. Não foi feita a
continuação causal inteira; derivadas do cutoff reaparecem se ele for variável.
Contribuição escrita e rastreável, sem novo teorema Lean, original ou gate.
'''
rp=O/'ENTREGA_016_A7b_canal_traco_ghost_curvo.md';save(rp,report);save(H/'ghost_conformal_curvature/DERIVACAO.md',report)
review=f'''[REAL — conferência local do parecer; DECLARADO — texto externo; DERIVED — correções]
# A7.b — revisão Kimi métrica aproveitada com correções
Abertura SHA256 `{opening}`. UTC {now}.
Job2177daf6-29db-4d0c-940a-63d4c582fa04; execução2b2ea20e-990e-4410-ae1d-e9bf1a630e05.
Resposta inteira lida: received_reviews/2177daf6-29db-4d0c-940a-63d4c582fa04.md,
SHA256 `{sha(H/'received_reviews/2177daf6-29db-4d0c-940a-63d4c582fa04.md')}`.

O parecer oferece derivação útil da contração transposta, aritmética dos cinco
coeficientes, identidade longitudinal principal e expressão em Ric/R. Esses
resultados já tinham CAS local; não são novas provas apenas por concordância.

Correções verificadas nesta rodada:

1. O contraexemplo E01/E01 em p=e0 alegado como -61/240 vale **zero**.
E01=K_p(e1) é longitudinal. E11/E11 vale -7/10, como o parecer diz.
2. Nossa frase antiga "dez contrações duplas de base" era imprecisa. O código
metric_bubble_check_v2.py:111–117 testa os dez pares não ordenados de QUATRO
imagens K_p(e_nu), não os dez elementos gerais da fibra simétrica. A correção
de redação fica ao lado, com a fonte anterior preservada.
3. Cancelamento determina somente a razão dos pesos, não sinal global nem
normalização. Além disso, os pesos da Hessiana de Gamma não são os mesmos
do próprio Tr log: delta²Trlog=-Tr(G deltaQ G deltaQ) para Q linear. Assim,
Gamma=(hbar/2)Trlog H-hbar Trlog Q dá a Hessiana -métrica/2+ghost, exatamente
a convenção da fonte. A afirmação F=-Gamma/hbar no parecer confunde a ação
com seu segundo diferencial. O teste escalar exato confirma os dois sinais;
fases Lorentz completas continuam separadas como antes.
4. A seção9 troca sbarc para+b, enquanto BV069:79,96 fixa **-b**. Também
escreve sh=L_c h como se fosse a linearização; ela inclui K_gauge c.
5. Pedir F_K(K_pv,H)=0 isoladamente não é a identidade curva completa.
O setor h*c e os comutadores entre ordens contribuem. O termo fonte já
medido K_gauge(Fv)+2K g divv, cuja imagem por E é não nula, ilustra a
omissão sem exigir recalcular o laço plano.

{a['checks']} checks novos,rc0,CPU {a['cpu_seconds']}s; nenhuma bolha antiga
recalculada. Parecer e fontes originais intactos. Essas correções não anulam
o cancelamento principal calculado nem fecham Q2. Custo Kimi não informado
pelo recibo, portanto não registrado como zero. Uso318260entrada/34621saída,
310528cache/352881total, recuperado da execução, sem nova chamada.
'''
ap=O/'ENTREGA_016_A7b_revisao_Kimi_metrica.md';save(ap,review);save(H/'kimi_metric_review_audit/REVISAO.md',review)
catalog=json.loads((H/'orchestration_ghost_reduction/prepared_units.json').read_bytes())
dispatch=dict(at=now,status='STAGING_CONFIRMED_BY_COORDINATOR',
 coordinator_thread='01a0ce2b-8c2f-71b0-a9a8-91b17715a569',
 queue_registered=5,staging_after_confirmation=8,
 order='after orchestration_curved_source',units=catalog,
 separate_running_unit='Kimi curvature_log_terms job679d8876-d8b9-44db-ae96-3f8f8f67fb54',
 new_remote_execution_of_these_two_units=False)
save(H/'orchestration_ghost_reduction/DISPATCH_RECEIPT.json',dispatch)
ledger=O/'LEDGER_016.jsonl';raw=ledger.read_bytes()
events=[dict(event='A7_GHOST_CONFORMAL_CURVATURE',at=now,provider='local',target='A-7.b',
 checks=r['checks'],cpu_seconds=r['cpu_seconds'],report_sha256=sha(rp),full_Q2=False),
 dict(event='A7_KIMI_METRIC_REVIEW_AUDITED',at=now,provider='local',target='A-7.b',
 checks=a['checks'],cpu_seconds=a['cpu_seconds'],report_sha256=sha(ap),full_Q2=False)]
for u in catalog:events.append(dict(event='A7_GHOST_REDUCTION_STAGED_'+u['request_id'],at=now,
 provider=u['provider'],target='A-7.b',request_id=u['request_id'],payload_sha256=u['payload_sha256'],
 status='STAGING_CONFIRMED',new_external_execution=False))
for e in events:
 if e['event'].encode() not in raw:raw+=(json.dumps(e,ensure_ascii=False)+'\n').encode()
save(ledger,raw)
for directory,files,reportpath in [
 ('ghost_conformal_curvature',['ghost_conformal_curvature_check.py','ghost_conformal_curvature_run.log',
  'ghost_conformal_curvature/PRE_REGISTER.json','ghost_conformal_curvature/results.json','ghost_conformal_curvature/manifest.json',
  'ghost_conformal_curvature/DERIVACAO.md'],rp),
 ('kimi_metric_review_audit',['kimi_metric_review_audit.py','kimi_metric_review_audit_run.log',
  'kimi_metric_review_audit/PRE_REGISTER.json','kimi_metric_review_audit/results.json','kimi_metric_review_audit/manifest.json',
  'kimi_metric_review_audit/REVISAO.md','received_reviews/2177daf6-29db-4d0c-940a-63d4c582fa04.json',
  'received_reviews/2177daf6-29db-4d0c-940a-63d4c582fa04.md'],ap)]:
 paths=[H/f for f in files]+[Path(__file__),reportpath]
 save(H/directory/'delivery_manifest.json',dict(at=now,opening_sha256=opening,
   artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in paths]))
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',
 completed_this_turn=['Ghost fixed-background minimalization;127checks and flat coefficients recovered',
 'Trace restriction yields (7/4)box²+19Kbox with23checks under explicit analytic hypotheses',
 'Kimi metric review read/audited;15checks and corrections beside old source',
 'New Kimi ghost Hessian and MiMo multiplicative residue audit staged;5registered8staging'],
 pending_orchestration='5 registered,8staging;Kimi curvature_log_terms running',
 ghost_conformal_manifest=str(H/'ghost_conformal_curvature/delivery_manifest.json'),
 kimi_metric_review_manifest=str(H/'kimi_metric_review_audit/delivery_manifest.json'),
 ghost_reduction_catalog=str(H/'orchestration_ghost_reduction/prepared_units.json'),
 next=['Full curved ghost Hessian and metric sector incl tadpoles; integrate ordered source term without assuming separate transversality',
 'Pending reviews remain independent; do not edit or duplicate their payloads',
 'A7.b fullQ2 stillopen;A7.c onlyafter24h;A7.d,A8,PartB and finalaudit remain'])
save(cont,d)
progress=O/'ENTREGA_016_PROGRESSO.md';cost=json.loads((H/'ghost_minimal_heat/COST_SNAPSHOT.json').read_bytes())['total_known_partial']
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: canalghostde traço H=7box²/4+19Kbox condicionado,23checks CPU{r["cpu_seconds"]}s; parecerKimi auditado15checks CPU{a["cpu_seconds"]}s;2unidadesnovas staging,semduplicação. Custo parcialUS${cost},desconhecidosnãozero. Abertura{opening};ledger{sha(ledger)}.\n'.encode())
print(json.dumps(dict(reports=[str(rp),str(ap)],staged=[u['request_id'] for u in catalog],status='ACTIVE_PROGRESS'),ensure_ascii=False))
