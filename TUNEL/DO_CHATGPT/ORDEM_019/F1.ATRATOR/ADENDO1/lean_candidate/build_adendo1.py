"""Sandbox compiler; every attempt is immutable and preserves its source snapshot."""
import datetime, hashlib, json, os, pathlib, subprocess, sys, time
base=pathlib.Path(__file__).resolve().parent
kernel=pathlib.Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")
lean=pathlib.Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe")
name=sys.argv[1]
if name not in {"TheLightReadsItself", "TheSingularityReadsTheAttractorAdendo1"}: raise ValueError(name)
src=base/(name+".lean")
paths=[kernel/".lake/build/lib/lean"]+sorted((kernel/".lake/packages").glob("*/.lake/build/lib/lean"))
if not all(p.is_dir() for p in paths): raise RuntimeError("LEAN_PATH source missing")
env=dict(os.environ, LEAN_PATH=";".join(map(str,paths)))
root=base/"attempts"/name
root.mkdir(parents=True,exist_ok=True)
i=1
while (root/f"{i:03d}").exists(): i+=1
out=root/f"{i:03d}"; out.mkdir()
data=src.read_bytes()
with (out/src.name).open("xb") as f: f.write(data)
cmd=[str(lean),"-o",str(out/(name+".olean")),str(src)]
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
start=now(); t0=time.perf_counter()
r=subprocess.run(cmd,cwd=base,env=env,capture_output=True)
end=now(); seconds=time.perf_counter()-t0
log=r.stdout+r.stderr
with (out/"BUILD.log").open("xb") as f:f.write(log)
receipt=dict(start_utc=start,end_utc=end,seconds=seconds,command=cmd,LEAN_PATH=env["LEAN_PATH"],exit_code=r.returncode,toolchain=subprocess.check_output([str(lean),"--version"]).decode().strip(),source_sha256=hashlib.sha256(data).hexdigest(),attempt=str(out),build_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
with (out/"RECEIPT.json").open("x",encoding="utf-8",newline="\n") as f:json.dump(receipt,f,indent=2,ensure_ascii=False)
print(json.dumps(receipt,ensure_ascii=False))
print(log.decode("utf-8",errors="strict"))
sys.exit(r.returncode)
