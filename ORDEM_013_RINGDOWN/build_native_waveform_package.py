"""Standalone native SEOB conditional waveform supplement, without task state."""
from pathlib import Path
from datetime import datetime,timezone
import ast
import hashlib
import json
import zipfile

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'cache/source_evidence'
PACKAGE=ROOT/'C7_NATIVE_SEOB_WAVEFORM'


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


API='''"""Conditional ensemble ringdown: complete SEOB41 waveform, modified22/44.

No clock/readout is selected implicitly. All input masses are detector-frame.
Distance and polarization are physical common network parameters, never
independent fitted amplitudes per harmonic or detector.
"""
import math
import numpy as np
import native_seob_phase_source as native
import stable_peak_imr_model as model


def prepare_ringdown(coordinates,times,*,sample_rate=8192):
    """Coordinates: log(Mtot/Msun),log(q),chi1z,chi2z,iota,phase,t0_ms.

    times are seconds relative to the intrinsic phase-zero complex22 peak.
    The entire trial interval must be after that peak. No normalization to a
    chosen SNR is performed. This function retains the unchanged other modes.
    """
    x=np.asarray(coordinates,dtype=float)
    t=np.asarray(times,dtype=float)
    if t.ndim!=1 or len(t)<2 or not np.all(np.isfinite(t)) or np.any(np.diff(t)<=0):
        raise ValueError('Expected a finite, strictly increasing time grid')
    if not math.isfinite(sample_rate) or sample_rate<=0:
        raise ValueError('Positive finite generator rate required')
    raw=native.raw_phase_samples('SEOBNRv4HM',x,t,sample_rate=sample_rate)
    raw['coefficients']=np.fft.fft(raw['samples'],axis=0)/raw['n']
    raw['orders']=np.fft.fftfreq(raw['n'])*raw['n']
    return raw


def polarizations(prepared,*,reading,strength,distance_mpc,polarization_rad=0.,phase=None,redshift=0.):
    """Return h_plus,h_cross as dimensionless strain and conditional metadata.

    This is the effective ENSEMBLE envelope of the whole22/44 harmonics, not
    a unique stochastic trajectory or a quantization of Kerr quasinormal modes.
    A coherent-state initial slope is not treated as an exact exponential.
    """
    if reading=='R-RAIZ-COHERENT':
        raise ValueError('An initial coherent-state slope is not a full exponential waveform')
    if not math.isfinite(strength) or strength<0:
        raise ValueError('Nonnegative finite physical dephasing strength required')
    if not math.isfinite(distance_mpc) or distance_mpc<=0 or not math.isfinite(polarization_rad):
        raise ValueError('Positive finite distance and finite polarization required')
    phase=float(prepared['coordinates'][5] if phase is None else phase)
    if not math.isfinite(phase):
        raise ValueError('Finite orbital phase required')
    c=prepared['coefficients']; orders=prepared['orders']
    value=np.einsum('k,kjpt->jpt',np.exp(1j*phase*orders),c,optimize=True)
    if np.max(np.abs(value.imag))>1e-10*max(1.,np.max(np.abs(value.real))):
        raise ValueError('Nonreal finite-mode reconstruction')
    parts=value.real; h=parts[0].copy(); predictions=[]
    for j,ell in enumerate((2,4)):
        spin=prepared['remnant_spin']; spline=model.qnm_splines()[ell]
        if not spline.x[0]<=spin<=spline.x[-1]:
            raise ValueError('Remnant outside the supplied QNM grid')
        p=model.prediction(prepared['remnant_mass'],spin,reading,mode=(ell,ell,0),
                           qnm_dimensionless=complex(spline(spin)),redshift=redshift)
        h+=np.expm1(-strength*p['gamma_per_s']*prepared['times'])[None,:]*parts[j+1]
        predictions.append(p)
    cp,sp=math.cos(2*polarization_rad),math.sin(2*polarization_rad)
    # Matches common-network coefficients (cos2psi,sin2psi) in the reference API.
    hp,hc=cp*h[0]-sp*h[1],sp*h[0]+cp*h[1]
    amplitude=403./distance_mpc*1e-21
    return amplitude*hp,amplitude*hc,dict(family='SEOBNRv4HM',reading=reading,strength=strength,
        predictions=predictions,distance_mpc=distance_mpc,polarization_rad=polarization_rad,
        remnant_mass=prepared['remnant_mass'],remnant_spin=prepared['remnant_spin'],
        peak_generator_s=prepared['peak_generator_s'],native_dynamics=prepared['native_dynamics'],
        physical_clock_selected=False,scope='CONDITIONAL_WHOLE_HARMONIC_ENSEMBLE_ENVELOPE_NOT_CONFIRMED_PHYSICS')
'''


RUNNER='''"""Replay the portable generator against full PyCBC polarizations."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'MANIFEST.json').read_bytes())
for row in manifest['files']:
    if hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()!=row['sha256']:
        raise ValueError('Package integrity failed:'+row['path'])
sys.path.insert(0,str(ROOT))
import numpy as np
import lalsimulation as ls
import tgl_native_ringdown as api
import stable_peak_imr_model as reference

inputs=json.loads((ROOT/'VALIDATION_INPUTS.json').read_bytes())
if ls.SimulationVCSInfo.vcsId!=inputs['lal_commit']:
    raise ValueError('Reproduction uses a different LAL source commit; validate explicitly before accepting')
rows=[]
for source in inputs['sources']:
    x=np.array([np.log(source['mass']),np.log(source['q']),source['s1'],source['s2'],source['inclination'],source['phase'],.6])
    times=np.arange(410)/2048+.0034
    for rate in (8192,16384):
        prepared=api.prepare_ringdown(x,times,sample_rate=rate)
        for reading in ('R-B','R-RAIZ-0','R-LIN','R-MOD'):
            for strength in (0.,.37,1.):
                rp,rc,meta=reference.polarizations('SEOBNRv4HM',x,times,reading,strength,rate)
                for distance,psi in ((403.,0.),(650.,.31)):
                    hp,hc,out=api.polarizations(prepared,reading=reading,strength=strength,distance_mpc=distance,polarization_rad=psi)
                    cp,sp=np.cos(2*psi),np.sin(2*psi)
                    expected=np.array([cp*rp-sp*rc,sp*rp+cp*rc])*403./distance*1e-21
                    actual=np.array([hp,hc])
                    error=float(np.linalg.norm(actual-expected)/np.linalg.norm(expected))
                    rows.append(dict(source=source['name'],rate=rate,reading=reading,strength=strength,
                        distance=distance,psi=psi,relative_error=error,passes=bool(error<=1e-6)))
        reference.source_curves.cache_clear()
        print(json.dumps(dict(source=source['name'],rate=rate,done=True)),flush=True)
guards=[]
bad=[dict(strength=-1.),dict(distance_mpc=0.),dict(distance_mpc=float('nan')),
     dict(reading='R-RAIZ-COHERENT'),dict(reading='unknown'),dict(phase=float('nan'))]
for change in bad:
    args=dict(reading='R-B',strength=1.,distance_mpc=403.);args.update(change)
    try:
        api.polarizations(prepared,**args)
    except ValueError:
        guards.append(True)
    else:
        guards.append(False)
out=dict(status='PASS_PORTABLE_NATIVE_WAVEFORM' if all(r['passes'] for r in rows) and all(guards) else 'FAIL_PORTABLE_NATIVE_WAVEFORM',
         count=len(rows),max_relative_error=max(r['relative_error'] for r in rows),guards=guards,rows=rows,
         scientific_acceptance=False,lal_commit=ls.SimulationVCSInfo.vcsId,
         scope='Numerical waveform/phase/distance/polarization equivalence, not posterior calibration or physical confirmation')
run=ROOT/'cache'/('replay_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'));run.mkdir(parents=True)
raw=(json.dumps(out,indent=2)+'\\n').encode();p=run/'RESULT.json';temp=p.with_suffix('.tmp');temp.write_bytes(raw)
if temp.stat().st_size!=len(raw):raise ValueError('Short result write')
temp.replace(p)
print(json.dumps({k:v for k,v in out.items() if k!='rows'},ensure_ascii=False),flush=True)
print(json.dumps(dict(result=str(p))),flush=True)
if out['status']!='PASS_PORTABLE_NATIVE_WAVEFORM':raise ValueError('Portable waveform check failed')
'''


def main():
    if PACKAGE.exists():raise FileExistsError('Create-once package')
    validation=json.loads((SOURCE/'native_source_integral_validation/RESULT.json').read_bytes())
    if validation['status']!='PASS_NATIVE_SOURCE_INTEGRAL':raise ValueError('Unvalidated native integral')
    for name in ('native_source_integral_validation','native_seob_phase_validation'):
        reg=json.loads((SOURCE/name/'REGISTRATION.json').read_bytes())
        for p,h in reg['hashes'].items():
            if sha(SOURCE/p)!=h:raise ValueError('Validated source changed:'+p)
    PACKAGE.mkdir()
    copies=['native_seob_phase_source.py','stable_peak_imr_model.py','tgl_ringdown_prediction.py','QNM_GRID.json']
    provenance=[]
    for name in copies:
        (PACKAGE/name).write_bytes((SOURCE/name).read_bytes())
        provenance.append(dict(path=name,mode='BYTE_IDENTICAL_COPY',source_sha256=sha(SOURCE/name)))
    code=(SOURCE/'direct_seob_modes.py').read_text(encoding='utf-8'); tree=ast.parse(code)
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('direct_modes','sum_modes')]
    assert len(nodes)==2
    extracted='"""Verbatim native-mode helpers; task-only validator omitted."""\nimport lal\nimport lalsimulation as ls\nimport numpy as np\nfrom pycbc import pnutils\n\n'+'\n\n'.join(ast.get_source_segment(code,n) for n in nodes)+'\n'
    actual=ast.parse(extracted)
    for n in nodes:
        counterpart=next(v for v in actual.body if isinstance(v,ast.FunctionDef) and v.name==n.name)
        if ast.dump(n,include_attributes=False)!=ast.dump(counterpart,include_attributes=False):
            raise ValueError('Native helper semantics changed during extraction')
    (PACKAGE/'direct_seob_modes.py').write_bytes(extracted.encode())
    provenance.append(dict(path='direct_seob_modes.py',mode='VERBATIM_FUNCTION_BODIES_AST_VERIFIED',
                          source_sha256=sha(SOURCE/'direct_seob_modes.py'),functions=[n.name for n in nodes]))
    native=json.loads((SOURCE/'DIRECT_SEOB_MODES_CORRECTED_VALIDATION.json').read_bytes())
    original=json.loads((SOURCE/'REGISTRATION.json').read_bytes())
    inputs=dict(lal_commit=native['lal_commit'],sources=original['sources'])
    (PACKAGE/'VALIDATION_INPUTS.json').write_bytes((json.dumps(inputs,indent=2)+'\n').encode())
    (PACKAGE/'PROVENANCE.json').write_bytes((json.dumps(dict(files=provenance,source_integral_validation_sha256=sha(SOURCE/'native_source_integral_validation/RESULT.json')),indent=2)+'\n').encode())
    (PACKAGE/'tgl_native_ringdown.py').write_bytes(API.encode())
    (PACKAGE/'reproduce.py').write_bytes(RUNNER.encode())
    text='''# Native SEOB conditional ringdown waveform

TGL: Luiz Antonio Rotoli Miguel. External GR generator: LALSuite/PyCBC.
Research supplement; no event significance or calibrated source evidence claimed.

## Model and limits

The generator retains the complete SEOBNRv4HM (SEOB41) mode set: positive
22,21,33,44,55 and the corresponding negative-m partners. For a supplied
conditional reading L and nonnegative strength a,

    h_a = h_all + (exp(-a Gamma_220 t)-1) h_22
                  + (exp(-a Gamma_440 t)-1) h_44.

The rates are calculated from the supplied prediction module using runtime
beta=ALPHA_FINE_CODATA_2018*sqrt(e), family-specific remnant and supplied exact
Kerr QNM interpolation grid. This is an effective whole-harmonic ENSEMBLE
envelope. It is not a derivation of a unique classical realization, a unique
overtone prescription or the physical modular partition/clock. A coherent-state
initial-slope prediction is explicitly rejected as a full exponential waveform.
The R-B mass clock, R-RAIZ-0 positive oscillator, R-LIN bridge and R-MOD restricted
corotating clock retain their respective INPUT/CONJECTURE scopes in metadata.
No default reading is selected and no physical rate is fitted here.

The peak is the phase-zero face-on intrinsic complex22 amplitude maximum.
Projection into inclination and orbital phase happens after constructing the
native modes. All other harmonics remain unchanged. Distance/polarization are
shared physical factors for the complete signal; there is no per-mode fitting.

## Use

With Python3.12, PyCBC2.11.0, LALSimulation6.2.1, NumPy2.3.5 and SciPy1.16.3:

```python
import numpy as np
from tgl_native_ringdown import prepare_ringdown, polarizations

# Detector-frame binary mass, mass ratio, aligned spins, inclination,
# orbital phase and peak displacement in milliseconds.
x = [np.log(90.), np.log(2.), .25, -.15, .9, 1.2, 0.]
times = .0034 + np.arange(410)/2048.
prepared = prepare_ringdown(x, times, sample_rate=8192)
hp, hc, metadata = polarizations(prepared, reading='R-B', strength=1.,
                                 distance_mpc=403., polarization_rad=.45)
```

hp,hc are dimensionless strain at the common luminosity distance in Mpc.
times are seconds after the specified intrinsic peak; the entire shifted
interval must be after it. Detector strain is F_plus*hp+F_cross*hc with whatever
sky response and time delay the consumer has explicitly supplied. The consumer
must provide its own likelihood, priors, detector noise and inference checks.
`prepared` may be reused across strengths/readings/orbital phases; it is only
a numerical representation, not a prior or a posterior.

## Reproduction and numerical scope

Run `python -B reproduce.py`. It verifies all packaged hashes and the LAL commit,
regenerates three sources at8192/16384Hz, compares four conditional readings,
three strengths and two distance/polarization choices against complete PyCBC
waveforms, then exercises six rejection cases. It writes a fresh cache directory.
It needs no original workspace, private file, task memory, network access,
canonical um.py or event strain. No dependencies are installed by the runner.

Selected-source high-resolution tests in the parent study still exceed the
registered log-likelihood tolerance at SNR200/600, even after actual internal-mesh
refinement. Output sample rate is not automatically internal solver resolution.
This package exposes the measured internal step in metadata and does not claim
high-SNR convergence or calibrated five-sigma sensitivity. Source-integrated
statistical precision, independent repeats and posterior coverage remain open.

The original failed mode reconstruction and corrected provenance remain in
the parent research records. Native helper bodies were copied verbatim and
AST-checked; task-only validation imports were removed. Bundled model files
are byte-identical copies, identified by the included provenance manifest.
LALSuite/PyCBC are external dependencies; their code is not bundled here.
'''
    (PACKAGE/'README.md').write_bytes(text.encode())
    files=[dict(path=p.relative_to(PACKAGE).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(PACKAGE.iterdir()) if p.is_file()]
    manifest=dict(status='FROZEN_NATIVE_WAVEFORM_PACKAGE',date_utc=datetime.now(timezone.utc).isoformat(),files=files)
    (PACKAGE/'MANIFEST.json').write_bytes((json.dumps(manifest,indent=2)+'\n').encode())
    archive=ROOT/'cache/C7_NATIVE_SEOB_WAVEFORM_v1.zip'
    if archive.exists():raise FileExistsError(archive)
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(PACKAGE.iterdir()):
            if p.is_file():z.write(p,p.name)
    receipt=dict(status='PACKAGED_REPLAY_PENDING',package=PACKAGE.name,files=len(files),archive=str(archive.relative_to(ROOT)).replace('\\','/'),
                 bytes=archive.stat().st_size,sha256=sha(archive),manifest_sha256=sha(PACKAGE/'MANIFEST.json'))
    target=ROOT/'C7_NATIVE_SEOB_WAVEFORM_PACKAGE.json'
    if target.exists():raise FileExistsError(target)
    target.write_bytes((json.dumps(receipt,indent=2)+'\n').encode()); print(json.dumps(receipt))


if __name__=='__main__': main()
