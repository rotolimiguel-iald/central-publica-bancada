"""Close source-only R5 evidence, verify original V1 and explicitly scope changed guard."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,ast,importlib.util,resource,time
import numpy as np,lal,lalsimulation as ls
B=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN');D=B/'bis/015/t03';C=B/'bis/e2_code_v1_1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def body(p,name):
    node=next(n for n in ast.parse(p.read_text('utf-8-sig')).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==name)
    return ast.dump(node,include_attributes=False)
def main():
    start=time.perf_counter();m=json.loads((D/'R5/INPUT_MANIFEST.json').read_bytes())
    actual={p.name:sha(p) for p in C.glob('*.py')};changed=[n for n,h in m['source_tree'].items() if actual[n]!=h]
    assert changed==['registration_guard.py']
    preserved={name:body(C/'registration_guard.py',name)==body(B/'bis/e2_code/registration_guard.py',name) for name in ('positive','integer','checked_registration','authorize_event','time_guard')}
    assert all(preserved.values())
    spec=importlib.util.spec_from_file_location('audit_original',B/'bis/015/t03_preserve_and_copy.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    v1=helper.check();assert v1['acceptable']
    q=lal.CreateCOMPLEX16Vector(1)
    ls.SimIMREOBGenerateQNMFreqV2(q,15.,10.,[0.,0.,.99],[0.,0.,.99],5,5,1,ls.SEOBNRv4)
    f550=float(q.data[0].real/(2*np.pi));assert 2048<f550<4096
    r=dict(at=datetime.now(timezone.utc).isoformat(),status='SOURCE_R5_EVIDENCE_CLOSED_NOT_REGISTRATION',
      v1_guard_after=v1,source_runner_temporal_hashes_unchanged=True,changed_sibling_files_since_R5_freeze=changed,
      guard_change='Only unused chain helpers appended/schema-corrected after child imported; runner utilities and all original guard functions above remain structurally identical.',
      guard_AST_preservation=preserved,source_only_scope='Source, build_priors, validate_config, parameter_conversion, temporal contract. Does not qualify final activation/registration guard.',
      minimum_mass_max_spin_corner=dict(mass_1=15.,mass_2=10.,chi_1=.99,chi_2=.99,f550_GR_hz=f550,generation_4096_margin_hz=4096-f550),
      required_generation_sample_rate_hz=8192,required_generation_maximum_frequency_hz=4096,analysis_band_hz=[20,1024],
      source_path_function_hashes={f'{file}:{name}':hashlib.sha256(body(C/file,name).encode()).hexdigest() for file,names in [('pe_runner.py',['build_priors','validate_config','prior_conversion']),('pseob_source.py',['pseob_frequency_domain','parameter_conversion','generation_grid']),('temporal_contract.py',['validate_time_contract'])] for name in names},
      evidence={str(p.relative_to(D)):sha(p) for p in [D/'R5/generation_2048/RESULT.json',D/'R5/generation_4096/RESULT.json',D/'source_tests_001/RESULT.json',D/'native_bin_control_001/RESULT.json',D/'chain_tests_001/RESULT.json']},
      wall_seconds=time.perf_counter()-start,cpu_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime,
      heavy_machine_hours=0,seed_content_read=False,registration_activated=False)
    with (D/'R5_SOURCE_CLOSING.json').open('xb') as f:f.write((json.dumps(r,indent=2)+'\n').encode())
    print(json.dumps({k:r[k] for k in ['status','v1_guard_after','minimum_mass_max_spin_corner','source_only_scope']}))
if __name__=='__main__':main()
