"""Engineering mutation tests only; synthetic receipts are never proof evidence."""
from pathlib import Path
import importlib.util, json, hashlib, shutil, uuid
from datetime import datetime,timezone

S=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('runtime_proposal_test',S/'PROPOSTA_RUNTIME.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
base=S/'runtime_test_fixtures'/uuid.uuid4().hex;base.mkdir(parents=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    raw=(json.dumps(x,indent=2)+'\n').encode()
    if p.exists():p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')).write_bytes(p.read_bytes())
    tmp=p.with_suffix('.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(p)
gold=base/'synthetic_only';gold.mkdir()
(gold/'source.lean').write_text('-- SYNTHETIC READER FIXTURE; NEVER COMPILED\n',encoding='utf-8')
(gold/'log.txt').write_text('SYNTHETIC CONTROL LOG, NOT KERNEL EVIDENCE\nBENCH_DECL\tfixture_theorem\ttheorem\tpropext\n',encoding='utf-8')
save(gold/'receipt.json',dict(test_fixture=True,rc=0,source_sha256=sha(gold/'source.lean'),log_sha256=sha(gold/'log.txt')))
save(gold/'P1_QUADRO.json',dict(items=[dict(item='A2',status='MEDIDA',named_open_hypotheses=['FIXTURE_ONLY'])]))
unit=dict(module='FIXTURE',item='A2',rc=0,new_declaration_count=1,audited_declaration_count=1,axioms={'fixture_theorem':['propext']},declaration_kinds={'fixture_theorem':'theorem'})
for key,path in [('source','source.lean'),('log','log.txt'),('receipt','receipt.json')]:unit[key]=path;unit[key+'_sha256']=sha(gold/path)
save(gold/'P2_COMPILACAO.json',dict(units=[unit]))
save(gold/'CONSTANTS.json',dict(ALPHA_FINE_CODATA_2018=7.2973525693e-3))
save(gold/'PRONTO.json',dict(test_fixture=True,files={p.name:sha(p) for p in gold.iterdir()}))
pin=sha(gold/'PRONTO.json');results=[]
cases=['baseline','ONE_zero','wrong_pin','missing_pin','source_modified','log_modified','receipt_modified','P1_modified','P2_modified','missing_source','unknown_item','repinned_bad_rc','repinned_bad_axioms','repinned_bad_count','repinned_bad_source_binding','repinned_bad_kind']
for case in cases:
    root=base/case;shutil.copytree(gold,root);m.ROOT=root;m.EXPECTED_MANAGEMENT_PACKAGE_SHA256=pin;one=1;item='A2'
    if case=='ONE_zero':one=0
    if case=='wrong_pin':m.EXPECTED_MANAGEMENT_PACKAGE_SHA256='0'*64
    if case=='missing_pin':m.EXPECTED_MANAGEMENT_PACKAGE_SHA256=None
    if case=='unknown_item':item='NO_SUCH_ITEM'
    mutation={'source_modified':'source.lean','log_modified':'log.txt','receipt_modified':'receipt.json','P1_modified':'P1_QUADRO.json','P2_modified':'P2_COMPILACAO.json'}.get(case)
    if mutation:(root/mutation).write_bytes((root/mutation).read_bytes()+b'\nTAMPERED\n')
    if case=='missing_source':(root/'source.lean').rename(root/'source_removed.fixture')
    if case.startswith('repinned_'):
        if case in ('repinned_bad_rc','repinned_bad_source_binding'):
            r=json.loads((root/'receipt.json').read_bytes())
            if case=='repinned_bad_rc':r['rc']=1
            else:r['source_sha256']='0'*64
            save(root/'receipt.json',r)
        p2=json.loads((root/'P2_COMPILACAO.json').read_bytes());u=p2['units'][0]
        if case=='repinned_bad_axioms':u['axioms']={'different_theorem':['propext']}
        if case=='repinned_bad_count':u['audited_declaration_count']=2
        if case=='repinned_bad_kind':u['declaration_kinds']={'fixture_theorem':'definition'}
        u['receipt_sha256']=sha(root/'receipt.json');save(root/'P2_COMPILACAO.json',p2)
        save(root/'PRONTO.json',dict(test_fixture=True,files={p.name:sha(p) for p in root.iterdir() if p.is_file() and p.name!='PRONTO.json' and '.bak_' not in p.name}))
        m.EXPECTED_MANAGEMENT_PACKAGE_SHA256=sha(root/'PRONTO.json')
    result=m._read_stone(item,one);expected=case=='baseline';passed=result['all_verified']==expected and result.get('gate_changed') is False
    if expected:passed=passed and result['physical_contract_inhabitant'] is False and all(c['negative_control_passed'] for c in result['checks'])
    results.append(dict(case=case,expected=expected,passed=passed,result=result))
save(S/'RUNTIME_CONTROLS.json',dict(scope='SYNTHETIC_ENGINEERING_CONTROLS_NOT_LEAN_EVIDENCE',fixture_root=str(base),runtime_sha256=sha(S/'PROPOSTA_RUNTIME.py'),cases=results,all_passed=all(x['passed'] for x in results)))
assert all(x['passed'] for x in results),results
print(json.dumps(dict(controls=len(results),passed=True)))
