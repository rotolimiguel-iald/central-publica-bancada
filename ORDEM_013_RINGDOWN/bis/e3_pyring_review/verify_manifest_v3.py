"""Independent documentary V3 delta only; no producer import or science."""
import ast,hashlib,json,re,time
from pathlib import Path
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;B=HERE.parents[1];ROOT=B.parent
PREP=B/'bis/e3_pyring_preparation'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write_new(p,obj):
    with p.open('x',encoding='utf-8',newline='\n') as f:
        f.write(obj if isinstance(obj,str) else json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def main():
    started=time.perf_counter();checks=[]
    receipt=HERE/'MANIFEST_V3_INDEPENDENT_RECEIPT.json';report=HERE/'MANIFEST_V3_INDEPENDENT_REVIEW.md'
    if receipt.exists() or report.exists():raise FileExistsError('Independent V3 receipt already exists')
    def check(name,ok,detail=None):
        if not ok:raise RuntimeError(name)
        checks.append(dict(name=name,passed=True,detail=detail))
    p2=PREP/'MANIFEST_v2.json';p3=PREP/'MANIFEST_v3.json';v2=read(p2);v3=read(p3)
    prev=read(HERE/'MANIFEST_V2_INDEPENDENT_RECEIPT.json');producer=read(PREP/'MANIFEST_V3_REPIN_RECEIPT.json')
    check('v2_preserved',sha(p2)==prev['manifest_sha256']==producer['predecessor_sha256'])
    check('v1_preserved',sha(PREP/'MANIFEST.json')==sha(HERE/'snapshot_002/MANIFEST.json'))
    check('v3_producer_hash',sha(p3)==producer['successor_sha256'])
    actual={p.name:sha(p) for p in sorted(PREP.glob('*.py'))}
    check('nine_Kerr_sources_unchanged',len(actual)==9 and actual==v2['code_sha256']==v3['code_sha256']==prev['code_sha256'])
    oldpins=v2['source_and_config_pins'];newpins=v3['source_and_config_pins']
    key='ORDEM_013_RINGDOWN/bis/e2_code/registration_guard.py'
    changed={n:dict(old=h,new=newpins.get(n)) for n,h in oldpins.items() if newpins.get(n)!=h}
    additions={n:h for n,h in newpins.items() if n not in oldpins}
    expected_added={'ORDEM_013_RINGDOWN/bis/e2_review/ACTIVATION_APP_V2_PATH_RECEIPT.json',
        'ORDEM_013_RINGDOWN/bis/e3_pyring_preparation/MANIFEST_V3_NOTE.md',
        'ORDEM_013_RINGDOWN/bis/e3_pyring_preparation/MANIFEST_v2.json'}
    check('only_existing_pin_delta_is_guard',set(changed)=={key})
    check('three_documentary_additions',set(additions)==expected_added)
    allowed={'activation_scope','authorization_manifest_filename','changed_existing_dependency_pins','checks','code_change_since_predecessor',
        'created_utc','predecessor','revision','source_and_config_pins'}
    changed_fields=sorted(k for k in set(v2)|set(v3) if v2.get(k)!=v3.get(k))
    check('no_other_manifest_contract_change',set(changed_fields)<=allowed,changed_fields)
    check('prior_checks_retained',v3['checks'][:len(v2['checks'])]==v2['checks'])
    pin_results={}
    for name,pin in newpins.items():
        p=(ROOT/name).resolve()
        if not p.is_relative_to(ROOT.resolve()) or p.suffix.lower() in ('.h5','.hdf5','.gwf'):raise RuntimeError('Disallowed source read')
        h=sha(p);check('pin_'+name,h==pin);pin_results[name]=h
    guard=ROOT/key;oldguard=B/'bis/e2_review/activation_app_v2_path_snapshot/registration_guard.py'
    before=oldguard.read_bytes();after=guard.read_bytes()
    oldliteral=b'E2_REVIEW_APPLICATION_V1.json';newliteral=b'E2_REVIEW_APPLICATION_V2.json'
    check('old_guard_snapshot_pin',sha(oldguard)==oldpins[key])
    check('exact_one_literal_replacement',before.count(oldliteral)==1 and after==before.replace(oldliteral,newliteral))
    check('current_guard_pin',sha(guard)==newpins[key]==producer['guard_sha256'])
    guardreceipt=read(B/'bis/e2_review/ACTIVATION_APP_V2_PATH_RECEIPT.json')
    check('guard_receipt_hash',sha(B/'bis/e2_review/ACTIVATION_APP_V2_PATH_RECEIPT.json')==producer['guard_receipt_sha256'])
    check('producer_test_receipt_hash',sha(B/'bis/e2_review/ACTIVATION_APP_V2_PATH_TESTS.json')==guardreceipt['test_receipt_sha256'])
    for name,h in guardreceipt['files_created_sha256'].items():check('producer_evidence_'+name,sha(ROOT/name)==h)
    tests=read(B/'bis/e2_review/ACTIVATION_APP_V2_PATH_TESTS.json')
    check('producer_forty_cases_recorded',len(tests['checks'])==40 and guardreceipt['finite_checks']==40)
    # Narrow independent probe: evaluate path gate, deliberately stop before the first read.
    fn=next(n for n in ast.parse(after.decode()).body if isinstance(n,ast.FunctionDef) and n.name=='check_activation')
    reads=[]
    class ReachedRead(Exception):pass
    def no_read(*args,**kwargs):reads.append(str(args[0]));raise ReachedRead('No artifact read in path probe')
    ns=dict(contained=no_read,strict_json=lambda value:value)
    exec(compile(ast.Module(body=[fn],type_ignores=[]),'<guard_path_only>','exec',optimize=1),ns)
    for version in (1,2,3):
        reads.clear();activation=dict(receipt_relative_to_Chatgpt='ORDEM_013_RINGDOWN/bis/E2_REGISTRATION_RECEIPT.json',
            review_application_relative_to_Chatgpt=f'ORDEM_013_RINGDOWN/bis/E2_REVIEW_APPLICATION_V{version}.json',
            sealer_relative_to_Chatgpt='ORDEM_013_RINGDOWN/refeito/seal_e2_013bis.py')
        try:ns['check_activation'](dict(activation=activation),'UNUSED',None)
        except ValueError:check('guard_path_V'+str(version),version!=2 and not reads,'Refused before any file read')
        except ReachedRead:check('guard_path_V'+str(version),version==2 and len(reads)==1,'Expected path passes to first read; full activation not executed')
        else:raise RuntimeError('Path probe must stop before IO')
    nodes=[n for n in ast.parse((PREP/'custody.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name in ('contained','selected_manifest')]
    ns=dict(Path=Path,HERE=PREP,re=re)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'<manifest_selector>','exec',optimize=1),ns)
    check('selector_V3',ns['selected_manifest']({'manifest_filename':'MANIFEST_v3.json'})==p3.resolve())
    orchestrator=B/'refeito/activate_kerr_013bis.py'
    orch_text=orchestrator.read_text(encoding='utf-8');orch_tree=ast.parse(orch_text)
    calls=[n for n in ast.walk(orch_tree) if isinstance(n,ast.Call)]
    launches=[n for n in calls if isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='subprocess' and n.func.attr=='run']
    check('orchestrator_one_controller_launch_no_outer_timeout',len(launches)==1 and 'timeout' not in {k.arg for k in launches[0].keywords})
    review_reads=[n for n in calls if isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='review' and n.func.attr in ('read_bytes','read_text','open')]
    check('orchestrator_review_bytes_not_semantically_loaded',not review_reads,'Static finding: hashes alone do not bind review disposition to chosen manifest')
    check('orchestrator_qualifies_zero_exit_and_counter','A zero launcher return code is not posterior acceptance' in orch_text and 'after its guard' in orch_text)
    orch_review=dict(path=orchestrator.relative_to(ROOT).as_posix(),sha256=sha(orchestrator),executed=False,
        status='STATIC_REVIEW_AUTOMATIC_GO_BINDING_OPEN',
        accepted=['checked_registration first','Exact supplied manifest/review hashes and local paths','F0 closed receipt tied to registration and B2 hash','No competing outer timeout','Zero controller exit explicitly requires variant/convergence review','No scientific source changes'],
        findings=[dict(id='ORCH-R1',priority='P2',scope='Automatic application of existing GO, not Kerr V3 scientific/custody delta',
            problem='The review is hashed but its contents are never read. A historical or non-closing review plus a different valid manifest satisfies the same supplied-hash checks.',
            correction='Require the independent JSON receipt; strict-load it and require its manifest_filename/hash equal the selected manifest, its reviewed disposition accepted in an explicit allowlist, and blocking_findings empty. Pin narrative MD separately if desired. Do this before publishing authorization.',
            blocking_for='Treating this orchestrator as a fail-closed automatic applicator of the reviewed GO'),
          dict(id='ORCH-N1',priority='P3',problem='If log.open fails before creating the log, unconditional sha(log) prevents publication of the outer failure receipt.',
            correction='Hash the log only when it exists; record null and error_type otherwise. Keep authorization/failed attempt preserved.')])
    check('manifest_current_at_end',sha(p3)==producer['successor_sha256'])
    check('Kerr_code_current_at_end',{p.name:sha(p) for p in PREP.glob('*.py')}==actual)
    result=dict(status='V3_DOCUMENTARY_DELTA_CLOSED_NO_EXECUTION_AUTHORIZATION',created_utc=datetime.now(timezone.utc).isoformat(),
        manifest_filename='MANIFEST_v3.json',manifest_sha256=sha(p3),predecessor_sha256=sha(p2),
        guard_sha256=sha(guard),code_sha256=actual,source_and_config_pins_verified=pin_results,
        changed_existing_pins=changed,added_documentary_pins=additions,changed_top_level_fields=changed_fields,
        checks=checks,checks_count=len(checks),producer_tests_reexecuted=False,
        independent_path_probes=3,scientific_checks_reexecuted=False,blocking_findings=[],
        orchestrator_static_review=orch_review,
        nonblocking_notes_disposition='N1/N2 remain unchanged in source; principal will qualify counter and failure receipt semantics in outputs',
        custody_status='PAGO_NO_ESCOPO_DO_DELTA_DOCUMENTAL_V3',E3_1_status='NAO_PAGO_NAO_EXECUTADO',
        equivalence_status='OPEN_IDENTITY_NOT_ESTABLISHED_GWOSC_C00_AR_PSD_EXECUTABLE_VERSION',
        execution_authorized=False,activation_created=False,physical_waveforms=0,strain_values_read=0,PE_runs=0,
        excluded_scope=['Native Win32 ACL helper','E2 candidate003 sealer execution and chronology','B2/F0-stop execution'],
        wall_seconds=time.perf_counter()-started,script_sha256=sha(__file__))
    write_new(receipt,result)
    text=f'''# Kerr V3 — fechamento independente do delta documental

[REAL — hashes e três provas finitas do caminho; OPEN — execução E3.1]

{result['created_utc']}

**PAGO no escopo do delta de custódia V3. Nenhum novo bloqueante.** Foram {len(checks)} verificações documentais/finítas, sem repetir ciência. `MANIFEST_v3.json`: `{sha(p3)}`.

Os nove fontes Kerr atuais conferem com V2 e V3. MANIFEST.json/V2 permanecem preservados. O único pin preexistente alterado é registration_guard.py: `{oldpins[key]}` → `{newpins[key]}`. Conferi contra o snapshot anterior: exatamente uma substituição literal de E2_REVIEW_APPLICATION_V1.json por E2_REVIEW_APPLICATION_V2.json; nenhum outro byte mudou.

Além desse repin, V3 acrescenta três pins documentais: recibo da guarda, nota V3 e manifesto V2. Os campos históricos herdados do manifesto continuam descrevendo etapas anteriores; não são novas execuções. Todos os pins do mapa V3 conferiram. O seletor aceita MANIFEST_v3.json; controller/runner conservam o transporte do hash autorizado já revisado.

Três controles próprios sob optimize=1: caminho V1 e V3 recusados antes de qualquer leitura; caminho V2 alcança a primeira leitura, interrompida deliberadamente pelo fixture. Isso não executa ativação. Os40 controles de A tiveram recibo/proveniência conferidos, sem rerun e sem serem promovidos a controles independentes.

A autorização futura do principal deverá indicar `manifest_filename: MANIFEST_v3.json` e o hash acima. Nenhuma autorização/ativação foi criada. Este fechamento não audita ACL nativa, selagem candidate003, sua cronologia ou a conclusão de B2/F0-stop. Nenhuma fonte congelada, produção ou manifesto foi editado pelo revisor.

**PAGO:** preparação científica/contratual no recorte já auditado e atualização documental V3. **NÃO PAGO:** execução, custo físico medido, convergência/posterior e aceitação E3.1. **OPEN:** identidade GWOSC/C00_AR, PSDs da release e versão executável; identidade não demonstrada não é prova de inequivalência física. A declaração de reprodução equivalente continua não sustentada.

N1/N2 permanecem qualificações obrigatórias nas saídas conforme decisão do principal; nenhum fonte foi modificado para resolvê-las. Execução somente pelo principal após E2/B2/F0-stop e autorização própria.

## Orquestrador externo — revisão estática separada

`refeito/activate_kerr_013bis.py`, SHA256 `{orch_review['sha256']}`: somente lido/AST, não executado. Confere checked_registration, caminhos locais, hashes fornecidos, F0 com after_processes vazio sob o mesmo registro e hash da entrega B2. Não cria timeout externo concorrente; o controller continua responsável por prazo/cleanup. Retorno zero vira EXECUTION_COMPLETED_REVIEW_PENDING, com aviso explícito de que variantes/convergência ainda devem ser examinadas. A semântica de contador após a guarda está qualificada. Esses pontos estão corretos no alcance estático.

**ORCH-R1 [P2 — vínculo do GO automático pendente]:** o script hasheia o parecer, mas não lê seu conteúdo nem compara o manifesto nele auditado com o escolhido. Um parecer anterior ou que não feche bloqueantes passa pelos mesmos checks se seus bytes/hash forem fornecidos corretamente. Correção exata: aceitar o recibo independente JSON, carregar estritamente e exigir manifest_filename/manifest_sha256 iguais ao selecionado, status de fechamento em allowlist explícita e blocking_findings vazio, antes de publicar autorização. MD pode continuar pinado como narrativa. No estado atual, o pareamento depende da decisão manual do principal; não chamar o script de validador automático desse GO. Este achado é do orquestrador novo, não reabre a ciência ou o repin V3.

**ORCH-N1 [P3 — recibo de falha]:** se log.open falhar sem criar o arquivo, sha(log) incondicional impede gravar o recibo externo. Usar hash nulo quando ausente e preservar error_type evita mascarar a causa. Não é falso aceite de posterior; é lacuna de registro da tentativa.

Recibo: MANIFEST_V3_INDEPENDENT_RECEIPT.json, SHA256 `{sha(receipt)}`. Script: verify_manifest_v3.py. Tempo documental {result['wall_seconds']:.6f}s. Nenhuma waveform física, valor de strain ou PE.
'''
    write_new(report,text)
    print(json.dumps(dict(status=result['status'],checks=len(checks),manifest_sha256=sha(p3),receipt_sha256=sha(receipt),report_sha256=sha(report))))

if __name__=='__main__':main()
