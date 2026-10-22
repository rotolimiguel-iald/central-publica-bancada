import pathlib,os,subprocess,time,datetime,json,hashlib
base=pathlib.Path(__file__).resolve().parent
kernel=pathlib.Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")
lean=pathlib.Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe")
src=base/"TGLExt/TimeGravitonMatrix.lean"
root=base/"attempts";root.mkdir(exist_ok=True)
i=1
while(root/f"{i:03d}").exists():i+=1
out=root/f"{i:03d}";out.mkdir()
b=src.read_bytes();(out/src.name).write_bytes(b)
paths=[kernel/".lake/build/lib/lean"]+sorted((kernel/".lake/packages").glob("*/.lake/build/lib/lean"))
env=dict(os.environ,LEAN_PATH=";".join(map(str,paths)))
cmd=[str(lean),"-o",str(out/"TimeGravitonMatrix.olean"),str(src)]
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
start=now();t=time.perf_counter()
r=subprocess.run(cmd,cwd=base,env=env,capture_output=True)
end=now();seconds=time.perf_counter()-t
meta=dict(start_utc=start,end_utc=end,seconds=seconds,command=cmd,LEAN_PATH=env["LEAN_PATH"],exit_code=r.returncode,source_sha256=hashlib.sha256(b).hexdigest(),toolchain=subprocess.check_output([str(lean),"--version"]).decode().strip())
(out/"STDOUT.log").write_bytes(r.stdout+r.stderr)
(out/"BUILD.log").write_bytes(json.dumps(meta,ensure_ascii=False,indent=2).encode()+b"\n--- LEAN ---\n"+r.stdout+r.stderr)
with(out/"RECEIPT.json").open("x",encoding="utf-8")as f:json.dump(meta,f,ensure_ascii=False,indent=2)
print(json.dumps(meta,ensure_ascii=False));print((r.stdout+r.stderr).decode())
raise SystemExit(r.returncode)
