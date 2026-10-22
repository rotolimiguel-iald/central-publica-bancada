"""Immutable operational checkpoint; does not modify canonical memory."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os
B=Path(__file__).resolve().parents[1]

def main():
    files=[
        'RINGDOWN_5SIGMA_V1.json','bis/PART_B_BUDGET_START.json',
        'bis/E2_REGISTRATION_RECEIPT.json','bis/B2_DELIVERY_MANIFEST.json',
        'bis/e3_pyring_review/KERR_CONTINUATION_REVIEW.json',
        'bis/e3_pyring_review/KERR_V2_POST_RESULT_REVIEW.json',
        'bis/E3_KERR_AUTHORIZATION_V2.json','bis/E3_KERR_LAUNCH_V2.json',
        'cache/E3_KERR220_CALIBRATION_V2/public_psd/COMPARISON.json',
        'cache/E3_KERR220_CALIBRATION_V2/public_psd/CONVERGENCE.json',
        'bis/E3_PILOT_FAILURE_AUDIT_V1.json',
        'cache/E3_PSEOB_PILOT_V1/CONTROLLER.json','cache/E3_PSEOB_PILOT_V1/LAUNCH_CONTEXT.json',
        'bis/e3_publication_refresh/PUBLICATION_METADATA_REVIEW_INDEX.json',
        'bis/e3_blind_prepare/MANIFEST.json','bis/e3_blind_prepare/TWO_PHASE_ADDENDUM_RECEIPT.json',
        'bis/e3_injection_prepare/INJECTION_CANDIDATE_DESIGN.json',
        'bis/e3_injection_prepare/METRICS_PLAN_DRAFT_V1.md',
        'bis/E3_CALIBRATION_NOISE_METADATA_V1.json',
        'bis/E3_CALIBRATION_BUDGET_COEFFICIENTS_V1.json',
        'bis/E3_ALTERNATIVE5_METADATA_ONLY_V1.json',
        'bis/e3_allocation_review/REVIEW_RECEIPT_V1.json',
        'bis/e6_prepare/PREPARATION_MANIFEST.json',
    ]
    refs={}
    for name in files:
        p=B/name
        refs[name]={'exists':p.is_file()}
        if p.is_file():
            raw=p.read_bytes();refs[name].update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    now=datetime.now(timezone.utc)
    value={
        'status':'ORDER_ACTIVE_PILOT_NATIVE_FAILURE_DIAGNOSIS_IN_PROGRESS',
        'created_utc':now.isoformat(),
        'active_goal':'ORDEM_013BIS, not historical v369 notifications',
        'references':refs,
        'kerr':'V2 accepted by independent reviewer for descriptive known-event comparison; exact reproduction remains OPEN. V1 failed/partial retained.',
        'pilot':'Original GW250114_PILOT ended -11 after11.011s; group absent, no accepted posterior. Preserve all outputs; no rerun into existing directory.',
        'original_pilot_deadline_utc':'2026-09-23T06:35:19.847427+00:00',
        'global_deadline_utc':'2026-09-24T11:06:33.802143+00:00',
        'active_exec_sessions':[],
        'agents':{
            'A':'01a0ca10-c0e8-7c62-8ee8-4f153cd38299: bounded isolated waveform diagnosis<=10min in e3_pilot_failure_diagnostic, then repair proposal; no E2 edits',
            'B':'01a0ca1b-47e5-73c3-9c38-e334310b6c8c: independent native failure/repair review; observer pending cache-output fix and tests, not required for pilot',
            'W':'01a0cac1-c4c5-7de1-af2e-e0ba93627b41: independent e3_blind_prepare review; E6 author; allocation helper two defects, remains unused',
            'R':'01a0cac4-d5d0-79c3-85e1-32c4165adaf3: metrics draft done, independent E6 prep review next'
        },
        'next':['Get A/B native diagnosis; repair in new version and witnessed amendment, never modify E2 or /opt.',
                'Relaunch reviewed pilot inside original absolute envelope if repair supported.',
                'After pilot, E3.2 budget (including partial cost if needed); immutable versions + active fixed budget projection for download-only then SHA-pinned jobs.',
                'Calibrations/blind jobs then TEST/E6/E7/B3-B5/final; do not stop at milestone.'],
        'budget_helper':'Original optional renderer unused: review F1 symlink containment/F2 serialized size. Also cannot handle failed pilot or download-only phases.',
        'publication':'14 scoped false-published candidates,10unheld; highest SNR GW230919_21571216.8, followed GW241111_11155216.3. Earlier16.3asoverallhighest was incomplete.',
        'confidentiality':'Never read or print blind seed/offsets. Only Chatgpt writes. Canonical memories and E2/runtime frozen.',
    }
    path=B/'bis'/('EXECUTION_CHECKPOINT_'+now.strftime('%Y%m%dT%H%M%S%fZ')+'.json')
    tmp=path.with_name(path.name+'.pending');raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.stat().st_size!=len(raw):raise IOError('Incomplete checkpoint')
    os.link(tmp,path);tmp.unlink()
    print(json.dumps({'path':str(path),'sha256':hashlib.sha256(raw).hexdigest()}))
if __name__=='__main__':main()
