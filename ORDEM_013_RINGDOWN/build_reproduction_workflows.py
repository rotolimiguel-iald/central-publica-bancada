"""Build an additive posterior-regeneration supplement; preserve package v1."""
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
        while block := stream.read(8*1024*1024):
            h.update(block)
    return h.hexdigest()


def main():
    package = ROOT / 'C7_POSTERIOR_REPRODUCTION'
    if package.exists():
        raise FileExistsError('Keep prior package; build a new version after review')
    package.mkdir()
    assets = []
    def copy(source, destination):
        target = package / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    modules = ['fetch_public.py', 'tgl_ringdown_prediction.py', 'posterior_220_readout.py',
        'catalog_220_readout.py', 'joint_modes_posterior.py', 'free_clock_posterior.py', 'combine_catalog.py',
        'REGISTRO_C4.json', 'C4_SCHEMA.json', 'C4_CATALOG_SCHEMA.json', 'QNM_GRID.json']
    for name in modules:
        dest = 'assets/ORDEM_013_RINGDOWN/' + name
        copy(ROOT / name, dest)
        assets.append(dict(path=dest, destination='ORDEM_013_RINGDOWN/' + name))
    receipt = 'TUNEL/DO_CHATGPT/ENTREGA_013_C4a_REGISTRO_POSTERIORES.md'
    copy(ROOT.parent / receipt, 'assets/' + receipt)
    assets.append(dict(path='assets/' + receipt, destination=receipt))
    outputs = {
        'primary': [('C4_220_INITIAL.json', ['N', 'quantiles', 'rows'])],
        'joint': [('C4_JOINT_MODES.json', ['N', 'GR_HPD_controls', 'rows', 'independent_five_dimensional_KDE_quadrature'])],
        'free_clock': [('C4_FREE_CLOCK.json', ['N', 'rows'])],
        'catalog': [('C4_CATALOG_220.json', ['N_events', 'N_posterior_draws', 'rows', 'catalog']),
                    ('C4_CATALOG_COMBINATION.json', ['common_deformation_GR_diagnostics', 'catalog'])],
    }
    # Inspect exact output schemas before publishing the driver manifest.
    stages = {}
    commands = {'primary': [['posterior_220_readout.py']], 'joint': [['joint_modes_posterior.py']],
        'free_clock': [['free_clock_posterior.py']],
        'catalog': [['catalog_220_readout.py'], ['combine_catalog.py']]}
    for stage, products in outputs.items():
        rows = []
        for name, fields in products:
            value = json.loads((ROOT / name).read_bytes())
            missing = set(fields) - set(value)
            if missing:
                raise ValueError(f'Inspect output schema {name}; missing {missing}, actual {list(value)}')
            copy(ROOT / name, 'reference/' + name)
            rows.append(dict(name=name, fields=fields))
        stages[stage] = dict(commands=commands[stage], outputs=rows)
    external = []
    archives = []
    for record, key in [(17018009, 'TGR_companion_S250114ax_results.tar.gz'), (21454847, 'pSEOB.tar.gz')]:
        folder = ROOT / f'cache/public/{record}'
        info = json.loads((folder / (key + '.receipt.json')).read_bytes())
        archives.append(dict(id=str(record), record=record, filename=key, bytes=info['bytes'],
            sha256=info['sha256'], url=info['url'], attribution='LVK, CC BY 4.0', doi=info['doi']))
        extracted = json.loads((folder / 'extraction_receipt.json').read_bytes())
        for row in extracted['files']:
            member = row['member']
            selected = (member.endswith('gw250114_pseobnr/posterior_samples.h5') if record == 17018009 else
                (member.startswith('pSEOB/metafiles/') and member.endswith('.h5')) or member == 'pSEOB/pSEOBNR_main_figure.ipynb')
            if not selected:
                continue
            relative = f'cache/public/{record}/extracted/' + member
            p = ROOT / relative
            if not p.is_file() or sha(p) != row['sha256']:
                raise ValueError('Selected public source changed: ' + relative)
            external.append(dict(path=relative, bytes=p.stat().st_size, sha256=row['sha256'],
                archive=str(record), member=member, stages=['catalog'] if record == 21454847 else ['primary', 'joint', 'free_clock']))
    copy(ROOT / 'package_reproduce_analysis.py', 'reproduce.py')
    text = '''# Public-posterior regeneration supplement

This supplements the immutable independent package v1. It recalculates numerical
results from public posterior samples, not from the reference JSON outputs.
It does not rerun the LVK samplers or claim independent scientific confirmation.

Use Python with NumPy 2.5.3, SciPy 1.18.1 and h5py 3.16.0 (tested versions).
Each command creates a fresh directory under cache, copies only the declared
inputs, verifies hashes, executes the existing analysis scripts unchanged, and
compares all numerical leaves of the declared output subtrees with the reference.
Per-script logs and failed runs are preserved. Counts and verdicts must agree.

```sh
python reproduce.py primary --download
python reproduce.py joint --download
python reproduce.py free_clock --download
python reproduce.py catalog --download
```

Alternatively use `--archive-cache /path/to/public` containing RECORD/filename,
or `--source-root /path/to/ORDEM_013_RINGDOWN` for existing verified extracted
files. About 2.4 GB of source archives are needed for all stages. Files are
attributed to LVK under CC BY 4.0; URLs and member hashes are in MANIFEST.json.
The notebook is parsed only with AST literal_eval, never executed.

These are conditional ensemble/ringdown sector comparisons. The catalog counts
GW250114 once and must not be multiplied by the standalone or joint-mode result.
Older GWTC-3 reconciliation and injection regeneration are separate work; they
are not claimed complete by this supplement. Earlier per-stage JSON status
strings preserve their historical scope; later controls are separate evidence.
Bayes ratios are not sigma. No physical clock or unraveling is selected here.
'''
    target = package / 'README.md'
    target.write_bytes(text.encode('utf-8'))
    files = [dict(path=p.relative_to(package).as_posix(), bytes=p.stat().st_size, sha256=sha(p))
        for p in sorted(package.rglob('*')) if p.is_file()]
    atomic_json(package / 'MANIFEST.json', dict(status='POSTERIOR_REGENERATION_SUPPLEMENT',
        created_utc=datetime.now(timezone.utc).isoformat(), generator_sha256=sha(Path(__file__)),
        assets=assets, stages=stages, external_inputs=external, archives=archives, shipped_files=files))
    print(json.dumps(dict(package=str(package), files=len(files), external_inputs=len(external))))


if __name__ == '__main__':
    main()
