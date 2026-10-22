"""Build the additive GWTC-3 reproduction; preserve all earlier packages."""
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
    package = ROOT / 'C7_GWTC3_REPRODUCTION'
    if package.exists():
        raise FileExistsError('Preserve existing package')
    package.mkdir()
    assets = []

    def copy(source, destination):
        target = package / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)

    names = ['fetch_public.py', 'tgl_ringdown_prediction.py', 'posterior_220_readout.py',
             'catalog_220_readout.py', 'combine_catalog.py', 'gwtc3_posterior_readout.py',
             'read_gwtc3_selection.py', 'combine_gwtc3.py', 'REGISTRO_C4.json',
             'QNM_GRID.json', 'C4_GWTC3_SCHEMA.json', 'C4_GWTC3_PAPER_RECEIPT.json',
             'C4_CATALOG_220.json', 'cache/literature/gwtc3_article_v3.html']
    for name in names:
        dest = 'assets/ORDEM_013_RINGDOWN/' + name
        copy(ROOT / name, dest)
        assets.append(dict(path=dest, destination='ORDEM_013_RINGDOWN/' + name))
    receipt = 'TUNEL/DO_CHATGPT/ENTREGA_013_C4a_REGISTRO_POSTERIORES.md'
    copy(ROOT.parent / receipt, 'assets/' + receipt)
    assets.append(dict(path='assets/' + receipt, destination=receipt))
    products = {
        'C4_GWTC3_220.json': ['N_events', 'rows', 'catalog', 'duplicate_reconciliation'],
        'C4_GWTC3_SELECTION.json': ['table_events', 'excluded_by_authors', 'selected_events',
                                   'archive_products_outside_table'],
        'C4_GWTC3_PUBLISHED_COMBINATION.json': ['N_events', 'selected_events',
                                               'common_deformation_GR_diagnostics', 'catalog'],
    }
    outputs = []
    for name, fields in products.items():
        value = json.loads((ROOT / name).read_bytes())
        if set(fields) - set(value):
            raise ValueError('Uninspected output schema: ' + name)
        copy(ROOT / name, 'reference/' + name)
        outputs.append(dict(name=name, fields=fields))
    for name in ['C4_GWTC3_CONVENTIONS.json', 'C4_GWTC3_SOURCE_DOCS.json',
                 'C7_GWTC3_EVENT_READINGS.csv', 'C4_GWTC3_COMBINATION.json',
                 'combine_gwtc3.py.bak_ALL18_ONLY']:
        copy(ROOT / name, 'evidence/' + name)
    key = 'IGWN-GWTC3-TGR-v2-rin.zip'
    folder = ROOT / 'cache/public/17461225'
    info = json.loads((folder / (key + '.receipt.json')).read_bytes())
    if sha(folder / key) != info['sha256']:
        raise ValueError('Original public archive changed')
    extracted = json.loads((folder / 'extraction_receipt.json').read_bytes())
    external = []
    for row in extracted['files']:
        path = ROOT / row['path']
        if sha(path) != row['sha256'] or path.stat().st_size != row['bytes']:
            raise ValueError('Public member changed: ' + row['path'])
        external.append(dict(path=row['path'], bytes=row['bytes'], sha256=row['sha256'],
                             archive='17461225', member=row['member'], stages=['full']))
    if len(external) != 18:
        raise ValueError('Unexpected extracted posterior count')
    archive = dict(id='17461225', record=17461225, filename=key, format='zip',
                   bytes=info['bytes'], sha256=info['sha256'], url=info['url'],
                   doi=info['doi'], attribution='LVK, CC BY 4.0')
    copy(ROOT / 'package_reproduce_gwtc3.py', 'reproduce.py')
    readme = '''# GWTC-3 posterior and published-selection reproduction

This additive supplement recalculates all 18 released pSEOB posterior readouts,
extracts Table 13 and the two explicit author exclusions from the archived
primary article, and recomputes the separate ten-event combination. It never
multiplies a GWTC-3 likelihood by an overlapping newer-catalog likelihood.

```sh
python reproduce.py full --download
python reproduce.py full --archive-cache /path/to/public
```

The second command expects `17461225/IGWN-GWTC3-TGR-v2-rin.zip`. Alternatively,
`--source-root /path/to/ORDEM_013_RINGDOWN` uses verified extracted members.
Dependencies: NumPy, SciPy, h5py and LAL (UTC/GPS conversion). Tested versions
are recorded in the replay receipt. The archive is about 2.21 GB; the 18 inputs
about 1.23 GB. Provide additional free space for the fresh working directory.
All public files are attributed to LVK, CC BY 4.0; DOI, URLs and hashes are in
MANIFEST.json. The archived article is only read, never executed.

Each run verifies shipped files and public inputs, streams only declared ZIP
members to checked destinations, checks their CRC and SHA-256, then executes
the unchanged analysis scripts. It compares all numerical leaves and all
strings (including event identities and verdicts) in declared result subtrees.
Numerical tolerances are relative 2e-7 and absolute 1e-10; counts are exact.
Logs and failed runs are preserved. Reference target outputs are not inputs.

One explicit comparison input is `C4_CATALOG_220.json`: its event names identify
overlap by GPS, and its old-versus-new numbers populate a comparison column.
Its posterior likelihoods are never included in the GWTC-3 calculation. The
newer-catalog file itself can be regenerated with C7_POSTERIOR_REPRODUCTION.

The historical all-18 control is included under evidence, distinct from the
published ten-event selection. The former is not represented as the paper's
joint result; neither is pooled with the current release. Original executable
versions and remnant-postprocessing provenance are unavailable in the legacy
HDF5. Ratios are conditional on the inspected uniform-prior convention and
matched nuisance priors. The publication selection was audited nonblindly.

The conclusion is INCONCLUSIVE_SYSTEMATICS, not a physical confirmation or a
frequentist sigma. No clock, partition or physical unraveling is selected.
The primary newer catalog remains the preferred analysis on overlapping data.
This supplement does not rerun LVK parameter estimation or independently
validate its waveform or calibration assumptions.
'''
    (package / 'README.md').write_bytes(readme.encode('utf-8'))
    files = [dict(path=p.relative_to(package).as_posix(), bytes=p.stat().st_size, sha256=sha(p))
             for p in sorted(package.rglob('*')) if p.is_file()]
    atomic_json(package / 'MANIFEST.json', dict(status='GWTC3_REGENERATION_SUPPLEMENT',
        created_utc=datetime.now(timezone.utc).isoformat(), generator_sha256=sha(Path(__file__)),
        assets=assets, external_inputs=external, archives=[archive], shipped_files=files,
        comparison_inputs=[dict(path='C4_CATALOG_220.json',
            role='GPS identity and comparison column only; not a GWTC-3 likelihood input')],
        stages=dict(full=dict(commands=[['gwtc3_posterior_readout.py'],
              ['read_gwtc3_selection.py'], ['combine_gwtc3.py']], outputs=outputs))))
    print(json.dumps(dict(package=str(package), files=len(files), external_inputs=len(external))))


if __name__ == '__main__':
    main()
