"""Audit only published uncertainties/keys; never convert centres or assemble C."""
from pathlib import Path
from decimal import Decimal
from collections import defaultdict
from hashlib import sha256
import json, re
ROOT=Path(__file__).resolve().parent
J=ROOT.parent
P=J.parent

def put(name,obj):
    p=ROOT/name
    b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
    if p.exists():
        assert p.read_bytes()==b, name+' changed'
        return
    q=p.with_suffix(p.suffix+'.tmp')
    with q.open('xb') as f: f.write(b)
    assert q.stat().st_size==len(b)
    q.replace(p)

def main():
    inherited=[]
    for path in [P/'UPSTREAM_MANIFEST.json',J/'SOURCES.json',J/'MANIFESTO_ENTREGA.json',ROOT/'PRIMARY_SOURCES.json']:
        inherited.append({'path':str(path),'sha256':sha256(path.read_bytes()).hexdigest()})
    meta=json.loads((J/'SELECTION_V01_IDENTIFIERS.json').read_text(encoding='utf-8'))
    rows=(P/'upstream/data/host_data.dat').read_text(encoding='utf-8').splitlines()
    def attach(r):
        t=re.split('[#;]',rows[r['line']-1],maxsplit=1)[0].split()
        assert [t[0],t[3],t[4],t[5]]==[r[k] for k in ['host','method','anchor','source']]
        # t[1] (observed centre) deliberately never converted or included.
        return {**r,'sigma_mag':str(Decimal(t[2])),
                'mas_key':'&'.join(r[k] for k in ['method','anchor','source']),
                'hms_key':'&'.join(r[k] for k in ['host','method','source'])}
    hosts=[attach(r) for r in meta['v01']['hosts']]
    refs=[attach(r) for r in meta['v01']['reference_rows']]
    refmap=defaultdict(list)
    for r in refs: refmap[r['mas_key']].append(r)
    missing=[r['mas_key'] for r in hosts if r['mas_key'] not in refmap]
    assert not missing, missing
    assert all(len(v)==1 for v in refmap.values())
    groups=defaultdict(list)
    for r in hosts: groups[r['hms_key']].append(r)
    inconsistent=[]
    for key,rr in groups.items():
        vals=[Decimal(r['sigma_mag']) for r in rr]
        if len(set(vals))>1: inconsistent.append({'hms_key':key,'errors':list(map(str,vals))})
    # If any errors differ, don't silently replace upstream allclose/min semantics.
    assert not inconsistent, inconsistent
    nonnegative=True
    for r in hosts:
        h=Decimal(groups[r['hms_key']][0]['sigma_mag'])
        d=Decimal(r['sigma_mag'])**2-h*h
        nonnegative &= d>=0
    arows=[]
    for n,line in enumerate((P/'upstream/data/anchors.dat').read_text().splitlines(),1):
        t=line.split('#')[0].split()
        if not t: continue
        arows.append({'anchor':t[0],'sigma_mag':str(Decimal(t[2])),'row_id':'data/anchors.dat:L'+str(n)})
    anchor={r['anchor']:Decimal(r['sigma_mag']) for r in arows}
    relevant={o['host'] for o in meta['jagb_overlap']}
    relevant_rows=[r for r in hosts if r['host'] in relevant]
    jagb=[r for r in hosts if r['method'].startswith('jagb')]
    jrefs=[r for r in refs if r['method'].startswith('jagb')]
    cc=next(r for r in jagb if r['host']=='N5643' and r['source']=='CCHP')
    ss=next(r for r in jagb if r['host']=='N5643' and r['source']=='SH0ES')
    doc={'status':'ERRORS_AND_IDENTIFIERS_ONLY_NOT_A_FIT',
         'request_id':'54feb986-d927-4ff9-aa69-3c07680ee78b',
         'upstream_commit':meta['upstream_commit'],'inherited_manifests':inherited,
         'source':{'path':str(P/'upstream/data/host_data.dat'),'sha256':sha256((P/'upstream/data/host_data.dat').read_bytes()).hexdigest()},
         'anchor_errors':arows,'mas_reference_errors':refs,'jagb_host_errors':jagb,
         'eleven_host_method_rows':relevant_rows,
         'primitive_hms_groups':[{'key':k,'sigma_mag':v[0]['sigma_mag'],'row_ids':[r['row_id'] for r in v]} for k,v in groups.items()],
         'checks':{'host_rows':len(hosts),'unique_hms':len(groups),'all_hms_errors_exactly_equal_within_group':not inconsistent,
                   'missing_mas':missing,'all_residual_diagonal_variances_nonnegative':bool(nonnegative),
                   'centres_converted':False,'upstream_executed':False,'global_covariance_assembled':False},
         'algebraic_coefficient_examples_mag2':{
             'common_N4258_anchor':str(anchor['N4258']**2),
             'JAGB_cross_MAS_multiplier_rho_M':str(Decimal(jrefs[0]['sigma_mag'])*Decimal(jrefs[1]['sigma_mag'])),
             'N5643_cross_HMS_multiplier_rho_H':str(Decimal(cc['sigma_mag'])*Decimal(ss['sigma_mag'])),
             'warning':'Coefficients only; no correlation coefficient estimated from data.'}}
    put('ERROR_COMPONENTS.json',doc)
    print(json.dumps({'checks':doc['checks'],'mas_N4258':[r for r in refs if r['anchor']=='N4258'],
                     'examples':doc['algebraic_coefficient_examples_mag2']},ensure_ascii=False,indent=2))

if __name__=='__main__': main()