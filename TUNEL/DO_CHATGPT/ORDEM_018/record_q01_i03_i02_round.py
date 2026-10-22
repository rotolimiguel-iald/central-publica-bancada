"""Persist verified local progress and queue status without running science."""
import json
from datetime import datetime, timezone
from pathlib import Path
from audit_inputs import file_info, safe_write, save_json

ROOT = Path(__file__).resolve().parent
MEM = Path(r'C:\IALD\Central de Patentes\memory')
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
MARK = '<!-- ORDEM018_Q01_PASS9_I03_ACCEPT_I02_REVIEW_20261006 -->'

def checked_replace(path, before, after):
    old_backups = set(path.parent.glob(path.name + '.bak_*'))
    assert path.read_bytes() == before, 'Concurrent change: ' + str(path)
    safe_write(path, after)
    new_backups = set(path.parent.glob(path.name + '.bak_*')) - old_backups
    assert len(new_backups) == 1
    backup = new_backups.pop()
    assert backup.read_bytes() == before and path.read_bytes() == after
    return {'before_bytes': len(before), 'backup': file_info(backup), 'after': file_info(path)}

def update_json(path, edit):
    before = path.read_bytes()
    obj = json.loads(before)
    edit(obj)
    after = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    return checked_replace(path, before, after)

def verify(pin):
    actual = file_info(pin['path'])
    assert all(actual[k] == pin[k] for k in ('bytes', 'sha256')), actual['path']
    return actual

def main():
    output = ROOT / 'RECIBO_MEMORIA_Q01_I03_I02.json'
    assert not output.exists(), 'Already recorded; no repeat.'
    now = datetime.now(timezone.utc).isoformat()
    qp = ROOT / 'RECIBO_ROOT_Q01_PASS9.json'
    q = json.loads(qp.read_bytes())
    assert q['status'] == 'ROOT_VERIFIED_Q01_PASS9_SINGLE_EXECUTION'
    assert q['consumed_once'] is True and q['retry_allowed'] is False
    assert q['case_count'] == q['service_invocations'] == 9
    assert all(c['status'] == 'PASS' for c in q['per_case_records'])
    assert sum(c['observed']['calls'] for c in q['per_case_records']) == q['observed_total_evaluations']
    qpins = [verify(q[k]) for k in ('external_receipt', 'terminal', 'result', 'claim', 'loaded_attestation', 'decision')]
    qpins += [verify(e) for e in q['preparation_members_unchanged'] + q['output_files']]
    cp = ROOT / 'RECIBO_ROOT_REVISAO_COVARIANCIA_F9.json'
    c = json.loads(cp.read_bytes())
    assert c['status'] == 'STATIC_INDEPENDENT_REVIEW_ACCEPTED_NO_NUMERICAL_EXECUTION'
    for e in c['manifest_members_verified_by_root'] + c['source_pins_verified_by_root']:
        verify(e)
    np = ROOT / 'RECIBO_ROOT_INTAKE_LIGACAO_F9.json'
    n = json.loads(np.read_bytes())
    for e in n['manifest_members_and_backups_verified'] + n['source_pins_verified']:
        verify(e)
    ap = ROOT / 'RECIBO_ROOT_REVISAO_LIGACAO_F9.json'
    accepted_i02 = ap.is_file()
    if accepted_i02:
        a = json.loads(ap.read_bytes())
        assert a['status'] == 'STATIC_INDEPENDENT_REVIEW_ACCEPTED_NO_NUMERICAL_EXECUTION'
        for e in a['manifest_members_verified_by_root']:
            verify(e)
    hp = ROOT / 'HEARTBEAT_Q01_I03_I02_TOOL_RECEIPT.json'
    h = json.loads(hp.read_bytes())
    meta, occupancy = [json.loads(line) for line in h['status_tool']['output'].splitlines()]
    heartbeat_receipt = json.loads(h['receipt_tool']['output'])
    assert heartbeat_receipt['state'] == 'needs_attention'
    pins = {k: file_info(p) for k, p in [('Q01', qp), ('I03', cp), ('I02_intake', np), ('heartbeat', hp), ('manager_notice', ROOT/'I02_I03_MANAGER_NOTICE_RECEIPT.json')]}
    if accepted_i02:
        pins['I02_acceptance'] = file_info(ap)
    i02_state = 'STATIC_INDEPENDENT_REVIEW_ACCEPTED_NO_NUMERICAL_EXECUTION' if accepted_i02 else 'DELIVERED_INDEPENDENT_REVIEW_PENDING'
    def ledger(d):
        assert d['ordem018_F9_node_coupling_preparation']['request_id'] == n['request_id']
        d['last_checked_at'] = meta['at']
        d['status'] = 'REMOTE_QUEUE_BLOCKED_LOCAL_PREPARATIONS_REVIEWED' if accepted_i02 else 'REMOTE_QUEUE_BLOCKED_LOCAL_I02_REVIEW'
        d['free_admission_slots'] = 5 - len(occupancy['coordination_rows'])
        d['free_execution_slots'] = 3 - len(occupancy['execution_rows'])
        d['pending_request'] = None if accepted_i02 else n['request_id']
        d['manager_cursor'] = 'ca905f1b-d9cd-4a47-9f7e-cb2b71f4b405:123'
        d['manager_runtime_status'] = 'Official revision123 completed; I02 delivery received, no duplicate request.'
        d['next_action'] = 'Determine bounded qualification of new joins after I02 review. Q01 scalar cases consumed; broader F1e Q01/Q02/Q03 remain open. No observed-data release or remote retry.'
        d['queue_read_error'] = dict(h['next'], at=meta['at'], receipt=pins['heartbeat'])
        d['effective_limits_verified'] = {'at': meta['at'], 'coordination': 5, 'executions': 3, 'per_parallel_provider': 1, 'parallel_providers': ['kimi', 'mimo', 'deepseek'], 'other_providers_exclusive': True, 'sources': [file_info(BASE/'iald_orchestrator'/f) for f in ('coordination.py','runtime.py','transport.py')]}
        d['provider_eligibility_observation'] = {'at': meta['at'], 'receipt': pins['heartbeat'], 'canonical_memory': meta['canonical_memory'], 'sources_ok': meta['sources']['ok'], 'providers': meta['providers'], 'ready_is_not_dispatch_eligibility': True, 'manager_informed': True, 'change_from_previous': 'No new provider eligibility or source authorization; I02 delivered locally.'}
        d['ordem018_F9_precision_qualification_preparation'].update(status='CONSUMED_Q01_PASS9_ONCE', root_result=pins['Q01'], consumed=True, retry_allowed=False, service_invocations=9, observed_evaluations=q['observed_total_evaluations'], scope='Nine scalar-service cases only; broader F1e Q01 new-join qualification remains open.')
        d['ordem018_F9_joint_covariance_preparation'].update(status=c['status'], root_review=pins['I03'], review_map_sequence=609, acceptance_map_sequence=611)
        d['ordem018_F9_node_coupling_preparation'].update(status=i02_state, root_intake=pins['I02_intake'], delivery_map_sequence=610, review_agent='/root/ordem018_proveniencia')
        if accepted_i02:
            d['ordem018_F9_node_coupling_preparation'].update(root_review=pins['I02_acceptance'], review_map_sequence=612, acceptance_map_sequence=613)
    ledger_change = update_json(BASE/'state/handoffs/slot_management.json', ledger)
    snapshot_change = update_json(ROOT/'SLOT_SNAPSHOT.json', lambda d: d.update(checked_at=meta['at'], nonterminal=occupancy['coordination_rows'], executions=occupancy['execution_rows'], next_state='needs_attention', next_error=h['next']['error'], metadata_status=pins['heartbeat'], provider_calls=0, dispatch='No remote/Work call. Original authorization/generation preserved. Local I02 delivered and independently reviewed or under review; no duplicate solicitation.'))
    i02_text = 'revisão independente aceita estaticamente, com limites documentados no recibo ROOT' if accepted_i02 else 'em revisão independente por ordem018_proveniencia'
    note = f'''{MARK}
## 06/10/2026 UTC — Q01 escalar PASS9; I03 aceita; I02 entregue

[REAL — execução local, mapas605/608] A unidade Q01 {q['request_id']} foi consumida UMA vez, após decisão ROOT e revisão independente: nove casos PASS, {q['observed_total_evaluations']} avaliações, {q['external_wall_seconds']:.6f}s no comando externo, exit{q['external_exit_code']}. Inclui cinco janelas gaussianas, polinômio positivo, orçamento insuficiente sem callback e exceção propagada sem repetição. O caso de orçamento curto P02 preserva converged=false como resultado esperado; PASS não significa convergência em todos os casos. Os erros permanecem estimados, sem certificado uniforme. Recibo {pins['Q01']['path']} SHA256 {pins['Q01']['sha256']}. Esta consolidação lê os recibos, NÃO executa novamente.

[ESCOPO] Q01 é o nome desta unidade dos serviços escalares, não conclusão de toda a dependência Q01 do quadro F1e. Transformações y/C, offsets, prefator/medida, priors, perfis, ligações e coleção completa ainda exigem qualificação delimitada própria. Q02/Q03 continuam abertos. Nenhuma observação cosmológica, likelihood científica, evidência, sigma ou veredito decorre do PASS9.

[REAL documental — mapas609/611] I03 aceita após leitura integral do parecer independente e conferência ROOT de15 membros e22 fontes;61 verificações documentais do revisor, sem bloqueador material. Builder de C nativa, nove blocos,36cross explícitos,600 rótulos e cincoMM; único transporte TCTᵀ fica no consumidor. Nenhuma matriz foi montada nesta revisão; PSD/posto/suporte/normalização e O01/O02 continuam condicionais. Recibo {pins['I03']['path']} SHA256 {pins['I03']['sha256']}.

[REAL documental — mapa610] I02 pedido {n['request_id']} entregue pela gerente oficial: oito membros, quatro backups e16 fontes conferidos por ROOT; {i02_text}. Adaptador por nó reaproveita montagem, priors e envelope theta; perfil opcional separado. Store POSIX e guard externos não estão qualificados por esta entrega. Não há launcher, AUTH/CLAIM científico, importação candidata, fundo novo ou observado aberto. Recibo de recepção {pins['I02_intake']['path']} SHA256 {pins['I02_intake']['sha256']}.

[REAL operacional] Heartbeat consultou next primeiro; o pedido Claude antigo continua incompatível com a geração autorizada. Recibo needs_attention, não idle. Estado em{meta['at']}: {len(occupancy['coordination_rows'])} coordenação não terminal, {len(occupancy['execution_rows'])} execuções; limites5/3/1. Memória comum ready somente pelo retrato verificado; âncora one_supercondutor.py ainda divergente (sources.ok=false). Vagas livres não tornam o despacho elegível. Gerente informada, pedido I02 entregue sem cobrança duplicada; zero chamadas remotas/Work nesta rodada, sem repin ou repetição de unidades.

[OPEN] F1/F3 seguem abertas e F4 não está pronta; objetivo ativo. Abertura observada exige V1 concreto por hash e decisão do operador. Nenhum kernel, gate ou original canônico alterado. A procedência separa execução Q01 local, revisões estáticas locais e entrega documental da gerente.'''
    if accepted_i02:
        note += f"\n\n[REAL documental] Aceite I02 em {pins['I02_acceptance']['path']} SHA256 {pins['I02_acceptance']['sha256']}. O controlador deve conferir compatibilidades antes de consumir o fundo; detecção tardia não é sucesso incorreto, mas pode consumir uma unidade. Não declara preflight ou runtime completo."
    changes = []
    for path in [MEM/f for f in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md')] + [ROOT/'ENTREGA_018_F1_HUBBLE.md',ROOT/'ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md']:
        before = path.read_bytes()
        assert MARK.encode() not in before
        after = before + ('\r\n\r\n'+note.replace('\n','\r\n')+'\r\n').encode('utf-8')
        changes.append(checked_replace(path,before,after))
        assert path.read_bytes().startswith(before) and path.read_bytes().count(MARK.encode()) == 1
    def continuity(d):
        d.update(updated_at=now,F9_precision_qualification_result=pins['Q01'],F9_joint_covariance_acceptance=pins['I03'],F9_node_coupling_intake=pins['I02_intake'],F9_node_coupling_status=i02_state)
        if accepted_i02:
            d['F9_node_coupling_acceptance'] = pins['I02_acceptance']
        d['milestone_sequences'] = sorted(set(d.get('milestone_sequences',[])+[601,602,605,608,609,610,611,612,613]))
        d['phases']['F1'] = 'THEORY_POINT_CONSUMED_ONCE; SCALAR_Q01_PASS9_ONCE; I03_STATIC_ACCEPTED; I02_'+('STATIC_ACCEPTED' if accepted_i02 else 'REVIEW_PENDING')+'; FULL_JOINT_QUALIFICATION_OPEN; OBSERVED_CLOSED'
        d['next_steps'] = ['Complete independent I02 review if still pending; no duplicate implementation or consumption.', 'Prepare concrete bounded qualification of newly connected consumer/prior/profile/covariance interfaces; scalar Q01 is already consumed and does not close the whole F1e Q01 dependency.', 'Preserve Q02/Q03 physical-domain and joint-geometry qualification dependencies and O01/O02/O03/O04 decisions.', 'Consolidate actual V1 before operator decision to open observed data; F1/F3 open, F4 not ready.']
    continuity_change = update_json(ROOT/'CONTINUIDADE.json',continuity)
    save_json(output,{'at':now,'marker':MARK,'pins':pins,'memory_changes':changes,'ledger_change':ledger_change,'snapshot_change':snapshot_change,'continuity_change':continuity_change,'Q01_pin_checks':qpins,'I02_static_accepted':accepted_i02,'scope':'Recording and byte verification only; no new scientific execution, observed reads, remote provider calls or Work assistance.'})
    def manifest(d):
        files={Path(e['path']) for e in d['files']}
        files.update([Path(__file__).resolve(),output]+[Path(e['path']) for e in pins.values()])
        for folder in ('f9_precision_qualification_preparation','proveniencia/revisao_f9_precision_qualification','f9_joint_covariance_preparation','derivacoes/revisao_f9_joint_covariance','f9_node_coupling_preparation','proveniencia/revisao_f9_node_coupling'):
            files.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and '.bak_' not in p.name and '.tmp' not in p.name and '__pycache__' not in p.parts)
        assert all(p.resolve().is_relative_to(ROOT.resolve()) for p in files)
        d.update(updated_at=now,previous_snapshot=file_info(ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json'),status='PARTIAL_Q01_SCALAR_PASS9_I03_STATIC_ACCEPTED_I02_'+('STATIC_ACCEPTED' if accepted_i02 else 'REVIEW_PENDING'),files=[file_info(p) for p in sorted(files,key=lambda p:str(p).casefold())])
    manifest_change=update_json(ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json',manifest)
    vp=ROOT/'VERIFICACAO_MEMORIA_Q01_I03_I02.json'
    save_json(vp,{'at':now,'memory_receipt':file_info(output),'manifest_change':manifest_change,'memory_surfaces_verified':len(changes),'immediate_byte_backups_verified':True,'append_prefixes_preserved':True})
    print(json.dumps({'receipt':file_info(output),'verification':file_info(vp),'manifest':file_info(ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json'),'I02_static_accepted':accepted_i02,'surfaces':len(changes)},ensure_ascii=False))

if __name__ == '__main__':
    main()
