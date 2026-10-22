"""Nonlinear source integration with exact shared distance/polarization prior.

Nested sampling targets an equal mixture of separately centered likelihoods.
This is computational multiple-target integration, NEVER a product of mock data.
Each component evidence is reconstructed with its own importance weights.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "vendor"))
import argparse
from datetime import datetime, timezone
import hashlib
import json
import multiprocessing as mp
import time
import numpy as np
from scipy.special import logsumexp
import coherent_imr_model as model
from coherent_imr_likelihood import marginalized_source_log_likelihood
from tgl_ringdown_likelihood import linear_statistics

REG = ROOT / "REGISTRATION.json"
FAMILIES = ("IMRPhenomXPHM", "SEOBNRv4HM")
SOURCES = [dict(name="reference", mass=72., q=39/33, s1=.05, s2=-.03, inclination=.6, phase=.37, psi=0.),
           dict(name="source_64", mass=64., q=1.5, s1=.15, s2=.05, inclination=1., phase=.8, psi=.22),
           dict(name="source_90", mass=90., q=2., s1=.25, s2=-.15, inclination=.9, phase=1.2, psi=.45)]
_STATE = None
_FAMILY = None
_PROGRESS = None
_LAST_PRINT = 0.
_LAST_REGULAR = None


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value, replace=False):
    if path.exists() and not replace:
        raise FileExistsError(path)
    raw = (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+"\n").encode()
    temp = path.with_name(path.name+".tmp")
    temp.write_bytes(raw)
    if temp.stat().st_size != len(raw):
        raise ValueError("Short write")
    temp.replace(path)


def save_arrays(path, **values):
    if path.exists():
        raise FileExistsError(path)
    temp = path.with_name(path.name+".tmp.npz")
    np.savez_compressed(temp, **values)
    if temp.stat().st_size == 0:
        raise ValueError("Empty arrays")
    temp.replace(path)


def source_vector(s):
    return np.array([np.log(s["mass"]), np.log(s["q"]), s["s1"], s["s2"], s["inclination"], s["phase"], 0.])


def prior_transform(u):
    """Proper priors, independent of any same-event posterior or fitted source."""
    u = np.asarray(u)
    if u.shape != (7,) or np.any(u < 0) or np.any(u > 1):
        raise ValueError("Seven unit-cube coordinates required")
    return np.array([np.log(50.+60.*u[0]), np.log(1.+2.*u[1]), -.4+.8*u[2], -.4+.8*u[3],
                     np.arccos(-.95+1.9*u[4]), 2*np.pi*u[5], -1.+2.*u[6]])


def paired_polarizations(family, x, times, sample_rate=8192):
    """Both hypotheses from one physical source generation, no Taylor model."""
    # a=1 invokes the original verified implementation and fills its LRU cache.
    hp1, hc1, meta = model.polarizations(family, x, times, "R-B", 1., sample_rate)
    curves, mf, spin, peak = model.source_curves(family, tuple(x[:6]), sample_rate, True)
    if any(spin < s.x[0] or spin > s.x[-1] for s in model.qnm_splines().values()):
        raise ValueError("Remnant outside verified QNM grid")
    t = np.asarray(times)-x[6]*1e-3
    p, c, start, end, ratio = curves["all"]
    if min(t) < start or (max(t) > end and ratio > 1e-5):
        raise ValueError("Incomplete GR waveform interval")
    hp0, hc0 = np.asarray(p(t)), np.asarray(c(t))
    hp0[t > end] = 0.
    hc0[t > end] = 0.
    if not np.all(np.isfinite(hp0)) or not np.all(np.isfinite(hc0)):
        raise ValueError("Nonfinite GR waveform")
    return ((hp0, hc0), (hp1, hc1)), meta


def basis_from_polarizations(pair, white):
    first, second = [], []
    hp, hc = pair
    for fp, fc in model.RESPONSES:
        first.append(white @ (fp*hp+fc*hc))
        second.append(white @ (fc*hp-fp*hc))
    return np.column_stack([np.concatenate(first), np.concatenate(second)])


def register():
    names = [Path(__file__).name, "validate_source_evidence.py", "coherent_imr_model.py", "coherent_imr_likelihood.py",
             "tgl_ringdown_likelihood.py", "tgl_ringdown_prediction.py", "QNM_GRID.json", "REGISTRO_C6.json",
             "PROVENANCE.json", "vendor/MANIFEST.json"]
    names += [f"cache/recolored_noise/{p}_noise.npz" for p in ("O4", "O5")]
    reg = dict(status="REGISTERED_NONBLIND_NONLINEAR_SOURCE_INTEGRATION", date_utc=datetime.now(timezone.utc).isoformat(),
               sources=SOURCES, injection_families=FAMILIES, recovery_families=FAMILIES,
               psds=["O4", "O5"], reading="R-B", injection_a=[0., 1.], recovery_a=[0., 1.],
               noise_indices=[50, 100], N_per_cell=50, target_snr=40.,
               time_start_s=.0034, n_time=410, sampling_hz=2048, waveform_hz=8192,
               time_scope="Fixed 3.4 ms after intrinsic complex-22 peak for every injection, same time samples under both hypotheses; new experiment, old C6 untouched",
               priors=dict(total_detector_mass_solar=[50., 110.], mass_ratio=[1., 3.], spin1z=[-.4, .4], spin2z=[-.4, .4],
                           cos_inclination=[-.95, .95], orbital_reference_phase=[0., float(2*np.pi)], peak_shift_ms=[-1., 1.],
                           types="Independent uniforms in listed physical coordinates, not in their logs",
                           amplitude_prior_sd=3., distance="Inverse-Rayleigh D_ref=403 Mpc, shared two Gaussian coefficients; NOT uniform volume",
                           polarization="Uniform modulo pi, common to network"),
               conditioning="Known sky/responses/time delays, zero transverse spins, 22/44 whole-harmonic conditional damping; other harmonics unchanged",
               mixture="Computational arithmetic mean of 2400 separate centered likelihood components. NEVER product of injections. Evidence reconstructed per component; equivalent ratios independent of centering.",
               centers="Known injected-signal log likelihood ratio: .5||h||^2 + n dot h; numerical integration only, never source prior",
               pilot=dict(nlive=256, sample="rwalk", walks=20, bound="multi", dlogz=.5, maxcall=24000, seed=130522, processes=6),
               integration_diagnostics=dict(min_component_ESS=100, max_component_weight=.05, independent_seed_and_nlive_repeat_required=True,
                                            max_lnB_between_repeats=.2, max_rate_control_logL_change=.1),
               acceptance="No cell accepted from a single pilot. Stop limits, ESS, multimodal stability, waveform rate and opposite-family controls remain explicit",
               outstanding=["repeat convergence", "continuous-dephasing posterior bias/coverage", "SNR200/600", "other conditional readings", "physical partition selection remains external"],
               no_target_strain_read=True, original_C6_unchanged=True,
               hashes={n:sha(ROOT/n) for n in names})
    write(REG, reg)
    print(json.dumps(dict(status=reg["status"], sha256=sha(REG))), flush=True)


def check():
    reg = json.loads(REG.read_bytes())
    for name, value in reg["hashes"].items():
        if sha(ROOT/name) != value:
            raise ValueError("Registered file changed: "+name)
    manifest = json.loads((ROOT/"vendor/MANIFEST.json").read_bytes())
    for row in manifest["files"]:
        if sha(ROOT/"vendor"/row["path"]) != row["sha256"]:
            raise ValueError("Vendored dependency changed")
    return reg


def prepare():
    reg = check()
    path = ROOT/"INJECTIONS.npz"
    if path.exists():
        raise FileExistsError("Frozen injections already exist")
    times = np.arange(reg["n_time"])/reg["sampling_hz"]+reg["time_start_s"]
    arrays, labels, count = dict(times=times), [], 0
    source_pairs = {}
    for source in SOURCES:
        for family in FAMILIES:
            pair, metadata = paired_polarizations(family, source_vector(source), times, reg["waveform_hz"])
            source_pairs[(source["name"], family)] = pair
    for psd in reg["psds"]:
        with np.load(ROOT/f"cache/recolored_noise/{psd}_noise.npz") as f:
            white = f["whitener_scaled"].copy()
            low, high = reg["noise_indices"]
            noise = np.hstack([f[d+"_strain_scaled"][low:high]@white.T for d in ("H1", "L1")])
            for d in ("H1", "L1"):
                arrays[psd+"_"+d+"_gps"] = f[d+"_original_GPS"][low:high].copy()
        targets, centers = [], []
        for source in SOURCES:
            orientation = np.array([np.cos(2*source["psi"]), np.sin(2*source["psi"])])
            for family in FAMILIES:
                for a in reg["injection_a"]:
                    basis = basis_from_polarizations(source_pairs[(source["name"], family)][int(a)], white)
                    signal = basis @ orientation
                    signal *= reg["target_snr"]/np.linalg.norm(signal)
                    targets.append(signal[None, :]+noise)
                    centers.extend((.5*(signal@signal)+noise@signal).tolist())
                    for k in range(len(noise)):
                        labels.append(dict(psd=psd, source=source["name"], injection_family=family, injection_a=a,
                                           noise_index=reg["noise_indices"][0]+k, snr=reg["target_snr"]))
                        count += 1
        arrays[psd+"_white"] = white
        arrays[psd+"_targets"] = np.vstack(targets)
        arrays[psd+"_centers"] = np.array(centers)
    save_arrays(path, **arrays)
    write(ROOT/"INJECTIONS.json", dict(registration_sha256=sha(REG), arrays_sha256=sha(path), labels=labels,
                                     count=count, independent_noise_intervals_per_detector=50,
                                     scope="Paired reused noise; 1200 mock datasets are not independent events"))
    print(json.dumps(dict(status="PREPARED", datasets=count, likelihood_components=2*count)), flush=True)


def load_state():
    check()
    info = json.loads((ROOT/"INJECTIONS.json").read_bytes())
    if info["registration_sha256"] != sha(REG) or info["arrays_sha256"] != sha(ROOT/"INJECTIONS.npz"):
        raise ValueError("Injection custody mismatch")
    with np.load(ROOT/"INJECTIONS.npz") as f:
        state = {k:f[k].copy() for k in f.files}
    state["labels"] = info["labels"]
    return state


def component_loglikes(family, x, state, sample_rate=8192):
    pairs, metadata = paired_polarizations(family, x, state["times"], sample_rate)
    rows = []
    for a in (0, 1):
        across_psds = []
        for psd in ("O4", "O5"):
            basis = basis_from_polarizations(pairs[a], state[psd+"_white"])
            _, value = linear_statistics(basis, state[psd+"_targets"], 3.)
            across_psds.extend((value[0]-state[psd+"_centers"]).tolist())
        rows.append(across_psds)
    values = np.asarray(rows).ravel()
    if not np.all(np.isfinite(values)):
        raise ValueError("Nonfinite component likelihood")
    return values


def log_mixture(components):
    return float(logsumexp(components)-np.log(len(components)))


def component_integrals(logwt, logmix, blobs):
    """Integral Z_c = sum_i w_mix,i exp(ell_c,i - ell_mix,i)."""
    weights = np.asarray(logwt)[:, None]+np.asarray(blobs)-np.asarray(logmix)[:, None]
    logz = logsumexp(weights, axis=0)
    normalized = np.exp(weights-logz[None, :])
    ess = 1./np.sum(normalized**2, axis=0)
    maximum = np.max(normalized, axis=0)
    return logz, ess, maximum


def initialize(family):
    global _STATE, _FAMILY
    _STATE = load_state()
    _FAMILY = family


def loglike(x):
    values = component_loglikes(_FAMILY, np.asarray(x), _STATE)
    return log_mixture(values), values


def progress(results, niter, ncall, **kwargs):
    global _LAST_PRINT, _LAST_REGULAR
    if kwargs.get("add_live_it") is None:
        delta = float(results.delta_logz)
        _LAST_REGULAR = dict(niter=int(niter), ncall=int(ncall), delta_logz=delta if np.isfinite(delta) else None)
    if time.monotonic()-_LAST_PRINT < 25:
        return
    _LAST_PRINT = time.monotonic()
    row = dict(date_utc=datetime.now(timezone.utc).isoformat(), pid=os.getpid(),
               niter=int(niter), ncall=int(ncall), logz=float(results.logz), last_regular=_LAST_REGULAR)
    if np.isfinite(row["logz"]):
        write(_PROGRESS, row, replace=True)
        print(json.dumps(row), flush=True)


def summarize(result, output, family, seed, nlive, maxcall):
    blobs = np.stack(result.blob)
    z, ess, maximum = component_integrals(result.logwt, result.logl, blobs)
    state = _STATE
    count = len(state["labels"])
    delta = z[count:]-z[:count]
    rows = []
    for label in state["labels"]:
        group = {k:label[k] for k in ("psd", "source", "injection_family", "injection_a", "snr")}
        if any(r["cell"] == group for r in rows):
            continue
        indices = [k for k, other in enumerate(state["labels"]) if all(other[key] == val for key, val in group.items())]
        ii = np.array(indices)
        values = delta[ii]
        subset = np.r_[ii, count+ii]
        rows.append(dict(cell=group, N=len(ii), lnB_mean=float(values.mean()), lnB_sd=float(values.std(ddof=1)),
                         lnB_quantiles=np.quantile(values, [.05, .5, .95]).tolist(),
                         min_ESS=float(ess[subset].min()), max_single_weight=float(maximum[subset].max()),
                         status="PILOT_UNVALIDATED_NOT_SCIENTIFIC_ACCEPTANCE"))
    save_arrays(output/"samples.npz", samples=result.samples, samples_u=result.samples_u, logwt=result.logwt,
                logl=result.logl, logvol=result.logvol, logz_sequence=result.logz, logzerr=result.logzerr,
                components=blobs, component_logz=z, component_ESS=ess, component_max_weight=maximum,
                lnB=delta, ncall=result.ncall)
    report = dict(status="NONLINEAR_SOURCE_INTEGRATION_PILOT", family=family, seed=seed, nlive=nlive,
                  ncall=int(np.sum(result.ncall)), maxcall=maxcall, logz=float(result.logz[-1]),
                  sampler_logz_error=float(result.logzerr[-1]), last_regular=_LAST_REGULAR,
                  maxcall_reached=int(np.sum(result.ncall)) >= maxcall, rows=rows,
                  source_dimensions_integrated=7, common_amplitudes_integrated=2,
                  component_ESS_range=[float(ess.min()), float(ess.max())],
                  components_passing_weight_thresholds=int(np.count_nonzero((ess >= 100)&(maximum <= .05))),
                  component_count=len(z), registration_sha256=sha(REG),
                  scientific_acceptance=False, no_target_strain_read=True,
                  remaining="Independent seed/live-point convergence, waveform-rate controls, continuous-a coverage, other SNR/readings and source physics",
                  arrays_sha256=sha(output/"samples.npz"))
    write(output/"RESULT.json", report)
    print(json.dumps({k:report[k] for k in ("status", "family", "ncall", "component_ESS_range", "components_passing_weight_thresholds", "maxcall_reached")}), flush=True)


def run(args):
    global _PROGRESS
    import dynesty
    reg = check()
    name = f"{args.family}_seed{args.seed}_nlive{args.nlive}"
    output = ROOT/"runs"/name
    output.mkdir(parents=True, exist_ok=True)
    if (output/"RESULT.json").exists():
        raise FileExistsError("Completed run exists")
    checkpoint = output/"checkpoint.pkl"
    if checkpoint.exists() and not args.resume:
        raise FileExistsError("Checkpoint exists: resume explicitly")
    if args.resume and not checkpoint.exists():
        raise FileNotFoundError(checkpoint)
    _PROGRESS = output/"PROGRESS.json"
    initialize(args.family)
    with mp.get_context("fork").Pool(args.processes, initializer=initialize, initargs=(args.family,)) as pool:
        if args.resume:
            sampler = dynesty.NestedSampler.restore(str(checkpoint), pool=pool)
        else:
            write(output/"START.json", dict(date_utc=datetime.now(timezone.utc).isoformat(), pid=os.getpid(),
                       family=args.family, seed=args.seed, nlive=args.nlive, maxcall=args.maxcall,
                       registration_sha256=sha(REG), dynesty=dynesty.__version__, processes=args.processes))
            sampler = dynesty.NestedSampler(loglike, prior_transform, 7, nlive=args.nlive,
                         bound="multi", sample="rwalk", walks=20, periodic=[5],
                         rstate=np.random.default_rng(args.seed), pool=pool, queue_size=args.processes,
                         use_pool={"prior_transform":False}, blob=True)
        sampler.run_nested(dlogz=.5, maxcall=args.maxcall, print_progress=True, print_func=progress,
                           checkpoint_file=str(checkpoint), checkpoint_every=60, resume=args.resume)
        summarize(sampler.results, output, args.family, args.seed, args.nlive, args.maxcall)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["register", "prepare", "run"])
    parser.add_argument("--family", choices=FAMILIES, default=FAMILIES[0])
    parser.add_argument("--seed", type=int, default=130522)
    parser.add_argument("--nlive", type=int, default=256)
    parser.add_argument("--maxcall", type=int, default=24000)
    parser.add_argument("--processes", type=int, default=6)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    {"register":register, "prepare":prepare, "run":lambda:run(args)}[args.command]()
