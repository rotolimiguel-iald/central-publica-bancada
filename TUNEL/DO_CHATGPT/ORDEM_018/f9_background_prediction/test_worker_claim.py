"""Stand-in-only worker admission tests. No CAMB/scientific imports or calls."""
from pathlib import Path
from datetime import datetime
import hashlib,importlib.util,json,sys,threading
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('guarded_background',ROOT/'background_controls.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
protocol=m.read('PROTOCOL.json');tests=[];calls=[]
fixtures=ROOT/('claim_test_fixtures_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'));fixtures.mkdir()
def fixture(name):
 p=fixtures/name;p.mkdir();(p/'PROTOCOL.json').write_bytes((ROOT/'PROTOCOL.json').read_bytes());(p/'BBN_METADATA.json').write_bytes((ROOT/'BBN_METADATA.json').read_bytes());m.HERE=p;return p

def fake(*a):calls.append('stand-in');return {'kind':'TEST_STAND_IN_NOT_SCIENCE'}
def refused(fn):
 try:fn()
 except FileExistsError:return True
 return False

def check(name,cond):
 tests.append({'name':name,'passed':bool(cond)})
 assert cond,name

p=fixture('existing_output');out=p/'out.json';out.write_text('{}');n=len(calls)
check('preexisting_output_refused_before_solver',refused(lambda:m.execute_worker_once(protocol,'center','baseline',out,fake)) and len(calls)==n)
p=fixture('existing_partial');out=p/'out.json';out.with_name('out.json.new').write_text('{');n=len(calls)
check('partial_output_refused_before_solver',refused(lambda:m.execute_worker_once(protocol,'center','baseline',out,fake)) and len(calls)==n)
p=fixture('success');out=p/'out.json';n=len(calls);m.execute_worker_once(protocol,'center','baseline',out,fake)
check('first_attempt_once',len(calls)==n+1 and out.is_file())
check('same_output_repeat_no_solver',refused(lambda:m.execute_worker_once(protocol,'center','baseline',out,fake)) and len(calls)==n+1)
check('renamed_output_repeat_no_solver',refused(lambda:m.execute_worker_once(protocol,'center','baseline',p/'other.json',fake)) and len(calls)==n+1)
check('success_claim_and_terminal_retained',len(list((p/'worker_claims').glob('*.claim.json')))==1 and len(list((p/'worker_claims').glob('*.terminal.json')))==1 and out.with_name('out.json.claim.json').exists())
p=fixture('failure');out=p/'out.json';n=len(calls)
def fail(*a):calls.append('failed_stand-in');raise RuntimeError('controlled stand-in failure')
try:m.execute_worker_once(protocol,'center','baseline',out,fail)
except RuntimeError:pass
check('failure_receipt_retained',any(json.loads(x.read_text())['status']=='FAILED_OR_INTERRUPTED_NO_RETRY' for x in (p/'worker_claims').glob('*.terminal.json')))
check('failure_repeat_no_solver',refused(lambda:m.execute_worker_once(protocol,'center','baseline',p/'retry.json',fake)) and len(calls)==n+1)
p=fixture('uncertain');out=p/'out.json';n=len(calls)
logical={'request_id':protocol['request_id'],'protocol_sha256':m.sha(p/'PROTOCOL.json'),'point_id':'center','profile_id':'baseline'}
key=hashlib.sha256(json.dumps(logical,sort_keys=True).encode()).hexdigest();(p/'worker_claims').mkdir();(p/'worker_claims'/(key+'.claim.json')).write_text('{')
check('truncated_claim_without_terminal_blocks_retry',refused(lambda:m.execute_worker_once(protocol,'center','baseline',out,fake)) and len(calls)==n)
p=fixture('concurrent');out=p/'out.json';n=len(calls);entered=threading.Event();release=threading.Event();errors=[]
def waiting(*a):
 calls.append('concurrent_stand-in');entered.set()
 if not release.wait(5):raise RuntimeError('stand-in wait timed out')
 return {'kind':'TEST_STAND_IN_NOT_SCIENCE'}
def first():
 try:m.execute_worker_once(protocol,'center','baseline',out,waiting)
 except BaseException as e:errors.append(repr(e))
t=threading.Thread(target=first);t.start();assert entered.wait(5)
same=refused(lambda:m.execute_worker_once(protocol,'center','baseline',p/'other.json',fake))
different=refused(lambda:m.execute_worker_once(protocol,'corner_LLL','baseline',out,fake))
release.set();t.join(5)
check('concurrent_same_logical_attempt_only_once',same and not errors and not t.is_alive() and len(calls)==n+1)
check('concurrent_different_point_same_output_refused',different and len(calls)==n+1)
p=fixture('cli_direct');out=p/'out.json';out.write_text('{}');n=len(calls);m.check_delivery=lambda:None;m.prediction_worker=fake
oldargv=sys.argv;sys.argv=['background_controls.py','--worker','center','baseline','--worker-output',str(out)]
try:check('direct_worker_cli_refuses_before_solver',refused(m.main) and len(calls)==n)
finally:sys.argv=oldargv
check('no_camb_numpy_scipy_imported',not any(x in sys.modules for x in ('camb','numpy','scipy')))
m.HERE=ROOT
result={'status':'PASS','checks':tests,'count':len(tests),'stand_in_calls':len(calls),'CAMB_calls':0,'science_runs':0,'fixture_path':str(fixtures),'engine_sha256':m.sha(ROOT/'background_controls.py')}
m.write_new(ROOT/'VALIDACAO_WORKER_CLAIM.json',result);print(json.dumps(result))