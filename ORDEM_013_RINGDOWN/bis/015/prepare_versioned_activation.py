"""T03-C/xi: version the launch guard without overwriting cited artifacts."""
from pathlib import Path
import sys,json,ast
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[1];ROOT=B.parent;A=D/'activation_v2'
sys.path.insert(0,str(ROOT/'ORDEM_016_QG'))
from prepare_part_d import write,save,sha,now
def main():
    C=B/'bis/e2_code_v1_1';V=B/'bis/e2_code_v1_1_2'
    assert not V.exists();r=json.loads((B/'RINGDOWN_5SIGMA_V1_1_1.json').read_bytes())
    assert {p.relative_to(C).as_posix():sha(p) for p in C.rglob('*.py')}==r['own_code_tree_sha256']
    for name,h in r['own_code_tree_sha256'].items():
        p=C/name;assert sha(p)==h;write(V/name,p.read_bytes())
    p=V/'registration_guard.py';s=p.read_text('utf-8-sig')
    before="""    if activation['receipt_relative_to_Chatgpt']!='ORDEM_013_RINGDOWN/bis/015/E2_V1_1_REGISTRATION_RECEIPT.json':
        raise ValueError('Wrong V1.1 activation receipt path')"""
    after="""    match=re.fullmatch(r'ENTREGA_015_E2_REGISTRO_V1_1(?:_([1-9][0-9]*))?\\.md',Path(note).name)
    if match is None or Path(note).resolve()!=contained(reg['witness_relative_to_Chatgpt']):
        raise ValueError('Wrong activation witness identity')
    ordinal='' if match[1] is None else '_'+match[1]
    expected='ORDEM_013_RINGDOWN/bis/015/E2_V1_1'+ordinal+'_REGISTRATION_RECEIPT.json'
    if activation['receipt_relative_to_Chatgpt']!=expected:
        raise ValueError('Wrong per-amendment activation receipt path')"""
    assert s.count(before)==1;s=s.replace(before,after)
    write(p,s.encode(),True)
    # The immediate byte backup is outside the .py glob, and retained.
    code={p.relative_to(V).as_posix():sha(p) for p in V.rglob('*.py')}
    changed=[n for n,h in code.items() if h!=r['own_code_tree_sha256'][n]]
    assert changed==['registration_guard.py'],changed
    old_ast=ast.parse((C/'registration_guard.py').read_text());new_ast=ast.parse(s)
    differences=[]
    for x,y in zip(old_ast.body,new_ast.body):
        if ast.dump(x)!=ast.dump(y):differences.append(getattr(x,'name',type(x).__name__))
    assert differences==['check_activation_v1_1']
    source=D/'test_integrated_guard_v3.py';test=source.read_text()
    test=test.replace("C=B/'bis/e2_code_v1_1';D=B/'bis/015/t03/guard_integration_tests_003'",
        "C=B/'bis/e2_code_v1_1_2';D=B/'bis/015/activation_v2/integration_tests'")
    target=D/'test_integrated_guard_activation_v2.py';write(target,test.encode())
    save(A/'PREPARED.json',dict(at=now.isoformat(),scope='T03_C_GUARD_CORRECTION_AND_XI_VERSIONED_CODE',
        original_tree=r['own_code_tree_sha256'],new_tree=code,changed_functions=differences,
        old_source_sha256=sha(C/'registration_guard.py'),new_source_sha256=sha(p),
        integration_test_source_sha256=sha(source),integration_test_copy_sha256=sha(target),
        no_original_overwrite=True,scientific_code_changed=False,gate_changed=False))
    print(json.dumps(dict(tree=str(V),changed=changed)))
if __name__=='__main__':main()
