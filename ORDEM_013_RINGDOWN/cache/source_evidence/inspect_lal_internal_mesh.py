"""Calculate the actual SEOB high-rate mesh from the exact installed source."""
from datetime import datetime, timezone
import json
import math
import lal
import source_evidence as se


def main():
    directory = se.ROOT/"lal_generator_source_gitlab"
    source = directory/"LALSimIMRSpinAlignedEOB.c"
    provenance = json.loads((directory/"PROVENANCE.json").read_bytes())
    if se.sha(source) != provenance["sha256"]:
        raise ValueError("Primary source changed")
    lines = source.read_text().splitlines()
    needles = ["const REAL8 EPS_ABS = 1.0e-10", "const REAL8 EPS_REL = 1.0e-9",
               "resampEstimate = 50. * deltaT / mTScaled", "resampPwr = (UINT4) ceil (log2 (resampEstimate))",
               "resampFac *= 2u", "deltaTHigh = deltaT / (REAL8) resampFac",
               "nStepBack = ceil (tStepBack / odeStep/ mTScaled)", "hiSRndx = retLen - nStepBack",
               "fmod (rdMatchPoint->data[1], deltaTHigh / mTScaled)"]
    anchors = {}
    for needle in needles:
        found = [i+1 for i,line in enumerate(lines) if needle in line]
        if len(found) != 1:
            raise ValueError("Primary source formula absent or ambiguous: "+needle)
        anchors[needle] = found[0]
    rows = []
    for physical in se.SOURCES:
        mt = physical["mass"]*lal.MTSUN_SI
        for rate in (8192,16384,32768,65536,131072,262144,524288):
            dt = 1./rate
            estimate = 50.*dt/mt
            factor = 2**math.ceil(math.log2(estimate)) if estimate > 1. else 1
            rows.append(dict(source=physical["name"], total_mass_solar=physical["mass"], output_rate=rate,
                             resample_factor=factor, internal_deltaT_s=dt/factor,
                             internal_deltaT_over_M=dt/(factor*mt),
                             internal_rate=factor*rate))
    selected = [r for r in rows if r["source"] == "source_90" and r["output_rate"] in (32768,65536,131072)]
    if len({r["internal_rate"] for r in selected}) != 1:
        raise ValueError("Expected plateau calculation differs")
    result = dict(status="SOURCE_VERIFIED_INTERNAL_MESH_PLATEAU", date_utc=datetime.now(timezone.utc).isoformat(),
                  source_url=provenance["url"], source_commit=provenance["installed_commit"], source_sha256=se.sha(source),
                  source_lines=anchors, table=rows,
                  derived_fact="For source90 all three output rates32768/65536/131072 use the same131072Hz internal high-rate grid. Fixed ODE tolerances remain1e-10 absolute and1e-9 relative.",
                  limitation="The initial low-rate trajectory and step-back origin still change; this calculation is not a runtime trace and does not prove a unique cause of the residual. No generator or installed library modified.",
                  next_control="A source90 output rate262144 or524288 genuinely halves the high-rate grid. Use a memory-bounded selected-source control first; source72/source64 retain a plateau longer. ODE tolerances are separately fixed in this implementation.")
    se.write(se.ROOT/"LAL_INTERNAL_MESH_AUDIT.json", result)
    print(json.dumps(dict(status=result["status"], source90=[r for r in rows if r["source"]=="source_90"])),flush=True)


if __name__=="__main__":
    main()
