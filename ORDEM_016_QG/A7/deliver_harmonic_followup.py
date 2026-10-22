"""Record accepted orchestration and audited angular component, no gate edits."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid

H=Path(__file__).resolve().parent;C=H.parents[1];O=C/'TUNEL/DO_CHATGPT'
D=H/'orchestration_harmonic_followup';A=H/'finite_angular_contact'
at=datetime.now(timezone.utc).isoformat()
stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data,existing=False):
    if isinstance(data,str):data=data.encode('utf-8')
    if p.exists():
        assert existing,p
        old=p.read_bytes();b=p.with_name(p.name+'.bak_'+stamp)
        b.write_bytes(old);assert b.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(data);assert t.read_bytes()==data;t.replace(p)
def put(p,obj,existing=False):write(p,json.dumps(obj,ensure_ascii=False,indent=2).encode(),existing)

cat=json.loads((D/'prepared_units.json').read_bytes())
for row in cat:assert sha(Path(row['payload']))==row['payload_sha256']
result=json.loads((A/'results.json').read_bytes())
assert result['checks']==184 and not result['full_Q2']
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
acceptance=dict(at=at,status='COORDINATOR_ACCEPTED_STAGING_NO_JOB_IDS',
    source_thread='01a0ce2b-8c2f-71b0-a9a8-91b17715a569',
    source='Official send_message_to_thread response received by source task',
    note='Three exact payloads accepted after five earlier staging units; zero new remote executions in acceptance; Kimi 7ed451ee running once',
    units=cat,external_execution_by_this_turn=False)
put(D/'coordinator_acceptance.json',acceptance)

text=f'''[REAL — preparação e aceite da coordenação; OPEN — respostas]
# A7.b — duas novas unidades Kimi e uma MiMo
Abertura SHA256 `{opening}`. UTC {at}.

Ordem do operador: ampliar a distribuição de tarefas, especialmente ao Kimi.
Foram preparadas três perguntas distintas, com fontes integrais selecionadas,
linhas e SHA calculados; prévias locais selecionaram os executores exigidos.
Memória científica comum e capacidade máxima seguem o adaptador existente.

| Executor | Unidade | Resultado solicitado |
|---|---|---|
| Kimi | harmonic_reference_intertwining | Identidade entre referências diferenciais para somar contatos sem duplicar contribuições |
| Kimi | smooth_reference_ward_transport | Transporte BRST dos termos suaves de uma referência Hadamard admissível |
| MiMo | angular_harmonic_contact_table | Tabela racional por momentos esféricos/Laurent, independente da conta local |

Coordenação confirmou aceite no staging após as cinco unidades anteriores.
Ainda não há job_id dessas três: aceite não significa execução. Kimi
7ed451ee-e554-4667-9d52-86c0f7c3c55b continua sob execução única da coordenação.
MiMo 9a0fd610-896a-4c31-ba92-e14c9d876330 terminou FAILED/IncompleteRead,
execução7847c199-3c2b-453a-8e20-d24c04ae0c15; sem resposta aproveitável e sem
repetição. Uso/custo desconhecidos, não zero. Nenhum prompt anterior alterado.

Os IDs, hashes e arquivos exatos estão em prepared_units.json. Esta etapa
fez zero chamadas novas de inferência; não alterou o escalonador, o kernel,
o gate, o programa canônico nem o piloto de fine-tuning adiado.
'''
delivery=O/'ENTREGA_016_A7_orquestracao_harmonica_e_referencia.md'
write(delivery,text)

rows=['| m | l | sem log | log | log² |','|---|---|---|---|---|']
group={}
for row in result['table']:group.setdefault((row['m'],row['l']),{})[row['ell']]=row['coefficient']
for (m,l),v in group.items():rows.append(f'| {m} | {l} | {v[0]} | {v[1]} | {v[2]} |')
math=f'''[DERIVED — componente da extensão fixa; REAL — CAS exato; OPEN — soma Ward]
# A7.b — projetores angulares dos contatos finitos
Abertura SHA256 `{opening}`. UTC {at}.

Mantemos R=FP_a[(1-a)mu^(2a)z^a .]. Para H_l harmônico, m-l par,
b=(m+4-l)/2 e f=H_l(x)z^(-b-l)L^ell, a representação por derivadas
radiais usa os coeficientes v_r da inversão triangular já construída.
Foi calculada a diferença

    R(f)-sum_r v_r H_l(partial)R(z^-b L^r)
      = C c_(m,l,ell) Box^((m-l)/2) H_l(partial)delta.

{chr(10).join(rows)}

Os coeficientes foram calculados pelo motor de contatos e conferidos por
resíduos de Taylor em S3 e parte finita Laurent explícita. Os polos dos logs
foram conservados antes da parte finita. Os projetores zonais também foram
conferidos em famílias harmônicas de dois planos, incluindo graus maiores
que m (contato zero, sem apagar o kernel), e em três nós não unitários.
São {result['checks']} verificações e {result['negative_controls']} controles negativos,
rc0, CPU{result['cpu_seconds']}s. Não é prova CAS da existência analítica de
distribuições; as identidades de resíduos permanecem entradas declaradas.

O motor puro devolve coeficientes de monômios q^I para contrair com jatos
simétricos covariantes. A ação do delta dá (-1)^m. Não se divide de novo por
I!: os fatores multinomiais já pertencem ao polinômio. Em nós não unitários,
o projetor é homogeneizado com z=x.x; o kernel de grau -m-4, multiplicado
por z² e pelo projetor de grau m em x, tem grau zero.

Este é um componente reutilizável no cálculo dos kernels reais. Não se
identifica a referência harmônica com uma prescrição que preserve BRST,
não se escolhe contratermo e não se declara Q2 inteira. A auditoria remota
MiMo foi preparada ANTES desses resultados e não os recebeu.
'''
mathfile=O/'ENTREGA_016_A7b_tabela_angular_contatos_finitos.md'
write(mathfile,math)
files=[Path(__file__),H/'prepare_harmonic_followup_units.py',D/'prepared_units.json',
       D/'coordinator_acceptance.json',A/'manifest.json',A/'PRE_REGISTER.json',A/'results.json',
       H/'finite_angular_contact_engine.py',H/'finite_angular_contact_check.py',
       H/'finite_angular_contact_run.log',delivery,mathfile]
for row in cat:
    files.append(Path(row['payload']))
    slug=Path(row['payload']).name.removesuffix('_submit.json')
    files.extend([D/(slug+'_preview.json'),D/(slug+'_receipt.json')])
manifest=dict(at=at,opening_sha256=opening,artifacts=[dict(path=str(p),sha256=sha(p)) for p in files])
put(D/'delivery_manifest.json',manifest)
for r in manifest['artifacts']:assert sha(Path(r['path']))==r['sha256']

ledger=O/'LEDGER_016.jsonl'
event=dict(event='A7_HARMONIC_REVIEWS_STAGED_AND_LOCAL_TABLE',at=at,target='A-7.b',
    request_ids=[r['request_id'] for r in cat],external_execution=False,
    local_checks=result['checks'],cpu_seconds=result['cpu_seconds'],
    manifest_sha256=sha(D/'delivery_manifest.json'),
    failed_job_reported='9a0fd610-896a-4c31-ba92-e14c9d876330',
    failed_usage_cost='UNKNOWN_NOT_ZERO')
write(ledger,ledger.read_bytes()+(json.dumps(event,ensure_ascii=False)+'\n').encode(),True)
progress=O/'ENTREGA_016_PROGRESSO.md'
write(progress,progress.read_bytes()+f'\n- {at} A7.b PROGRESS: 3 revisões novas aceitas em staging (Kimi2/MiMo1), 184 controles locais da tabela angular, CPU{result["cpu_seconds"]}s; zero nova inferência nesta preparação; Q2 completa OPEN.\n'.encode(),True)
continuity=H/'CONTINUIDADE.json';v=json.loads(continuity.read_bytes())
v.update(at=at,previous_goal_turn='PROGRESS',
    harmonic_contact_table_manifest=str(D/'delivery_manifest.json'),
    new_harmonic_review_catalog=str(D/'prepared_units.json'),
    pending_orchestration='5registered/8staging after official acceptance; 3 newunits not yet submitted',
    latest_live_execution=dict(job_id='7ed451ee-e554-4667-9d52-86c0f7c3c55b',
        status='execution_waiting_owned_by_coordinator',observed_utc=at))
v['latest_orchestration']=dict(at=at,source='Official coordinator message and bridge list',
    registered=5,staging=8,currently_executing='Kimi finite_two_point_ward_contact')
v['completed_this_turn']=['3newdistinctreviews previewed and accepted in staging',
    '27 rational harmonic coefficients;184exactchecks,2negativecontrols,rc0']
v['next']=['Finish local finite_metric_pair_check process; do not duplicate it',
    'Then independent raw-kernel/reference compatibility and ghost finite contacts',
    'Do not send local conclusions into pending independent reviews',
    'A7.c after24h if unpaid, A7.d,A8,PartB,finalaudit remain']
put(continuity,v,True)
print(json.dumps(dict(artifacts=len(files),verified=True,catalog=str(D/'prepared_units.json'),
    angular_checks=result['checks'],external_execution=False)))
