"""Record the measured DeepSeek review without changing the theory's sources."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
HERE=Path(__file__).resolve().parent;CHAT=HERE.parents[1];OUT=CHAT/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,data):
    if isinstance(data,str):data=data.encode()
    if p.exists():
        old=p.read_bytes()
        if old==data:return
        bak=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        bak.write_bytes(old);assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(data)
    assert data and t.read_bytes()==data;t.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
job='b6d4bbc6-7bd5-4f73-ae34-4f5738376b06'
receipt=json.loads((HERE/'received_reviews'/(job+'.json')).read_bytes())
result=json.loads((HERE/'odd_bracket_review/results.json').read_bytes())
report=f'''[DERIVED — consistência WZ com convenções explícitas; REAL — contraexemplos CAS; OPEN — coeficiente causal]
# A7.b — revisão dos sinais do parecer DeepSeek
Abertura SHA256 `{opening}`. UTC {now}.
Resposta job{job}, execução{receipt['execution_id']}, lida integralmente.

**1. O bracket é ímpar.** Para paridades de Grassmann epsilon,

    (F,G)=-(-1)^((epsilon_F+1)(epsilon_G+1))(G,F).

O expoente epsilon_F epsilon_G do parecer é o de um bracket PAR, portanto
incompatível com a definição canônica impressa. Em particular, uma ação par
pode ter (S,S) não nulo. O CAS implementa derivadas esquerda/direita numa
álgebra exterior, sem redefinir a convenção para salvar a resposta.

**2. Jacobi usa a ação inteira.** A identidade é (S,(S,S))=0 para S par.
Não vale (S0,(S,S))=0 para qualquer S. Contraexemplo exato: x par, theta,c,d
ímpares, somente (x,theta)=1; S=theta(xc+d), S0=x. Então

    (S0,S0)=0, (S,S)=2theta c d,
    (S,(S,S))=0, (S0,(S,S))=2c d≠0.

Pode-se atribuir gh(x)=0,gh(theta)=-1,gh(c)=gh(d)=1, conservando gh(S)=0.
É contraexemplo algébrico à frase universal, não uma ação física alternativa.

**3. O sinal do antighost não foi reproduzido.** Na fórmula de bracket
impressa pelo provedor, com (barc,barc^ddagger)=1 e s=(S,·), o termo
-barc^ddagger b gera +b. Não gera -b. A fonte069 especifica o bracket
compatível com suas convenções; o parecer não pode simultaneamente adotar
uma fórmula incompatível e anunciar compatibilidade. É necessário ajustar
a convenção de pares/antifields, sem alterar silenciosamente a ação fonte.
Mudar apenas uma declaração separada de s, mantendo S e bracket intactos,
NÃO muda (S,S). O controle correto detecta desacordo entre s e (S,·), não
um valor novo da equação mestra calculada com entradas idênticas.

**4. Wess–Zumino corrigida, com seu alcance.** Seja S_cl a ação BV CLÁSSICA
COMPLETA (incluindo interação) que satisfaz CME no domínio considerado.
Se Gamma=S_cl+hbar Gamma1+... e a quebra do funcional de Slavnov começa
em hbar, Jacobi expandida nessa ordem dá (S_cl,A1)=0, após conservar os
contatos requeridos pela Ward. Para a formulação causal, usa-se a Ward e
nilpotência com as hipóteses dos Teoremas3/6/7 de Fröb já consultados;
essa expressão simplificada não elimina os contatos da QME.

Não substituir S_cl por sua parte LIVRE S0 em todas as valências. Se
s=s0+s1+... e a=Σa_E, a equação na valência E contém Σ_j s_j a_(E-j).
Somente no primeiro grau adequado a condição pode reduzir-se a s0a_E=0.
Se o cutoff produz um defeito clássico, incluí-lo no complexo estendido
ou declarar o recorte chi=1; não presumir CME global por omissão de dchi.

Adotando a graduação TOTAL em que s d_H+d_H s=0, a consistência local é

    s a_4^1+d_H b_3^2=0.

Índice superior é ghost; inferior é grau de forma. Para Gamma→Gamma+hbar B,
com densidade B_4^0, o representante muda por

    a' = a+s B_4^0+d_H eta_3^1,   b'=b+s eta_3^1.

Esses sinais preservam WZ pela anticomutação indicada. Se a=s B+d eta,
a remoção usa a MUDANÇA com sinais opostos. Na convenção de coeficientes
onde s comuta com d, a descida muda de sinais; não misturar as duas tabelas.
Com cutoff, integral chi d eta = -integral dchi wedge eta para suporte
compacto. A contribuição de borda deve ser mantida.

WZ é linear: (a,b) e (-a,-b) passam juntos. Não detecta sozinho o sinal de
um coeficiente físico. Já a não exatidão de um cociclo DADO é questão de
cohomologia e pode ser provada sem grafos; os grafos/prescrição determinam
qual cociclo efetivamente ocorre. A separação anterior do parecer confundia
essas duas tarefas. Os limites clássicos de valência também não autorizam
truncar antes das contrações, conforme a medida quantum_filtration já entregue.

CAS: {result['checks']} identidades, incluindo brackets canônicos, antissimetria
e Jacobi em uma base finita, e3controles negativos; rc0,CPU{result['cpu_seconds']}s.
Os contraexemplos são exatos. A validade geral de Jacobi é a identidade
algébrica padrão, não inferência por amostragem desses testes. Nenhum
coeficiente quântico foi fabricado; os erros do parecer não invalidam por
si a construção da fonte. Kernel, originais e gate intactos.

Uso informado:232032entrada+26790saída=258822tokens,225280cache;
custo estimadoUS$0.03552528. Recuperar/revisar não fez nova chamada remota.
'''
rp=HERE/'odd_bracket_review/REVISAO_E_WZ_CORRIGIDA.md';save(rp,report)
save(OUT/'ENTREGA_016_A7b_revisao_DeepSeek_WZ.md',report)
paths=[HERE/'odd_bracket_review_check.py',HERE/'odd_bracket_review_run.log',
    HERE/'odd_bracket_review/PRE_REGISTER.json',HERE/'odd_bracket_review/results.json',rp,
    HERE/'received_reviews'/(job+'.md'),HERE/'received_reviews'/(job+'.json'),
    CHAT/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md',
    HERE/'quantum_filtration/DERIVACAO_FILTRACAO.md']
save(HERE/'odd_bracket_review/manifest.json',json.dumps(dict(at=now,opening_sha256=opening,
    artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in paths]),ensure_ascii=False,indent=2))
ledger=OUT/'LEDGER_016.jsonl';old=ledger.read_bytes()
marker='A7_DEEPSEEK_WZ_RECEIVED_AND_REVIEWED';assert marker.encode() not in old
meta=receipt['result_metadata']
event=dict(event=marker,at=now,provider='deepseek',target='A-7.b',job_id=job,
    execution_id=receipt['execution_id'],request_id=receipt['request_id'],
    prompt_sha256=receipt['prompt_sha256'],response_sha256=receipt['response_sha256'],
    usage=meta.get('usage'),cost_estimate_usd=meta.get('cost_estimate_usd'),
    new_external_execution=False,checks=result['checks'],negatives=3,
    cpu_seconds=result['cpu_seconds'],review_sha256=sha(rp))
save(ledger,old+(json.dumps(event,ensure_ascii=False)+'\n').encode())
costs={}
for line in ledger.read_text('utf-8-sig').splitlines():
    if not line.strip():continue
    e=json.loads(line);v=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    key=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
    if key and v is not None:costs[key]=Decimal(str(v))
total=str(sum(costs.values(),Decimal(0)))
cont=HERE/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,previous_goal_turn='PROGRESS',status='ACTIVE',partial_metered_cost_usd=total,
    deepseek_wz_review_manifest=str(HERE/'odd_bracket_review/manifest.json'),
    pending_orchestration='5 registered (Kimi3/MiMo2);9 staging(Kimi5/MiMo4);Kimi incidence executing')
d['completed_this_turn'].append('DeepSeek WZ reviewed, three sign/Jacobi errors measured and corrected,583 checks')
d['latest_orchestration']=dict(at=now,source='Official coordinator message, snapshot only',
    nonterminal_registered=dict(kimi=3,mimo=2,deepseek=0,total=5),
    staging=dict(kimi=5,mimo=4,deepseek=0,total=9),
    currently_executing='Kimi one_loop_incidence',
    new_metric_job='2177daf6-29db-4d0c-940a-63d4c582fa04',
    new_finite_contact_request='54481007-1ab2-4694-94c4-d301f5a260a2',
    new_remote_execution_by_this_script=False)
save(cont,json.dumps(d,ensure_ascii=False,indent=2))
progress=OUT/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: DeepSeek WZ revisto,583checks+3negativos,CPU{result["cpu_seconds"]}s; sinais/ação completa explicitados. Q2finitaOPEN. Fila5+staging9 conforme coordenação. Custo externo parcialUS${total};desconhecidos não zerados. Abertura{opening}.\n'.encode())
print(json.dumps(dict(report=str(rp),partial_metered_cost_usd=total,status='ACTIVE_PROGRESS'),ensure_ascii=False))
