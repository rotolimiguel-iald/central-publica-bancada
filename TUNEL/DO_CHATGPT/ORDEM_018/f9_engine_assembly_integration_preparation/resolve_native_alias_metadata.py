"""Supplement UNC inventory using ELF SONAME, leaving Linux alias checks explicit.
No Linux process, native load, scientific import or candidate invocation.
"""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, struct, os, uuid

BASE = Path(__file__).resolve().parent
UNC = '\\\\wsl.localhost\\Ubuntu-24.04'
SYSTEM = '/usr/lib/x86_64-linux-gnu'


def host(p): return Path(UNC + p.replace('/', '\\'))


def dynamic(raw):
    if raw[:6] != b'\x7fELF\x02\x01': return None, []
    off = struct.unpack_from('<Q', raw, 32)[0]; size, count = struct.unpack_from('<HH', raw, 54)
    loads, section = [], None
    for i in range(count):
        row = struct.unpack_from('<IIQQQQQQ', raw, off+i*size)
        if row[0] == 1: loads.append((row[3], row[2], row[5]))
        if row[0] == 2: section = (row[2], row[5])
    if section is None: return None, []
    entries = []
    for i in range(section[0], sum(section), 16):
        key, value = struct.unpack_from('<qQ', raw, i)
        if key == 0: break
        entries.append((key, value))
    address = next((v for k, v in entries if k == 5), None)
    if address is None: return None, []
    base = next(o+address-a for a,o,s in loads if a <= address < a+s)
    def text(v):
        start=base+v; return raw[start:raw.index(b'\0',start)].decode()
    return next((text(v) for k,v in entries if k==14),None), [text(v) for k,v in entries if k==1]


def main():
    p=BASE/'RUNTIME_INVENTORY.json';old=p.read_bytes();doc=json.loads(old)
    assert 'alias_resolution_metadata' not in doc, 'Already supplemented; no automatic repeat'
    pins={x['path']:x for x in doc['pins']}
    queue=sorted({r['needed'] for r in doc['unresolved_native_dependencies']})
    seen=set();aliases=[];missing=[]
    while queue:
        name=queue.pop()
        if name in seen:continue
        seen.add(name)
        # A SONAME does not prove the on-host symlink: runtime must compare hash.
        candidates=[]
        for f in sorted(host(SYSTEM).glob(name+'*')):
            if not f.is_file():continue
            raw=f.read_bytes();soname,needed=dynamic(raw)
            if soname==name:
                candidates.append((SYSTEM+'/'+f.name,raw,needed))
        digests={hashlib.sha256(raw).hexdigest() for _,raw,_ in candidates}
        if len(digests)!=1:
            missing.append({'needed':name,'candidate_paths':[p for p,_,_ in candidates],
                            'reason':'NO_UNIQUE_BYTES_FOR_SONAME'})
            continue
        path,raw,needed=candidates[0]
        pin={'path':path,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()};pins[path]=pin
        aliases.append({'alias_path':SYSTEM+'/'+name,'candidate_path':path,'bytes':pin['bytes'],
                        'sha256':pin['sha256'],'ELF_SONAME':name,
                        'status':'CANDIDATE_ONLY_LINUX_ALIAS_HASH_REQUIRED_BEFORE_SOLVER'})
        for dep in needed:
            if not any(Path(x).name==dep for x in pins) and dep not in seen:queue.append(dep)
    doc['alias_resolution_metadata']={'created_utc':datetime.now(timezone.utc).isoformat(),
        'input_sha256':hashlib.sha256(old).hexdigest(),'method':'ELF DT_SONAME matching; not symlink observation',
        'checks_required_in_Linux':aliases,'unresolved':missing,'Linux_processes_started':0}
    doc['pins']=[pins[x] for x in sorted(pins)]
    doc['original_unresolved_native_dependencies']=doc['unresolved_native_dependencies']
    doc['unresolved_native_dependencies']=missing
    doc['status']='STATIC_PINS_WITH_CONDITIONAL_NATIVE_ALIAS_CHECKS'
    raw=(json.dumps(doc,ensure_ascii=False,indent=2)+'\n').encode()
    bak=p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'));bak.write_bytes(old);assert bak.read_bytes()==old
    temp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);temp.write_bytes(raw);assert temp.read_bytes()==raw and p.read_bytes()==old;os.replace(temp,p)
    print(json.dumps({'files':len(pins),'native_alias_candidates':len(aliases),'unresolved':missing,
        'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'candidate_imports':0,'solver_calls':0}))


if __name__=='__main__':main()
