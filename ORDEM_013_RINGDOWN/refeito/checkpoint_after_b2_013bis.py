"""Add a new measured checkpoint; never rewrite prior state or read private seed."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,os
B=Path(__file__).resolve().parents[1];R=B.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    now=datetime.now(timezone.utc);tag=now.strftime('%Y%m%dT%H%M%SZ')
    names=['RINGDOWN_5SIGMA_V1.json','bis/E2_REGISTRATION_RECEIPT.json','bis/E2_REGISTRATION_SMOKE.json',
      'bis/E2_REVIEW_APPLICATION_V2.json','bis/B2_DELIVERY_MANIFEST.json','bis/RESULT_E2_NULL_CAMPAIGN.json',
      'bis/E2_NULL_RECEIPTS_AUDIT_V1.json','bis/E2_CUSTODY_HOST_VERIFIED_V1.json',
      'bis/F0_CLOSED_20260922T215825Z.json','bis/E3_KERR_AUTHORIZATION_V1.json',
      'bis/e3_pyring_preparation/MANIFEST_v3.json',
      'bis/e3_pyring_review/ORCHESTRATOR_R1_N1_CLOSING_RECEIPT.json',
      'bis/e4_indep_review/runs/authorized_001/INDEPENDENT_REVIEW.json',
      'cache/E3_KERR220_CALIBRATION_V1/welch/FAILURE.json',
      'cache/E3_KERR220_CALIBRATION_V1/welch/CONTROLLER.json',
      'cache/E3_KERR220_CALIBRATION_V1/public_psd/CONDITIONING.json']
    facts={n:{'sha256':sha(B/n),'bytes':(B/n).stat().st_size} for n in names}
    budget=json.loads((B/'bis/PART_B_BUDGET_START.json').read_bytes())
    cost=B/'cache/E3_KERR220_CALIBRATION_V1/COST.json'
    value={'objective':'ORDEM_013BIS; continue to final report, not historical v369',
      'utc':now.isoformat(),'status':'B2_DELIVERED_E3_1_KERR_IN_PROGRESS' if not cost.exists() else 'KERR_COST_EXISTS_REVIEW_REQUIRED',
      'hours_elapsed_part_B':(now-datetime.fromisoformat(budget['started_utc'])).total_seconds()/3600,
      'hard_deadline_utc':budget['hard_deadline_utc'],'files':facts,
      'running_tool_session_hint':36271,'session_hint_not_OS_process_identity':True,
      'B2_delivery_sha256':sha(R/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_B2_registro_e_440.md'),
      'F0':'2977 files hashed; no old owned processes remained, no signals necessary',
      'seed_custody':'Seed unchanged; exclusive DACL transferred from Windows sandbox SID to host SID after reviewed fixture. Owner retained. No seed bytes/offsets disclosed. Never open seed for conversation.',
      'immutable':'E2 registration/witness/activation, e2_code14, E7producer2, entire E4python66, Kerr9/manifestv3. Do not modify them for failures.',
      'current_Kerr':'Welch conditioning rejected before sampling, threshold unchanged. Preplanned public_psd sampling started with both detector conditioning receipts. Even controller rc0 requires per-variant convergence/review; equivalence release remains OPEN.',
      'agents':{'A':'Allocation preparation completed; diagnostic exact failed Welch condition authorized, no PE',
        'B':'Pilot audit preparation, no execution; independent Kerr/orchestration review closed',
        'W':'E4 numerical310PASS; frozen E7 producer',
        'R':'Custody closed; post-result null interpretation review only'},
      'next':['Review completed Kerr and diagnostic; run registered full IMR pilot only after Kerr attempt',
        'Measure pilot cost/convergence, register E3.2 budget/jobs before E3.3',
        'Calibrate possible cells and blinded events within remaining40h; preserve failures/gate',
        'B3/B4/test/E6/E7/B5/final with all unpaid costs and scoped verdicts'],
      'not_done':['IMR pilot','E3.2 allocation','new blind PE','E3.3 physical calibration','E6','E7 actual extraction','final report'],
      'script_sha256':sha(Path(__file__))}
    out=B/'bis'/('EXECUTION_CHECKPOINT_'+tag+'.json');raw=(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode()
    with out.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    print(json.dumps({'path':str(out),'sha256':sha(out),'status':value['status']}))
if __name__=='__main__':main()
