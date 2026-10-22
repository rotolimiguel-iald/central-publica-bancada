"""Prepare a documentary report; never import or execute scientific candidates."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
NOW = datetime.now(timezone.utc).isoformat()
CFG = json.loads((HERE / 'ESCOPO_E_COBERTURA.json').read_text(encoding='utf-8-sig'))
CAT = json.loads((HERE / 'CATALOGO_ROTAS_E_SEQS.json').read_text(encoding='utf-8-sig'))
ADDENDUM = json.loads((HERE / 'ADENDO_MAPA_I02_664.json').read_text(encoding='utf-8-sig'))['record']
for route in CAT['routes']:
    if route['route_id'] == ADDENDUM['rota_id'] and not any(r['seq'] == ADDENDUM['seq'] for r in route['records']):
        route['records'].append({'seq': ADDENDUM['seq'], 'record_sha': ADDENDUM['sha'],
            'title': ADDENDUM['titulo'], 'result': ADDENDUM['resultado'], 'status': ADDENDUM['status']})
OPENING = json.loads((HERE / 'ADENDO_ABERTURA_VERIFICADA.json').read_text(encoding='utf-8'))
OPENING_MAP = json.loads((HERE / 'ADENDO_MAPA_ABERTURA_665.json').read_text(encoding='utf-8'))['data']
CAT['routes'].append({'route_id': OPENING_MAP['rota']['rota_id'], 'records': OPENING_MAP['registros']})

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def pin(path):
    p = Path(path)
    data = p.read_bytes()
    return {'path': str(p.resolve()), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def safe_write(name, value):
    target = HERE / name
    assert target.parent.resolve() == HERE
    data = (value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2))
    blob = (data.rstrip() + '\n').encode('utf-8')
    if target.exists():
        old = target.read_bytes()
        backup = target.with_name(target.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temp = target.with_name(target.name + '.tmp')
    with temp.open('xb') as handle:
        handle.write(blob)
        handle.flush()
        os.fsync(handle.fileno())
    assert temp.read_bytes() == blob and len(blob) > 0
    os.replace(temp, target)
    assert target.read_bytes() == blob

def link(name, label=None):
    p = Path(name)
    if not p.is_absolute():
        p = ROOT / p
    return '[' + (label or p.name) + '](<' + p.as_posix() + '>)'

def records(obj):
    if isinstance(obj, dict):
        if ('path' in obj or 'caminho' in obj) and isinstance(obj.get('sha256'), str):
            yield obj
        for val in obj.values():
            yield from records(val)
    elif isinstance(obj, list):
        for val in obj:
            yield from records(val)

evidence, missing = [], []
for name in CFG['evidence_files']:
    try:
        evidence.append({'reference': name, **pin(ROOT / name)})
    except (OSError, ValueError) as exc:
        missing.append({'reference': name, 'status': 'READ_FAILURE', 'error': str(exc)})

# Bounded integrity checks only. No candidate is imported or evaluated.
expected = []
for row in OPENING['records']:
    expected.append(('ADENDO_ABERTURA_VERIFICADA.json', row['source']))
for name, key in [
    ('proveniencia/REVISAO_CONSOLIDACAO_F0_F2_RECIBO.json', 'files'),
    ('proveniencia/REVISAO_CONSOLIDACAO_F0_F2_CORRECOES.json', 'sources'),
    ('preregistros/fase8_reconciliacao_v1/MANIFESTO_RECONCILIACAO.json', 'members'),
    ('f9_i02_preflight_independent_review_root/MANIFESTO_REVISAO.json', 'files'),
    ('COMPARACAO_ESPECIFICACOES_F9.json', 'sources'),
]:
    for rec in read_json(ROOT / name)[key]:
        if 'sha256' in rec:
            expected.append((name, rec))

# F8 contracts and the exact reconciliation sources are hash-only reads.
f8 = read_json(ROOT / 'preregistros/fase8_reconciliacao_v1/AUDITORIA_BYTES_E_FONTES.json')
for row in f8['manifest_member_checks']:
    expected.append(('F8 prior manifest member check', row['actual']))

checks = []
for origin, item in expected:
    p = item.get('path', item.get('caminho'))
    try:
        actual = pin(p)
        checks.append({'source_receipt': origin, 'expected': item, 'actual': actual,
                       'matches': actual['sha256'] == item['sha256'] and
                       ('bytes' not in item or actual['bytes'] == item['bytes'])})
    except (OSError, ValueError) as exc:
        checks.append({'source_receipt': origin, 'expected': item, 'matches': False,
                       'status': 'NOT_RECHECKED_READ_FAILURE', 'error': str(exc)})
safe_write('CONFERENCIA_PINS.json', {'at': NOW, 'scope': 'Bytes only; no scientific execution',
    'checks': checks, 'all_matches': all(x['matches'] for x in checks)})

# Preserve primary-source references as given by existing receipts. Hash only
# documentary bodies; do not reopen tables, covariance arrays, chains or centres.
primary = []
for manifest in ['FONTES_PUBLICAS.json', 'FONTES_ATUALIZACAO_F0.json',
                 'FONTES_PUBLICAS_ADICIONAIS.json', 'FONTE_SIMONS.json',
                 'proveniencia/MANIFESTO_FONTES_F1.json',
                 'derivacoes/F2_FONTES_SHA256.json',
                 'preregistros/primordial/FONTES_PRIMARIAS.json']:
    for rec in records(read_json(ROOT / manifest)):
        p = Path(rec.get('path', rec.get('caminho')))
        if not p.is_absolute():
            p = (ROOT / manifest).parent / p
        out = {'receipt': manifest, 'recorded': rec,
               'content_status': 'PRIMARY_READING_ATTRIBUTED_TO_SOURCE_AUDIT_NOT_REPEATED'}
        if p.suffix.lower() in {'.html', '.tex', '.docx', '.md'}:
            try:
                out['actual'] = pin(p)
                out['identity_matches'] = out['actual']['sha256'] == rec['sha256']
            except (OSError, ValueError) as exc:
                out['identity_status'] = 'NOT_RECHECKED_READ_FAILURE'
                out['error'] = str(exc)
        else:
            out['identity_status'] = 'DOCUMENTARY_RECEIPT_ONLY_NO_DATA_BODY_OPENING'
        primary.append(out)
safe_write('FONTES_EVIDENCIAS.json', {'at': NOW, 'evidence': evidence, 'missing': missing,
    'primary_sources': primary, 'no_observed_data_reopened': True,
    'meaning': 'A valid hash identifies bytes; it does not independently establish scientific truth.'})

# Acknowledged local dispatch != a remote provider execution.
mapping = {
 'F9_AFFINE_PROFILE_DISPATCH_RECEIPT.json':'F9_AFFINE_PROFILE_PREPARATION_REQUEST.json',
 'F9_PRECISION_SERVICES_DISPATCH_RECEIPT.json':'F9_PRECISION_SERVICES_PREPARATION_REQUEST.json',
 'F9_NODE_COUPLING_DISPATCH_RECEIPT.json':'F9_NODE_COUPLING_PREPARATION_REQUEST.json',
 'F9_NEXT_JOIN_QUALIFICATION_DISPATCH_RECEIPT.json':'F9_NEXT_JOIN_QUALIFICATION_REQUEST.json',
}
dispatches = []
for p in sorted(ROOT.glob('*DISPATCH_RECEIPT.json')):
    d = read_json(p)
    rid = d.get('request_id')
    request_file = None
    if rid is None and p.name in mapping:
        request_file = ROOT / mapping[p.name]
        rid = read_json(request_file)['request_id']
    ack = any(k in d for k in ['official_ack','official_send_ack','official_send','response','tool_result','dispatch','content'])
    dispatches.append({'request_id': rid, 'nature': 'LOCAL_CODEX_THREAD_COORDINATION',
        'acknowledged_dispatch': ack, 'receipt': pin(p),
        'request_identity_source': pin(request_file) if request_file else 'receipt request_id',
        'work_assistance_used': d.get('Work_assistance_used', 'NOT_ESTABLISHED_BY_THIS_RECEIPT'),
        'remote_execution_inferred': False,
        'note': 'Dispatch is recorded, not a claim that the requested work has completed.'})
slot = read_json(ROOT / 'SLOT_SNAPSHOT.json')
registry = read_json(ROOT / 'F0_RANKING_REGISTRY.json')
safe_write('DESPACHOS_VERIFICADOS.json', {'at': NOW, 'local_dispatches': dispatches,
    'remote_snapshot': {'at': slot['checked_at'], 'pending': slot['nonterminal'],
       'executions': slot['executions'], 'provider_calls': slot['provider_calls'],
       'error': slot['next_error'], 'limits': slot['limits'],
       'scope': 'This queue snapshot only; not a claim about all historical account activity.'},
    'prepared_not_dispatched_request_ids': registry.get('prepared_not_dispatched_request_ids'),
    'remote_calls_in_current_preparation': 0, 'Work_in_current_preparation': False})

routes = {r['route_id']: r for r in CAT['routes']}
assert {r['route'] for r in registry['routes']} == set(CFG['route_links'])
coverage_routes = []
for item in registry['routes']:
    rid = item['route']
    refs = [{'route_id': r, 'seqs': [z['seq'] for z in routes[r]['records']]}
            for r in CFG['route_links'][rid]]
    coverage_routes.append({'route': rid, 'ranking_as_reviewed': item,
                            'current_documentary_reading': CFG['route_updates'][rid], 'map_history': refs})
safe_write('COBERTURA_REQUISITOS.json', {'at': NOW, 'request_id': CFG['request_id'],
    'status': 'REPORT_UNDER_CONSTRUCTION_NOT_FINAL', 'requirements': CFG['phases'],
    'routes': coverage_routes, 'extra_route_R_N': 'OPEN_NO_QUANTITATIVE_PRIMORDIAL_GW_PREDICTION_IN_ADENDUM',
    'operator_decisions': CFG['decisions'], 'scientific_execution': False})

text = (HERE / 'CORPO_RELATORIO.md').read_text(encoding='utf-8')
text += '\n\n## Cobertura requisito a requisito\n\n'
for row in CFG['phases']:
    text += '### ' + row['id'] + ' — ' + row['status'] + '\n\n'
    text += row['finding'] + '\n\n**O que falta / limite:** ' + row['remaining'] + '\n\n'
    text += 'Evidência: ' + '; '.join(link(x) for x in row['evidence']) + '.\n\n'
text += '## Catálogo completo R-A–R-M e ranking condicionado\n\n'
text += 'Números abaixo são transcritos do registro F0 revisado, não recalculados. '
text += 'A coluna histórica de decisões do registro é preservada no JSON; a leitura atual aparece em cada rota. '
text += 'D representa separação esperada sob as hipóteses indicadas; não é significância observada global.\n\n'
for row in coverage_routes:
    item = row['ranking_as_reviewed']
    text += '### ' + row['route'] + ' — ' + item['name'] + ' (posição: ' + str(item['rank']) + ')\n\n'
    text += '**Previsão e estatuto:** ' + item['prediction'] + '. ' + item['statute'] + '.\n\n'
    text += '**Dados / precisão:** ' + item['data'] + '\n\n**Separação:** ' + item['separation'] + '\n\n'
    text += '**Estado vigente:** ' + row['current_documentary_reading'] + '\n\n'
    text += '**Fontes locais da leitura:** ' + item['source'] + '. As identidades estão em FONTES_EVIDENCIAS.json.\n\n'
    for r in row['map_history']:
        text += '- `' + r['route_id'] + '` — seqs ' + ', '.join(map(str, r['seqs'])) + '.\n'
    text += '\n'
text += '## Decisões reservadas e maturidade do pacote\n\n'
for d in CFG['decisions']:
    text += '- **' + d['id'] + '** (' + d['owner'] + '; ' + d['concrete_package'] + '): ' + d['state'] + ' ' + d['remaining'] + '\n'
text += '\nEstas reservas não são uma pergunta de aprovação neste relatório: primeiro deve existir o pacote concreto revisável.\n'
text += '\n## Despachos efetivamente documentados\n\n'
text += 'A tabela identifica coordenação oficial entre tarefas locais do Codex. Não são chamadas a Kimi, MiMo, Claude ou DeepSeek. '
text += 'Um ACK confirma envio; não execução científica nem conclusão.\n\n| request_id | Recibo de envio |\n|---|---|\n'
for d in dispatches:
    text += '| `' + str(d['request_id']) + '` | ' + link(d['receipt']['path']) + ' |\n'
text += '\nO snapshot remoto de ' + slot['checked_at'] + ' contém o pedido Claude `4529daec-d42e-4c01-87d1-dd3d183070b7`, '
text += 'job `65f577e6-8dd1-4e91-8b79-c86e2abbc68a`, em prompt_ready, sem execution_task_id e sem execução. '
text += 'A geração canônica diverge da autorizada; sources.ok=false foi registrado na conferência anterior. '
text += 'Não repinamos nem repetimos o pedido. Os limites 5 coordenações / 3 execuções / 1 por provedor foram preservados. '
text += 'O payload MiMo `a4534bcd-8058-48a7-b5fa-34bc046dc46e` não constitui despacho: a prévia local recusou integridade. '
text += 'Ausência de Work é afirmada nesta preparação e nos recibos que a registram; não é inferida para toda a história.\n'
text += '\n## Integridade e alcance deste candidato\n\n'
text += 'Corte documental: ' + NOW + '. O catálogo contém ' + str(len(CAT['routes'])) + ' rotas e '
text += str(sum(len(r['records']) for r in CAT['routes'])) + ' registros lidos pela ferramenta oficial, incluindo as seqs históricas. '
text += 'Não é inventário de todo o acervo. Snapshot inicial seguido pelo adendo I02 seq664.\n\n'
text += 'Foram conferidas ' + str(len(checks)) + ' referências de hash dos recibos escolhidos; '
text += str(sum(x['matches'] for x in checks)) + ' coincidem. Falhas ou leituras indisponíveis permanecem em CONFERENCIA_PINS.json. '
text += 'Há ' + str(len(missing)) + ' referência(s) local(is) não lida(s), listadas em FONTES_EVIDENCIAS.json. '
text += 'As fontes primárias são ligadas aos recibos locais e seus estatutos; identidade de bytes não substitui releitura ou prova.\n\n'
text += 'Nenhum candidato foi importado/executado; nenhum solver, WSL, centro observado, rede ou provedor foi acionado. '
text += 'Não foram criados AUTH/CLAIM/ROOT_DECISION nem alterados kernel, gate, arquivos canônicos, relatórios ROOT ou memórias globais. '
text += 'A preparação escreve apenas nesta pasta; a consolidação nas superfícies globais cabe à ROOT após revisão.\n\n'
text += '**Próximo passo:** revisão documental ROOT deste candidato e continuidade das dependências científicas já atribuídas. '
text += 'Não repetir unidades consumidas. F1 e F3 abertos impedem chamar este arquivo de entrega final.\n'
safe_write('ENTREGA_018_RELATORIO_FINAL.md', text)

members = [pin(p) for p in sorted(HERE.iterdir()) if p.is_file()
           and '.bak_' not in p.name and p.name not in {'MANIFESTO_PREPARACAO.json','RECIBO_PREPARACAO.json','RECIBO_COORDENACAO.json','RECIBO_MAPA.json'}]
manifest = {'schema':'F4_CONSOLIDATION_MANIFEST_V1','at':NOW,'request_id':CFG['request_id'],
            'parent_request_id':CFG['parent_request_id'],'status':'REPORT_UNDER_CONSTRUCTION_NOT_FINAL',
            'members':members,'member_count':len(members)}
safe_write('MANIFESTO_PREPARACAO.json', manifest)
receipt = {'schema':'F4_DOCUMENTARY_PREPARATION_RECEIPT_V1','at':NOW,
    'request_id':CFG['request_id'],'parent_request_id':CFG['parent_request_id'],
    'status':'PREPARED_FOR_ROOT_REVIEW_NOT_SCIENTIFIC_COMPLETION',
    'manifest':pin(HERE/'MANIFESTO_PREPARACAO.json'),
    'report':pin(HERE/'ENTREGA_018_RELATORIO_FINAL.md'),
    'requirements':len(CFG['phases']),'routes_A_to_M':len(coverage_routes),
    'map_routes':len(CAT['routes']),'map_records':sum(len(r['records']) for r in CAT['routes']),
    'pin_checks':len(checks),'pin_matches':sum(x['matches'] for x in checks),
    'missing_references':missing,'local_dispatches':len(dispatches),
    'scientific_calculations':0,'provider_calls':0,'Work_calls':0,
    'observed_data_reopened':False,'root_memories_changed':False,'gate_changed':False,
    'integrity_ready_for_review':not missing and all(x['matches'] for x in checks)}
safe_write('RECIBO_PREPARACAO.json',receipt)
print(json.dumps(receipt,ensure_ascii=False))
