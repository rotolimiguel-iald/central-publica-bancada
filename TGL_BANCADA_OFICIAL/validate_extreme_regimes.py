"""Measure conditional scenarios using the existing resident executor, without a fit."""
import hashlib
import json
import math
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from validate_cosmology_live import gw_signature

HERE = Path(__file__).resolve().parent
CANON = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL')
BASE = 'http://127.0.0.1:18765/api/universe'
ASSETS = ['static/universe-map.html', 'static/universe-map.css', 'static/universe-map.js', 'static/universe.html', 'static/universe.js', 'static/universe.css']


def request(url, data=None):
    req = urllib.request.Request(url, json.dumps(data).encode() if data is not None else None,
                                 headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def main():
    before = json.loads((HERE / 'state/extremes_gw_before.json').read_text())
    baseline = {'mass_source_solar': 65, 'spin': .7, 'redshift': .1, 'amplitude': 1e-21,
                'phase': 0, 'duration_s': .12, 'reading': 'R-B'}
    variants = {
        'mass_clock_reference': {},
        'mass_clock_high_spin': {'spin': .95},
        'mass_clock_high_frequency': {'mass_source_solar': 20},
        'planck_clock_reference': {'reading': 'R-A'},
        'planck_clock_high_frequency': {'reading': 'R-A', 'mass_source_solar': 20},
        'global_control': {'reading': 'R-GLOBAL'},
    }
    measured = {}
    for name, changes in variants.items():
        parameters = {**baseline, **changes}
        result = request(BASE + '/model', parameters)
        assert result['scope'] == 'CONDITIONAL_ENSEMBLE_NOT_EVENT_FIT'
        p = result['prediction']
        assert all(math.isfinite(p[key]) for key in ['f_gr_hz', 'tau_gr_s', 'gamma_per_s', 'x', 'delta_tau_ensemble_exact'])
        assert p['reading'] == parameters['reading']
        assert math.isclose(p['x'], p['gamma_per_s'] * p['tau_gr_s'], rel_tol=1e-13, abs_tol=0)
        assert math.isclose(p['delta_tau_ensemble_exact'], -p['x']/(1+p['x']), rel_tol=1e-13, abs_tol=0)
        measured[name] = {'parameters': parameters, 'prediction': p, 'source': result['source'],
                          'scope': result['scope'], 'mass_detector_solar': result['mass_detector_solar']}
    ref, high = measured['mass_clock_reference']['prediction'], measured['mass_clock_high_frequency']['prediction']
    assert high['f_gr_hz'] > ref['f_gr_hz'] and high['gamma_per_s'] > ref['gamma_per_s']
    assert math.isclose(ref['x'], high['x'], rel_tol=1e-13)
    assert measured['mass_clock_high_spin']['prediction']['x'] > ref['x']
    a_ref, a_high = measured['planck_clock_reference']['prediction'], measured['planck_clock_high_frequency']['prediction']
    assert 0 < a_ref['x'] < 1e-30 and a_high['x'] > a_ref['x']
    assert math.isclose(a_high['x'] / a_ref['x'], 65/20, rel_tol=1e-13)
    assert measured['global_control']['prediction']['x'] == 0
    after = gw_signature(request(BASE + '/status'))
    assert before == after, 'Resident GW load changed'
    pins = {}
    for name in ASSETS:
        assert (HERE/name).read_bytes() == (CANON/name).read_bytes()
        pins[name] = hashlib.sha256((CANON/name).read_bytes()).hexdigest()
    report = {'created_utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS', 'cases': measured,
              'gw_unchanged': True, 'gw': after, 'installed_sha256': pins,
              'scope': 'CONDITIONAL_MODEL_CONTROLS_NOT_DETECTION_NOT_SENSITIVITY_NOT_SIGMA'}
    name = 'extremes_validation_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.json'
    body = json.dumps(report, ensure_ascii=False, indent=2).encode()
    for root in (HERE, CANON):
        file = root/'state'/name
        tmp = file.with_suffix('.tmp')
        with tmp.open('xb') as out:
            out.write(body)
        assert tmp.stat().st_size == len(body)
        tmp.replace(file)
    print(json.dumps({'receipt': str(HERE/'state'/name), 'gw_unchanged': True,
                     'measured': {name: {key: case['prediction'][key] for key in ['f_gr_hz','gamma_per_s','x','delta_tau_ensemble_exact']} for name,case in measured.items()}}, ensure_ascii=False))


if __name__ == '__main__':
    main()
