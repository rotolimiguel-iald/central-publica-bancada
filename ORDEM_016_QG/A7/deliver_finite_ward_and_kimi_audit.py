"""Record the measured partial Ward difference and audited external contribution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT'
D=H/'finite_ward_delivery';D.mkdir(exist_ok=True)
now=datetime.now(timezone.utc).isoformat();stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data,existing=False):
    if isinstance(data,str):data=data.encode()
    if p.exists():
        assert existing,p
        old=p.read_bytes();backup=p.with_name(p.name+'.bak_'+stamp)
        backup.write_bytes(old);assert backup.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(data);assert tmp.read_bytes()==data;tmp.replace(p)
def put(p,v,existing=False):write(p,json.dumps(v,indent=2,ensure_ascii=False),existing)
r=json.loads((H/'finite_pair_ward/results.json').read_bytes())
a=json.loads((H/'kimi_finite_ward_audit_v2/audit_results.json').read_bytes())
receipt=json.loads((H/'kimi_finite_ward_audit/RECEIPT.json').read_bytes())
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[DERIVED — diferença Ward local parcial; REAL — CAS; OPEN — identidade completa]
# A7.b — inserção de gauge ordenada nos pares finitos
Abertura SHA256 `{opening}`. UTC {now}.

Inserimos G(v)=nabla v+(nabla v)^t diretamente nos vértices métrico e ghost,
preservando a ordem exterior-y / Taylor simetrizado / interior-x. Aplicamos
a Hessiana física E ao contato fonte covariante medido na entrega anterior.
Não substituímos cinco derivadas covariantes por momentos comutantes.

Na convenção comum contato/C, com a fase Fourier i separada, a combinação
-par_métrico/2 + par_ghost + E DeltaR, RELATIVA à referência harmônica, deu:

| ordem | base | coeficientes |
|---|---|---|
| K0 | p⁴Tpv, p²pTp pv, p⁴trT pv | {r['partial_Ward_coefficients']['0']} |
| K1 | K[p²Tpv, pTp pv, p²trT pv] | {r['partial_Ward_coefficients']['1']} |
| K2 | K²[Tpv, trT pv] | {r['partial_Ward_coefficients']['2']} |

Este resultado NÃO é o coeficiente da anomalia completa. A referência
diferencial também pode ter imagem Ward; não foi demonstrada neutra.
O tadpole finito, os jatos W admissíveis e as valências superiores não
entram nessa soma. Um tadpole tau K² trh acrescentaria tau K²[G-gdiv];
tau não foi ajustado nesta medição. Nenhuma subtração foi adotada.

**Contagem exata:** 100 comparações de jatos planos, três verificações dos
ajustes e UMA validação nova com momento não axial = {r['checks']}. As três
verificações dos ajustes não são três previsões independentes. No teste
não axial K1, p=(1,2,-1,1), v=(2,-1,1,3), T=e11, o valor medido e previsto
é 86045/1728. CPU {r['cpu_seconds']}s; execução integral rc0.

Os novos adaptadores v2 apenas permitem injetar o provedor de jatos; a
reversão das duas alterações devolve exatamente os motores anteriores.
SHA de fontes, registro prévio, log e resultados constam no manifesto.
O próximo elo é calcular a contribuição da referência na MESMA prescrição,
sem apagar os harmônicos altos por não terem diferença local. Q2 OPEN.
'''
rf=O/'ENTREGA_016_A7b_diferenca_Ward_finita_ordenada.md';write(rf,report)
review=f'''[REAL — auditoria CAS; DERIVED — recorrência escalar; DECLARADO — parecer externo]
# A7.b — revisão da contribuição Kimi finite_two_point_ward_contact
Abertura SHA256 `{opening}`. UTC {now}.
Job `{receipt['job_id']}`, modelo {receipt['model']}. O original foi preservado
integralmente. Uso informado: {receipt['usage']}. Assinatura: sem cobrança
incremental estimada aqui. Nenhuma repetição da chamada.

**Aproveitado:** recorrências dos contatos de potências puras e mudança de
referência escalar. Para U_n=z^-n e D_n=Box^(n-2)R(U2)/
[4^(n-2)(n-1)!(n-2)!], na referência plana:

    R(U_n)-D_n = [H_(n-1)+H_(n-2)-1] Res(U_n),
    R(U3)-D3 = -3 C Box delta/64,
    R(U4)-D4 = -7 C Box² delta/2304.

A recorrência foi confrontada com o motor meromorfo já auditado, n2..8.
É uma conversão escalar PLANA; ainda não é transporte da amplitude curva.

**Erros medidos e limites:**
- Script recebido: 24 PASS, 1 FAIL, rc1. T7 deixa D3-D2, símbolos
  independentes; usou D3 onde a identidade para zD3 pede D2. A identidade
  distribucional multiplicativa não é refutada por esse erro no teste.
- A substituição Riem1²=2Ric1²-R1²/3 módulo derivada total está incorreta.
  No controle transversal h12=h21=1, p=e0: Riem1²=2, Ric1²=1/2, R1=0;
  a fórmula proposta erra por 1. A combinação de Euler é 4Ric1²-R1².
- Pi G=0 não substitui a STI completa com fonte antifield e tadpole.
- Localidade sozinha não demonstra que uma quebra está na imagem BRST.
  Calculamos algo mais limitado: a matriz Ward do símbolo plano simétrico
  de cinco coeficientes tem posto3 e núcleo2. Os dois quadráticos covariantes
  Ric1² e R1² são Ward-neutros; não cancelam uma quebra não nula por si sós.
- Ric1(G)=R1(G)=0 não demonstra Wess–Zumino para a quebra calculada.
  h*local h, tal como escrito sem ghost, tampouco tem grau de ghost zero.

Auditoria própria v2: {a['checks']} verificações, rc0, CPU{a['cpu_seconds']}s.
A v1 local falhou por confundir resíduo de x_i U com q_i Res(U)/q² na
expressão esperada; foi corrigida em arquivo novo. Fonte/log v1 preservados.
Uma tentativa de gerar v2 por comando PowerShell falhou na interpretação
de aspas antes de criar o arquivo; substituída por preparador em arquivo.

O Kimi deixou L1/L2, curvatura e anomalia integral abertos. A bancada já
possui cálculos posteriores para parte desses itens; isso não retroage
ao pacote recebido pelo revisor. Parecer incorporado apenas neste escopo.
'''
af=O/'ENTREGA_016_A7b_auditoria_Kimi_Ward_finito.md';write(af,review)
mf=O/'ENTREGA_016_MEDIDA_teste_Kimi_Ward_finito.md'
write(mf,f'''[REAL — testes recusados e correção local preservada]
# A7.b — testes Ward finitos
Abertura SHA256 `{opening}`. UTC {now}.
Comando: symbolic_runtime/Scripts/python.exe -X utf8 -B <script>.
kimi_finite_ward_audit/provided_check.py: rc1, T7=D3-D2, demais24 PASS.
audit_kimi_finite_ward.py: rc1, esperado incorreto q0/4 contra -q0/8.
audit_kimi_finite_ward_v2.py: rc0,51controles, corrige apenas o esperado.
Logs/fontes e hashes no manifesto desta entrega. Custos de máquina:
Ward621.890625s CPU; auditorv2{a['cpu_seconds']}s; falhas não cronometradas
separadamente. Nenhuma chamada externa extra para corrigir esses testes.
Próximo ramo dentro de A7.b: contribuição da referência diferencial.
''')
files=[Path(__file__),rf,af,mf,H/'finite_pair_ward_check.py',H/'finite_pair_ward_run.log',
 H/'finite_pair_ward/results.json',H/'finite_pair_ward/PRE_REGISTER.json',H/'finite_pair_ward/manifest.json',
 H/'prepare_finite_pair_jet_inputs.py',H/'finite_pair_jet_inputs_manifest.json',
 H/'finite_metric_pair_engine_v2.py',H/'finite_ghost_pair_engine_v2.py',
 H/'receive_kimi_finite_ward.py',H/'kimi_finite_ward_audit/ANSWER.md',
 H/'kimi_finite_ward_audit/RECEIPT.json',H/'kimi_finite_ward_audit/provided_check.py',
 H/'kimi_finite_ward_audit/provided_check_run.log',H/'audit_kimi_finite_ward.py',
 H/'kimi_finite_ward_audit/audit_run.log',H/'kimi_finite_ward_audit/AUDIT_PRE_REGISTER.json',
 H/'prepare_kimi_finite_ward_audit_v2.py',H/'audit_kimi_finite_ward_v2.py',
 H/'kimi_finite_ward_audit_v2_run.log',H/'kimi_finite_ward_audit_v2/AUDIT_PRE_REGISTER.json',
 H/'kimi_finite_ward_audit_v2/audit_results.json']
manifest=dict(at=now,opening_sha256=opening,artifacts=[dict(path=str(p),sha256=sha(p)) for p in files])
put(D/'manifest.json',manifest)
for row in manifest['artifacts']:assert sha(Path(row['path']))==row['sha256']
payload=H/'orchestration_finite_contact/kimi_a7_finite_two_point_ward_contact_submit.json'
prompt=json.loads(payload.read_bytes())['prompt']
event=dict(at=now,event='KIMI_FINITE_WARD_RECEIVED_AND_AUDITED',provider='kimi',target='A7.b',
 job_id=receipt['job_id'],request_id='54481007-1ab2-4694-94c4-d301f5a260a2',
 prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),payload_sha256=sha(payload),
 response_sha256=receipt['answer_sha256'],usage=receipt['usage'],cost_usd=None,
 cost_status='SUBSCRIPTION_NO_INCREMENTAL_INVOICE',local_checks=a['checks'],
 partial_ward_checks=r['checks'],cpu_seconds=r['cpu_seconds']+a['cpu_seconds'],
 delivery_manifest_sha256=sha(D/'manifest.json'),full_Q2=False)
ledger=O/'LEDGER_016.jsonl'
write(ledger,ledger.read_bytes()+(json.dumps(event)+'\n').encode(),True)
progress=O/'ENTREGA_016_PROGRESSO.md'
write(progress,progress.read_bytes()+f'\n- {now} A7.b PROGRESS: diferença Ward ordenada104controles + auditoria Kimi51controles; CPU{event["cpu_seconds"]}s. Kimi393981tokens informados, T7 recusado; recorrência escalar aproveitada. Q2 OPEN; gate intacto.\n'.encode(),True)
cont=H/'CONTINUIDADE.json';v=json.loads(cont.read_bytes())
v.update(at=now,previous_goal_turn='PROGRESS',finite_ward_manifest=str(D/'manifest.json'))
v['completed_this_turn']=['Ward finite local difference measured with ordered gauge jets,104checks',
 'Kimi completed answer audited: scalar recurrences accepted, T7/GB and STI/WZ promotion rejected,51checks']
v['next']=['Compute differential reference contribution without discarding high harmonics',
 'Keep finite tadpole, admissible W and full T-products explicit',
 'A7.c after24h if unpaid; A7.d,A8,PartB,finalaudit remain']
v['latest_orchestration']=dict(at=now,source='Official coordinator completion message',registered=5,staging=7,
 currently_executing='Kimi curved_antifield_source')
v['latest_live_execution']=dict(job_id='3043848f-1e12-45b4-a5aa-127e2e3887fd',
 status='execution_waiting_owned_by_coordinator',observed_utc=now)
v['pending_orchestration']='5 nonterminal/7 staging per coordinator; harmonic_followup remains queued'
put(cont,v,True)
print(json.dumps(dict(delivered=True,artifacts=len(files),checks=event['local_checks']+event['partial_ward_checks'],
                     cpu_seconds=event['cpu_seconds'],full_Q2=False)))
