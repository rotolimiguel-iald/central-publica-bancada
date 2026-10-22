"""Fail-closed validation for frozen C1 evidence (stdlib only)."""
from pathlib import Path
from collections import Counter
import hashlib
import csv
import json
import math

READINGS = {'R-A','R-B','R-RAIZ-0','R-RAIZ-EP4','R-RAIZ-REST','R-LIN','R-MOD','R-GLOBAL'}
SMALL = {'R-A','R-RAIZ-EP4','R-RAIZ-REST'}
STATUS = 'PASS_NUMERICAL_C1_CONTROLS__KERR_KMS_BRIDGE_STILL_CONDITIONAL'

def require(condition, reason):
    if not condition:
        raise ValueError(reason)

def finite(value, name):
    require(not isinstance(value, bool) and math.isfinite(float(value)), 'Nonfinite/non-numeric '+name)
    return float(value)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def keys(rows, label):
    pairs = [(r['event'],r['reading']) for r in rows]
    require(len(pairs)==len(set(pairs)), 'Duplicate keys: '+label)
    events = {e for e,r in pairs}
    require(len(events)==33, 'Expected 33 events: '+label)
    require(set(pairs)=={(e,r) for e in events for r in READINGS}, 'Incomplete 33 by 8 grid: '+label)
    return set(pairs)

def validate_inputs(raw, catalog):
    csv_keys=keys(raw,'CSV')
    cat_rows=[dict(event=e['event'],reading=r['reading']) for e in catalog['rows'] for r in e['rows']]
    require(keys(cat_rows,'catalog')==csv_keys,'Catalog/CSV keys differ')
    for row in raw:
        for field in ('Gamma_per_second','Gamma_over_omega','delta_tau'):
            finite(row[field],field)
    return {(r['event'],r['reading']):r for r in raw}

def validate_clock(core):
    require(core.get('all_verified') is True,'Clock result is not sealed')
    require(core['P1']['verdict']=='P1_NOT_FALSIFIED_UNDERPOWERED','P1 status changed')
    require(core['P2']['verdict']=='P2_EXCLUDED_IN_READING','P2 status changed')
    require(core['tau_star_alternatives']['unruh_g_excluded'] is True,'Unruh-g result changed')
    bound=finite(core['P2']['tau_star_bound_if_reading_in_tP'],'P2 bound')
    require(bound>0,'Nonpositive P2 bound')
    return dict(P1_excluded=False,P2_excluded=True,unruh_g_excluded=True,
                bound=bound,note=core['P2']['gamma_upper_bound_note'])

def validate_evidence(root, measured, core):
    require(measured.get('status')==STATUS,'Control status changed')
    mandatory={'C1_LEITURAS.json','tgl_ringdown_prediction.py','C4_CATALOG_220.json',
       'C7_INDEPENDENT/tables/event_reading_predictions.csv','cache/casa/um_absoluto.json',
       'refeito/measure_c1_013bis_v2.py','refeito/c1_evidence_guards.py'}
    deps=measured['dependencies']
    require(mandatory <= set(deps),'Missing measured dependency')
    root=root.resolve()
    for rel,digest in deps.items():
        p=(root/rel).resolve()
        require(p.is_relative_to(root),'Dependency outside bench')
        require(sha(p)==digest,'Stale dependency: '+rel)
    with (root/'C7_INDEPENDENT/tables/event_reading_predictions.csv').open(encoding='utf-8-sig') as f:
        raw=list(csv.DictReader(f))
    catalog=json.loads((root/'C4_CATALOG_220.json').read_bytes())
    validated_csv=validate_inputs(raw,catalog)
    rows=measured['csv_checks']
    require(keys(rows,'measured evidence')==set(validated_csv),'Evidence keys differ from hashed sources')
    require(measured['checked']==len(rows)==264,'Incorrect coverage count')
    for r in rows:
        require(set(r['relative_errors'])=={'gamma_per_s','gamma_over_omega','delta_tau'},'Missing error metric')
        for field,v in r['relative_errors'].items():
            require(0<=finite(v,field)<1e-12,'Relative error above threshold')
        require(isinstance(r['sub_resolution'],bool),'Bad classification flag')
        require(r['sub_resolution']==(r['reading'] in SMALL|{'R-GLOBAL'}),'Unexpected small-effect partition')
    n_small=sum(r['reading'] in SMALL for r in rows)
    n_zero=sum(r['reading']=='R-GLOBAL' for r in rows)
    n_sub=sum(r['sub_resolution'] for r in rows)
    require((n_small,n_zero,n_sub)==(99,33,132),'Incorrect classification counts')
    require(measured['sub_resolution_checked']==n_sub,'Reported count mismatch')
    clock=validate_clock(core)
    require(finite(measured['P2_tau_star_bound_tP'],'measured P2 bound')==clock['bound'],'P2 bound differs')
    require(measured['unit_guard_rejected_mixed_dimensions'] is True,'Unit negative control missing')
    require(set(measured['dimensions'])==READINGS|{'R-RAIZ-COHERENT','R-PROP'},'Missing dimensions')
    for reading,dim in measured['dimensions'].items():
        require(dim==['0','0','0' if reading=='R-PROP' else '-1'],'Unexpected derived dimension')
    spins=measured['spin_comparison']
    require([r['spin'] for r in spins]==[0,.3,.5,.6785,.8,.9,.95],'Incomplete spin grid')
    for row in spins:
        require(set(row)=={'spin','exact_qnm','delta_mod','delta_root_zero','delta_mod_bcw_control','mod_bcw_relative_error'},'Incomplete spin schema')
        pair=row['exact_qnm']
        require(isinstance(pair,list) and len(pair)==2,'Incomplete QNM pair')
        require(finite(pair[0],'QNM real')>0 and finite(pair[1],'QNM imaginary')<0,'QNM convention differs')
        for k,v in row.items():
            for item in (v if isinstance(v,list) else [v]): finite(item,k)
    profiles=measured['profile_comparison']
    require(len(profiles)==5 and {r['reading'] for r in profiles}=={'R-A','R-B','R-RAIZ-EP4','R-RAIZ-REST','R-LIN'},'Incomplete or duplicate profiles')
    for row in profiles:
        require(set(row)=={'reading','comparison_redshift','gamma_legacy_over_modern_minus_one','delta_legacy_over_modern_minus_one'},'Incomplete profile schema')
        require(row['comparison_redshift']==0,'Comparison is not at z=0')
        for k in ('comparison_redshift','gamma_legacy_over_modern_minus_one','delta_legacy_over_modern_minus_one'):
            finite(row[k],k)
    return dict(checked=len(rows),small=n_small,zero=n_zero,sub_resolution=n_sub,clock=clock)
