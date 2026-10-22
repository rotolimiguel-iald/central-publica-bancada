import datetime, hashlib, json, os, pathlib, subprocess, time

base = pathlib.Path(__file__).resolve().parent
kernel = pathlib.Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
lean = pathlib.Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
src = base / 'OpticalPopulationBridgeR2.lean'
paths = [kernel / '.lake/build/lib/lean'] + sorted((kernel / '.lake/packages').glob('*/.lake/build/lib/lean'))
env = dict(os.environ, LEAN_PATH=';'.join(map(str, paths)))
attempts = base / 'attempts'
idx = 1
while (attempts / f'{idx:03d}').exists():
    idx += 1
out = attempts / f'{idx:03d}'
out.mkdir()
data = src.read_bytes()
(out / src.name).write_bytes(data)
cmd = [str(lean), '-o', str(out / 'OpticalPopulationBridgeR2.olean'), str(src)]
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
t0 = time.perf_counter()
r = subprocess.run(cmd, cwd=base, env=env, capture_output=True)
duration = time.perf_counter() - t0
end = datetime.datetime.now(datetime.timezone.utc).isoformat()
(out / 'BUILD.log').write_bytes(r.stdout + r.stderr)
receipt = {'start_utc': start, 'end_utc': end, 'seconds': duration, 'command': cmd,
           'LEAN_PATH': env['LEAN_PATH'], 'exit_code': r.returncode,
           'toolchain': subprocess.check_output([str(lean), '--version'], text=True).strip(),
           'source_sha256': hashlib.sha256(data).hexdigest(), 'attempt': idx}
(out / 'RECEIPT.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
print(json.dumps(receipt, ensure_ascii=False))
print((r.stdout+r.stderr).decode('utf-8', 'replace'))
raise SystemExit(r.returncode)
