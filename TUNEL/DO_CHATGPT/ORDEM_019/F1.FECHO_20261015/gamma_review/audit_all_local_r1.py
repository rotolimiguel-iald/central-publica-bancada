from pathlib import Path
import datetime, hashlib, json, os, subprocess, time

B = Path(__file__).resolve().parent
NAMES = ['lift', 'positive', 'tomita']
PREFIXES = ['F1Fecho.ExponentialLift', 'F1Fecho.ExponentialLiftPositive', 'F1Fecho.ExponentialTomita']
TRIO = {'propext', 'Classical.choice', 'Quot.sound'}

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

def put(p, s):
    if isinstance(s, str):
        s = s.encode('utf-8')
    with p.open('xb') as f:
        f.write(s)

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

rows = []
paths = []
deps = [pin(__file__)]
for name in NAMES:
    rp = B / name / 'RECEIPT_R1.json'
    r = json.loads(rp.read_text(encoding='utf-8'))
    assert r['passed'] and r['exit_code'] == 0
    rows.append(r)
    deps.extend([pin(rp), pin(r['source']['path']), pin(r['olean']['path'])])
    paths.extend(r['LEAN_PATH'].split(';'))
paths = list(dict.fromkeys(paths))
modules = [Path(r['source']['path']).stem for r in rows]
assert 'CanonicalWeylAssemblyR3' not in modules
for r, module in zip(rows, modules):
    own = Path(r['olean']['path']).parent
    paths = [str(own)] + [x for x in paths if not (Path(x) / (module + '.olean')).is_file()]

D = B / 'all_local'
D.mkdir(exist_ok=False)
src = D / 'AllLocalAuditR1.lean'
olean = D / 'AllLocalAuditR1.olean'
source = '\n'.join('import ' + m for m in modules) + '\nimport Lean\n\n'
source += '''open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let roots : List Name := [''' + ', '.join('`' + p for p in modules) + ''']
  let indices := roots.filterMap env.getModuleIdx?
  unless indices.length == roots.length do throwError "MISSING_MODULE_REFUSED"
  let mut count := 0
  for (n, ci) in env.constants.toList do
    if (env.getModuleIdxFor? n).any (fun i => indices.contains i) then
      count := count + 1
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\\t" ++ n.toString ++ "\\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
  if count == 0 then throwError "EMPTY_AUDIT_REFUSED"
  IO.println ("AUDITED_COUNT\\t" ++ toString count)
'''
put(src, source)
deps.append(pin(src))
cmd = [rows[0]['command'][0], '-R', str(D), '-o', str(olean), str(src)]
lean_path = ';'.join([str(D)] + paths)
toolchain = subprocess.check_output([cmd[0], '--version'], text=True, encoding='utf-8').strip()
start = now()
tick = time.perf_counter()
result = subprocess.run(cmd, cwd=D, env=dict(os.environ, LEAN_PATH=lean_path), capture_output=True)
seconds = time.perf_counter() - tick
end = now()
put(D / 'STDOUT.log', result.stdout)
put(D / 'STDERR.log', result.stderr)
axioms = {}
for line in result.stdout.decode('utf-8').splitlines():
    if line.startswith('LOCAL_DECL\t'):
        _, name, a = line.split('\t')
        axioms[name] = [x for x in a.split(',') if x]
counts = {p: sum(name == p or (p + '.') in name for name in axioms) for p in PREFIXES}
for p in deps:
    assert pin(p['path'])['sha256'] == p['sha256']
passed = (result.returncode == 0 and all(counts.values())
          and all(set(a) <= TRIO for a in axioms.values())
          and b'sorryAx' not in result.stdout + result.stderr)
r = {'unit': 'F1.FECHO_20261015', 'claim': 845, 'start_utc': start, 'end_utc': end,
     'seconds': seconds, 'command': cmd, 'toolchain': toolchain, 'LEAN_PATH': lean_path,
     'exit_code': result.returncode, 'passed': passed, 'all_decl_count': len(axioms),
     'counts': counts, 'axioms': axioms, 'dependencies_before_after': deps,
     'source': pin(src), 'stdout': pin(D / 'STDOUT.log'), 'stderr': pin(D / 'STDERR.log'),
     'olean': pin(olean) if olean.exists() else None,
     'scope': 'All declarations owned by the three imported modules, including private helpers, selected by getModuleIdxFor? from env.constants.toList.',
     'originals_memory_production_gate_modified': False}
put(D / 'BUILD.log', json.dumps({k: r[k] for k in ['start_utc', 'end_utc', 'seconds', 'command', 'toolchain', 'LEAN_PATH', 'exit_code']}, ensure_ascii=False, indent=2)
    + '\nSTDOUT\n' + result.stdout.decode('utf-8') + '\nSTDERR\n' + result.stderr.decode('utf-8'))
r['build'] = pin(D / 'BUILD.log')
put(D / 'RECEIPT_R1.json', json.dumps(r, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'passed': passed, 'exit': result.returncode, 'seconds': seconds,
                  'count': len(axioms), 'counts': counts, 'receipt': pin(D / 'RECEIPT_R1.json')}, ensure_ascii=False))
raise SystemExit(0 if passed else 1)
