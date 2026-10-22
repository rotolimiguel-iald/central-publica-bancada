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
    check_activation(reg,digest,note)
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
    for name in ('numpy','scipy','bilby','dynesty','lal','lalsimulation','gwpy','h5py','astropy','pandas'):
        module=sys.modules.get(name)
        origin=getattr(module,'__file__',None) if module else None
        if origin is None:
            spec=importlib.util.find_spec(name);origin=spec.origin if spec else None
        if not origin:raise ValueError('Missing runtime origin '+name)
        p=Path(origin).resolve()
        if not p.is_relative_to('/opt/lal_env') or pins.get(str(p))!=sha(p):raise ValueError('Unpinned active module '+name)
    time_guard(reg)
    return reg,digest


def check_activation(reg,digest,note):
    """Final immutable marker closes partial sealer publication; no seed reads."""
    activation=reg['activation']
    expected_paths={
      'receipt_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/bis/E2_REGISTRATION_RECEIPT.json',
      'review_application_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/bis/E2_REVIEW_APPLICATION_V2.json',
      'sealer_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/refeito/seal_e2_013bis.py'}
    if any(activation[k]!=v for k,v in expected_paths.items()):raise ValueError('Activation artifact paths differ')
    receipt=strict_json(contained(activation['receipt_relative_to_Chatgpt']).read_bytes())
    app_path=contained(activation['review_application_relative_to_Chatgpt'])
    sealer_path=contained(activation['sealer_relative_to_Chatgpt'])
    if sha(app_path)!=activation['review_application_sha256'] or sha(sealer_path)!=activation['sealer_sha256']:
        raise ValueError('Activation application/sealer pin changed')
    if receipt['status']!='E2_ACTIVATION_COMPLETE' or receipt['registration_sha256']!=digest or receipt['witness_sha256']!=sha(note):
        raise ValueError('Activation incomplete or registration/witness differs')
    if receipt['review_application_sha256']!=activation['review_application_sha256'] or receipt['sealer_sha256']!=activation['sealer_sha256']:
        raise ValueError('Activation receipt pins differ')
    if not utc(reg['registered_utc'])<=utc(receipt['finished_utc'])<=datetime.now(timezone.utc):
        raise ValueError('Activation chronology invalid')
    application=strict_json(app_path.read_bytes())
    candidate=reg['registration_provenance']['candidate_sha256']
    if not isinstance(candidate,str) or not re.fullmatch('[0-9a-f]{64}',candidate):raise ValueError('Candidate pin required')
    if application['status']!='APPLY_EXISTING_GO_TO_REVIEWED_CANDIDATE' or application['candidate_sha256']!=candidate:
        raise ValueError('Reviewed GO application differs from registered candidate')
    if application['sealer_sha256']!=activation['sealer_sha256']:
        raise ValueError('Reviewed application sealer differs')
    if utc(application['created_utc'])>utc(reg['registered_utc']):
        raise ValueError('Review application postdates registration')
    reviews=application['reviews']
    if not isinstance(reviews,dict) or set(reviews)!={'PE','MAIN','E7','ACTIVATION'}:raise ValueError('Four required review roles')
    for role,review in reviews.items():
        files=review['files']
        if review['status']!='BLOCKERS_CLOSED' or review['blocking_findings']!=[] or not isinstance(files,dict) or not files:
            raise ValueError('Review blockers not closed: '+role)
        for relative,pin in files.items():
            if not isinstance(relative,str) or Path(relative).is_absolute() or '..' in Path(relative).parts:
                raise ValueError('Review path must be relative to B')
            if not isinstance(pin,str) or not re.fullmatch('[0-9a-f]{64}',pin) or sha(contained(relative,root=BASE))!=pin:
                raise ValueError('Reviewed file pin changed: '+role)
    return True

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

def validate_job_reviews(reg,job):
    """Metadata-only gates, independent of any fitted posterior width."""
    if job['mode']!='blind_test':return
    authorize_event(reg,job['event'],job['mode'])
    review=job['publication_metadata_review']
    evidence=contained(review['relative_to_Chatgpt'])
    reviewed=utc(review['reviewed_utc'])
    if review['review_passed'] is not True or not str(review['scope']).strip() or sha(evidence)!=review['sha256'] or not utc(reg['registered_utc'])<=reviewed<=datetime.now(timezone.utc):
        raise ValueError('Publication review unpaid/pin differs')
    entry=reg['test_candidates'][job['event']]
    if type(entry['data_quality_hold']) is not bool:raise ValueError('Explicit data quality hold boolean required')
    if entry['data_quality_hold']:
        review=job['data_quality_resolution']
        evidence=contained(review['relative_to_Chatgpt'])
        reviewed=utc(review['reviewed_utc'])
        if review['review_passed'] is not True or not isinstance(review['method'],str) or not review['method'].strip() or sha(evidence)!=review['sha256'] or not utc(reg['registered_utc'])<=reviewed<=datetime.now(timezone.utc):
            raise ValueError('Data quality hold unresolved or evidence changed')


def load_jobs(reg,digest):
    jobs=dict(reg['pe_jobs']);policy=reg.get('allocation_policy')
    for job in jobs.values():validate_job_reviews(reg,job)
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
        validate_job_reviews(reg,job)
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


V1_PIN = 'e1be6b0409720c6883af5281458922fb03c5329bc0b08df7efe129d65e487416'
V1_WITNESS_PIN = 'e95787fd52852c090b18d760ba5f58cb422087b136686414571023a19782403c'

# V1.1 statistical and chronology contract. No caller may bypass the later runtime gate.
STATISTICAL_FIELDS=('observables','statistics','systematic_gate','nulls','route_IV',
    'conventions','planning_targets','permitted_verdicts','forbidden_verdicts','stopping','calibration_event_ids')


def statistical_subobject(reg):
    obj={key:reg[key] for key in STATISTICAL_FIELDS}
    obj['blinding']={key:reg['blinding'][key] for key in ('seed_commitment_sha256','offset_half_range')}
    return obj


def statistical_digest(reg):
    raw=json.dumps(statistical_subobject(reg),sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def verify_statistical_identity(original,candidate):
    wanted=statistical_digest(original)
    if statistical_subobject(candidate)!=statistical_subobject(original) or statistical_digest(candidate)!=wanted:
        raise ValueError('Frozen V1 statistical subobject changed')
    if candidate.get('statistical_subobject_sha256')!=wanted:raise ValueError('Statistical commitment differs')
    old_cells=original['nulls']['cells'];new_cells=candidate['nulls_v1_1']['cells']
    if not isinstance(old_cells,dict) or not isinstance(new_cells,dict):raise ValueError('Null cells require id-keyed mapping')
    old_ids=list(old_cells);new_ids=list(new_cells)
    if not all(isinstance(k,str) and k for k in new_ids):raise ValueError('Invalid null cell id')
    if len(new_ids)!=len(set(new_ids)) or set(old_ids)&set(new_ids):raise ValueError('Old/repeated null cell id forbidden')
    return wanted


def numbered_chain(root,pattern,prefix,suffix='.json'):
    entries={}
    for p in root.glob(pattern):
        match=re.fullmatch(re.escape(prefix)+r'([1-9][0-9]*)'+re.escape(suffix),p.name)
        if match is None:raise ValueError('Malformed chain filename: '+p.name)
        n=int(match[1])
        if n in entries:raise ValueError('Repeated chain ordinal')
        if p.is_symlink() or p.resolve().parent!=root.resolve():raise ValueError('Redirected chain member')
        entries[n]=p
    if sorted(entries)!=list(range(1,len(entries)+1)):raise ValueError('Nonconsecutive amendment/allocation chain')
    return [entries[n] for n in sorted(entries)]


def load_registration_chain_v1_1():
    original_path=BASE/'RINGDOWN_5SIGMA_V1.json'
    original=strict_json(original_path.read_bytes());parent=sha(original_path)
    if parent!=V1_PIN:raise ValueError('Historical V1 pin changed')
    v1_note=contained(original['witness_relative_to_Chatgpt'])
    v1_witness=check_witness(v1_note,parent,original['registered_utc'])
    if v1_witness!=V1_WITNESS_PIN:raise ValueError('Historical V1 witness pin changed')
    paths=[BASE/'RINGDOWN_5SIGMA_V1_1.json']+numbered_chain(BASE,'RINGDOWN_5SIGMA_V1_1_*.json','RINGDOWN_5SIGMA_V1_1_')
    previous=None;previous_time=utc(original['registered_utc']);root_time=None
    for index,path in enumerate(paths):
        if path.is_symlink():raise ValueError('Redirected amendment')
        reg=strict_json(path.read_bytes());digest=sha(path)
        if reg['parent_registration_sha256']!=parent:raise ValueError('Amendment parent mismatch')
        if reg['v1_witness_sha256']!=v1_witness:raise ValueError('V1 witness changed')
        verify_statistical_identity(original,reg)
        issued=utc(reg['registered_utc'])
        if issued<previous_time:raise ValueError('Amendment chronology reversed')
        expected='ENTREGA_015_E2_REGISTRO_V1_1'+('' if index==0 else '_'+str(index))+'.md'
        note=contained(reg['witness_relative_to_Chatgpt'])
        if note!=ROOT/'TUNEL/DO_CHATGPT'/expected:raise ValueError('Wrong amendment witness path')
        check_witness(note,digest,reg['registered_utc'])
        dates=re.findall(r'^registered_utc: (\S+)\s*$',note.read_text('utf-8-sig'),re.M)
        witnessed=utc(dates[0])
        if root_time is None:root_time=witnessed
        if previous is not None:
            if any(name not in reg['pe_jobs'] or reg['pe_jobs'][name]!=job for name,job in previous['pe_jobs'].items()):
                raise ValueError('Existing job removed or replaced by amendment')
        if set(reg['pe_jobs'])&set(original['pe_jobs']):raise ValueError('V1 job cannot be relaunched in V1.1')
        # Promotion metadata itself is not authorization: evidence and chronology must match.
        promotions={}
        for change in reg.get('test_candidates_amendments',[]):
            if change.get('promotion') is not True:continue
            event=change['event']
            if event in promotions:raise ValueError('Duplicate promotion')
            reviewed=utc(change['census_reviewed_utc'])
            if not root_time<=reviewed<=datetime.now(timezone.utc):raise ValueError('Census predates V1.1 or is future')
            if sha(contained(change['evidence_relative_to_Chatgpt']))!=change['evidence_sha256']:raise ValueError('Promotion evidence mismatch')
            if reg['test_candidates'][event]['eligible'] is not True:raise ValueError('Promotion/eligibility disagreement')
            promotions[event]=change
        antecedent=original if previous is None else previous
        for event,entry in reg['test_candidates'].items():
            old=antecedent['test_candidates'].get(event,{})
            if entry.get('eligible') is True and old.get('eligible') is not True and event not in promotions:
                raise ValueError('Eligibility changed without witnessed promotion')
        previous=reg;previous_time=witnessed;parent=digest
    return reg,digest,note
