"""Audit completed C4 proofs and preserve terminal transport failure without retry."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,subprocess
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'C4'
sys.path.insert(0,str(ROOT/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import OUT,BASE,sha,put,write,append
now=datetime.now(timezone.utc).isoformat()
spec=[('NullScreenFrame_v2.lean','screen_02'),('BoostScreenPolarizations_v2.lean','polarizations_02'),('StrictCocycleGauge.lean','gauge_01')]
args=[];receipts=[]
for name,label in spec:
    source=D/name;rp=D/(label+'.json');r=json.loads(rp.read_bytes())
    assert r['rc']==0 and r['source_sha256']==sha(source) and r['log_sha256']==sha(D/(label+'.log'))
    args += [str(source),str(D/(label+'.log'))]
    receipts.append(dict(path=str(rp),sha256=sha(rp),**r))
auditor=OUT.parent/'PARA_CHATGPT/ORDEM_016_INSUMOS/A6_EQUACAO_DA_VERDADE/MEDIDAS_DO_REDATOR/auditar_axiomas.py'
a=subprocess.run([sys.executable,'-X','utf8','-B',str(auditor),*args],capture_output=True)
assert a.returncode==0,a.stdout
write(D/'AXIOM_AUDIT_INITIAL.json',a.stdout)
audits=json.loads(a.stdout);assert all(x['auditoria']=='PASSA' for x in audits)
assert sum(x['n_theorem_lemma_na_fonte'] for x in audits)==19
fp=BASE/'state/handoffs/2372eee7-6542-4ba0-81b0-695206dad41f_delivery.json'
j=json.loads(fp.read_bytes())['job'];e=j['execution']
assert e['status']=='failed' and e['result'] is None
fail=dict(at=now,event='C4_MIMO_TERMINAL_FAILURE',provider='mimo',request_id=j['request_id'],job_id=j['id'],execution_task_id=e['id'],
    receipt_path=str(fp),receipt_sha256=sha(fp),error=e['error'],status='failed',result=None,usage=None,cost_estimate_usd=None,
    unknown_is_not_zero=True,retry=False,diagnosis='Final SSE stop and usage absent; not evidence of quota exhaustion')
put(D/'orchestration/MIMO_FAILURE.json',fail)
append(OUT/'LEDGER_016.jsonl',json.dumps(fail,ensure_ascii=False)+'\n')
data=dict(at=now,status='C4_ACTIVE',lean_theorems=19,all_trio=True,receipts=receipts,
    exact_CAS_checks=json.loads((D/'SECTION_CAS.json').read_bytes())['checks'],
    scope=['Concrete transverse frame transported by contract wedgeBoostMap','Two conjugate distinct circular polarizations',
           'Pointwise cocycle coboundary theorem; no AE diagonal substitution','Boost phase depends on frame gauge'],
    full_induced_helicity_representation=False,regional_modular_witness=False,gate_changed=False,
    pending=['Kimi AE strictification critique','DeepSeek KMS counterexample critique','Kimi C3 final review prepared'],
    opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'))
put(D/'CHECKPOINT_INITIAL.json',data)
state=ROOT/'A7/CONTINUIDADE.json';d=json.loads(state.read_bytes());d.update(at=now,status='ACTIVE',next=['Finish C4 cocycle scope and source critique','C5 KMS','C6 Q2 remainder','Part B and final audit'],
    pending_orchestration='MiMo46f terminal failed, no retry. Kimi8c777290 and DeepSeekaa091239 running last official report; Kimi b1751f8b final C3 critique prepared and sent to coordinator.',
    C4_checkpoint=str(D/'CHECKPOINT_INITIAL.json'))
put(state,d,True)
print(json.dumps(dict(theorems=19,cas_checks=data['exact_CAS_checks'],mimo='failed_no_retry')))
