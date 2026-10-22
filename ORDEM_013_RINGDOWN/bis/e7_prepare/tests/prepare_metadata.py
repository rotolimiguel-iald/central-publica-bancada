"""Metadata-only preparation. Never opens HDF5/tarball posterior payloads."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parents[1]
BASE=OUT.parents[1]
ROOT=BASE.parent

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def write(name,value):
    p=OUT/name
    raw=(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    temp=p.with_suffix(p.suffix+'.pending')
    with temp.open('xb') as stream: stream.write(raw)
    if temp.stat().st_size!=len(raw): raise IOError('short write')
    import os
    os.link(temp,p); temp.unlink()

dataset=read(BASE/'bis/e0_core/DATASET.json')
nuisance=read(BASE/'NUISANCE_V1.json')
power=read(BASE/'PORTAO_DA_AMPLIACAO_V1.json')
c1=read(BASE/'C1_LEITURAS_v4.json')
selected=set(dataset['sets']['GWTC5_33'])
rows=[r for r in dataset['rows'] if r['product_id'] in selected]
planrows=[]
archives={}
for record,filename in [('21454847','pSEOB.tar.gz'),('17018009','TGR_companion_S250114ax_results.tar.gz')]:
    receipt=BASE/'cache/public'/record/(filename+'.receipt.json')
    r=read(receipt)
    archives[record]={'path':str((receipt.parent/filename).relative_to(ROOT)).replace('\\','/'),
                      'receipt':str(receipt.relative_to(ROOT)).replace('\\','/'),
                      'receipt_sha256':digest(receipt),'sha256':r['sha256']}
for row in rows:
    event=nuisance['conditional_diagnostics']['events'][row['product_id']]
    group=row['dataset'].rsplit('/',1)[0]
    prior_paths={k:[] for k in ('df220','dtau220','Mfdet','af','z')}
    for old,new in [('df','df220'),('dtau','dtau220')]:
        prior_paths[new]=[group+'/'+p['path'] for p in event['priors'][old]['declarations']]
    archive=next(v for k,v in archives.items() if '/'+k+'/' in row['source_path'])
    fields={new:row['field_mapping'][old] for old,new in
            [('df','df220'),('dtau','dtau220'),('mass_detector','Mfdet'),('spin','af'),('redshift','z')]}
    planrows.append(dict(event_id=row['event'],role='calibration',model=row['model'],
                         source_path=row['source_path'],source_sha256=row['source_sha256'],
                         dataset=row['dataset'],N_source=row['N'],fields=fields,
                         mass_frame='detector',mass_unit='solar_mass',prior_paths=prior_paths,
                         tar_path=archive['path'],tar_sha256=archive['sha256'],
                         archive_receipt=archive['receipt'],archive_receipt_sha256=archive['receipt_sha256'],
                         source_pins_status='DECLARADO_FROM_PINNED_METADATA_REHASH_REQUIRED_AT_EXTRACTION'))
assert len(planrows)==33 and len({r['event_id'] for r in planrows})==33
plan={'status':'READY_FOR_REGISTERED_CALIBRATION_EXTRACTION','catalogue':'GWTC5_33',
      'authorization':'NOT_GRANTED_PREPARATION_ONLY','events':planrows,
      'prior_limits':'Mfdet/af/z derived prior OPEN; no factorization or normalization claim',
      'thinning':{'factor':1,'seed':None,'method':'none'}}
write('EXTRACTION_PLAN.json',plan)
sources=['C1_LEITURAS_v4.json','C4_SCHEMA.json','C4_CATALOG_SCHEMA.json','C4_GWTC3_SCHEMA.json',
         'bis/e0_core/DATASET.json','NUISANCE_V1.json','PORTAO_DA_AMPLIACAO_V1.json',
         'bis/F2_CONTROL_SCHEMAS.json','bis/e1_selection/SELECTION_AND_CONTROLS.json',
         'bis/e2_code/registration_guard.py']
inventory={str((BASE/s).relative_to(ROOT)).replace('\\','/'):
           {'sha256':digest(BASE/s),'bytes':(BASE/s).stat().st_size,'mode':'METADATA_OR_CODE_ONLY'} for s in sources}
order=ROOT/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md'
inventory[order.relative_to(ROOT).as_posix()]={'sha256':digest(order),'bytes':order.stat().st_size,'mode':'ORDER_E2_E7_LIMITS_READ'}
for v in archives.values():
    p=ROOT/v['receipt'];inventory[v['receipt']]={'sha256':digest(p),'bytes':p.stat().st_size,'mode':'ARCHIVE_RECEIPT_ONLY'}
write('SOURCE_PINS.json',{'status':'REAL_HASHED_METADATA_NO_NEW_POSTERIOR_READ',
                       'created_utc':datetime.now(timezone.utc).isoformat(),'sources':inventory,
                       'dataset_products':len(dataset['rows']),'selected_plan_products':len(planrows),
                       'metadata_mappings':[dict(dataset=r['dataset'],fields=r['fields']) for r in planrows],
                       'nuisance_gate':nuisance['gate'],
                       'local_covariance_status':nuisance['synthetic_E2_nuisance_INPUT']['status']})
readings={r['reading']:{'N_target_information':None,'status':'OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED',
                      'C1_scope':r['canonical_scope'],
                      'conditional_E0_targets':[p for p in power['planning_targets'] if p['reading']==r['reading']]}
          for r in c1['rows']}
producer=OUT/'producer'
tree={p.relative_to(producer).as_posix():digest(p) for p in producer.rglob('*.py')}
rel=OUT.relative_to(ROOT).as_posix()
e7={'guard_path':'ORDEM_013_RINGDOWN/bis/e2_code/registration_guard.py',
    'guard_sha256':digest(BASE/'bis/e2_code/registration_guard.py'),
    'guard_pin_status':'OBSERVED_DRAFT_RECHECK_WITH_PRINCIPAL_BEFORE_E2',
    'producer_directory':rel+'/producer','producer_tree_sha256':tree,
    'plan_path':rel+'/EXTRACTION_PLAN.json','plan_sha256':digest(OUT/'EXTRACTION_PLAN.json'),
    'nuisance_path':'ORDEM_013_RINGDOWN/NUISANCE_V1.json','nuisance_sha256':digest(BASE/'NUISANCE_V1.json'),
    'readings':readings}
write('E2_INCLUDE.json',{'status':'FRAGMENT_FOR_PRINCIPAL_NOT_A_REGISTRATION', 'e7':e7,
      'extra_code_roots':[{'relative_to_Chatgpt':rel+'/producer','files_sha256':tree}],
      'input_pins_relative_to_Chatgpt':{**{k:v['sha256'] for k,v in inventory.items() if not k.endswith('.py')},
        rel+'/EXTRACTION_PLAN.json':digest(OUT/'EXTRACTION_PLAN.json'),rel+'/PLAN.md':digest(OUT/'PLAN.md')}})
print(json.dumps({'metadata_only':True,'events_planned':len(planrows),'producer_sha256':tree},indent=2))
