"""AST/bytes packaging only; never imports a scientific candidate."""
import ast
import datetime
import hashlib
import json
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
RID=json.loads((ROOT/'IDENTIDADE_PREPARACAO.json').read_bytes())['request_id']

def pin(p):
    p=Path(p).resolve();b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def write_bytes(name,b):
    p=ROOT/name
    if p.exists():
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        bak.write_bytes(old);assert bak.read_bytes()==old
    temp=p.with_name(p.name+'.tmp')
    with temp.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert temp.read_bytes()==b and b
    os.replace(temp,p);assert p.read_bytes()==b

def write(name,doc):write_bytes(name,(json.dumps(doc,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())

def literal(path,name):
    tree=ast.parse(path.read_bytes())
    values=[ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)]
    assert len(values)==1;return values[0]

def main():
    request=BASE/'F9_I03_QUALIFICATION_PREPARATION_REQUEST.json';req=json.loads(request.read_bytes())
    assert req['request_id']=='b89a3fc5-244f-4c72-8f59-7b2ecc74c62b'
    for field in ('basis','I03_static_review'):assert pin(req[field]['path'])==req[field]
    paths={'builder':'f9_joint_covariance_preparation/joint_covariance.py',
      'metadata':'f9_joint_covariance_preparation/METADATA_ESTRUTURA_FAMILIA.json',
      'primitive':'covariance_support/qualify_stellar_family.py',
      'consumer':'f9_likelihood_consumer_preparation/likelihood_consumer.py',
      'backend':'covariance_support/linear_gaussian.py','support':'covariance_support/singular_gaussian_v2.py',
      'helpers':'f9_matrix_consumer_qualification_preparation/cases.py',
      'layout':'f9_structural_layout_preparation/LAYOUT_ESTRUTURAL_3CMB_13BAO.json',
      'design':'h0dn_documentary_review/linear_design/ESPECIFICACAO_LINEAR.json'}
    sources={k:pin(BASE/p) for k,p in paths.items()}
    meta=json.loads(Path(sources['metadata']['path']).read_bytes())
    assert literal(Path(sources['builder']['path']),'METADATA_SHA256')==sources['metadata']['sha256']
    inherited={}
    groups=[meta['source_pins'],literal(Path(sources['consumer']['path']),'SOURCE_PINS'),
            literal(Path(sources['consumer']['path']),'ASSEMBLY_SOURCE_PINS')]
    for group in groups:
        for rec in group.values():
            assert pin(rec['path'])==rec
            inherited[rec['path']]=rec
    selected=[r for r in meta['family_labels'] if r['label'] in ('STELLAR_0_000__SBF_UPSTREAM_M_ONLY','STELLAR_1_055__SBF_UPSTREAM_M_ONLY')]
    assert len(selected)==2 and selected[0]['fraction_strings']==['0']*4 and selected[1]['fraction_strings']==['1/4']*4
    assert selected[1]['sign_scenario']=='cepheid_opposite'
    runtime_path=BASE/'f9_matrix_consumer_qualification_preparation/RUNTIME_INVENTORY.json'
    runtime=json.loads(runtime_path.read_bytes())
    for rec in runtime['files']:assert pin(rec['path'])==rec
    runtime['this_unit_status']='BYTES_RECHECKED; NO_NUMPY_IMPORT_OR_NEW_NATIVE_EXECUTION'
    runtime['previous_inventory']=pin(runtime_path)
    runtime['previous_finite_execution_receipt']=req['basis']
    write('RUNTIME_INVENTORY.json',runtime)
    driver_source=BASE/'f9_matrix_consumer_qualification_preparation/driver.py'
    text=driver_source.read_text(encoding='utf-8')
    tree=ast.parse(text)
    old=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='worker')
    source_lines=text.splitlines(keepends=True)
    worker_text=(ROOT/'worker_template.py').read_text(encoding='utf-8')
    worker_ast=ast.parse(worker_text);new=next(n for n in worker_ast.body if isinstance(n,ast.FunctionDef) and n.name=='worker')
    replacement=''.join(worker_text.splitlines(keepends=True)[new.lineno-1:new.end_lineno])+'\n'
    text=''.join(source_lines[:old.lineno-1])+replacement+''.join(source_lines[old.end_lineno:])
    changes={
      'f9_matrix_consumer_qualification_preparation':'f9_i03_covariance_qualification_preparation',
      '755c3b08-e8a6-448d-a7b1-1ec08d4dc7c7':RID,
      'Q01_MATRIX_CONSUMER_JOIN':'I03_COVARIANCE_CONSUMER_JOIN',
      'Q01_MATRIX_CONSUMER_ROOT_DECISION_V1':'I03_COVARIANCE_ROOT_DECISION_V1',
      'FIVE_SYNTHETIC_MATRIX_JOIN_CASES_ONLY':'SIX_SYNTHETIC_COVARIANCE_JOIN_CASES_ONLY',
      "['J01','J02','J03','J04','J05']":"['V01','V02','V03','V04','V05','V06']",
      'One future supervised matrix-join control':'One future supervised I03 covariance-join control'}
    for before,after in changes.items():assert before in text; text=text.replace(before,after)
    ast.parse(text);write_bytes('driver.py',text.encode())
    lineage={'request_id':RID,'parent_request':pin(request),'basis':req['basis'],
       'I03_static_review':req['I03_static_review'],'direct':sources,'inherited':list(inherited.values()),
       'driver_template':pin(driver_source),'runtime_snapshot':pin(runtime_path),
       'scope_of_inherited_error_inputs':'hash custody only; never parsed/imported as scientific values',
       'primitive_loader':'original function AST only; no historical main or audit_inputs import'}
    write('SOURCE_LINEAGE.json',lineage)
    contract={'schema':'I03_COVARIANCE_PREPARATION_V1','request_id':RID,'unit':'I03_COVARIANCE_CONSUMER_JOIN',
      'status':'PREPARATION_ONLY_PENDING_INDEPENDENT_REVIEW_AND_ROOT_DECISION','sources':sources,
      'lineage':pin(ROOT/'SOURCE_LINEAGE.json'),'runtime':pin(ROOT/'RUNTIME_INVENTORY.json'),
      'case_order':['V01','V02','V03','V04','V05','V06'],'selected_scenarios':selected,
      'budgets':{'cases':6,'builder_constructors':1,'build_attempts':5,'primitive_calls':16,
        'consumer_prepare_attempts':4,'backend_constructors':3,'evaluate_attempts':2,
        'reference_stellar_pairs':63368,'max_reference_fraction_bits':8192,
        'seconds_nominal':120,'worker_cooperative_seconds':80,'wait_seconds':90,'output_acceptance_bytes_per_stream':131072},
      'acceptance':{'matrix_comparison':'EXACT_F64_EQUALITY_TO_DYADIC_RATIONAL_PAIR_REFERENCE',
                    'quadratic_absolute_tolerance':2e-7,'uniform_certificate':False},
      'decision_schema':{'schema':'I03_COVARIANCE_ROOT_DECISION_V1','request_id':RID,'unit':'I03_COVARIANCE_CONSUMER_JOIN',
        'authorize_single_execution':'FUTURE_BOOLEAN_NOT_AUTHORIZATION','manifest_sha256':'FUTURE_REAL_HASH',
        'review_reference':'FUTURE_INDEPENDENT_REVIEW','scope':'SIX_SYNTHETIC_COVARIANCE_JOIN_CASES_ONLY'},
      'not_covered':['all600scenarios','real covariance/MM/O01/O02','assembler or cosmological solver','physical priors/theta integration',
        'independent absolute normalization oracle','I02guard/FS/controller39f88/P3','Windows system DLL closure',
        'hard RAM/disk caps','Q01entire/Q02/Q03/V1/observed/sigma']}
    write('CONTROL_CONTRACT.json',contract)
    for name in ('cases.py','worker_template.py','driver.py','build_preparation.py'):ast.parse((ROOT/name).read_bytes(),filename=str(ROOT/name))
    for name in ('AUTH.json','CLAIM.json','RUN_CLAIM.json','ROOT_DECISION.json','execution_once'):assert not (ROOT/name).exists()
    for rec in list(sources.values())+list(inherited.values()):assert pin(rec['path'])==rec
    write('STATIC_PREPARATION_RECEIPT.json',{'request_id':RID,'status':'BYTES_AND_AST_ONLY',
       'candidate_imports':0,'numpy_imports':0,'scientific_execution':0,'observed_values_read':False,
       'source_files_direct':len(sources),'source_files_inherited':len(inherited),
       'runtime_files_rechecked':len(runtime['files']),'runtime_bytes_rechecked':sum(r['bytes'] for r in runtime['files']),
       'case_count':6,'checks':['parent/basis/I03review pins','builder metadata identity','scenario selection in metadata',
         'inherited pins only, no error values parsed','runtime bytes recheck','driver template replacements','AST syntax only','noAUTH/CLAIM/execution'],
       'review':'PENDING','matrices_constructed':0})
    names=['IDENTIDADE_PREPARACAO.json','cases.py','worker_template.py','driver.py','build_preparation.py',
       'CONTROL_CONTRACT.json','SOURCE_LINEAGE.json','RUNTIME_INVENTORY.json','STATIC_PREPARATION_RECEIPT.json','REFERENCIAS_E_COMANDO.md']
    write('MANIFESTO_PREPARACAO.json',{'request_id':RID,'unit':'I03_COVARIANCE_CONSUMER_JOIN','status':contract['status'],
       'members':[pin(ROOT/n) for n in names],'backups':[pin(p) for p in sorted(ROOT.glob('*.bak_*'))],
       'excludes':['MANIFESTO_PREPARACAO.json','RECIBO_COORDENACAO.json'],'authorization_created':False,'execution_created':False})
    print(json.dumps({'manifest':pin(ROOT/'MANIFESTO_PREPARACAO.json'),'status':'PREPARATION_ONLY'}))

if __name__=='__main__':main()
