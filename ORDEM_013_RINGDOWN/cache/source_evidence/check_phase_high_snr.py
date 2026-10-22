"""Template-rate and phase-quadrature controls at the registered future SNRs.

These are likelihood evaluations at specified source points, not completed
source evidence or coverage. No on-source data and no physical clock selection.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from datetime import datetime, timezone
import json
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
import continuous_phase_source as cp


def main():
    pm.check()
    output=se.ROOT/"PHASE_HIGH_SNR_CONTROLS.json"
    if output.exists():
        raise FileExistsError("Preserve high-SNR control")
    state=se.load_state()
    noises={}
    labels={}
    for psd in ("O4","O5"):
        with np.load(se.ROOT/f"cache/recolored_noise/{psd}_noise.npz") as f:
            noises[psd]=np.hstack([f[d+"_strain_scaled"][50:100]@state[psd+"_white"].T for d in ("H1","L1")])
        labels[psd]=[v for v in state["labels"] if v["psd"]==psd]
    rows=[]
    for family in se.FAMILIES:
        for source in se.SOURCES:
            x=se.source_vector(source)
            values={}
            for rate in (8192,16384,32768):
                raw=cp.raw_phase_samples(family,x,state["times"],sample_rate=rate)
                for psd in ("O4","O5"):
                    # Retain the original frozen injection, including its8192Hz
                    # generation. Vary ONLY recovery resolution in this control.
                    ids=[i for i,v in enumerate(labels[psd]) if v["source"]==source["name"]]
                    noise_indices=[labels[psd][i]["noise_index"]-50 for i in ids]
                    noise=noises[psd][noise_indices]
                    signal=state[psd+"_targets"][ids]-noise
                    norms=np.linalg.norm(signal,axis=1)
                    if np.max(np.abs(norms-40))>1e-10:
                        raise ValueError("Frozen injection no longer has SNR40")
                    snrs=(40.,200.,600.)
                    targets=np.vstack([signal*(snr/40.)+noise for snr in snrs])
                    bank=cp.make_bank(raw,"R-B",[0.,.37,1.],state[psd+"_white"])
                    logl,controls=cp.marginal_loglikes(bank,targets)
                    values[(rate,psd)]=(logl.reshape(3,3,len(ids)),controls,ids)
                print(json.dumps(dict(family=family,source=source["name"],rate_done=rate)),flush=True)
            for psd in ("O4","O5"):
                low,controls,ids=values[(8192,psd)]
                middle,mc,_=values[(16384,psd)]
                high,hc,_=values[(32768,psd)]
                for j,snr in enumerate((40.,200.,600.)):
                    for k,a in enumerate((0.,.37,1.)):
                        for injection_family in se.FAMILIES:
                            for injection_a in (0.,1.):
                                selection=np.array([labels[psd][i]["injection_family"]==injection_family and
                                    labels[psd][i]["injection_a"]==injection_a for i in ids])
                                one=float(np.max(np.abs(middle[k,j,selection]-low[k,j,selection])))
                                two=float(np.max(np.abs(high[k,j,selection]-middle[k,j,selection])))
                                rows.append(dict(recovery_family=family,source=source["name"],psd=psd,snr=snr,
                                    recovery_a=a,injection_family=injection_family,injection_a=injection_a,N=int(selection.sum()),
                                    change_8192_to_16384=one,change_16384_to_32768=two,
                                    first_rate_pass=one<=.1,second_rate_pass=two<=.1,
                                    largest_phase_grid=max(c["phase_grid"] for cs in (controls,mc,hc) for c in cs),
                                    max_phase_quadrature_error=max(c["error"] for cs in (controls,mc,hc) for c in cs)))
    summaries=[]
    for snr in (40.,200.,600.):
        selected=[r for r in rows if r["snr"]==snr]
        summaries.append(dict(snr=snr,cells=len(selected),pass8192=sum(r["first_rate_pass"] for r in selected),
            pass16384=sum(r["second_rate_pass"] for r in selected),
            max_change8192=max(r["change_8192_to_16384"] for r in selected),
            max_change16384=max(r["change_16384_to_32768"] for r in selected)))
    se.write(output,dict(status="HIGH_SNR_POINT_CONTROLS_ONLY",date_utc=datetime.now(timezone.utc).isoformat(),rows=rows,
        summary=summaries,scientific_acceptance=False,posterior_region_tested=False,
        scope="Frozen injection rescaled in SNR; all50 paired noises retained. These likelihoods at original source coordinates do not establish posterior evidence, coverage, or adequate injection resolution at SNR600.",
        hashes={str(p.relative_to(se.ROOT)):se.sha(p) for p in (se.Path(__file__),se.ROOT/"continuous_phase_source.py",pm.REG,se.ROOT/"INJECTIONS.npz")}))
    print(json.dumps(dict(status="HIGH_SNR_POINT_CONTROLS_ONLY",summary=summaries)),flush=True)


if __name__=="__main__":
    main()
