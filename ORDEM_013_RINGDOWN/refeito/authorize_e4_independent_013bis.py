"""Authorize the separately prepared finite E4/E5 review after producer completion."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json
B=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(B/'bis/e2_code'))
from registration_guard import checked_registration,sha,publish_new

def main():
    reg,digest=checked_registration()
    review=B/'bis/e4_indep_review';package=json.loads((review/'REVIEW_PACKAGE.json').read_bytes())
    for name,pin in package['review_package_sha256'].items():
        if sha(review/name)!=pin:raise ValueError('Independent review changed before authorization')
    output=B/'bis/e4_e5_prepare/runs/authorized_001'
    result=output/'DETERMINISTIC_DIAGNOSTICS.json';receipt=output/'RESULT_RECEIPT.json'
    values=json.loads(result.read_bytes());rc=json.loads(receipt.read_bytes())
    if values['E2_registration_sha256']!=digest or rc['result_sha256']!=sha(result) or rc['status']!='COMPLETED_DETERMINISTIC_ARCHIVED_DIAGNOSTICS':
        raise ValueError('Producer did not complete under this registration')
    auth={**package['activation_fields'],'status':'AUTHORIZED_BY_PRINCIPAL_AFTER_E2',
      'registered_utc':datetime.now(timezone.utc).isoformat(),'E2_registration_sha256':digest,
      'producer_result_path':str(result),'producer_result_sha256':sha(result),
      'producer_receipt_path':str(receipt),'producer_receipt_sha256':sha(receipt),
      'run_id':'authorized_001','authorizer_sha256':sha(Path(__file__))}
    path=B/'bis/E4_INDEPENDENT_AUTHORIZATION_V1.json';publish_new(path,auth)
    print(json.dumps({'path':str(path),'sha256':sha(path),'status':auth['status']}))

if __name__=='__main__':main()
