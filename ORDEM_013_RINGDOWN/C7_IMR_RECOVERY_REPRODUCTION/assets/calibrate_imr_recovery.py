"""Non-blind, conditional full-IMR-shape recovery experiment.

Uses previously generated aligned-spin IMR controls and unused forecast noise
indices 50:256. Physical source parameters are held at their supplied values.
This tests waveform adequacy within an explicit two-family set, not coverage
for arbitrary real signals or a derivation of a physical TGL partition.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import numpy as np
from scipy.special import logsumexp
from tgl_ringdown_prediction import prediction, scales
from tgl_ringdown_likelihood import linear_statistics, profile_intervals
from diagnose_overtones import control_modes
from forecast_recolored_imr import distribution

ROOT = Path(__file__).resolve().parent
REG = ROOT / "REGISTRO_C5_IMR_RECOVERY.json"
OUTPUT = ROOT / "C5_IMR_RECOVERY.json"
RESPONSES = {"H1":(.7, .2), "L1":(-.3, .8)}
READINGS = ["R-A", "R-B", "R-RAIZ-0", "R-RAIZ-EP4", "R-RAIZ-REST", "R-LIN", "R-MOD", "R-GLOBAL"]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create(path, data):
    if path.exists():
        raise FileExistsError("Preserve prior experiment: "+str(path))
    raw = (json.dumps(data, indent=2, ensure_ascii=False)+"\n").encode()
    temp = path.with_name(path.name+".tmp")
    temp.write_bytes(raw)
    if temp.stat().st_size != len(raw):
        raise ValueError("Short write")
    temp.replace(path)


def register():
    files = [Path(__file__).name, "tgl_ringdown_prediction.py", "tgl_ringdown_likelihood.py",
             "diagnose_overtones.py", "forecast_recolored_imr.py", "QNM_GRID.json", "C5_EXTRA_QNMS.json",
             "C5_IMR_CONTROLS.json", "C5_RECOLORED_NOISE.json", "REGISTRO_C6.json"]
    families = json.loads((ROOT/"C5_IMR_CONTROLS.json").read_bytes())["families"]
    scenarios = json.loads((ROOT/"C5_RECOLORED_NOISE.json").read_bytes())["scenarios"]
    files += [f"cache/imr_controls/{f['family']}.npz" for f in families]
    files += [s["cache_path"] for s in scenarios if s["psd"] in ("O4", "O5")]
    reg = dict(status="REGISTERED_NONBLIND_MODEL_ADEQUACY_EXTENSION",
               created_utc=datetime.now(timezone.utc).isoformat(),
               prior_knowledge="All previous injection/strain results are known; this is not a blind discovery test",
               computed_psds=["O4", "O5"], readings=READINGS, snrs=[40., 200., 600.],
               injection_amplitudes=[0., 1.], noise_indices=[50, 256], N=206,
               start_tM=10., sample_rate_hz=2048., amplitude_prior_sd_strain=1e-20,
               response_factors=RESPONSES,
               source_parameters="The two fixed, family-specific remnants and original binary parameters from C5_IMR_CONTROLS; no parameter estimation or external IMR prior",
               recovery="Exact 22,44,other harmonic shapes from each supplied IMR family; six independently Gaussian real coefficients per detector",
               waveform_normalization="Each harmonic pair divided by its maximum polarization norm in the declared interval at a=0. The divisor stays fixed for every a and is identical under both point hypotheses.",
               deformation="Whole 22 and 44 harmonics damped by their fundamental Gamma times time since the 22 peak; other modes unchanged, matching prior C5 injections. It is a conditional transposition, not a unique overtone theory.",
               recovery_choices=["SEOBNRv4HM", "IMRPhenomXPHM", "EQUAL_FAMILY_MIXTURE"],
               family_mixture="Prior probability 1/2 for each entire network family under a=0 and a=1. Bayesian marginal likelihood is logsumexp minus log(2), not the maximum. Diagnostic profile likelihood maximizes over the two families.",
               criteria=dict(max_absolute_median_bias=.2, coverage90_min=.80, coverage90_max=.97,
                             profile_boundary_hits=0, minimum_injections=50),
               diagnostic_grid="Both-family-safe interval [-0.8,2]/max(Gamma*tau_GR), 2401 points plus exact 0 and 1; negative a is diagnostic only, never a physical hypothesis",
               unidentifiable="max(Gamma*tau_GR)<1e-12 receives only point likelihoods and no claimed calibration",
               interpretation="Same-family success is manufactured closure, opposite-family fit is mismatch control. Mixture success covers only the declared two-family set at this one source; it does not pay full astrophysical acceptance.",
               no_target_strain_read=True, original_C6_unchanged=True,
               hashes={n:sha(ROOT/n) for n in files})
    create(REG, reg)
    print(json.dumps(dict(status=reg["status"], sha256=sha(REG), cells_planned=576,
                          N=reg["N"], target_strain=False)), flush=True)


def shapes(family, waveform, times, start_tM):
    tp = times+start_tM*scales(family["remnant_mass_detector_solar"], "CODATA2018_IAU2015")[0]
    values = {k:np.interp(tp, waveform["time_from_peak_s"], waveform[k])*1e21
              for k in ("22_plus", "22_cross", "44_plus", "44_cross", "other_plus", "other_cross")}
    norms = {k:float(np.max(np.hypot(values[k+"_plus"], values[k+"_cross"])))
             for k in ("22", "44", "other")}
    if min(norms.values()) <= 0:
        raise ValueError("Degenerate harmonic basis")
    return tp, values, norms


def run():
    if OUTPUT.exists():
        raise FileExistsError("Preserve prior scientific result")
    reg = json.loads(REG.read_bytes())
    for name, expected in reg["hashes"].items():
        if sha(ROOT/name) != expected:
            raise ValueError("Registered input changed: "+name)
    families = json.loads((ROOT/"C5_IMR_CONTROLS.json").read_bytes())["families"]
    meta = json.loads((ROOT/"C5_RECOLORED_NOISE.json").read_bytes())
    outputs, caches = [], []
    directory = ROOT/"cache/imr_recovery"
    directory.mkdir(exist_ok=True)
    for scenario in meta["scenarios"]:
        if scenario["psd"] not in reg["computed_psds"]:
            continue
        checkpoint = directory/f"{scenario['psd']}.json"
        if checkpoint.exists():
            saved = json.loads(checkpoint.read_bytes())
            if saved["registration_sha256"] != sha(REG):
                raise ValueError("Checkpoint registration changed")
            if sha(ROOT/saved["cache"]["path"]) != saved["cache"]["sha256"]:
                raise ValueError("Checkpoint draws changed")
            outputs.extend(saved["results"]); caches.append(saved["cache"])
            print(json.dumps(dict(reused_checkpoint=scenario["psd"])), flush=True)
            continue
        with np.load(ROOT/scenario["cache_path"]) as data:
            white = data["whitener_scaled"].copy()
            lo, hi = reg["noise_indices"]
            noise = {d:data[d+"_strain_scaled"][lo:hi] @ white.T for d in RESPONSES}
            gps = {d:data[d+"_original_GPS"][lo:hi].copy() for d in RESPONSES}
        if any(len(x) != reg["N"] for x in noise.values()):
            raise ValueError("Insufficient unused noise intervals")
        times = np.arange(white.shape[1])/reg["sample_rate_hz"]
        prepared = []
        for family in families:
            with np.load(ROOT/f"cache/imr_controls/{family['family']}.npz") as data:
                tp, value, norms = shapes(family, data, times, reg["start_tM"])
            prepared.append(dict(family=family, exact=control_modes(family), tp=tp, values=value, norms=norms))
        rows, draws = [], []
        for reading in READINGS:
            for p in prepared:
                f = p["family"]
                pred = {ell:prediction(f["remnant_mass_detector_solar"], f["remnant_spin"], reading,
                           mode=(ell,ell,0), qnm_dimensionless=p["exact"][(ell,ell,0)]) for ell in (2,4)}
                p["pred"] = pred
            maxx = max(p["pred"][ell]["x"] for p in prepared for ell in (2,4))
            unresolved = maxx < 1e-12
            grid = np.array([0.,1.]) if unresolved else np.unique(np.r_[np.linspace(-.8,2.,2401)/maxx,0.,1.])
            zero = int(np.flatnonzero(grid==0)[0]); one = int(np.flatnonzero(grid==1)[0])
            bases = []
            for p in prepared:
                columns = []
                for name, ell in (("22",2),("44",4),("other",None)):
                    gamma = 0. if ell is None else p["pred"][ell]["gamma_per_s"]
                    envelope = np.exp(-grid[:,None]*gamma*p["tp"][None,:])
                    columns += [envelope*p["values"][name+"_"+pol][None,:]/p["norms"][name]
                                for pol in ("plus","cross")]
                raw = np.stack(columns,axis=-1)
                bases.append(np.einsum("kt,gti->gki", white, raw, optimize=True))
            targets = {d:[] for d in RESPONSES}; clean = {d:[] for d in RESPONSES}; cells=[]
            for p in prepared:
                for injected in reg["injection_amplitudes"]:
                    signals={}
                    for d,(fp,fc) in RESPONSES.items():
                        val=p["values"]
                        y=fp*val["other_plus"]+fc*val["other_cross"]
                        for ell in (2,4):
                            name=str(ell)*2
                            y=y+(fp*val[name+"_plus"]+fc*val[name+"_cross"])*np.exp(-injected*p["pred"][ell]["gamma_per_s"]*p["tp"])
                        signals[d]=white@y
                    norm=np.sqrt(sum(y@y for y in signals.values()))
                    for snr in reg["snrs"]:
                        for d in RESPONSES:
                            clean[d].append(signals[d]*snr/norm)
                            targets[d].extend(noise[d]+signals[d][None,:]*snr/norm)
                        cells.append(dict(injection_family=p["family"]["family"], psd=scenario["psd"],
                                          reading=reading, injected_a=injected, SNR=snr,
                                          reference_SNR_403Mpc=float(norm), max_Gamma_tau=float(maxx)))
            profile_by_family=[]; marginal_by_family=[]; clean_by_family=[]
            for basis in bases:
                total_profile=0.;total_marginal=0.;total_clean=0.
                for d in RESPONSES:
                    profile, marginal=linear_statistics(basis, np.asarray(targets[d]), 10.)
                    clean_profile,_=linear_statistics(basis, np.asarray(clean[d]), 10.)
                    total_profile=total_profile+profile;total_marginal=total_marginal+marginal
                    total_clean=total_clean+clean_profile
                profile_by_family.append(total_profile)
                marginal_by_family.append(total_marginal)
                clean_by_family.append(total_clean)
            choices=[(families[i]["family"],profile_by_family[i],marginal_by_family[i],clean_by_family[i]) for i in range(2)]
            choices.append(("EQUAL_FAMILY_MIXTURE",np.maximum(*profile_by_family),
                            np.logaddexp(*marginal_by_family)-np.log(2),np.maximum(*clean_by_family)))
            for label, profile, marginal, clean_profile in choices:
                fit=None if unresolved else profile_intervals(grid,profile)
                cleanfit=None if unresolved else profile_intervals(grid,clean_profile)
                for index, initial in enumerate(cells):
                    row=dict(initial, recovery=label, N=reg["N"], draws_index=len(draws))
                    lo=index*reg["N"];hi=(index+1)*reg["N"]
                    lnb=marginal[one,lo:hi]-marginal[zero,lo:hi]
                    row["lnB"]=distribution(lnb)
                    if unresolved:
                        row.update(status="UNIDENTIFIABLE_AT_NUMERICAL_AND_OBSERVATIONAL_PRECISION",
                                   absolute_bias=None,coverage_90=None,boundary_hits=None)
                        saved=np.column_stack([lnb,np.full((reg["N"],3),np.nan)])
                    else:
                        subset=fit[lo:hi]; est=np.array([x["MLE"] for x in subset])
                        intervals=np.array([x["CI90"] for x in subset])
                        bias=float(abs(np.median(est)-row["injected_a"]))
                        coverage=float(np.mean((intervals[:,0]<=row["injected_a"])&(row["injected_a"]<=intervals[:,1])))
                        boundary=sum(x["boundary"] for x in subset)
                        passed=bias<=.2 and .8<=coverage<=.97 and boundary==0
                        sigma=float(np.median(intervals[:,1]-intervals[:,0])/(2*1.6448536269514722))
                        row.update(status="CALIBRATED_CONDITIONAL_CELL" if passed else "INCONCLUSIVE_SYSTEMATICS",
                                   absolute_bias=bias, coverage_90=coverage,boundary_hits=boundary,
                                   power_proxy=None if boundary else 1/sigma,
                                   noiseless_a_hat=cleanfit[index]["MLE"],
                                   noiseless_boundary=cleanfit[index]["boundary"],
                                   noiseless_residual_norm_squared=float(row["SNR"]**2-2*np.max(clean_profile[:,index])))
                        saved=np.column_stack([lnb,est,intervals])
                    rows.append(row);draws.append(saved)
            print(json.dumps(dict(psd=scenario["psd"],reading=reading,cells_total=len(rows))),flush=True)
        cache=directory/f"{scenario['psd']}_draws.npz"
        if cache.exists():raise FileExistsError(cache)
        np.savez_compressed(cache,draws=np.asarray(draws),columns=["lnB","a_hat","CI90_lower","CI90_upper"],
                            H1_original_GPS=gps["H1"],L1_original_GPS=gps["L1"])
        rowcache=dict(path=cache.relative_to(ROOT).as_posix(),sha256=sha(cache))
        create(checkpoint,dict(registration_sha256=sha(REG),cache=rowcache,results=rows))
        outputs.extend(rows);caches.append(rowcache)
    verdicts={k:sum(r["status"]==k for r in outputs) for k in sorted({r["status"] for r in outputs})}
    joint=[]
    for psd in reg["computed_psds"]:
        for reading in READINGS:
            for snr in reg["snrs"]:
                selected=[r for r in outputs if r["psd"]==psd and r["reading"]==reading and r["SNR"]==snr
                          and r["recovery"]=="EQUAL_FAMILY_MIXTURE"]
                if len(selected)!=4:raise ValueError("Incomplete two-family criterion")
                joint.append(dict(psd=psd,reading=reading,SNR=snr,pass_all_four=all(r["status"]=="CALIBRATED_CONDITIONAL_CELL" for r in selected)))
    result=dict(status="CONDITIONAL_IMR_RECOVERY_CALCULATED",registration_sha256=sha(REG),
                number_of_cells=len(outputs),N_per_cell=reg["N"],results=outputs,draws=caches,
                status_counts=verdicts,joint_mixture_criteria=joint,
                original_C5_and_C6_modified=False,no_target_strain_read=True,
                scope=reg["interpretation"],no_free_physical_partition_selected=True)
    create(OUTPUT,result)
    print(json.dumps(dict(status=result["status"],cells=len(outputs),counts=verdicts,
                          joint_mixture_pass=sum(x["pass_all_four"] for x in joint))),flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("command",choices=["register","run"])
    args=parser.parse_args()
    register() if args.command=="register" else run()
