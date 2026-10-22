"""Metadata-only proposal for F3/D. Never imports bench code or opens strain/posteriors."""
from pathlib import Path
import ast, csv, hashlib, io, json, os, time
from datetime import datetime, timezone

OUT=Path(__file__).resolve().parent
ROOT=Path(r"C:\IALD\Central de Patentes\Chatgpt")
BENCH=ROOT/"ORDEM_013_RINGDOWN/bis"
V1=ROOT/"TUNEL/PARA_CHATGPT/ORDEM_018_INSUMOS/RAMO_B_V1__PREREGISTRO_RAMO_B_RINGDOWN_V1.json"
CAT=Path(r"C:\IALD\Bancada_Um\investigacao\fase6_eco_radical_01out\catalogo_v3.csv")
STRAIN_MANIFEST=Path(r"C:\IALD\Bancada_Um\fontes_externas\gwosc_o4\GWOSC_O4_32S_V1.manifest.json")
PROTOCOL=ROOT/"TUNEL/PARA_CHATGPT/ORDEM_015_INSUMOS/PROTOCOLO_ANTI_PAREDE.md"
ALLOWED={V1,CAT,STRAIN_MANIFEST,PROTOCOL}
ALLOWED.update(BENCH/("e2_code_v1_1_2/"+n) for n in ("pseob_source.py","pe_runner.py","injection_design.py","strain_io.py","temporal_contract.py","registration_guard.py","synthetic_null.py"))
RECEIPTS=("015/t03/R5/INPUT_MANIFEST.json","015/t03/R5/generation_4096/RESULT.json","015/t03/source_tests_001/RESULT.json","015/t03/native_bin_control_001/RESULT.json","015/t03/chain_tests_002/RESULT.json","015/t03/R5_SOURCE_CLOSING.json","015/t03/SOURCE_DELIVERY.json","015/t08/T08_PE_METADATA_INDEX.json","015/t07/T07_DOWNLOAD_PLAN_v3.json","015/t07/T07_ONSOURCE_QUALITY_AUDIT.json")
ALLOWED.update(BENCH/x for x in RECEIPTS)
ALLOWED.update(BENCH/("015/t08/ZENODO_"+str(n)+"_METADATA.json") for n in (17602505,20348005,20348006))
sources={}
def read_doc(p):
    p=Path(p)
    assert p in ALLOWED, "Not in metadata/code allowlist"
    assert p.suffix in (".json",".csv",".md",".py")
    raw=p.read_bytes()
    sources[str(p)]={"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),"scope":"metadata/code only"}
    return raw.decode("utf-8-sig")
def jread(p): return json.loads(read_doc(p))
def atomic_json(name,value):
    p=OUT/name;raw=(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode("utf-8")
    if p.exists():
        old=p.read_bytes();bak=p.with_name(p.name+".bak_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        bak.write_bytes(old);assert bak.read_bytes()==old
    tmp=p.with_name(p.name+".tmp_"+str(os.getpid()));tmp.write_bytes(raw)
    assert tmp.stat().st_size==len(raw) and tmp.read_bytes()==raw
    os.replace(tmp,p);assert p.read_bytes()==raw
    return hashlib.sha256(raw).hexdigest()
def win_path(value):
    if value.startswith("/mnt/c/"): return Path("C:/"+value[7:])
    return Path(value)
def stat_only(value,declared_size=None):
    p=win_path(value)
    # Content is deliberately never opened, including for a fresh digest.
    try:
        st=p.stat()
        return {"path":str(p),"exists":True,"bytes":st.st_size,"mtime_ns":st.st_mtime_ns,
                "declared_size_matches":None if declared_size is None else st.st_size==declared_size,
                "content_opened":False,"content_hash_recomputed":False}
    except OSError as e: return {"path":str(p),"exists":False,"error":str(e),"content_opened":False}

started=time.perf_counter()
v=jread(V1);d=v["conjuntos"]["D"];names=d["eventos_elegiveis"];holds=d["com_data_quality_hold"]
assert len(names)==14 and len(set(names))==14 and len(holds)==4 and set(holds)<=set(names)
catalog=list(csv.DictReader(io.StringIO(read_doc(CAT))))
sm=jread(STRAIN_MANIFEST)
read_doc(PROTOCOL)
source_pins=[]
for p in (CAT,STRAIN_MANIFEST):
    declared=[x for x in v["fontes"] if Path(x["caminho"]).name==p.name]
    assert len(declared)==1
    actual=sources[str(p)]
    source_pins.append({"path":str(p),"declared":declared[0],"actual":actual,"matches":actual["sha256"]==declared[0]["sha256"] and actual["bytes"]==declared[0]["bytes"]})
assert all(x["matches"] for x in source_pins)
gr_index=jread(BENCH/"015/t08/T08_PE_METADATA_INDEX.json")
gr_release_checks=[]
for release in gr_index["rows"]:
    p=BENCH/("015/t08/ZENODO_"+str(release["record_id"])+"_METADATA.json")
    jread(p)
    gr_release_checks.append({"record_id":release["record_id"],"metadata_path":str(p),"matches_index":sources[str(p)]["sha256"]==release["sha256"]})
assert all(x["matches_index"] for x in gr_release_checks)
pred={x["evento"]:x for x in d["previsao_da_hipotese_por_evento_INFORMACAO_CEGA"]}
t07_plan=jread(BENCH/"015/t07/T07_DOWNLOAD_PLAN_v3.json")
t07_quality=jread(BENCH/"015/t07/T07_ONSOURCE_QUALITY_AUDIT.json")
rows=[]
for ordinal,event in enumerate(names,1):
    matches=[x for x in catalog if x["commonName"]==event]
    assert len(matches)==1
    cat=matches[0];gps=float(cat["GPS"])
    series=[x for x in sm["series"] if x["event"]==event]
    assert len(series)==2 and {x["det"] for x in series}=={"H1","L1"}
    refs=[]
    for release in gr_index["rows"]:
        for f in release["files"]:
            if event in f["key"]:
                refs.append({"record_id":release["record_id"],"record_url":release["url"],"release_title":release["title"],
                            "release_updated":release["updated"],"license":release["license"],"file_descriptor":f,
                            "posterior_content_opened":False,"local_posterior_presence_not_searched":True})
    assert len(refs)==1
    series_out=[]
    for s in series:
        end=float(s["t0"])+int(s["n"])/float(s["fs"])
        series_out.append({
            "detector":s["det"],"official_url":s["url"],
            "hdf5":stat_only(s["hdf5"],s["hdf5_bytes"]),"hdf5_sha256_DECLARED_IN_PINNED_MANIFEST":s["hdf5_sha256"],
            "npz":stat_only(s["npz"]),"npz_sha256_DECLARED_IN_PINNED_MANIFEST":s["npz_sha256"],
            "manifest_status":s["status"],"manifest_nan":s["nan"],"sample_rate_hz":s["fs"],
            "n":s["n"],"t0":s["t0"],"end_exclusive":end,"GPS_inside_manifest_window":float(s["t0"])<=gps<end,
            "URL_listed_in_catalog_files_4k":s["url"] in cat["files_4k"],
            "quality_reassessed":False})
    gr={k:pred[event][k] for k in ("SNR_rede_GWOSC","Mf_det_mediana_GR","chi_f_mediana_GR","metadata_origin")}
    assert float(cat["network_matched_filter_snr"])==float(gr["SNR_rede_GWOSC"])
    rows.append({
        "ordinal_V1":ordinal,"event":event,"candidate_list_status":"PRESERVED_V1_NOT_RATIFIED",
        "GPS_V1":d["gps_lido_do_5SIGMA"].get(event),"GPS_proposed":gps,"GPS_text_as_catalog":cat["GPS"],
        "GPS_status":"REAL_READ_IN_PINNED_RESIDENT_CATALOG; exact publication timing precision not independently remeasured",
        "catalog":cat["catalog.shortName"],"catalog_version":cat["version"],"data_quality_hold":event in holds,
        "hold_status":"PRESERVED_NO_REASSESSMENT","series":series_out,
        "GR_metadata_in_V1":gr,"GR_metadata_status":"DECLARADO_IN_V1; source table values not newly verified",
        "GR_release_metadata":refs,
        "catalog_GR_allowed_fields":{k:cat[k] for k in ("final_mass_source","redshift","network_matched_filter_snr")},
        "source_frame_mass_times_1_plus_z_DIAGNOSTIC_ONLY":float(cat["final_mass_source"])*(1+float(cat["redshift"])),
        "not_a_replacement_for_Mf_det":"median(M_source)*(1+median(z)) is not generally median(M_detector)",
        "PSD":{"status":"NOT_IDENTIFIED_IN_NAMED_MANIFESTS; not a global absence claim",
               "strain_manifest_has_PSD_descriptor":any("psd" in k.lower() for k in series[0]),
               "T07_named_plan_rows":sum(x.get("event")==event for x in t07_plan["files"]),
               "T07_named_quality_rows":sum(x.get("event")==event for x in t07_quality["rows"]),
               "required_next_step":"A distinct authorized data-preparation stage must freeze offsource windows, DQ, exclusion, estimator and PSD hash before event PE."}})
assert all(x["GPS_V1"] is None for x in rows)
summary={
 "n_candidates":len(rows),"n_GPS_resolved_in_proposal":len(rows),"n_holds_preserved":len(holds),
 "n_no_hold_preserved":len(d["elegiveis_sem_hold"]),
 "n_hdf5_exist":sum(s["hdf5"]["exists"] for r in rows for s in r["series"]),
 "n_npz_exist":sum(s["npz"]["exists"] for r in rows for s in r["series"]),
 "n_hdf5_size_match":sum(s["hdf5"].get("declared_size_matches") is True for r in rows for s in r["series"]),
 "n_GPS_covered_by_named_series":sum(s["GPS_inside_manifest_window"] for r in rows for s in r["series"]),
 "n_official_URLs_agree_catalog_manifest":sum(s["URL_listed_in_catalog_files_4k"] for r in rows for s in r["series"]),
 "n_GR_release_descriptors":sum(len(r["GR_release_metadata"]) for r in rows)}
metadata={
 "status":"PROPOSTA_DE_MANIFESTO_METADATA_NAO_RATIFICADA","created_utc":datetime.now(timezone.utc).isoformat(),
 "scope":"Identidade/GPS/existencia por stat/metadados GR. Sem strain, posterior ou delta_tau observado.",
 "source_V1":str(V1),"source_V1_sha256":sources[str(V1)]["sha256"],
 "original_candidate_order":names,"four_holds":holds,"V1_unchanged":hashlib.sha256(V1.read_bytes()).hexdigest()==sources[str(V1)]["sha256"],
 "ratified":False,"gate_changed":False,"source_pin_checks":source_pins,"GR_release_metadata_pin_checks":gr_release_checks,
 "summary":summary,"events":rows,
 "bounds":{"strain_contents_read":False,"posterior_contents_read":False,"observed_delta_tau_read":False,
           "PE_executed":False,"canonical_original_executed":False,"private_directories_opened":False,
           "instrument_only_static_read":True,"remote_model_calls":0,"packages_installed":0}}
codes=[]
r5=jread(BENCH/"015/t03/R5/INPUT_MANIFEST.json")
for p in sorted(x for x in ALLOWED if x.suffix==".py"):
    text=read_doc(p);tree=ast.parse(text)
    codes.append({"path":str(p),"sha256":sources[str(p)]["sha256"],"bytes":sources[str(p)]["bytes"],
                  "R5_whole_file_sha256":r5["source_tree"].get(p.name),
                  "R5_whole_file_match":r5["source_tree"].get(p.name)==sources[str(p)]["sha256"],
                  "functions":[{"name":n.name,"line":n.lineno} for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))]})
controls=[]
for rel in RECEIPTS:
    if "t03" not in rel or rel.endswith("INPUT_MANIFEST.json"): continue
    control=jread(BENCH/rel)
    controls.append({"path":str(BENCH/rel),"sha256":sources[str(BENCH/rel)]["sha256"],
                     "declared_status":control.get("status"),
                     "allowed_metrics":{k:control[k] for k in ("n_items","status_counts","crashes","wall_seconds","cpu_seconds","strain_read","PE_run","native_waveforms","source_runtime_scope","source_cpu_seconds_measured","source_wall_seconds_measured") if k in control},
                     "tests_names":control.get("tests"),
                     "note":"Existing receipt inspected and hashed; its execution was not repeated."})
instrument={
 "status":"INSTRUMENTO_RESIDENTE_IDENTIFICADO__ADAPTACAO_SINTETICA_SO220_PENDENTE",
 "code":codes,"prior_control_receipts":controls,
 "gaps":[
 "injection_design.inject_into_ifos requires REAL_OFFSOURCE and real event ids/GPS, so it cannot be used unchanged for this synthetic-only pilot.",
 "validate_truth_support assumes dict priors for all deformation coordinates; pe_runner permits numeric fixed deformations. The proposed only-DTau220 variant therefore needs a separately tested fixed-prior handling path.",
 "inject_into_ifos does not forward generation_maximum_frequency_hz/generation_sample_rate_hz required by current pseob_frequency_domain.",
 "pe_runner whole-file hash differs from R5 INPUT_MANIFEST. This audit does not infer that later changes are unsafe or qualified; pin/qualify the exact copied driver.",
 "R5/SOURCE receipts qualify the source, not activation, final registration or complete injection/PE pipeline."],
 "reusable_controls":[
 "Fresh LAL dictionary every waveform call; duplicate overrides prohibited.",
 "Native ringdown buffer bound checked before LAL; EDOM receipt plus call/time count.",
 "Generation Nyquist 4096 Hz/sample rate 8192 Hz, common Fourier bins restricted to analysis data without interpolation.",
 "Shared conservative temporal bounds abort out-of-window configurations; do not trim priors after failure.",
 "Strain reader pins content, checks quality/finiteness, chooses first valid fixed-length offsource block and Welch Hann/50%/median PSD. Not run here.",
 "Physical masses/spins remain free in recovery; explicit fixed zeros for DOmega220/DTau440/DOmega440; deformation only DTau220, not removal of GR higher harmonics."],
 "qualification_scope":"Only codes and historical receipts; zero new source generation, injection or PE."}
meta_hash=atomic_json("PROPOSTA_MANIFESTO_METADATA_D.json",metadata)
inst_hash=atomic_json("AUDITORIA_INSTRUMENTO_SO220.json",instrument)
audit={"status":"METADATA_PREPARATION_COMPLETED_NOT_RATIFIED","source_inventory":sources,"summary":summary,
       "outputs":{"PROPOSTA_MANIFESTO_METADATA_D.json":meta_hash,"AUDITORIA_INSTRUMENTO_SO220.json":inst_hash},
       "wall_seconds_this_metadata_audit":time.perf_counter()-started,"bounds":metadata["bounds"],
       "discovery_note":"A prior filename search reported access denied in an E2_PRIVATE subtree; no content was read and that subtree was not retried."}
audit_hash=atomic_json("AUDITORIA_METADATA_D.json",audit)
print(json.dumps({"summary":summary,"metadata_sha256":meta_hash,"instrument_sha256":inst_hash,"audit_sha256":audit_hash},ensure_ascii=False))
