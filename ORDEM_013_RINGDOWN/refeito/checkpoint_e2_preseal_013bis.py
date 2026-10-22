from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
B=Path(__file__).resolve().parents[1];D=B.parent/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if (B/'RINGDOWN_5SIGMA_V1.json').exists():raise ValueError('Preseal checkpoint cannot describe registered stage')
now=datetime.now(timezone.utc)
names=['bis/E2_REVIEW_CANDIDATE_001.json','bis/E2_DESIGN_DRAFT_004.json',
       'bis/e2_review/ACTIVATION_V2_CLOSING_RECEIPT.json','bis/e4_e5_prepare/PE_R1_R2_R3_CLOSING_REVIEW.md',
       'bis/e7_prepare/MAIN_CODE_REVIEW_CLOSING_V3.md','bis/e2_publication_census/E7_INDEPENDENT_REVIEW_V4.md',
       'refeito/seal_e2_013bis.py','refeito/e2_private_directory.ps1',
       'refeito/write_e2_review_application_013bis.py','refeito/smoke_e2_registration_013bis.py',
       'refeito/activate_e4_e5_013bis.py','refeito/close_f0_at_pilot_013bis.py']
record={'utc':now.isoformat(),'goal':'ORDEM_013BIS through final report, not v369 rerun',
 'stage':'E2_CANDIDATE_ASSEMBLED_WAITING_ACTIVATION_SEALER_INDEPENDENT_CLOSURE',
 'registered':False,'seed_exists':(B/'cache/E2_PRIVATE/BLIND_SEED_V1.bin').exists(),
 'null_campaign_outputs':[p.name for p in (B/'bis').glob('RESULT_E2_NULL*')],
 'science_declaration':'No new PE/strain values/waveforms/MC campaign in this stage. Finite toys/mocks and two remnant rows are separate.',
 'files_sha256':{n:sha(B/n) for n in names},
 'required_next':['Read E2_SEALER_CLOSING_REVIEW.md and address blocking findings only; no new user confirmation',
 'Apply existing GO to exact candidate via write_e2_review_application_013bis.py after reading scoped reviews',
 'Windows seal_e2_013bis.py exact candidate and application hashes; creates exclusive NTFS private seed then final activation marker',
 'WSL smoke_e2_registration_013bis.py; launch null_campaign.py and activate_e4_e5_013bis.py',
 'Independent E4 numerical review, formal B2 delivery; F0 stop only before E3.1, then Kerr and pilot',
 'E3.2 budget, E3.3 possible calibration/blind PE, test, E6,E7, final report'],
 'freeze':['bis/e2_code/**/*.py (14)','bis/e4_e5_prepare/**/*.py (66)','bis/e7_prepare/producer/**/*.py (2)'],
 'agents':{'Averroes':'01a0ca10-c0e8-7c62-8ee8-4f153cd38299 — Kerr preparation/repin after final guard',
 'Beauvoir':'01a0ca1b-47e5-73c3-9c38-e334310b6c8c — independent Kerr review in bis/e3_pyring_review',
 'Wegener':'01a0cac1-c4c5-7de1-af2e-e0ba93627b41 — independent E4/E5 numerical review preparation, await activation',
 'Russell':'01a0cac4-d5d0-79c3-85e1-32c4165adaf3 — E2 sealer closing, E7 F3 closed'},
 'budget':json.loads((B/'bis/PART_B_BUDGET_START.json').read_bytes()),
 'scope':'Writes Chatgpt only. No canonical/kernel/memory/Atlas/site/push. F0 old processes not yet stopped; no heavy new job yet.'}
out=B/'bis'/('EXECUTION_CHECKPOINT_'+now.strftime('%Y%m%dT%H%M%SZ')+'.json')
with out.open('x',encoding='utf-8') as f:json.dump(record,f,indent=2,ensure_ascii=False)
print(json.dumps({'file':str(out),'sha256':sha(out)}))
