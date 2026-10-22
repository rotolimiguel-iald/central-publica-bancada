"""Independent primitive-only fingerprint audit; never builds the stellar covariance."""
import json, hashlib, struct
from fractions import Fraction
from pathlib import Path
from datetime import datetime, timezone
from audit_provenance import OUT, atomic, metadata
B=OUT.parent/'covariance_support'
E=OUT.parent/'h0dn_documentary_review/jagb_extension/residual_systematics'
inputs={}
def read(p):
    m,r=metadata(p);inputs[str(p)]=m;return json.loads(r)
contract=read(E/'CONTRATO_PSD_CANDIDATO.json')
errors=read(E/'ERROR_COMPONENTS.json')
protocol=read(B/'STELLAR_FAMILY_PROTOCOL.json')
result=read(B/'STELLAR_FAMILY_RESULT.json')
checks=[]
def check(name,b):
    checks.append({'name':name,'passed':bool(b)})
    assert b,name
for item in protocol['inputs']+[result['protocol']]:
    m,r=metadata(Path(item['path']));inputs[item['path']]=m
    check('pin:'+item['path'],m['sha256']==item['sha256'] and m['bytes']==item['bytes'])
check('receipt_inputs_match_protocol',result['inputs']==protocol['inputs'])
for mapfile in ['RESIDUAIS_MAPA_SEQ435.json','RESIDUAIS_MAPA_SEQ439.json']:
    record=read(OUT/mapfile)
    for item in record['artefatos']:
        m,r=metadata(Path(item['caminho']));inputs[item['caminho']]=m
        check('map_pin:'+item['caminho'],m['sha256']==item['sha256'] and m['bytes']==item['bytes'])
mk=[r['mas_key'] for r in errors['mas_reference_errors']]
hk=[r['key'] for r in errors['primitive_hms_groups']]
g=contract['groups']
def direct_entries(keys,partition,scenario,key_kind):
    # Independent entrywise definition, without block filling or NumPy.
    membership={key:n for n,grp in enumerate(partition) for key in grp}
    def sign(key):
        fields=key.split('&')
        method=fields[0 if key_kind=='MAS' else 1]
        return -1 if (scenario=='cepheid_opposite' and method.startswith('ceph_')) or (scenario=='SH0ES_JAGB_opposite' and method.startswith('jagb_') and fields[-1]=='SH0ES') else 1
    return [1 if k==l else (sign(k)*sign(l) if k in membership and l in membership and membership[k]==membership[l] else 0) for k in keys for l in keys]
def matrix_bytes(keys,e1,e2,u,v):
    n=len(keys)
    return b''.join(struct.pack('<d',1.0 if i//n==i%n else (u*a+v*b)/4.0) for i,(a,b) in enumerate(zip(e1,e2)))
predicted=[]
for scenario_row in contract['candidate_grid']['sign_scenarios']:
    s=scenario_row['id']
    em1=direct_entries(mk,g['MAS_same_program_at_N4258'],s,'MAS')
    em2=direct_entries(mk,[g['MAS_JAGB_reference_pair']],s,'MAS')
    eh1=direct_entries(hk,g['HMS_by_eleven_hosts'],s,'HMS')
    eh2=direct_entries(hk,[g['HMS_N5643_JAGB_pair']],s,'HMS')
    for t in contract['candidate_grid']['fraction_tuples_order_u_v_p_q']:
        quarters=[Fraction(x)*4 for x in t]
        assert all(x.denominator==1 for x in quarters)
        u,v,p,q=map(int,quarters)
        digest=hashlib.sha256(matrix_bytes(mk,em1,em2,u,v)+matrix_bytes(hk,eh1,eh2,p,q)).hexdigest()
        predicted.append((s,t,digest))
check('all_cases_enumerated',len(predicted)==len(result['cases'])==300)
seen={}
for i,((s,t,digest),reported) in enumerate(zip(predicted,result['cases'])):
    check('entrywise_design_hash:'+str(i),reported['scenario']==s and reported['fractions']==t and reported['design_sha256']==digest)
    if digest in seen:
        check('duplicate_link:'+str(i),reported['same_primitive_design_as']==seen[digest])
    else:
        seen[digest]=i
        check('recorded_rank_and_tolerances:'+str(i),reported['rank']==106 and reported['cutoff_sensitivity_ranks']==[106,106] and reported['null_projector_error']<1e-8 and reported['marginal_error']<1e-15)
check('283_unique_primitive_designs',len(seen)==result['unique_primitive_designs']==283)
check('unchanged_block_scope',not result['global_SN_background_covariance_assembled'] and not result['likelihood_evaluated'] and result['model_verdict'] is None)
doc={'at':datetime.now(timezone.utc).isoformat(),'scope':'PRIMITIVE_ENTRYWISE_FINGERPRINTS_AND_CUSTODY_ONLY',
'author_source_executed':False,'stellar_or_global_C_reassembled':False,'centres_opened_in_this_extension':False,
'previous_review_incidental_text_exposure':'See REVISAO_RESIDUAIS_PSD.json; no blinded-review claim.',
'all_passed':all(x['passed'] for x in checks),'checks':checks,'count_checks':len(checks),
'independent_primitive_designs_matching':len(predicted),'unique_primitive_designs':len(seen),
'author_recorded_metrics_not_reexecuted':{k:result[k] for k in ['baseline_rank','baseline_nullity','pairwise_max_error','wall_seconds','cpu_seconds','numpy']},
'author_recorded_max_null_projector_error':max(x.get('null_projector_error',0) for x in result['cases']),
'author_recorded_max_marginal_error':max(x.get('marginal_error',0) for x in result['cases']),
'limits':'No independent eigendecomposition, physical residual covariance, global support or V1 qualification. Primitive-design uniqueness does not imply injective map to observational covariance.',
'sources':list(inputs.values())}
atomic(OUT/'REVISAO_IMPLEMENTACAO_PSD_ESTELAR.json',json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:doc[k] for k in ['all_passed','count_checks','independent_primitive_designs_matching','unique_primitive_designs','author_recorded_metrics_not_reexecuted','author_recorded_max_null_projector_error','author_recorded_max_marginal_error']},ensure_ascii=False))
