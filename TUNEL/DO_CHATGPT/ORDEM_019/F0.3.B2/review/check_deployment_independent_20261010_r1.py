"""Independent read-only deployed-byte and runtime check; no Bench imports or fits."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, math, re, subprocess, time, urllib.request
BASE = Path(r'C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F0.3.B2')
OUT = BASE/'review'
BENCH = Path(r'C:/IALD/Bancada_Um')
CANDIDATE = BASE/'candidate'
STEM = 'DEPLOYMENT_INDEPENDENT_CHECK_20261010_R1'
for suffix in ('.json','.md','_HTTP_STATE.json','_PROCESS.json'):
    if (OUT/(STEM+suffix)).exists():
        raise FileExistsError(OUT/(STEM+suffix))
start = datetime.now(timezone.utc).isoformat(); timer = time.monotonic()
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(path):
    b = path.read_bytes()
    return dict(path=str(path),sha256=sha(b),bytes=len(b))
def readj(path):
    b = path.read_bytes()
    return json.loads(b),dict(path=str(path),sha256=sha(b),bytes=len(b))
def write_new(path, data):
    b = data if isinstance(data,bytes) else data.encode('utf-8')
    with path.open('xb') as f: f.write(b)
def is_child(p, root):
    try: p.resolve().relative_to(root.resolve()); return True
    except ValueError: return False
failures=[]
def check(condition, label):
    if not condition: failures.append(label)
    return bool(condition)
receipts={}; receipt_pins={}
for name in ('DEPLOY_RECEIPT_R1','RESTART_RECEIPT_R1','LIVE_VERIFICATION_R1'):
    receipts[name],receipt_pins[name]=readj(BASE/(name+'.json'))
dep=receipts['DEPLOY_RECEIPT_R1']; rst=receipts['RESTART_RECEIPT_R1']; oldlive=receipts['LIVE_VERIFICATION_R1']
manifest_raw=(BENCH/'canonical_contracts.json').read_bytes(); manifest=json.loads(manifest_raw)
manifest_pin=dict(path=str(BENCH/'canonical_contracts.json'),sha256=sha(manifest_raw),bytes=len(manifest_raw))
check(manifest_raw==(CANDIDATE/'canonical_contracts.json').read_bytes(),'installed manifest != candidate')
check(manifest_pin['sha256']==dep['manifest_sha256'],'installed manifest != deployment receipt')
deployment=[]
for entry in dep['files']:
    relative=entry['relative']; target=BENCH/relative; staged=CANDIDATE/relative
    if not check(is_child(target,BENCH) and is_child(staged,CANDIDATE),'unsafe deployment path '+relative): continue
    target_pin=pin(target); staged_pin=pin(staged)
    row=dict(relative=relative,installed=target_pin,candidate=staged_pin)
    row['matches_receipt']=check(target_pin['sha256']==entry['new_sha256'] and target_pin['bytes']==entry['bytes'],'deployed bytes mismatch '+relative)
    row['matches_candidate']=check(target_pin['sha256']==staged_pin['sha256'] and target_pin['bytes']==staged_pin['bytes'],'candidate mismatch '+relative)
    if entry.get('old_sha256'):
        backup=Path(entry['backup'])
        check(is_child(backup,BENCH),'backup escapes Bench '+relative)
        row['backup']=pin(backup)
        row['backup_matches_old']=check(row['backup']['sha256']==entry['old_sha256'],'old backup mismatch '+relative)
    else:
        row['backup']=None
        check(entry.get('backup') is None,'unexpected backup for new path '+relative)
    deployment.append(row)
manifest_checks={}
for group in ('code','sources'):
    rows=[]
    for entry in manifest[group]:
        p=Path(entry['path']); p=p if p.is_absolute() else BENCH/p
        actual=pin(p)
        row=dict(expected=entry,actual=actual)
        row['matches']=check(actual['sha256']==entry['sha256'] and actual['bytes']==entry['bytes'],group+' mismatch '+entry['path'])
        rows.append(row)
    manifest_checks[group]=rows
c=manifest['canonical']; script_path=Path(c['script']['path']); seal_path=Path(c['seal']['path'])
script_raw=script_path.read_bytes(); seal_raw=seal_path.read_bytes(); seal=json.loads(seal_raw); script_text=script_raw.decode('utf-8-sig')
version=re.search(r'^UM_VERSION\s*=\s*["\x27]([^"\x27]+)',script_text,re.M).group(1)
alpha=float(re.search(r'^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)',script_text,re.M).group(1))
identity=dict(version=version,um_py_sha256=sha(script_raw),um_py_bytes=len(script_raw),seal_sha256=sha(seal_raw),seal_bytes=len(seal_raw),seal_version=seal.get('um_version'),seal_program_sha256=seal.get('sha256',{}).get('um.py'),alpha=alpha,beta_tgl=alpha*math.sqrt(math.e))
for kind,b in [('script',script_raw),('seal',seal_raw)]:
    check(sha(b)==c[kind]['sha256'] and len(b)==c[kind]['bytes'],'canonical '+kind+' differs from manifest')
check(version==c['version']==seal.get('um_version'),'versions differ')
check(seal.get('sha256',{}).get('um.py')==sha(script_raw),'seal does not bind actual program')
request=urllib.request.Request('http://127.0.0.1:18777/api/estado',headers={'X-Cliente':'B2-independent-readonly-review'})
http_start=datetime.now(timezone.utc).isoformat()
with urllib.request.urlopen(request,timeout=45) as response:
    raw_state=response.read(); http_status=response.status
http_end=datetime.now(timezone.utc).isoformat(); state=json.loads(raw_state)
write_new(OUT/(STEM+'_HTTP_STATE.json'),raw_state)
check(http_status==200,'HTTP status is not 200')
check(state.get('pronta') is True and state.get('erro') is None,'service is not ready')
current=state.get('canone',{})
for field in ('canonical_version','um_py_sha256','seal_sha256','canonical_manifest_sha256','alpha','beta_tgl'):
    expected={'canonical_version':version,'canonical_manifest_sha256':sha(manifest_raw)}.get(field,identity.get(field))
    check(current.get(field)==expected,'HTTP canonical identity mismatch '+field)
check(current.get('ok') is True,'HTTP canonical check not ok')
alpha_provenance=state.get('motor',{}).get('fontes',{}).get('alpha',{})
for field,expected in [('um_py_sha256',sha(script_raw)),('seal_sha256',sha(seal_raw)),('um_version',version),('canonical_manifest_sha256',sha(manifest_raw))]:
    check(alpha_provenance.get(field)==expected,'resident alpha provenance mismatch '+field)
ps = '$p=Get-CimInstance Win32_Process -Filter "ProcessId='+str(rst['new_server'])+'"; $l=@(Get-NetTCPConnection -LocalPort 18777 -State Listen); [pscustomobject]@{process=($p | Select-Object ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine,CreationDate);listeners=@($l | Select-Object LocalAddress,LocalPort,OwningProcess)} | ConvertTo-Json -Depth 5'
proc=subprocess.run(['powershell.exe','-NoProfile','-Command',ps],capture_output=True,text=True,encoding='utf-8',timeout=30)
check(proc.returncode==0,'process inspection failed')
process_record=json.loads(proc.stdout); write_new(OUT/(STEM+'_PROCESS.json'),json.dumps(process_record,ensure_ascii=False,indent=2))
check(process_record['process']['ProcessId']==rst['new_server'],'current process differs from restart receipt')
check(any(x['OwningProcess']==rst['new_server'] and x['LocalAddress']=='127.0.0.1' for x in process_record['listeners']),'loopback listener does not belong to restarted process')
check(str(BENCH/'um_bancada.py').lower() in process_record['process']['CommandLine'].lower(),'running process command is not Bench service')
# Static declaration comparison only. No import or new launch of the MCP service.
mcp_raw=(BENCH/'mcp_um.py').read_bytes(); mcp_tree=ast.parse(mcp_raw.decode('utf-8-sig'))
static_tools=[]
for node in mcp_tree.body:
    if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
        for deco in node.decorator_list:
            expr=deco.func if isinstance(deco,ast.Call) else deco
            if isinstance(expr,ast.Attribute) and expr.attr=='tool':
                static_tools.append(dict(name=node.name,line=node.lineno));break
reported=oldlive['mcp']['tools']; declared=[x['name'] for x in static_tools]
check(len(reported)==28 and len(set(reported))==28,'historical MCP list does not contain 28 unique tools')
check(set(reported)==set(declared),'installed MCP declarations differ from fresh-session reported tools')
verify_path=BASE/'verify_live.py'; verify_text=verify_path.read_text(encoding='utf-8-sig')
anchors={needle:[i for i,l in enumerate(verify_text.splitlines(),1) if needle in l] for needle in ('StdioServerParameters','mcp_um.py','await session.initialize()','await session.list_tools()','await session.call_tool(','LIVE_VERIFICATION_R1.json')}
for needle,lines in anchors.items():check(bool(lines),'fresh MCP verifier lacks '+needle)
for record,label in [(oldlive['state']['canone'],'historical HTTP'),(oldlive['mcp']['result']['canonical'],'historical fresh MCP')]:
    for field,expected in [('um_py_sha256',sha(script_raw)),('seal_sha256',sha(seal_raw)),('canonical_manifest_sha256',sha(manifest_raw)),('canonical_version',version)]:
        check(record.get(field)==expected,label+' differs from installed '+field)
check(oldlive.get('observed_fit') is False,'historical verifier reports observed fit')
check(oldlive['mcp']['result'].get('synthetic') is True,'historical MCP test is not marked synthetic')
# Re-read all receipt and manifest bytes at the end to identify concurrent drift.
for name,expected in receipt_pins.items():check(pin(Path(expected['path']))['sha256']==expected['sha256'],'receipt drift '+name)
check(sha((BENCH/'canonical_contracts.json').read_bytes())==sha(manifest_raw),'manifest changed during review')
end=datetime.now(timezone.utc).isoformat()
result=dict(schema=1,statute='REAL_READ_ONLY_BYTE_AND_RUNTIME_VERIFICATION',scope='Deployment integrity and live identity; no physical confirmation, observed fit or data opening',begin_utc=start,end_utc=end,seconds=time.monotonic()-timer,ok=not failures,failures=failures,unit='F0.3.B2',claim_parent=639,nos_vivo=dict(requested='F0.3.B2 not in graph',fallback='F0.3; existing v391 custody/catalog/read-only canonical validation reused; no graph rebuild'),receipt_pins=receipt_pins,manifest=manifest_pin,deployment_count=len(deployment),deployment=deployment,manifest_checks=manifest_checks,canonical_identity=identity,http=dict(url=request.full_url,method='GET',status=http_status,begin_utc=http_start,end_utc=http_end,raw_pin=pin(OUT/(STEM+'_HTTP_STATE.json')),state=state),process=dict(raw_pin=pin(OUT/(STEM+'_PROCESS.json')),record=process_record),fresh_mcp_evidence=dict(evidence_type='RECORDED_FRESH_STDIO_SESSION_CORROBORATED_BY_VERIFIER_SOURCE_AND_INSTALLED_DECLARATIONS; not relaunched in this review',receipt_pin=receipt_pins['LIVE_VERIFICATION_R1'],verifier_pin=pin(verify_path),verifier_lines=anchors,installed_mcp_pin=dict(path=str(BENCH/'mcp_um.py'),sha256=sha(mcp_raw),bytes=len(mcp_raw)),reported_tools=reported,installed_declarations=static_tools,recorded_canonical=oldlive['mcp']['result']['canonical']),limitations=['The historical restart receipt runtime_verified=false is its pre-verification snapshot; the later LIVE receipt and this independent GET verify readiness.', 'The recorded fresh stdio session exposed 28 tools and completed one synthetic call. Existing client sessions were not individually inspected; they may need reconnect and discovery refresh.', 'No claim that all old clients have reconnected, or that old service idle was formally proved.', 'Disk equality plus fresh process/manifest identity does not constitute a dump of every in-memory Python object.', 'Source custody hashes do not imply operator source admission or scientific validation. No statistical significance of nature is computed.'],observed_fit=False,original_um_executed=False,bench_writes=False,restart_performed=False,gate_effect='NONE',review_script=pin(Path(__file__)))
write_new(OUT/(STEM+'.json'),json.dumps(result,ensure_ascii=False,indent=2))
lines=['# Verificação independente da implantação — 10/10/2026','',f"[REAL] Resultado: {'PASS' if result['ok'] else 'FAIL'}. Intervalo: {start} a {end}.",'',f"- {len(deployment)} arquivos instalados: bytes iguais ao candidato e ao recibo; backups conferidos quando havia versão anterior.",f"- Manifesto: {len(manifest_checks['code'])} entradas de código e {len(manifest_checks['sources'])} fontes conferidas por tamanho e SHA-256; nenhuma fonte foi importada ou analisada numericamente.",f"- Programa {version}: `{sha(script_raw)}`; selo: `{sha(seal_raw)}`; vínculo selo→programa conferido.",f"- Manifesto instalado: `{sha(manifest_raw)}`.",f"- GET /api/estado HTTP {http_status}, pronta={state.get('pronta')}, erro={state.get('erro')}; identidade carregada e proveniência do alpha coincidem com os bytes atuais.",f"- Processo {rst['new_server']}, socket 127.0.0.1:18777, início e comando conferidos. Atividades no instantâneo: {state.get('atividades')}.",'- MCP: o recibo LIVE guarda uma sessão stdio nova, 28 ferramentas distintas e chamada sintética; o verificador inicia mcp_um.py instalado, inicializa a sessão e consulta a lista. Os 28 nomes coincidem com as declarações atuais por AST, sem importar o módulo nesta revisão.','', '## Limites','', 'A sessão MCP registrada é nova; esta revisão não mede a reconexão de cada sessão antiga. Clientes ainda conectados à descoberta anterior precisam reconectar/atualizar sua lista. O runtime_verified=false do recibo de reinício é o retrato anterior à verificação LIVE, não o estado medido agora.','', 'A igualdade de arquivos e a identidade do processo não são um despejo de todos os objetos em RAM. Não se alegou ociosidade formal do serviço anterior. Custódia não é admissão pelo operador. Nenhum fit, abertura de dado, reinício ou escrita na Bancada foi feito; não há sigma de natureza e o gate permanece intocado.','', '## Reaproveitamento','', 'F0.3.B2 não consta do grafo Nós Vivo; a consulta F0.3 localizou a custódia v391 e a validação canônica existente. O relatório reutiliza DEPLOY_RECEIPT_R1, RESTART_RECEIPT_R1 e LIVE_VERIFICATION_R1 e acrescenta leitura independente dos bytes e do estado atual.','', '## Evidências','',f'- JSON completo: `{STEM}.json`.',f'- HTTP bruto: `{STEM}_HTTP_STATE.json`.',f'- Processo/socket: `{STEM}_PROCESS.json`.']
if failures:lines.extend(['','## Falhas','']+['- '+x for x in failures])
write_new(OUT/(STEM+'.md'),'\n'.join(lines)+'\n')
print(json.dumps(dict(ok=result['ok'],failures=failures,deployed=len(deployment),code=len(manifest_checks['code']),sources=len(manifest_checks['sources']),tools=len(reported),json=pin(OUT/(STEM+'.json')),md=pin(OUT/(STEM+'.md'))),ensure_ascii=False))