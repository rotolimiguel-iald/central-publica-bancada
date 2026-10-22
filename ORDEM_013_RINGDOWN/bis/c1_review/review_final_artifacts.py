"""Independent optimized-mode re-review. Only review-directory writes.

Imports the pure guard module after source inspection. Never runs a producer,
recorder main, um.py, or the original test script with its output side effect.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast
import copy
import csv
import hashlib
import importlib.util
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name):
    return json.loads((ROOT/name).read_bytes())


def require(condition,reason):
    if not condition:raise RuntimeError(reason)


def main():
    output=HERE/'final_artifact_checks.json'
    require(not output.exists(),'Review output already exists')
    require(sys.flags.optimize==1,'Must execute with python -O')
    previous=load('bis/c1_review/independent_results.json')
    names=set(previous['inputs_before']) | {
        'refeito/c1_evidence_guards.py','refeito/measure_c1_013bis_v2.py',
        'refeito/record_c1_013bis_v3.py','refeito/test_c1_guards_013bis.py',
        'bis/C1_NUMERICAL_CONTROLS_v2.json','bis/C1_GUARD_MUTATION_TESTS.json',
        'C1_LEITURAS_v3.json','C1_ADENDO_CORRECOES_013BIS_v2.md',
        'REAPROVEITAMENTO_C1_v2.md','bis/C1_ADVERSARIAL_REVIEW.md'}
    before={n:sha(ROOT/n) for n in sorted(names)}
    spec=importlib.util.spec_from_file_location('reviewed_c1_guards',ROOT/'refeito/c1_evidence_guards.py')
    guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
    cat=load('C4_CATALOG_220.json');measured=load('bis/C1_NUMERICAL_CONTROLS_v2.json')
    core=load('cache/casa/um_absoluto.json')['core']['clock_test_result_v369']
    with (ROOT/'C7_INDEPENDENT/tables/event_reading_predictions.csv').open(encoding='utf-8-sig',newline='') as f:
        csv_rows=list(csv.DictReader(f))
    guard.validate_inputs(csv_rows,cat)
    positive=guard.validate_evidence(ROOT,measured,core)
    cases=[]
    def probe(name,fn,group):
        try:fn()
        except (ValueError,KeyError,TypeError) as exc:
            cases.append({'name':name,'group':group,'rejected':True,'exception':type(exc).__name__,'message':str(exc)})
        else:cases.append({'name':name,'group':group,'rejected':False})
    r=copy.deepcopy(csv_rows);r.insert(0,dict(r[0],delta_tau='12345'))
    probe('conflicting_duplicate_csv',lambda:guard.validate_inputs(r,cat),'original_ten')
    r=copy.deepcopy(csv_rows);r[-1]['delta_tau']='NaN'
    probe('nan_last_csv_column',lambda:guard.validate_inputs(r,cat),'original_ten')
    probe('missing_csv_row',lambda:guard.validate_inputs(csv_rows[:-1],cat),'original_ten')
    m=copy.deepcopy(measured);m['csv_checks'][0]['relative_errors']['delta_tau']=float('nan')
    probe('nan_recorded_error',lambda:guard.validate_evidence(ROOT,m,core),'original_ten')
    m=copy.deepcopy(measured);m['dependencies'].pop('refeito/c1_evidence_guards.py')
    probe('missing_dependency',lambda:guard.validate_evidence(ROOT,m,core),'original_ten')
    m=copy.deepcopy(measured);m['dependencies']['tgl_ringdown_prediction.py']='0'*64
    probe('changed_dependency',lambda:guard.validate_evidence(ROOT,m,core),'original_ten')
    m=copy.deepcopy(measured);m['checked']=263
    probe('wrong_coverage_count',lambda:guard.validate_evidence(ROOT,m,core),'original_ten')
    c=copy.deepcopy(core);c['P1']['verdict']='P1_FALSIFIED_IN_READING'
    probe('changed_P1',lambda:guard.validate_evidence(ROOT,measured,c),'original_ten')
    c=copy.deepcopy(core);c['all_verified']=False
    probe('unsealed_clock',lambda:guard.validate_evidence(ROOT,measured,c),'original_ten')
    m=copy.deepcopy(measured);m['P2_tau_star_bound_tP']*=2
    probe('changed_bound',lambda:guard.validate_evidence(ROOT,m,core),'original_ten')
    # Preserve all dependency hashes but rename every event in the recorded checks.
    m=copy.deepcopy(measured)
    for row in m['csv_checks']:row['event']='WRONG_'+row['event']
    probe('evidence_keys_disjoint_from_hashed_csv',lambda:guard.validate_evidence(ROOT,m,core),'additional')
    m=copy.deepcopy(measured);m['profile_comparison']=[]
    probe('empty_profile_table',lambda:guard.validate_evidence(ROOT,m,core),'additional')
    m=copy.deepcopy(measured);m['profile_comparison'][0]['comparison_redshift']=1
    probe('profile_redshift_not_zero',lambda:guard.validate_evidence(ROOT,m,core),'additional')
    m=copy.deepcopy(measured)
    for row in m['spin_comparison']:row.pop('exact_qnm')
    probe('all_qnm_pairs_missing',lambda:guard.validate_evidence(ROOT,m,core),'additional')
    # Exercise exactly write_new's body using in-memory fake path objects.
    tree=ast.parse((ROOT/'refeito/record_c1_013bis_v3.py').read_text(encoding='utf-8-sig'))
    function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='write_new')
    isolated=ast.Module(body=[function],type_ignores=[])
    class FakePath:
        name='synthetic'
        def __init__(self):self.data=b'';self.replaced=False
        def exists(self):return False
        def with_name(self,name):return self
        def open(self,mode):return self
        def __enter__(self):return self
        def __exit__(self,*args):return False
        def write(self,data):self.data=data;return len(data)
        def read_bytes(self):return self.data+b'CORRUPTED'
        def replace(self,target):self.replaced=True
    write_checks=[]
    for optimize in (0,1):
        namespace={};exec(compile(isolated,'isolated_write_new', 'exec',optimize=optimize),namespace)
        p=FakePath();exception=None
        try:namespace['write_new'](p,'synthetic review payload')
        except AssertionError as exc:exception=type(exc).__name__
        write_checks.append({'compiled_optimize':optimize,'corrupted_bytes_replaced':p.replaced,'exception':exception})
    old=load('bis/C1_NUMERICAL_CONTROLS.json')
    diff=[key for key in old.keys()|measured.keys() if old.get(key)!=measured.get(key)]
    v2=load('C1_LEITURAS_v2.json');v3=load('C1_LEITURAS_v3.json')
    gen=v3['v3_generator'];genpath=Path(gen['path'])
    newad=(ROOT/'C1_ADENDO_CORRECOES_013BIS_v2.md').read_text(encoding='utf-8')
    ed={'P2_scope_present':'Cota da série mediana, com margem de calibração; sem nível de confiança atribuído.' in newad,
        'omega_real_present':'ν=ω_R−mΩH' in newad,
        'kappa_SI_formula_present':'κ=√(1−χ²)/[2t_M(1+√(1−χ²))]' in newad,
        'unlogged_web_failure_removed':'ferramenta web' not in newad,
        'partial_BW_reading_scope_retained':'introdução, Teoremas 1–2' in newad,
        'physical_selection_absent':v3['hypothesis_selected'] is False and all(x['physical_selection'] is None and x['relation_to_operator_16Sep'] is None for x in v3['rows'])}
    archived=load('bis/C1_GUARD_MUTATION_TESTS.json')
    integrity={
        'historic_inputs_unchanged_since_previous_review':all(sha(ROOT/p)==h for p,h in previous['inputs_before'].items()),
        'v3_generator_sha_correct':sha(genpath)==gen['sha256'],
        'origin_generator_sha_correct':sha(ROOT/'complete_c1_contract.py')==v3['origin_generator_sha256'],
        'supersedes_v2_sha_correct':v3['supersedes']=='C1_LEITURAS_v2.json' and v3['supersedes_sha256']==sha(ROOT/'C1_LEITURAS_v2.json'),
        'numeric_reference_sha_correct':v3['numerical_controls']['sha256']==sha(ROOT/'bis/C1_NUMERICAL_CONTROLS_v2.json'),
        'primary_reference_sha_correct':v3['primary_retrievals']['sha256']==sha(ROOT/'bis/C1_PRIMARY_RETRIEVALS.json'),
        'mutation_script_sha_correct':archived['code_sha256']==sha(ROOT/'refeito/test_c1_guards_013bis.py'),
        'v3_rows_equal_previously_verified_v2_rows':v3['rows']==v2['rows']}
    hashes_in_prose=[]
    import re
    for filename in ('C1_ADENDO_CORRECOES_013BIS_v2.md','REAPROVEITAMENTO_C1_v2.md'):
        content=(ROOT/filename).read_text(encoding='utf-8')
        known_hashes=set(before.values())|{sha(ROOT/'cache/literature/013bis'/r['name']) for r in load('bis/C1_PRIMARY_RETRIEVALS.json') if r.get('sha256')}
        opening=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'
        known_hashes.add(sha(opening))
        hashes_in_prose.append({'file':filename,'unmatched_hashes':[h for h in re.findall(r'\b[0-9a-f]{64}\b',content) if h not in known_hashes]})
    after={n:sha(ROOT/n) for n in sorted(names)}
    require(before==after,'Audited artifact changed during review')
    result={'utc':datetime.now(timezone.utc).isoformat(),'status':'B1_CLOSED__B2_PARTIAL__CURRENT_NUMERICAL_ARTIFACTS_VERIFIED',
            'python':sys.version,'optimization':sys.flags.optimize,'bytecode_writes_disabled':sys.dont_write_bytecode,
            'script_sha256':sha(Path(__file__)),'input_hashes':before,'inputs_unchanged':before==after,
            'positive_control':positive,'mutations':cases,'write_new_fake_path_probe':write_checks,
            'numeric_diff_keys':sorted(diff),'previous_independent_csv_max_relative_error':previous['csv']['max_relative_error'],
            'integrity':integrity,'editorials':ed,'prose_hash_checks':hashes_in_prose,
            'original_mutations_rejected':sum(t['rejected'] for t in cases if t['group']=='original_ten'),
            'additional_mutations_accepted':sum(not t['rejected'] for t in cases if t['group']=='additional'),
            'scope':'No main of recorder/producer/test was executed; only guards and isolated write_new with fake paths.'}
    raw=(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
    tmp=output.with_suffix('.json.tmp')
    with tmp.open('xb') as f:f.write(raw)
    require(tmp.read_bytes()==raw,'Output byte mismatch')
    require(not output.exists(),'Output appeared concurrently')
    tmp.rename(output)
    print(json.dumps({k:result[k] for k in ('status','optimization','original_mutations_rejected','additional_mutations_accepted','numeric_diff_keys','integrity','editorials','prose_hash_checks','write_new_fake_path_probe','inputs_unchanged')},ensure_ascii=False,indent=2))
    print('RESULT_SHA256',sha(output))


if __name__=='__main__':main()
