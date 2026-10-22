"""Single authorized runtime import inventory; never calls scientific candidates."""
import os,sys,time,json,hashlib,stat,resource,importlib
from pathlib import Path
ENTRY=time.monotonic()
ROOT=Path('/opt/iald_ordem018_d72_d72f7125')
PLAN=json.loads((ROOT/'inspection'/'IMPORT_INSPECTION_PLAN.json').read_bytes())
assert os.getuid()==os.geteuid()==65534 and os.getgid()==65534
assert sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
assert resource.getrlimit(resource.RLIMIT_AS)==(8589934592,8589934592)
assert all(os.environ.get(k)=='1' for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'])
SITE='/opt/lal_env/lib/python3.12/site-packages'
SEARCH=['/usr/lib/python3.12','/usr/lib/python3.12/lib-dynload',SITE]
sys.path[:]=SEARCH
DAT={x['path'] for x in PLAN['six_authorized_tables']}
READS=set();ABSENT=set();SCANS=set();DLOPEN=[];EVENTS=[];DENIED=[]
SELFPROC='/proc/'+str(os.getpid())
PROC={SELFPROC+'/maps',SELFPROC+'/stat',SELFPROC+'/cmdline'}
def norm(p):return os.path.abspath(os.fsdecode(p))
def runtime_path(p):return p.startswith('/usr/lib/') or p.startswith('/opt/lal_env/lib/python3.12/site-packages/')
def admissible_read(p):
 return (p in DAT or p in PROC or p==str(ROOT/'inspection'/'runtime_import_collector.py') or
  runtime_path(p) and (p.endswith(('.py','.pyc','.pyi','.cfg','.ini','.toml')) or '.so' in os.path.basename(p) or '.dist-info/' in p or p.endswith(('gconv-modules.cache','LC_CTYPE'))))
def denied(event,target):
 DENIED.append({'event':event,'target':str(target)[:2000]})
 raise PermissionError('IMPORT_INSPECTION_SCOPE_DENIED:'+event)
def hook(event,args):
 if len(EVENTS)>50000:denied('audit_capacity','50000')
 if event=='open':
  p,mode,flags=args
  if isinstance(p,int):
   if p not in (0,1,2):denied(event,p)
   return
  p=norm(p)
  if flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):denied(event,p)
  if not admissible_read(p) and p not in ['/usr/lib/python312.zip','/usr/bin/python3.12']:
   denied(event,p)
  READS.add(p)
  if not os.path.lexists(p):ABSENT.add(p)
  EVENTS.append({'event':event,'path':p,'present_at_event':os.path.lexists(p)})
 elif event in ('os.listdir','os.scandir'):
  p=args[0]
  if isinstance(p,int):denied(event,p)
  p=norm(p)
  if not (p in SEARCH or runtime_path(p) or p==SELFPROC+'/task'):denied(event,p)
  SCANS.add(p)
  if not os.path.lexists(p):ABSENT.add(p)
  EVENTS.append({'event':event,'path':p,'present_at_event':os.path.lexists(p)})
 elif event=='ctypes.dlopen':DLOPEN.append(args[0])
 elif event=='import':
  EVENTS.append({'event':event,'name':str(args[0]),'origin':str(args[1]) if len(args)>1 else None})
 elif event.startswith(('socket.','subprocess.','os.exec','os.spawn','os.fork','os.posix_spawn')) or event in ('os.system','os.remove','os.rename','os.rmdir','os.mkdir','os.symlink','os.link','os.chmod','os.chown','os.truncate','os.utime','os.chdir','os.chroot'):
  denied(event,str(args)[:2000])
def modules():
 return {n:getattr(m,'__file__',None) for n,m in sys.modules.copy().items()}
def native_maps():
 paths=set()
 for line in Path(SELFPROC+'/maps').read_text().splitlines():
  row=line.split(None,5)
  if len(row)==6 and row[5].startswith('/'):
   assert not row[5].endswith(' (deleted)');paths.add(row[5])
 return sorted(paths)
def pin(p):
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  a=os.fstat(fd);assert stat.S_ISREG(a.st_mode)
  h=hashlib.sha256();n=0
  while True:
   b=os.read(fd,1048576)
   if not b:break
   h.update(b);n+=len(b)
  z=os.fstat(fd);assert (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns) and n==a.st_size
  return {'bytes':n,'sha256':h.hexdigest()}
 finally:os.close(fd)
baseline=modules();sys.addaudithook(hook)
try:
 # Only stdlib dependencies found by AST in d72. No candidate import is performed.
 for name in PLAN['stdlib_imports']:importlib.import_module(name)
 modules_before_scientific=modules()
 for name in ('numpy','camb'):importlib.import_module(name)
 import importlib.metadata
 versions={n:importlib.metadata.version(n) for n in ('numpy','scipy','camb')}
 assert versions==PLAN['expected_package_versions']
 loaded=modules();maps=native_maps()
 threads=len(os.listdir(SELFPROC+'/task'))
 assert threads==1
 scientific_prefixes=[str(ROOT/'package')]
 assert not any(p and any(p.startswith(x) for x in scientific_prefixes) for p in loaded.values())
 assert 'sitecustomize' not in sys.modules and 'site' not in sys.modules
 table_pins={p:pin(p) for p in sorted(DAT)}
 for item in PLAN['six_authorized_tables']:assert table_pins[item['path']]==item['expected_pin']
 wanted={p for p in READS if p not in PROC and os.path.isfile(p)}
 wanted.update(p for p in loaded.values() if p and os.path.isabs(p))
 wanted.update(maps);wanted.update(DAT)
 wanted.discard(str(ROOT/'inspection'/'runtime_import_collector.py'))
 files={p:pin(p) for p in sorted(wanted)}
 assert not DENIED
 usage=resource.getrusage(resource.RUSAGE_SELF)
 result={'schema':'F9_ACTUAL_AUTHORIZED_IMPORT_OBSERVATION_V1','status':'IMPORT_ONLY_COMPLETED','uid':os.getuid(),'gid':os.getgid(),'pid':os.getpid(),'ppid':os.getppid(),'executable':str(Path(sys.executable).resolve()),'python_version':sys.version,'python_search_path':sys.path,'no_site':sys.flags.no_site,'isolated':sys.flags.isolated,'dont_write_bytecode':sys.dont_write_bytecode,'packages':versions,'baseline_modules':baseline,'modules_before_scientific':modules_before_scientific,'loaded_modules':loaded,'loaded_object_modules':{n:{'name':sys.modules[n].__name__,'file':sys.modules[n].__file__,'version':getattr(sys.modules[n],'__version__',None),'object_id_process_local':id(sys.modules[n])} for n in ('numpy','camb')},'files':files,'absent_paths':sorted(p for p in ABSENT if not os.path.lexists(p)),'scan_directories':sorted(p for p in SCANS if os.path.isdir(p) and p!=SELFPROC+'/task'),'native_map_pins':{p:files[p] for p in maps},'ctypes_dlopen_events':DLOPEN,'six_table_pins':table_pins,'audit_events':EVENTS,'denied_events':DENIED,'threads_sample_after_import':threads,'elapsed_from_collector_entry_seconds':time.monotonic()-ENTRY,'resource_usage':{'user_cpu_seconds':usage.ru_utime,'system_cpu_seconds':usage.ru_stime,'max_rss_kib_linux':usage.ru_maxrss},'candidate_imports':0,'explicit_science_calls':0,'native_file_operations':None,'native_network_operations':None,'transient_native_threads_between_samples':None,'evidence_scope':'COOPERATIVE_PYTHON_AUDIT_AND_ACTUAL_IMPORTED_MODULES_AND_SAMPLED_NATIVE_MAPS_NOT_SYSCALL_ISOLATION'}
 print(json.dumps(result,ensure_ascii=False,sort_keys=True))
except BaseException as exc:
 print(json.dumps({'schema':'F9_IMPORT_INSPECTION_FAILURE_V1','status':'FAILED_NO_AUTOMATIC_RETRY','exception_type':type(exc).__name__,'message':str(exc),'elapsed_seconds':time.monotonic()-ENTRY,'denied_events':DENIED,'audit_events':EVENTS,'loaded_modules_at_failure':modules(),'science_calls':0,'native_file_operations':None,'native_network_operations':None},ensure_ascii=False))
 raise
