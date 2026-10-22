"""Deliver the local review and record the new previewed Kimi unit."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, uuid
HERE=Path(__file__).resolve().parent; CHAT=HERE.parents[1]; OUT=CHAT/'TUNEL/DO_CHATGPT'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,data):
    if isinstance(data,str): data=data.encode()
    if p.exists():
        old=p.read_bytes()
        if old==data:return
        bak=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        bak.write_bytes(old); assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(data); assert data and tmp.read_bytes()==data
    tmp.replace(p)
now=datetime.now(timezone.utc).isoformat()
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
receipt=json.loads((HERE/'received_reviews/187b509f-0a81-41e3-9f6a-835c870b525c.json').read_bytes())
result=json.loads((HERE/'sigma_restriction/results.json').read_bytes())
catalog=HERE/'orchestration_finite_contact/prepared_units.json'
unit=json.loads(catalog.read_bytes())[0]
report=f'''[DERIVED — quociente clássico por ideal diferencial; REAL — CAS e revisão MiMo; OPEN — prescrição causal]
# A7.b — sigma constante: restrição clássica não é integração quântica
Abertura SHA256 `{opening}`. UTC {now}.

Parecer MiMo job{receipt['job_id']}, execução{receipt['execution_id']}, lido
integralmente. A distinção entre projetar o setor sigma e integrar suas flutuações
é correta. A alegação adicional de que s agindo em h recebe EOM de xi é incorreta:
sg=Lie_c g; as equações de movimento entram em s dos ANTIFIELDS.

**Prova escrita no modelo fonte, antes de qualquer contração quântica.**
Use coordenadas de alvo xi próximas do valor constante phi0. Seja I o ideal
diferencial gerado por TODOS os jatos de xi e xi^ddagger. No sigma modelo sem
potencial/fonte linear, S_sigma é quadrático nas derivadas de xi, com métrica
do alvo suave. Assim E_xi pertence a I, e o tensor de energia também (na
verdade começa em grau dois em xi e seus jatos). Temos

    s xi=c^mu partial_mu xi ∈ I,
    s xi^ddagger=±E_xi + termos lineares em xi^ddagger e seus jatos ∈ I.

O sinal depende da convenção esquerda/direita do antibracket, irrelevante
para a pertença ao ideal. Como s comuta com o prolongamento por jatos e é
derivação, sI⊂I. Logo ele induz um diferencial no quociente clássico, e seu
quadrado é zero quando o s completo da fonte o é. Na restrição, a ação se
reduz a Einstein–Hilbert mais os acoplamentos BV métricos/ghosts; o termo
sigma na transformação do antifield métrico desaparece e o termo
xi^ddagger Lie_c xi no antifield ghost desaparece. O par não mínimo pode
ser mantido com a gauge de De Donder exclusivamente métrica aqui usada.

Não apagamos os antifields dos campos RETIDOS. O aviso da087, l.11, refere-se
justamente a esses antifields. A alegada tensão interna X4 do parecer não
decorre daquele aviso. Trata-se de QUOCIENTE DE COMPLEXOS, não de afirmar
que I é ideal de Poisson-BV: (xi,xi^ddagger)=1 impede esta última afirmação.
O antibracket do setor retido é definido separadamente sobre seus pares.

**Controle local e alcance.** O CAS usa a carta hemisférica de S3,
G_ij=delta_ij+xi_i xi_j/(1-|xi|²), dimensão espaço-temporal4 e densidade
métrica inversa A^mu nu arbitrária. Deriva Euler a partir da lagrangiana,
confere E_xi(0)=0, T(0)=0 e as três linearizações

    E_i,lin=-c_m[A^mu nu partial_mu partial_nu xi_i
                   +(partial_mu A^mu nu)partial_nu xi_i].

São19checks+2negativos, rc0, CPU{result['cpu_seconds']}s. Uma fonte J xi
destrói a restrição; apagar SOMENTE os antifields sigma, mantendo xi livre,
também não dá ideal estável. A prova de sI⊂I é o argumento escrito acima,
não uma conclusão universal produzida por esses testes finitos.

As três Hessianas de flutuação NÃO são zero. Portanto fixar o valor de
fundo não apaga os propagadores. Em produtos quânticos, xi(x)⋆xi(y) contém
ħG(x,y): não há transporte automático desse quociente clássico. Um
determinante não trivial também não implica quebra Ward; seria preciso
calcular sua variação na prescrição escolhida.

**Demais correções da revisão.** W5/X6 confundem o H4 do CE quadrático com
o H4 completo: a087 diz explicitamente que NÃO o exaure. R4/W6 transformam
a observação sobre contratermos de0/1/2pernas da072 numa cota universal;
esta não é estabelecida ali, e a filtração quântica já entregue permite
valências maiores. K/Lambda e os operadores da restrição estão em
model_inputs/DERIVACAO_OPERADORES.md; o parecer só recebeu excertos anteriores.
Não declarar novamente inexistente o que a bancada já construiu. O fundo
069 sigma=id continua distinto do espaço-forma087 sigma constante.

Nada aqui fixa a normalização causal completa, integra sigma, move gate ou
modifica um.py. Recuperação da resposta fez zero chamadas novas a provedores.
Uso informado:331360entrada+34313saída=365673tokens; custo estimadoUS$0.17399391.
'''
rp=HERE/'sigma_restriction/REVISAO_MIMO_E_IDEAL_CLASSICO.md'
save(rp,report);save(OUT/'ENTREGA_016_A7b_revisao_MiMo_sigma.md',report)
files=[HERE/'sigma_restriction_check.py',HERE/'sigma_restriction_run.log',
    HERE/'sigma_restriction/PRE_REGISTER.json',HERE/'sigma_restriction/results.json',rp,
    HERE/'received_reviews/187b509f-0a81-41e3-9f6a-835c870b525c.md',
    HERE/'received_reviews/187b509f-0a81-41e3-9f6a-835c870b525c.json',
    HERE/'model_inputs/DERIVACAO_OPERADORES.md',HERE/'quantum_filtration/DERIVACAO_FILTRACAO.md',
    CHAT/'CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md',
    CHAT/'COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md',
    CHAT/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md']
manifest=dict(at=now,opening_sha256=opening,artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files])
save(HERE/'sigma_restriction/manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))
save(OUT/'ENTREGA_016_A7_orquestracao_contato_finito.md',f'''[REAL — unidade preparada e rota conferida; OPEN — execução e resposta]
Abertura SHA256 `{opening}`. UTC {now}.
Kimi request{unit['request_id']}: contato Ward/Slavnov finito de dois campos
sob extensão de um par já fixada. Catálogo `{catalog}`, SHA256 `{sha(catalog)}`.
Prévia selected=kimi;{unit['prompt_chars']} caracteres; fontes com hashes e
linhas. Encaminhada pela ferramenta oficial à coordenação para staging APÓS
orchestration_completion. Uma chamada por unidade; nenhuma execução por esta
bancada, nenhuma mudança de fila/capacidade, sem anunciar resultado pronto.
Preparador v1 parou no limite local antes de UUID/submissão,24851>24000.
V2 projetou a fonte linear nas linhas1–29 e passou. Sem perda no original.
''')
save(OUT/'ENTREGA_016_MEDIDA_preparo_contato_finito_contexto.md',f'''[REAL — limite local de preparação]
Abertura SHA256 `{opening}`.
Comando: C:/Python314/python.exe -X utf8 -B A7/prepare_finite_contact_review.py.
rc1: AssertionError24851 no assert len(prompt)<=24000, ANTES de UUID/payload.
Não houve stdout independente salvo; evidência é o retorno da ferramenta na
sessão. Script preservado SHA256 `{sha(HERE/'prepare_finite_contact_review.py')}`.
V2 SHA256 `{sha(HERE/'prepare_finite_contact_review_v2.py')}` limita uma fonte
a1–29 e preserva hash do arquivo inteiro/linhas citadas. rc0 e selected=kimi.
Zero chamadas remotas em ambas preparações; próxima etapa é worker existente.
''')
ledger=OUT/'LEDGER_016.jsonl'; old=ledger.read_bytes()
marker='A7_MIMO_MODEL_INPUT_RECEIVED_AND_REVIEWED'
assert marker.encode() not in old
meta=receipt['result_metadata']
events=[dict(event=marker,at=now,provider='mimo',target='A-7.b',
    job_id=receipt['job_id'],execution_id=receipt['execution_id'],request_id=receipt['request_id'],
    prompt_sha256=receipt['prompt_sha256'],response_sha256=receipt['response_sha256'],
    usage=meta.get('usage'),cost_estimate_usd=meta.get('cost_estimate_usd'),
    new_external_execution=False,review_sha256=sha(rp)),
    dict(event='A7_CLASSICAL_SIGMA_IDEAL_CAS',at=now,provider='local',target='A-7.b',
        checks=19,negatives=2,cpu_seconds=result['cpu_seconds'],report_sha256=sha(rp)),
    dict(event='A7_KIMI_FINITE_CONTACT_PREVIEW_AND_DISPATCH',at=now,provider='kimi',
        request_id=unit['request_id'],target='A-7.b',catalog_sha256=sha(catalog),
        status='PREVIEWED_SENT_TO_COORDINATOR',new_external_execution=False)]
save(ledger,old+''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in events).encode())
costs={}
for line in ledger.read_text('utf-8-sig').splitlines():
    if not line.strip():continue
    e=json.loads(line);v=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    key=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
    if key and v is not None:costs[key]=Decimal(str(v))
total=str(sum(costs.values(),Decimal(0)))
cont=HERE/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,previous_goal_turn='PROGRESS',status='ACTIVE',partial_metered_cost_usd=total,
    sigma_restriction_manifest=str(HERE/'sigma_restriction/manifest.json'),
    recovered_mimo_review=receipt['job_id'],finite_contact_catalog=str(catalog))
d['completed_this_turn']=['MiMo model-input audit reviewed; classical differential ideal proved in stated sigma model',
    '19 exact local Euler/Hessian checks and2 negative controls',
    'New Kimi finite-contact unit previewed and sent to coordinator, execution pending']
save(cont,json.dumps(d,ensure_ascii=False,indent=2))
progress=OUT/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: MiMo revisto, ideal diferencial sigma clássico,19checks+2negativos,CPU{result["cpu_seconds"]}s;novo Kimi contato finito preparado. Q2completaOPEN. Custo externo parcialUS${total},desconhecidos preservados. Abertura{opening}.\n'.encode())
print(json.dumps(dict(review=str(rp),checks=19,partial_metered_cost_usd=total,new_request=unit['request_id']),ensure_ascii=False))
