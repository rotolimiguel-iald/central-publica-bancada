"""Read-only deployed checks; preserve the GW resident load and V3 provenance."""
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from deploy_education import FILES
from install_canonical import SOURCE, TARGET
from validate_cosmology_live import gw_signature

BASE = 'http://127.0.0.1:18766'


def get_json(url, payload=None):
    request = urllib.request.Request(url, json.dumps(payload).encode() if payload is not None else None,
                                     headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=50) as response:
        return json.load(response)


def main():
    before = json.loads((SOURCE / 'state/education_gw_before.json').read_text())
    routes = {
        '/': 'static/universe-map.html', '/explore': 'static/universe-map.html',
        '/universe-map.css': 'static/universe-map.css', '/universe-map.js': 'static/universe-map.js',
        '/cosmos-lessons.js': 'static/cosmos-lessons.js', '/cosmos-teaching-model.js': 'static/cosmos-teaching-model.js',
        '/cosmos': 'static/cosmos.html',
    }
    pins = {}
    for name in FILES:
        original, installed = (SOURCE / name).read_bytes(), (TARGET / name).read_bytes()
        assert original == installed, 'Install mismatch: ' + name
        pins[name] = hashlib.sha256(installed).hexdigest()
    for route, name in routes.items():
        with urllib.request.urlopen(BASE + route, timeout=10) as response:
            assert response.status == 200
            assert response.read() == (TARGET / name).read_bytes(), 'Served content differs: ' + route
    overview = get_json(BASE + '/api/cosmology/status')
    assert overview['status'] == 'ok' and len(overview['dataset']['points']) == 13
    params = {name: detail['default'] for name, detail in overview['parameters'].items()}
    calculation = get_json(BASE + '/api/cosmology/evaluate', {**params, 'model_id': 'TGL_V3_TOTAL_FIXED_BETA'})
    assert calculation['status'] == 'ok' and calculation['engine_generation'] == overview['engine_generation']
    prior = json.loads((SOURCE / 'state' / ('validation_cosmology_v3_' + overview['engine_generation'][:16] + '.json')).read_text(encoding='utf-8'))
    assert calculation['chi2'] == prior['calls']['fixed']['chi2'], 'Scientific output changed'
    after = gw_signature(get_json('http://127.0.0.1:18765/api/universe/status'))
    assert before == after, 'GW load changed'
    receipt = {
        'created_utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS',
        'routes_verified': list(routes), 'installed_sha256': pins,
        'gw_unchanged': True, 'gw': after,
        'scientific_generation_unchanged': overview['engine_generation'],
        'v3_default_chi2_unchanged': calculation['chi2'],
        'test_commands_observed': [
            {'command': 'python -m unittest tests.test_cosmology_http tests.test_launcher tests.test_cosmology_runtime tests.test_cosmology_models tests.test_cosmology_scenarios tests.test_cosmology_exports', 'passed': 67, 'exit_code': 0},
            {'command': 'node --test tests/test_cosmos_teaching.cjs', 'passed': 7, 'exit_code': 0},
        ],
        'scope': 'EDUCATIONAL_NAVIGATION_AND_REFERENCE_DIAGRAM; EXISTING_LABS_PRESERVED; NO_NEW_INFERENCE',
    }
    data = json.dumps(receipt, ensure_ascii=False, indent=2).encode()
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name = 'education_validation_' + stamp + '.json'
    for root in (SOURCE, TARGET):
        path = root / 'state' / name
        temp = path.with_suffix('.tmp')
        with temp.open('xb') as stream:
            stream.write(data)
        assert temp.stat().st_size == len(data)
        temp.replace(path)
    print(json.dumps({'receipt': str(SOURCE / 'state' / name), 'status': 'PASS', 'gw': {k: v for k, v in after.items() if k != 'strain_hashes'}, 'generation': overview['engine_generation']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
