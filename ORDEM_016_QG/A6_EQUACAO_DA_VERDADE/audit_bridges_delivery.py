from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT.parent / 'TUNEL/DO_CHATGPT'
B = HERE / 'B_fechamentos'
spec = importlib.util.spec_from_file_location('audit', ROOT/'A0/auditar_axiomas.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, value):
    raw = value if isinstance(value, bytes) else (value.encode('utf-8') if isinstance(value, str)
        else json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8'))
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if path.exists():
        old = path.read_bytes()
        bak = path.with_name(path.name+'.bak_'+stamp)
        bak.write_bytes(old)
        assert bak.read_bytes() == old
    tmp = path.with_name(path.name+'.tmp_'+stamp)
    tmp.write_bytes(raw)
    assert tmp.read_bytes() == raw and raw
    tmp.replace(path)

units = [
    ('B7', 'InscriptionBridge.lean', 'inscription_bridge_01'),
    ('B4', 'PenaltyThreeLocksBridge_v2.lean', 'penalty_bridge_02'),
    ('B1c', 'TheEquationOfTruth_T20_v3.lean', 'single_time_02'),
    ('B6', 'OperatorContourBridge_v2.lean', 'operator_contour_02'),
]
results = []
for branch, filename, label in units:
    source, log = B/filename, B/(label+'.log')
    receipt = json.loads((B/(label+'.json')).read_bytes())
    assert receipt['rc'] == 0
    assert receipt['source_sha256'] == sha(source)
    assert receipt['log_sha256'] == sha(log)
    assert not receipt['newer_kernel_files'] and not receipt['scan_errors']
    result = audit.audita(str(source), str(log))
    assert result['auditoria'] == 'PASSA', result['motivos']
    save(B/(label+'_audit.json'), result)
    results.append(dict(branch=branch, source=str(source), source_sha256=sha(source),
        label=label, log_sha256=sha(log), receipt=receipt, audit=result))

original = (HERE/'A_reproducao/TheEquationOfTruth.lean').read_bytes()
assert (B/'TheEquationOfTruth_T20_v3.lean').read_bytes().startswith(original)
manifest = dict(status='REAL_COMPILED_AND_AUDITED_SCOPED', at=datetime.now(timezone.utc).isoformat(),
    original_prefix_bytes=len(original), original_prefix_sha256=hashlib.sha256(original).hexdigest(),
    prefix_preserved=True, units=results,
    packaging_status='MEDIDA: companion modules required for additional imports; monolithic integration pending',
    gate_changed=False)
save(B/'bridges_and_single_time_manifest.json', manifest)

lines = ['[REAL — compilações isoladas e auditoria de axiomas; escopo matemático dos enunciados]', '',
    '# A6 — pontes B7/B4, amostra temporal B1c e controle B6', '',
    'Quatro módulos compilados com código zero. Os hashes de fonte/log foram recalculados e comparados aos recibos. '
    'A auditoria exige cobertura de todos os teoremas da fonte e axiomas contidos em propext, Classical.choice, Quot.sound.', '',
    '| Ramo | Fonte | Teoremas locais | Declarações auditadas | Avisos |',
    '|---|---|---:|---:|---:|']
for item in results:
    a=item['audit']
    lines.append(f"| {item['branch']} | {Path(item['source']).name} | {a['n_theorem_lemma_na_fonte']} | {a['n_declaracoes_auditadas']} | {a['n_warnings']} |")
lines += ['', 'B7 transporta uma inscrição usando o construtor canônico NameIsTheContent e prova existência '
    'de mudança de conteúdo fora do núcleo com forma preservada. B4 identifica exatamente penalty e H3L '
    'e seus projetores nos tipos especificados; não instancia automaticamente as matrizes float do runtime.', '',
    'B1c prova em dimensão finita que conservação de um leitor contínuo em um único tempo positivo '
    'implica fatoração pelo projetor, usando iteração e o limite já demonstrado. B6 exibe dinâmica '
    'não estática que preserva a leitura e uma dinâmica incompatível que a leitura reprova.', '',
    f'Prefixo V3 preservado byte a byte: {len(original)} bytes, SHA256 {manifest["original_prefix_sha256"]}.', '',
    '**MEDIDA de empacotamento:** Lean recusa import depois de comandos. O probe appended_import_probe_01 '
    'registrou esse erro. Para conservar o prefixo V3 integral, as pontes foram compiladas em módulos '
    'companheiros. A exigência de monólito final permanece pendente de organização da gerência. '
    'Os módulos de versões distintas não devem ser importados juntos: contêm declarações homônimas. '
    'A integração futura precisa escolher uma única base e regenerar os imports dos companheiros.', '',
    'Tentativas anteriores preservadas: penalty_bridge_01, single_time_01 e operator_contour_01. '
    'Os recibos finais não apontam arquivos novos no kernel. Nenhum um.py ou gate foi alterado.', '',
    'Manifesto detalhado: '+str(B/'bridges_and_single_time_manifest.json'), '']
save(OUT/'ENTREGA_016_A6_B_pontes_amostra_e_controle.md', '\n'.join(lines))

ledger = OUT/'LEDGER_016.jsonl'
old = ledger.read_bytes()
entries = []
marker = 'A6_BRIDGES_SINGLE_TIME_AUDITED'
if marker.encode() not in old:
    entries.append(dict(event=marker, at=manifest['at'], manifest=str(B/'bridges_and_single_time_manifest.json'),
        manifest_sha256=sha(B/'bridges_and_single_time_manifest.json'), gate_changed=False))
for unit in json.loads((HERE/'orchestration_additional/prepared_units.json').read_bytes()):
    if unit['request_id'].encode() not in old:
        entries.append(dict(event='unit_prepared_for_coordination', at=manifest['at'], **unit,
                            external_execution=False, tokens=None, cost_estimate_usd=None))
if entries:
    extension=''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in entries).encode('utf-8')
    save(ledger, old+(b'' if old.endswith(b'\n') else b'\n')+extension)
print(json.dumps([dict(branch=r['branch'], audit=r['audit']['auditoria'],
    declarations=r['audit']['n_declaracoes_auditadas']) for r in results],ensure_ascii=False))
