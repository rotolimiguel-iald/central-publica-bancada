"""Documentary assembly only: no scientific imports, data values or execution."""
import copy
import hashlib
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
BASE=ROOT.parents[2]/"IALD_ORQUESTRACAO_20260923"
sys.path.insert(0,str(BASE))
from iald_orchestrator.safe_files import save_json, replace_bytes
if (OUT/"MANIFESTO_PREPARACAO.json").exists():
    raise RuntimeError("Preparation already materialized; review existing identity, do not regenerate.")
at=datetime.now(timezone.utc).isoformat()
source_paths={
 "resolver":"f9_consolidated_draft/RESOLUTOR_F9.json",
 "recommendation":"F9_ESCOLHAS_CONCRETAS_PROPOSTAS.md",
 "dependencies":"preregistros/f9_completion_dependencies/QUADRO_DEPENDENCIAS_F9.json",
 "mm_contract":"f9_mm_model_preparation/CONTRATO_MM_CANDIDATO.json",
 "mm_review":"derivacoes/revisao_mm_model/PARECER_MM_DOCUMENTAL.md",
 "covariance_contract":"f9_joint_covariance_preparation/CONTRATO_CANDIDATO.json",
 "covariance_review":"RECIBO_ROOT_REVISAO_COVARIANCIA_F9.json",
 "consumer":"f9_likelihood_consumer_preparation/likelihood_consumer.py",
 "prior":"f9_physical_prior_preparation/physical_prior.py",
 "theta_contract":"f9_theta_integration_preparation/CONTRATO_API.json",
 "verdict_v2":"f9_verdict_contract/F9_VERDICT_CONTRACT_CANDIDATE_V2.json",
 "certificate_interface":"f9_numerical_certification_preparation/INTERFACE_CERTIFICADOS_F9.json",
 "tail":"f9_tail_envelope_implementation_v2/tail_envelope.py",
 "tail_receipt":"RECIBO_ROOT_CONTROLES_TAIL_V2_PASS.json",
 "reducer":"f9_decision_reducer_preparation/decision_reducer.py",
 "reducer_receipt":"RECIBO_ROOT_REDUTOR_F9_PASS24.json",
 "scalar_receipt":"RECIBO_ROOT_Q01_PASS9.json",
 "theta_receipt":"RECIBO_ROOT_Q01_THETA_PASS15.json",
 "prior_receipt":"RECIBO_ROOT_Q01_EXTRA_PRIORS_PASS11.json",
 "marshal_limit":"DIAGNOSTICO_SERIALIZACAO_Q01_EXTRA_PRIORS.json",
 "profile_review":"RECIBO_ROOT_REVISAO_PERFIS_F9.json",
 "i02_repair":"f9_node_preflight_repair_preparation/CONTRATO_REPARO.json",
 "matrix_request":"F9_MATRIX_JOIN_PREPARATION_REQUEST.json",
}
raw={k:(ROOT/v).read_bytes() for k,v in source_paths.items()}
def pin(path):
    b=Path(path).read_bytes()
    return {"path":str(path),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
pins={k:pin(ROOT/v) for k,v in source_paths.items()}
def doc(k):return json.loads(raw[k])
old=doc("resolver");mm=doc("mm_contract");cov=doc("covariance_contract");theta=doc("theta_contract");v2=doc("verdict_v2")
# The original resolver snapshots are checked as historical evidence, not current originals.
historical=[]
for key,item in old["sources"].items():
    snap=item.get("snapshot")
    anchor=snap or item
    q=Path(anchor["path"]);actual=pin(q)
    if actual["bytes"]!=anchor["bytes"] or actual["sha256"]!=anchor["sha256"]:
        raise ValueError("Historical referenced bytes changed:"+key)
    historical.append({"source_id":key,**actual,"scope":("HISTORICAL_EXACT_SNAPSHOT; original not revalidated" if snap else "ORIGINAL_DOCUMENTARY_REFERENCE_REVALIDATED_AGAINST_HISTORICAL_PIN"),"snapshot_present":bool(snap)})
identity={"schema":"F9_EXECUTIVE_CONTRACT_PREPARATION_ID_V1","request_id":str(uuid.uuid4()),"created_at":at,"mission":"ORDEM018 F1e","scope":"Consolidated unratified scientific recipe and staged readiness; documentary only","execution_authorized":False,"opening_authorized":False}
save_json(OUT/"IDENTIDADE_PREPARACAO.json",identity)
science=copy.deepcopy(old["resolved_contract"])
science["model_status"]="PROPOSAL_NOT_OPERATOR_RATIFIED"
science["units"]={
 "native_covariance":cov["units"],
 "target":"16 dimensionless + 267 mag rows",
 "transformation_owner":cov["transformation_owner"],
 "y_C_origin":"consumer applies T to native y and affine origin, T C Tt including cross blocks",
 "X_and_model_means":"caller supplies these already in target units; consumer does not multiply them by T again",
 "scientific_rank_measured_here":False,
}
science["systematics"]["dedup_rule"]="NONE in current builder; all 600 ordered labels retained. Future equivalence compression requires a separately frozen proof and complete label map."
science["systematics"]["order"]=cov["O02"]["order"]
science["systematics"]["common_invariants"]=cov["O02"]["common_invariants"]
science["MM"]={
 "status":"PROPOSED_A_NOT_RATIFIED_REFERENCE_CENTRES_NOT_OPENED",
 "count":5,"selection_removed":False,"recommended":mm["recommendation"],
 "fixed_upstream_config":mm["fixed_upstream_config"],
 "working_law":mm["alternatives"]["A"],
 "alternative_B":mm["alternatives"]["B"],
 "recipe":"H0DN_MM_DZ_UPSTREAM_SYMMETRIC",
 "variance":"[sigmaD^2/D_ref^2+(sigma_v^2+240^2)/v_ref^2]/ln(10)^2 in native dex^2",
 "sigmaD":"(abs(d_minus)+abs(d_plus))/2; upstream symmetrization retained",
 "response":"y=log10[U(v)/D], U=v*(1-(q0+3)*z/2+(11+7*q0+3*q0^2-j0)*z^2/6), z=v/c",
 "covariance":"5 positive diagonal native variances; all MM-rest cross blocks explicitly zero as INPUT",
 "reference_rule":"D_ref,v_ref/errors/units/provenance are populated from predeclared source/row mapping only after authorized opening, then pinned identically across models before constructing the compound. No fitted/prediction-dependent reference.",
 "reference_endogeneity_required":True,
 "conditional_model_not_empirical_independence":True,
 "fixed_estimated_C_is_not_known_true_C":True,
 "numeric_references":None,"numerical_variances":None,
 "calibration_consequences":mm["calibration_consequences"],
}
science["physical_priors"]["H5_implemented_coordinate"]="u=1/rd in [1/160,1/130]; density1/(30*u^2). Equivalent to physical uniform rd with its Jacobian; q=rd/rd_CAMB remains equivalent documentary coordinate."
science["background"]["full_prior_qualified"]=False
science["background"]["selected_preparation"]="Direct existing prediction worker at all fixed finite-grid nodes, subject to qualified controller/runtime; no prior truncation or table extrapolation."
science["background"]["alternative"]="Expanded table covering full prior with qualified interpolation/error contract; not currently selected."
science["background"]["control_scope"]="Existing five-point background checks and one consumed theoretical point do not qualify the full prior or the new multi-node controller."
science["frequentist"].pop("eight_synthetic_controls",None)
science["frequentist"]["implementation_evidence"]={
 "reducer":pins["reducer_receipt"],"reducer_scope":doc("reducer_receipt")["scope"],
 "tail":pins["tail_receipt"],"tail_scope":doc("tail_receipt")["scope"],
 "physical_certificates_available":False,
}
pv=science["frequentist"]["recommended_calibration"]["p_value"]
pv["zero_dimension"]="Current F9 API: d=0 and positive certified lower statistic => INVALID/CONTRACT_INCOHERENCE_NOT_REJECTION, p=null. Nonpositive lower statistic gives inclusive atom upper bound1 only after semantic validation."
pv["positive_lower"]="Certified conditional upper tail envelope, not necessarily exact SF; current rational implementation may conservatively return1 after validated semantic/resource fallback."
science["bayesian_relative"]["outer_integrator"]=theta
science["bayesian_relative"]["current_scope"]="Scalar/extra-prior and synthetic theta qualifications exist separately. Actual matrix-consumer join and complete controller/physical integration remain unqualified."
science["bayesian_relative"]["engineering_output"]="ENGINEERING_ONLY values remain possible without uniform theory error certification; must expose refinement/concentration/boundary/underflow and UNBOUNDED_THEORY_ERROR. Such values are not certified significance."
science["bayesian_relative"]["global_error_bound"]=None
updates={
 "C01":("MM recipe now concrete as conditional proposal A; same Planck3+DESI13+local267 selection retained.","Synthetic joint qualification, recipe ratification and authorized reference binding remain."),
 "C02":("Five-model assembly/consumer/prior modules exist; mappings unchanged.","Matrix join under preparation755c3b08 and complete multi-node controller qualification remain."),
 "C03":("Proper original-coordinate priors retained; scalar extra-prior PASS11 once; H5 u transform explicit.","Physical/matrix coupling, chosen controller plan and ratification remain."),
 "C04":("Common kappa d_eta in R63 retained, relative evidence only.","Actual support/full rank/common normalization assessed after authorized data admission; synthetic qualification before use."),
 "C05":("Builder specifies9blocks/36crosses/native283x283 and ordered300x2 family; static review accepted.","Numerical synthetic builder/consumer qualification and eventual full600physical application checks remain; no dedup now."),
 "C06":("A working Gaussian at fixed reference scales with upstream MM_DZ variance and five retained rows proposed; B documented separately.","Operator ratification, authorized references/provenance and conditional-law limitations remain; true known C is not inferred."),
 "C07":("Direct full-box finite-grid motor preparation selected; no reuse of consumed single-point admission.","New multi-node supplier, guard, OS supervision, runtime and concrete resource plan remain to qualify."),
 "C08":("Consumer alone transforms native y/C/origin; X/means supplied already in target units.","Numerical support/normalization/rank checks remain; no jitter or duplicate T."),
 "C09":("Existing reducer passed24 invented logical cases once under V2.","Physical input/certificate verification and complete scenario records required before statistical decision."),
 "C10":("Tail implementation passed8primary+9negative synthetic groups once; dimension0 guard explicit.","Physical global L/U/support/span/theory certificates remain; no local optimum promoted to global lower bound."),
 "C11":("Synthetic theta PASS15 and extra-prior PASS11 exist, preserving full physical boxes.","Matrix/conditional joins, controller runtime/resources, physical integration and explicit error status remain."),
 "C12":("Historical provenance and E45 retained with P4/P5 separate; no re-execution.","Use-novelty and source-selection audit remains visible; no historical scalar number copied as new joint result."),
 "C13":("One consolidated unratified recipe prepared; freeze, opening and application validations staged separately.","Complete executable/runtime/resource package and independent review before V1 proposal; actual input certificates after opening.")
}
clauses=[]
for row in old["clauses"]:
    ident=row["id"];new,remaining=updates[ident]
    clauses.append({"id":ident,"title":row["title"],"status":"CONSOLIDATED_PROPOSAL_NOT_RATIFIED","historical_clause":row,"current_resolution":new,"remaining_condition":remaining})
decisions=[
 {"id":"O01","recommended":"A_UPSTREAM_FIXED_ERROR_WORKING_GAUSSIAN","alternative":"B_PRIMITIVE_JOINT_LAW_REQUIRES_DISTINCT_IMPLEMENTATION","ratified":False,"contract_pointer":"resolved_contract/MM","scope":"Scientific sampling assumption; source errors/frozen values do not prove adequacy."},
 {"id":"O02","recommended":"FINITE_300_STELLAR_X_2_SBF_ORDERED_FAMILY_NO_DEDUP","alternative":"EXPANDED_DEPENDENCE_MODEL_REQUIRES_NEW_FROZEN_RECIPE","ratified":False,"contract_pointer":"resolved_contract/systematics","scope":"Restricted sensitivity family and explicit cross-covariance INPUTs, not exhaustive physical systematics."},
 {"id":"O03","recommended":"COMMON_KAPPA_D_ETA_R63_WITH_PROPER_PHYSICAL_PRIORS","alternative":"PROPER_NUISANCE_PRIORS_REQUIRE_JUSTIFIED_WIDTHS_NOT_INVENTED_HERE","ratified":False,"contract_pointer":"resolved_contract/nuisance","scope":"Only finite relative evidences, common supported coordinates; no absolute evidence."},
 {"id":"O04","recommended":"V2_SEPARATE_FIVE_FREQUENTIST_TESTS_RELATIVE_BAYES_AND_POWER","alternative":"DESCRIPTIVE_ENGINEERING_OUTPUT_WHEN_CERTIFICATION_UNAVAILABLE_NO_SIGMA","ratified":False,"contract_pointer":"resolved_contract/frequentist","scope":"May report other valid calibrated rejection despite unavailable test; no missing p replaced by1 or0."}
]
stages=[
 {"id":"S0_PREPARE","current":True,"permitted":"Documentary assembly and separately authorized synthetic qualifications.","requires_before_next":["Independent semantic review of consolidated choices","Qualified reusable joins/controller and pinned executable/runtime","Concrete complete-domain resource/precision plan","Precisely fixed source/row/reference recipes and600scenario labels"],"not_required_here":"Observed values or physical actual-rank certificates; requiring their evaluation before opening would invert the prerequisite order."},
 {"id":"S1_FREEZE_PROPOSAL","current":False,"permitted":"Complete V1 recipe/code/runtime/selection/resources/failure/output contract pinned for operator.","requires_before_next":["Operator ratification of concrete O01-O04 and final V1","Separate explicit opening decision under ORDEM018 section6"],"confers_opening":False},
 {"id":"S2_BIND_AUTHORIZED_INPUTS","current":False,"permitted":"Only after section6 decision, retrieve predetermined sources/rows and construct reference/input manifest by frozen rules before compound evaluation.","requires_before_next":["Verify identity/hash/order/units","Bind MM fixed-reference provenance/endogeneity","Construct all600C cases by frozen rules","Run predeclared actual support/rank/normalization and law-applicability checks"],"no_data_dependent_recipe_revision":True},
 {"id":"S3_EVALUATE_AND_REPORT","current":False,"permitted":"Authorized full-domain evaluation and separate valid engineering/statistical outputs.","requires":["Every model/scenario represented or explicit failure","Physical statistical certificates before robust p or sigma","Retain valid independent outputs when another field unavailable"],"no_global_confirmation":True},
]
contract={
 "schema":"F9_CONSOLIDATED_EXECUTIVE_RECIPE_V1_PREPARATION",
 "identity":identity,"status":"DOCUMENTARY_CONSOLIDATION_PENDING_INDEPENDENT_REVIEW",
 "frozen_V1":False,"ratified":False,"opening_authorized":False,"execution_authorized":False,"F1_complete":False,
 "authority":"ORDEM018 F1e preparation only; operator reserves scientific ratification and section6 opening.",
 "source_pins":pins,"historical_source_snapshots":historical,
 "historical_reference_rule":"Inherited source_ids resolve through historical resolver references. Each entry records whether a snapshot or the original documentary artifact was revalidated; no experimental data refreshed.",
 "resolved_contract":science,"clauses":clauses,"operator_decisions":decisions,"staged_contract":stages,
 "controller_bindings_pending":{"request_id":None,"runtime_manifest":None,"global_configuration":None,"all_point_admission":None,"first_level":None,"last_level":None,"max_callback_calls":None,"wall_seconds":None,"cpu_policy":None,"memory_bytes":None,"guard":None,"supervisor":None,"durable_store_qualification":None},
 "qualification_registry":[{"id":k,"status":doc(k)["status"],"receipt":pins[k],"scope":doc(k).get("scope","See pinned receipt; no broader claim.")} for k in ["scalar_receipt","theta_receipt","prior_receipt","reducer_receipt","tail_receipt","covariance_review","profile_review"]],
 "remaining_qualification":{"Q01":"Matrix/consumer/actual joins; pending new preparation, do not repeat consumed scalar controls.","Q02":"New controller/supplier/guard/runtime/resources/full-domain engineering integration; no uniform CAMB theorem required to label engineering output honestly.","Q03":"Predeclare certificates and fallback before freeze; apply actual common-support/global-span/L/U/tail verification to authorized physical inputs after opening."},
 "provenance_limit":{"receipt":pins["marshal_limit"],"cross_process_marshal_reproduced":False,"source_and_runtime_pins_are_distinct_from_loaded_code_hash":True,"repeat_consumed_unit":False},
 "observed_outputs_now":copy.deepcopy(v2["outputs_now"]),
 "operations":{"scientific_imports":0,"candidate_imports":0,"new_scientific_units_executed":0,"solver_calls":0,"observed_reads":0,"remote_calls":0,"work_calls":0},
}
# Semantic/documentary checks, not execution tests or numerical proof.
assert science["models"]==old["resolved_contract"]["models"]
assert science["data"]==old["resolved_contract"]["data"]
assert science["nuisance"]==old["resolved_contract"]["nuisance"]
assert len(clauses)==13 and len(decisions)==4 and len(science["models"])==5
assert cov["dimensions"]["joint_rows"]==283 and cov["dimensions"]["nuisance_columns"]==63
assert cov["dimensions"]["complete_label_count"]==600 and science["MM"]["count"]==5
assert v2["primary_family"]==science["frequentist"]["primary_family"]
assert all(v is None for v in contract["observed_outputs_now"].values())
assert "if d == 0 and a > 0:" in raw["tail"].decode("utf-8")
assert "CONTRACT_INCOHERENCE_NOT_REJECTION" in raw["tail"].decode("utf-8")
assert all((ROOT/source_paths[k]).read_bytes()==v for k,v in raw.items())
save_json(OUT/"CONTRATO_CONSOLIDADO.json",contract)
save_json(OUT/"RECIBO_DOCUMENTAL.json",{"at":at,"status":"STRUCTURAL_SEMANTIC_ASSERTIONS_PASSED","scope":"Source byte hashes, preservation of models/data/nuisance,13clauses/4decisions/5models/283rows/63nuisance/600labels, null observed outputs; not independent scientific approval or execution qualification.","sources":len(pins),"historical_references_verified":len(historical),"execution_authorized":False,"opening_authorized":False})
note="""# Consolidação do contrato da Fase 9 — proposta ainda não ratificada

[REAL documental] Esta preparação reúne as treze cláusulas da Fase 9 e as decisões O01–O04 num contrato único. Cada cláusula conserva o texto histórico ao lado da resolução atual. Os cinco modelos, os dados e a medida comum dos 63 parâmetros nuisance permanecem iguais ao resolver anterior; não há novo resultado científico.

A proposta O01 fixa o experimento de trabalho gaussiano e a receita upstream dos cinco masers. A covariância continua uma hipótese explícita: congelar uma estimativa não a torna a covariância verdadeira. O02 conserva os 600 rótulos de sensibilidade, na ordem declarada e sem deduplicação. O03 conserva kappa d_eta comum e os priors físicos normalizados; o uso de u=1/rd inclui seu jacobiano. O04 conserva os cinco testes do V2, com Bayes relativo e poder em campos separados.

A transformação de unidades tem um único responsável: o consumidor transforma y, a origem afim e C nativos; X e médias já chegam nas unidades de destino. Aplicar T outra vez a essas colunas seria um erro. A cauda vigente também recusa dimensão zero com estatística inferior positiva como incoerência de contrato, sem p ou rejeição.

Os controles escalares, de theta, dos priors, do redutor e da cauda já consumidos são vinculados pelos recibos, com seu alcance limitado. Não são repetidos. A diferença de serialização marshal permanece documentada e sem causa estabelecida; não é anunciada reprodução independente daquele hash.

A sequência está explícita: completar e revisar o executável, as regras e os recursos; congelar a proposta V1; obter ratificação e decisão separada de abertura; só então preencher as referências fixas por regras predefinidas, conferir a matriz física e aplicar o composto. As verificações reais de suporte/rank pertencem a essa etapa posterior. A revisão sintética da bancada continua anterior ao uso.

[OPEN] O controlador completo, seu runtime, guard, supervisão, admissão de todos os pontos e os valores concretos de recursos/refinamento ainda estão pendentes. Campos nulos não são defaults nem autorização. A junção matricial está em preparação independente pela gerente. Assim, este arquivo não é V1 congelado, não encerra F1 e não abre observados.

Uma saída ENGINEERING_ONLY pode ser útil se informar honestamente o erro não limitado, refinamento, concentração e falhas. Ela não autoriza sigma. Um teste calibrado válido pode produzir rejeição mesmo quando outro esteja indisponível; ausência de certificado nunca é não-rejeição.

Não foram importados candidatos científicos, NumPy/CAMB ou dados; não houve solver, WSL, provedor, Work, AUTH/CLAIM nem alteração no kernel ou no gate. Requer revisão independente antes de promover a consolidação.
"""
replace_bytes(OUT/"NOTA_CONSOLIDACAO.md",note.encode("utf-8"))
members=[pin(p) for p in sorted(OUT.iterdir()) if p.is_file() and ".bak_" not in p.name and ".tmp_" not in p.name and p.name!="MANIFESTO_PREPARACAO.json"]
manifest={"schema":"F9_DOCUMENTARY_PREPARATION_MANIFEST_V1","at":at,"request_id":identity["request_id"],"members":members,"sources":pins,"historical_snapshots":historical,"status":"PREPARED_UNREVIEWED_NOT_FROZEN","scientific_execution":False,"opening_authorized":False}
save_json(OUT/"MANIFESTO_PREPARACAO.json",manifest)
print(json.dumps({"identity":identity,"manifest":pin(OUT/"MANIFESTO_PREPARACAO.json"),"contract":pin(OUT/"CONTRATO_CONSOLIDADO.json"),"members":len(members),"sources":len(pins),"historical_snapshots":len(historical)},ensure_ascii=False))
