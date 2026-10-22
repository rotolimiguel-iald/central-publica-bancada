"""Bounded documentary checks: hashes, identifiers and errors; no upstream imports or C."""
import json, re, hashlib
from pathlib import Path
from decimal import Decimal
from fractions import Fraction
from itertools import product
from collections import defaultdict
from datetime import datetime, timezone
from audit_provenance import OUT, atomic, metadata

ROOT=OUT.parent
P=ROOT/'h0dn_documentary_review'
J=P/'jagb_extension'
B=J/'residual_systematics'
SNAP=OUT/'residual_psd_snapshot'
SNAP.mkdir(exist_ok=True)
files={}
checks=[]
def pin(path):
    path=Path(path)
    item,raw=metadata(path)
    files[str(path)]=item
    return item,raw
def read_json(path):
    return json.loads(pin(path)[1].decode('utf-8-sig'))
def check(name,condition,detail=None):
    checks.append({'name':name,'passed':bool(condition),'detail':detail})
    assert condition,name
def verify_entry(entry,base):
    path=Path(entry['path'])
    if not path.is_absolute(): path=base/path
    item,raw=pin(path)
    check('sha256:'+str(path),item['sha256']==entry['sha256'])
    if 'bytes' in entry: check('size:'+str(path),len(raw)==entry['bytes'])
    if 'git_blob_sha1' in entry:
        check('git_blob:'+str(path),hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==entry['git_blob_sha1'])
    return path
m=read_json(B/'MANIFESTO_ENTREGA.json')
for name in ['MANIFESTO_ENTREGA.json','REVISAO_RESIDUAIS.md','CONTRATO_PSD_CANDIDATO.json','ERROR_COMPONENTS.json','VALIDACAO_DOCUMENTAL.json','PRIMARY_SOURCES.json']:
    _,raw=pin(B/name)
    atomic(SNAP/name,raw)
for e in m['files']: verify_entry(e,B)
for e in m['inherited_manifests']: verify_entry(e,B)
inherited=[]
for path,base in [(P/'UPSTREAM_MANIFEST.json',P/'upstream'),(J/'SOURCES.json',J/'upstream'),(J/'MANIFESTO_ENTREGA.json',J),(B/'PRIMARY_SOURCES.json',B)]:
    doc=read_json(path)
    for e in doc['files']:
        inherited.append(str(verify_entry(e,base)))
        if 'text_path' in e:
            tp=verify_entry({'path':e['text_path'],'sha256':e['text_sha256']},base)
            inherited.append(str(tp))
c=read_json(B/'CONTRATO_PSD_CANDIDATO.json')
e=read_json(B/'ERROR_COMPONENTS.json')
s=read_json(J/'SELECTION_V01_IDENTIFIERS.json')
for item in [c['selection'],c['errors'],e['source']]+e['inherited_manifests']:
    verify_entry(item,B)
# Only identifier/error groups captured. The observed centre token is skipped,
# never bound, converted, emitted, used in a decision, or saved to this receipt.
source_rows=pin(P/'upstream/data/host_data.dat')[1].splitlines()
host_pattern=re.compile(rb'^\s*(\S+)\s+\S+\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')
def projected(row):
    match=host_pattern.match(source_rows[row['line']-1])
    assert match is not None
    host,sigma,method,anchor,origin=[t.decode('utf-8') for t in match.groups()]
    check('row_identity:'+row['row_id'],[host,method,anchor,origin]==[row[k] for k in ['host','method','anchor','source']])
    sd=Decimal(sigma)
    check('finite_nonnegative_error:'+row['row_id'],sd.is_finite() and sd>=0)
    return {**row,'sigma_mag':str(sd),'mas_key':'&'.join([method,anchor,origin]),'hms_key':'&'.join([host,method,origin])}
hosts=[projected(r) for r in s['v01']['hosts']]
refs=[projected(r) for r in s['v01']['reference_rows']]
refmap={r['mas_key']:r for r in refs}
check('unique_MAS_reference_keys',len(refmap)==len(refs)==14)
check('every_host_MAS_has_reference',all(r['mas_key'] in refmap for r in hosts))
check('reference_errors_match_receipt',refs==e['mas_reference_errors'])
groups=defaultdict(list)
for row in hosts: groups[row['hms_key']].append(row)
check('host_rows_and_HMS_counts',len(hosts)==178 and len(groups)==104)
derived_groups=[{'key':k,'sigma_mag':v[0]['sigma_mag'],'row_ids':[r['row_id'] for r in v]} for k,v in groups.items()]
check('HMS_group_membership_and_errors',derived_groups==e['primitive_hms_groups'])
check('HMS_errors_exactly_equal',all(len({Decimal(r['sigma_mag']) for r in v})==1 for v in groups.values()))
d0=[Decimal(r['sigma_mag'])**2-Decimal(groups[r['hms_key']][0]['sigma_mag'])**2 for r in hosts]
check('D0_zero_without_C_assembly',all(x==0 for x in d0))
jagb=[r for r in hosts if r['method'].startswith('jagb_')]
check('JAGB_errors_exact',jagb==e['jagb_host_errors'])
relevant={r['host'] for r in jagb}
check('twelve_JAGB_rows_eleven_hosts',len(jagb)==12 and len(relevant)==11)
erows=[r for r in hosts if r['host'] in relevant]
check('eleven_host_rows_exact',erows==e['eleven_host_method_rows'])
anchor_rows=pin(P/'upstream/data/anchors.dat')[1].splitlines()
apat=re.compile(rb'^\s*(\S+)\s+\S+\s+(\S+)')
for a in e['anchor_errors']:
    n=int(a['row_id'].split(':L')[1])
    ma=apat.match(anchor_rows[n-1])
    aid,sd=[t.decode() for t in ma.groups()]
    check('anchor_error:'+a['anchor'],aid==a['anchor'] and Decimal(sd)==Decimal(a['sigma_mag']))
g=c['groups']
expected_ref=[[f'{method}_jwst&N4258&{origin}' for method in ['ceph','trgb','jagb']] for origin in ['CCHP','SH0ES']]
check('MAS_program_groups_exact',g['MAS_same_program_at_N4258']==expected_ref and all(k in refmap for v in expected_ref for k in v))
check('MAS_program_groups_disjoint',len({k for v in expected_ref for k in v})==sum(map(len,expected_ref)))
jref=[r['mas_key'] for r in refs if r['method'].startswith('jagb_')]
check('JAGB_reference_pair_exact',g['MAS_JAGB_reference_pair']==jref)
expected_hms=[sorted({r['hms_key'] for r in erows if r['host']==h and r['method'].split('_')[0] in ['ceph','trgb','jagb']}) for h in sorted(relevant)]
check('HMS_host_groups_exact',g['HMS_by_eleven_hosts']==expected_hms)
flat=[k for v in expected_hms for k in v]
check('HMS_groups_disjoint_and_present',len(flat)==len(set(flat)) and set(flat)<=set(groups))
n5643=[r for r in jagb if r['host']=='N5643']
check('N5643_pair_exact',g['HMS_N5643_JAGB_pair']==[r['hms_key'] for r in n5643] and len(n5643)==2)
grid=c['candidate_grid']
axes=[Fraction(x) for x in grid['axis_values']]
expected=[list(map(str,t)) for t in product(axes,repeat=4) if t[0]+t[1]<=Fraction(3,4) and t[2]+t[3]<=Fraction(3,4)]
check('grid_exact_order_and_completeness',grid['fraction_tuples_order_u_v_p_q']==expected and len(expected)==100)
check('grid_contains_baseline',['0','0','0','0'] in expected)
residual_weights=[1-Fraction(t[a])-Fraction(t[b]) for t in expected for a,b in [(0,1),(2,3)]]
check('interior_I_weight_at_least_quarter',min(residual_weights)==Fraction(1,4))
check('three_prespecified_sign_scenarios',[x['id'] for x in grid['sign_scenarios']]==['all_same','cepheid_opposite','SH0ES_JAGB_opposite'])
anchors={r['anchor']:Decimal(r['sigma_mag']) for r in e['anchor_errors']}
coeff={'common_N4258_anchor':anchors['N4258']**2,
       'JAGB_cross_MAS_multiplier_rho_M':Decimal(refmap[jref[0]]['sigma_mag'])*Decimal(refmap[jref[1]]['sigma_mag']),
       'N5643_cross_HMS_multiplier_rho_H':Decimal(n5643[0]['sigma_mag'])*Decimal(n5643[1]['sigma_mag'])}
check('three_error_products_exact',all(v==Decimal(c['candidate_pair_coefficients_mag2'][k]) for k,v in coeff.items()))
check('MAS_HMS_cross_level_exclusion_explicit','not included' in c['latent_cross_MAS_HMS'])
check('documentary_not_ratified','NOT_RATIFIED' in c['status'] and not c['global_C_assembled'] and not c['upstream_executed'])
result={'request_id':c['request_id'],'reviewed_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'HASHES_IDENTIFIERS_ERRORS_AND_SYMBOLIC_PROOF_ONLY',
        'map_consulted_seq':435,'statute':'REAL documentary checks; DERIVED conditional proof; OPEN physical correlations',
        'checks':checks,'all_passed':all(x['passed'] for x in checks),
        'counts':{'checks':len(checks),'inherited_hash_entries':len(inherited),'inherited_unique_paths':len(set(inherited)),
                  'all_unique_pinned_paths':len(files),'hosts':len(hosts),'MAS':len(refs),'HMS':len(groups),
                  'host_group_keys':len(flat),'grid_tuples':len(expected),'sign_scenarios':3},
        'coefficients_mag2':{k:str(v) for k,v in coeff.items()},
        'sources':list(files.values()),
        'source_code_execution':False,'physical_tests':False,'C_assembled':False,'S_g_H0_evidence':False,
        'observed_centres_converted_or_used':False,
        'incidental_public_centres_exposed_by_reviewer_search':True,
        'incident':'An overbroad rg over two archived public texts returned a distance-modulus paragraph and numerical table fragments. Search stopped; no blind-review claim. No centre entered the checks, family, covariance or conclusion.',
        'new_verdict':None}
atomic(OUT/'REVISAO_RESIDUAIS_PSD.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'all_passed':result['all_passed'],'counts':result['counts'],'coefficients_mag2':result['coefficients_mag2'],'receipt':metadata(OUT/'REVISAO_RESIDUAIS_PSD.json')[0]},ensure_ascii=False))
