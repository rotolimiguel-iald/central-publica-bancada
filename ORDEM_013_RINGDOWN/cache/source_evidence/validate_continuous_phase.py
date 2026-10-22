"""Compare continuous-strength phase integrals to direct complete waveforms."""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from datetime import datetime, timezone
import json
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
import peak_phase_coordinates as pc
import continuous_phase_source as cp


def main():
    pm.check()
    if se.sha(se.ROOT/"REGISTRO_C6.json")!=se.sha(se.ROOT.parent.parent/"REGISTRO_C6.json"):
        raise ValueError("C6 registration changed")
    target=se.ROOT/"CONTINUOUS_PHASE_VALIDATION.json"
    if target.exists():
        raise FileExistsError("Validation is create-once")
    state=se.load_state()
    strengths=np.array([-.25,0.,.37,1.,2.])
    rows=[]
    for family in se.FAMILIES:
        for source in (se.SOURCES[0],se.SOURCES[2]):
            x=se.source_vector(source)
            raw=cp.raw_phase_samples(family,x,state["times"])
            for reading in ("R-B","R-RAIZ-0","R-LIN","R-MOD"):
                for psd in ("O4","O5"):
                    bank=cp.make_bank(raw,reading,strengths,state[psd+"_white"])
                    direct_controls=[]
                    for phase in (.173,.619,1.413):
                        y=x.copy();y[5]=phase
                        for i,a in enumerate(strengths):
                            original,meta=se.model.network_basis(family,y,state["times"],reading,float(a),state[psd+"_white"])
                            interpolated=pc.evaluate_bank(bank,[phase],i)[0]
                            relative=float(np.linalg.norm(original-interpolated)/np.linalg.norm(original))
                            _,direct=se.linear_statistics(original,state[psd+"_targets"],3.)
                            approximate=pc.bank_loglikes(bank,[phase],state[psd+"_targets"],i)
                            ll_error=float(np.max(np.abs(direct-approximate)))
                            if relative>1e-6 or ll_error>.001:
                                raise ValueError(f"Continuous-strength bank differs from original: {family},{reading},{a},{relative},{ll_error}")
                            direct_controls.append(dict(phase=phase,strength=float(a),relative_waveform_error=relative,logL_error=ll_error))
                    integrated,quadratures=cp.marginal_loglikes(bank,state[psd+"_targets"])
                    row=dict(family=family,source=source["name"],reading=reading,psd=psd,
                             direct_controls=direct_controls,quadratures=quadratures)
                    if reading=="R-B":
                        old=pc.phase_bank(family,x,state["times"],state[psd+"_white"])
                        errors=[]
                        for previous_index,new_index in ((0,1),(1,3)):
                            before=pc.phase_integral(old,state[psd+"_targets"],previous_index,n=1024)
                            errors.append(float(np.max(np.abs(before-integrated[new_index]))))
                        row["original_zero_one_integral_error"]=max(errors)
                        if max(errors)>2e-5:
                            raise ValueError("Original binary-hypothesis integral changed")
                    rows.append(row)
                    print(json.dumps(dict(cells_done=len(rows),family=family,reading=reading,psd=psd)),flush=True)
    se.write(target,dict(status="PASS_CONTINUOUS_STRENGTH_PHASE_LIKELIHOOD",date_utc=datetime.now(timezone.utc).isoformat(),
        rows=rows,families=2,source_points_per_family=2,readings=4,strengths=strengths.tolist(),
        physical_clock_selected=False,continuous_strength_prior_selected=False,
        negative_strength_scope="Phenomenological numerical control, not a physical GKLS claim",
        scientific_acceptance=False,source_integrals_or_coverage_completed=False,
        original_C6_changed=False,
        hashes={p.name:se.sha(p) for p in (se.Path(__file__),se.ROOT/"continuous_phase_source.py",se.ROOT/"coherent_imr_model.py",pm.REG)}))
    allc=[c for r in rows for c in r["direct_controls"]]
    print(json.dumps(dict(status="PASS_CONTINUOUS_STRENGTH_PHASE_LIKELIHOOD",cells=len(rows),direct_controls=len(allc),
        max_waveform_error=max(c["relative_waveform_error"] for c in allc),max_logL_error=max(c["logL_error"] for c in allc),
        max_old_zero_one_error=max(r.get("original_zero_one_integral_error",0.) for r in rows))),flush=True)


if __name__=="__main__":
    main()
