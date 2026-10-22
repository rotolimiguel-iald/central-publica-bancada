r"""P7: reproduce eligible P2 files over a new copy of the pinned v371 kernel.

Usage: python -X utf8 -B reproduzir.py --work C:\path\new_directory --expected-ready-sha256 HASH
Requires the recorded Lean 4.31.0 toolchain and read-only Mathlib dependencies.
Never runs lake build, um.py, a provider, or the management gate reader.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, shutil, subprocess, sys, time

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, obj):
    raw=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
    if p.exists():raise FileExistsError(p)
    t=p.with_suffix(p.suffix+'.tmp');t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work',required=True)
    parser.add_argument('--expected-ready-sha256',required=True,help='External management pin, received independently of this package')
    args=parser.parse_args()
    package=Path(__file__).resolve().parent;work=Path(args.work).resolve()
    if work.exists() or work.is_relative_to(package):raise ValueError('Use a new output directory outside the sealed package')
    if not args.expected_ready_sha256 or sha(package/'PRONTO.json') != args.expected_ready_sha256:
        raise ValueError('EXTERNAL_READY_PIN_MISMATCH')
    ready=json.loads((package/'PRONTO.json').read_bytes())
    for rel,expected in ready['files'].items():
        p=(package/rel).resolve()
        if not p.is_relative_to(package) or sha(p)!=expected:raise ValueError('PACKAGE_HASH_MISMATCH: '+rel)
    snapshot=json.loads((package/'evidencias/KERNEL_SNAPSHOT.json').read_bytes())
    base=package/'kernel_v371'
    for row in snapshot['formal_sources']+snapshot['copied_build']:
        if sha(base/row['path'])!=row['sha256']:raise ValueError('BASE_HASH_MISMATCH: '+row['path'])
    cfg=json.loads((package/'REPRODUCAO_CONFIG.json').read_bytes())
    for p in cfg['external_imports']:
        if not Path(p).is_dir():raise FileNotFoundError('MATHLIB_DEPENDENCY_MISSING: '+p)
    if not Path(cfg['lake']).is_file():raise FileNotFoundError(cfg['lake'])
    work.mkdir(parents=True);shutil.copytree(base,work/'kernel_v371')
    shutil.copytree(package/'lean',work/'lean',ignore=shutil.ignore_patterns('*.olean*','*.ilean','*.tmp'))
    envdir=work/'compiler_env';envdir.mkdir()
    for name in ['lean-toolchain','lakefile.toml','lake-manifest.json']:
        shutil.copy2(package/'reproduction_environment'/name,envdir/name)
    configuration=dict(root=str(work/'lean'),cwd=str(envdir),logs=str(work/'logs'),lake=cfg['lake'],
        imports=[str(work/'kernel_v371/.lake/build/lib/lean')]+cfg['external_imports'])
    save(work/'compile_config.json',configuration)
    order=json.loads((package/'P2_COMPILACAO.json').read_bytes())['reproduction_order']
    results=[];started=time.monotonic()
    for index,module in enumerate(order):
        source=work/'lean'/(module+'.lean');label=f'reproduce_{index:03d}_{module}'
        start=time.monotonic()
        result=subprocess.run([sys.executable,'-X','utf8','-B',str(package/'run_lean.py'),str(work/'compile_config.json'),str(source),label],capture_output=True,text=True,encoding='utf-8')
        receipt=work/'logs'/(label+'.json')
        if not receipt.exists():
            results.append(dict(module=module,status='RUNNER_FAILED',stderr=result.stderr,rc=result.returncode));continue
        data=json.loads(receipt.read_bytes());log=receipt.with_suffix('.log').read_text('utf-8',errors='replace')
        axioms=[line for line in log.splitlines() if line.startswith('BENCH_DECL\t') or 'depends on axioms' in line or 'does not depend on any axioms' in line]
        results.append(dict(module=module,rc=data['rc'],seconds=time.monotonic()-start,receipt=str(receipt),receipt_sha256=sha(receipt),axioms=axioms))
        print(json.dumps(dict(module=module,rc=data['rc'],wall_seconds=data['wall_seconds'],cpu_seconds=data['cpu_seconds'],axiom_lines=len(axioms))),flush=True)
        for line in axioms:print(line,flush=True)
    save(work/'REPRODUCAO_RESULTADO.json',dict(at=datetime.now(timezone.utc).isoformat(),package_ready_sha256=sha(package/'PRONTO.json'),
        seconds=time.monotonic()-started,files=results,gate_changed=False))
    sys.exit(0 if results and all(x.get('rc')==0 for x in results) else 1)
if __name__=='__main__':main()
