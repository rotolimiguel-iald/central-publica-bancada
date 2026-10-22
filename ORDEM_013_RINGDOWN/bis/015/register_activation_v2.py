"""Register the ordinal-bound receipt repair under T03-C and chain xi."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,sys,hashlib,os
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;A=D/'activation_v2';B=D.parents[1];ROOT=B.parent
C=B/'bis/e2_code_v1_1_2';OLD=B/'bis/e2_code_v1_1';OUT=ROOT/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
    raw=x if isinstance(x,bytes) else (json.dumps(x,indent=2,allow_nan=False)+'\n').encode()
    p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.pending');assert not p.exists()
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;os.link(tmp,p);tmp.unlink()
def main():
    sys.path.insert(0,str(C));import registration_guard as g
    parent=B/'RINGDOWN_5SIGMA_V1_1_1.json';path=B/'RINGDOWN_5SIGMA_V1_1_2.json'
    note=OUT/'ENTREGA_015_E2_REGISTRO_V1_1_2.md';receipt=D/'E2_V1_1_2_REGISTRATION_RECEIPT.json'
    assert not any(p.exists() for p in (path,note,receipt,B/'bis/PART_015_BUDGET_START.json'))
    prior=json.loads(parent.read_bytes());reg=json.loads(parent.read_bytes())
    tree={p.relative_to(C).as_posix():sha(p) for p in C.rglob('*.py')}
    old_tree={p.relative_to(OLD).as_posix():sha(p) for p in OLD.rglob('*.py')}
    assert old_tree==prior['own_code_tree_sha256']
    assert set(tree)==set(old_tree) and [n for n,h in tree.items() if h!=old_tree[n]]==['registration_guard.py']
    oldast=ast.parse((OLD/'registration_guard.py').read_text());newast=ast.parse((C/'registration_guard.py').read_text())
    assert len(oldast.body)==len(newast.body)
    assert [getattr(a,'name',type(a).__name__) for a,b in zip(oldast.body,newast.body) if ast.dump(a)!=ast.dump(b)]==['check_activation_v1_1']
    integration=A/'integration_tests/RESULT.json';test=json.loads(integration.read_bytes())
    assert test['guard_sha256']==tree['registration_guard.py'] and all(v['passed'] for v in test['tests'])
    inherited_path=D/'t03/C1_GUARD_MUTATION_TESTS_V1_1.json';inherited=json.loads(inherited_path.read_bytes())
    assert inherited['own_code_tree_sha256']==old_tree
    inherited_tests=[v for v in inherited['tests'] if not v['name'].startswith('guard_integration_tests_003:')]
    tests=[dict(v,inherited_on_AST_identical_dependencies=True) for v in inherited_tests]
    tests += [dict(name='activation_v2:'+v['name'],passed=True,evidence=v,inherited_on_AST_identical_dependencies=False) for v in test['tests']]
    proof=dict(status='V1_1_GUARD_PROBES_PASSED',finished_utc=datetime.now(timezone.utc).isoformat(),
        own_code_tree_sha256=tree,statistical_subobject_sha256=reg['statistical_subobject_sha256'],tests=tests,
        current_round_tests=len(test['tests']),inherited_tests=len(inherited_tests),
        sources={str(inherited_path.relative_to(ROOT)):sha(inherited_path),str(integration.relative_to(ROOT)):sha(integration)},
        scope='Only check_activation_v1_1 changed; 53 integration tests freshly executed; other controls transported on unchanged ASTs/code; not external management audit',
        seed_read=False,heavy_jobs=0)
    pp=A/'C1_GUARD_MUTATION_TESTS_V1_1_2.json';save(pp,proof)
    reg.update(parent_registration_sha256=sha(parent),registered_utc=datetime.now(timezone.utc).isoformat(),
        witness_relative_to_Chatgpt=note.relative_to(ROOT).as_posix(),own_code_tree_sha256=tree)
    reg['activation_v1_1']['receipt_relative_to_Chatgpt']=receipt.relative_to(ROOT).as_posix()
    reg['activation_v1_1']['probes_result_relative_to_Chatgpt']=pp.relative_to(ROOT).as_posix()
    reg['code_directory_v1_1']=C.relative_to(ROOT).as_posix()
    reg['activation_repair_v1_1_2']=dict(scope='T03_C_AND_XI_ORDINAL_BOUND_IMMUTABLE_RECEIPT',
        predecessor_code_directory=OLD.relative_to(ROOT).as_posix(),changed_functions=['check_activation_v1_1'],
        old_receipt_preserved_sha256=sha(D/'E2_V1_1_REGISTRATION_RECEIPT.json'),
        scientific_code_changed=False,script_sha256=sha(Path(__file__)),
        prior_1_activation_status='MEDIDA_FIXED_BASE_MARKER_MISMATCH_NOT_RETROACTIVELY_EXECUTABLE')
    g.verify_statistical_identity(json.loads((B/'RINGDOWN_5SIGMA_V1.json').read_bytes()),reg)
    save(path,reg)
    text=f'''[REAL — T03-C/xi: guarda corrigida em cópia versionada; nenhuma alteração científica]

registro_sha256: {sha(path)}
registered_utc: {reg['registered_utc']}

Abertura015SHA256: {sha(OUT/'ENTREGA_015_ABERTURA_operador.md')}
Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}

Pai V1.1.1:{sha(parent)}. Nova árvore e2_code_v1_1_2; somente check_activation_v1_1 mudou. Recibo imutável por ordinal derivado da testemunha selecionada, registro e testemunha cruzados por SHA.53 controles de integração recém-executados;{len(inherited_tests)} controles anteriores transportados sobre dependências de AST/código idênticas, não alegados como reexecutados.
Código científico, R5, runtime, calendário e autorização cega preservados. Recibo base e árvores anteriores intactos. O elo .1 permanece histórico com a MEDIDA de ativação, não executável retroativamente. R7 continua obrigatório antes de job pesado; esta testemunha não o cria.
'''
    save(note,text.encode())
    r5=ROOT/reg['activation_v1_1']['qualification_R5_relative_to_Chatgpt']
    marker=dict(status='E2_V1_1_REGISTERED',registration_sha256=sha(path),witness_sha256=sha(note),
        probes_result_sha256=sha(pp),qualification_R5_sha256=sha(r5),supersedes_sha256=sha(D/'E2_V1_1_REGISTRATION_RECEIPT.json'))
    save(receipt,marker)
    loaded,digest,actualnote=g.load_registration_chain_v1_1();assert digest==sha(path)
    g.check_activation_v1_1(loaded,digest,actualnote)
    try:g.checked_registration()
    except FileNotFoundError as exc:
        assert Path(exc.filename)==B/'bis/PART_015_BUDGET_START.json'
        outcome=dict(exception=type(exc).__name__,message=str(exc),expected=True)
    else:raise AssertionError('Unexpected execution authorization without real R7')
    jobs=g.load_authorized_configuration(loaded,digest)
    assert set(jobs['pe_jobs'])==set(reg['pe_jobs'])
    result=dict(status='VERSIONED_ACTIVATION_CHECKED_R7_STILL_REQUIRED',at=datetime.now(timezone.utc).isoformat(),
      registration_sha256=digest,witness_sha256=sha(note),receipt_sha256=sha(receipt),guard_sha256=sha(C/'registration_guard.py'),
      newly_executed_controls=len(test['tests']),inherited_controls=len(inherited_tests),
      actual_guard_outcome=outcome,allocation_chain_verified=True,real_clock_created=False,heavy_jobs=0,seed_read=False,gate_changed=False)
    save(A/'REGISTERED_RESULT.json',result);print(json.dumps(result))
if __name__=='__main__':main()
