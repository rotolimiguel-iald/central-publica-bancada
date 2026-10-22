from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
folder = root / 'A2'
out = root.parent / 'TUNEL/DO_CHATGPT'
now = datetime.now(timezone.utc)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def create(path, data):
    assert not path.exists(), path
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(data)
    assert temp.read_bytes() == data
    temp.rename(path)

def append(path, data):
    old = path.read_bytes()
    create(path.with_name(path.name + '.bak_' + now.strftime('%Y%m%d_%H%M%S_%f')), old)
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(old + data)
    assert temp.read_bytes() == old + data
    temp.replace(path)

passed = [('LightRayRealFourierUniqueness_v2.lean', 'real_fourier_unique_02'),
          ('LightRayDensitySeparation_v2.lean', 'density_separation_02')]
if len(sys.argv) == 3:
    passed.append((sys.argv[1], sys.argv[2]))
records = []
args = [sys.executable, '-X', 'utf8', '-B', str(root/'A0/auditar_axiomas.py')]
for source, label in passed:
    receipt = json.loads((folder/(label+'.json')).read_bytes())
    assert receipt['rc'] == 0
    assert receipt['source_sha256'] == sha(folder/source)
    assert receipt['log_sha256'] == sha(folder/(label+'.log'))
    assert not receipt['newer_kernel_files'] and not receipt['scan_errors']
    records.append({'source': source, 'source_sha256': sha(folder/source),
                    'receipt': label+'.json', 'receipt_sha256': sha(folder/(label+'.json')),
                    'log': label+'.log', 'log_sha256': sha(folder/(label+'.log'))})
    args.extend([str(folder/source), str(folder/(label+'.log'))])
audit = subprocess.run(args, capture_output=True)
assert audit.returncode == 0, audit.stdout + audit.stderr
create(folder/'density_separation_axioms.json', audit.stdout)
audits = json.loads(audit.stdout)
count = sum(a['n_theorem_lemma_na_fonte'] for a in audits)

providers = []
for prefix in ['a23_kimi_direct', 'a23_mimo_medium', 'a23_gemini_low']:
    path = folder/(prefix+'_stdout.json')
    data = json.loads(path.read_bytes())
    result = data.get('result') or {}
    usage = result.get('usage') or {}
    accounting = result.get('request_cost_accounting') or {}
    providers.append({'provider': data['execution_constraints']['required_provider'],
                      'request_id': data['request_id'], 'task_id': data['id'],
                      'status': data['status'], 'artifact': path.name, 'sha256': sha(path),
                      'elapsed_seconds': result.get('elapsed_seconds'),
                      'input_tokens': usage.get('input_tokens', usage.get('prompt_tokens')),
                      'output_tokens': usage.get('output_tokens', usage.get('completion_tokens')),
                      'total_tokens': usage.get('total_tokens'),
                      'reasoning_tokens': usage.get('thinking_tokens',
                          (usage.get('completion_tokens_details') or {}).get('reasoning_tokens')),
                      'cost_usd': accounting.get('accounted_usd', usage.get('cost_usd')),
                      'cost_status': accounting.get('status', 'NOT_REPORTED'),
                      'raw_usage': usage or None})
mimo = next(p for p in providers if p['provider'] == 'mimo')
ledger_entry = dict(mimo, event='usage_normalization_correction', ts=now.isoformat(),
                    alvo='A-2', ramo='A-2.3.a', provedor='mimo',
                    execution_task_id=mimo['task_id'], tokens_in=mimo['input_tokens'],
                    tokens_out=mimo['output_tokens'], tokens_total_reported=mimo['total_tokens'],
                    tokens_thinking_reported=mimo['reasoning_tokens'],
                    custo_usd=mimo['cost_usd'], supersedes_fields_only=True,
                    reason='Provider uses prompt_tokens/completion_tokens; previous raw_usage preserved. Cost is token-priced estimate, not invoice. This is NOT another call.')
append(out/'LEDGER_016.jsonl', (json.dumps(ledger_entry, ensure_ascii=False)+'\n').encode())

receipts = []
for pattern in ['real_fourier_unique_*.json', 'density_separation_0*.json', 'gaussian_transform_0*.json']:
    for path in sorted(folder.glob(pattern)):
        record = json.loads(path.read_bytes())
        if 'wall_seconds' in record:
            receipts.append(dict(record, file=path.name))
wall = sum(r['wall_seconds'] for r in receipts)
cpu = sum(r['cpu_user_seconds']+r['cpu_kernel_seconds'] for r in receipts)
bench = (now-min(datetime.fromisoformat(r['utc']) for r in receipts)).total_seconds()
opening = sha(out/'ENTREGA_016_ABERTURA_operador.md')
known = sum(Decimal(str(p['cost_usd'])) for p in providers if p['cost_usd'] is not None)
manifest = {'status': 'REAL_ISOLATED_PARTIAL_DENSITY', 'utc': now.isoformat(),
            'opening_sha256': opening, 'records': records, 'compiled_theorems': count,
            'audit_sha256': sha(folder/'density_separation_axioms.json'),
            'providers': providers, 'machine_wall_seconds': wall, 'machine_cpu_seconds': cpu,
            'bench_window_seconds': bench, 'compile_attempts': [r['file'] for r in receipts],
            'density': 'OPEN_REAL_ORTHOGONALITY_AND_CLOSURE', 'gate_changed': False,
            'mimo_review': {'formula': 'CORRECT_COEFFICIENT',
                           'derivation': 'SIGN_ERROR_IN_COMPLETED_SQUARE_AND_UNJUSTIFIED_COMPLEX_CONTOUR_SHIFT',
                           'correct_square': '-b*u^2+A*u=-b*(u-A/(2*b))^2+A^2/(4*b)'}}
create(folder/'density_separation_manifest.json', json.dumps(manifest, indent=2, ensure_ascii=False).encode())
report = f'''[REAL] A-2.3.a: separação espectral compilada e divisão operacional retomada.

Abertura SHA256: {opening}

**Matemática.** Mais {count} teoremas auditados nesta entrega. Para H no subespaço padrão K_c e g real, positiva quase em toda parte, em L² e com g(-p)=exp(-cp)g(p), a anulação da parte real de F(conj(H)g) implica H=0. A prova usa a unicidade Fourier já existente, a relação modular efetiva de K_c e o fator estritamente positivo 1+exp(-2cp). Não substitui densidade real por densidade complexa. Densidade integral e meia-inclusão ainda exigem ligar a ortogonalidade dos vetores gaussianos a essa transformada e aplicar o fecho real.

**MiMo — tarefa média concluída.** Conferiu a candidata Ff_r(p)=sqrt(π/b) exp(-π²p²/b+π²p) exp(-2πirp). A fórmula está correta, mas o texto recebido contém uma igualdade falsa no passo 3: o quadrado correto é -b(u-A/(2b))²+A²/(4b), com MENOS, não mais. Além disso, a substituição complexa não devolve automaticamente uma integral sobre a reta real; exige deslocamento de contorno justificado. A resposta original foi preservada. A integração local usa o teorema de integral gaussiana quadrática do Mathlib, cuja prova inclui esse deslocamento, e mantém o compilador como verificação.

**Gemini/Antigravity — tarefa baixa concluída.** Conferiu o inventário fornecido de 20 teoremas anteriores e assinalou corretamente a hipótese de densidade ainda aberta. Sua leitura de JSON não é recompilação independente. **Kimi — tarefa alta não executada pelo modelo.** A sessão de infraestrutura encontrou falha de conexão na renovação OAuth, zero llm.request e nenhum usage.record de inferência; não há evidência de cota esgotada. Não houve repetição automática da unidade.

**Divisão retomada.** A tarefa “Orquestrar IAs na Central IALD” cuida da fila, dos adaptadores e do diagnóstico; esta bancada integra as respostas e constrói/verifica Lean. IDs compartilhados para impedir duplicação. A nova ordem torna Física assistência opcional; mantém memória comum, executor fixado e proteção contra reexecução incerta. Não altera o alcance das provas.

**Uso medido.** MiMo: {mimo['input_tokens']} entrada, {mimo['output_tokens']} saída, {mimo['reasoning_tokens']} de raciocínio incluídos na saída, {mimo['total_tokens']} total; {mimo['elapsed_seconds']} s; US$ {mimo['cost_usd']} estimados pelos tokens, não fatura. Gemini: consumo no manifesto. Custo conhecido destas três unidades: US$ {known}; custos sem informação continuam desconhecidos. A correção de normalização do ledger é aditiva e não conta nova chamada. Lean: {wall/3600:.9f} h parede e {cpu/3600:.9f} h CPU em {len(receipts)} recibos; janela de bancada {bench/3600:.6f} h, sem afirmar dedicação exclusiva. Nenhuma execução pesada da Parte B.

**Custódia.** rc0 nos arquivos aprovados, cobertura integral de #print axioms, somente trio permitido, nenhum sorry/axioma novo. Tentativas falhas preservadas; fontes e logs conferidos por SHA256. Nenhuma escrita em um.py/kernel canônico e nenhum movimento de gate.

Manifesto: {folder/'density_separation_manifest.json'}
SHA256: {sha(folder/'density_separation_manifest.json')}
Auditoria: {folder/'density_separation_axioms.json'}
SHA256: {sha(folder/'density_separation_axioms.json')}
'''
destination = out/'ENTREGA_016_MEDIDA_A2_3a_separacao_e_orquestracao.md'
create(destination, report.encode())
append(out/'ENTREGA_016_PROGRESSO.md',
       f'\n{now.isoformat()} | A-2.3.a EM CURSO/MEDIDA | +{count} teoremas: separação por Fourier real; densidade OPEN | MiMo e Gemini concluídos, Kimi falhou antes da inferência; divisão retomada | Lean {wall/3600:.9f}h parede / {cpu/3600:.9f}h CPU; bancada {bench/3600:.6f}h. US${known} conhecido nestas unidades, demais custos desconhecidos; B pesada 0h.\n'.encode())
print(json.dumps({'report': str(destination), 'sha256': sha(destination), 'theorems': count,
                  'providers': [{k:p[k] for k in ['provider','status','total_tokens','cost_usd']} for p in providers]}, ensure_ascii=False))
