"""Reconstruct V00/V01 identifier selection; never parse observed centres or run H0DN."""
from pathlib import Path
from collections import Counter, defaultdict
import fnmatch
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
ANCHORS={'N4258','MW','LMC','SMC','M31','ALL'}

def source(relative):
    a=ROOT/'upstream'/relative
    return a if a.exists() else PARENT/'upstream'/relative

def records(relative,columns):
    # Select identifier columns only; numeric measurement fields never parsed.
    result=[]
    for line_no,line in enumerate(source(relative).read_text(encoding='utf-8').splitlines(),1):
        tokens=re.split(r'[#;]',line,maxsplit=1)[0].split()
        if not tokens:continue
        if tokens[0].lower() in {'host','name','no','groupname'}:continue
        result.append({'row_id':relative+':L'+str(line_no),'line':line_no,
                       **{name:tokens[index] for name,index in columns.items()}})
    return result

def write_new(name,obj):
    p=ROOT/name;b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
    if p.exists():
        assert p.read_bytes()==b,'Output differs; do not overwrite: '+name
    else:
        q=p.with_suffix('.tmp');q.write_bytes(b);assert q.stat().st_size==len(b);q.replace(p)

def select(hosts,sn,sbf,groups,exclusions):
    # Independent metadata implementation of configured filters and identifier joins.
    h=[r for r in hosts if not any(fnmatch.fnmatchcase(r[k].lower(),p.lower())
        for k in ('host','method','anchor','source') for p in exclusions)]
    available={r['host'] for r in h};calhosts={r['host'] for r in sn+sbf}
    bygroup=defaultdict(set)
    for g in groups:bygroup[g['group']].add(g['host'])
    admitted={g for g,hs in bygroup.items() if hs & available and hs & calhosts}
    repeats=Counter(r['host'] for r in h)
    gg=[g for g in groups if g['group'] in admitted and repeats[g['host']]<=1]
    extra={g['host'] for g in gg}
    ss=[s for s in sn if s['host'] in available|extra]
    bb=[s for s in sbf if s['host'] in available|extra]
    used={r['host'] for r in ss+bb}|extra
    hh=[r for r in h if r['host'] in used|ANCHORS]
    refs=[r for r in hh if r['host'] in ANCHORS]
    hh=[r for r in hh if r['host'] not in ANCHORS]
    return dict(hosts=hh,reference_rows=refs,sn_calibrators=ss,sbf_calibrators=bb,groups=gg,
        exclusions=exclusions,counts={'host_equations':len(hh),'reference_rows':len(refs),
            'sn_calibrator_equations':len(ss),'sbf_calibrator_equations':len(bb),
            'group_equations':len(gg),'unique_hosts':len({r['host'] for r in hh})})

def main():
    manifests=[json.loads((PARENT/'UPSTREAM_MANIFEST.json').read_text()),json.loads((ROOT/'SOURCES.json').read_text())]
    checked=[]
    for m in manifests:
        for item in m['files']:
            p=Path(item['path']) if Path(item['path']).is_absolute() else PARENT/'upstream'/item['path']
            assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256']
            checked.append(str(p))
    cols={'host':0,'method':3,'anchor':4,'source':5}
    hosts=records('data/host_data.dat',cols)
    alt=records('data/host_data_nomet.dat',cols)
    sn=records('data/sn1a_calib.dat',{'host':1,'sn':2})
    sbf=records('data/sbf_calib.dat',{'host':0})
    groups=records('data/groups.dat',{'group':0,'host':1})
    hf=records('data/sn1a_hf_pp.dat',{'sn':0})
    v00=select(hosts,sn,sbf,groups,['*jagb*','*mira*','b25','SMC'])
    v01=select(hosts,sn,sbf,groups,['*mira*','SMC','b25'])
    jagb=[r for r in v01['hosts'] if r['method'].startswith('jagb')]
    jhosts=sorted({r['host'] for r in jagb})
    overlaps=[]
    for host in jhosts:
        family=[r for r in v01['hosts'] if r['host']==host]
        overlaps.append({'host':host,'jagb_rows':[r for r in family if r['method'].startswith('jagb')],
            'cepheid_rows':[r for r in family if r['method'].startswith('ceph')],
            'trgb_rows':[r for r in family if r['method'].startswith('trgb')],
            'sn_calibrators':[r for r in v01['sn_calibrators'] if r['host']==host],
            'sbf_calibrators':[r for r in v01['sbf_calibrators'] if r['host']==host],
            'group_rows':[r for r in v01['groups'] if r['host']==host]})
    jagb_ids={(r['host'],r['method'],r['anchor'],r['source']) for r in hosts if r['method'].startswith('jagb')}
    alt_ids={(r['host'],r['method'],r['anchor'],r['source']) for r in alt if r['method'].startswith('jagb')}
    host_ids={r['row_id'] for r in v01['hosts']}
    # Response labels define an additive bias in measured Cepheid distance moduli.
    response={'units':'mag','definition':'E[y_host]=mu_host+c_C*delta_C',
       'sign':'positive delta_C means published Cepheid mu biased high',
       'rows':[{'row_id':r['row_id'],'host':r['host'],'method':r['method'],
                'c_C':int(r['method'].startswith('ceph'))} for r in v01['hosts']],
       'all_non_host_equations':'c_C=0 before propagation through the common parameter fit',
       'runtime_condition':'requires full C support and design-rank validation; no covariance inferred here'}
    sn_jagb={r['sn'] for o in overlaps for r in o['sn_calibrators']}
    output={'scope':'IDENTIFIER_ONLY_V01_CANDIDATE_NOT_RATIFIED_NO_FIT',
       'upstream_commit':manifests[0]['commit'],'verified_source_files':len(checked),
       'v00':v00,'v01':v01,'jagb_overlap':overlaps,
       'jagb_reference_rows':[r for r in v01['reference_rows'] if r['method'].startswith('jagb')],
       'jagb_summary':{'host_rows':len(jagb),'unique_hosts':len(jhosts),
         'rows_by_source':dict(Counter(r['source'] for r in jagb)),
         'all_hosts_also_cepheid':all(o['cepheid_rows'] for o in overlaps),
         'all_hosts_also_trgb':all(o['trgb_rows'] for o in overlaps),
         'shared_sn_identifiers':sorted(sn_jagb),
         'jagb_identity_keys_same_in_nomet':jagb_ids==alt_ids,
         'new_host_rows_vs_v00':sorted(host_ids-{r['row_id'] for r in v00['hosts']}),
         'same_sn_rows_v00_v01':v00['sn_calibrators']==v01['sn_calibrators'],
         'same_sbf_rows_v00_v01':v00['sbf_calibrators']==v01['sbf_calibrators'],
         'same_group_rows_v00_v01':v00['groups']==v01['groups']},
       'sn_flow_identifiers':{'row_count':len(hf),'distinct_names':len({r['sn'] for r in hf}),
         'overlap_with_all_calibrator_names':sorted({r['sn'] for r in sn}&{r['sn'] for r in hf}),
         'limitation':'name inequality does not establish independent systematic calibration'},
       'covariance_map':[
        {'type':'measurement_covariance','key':'same anchor','formula':'sigma_anchor^2',
         'jagb_anchor':'N4258','code':'equations.py:352-359','status':'IMPLEMENTED'},
        {'type':'measurement_covariance','key':'same method+anchor+source (MAS)','formula':'sigma_MAS^2',
         'code':'equations.py:360-366','status':'IMPLEMENTED_WITHIN_GROUP'},
        {'type':'measurement_covariance','key':'same host+method+source (HMS)','formula':'sigma_HMS^2 off diagonal',
         'code':'equations.py:368-376','status':'IMPLEMENTED_WITHIN_GROUP'},
        {'type':'shared_model_parameter','key':'same host mu','code':'equations.py:334-344 and 399-413',
         'status':'SAME_PARAMETER_NOT_AN_EXTRA_DATUM'},
        {'type':'shared_measurement','key':'same SN and same flow intercept','code':'equations.py:399-413 and 519-527',
         'status':'ONE_EQUATION_PER_SUPPLIED_ROW_NOT_ONE_PER_STELLAR_METHOD'},
        {'type':'unprovided_cross_covariance','key':'residual stellar cross-method / cross-source / shared-instrument terms beyond the above',
         'status':'NOT_QUANTIFIED_BY_THIS_RELEASE_CODE_REVIEW_NOT_PROVEN_ZERO'}],
       'upstream_executed':False,'centres_parsed_as_numbers':False,'new_verdict':None}
    write_new('SELECTION_V01_IDENTIFIERS.json',output)
    write_new('CEPHEID_RESPONSE_CANDIDATE.json',response)
    print(json.dumps({'v00':v00['counts'],'v01':v01['counts'],'jagb':output['jagb_summary'],
          'sn_flow':output['sn_flow_identifiers']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
