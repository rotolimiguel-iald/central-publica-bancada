"""Reuse R78 once at the analytically selected cut; coherent-drive conversion."""
from pathlib import Path
import hashlib, importlib.util, json, math, sys


def calculate(plan):
    import numpy as np
    for row in plan['sources']:
        if hashlib.sha256(Path(row['path']).read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Source changed: '+row['path'])
    source=next(row for row in plan['sources'] if row['role']=='r78_consumer')
    sys.dont_write_bytecode=True
    spec=importlib.util.spec_from_file_location('pinned_r78_response_reuse',source['path'])
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    reused=json.loads(json.dumps(plan['reused_plan']))
    if reused['cut'] != plan['selected_cut']:raise ValueError('Cut mismatch')
    result=mod.calculate(reused)
    factor=math.sqrt(2)/(reused['input_gain']*reused['output_gain'])
    for branch in result['branches'].values():
        def complex_array(name):
            d=branch[name];return np.asarray(d['real'])+1j*np.asarray(d['imag'])
        hp=-1j*factor*complex_array('wirtinger_h_plus')
        hm=1j*factor*complex_array('wirtinger_h_minus')
        if not np.all(np.isfinite(hp)) or not np.all(np.isfinite(hm)):raise ValueError('Nonfinite converted response')
        branch['coherent_drive_H_plus']={'real':hp.real.tolist(),'imag':hp.imag.tolist()}
        branch['coherent_drive_H_minus']={'real':hm.real.tolist(),'imag':hm.imag.tolist()}
        branch['coherent_drive_convention']='Hcoh=i sqrt(kappa_i)(alpha* ai-alpha ai†); u=x+iy=-i sqrt(2) alpha/gain_in; alpha_out=z/gain_out. Fixed synthetic model normalization, not calibrated RF/laser.'
        branch['continuum_tail_each_H_plus_minus']=plan['planning']['physical_H_tail_upper_at_selected_cut']
    result['inherited_r78_scope_historical']=result.pop('limits')
    result['limits']=plan['limits']
    result['status']='SYNTHETIC_RESPONSE_REFINEMENT_WITH_ANALYTIC_CONTINUUM_TAIL'
    result['planning']=plan['planning']
    result['numerical_error_not_rigorously_enclosed']=True
    result['finite_difference_error_separate_from_cut_tail']=True
    result['passed']=all(row['passed'] for row in result['checks'])
    json.dumps(result,allow_nan=False)
    return result
