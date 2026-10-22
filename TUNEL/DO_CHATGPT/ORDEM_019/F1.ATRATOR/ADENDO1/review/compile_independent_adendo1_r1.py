"""Independent exact-source recompilation; outputs only in a fresh review sandbox."""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, time

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'review' / 'lean_independent'
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
FINAL = BASE / 'lean_candidate' / 'FINAL_LEAN_ADENDO1_R1.json'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(p, raw):
    with Path(p).open('xb') as f: f.write(raw)
    assert Path(p).read_bytes() == raw
def putj(p, v): put(p, (json.dumps(v, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

OUT.mkdir(exist_ok=False)
final = json.loads(FINAL.read_text(encoding='utf-8'))
prereg = json.loads((BASE / 'PREREGISTRO_ADENDO1_R1.json').read_text(encoding='utf-8'))
paths = [KERNEL / '.lake/build/lib/lean'] + sorted((KERNEL / '.lake/packages').glob('*/.lake/build/lib/lean'))
assert all(p.is_dir() and p.is_relative_to(KERNEL / '.lake') for p in paths)
env = dict(os.environ, LEAN_PATH=';'.join(map(str, paths)))
version = subprocess.check_output([str(LEAN), '--version'], text=True).strip()
assert '4.31.0' in version
results = []
for entry in final['accepted']:
    src = Path(entry['source']['path'])
    raw = src.read_bytes()
    assert sha(src) == entry['source']['sha256']
    assert re.search(r'\bsorry\b|\badmit\b|\baxiom\s', raw.decode('utf-8')) is None
    spans = []
    for verb in prereg['verbatims']:
        original = Path(verb['source']).read_bytes()
        assert hashlib.sha256(original).hexdigest() == verb['sha256']
        assert raw.count(original) == 1
        spans.append({'id': verb['id'], 'sha256': verb['sha256'], 'offset': raw.index(original), 'bytes': len(original)})
    local = OUT / src.name
    put(local, raw)
    olean = local.with_suffix('.olean')
    cmd = [str(LEAN), '-o', str(olean), str(local)]
    start = now(); tick = time.perf_counter()
    cp = subprocess.run(cmd, cwd=OUT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elapsed = time.perf_counter() - tick; end = now()
    output = cp.stdout + cp.stderr
    log = OUT / (src.stem + '_BUILD.log')
    header = f'COMMAND: {cmd!r}\nTOOLCHAIN: {version}\nLEAN_PATH: {env["LEAN_PATH"]}\nSTART: {start}\nEND: {end}\nSECONDS: {elapsed}\nEXIT: {cp.returncode}\nOUTPUT:\n'
    put(log, header.encode('utf-8') + output)
    axioms = []
    for name, text in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", output.decode('utf-8', 'strict')):
        ax = [x.strip() for x in text.split(',') if x.strip()]
        assert set(ax) <= {'propext', 'Classical.choice', 'Quot.sound'}
        axioms.append({'name': name, 'axioms': ax})
    assert sha(src) == sha(local) == entry['source']['sha256']
    original_olean = Path(entry['olean']['path'])
    assert sha(original_olean) == entry['olean']['sha256']
    rec = {'source': str(src), 'source_sha256': sha(src), 'copy': str(local), 'copy_sha256': sha(local),
           'final_receipt': str(FINAL), 'final_receipt_sha256': sha(FINAL), 'command': cmd,
           'cwd': str(OUT), 'toolchain': version, 'LEAN_PATH': env['LEAN_PATH'], 'start_utc': start,
           'end_utc': end, 'seconds': elapsed, 'exit_code': cp.returncode, 'axioms': axioms,
           'printed_count': len(axioms), 'sorry_source': False, 'sorryAx_log': b'sorryAx' in output,
           'verbatim_spans': spans, 'olean': str(olean), 'olean_sha256': sha(olean) if olean.exists() else None,
           'original_olean': str(original_olean), 'original_olean_sha256': sha(original_olean),
           'olean_byte_identical': olean.exists() and olean.read_bytes() == original_olean.read_bytes(),
           'log': str(log), 'log_sha256': sha(log)}
    putj(OUT / (src.stem + '_RECEIPT.json'), rec)
    results.append(rec)
    print(json.dumps({'source': src.name, 'exit': cp.returncode, 'seconds': elapsed, 'printed': len(axioms), 'olean_identical': rec['olean_byte_identical']}), flush=True)
    assert cp.returncode == 0 and not rec['sorryAx_log']
    assert len(axioms) == entry['printed_declarations']
    assert rec['olean_byte_identical']
putj(OUT / 'INDEPENDENT_BUILD_RESULT.json', {'created_utc': now(), 'status': 'PASSA', 'script_sha256': sha(__file__), 'builds': results})
