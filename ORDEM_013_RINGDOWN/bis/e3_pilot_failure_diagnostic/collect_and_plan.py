"""Archive read-only source evidence and publish a bounded plan before waveforms."""
import hashlib
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
B = HERE.parents[1]
ROOT = B.parent


def digest(raw): return hashlib.sha256(raw).hexdigest()


def save(path, raw):
    if path.exists():
        if path.read_bytes() != raw: raise ValueError('Existing evidence differs; no overwrite')
        return
    with path.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    if path.stat().st_size != len(raw): raise OSError("Incomplete diagnostic artifact")


def main():
    if os.name != "posix" or Path(sys.prefix).resolve() != Path("/opt/lal_env"):
        raise RuntimeError("Pinned WSL environment required")
    folder = HERE / "sources"
    folder.mkdir(exist_ok=True)
    installed = Path("/opt/lal_env/lib/python3.12/site-packages")
    files = {
        "bilby_gw_source.py": installed / "bilby/gw/source.py",
        "bilby_base_sampler.py": installed / "bilby/core/sampler/base_sampler.py",
        "bilby_prior_dict.py": installed / "bilby/core/prior/dict.py",
        "bilby_random.py": installed / "bilby/core/utils/random.py",
        "lal_git_version.py": installed / "lalsimulation/git_version.py",
        "pseob_source.py": B / "bis/e2_code/pseob_source.py",
        "temporal_contract.py": B / "bis/e2_code/temporal_contract.py",
        "pe_runner.py": B / "bis/e2_code/pe_runner.py",
    }
    evidence = []
    for name, path in files.items():
        raw = path.read_bytes()
        save(folder / name, raw)
        evidence.append({"original_path": str(path), "copy": str(folder / name), "sha256": digest(raw), "bytes": len(raw)})
    import re
    version = (folder / "lal_git_version.py").read_text()
    commit = re.search(r'^id = "([0-9a-f]{40})"', version, re.M).group(1)
    for name in ("LALSimIMRSpinAlignedEOB.c", "LALSimInspiralGeneratorConditioning.c", "LALSimInspiral.c"):
        doxygen_names = {'LALSimIMRSpinAlignedEOB.c':'_l_a_l_sim_i_m_r_spin_aligned_e_o_b_8c_source.html',
                         'LALSimInspiralGeneratorConditioning.c':'_l_a_l_sim_inspiral_generator_conditioning_8c_source.html',
                         'LALSimInspiral.c':'_l_a_l_sim_inspiral_8c_source.html'}
        url = 'https://lscsoft.docs.ligo.org/lalsuite/7.26/lalsimulation/' + doxygen_names[name]
        with urllib.request.urlopen(url, timeout=20) as response:
            raw = response.read(5_000_001)
        if len(raw) > 5_000_000: raise ValueError("Source size cap")
        save(folder / (name+'.html'), raw)
        from html.parser import HTMLParser
        class Lines(HTMLParser):
            def __init__(self): super().__init__(); self.level=0; self.parts=[]; self.lines=[]
            def handle_starttag(self, tag, attrs):
                if tag=='div' and dict(attrs).get('class')=='line': self.level=1; self.parts=[]
                elif self.level and tag=='div': self.level+=1
            def handle_endtag(self,tag):
                if self.level and tag=='div':
                    self.level-=1
                    if not self.level: self.lines.append(''.join(self.parts))
            def handle_data(self,data):
                if self.level: self.parts.append(data)
        parser=Lines(); parser.feed(raw.decode()); extracted='\n'.join(parser.lines)+'\n'
        save(folder / name, extracted.encode())
        evidence.append({"primary_url": url, "source_commit": commit, "copy": str(folder/name), "sha256": digest(raw), "bytes": len(raw),
                         "source_identity_scope": "Official versioned 7.26 documentation; its VCS header declares installed commit/tag. Binary reproducibility not established; initial GitHub commit URL returned 404."})
    reg_path = B / "RINGDOWN_5SIGMA_V1.json"
    reg = json.loads(reg_path.read_bytes())
    cfg = reg["pe_jobs"]["GW250114_PILOT"]
    run = B / "cache/E3_PSEOB_PILOT_V1"
    controller = json.loads((run / "CONTROLLER.json").read_bytes())
    if controller["blind"] is not False or controller["job"] != "GW250114_PILOT":
        raise ValueError("Only explicitly authorized calibration logs")
    if digest((run/"PRIVATE.log").read_bytes()) != controller["private_log_sha256"]:
        raise ValueError("Calibration log changed")
    for name in ("CONTROLLER.json", "PRIVATE.log"):
        raw = (run/name).read_bytes()
        save(folder/("original_"+name), raw)
        evidence.append({"original_path": str(run/name), "copy": str(folder/("original_"+name)), "sha256": digest(raw), "bytes": len(raw)})
    budget = json.loads((ROOT/reg["budget_relative_to_Chatgpt"]).read_bytes())
    started = datetime.now(timezone.utc)
    hard = datetime.fromisoformat(budget["hard_deadline_utc"])
    plan = {"status": "INPUTS_RECORDED_BEFORE_ANY_DIAGNOSTIC_WAVEFORM", "created_utc": started.isoformat(),
      "deadline_utc": min(hard, started+timedelta(seconds=600)).isoformat(), "total_wall_cap_seconds": 600,
      "per_child_wall_cap_seconds": 45, "max_sequential_waveform_children": 10, "workers_per_child": 1,
      "thread_caps": 1, "core_dumps": "DISABLED", "child_process_group": "owned isolated group, kill on timeout",
      "registration_sha256": digest(reg_path.read_bytes()), "pilot_configuration_INPUT": cfg,
      "scope": "No strain/posterior, no PE/likelihood. Finite source-only calls and prior-draw replay only. No source/runtime edits.",
      "planned_prior_replay": "At most eight constrained prior samples with registered calibration sampler seed; no likelihood. Match physical SI tuples printed in original log before assigning exact draw identity.",
      "planned_waveform_inputs": [
        {"case": "LOW_GR", "mass_1": 21.0, "mass_2": 13.0, "chi_1": -0.14, "chi_2": -0.058, "dtau220": 0.0, "dtau440": 0.0, "domega220": 0.0, "domega440": 0.0},
        {"case": "LOW_DEFORMED", "mass_1": 21.0, "mass_2": 13.0, "chi_1": -0.14, "chi_2": -0.058, "dtau220": 0.3, "dtau440": 1.0, "domega220": 0.8, "domega440": 1.5},
        {"case": "MID_GR", "mass_1": 40.0, "mass_2": 30.0, "chi_1": 0.1, "chi_2": -0.1, "dtau220": 0.0, "dtau440": 0.0, "domega220": 0.0, "domega440": 0.0}],
      "common_diagnostic_parameters": {"luminosity_distance": 1000.0, "theta_jn": 0.8, "phase": 0.3,
        "geocent_time": 1420878141.2, "minimum_frequency": 20.0, "reference_frequency": 20.0,
        "duration_s": 16, "frequency_grid_nyquist_hz": 2048, "analysis_band_upper_hz": 1024},
      "generation_fmax_variants_INPUT": [1024, 2048, 8192],
      "interpretation": "fmax variants are isolated diagnostics, not approval to change registered science band or prior. Never suppress higher modes or reject prior region to obtain success.",
      "adaptive_choice": "Within the ten-child cap: prioritize exact replay matches if established; otherwise representative cases. Write each complete case input before native call. No repeated search until pass.",
      "source_evidence": evidence, "planner_sha256": digest(Path(__file__).read_bytes()),
      "waveforms_executed_at_plan_time": 0}
    save(HERE/"PLAN_INPUTS.json", (json.dumps(plan,indent=2)+"\n").encode())
    print(json.dumps({"plan_sha256": digest((HERE/"PLAN_INPUTS.json").read_bytes()), "deadline_utc": plan["deadline_utc"], "source_files": len(evidence)}))


if __name__ == "__main__": main()
