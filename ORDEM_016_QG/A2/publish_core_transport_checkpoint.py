from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, sys

root = Path(__file__).resolve().parents[1]
folder = root/'A2'
out = root.parent/'TUNEL/DO_CHATGPT'
now = datetime.now(timezone.utc)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def create(p, data):
    assert not p.exists(), p
    temp = p.with_name(p.name+'.tmp')
    with temp.open('xb') as f: f.write(data)
    assert temp.read_bytes() == data
    temp.rename(p)
def append(p, data):
    old=p.read_bytes()
    create(p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f')), old)
    temp=p.with_name(p.name+'.tmp')
    with temp.open('xb') as f: f.write(old+data)
    assert temp.read_bytes()==old+data
    temp.replace(p)

passed=[('LightRayVerticalDecay_v4.lean','vertical_decay_04'),
        ('LightRayBoundaryBalance_v3.lean','boundary_balance_03'),
        ('LightRayFourierBoundary_v2.lean','fourier_boundary_02'),
        ('LightRayCoreMembership.lean','core_membership_01'),
        ('LightRayCoreExtension_v2.lean','core_extension_02')]
records=[]
for source,label in passed:
    receipt=json.loads((folder/(label+'.json')).read_bytes())
    assert receipt['rc']==0
    assert receipt['source_sha256']==sha(folder/source)
    assert receipt['log_sha256']==sha(folder/(label+'.log'))
    assert not receipt['newer_kernel_files'] and not receipt['scan_errors']
    records.append({'source':source,'source_sha256':sha(folder/source),
                    'log':label+'.log','log_sha256':sha(folder/(label+'.log')),
                    'receipt':label+'.json','receipt_sha256':sha(folder/(label+'.json'))})
audit_args=[sys.executable,'-X','utf8','-B',str(root/'A0/auditar_axiomas.py')]
for source,label in passed: audit_args.extend([str(folder/source),str(folder/(label+'.log'))])
audit=subprocess.run(audit_args,capture_output=True)
assert audit.returncode==0, audit.stdout+audit.stderr
create(folder/'core_transport_axioms.json',audit.stdout)
audits=json.loads(audit.stdout)
n=sum(x['n_theorem_lemma_na_fonte'] for x in audits)

labels=['vertical_decay_01','vertical_decay_02','vertical_decay_03','vertical_decay_04',
        'boundary_balance_01','boundary_balance_03','fourier_boundary_01','fourier_boundary_02',
        'core_membership_01','core_extension_01','core_extension_02']
receipts=[json.loads((folder/(label+'.json')).read_bytes()) for label in labels]
wall=sum(x['wall_seconds'] for x in receipts)
cpu=sum(x['cpu_user_seconds']+x['cpu_kernel_seconds'] for x in receipts)
bench=(now-datetime.fromisoformat(receipts[0]['utc'])).total_seconds()
opening=sha(out/'ENTREGA_016_ABERTURA_operador.md')

base=root.parent/'IALD_ORQUESTRACAO_20260923'
job_id='bcacca23-9116-4043-8b69-ac7264009303'
res=subprocess.run([sys.executable,'-X','utf8','-B',str(base/'bridge.py')],
    input=json.dumps({'operation':'get','job_id':job_id}).encode(),capture_output=True)
assert res.returncode==0, res.stderr
job=json.loads(res.stdout)
execution=job.get('execution') or {}
metadata={k:job.get(k) for k in ['id','request_id','stage','thread_id','execution_task_id','updated_at']}
metadata.update(executor_status=execution.get('status'),executor_error=execution.get('error'),
                result_available=bool(execution.get('result')),checked_at=now.isoformat())
create(folder/'core_transport_orchestration_status.json',json.dumps(metadata,indent=2).encode())
ledger=out/'LEDGER_016.jsonl'
entry={'ts':now.isoformat(),'alvo':'A-2','ramo':'A-2.3.a','provedor':'mimo',
       'request_id':job['request_id'],'job_id':job_id,'execution_task_id':job.get('execution_task_id'),
       'question_sha256':hashlib.sha256(execution.get('prompt','').encode()).hexdigest(),
       'answer_sha256':None,'tokens_in':None,'tokens_cache':None,'tokens_out':None,'custo_usd':None,
       'desfecho':'execution_observed_'+str(execution.get('status')),
       'reason':'Official worker executing unique unit. Usage pending actual receipt; null is not zero. Work synthesis awaits daily quota; no fallback.'}
append(ledger,(json.dumps(entry,ensure_ascii=False)+'\n').encode())
rows=[json.loads(line) for line in ledger.read_text(encoding='utf-8').splitlines() if line]
known_cost=sum(x.get('custo_usd') or 0 for x in rows)
unknown_cost=sum(x.get('custo_usd') is None for x in rows)

manifest={'status':'REAL_ISOLATED_WITH_EXPLICIT_DENSITY_HYPOTHESIS','utc':now.isoformat(),
          'opening_sha256':opening,'records':records,'axioms_sha256':sha(folder/'core_transport_axioms.json'),
          'compiled_theorems':n,'attempt_receipts':labels,'wall_seconds':wall,'cpu_seconds':cpu,
          'bench_window_seconds':bench,'infrastructure_failure':{
              'log':'boundary_balance_02.log','sha256':sha(folder/'boundary_balance_02.log'),
              'reason':'Source creation failed before compilation; runner could not hash absent source. No proof/result inferred; source subsequently created and compiled under label03.'},
          'density':'OPEN','halfline_isotony':'CONDITIONAL_ON_NAMED_DENSITY',
          'mimo':metadata,'ledger_known_cost_usd':known_cost,'ledger_events_cost_pending':unknown_cost}
create(folder/'core_transport_manifest.json',json.dumps(manifest,indent=2,ensure_ascii=False).encode())
report=f'''[REAL] A-2.3.a: transporte do núcleo ligado ao K construído; extensão condicionada somente à densidade.

Abertura SHA256: {opening}

**Resultado.** Foram compilados mais {n} teoremas em arquivos isolados: o contorno vertical desaparece, Cauchy identifica as integrais de fronteira, a normalização Fourier existente dá Fg(p)=exp(2π²p) conjugado(Fg(-p)), e esta identidade paga a pertença ao domínio ponderado efetivo. Com c=2π², cada g=m_a f_r (a≥0, b>0) pertence ao MESMO subespaço padrão K transportado por Fourier, não a uma cópia homônima. U(a)f_r=g foi ligado ao U da reta de luz existente.

**Extensão.** halfline_isotony_of_gaussian_density usa a continuidade do U existente, o span real dos f_r e o caráter fechado de K. A única hipótese matemática adicional desse lema é hdensity: K está contido no fecho do span real. Ela permanece OPEN. A prova não assume meia-inclusão disfarçada no domínio: o domínio foi pago por spectral_balance_mem_standard, com spectralJ(f) como testemunha L² do peso. A rotina não prova por si só a densidade, o fator 2π forçado, AQFT completa, H1/H2/H3 ou novo gate.

**Validação.** Cinco arquivos aprovados, rc0, todos os theorem/lemma cobertos por #print axioms, axiomas contidos no trio, sem sorry/axiom novo/native_decide. Recibos de todas as tentativas preservados. Nenhum arquivo canônico alterado. Houve uma falha de infraestrutura entre boundary_balance_01 e 03 (criação Python com bytes Unicode inválidos; chamada seguinte recebeu fonte ausente); log preservado e marcado sem resultado. Não se usa esse log como evidência de prova.

**Orquestração.** Job {job_id}, tarefa executora {job.get('execution_task_id')}, estado {job.get('stage')}, executor {execution.get('status')}. Física preparou o pedido; MiMo está fixado, chamada única. O resultado/consumo ainda depende de recibo do executor. Kimi será cético em unidade própria posterior, sem substituir/repetir a unidade MiMo. A coordenação informou esgotamento dos 3 envios Work de hoje; síntese posterior segue a fila e a cota, sem desvio por executor direto.

**Custo medido neste checkpoint.** Lean: {wall/3600:.9f} h parede, {cpu/3600:.9f} h CPU, em {len(receipts)} recibos; janela de bancada desde a primeira compilação: {bench/3600:.6f} h (não exclusiva de raciocínio). A tentativa de fonte ausente não tem recibo íntegro de custo e está separada. Ledger: US$ {known_cost} conhecido, {unknown_cost} evento(s) com consumo pendente; não anunciar custo total zero. Parte B pesada: nenhuma execução iniciada.

**Próximo passo.** Densidade real do núcleo — exatamente a questão única delegada ao MiMo —, depois crítica independente e compilação. Sem encerrar A-2.3.a nem saltar para a rota condicional final da árvore.

Manifesto: {folder/'core_transport_manifest.json'}
SHA256: {sha(folder/'core_transport_manifest.json')}
Auditoria: {folder/'core_transport_axioms.json'}
SHA256: {sha(folder/'core_transport_axioms.json')}
'''
dest=out/'ENTREGA_016_MEDIDA_A2_3a_transporte_do_core.md'
create(dest,report.encode())
append(out/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} | A-2.3.a EM CURSO/MEDIDA PARCIAL | Mais {n} teoremas: domínio e U no núcleo pagos; extensão compilada sob densidade explícita OPEN | Lean {wall/3600:.9f}h parede, {cpu/3600:.9f}h CPU; bancada {bench/3600:.6f}h. MiMo {execution.get("status")}; ledger conhecido US${known_cost}, consumo pendente {unknown_cost}. B pesada 0h.\n'.encode())
print(json.dumps({'report':str(dest),'sha256':sha(dest),'theorems':n,'orchestration':metadata},ensure_ascii=False))
