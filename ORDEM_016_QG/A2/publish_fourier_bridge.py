from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
folder = root / 'A2'
out = root.parent / 'TUNEL/DO_CHATGPT'
stamp = datetime.datetime.now(datetime.timezone.utc)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def create(p, data):
    assert not p.exists(), p
    tmp = p.with_name(p.name + '.tmp')
    with tmp.open('xb') as f: f.write(data)
    assert tmp.read_bytes() == data
    tmp.rename(p)
def replace(p, data):
    create(p.with_name(p.name + '.bak_' + stamp.strftime('%Y%m%d_%H%M%S_%f')), p.read_bytes())
    tmp = p.with_name(p.name + '.tmp')
    with tmp.open('xb') as f: f.write(data)
    assert tmp.read_bytes() == data
    tmp.replace(p)

pairs = [('RetaDeLuzBorchersAudited', 'lightray_01'),
         ('FourierLightRayBridge', 'fourier_bridge_01'),
         ('FourierStandardTransport_v3', 'fourier_standard_03')]
args = [sys.executable, '-X', 'utf8', '-B', str(root / 'A0/auditar_axiomas.py')]
artifacts = []
for source, label in pairs:
    src, log, rec = folder / f'{source}.lean', folder / f'{label}.log', folder / f'{label}.json'
    r = json.loads(rec.read_bytes())
    assert r['rc'] == 0 and not r['newer_kernel_files'] and not r['scan_errors']
    assert sha(src) == r['source_sha256'] and sha(log) == r['log_sha256']
    args += [str(src), str(log)]
    artifacts += [{'file': str(p), 'sha256': sha(p)} for p in [src, log, rec]]
audit = subprocess.run(args, capture_output=True)
assert audit.returncode == 0, audit.stdout + audit.stderr
create(folder / 'fourier_bridge_axioms.json', audit.stdout)
receipts = []
for label in ['lightray_01', 'fourier_bridge_01', 'fourier_standard_01', 'fourier_standard_02', 'fourier_standard_03']:
    p = folder / f'{label}.json'
    r = json.loads(p.read_bytes())
    receipts.append(dict(file=str(p), sha256=sha(p), rc=r['rc'], wall_seconds=r['wall_seconds'],
                         cpu_seconds=r['cpu_user_seconds'] + r['cpu_kernel_seconds'], utc=r['utc']))
wall = sum(r['wall_seconds'] for r in receipts)
cpu = sum(r['cpu_seconds'] for r in receipts)
opening = sha(out / 'ENTREGA_016_ABERTURA_operador.md')
ledger = [json.loads(l) for l in (out / 'LEDGER_016.jsonl').read_text().splitlines() if l]
cost = sum(float(r.get('custo_usd') or 0) for r in ledger)
tokens = sum(sum(int(r.get(k) or 0) for k in ('tokens_in','tokens_cache','tokens_out')) for r in ledger)
bench = (stamp - min(datetime.datetime.fromisoformat(r['utc']) for r in receipts)).total_seconds()/3600
manifest = dict(utc=stamp.isoformat(), opening_sha256=opening, artifacts=artifacts,
                compilation_attempts=receipts, audit_sha256=sha(folder / 'fourier_bridge_axioms.json'),
                wall_hours=wall/3600, cpu_hours=cpu/3600, observed_bench_hours=bench,
                executor_tokens=tokens, external_cost_usd=cost, gate_moved=False,
                scope='Fourier intertwining, explicit logarithmic phase, exact spectral graph/domain and transported standard subspace',
                not_claimed=['abstract unbounded functional calculus implemented in Mathlib',
                             'half-sided isotony', 'nondefinitional uniqueness of 2*pi', 'physical AQFT pair'])
create(folder / 'fourier_delivery_manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode())
text = f'''[REAL] A-2.2.a — ponte explícita de Fourier e transporte do subespaço padrão compilados.

Abertura SHA256: {opening}

[DERIVED — Lean isolado] Reutilizando fourier_shift, provou-se F D(s) = M_exp(-2πisω) F e, em s=2πt, F D(2πt)=M_exp(it log δ) F, onde δ(ω)=exp(-2c0ω), c0=2π². A constante não é ajustada: a igualdade dos coeficientes fixa c0 nesta convenção de Fourier. Essa igualdade NÃO é ainda a prova de que Borchers força 2π.

O símbolo δ está ligado ao operador EXISTENTE continuousModularDelta, pelo grafo e pelo domínio exatos. A segunda pedra constrói rapidityStandardSubspace(c)=F⁻¹K_c como StandardSubspace real fechado, cíclico e separante; prova a condição de ponto fixo transportada, o grafo da Delta transportada e sua condição de domínio. Nenhum operador canônico foi substituído por homônimo. O grupo de fase aqui é o multiplicador explícito exp(it log δ); não se anuncia um cálculo funcional abstrato ilimitado que a biblioteca não fornece.

Reprodução da reta de luz: 22 teoremas; ponte: 11 teoremas; transporte: 5 teoremas e a definição do StandardSubspace também com #print axioms. Auditoria integral das declarações nas três fontes: trio permitido, zero sorry/axioma novo. Duas falhas anteriores de transporte preservadas: instâncias reais distintas (Lp.instModule versus complexToReal) impediam as reescritas; a terceira versão fixa a instância Module efetivamente usada. Três ciclos, abaixo do teto seis.

Estado: PAGO para a ponte explícita A-2.2.a no escopo acima; revisão por outro provedor ainda pendente. A-2.3 permanece NÃO PAGO: isotonia da meia-reta, densidade/core/Hardy e controles de largura/sinal. O pedido MiMo A2.3.a foi preparado sem execução, para trabalhar nessa lacuna específica; resposta de modelo não substituirá compilação.

Recursos (incluem as duas tentativas falhas): {wall/3600:.9f}h parede Lean, {cpu/3600:.9f}h CPU; intervalo observado de bancada {bench:.6f}h (não estimativa de atenção exclusiva). Zero alteração canônica detectada em cada compilação. Ledger até esta entrega: US${cost}, tokens executores {tokens}; coordenação não mensurada nesse total. B pesada 0h. Não move gate.

Artefatos e SHA256:
'''
text += '\n'.join(f"- {a['file']} — {a['sha256']}" for a in artifacts)
text += f"\n- Auditoria: {folder/'fourier_bridge_axioms.json'} — {sha(folder/'fourier_bridge_axioms.json')}\n- Manifesto: {folder/'fourier_delivery_manifest.json'} — {sha(folder/'fourier_delivery_manifest.json')}\n"
report = out / 'ENTREGA_016_A2_2_ponte_fourier.md'
create(report, text.encode())
p = out / 'ENTREGA_016_PROGRESSO.md'
addition = f'\n{stamp.isoformat()} | A-2.2.a | PAGO no escopo de ponte Fourier/Delta/K; isotonia e 2π forçado em A2.3 pendentes | bancada observada {bench:.6f}h, Lean {wall/3600:.9f}h parede, {cpu/3600:.9f}h CPU; ledger US${cost}, tokens {tokens}; B pesada 0h | A-2.3.a próximo.\n'.encode()
replace(p, p.read_bytes() + addition)
print(json.dumps({'report':str(report), 'sha256':sha(report), 'audit_rc':audit.returncode, 'attempts':len(receipts)}))
