"""Record completed logical cases and static reviews; never run scientific code."""
from pathlib import Path
from datetime import datetime, timezone
import json
import sqlite3
from audit_inputs import file_info, save_json, safe_write

ROOT = Path(__file__).resolve().parent
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
MEM = Path(r'C:\IALD\Central de Patentes\memory')
MARK = '<!-- ORDEM018_F9_LOGIC584_REVIEWS585586_PROFILE588_20261006 -->'

def update(path, edit):
    before = path.read_bytes()
    value = json.loads(before)
    edit(value)
    assert path.read_bytes() == before
    save_json(path, value)

def main():
    out = ROOT / 'RECIBO_MEMORIA_REDUTOR_INTEGRACOES_F9.json'
    assert not out.exists()
    now = datetime.now(timezone.utc).isoformat()
    logic_path = ROOT / 'RECIBO_ROOT_REDUTOR_F9_PASS24.json'
    logic = json.loads(logic_path.read_bytes())
    tool_path = ROOT / 'F9_DECISION_LOGIC_TOOL_RECEIPT.json'
    tool = json.loads(tool_path.read_bytes())
    assert tool['exit_code'] == 0 and logic['checks_passed'] == 24
    assert logic['status'] == 'ROOT_VERIFIED_PASS24_LOGICAL_CASES_ONCE'
    reviews_path = ROOT / 'RECIBO_ROOT_REVISOES_PRECISAO_THETA_F9.json'
    reviews = json.loads(reviews_path.read_bytes())
    assert reviews['status'] == 'STATIC_REVIEWS_585_586_ACCEPTED_NO_NUMERICAL_EXECUTION'
    request_path = ROOT / 'F9_AFFINE_PROFILE_PREPARATION_REQUEST.json'
    request = json.loads(request_path.read_bytes())
    ack_path = ROOT / 'F9_AFFINE_PROFILE_DISPATCH_RECEIPT.json'
    ack = json.loads(ack_path.read_bytes())
    assert ack.get('isError') is False
    assert json.loads(ack['content'][0]['text'])['threadId'] == request['manager_thread_id']
    pins = {name: file_info(path) for name, path in (
        ('logic', logic_path), ('tool', tool_path), ('reviews', reviews_path),
        ('profile_request', request_path), ('profile_dispatch', ack_path),
        ('dependencies', ROOT/'preregistros/f9_completion_dependencies/MANIFESTO_ENTREGA.json'),
        ('metadata', ROOT/'ORCHESTRATOR_METADATA_F9_LOGIC_ROUND.json'))}
    with sqlite3.connect((BASE/'state/tasks.sqlite3').as_uri()+'?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        jobs = [dict(x) for x in db.execute("SELECT id,request_id,stage,execution_task_id,execution_constraints FROM coordination_jobs WHERE stage NOT IN ('completed','failed','cancelled') ORDER BY created_at,id")]
        tasks = [dict(x) for x in db.execute("SELECT id,status FROM tasks WHERE status IN ('queued','running') ORDER BY created_at,id")]
        blocks = [dict(x) for x in db.execute('SELECT * FROM provider_blocks')]
    ledger_path = BASE/'state/handoffs/slot_management.json'
    def ledger(d):
        for e in d['effective_limits_verified']['sources']:
            actual = file_info(e['path'])
            assert all(actual[k] == e[k] for k in ('bytes', 'sha256'))
        # Restore the structured diagnostic if a recent metadata update flattened it.
        if not isinstance(d.get('queue_read_error'), dict):
            original = None
            for backup in sorted(ledger_path.parent.glob('slot_management.json.bak_*'), reverse=True):
                candidate = json.loads(backup.read_bytes()).get('queue_read_error')
                if isinstance(candidate, dict):
                    original = candidate
                    break
            assert original is not None
            d['queue_read_error'] = original
        d['queue_read_error'].update(at=now, receipt='needs_attention', dispatch='none', current_error='Geração canônica diferente da autorizada no pedido.')
        d['effective_limits_verified']['at'] = now
        d.update(last_checked_at=now, free_admission_slots=5-len(jobs), free_execution_slots=3-len(tasks),
                 pending_request=request['request_id'], manager_cursor='ca905f1b-d9cd-4a47-9f7e-cb2b71f4b405:120',
                 manager_runtime_status='Official revision120: concrete affine profile preparation inProgress')
        d['ordem018_F9_precision_services_preparation'].update(status='STATIC_INDEPENDENT_REVIEW_ACCEPTED_NO_EXECUTION', root_review=pins['reviews'], delivery_map_sequence=578, review_map_sequence=586)
        d['ordem018_F9_theta_integration_preparation'] = {
            'request_id':'ad02511d-1536-4a1b-a6c4-fb3e5eb26550',
            'manifest':file_info(ROOT/'f9_theta_integration_preparation/MANIFESTO_PREPARACAO.json'),
            'status':'STATIC_INDEPENDENT_REVIEW_ACCEPTED_NO_EXECUTION','root_review':pins['reviews'],
            'delivery_map_sequence':580,'review_map_sequence':585}
        d['ordem018_F9_decision_reducer'] = {
            'request_id':logic['request_id'],'status':'CONSUMED_PASS24_LOGICAL_CASES_ONCE',
            'root_receipt':pins['logic'],'tool_receipt':pins['tool'],'result_map_sequence':584,
            'statistical_calibration':False,'observed_reads':0,'science_calls':0,'retry_allowed':False}
        d['ordem018_F9_completion_dependencies'] = {'status':'DOCUMENTARY_DELIVERY_INTEGRITY_VERIFIED', 'manifest':pins['dependencies'], 'delivery_map_sequence':579}
        d['ordem018_F9_affine_profile_preparation'].update(status='OFFICIAL_DISPATCH_ACKNOWLEDGED_MANAGER_IN_PROGRESS', dispatch_receipt=pins['profile_dispatch'], map_sequence=588)
        meta = json.loads((ROOT/'ORCHESTRATOR_METADATA_F9_LOGIC_ROUND.json').read_bytes())
        d['provider_eligibility_observation'].update(at=now, receipt=pins['metadata'], canonical_memory=meta['canonical_memory'], sources_ok=meta['sources']['ok'])
        d['ordem018_discriminante_slot_request']['latest_check'] = {
            'at':now,'queue_state':'needs_attention','nonterminal':len(jobs),'active_executions':len(tasks),
            'provider_calls':0,'work_calls':0,'useful_local_work':'Logical cases consumed; precision/theta reviews accepted; concrete affine profile request acknowledged.'}
    update(ledger_path, ledger)
    update(ROOT/'SLOT_SNAPSHOT.json', lambda d: d.update(
        checked_at=now, nonterminal=jobs, executions=tasks, provider_blocks=blocks,
        next_state='needs_attention', metadata_status=pins['metadata'],
        dispatch='No remote/Work calls. Local static work and one invented-record logical unit only; new concrete affine profile preparation is pending.'))
    note = f'''{MARK}
## 06/10/2026 UTC — Redutor lógico verificado; serviços e integral θ revisados

[REAL computacional — mapas581/583/584] bf6d passou os24 casos lógicos inventados em uma única execução, saída externa0. ROOT conferiu24 nomes distintos, claim, fonte/driver e cinco membros selados intactos. Recibo {pins['logic']['path']} SHA256 {pins['logic']['sha256']}. Testados completude, H1 OR/AND, direção, máximo por cenários e Bonferroni5 em log; underflow não vira p=0. Não houve dado observado, calibração estatística, likelihood, solver ou veredito físico. As referências fictícias são identificadas como tal; não autenticam certificados. Unidade consumida, sem repetição.

[REAL documental — mapas578/580/585/586/588] Entregas f820 (dois serviços de precisão) e ad025 (integrador θ) recebidas e revisadas independentemente; ROOT leu os dois pareceres e conferiu11/22 membros entre pacotes e respectivas revisões. Nenhum bloqueador material no recorte ENGINEERING_ONLY. Recibo {pins['reviews']['path']} SHA256 {pins['reviews']['sha256']}. Nenhuma dessas duas implementações foi importada ou executada nesta rodada. Estimadores não são certificados uniformes; picos não amostrados permanecem sem cota. Correções documentais ao lado: J é integral positiva cujo log o callback transporta; O(NlogN) descreve organização da fila, não teto geral demonstrado perante recomposições lineares.

[REAL documental — mapa579] Quadro F1e recebido com13 dependências (6 implementação,3 qualificação futura,4 decisões),38 fontes pinadas e44 conferências declaradas no recibo; ROOT verificou8 membros do manifesto. Fonte {pins['dependencies']['path']} SHA256 {pins['dependencies']['sha256']}. A seq577 era seu corte: as entregas/revisões posteriores aqui registradas substituem somente o estado pendente dessas peças, sem alterar o quadro selado. Ligação das APIs, builder C/família e perfil/estimativas continuam necessários; não repetir controles já consumidos nem exigir certificado uniforme para toda preparação de engenharia.

[REAL operacional — mapa588] Nova dependência concreta I05 atribuída oficialmente à gerente: {request['request_id']}, perfil dos extras em θ fixo reutilizando a geometria gaussiana; H4 usa B/A para likelihood, sem o deslocamento de prior. Pedido {pins['profile_request']['path']} SHA256 {pins['profile_request']['sha256']}; ferramenta confirmou envio, revisão120 da tarefa indica inProgress. Preparação somente, sem importação, ensaio numérico, solver, observados, WSL, rede, AUTH/CLAIM ou alegação de mínimo global. Solicitação pendente no ledger; não cobrar novamente sem mudança.

[REAL operacional] Fila remota mantém needs_attention: {len(jobs)} coordenação não terminal, {len(tasks)} execuções, limites5/3 e uma por provedor paralelo. Memória/fontes impedem despacho; ready não significa elegível. Nenhum provedor ou Work acionado, repin ou fallback. MM condicional; V1 não ratificada, observados fechados. F1/F3 abertos e F4 não pronta; objetivo ativo. c435, ffd6, NC02 e demais controles consumidos preservados. Nenhum kernel/gate/original científico alterado.'''
    changes = []
    paths = [MEM/n for n in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md')]+[
        ROOT/'ENTREGA_018_F1_HUBBLE.md',ROOT/'ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md']
    for path in paths:
        old = path.read_bytes()
        assert MARK.encode() not in old
        new = old + ('\r\n\r\n'+note.replace('\n','\r\n')+'\r\n').encode('utf-8')
        assert path.read_bytes() == old
        safe_write(path,new)
        assert path.stat().st_size > len(old)
        changes.append({'before_bytes':len(old),'after':file_info(path)})
    def continuity(d):
        d.update(updated_at=now,F9_decision_reducer_result=pins['logic'],F9_precision_theta_static_reviews=pins['reviews'],
                 F9_completion_dependencies=pins['dependencies'],F9_affine_profile_request=pins['profile_request'],
                 F9_affine_profile_dispatch=pins['profile_dispatch'])
        d['milestone_sequences'] = sorted(set(d.get('milestone_sequences',[])+[575,576,577,578,579,580,581,582,583,584,585,586,588]))
        d['phases']['F1'] = 'THEORY_POINT_AND_FIVE_MODELS_COMPUTED_ONCE; CONSUMER_PRIORS_PRECISION_THETA_STATIC_ACCEPTED; REDUCER24_LOGICAL_CASES_PASS_ONCE; AFFINE_PROFILE_PREPARATION_ACTIVE; OBSERVED_COMPOSITE_CLOSED'
        d['next_steps'] = [
            'Prepare I02 concrete callback connecting existing engine/assembly/consumer/priors/precision/theta interfaces; preserve full-grid admission and durable node identity.',
            'Prepare I03 full joint covariance/scenario builder from explicit injected inputs; no observed references or inferred cross-block zeros.',
            'Receive/review concrete I05 affine profile preparation4eea, without repeated solicitation or numeric execution.',
            'Qualify only new joins in specifically bounded units; consolidate actual V1 before operator ratification/data decision. F1/F3 open, F4 not ready.']
    update(ROOT/'CONTINUIDADE.json',continuity)
    save_json(out,{'at':now,'marker':MARK,'pins':pins,'changes':changes,
                   'continuity':file_info(ROOT/'CONTINUIDADE.json'),'ledger':file_info(ledger_path),
                   'backup_policy':'Immediate exact-byte same-folder backups; verified temporary replacement and compare-before-write.'})
    def manifest(d):
        files = {Path(e['path']) for e in d['files']}
        files.update([Path(__file__).resolve(),out]+[Path(e['path']) for e in pins.values()])
        folders = ['f9_decision_reducer_preparation','proveniencia/revisao_f9_decision_reducer',
                   'f9_precision_services_preparation','derivacoes/revisao_f9_precision_services',
                   'f9_theta_integration_preparation','preregistros/revisao_f9_theta_integration',
                   'preregistros/f9_completion_dependencies']
        for folder in folders:
            files.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and '.bak_' not in p.name and '.tmp' not in p.name and '__pycache__' not in p.parts)
        assert all(p.resolve().is_relative_to(ROOT.resolve()) for p in files)
        d.update(updated_at=now,previous_snapshot=file_info(ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json'),
                 status='PARTIAL_F9_LOGIC24_PASS_PRECISION_THETA_STATIC_ACCEPTED_PROFILE_PREPARATION_ACTIVE',
                 files=[file_info(p) for p in sorted(files,key=lambda p:str(p).casefold())])
    update(ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json',manifest)
    print(json.dumps({'memory_receipt':file_info(out),'manifest':file_info(ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json'),
                      'nonterminal':len(jobs),'active_executions':len(tasks),'surfaces':len(changes)},ensure_ascii=False))

if __name__ == '__main__':
    main()
