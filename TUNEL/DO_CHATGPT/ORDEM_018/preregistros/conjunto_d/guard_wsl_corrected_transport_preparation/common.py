"""Pure stdlib protocol helpers. Importing this module runs no control."""
import os, sys, json, hashlib, time
from pathlib import Path, PurePosixPath
REQUEST = "5b67deb6-fec2-43d6-af61-347f1a3e5b83"
SCOPE = "WSL312_ONE_STDLIB_CACHE_LATCH_CONTROL"
CASE = "WSL_CACHE_LATCH_POSIX_002"
WIN = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\preregistros\conjunto_d\guard_wsl_corrected_transport_preparation")
LINUX_ARGV_ROOT = PurePosixPath('/mnt/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/guard_wsl_corrected_transport_preparation')
# POSIX representation for transported tokens; concrete Path is only for host IO.
LINUX = Path(LINUX_ARGV_ROOT.as_posix())
BASE = WIN if os.name == "nt" else LINUX
PY = "/opt/lal_env/bin/python"
FLAGS = ["-I", "-S", "-B", "-X", "utf8"]
SCIENCE = {"lal", "lalsimulation", "numpy", "bilby", "dynesty", "scipy"}
def need(ok, text):
    if not ok: raise RuntimeError(text)
def digest(raw): return hashlib.sha256(raw).hexdigest()
def pin(path):
    raw = Path(path).read_bytes(); return {"bytes": len(raw), "sha256": digest(raw)}
def read(path): return json.loads(Path(path).read_bytes())
def fresh(path, obj):
    raw = (json.dumps(obj, sort_keys=True, allow_nan=False) + "\n").encode()
    with Path(path).open("xb") as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    need(Path(path).read_bytes() == raw, "Receipt readback")
def writefd(fd, raw):
    view = memoryview(raw)
    while view:
        n = os.write(fd, view); need(n > 0, "Incomplete write"); view = view[n:]
    os.fsync(fd)
def no_science(): need(not any(n==x or n.startswith(x+".") for n in sys.modules for x in SCIENCE), "Scientific import forbidden")
def check_pins(c, linux=False):
    for item in c["local_pins"]:
        need(pin(BASE/item["relative_path"]) == {k:item[k] for k in ("bytes","sha256")}, "Local pin mismatch")
    if linux:
        need(os.name == "posix" and sys.version_info[:2] == (3,12), "WSL CPython 3.12 required")
        need(sys.executable == PY and Path(PY).resolve() == Path("/usr/bin/python3.12"), "Interpreter identity")
        for item in c["linux_pins"]:
            need(pin(item["path"]) == {k:item[k] for k in ("bytes","sha256")}, "Linux pin mismatch")
    no_science()
def authorization(c):
    a=read(BASE/"AUTORIZACAO_ROOT.json"); ah=pin(BASE/"AUTORIZACAO_ROOT.json")["sha256"]
    need(a.get("authorized") is True and a.get("request_id")==REQUEST and a.get("scope")==SCOPE, "Specific authorization required")
    need(a.get("contract_sha256")==pin(BASE/"CONTRATO_WSL.json")["sha256"], "Authorization contract mismatch")
    need(a.get("max_control_runs")==1 and a.get("max_control_children")==1 and a.get("nominal_total_s")==60, "Frozen limits")
    name=a.get("review_file", ""); need(name in ("REVISAO_ROOT.json", "REVISAO_ROOT.md"), "Fixed local review")
    need(pin(BASE/name)["sha256"]==a.get("review_sha256") and a.get("review_accepted") is True, "ROOT review absent")
    need(a.get("PE_authorized") is False and a.get("D_authorized") is False, "Wrong scope")
    return a,ah
def proc_identity(pid):
    p=Path("/proc")/str(pid); stat=(p/"stat").read_text(); tail=stat[stat.rfind(")")+2:].split()
    return {"pid":pid,"start_ticks":int(tail[19]),"state":tail[0],"ppid":int(tail[1]),
            "exe":str((p/"exe").resolve(strict=True)),"argv":(p/"cmdline").read_bytes().split(b"\0")[:-1],
            "boot_id":Path("/proc/sys/kernel/random/boot_id").read_text().strip()}
def serial_identity(x): return {**x,"argv":[s.decode() for s in x["argv"]]}
def matches(x, argv):
    return x["exe"]=="/usr/bin/python3.12" and x["argv"]==[s.encode() for s in argv]
def exact_signal(pid, argv):
    import signal
    fd=os.pidfd_open(pid,0)
    try:
        x=proc_identity(pid); need(matches(x,argv), "Process identity changed; no signal")
        signal.pidfd_send_signal(fd,signal.SIGKILL,None,0)
        return serial_identity(x)
    finally: os.close(fd)
def argv_for(role, nonce):
    script="worker.py" if role=="--child" else "linux_control.py"
    return [PY,*FLAGS,(LINUX_ARGV_ROOT/script).as_posix(),role,REQUEST,nonce]
def scoped_processes(nonce):
    targets=[argv_for("--supervisor",nonce),argv_for("--child",nonce)]; found=[]
    for p in Path("/proc").iterdir():
        if not p.name.isdecimal(): continue
        try:
            if p.stat().st_uid != os.getuid(): continue
            x=proc_identity(int(p.name))
        except (FileNotFoundError, ProcessLookupError): continue
        except PermissionError as exc:
            raise RuntimeError("Cannot inspect same-UID process identity; cleanup uncertain") from exc
        for target in targets:
            if matches(x,target): found.append((x,target))
    return found

def observed_argv(role, nonce):
    """Observe this Linux receiver before any control/hook; never infer delivery."""
    expected = argv_for(role, nonce)
    process = serial_identity(proc_identity(os.getpid()))
    received = process["argv"]
    script_received = list(sys.argv)
    script_expected = expected[6:]
    return {"request_id": REQUEST, "nonce": nonce, "role": role, "process": process,
            "expected_process_argv": expected, "received_process_argv": received,
            "expected_script_argv": script_expected, "received_script_argv": script_received,
            "process_argv_matches": received == expected,
            "script_argv_matches": script_received == script_expected}

def validate_observed_argv(row, role, nonce):
    """Recompute expectations in each parent; the receiver's booleans are not proof."""
    expected = argv_for(role, nonce)
    need(row["request_id"] == REQUEST and row["nonce"] == nonce and row["role"] == role,
         "Received argv receipt identity")
    need(row["expected_process_argv"] == expected and row["received_process_argv"] == expected,
         "Received process argv differs from exact expected tokens")
    need(row["process"]["argv"] == expected and row["process"]["exe"] == "/usr/bin/python3.12",
         "Received argv process identity")
    need(row["expected_script_argv"] == expected[6:] and row["received_script_argv"] == expected[6:],
         "Received sys.argv differs from exact expected tokens")
    need(row["process_argv_matches"] is True and row["script_argv_matches"] is True,
         "Received argv equality flags")
