"""Inspect computed products, adversarial guards and exact release ZIP bytes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import shutil
import tempfile
import zipfile
from fetch_public import atomic_json

ROOT = Path(__file__).resolve().parent


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        while block := stream.read(8 * 1024 * 1024):
            h.update(block)
    return h.hexdigest()


def main():
    destination = ROOT / 'C7_GWTC3_REPRODUCTION_VALIDATION.json'
    if destination.exists():
        raise FileExistsError('Preserve previous validation')
    name = 'C7_GWTC3_REPRODUCTION'
    package = ROOT / name
    manifest = json.loads((package / 'MANIFEST.json').read_bytes())
    spec = importlib.util.spec_from_file_location('gwtc3_driver_review', package / 'reproduce.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for row in manifest['shipped_files']:
        module.verify(module.checked(package, row['path']), row)
    candidates = sorted((package / 'cache').glob('run_full_*/RESULT.json'))
    if len(candidates) != 1:
        raise ValueError('Expected exactly one completed documented replay')
    receipt_path = candidates[0]
    receipt = json.loads(receipt_path.read_bytes())
    if receipt['status'] != 'PASS' or receipt['manifest_sha256'] != sha(package / 'MANIFEST.json'):
        raise ValueError('Invalid or stale replay receipt')
    if receipt['reference_results_copied_as_inputs'] or receipt['external_inputs'] != 18:
        raise ValueError('Unexpected input scope')
    run = receipt_path.parent / 'ORDEM_013_RINGDOWN'
    rechecked = []
    for output in manifest['stages']['full']['outputs']:
        actual = json.loads((run / output['name']).read_bytes())
        expected = json.loads((package / 'reference' / output['name']).read_bytes())
        check = next(x for x in receipt['comparisons'] if x['output'] == output['name'])
        if sha(run / output['name']) != check['output_sha256']:
            raise ValueError('Computed product changed since replay')
        errors = []
        for key in output['fields']:
            module.numeric_comparison(actual[key], expected[key], key, errors)
        rechecked.append(dict(output=output['name'], numerical_leaves=len(errors),
            max_absolute_difference=max((v for _, v in errors), default=0)))
    selection = json.loads((run / 'C4_GWTC3_SELECTION.json').read_bytes())
    combination = json.loads((run / 'C4_GWTC3_PUBLISHED_COMBINATION.json').read_bytes())
    if set(selection['selected_events']) != set(combination['selected_events']) or combination['N_events'] != 10:
        raise ValueError('Selection not used by calculation')
    temporary = Path(tempfile.mkdtemp(prefix='gwtc3_guard_', dir=ROOT / 'cache'))
    sample = manifest['shipped_files'][0]
    path = temporary / 'sample'
    shutil.copyfile(package / sample['path'], path)
    module.verify(path, sample)
    content = bytearray(path.read_bytes())
    content[len(content)//2] ^= 1
    path.write_bytes(content)
    refused = []
    cases = [('mutated_file', lambda: module.verify(path, sample))]
    for unsafe in ('../escape', '/absolute', 'bad\\path'):
        cases.append(('path:' + unsafe, lambda p=unsafe: module.checked(temporary, p)))
    cases += [
        ('changed_event_identity', lambda: module.numeric_comparison(['GWdifferent'], ['GW150914_095045'], 'selected_events')),
        ('changed_verdict', lambda: module.numeric_comparison('NOT_EXCLUDED', 'INCONCLUSIVE_SYSTEMATICS', 'verdict')),
        ('changed_count', lambda: module.numeric_comparison(11, 10, 'N_events')),
        ('changed_measurement', lambda: module.numeric_comparison(1.1, 1., 'lnB')),
    ]
    for label, action in cases:
        try:
            action()
        except ValueError:
            refused.append(label)
        else:
            raise ValueError('Adversarial input accepted: ' + label)
    archive = ROOT / 'cache' / (name + '_v1.zip')
    if archive.exists():
        raise FileExistsError('Preserve earlier archive')
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as handle:
        for row in manifest['shipped_files']:
            handle.write(package / row['path'], name + '/' + row['path'])
        handle.write(package / 'MANIFEST.json', name + '/MANIFEST.json')
        handle.write(receipt_path, name + '/replay_receipts/full.json')
    with zipfile.ZipFile(archive) as handle:
        if handle.testzip() is not None:
            raise ValueError('Distribution ZIP CRC failure')
        for row in manifest['shipped_files']:
            if hashlib.sha256(handle.read(name + '/' + row['path'])).hexdigest() != row['sha256']:
                raise ValueError('Changed distribution member')
        members = len(handle.namelist())
    result = dict(status='PASS', date_utc=datetime.now(timezone.utc).isoformat(),
        package=name, archive=archive.relative_to(ROOT).as_posix(), bytes=archive.stat().st_size,
        sha256=sha(archive), members=members, manifest_sha256=sha(package / 'MANIFEST.json'),
        replay_receipt=receipt_path.relative_to(ROOT).as_posix(), replay_sha256=sha(receipt_path),
        scientific_comparisons=rechecked, adversarial_refusals=refused,
        published_selection_count=combination['N_events'],
        fresh_archive_extraction=True, public_download_repeated=False,
        scope='Recalculation from pinned public ZIP, no original LVK inference rerun; newer-catalog output only identity/comparison input',
        source_sha256=sha(Path(__file__)))
    atomic_json(destination, result)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
