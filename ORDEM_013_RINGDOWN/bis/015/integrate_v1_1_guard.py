"""Wire existing guard entry points to the witnessed V1.1 protocol in the copy."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,os
B=Path(__file__).resolve().parents[2];C=B/'bis/e2_code_v1_1';D=B/'bis/015/t03'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def replace(s,a,b):
    if s.count(a)!=1:raise ValueError('Nonunique integration anchor: '+a[:80])
    return s.replace(a,b)
def main():
    p=C/'registration_guard.py';raw=p.read_bytes();snap=D/'guard_integration_before_001';snap.mkdir(exist_ok=False)
    with (snap/p.name).open('xb') as f:f.write(raw)
    s=raw.decode();s=replace(s,'import hashlib,json,re,os,sys,math,stat,importlib.util','import hashlib,json,re,os,sys,math,stat,importlib.util,ast')
    start=s.index('    path=BASE/',s.index('def checked_registration():'));end=s.index('    own=',start)
    s=s[:start]+'''    reg,digest,note=load_registration_chain_v1_1()
    if reg['status']!='REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST':raise ValueError('Not an active E2 registration')
    check_activation_v1_1(reg,digest,note)
'''+s[end:]
    start=s.index('def check_activation(');end=s.index('\ndef time_guard(',start)
    s=s[:start]+'''def check_activation_v1_1(reg,digest,note):
    """Local calibration marker; this never substitutes for management blind audit."""
    activation=reg['activation_v1_1']
    if activation['receipt_relative_to_Chatgpt']!='ORDEM_013_RINGDOWN/bis/015/E2_V1_1_REGISTRATION_RECEIPT.json':
        raise ValueError('Wrong V1.1 activation receipt path')
    receipt=strict_json(contained(activation['receipt_relative_to_Chatgpt']).read_bytes())
    if receipt['status']!='E2_V1_1_REGISTERED' or receipt['registration_sha256']!=digest or receipt['witness_sha256']!=sha(note):
        raise ValueError('V1.1 activation does not match latest registration/witness')
    probes=contained(activation['probes_result_relative_to_Chatgpt'])
    qualification=contained(activation['qualification_R5_relative_to_Chatgpt'])
    scope=contained(activation['qualification_scope_relative_to_Chatgpt'])
    manifest=contained(activation['qualification_inputs_relative_to_Chatgpt'])
    if any(not p.is_relative_to(BASE/'bis/015') for p in (probes,qualification,scope,manifest)):
        raise ValueError('V1.1 local evidence outside its bench')
    if sha(probes)!=receipt['probes_result_sha256'] or sha(qualification)!=receipt['qualification_R5_sha256']:
        raise ValueError('Activation evidence hash differs')
    if sha(scope)!=activation['qualification_scope_sha256']:raise ValueError('R5 source scope changed')
    q=strict_json(qualification.read_bytes());m=strict_json(manifest.read_bytes());p=strict_json(probes.read_bytes());sc=strict_json(scope.read_bytes())
    if q['status']!='R5_SOURCE_ONLY_QUALIFIED' or q['crashes'] or q['failures']:
        raise ValueError('R5 source qualification unpaid')
    n=integer(q['n_items'],'R5 items',1000)
    if q['returns']!=n or q['status_counts']!={'FINITE_WAVEFORM':n} or m['random_draws']<1000 or m['total']!=n:
        raise ValueError('R5 incomplete or nonfinite qualification')
    if q['input_manifest_sha256']!=sha(manifest):raise ValueError('R5 inputs changed')
    for name,pin in m['inputs'].items():
        path=(manifest.parent/name).resolve()
        if not path.is_relative_to(manifest.parent.resolve()) or sha(path)!=pin:raise ValueError('R5 input pin changed')
    # R5 qualified source/priors, not this new activation implementation.
    for name in ('pseob_source.py','temporal_contract.py'):
        if sha(CODE/name)!=m['source_tree'][name]:raise ValueError('Qualified source/temporal code changed')
    required={'pe_runner.py:build_priors','pe_runner.py:validate_config','pe_runner.py:prior_conversion',
      'pseob_source.py:pseob_frequency_domain','pseob_source.py:parameter_conversion','pseob_source.py:generation_grid',
      'temporal_contract.py:validate_time_contract'}
    if set(sc['source_path_function_hashes'])!=required:raise ValueError('R5 source scope incomplete')
    if sc['evidence'].get('R5/generation_4096/RESULT.json')!=sha(qualification):raise ValueError('Qualification scope/result mismatch')
    for label,pin in sc['source_path_function_hashes'].items():
        file,name=label.split(':');nodes=[n for n in ast.parse((CODE/file).read_text('utf-8-sig')).body if isinstance(n,ast.FunctionDef) and n.name==name]
        if len(nodes)!=1 or hashlib.sha256(ast.dump(nodes[0],include_attributes=False).encode()).hexdigest()!=pin:
            raise ValueError('R5 qualified function changed: '+label)
    if p['status']!='V1_1_GUARD_PROBES_PASSED' or p['own_code_tree_sha256']!=reg['own_code_tree_sha256']:
        raise ValueError('Guard probes do not cover this code tree')
    if p['statistical_subobject_sha256']!=reg['statistical_subobject_sha256']:
        raise ValueError('Guard probes statistical commitment differs')
    if not isinstance(p['tests'],list) or not p['tests'] or any(t.get('passed') is not True for t in p['tests']):
        raise ValueError('Guard probes failed or absent')
    if not utc(q['at'])<=utc(reg['registered_utc']) or not utc(p['finished_utc'])<=utc(reg['registered_utc']):
        raise ValueError('Qualification/probes postdate registration')
    return True


def check_blind_activation(reg):
    """An external management receipt is separate from local calibration controls."""
    current,digest,_=load_registration_chain_v1_1()
    if reg['registration_id']!=current['registration_id'] or reg['test_candidates']!=current['test_candidates']:
        raise ValueError('Blind authorization uses stale registration/candidates')
    note=ROOT/'TUNEL/PARA_CHATGPT/RECIBO_015_V1_1_AUDITADA.md'
    text=note.read_text('utf-8-sig')
    if re.findall(r'^registro_sha256: ([0-9a-f]{64})\\s*$',text,re.M)!=[digest]:
        raise ValueError('Management blind-audit receipt differs or is ambiguous')
    if not utc(current['registered_utc']).timestamp()<=note.stat().st_mtime<=datetime.now(timezone.utc).timestamp()+2:
        raise ValueError('Management audit chronology invalid')
    return True

'''+s[end:]
    s=replace(s,"    if mode=='blind_test':\n        if event in known:","    if mode=='blind_test':\n        check_blind_activation(reg)\n        if event in known:")
    start=s.index('def load_jobs(');end=s.index('\ndef validate_launch(',start)
    s=s[:start]+'''def load_jobs(reg,digest):
    return load_authorized_configuration(reg,digest)['pe_jobs']


def load_authorized_configuration(reg,digest):
    """Validate every allocation link; latest cumulative allocation governs."""
    view=dict(reg);jobs=dict(reg['pe_jobs']);downloads=dict(reg.get('downloads',{}))
    for job in jobs.values():validate_job_reviews(reg,job)
    policy=reg['allocation_policy']
    if policy['pattern']!='ORCAMENTO_015_v*.json':raise ValueError('Wrong allocation chain pattern')
    cap=positive(policy['max_job_wall_seconds'],'allocation cap')
    if cap>28800:raise ValueError('Allocation wall cap exceeds eight hours')
    paths=numbered_chain(BASE,policy['pattern'],'ORCAMENTO_015_v')
    # Earlier allocations remain valid across amendments; each points to its actual ancestor.
    regs=[BASE/'RINGDOWN_5SIGMA_V1_1.json']+numbered_chain(BASE,'RINGDOWN_5SIGMA_V1_1_*.json','RINGDOWN_5SIGMA_V1_1_')
    if sha(regs[-1])!=digest:raise ValueError('Allocation caller is not latest registration')
    ancestors={}
    for index,path in enumerate(regs):
        ancestor=strict_json(path.read_bytes());pin=sha(path)
        note=contained(ancestor['witness_relative_to_Chatgpt']);check_witness(note,pin,ancestor['registered_utc'])
        dates=re.findall(r'^registered_utc: (\\S+)\\s*$',note.read_text('utf-8-sig'),re.M)
        ancestors[pin]=(index,utc(dates[0]))
    original=strict_json((BASE/'RINGDOWN_5SIGMA_V1.json').read_bytes())
    old_jobs=set(original['pe_jobs']);previous=None;previous_time=None;previous_index=-1
    previous_jobs={};previous_downloads={};snapshots={}
    for k,path in enumerate(paths,1):
        pin=sha(path);allocation=strict_json(path.read_bytes());snapshots[path]=pin
        if allocation['supersedes_sha256']!=previous:raise ValueError('Allocation parent mismatch')
        parent=allocation['parent_registration_sha256']
        if parent not in ancestors:raise ValueError('Unknown allocation registration ancestor')
        index,witnessed=ancestors[parent];issued=utc(allocation['registered_utc'])
        if index<previous_index or issued<witnessed or (previous_time is not None and issued<previous_time):
            raise ValueError('Allocation chronology reversed')
        note=contained(allocation['witness_relative_to_Chatgpt'])
        if note!=ROOT/'TUNEL/DO_CHATGPT'/('ENTREGA_015_ORCAMENTO_015_v'+str(k)+'.md'):
            raise ValueError('Wrong allocation witness path')
        check_witness(note,pin,allocation['registered_utc'],'allocation_sha256');snapshots[note]=sha(note)
        dates=re.findall(r'^registered_utc: (\\S+)\\s*$',note.read_text('utf-8-sig'),re.M)
        config=contained(allocation['jobs_relative_to_Chatgpt']);config_pin=sha(config);snapshots[config]=config_pin
        if config_pin!=allocation['jobs_sha256']:raise ValueError('Allocation configuration changed')
        extra=strict_json(config.read_bytes())
        if extra['schema_version']!='E2_PE_JOBS_V2' or extra['parent_registration_sha256']!=parent:
            raise ValueError('Wrong allocation jobs schema/parent')
        new_jobs=extra['jobs'];new_downloads=extra.get('downloads',{})
        if not isinstance(new_jobs,dict) or not isinstance(new_downloads,dict):raise ValueError('Allocation maps required')
        if any(name not in new_jobs or new_jobs[name]!=job for name,job in previous_jobs.items()):
            raise ValueError('Allocated job removed/replaced')
        if any(name not in new_downloads or new_downloads[name]!=item for name,item in previous_downloads.items()):
            raise ValueError('Allocated download removed/replaced')
        for name,job in new_jobs.items():
            if name in old_jobs:raise ValueError('V1 job cannot be relaunched')
            if name in jobs and jobs[name]!=job:raise ValueError('Allocation replaces an existing job')
            if positive(job['wall_budget_seconds'],'job wall')>cap:raise ValueError('Job exceeds allocation wall cap')
            validate_job_reviews(reg,job);jobs[name]=job
        for name,item in new_downloads.items():
            if name in downloads and downloads[name]!=item:raise ValueError('Allocation replaces a download')
            if not item.get('license_receipt_relative_to_Chatgpt') or not item.get('license_receipt_sha256'):
                raise ValueError('Per-file license receipt required')
            license=contained(item['license_receipt_relative_to_Chatgpt'])
            if sha(license)!=item['license_receipt_sha256']:raise ValueError('License receipt changed')
            snapshots[license]=item['license_receipt_sha256'];downloads[name]=item
        previous=pin;previous_time=utc(dates[0]);previous_index=index
        previous_jobs=new_jobs;previous_downloads=new_downloads
    if paths!=numbered_chain(BASE,policy['pattern'],'ORCAMENTO_015_v') or any(sha(p)!=pin for p,pin in snapshots.items()):
        raise ValueError('Allocation chain changed during read')
    view.update(pe_jobs=jobs,downloads=downloads,_parent_registration_sha256=digest,_allocation_sha256=previous)
    return view

'''+s[end:]
    # Check every chain member status and refuse a half-written newly appearing amendment.
    s=replace(s,"        reg=strict_json(path.read_bytes());digest=sha(path)\n        if reg['parent_registration_sha256']", "        reg=strict_json(path.read_bytes());digest=sha(path)\n        if reg['status']!='REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST':raise ValueError('Inactive amendment')\n        if reg['parent_registration_sha256']")
    ast.parse(s);out=s.encode();temp=p.with_name(p.name+'.integration.pending')
    with temp.open('xb') as f:f.write(out);f.flush();os.fsync(f.fileno())
    assert temp.stat().st_size==len(out);os.replace(temp,p)
    result=dict(at=datetime.now(timezone.utc).isoformat(),status='V1_1_GUARD_WIRED_PENDING_PROBES_AND_REGISTRATION',before_sha256=sha(snap/p.name),after_sha256=sha(p),old_V1_changed=False,real_activation=False)
    with (D/'GUARD_INTEGRATION_PATCH_001.json').open('xb') as f:f.write((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(result))
if __name__=='__main__':main()
