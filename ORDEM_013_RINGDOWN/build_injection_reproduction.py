"""Create a raw off-source-to-forecast reproduction supplement, no v1 changes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
from fetch_public import atomic_json

ROOT = Path(__file__).resolve().parent


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        while block := stream.read(8 * 1024 * 1024):
            h.update(block)
    return h.hexdigest()


def main():
    target = ROOT / 'C7_INJECTION_REPRODUCTION'
    if target.exists():
        raise FileExistsError('Preserve existing supplement')
    target.mkdir()
    assets = []
    def copy(name, destination=None, asset=True):
        destination = destination or 'assets/ORDEM_013_RINGDOWN/' + name
        p = target / destination
        p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, p)
        if asset:
            assets.append(dict(path=destination, destination='ORDEM_013_RINGDOWN/' + name))
    names = ['fetch_public.py', 'tgl_ringdown_prediction.py', 'tgl_ringdown_likelihood.py',
        'diagnose_overtones.py', 'prepare_imr_controls.py', 'prepare_empirical_noise.py',
        'prepare_recolored_noise.py', 'forecast_recolored_imr.py', 'verify_recolored_forecast.py',
        'QNM_GRID.json', 'C5_EXTRA_QNMS.json', 'FISHER_INPUTS.json']
    for name in names:
        copy(name)
    curves = json.loads((ROOT / 'FISHER_INPUTS.json').read_bytes())['psds']
    for curve in curves:
        name = 'cache/psd/' + curve['filename']
        if sha(ROOT / name) != curve['sha256']:
            raise ValueError('PSD input changed')
        copy(name)
    external = []
    for path in sorted((ROOT / 'cache/gwosc/offsource').glob('*.hdf5.receipt.json')):
        receipt = json.loads(path.read_bytes())
        relative = 'cache/gwosc/offsource/' + path.name.removesuffix('.receipt.json')
        source = ROOT / relative
        if sha(source) != receipt['sha256'] or source.stat().st_size != receipt['bytes']:
            raise ValueError('Raw off-source input changed')
        copy(path.relative_to(ROOT).as_posix())
        external.append(dict(path=relative, bytes=receipt['bytes'], sha256=receipt['sha256'],
            url=receipt['url'], stages=['full'], attribution='GWOSC / LVK, CC BY 4.0'))
    if len(external) != 2:
        raise ValueError('Expected exactly the registered H1/L1 off-source pair')
    products = [
        ('C5_IMR_CONTROLS.json', ['parameters', 'families']),
        ('C5_EMPIRICAL_NOISE.json', ['detectors']),
        ('C5_RECOLORED_NOISE.json', ['scenarios']),
        ('C5_RECOLORED_FORECAST.json', ['number_of_cells', 'low_frequency_controls', 'results']),
        ('C5_RECOLORED_VALIDATION.json', ['independent_SVD_controls', 'continuous_profile_refinement', 'noise_only_prior_volume']),
    ]
    outputs = []
    for name, fields in products:
        data = json.loads((ROOT / name).read_bytes())
        if not set(fields) <= set(data):
            raise ValueError('Inspect output schema: ' + name)
        copy(name, 'reference/' + name, asset=False)
        outputs.append(dict(name=name, fields=fields))
    copy('package_reproduce_analysis.py', 'reproduce.py', asset=False)
    commands = [[name] for name in ['prepare_imr_controls.py', 'prepare_empirical_noise.py',
        'prepare_recolored_noise.py', 'forecast_recolored_imr.py', 'verify_recolored_forecast.py']]
    readme = '''# Raw off-source and IMR injection reproduction

This supplement generates both IMR waveform families anew, estimates H1/L1 noise
from the public pre-event strain, recolors its held-out intervals, recomputes all
4608 conditional forecast cells, and runs the independent SVD integral controls.
No saved forecast, noise NPZ, or IMR NPZ is used as a calculation input.
The QNM interpolation and extra-mode tables are supplied numerical inputs with
their method/cross-check provenance. They are not solved again in this command.

```sh
python reproduce.py full --download --imr-python /path/to/pycbc/environment/python
```

Instead of downloading, pass `--source-root /path/to/ORDEM_013_RINGDOWN` with
the two verified files under cache/gwosc/offsource. Only these manifest paths
are read. Each invocation gets a fresh output folder, and failed logs survive.
Approximately 257 MB of public off-source strain is required. The code rejects
files extending into the event window. Continuous-wave hardware injections
present in these off-source data are retained as documented by the noise report.

Test environments: main Python with NumPy 2.5.3, SciPy 1.18.1, h5py 3.16.0;
IMR Python with PyCBC 2.11.0 and LALSimulation 6.2.1. No install into a system
environment is needed. The driver compares scientific numerical subtrees and
decision counts/verdicts to the supplied reference; it does not compare new
NPZ container timestamps or machine-specific paths.

O5 is an A+ design scenario; ET and CE are also design curves. The same 50 paired
noise intervals recur across cells. Recovered mode amplitudes are free and the
true remnant is fixed. FULL_IMR and manufactured MATCHED_RINGDOWN are separate
tests. The whole 22/44 harmonics receive their respective fundamental's imposed
rate; this is a conditional injection convention, not a unique overtone law.

No joint group passed both waveform families and both injected hypotheses in
the reference experiment. A small positive lnB can be generated by prior volume;
the SVD noise-only controls quantify this. Reproduction does not remove these
limitations or convert a Bayes ratio to sigma. Frozen on-source C6 is untouched.
'''
    (target / 'README.md').write_bytes(readme.encode('utf-8'))
    files = [dict(path=p.relative_to(target).as_posix(), bytes=p.stat().st_size, sha256=sha(p))
        for p in sorted(target.rglob('*')) if p.is_file()]
    atomic_json(target / 'MANIFEST.json', dict(status='RAW_OFF_SOURCE_TO_FORECAST_REGENERATION',
        created_utc=datetime.now(timezone.utc).isoformat(), assets=assets, external_inputs=external,
        archives=[], stages={'full': dict(commands=commands, outputs=outputs)},
        shipped_files=files, generator_sha256=sha(Path(__file__))))
    print(json.dumps(dict(package=str(target), files=len(files), raw_external_inputs=len(external))))


if __name__ == '__main__':
    main()
