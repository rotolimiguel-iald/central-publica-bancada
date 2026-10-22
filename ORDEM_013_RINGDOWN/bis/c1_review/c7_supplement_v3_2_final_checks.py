"""Close S2 and verify final ZIP selection/bytes without extraction or science."""
from pathlib import Path,PurePosixPath
from types import SimpleNamespace
from datetime import datetime,timezone
import ast,hashlib,json,zipfile
B=Path(__file__).resolve().parents[2]
def require(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
def put(p,raw):
    require(not p.exists(),'Own output exists');tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    require(tmp.read_bytes()==raw and len(raw)>0,'Own write mismatch');tmp.rename(p)
harness=Path(__file__).with_name('c7_supplement_cleanup_checks.py').read_text(encoding='utf-8');tree=ast.parse(harness)
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'check_manifest','check_zip'}]
exec(compile(ast.fix_missing_locations(ast.Module(body=functions,type_ignores=[])),'reused_readonly_checks','exec'),globals())
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='lifecycle_probes');code=ast.get_source_segment(harness,fn)
replacements={
    "require(any(e[0] == 'mkdir' and e[1].startswith('/package/') for e in events), 'Write-before-validation not reproduced')":
    "require(not events and not active, 'Internal path mutated before refusal')",
    "require(error and error.startswith('PermissionError:') and len(active) == 1, 'Pretry leak not reproduced')":
    "require(error and error.startswith('PermissionError:') and not active and not any(e[0] == 'mkdtemp' for e in events), 'Output failure created temporary')"}
for before,after in replacements.items():require(code.count(before)==1,'Harness anchor');code=code.replace(before,after)
exec(compile(code,'fixed_confinement_lifecycle_harness','exec',optimize=1),globals())
build=read(B/'bis/C7_SUPPLEMENTS_V3_2_BUILD.json');builder=B/'refeito/close_supplement_confinement_013bis.py'
require(sha(builder)==build['builder_sha256'],'Supplement builder pin')
rows=[]
for r in build['packages']:
    root=B/r['package'];old=B/r['package'].replace('_v3_2','_v3_1')
    m,names=check_manifest(root);om,oldnames=check_manifest(old)
    require(names==oldnames and m['supersedes_manifest_sha256']==sha(old/'MANIFEST.json'),'Supplement lineage')
    require(sha(root/'MANIFEST.json')==r['manifest_sha256'] and sha(B/r['archive'])==r['sha256'],'Supplement build pins')
    check_zip(B/r['archive'],root,names)
    changes=[n for n in sorted(names) if (root/n).read_bytes()!=(old/n).read_bytes()]
    require(changes==['README.md','reproduce.py'],'Scientific assets changed')
    probe=lifecycle_probes((root/'reproduce.py').read_text(encoding='utf-8'),root.name)
    records=list((B/'bis/supplement_cleanup_v3_2').glob(root.name+'_*/TEMPORARY_REMOVED.json'))
    require(len(records)==1,'Ambiguous cleanup receipt')
    removed=read(records[0]);intent=read(records[0].with_name('CLEANUP_INTENT.json'))
    temp=Path(removed['temporary']).resolve();work=(B/'cache/supplement_cleanup_v3_2').resolve()
    require(removed['removed'] is True and intent['temporary']==removed['temporary'],'Cleanup status')
    require(intent['manifest_sha256']==sha(root/'MANIFEST.json'),'Cleanup identity')
    require(temp.is_relative_to(work) and temp!=work and not temp.exists(),'Temporary not removed/confined')
    log=B/'bis/supplement_cleanup_v3_2'/(root.name+'.log')
    require('FileNotFoundError: Provide --source-root' in log.read_text(encoding='utf-8'),'Negative failure reason')
    rows.append(dict(package=root.name,files=len(names),manifest_sha256=sha(root/'MANIFEST.json'),archive_sha256=sha(B/r['archive']),
        wrapper_sha256=sha(root/'reproduce.py'),changes=changes,negative_log_sha256=sha(log),
        removal_receipt_sha256=sha(records[0]),temporary_absent=True,lifecycle_probes=probe))

receiptpath=B/'bis/C7_FINAL_BUNDLE_V3_1_VALIDATION.json';receipt=read(receiptpath)
archive=B/receipt['archive'];require(sha(archive)==receipt['archive_sha256'],'Final archive receipt')
finalbuilder=B/'refeito/build_final_bundle_v3_1_013bis.py'
def selection(p):
    main=next(n for n in ast.parse(p.read_text(encoding='utf-8')).body if isinstance(n,ast.FunctionDef) and n.name=='main')
    return next(ast.literal_eval(n.value) for n in main.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='packages' for t in n.targets))
expected=['C7_INDEPENDENT_v3_3','C7_POSTERIOR_REPRODUCTION_v3_2','C7_GWTC3_REPRODUCTION_v3_2','C7_INJECTION_REPRODUCTION_v3_2','C7_IMR_RECOVERY_REPRODUCTION_v3','C7_COHERENT_SOURCE_REPRODUCTION_v3','C7_NATIVE_SEOB_WAVEFORM_v3']
require(selection(finalbuilder)==expected,'Wrong builder selection')
prefix='TGL_RINGDOWN_DELIVERY_v3_1/'
with zipfile.ZipFile(archive) as z:
    m=json.loads(z.read(prefix+'MANIFEST.json'));names={r['path'] for r in m['files']}
    require(len(names)==len(m['files'])==receipt['files']==231,'Final manifest coverage')
    require(len(z.namelist())==232 and set(z.namelist())=={prefix+n for n in names|{'MANIFEST.json'}},'Final ZIP extra/missing members')
    for r in m['files']:
        rel=PurePosixPath(r['path']);require(not rel.is_absolute() and '..' not in rel.parts and '\\' not in r['path'],'Unsafe final path')
        raw=z.read(prefix+r['path']);require(len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'],'Final member mismatch')
    require(m['builder_sha256']==sha(finalbuilder),'Effective final builder pin')
    require(m['source_packages']==receipt['source_packages'],'Final source receipts differ')
    require([r['package'] for r in m['source_packages']]==expected,'Wrong ZIP selection')
    for r in m['source_packages']:
        root=B/r['package'];require(sha(root/'MANIFEST.json')==r['manifest_sha256'] and sha(B/r['archive'])==r['sha256'],'Source package pin')
        inner=json.loads(z.read(prefix+r['package']+'/MANIFEST.json'))
        require(z.read(prefix+r['package']+'/MANIFEST.json')==(root/'MANIFEST.json').read_bytes(),'Embedded manifest differs')
        innerrows=inner.get('files',inner.get('shipped_files'))
        actual={n.removeprefix(r['package']+'/') for n in names if n.startswith(r['package']+'/')}
        require(actual=={x['path'] for x in innerrows}|{'MANIFEST.json'},'Embedded subpackage coverage')
        for x in innerrows:
            raw=z.read(prefix+r['package']+'/'+x['path'])
            require(raw==(root/x['path']).read_bytes() and hashlib.sha256(raw).hexdigest()==x['sha256'],'Embedded bytes changed')
    for n in names:
        if n.startswith('validation/'):require(z.read(prefix+n)==(B/'bis'/Path(n).name).read_bytes(),'Embedded validation receipt changed')
    require(z.read(prefix+'README.md')==z.read(prefix+'OVERVIEW.md'),'Final guide mismatch')
    guide=z.read(prefix+'README.md').decode('utf-8')
    require(all(n in guide for n in expected),'Final guide package list')
    require('CONJECTURE \u2014 management hypothesis, not TGL canon' in guide,'Final MOD scope marker')
    require(z.testzip() is None,'ZIP CRC error')
    final_manifest_sha256=hashlib.sha256(z.read(prefix+'MANIFEST.json')).hexdigest()
verifylog=B/'bis/C7_FINAL_BUNDLE_V3_1_VERIFY.log';verify=json.loads(verifylog.read_bytes())
require(verify==receipt['verification'] and verify['files']==231 and verify['status']=='PASS','Verifier receipt differs')
require(receipt['status']=='PASS_CLEAN_BUNDLE_BYTE_VERIFICATION' and receipt['temporary_removed'] is True,'Final receipt not pass')
prior_effective=B/'refeito/build_final_bundle_v3_final_013bis.py';prior_selected=selection(prior_effective)
require(all(n.replace('_v3_2','_v3_1') in prior_selected for n in expected[1:4]),'Prior effective builder clarification differs')
result=dict(status='S2_CLOSED_AND_FINAL_ZIP_SELECTION_BYTES_VERIFIED',utc=datetime.now(timezone.utc).isoformat(),
    no_scientific_execution=True,supplements=rows,independent_zero_mkdir_refusals=6,total_mock_lifecycle_cases=15,
    source_builder_sha256=sha(builder),final_builder_sha256=sha(finalbuilder),archive=str(archive.relative_to(B)),archive_sha256=sha(archive),
    final_manifest_sha256=final_manifest_sha256,final_files=231,zip_members=232,selected_packages=expected,
    final_receipt_sha256=sha(receiptpath),final_verify_log_sha256=sha(verifylog),
    final_extraction_cleanup='DECLARADO by principal authorized agent receipt; no temporary path in receipt to recheck absence',
    previous_effective_builder=dict(path=str(prior_effective.relative_to(B)),sha256=sha(prior_effective),selected_packages=prior_selected),
    execution_provenance='Prior real replays/negative tests/extraction performed by principal authorized agent, not human operator; this reviewer checked receipts and ran own mocks only',
    script_sha256=sha(Path(__file__)))
out=B/'bis/c1_review/c7_supplement_v3_2_final_results.json';put(out,(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
paths=['refeito/close_supplement_confinement_013bis.py','bis/C7_SUPPLEMENTS_V3_2_BUILD.json','refeito/build_final_bundle_v3_1_013bis.py','cache/TGL_RINGDOWN_DELIVERY_v3_1.zip','bis/C7_FINAL_BUNDLE_V3_1_VALIDATION.json','bis/C7_FINAL_BUNDLE_V3_1_VERIFY.log','bis/c1_review/c7_supplement_v3_2_final_checks.py','bis/c1_review/c7_supplement_v3_2_final_results.json']
hashrows='\n'.join(f'| `{n}` | `{sha(B/n)}` |' for n in paths)
packagelist='\n'.join('- `'+n+'`' for n in expected)
report=f'''[REAL — fechamento independente de S2 e seleção/bytes do ZIP final; sem nova ciência]

# C7 suplementos v3_2 — fechamento S2 / M6

Data UTC: {result['utc']}.

**S2 fechado nos três suplementos v3_2. Seleção e integridade do ZIP final aprovadas neste recorte.** Não resta bloqueante dos achados S1/S2 examinados; R1–R4 do pacote principal têm os fechamentos próprios v3_2/v3_3. Este parecer é novo e não substitui os anteriores.

POSTERIOR/GWTC3/INJECTION resolvem e recusam work/output internos antes de qualquer mkdir. Reexecutei o bloco real em memória sob optimize=1: seis recusas independentes (duas por wrapper), zero mkdir/mkdtemp/subprocess. Mais nove sondas preservam S1 e exercitam finally: falha de criação do destino ocorre antes de mkdtemp; cleanup normal e cleanup após falha de escrita do recibo removem somente o filho validado. Nenhuma remoção real foi feita pelos mocks.

As três negativas por fonte ausente, executadas pelo **agente principal autorizado**, conferem nos logs/intenções/recibos; seus temporários estão ausentes e eram descendentes próprios das raízes declaradas. Tamanhos/hashes/ZIPs dos três pacotes conferem. Apenas README e reproduce.py mudaram versus v3_1, além do manifesto; assets científicos permanecem idênticos. Não houve nova campanha por esta revisão.

O ZIP `cache/TGL_RINGDOWN_DELIVERY_v3_1.zip` contém **231 arquivos listados + MANIFEST.json = 232 membros**, sem ausências/duplicatas/extras. Conferi por leitura direta todos os tamanhos/hashes e os bytes dos subpacotes contra as pastas/manifestos de origem. CRC passa. Builder hasheado no manifesto é `build_final_bundle_v3_1_013bis.py`. A seleção efetiva no ZIP, no manifesto/recibo e no builder coincide:

{packagelist}

Recibos embarcados coincidem com os originais, incluindo C7_SUPPLEMENTS_V3_2_BUILD. README/OVERVIEW coincidem, listam as versões corretas e preservam a marca literal R-MOD. O log do verificador contém PASS/231 e coincide com C7_FINAL_BUNDLE_V3_1_VALIDATION. Essa extração foi executada pelo agente principal autorizado; minha verificação do ZIP é direta, independente e sem nova extração. O recibo final registra temporary_removed=true mas não informa o caminho: a ausência física desse temporário específico fica [DECLARADO], distinta das três remoções dos suplementos efetivamente reconstatadas. Isso não impede fechar S2 e a seleção pedida.

**Erratas de proveniência dos pareceres anteriores:** “replay do operador” deve ser lido como **replay do agente principal autorizado pelo operador**, não execução pessoal do humano. Além disso, a observação anterior de seleção v3 referia-se ao arquivo build_final_bundle_v3_3_013bis.py efetivamente lido; o builder então vigente informado pelo agente principal era build_final_bundle_v3_final_013bis.py, que conferi agora e seleciona v3_1. Não imputo ao builder efetivo anterior a seleção do arquivo antigo. A nova entrega v3_1 seleciona os suplementos v3_2, como comprovado acima.

O fechamento é de engenharia documental/confinamento e integridade para M6, não certificação global da ciência ou de todos os requisitos de entrega. As raízes externas à entrega composta seguem a instrução do README; a guarda dos wrappers é relativa a cada pacote próprio. Ciência congelada, C5/PE, injeção A e a ressalva operacional F2-INJ-R1 são assuntos separados. Sem alteração de produção, manifests, memórias ou parecer anterior.

Controle próprio: `bis/c1_review/c7_supplement_v3_2_final_checks.py`, Python bundled −B −O; resultados em `c7_supplement_v3_2_final_results.json`.

| Caminho relativo à raiz | SHA256 lido |
|---|---|
{hashrows}
'''
dest=B/'bis/C7_SUPPLEMENTS_V3_2_CLOSING_REVIEW.md';put(dest,report.encode())
print(json.dumps(dict(status=result['status'],report=str(dest),report_sha256=sha(dest),final_files=231,zero_mkdir_refusals=6)))
