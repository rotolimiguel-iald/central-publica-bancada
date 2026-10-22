"""Record the finite marked contact, its combination and preserved failed attempts."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid
HERE=Path(__file__).resolve().parent;CHAT=HERE.parents[1];OUT=CHAT/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,b):
    if isinstance(b,str):b=b.encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        bk.write_bytes(old);assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert b and t.read_bytes()==b;t.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
r=json.loads((HERE/'finite_antifield_contact_v3/results.json').read_bytes())
v=json.loads((HERE/'finite_hc_independent/results.json').read_bytes())
report=f'''[DERIVED — contato finito marcado e exatidão principal hc; REAL — CAS; OPEN — causal completo]
# A7.b — combinar a fonte h* c com a Hessiana
Abertura SHA256 `{opening}`. UTC {now}.

Mantida a extensão de um par R=FP[(1-a)mu^(2a)z^a·], com mu fixo.
O numerador marcado já medido, sem seu fator global, é

    R0(q)v=-3q² K_q(v)/8 + q⊗q(q·v)/2 = K_q F(q)v.

Chamando q de símbolo formal das derivadas do delta, o mesmo cálculo de
resíduos da entrega precedente dá agora, para P3 cúbico,

    N3[P3]=-13P3/48-q² Lap_q(P3)/64,
    R(P3(partial)U2)-P3(partial)R(U2)=C N3[P3](partial)delta.

As derivadas radiais abertas precisam dos fatores métricos de partial_i z.
Após a correção registrada abaixo, as duas assinaturas dão

    N3[R0]v=(5/32)q²K_q(v)-(13/96)q⊗q(q·v)
                         -(1/64)q²g(q·v).

A parcela de traço é nova e não é gauge pura. Com o símbolo físico NÃO
gauge-fixado E(q)H=q²ItrH-Itr K C(H), usado nas entregas anteriores,

    E(q)N3[R0]v=-(1/32)q²(q·v)(q⊗q-q²g).

É importante manter E; substituir pela Hessiana gauge-fixada destrói essa
identificação. O fator4kappa e sinais/fases de Fourier completos ainda não
foram fixados na comparação causal. Por isso lambda abaixo registra esse
fator RELATIVO; ele não foi ajustado nem identificado como parâmetro físico.

**Combinação explícita.** Retirados C e o fator global comum, a quebra local
do setor principal hc, a partir das duas extensões uniformes, é

    W_lambda(T,v)=(187/1920)q4(Tq·v)
       +(43/960+lambda/32)q4 trT(q·v)
       +(-7/40-lambda/32)q²(qTq)(q·v).

Ela não se anula por uma escolha de lambda. Um controle particularmente
direto toma q=v=e0 e T=K_q(e0): W=-21/320, e a contribuição marcada é
zero por E K=0. Esse é um contato finito de normalização, não uma nova
obstrução cohomológica inferida desse número.

Subtrair os DOIS contatos calculados, N4[P] da Hessiana e N3[R0] da fonte,
leva às extensões diferenciais P(partial)R(U2) e R0(partial)R(U2).
Nelas as duas parcelas se anulam separadamente pela transversalidade e
E K=0. A restauração desse setor vale para qualquer fator relativo constante;
isso não dispensa fixá-lo para determinar a amplitude física original.

**Forma BV e WZ no recorte.** No modelo livre principal, use
hat_h^ddagger=h^ddagger+C*barc, com s0hat_h^ddagger=Hh e s0c=0.
O polinômio local que codifica as diferenças é da forma

    B = (1/2)<h,N4 h> + lambda'<hat_h^ddagger,N3 c>,

com os fatores globais recolocados em lambda' e no primeiro termo.
Ele tem ghost0, e sua variação contém a combinação hc obtida. A parcela
com antighost em hat_h^ddagger deve ser conservada para cancelar os termos
com b; não é um novo laço. Assim a quebra PRINCIPAL aqui reconstruída é
s0-exata, módulo integrações por partes, nessa classe local de símbolos.
Pode-se escolher a densidade simetrizada s0B, que é fechada por s0²=0.
Ao recolocar cutoffs, as integrações por partes trazem derivadas de chi;
esta entrega vale na região chi constante, sem declarar tais termos zero.

Uma checagem explícita da consistência integrada: a matriz de dois ghosts
K(-q)^T N4(q)K(q) é simétrica sob (i,q)↔(j,-q), logo sua contração com
c_i(-q)c_j(q) é nula por Grassmann. O número duplo-gauge -21/320 não
contradiz WZ: esta usa a antissimetria dos ghosts, não a nulidade de cada
entrada da matriz. A contribuição marcada anula por E K=0.

**Evidência e limites.** v3:138identidades exatas nas duas assinaturas,
quatro controles descritos,rc0,CPU{r['cpu_seconds']}s. Auditoria independente
por momentos esféricos/Taylor, incluindo o sinal ÍMPAR do jato de teste:
36checks,3negativos,rc0,CPU{v['cpu_seconds']}s. Fontes e logs nos manifestos.
Não foi provada admissibilidade de toda uma hierarquia de normalização,
realidade da amplitude Lorentziana com suas fases, Ward não linear completa,
curvatura ou equivalência ao par físico. Q2 completa continua aberta.
Nenhuma mudança em kernel,um.py ou gate; nenhuma nova execução remota.
'''
rp=HERE/'finite_antifield_contact_v3/DERIVACAO_HC_FINITA.md';save(rp,report)
save(OUT/'ENTREGA_016_A7b_contato_finito_hc.md',report)
save(OUT/'ENTREGA_016_MEDIDA_contato_cubico_tipos_e_metrica.md',f'''[REAL — duas falhas locais distintas, preservadas e diagnosticadas]
Abertura SHA256 `{opening}`.
v1, comando symbolic_runtime/Scripts/python.exe -X utf8 -B A7/finite_antifield_contact_check.py,
rc1: bool*Symbol recusado pelo Sympy. LogSHA256 `{sha(HERE/'finite_antifield_contact_run.log')}`.
v2 substituiu deltas booleanos por inteiros. Passou a parte euclidiana e
falhou no teste Lorentziano: faltavam g_ii g_jj g_kk e g_ww dos numeradores
de derivadas de z. Não era falha da identidade física nem licença para
eliminar o controle Lorentziano. LogSHA256 `{sha(HERE/'finite_antifield_contact_v2_run.log')}`.
v3 restaura esses fatores, sem mudar a fórmula alvo/coeficientes de entrada;
rc0,138checks,CPU{r['cpu_seconds']}s. LogSHA256 `{sha(HERE/'finite_antifield_contact_v3_run.log')}`.
Cada tentativa tem script/preregistro próprio. Próximo passo: contatos
com cutoff/curvatura e hierarquia causal. Zero novas chamadas de modelos.
''')
for folder,script,log in [('finite_antifield_contact_v3','finite_antifield_contact_check_v3.py','finite_antifield_contact_v3_run.log'),
                         ('finite_hc_independent','finite_hc_independent_audit.py','finite_hc_independent_run.log')]:
    files=[HERE/script,HERE/log,HERE/folder/'PRE_REGISTER.json',HERE/folder/'results.json',rp,
        HERE/'antifield_vertex/results.json',HERE/'finite_principal_contact/results.json',
        HERE/'finite_antifield_contact_check.py',HERE/'finite_antifield_contact_run.log',
        HERE/'finite_antifield_contact_check_v2.py',HERE/'finite_antifield_contact_v2_run.log']
    save(HERE/folder/'manifest.json',json.dumps(dict(at=now,opening_sha256=opening,
        artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]),ensure_ascii=False,indent=2))
cpu=r['cpu_seconds']+v['cpu_seconds'];ledger=OUT/'LEDGER_016.jsonl'
events=[dict(event='A7_FINITE_HC_CONTACT_AND_GRADED_CONSISTENCY',at=now,provider='local',target='A-7.b',
    checks=138,independent_checks=36,cpu_seconds=cpu,report_sha256=sha(rp),full_Q2=False)]
j='04dae5a6-b78a-4f0f-83c7-4cb1b6c3c0be';rec=json.loads((HERE/'received_reviews'/(j+'.json')).read_bytes())
if ('A7_KIMI_INCIDENCE_RECEIVED_'+j).encode() not in ledger.read_bytes():
    events.append(dict(event='A7_KIMI_INCIDENCE_RECEIVED_'+j,at=now,provider='kimi',target='A-7.b',
        job_id=j,request_id=rec['request_id'],execution_id=rec['execution_id'],
        prompt_sha256=rec['prompt_sha256'],response_sha256=rec['response_sha256'],
        usage=rec['result_metadata'].get('usage'),cost_estimate_usd=rec['result_metadata'].get('cost_estimate_usd'),
        new_external_execution=False,status='DECLARADO_READ_PENDING_LOCAL_TEST'))
save(ledger,ledger.read_bytes()+''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events).encode())
cont=HERE/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,previous_goal_turn='PROGRESS',status='ACTIVE',
    completed_this_turn=['Rank3 finite contact and principal hc combination computed',
        '138 checks and independent angular/graded audit36 checks',
        'Kimi incidence recovered and read; specific code defects await minimal tests'],
    finite_hc_manifest=str(HERE/'finite_antifield_contact_v3/manifest.json'),
    finite_hc_independent_manifest=str(HERE/'finite_hc_independent/manifest.json'),
    next=['Audit incidence code using minimal counterexamples before full enumeration',
          'Fix physical relative factors and continue cutoff/curved/multilinear finite causal prescription',
          'Consume pending independent reviews without repeats'])
save(cont,json.dumps(d,ensure_ascii=False,indent=2))
progress=OUT/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: contato cúbico/fonte e combinação hc finita simbólica,138+36checks;CPU{cpu}s,2falhas locais preservadas. Subtração s0-exata no principal, Q2completaOPEN. Kimi incidência recebido para revisão. Abertura{opening}.\n'.encode())
print(json.dumps(dict(report=str(rp),cpu_seconds=cpu,status='ACTIVE_PROGRESS'),ensure_ascii=False))
