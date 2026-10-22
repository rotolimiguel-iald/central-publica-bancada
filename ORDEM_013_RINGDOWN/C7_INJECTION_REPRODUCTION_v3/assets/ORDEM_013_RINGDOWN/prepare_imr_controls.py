"""Public LAL/PyCBC IMR-family controls; no observed event strain is used."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import hashlib
import json
import numpy as np
import lal
import lalsimulation as lalsim
import pycbc
from pycbc.waveform import get_td_waveform
from lalinference.imrtgr import nrutils
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def main():
    out=ROOT/'cache'/'imr_controls';out.mkdir(exist_ok=True)
    pars=dict(mass1=39.,mass2=33.,spin1z=.05,spin2z=-.03,
        spin1x=0.,spin1y=0.,spin2x=0.,spin2y=0.,inclination=.6,
        coa_phase=.37,distance=403.,delta_t=1/4096,f_lower=20.,f_ref=20.)
    rows=[]
    for family in ('SEOBNRv4HM','IMRPhenomXPHM'):
        products={}
        for label,modes in [('all',None),('22',[(2,2)]),('44',[(4,4)])]:
            opts=dict(pars,approximant=family)
            if modes:opts['mode_array']=modes
            hp,hc=get_td_waveform(**opts)
            times=np.asarray(hp.sample_times)
            products[label]=(times,np.asarray(hp),np.asarray(hc))
            print(json.dumps(dict(family=family,component=label,N=len(hp),start=float(times[0]),end=float(times[-1]))),flush=True)
        peak_index=int(np.argmax(products['22'][1]**2+products['22'][2]**2))
        peak=float(products['22'][0][peak_index])
        # Fine interpolation only aligns outputs' existing reference epochs.
        time=np.arange(-.02,.251,1/4096)
        arrays={'time_from_peak_s':time}
        for name,(t,hp,hc) in products.items():
            if time[0]+peak<t[0] or time[-1]+peak>t[-1]:
                # A TD generator may terminate after the damped tail; zero there
                # is permitted only if its final amplitude is negligible.
                ratio=float(np.hypot(hp[-1],hc[-1])/np.max(np.hypot(hp,hc)))
                if time[0]+peak<t[0] or ratio>1e-5:
                    raise ValueError(f'Insufficient {family}/{name} tail: {ratio}')
            arrays[name+'_plus']=np.interp(time+peak,t,hp,left=np.nan,right=0.)
            arrays[name+'_cross']=np.interp(time+peak,t,hc,left=np.nan,right=0.)
        arrays['other_plus']=arrays['all_plus']-arrays['22_plus']-arrays['44_plus']
        arrays['other_cross']=arrays['all_cross']-arrays['22_cross']-arrays['44_cross']
        target=out/(family+'.npz')
        if target.exists():raise FileExistsError('Preserve existing IMR control')
        np.savez_compressed(target,**arrays)
        if family=='SEOBNRv4HM':
            code,mf_frac,chi=lalsim.SimIMREOBFinalMassSpin(pars['mass1'],pars['mass2'],
                [0.,0.,pars['spin1z']],[0.,0.,pars['spin2z']],lalsim.SEOBNRv4)
            if code!=0:raise ValueError('LAL EOB remnant fit failed')
            mf=(pars['mass1']+pars['mass2'])*mf_frac
            method='SimIMREOBFinalMassSpin SEOBNRv4'
        else:
            eta=pars['mass1']*pars['mass2']/(pars['mass1']+pars['mass2'])**2
            mf=(pars['mass1']+pars['mass2'])*lalsim.SimIMRPhenomXFinalMass2017(eta,pars['spin1z'],pars['spin2z'])
            chi=lalsim.SimIMRPhenomXFinalSpin2017(eta,pars['spin1z'],pars['spin2z'])
            method='SimIMRPhenomXFinalMass2017 / FinalSpin2017'
        rows.append(dict(family=family,path=str(target),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
            peak_22_reference_s=peak,remnant_mass_detector_solar=float(mf),remnant_spin=float(chi),
            remnant_method=method,
            UIB2016_mass_control=float(nrutils.bbh_final_mass_non_precessing_UIB2016(39.,33.,.05,-.03)),
            UIB2016_spin_control=float(nrutils.bbh_final_spin_non_precessing_UIB2016(39.,33.,.05,-.03))))
    atomic_json(ROOT/'C5_IMR_CONTROLS.json',dict(status='TWO_IMR_FAMILIES_GENERATED',
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        parameters=pars,pycbc_version=pycbc.__version__,lalsimulation_version=lalsim.__version__,
        peak_definition='Maximum of isolated 22 polarization amplitude; common generator epoch retained for all components',
        scope='Aligned-spin representative source, not a sample from the observed event; XPHM retains its aligned-spin limit',families=rows))

if __name__=='__main__':main()
