"""Prepared pure unittest child. Only a pinned, claimed supervisor can enter."""
from pathlib import Path
import sys,os,json,hashlib,types,unittest,time,datetime,ast
BASE=Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\preregistros\conjunto_d\guard_doubles_run_preparation")
REQUEST="83bed917-9a88-4505-a26c-0bb75e2f7c86"
def require(ok,message):
    if not ok:raise RuntimeError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def read_json(p):return json.loads(p.read_bytes())
def main():
    require(sys.argv[1:]==["--supervised-stdin"],"Only supervised entry")
    require(Path(__file__).resolve()==BASE/"worker.py","Fixed worker path")
    cp=BASE/"CONTRATO_DOUBLES.json"; contract_bytes=cp.read_bytes();c=json.loads(contract_bytes)
    token=json.loads(sys.stdin.buffer.readline(4097))
    claim=read_json(BASE/"CLAIM.json"); auth=read_json(BASE/"AUTORIZACAO_ROOT.json")
    require(c["request_id"]==REQUEST==claim["request_id"]==token["request_id"]==auth["request_id"],"Request identity")
    require(token["nonce"]==claim["nonce"] and os.getppid()==claim["pid_supervisor"],"Parent/nonce mismatch")
    require(claim["contract_sha256"]==auth["contract_sha256"]==digest(contract_bytes),"Contract pin")
    require(auth["authorized"] is True and auth["scope"]==c["scope"]=="AUDIT_GUARD_21_PURE_DOUBLES_ONLY_ONCE","Authorization")
    require(digest((BASE/"AUTORIZACAO_ROOT.json").read_bytes())==claim["authorization_sha256"],"Authorization changed")
    cache={}
    for pin in c["execution_pins"]:
        b=Path(pin["path"]).read_bytes()
        require(len(b)==pin["bytes"] and digest(b)==pin["sha256"],"Pin mismatch")
        cache[pin["path"]]=b
    require(Path(sys.executable).resolve()==Path(c["interpreter"]).resolve(),"Interpreter")
    reservation={"request_id":REQUEST,"pid":os.getpid(),"parent_pid":os.getppid(),
                 "contract_sha256":digest(contract_bytes),"time_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    encoded=(json.dumps(reservation,sort_keys=True)+"\n").encode()
    # Durable single-use reservation BEFORE candidate/test import or exec.
    with (BASE/"RUN"/"WORKER_CLAIM.json").open("xb") as f:
        f.write(encoded);f.flush();os.fsync(f.fileno())
    names=c["test_names"];sources=c["source_modules"]
    tree=ast.parse(cache[sources["guard_doubles_suite"]].decode("utf-8"))
    cl=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="Doubles")
    found=[n.name for n in cl.body if isinstance(n,ast.FunctionDef) and n.name.startswith("test_")]
    require(found==names and len(names)==21,"Exact prepared21")
    denials=[]
    allowed_imports=set(sys.stdlib_module_names)|{"audit_guard","result_acceptance"}
    allowed_reads={str(Path(p).resolve()).casefold() for p in sources.values()}
    std_roots=[Path(sys.base_prefix)/"Lib",Path(sys.base_prefix)/"DLLs"]
    def guard(event,args):
        forbidden=event.startswith(("subprocess.","socket.","os.spawn")) or event in ("os.system","os.posix_spawn","os.fork","os.forkpty","ctypes.dlopen","ctypes.dlsym")
        if event=="import":forbidden=forbidden or args[0].split(".")[0] not in allowed_imports
        if event=="open":
            target,mode,flags=args
            writing=(isinstance(mode,str) and any(x in mode for x in "wax+")) or (isinstance(flags,int) and bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)))
            forbidden=forbidden or writing
            if not isinstance(target,int):
                p=Path(target).resolve()
                admitted=str(p).casefold() in allowed_reads or any(p.is_relative_to(q) for q in std_roots)
                forbidden=forbidden or not admitted
        if forbidden:
            denials.append({"event":event,"target":str(args[:2])[:250]})
            raise PermissionError("Pure doubles scope: "+event)
    # Cooperative Python audit guard; not a claim of native/OS sandbox isolation.
    sys.addaudithook(guard)
    start=time.monotonic()
    for name in ("audit_guard","result_acceptance","guard_doubles_suite"):
        path=sources[name]
        module=types.ModuleType(name);module.__file__=path
        sys.modules[name]=module
        exec(compile(cache[path],path,"exec"),module.__dict__)
    cls=sys.modules["guard_doubles_suite"].Doubles
    class RecordedResult(unittest.TextTestResult):
        def __init__(self,*a,**kw):super().__init__(*a,**kw);self.names=[]
        def startTest(self,test):
            self.names.append(test._testMethodName)
            super().startTest(test)
    suite=unittest.TestSuite(cls(name) for name in names)
    result=unittest.TextTestRunner(stream=sys.stderr,verbosity=2,resultclass=RecordedResult).run(suite)
    extra=len(result.skipped)+len(result.expectedFailures)+len(result.unexpectedSuccesses)
    passed=result.wasSuccessful() and result.testsRun==21 and result.names==names and not denials and extra==0
    payload={"request_id":REQUEST,"status":"PASS" if passed else "FAILED",
             "tests_run":result.testsRun,"test_names":result.names,"errors":len(result.errors),"failures":len(result.failures),
             "unexpected_or_skipped":extra,"guard_denials":denials,"suite_wall_s":time.monotonic()-start,
             "python":sys.version,"interpreter":sys.executable,"source_modules_from_pinned_bytes":True,
             "scientific_calls":0,"science_scope":"pure doubles only; dummy counters are not native execution","retry_allowed":False}
    print(json.dumps(payload,ensure_ascii=False),flush=True)
    return 0 if passed else 1
if __name__=="__main__":
    try:sys.exit(main())
    except Exception as exc:
        print(json.dumps({"request_id":REQUEST,"status":"FAILED","exception":type(exc).__name__,"message":str(exc)[:2000],"retry_allowed":False}),flush=True)
        sys.exit(1)
