"""Synthetic metadata gates only; never read a result or posterior."""
import ast,copy,json,hashlib,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
def main():
    ns={};tree=ast.parse((HERE/'review_future_pilot.py').read_text())
    import math
    ns['math']=math
    funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('finite','count','gates')]
    exec(compile(ast.Module(body=funcs,type_ignores=[]),'<metadata gates only>','exec',optimize=1),ns)
    settings=dict(dlogz=.1,maxcall=1000,minimum_effective_samples=100,minimum_posterior_samples=1000)
    ctrl=dict(status='CHILD_COMPLETED_REQUIRES_REVIEW',returncode=0,cleanup=dict(group_absent=True))
    conv=dict(status='CONVERGENCE_CRITERIA_MET_REQUIRES_INDEPENDENT_REVIEW',accepted_for_analysis=True,before_add_live=True,
        delta_logz=.09,threshold=.1,ncall=900,ncall_reported=900,ess=101.,posterior_samples=1001,log_evidence=-10.,log_evidence_err=.1)
    results=[]
    def check(name,ok):
        if not ok:raise RuntimeError(name)
        results.append(dict(name=name,passed=True))
    check('valid_synthetic_metadata',not ns['gates'](ctrl,conv,settings))
    for name,value in [('before_add_live',False),('delta_logz',.1),('delta_logz',float('nan')),('ncall',1000),('ncall',True),
        ('ncall_reported',899),('ess',99.),('posterior_samples',999),('accepted_for_analysis',False),('status','PARTIAL_LIKELIHOOD_PLATEAU'),
        ('threshold',.2),('log_evidence',float('inf')),('log_evidence_err',-1.)]:
        x=copy.deepcopy(conv);x[name]=value
        check('refuse_'+name+'_'+str(value),bool(ns['gates'](ctrl,x,settings)))
    for status in ('BUDGET_STOPPED_PARTIAL_NOT_POSTERIOR','OWNED_GROUP_CLEANUP_UNCONFIRMED','CHILD_FAILED_OR_INTERRUPTED','PARTIAL_MAXCALL_NOT_ACCEPTED'):
        c=copy.deepcopy(ctrl);c['status']=status;check(status,bool(ns['gates'](c,conv,settings)))
    c=copy.deepcopy(ctrl);c['cleanup']['group_absent']=False
    check('cleanup_not_confirmed',bool(ns['gates'](c,conv,settings)))
    check('explicit_failure',bool(ns['gates'](ctrl,conv,settings,True)))
    check('partial_analyst',bool(ns['gates'](ctrl,conv,settings,False,{'accepted':False})))
    check('missing_convergence',bool(ns['gates'](ctrl,None,settings)))
    result=dict(status='PREPARATION_METADATA_FIXTURES_ONLY',python_optimize=sys.flags.optimize,checks=results,
        actual_outputs_opened=False,posterior_or_strain_opened=False,science_executed=False,
        coverage_limit='Only pure metadata gates and Python syntax; accepted HDF5/posterior path remains unexecuted until real result exists',
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    with (HERE/'PREPARATION_TESTS.json').open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(dict(checks=len(results),status=result['status'])))
if __name__=='__main__':main()
