"""Preserve local checks, scoped measurements and accepted review staging."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, uuid

H = Path(__file__).resolve().parent
C = H.parents[1]
O = C / 'TUNEL/DO_CHATGPT'
D = H / 'bilocal_progress_delivery'
D.mkdir(exist_ok=True)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write(p, b, update=False):
    if p.exists():
        assert update, p
        old = p.read_bytes()
        backup = p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as f:
            f.write(old)
        assert backup.read_bytes() == old
    t = p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:
        f.write(b)
    assert b and t.read_bytes() == b
    t.replace(p)

def put(p, v, update=False):
    write(p, json.dumps(v, ensure_ascii=False, indent=2).encode(), update)

groups = [
 ('einstein_test_field','einstein_test_field_check.py','einstein_test_field_run.log'),
 ('einstein_source_adjoint','einstein_source_adjoint_check.py','einstein_source_adjoint_run.log'),
 ('free_parametrix_brst','free_parametrix_brst_check.py','free_parametrix_brst_run.log'),
 ('pair_parametrix_brst','pair_parametrix_brst_check.py','pair_parametrix_brst_run.log'),
 ('mixed_parametrix_frame','mixed_parametrix_frame_check.py','mixed_parametrix_frame_run.log'),
 ('ghost_mixed_parametrix_frame_v2','ghost_mixed_parametrix_frame_check_v2.py','ghost_mixed_parametrix_frame_v2_run.log'),
 ('bilocal_first_curvature_v2','bilocal_first_curvature_check_v2.py','bilocal_first_curvature_v2_run.log'),
 ('pair_source_orientation','pair_source_orientation_check.py','pair_source_orientation_run.log'),
 ('curved_pair_fourier','curved_pair_fourier_check.py','curved_pair_fourier_run.log'),
 ('bilocal_regulator_contact','bilocal_regulator_contact_check.py','bilocal_regulator_contact_run.log')]
results = {stem:json.loads((H/stem/'results.json').read_bytes()) for stem,_,_ in groups}
checks = sum(v['checks'] for v in results.values())
cpu = sum(v['cpu_seconds'] for v in results.values())
negative = sum(v.get('negative_controls',0) for v in results.values())
now = datetime.now(timezone.utc).isoformat()
opening = sha(O/'ENTREGA_016_ABERTURA_operador.md')
catalog = json.loads((H/'orchestration_bilocal/prepared_units.json').read_bytes())

acceptance = dict(at=now, source_thread_id='01a0ce2b-8c2f-71b0-a9a8-91b17715a569',
    evidence='Official send_message_to_thread reply: four units accepted after nonlocal_followup; hashes and absence of request_ids checked',
    status='ACCEPTED_STAGING_NOT_SUBMITTED', job_ids=[],
    nonterminal_jobs_reported=5, staging_units_reported=11,
    coordinator_receipt='IALD_ORQUESTRACAO_20260923/state/handoffs/a7_bilocal_pending_submissions.json',
    receipt_contents_not_read_here=True,
    request_ids=[v['request_id'] for v in catalog])
put(H/'orchestration_bilocal/coordinator_acceptance.json', acceptance)

report = O/'ENTREGA_016_A7b_geometria_bilocal_e_fonte_Einstein.md'
text = f'''[DERIVED — componentes escritos; REAL — CAS exato; OPEN — Q2 completo]
# A7.b — fonte Einstein e geometria de dois extremos
Abertura SHA256 `{opening}`. UTC {now}.

O operador E foi aplicado ao teste tensorial completo em RNC, antes da
extensão, com levantamento de índices e densidade. Foram conferidos os
campos do teste, o limite plano e um controle não axial. O argumento de
auto-adjunção formal usa testes compactos; a extração do símbolo bulk não
elimina por decreto os termos do corte.

Na base [p² Tpv, (pTp)(pv), p² trT(pv)], as colunas (1,L,L²) da fonte
adjunta primeiraK são:
{json.dumps(results['einstein_source_adjoint']['coefficients'])}
Fatores comuns C_E, i e K retirados. Isso mede R(E T,c), não a quebra Q2.

Os dois cálculos longos dos pares terminaram rc0, sem reinício:
- Taylor covariante ordenado (sessão93180): {results['curved_pair_fourier']['cpu_seconds']}s CPU.
- Teste em X e ghost em Y (sessão65231): {results['pair_source_orientation']['cpu_seconds']}s CPU.
Seus coeficientes curvos diferem. Ambos passaram os respectivos controles
plano/não axial; isso não prova equivalência das duas montagens a uma mesma
distribuição de Ward. Somá-los à fonte sem derivar a integração por partes
bilocal não é autorizado pelo cálculo. Logs não nulos isolados não
estabelecem uma classe de anomalia quântica.

A identidade BRST livre dos propagadores foi conferida em coordenadas e
nas matrizes dos pares. Os jatos mistos métricos e fantasmas também foram
cotejados: o ghost superior tem sinal de conexão diferente do inferior.
Há verificações simbólicas e avaliações racionais específicas; o total
abaixo não significa igual número de teoremas independentes.

O motor bilocal mantém X e Y em UMA carta RNC antes de derivar:
 d1=-(X²Y²-(X.Y)²)/3,
 P1=((X²-Y²)I-XXᵀ+YYᵀ)/6+(XYᵀ-YXᵀ)/2.
A primeira expressão vem da energia da geodésica a primeiraK; a segunda,
da integral da conexão no segmento. A correção da trajetória contribui
em ordem superior. Inversa, isometria, transporte e recuperação dos jatos
da fonte passaram em1178 verificações. O teste v1 falhou porque comparou
expressões antes de impor o auxiliar z=X². O v2 só impõe essa restrição
DEPOIS das derivadas; o motor não foi alterado. O mesmo ocorreu no teste
ghost misto: v1 preservado, v2 registra256 identidades após a restrição.

Um controle concreto mostra por que ancorar cedo demais perde informação:
 (dYi dYj d1)|Y=0 = -2/3 (X² delta_ij-XiXj),
apesar de d1 e sua primeira derivada sumirem em Y=0. Para os completamentos
rho²=w+K d1 e w=(X-Y)² da MESMA prescrição ancorada, e para
u=w^-2 log(mu²w)^ell, ell=0,1, a diferença entre as segundas derivadas dos
reguladores estendidos produz -K*pi²*delta_ij*delta4(X)/2 a primeiraK.
Derivação: resíduo radial, área2pi² de S3 e <ni nj>=delta_ij/4; o fator
(1-a) é conservado inclusive no polo duplo do log. Testes que descartam
o termo falham em8 controles negativos. Esse é um exemplo escalar da
diferença entre completamentos; não seleciona uma nova prescrição física
nem fornece sozinho o comutador bitensorial geral.

Novas revisões aceitas pela coordenação: Kimi/divergência do par em Y;
Kimi/contatos do regulador em Y; MiMo/transporte bilocal independente;
DeepSeek/implementação da fonte Einstein. Mesma memória canônica, prévias
com executor correto, IDs persistidos e uma chamada por unidade. Estão em
STAGING, ainda sem job_id nesta entrega. Nenhum resultado esperado novo
foi inserido nos prompts de revisão, preservando a independência.

Total dos grupos: {checks} verificações reportadas, {negative} negativos,
{cpu}s CPU (inclui os dois processos iniciados antes desta entrega).
Todos os dez comandos finais terminaram rc0 no Python simbólico de A4.
Custos das falhas preparatórias não medidos não entram como zero; v1/logs
continuam preservados. Nenhum original, kernel ou gate foi alterado.
Próximo: montar as derivadas Y dos kernels/vértices/medidas antes de Y=0,
transportar os contatos na mesma prescrição e então fazer a soma de Ward.
A7.b segue dentro do timebox; A7.c/d, A8 e ParteB continuam obrigatórios.
'''
write(report, text.encode())

files = {Path(__file__), report, H/'prepare_bilocal_units.py'}
for stem, script, log in groups:
    files.update([H/script,H/log,H/stem/'PRE_REGISTER.json',H/stem/'results.json',H/stem/'manifest.json'])
    manifest = json.loads((H/stem/'manifest.json').read_bytes())
    for item in manifest.get('artifacts',[]):
        p = Path(item['path'])
        assert sha(p) == item['sha256'], p
        files.add(p)
for name in ['bilocal_first_curvature_check.py','bilocal_first_curvature_run.log',
             'ghost_mixed_parametrix_frame_check.py','ghost_mixed_parametrix_frame_run.log',
             'ghost_mixed_parametrix_frame_v2_inputs.json']:
    files.add(H/name)
files.update((H/'orchestration_bilocal').glob('*.json'))
put(D/'manifest.json',dict(at=now,opening_sha256=opening,checks_reported=checks,
    negative_controls=negative,cpu_seconds=cpu,full_Q2=False,
    artifacts=[dict(path=str(p),sha256=sha(p)) for p in sorted(files)]))

ledger = O/'LEDGER_016.jsonl'
events=[dict(at=now,event='A7_BILOCAL_PROGRESS_DELIVERED',target='A7.b',checks=checks,
             negative_controls=negative,cpu_seconds=cpu,new_external_execution=False,
             full_Q2=False,delivery_manifest_sha256=sha(D/'manifest.json'))]
for unit in catalog:
    payload=json.loads(Path(unit['payload']).read_bytes())
    events.append(dict(at=now,event='A7_BILOCAL_REVIEW_STAGED',provider=unit['provider'],
        target='A7.b',request_id=unit['request_id'],lemma_id=unit['lemma'],
        prompt_sha256=hashlib.sha256(payload['prompt'].encode()).hexdigest(),
        payload_sha256=sha(Path(unit['payload'])),status='ACCEPTED_STAGING_NOT_SUBMITTED',
        remote_call=False,tokens=None,cost_estimate_usd=None))
write(ledger,ledger.read_bytes()+''.join(json.dumps(e)+'\n' for e in events).encode(),True)

rows=[json.loads(line) for line in ledger.read_text('utf-8-sig').splitlines() if line.strip()]
parents={}
def root(k):
    parents.setdefault(k,k)
    if parents[k]!=k:
        parents[k]=root(parents[k])
    return parents[k]
def ids(r):
    return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
for row in rows:
    ix=ids(row)
    for k in ix[1:]:
        parents[root(k)]=root(ix[0])
known={}
for row in rows:
    ix=ids(row)
    cost=row.get('cost_estimate_usd',row.get('cost_usd',row.get('custo_usd')))
    if ix and cost is not None:
        known[root(ix[0])]=Decimal(str(cost))
total=sum(known.values(),Decimal())
put(D/'COST_SUM.json',dict(at=now,ledger_sha256=sha(ledger),known_partial_usd=str(total),unknown_calls_not_zero=True))
progress=O/'ENTREGA_016_PROGRESSO.md'
write(progress,progress.read_bytes()+f'\n- {now} A7.b PROGRESS: fonte Einstein, dois pares, BRST livre, jatos e motor bilocal conferidos; {checks} checks reportados/{negative} negativos; CPU{cpu}s. Dois Kimi+MiMo+DeepSeek aceitos em staging, ainda sem job_id. Custo parcial deduplicadoUS${total}; desconhecidos não zerados. Q2 OPEN.\n'.encode(),True)
p=H/'CONTINUIDADE.json'
v=json.loads(p.read_bytes())
v.update(at=now,previous_goal_turn='PROGRESS',bilocal_progress_manifest=str(D/'manifest.json'),
         own_live_processes=[],partial_metered_cost_usd=str(total))
v['completed_this_turn']=[
    'Einstein test field and singular source adjoint through firstK checked',
    'Both Fourier pair runs completed: sessions93180 and65231 rc0; not proven equivalent to full Ward distribution',
    'Free BRST and mixed derivatives checked; auxiliary-radius v1 failures preserved and v2 checked',
    'Two-endpoint firstK engine1178 checks; regulator contact55 checks/8 negatives',
    'Four new provider reviews previewed and accepted in staging, not yet submitted']
v['bilocal_review_catalog']=str(H/'orchestration_bilocal/prepared_units.json')
v['latest_live_execution']=dict(job_id='0e8fc209-ca23-4868-bac3-bc5b053936bf',
    status='COORDINATOR_REPORTED_EXECUTING',session_id_owned_by_coordinator=19998,
    observed_utc=now)
v['next']=[
    'Read complete Kimi3979f662 review through specific coordinator delivery; audit without trusting coefficients',
    'Implement full bilocal Y integration by parts on pair kernels and vertices before anchoring',
    'Do not add unequal bulk symbols and call remainder Q2; keep cutoff/W/tad/higher arities explicit',
    'Keep independent reviews unchanged; four new units behind nonlocal_followup',
    'A7.b timebox ends approximately20:32UTC; then A7.c/d,A8,PartB and final audit']
put(p,v,True)
print(json.dumps(dict(delivered=True,artifacts=len(files),checks=checks,negative_controls=negative,
    cpu_seconds=cpu,partial_known_cost_usd=str(total),new_reviews='4 ACCEPTED_STAGING',own_processes_running=0)))
