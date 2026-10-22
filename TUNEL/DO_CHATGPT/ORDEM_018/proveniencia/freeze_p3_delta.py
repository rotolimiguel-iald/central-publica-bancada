from pathlib import Path
import json,difflib,datetime
from audit_provenance import OUT,atomic,metadata
b=OUT.parent/'preregistros'/'conjunto_d'/'p3_preparacao';s=OUT/'p3_review_snapshot'
old=json.loads((s/'CONTRATO_P3.json').read_text());new=json.loads((b/'CONTRATO_P3.json').read_text())
print('Changed contract top-level fields:',[k for k in new if old.get(k)!=new[k]])
for k in new:
 if old.get(k)!=new[k] and k not in ['inputs']:print(k,json.dumps(new[k],ensure_ascii=False))
print((b/'ADENDO_P3_01_EXCECOES_V2.md').read_text(encoding='utf-8'))
paths=['CONTRATO_P3.json','driver_p3.py','failure_audit.py','MANIFESTO_P3_PREPARADO_V2.json','CONTROLES_EXCECOES_P3_V2_FINAL.json','CONTROLES_PREPARACAO_V2_FINAL.json','COMANDO_EXATO_NAO_EXECUTADO.json','ADENDO_P3_01_EXCECOES_V2.md']
d=OUT/'p3_delta_snapshot';d.mkdir(exist_ok=True);sources=[]
for name in paths:
 m,raw=metadata(b/name);sources.append(m);dest=d/name
 if dest.exists():assert dest.read_bytes()==raw
 else:atomic(dest,raw)
protocol={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Delta receipt only; pure stubs and AST, no scientific runtime.','sources':sources,'checks':['v2_manifest_pins','frozen_scientific_contract_fields_unchanged','source_P0P2_runtime_NPZ_pin_unchanged','wrapper_signature_and_args_kwargs_return_identity','success_None_EDOM_errno_EDOM_text_generic_post_attempt_pre_attempt_temporal_budget_source_deadline','external_dedup_same_exception_preserves_stage','driver_handler_status_and_counter_boundary_with_AST_stub','exact_final_command_hash_matches_contract','no_pilot_or_authorization_created']}
atomic(OUT/'REVISAO_P3_DELTA_PROTOCOL.json',json.dumps(protocol,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'protocol':metadata(OUT/'REVISAO_P3_DELTA_PROTOCOL.json')[0],'sources':sources[:3]},ensure_ascii=False))
