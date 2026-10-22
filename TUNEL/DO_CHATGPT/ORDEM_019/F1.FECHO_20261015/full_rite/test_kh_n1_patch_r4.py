"""Real pre-audit contract tests; no import or execution of um.py."""
from pathlib import Path
import ast, copy, datetime as dt, hashlib, importlib.util, json, re, time
P=Path(__file__).resolve().parent; U=P.parent
b=P/'build_kh_n1_patch_r3.py'
s=importlib.util.spec_from_file_location('kh_builder',b);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
D=P/'kh_patch_tests_r4';D.mkdir(exist_ok=False)
def pin(p):
 p=Path(p);r=p.read_bytes();return dict(path=str(p.resolve()),sha256=hashlib.sha256(r).hexdigest(),bytes=len(r))
def put(n,d):
 p=D/n;m.exclusive(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode());return p
start=dt.datetime.now(dt.timezone.utc).isoformat();t=time.perf_counter()
source=U/'candidate_r4/um.py';raw=source.read_bytes();_,emb=m.literal(ast.parse(raw.decode()),'_EMBEDDED_KERNEL_FILES')
cp=P/'kh_patch_tests_r3/KH_N1_V394_PREAUDIT_CONTRACT_R3.json';c=json.loads(cp.read_bytes());lt=Path(c['audit_log']['path']).read_text(encoding='utf-8');parsed=m.parse_audit_log(lt)
rows=[]
def case(name,fn,refuse=False):
 try:fn();ok=not refuse;error=None
 except Exception as e:ok=refuse;error=type(e).__name__+': '+str(e)
 rows.append(dict(name=name,passed=ok,expected_refusal=refuse,error=error));print(name,ok,flush=True)
case('actual_preaudit_contract',lambda:m.validate_contract(c,emb))
for field in ['decl','thm','axiom_report_entries','nao_lidas_pelo_regex','fora_do_trio','sorryAx_no_log_do_audit']:
 x=copy.deepcopy(c);x[field]+=1;case('changed_'+field,lambda x=x:m.validate_contract(x,emb),True)
x=copy.deepcopy(c);x['decl']+=1;x['axiom_report_entries']+=1;case('coherent_decl_and_entries_plus_one',lambda:m.validate_contract(x,emb),True)
x=copy.deepcopy(c);x['decl']=True;case('boolean_count',lambda:m.validate_contract(x,emb),True)
total=next(l for l in lt.splitlines() if l.startswith('TGL_AXIOM_COVERAGE_TOTAL'));case('duplicate_TOTAL',lambda:m.parse_audit_log(lt+'\n'+total+'\n'),True)
name=next(n for n in parsed['reports']['complete'] if re.fullmatch(r'[A-Za-z_][A-Za-z_0-9.]*',n))
pat="'"+re.escape(name)+r"' (?:depends on axioms:\s*\[[^]]*\]|does not depend on any axioms)"
missing,nremoved=re.subn(pat,'',lt,flags=re.S);assert nremoved>0
case('missing_unique_declaration_all_rows',lambda:m.parse_audit_log(missing),True)
case('outside_trio_in_actual_row',lambda:m.parse_audit_log(lt.replace('propext','UnexpectedAxiom',1)),True)
case('sorryAx_in_actual_row',lambda:m.parse_audit_log(lt.replace('propext','sorryAx',1)),True)
audit=json.loads(Path(c['audit_receipt']['path']).read_bytes());audit['exit_code']=1
x=copy.deepcopy(c);x['audit_receipt']=pin(put('FAILED_AUDIT_FIXTURE.json',audit));case('failed_receipt',lambda:m.validate_contract(x,emb),True)
x=copy.deepcopy(c);x['audit_log']['sha256']='0'*64;case('bad_log_pin',lambda:m.validate_contract(x,emb),True)
em=copy.deepcopy(emb);k='TGLExt/TimeGravitonScalar.lean';em[k]+='\n-- coherent mutation fixture\n';x=copy.deepcopy(c);x['formal_files_sha256'][k]=m.digest(em[k].encode());case('coherent_embedded_and_contract_mutation',lambda:m.validate_contract(x,em),True)
patched,detail=m.compose(raw.decode(),c,cp,cp.read_bytes());before=ast.parse(raw.decode());after=ast.parse(patched)
def fc(tree):return {(type(n).__name__,n.name):ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
def require(value):
 if not value:raise AssertionError('Requirement failed')
case('all_functions_classes_unchanged',lambda:require(fc(before)==fc(after)))
original=next(s for s in m.literal(before,'_V393_SPECS')[1] if s['nome']=='kh_n1_cobertura_v393');changed=next(s for s in m.literal(after,'_V393_SPECS')[1] if s['nome']=='kh_n1_cobertura_v393')
case('full_historical_spec_preserved',lambda:require(changed['extras']['v393_original_spec_preserved']==original))
receipt=dict(passed=all(r['passed'] for r in rows),start_utc=start,end_utc=dt.datetime.now(dt.timezone.utc).isoformat(),seconds=time.perf_counter()-t,builder=pin(b),test_script=pin(__file__),source=pin(source),contract=pin(cp),tests=rows,counts={k:v for k,v in parsed.items() if k!='reports'},report_lengths={k:len(v) for k,v in parsed['reports'].items()},patch_detail=detail,patched_sha256=m.digest(patched.encode()),previous_attempt=pin(P/'kh_patch_tests_r3/PATCH_TEST_RECEIPT_R3.json'),fixture_correction={'previous_failure':'Removed only one duplicate print; unique declaration set was unchanged. Correct refusal test removes all rows of one declaration.','declaration':name,'removed_rows':nremoved},scope='Actual separately measured full-audit log and receipts; local negative fixtures and AST-only composition. No um.py execution.')
r=put('PATCH_TEST_RECEIPT_R4.json',receipt);print(json.dumps(dict(receipt=pin(r),passed=receipt['passed']),ensure_ascii=False));raise SystemExit(0 if receipt['passed'] else 1)
