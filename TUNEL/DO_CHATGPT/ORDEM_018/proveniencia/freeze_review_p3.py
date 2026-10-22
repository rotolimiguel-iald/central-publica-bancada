from pathlib import Path
import json,datetime,hashlib
from audit_provenance import OUT,atomic,metadata
b=OUT.parent/'preregistros'/'conjunto_d'/'p3_preparacao'
names=['CONTRATO_P3.json','driver_p3.py','launch_p3.py','prior_transform.py','MANIFESTO_P3_PREPARADO.json','RUNTIME_P3_READONLY.json','INTERPRETER_PIN.json','COMANDO_EXATO_NAO_EXECUTADO.json','NOTA_P3_PREPARADO.md','src/pseob_source.py','src/synthetic_adapter_v2.py','src/temporal_contract.py','CONTROLES_PREPARACAO_FINAL.json']
folder=OUT/'p3_review_snapshot';folder.mkdir(exist_ok=True)
sources=[]
for name in names:
    p=b/name;m,raw=metadata(p);sources.append(m)
    dest=folder/name.replace('/','__')
    if dest.exists():assert dest.read_bytes()==raw
    else:atomic(dest,raw)
protocol={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Static review and pure arithmetic/stub controls only. No sampler or physical likelihood construction, native waveform, observed data, original script execution or author edits.','sources':sources,'tests':['manifest_and_contract_pins','runtime_1162_pins_read_only_and_165_subset','same_qualified_three_source_bytes','NPZ_pin_and_truth_hash_chain','mass_inverse_CDF_piece_endpoints_and_closed_form_area','normalization_transformation_at_17_fixed_points','angle_priors_and_periodic_indices','invalid_cube_rejection','AST_extracted_budget_logl_stub_all_10000_calls_and_10001_rejection','AST_extracted_budget_stops_wall_CPU','AST_extracted_audit_mock_blocks_foreign_data_network_child_and_writes','driver_launch_static_no_resume_and_abort_rules','installed_bilby_dynesty_source_wiring_read_only','no_authorization_or_execution_created'], 'controls_tolerances':{'mass_endpoint_abs':1e-10,'CDF_roundtrip_abs':1e-12,'mass_jac_relative':2e-7},'finding_threshold':'P2+ or concrete execution blockers. No claim of P3 runtime validation.'}
atomic(OUT/'REVISAO_P3_PROTOCOL.json',json.dumps(protocol,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'protocol':metadata(OUT/'REVISAO_P3_PROTOCOL.json')[0],'sources':len(sources)},ensure_ascii=False))
