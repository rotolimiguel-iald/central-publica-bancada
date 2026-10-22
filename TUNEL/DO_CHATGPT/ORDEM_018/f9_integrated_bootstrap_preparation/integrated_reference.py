"""External, stdlib-only custody and independent outer-sum reference.

Reads actual committed I02 bytes. Does not import the theta algorithm or invoke
likelihood/native background a second time. A passing reference is engineering
consistency, not an independent validation of CAMB or a physical error bound.
"""
import base64
from fractions import Fraction
import itertools
import math
import os
from pathlib import Path
import stat
from posix_protocol import canonical, document, need, read_bytes, sha

MODELS=('H1_TGL','H2_LCDM','H3_beta_free','H4_Cepheid','H5_rd_free')

def unpack(root,claim_path,cap):
    raw=read_bytes(str(claim_path),cap);claim=document(raw)
    need(claim['schema']=='F9_DURABLE_CLAIM_V1' and claim['identity_sha256']==sha(canonical(claim['identity'])),'REFERENCE_CLAIM_IDENTITY')
    stem=claim_path.name[:-len('.claim.json')]
    need(not (root/(stem+'.failure.json')).exists(),'FAILURE_RECEIPT_PRESENT')
    result_raw=read_bytes(str(root/(stem+'.result.json')),cap);row=document(result_raw)
    need(row['schema']=='F9_DURABLE_RESULT_V1' and row['claim_sha256']==sha(raw),'REFERENCE_RESULT_LINK')
    payload={}
    for name,item in row['files'].items():
        data=base64.b64decode(item['base64'],validate=True)
        need(len(data)==item['bytes'] and sha(data)==item['sha256'],'REFERENCE_PAYLOAD_PIN');payload[name]=data
    return claim,payload,sha(result_raw)

def store_measurements(roots):
    inodes={};paths=0;creation_inodes=set()
    for root in roots.values():
        for path in Path(root).iterdir():
            s=path.lstat();need(stat.S_ISREG(s.st_mode) and s.st_uid==os.geteuid() and stat.S_IMODE(s.st_mode)==0o600,'STORE_MEMBER_TYPE')
            key=(s.st_dev,s.st_ino);inodes[key]=(s.st_size,s.st_blocks*512);paths+=1
            if path.name.startswith('.pending_') or path.name.endswith('.claim.json'):creation_inodes.add(key)
    return {'physical_unique_inode_bytes':sum(x[0] for x in inodes.values()),
            'allocated_unique_inode_bytes':sum(x[1] for x in inodes.values()),'unique_inodes':len(inodes),
            'exclusive_creation_inodes':len(creation_inodes),'paths':paths}

def verify(*, roots, result, recipe, family_ids, checkpoint):
    need([r['scenario_id'] for r in result['scenarios']]==family_ids and len(family_ids)==600,'REFERENCE_FULL_ORDERED_FAMILY')
    root=Path(roots['nodes']);cap=recipe['resources']['max_record_bytes'];unit=result['execution_unit_id']
    tables={name:{} for name in family_ids};backgrounds={};cache_hits=new_calls=0;chain=[];nodes=0
    for path in sorted(root.glob('background_*.claim.json')):
        checkpoint();claim,files,pin=unpack(root,path,cap)
        receipt=document(files['receipt_json']);packet_hash=sha(files['packet_json'])
        need(receipt['nonce']==claim['token'] and receipt['solver_calls_attempted']==receipt['solver_calls_returned']==1,'REFERENCE_BG_COUNTS_NONCE')
        need(receipt['request_id']==unit+':background' and receipt['observed_reads'] is False,'REFERENCE_BG_SCOPE')
        need(packet_hash not in backgrounds,'DUPLICATE_BACKGROUND_PACKET')
        backgrounds[packet_hash]={'receipt_sha256':sha(files['receipt_json']),'nonce':claim['token'],'result_pin':pin}
    need(len(backgrounds)==125,'REFERENCE_EXACT_BACKGROUND_COUNT')
    for path in sorted(root.glob('node_*.claim.json')):
        checkpoint();claim,files,pin=unpack(root,path,cap);desc=claim['identity']['descriptor'];env=document(files['envelope_json'])
        conditional=env['conditional_result'];receipt=env['receipt'];scenario=desc['execution_unit_id'][len(unit)+1:]
        need(desc['execution_unit_id']==unit+':'+scenario and scenario in tables,'REFERENCE_SCENARIO')
        key=tuple(Fraction(v,desc['dyadic_denominator']) for v in desc['dyadic_numerators'])
        need(key not in tables[scenario],'REFERENCE_DUPLICATE_NODE')
        need(receipt['node_id']==desc['node_id']==claim['key'] and receipt['conditional_result_reference']['sha256']==sha(canonical(conditional)),'REFERENCE_NODE_CHAIN')
        prov=conditional['provenance'];bg=backgrounds[prov['background_sha256']]
        need(receipt['background_execution_reference']['sha256']==bg['receipt_sha256'],'REFERENCE_BACKGROUND_BINDING')
        need(prov['assembly_sha256']==sha(files['assembly_json']) and prov['precision_sha256']==sha(files['precision_json']),'REFERENCE_NODE_ARTIFACTS')
        need(conditional['status']=='ENGINEERING_ONLY' and all(conditional[k] is None for k in ('p','sigma','verdict','lnB','absolute_evidence')),'REFERENCE_NO_PHYSICAL_VERDICT')
        need(conditional['normalization']['rank']==211 and conditional['normalization']['eta_dimension']==63,'REFERENCE_SUPPORT_NORMALIZATION')
        values={}
        for model in MODELS:
            value=conditional['models'][model]['log_conditional_integral']
            if value=={'$float':'-inf'}:value=-math.inf
            else:need(type(value) in (float,int) and math.isfinite(value),'REFERENCE_FINITE_LOG')
            values[model]=value
        tables[scenario][key]=values;nodes+=1;chain.append(pin)
        calls=receipt['background_calls_this_callback'];need(calls in (0,1),'REFERENCE_CALL_FIELD')
        new_calls+=calls;cache_hits+=1-calls
    need(nodes==75000 and new_calls==125 and cache_hits==74875,'REFERENCE_FULL_NODE_CACHE_COUNTS')
    maximum_gap=0.;comparisons=0
    for scenario,record in zip(family_ids,result['scenarios']):
        need(len(tables[scenario])==125,'REFERENCE_FULL_FINEST_GRID')
        for level_record in record['theta_result']['levels']:
            level=level_record['level'];need(level in (1,2),'REFERENCE_LEVEL');n=2**level
            for model in MODELS:
                terms=[]
                for indices in itertools.product(range(n+1),repeat=3):
                    key=tuple(Fraction(i,n) for i in indices);value=tables[scenario][key][model]
                    if value==-math.inf:continue
                    weight=Fraction(math.prod(1 if i in (0,n) else (4 if i%2 else 2) for i in indices),(3*n)**3)
                    terms.append(value+math.log(weight.numerator)-math.log(weight.denominator))
                expected=level_record['models'][model]['log_relative_integral_without_log_kappa']
                if not terms:need(expected is None,'REFERENCE_ZERO_RULE');continue
                top=max(terms);actual=top+math.log(math.fsum(math.exp(v-top) for v in terms))
                gap=abs(actual-expected);need(gap<=recipe['integrated_reference']['absolute_logsum_tolerance'],'INDEPENDENT_OUTER_SUM_MISMATCH')
                maximum_gap=max(maximum_gap,gap);comparisons+=1
    return {'schema':'F9_INTEGRATED_EXTERNAL_REFERENCE_V1','scope':'CUSTODY_AND_RATIONAL_OUTER_SUM_NOT_SOLVER_ERROR_BOUND',
            'node_count':nodes,'background_count':len(backgrounds),'cache_hits':cache_hits,'sum_comparisons':comparisons,
            'maximum_absolute_logsum_difference':maximum_gap,'node_result_chain_sha256':sha(canonical(chain)),
            'background_nonces':sorted(v['nonce'] for v in backgrounds.values()),'store':store_measurements(roots),
            'p':None,'sigma':None,'verdict':None}
