from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT.parent/'TUNEL/DO_CHATGPT'
BASE = ROOT.parent/'IALD_ORQUESTRACAO_20260923'
DEST = HERE/'orchestration_reviews_20260924'
sys.path.insert(0, str(BASE))
from iald_orchestrator.coordination import Coordination
sys.path.insert(0, str(ROOT/'A0'))
from auditar_axiomas import audita

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def save(path, raw):
    if isinstance(raw, str): raw=raw.encode('utf-8')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if path.exists():
        before=path.read_bytes()
        backup=path.with_name(path.name+'.bak_'+stamp)
        with backup.open('xb') as stream: stream.write(before)
        assert backup.read_bytes()==before
    tmp=path.with_name(path.name+'.tmp_'+stamp)
    with tmp.open('xb') as stream: stream.write(raw)
    assert raw and tmp.read_bytes()==raw
    tmp.replace(path)

def dump(path,obj): save(path,json.dumps(obj,ensure_ascii=False,indent=2))

coord=Coordination()
j=coord.get('f8ec22e7-21c2-4bf4-b3bc-29655e681481')
assert j['stage']=='completed'
e=j['execution']; result=e['result']; answer=result['text']
save(DEST/'kimi_a3_faithfulness_response.md',answer)
manifest_path=ROOT/'A3/translation_operator_faithfulness_manifest.json'
manifest=json.loads(manifest_path.read_bytes())
checks=[]
for proof in manifest['proofs']:
    src=Path(proof['source']); log=Path(proof['audit']['log'])
    assert sha(src.read_bytes())==proof['source_sha256']
    assert sha(log.read_bytes())==proof['log_sha256']
    audit=audita(str(src),str(log))
    assert audit['auditoria']=='PASSA' and proof['receipt']['rc']==0
    checks.append(dict(source=str(src),source_sha256=sha(src.read_bytes()),
                       log_sha256=sha(log.read_bytes()),audit=audit['auditoria'],
                       declarations=audit['n_declaracoes_auditadas']))
assert sum(p['declarations'] for p in checks)==23
at=datetime.now(timezone.utc).isoformat()
review=dict(at=at,status='REAL_LOCAL_REVIEW_OF_DECLARED_PROVIDER_OUTPUT',
    job_id=j['id'],execution_id=j['execution_task_id'],model=result.get('model'),
    answer_sha256=sha(answer.encode('utf-8')),usage=result.get('usage'),
    explicit_cost_usd=None,cost_note='No explicit monetary cost in this result; do not assume zero.',
    canonical_memory_receipt=result.get('canonical_memory'),
    existing_manifest_sha256=sha(manifest_path.read_bytes()),existing_proof_checks=checks,
    accepted='Pointwise phase faithfulness requires an a.e. operator-to-pointwise bridge.',
    already_implemented='23 audited declarations in UnitMultiplierIdentity, OrbitalMeasureSupport_v2 and OrbitalTranslationOperators_v2; no new duplication.',
    rejected='Counterexample section 2.2: making W measure-zero does not imply phase=1 on its complement.',
    fresh_compilation=False,kernel_or_gate_changes=False)
dump(DEST/'kimi_a3_faithfulness_review.json',review)
ledger=OUT/'LEDGER_016.jsonl'; prior=ledger.read_bytes()
entries=[json.loads(line) for line in prior.decode('utf-8-sig').splitlines() if line.strip()]
if not any(x.get('event')=='executor_result_reviewed' and x.get('execution_id')==j['execution_task_id'] for x in entries):
    event=dict(ts=at,event='executor_result_reviewed',provedor='kimi',alvo='A-3',
        ramo='skeptic_operator_faithfulness_from_orbit',job_id=j['id'],
        request_id=j['request_id'],execution_id=j['execution_task_id'],
        question_sha256=sha(j['prompt'].encode('utf-8')),answer_sha256=sha(answer.encode('utf-8')),
        usage=result.get('usage'),custo_usd=None,desfecho='completed_reviewed_partial_acceptance_no_duplicate_proofs')
    save(ledger,prior+(json.dumps(event,ensure_ascii=False)+'\n').encode('utf-8'))

polar=coord.get('4f01bd55-230e-4510-be80-742372dd74b2')
assert polar['request_id']=='5c6322c7-b76e-4381-ac02-7955eedbecc9'
polar_path=DEST/'kimi_polar_geometry_scope_receipt.json'
receipt=json.loads(polar_path.read_bytes())
receipt.update(job_id=polar['id'],status=polar['stage'],registered_at=polar['created_at'],
    registered_by='coordinator_thread', prior_local_capacity_refusal_preserved=True)
dump(polar_path,receipt)
entries=[json.loads(line) for line in ledger.read_bytes().decode('utf-8-sig').splitlines() if line.strip()]
if not any(x.get('job_id')==polar['id'] for x in entries):
    event=dict(ts=at,event='coordination_registered_by_coordinator',provedor='kimi',alvo='A-4',
        ramo='A-4k.2',lemma_id='kimi_polar_geometry_scope',job_id=polar['id'],
        request_id=polar['request_id'],question_sha256=sha(polar['prompt'].encode('utf-8')),
        answer_sha256=None,custo_usd=None,desfecho=polar['stage'])
    save(ledger,ledger.read_bytes()+(json.dumps(event,ensure_ascii=False)+'\n').encode('utf-8'))
report=OUT/'ENTREGA_016_ORQUESTRACAO_reforco_A4_Kimi_MiMo.md'
adendo=(f'\n## Adendo {at}\n\n'
    f'A segunda unidade Kimi foi registrada pela coordenação: `{polar["id"]}`, '
    f'estado `{polar["stage"]}`. Mantido o request_id original; a recusa local anterior '
    'permanece em seu recibo. A unidade MiMo A4 segue preparada para a próxima vaga.\n\n'
    'A revisão Kimi A3 anterior concluiu: 317451 tokens de entrada, 14012 de saída, '
    '331463 totais. A ponte sugerida já existe em 23 declarações cujas fontes/logs foram '
    'novamente conferidos nesta rodada, sem nova compilação. Nenhuma reimplementação. '
    'O contraexemplo §2.2 foi rejeitado: retirar um aberto do suporte não torna a fase '
    'identicamente 1 no complemento. Resposta preservada com correção ao lado.\n')
save(report,report.read_bytes()+adendo.encode('utf-8'))
print(json.dumps(dict(reviewed_job=j['id'],existing_declarations=23,
    polar_registered=polar['id'],polar_stage=polar['stage'],usage=result.get('usage')),ensure_ascii=False))
