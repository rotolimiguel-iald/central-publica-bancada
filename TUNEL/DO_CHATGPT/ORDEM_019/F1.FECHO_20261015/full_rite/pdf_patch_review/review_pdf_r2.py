from pathlib import Path
import ast, contextlib, datetime, hashlib, io, json, os, subprocess, types

B = Path(__file__).resolve().parent
P = B.parent
patch = P / 'compile_pdf_offline_r2.py'
receipt = P / 'pdf_patch_r2/PDF_PATCH_RECEIPT_R2.json'

def pin(p):
    p = Path(p); raw = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def put(p, text):
    with p.open('x', encoding='utf-8', newline='\n') as f:
        f.write(text)

r = json.loads(receipt.read_text(encoding='utf-8'))
assert r['passed'] and all(c['passed'] for c in r['checks'])
verified = {}
def verify(x):
    if isinstance(x, dict):
        if 'path' in x and 'sha256' in x:
            actual = pin(x['path']); assert actual['sha256'] == x['sha256']
            verified[x['path']] = actual
        else:
            for y in x.values(): verify(y)
    elif isinstance(x, list):
        for y in x: verify(y)
verify(r)
source = patch.read_text(encoding='utf-8')
tree = ast.parse(source)
assert len(tree.body) == 1 and isinstance(tree.body[0], ast.FunctionDef)
assert tree.body[0].name == 'compile_pdf'
calls = []
checks = []
cases = [
    ('absent_engine', False, True, None, [], True, None, 0),
    ('miktex_two_success', True, True, 'MiKTeX-pdfTeX', [0, 0], True, True, 3),
    ('identify_failure', True, True, 'IDENTITY_FAILURE', [], True, False, 1),
    ('first_pass_fails_old_pdf', True, True, 'MiKTeX', [1], True, False, 2),
    ('second_pass_fails_old_pdf', True, True, 'MiKTeX', [0, 1], True, False, 3),
    ('two_success_no_pdf', True, True, 'MiKTeX', [0, 0], False, False, 3),
    ('timeout_refused', True, True, 'MiKTeX', ['TIMEOUT'], True, False, 2),
    ('unknown_engine_scope', True, True, 'OtherEngine 1.0', [0, 0], True, True, 3),
    ('legacy_online_mode', True, False, None, [0, 0], True, True, 2),
    ('miktex_identity_stderr', True, True, 'STDERR_MIKTEX', [0, 0], True, True, 3),
]
for name, available, offline, identity, exits, pdf_exists, expected, ncall in cases:
    sequence = list(exits); invocations = []
    def fake_run(cmd, **kw):
        invocations.append({'command': list(cmd), 'kwargs': {k: str(v) for k, v in kw.items()}})
        if cmd[-1] == '--version':
            return types.SimpleNamespace(returncode=1 if identity == 'IDENTITY_FAILURE' else 0,
                stdout='' if identity == 'STDERR_MIKTEX' else identity or '',
                stderr='MiKTeX' if identity == 'STDERR_MIKTEX' else '')
        code = sequence.pop(0)
        if code == 'TIMEOUT': raise subprocess.TimeoutExpired(cmd, 180)
        return types.SimpleNamespace(returncode=code, stdout='', stderr='')
    fake_os = types.SimpleNamespace(environ={'TGL_NO_NETWORK': '1'} if offline else {},
        path=types.SimpleNamespace(exists=lambda path: pdf_exists, join=os.path.join))
    ns = {'os': fake_os, 'OUT': str(B / name),
          'shutil': types.SimpleNamespace(which=lambda exe: 'PINNED_pdflatex.exe' if available else None),
          'subprocess': types.SimpleNamespace(run=fake_run, DEVNULL=subprocess.DEVNULL)}
    exec(compile(source, str(patch), 'exec'), ns)
    messages = io.StringIO()
    with contextlib.redirect_stdout(messages): actual = ns['compile_pdf']('fixture')
    assert actual is expected and len(invocations) == ncall
    for call in invocations:
        command = call['command']
        if '--version' not in command:
            hardened = offline and identity in {'MiKTeX-pdfTeX', 'MiKTeX', 'STDERR_MIKTEX'}
            assert ('--disable-installer' in command) == hardened
            assert ('--disable-write18' in command) == hardened
            assert '-halt-on-error' in command
    checks.append({'name': name, 'passed': True, 'actual': actual, 'expected': expected,
                   'calls': invocations, 'messages': messages.getvalue()})

native_commands = r['commands']
compile_calls = [x for x in native_commands if '--version' not in x['command']]
assert all('--disable-installer' in x['command'] and '--disable-write18' in x['command'] for x in compile_calls)
assert [x['exit_code'] for x in compile_calls] == [0, 0, 1, 1]
assert b'%PDF-' in (P / 'pdf_patch_r2/local_ok/fixture.pdf').read_bytes()[:10]
assert (P / 'pdf_patch_r2/stale_pdf_then_failure/fixture.pdf').exists()
for key in verified:
    assert pin(key)['sha256'] == verified[key]['sha256']
result = {'unit': 'F1.FECHO_20261015', 'claim': 845,
          'reviewer': 'codex-atrator-skeptic',
          'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'verdict': 'PASSA_COM_ESCOPO_MIKTEX_LOCAL', 'material_findings': [],
          'independent_mock_tests': checks, 'independent_mock_pass_count': len(checks),
          'builder_native_checks_verified': len(r['checks']),
          'native_receipt': pin(receipt), 'patch': pin(patch),
          'verified_native_pins': list(verified.values()), 'script': pin(__file__),
          'findings': [
              'R2 exige exit 0 nas duas passagens, antes de consultar existência do PDF. PDF velho não mascara falha da primeira ou segunda passagem.',
              'Identificação MiKTeX consulta stdout e stderr de --version; falha de identificação ou timeout retorna False. Motor ausente retorna None.',
              'Apenas MiKTeX identificado com TGL_NO_NETWORK=1 recebe as opções documentadas --disable-installer e --disable-write18.',
              'O recibo nativo contém duas passagens bem sucedidas e duas recusas por pacote ausente; 11 verificações e seus pinos conferem. Nesta revisão não se relançou motor nativo: 10 casos independentes com subprocess substituído verificam os ramos.',
              'A fonte de patch contém uma única definição compile_pdf. Aplicação ao candidato completo e comparação das demais funções são responsabilidade da integração posterior.'
          ],
          'scope': ['Não é firewall/sandbox do processo nativo.',
                    'Outros motores e modo sem TGL_NO_NETWORK mantêm opções anteriores; o contrato auditado é o MiKTeX identificado nesta máquina.',
                    'True exige dois exits zero e PDF existente; não valida conteúdo, frescor ou renderização do PDF.',
                    'Os testes independentes não executaram processos externos, provedor, rede, um.py nem dados científicos.'],
          'production_memory_gate_modified': False}
put(B / 'REVISAO_PDF_R2_R1.json', json.dumps(result, ensure_ascii=False, indent=2) + '\n')
md = ['# Revisão independente — patch PDF R2', '',
      '[REAL] **PASSA COM ESCOPO MIKTEX LOCAL**, sem achado material.', '',
      f"10/10 casos independentes simulados passam; 11/11 verificações nativas do construtor e {len(verified)} pinos foram conferidos.", '']
md += ['- ' + x for x in result['findings']]
md += ['', '## Limites', ''] + ['- ' + x for x in result['scope']]
md += ['', 'Relatório JSON contém comandos simulados, hashes e recibo nativo. Nenhuma alteração de produção, memória ou gate.', '']
put(B / 'REVISAO_PDF_R2_R1.md', '\n'.join(md))
print(json.dumps({'verdict': result['verdict'], 'mock_passed': len(checks),
                  'native_verified': len(r['checks']), 'pins': len(verified),
                  'json': pin(B / 'REVISAO_PDF_R2_R1.json'),
                  'md': pin(B / 'REVISAO_PDF_R2_R1.md')}, ensure_ascii=False))
