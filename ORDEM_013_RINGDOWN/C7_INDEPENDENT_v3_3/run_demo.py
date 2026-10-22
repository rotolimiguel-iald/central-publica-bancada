"""Portable NumPy-only waveform example; writes only when --output is supplied."""
import argparse
from pathlib import Path
import json
import numpy as np
from tgl_ringdown_prediction import prediction,beta_tgl
from tgl_ringdown_template import ringdown
from tgl_ringdown_unravelings import conditional_ringdown

ROOT=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',action='store_true');args=parser.parse_args()
    reference=json.loads((ROOT/'tables/reference_QNM.json').read_bytes())
    exact=complex(reference['omega_real'],reference['omega_imag'])
    kwargs=dict(mass_detector_solar=68.1,spin=.68,strain_amplitude=1e-21,
        qnm_dimensionless=exact,inclination=.6,t_start=.001,phase=.37,deformation=1.)
    times=np.arange(512)/4096.
    gr=ringdown(times,reading='R-GLOBAL',**kwargs)
    dephased=ringdown(times,reading='R-B',**kwargs)
    cauchy=conditional_ringdown(times,reading='R-LIN',observable='cauchy_phase',seed=13013,**kwargs)
    root=conditional_ringdown(times,reading='R-RAIZ-COHERENT',occupation=64.,observable='ensemble',**kwargs)
    predictions=[prediction(68.1,.68,r,qnm_dimensionless=exact) for r in
        ('R-A','R-B','R-RAIZ-0','R-RAIZ-EP4','R-RAIZ-REST','R-LIN','R-MOD','R-GLOBAL')]
    rb=next(p for p in predictions if p['reading']=='R-B')
    if not 0<rb['gamma_over_omega']<.01:raise ValueError('Reference scale unexpectedly changed')
    if np.array_equal(gr['plus'],dephased['plus']):raise ValueError('Deformation does not affect waveform')
    output=dict(beta_runtime=beta_tgl(),reference=reference,
        predictions=predictions,
        relative_R_B_waveform_change=float(np.linalg.norm(dephased['plus']-gr['plus'])/np.linalg.norm(gr['plus'])),
        scope='Illustrative reference source; no fit or physical confirmation',numpy_version=np.__version__)
    if args.output:
        folder=ROOT/'demo_output';folder.mkdir(exist_ok=True)
        target=folder/'predictions.json';temp=folder/'predictions.json.tmp'
        temp.write_bytes(json.dumps(output,indent=2).encode());temp.replace(target)
        waves=np.column_stack([times,gr['plus'],dephased['plus'],cauchy['plus'],root['plus']])
        np.savetxt(folder/'waveforms.csv',waves,delimiter=',',header='time_s,GR_plus,R_B_mean_plus,R_LIN_Cauchy_plus,root_N64_mean_plus',comments='')
    print(json.dumps(output,indent=2))

if __name__=='__main__':main()
