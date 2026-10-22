"""Document V01 design from pinned identifiers only. No y, C, fit, or upstream import."""
from pathlib import Path
from collections import defaultdict,Counter
from fractions import Fraction
from hashlib import sha256
import json,re
ROOT=Path(__file__).resolve().parent
P=ROOT.parent
J=P/'jagb_extension'
ORD=P.parent

def digest(p):return sha256(p.read_bytes()).hexdigest()
def put(name,obj):
    b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode();p=ROOT/name
    if p.exists():
        assert p.read_bytes()==b,'Changed artifact: '+str(p)
        return
    q=p.with_suffix(p.suffix+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.stat().st_size==len(b);q.replace(p)

def main():
    custody=[]
    for man,base in [(P/'UPSTREAM_MANIFEST.json',P/'upstream'),(J/'SOURCES.json',J/'upstream'),(J/'MANIFESTO_ENTREGA.json',J)]:
        for f in json.loads(man.read_text(encoding='utf-8'))['files']:
            p=Path(f['path']);p=p if p.is_absolute() else base/p
            assert digest(p)==f['sha256'],str(p)
            custody.append(str(p))
    f9=json.loads((ORD/'F9_ASSEMBLY_MANIFEST.json').read_text(encoding='utf-8'))
    f9_source_checks=[]
    for item in [f9['note']]+f9['sources']:
        actual=digest(Path(item['path']))
        matches=actual==item['sha256']
        f9_source_checks.append({'path':item['path'],'expected_sha256':item['sha256'],'actual_sha256':actual,'matches':matches})
        if item is f9['note']: assert matches, 'Active assembly note changed; review it first'
        if matches: custody.append(item['path'])
    # Ancillary F9 input may be concurrently updated by its owner. Do not repin it.
    # Only the verified assembly note is consumed; actual V1 contents are NOT read.
    metadata=json.loads((J/'SELECTION_V01_IDENTIFIERS.json').read_text(encoding='utf-8'))
    m=metadata['v01']
    hosts=sorted({r['host'] for k in ['hosts','groups','sn_calibrators','sbf_calibrators'] for r in m[k]})
    direct={r['host'] for r in m['hosts']}
    groups=list(dict.fromkeys(r['group'] for r in m['groups']))
    eta=[{'key':'mu_host:'+h,'unit':'mag'} for h in hosts]+[{'key':'mu_group:'+g,'unit':'mag'} for g in groups]+[{'key':'M_B','unit':'mag'},{'key':'M110_offset','unit':'mag'}]
    idx={p['key']:i for i,p in enumerate(eta)}
    rows=[]
    def add(row_id,family,coeffs,ah='0',cc='0',ref=None):
        assert set(coeffs)<=set(idx)
        rows.append({'row_id':row_id,'family':family,'X':coeffs,'a_h':ah,'c_C':cc,'source':ref or row_id})
    for r in m['hosts']:
        add(r['row_id'],'host',{'mu_host:'+r['host']:'1'},cc='1' if r['method'].startswith('ceph') else '0')
    for r in m['groups']:
        add(r['row_id'],'group',{'mu_host:'+r['host']:'1','mu_group:'+r['group']:'-1'})
    for r in m['sn_calibrators']:
        add(r['row_id'],'SN_calibrator',{'mu_host:'+r['host']:'1','M_B':'1'})
    for r in m['sbf_calibrators']:
        add(r['row_id'],'SBF_calibrator',{'mu_host:'+r['host']:'1','M110_offset':'1'})
    add('derived:SN_HF_intercept','SN_HF',{'M_B':'-1/5'},ah='1',ref='equations.py:519-527; intercept.py')
    add('derived:SBF_HF_intercept','SBF_HF',{'M110_offset':'-1/5'},ah='1',ref='equations.py:619-627; intercept.py')
    # Only the object identifier is selected. Every numeric source token is ignored.
    mm=[]
    for line_no,line in enumerate((J/'upstream/data/megamaser.dat').read_text(encoding='utf-8').splitlines(),1):
        clean=line.split('#',1)[0].strip()
        if not clean:continue
        name=clean.split(maxsplit=1)[0]
        if name.lower() in ('name','host'):continue
        rr={'row_id':'data/megamaser.dat:L'+str(line_no),'name':name};mm.append(rr)
        add(rr['row_id'],'megamaser',{},ah='1',ref='equations.py:630-643; '+rr['row_id'])
    # Graph proof certificates, no covariance matrix or eigenvalues.
    edges=[];families=defaultdict(list);hms_keys=set();mas_keys=set()
    for r in m['hosts']:
        hms='&'.join(r[k] for k in ('host','method','source'))
        mas='&'.join(r[k] for k in ('method','anchor','source'))
        edges.append({'row_id':r['row_id'],'HMS':hms,'MAS':mas,'anchor':r['anchor']})
        hms_keys.add(hms);mas_keys.add(mas);families[(r['method'],r['source'])].append(r)
    cycles=[];components=[]
    for (method,source),rr in families.items():
        hs=sorted({r['host'] for r in rr});aa=sorted({r['anchor'] for r in rr})
        lookup={(r['host'],r['anchor']):r['row_id'] for r in rr}
        assert len(lookup)==len(rr)
        assert set(lookup)==set((h,a) for h in hs for a in aa), 'Not a complete component; derive general cycle basis'
        components.append({'method':method,'source':source,'HMS_vertices':len(hs),'MAS_vertices':len(aa),'edges':len(rr),
            'incidence_rank':len(hs)+len(aa)-1,'cycle_dimension':(len(hs)-1)*(len(aa)-1)})
        if len(aa)==1:continue
        h0,a0=hs[0],aa[0]
        for h in hs[1:]:
            for a in aa[1:]:
                cycles.append({'id':'cycle:'+method+':'+source+':'+h+':'+a,
                    'coefficients':{lookup[(h,a)]:1,lookup[(h,a0)]:-1,lookup[(h0,a)]:-1,lookup[(h0,a0)]:1}})
    rowmap={r['row_id']:r for r in rows};emap={r['row_id']:r for r in edges}
    for c in cycles:
        for keyname in ('HMS','MAS','anchor'):
            totals=defaultdict(int)
            for rid,w in c['coefficients'].items():totals[emap[rid][keyname]]+=w
            assert all(v==0 for v in totals.values())
        totals=defaultdict(Fraction);ha=Fraction(0);ca=Fraction(0)
        for rid,w in c['coefficients'].items():
            rr=rowmap[rid];ha+=w*Fraction(rr['a_h']);ca+=w*Fraction(rr['c_C'])
            for k,v in rr['X'].items():totals[k]+=w*Fraction(v)
        assert all(v==0 for v in totals.values()) and ha==ca==0
    # Rank of X: every group connects to a directly measured host; all extra hosts attach to such a group.
    groupmembers={g:{r['host'] for r in m['groups'] if r['group']==g} for g in groups}
    assert all(v&direct for v in groupmembers.values())
    assert set(hosts)-direct <= set().union(*groupmembers.values())
    mixed=next(h for h in sorted(direct) if any(r['host']==h and r['method'].startswith('ceph') for r in m['hosts']) and any(r['host']==h and not r['method'].startswith('ceph') for r in m['hosts']))
    mixed_pair=[next(r['row_id'] for r in m['hosts'] if r['host']==mixed and test(r)) for test in [lambda r:r['method'].startswith('ceph'),lambda r:not r['method'].startswith('ceph')]]
    rank_z=sum(c['incidence_rank'] for c in components)
    assert len(cycles)==len(m['hosts'])-rank_z
    counts={'rows':len(rows),'row_families':dict(Counter(r['family'] for r in rows)), 'direct_hosts':len(direct),'all_host_parameters':len(hosts),'group_parameters':len(groups),'eta_dimension':len(eta),'upstream_parameter_dimension':len(eta)+1,'a_h_nonzero_rows':sum(r['a_h']!='0' for r in rows),'c_C_nonzero_rows':sum(r['c_C']!='0' for r in rows),'active_HMS':len(hms_keys),'active_MAS':len(mas_keys),'reference_rows_in_selection':len(m['reference_rows']),'incidence_components':len(components),'host_incidence_rank':rank_z,'host_cycle_constraints':len(cycles)}
    spec={'status':'DOCUMENTARY_SYMBOLIC_DESIGN_NO_Y_NO_C_NO_FIT','unit_id':json.loads((ROOT/'UNIDADE.json').read_text())['unit_id'],
      'notation':'y = X eta + a_h h + c_C delta_C + epsilon; upstream coefficient matrix A=[X,a_h]',
      'eta_columns':eta,'h':{'definition':'log10(H0/(km/s/Mpc))','upstream_column_index_zero_based':len(eta),'unit':'dex'},
      'row_order':'upstream loop order; stable source row IDs identify all raw rows; intercept rows are named derived rows',
      'rows':rows,'mas_hms_graph':edges,'components':components,'deterministic_cycles':cycles,
      'counts':counts,'rank_certificate':{'X_full_column_rank':True,'proof':'host rows fix direct mu; group links fix group and extra mu; SN and SBF calibrators fix two magnitudes',
         'X_a_h_full_column_rank':True,'proof_a_h':'nonzero h coefficient in five maser rows while X is zero there',
         'c_C_not_in_span_X_a_h':True,'proof_c_C':'two host rows of same host have identical X and zero a_h but different c_C',
         'mixed_host_witness':mixed_pair},
      'support_certificate':{'host_X_and_c_C_in_HMS_incidence_range':True,'host_a_h_zero':True,'all_cycle_constraints_annihilate_X_a_h_c_C':True,'actual_y_cycle_constraints_checked':False,'positive_MAS_and_HMS_variances_and_baseline_construction_required':True,'nonhost_covariance_support_requires_existing_guard':True},
      'values':{'observed_centres':None,'observed_covariance':None,'S':None,'g':None,'H0':None,'lnB':None},
      'forbidden_operations_performed':False,'upstream_executed':False,'remote_model_calls':0}
    put('ESPECIFICACAO_LINEAR.json',spec)
    inputs=[P/'UPSTREAM_MANIFEST.json',J/'SOURCES.json',J/'MANIFESTO_ENTREGA.json',J/'SELECTION_V01_IDENTIFIERS.json',ORD/'F9_ASSEMBLY_MANIFEST.json',ORD/'F9_LIKELIHOOD_ASSEMBLY_CANDIDATE.md']
    put('INPUTS_PINADOS.json',{'inputs':[{'path':str(p),'sha256':digest(p),'bytes':p.stat().st_size} for p in inputs],'inherited_paths_verified':len(custody),'inherited_unique_paths':len(set(custody)),'f9_dependency_checks':f9_source_checks,'F9_V1_contents_read':False,'initial_run_failed_on_stale_ancillary_F9_pin':True})
    print(json.dumps({'counts':counts,'components':components,'mixed_host_witness':mixed_pair,'extra_hosts':sorted(set(hosts)-direct)},indent=2))

if __name__=='__main__':main()