"""Separate calibration custody, never an E2 blind authorization."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,os,sys,importlib.util

HERE=Path(__file__).resolve().parent
B=HERE.parents[1]
ROOT=B.parent


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def strict_json(data):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('Duplicate JSON key')
            out[k]=v
        return out
    def invalid(x):raise ValueError('Nonfinite JSON constant')
    return json.loads(data,object_pairs_hook=pairs,parse_constant=invalid)


def utc(value):
    t=datetime.fromisoformat(value.replace('Z','+00:00'))
    if t.tzinfo is None:raise ValueError('Timezone required')
    return t.astimezone(timezone.utc)


def contained(root,name):
    p=(Path(root)/name).resolve()
    if not p.is_relative_to(Path(root).resolve()):raise ValueError('Path outside calibration workspace')
    return p


def publish_new(path,value):
    raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    temp=path.with_name(path.name+'.pending')
    with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if temp.stat().st_size!=len(raw):raise OSError('Incomplete output')
    os.link(temp,path);temp.unlink()


def verify(authorization_path):
    authpath=contained(ROOT,authorization_path)
    auth=strict_json(authpath.read_bytes());manifest_path=HERE/'MANIFEST.json'
    if auth['status']!='CALIBRATION_ONLY_REVIEWED' or auth['manifest_sha256']!=sha(manifest_path):
        raise ValueError('Own reviewed calibration manifest required')
    now=datetime.now(timezone.utc)
    if not utc(auth['approved_utc'])<=now<utc(auth['valid_until_utc']):raise ValueError('Authorization expired/not yet valid')
    if not auth.get('reviewer'):raise ValueError('Named independent reviewer required')
    manifest=strict_json(manifest_path.read_bytes())
    if manifest['status']!='PREPARED_NOT_EXECUTED_CALIBRATION_ONLY':raise ValueError('Wrong manifest scope')
    own={p.name:sha(p) for p in HERE.glob('*.py')}
    if own!=manifest['code_sha256']:raise ValueError('Calibration code tree changed')
    for name,pin in manifest['source_and_config_pins'].items():
        if sha(contained(ROOT,name))!=pin:raise ValueError('Pinned calibration source/config changed: '+name)
    cfg=strict_json((HERE/'CONFIG.json').read_bytes())
    if cfg['event']!='GW250114_082203' or cfg['mode']!='calibration' or cfg['wall_envelope_seconds']!=7200:
        raise ValueError('Not the calibration-only 2h design')
    if os.name!='posix' or Path(sys.prefix).resolve()!=Path('/opt/lal_env'):raise RuntimeError('Pinned WSL /opt/lal_env required')
    runtime=strict_json(contained(ROOT,cfg['runtime_manifest_path']).read_bytes())
    if Path(sys.executable).resolve()!=Path(runtime['python_executable']).resolve() or sha(sys.executable)!=runtime['python_executable_sha256']:
        raise ValueError('Interpreter changed')
    for name,entry in runtime['files'].items():
        p=Path(name).resolve()
        if not p.is_relative_to('/opt/lal_env') or sha(p)!=entry['sha256']:raise ValueError('Runtime changed')
    for name in ('numpy','scipy','bilby','dynesty','lal','h5py','astropy','pandas'):
        module=sys.modules.get(name)
        origin=getattr(module,'__file__',None) if module else None
        if origin is None:
            spec=importlib.util.find_spec(name);origin=spec.origin if spec else None
        if not origin:raise ValueError('Runtime origin missing')
        path=Path(origin).resolve()
        if not path.is_relative_to('/opt/lal_env') or runtime['files'].get(str(path),{}).get('sha256')!=sha(path):raise ValueError('Unpinned active origin '+name)
    budget=strict_json(contained(ROOT,cfg['budget_path']).read_bytes())
    hard=utc(budget['hard_deadline_utc'])
    if now>=hard:raise TimeoutError('Part B deadline')
    # Only after every dependency has been hashed may pinned E2 helpers import.
    sys.path.insert(0,str(B/'bis/e2_code'))
    return cfg,manifest,auth,min(hard,utc(auth['valid_until_utc']))
