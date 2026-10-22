"""Custody and progress for corrected incidence and finite cutoff completion."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid,sys
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
def js(p):return json.loads(p.read_bytes())
now=datetime.now(timezone.utc).isoformat();opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
inv=js(HERE/'incidence_decorated/results.json');ia=js(HERE/'incidence_decorated_audit/results.json')
cut=js(HERE/'finite_cutoff_contact/results.json');pos=js(HERE/'finite_cutoff_position/results.json')
inventory_report=f'''[REAL — inventário e auditoria executados; DERIVED — cobertura combinatória delimitada]
# A7.b — incidências decoradas corrigidas
Abertura SHA256 `{opening}`. UTC {now}.

O novo enumerador inclui a cor de cada vértice, o tipo e a orientação das
linhas no certificado canônico. Os originais e os defeitos da resposta
Kimi ficam preservados. Não se promove a crítica não reproduzida dos
índices móveis a fato: os 2.187 controles anteriores não a confirmaram.

Para grafos conexos de um laço I=V, E=sum(v_i-2); com v_i>=3 e E<=6,
V<=6 e v_i<=8. As partições produzem 29 famílias. Geram-se todos os
multigrafos com esses graus, todas as cores admissíveis e todas as linhas
H-H ou C->CB que respeitam os slots. Quocientar em etapas preserva as
órbitas, pois cada etapa subsequente percorre todas as decorações.

Resultado: **{inv['types']} tipos de ação**, por E=1..6:
{json.dumps(inv['by_E'],ensure_ascii=False)}. Inclui tadpoles e grafos
conexos redutíveis; não se impôs 1PI. Assinaturas METRIC=H^v,
GHOST=(CB,C,H),HDAG=(h†,C,H),CDAG=(c†,C,C), estas três cúbicas.
Pernas externas não são numeradas, e derivadas/tensores dos vértices não
são decompostos em diagramas individuais. Isso delimita o significado
de tipo; não é contagem de termos da amplitude.

Auditoria sem importar o motor: {ia['rows_checked']} registros revalidados,
sem duplicatas, com todos os automorfismos de vértices conferidos por
permutações que preservam as cores. Oráculo por emparelhamentos de
meias-arestas reproduz E=1,2,3: 2,11,41 tipos, respectivamente a partir
de 4,69,1900 emparelhamentos rotulados. Três controles negativos;
o motor tem outros cinco. CPU motor {inv['cpu_seconds']}s,
auditoria {ia['cpu_seconds']}s; ambos rc0.

Todos os tipos têm ghost0. **Não há inserção Ward/EOM/cutoff definida
por essa enumeração**. Seu catálogo continua pendente: não basta mudar
o número de ghost de um registro. Pesos de amplitude permanecem null;
automorfismo combinatório não foi usado como peso de Feynman.
O resultado organiza o cálculo; não determina a anomalia nem move gate.

Reprodução: Python314 -X utf8 -B incidence_decorated_run.py e
incidence_decorated_audit.py, com destinos novos (artefatos existentes
são protegidos). Fontes, entradas e logs têm hashes nos manifestos.
'''
ir=HERE/'incidence_decorated/INVENTARIO_AUDITADO.md';save(ir,inventory_report)
save(OUT/'ENTREGA_016_A7b_incidencias_decoradas.md',inventory_report)
cutoff_report=f'''[DERIVED — completamento BV quadrático com cutoff; REAL — CAS exato; OPEN — Q2 causal completa]
# A7.b — termos de fronteira do contato finito hc
Abertura SHA256 `{opening}`. UTC {now}.

N é o contato quártico da Hessiana e R o contato cúbico da fonte,
calculados nas entregas anteriores, com seus coeficientes lidos dos
resultados. No setor livre principal, sh=Kc, sc=0,
s hat_h†=Eh e EK=0; hat_h† conserva seu termo com antighost.
E é a Hessiana física não gauge-fixada. Seja chi uma função escalar
externa BRST-inerte. Considere

    B_chi=integral chi [ (1/2) h:N(partial)h + lambda hat_h†:R(partial)c ].

As constantes físicas globais continuam separadas; lambda não é ajustado.
No pareamento formal integrado, N*=N, E*=E e R* tem sinal negativo
por ser cúbico. A integração por partes dá EXATAMENTE

    sB_chi = integral c · [chi K* N h + [K*,chi] N h
                         +(1/2) K* [N,chi]h
                         +lambda(chi R* E h + [R*,chi] E h)].

A primeira correção tem coeficiente UM, não meio: há duas contribuições
de 1/2 ao mover as derivadas das duas pernas métricas. K* atua no
produto inteiro à sua direita. Até cinco derivadas de chi no setor
métrico e três no setor fonte podem aparecer. Quando chi é constante,
todas essas correções desaparecem e recupera-se o resultado anterior.

**Consistência com ghosts.** Para momentos formais q do h, r do ghost,
k=-q-r do cutoff, a parcela métrica é

    (1/2) [ N_q(H,K_r v) + N_r(H,K_r v) ],

onde N_p(H,T)=H:N(p)T. Substituir H=K_q w dá coeficiente simétrico sob
(q,w)<->(r,v); a anticomutação dos dois modos ghost o anula.
A fonte anula por E_q K_q=0. Logo s0(s0 B_chi)=0 com chi variável,
para esta primitiva. Não se descartou uma divergência com cutoff variável.

Controle q=e0,r=2e0,v=w=e0: manter somente chi vezes a fórmula de
cutoff constante dá defeito de troca **-1323/320**. O completamento
dá zero; o coeficiente simétrico é -357/320. Isso vale nas duas
assinaturas. O teste detecta também o erro de meio no primeiro
comutador e o sinal errado do adjunto cúbico.

CAS: {cut['checks']} identidades polinomiais gerais, duas assinaturas,
3 controles, rc0, CPU {cut['cpu_seconds']}s. Verificação independente
em posição: chi=(1-x²)^6 em [-1,1], com os jatos necessários nulos
nas extremidades, {pos['checks']} checks e 2 controles, rc0,
CPU {pos['cpu_seconds']}s. Por exemplo a omissão de fronteira métrica
no primeiro caso muda a integral em {pos['records'][0]['metric_omitted_boundary']};
na fonte, em {pos['records'][0]['source_omitted_boundary']}, ambos não zero.

**Alcance:** obtivemos o completamento local com cutoff da primitiva
principal já medida. Não se identificou por esse cálculo o coeficiente
de todos os termos com derivadas dos acoplamentos no produto temporal
original. Curvatura, fases relativas da amplitude e a família multilocal
admissível continuam necessárias para Q2 completa no modelo truncado.
Nenhum original, kernel ou gate alterado. Reprodução e hashes nos
manifestos finite_cutoff_contact e finite_cutoff_position.
'''
cr=HERE/'finite_cutoff_contact/DERIVACAO_CUTOFF.md';save(cr,cutoff_report)
save(OUT/'ENTREGA_016_A7b_contatos_cutoff_finito.md',cutoff_report)
configs=[('incidence_decorated',['incidence_decorated_engine.py','incidence_decorated_run.py','incidence_decorated_run.log'],[ir,HERE/'incidence_decorated/inventory.json']),
 ('incidence_decorated_audit',['incidence_decorated_audit.py','incidence_decorated_audit_run.log'],[ir,HERE/'incidence_decorated/inventory.json']),
 ('finite_cutoff_contact',['finite_cutoff_contact_check.py','finite_cutoff_contact_run.log'],[cr,HERE/'finite_principal_contact/results.json',HERE/'finite_antifield_contact_v3/results.json']),
 ('finite_cutoff_position',['finite_cutoff_position_audit.py','finite_cutoff_position_run.log'],[cr,HERE/'finite_principal_contact/results.json',HERE/'finite_antifield_contact_v3/results.json'])]
for folder,names,extra in configs:
    files=[HERE/n for n in names]+[HERE/folder/'PRE_REGISTER.json',HERE/folder/'results.json']+extra
    save(HERE/folder/'manifest.json',json.dumps(dict(at=now,opening_sha256=opening,
        artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]),ensure_ascii=False,indent=2))

# Recover the failed unit through the public client. Never transition or retry.
sys.path.insert(0,str(CHAT/'IALD_ORQUESTRACAO_20260923'))
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.coordination import Coordination
job='f423503e-8c02-467a-b8cc-c3db91323a82';rec=Coordination(Runtime(recover=False)).get(job)
ex=rec['execution'];assert ex['status']=='failed'
failed=dict(at=now,job_id=job,request_id=rec['request_id'],execution_id=ex['id'],
    provider='mimo',status=ex['status'],error=ex.get('error'),
    prompt_sha256=hashlib.sha256(rec['prompt'].encode()).hexdigest(),response_sha256=None,
    usage=None,cost_estimate_usd=None,new_external_execution=False,retry=False)
fp=HERE/'received_reviews'/f'{job}_failure.json';save(fp,json.dumps(failed,ensure_ascii=False,indent=2))
save(OUT/'ENTREGA_016_MEDIDA_MiMo_filtracao_transporte.md',f'''[REAL — estado failed consultado na API local; OPEN — conteúdo não recebido]
Abertura SHA256 `{opening}`. UTC {now}.
Unidade MiMo filtration_skeptic: job {job}, execução {ex['id']}.
Erro devolvido: `{ex.get('error')}`. Nenhum texto final, token ou custo
retornado; valores desconhecidos, não zero. Não se infere defeito
matemático nem inexistência de cobrança. A chamada não foi repetida,
nem substituída por outro provedor. Recibo `{fp}`, SHA256 `{sha(fp)}`.
A verificação local de incidências prosseguiu, e a coordenação foi
avisada para continuar a próxima unidade já autorizada na fila.
''')
ledger=OUT/'LEDGER_016.jsonl';events=[]
for event,provider,extra in [
 ('A7_DECORATED_INCIDENCE_AUDITED','local',dict(types=inv['types'],cpu_seconds=inv['cpu_seconds']+ia['cpu_seconds'],report_sha256=sha(ir))),
 ('A7_FINITE_CUTOFF_COMPLETION','local',dict(checks=cut['checks']+pos['checks'],cpu_seconds=cut['cpu_seconds']+pos['cpu_seconds'],report_sha256=sha(cr))),
 ('A7_MIMO_FILTRATION_FAILED_'+job,'mimo',failed)]:
    if event.encode() not in ledger.read_bytes():events.append(dict(event=event,at=now,target='A-7.b',provider=provider,**{k:v for k,v in extra.items() if k not in ('at','provider')}))
save(ledger,ledger.read_bytes()+''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events).encode())
cont=HERE/'CONTINUIDADE.json';d=js(cont)
d.update(at=now,previous_goal_turn='PROGRESS',status='ACTIVE',
    completed_this_turn=['6842 action incidence types independently validated; E<=3 half-edge oracle agrees',
        'Finite principal quadratic BV cutoff completion:304 general polynomial and12 independent position checks',
        'MiMo filtration failed IncompleteRead; receipt preserved, no retry'],
    incidence_corrected_manifest=str(HERE/'incidence_decorated/manifest.json'),
    incidence_independent_manifest=str(HERE/'incidence_decorated_audit/manifest.json'),
    finite_cutoff_manifest=str(HERE/'finite_cutoff_contact/manifest.json'),
    finite_cutoff_position_manifest=str(HERE/'finite_cutoff_position/manifest.json'),
    pending_orchestration='Read official coordinator; latest MiMo filtration failed, do not repeat',
    next=['Match the explicit finite-cutoff primitive to actual causal insertions; fix physical phases and curved terms',
          'Consume pending independent reviews without repeats',
          'Continue A7.b within its remaining timebox, then A7.c if necessary, A7.d, A8 and Part B'])
save(cont,json.dumps(d,ensure_ascii=False,indent=2))
progress=OUT/'ENTREGA_016_PROGRESSO.md';cpu=sum(x['cpu_seconds'] for x in (inv,ia,cut,pos))
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO:6842tipos auditados+cutoff finito304+12checks,CPU{cpu}s;Q2completaOPEN. MiMo filtration falhouIncompleteRead,custo/tokens desconhecidos,sem repetição. Abertura{opening}.\n'.encode())
print(json.dumps(dict(at=now,cpu_seconds=cpu,inventory_report=str(ir),cutoff_report=str(cr),status='ACTIVE_PROGRESS'),ensure_ascii=False))
