"""Build a proposal and analytic cost estimates only; no waveform, injection or PE."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, math, os

OUT=Path(__file__).resolve().parent
ROOT=Path(r"C:\IALD\Central de Patentes\Chatgpt")
V1=ROOT/"TUNEL/PARA_CHATGPT/ORDEM_018_INSUMOS/RAMO_B_V1__PREREGISTRO_RAMO_B_RINGDOWN_V1.json"
R5=ROOT/"ORDEM_013_RINGDOWN/bis/015/t03/R5/generation_4096/RESULT.json"
v1raw=V1.read_bytes();v1=json.loads(v1raw.decode("utf-8-sig"))
r5raw=R5.read_bytes();r5=json.loads(r5raw)
ALPHA_FINE_CODATA_2018=7.2973525693e-3
beta=ALPHA_FINE_CODATA_2018*math.sqrt(math.e)
def prediction(spin):
    root=math.sqrt(1-spin*spin)
    k=4*math.pi*(1+root)/root
    F=1.5251-1.1568*(1-spin)**0.1292
    Q=0.7000+1.4187*(1-spin)**(-0.4990)
    x=beta*k*F*Q
    return {"synthetic_remnant_spin":spin,"beta_runtime":beta,"k":k,"F_BCW":F,"Q_BCW":Q,"x":x,"delta_tau220":-x/(1+x)}
illustrations=[prediction(x) for x in (0.0,0.68,0.9)]
cpu_per=r5["cpu_seconds"]/r5["n_items"]
wall_per=r5["wall_seconds"]/r5["n_items"]
plan={
 "id":"ORDEM018_F3_D_SYNTHETIC_PILOT_PROPOSAL",
 "status":"PROPOSTA_NAO_RATIFICADA_NAO_EXECUTAVEL_COMO_JOB",
 "created_utc":datetime.now(timezone.utc).isoformat(),
 "authorized_now":"Metadata preparation, static code audit and pilot planning only.",
 "requires_new_concrete_contract_before_execution":True,
 "V1_sha256":hashlib.sha256(v1raw).hexdigest(),
 "scope":{"synthetic_only":True,"event_D_GPS_used_in_pilot":False,"observed_D_strain_or_posterior_used":False,
          "data_mock_note":"Only analytic PSD and independently seeded Gaussian noise; no offsource noise read either.",
          "hypothesis":"Full IMR pSEOBNRv4HM_PA with DTau220 as the only free deformation. GR higher modes remain in the waveform.",
          "fixed_deformations":{"domega220":0.0,"dtau440":0.0,"domega440":0.0},
          "test_claim":"Algorithm/cost pilot only; no event verdict, composite, precision or coverage claim."},
 "synthetic_design":{
   "source_fixtures":[
      {"id":"SYN_A","mass_1_detector_solar":50.0,"mass_2_detector_solar":35.0,"chi_1":0.3,"chi_2":0.1},
      {"id":"SYN_B_RESERVED","mass_1_detector_solar":90.0,"mass_2_detector_solar":60.0,"chi_1":0.7,"chi_2":0.3}],
   "mass_spin_note":"Arbitrary simulation fixtures. Not estimates from D. SYN_B is a reserved stress/cost case, not an automatic second PE.",
   "geometry":{"theta_jn":0.7,"ra":1.0,"dec":0.2,"psi":0.4,"phase":1.2,
               "geocent_time_synthetic_GPS":1000000000.0},
   "grid":{"duration_s":32.0,"sample_rate_hz":4096,"generation_sample_rate_hz":8192,
           "generation_maximum_frequency_hz":4096,"minimum_frequency_hz":20.0,
           "maximum_frequency_hz":1024.0,"reference_frequency_hz":20.0,"roll_off_s":0.4,
           "geocenter_seconds_after_segment_start":16.0},
   "grid_condition":"Validate conservative temporal margins over entire proposed prior before freeze. If too short, widen registered segment for every paired case before PE; do not reject prior samples as a fix.",
   "detectors":["H1","L1"],
   "PSD":{"kind":"Analytic design PSD","proposed_function":"lalsimulation.SimNoisePSDaLIGOZeroDetHighPower",
          "pin_required":"installed module/version and generated numeric PSD hash; verify function availability; no install",
          "qualification":"Strictly positive finite in analysis band; synthetic strain variance and one-sided normalization checks"},
   "SNR_definition":"Full IMR network optimal SNR in fixed synthetic PSD/band, not ringdown SNR.",
   "target_network_SNR_pilot":20.0,
   "reserved_SNR_stress":[12.0,30.0],
   "noise_and_pairing":"Stage source checks in zero noise; two paired pilot jobs use the same synthetic Gaussian noise seed and signal-source fixture, one GR and one RB. This is correlated by design, not two independent events.",
   "proposed_seeds":{"noise":180601,"sampler_GR":180602,"sampler_RB":180603},
   "seed_policy":"Freeze before waveform/recovery; known synthetic truth stored separately from any future D blind seed.",
   "RB_truth":"Compute remnant spin from the frozen GR remnant-conversion function for the synthetic progenitor; calculate DTau220 from V1 beta*k*N and exact -x/(1+x). Do not inject an arbitrary envelope or infer truth from a recovered posterior.",
   "remnant_condition":"Hash/freeze exact remnant fit and units in copied driver before generating truth. Mf_det used consistently; mass cancels in x for M_X=M_f.",
   "beta":{"ALPHA_FINE_CODATA_2018":ALPHA_FINE_CODATA_2018,"formula_runtime":"ALPHA_FINE_CODATA_2018 * sqrt(e)","computed":beta},
   "analytic_spin_illustrations_not_D_and_not_injection_results":illustrations,
   "recovery_priors_proposed":{
      "mass_1":{"kind":"Uniform","minimum":35.0,"maximum":110.0},
      "mass_2":{"kind":"Uniform","minimum":20.0,"maximum":80.0},
      "mass_ratio":{"kind":"Constraint","minimum":0.2,"maximum":1.0},
      "chi_1":{"kind":"Uniform","minimum":-0.8,"maximum":0.95},
      "chi_2":{"kind":"Uniform","minimum":-0.8,"maximum":0.95},
      "dtau220":{"kind":"Uniform","minimum":-0.8,"maximum":2.0},
      "domega220":0.0,"dtau440":0.0,"domega440":0.0,
      "luminosity_distance":{"kind":"Uniform","minimum":10.0,"maximum":10000.0},
      "theta_jn":{"kind":"Sine","minimum":0.0,"maximum":math.pi},
      "ra":{"kind":"Uniform","minimum":0.0,"maximum":2*math.pi,"boundary":"periodic"},
      "dec":{"kind":"Cosine","minimum":-math.pi/2,"maximum":math.pi/2},
      "psi":{"kind":"Uniform","minimum":0.0,"maximum":math.pi,"boundary":"periodic"},
      "phase":{"kind":"Uniform","minimum":0.0,"maximum":2*math.pi,"boundary":"periodic"},
      "geocent_time":{"kind":"Uniform","minimum":999999999.9,"maximum":1000000000.1}},
   "prior_conditions":"Proposal for synthetic cost pilot only; not an amendment of V1 D priors. Verify rescaled distance and synthetic RB truth are strictly inside support before freeze. No posterior-driven prior change.",
   "sampler_proposal":{"backend":"bilby/dynesty","nlive":256,"walks":25,"dlogz":0.1,"maxcall_per_job":10000,
                       "workers":1,"wall_cap_seconds_per_job":3600,"check_point":False,"check_point_plot":False},
   "convergence_scope":"A maxcall/deadline exit is a cost measurement, not a converged posterior. No C2 acceptance or coverage from an unconverged pilot."},
 "ordered_stages":[
  {"stage":"P0_CONTRATO","action":"Review proposal, approve synthetic-only copied-driver contract and resource caps; preserve V1 and D holds.",
   "continue_if":"Exact instrument/PSD/remnant/config/seed hashes frozen; no D data paths admitted."},
  {"stage":"P1_ADAPTADOR_COPIADO","action":"In a new authorized working copy, add a separate synthetic-noise path, fix numeric fixed-prior handling, forward generation fields. Keep real-data guards intact. No changes now.",
   "controls":["Reject real data paths and real event identifiers in synthetic mode","Truth validation supports numeric fixed values and rejects disagreement",
               "All three fixed deformations remain exactly zero in injection and recovery",
               "Fresh LAL dictionaries; GR->RB->GR call sequence reproduces first GR waveform",
               "Adapter transfers generation8192/max4096 and exact common FFT bins",
               "Cost/deadline counters and atomic failure receipts; no hidden restart"],
   "planned_native_calls_at_most":120,"native_CPU_proxy_seconds":120*cpu_per,"planning_wall_cap_seconds":900},
  {"stage":"P2_INJECAO_FONTE","action":"Generate SYN_A GR/RB and one reserved stress fixture; measure PSD normalization, temporal margins, finite/nonzero polarization, exact injected deformation and SNR scaling. Generate no event data.",
   "controls":["GR at DTau220=0 has exact parameter identity; numerical residual tolerance frozen before measurement",
               "RB truth from runtime beta and preregistered law, not from fit",
               "Units, reference frequency, data/generation grids equal between injection/recovery",
               "SNR target reached to rtol1e-8/atol1e-10 as in resident adapter",
               "No truncation of tail or event labels; retain failure cases"],
   "planned_native_calls_at_most":32,"native_CPU_proxy_seconds":32*cpu_per,"planning_wall_cap_seconds":600},
  {"stage":"P3_DOIS_PE_SINTETICOS_CUSTO","action":"Only after P0-P2 and authorized launch: paired SYN_A GR/RB, 2 jobs, at most10000 likelihood calls each, one worker, 3600s per-job cap.",
   "native_CPU_proxy_seconds":20000*cpu_per,"planning_wall_cap_seconds":7200,
   "outputs":["versions/config/seed/code/PSD hashes","commands/return codes/log hashes","likelihood and waveform call counts",
              "CPU/wall/RSS","convergence/ESS/evidence error diagnostics","synthetic-only bias diagnostics with uncertainty","finite failure list"]},
  {"stage":"P4_REPLANEJAR_C2","action":"Use measured pilot call rate/convergence to propose a separate injection campaign and prefreeze its sample count and tests; do not extrapolate success from two draws.",
   "sizing":"For binomial coverage p~0.9 and desired SE<=0.03, n>=ceil(0.9*0.1/0.03^2)=100 independent recoveries per cell is a planning proxy only. Exact binomial interval and target precision must be ratified.",
   "C2_bias":"Require |mean bias|<=0.2*|delta_pred| with a prespecified uncertainty criterion. A single successful injection does not establish it.",
   "not_executed":True}],
 "failure_tree":[
   "If the synthetic path cannot reject real data or preserve fixed zeros, record measured failing control; correct only the authorized copy and repeat affected controls.",
   "If source EDOM occurs at qualified8192/max4096, retain parameters/return code/log/cost, consult existing R5 case identity and temporal margins; do not silently shrink prior or change waveform family.",
   "If temporal bounds fail, compute required registered duration and its cost, amend the synthetic contract before any paired recovery; preserve equal conditions.",
   "If PE hits call/time limit, report actual calls/CPU/ESS/return code as a partial cost measurement; no automatic extension, restart or event-D fallback.",
   "If the tree reaches its registered cap, deliver the measurement and remaining alternatives to management. This is not a declaration of a physical/technical wall."],
 "cost":{
  "basis":{"path":str(R5),"sha256":hashlib.sha256(r5raw).hexdigest(),"status":r5["status"],
           "n_source_items":r5["n_items"],"historical_CPU_seconds":r5["cpu_seconds"],"historical_wall_seconds":r5["wall_seconds"]},
  "historical_CPU_seconds_per_source_item":cpu_per,"historical_wall_seconds_per_source_item":wall_per,
  "total_P1_P2_P3_source_calls_proxy":20152,
  "total_native_CPU_proxy_seconds":20152*cpu_per,
  "three_times_native_proxy_for_planning_seconds":3*20152*cpu_per,
  "planning_multiplier":3.0,"multiplier_status":"INPUT allowance, not measured likelihood overhead or guarantee",
  "proposed_total_wall_cap_seconds_P1_P2_P3":8700,
  "actual_waveforms_injections_PE_this_delivery":0,
  "actual_compute_for_new_pilot_seconds":0.0,
  "new_remote_calls":0,
  "paid_infrastructure":"Not contracted or installed. Local-only proposal; no cloud cost commitment.",
  "limitations":"Historical source-only CPU/wall is not a new pilot, likelihood benchmark, full PE cost or cost of 14 D events. No linear event-count promise.",
  "next_estimator":"For each proposed future campaign, measured T_wave+likelihood overhead, observed Ncalls distribution and job wall/CPU/RSS replace this proxy; account for repeated seeds and concurrency explicitly."},
 "data_readiness_remaining":[
  "Ratify GPS metadata completion and exact GR source-table provenance; keep V1 list and four holds.",
  "Freeze D PSD/DQ/offsource/exclusion artifacts in a distinct authorized stage. No PSD file was identified in named manifests; do not equate a32s strain slice with a ready PSD.",
  "Qualify exact copied synthetic adapter/driver and registration before PE.",
  "A pilot and any future blinded D sigma collection are distinct steps. Do not read D centers to plan either."
 ]}
def write(name,value):
    p=OUT/name;raw=(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode()
    if p.exists():
        old=p.read_bytes();bak=p.with_name(p.name+".bak_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f"));bak.write_bytes(old);assert bak.read_bytes()==old
    tmp=p.with_name(p.name+".tmp_"+str(os.getpid()));tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,p)
write("PLANO_PILOTO_SINTETICO_SO220.json",plan)
print(json.dumps({"beta_runtime":beta,"illustrations":illustrations,"source_CPU_proxy_s":plan["cost"]["total_native_CPU_proxy_seconds"],
                  "plan_sha256":hashlib.sha256((OUT/"PLANO_PILOTO_SINTETICO_SO220.json").read_bytes()).hexdigest()}))
