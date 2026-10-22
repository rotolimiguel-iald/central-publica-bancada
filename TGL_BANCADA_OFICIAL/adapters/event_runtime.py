"""Registered event windows from resident arrays; no fit or significance claim."""
from __future__ import annotations

import hashlib
import math
from pathlib import Path
import time

import numpy as np

NOISE_CACHE = {}


def checked_noise(source, samples):
    key = (source['path'], source['sha256'], samples)
    if key not in NOISE_CACHE:
        path = Path(source['path'])
        if hashlib.sha256(path.read_bytes()).hexdigest() != source['sha256']:
            raise ValueError('Registered noise cache changed')
        with np.load(path, allow_pickle=False) as saved:
            w = np.array(saved['whitener_scaled'], dtype=float, copy=True)
            frequency = np.array(saved['frequency_hz'], dtype=float, copy=True)
            psd = np.array(saved['median_psd_strain'], dtype=float, copy=True)
        if w.ndim != 2 or w.shape[1] != samples or not np.all(np.isfinite(w)):
            raise ValueError('Noise whitener incompatible with registered window')
        if frequency.ndim != 1 or frequency.shape != psd.shape or not np.all(np.isfinite(frequency)):
            raise ValueError('Invalid noise spectrum')
        if not np.all(np.isfinite(psd)) or np.any(psd < 0):
            raise ValueError('Invalid noise PSD')
        # Right polar factor: positive symmetric whitening in the original
        # sample coordinates. It mixes samples, but preserves ||W x|| exactly
        # in exact arithmetic; it is not reconstruction of a clean signal.
        _, singular_values, right = np.linalg.svd(w, full_matrices=False)
        symmetric = (right.T * singular_values) @ right
        for a in (w, frequency, psd, symmetric):
            a.flags.writeable = False
        NOISE_CACHE[key] = (w, frequency, psd, symmetric)
    return NOISE_CACHE[key]


def quality_for_window(arrays, record, times_gps, profile):
    result = {'passed': True, 'required_dq': profile['required_dq'],
              'required_injections': profile['required_injections'], 'masks': {}}
    for group, key, names_key, required in (
        ('dq', '/quality/simple/DQmask', '/quality/simple/DQShortnames', profile['required_dq']),
        ('injections', '/quality/injections/Injmask', '/quality/injections/InjShortnames', profile['required_injections']),
    ):
        if key not in arrays or names_key not in record['metadata']:
            raise ValueError('Required quality mask/names missing: ' + key)
        mask = arrays[key]
        names = record['metadata'][names_key]
        attrs = record.get('dataset_attributes', {}).get(key, {})
        spacing = float(attrs.get('Xspacing', float('nan')))
        start = float(attrs.get('Xstart', float('nan')))
        if not math.isfinite(spacing) or spacing <= 0 or not math.isfinite(start):
            raise ValueError('Quality-mask time reference absent; reload domain')
        if attrs.get('Xunits') not in ('second', 'seconds', 's'):
            raise ValueError('Quality-mask time unit is not seconds')
        if mask.ndim != 1 or mask.dtype.kind not in 'ui' or len(set(names)) != len(names):
            raise ValueError('Invalid quality mask or duplicated bit name')
        missing = set(required) - set(names)
        if missing:
            raise ValueError('Required quality bit absent: ' + ', '.join(sorted(missing)))
        first_bin = math.floor((float(np.min(times_gps)) - start) / spacing)
        last_bin = math.floor((float(np.max(times_gps)) - start) / spacing)
        if first_bin < 0 or last_bin >= len(mask):
            raise ValueError('Window outside quality-mask coverage')
        indices = np.arange(first_bin, last_bin + 1, dtype=np.int64)
        bits = sum(1 << names.index(name) for name in required)
        checks = (mask[indices] & bits) == bits
        passed = bool(np.all(checks))
        result['masks'][group] = {'passed': passed, 'bins_checked': len(indices),
                                   'failed_bins': int(np.count_nonzero(~checks)),
                                   'start_gps': start, 'spacing_s': spacing}
        result['passed'] = result['passed'] and passed
    if not result['passed']:
        raise ValueError('Registered DQ/injection criteria failed for this window')
    return result


def event_view(domain, request, verify_models):
    started = time.perf_counter()
    profile = request['profile']  # Supplied by the server allowlist, never by HTTP clients.
    start_tm = float(request.get('start_tm', profile['primary_start_tm']))
    if start_tm not in profile['starts_tm']:
        raise ValueError('Select a registered event start time')
    reading = request.get('reading')
    if reading not in ('R-A', 'R-B', 'R-RAIZ-0', 'R-GLOBAL'):
        raise ValueError('Select an explicit clock reading')
    mass = float(request.get('mass_source_solar', profile['reference_mass_detector_solar'] / (1 + profile['redshift'])))
    spin = float(request.get('spin', .7))
    z = float(request.get('redshift', profile['redshift']))
    if not all(math.isfinite(v) for v in (mass, spin, z)) or not 1 <= mass <= 1e4 or not 0 <= spin < 1 or z < 0:
        raise ValueError('Invalid event model mass/spin/redshift')
    params = request.get('detectors')
    if not isinstance(params, dict) or set(params) != {'H1', 'L1'}:
        raise ValueError('Explicit amplitude and phase required for H1 and L1')
    manifest = verify_models()
    from tgl_ringdown_prediction import prediction
    from tgl_ringdown_template import ringdown
    detector_mass = mass * (1 + z)
    p = prediction(detector_mass, spin, reading, redshift=z)
    channels = []
    count = int(profile['samples'])
    stride = int(profile['stride'])
    with domain.lock:
        if domain.state['status'] not in ('READY', 'PARTIAL'):
            raise ValueError('Complete the resident domain load before opening an event')
        for detector in ('H1', 'L1'):
            source = profile['sources'][detector]
            candidates = [r for r in domain.records if r['name'] == source['name']
                          and r.get('source_sha256') == source['sha256']
                          and r.get('source_path') == source['path']]
            if len(candidates) != 1:
                raise ValueError('Registered event source not uniquely resident: ' + detector)
            record = candidates[0]
            if record['detector'] != detector:
                raise ValueError('Event detector does not match source metadata')
            dt = record['dt_s']
            if not math.isclose(1 / dt, profile['input_sample_rate_hz'], rel_tol=1e-12):
                raise ValueError('Resident sample rate does not match registration')
            peak = profile['reference_peak_gps'][detector]
            requested_gps = peak + start_tm * profile['reference_tM_seconds']
            first = math.ceil((requested_gps - record['gps_start']) / dt)
            indices = first + np.arange(count, dtype=np.int64) * stride
            raw_stop = first + count * stride
            if indices[0] < 0 or raw_stop > record['rows']:
                raise ValueError('Event window outside resident strain')
            arrays = domain.arrays[record['id']]
            observed = arrays['/strain/Strain'][indices]
            if len(observed) != count or not np.all(np.isfinite(observed)):
                raise ValueError('Event window includes nonfinite or missing strain')
            # Avoid accumulating GPS-scale floating point subtraction errors.
            relative = indices * dt + (record['gps_start'] - peak)
            times_gps = record['gps_start'] + indices * dt
            quality_interval = np.array([record['gps_start'] + first * dt,
                                         record['gps_start'] + (raw_stop - 1) * dt])
            quality = quality_for_window(arrays, record, quality_interval, profile)
            amplitude = float(params[detector]['amplitude'])
            phase = float(params[detector]['phase'])
            if not math.isfinite(amplitude) or not 0 <= amplitude <= 1e-15 or not math.isfinite(phase):
                raise ValueError('Invalid detector amplitude/phase')
            # Free detector coefficients, defined at the FIRST selected sample;
            # no antenna reconstruction, auto-fit or peak-amplitude interpretation.
            model_time = np.arange(count) * dt * stride
            gr = ringdown(model_time, detector_mass, spin, reading, amplitude,
                          phase=phase, deformation=0, redshift=z)['plus']
            tgl = ringdown(model_time, detector_mass, spin, reading, amplitude,
                           phase=phase, deformation=1, redshift=z)['plus']
            w, frequency, psd, symmetric = checked_noise(profile['noise_sources'][detector], count)
            residual_gr = observed - gr
            residual_tgl = observed - tgl
            weighted_gr = w @ (residual_gr * 1e21)
            weighted_tgl = w @ (residual_tgl * 1e21)
            vectors = {'strain': observed, 'gr': gr, 'tgl': tgl,
                       'residual_gr': residual_gr, 'residual_tgl': residual_tgl}
            normalized = {name: symmetric @ (vector * 1e21) for name, vector in vectors.items()}
            norm_checks = {}
            for name, weighted in (('residual_gr', weighted_gr), ('residual_tgl', weighted_tgl)):
                norm = float(normalized[name] @ normalized[name])
                expected = float(weighted @ weighted)
                if not math.isclose(norm, expected, rel_tol=1e-8, abs_tol=1e-9):
                    raise ValueError('Symmetric whitening changed the registered residual norm')
                norm_checks[name] = abs(norm - expected) / max(expected, 1e-30)
            # Indices rather than time: the polynomial quotient mixes samples.
            spectral_indices = np.unique(np.linspace(0, len(frequency) - 1, 513, dtype=int))
            channels.append({
                'detector': detector, 'time_s': relative.tolist(), 'strain': observed.tolist(),
                'gr': gr.tolist(), 'tgl': tgl.tolist(),
                'residual_gr': residual_gr.tolist(), 'residual_tgl': residual_tgl.tolist(),
                'normalized': {name: vector.tolist() for name, vector in normalized.items()},
                'normalization': {'method': 'RIGHT_POLAR_FACTOR_SQRT_W_TRANSPOSE_W',
                                  'units': 'dimensionless', 'input_scale': 1e21,
                                  'mixes_samples_nonlocally': True, 'norm_relative_errors': norm_checks,
                                  'scope': 'NOISE_NORMALIZED_DISPLAY_NOT_SIGNAL_RECONSTRUCTION'},
                'quality': quality, 'first_sample_gps': float(times_gps[0]),
                'last_sample_gps': float(times_gps[-1]), 'requested_start_gps': requested_gps,
                'first_sample_index': first, 'source_id': record['id'],
                'source_sha256': record['source_sha256'], 'strain_array_sha256': record['strain_array_sha256'],
                'units': {'x': 's from detector reference peak', 'y': 'strain'},
                'model_time_origin_s': float(relative[0]),
                'amplitude_reference': 'FIRST_SELECTED_SAMPLE_EFFECTIVE_DETECTOR_STRAIN',
                'noise': {'source_sha256': profile['noise_sources'][detector]['sha256'],
                          'frequency_hz': frequency[spectral_indices].tolist(),
                          'median_psd_strain_per_hz': psd[spectral_indices].tolist(),
                          'whitener_shape': list(w.shape),
                          'diagnostic_norm2_gr': float(weighted_gr @ weighted_gr),
                          'diagnostic_norm2_tgl': float(weighted_tgl @ weighted_tgl),
                          'scope': 'FIXED_PARAMETERS_QUOTIENT_RESIDUAL_NORM_NOT_PVALUE_OR_SIGMA'},
            })
        return {
            'event': profile['event'], 'scope': 'EXPLORATORY_DETECTOR_OVERLAY_NOT_C6_INFERENCE',
            'channels': channels, 'prediction': p,
            'parameters': {k: v for k, v in request.items() if k not in ('profile', 'operation', 'request_id')},
            'physical_gate': profile['physical_gate'], 'load_id': domain.state['load_id'],
            'generation': domain.generation,
            'domain_load_status': domain.state['status'],
            'data_reads_since_load': domain.data_reads - domain.state['reads_after_load'],
            'elapsed_ms': (time.perf_counter() - started) * 1000,
            'source': {'model_files': manifest['files'], 'event_provenance': profile['provenance']},
            'model_assumptions': ['220_BCW_FIT_ENSEMBLE', 'INDEPENDENT_MANUAL_DETECTOR_AMPLITUDES_AND_PHASES',
                                  'NO_ANTENNA_RECONSTRUCTION_NO_POSTERIOR_FIT',
                                  'REGISTERED_TIME_WINDOW_FIXED_AS_PARAMETERS_CHANGE',
                                  'STRIDE2_WITHOUT_PRE_ONSET_FILTER_AS_REGISTERED'],
        }
