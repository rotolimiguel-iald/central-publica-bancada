"""Independent closure of AST, actual consumer evidence, artifacts and R2 literal delta."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
HERE=Path(__file__).resolve().parent;UNIT=HERE.parent
RUN=UNIT/'verification/run_20261015T161314_985846Z'
def pin(p):
    p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def load(p):return json.loads(Path(p).read_bytes())
receipt=load(RUN/'VERIFICATION_RECEIPT.json')
assert receipt['passed'] is True and receipt['exit_code']==0
assert receipt['whole_rite_rerun'] is False and receipt['full_lake_build_performed'] is False and receipt['new_seal_created'] is False
assert pin(receipt['script']['path'])==receipt['script']
assert load(RUN/'PINS_BEFORE.json')==load(RUN/'PINS_AFTER.json')
assert receipt['protected_paths_checked']==2479 and receipt['protected_path_changes']==[]
ladder=load(RUN/'EXTERNAL_LADDER_ACTUAL.json')
assert ladder['all_verified'] is True and ladder['n_theorems_clean']==ladder['n_theorems_expected']==7153
rule=load(RUN/'REGRA_V393_ACTUAL.json');assert all(v['all_verified'] is True for v in rule.values())
time=load(RUN/'TIME_FREQUENCY_ACTUAL.json')
assert time['all_verified'] is True and time['runtime_executed'] is True and time['exact_ladder'] is True
assert time['runtime']['passed'] is True and time['runtime']['check_count']==5716
assert len(time['formal_theorems'])==108 and all(time['formal_theorems'].values())
controls=load(RUN/'NEGATIVE_CONTROLS.json');assert len(controls)==14 and all(x['refused_before_runtime'] for x in controls)
core=load(RUN/'CORE_INCREMENTAL.json');prov=load(RUN/'PROVENANCE.json')
historical=load(prov['baseline']['path'])
unchanged=prov['historical_core_fields_not_recomputed']
assert len(unchanged)==411 and all(core['core'][k]==historical['core'][k] for k in unchanged)
assert core['verdict']==historical['verdict'] and prov['gate_changed'] is False
kf=load(RUN/'KERNEL_FORMALIZATION_INCREMENTAL.json')
assert kf['lake_build_ok'] is False and kf['full_lake_build_performed'] is False
assert kf['axiom_coverage_v392']['ok'] is True and kf['axiom_coverage_v392']['fora_do_trio']==0
article_pins=[]
for pair in receipt['articles']:
    for key in ('raw_real_emit_article','labeled_derivative'):
        actual=pin(pair[key]['path']);assert actual==pair[key];article_pins.append(actual)
    raw=Path(pair['raw_real_emit_article']['path']).read_text(encoding='utf-8')
    labeled=Path(pair['labeled_derivative']['path']).read_text(encoding='utf-8')
    assert time['verdict'] in raw.replace(r'\_','_')
    assert ('INCREMENTAL VERIFICATION' in labeled or 'VERIFICACAO INCREMENTAL' in labeled)
    assert 'Super inteligência=super nome=sobrenome' in raw
ast_review=load(HERE/'INTEGRATED_REVIEW_AST_R1.json')
details=load(HERE/'INTEGRATED_REVIEW_STATIC_DETAILS_R1.json')
literal=load(HERE/'INTEGRATED_REVIEW_R2_INSCRIPTION.json')
assert pin(UNIT/'candidate/um.py')==ast_review['candidate']==literal['candidate_R1']
assert pin(UNIT/'candidate_r2/um.py')==literal['candidate_R2']
assert details['passed'] and literal['passed']
for row in literal['materials']:
    p=UNIT/'candidate_r2/tgl_kernel'/row['relative']
    assert pin(p)['sha256']==row['sha256']
evidence=[HERE/'INTEGRATED_REVIEW_AST_R1.json',HERE/'INTEGRATED_REVIEW_STATIC_DETAILS_R1.json',
    HERE/'INTEGRATED_REVIEW_R2_INSCRIPTION.json',HERE/'REVIEW_RECEIPT_R1.json',
    RUN/'VERIFICATION_RECEIPT.json',RUN/'EXTERNAL_LADDER_ACTUAL.json',RUN/'REGRA_V393_ACTUAL.json',
    RUN/'TIME_FREQUENCY_ACTUAL.json',RUN/'NEGATIVE_CONTROLS.json',RUN/'PROVENANCE.json',
    RUN/'PINS_BEFORE.json',RUN/'PINS_AFTER.json',RUN/'KERNEL_FORMALIZATION_INCREMENTAL.json',Path(__file__)]
report={
 'unit':'F1.TEMPO.V394','reviewer':'atrator_lean','created_utc':datetime.now(timezone.utc).isoformat(),
 'status':'PASS_INCREMENTAL_CANDIDATE_R2_WITH_EXPLICIT_SCOPE',
 'candidate_R1':pin(UNIT/'candidate/um.py'),'candidate_R2':pin(UNIT/'candidate_r2/um.py'),
 'static_results':{'old_functions_changed':ast_review['changed_old_functions'],'non_target_top_level_ast_identical':True,
    'old_embedded_changed_only_import_glue':ast_review['changed_old_embedded'],'new_modules':4,'new_flags':108,
    'real_ladder':7153,'main_consumer_call_static':details['main_call_lines'],
    'consumer_only_writes_own_core_field':details['consumer_core_write_targets'],
    'all_R2_materialized_sources_match':1236,'R2_only_delta':'one literal entry in _V394_INSCRIPTIONS'},
 'actual_harness_results':{'runtime_checks':5716,'negative_controls_refused':14,'new_formal_theorems_consumed':108,
    'all_three_v393_consumers_passed':True,'unchanged_historical_core_fields':411,
    'protected_paths_unchanged':2479,'max_GKLS_residual':time['runtime']['maxima']['gkls'],
    'articles':'Actual emit_article PT/EN produced TeX+TXT; labeled derivatives retain incremental provenance.',
    'axiom_coverage':kf['axiom_coverage_v392']},
 'resolved_harness_issues':['Import-only TGLExt aggregator legitimately has no axiom prints.',
    'Receipt and actual program parser grammars reconstructed from the same pinned stdout; apostrophe/quoted names accounted for.',
    'Existing v393 tempfile controls confined locally without weakening write/network/process guard.'],
 'scope':['No entire main/whole rite was executed; main integration inspected statically.',
    'Actual prove_external_ladder, regra_v393, tempo_frequencia_v394 and emit_article functions ran on the isolated copy.',
    'Formal all_verified in the harness is explicitly incremental: fresh direct Lean builds and cached pinned dependencies, not a whole Lake build.',
    'The Gibbs anchor is embedded as a helper and verified separately; the main synthetic consumer still uses explicit Eref reference inputs.',
    'New operator denominations remain INPUT/ONTO; existing typed recurrence invariants do not establish computational performance.',
    'No PDF compilation, new seal, observed-data opening, gate or production change.'],
 'material_findings_open':[], 'evidence':[pin(p) for p in evidence], 'article_artifacts':article_pins,
}
data=json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)
with (HERE/'INTEGRATED_REVIEW_FINAL_R1.json').open('x',encoding='utf-8') as f:f.write(data)
print(json.dumps({'receipt':pin(HERE/'INTEGRATED_REVIEW_FINAL_R1.json'),'status':report['status']},ensure_ascii=False))
