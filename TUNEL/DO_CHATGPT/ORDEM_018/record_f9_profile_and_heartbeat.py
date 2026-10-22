"""Record static I05 acceptance and the bounded heartbeat, without science calls."""
from pathlib import Path
from datetime import datetime, timezone
import json
from audit_inputs import file_info, save_json, safe_write

ROOT = Path(__file__).resolve().parent
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
MEM = Path(r'C:\IALD\Central de Patentes\memory')
MARK = '<!-- ORDEM018_I05_ACCEPTED598_I02_PENDING_Q01_REVIEW_20261006 -->'


def replace_checked(path, before, after):
    backups_before = set(path.parent.glob(path.name + '.bak_*'))
    assert path.read_bytes() == before
    safe_write(path, after)
    assert path.read_bytes() == after
    new_backups = set(path.parent.glob(path.name + '.bak_*')) - backups_before
    assert len(new_backups) == 1
    backup = new_backups.pop()
    assert backup.read_bytes() == before
    return {'before_bytes': len(before), 'backup': file_info(backup), 'after': file_info(path)}


def update_json(path, edit):
    before = path.read_bytes()
    obj = json.loads(before)
    edit(obj)
    after = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    return replace_checked(path, before, after)


def main():
    out = ROOT / 'RECIBO_MEMORIA_PERFIS_HEARTBEAT_F9.json'
    assert not out.exists(), 'Already recorded; do not repeat.'
    now = datetime.now(timezone.utc).isoformat()
    profile_path = ROOT / 'RECIBO_ROOT_REVISAO_PERFIS_F9.json'
    profile = json.loads(profile_path.read_bytes())
    assert profile['status'] == 'STATIC_INDEPENDENT_REVIEW_ACCEPTED_NO_NUMERICAL_EXECUTION'
    assert len(profile['manifest_members_verified_by_root']) == 12
    for item in profile['manifest_members_verified_by_root']:
        actual = file_info(item['path'])
        assert all(actual[k] == item[k] for k in ('bytes', 'sha256'))
    qpath = ROOT / 'f9_precision_qualification_preparation/MANIFESTO_PREPARACAO.json'
    q = json.loads(qpath.read_bytes())
    qchecks = []
    for item in q['members']:
        actual = file_info(item['path'])
        assert Path(actual['path']).resolve().is_relative_to(qpath.parent.resolve())
        assert all(actual[k] == item[k] for k in ('bytes', 'sha256'))
        qchecks.append(actual)
    assert q['candidate_imports'] == q['controls_executed'] == 0
    req_path = ROOT / 'F9_NODE_COUPLING_PREPARATION_REQUEST.json'
    req = json.loads(req_path.read_bytes())
    dispatch_path = ROOT / 'F9_NODE_COUPLING_DISPATCH_RECEIPT.json'
    dispatch = json.loads(dispatch_path.read_bytes())
    assert not dispatch['dispatch']['isError']
    assert json.loads(dispatch['dispatch']['content'][0]['text'])['threadId'] == req['manager_thread_id']
    meta, occupancy = [json.loads(x) for x in dispatch['local_status_tool']['output'].splitlines()]
    pins = {key: file_info(p) for key, p in [
        ('profile_acceptance', profile_path), ('profile_intake', ROOT/'RECIBO_ROOT_INTAKE_PERFIS_F9.json'),
        ('node_request', req_path), ('node_dispatch', dispatch_path), ('Q01_preparation', qpath),
        ('I03_identity', ROOT/'f9_joint_covariance_preparation/IDENTIDADE_PREPARACAO.json')]}
    ledger_path = BASE / 'state/handoffs/slot_management.json'
    def ledger(d):
        assert d['pending_request'] == req['request_id']
        d['ordem018_F9_affine_profile_preparation'].update(
            status=profile['status'], root_review=pins['profile_acceptance'], review_map_sequence=596, acceptance_map_sequence=598)
        d['ordem018_F9_precision_qualification_preparation'] = {
            'request_id': q['request_id'], 'status': 'PREPARED_INDEPENDENT_REVIEW_PENDING_NO_EXECUTION',
            'manifest': pins['Q01_preparation'], 'root_verified_members': len(qchecks),
            'map_sequence': 597, 'review_agent': '/root/ordem018_proveniencia',
            'maximum_service_calls_proposed': q['maximum_service_calls'],
            'maximum_total_evaluations_proposed': q['maximum_total_evaluations'], 'consumed': False}
        d['ordem018_F9_joint_covariance_preparation'] = {
            'identity': pins['I03_identity'], 'status': 'PREPARATION_ACTIVE_NOT_DELIVERED',
            'agent': '/root/ordem018_preregistros', 'observed_reads': 0}
        d['ordem018_F9_node_coupling_preparation']['status'] = 'OFFICIAL_DISPATCH_ACKNOWLEDGED_MANAGER_IN_PROGRESS'
        d['manager_cursor'] = 'ca905f1b-d9cd-4a47-9f7e-cb2b71f4b405:122'
        d['manager_runtime_status'] = 'Official revision122: I02 preparation inProgress'
        d['next_action'] = 'Await concrete I02 and I03; review Q01. No repeated solicitation, provider retry, repin or observed-data release.'
    ledger_change = update_json(ledger_path, ledger)
    snapshot_change = update_json(ROOT/'SLOT_SNAPSHOT.json', lambda d: d.update(
        checked_at=meta['at'], nonterminal=occupancy['coordination_rows'], executions=occupancy['execution_rows'],
        next_state='needs_attention', metadata_status=pins['node_dispatch'],
        dispatch='Zero remote or Work calls. Old generation mismatch and operational source anchor preserved. I02 local preparation pending.'))
    note = f'''{MARK}
## 06/10/2026 UTC — I05 revisado; I02 atribuído; Q01 preparado

[REAL documental — mapas593/596/598] I05, perfis afins em θ fixo, entregue pela gerente e aceito após revisão estática independente sem bloqueador material. ROOT leu o parecer integral e conferiu12 membros entre pacote e revisão; as85 conferências do revisor são estáticas, não ensaios numéricos. H4 mantém B/A sem peso de prior; H5 varia apenas BAO em1/rd. Suporte e normalização reutilizam a987/df482. Estimativas factíveis ENGINEERING_ONLY, certificados condicionais UNAVAILABLE e mínimo global NOT_SEARCHED. Nenhuma importação ou execução do candidato. Recibo {pins['profile_acceptance']['path']} SHA256 {pins['profile_acceptance']['sha256']}.

[REAL documental — mapas594/597] I02 foi transferido da preparação planejada pela ROOT à gerente oficial, pedido {req['request_id']}, reconhecido pela ferramenta; revisão122 confirma inProgress. Fonte {pins['node_request']['path']} SHA256 {pins['node_request']['sha256']}. Objetivo concreto: ligar as APIs existentes por nó, um fundo comum para os cinco modelos, recibos verificáveis e claim durável antes de consumo futuro. Não duplicar I02. Q01, pedido {q['request_id']}, foi preparado e encaminhado à revisão independente: nove chamadas propostas, teto16433 avaliações, zero consumo. ROOT conferiu{len(qchecks)} membros do manifesto, incluindo backups; isso não aceita nem executa o protocolo. Manifesto {pins['Q01_preparation']['path']} SHA256 {pins['Q01_preparation']['sha256']}. I03 permanece em preparação por agente distinto.

[REAL operacional] Heartbeat consultou next primeiro e recebeu ValueError de geração canônica distinta; registrado needs_attention, não idle. Snapshot local em{meta['at']}: {len(occupancy['coordination_rows'])} coordenação antiga não terminal e{len(occupancy['execution_rows'])} execuções; limites5/3 e uma por provedor paralelo. Correção de estado ao lado: memória comum agora informa ready por SOURCE_ACCESS_UNAVAILABLE_USING_VERIFIED_SNAPSHOT; isso não restaura acesso aos originais nem valida a geração antiga. A âncora one_supercondutor.py continua divergente, sources.ok=false: vagas livres não são capacidade remota elegível. Gerente informada; nenhum provedor/Work, repin, substituição ou repetição. slot_management.json registra entrega I05 e pedido I02 pendente, sem cobrança duplicada.

[OPEN] MM permanece condicional; V1 e abertura observada dependem das decisões previstas na ORDEM018. Nenhum novo composto, likelihood, evidência, p, sigma, veredito físico, kernel, gate ou original científico foi produzido ou alterado nesta rodada. Unidades antigas consumidas/falhas/incertas continuam preservadas. F1/F3 abertas, F4 não pronta e objetivo ativo.'''
    changes = []
    for p in [MEM/n for n in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md')] + [
            ROOT/'ENTREGA_018_F1_HUBBLE.md', ROOT/'ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md']:
        old = p.read_bytes()
        assert MARK.encode() not in old
        new = old + ('\r\n\r\n'+note.replace('\n','\r\n')+'\r\n').encode('utf-8')
        changes.append(replace_checked(p, old, new))
        assert p.read_bytes().startswith(old) and p.read_bytes().count(MARK.encode()) == 1
    def continuity(d):
        d.update(updated_at=now,F9_affine_profile_acceptance=pins['profile_acceptance'],
                 F9_node_coupling_request=pins['node_request'],F9_node_coupling_dispatch=pins['node_dispatch'],
                 F9_precision_qualification_preparation=pins['Q01_preparation'],F9_joint_covariance_identity=pins['I03_identity'])
        d['milestone_sequences'] = sorted(set(d.get('milestone_sequences',[])+[593,594,596,597,598]))
        d['phases']['F1'] = 'THEORY_POINT_CONSUMED_ONCE; CONSUMER_PRIORS_PRECISION_THETA_AND_PROFILE_STATIC_ACCEPTED; REDUCER24_PASS_ONCE; I02_I03_PREPARATION; Q01_REVIEW_PENDING; OBSERVED_CLOSED'
        d['next_steps'] = [
            'Receive concrete I02 callback delivery from manager, without duplicate solicitation or science consumption.',
            'Receive I03 full covariance/family builder and independently review; preserve explicit missing inputs and all 600 labels.',
            'Finish independent Q01 review before a concrete ROOT execution decision; no retry of failed or consumed units.',
            'Consolidate actual V1 and operator decisions before observed-data release; F1/F3 open and F4 not ready.']
    continuity_change = update_json(ROOT/'CONTINUIDADE.json',continuity)
    save_json(out, {'at':now,'marker':MARK,'pins':pins,'memory_changes':changes,'ledger_change':ledger_change,
                    'snapshot_change':snapshot_change,'continuity_change':continuity_change,
                    'Q01_verified_members':qchecks,'new_remote_calls':0,'numerical_execution':0,
                    'backup_verification':'Each newly created backup matches immediately preceding bytes; append preserves whole prefix.'})
    def manifest(d):
        files = {Path(e['path']) for e in d['files']}
        files.update([Path(__file__).resolve(),out]+[Path(e['path']) for e in pins.values()])
        for folder in ('f9_affine_profile_preparation','proveniencia/revisao_f9_affine_profile','f9_precision_qualification_preparation'):
            files.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and '.bak_' not in p.name and '.tmp' not in p.name and '__pycache__' not in p.parts)
        assert all(p.resolve().is_relative_to(ROOT.resolve()) for p in files)
        d.update(updated_at=now,previous_snapshot=file_info(ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json'),
                 status='PARTIAL_PROFILE_STATIC_ACCEPTED_I02_I03_PREPARATION_Q01_REVIEW_PENDING',
                 files=[file_info(p) for p in sorted(files,key=lambda p:str(p).casefold())])
    manifest_change = update_json(ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json',manifest)
    verification = ROOT/'VERIFICACAO_MEMORIA_PERFIS_HEARTBEAT_F9.json'
    save_json(verification,{'at':now,'memory_receipt':file_info(out),'manifest_change':manifest_change,
                            'memory_surfaces_verified':len(changes),'all_immediate_backups_verified':True})
    print(json.dumps({'receipt':file_info(out),'verification':file_info(verification),'surfaces':len(changes),
                      'manifest':file_info(ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json')},ensure_ascii=False))


if __name__ == '__main__':
    main()
