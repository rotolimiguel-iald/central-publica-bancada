"""Record independent static review, no waveforms, PE, strain, or posterior."""
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
import re

HERE=Path(__file__).resolve().parent
B=HERE.parents[1]
ROOT=B.parent
pins={}
checks=[]
def sha(path):
    value=hashlib.sha256(path.read_bytes()).hexdigest();pins[str(path)]=value
    return value
def load(path):
    sha(path);return json.loads(path.read_bytes())
def check(name,value):
    checks.append(dict(name=name,passed=bool(value)))
    if not value:raise ValueError(name)

regpath=B/'RINGDOWN_5SIGMA_V1.json';reg=load(regpath)
code=B/'bis/e2_code'
tree={p.relative_to(code).as_posix():sha(p) for p in code.rglob('*.py')}
check('frozen_whole_tree_unchanged',tree==reg['own_code_tree_sha256'] and len(tree)==14)
run=B/'cache/E3_PSEOB_PILOT_V1'
controller=load(run/'CONTROLLER.json');ctx=load(run/'LAUNCH_CONTEXT.json')
check('known_calibration_log_authorized',controller['job']=='GW250114_PILOT' and controller['blind'] is False)
check('preserved_log_pin',sha(run/'PRIVATE.log')==controller['private_log_sha256'])
text=(run/'PRIVATE.log').read_text()
check('registration_bindings',controller['registration_sha256']==ctx['registration_sha256']==sha(regpath))
check('controller_source_pin',controller['controller_code_sha256']==sha(code/'run_controlled.py'))
cfg=reg['pe_jobs']['GW250114_PILOT']
check('configuration_pin',hashlib.sha256(json.dumps(cfg,sort_keys=True,allow_nan=False).encode()).hexdigest()==ctx['config_sha256'])
check('failed_not_posterior',controller['returncode']==-11 and controller['status']=='CHILD_FAILED_OR_INTERRUPTED')
check('cleanup_receipt',controller['cleanup']['group_absent'] is True)
srcfolder=B/'cache/source_evidence/lal_generator_source_gitlab'
prov=load(srcfolder/'PROVENANCE.json')
check('C_source_archived_pin',sha(srcfolder/'LALSimIMRSpinAlignedEOB.c')==prov['sha256'])
c=(srcfolder/'LALSimIMRSpinAlignedEOB.c').read_text()
check('HM_550_guard_source',all(s in c for s in ['mode_highest_freqL = 5','mode_highest_freqM = 5','deltaT > LAL_PI / creal (modeFreq)']))
site=Path('/opt/lal_env/lib/python3.12/site-packages')
runtime=load(B/'bis/E2_SCIENTIFIC_RUNTIME_MANIFEST.json')
installed={}
for name in ['bilby/gw/source.py','lalsimulation/git_version.py']:
    path=site/name
    check('installed_pin:'+name,sha(path)==runtime['files'][str(path)]['sha256'])
    installed[name]=path.read_text()
commit=re.search(r'^id = "([0-9a-f]{40})"',installed['lalsimulation/git_version.py'],re.M).group(1)
check('C_commit_matches_declared_install',commit==prov['installed_commit'])
check('bilby_EDOM_to_none',"if EDOM:" in installed['bilby/gw/source.py'] and 'return None' in installed['bilby/gw/source.py'])
witness=ROOT/reg['witness_relative_to_Chatgpt'];sha(witness)
check('parent_witness_binding',re.findall(r'^registro_sha256: ([a-f0-9]{64})$',witness.read_text(),re.M)==[sha(regpath)])
diagnostic=B/'bis/e3_pilot_failure_diagnostic'
available=[p.name for p in diagnostic.iterdir()] if diagnostic.exists() else []
for name in ('collect_and_plan.py','PLAN_INPUTS.json'):
    if (diagnostic/name).exists():sha(diagnostic/name)
sha(HERE/'PILOT_NATIVE_FAILURE_PRELIMINARY_REVIEW.md')
report=dict(status='DIAGNOSIS_OPEN_NO_CONTINUATION_APPROVAL',created_utc=datetime.now(timezone.utc).isoformat(),
    blocking_findings=[
      dict(id='NF-R1',issue='Native crash causal path and complete failing input not isolated by this review; consume A finite diagnosis before repair approval.'),
      dict(id='NF-R2',issue='Concrete repair must preserve prior, family/modes and analysis band while resolving numerical generation failures without silent -inf support trimming.'),
      dict(id='NF-R3',issue='Versioned amendment, exact source/import pins, parent registration/witness and original absolute stop required before continuation.')],
    checks=checks,input_hashes=pins,controller=controller,context=ctx,
    failure_observations=dict(nyquist_messages=text.count('Ringdown frequency > Nyquist frequency!'),
       explicit_minus_infinity_messages=text.count('Likelihood will be set to -inf.'),
       original_absolute_stop=ctx['stop_utc'],source_calls=None,likelihood_calls=None,posterior=None,
       final_artifacts_present={name:(run/name).exists() for name in ['PRIVATE_CONVERGENCE.json','ANALYST_OUTPUT.json','FAILURE.json']},
       analysis_fs_hz=cfg['sample_rate_hz'],analysis_fmax_hz=cfg['maximum_frequency_hz'],
       domega_prior_upper={name:cfg['priors'][name]['maximum'] for name in ('domega220','domega440')}),
    primary_source_identity=dict(declared_commit=commit,C_source_sha256=prov['sha256'],binary_build_reproducibility='NOT_ESTABLISHED'),
    A_diagnostic_files_at_snapshot=available,
    scope=['Read-only known-calibration log and source review. No native diagnostic executed by reviewer.',
           'Two EDOM warnings do not identify the later SIGSEGV call.',
           'The logged Nyquist guard uses GR550 in the HM branch; not direct evidence against the domega prior.',
           'Data Nyquist2048 and generation fmax1024 are distinct; exact native deltaT awaits source/diagnostic corroboration.',
           'No approval to extend the original 8h envelope or silently inherit amendment in blind jobs.'],
    scientific_execution=False,original_sources_modified=False,script_sha256=sha(Path(__file__)))
out=HERE/'PILOT_NATIVE_FAILURE_PRELIMINARY_REVIEW.json'
with out.open('xb') as f:f.write((json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
print(json.dumps(dict(status=report['status'],checks=len(checks),receipt_sha256=sha(out),A_files=available)))
