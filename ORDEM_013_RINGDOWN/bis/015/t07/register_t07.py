"""Create the immutable T07(a) preregistration from source bytes."""
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path
b=Path(r"C:\IALD\Central de Patentes\Chatgpt")
root=b/"ORDEM_013_RINGDOWN"
d=root/"bis/015/t07"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=[
"C7_COHERENT_SOURCE_REPRODUCTION_v3/coherent_imr_model.py",
"C7_COHERENT_SOURCE_REPRODUCTION_v3/tgl_ringdown_prediction.py",
"C7_COHERENT_SOURCE_REPRODUCTION_v3/nonlinear_coherent_recovery.py",
"C7_COHERENT_SOURCE_REPRODUCTION_v3/QNM_GRID.json",
"C7_COHERENT_SOURCE_REPRODUCTION_v3/cache/recolored_noise/O4_noise.npz",
]
reg={
"status":"REGISTERED_T07_A_NONBLIND_LOCAL_CONSTRUCTIVE_SEARCH",
"registered_utc":datetime.now(timezone.utc).isoformat(),
"opening_sha256":sha(b/"TUNEL/DO_CHATGPT/ENTREGA_016_ABERTURA_operador.md"),
"order_015_sha256":sha(b/"TUNEL/PARA_CHATGPT/ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md"),
"budget_v8_sha256":sha(root/"ORCAMENTO_015_v8.json"),
"source_sha256":{x:sha(root/x) for x in rel},
"runner_sha256":sha(d/"source_free_local.py"),
"source":{"name":"reference","mass":72.0,"q":39/33,"s1":0.05,"s2":-0.03,"inclination":0.6,"phase":0.37,"psi":0.0},
"family":"SEOBNRv4HM","psd":"O4","reference_SNR":40,
"readings":["R-B","R-MOD","R-RAIZ-0","R-LIN"],
"injection_a":[0.0,1.0],"recovery_a":0.0,
"n_samples":410,"sample_rate":2048,
"optimizer":"Powell with same per-stage maxfev 150 then 350 for every reading, fixed bounds/steps from pinned C7 script",
"maxfev_stages":[150,350],"hardcap_wall_seconds":3600,
"status_rule":"maxfev exit is NOT optimizer convergence. Local candidate residual is upper bound on global mismatch, not calibrated z, Bayes factor or physical exclusion.",
"no_blind_data":True,"gate_changed":False,
}
p=d/"T07_REGISTRATION.json"
data=(json.dumps(reg,ensure_ascii=False,indent=2)+"\n").encode()
with p.open("xb") as f:f.write(data)
assert p.stat().st_size==len(data)
print(json.dumps({"registration_sha256":sha(p),"runner_sha256":reg["runner_sha256"],"source_count":len(rel)}))

