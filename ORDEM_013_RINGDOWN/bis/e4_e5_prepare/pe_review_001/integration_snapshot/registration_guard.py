"""Read-only authorization of a whole code tree and its E2 tunnel witness."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,re,os,sys,math,stat,importlib.util

BASE=Path(__file__).resolve().parents[2]
ROOT=BASE.parent
CODE=Path(__file__).resolve().parent

def strict_json(payload):
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('Duplicate JSON key: '+key)
            result[key]=value
        return result
    def invalid(value):raise ValueError('Nonfinite JSON constant: '+value)
    return json.loads(payload,object_pairs_hook=pairs,parse_constant=invalid)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def contained(name,root=ROOT):
    p=(root/name).resolve()
    if not p.is_relative_to(root.resolve()):raise ValueError('Path outside registered root')
    return p

def checked_registration():
    path=BASE/'RINGDOWN_5SIGMA_V1.json'
    digest=sha(path);reg=strict_json(path.read_text(encoding='utf-8-sig'))
    if reg['status']!='REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST':raise ValueError('Not an active E2 registration')
    note=contained(reg['witness_relative_to_Chatgpt'])
    text=note.read_text(encoding='utf-8')
    matches=re.findall(r'^registro_sha256: ([0-9a-f]{64})$',text,re.M)
    if matches!=[digest]:raise ValueError('Tunnel witness hash differs or is ambiguous')
    check_witness(note,digest,reg['registered_utc'])
    own={str(p.relative_to(CODE)).replace('\\','/'):sha(p) for p in CODE.rglob('*.py')}
    if own!=reg['own_code_tree_sha256']:raise ValueError('Own code tree differs from complete registered tree')
    for entry in reg.get('extra_code_roots',[]):
        root=contained(entry['relative_to_Chatgpt'])
        actual={p.relative_to(root).as_posix():sha(p) for p in root.rglob('*.py')}
        if actual!=entry['files_sha256']:raise ValueError('Extra code root changed')
    for name,wanted in reg['input_pins_relative_to_Chatgpt'].items():
        if sha(contained(name))!=wanted:raise ValueError('Registered input changed: '+name)
    runtime=contained(reg['runtime_manifest_relative_to_Chatgpt'])
    if sha(runtime)!=reg['runtime_manifest_sha256']:raise ValueError('Runtime manifest changed')
    environment=strict_json(runtime.read_bytes())
    if os.name!='posix' or Path(sys.prefix).resolve()!=Path('/opt/lal_env') or Path(sys.executable).resolve()!=Path(environment['python_executable']).resolve():
        raise RuntimeError('Active interpreter must be pinned /opt/lal_env')
    for name,wanted in environment['files'].items():
        p=Path(name).resolve()
        if not p.is_relative_to('/opt/lal_env') or sha(p)!=wanted['sha256']:raise ValueError('Scientific runtime code changed')
    if sha(Path(environment['python_executable']))!=environment['python_executable_sha256']:raise ValueError('Python interpreter changed')
    pins={str(Path(k).resolve()):v['sha256'] for k,v in environment['files'].items()}
    for name in ('numpy','scipy','bilby','dynesty','lal','lalsimulation','gwpy','h5py'):
        module=sys.modules.get(name)
        origin=getattr(module,'__file__',None) if module else None
        if origin is None:
            spec=importlib.util.find_spec(name);origin=spec.origin if spec else None
        if not origin:raise ValueError('Missing runtime origin '+name)
        p=Path(origin).resolve()
        if not p.is_relative_to('/opt/lal_env') or pins.get(str(p))!=sha(p):raise ValueError('Unpinned active module '+name)
    time_guard(reg)
    return reg,digest

def time_guard(reg):
    budget=contained(reg['budget_relative_to_Chatgpt'])
    if sha(budget)!=reg['budget_sha256']:raise ValueError('Budget changed')
    b=strict_json(budget.read_bytes())
    deadline=datetime.fromisoformat(b['hard_deadline_utc'])
    if deadline.tzinfo is None or datetime.now(timezone.utc)>=deadline:raise TimeoutError('Part B hard deadline reached')
    return deadline

def authorize_event(reg,event,mode):
    if mode not in ('calibration','blind_test'):raise ValueError('Unknown analysis mode')
    known=set(reg['calibration_event_ids'])
    if mode=='calibration' and event not in known:raise ValueError('New event cannot enter calibration path')
    if mode=='blind_test':
        if event in known:raise ValueError('Published calibration event cannot enter blind test')
        entry=reg['test_candidates'].get(event)
        if entry is None:raise ValueError('Event has no registered pre-analysis candidate entry')
        if entry['eligible'] is not True:raise ValueError('Pre-analysis eligibility unpaid or failed')
        if entry['published_deformation_at_registration'] is not False:raise ValueError('Blindness census not established')
        if not entry.get('publication_census_scope'):raise ValueError('Scoped publication census required')
    return True

def output_path(name):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,150}',name):raise ValueError('Unsafe output name')
    return BASE/'cache'/name

def utc(value):
    value=datetime.fromisoformat(value.replace('Z','+00:00'))
    if value.tzinfo is None:raise ValueError('Timezone required')
    return value.astimezone(timezone.utc)

def positive(value,name):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value<=0:
        raise ValueError('Positive finite value required: '+name)
    return value

def integer(value,name,minimum=1):
    if type(value) is not int or value<minimum:raise ValueError('Invalid integer: '+name)
    return value

def publish_new(path,value):
    raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode();temp=path.with_name(path.name+'.pending')
    with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if temp.stat().st_size!=len(raw):raise OSError('Incomplete temporary retained')
    os.link(temp,path);temp.unlink()

def check_witness(path,digest,issued,label='registro_sha256'):
    path=contained(path)
    if not path.is_relative_to(ROOT/'TUNEL'/'DO_CHATGPT'):raise ValueError('Witness must be in DO_CHATGPT')
    text=path.read_text(encoding='utf-8-sig')
    hashes=re.findall(r'^'+label+r': ([0-9a-f]{64})\s*$',text,re.M)
    dates=re.findall(r'^registered_utc: (\S+)\s*$',text,re.M)
    if hashes!=[digest] or len(dates)!=1:raise ValueError('Ambiguous witness')
    written=utc(dates[0]);now=datetime.now(timezone.utc);mtime=path.stat().st_mtime
    if not utc(issued)<=written<=now or mtime<written.timestamp()-2 or mtime>now.timestamp()+2:
        raise ValueError('Witness chronology invalid')
    return sha(path)

def load_jobs(reg,digest):
    jobs=dict(reg['pe_jobs']);policy=reg.get('allocation_policy')
    if policy is None:return jobs
    path=contained(policy['relative_to_Chatgpt'])
    if not path.exists():return jobs
    allocation=strict_json(path.read_bytes())
    if allocation['parent_registration_sha256']!=digest:raise ValueError('Allocation parent differs')
    check_witness(allocation['witness_relative_to_Chatgpt'],sha(path),allocation['registered_utc'],'allocation_sha256')
    if utc(allocation['registered_utc'])<utc(reg['registered_utc']):raise ValueError('Allocation predates E2')
    config=contained(allocation['jobs_relative_to_Chatgpt'])
    if sha(config)!=allocation['jobs_sha256']:raise ValueError('Allocation config changed')
    extra=strict_json(config.read_bytes())
    if extra['parent_registration_sha256']!=digest or extra['schema_version']!='E2_PE_JOBS_V2':raise ValueError('Wrong jobs schema')
    for name,job in extra['jobs'].items():
        if name in jobs:raise ValueError('Allocation cannot replace registered job')
        if positive(job['wall_budget_seconds'],'job wall')>positive(policy['max_job_wall_seconds'],'allocation cap'):
            raise ValueError('Allocation job exceeds cap')
        if job['mode']=='blind_test':
            review=job['publication_metadata_review'];evidence=contained(review['relative_to_Chatgpt'])
            if review['review_passed'] is not True or not review['scope'] or sha(evidence)!=review['sha256'] or utc(review['reviewed_utc'])<utc(reg['registered_utc']):
                raise ValueError('Publication review unpaid/pin differs')
        jobs[name]=job
    return jobs

def load_authorized_configuration(reg,digest):
    """Derived view only; checked_registration always checks the original map first."""
    policy=reg.get('allocation_policy');allocation_path=contained(policy['relative_to_Chatgpt']) if policy else None
    initial=sha(allocation_path) if allocation_path and allocation_path.exists() else None
    view=dict(reg);view['pe_jobs']=load_jobs(reg,digest);view['downloads']=dict(reg.get('downloads',{}))
    if initial is not None:
        allocation=strict_json(allocation_path.read_bytes())
        config=contained(allocation['jobs_relative_to_Chatgpt'])
        if sha(config)!=allocation['jobs_sha256']:raise ValueError('Dynamic config changed')
        extra=strict_json(config.read_bytes())
        for name,item in extra.get('downloads',{}).items():
            if name in view['downloads']:raise ValueError('Dynamic download cannot replace original')
            if not item.get('license_receipt_relative_to_Chatgpt') or not item.get('license_receipt_sha256'):
                raise ValueError('Per-file license receipt required')
            if sha(contained(item['license_receipt_relative_to_Chatgpt']))!=item['license_receipt_sha256']:
                raise ValueError('License receipt changed')
            view['downloads'][name]=item
        if sha(allocation_path)!=initial:raise ValueError('Allocation changed during read')
    view['_parent_registration_sha256']=digest
    view['_allocation_sha256']=initial
    return view

def validate_launch(context_path,reg,digest,job,cfg):
    path=contained(context_path);context=strict_json(path.read_bytes());out=output_path(cfg['output_directory_name'])
    if path!=out/'LAUNCH_CONTEXT.json' or context['registration_sha256']!=digest or context['job']!=job:
        raise ValueError('Launch identity differs')
    if context['config_sha256']!=hashlib.sha256(json.dumps(cfg,sort_keys=True,allow_nan=False).encode()).hexdigest():
        raise ValueError('Config differs from controller context')
    if os.name!='posix' or context['controller_pid']!=os.getppid() or os.getsid(0)!=os.getpid() or os.getpgrp()!=os.getpid():
        raise ValueError('Runner must be new group leader under controller')
    pid=context['controller_pid'];ticks=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()[19]
    if ticks!=context['controller_start_ticks']:raise ValueError('Controller PID reused')
    if utc(context['stop_utc'])>time_guard(reg) or datetime.now(timezone.utc)>=utc(context['stop_utc']):
        raise TimeoutError('Launch deadline invalid')
    expected=(out/'PRIVATE.log').stat()
    for fd in (1,2):
        actual=os.fstat(fd)
        if os.isatty(fd) or not stat.S_ISREG(actual.st_mode) or (actual.st_dev,actual.st_ino)!=(expected.st_dev,expected.st_ino):
            raise ValueError('Private regular-file stdout/stderr required')
    if cfg['privacy_mode']!='procedural_same_host':raise ValueError('Unknown privacy contract')
    publish_new(out/'LAUNCH_CLAIM.json',dict(pid=os.getpid(),pgid=os.getpgrp(),registration_sha256=digest,
        context_sha256=sha(path),claimed_utc=datetime.now(timezone.utc).isoformat()))
    return context,out
