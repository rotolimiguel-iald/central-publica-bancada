"""Prepare an additive corrected peak-convention run using existing candidates."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    run=ROOT/"cache/nonlinear_intrinsic_peak"
    if run.exists():raise FileExistsError("Create-once run preparation")
    previous=json.loads((ROOT/"C5_NONLINEAR_COHERENT.json").read_bytes())
    if len(previous["results"])!=12:raise ValueError("Original search incomplete")
    run.mkdir()
    names=["coherent_imr_model.py","coherent_imr_likelihood.py","nonlinear_coherent_recovery.py",
           "validate_coherent_model.py","validate_coherent_likelihood.py","tgl_ringdown_prediction.py","tgl_ringdown_likelihood.py",
           "QNM_GRID.json","REGISTRO_C6.json","C5_SOURCE_UNCERTAINTY_SUMMARY.json",
           "cache/recolored_noise/O4_noise.npz","cache/recolored_noise/O5_noise.npz"]
    for name in names:
        p=run/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/name).read_bytes())
        if sha(p)!=sha(ROOT/name):raise ValueError("Copy differs")
    candidates={r["label"]:r["best"]["x"] for r in previous["results"]}
    (run/"PREVIOUS_CANDIDATES.json").write_bytes((json.dumps(candidates,indent=2)+"\n").encode())
    module=run/"coherent_imr_model.py";old=module.read_bytes()
    module.with_suffix(".py.original_bytes").write_bytes(old)
    text=old.decode()
    before='modes=[("all",None),("22",[(2,2)])]+([("44",[(4,4)])] if include44 else [])'
    after='modes=[("all",None)]+([("22",[(2,2)]),("44",[(4,4)])] if include44 else [])'
    if text.count(before)!=1:raise ValueError("Unexpected mode selection")
    text=text.replace(before,after)
    before='t,p,c=products["22"];index=int(np.argmax(p*p+c*c));amplitude=p[index]**2+c[index]**2'
    after='''# The intrinsic complex 22 amplitude is measured face-on. Its norm is
    # independent of inclination and orbital phase, unlike the projected norm.
    face_args=dict(pars,inclination=0.,mode_array=[(2,2)])
    face_p,face_c=get_td_waveform(**face_args)
    t=np.asarray(face_p.sample_times);p=np.asarray(face_p)*1e21;c=np.asarray(face_c)*1e21
    index=int(np.argmax(p*p+c*c));amplitude=p[index]**2+c[index]**2'''
    if text.count(before)!=1:raise ValueError("Unexpected peak code")
    text=text.replace(before,after)
    tmp=module.with_suffix(".tmp");tmp.write_bytes(text.encode());tmp.replace(module)
    runner=run/"nonlinear_coherent_recovery.py";old=runner.read_bytes();runner.with_suffix(".py.original_bytes").write_bytes(old)
    text=old.decode()
    replacements={
        '"REGISTRO_C6.json","C5_SOURCE_UNCERTAINTY_SUMMARY.json",':'"REGISTRO_C6.json","C5_SOURCE_UNCERTAINTY_SUMMARY.json","PREVIOUS_CANDIDATES.json",',
        'start="10 tM of injection-family remnant, fixed throughout each fit",':'start="10 tM after intrinsic complex-22 amplitude peak, fixed throughout each fit",\n             peak="Face-on isolated 22 amplitude; independent of source inclination and reference phase",',
        'search="Derivative-free bounded Powell, mass/common-spin/time stage maxfev150 then all seven nonlinear coordinates maxfev350; initialized at simulated source, local search only",':'search="Derivative-free bounded Powell over seven coordinates, maxfev350; start from best of original source and prior registered candidate. Local search only; previous peak convention preserved separately",'
    }
    for before,after in replacements.items():
        if text.count(before)!=1:raise ValueError("Unexpected runner field: "+before)
        text=text.replace(before,after)
    begin=text.index('    # Stage one explicitly changes both component spins equally.')
    end=text.index('    x=np.array(best["x"])',begin)
    text=text[:begin]+'''    previous=json.loads((ROOT/"PREVIOUS_CANDIDATES.json").read_bytes())[label]
    seeded=np.clip((np.array(previous)-x0)/STEPS,lower/STEPS,upper/STEPS)
    objective(seeded)
    start=(np.array(best["x"])-x0)/STEPS
    second=minimize(objective,start,method="Powell",bounds=bounds,options=dict(maxfev=350,ftol=1e-7,xtol=1e-4))
'''+text[end:]
    if text.count('for r in (first,second)')!=1:raise ValueError("Unexpected optimizer report")
    text=text.replace('for r in (first,second)','for r in (second,)')
    tmp=runner.with_suffix(".tmp");tmp.write_bytes(text.encode());tmp.replace(runner)
    (run/"PEAK_CORRECTION_PROVENANCE.json").write_bytes((json.dumps(dict(
        reason="Inclination-weighted polarization-norm peak jumps between carrier extrema; intrinsic complex-mode amplitude is the common reference",
        previous_results_sha256=sha(ROOT/"C5_NONLINEAR_COHERENT.json"),diagnosis_sha256=sha(ROOT/"C5_COHERENT_PEAK_DIAGNOSTIC.json"),
        parent_files={n:sha(ROOT/n) for n in names},new_model_sha256=sha(module),new_runner_sha256=sha(runner),
        preserved_original_C6=True,changed_convention_requires_separate_registration=True),indent=2)+"\n").encode())
    print(json.dumps(dict(status="PREPARED_NEW_INTRINSIC_PEAK_RUN",path=str(run),reused_candidates=len(candidates))),flush=True)


if __name__=="__main__":main()
