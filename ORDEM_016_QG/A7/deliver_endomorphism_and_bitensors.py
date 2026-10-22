"""Deliver E-insertion pieces and checked bitensor data for the same A7.b loop."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    b=v if isinstance(v,bytes) else (v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)).encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        bk.write_bytes(old);assert bk.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);tmp.write_bytes(b)
    assert b and tmp.read_bytes()==b;tmp.replace(p)
def data(rel):return json.loads((H/rel).read_bytes())
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
r=data('metric_endomorphism_bubble/results.json');b=data('metric_radial_bitensor_v2/results.json');c=data('angular_cubature/results.json')
report=f'''[DERIVED — parcelas tensoriais do laço; REAL — CAS exato; OPEN — soma curva]
# A7.b — inserções do endomorfismo e transporte tensorial
Abertura SHA256 `{opening}`. UTC {now}.

**Nova parcela da bolha.** Conservados os vértices métricos, a inversa de
Gram, I_tr e a contração transposta de Wick. Expandiu-se somente a parte
de endomorfismo dos propagadores; não se trocou o feixe por dez escalares.
Para D=q²-E, E=K(-2P_TL+6P_tr),

    D^-1=I/q²+E/q4+E²/q6+… .

Na mesma base bilinear [p²trAB,p²trA trB,pAp trB+pBp trA,pABp],
a bolha com dois vértices principais e UMA inserção de E dá

    K[-14/3, 3, -1, 8/3].

Na base [trAB,trA trB], a mesma bolha com DUAS inserções (na mesma
linha ou uma em cada linha) dá K²[34/3,41/3]. Um vértice de potencial
e um principal, com UMA inserção de E e todas as posições somadas,
dão K²[96,-24]. São coeficientes brutos/A0; o fator -1/2 da Hessiana
efetiva ainda não foi aplicado a estas tabelas.

São parcelas diferentes das bolhas de potencial já entregues. Os179
checks verificam os55 pares bilineares em cada parcela e a expansão
dos vértices fora dos nós. Um controle independente usa os denominadores
exatos q²+2K e q²-6K com os projetores tensoriais e o extrator radial,
sem inserções explícitas: os coeficientes deK eK² coincidem. Apagar cada
nova parcela produz um resíduo não nulo. rc0, CPU{r['cpu_seconds']}s.

**Dados geométricos para a parcela restante.** Em quadro ortonormal por
transporte radial, retire o fator4kappa/(4pi²) de GH; z=x²,L=log(mu²z),
S=I_tr Gram^-1, V=g g^t/2 e A_i=x^j Omega_ji/2 (Omega com K retirado).
Os jatos de ordemK, nas duas pontas X eY=0, são

    H1=S/4+V L,
    (nabla_Xi H)1=A_i S/z+2x_i V/z,
    (nabla_Yj H)1=A_j S/z-2x_j V/z,
    (nabla_Xi nabla_Yj H)1=
      (z delta_ij-x_i x_j)S/(3z²)+Omega_ij S/(2z)
      -2x_i A_j S/z²+2x_j A_i S/z²
      +V(-2delta_ij/z+4x_i x_j/z²).

Essas são matrizes de10 componentes; A eOmega agem na fibra inteira.
Os2500 componentes foram comparados com o parametrix em coordenadas
normais, convertendo as duas pernas tensoriais e o índice de derivada
com o coframe e incluindo Christoffel. Não se apagou a derivada transversal
do transporte. rc0, CPU{b['cpu_seconds']}s. A v1 da verificação esqueceu
impor z=sum x_i² e falhou; preservada. A v2 corrige apenas essa relação.

**Integração angular preparada:** cubatura racional em128 direções com
pesos assinados, conferida para TODOS os495 monômios de grau até8 em S³.
São pesos de quadratura, não probabilidades. Não integra funções arbitrárias;
a cota de grau do integrando deve ser verificada antes do uso no laço.
rc0, CPU{c['cpu_seconds']}s; nenhum laço foi inferido dessa preparação.

**Alcance:** o transporte e seus jatos estão conferidos, mas ainda precisam
ser contraídos com os dois vértices e o volume. Eles não podem ser somados
como se fossem os coeficientes de E acima: as decomposições sobrepõem-se.
A soma da bolha métrica curva, sua conversão covariante e sua combinação
com ghost/fonte BV continuam abertas. Q2 finita causal não foi calculada.
Nenhum original, kernel ou gate alterado.
'''
rp=O/'ENTREGA_016_A7b_bolha_endomorfismo_e_bitensores.md'
save(rp,report);save(H/'metric_endomorphism_bubble/DERIVACAO.md',report)
# Cotejo de dependências explicitamente ausentes do pacote recebido pelo Kimi.
verified=[]
for rel in ['marked_polynomial_audit_v2/manifest.json','metric_quartic_vertices/manifest.json']:
    m=data(rel)
    for entry in m.get('artifacts',m.get('files',[])):
        p=Path(entry['path']);assert sha(p)==entry['sha256'],str(p);verified.append(str(p))
pred=data('marked_polynomial/results.json');plan=data('marked_polynomial_audit_v2/PRE_REGISTER.json')
assert sha(H/'marked_polynomial/results.json')==plan['predecessor_sha256']
assert sha(H/'marked_polynomial_engine.py')==plan['engine_sha256']
assert sha(H/'marked_polynomial_check.py')==pred['source_sha256']
assert len(pred['cases'])==160 and all(x['residual_terms']==0 for x in pred['cases'])
assert pred['checks_passed']==168 and pred['nonvacuous_polarizations']==48
audit=data('marked_polynomial_audit_v2/results.json')
assert audit['checks_passed']==1439 and audit['classical_nonzero']==189
assert audit['UV_monomial_checks']==378 and len(audit['negative_controls'])==6
ap=O/'ENTREGA_016_A7b_cotejo_Kimi_identidade_marcada.md'
audit_report=f'''[REAL — cotejo de fontes; DECLARADO — parecer externo; DERIVED — identidade principal já entregue]
# A7.b — parecer Kimi sobre a identidade h*cc
Abertura SHA256 `{opening}`. UTC {now}.

O resultado de job7af2e0e2-f377-4d51-87d3-db09350b51e4 foi recuperado
uma única vez; texto integral e recibo preservados em received_reviews/.
O Kimi não encontrou contraexemplo à prova CAS no escopo principal plano.
Esse parecer é revisão documental; não substitui as contas locais.

Conferidos agora os hashes do motor, auditoria, relatório, logs e a
dependência que o pacote não lhe fornecia: metric_principal_vertices.py.
O predecessor contém160 polarizações, todas com resíduo polinomial zero,
e8 controles clássicos, total168;48 polarizações têm parcelas não nulas.
O fonte confirma que os8 excedentes são controles da Ward clássica, em
vez de deixar isso como suposição do parecer. A auditoria posterior contém
1439 checks:400+160+400+100+378+1;189 casos clássicos não nulos e6 negativos.
As importações são módulos puros; nenhum runner foi reexecutado neste cotejo.

A covariância O(4), a multilinearidade e a ausência de divisão por momentos
nos motores sustentam a redução simbólica p=a e0,r=b e0+c e1, incluindo
casos degenerados. A cobertura por simplex é até grau5 em q. O argumento
de grau do parecer usa o vértice de duas derivadas conferido contra a ação;
não é um novo teorema Lean nem uma varredura de numeradores além desse domínio.

Aceito o parecer para essa identidade principal logarítmica h*cc, com as
dependências locais conferidas e os sinais/fatores herdados da derivação
anterior. A expressão «400 pares A,B,v» deve ser lida como400 trincas.
Nada disso conclui a identidade curva completa ou a QME finita causal.
Não refiz os1439 testes nem anunciei nova prova por votação de modelo.
Gate e originais intactos.
'''
save(ap,audit_report)
local_audit=H/'received_reviews/marked_identity_local_cotejo.json'
save(local_audit,dict(at=now,verified_files=verified,predecessor_cases=160,
    source_sha256=sha(H/'marked_polynomial_check.py'),review_sha256=sha(H/'received_reviews/7af2e0e2-f377-4d51-87d3-db09350b51e4.md'),
    report_sha256=sha(ap),scope='EXISTING_PRINCIPAL_HSTAR_CC_POLYNOMIAL_IDENTITY_ONLY',rerun=False,full_Q2=False))
next_text='''[DERIVED — plano de cálculo dentro de A7.b; hipóteses de implementação ainda a testar]
# Próxima contração da bolha em posição — não é resultado já calculado

Usar metric_radial_bitensor_engine.py com suas2500comparações e angular_cubature/results.json.
Não somar um perfil completo aos E-insertions: estes já estarão nele, usar como controle de decomposição.

Representação proposta: cada perna interna tem índice (d,a), d=-1 semderivada ou0..3 comuma, a=0..9 fibra.
Vértice Gamma-Gamma tem no máximo uma derivada em cada campo. Formar matrizes50x50 W_A(d1a,d2b).
Separar N_X=1 (derivada no campo externo) e N_X=2 (externo semderivada); W00=0.
Extrair usando eh_cubic_16k(A,p,Ea,q,Eb,r), SEM impor r=-p-q até a integração por partes.
Termos q_i e r_j são W_i0,W_0j; termos q_i r_j são W_ij. Verificar Bose entrepernas.

Escolher A noquadro radial emX, B emY=0, fases externas exp(-ipX),exp(+ipY).
Na covderivada deA entra p_X=-p-K(zI-xx)p/6 e ainda -i*A_i^rep A no numerador de momento.
O termo geométrico deconexão externo é linear emx; pré-computar porquatrodireções. GaugefixingC_glinear nãoacrescentaV3.
Gbig(d,a;e,b)=nabla_Xd nabla_Ye H_ab (d/e=-1 omitidos), matriz50x50.
Condição decontração a testar explicitamente por4índices: frobenius(G.T W_X G,W_Y), mantendo posições das pontas.

Fatores: substituir cada momento interno por -i*nabla. Para N=N_X+N_Y,
parte plana usa Taylorj=N, coef(-1)^N*(p.x)^N/N!;
primeiraK dos propagadores evolume usa j=N-2, coef(-1)^(N-1)*(p.x)^(N-2)/(N-2)!;
correçãop_X de coframe tambémj=N-2;
conexão externa (-i extra) usa j=N-1, coef(-1)^N*(p.x)^(N-1)/(N-1)!.
Incluirmedida sqrt(g_X)=1-Kz/2. Normalização prevista rawbubble/A0 =angularmean/16.
ESSAS REGRAS SÃO CANDIDATAS: validarprimeiro todo coeficienteplano contra metric_bubble_v2 antes da curva.

Na primeiraK, graus angulares previstos<=6; no plano<=8. Provar/medir cota antes de cubatura.
Em nó inteirov, z=v², todos termos da expressão com Taylor têm grau-4: avaliar e multiplicarz²;
isso dá ovalor na esfera semraízes. ManterL simbólico; coeficientes deL podem produzirpólosmaiores,
não descartar antes de verificar sua soma angular e a prescrição deextensão.
Se usararrays inteiros, G0 denominadorcomum2z³ eG1semL denominador24z²; conferirconversões.

Um perfil emquadrosradiais nãoé automaticamente umaHessiana covariante integrada.
Converter/apurar adjuntos e divergências, eventualmente usando o caso ghost jápago como controle;
não escolher4coeficientes porWard=0. A fontecurva produzresíduo não nulo jámedido.
Correções deordemK², partefinita/estado/cutoff continuamdevidas depois.
'''
save(H/'metric_radial_bitensor_v2/PROXIMO_CALCULO.md',next_text)
ledger=O/'LEDGER_016.jsonl';raw=ledger.read_bytes()
events=[dict(event='A7_ENDOMORPHISM_INSERTIONS_AND_RADIAL_BITENSORS',at=now,provider='local',target='A-7.b',
    checks=r['checks']+b['checks']+c['checks'],cpu_seconds=r['cpu_seconds']+b['cpu_seconds']+c['cpu_seconds'],
    report_sha256=sha(rp),new_external_execution=False,full_Q2=False),
    dict(event='A7_KIMI_MARKED_IDENTITY_LOCAL_COTEJO',at=now,provider='local',target='A-7.b',
         report_sha256=sha(ap),job_id='7af2e0e2-f377-4d51-87d3-db09350b51e4',new_external_execution=False,full_Q2=False)]
for e in events:
    if e['event'].encode() not in raw:raw+=(json.dumps(e,ensure_ascii=False)+'\n').encode()
save(ledger,raw)
rows=[json.loads(t) for t in ledger.read_text('utf-8-sig').splitlines() if t.strip()];parents={}
def root(k):
    parents.setdefault(k,k)
    if parents[k]!=k:parents[k]=root(parents[k])
    return parents[k]
def ids(r):return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
for e in rows:
    ix=ids(e)
    for k in ix[1:]:parents[root(k)]=root(ix[0])
known={}
for e in rows:
    ix=ids(e);v=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    if ix and v is not None:known[root(ix[0])]=Decimal(str(v))
cost=sum(known.values(),Decimal(0))
save(H/'metric_endomorphism_bubble/COST_SNAPSHOT.json',dict(at=now,total_known_partial=str(cost),
    ledger_sha256=sha(ledger),unknown_cost_not_zero=True,billing_not_verified=True))
rels=['metric_endomorphism_bubble_check.py','metric_endomorphism_bubble_run.log',
 'metric_endomorphism_bubble/PRE_REGISTER.json','metric_endomorphism_bubble/results.json',
 'metric_endomorphism_bubble/DERIVACAO.md','metric_endomorphism_bubble/COST_SNAPSHOT.json',
 'metric_radial_bitensor_engine.py','metric_radial_bitensor_check.py','metric_radial_bitensor_run.log',
 'metric_radial_bitensor/PRE_REGISTER.json','metric_radial_bitensor_check_v2.py','metric_radial_bitensor_v2_run.log',
 'metric_radial_bitensor_v2/PRE_REGISTER.json','metric_radial_bitensor_v2/results.json',
 'metric_radial_bitensor_v2/PROXIMO_CALCULO.md','angular_cubature_check.py','angular_cubature_run.log',
 'angular_cubature/PRE_REGISTER.json','angular_cubature/results.json','capture_review_transition.py',
 'receive_kimi_marked_identity.py','received_reviews/marked_identity_local_cotejo.json',
 'received_reviews/7af2e0e2-f377-4d51-87d3-db09350b51e4.md',
 'received_reviews/7af2e0e2-f377-4d51-87d3-db09350b51e4.json',
 'received_reviews/A7_transition_after_mimo_log_failure.json']
files=[H/x for x in rels]+[Path(__file__),rp,ap]
manifest=H/'metric_endomorphism_bubble/delivery_manifest.json'
save(manifest,dict(at=now,opening_sha256=opening,artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',
    completed_this_turn=['E insertions in three metric bubble pieces179checks',
        'First-curvature bitensor jets2500componentchecks; degree8 spherical cubature495moments',
        'Kimi marked identity result recovered and dependencies verified without rerun',
        'MiMo log review IncompleteRead confirmed failed; no retry'],
    metric_endomorphism_manifest=str(manifest),
    position_bubble_plan=str(H/'metric_radial_bitensor_v2/PROXIMO_CALCULO.md'),
    latest_orchestration=dict(at=now,source='Official message then read-only Coordination API',registered=5,staging=8,
        last_completed='Kimi marked_tensor_identity',next='MiMo marked_wick_audit; worker owns transitions'),
    pending_orchestration='5 registered/8staging at coordinator snapshot before marked result readiness',
    latest_live_execution=dict(job_id='7af2e0e2-f377-4d51-87d3-db09350b51e4',
        execution_id='f3df9557-6545-488f-9372-404a709a3aeb',status='result_ready',observed_utc='2026-09-25T03:47:42.363678+00:00'),
    next=['Full position-space metric bubble using checked radial jets; follow PROXIMO_CALCULO and first validate flat normalization',
          'Do not double-count E-insertion subset when using full parametrix; K²/full finite causal sum stillopen',
          'A7.c onlyafter24h; A7.d,A8,PartB and finalaudit remain'],
    previous_turn_failure='Bitensorcheckv1 forgot z=x² in verification; v2 only enforces declared radial relation')
save(cont,d)
progress=O/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: E-inserções179checks;bitensores2500;cubatura495. CPU{events[0]["cpu_seconds"]}s. Kimi h*cc recebido/cotejado;MiMo log failed semretry. Custo parcialUS${cost},desconhecidosnãozero. Q2OPEN. Abertura{opening};ledger{sha(ledger)}.\n'.encode())
for item in data('metric_endomorphism_bubble/delivery_manifest.json')['artifacts']:assert sha(Path(item['path']))==item['sha256']
print(json.dumps(dict(report=str(rp),audit=str(ap),verified_artifacts=len(files),cost_partial=str(cost))))
