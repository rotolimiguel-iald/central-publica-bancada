"""Record reviewed provider claims and the resulting local derivations."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
HERE=Path(__file__).resolve().parent;CHAT=HERE.parents[1];OUT=CHAT/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,b):
    if isinstance(b,str):b=b.encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:f.write(b)
    assert b and t.read_bytes()==b;t.replace(p)
def fresh(p,o):assert not p.exists();save(p,json.dumps(o,ensure_ascii=False,indent=2))
now=datetime.now(timezone.utc).isoformat();opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
des=json.loads((HERE/'natural_density_descent/results.json').read_bytes())
temp=json.loads((HERE/'temporal_proposal_audit_v2/results.json').read_bytes())
curv=json.loads((HERE/'curved_primitive_mass/results.json').read_bytes())
real=json.loads((HERE/'bv_reality/results.json').read_bytes())
source=CHAT/'CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md'
report=f'''[DERIVED — descida de densidade natural; REAL — CAS e revisão do Kimi; OPEN — anomalia causal]
# A7.b — o grau correto de A_I e seu levantamento

Abertura SHA256 `{opening}`. UTC {now}.

O parecer Kimi cohomology_to_anomaly atribui A_I ao bidegrau(4,4). A fonte087
define A_I=rho_I c0c1c2c3 e diz expressamente que é ESCALAR: os quatro dx
foram substituídos por ghosts. Portanto seu bidegrau é(4,0), total4. Não é a
quatro-forma Omega_I=rho_I dx0dx1dx2dx3, que tem grau(0,4).
FonteSHA256 `{sha(source)}`. Não reaplicamos a prova de não exatidão da087.

Com d_r de grau(1-r,r), as fontes que podem chegar a(1,4) são(r,4-r):
(1,3),(2,2),(3,1),(4,0). Têm total4. As fontes propostas pelo Kimi,
(1+r,4-r), chegam a(2,4). Em particular d4:(4,0)->(1,4) NÃO é excluído
por grau. O argumento de isolamento do parecer é inválido. Estar no topo
de forma também não excluiria setas entrantes nem provaria sobrevivência.

O cálculo correto usa a naturalidade já demonstrada na fonte:

    s rho=c^mu partial_mu rho+(partial_mu c^mu)rho,
    sc^mu=c^nu partial_nu c^mu.

Na graduação TOTAL, c e dx são ímpares e anticomutam. Ponha eta=c+dx,
D=s+d. Então Deta^mu=eta^nu partial_nu c^mu e
D rho=eta^nu partial_nu rho+(div c)rho. Para P=eta0eta1eta2eta3,
o Leibniz ímpar dá DP=-P div c. O termo eta^nu(partial_nu rho)P é zero
porque repete um dos quatro geradores eta. Logo

    Omega=rho product_mu(c^mu+dx^mu),   D Omega=0.

Escrevendo Omega=Σ omega_q, temos s omega_q+d omega_(q-1)=0, q=0,...,4;
omega0=A_I, omega4=Omega_I. Esse levantamento explícito mata os diferenciais
SAINTES dessa classe por formas, incluindo d4, desde que usados no mesmo
complexo local. Não é uma declaração de anomalia zero. Conjugação074 pode
transportar o cociclo ao Q_N quando suas hipóteses de domínio forem mantidas;
o CAS aqui calcula D=s+d, não apaga C_N no complexo conjugado.

Há ainda um detector direto: se Omega=D Psi, sua componente de forma zero
seria A_I=s Psi0. Assim, CONDICIONALMENTE à não exatidão de A_I na087 e à
mesma classe de coeficientes, Omega não é D-exata. A inferência vale sobre
constantes reais; extensão ao anel Rher exige que os coeficientes sejam
inertes também para d, não só para s. Não produz H5 nulo nem exaustão de H4.

CAS exterior exato:12checks+2negativos, rc0,CPU{des['cpu_seconds']}s. Os
negativos omitem div c ou trocam c+dx por c-dx. A conta usa apenas a lei
de densidade natural, sem fixar os coeficientes da densidade de anomalia.
A crítica do Kimi que página CE não decide o BRST completo continua útil;
o detector por projeção continua condicional. Finitos jatos por coeficiente
não fornecem, por si, uma cota uniforme para procurar todas as primitivas.
Nenhum original, kernel ou gate foi alterado.
'''
rp=HERE/'natural_density_descent/DERIVACAO_E_REVISAO.md';save(rp,report)
save(OUT/'ENTREGA_016_A7b_descida_da_densidade_natural.md',report)
temporal=f'''[REAL — revisão local da proposta temporal; OPEN — prescrição causal completa]
# PM087 recebida do Kimi não está pronta para congelamento
Abertura SHA256 `{opening}`. UTC {now}.

O parecer foi lido integralmente e cotejado com suas fontes. O fundo da069
a=2cos(r/2), phi=id, não pode ser chamado de deSitter de raio2 para então
apagar phi. Para FLRW Lorentziano com fatias S3 unitárias, igualdade das
curvaturas seccionais exige a a''-(a')²-1=0. O perfil cos dá-2; o controle
cosh dá0. A inversão global da convenção de Riemann não muda essa desigualdade.
Não substituímos o horizonte: o teste087 continua o espaço-forma abstratoK>0.

A proposta confunde grau superficial omega com scaling degree sd. Em um
ciclo a um laço com n vértices de até2 derivadas, sd<=4n e dimensão relativa
4(n-1), portanto omega<=4, não4-4(n-1). Derivadas externas reduzem a cota
correspondente; inserções marcadas conservam sua própria contagem.
Não segue extensão única para n>=3. Contraexemplo crítico em aridade3:
|x|^-8 em R8 tem sd8; uma extensão pode mudar por c delta8. A integral radial
é logarítmica. A cota superficial também não diz quantos tensores locais existem.

Outras lacunas documentais: falta barc no multiplet, embora b tenha sido
incluído e chamado minimal; sqrt(kappa) altera nossa normalização e não é
real para todo kappa real não nulo permitido; Emax2 não segue de BV minimal;
mu, parametrix e hierarquia dos coeficientes finitos não foram efetivamente
fixados. A filtração quântica já medida permanece, sem reabrir truncamento falso.

CASv2:10checks,3afirmações rejeitadas,rc0,CPU{temp['cpu_seconds']}s. A v1
falhou ao comparar uma expressão trigonométrica não normalizada: simplificar
deu -4cos(r/2)^2/(cos r+1); trigsimp(expand_trig(expand(...))) dá-2.
Não era contraexemplo físico. V1, preregistro e traceback preservados; v2
somente fixa essa normalização simbólica, sem mudar o alvo. Nenhuma nova
chamada de modelo. Relatar lista de escolhas faltantes não congela PM087.
'''
tp=HERE/'temporal_proposal_audit_v2/REVISAO.md';save(tp,temporal)
save(OUT/'ENTREGA_016_A7b_revisao_prescricao_Kimi.md',temporal)
physical=f'''[DERIVED — realidade e parcela algébrica de curvatura da primitiva; REAL — CAS; OPEN — laços curvos/normalização causal]
# A7.b — conservar realidade e explicitar o termo inferior em K
Abertura SHA256 `{opening}`. UTC {now}.

O dicionário069 fixa h*=h,c*=c,b*=b,barc*=-barc para conjugação (não confundir
este * com o rótulo de antifield). Uma extensão compatível é

    (phi^ddagger)*=-epsilon_phi phi^ddagger,
    (sF)*=(-1)^paridade(F) s(F*),   phi*=epsilon_phi phi.

O star é antilinear e reverte os produtos. A identidade confere nos oito
geradores livres e estende-se aos produtos pelo Leibniz graduado. sc=c partial c
também a satisfaz. Assim h^ddagger,b^ddagger,c^ddagger são anti-reais e
barc^ddagger real; a ação BV escrita na069 permanece real. A combinação
u=4kappa(h^ddagger+C*barc) é anti-real para qualquer kappa real não nulo.

Os monômios de gerador A2,Z,u B c nabla u e u D1(nabla c)u, com coeficientes
reais, são ímpares e anti-reais. Portanto seu sF é real. Não se deve acrescentar
um i para 'tornar F real': isso tornaria sF não real. Os fatores i de Fourier
dos vértices são restaurados separadamente, como antes. Teste:20checks,
3negativos,rc0. É uma extensão explícita de convenção, não prova de toda a
hierarquia causal ou de um gerador não linear ainda não comparado aos laços.

Dos operadores livres já conferidos e C*=-Itr K_gauge/2 segue

    E=4kappa H= -box Itr + Itr K_gauge C +2K id+K g trace.

H é físico ANTES de eliminar b. Mantemos essa ORDEM de derivadas, sem
comutá-las silenciosamente. Escreva M(H)=2KH+Kg trH. Então
B(M)=-K(H/3+2g trH/3) e
D1(M;r,v)=K[sym(r,Hv)-sym(v_flat,H r_sharp)]. A contribuição algébrica dessa
curvatura à candidata marcada, retirado4iκA0, é

    -K{{ [(p+r/2)·v](H/3+2g trH/3)
         +[sym(r,Hv)-sym(v_flat,H r_sharp)]/3 }}.

A compatibilidade métrica e K constante justificam B paralelo. A mesma
identidade foi conferida nas fibras euclidiana e Lorentziana(+---):260checks,
80polarizações não nulas,4negativos. Não é cálculo do laço curvo. Os termos
gerados ao reordenar derivadas covariantes e os termos finitos permanecem
separados. A identidade covariante da parcela B continua

    delta Psi_B + (1/2)nabla_mu J^mu
      = u B[c.nabla E+(div c)E/2], J^mu=u B c^mu E.

Com cutoff chi, integral chi deltaPsi_B tem ainda
+(1/2)integral(nabla_mu chi)J^mu. A parcelaD1 não exige integração por partes
nessa representação. Os termos com antighost provenientes de u são conservados.
CPU realidade{real['cpu_seconds']}s;curvatura{curv['cpu_seconds']}s.
O lado da primitiva fica mais determinado; sua igualdade ao coeficiente causal
real, s1F e a hierarquia multilinear ainda não foram demonstrados.
'''
pp=HERE/'curved_primitive_mass/DERIVACAO_REALIDADE_E_CURVATURA.md';save(pp,physical)
save(OUT/'ENTREGA_016_A7b_realidade_e_curvatura_da_primitiva.md',physical)
items=[('natural_density_descent','natural_density_descent_check.py','natural_density_descent_run.log',rp),
       ('temporal_proposal_audit_v2','temporal_proposal_audit_v2.py','temporal_proposal_audit_v2_run.log',tp),
       ('bv_reality','bv_reality_check.py','bv_reality_run.log',pp),
       ('curved_primitive_mass','curved_primitive_mass_check.py','curved_primitive_mass_run.log',pp)]
for folder,script,log,note in items:
    files=[HERE/script,HERE/log,HERE/folder/'PRE_REGISTER.json',HERE/folder/'results.json',note,source,
           HERE/'received_reviews/ba337b71-5345-44e7-8481-04a24ba1569e.md',
           HERE/'received_reviews/1cb94397-825d-4005-8dc1-933481d302c0.md']
    if folder=='temporal_proposal_audit_v2':files += [HERE/'temporal_proposal_audit.py',HERE/'temporal_proposal_audit_run.log',HERE/'temporal_proposal_audit/PRE_REGISTER.json']
    fresh(HERE/folder/'manifest.json',dict(at=now,opening_sha256=opening,
          artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
save(OUT/'ENTREGA_016_MEDIDA_normalizacao_trigonometrica.md',f'''[REAL — falha de normalização simbólica preservada]
Abertura SHA256 `{opening}`.
Comando A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/temporal_proposal_audit.py.
O subprocesso Python terminou por AssertionError; o shell da primeira chamada
retornou0 porque o Get-Content subsequente terminou normalmente. Não é rc0 do teste.
LogSHA256{sha(HERE/'temporal_proposal_audit_run.log')}; scriptSHA256{sha(HERE/'temporal_proposal_audit.py')}.
Causa e correção: simplificação comum deixou -4cos(r/2)^2/(cos r+1); expand/trigsimp
reduz a-2. Próximo passo executado em temporal_proposal_audit_v2.py com rcPython
propagado explicitamente pelo shell:0;10checks,CPU{temp['cpu_seconds']}s.
V1 preservada; zero chamada remota. Não confundir essa falha CAS com uma física nova.
''')
ledger=OUT/'LEDGER_016.jsonl';cpu=sum(x['cpu_seconds'] for x in [des,temp,curv,real])
event=dict(event='A7_DENSITY_DESCENT_REALITY_CURVATURE_AND_KIMI_REVIEW',at=now,provider='local',target='A-7.b',
    descent_checks=12,descent_negatives=2,temporal_checks=10,curvature_checks=260,reality_checks=20,
    cpu_seconds=cpu,report_sha256=sha(rp),full_Q2=False,gate_changed=False)
save(ledger,ledger.read_bytes()+(json.dumps(event,ensure_ascii=False)+'\n').encode())
costs={}
for ln in ledger.read_text('utf-8-sig').splitlines():
    if not ln.strip():continue
    e=json.loads(ln);v=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    k=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
    if k and v is not None:costs[k]=Decimal(str(v))
total=str(sum(costs.values(),Decimal(0)))
cont=HERE/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',
    completed_this_turn=['Kimi temporal reviewed: scaling and geometry errors measured; PM087 not frozen',
      'Kimi cohomology corrected: A_I is(4,0); natural density explicit total-degree4 descent derived and checked',
      'Reality extension verified20checks/3negative; curvature mass contribution260checks in two signatures'],
    density_descent_manifest=str(HERE/'natural_density_descent/manifest.json'),
    reality_manifest=str(HERE/'bv_reality/manifest.json'),curvature_mass_manifest=str(HERE/'curved_primitive_mass/manifest.json'),
    temporal_review_manifest=str(HERE/'temporal_proposal_audit_v2/manifest.json'),
    next=['Prescribe complete causal extensions/finite hierarchy within A7b; logUV is not that prescription',
          'Compare new curved-primitive contributions and nonlinear terms against actual loop data',
          'Review queued Kimi/MiMo/DeepSeek results without reruns'],partial_metered_cost_usd=total)
save(cont,json.dumps(d,ensure_ascii=False,indent=2))
progress=OUT/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: doisKimi revisados;A_I corrigido(4,0),descida12checks+2negativos;PM087 recusada com10checks;realidade20+3negativos;curvatura260+4negativos;CPU{cpu}s. Prescrição/Q2finitaOPEN. Custo externo parcialUS${total}. Abertura{opening}.\n'.encode())
print(json.dumps(dict(reports=[str(rp),str(tp),str(pp)],cpu_seconds=cpu,full_Q2=False),ensure_ascii=False))
