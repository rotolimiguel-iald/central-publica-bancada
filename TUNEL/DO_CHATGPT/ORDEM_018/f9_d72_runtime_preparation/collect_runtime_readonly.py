"""Read-only current runtime metadata collector, never a science runner."""
import os, sys, json, hashlib, stat, time, datetime, resource
from pathlib import Path
if os.geteuid() == 0:
    raise SystemExit('NONROOT_INSPECTOR_REQUIRED')
START = datetime.datetime.now(datetime.timezone.utc).isoformat()
BASE = Path('/mnt/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_integrated_bootstrap_preparation')
HIST = BASE / 'RUNTIME_INVENTORY.json'
raw = HIST.read_bytes()
history = json.loads(raw)
FILES = {}; ERRORS = []
def info(path):
    try:
        s = os.lstat(path)
        return {'path': str(path), 'mode': oct(stat.S_IMODE(s.st_mode)), 'uid':s.st_uid,'gid':s.st_gid,
                'bytes':s.st_size,'mtime_ns':s.st_mtime_ns,'device':s.st_dev,'inode':s.st_ino,
                'type':'symlink' if stat.S_ISLNK(s.st_mode) else 'directory' if stat.S_ISDIR(s.st_mode) else 'file' if stat.S_ISREG(s.st_mode) else 'other',
                'realpath':os.path.realpath(path),'readable':os.access(path,os.R_OK),'writable':os.access(path,os.W_OK),'searchable':os.access(path,os.X_OK)}
    except OSError as exc:
        return {'path':str(path),'error':type(exc).__name__,'errno':exc.errno}
def pin(path):
    target = os.path.realpath(path)
    if target in FILES:return FILES[target]
    fd = os.open(target,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        s = os.fstat(fd)
        if not stat.S_ISREG(s.st_mode):raise ValueError('NOT_REGULAR')
        h = hashlib.sha256();n = 0
        while True:
            b = os.read(fd,1048576)
            if not b:break
            h.update(b);n+=len(b)
        a=os.fstat(fd)
        if (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)!=(a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns) or n!=s.st_size:
            raise ValueError('CHANGED_DURING_READ')
        FILES[target]={'bytes':n,'sha256':h.hexdigest()}
        return FILES[target]
    finally:os.close(fd)
def allowed_code(path):
    p=Path(path)
    return (p.suffix in ('.py','.pyc','.pyi','.pxd','.pyx','.h','.c','.cpp','.f','.f90','.f95','.inc','.pyf','.a','.o')
            or '.so' in p.name or '.dist-info/' in path or path in ('/usr/bin/python3.12','/etc/ld.so.cache','/opt/lal_env/pyvenv.cfg')
            or p.name.startswith('_sysconfigdata'))
items=[]
for old in history['pins']:
    path=old['path'];row=info(path)
    row['scope']='CURRENT_BYTES_CODE_NATIVE_METADATA' if allowed_code(path) else 'METADATA_ONLY_NO_DATA_CONTENT_READ'
    if allowed_code(path) and 'error' not in row:
        try:
            row['pin']=pin(path);row['historical_match']=row['pin']=={k:old[k] for k in ('bytes','sha256')}
        except (OSError,ValueError) as exc:
            row['read_error']=str(exc);ERRORS.append({'path':path,'error':str(exc)})
    items.append(row)
site=Path(history['site_packages'])
versions=[]
for pkg in ('numpy','scipy','camb','bilby','charset_normalizer'):
    dirs=sorted(site.glob(pkg+'-*.dist-info'))
    rows=[]
    for directory in dirs:
        meta=directory/'METADATA'
        try:
            body=meta.read_text(encoding='utf-8');fields={}
            for line in body.splitlines():
                if line.startswith(('Name: ','Version: ')):
                    key,value=line.split(': ',1);fields[key]=value
            rows.append({'directory':str(directory),'metadata':fields,'pin':pin(meta)})
        except OSError as exc:rows.append({'directory':str(directory),'error':str(exc)})
    versions.append({'package':pkg,'installed_metadata':rows,'module_imported':False})
paths=['/','/tmp','/var','/var/tmp','/home','/opt','/opt/lal_env','/opt/lal_env/bin','/opt/lal_env/bin/python','/usr/bin/python3.12',str(site),'/mnt','/mnt/c',str(BASE.parent),str(BASE),'/nonexistent','/usr/lib/python3.12','/usr/lib/python3.12/lib-dynload','/usr/local/lib/python3.12/dist-packages','/usr/lib/python3/dist-packages']
paths.extend(history['roots'])
paths.extend(history['exact_absent_probe_paths'])
paths.extend(['/lib64/ld-linux-x86-64.so.2','/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2'])
path_records=[info(p) for p in sorted(set(paths))]
for path in ['/opt/lal_env/bin/python','/usr/bin/python3.12','/lib64/ld-linux-x86-64.so.2','/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2','/opt/lal_env/pyvenv.cfg']:
    try:pin(path)
    except (OSError,ValueError) as exc:ERRORS.append({'path':path,'error':str(exc)})
mem={}
for line in Path('/proc/meminfo').read_text().splitlines():
    key,value=line.split(':',1)
    if key in ('MemTotal','MemFree','MemAvailable','SwapTotal','SwapFree','CommitLimit','Committed_AS'):
        mem[key+'_bytes']=int(value.strip().split()[0])*1024
fs=[]
for path in ['/','/opt/lal_env','/home','/tmp','/mnt/c',str(BASE)]:
    try:
        s=os.statvfs(path);fs.append({'path':path,'block_size':s.f_frsize,'total_bytes':s.f_blocks*s.f_frsize,'available_unprivileged_bytes':s.f_bavail*s.f_frsize,'free_bytes':s.f_bfree*s.f_frsize,'total_inodes':s.f_files,'free_inodes':s.f_favail,'flags':s.f_flag})
    except OSError as exc:fs.append({'path':path,'error':str(exc)})
cgroup={}
for path in ['/proc/self/cgroup','/sys/fs/cgroup/memory.max','/sys/fs/cgroup/memory.current','/sys/fs/cgroup/memory.swap.max','/sys/fs/cgroup/cpu.max','/sys/fs/cgroup/pids.max']:
    try:cgroup[path]=Path(path).read_text().strip()
    except OSError as exc:cgroup[path]={'error':type(exc).__name__,'errno':exc.errno}
maps=[]
for line in Path('/proc/self/maps').read_text().splitlines():
    fields=line.split(None,5)
    if len(fields)==6 and fields[-1].startswith('/'):
        path=fields[-1]
        if path not in maps:maps.append(path)
map_pins={}
for path in sorted(maps):
    try:map_pins[path]=pin(path)
    except (OSError,ValueError) as exc:ERRORS.append({'path':path,'error':str(exc)})
modules=[]
for name,m in sorted(sys.modules.copy().items()):
    file=getattr(m,'__file__',None)
    if file and os.path.isabs(file):
        try:modules.append({'name':name,'path':file,'pin':pin(file)})
        except (OSError,ValueError) as exc:ERRORS.append({'path':file,'error':str(exc)})
if any(name in sys.modules for name in ('numpy','scipy','camb','bilby')):
    raise SystemExit('SCIENTIFIC_IMPORT_PROHIBITED')
existing_dirs=[]
for root in history['roots']:
    try:
        for current,dirs,names in os.walk(root,followlinks=False):
            existing_dirs.append(current)
            dirs[:]=[d for d in dirs if not os.path.islink(os.path.join(current,d))]
    except OSError as exc:ERRORS.append({'path':root,'error':str(exc)})
result={'schema':'F9_D72_READ_ONLY_RUNTIME_OBSERVATIONS_V1','status':'REAL_READ_ONLY_INSPECTION_NOT_QUALIFICATION',
 'start_utc':START,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'historical_routes_source':{'path':str(HIST),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},
 'identity':{'uid':os.getuid(),'euid':os.geteuid(),'gid':os.getgid(),'groups':os.getgroups(),'pid':os.getpid(),'uname':list(os.uname()),'cwd':os.getcwd()},
 'interpreter':{'invoked_executable':sys.executable,'canonical_executable':os.path.realpath(sys.executable),'python_version':sys.version,'prefix':sys.prefix,'base_prefix':sys.base_prefix,'python_search_path_startup':sys.path,'isolated':sys.flags.isolated,'no_site':sys.flags.no_site,'dont_write_bytecode':sys.dont_write_bytecode},
 'files':FILES,'historical_routes':items,'path_metadata':path_records,'package_metadata':versions,
 'memory':mem,'filesystems':fs,'cgroup':cgroup,'rlimits':{name:list(resource.getrlimit(getattr(resource,name))) for name in ('RLIMIT_AS','RLIMIT_CPU','RLIMIT_FSIZE','RLIMIT_NOFILE','RLIMIT_NPROC')},
 'current_maps':{'scope':'STDLIB_INSPECTOR_PROCESS_ONLY_NOT_SCIENTIFIC_RUNTIME','pins':map_pins},
 'loaded_modules_inspector_only':modules,'existing_scan_directories_static_candidates':sorted(set(existing_dirs)),
 'scientific_native_map_pins':None,'scientific_import_trace':None,'scientific_loaded_objects':None,'scientific_transient_threads':None,'solver_calls':0,'scientific_candidate_imports':0,'linux_file_writes_by_collector':0,'errors':ERRORS}
print(json.dumps(result,ensure_ascii=False,indent=2))
