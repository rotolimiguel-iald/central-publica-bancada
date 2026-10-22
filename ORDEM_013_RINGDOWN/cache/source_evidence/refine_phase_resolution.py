"""Extend measured resolution failures to32/64/128kHz without changing physics.

Frozen8192Hz injections remain fixed to isolate recovery resolution. This cannot
by itself establish high-SNR injection accuracy or posterior calibration.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1",OMP_NUM_THREADS="1")
from datetime import datetime,timezone
import json
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
import peak_phase_coordinates as pc
import continuous_phase_source as cp


def main():
    pm.check()
    folder=se.ROOT/"resolution_refinement"
    folder.mkdir(exist_ok=False)
    rates=(32768,65536,131072)
    reg=dict(status="REGISTERED_RESOLUTION_CONTROL",date_utc=datetime.now(timezone.utc).isoformat(),rates=rates,
        reading="R-B",strengths=[0.,.37,1.],snrs=[40.,200.,600.],N_per_cell=50,
        original_injections_unchanged=True,posterior_calibration=False,C6_changed=False,
        hashes={p.name:se.sha(p) for p in (se.Path(__file__),se.ROOT/"continuous_phase_source.py",pm.REG,se.ROOT/"INJECTIONS.npz")})
    se.write(folder/"REGISTRATION.json",reg)
    state=se.load_state();targets={};target_labels={}
    for psd in ("O4","O5"):
        labels=[l for l in state["labels"] if l["psd"]==psd]
        with np.load(se.ROOT/f"cache/recolored_noise/{psd}_noise.npz") as f:
            noise=np.hstack([f[d+"_strain_scaled"][50:100]@state[psd+"_white"].T for d in ("H1","L1")])
        for source in se.SOURCES:
            ids=[i for i,l in enumerate(labels) if l["source"]==source["name"]]
            ns=noise[[labels[i]["noise_index"]-50 for i in ids]]
            signals=state[psd+"_targets"][ids]-ns
            if np.max(np.abs(np.linalg.norm(signals,axis=1)-40))>1e-10:raise ValueError("Injection SNR differs")
            targets[(psd,source["name"])]=np.vstack([signals*(s/40)+ns for s in (40.,200.,600.)])
            target_labels[(psd,source["name"])]=[labels[i] for i in ids]
    cells=[];diagnostics=[]
    for family in se.FAMILIES:
        for source in se.SOURCES:
            x=se.source_vector(source);values={}
            for rate in rates:
                raw=cp.raw_phase_samples(family,x,state["times"],sample_rate=rate)
                arrays={}
                for psd in ("O4","O5"):
                    data=targets[(psd,source["name"])]
                    bank=cp.make_bank(raw,"R-B",[0.,.37,1.],state[psd+"_white"])
                    integral,controls=cp.marginal_loglikes(bank,data)
                    values[(rate,psd)]=integral.reshape(3,3,200)
                    arrays[psd+"_log_integrals"]=integral
                    interp=[]
                    for phase in (.173,.619):
                        y=x.copy();y[5]=phase
                        for index,a in ((0,0.),(2,1.)):
                            basis,_=se.model.network_basis(family,y,state["times"],"R-B",a,state[psd+"_white"],rate)
                            approx=pc.evaluate_bank(bank,[phase],index)[0]
                            relative=float(np.linalg.norm(basis-approx)/np.linalg.norm(basis))
                            _,direct=se.linear_statistics(basis,data,3.)
                            reconstructed=pc.bank_loglikes(bank,[phase],data,index)
                            errors=np.abs(direct-reconstructed).reshape(3,200).max(axis=1)
                            interp.append(dict(phase=phase,a=a,relative_waveform_error=relative,
                                logL_errors_by_SNR=errors.tolist(),all_interpolation_pass=bool(relative<=1e-6 and max(errors)<=.001)))
                    diagnostics.append(dict(family=family,source=source["name"],rate=rate,psd=psd,quadrature=controls,interpolation=interp))
                se.save_arrays(folder/f"{family}_{source['name']}_{rate}.npz",**arrays)
                print(json.dumps(dict(family=family,source=source["name"],rate=rate,done=True)),flush=True)
            for psd in ("O4","O5"):
                labels=target_labels[(psd,source["name"])]
                for j,snr in enumerate((40.,200.,600.)):
                    for k,a in enumerate((0.,.37,1.)):
                        for injfam in se.FAMILIES:
                            for inja in (0.,1.):
                                use=np.array([l["injection_family"]==injfam and l["injection_a"]==inja for l in labels])
                                changes=[float(np.max(np.abs(values[(r2,psd)][k,j,use]-values[(r1,psd)][k,j,use]))) for r1,r2 in zip(rates[:-1],rates[1:])]
                                cells.append(dict(recovery_family=family,source=source["name"],psd=psd,snr=snr,recovery_a=a,
                                    injection_family=injfam,injection_a=inja,N=int(use.sum()),logL_changes=changes,
                                    passes=[v<=.1 for v in changes]))
    summary=[]
    for snr in (40.,200.,600.):
        selected=[c for c in cells if c["snr"]==snr]
        summary.append(dict(snr=snr,cells=len(selected),passed=[sum(c["passes"][i] for c in selected) for i in (0,1)],
                            max_changes=[max(c["logL_changes"][i] for c in selected) for i in (0,1)]))
    result=dict(status="RESOLUTION_DIAGNOSTIC_NOT_POSTERIOR_ACCEPTANCE",rows=cells,diagnostics=diagnostics,summary=summary,
        rates=rates,scientific_acceptance=False,physical_prior_changed=False,
        injection_accuracy_at_high_SNR_validated=False,registration_sha256=se.sha(folder/"REGISTRATION.json"),
        hashes={p.name:se.sha(p) for p in folder.glob("*.npz")})
    se.write(folder/"RESULT.json",result)
    print(json.dumps(dict(status=result["status"],summary=summary)),flush=True)


if __name__=="__main__":main()
