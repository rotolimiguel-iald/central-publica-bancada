"""T03 per-reading authorization and EDOM receipt on exceptional PE exits."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,os
B=Path(__file__).resolve().parents[2];C=B/'bis/e2_code_v1_1';D=B/'bis/015/t03'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def replace(s,a,b):
    if s.count(a)!=1:raise ValueError('Nonunique anchor: '+a[:80])
    return s.replace(a,b)
def main():
    backup=D/'reading_failure_before_001';backup.mkdir(exist_ok=False);rows=[]
    for name in ('blinding.py','pe_runner.py'):
        p=C/name;raw=p.read_bytes()
        with (backup/name).open('xb') as f:f.write(raw)
        s=raw.decode()
        if name=='blinding.py':
            s=replace(s,'import hashlib,hmac','import hashlib,hmac,math,re\nfrom numbers import Real')
            start=s.index('def unblinding_allowed(')
            s=s[:start]+'''def unblinding_allowed(registration,reading,information,systematic_gate,receipt):
    """A per-reading permission check, not a physical-significance verdict."""
    if systematic_gate is not True or not isinstance(reading,str):return False
    if not isinstance(registration,dict) or not isinstance(receipt,dict):return False
    config=registration.get('blinding',{})
    targets=config.get('minimum_information_to_unblind_by_reading',{})
    if not isinstance(targets,dict):return False
    threshold=targets.get(reading)
    def finite_positive(x):
        return isinstance(x,Real) and not isinstance(x,(bool,np.bool_)) and math.isfinite(x) and x>0
    if not finite_positive(threshold) or not finite_positive(information) or information<threshold:return False
    pin=receipt.get('dataset_sha256');expected=config.get('unblinding_dataset_sha256')
    if not isinstance(pin,str) or re.fullmatch('[0-9a-f]{64}',pin) is None or pin!=expected:return False
    return bool(receipt.get('status')=='REGISTERED_UNBLINDING_GATE_MET' and
                receipt.get('reading')==reading and receipt.get('scope')=='per-reading' and
                receipt.get('independent_review_passed') is True and
                receipt.get('seed_commitment_sha256')==config.get('seed_commitment_sha256') and
                receipt.get('information')==information and receipt.get('systematic_gate') is True and
                receipt.get('registration_id')==registration.get('registration_id'))


def select_authorized_reading(columns,registration,reading,information,systematic_gate,receipt):
    """Select already prepared reading-labelled columns; never accesses the seed.

    This does not decrypt a posterior or certify global evidence. Raw shared posterior
    columns are intentionally not a per-reading release: they would expose other readings.
    """
    if not unblinding_allowed(registration,reading,information,systematic_gate,receipt):
        raise ValueError('Per-reading release not authorized')
    allowed=registration['blinding'].get('release_columns_by_reading',{}).get(reading)
    if not isinstance(allowed,list) or not allowed or len(allowed)!=len(set(allowed)):
        raise ValueError('Explicit unique release columns required')
    if any(not isinstance(name,str) or not name.startswith(reading+':') for name in allowed):
        raise ValueError('Release must contain only columns labelled by this reading')
    if receipt.get('released_columns')!=allowed or not set(allowed)<=set(columns):
        raise ValueError('Receipt/available release columns differ')
    return {'status':'PER_READING_COLUMNS_SELECTED_NOT_GLOBAL_CLAIM','reading':reading,
            'columns':{name:columns[name] for name in allowed},'dataset_sha256':receipt['dataset_sha256']}
'''
        else:
            s=replace(s,"    bounds={k:np.quantile(np.asarray(posterior[k],dtype=float),[.005,.995]).tolist() for k in ('mass_1','mass_2','chi_1','chi_2')}\n    if any(not np.isfinite(v).all() for v in bounds.values()):raise ValueError('Nonfinite posterior EDOM region')",
                "    bounds=None if posterior is None else {k:np.quantile(np.asarray(posterior[k],dtype=float),[.005,.995]).tolist() for k in ('mass_1','mass_2','chi_1','chi_2')}\n    if bounds is not None and any(not np.isfinite(v).all() for v in bounds.values()):raise ValueError('Nonfinite posterior EDOM region')")
            s=replace(s,"            if all(bounds[k][0]<=params[k]<=bounds[k][1] for k in bounds):inside+=1", "            if bounds is not None and all(bounds[k][0]<=params[k]<=bounds[k][1] for k in bounds):inside+=1")
            s=replace(s,"    return dict(status='FAILED_EDOM_INSIDE_POSTERIOR_REGION' if inside else 'NO_EDOM_INSIDE_POSTERIOR_REGION',\n                inside=inside,edom=count", "    status='EDOM_RECORDED_NO_POSTERIOR_REGION' if bounds is None else ('FAILED_EDOM_INSIDE_POSTERIOR_REGION' if inside else 'NO_EDOM_INSIDE_POSTERIOR_REGION')\n    return dict(status=status,\n                inside=inside if bounds is not None else None,edom=count")
            s=replace(s,"    except Exception as error:\n        publish_new(outdir/'FAILURE.json',dict(status='FAILED_NO_ACCEPTED_POSTERIOR',error_type=type(error).__name__,",
'''    except Exception as error:
        edom={'status':'EDOM_UNAVAILABLE_BEFORE_SOURCE_INITIALIZATION','log_sha256':None}
        if source_counter is not None:
            try:
                edom=edom_posterior_status(outdir/'EDOM_LOG.jsonl',None,source_counter)
                if not (outdir/'EDOM_SUMMARY.json').exists():publish_new(outdir/'EDOM_SUMMARY.json',edom)
            except Exception as audit_error:
                edom={'status':'EDOM_AUDIT_FAILED','exception_type':type(audit_error).__name__,
                      'message':str(audit_error),'posterior_region_evaluated':False}
        publish_new(outdir/'FAILURE.json',dict(status='FAILED_NO_ACCEPTED_POSTERIOR',error_type=type(error).__name__,edom=edom,''')
        ast.parse(s);out=s.encode();temp=p.with_name(p.name+'.reading_failure.pending')
        with temp.open('xb') as f:f.write(out);f.flush();os.fsync(f.fileno())
        assert temp.stat().st_size==len(out);os.replace(temp,p)
        rows.append(dict(file=name,before_sha256=sha(backup/name),after_sha256=sha(p)))
    result=dict(at=datetime.now(timezone.utc).isoformat(),status='READING_FAILURE_CODE_PENDING_TESTS',files=rows,seed_read=False,real_release=False)
    with (D/'READING_FAILURE_PATCH_001.json').open('xb') as f:f.write((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(result))
if __name__=='__main__':main()
