"""Small finite guard tests; functions extracted by AST, no production entrypoint."""
import ast
import copy
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import types
import numpy as np

HERE=Path(__file__).resolve().parent
CODE=HERE.parent/'e2_code'
checks=[]


def functions(file,names,namespace):
    tree=ast.parse((CODE/file).read_text())
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    if {n.name for n in nodes}!=set(names):raise RuntimeError('Function missing')
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(CODE/file),'exec'),namespace)
    return namespace


def check(name,value):
    if not value:raise RuntimeError('Failed: '+name)
    checks.append(dict(name=name,passed=True))


def rejects(name,call,exception=(ValueError,RuntimeError,TimeoutError)):
    try:call()
    except exception:check(name,True)
    else:raise RuntimeError('Did not reject: '+name)


def main():
    ns={'math':math,'json':json}
    functions('registration_guard.py',['positive','integer','strict_json'],ns)
    rejects('duplicate_registration_key',lambda:ns['strict_json']('{"x":1,"x":2}'))
    rejects('NaN_registration_constant',lambda:ns['strict_json']('{"x":NaN}'))
    functions('pe_runner.py',['validate_config','terminal_state','convergence','posterior_columns'],ns)
    ns['PHYSICAL']=('mass_1','mass_2','chi_1','chi_2','luminosity_distance','theta_jn','phase','ra','dec','psi','geocent_time')
    ns['DEFORMATIONS']=('dtau220','dtau440','domega220','domega440')
    draft=json.loads((HERE.parent/'E2_DESIGN_DRAFT_001.json').read_text())
    cfg=copy.deepcopy(draft['pe_jobs']['GW250114_PILOT'])
    cfg.update(fixed_deformation_parameters={},privacy_mode='procedural_same_host')
    cfg.update(duration_s=8,segment_start_GPS=1420878135.)
    ns['validate_config'](cfg);check('declared_pilot_config_valid',True)
    for name,edit in [('fixed_mass',lambda c:c['priors'].update(mass_1=40)),
                      ('fixed_spin',lambda c:c['priors'].update(chi_1=.2)),
                      ('missing_deformation',lambda c:c['priors'].pop('dtau440')),
                      ('mass_ratio_sampled',lambda c:c['priors']['mass_ratio'].update(kind='Uniform')),
                      ('nonfinite_width',lambda c:c['priors']['dtau220'].update(maximum=float('nan'))),
                      ('checkpoint_enabled',lambda c:c['sampler'].update(check_point=True)),
                      ('too_many_workers',lambda c:c['sampler'].update(workers=29))]:
        item=copy.deepcopy(cfg);edit(item);rejects(name,lambda:ns['validate_config'](item))
    invalid_time=copy.deepcopy(cfg);invalid_time['priors']['geocent_time']['maximum']=1420878143.
    rejects('time_prior_outside_untapered_window',lambda:ns['validate_config'](invalid_time))
    source=functions('pseob_source.py',['validate_polarizations'],{'np':np})['validate_polarizations']
    f=np.arange(3.)
    check('None_preserved',source(None,f,0,2) is None)
    rejects('joint_zero',lambda:source({'plus':f*0,'cross':f*0},f,0,2))
    rejects('NaN_waveform',lambda:source({'plus':np.array([0,np.nan,1]),'cross':f},f,0,2))
    rejects('wrong_shape',lambda:source({'plus':np.zeros(2),'cross':f},f,0,2))
    check('single_zero_polarization_allowed',source({'plus':f,'cross':f*0},f,0,2) is not None)
    settings=cfg['sampler']
    sampler=types.SimpleNamespace(ncall=100,saved_run={'logz':[0.],'logvol':[-20.]},live_logl=np.array([0.,1.]))
    state=ns['terminal_state'](sampler,settings)
    check('delta_before_live_reached',state['status']=='DLOGZ_REACHED_REQUIRES_ESS' and state['before_add_live'])
    sampler.ncall=settings['maxcall'];check('maxcall_never_accepted',ns['terminal_state'](sampler,settings)['status']=='PARTIAL_MAXCALL_NOT_ACCEPTED')
    sampler.ncall=100;sampler.saved_run['logvol']=[0.]
    check('delta_fail_closed',ns['terminal_state'](sampler,settings)['status']=='PARTIAL_DLOGZ_NOT_REACHED')
    sampler.live_logl=np.array([0.,0.]);check('plateau_rejected',ns['terminal_state'](sampler,settings)['status']=='PARTIAL_LIKELIHOOD_PLATEAU')
    class Posterior(dict):
        def __len__(self):return 1000
    posterior=Posterior({k:np.ones(1000) for k in ns['PHYSICAL']+ns['DEFORMATIONS']})
    result=types.SimpleNamespace(meta_data={'e2_terminal':state},nested_samples={'weights':np.ones(1000)/1000},
        posterior=posterior,log_evidence=0.,log_evidence_err=.01,num_likelihood_evaluations=100)
    check('ESS_positive_control',ns['convergence'](result,settings)['accepted_for_analysis'])
    result.nested_samples={'weights':np.array([1.,0.])}
    check('low_ESS_rejected',ns['convergence'](result,settings)['status']=='PARTIAL_LOW_ESS')
    result.num_likelihood_evaluations=101
    check('ncall_mismatch_rejected',ns['convergence'](result,settings)['status']=='PARTIAL_NCALL_MISMATCH')
    check('paired_full_columns',len(ns['posterior_columns'](posterior,cfg))==15)
    posterior.pop('mass_1');rejects('missing_physical_column',lambda:ns['posterior_columns'](posterior,cfg))
    nsblind=functions('blinding.py',['unblinding_allowed'],{'np':np})
    reg={'blinding':{'minimum_information_to_unblind':float('nan')}}
    check('NaN_unblind_rejected',nsblind['unblinding_allowed'](reg,1.,True,{'status':'REGISTERED_UNBLINDING_GATE_MET'}) is False)
    # Pure mocked process group: leader exits but worker survives TERM.
    alive={'value':True};signals=[];clock={'t':0.}
    def killpg(pid,sig):
        signals.append(sig)
        if sig==signal.SIGKILL:alive['value']=False
    class Child:
        pid=1234
        def poll(self):return 0
        def wait(self,timeout):return 0
    controlled=functions('run_controlled.py',['cleanup_group'],{
        'os':types.SimpleNamespace(getpgrp=lambda:9000,killpg=killpg), 'signal':signal,
        'group_exists':lambda _:alive['value'],
        'time':types.SimpleNamespace(monotonic=lambda:clock['t'],sleep=lambda t:clock.update(t=clock['t']+t)),
        'subprocess':types.SimpleNamespace(TimeoutExpired=TimeoutError)})
    cleanup=controlled['cleanup_group'](Child(),.1)
    check('worker_killed_after_leader_exit',signals==[signal.SIGTERM,signal.SIGKILL] and cleanup['group_absent'])
    # Ensure mandatory launch-context at parser level before any registry/science.
    tree=ast.parse((CODE/'pe_runner.py').read_text())
    calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='add_argument']
    check('launcher_argument_required',any(any(isinstance(a,ast.Constant) and a.value=='--launch-context' for a in n.args)
        and any(k.arg=='required' and isinstance(k.value,ast.Constant) and k.value.value is True for k in n.keywords) for n in calls))
    out=dict(status='FINITE_MOCKS_ONLY_NO_PE_NO_WAVEFORM_NO_STRAIN_NO_SEED',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        checks=checks,source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in CODE.glob('*.py')},
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),real_processes_spawned=0)
    with (HERE/'OWNED_V3_TESTS.json').open('x') as f:json.dump(out,f,indent=2)
    print(json.dumps(dict(status=out['status'],passed=len(checks))))


if __name__=='__main__':main()
