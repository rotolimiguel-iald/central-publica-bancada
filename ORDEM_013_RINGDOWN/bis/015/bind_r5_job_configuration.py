"""Bind a registered/allocated source box to the exact configuration qualified by R5."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,os
B=Path(__file__).resolve().parents[2];C=B/'bis/e2_code_v1_1';D=B/'bis/015/t03'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=C/'registration_guard.py';raw=p.read_bytes();backup=D/'guard_before_job_qualification.py'
    with backup.open('xb') as f:f.write(raw)
    s=raw.decode('utf-8')
    anchor="    if not utc(q['at'])<=utc(reg['registered_utc']) or not utc(p['finished_utc'])<=utc(reg['registered_utc']):\n        raise ValueError('Qualification/probes postdate registration')\n    return True"
    assert s.count(anchor)==1
    s=s.replace(anchor,anchor.replace('    return True',"    for job in reg['pe_jobs'].values():validate_job_qualification(reg,job)\n    return True"))
    anchor='def validate_job_reviews(reg,job):\n    """Metadata-only gates, independent of any fitted posterior width."""'
    assert s.count(anchor)==1
    s=s.replace(anchor,'''SOURCE_QUALIFICATION_FIELDS=('variant','fixed_deformation_parameters','priors',
    'duration_s','sample_rate_hz','minimum_frequency_hz','maximum_frequency_hz',
    'generation_sample_rate_hz','generation_maximum_frequency_hz','reference_frequency_hz',
    'segment_start_GPS','onsource_roll_off_s')


def validate_job_qualification(reg,job):
    """Sampler/output identities may change; source support and grid may not."""
    activation=reg['activation_v1_1']
    manifest=contained(activation['qualification_inputs_relative_to_Chatgpt'])
    qualification=contained(activation['qualification_R5_relative_to_Chatgpt'])
    q=strict_json(qualification.read_bytes());m=strict_json(manifest.read_bytes())
    if q['status']!='R5_SOURCE_ONLY_QUALIFIED' or q['input_manifest_sha256']!=sha(manifest):
        raise ValueError('Job source qualification is absent or inputs changed')
    name=activation['qualification_configuration_name']
    if not isinstance(name,str) or Path(name).name!=name or name not in m['inputs']:
        raise ValueError('Qualified job configuration missing from R5 manifest')
    path=(manifest.parent/name).resolve()
    if not path.is_relative_to(manifest.parent.resolve()) or sha(path)!=m['inputs'][name]:
        raise ValueError('R5 qualified configuration changed')
    qualified=strict_json(path.read_bytes())
    if qualified['generation_maximum_frequency_hz']!=q['generation_maximum_frequency_hz']:
        raise ValueError('Job configuration belongs to a different R5 generation')
    for field in SOURCE_QUALIFICATION_FIELDS:
        if field not in job or job[field]!=qualified[field]:
            raise ValueError('Job source configuration differs from R5: '+field)
    return True


def validate_job_reviews(reg,job):
    """Source qualification and metadata gates, independent of fitted posterior width."""
    validate_job_qualification(reg,job)''')
    ast.parse(s);out=s.encode();temp=p.with_name(p.name+'.job_binding.pending')
    with temp.open('xb') as f:f.write(out);f.flush();os.fsync(f.fileno())
    assert temp.stat().st_size==len(out);os.replace(temp,p)
    receipt=dict(at=datetime.now(timezone.utc).isoformat(),status='R5_JOB_BOX_BINDING_IMPLEMENTED_PENDING_TESTS',before_sha256=sha(backup),after_sha256=sha(p),real_registration=False)
    with (D/'R5_JOB_BINDING_PATCH.json').open('xb') as f:f.write((json.dumps(receipt,indent=2)+'\n').encode())
    # New versions preserve earlier test evidence and the earlier draft-builder source.
    builder=B/'bis/015/prepare_v1_1_candidate.py';s=builder.read_text()
    old="qualification_scope_sha256=sha(scope),qualification_inputs_relative_to_Chatgpt="
    assert s.count(old)==1;s=s.replace(old,"qualification_scope_sha256=sha(scope),qualification_configuration_name='CONFIG_4096_RESERVED_INPUT.json',qualification_inputs_relative_to_Chatgpt=")
    s=s.replace('CANDIDATE_V1_1_001.json','CANDIDATE_V1_1_002.json').replace('CANDIDATE_001_RECEIPT.json','CANDIDATE_002_RECEIPT.json')
    with (B/'bis/015/prepare_v1_1_candidate_v2.py').open('xb') as f:f.write(s.encode())
    tests=(B/'bis/015/test_integrated_guard_v2.py').read_text().replace('guard_integration_tests_002','guard_integration_tests_003')
    old="    reg=copy.deepcopy(orig)";assert tests.count(old)==1
    tests=tests.replace(old,"    qualified_cfg=json.loads((B/'bis/015/t03/R5/CONFIG_4096_RESERVED_INPUT.json').read_bytes())\n"+old)
    tests=tests.replace("pe_jobs={'NEW_JOB':{'mode':'calibration','wall_budget_seconds':100}}","pe_jobs={'NEW_JOB':dict(copy.deepcopy(qualified_cfg),wall_budget_seconds=100)}")
    tests=tests.replace("qualification_scope_sha256=sha(scope),qualification_inputs_relative_to_Chatgpt=", "qualification_scope_sha256=sha(scope),qualification_configuration_name='CONFIG_4096_RESERVED_INPUT.json',qualification_inputs_relative_to_Chatgpt=")
    tests=tests.replace("jobs={'CAL2':{'mode':'calibration','wall_budget_seconds':200}}", "jobs={'CAL2':dict(copy.deepcopy(qualified_cfg),wall_budget_seconds=200)}")
    tests=tests.replace("extra2['jobs']['CAL3']={'mode':'calibration','wall_budget_seconds':300}","extra2['jobs']['CAL3']=dict(copy.deepcopy(qualified_cfg),wall_budget_seconds=300)")
    anchor="    check('missing_external_blind_review'"
    i=tests.index(anchor)
    tests=tests[:i]+'''    for label,change in [
      ('unqualified_fixed_440',lambda j:j.update(fixed_deformation_parameters={'dtau440':1.1,'domega440':0.0})),
      ('unqualified_mass_prior',lambda j:j['priors']['mass_1'].update(minimum=10)),
      ('unqualified_free_440',lambda j:j['priors'].update(dtau440={'kind':'Uniform','minimum':-.8,'maximum':4})),
      ('unqualified_frequency',lambda j:j.update(generation_maximum_frequency_hz=2048)),
      ('unqualified_time_support',lambda j:j.update(segment_start_GPS=0))]:
        job=copy.deepcopy(qualified_cfg);change(job)
        check(label,lambda:g.validate_job_qualification(reg,job),True)
    job=copy.deepcopy(qualified_cfg);job['sampler']['maxcall']+=1;job['output_directory_name']='ANOTHER_NEW_JOB'
    check('source_qualification_independent_of_output_sampler_budget',lambda:g.validate_job_qualification(reg,job))
'''+tests[i:]
    old="('unlicensed_download',lambda x:x['downloads'].update({'NEW_DOWNLOAD':{'url':'fixture'}}))"
    assert old in tests
    tests=tests.replace(old,"('allocated_box_not_qualified',lambda x:x['jobs']['CAL3']['priors']['mass_1'].update(minimum=10)),\n      "+old)
    with (B/'bis/015/test_integrated_guard_v3.py').open('xb') as f:f.write(tests.encode())
    print(json.dumps(receipt))
if __name__=='__main__':main()
