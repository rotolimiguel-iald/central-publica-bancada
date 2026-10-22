"""Independent PyCBC/LAL reference-PSD comparisons. Read-only libraries."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pycbc
import pycbc.psd
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def main():
    inputs=json.loads((ROOT/'FISHER_INPUTS.json').read_bytes())
    pairs={'O5':'aLIGOAPlusDesignSensitivityT1800042',
           'ET':'EinsteinTelescopeP1600143','CE':'CosmicExplorerP1600143'}
    results=[]
    for entry in inputs['psds']:
        key=entry['key']
        if key not in pairs:continue
        fun=getattr(pycbc.psd,pairs[key])
        curve=fun(length=8193,delta_f=.25,low_freq_cutoff=20.)
        f=np.arange(len(curve))*.25
        y=np.asarray(curve)
        raw=np.loadtxt(ROOT/'cache/psd'/entry['filename'])
        good=(raw[:,0]>0)&(raw[:,1]>0)&np.isfinite(raw[:,1])
        freq=f[80:]; test=y[80:]
        ref=np.exp(np.interp(np.log(freq),np.log(raw[good,0]),np.log(raw[good,1])))
        if entry['kind']=='ASD':ref=ref**2
        ratio=test/ref
        invalid=(~np.isfinite(ratio))|(ratio<=0)
        # LAL sets the Nyquist bin to zero. This is an FFT endpoint sentinel,
        # not a physical zero-noise value; all interior bins must stay positive.
        if np.any(invalid & (freq!=f[-1])):
            raise ValueError(('Invalid interior PSD control',key,freq[invalid].tolist()))
        excluded=freq[invalid].tolist()
        freq,ratio=freq[~invalid],ratio[~invalid]
        out=ROOT/'cache/psd'/(pairs[key]+'.npz')
        if out.exists():raise FileExistsError(out)
        np.savez(out,frequency=f,psd=y)
        results.append(dict(detector=key,function=pairs[key],pycbc_version=pycbc.__version__,
              ratio_definition='PyCBC PSD / Bilby file PSD',excluded_Nyquist_sentinel_hz=excluded,
              min=float(ratio.min()),max=float(ratio.max()),
              median=float(np.median(ratio)),ratios_at_hz={str(hz):float(np.interp(hz,freq,ratio)) for hz in [30,100,250,1000]},
              sampled_control_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
              reference_sha256=entry['sha256']))
    atomic_json(ROOT/'PSD_CONTROLS.json',dict(status='CONTROL_CURVES_COMPARED_NOT_ASSUMED_IDENTICAL',results=results))
    print(json.dumps(results),flush=True)

if __name__=='__main__':main()
