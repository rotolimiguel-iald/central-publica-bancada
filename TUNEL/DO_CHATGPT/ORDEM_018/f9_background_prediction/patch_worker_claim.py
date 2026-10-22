"""Repair pre-solver idempotence with byte-exact backup and atomic replacement."""
from pathlib import Path
from datetime import datetime
import hashlib,json
HERE=Path(__file__).resolve().parent
p=HERE/'background_controls.py';old=p.read_bytes();text=old.decode('utf-8')
needle="def prediction_worker(p,point_id,profile_id):"
assert text.count(needle)==1
addition='''def execute_worker_once(p,point_id,profile_id,output,solver=None):
    """Persist an exclusive logical claim BEFORE any solver, even for direct CLI.

    Claims survive failure, interruption and success. Output renaming never creates
    a new attempt for the same protocol/point/profile. A claim without terminal
    receipt means uncertain; neither main nor this worker retries it.
    """
    output=Path(output).resolve()
    require(output.is_relative_to(HERE.resolve()),'Worker output outside unit')
    require(output.parent.is_dir(),'Worker parent directory missing')
    require(point_id in {x['id'] for x in p['points']},'Unknown control point')
    require(profile_id in p['accuracy_profiles'],'Unknown accuracy profile')
    if output.exists() or output.with_name(output.name+'.new').exists():
        raise FileExistsError('Existing output or partial output; solver not invoked')
    logical={'request_id':p['request_id'],'protocol_sha256':sha(HERE/'PROTOCOL.json'),
             'point_id':point_id,'profile_id':profile_id}
    key=hashlib.sha256(json.dumps(logical,sort_keys=True).encode()).hexdigest()
    claims=HERE/'worker_claims';claims.mkdir(exist_ok=True)
    claim=claims/(key+'.claim.json')
    terminal=claims/(key+'.terminal.json')
    if terminal.exists():raise FileExistsError('Terminal attempt already recorded; no retry')
    payload={**logical,'output':str(output),'engine_sha256':sha(Path(__file__)),
             'status':'CLAIMED_MAY_HAVE_RUN_NO_RETRY','pid':os.getpid(),'timestamp_unix':time.time()}
    # open(x) is the atomic cross-process admission decision, not exists().
    # A partial claim is deliberately retained and blocks later entry.
    with claim.open('x',encoding='utf-8') as f:
        json.dump(payload,f,sort_keys=True,allow_nan=False)
        f.flush();os.fsync(f.fileno())
    try:
        # Re-check after claiming, before a solver can spend resources.
        if output.exists() or output.with_name(output.name+'.new').exists():
            raise FileExistsError('Output appeared after claim; no solver invoked')
        result=(solver or prediction_worker)(p,point_id,profile_id)
        write_new(output,result)
        write_new(terminal,{'status':'RESULT_WRITTEN_NO_RETRY','claim':str(claim),
                           'output':str(output),'output_sha256':sha(output)})
        return result
    except BaseException as exc:
        # Abrupt process death can prevent this receipt, but not erase the claim.
        if not terminal.exists():
            write_new(terminal,{'status':'FAILED_OR_INTERRUPTED_NO_RETRY','claim':str(claim),
                               'error_type':type(exc).__name__,'error':str(exc)})
        raise


'''
text=text.replace(needle,addition+needle)
oldcall="        write_new(output,prediction_worker(p,*args.worker));return 0"
assert text.count(oldcall)==1
text=text.replace(oldcall,"        execute_worker_once(p,*args.worker,output);return 0")
compile(text,str(p),'exec')
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');bak=p.with_name(p.name+'.bak_'+stamp)
with bak.open('xb') as f:f.write(old)
assert bak.read_bytes()==old
new=text.encode('utf-8');tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(new)
assert tmp.stat().st_size==len(new) and p.read_bytes()==old
tmp.replace(p)
receipt={'request_id':'f132a1d5-7477-405d-963b-b1659db63328','old_path':str(bak),'old_sha256':hashlib.sha256(old).hexdigest(),'new_sha256':hashlib.sha256(new).hexdigest(),'change':'exclusive durable logical claim before any solver including direct --worker; retain failure/uncertainty','science_runs':0}
with (HERE/'WORKER_FIX_RECEIPT.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2)
print(json.dumps(receipt))