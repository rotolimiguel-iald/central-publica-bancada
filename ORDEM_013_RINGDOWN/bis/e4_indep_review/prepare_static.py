"""Preparation ONLY: hashes, AST, metadata. Never import scientific modules."""
from pathlib import Path
from datetime import datetime,timezone
import ast,base64,hashlib,json,os
OUT=Path(__file__).resolve().parent;BASE=OUT.parents[1];P=BASE/'bis/e4_e5_prepare'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
    raw=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode();p=OUT/name;t=p.with_suffix(p.suffix+'.pending')
    with t.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if t.stat().st_size!=len(raw):raise IOError('Short staged write')
    os.link(t,p);t.unlink()
names=['PLAN.json','INPUT_MANIFEST.json','SCHEMA.json','deterministic_e4_e5.py','PIN_BUNDLE.json']
files={};snapshot={}
for name in names:
    p=P/name;raw=p.read_bytes();key=p.relative_to(BASE).as_posix()
    files[key]=dict(sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
    snapshot[key]={**files[key],'bytes_base64':base64.b64encode(raw).decode()}
for name in ('tgl_ringdown_prediction.py','FISHER_INPUTS.json'):
    p=BASE/name;files[name]=dict(sha256=sha(p),bytes=p.stat().st_size)
save('SOURCE_PINS.json',dict(status='METADATA_SOURCE_PINS_ONLY',files=files,
 archived_HDF_PSD_QNM_pins='Declared in pinned producer INPUT_MANIFEST; actual bytes rechecked only after activation'))
save('SOURCE_SNAPSHOT.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),files=snapshot))
plan=json.loads((P/'PLAN.json').read_bytes())
pairs=[[mode,reading] for mode in ('220','440') for reading in ('R-B','R-MOD','R-RAIZ-0','R-LIN')]
save('REVIEW_PLAN.json',dict(status='AWAITING_PRINCIPAL_ACTIVATION_AFTER_E2_AND_E4_PRODUCER',
 scientific_execution=False,source_pins_sha256=sha(OUT/'SOURCE_PINS.json'),readings=plan['readings'],
 variants=plan['variants'],forecast_expected_rows=1920,derivative_steps=[3e-5,1e-5],
 derivative_norm_relative_tolerance=1e-5,forecast_relative_tolerance=2e-8,forecast_absolute_tolerance=0,
 other_comparisons_relative_tolerance=2e-8,other_comparisons_absolute_tolerance=2e-10,
 density_pairs=pairs,density_bandwidth_multipliers=plan['E4']['posterior']['bandwidth_multipliers'],
 sample_policy='All paired archived draws; no thinning or filtering',
 numerical_checks_executed=0,producer_ownership='READ_ONLY_OTHER_AUTHOR',
 no_new_posterior_PE_MC_waveform_strain=True))
# Compile bytecode in memory only, never import or execute the code object.
raw=(OUT/'independent_review.py').read_bytes();tree=ast.parse(raw)
compile(tree,str(OUT/'independent_review.py'),'exec',optimize=1)
top_imports=[a.name for n in tree.body if isinstance(n,ast.Import) for a in n.names]
if set(top_imports)&{'numpy','scipy','h5py'}:raise ValueError('Science imported before activation')
save('STATIC_RECEIPT.json',dict(status='PARSED_COMPILED_NOT_EXECUTED',utc=datetime.now(timezone.utc).isoformat(),
 review_script_sha256=sha(OUT/'independent_review.py'),scientific_execution=False,
 producer_imported=False,posterior_values_read=False,numerical_checks_executed=0,
 syntax_only=True,top_level_imports=top_imports,source_snapshot_sha256=sha(OUT/'SOURCE_SNAPSHOT.json')))
package={n:sha(OUT/n) for n in ('independent_review.py','REVIEW_PLAN.json','SOURCE_PINS.json')}
save('REVIEW_PACKAGE.json',dict(status='PREPARED_NOT_AUTHORIZED_NOT_NUMERICALLY_TESTED',
 review_package_sha256=package,static_receipt_sha256=sha(OUT/'STATIC_RECEIPT.json'),
 preparation_sha256=sha(OUT/'PREPARATION.md'),source_snapshot_sha256=sha(OUT/'SOURCE_SNAPSHOT.json'),
 activation_fields=dict(status='TEMPLATE_NOT_AUTHORIZED',allowed_task='E4_E5_INDEPENDENT_REVIEW_ONLY',
 new_test_data_allowed=False,registered_utc=None,review_package_sha256=package,E2_registration_sha256=None,
 producer_result_path=None,producer_result_sha256=None,producer_receipt_path=None,producer_receipt_sha256=None,run_id=None)))
for name,item in files.items():
    if sha(BASE/name)!=item['sha256']:raise ValueError('Source changed during preparation')
print(json.dumps(dict(status='PREPARED_NOT_EXECUTED',package_sha256=sha(OUT/'REVIEW_PACKAGE.json'),
 review_script_sha256=sha(OUT/'independent_review.py'),numerical_checks_executed=0),indent=2))
