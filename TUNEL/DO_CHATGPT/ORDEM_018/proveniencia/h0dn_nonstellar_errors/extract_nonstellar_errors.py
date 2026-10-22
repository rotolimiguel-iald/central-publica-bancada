"""Extract only nonstellar identifiers, uncertainties and selected velocities/redshifts."""
import ast, configparser, hashlib, json, math, re, sys
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from audit_provenance import atomic, metadata
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
P=ROOT/'h0dn_documentary_review'
J=P/'jagb_extension'
U=P/'upstream'
JU=J/'upstream'
CODE=U/'h0_constrainer/h0_constrainer'
sources={}
checks=[]
def load(path):
    m,r=metadata(path);sources[str(path)]=m
    return r
def obj(path):return json.loads(load(path).decode('utf-8-sig'))
def check(name,ok):
    checks.append({'name':name,'passed':bool(ok)})
    assert ok,name
entries={}
for man,base in [(P/'UPSTREAM_MANIFEST.json',U),(J/'SOURCES.json',JU),(J/'MANIFESTO_ENTREGA.json',J)]:
    d=obj(man)
    for entry in d['files']:
        path=Path(entry['path'])
        if not path.is_absolute():path=base/path
        entries[str(path)]=entry
def pinned(path):
    raw=load(path)
    e=entries[str(path)]
    check('pin:'+str(path),hashlib.sha256(raw).hexdigest()==e['sha256'] and ('bytes' not in e or len(raw)==e['bytes']))
    if 'git_blob_sha1' in e:check('git_blob:'+str(path),hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==e['git_blob_sha1'])
    return raw
for name in ['equations.py','intercept.py','data_loader.py','main.py','config_reader.py']:
    pinned(CODE/name)
basepath=U/'h0_constrainer/configs/base_variants_config.ini'
varpath=U/'h0_constrainer/configs/variants.ini'
cp=configparser.ConfigParser();cp.read_string(pinned(basepath).decode('utf-8-sig'))
vp=configparser.ConfigParser();vp.read_string(pinned(varpath).decode('utf-8-sig'))
effective=dict(cp['DEFAULT']);effective.update(vp['V01 - Baseline + JAGB'])
allowed={'sn1a_calib','sn1a_hf','sn1a_hf_cov','sn1a_vp','sn1a_ignore_offdiag','sn1a_IR','sn1a_intrinsic','sbf_calib','sbf_hf','sbf_hf_cov','sbf_v','mm','mm_dz','vcorr_mm','groups','q0','j0','vpec_error','sbf_vpec_error','z_range_sn1a','z_range_sbf','zmin_hf','zmax_hf','calib_exclude','calib_include','unused_hosts_via_covariance'}
default_refs={}
tree=ast.parse((CODE/'main.py').read_text(encoding='utf-8'))
for n in ast.walk(tree):
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='get_config_value' and len(n.args)>=4:
        key=ast.literal_eval(n.args[2])
        if key in allowed:
            default=ast.unparse(n.args[3]) if isinstance(n.args[3],ast.Name) else ast.literal_eval(n.args[3])
            default_refs[key]={'value':default,'line':n.lineno}
config={}
for key in sorted(allowed):
    if key in effective:config[key]={'value':effective[key],'source':'base_variants_config.ini + V01 override'}
    elif key in default_refs:config[key]={'value':default_refs[key]['value'],'source':'main.py default','line':default_refs[key]['line']}
config['sbf_vpec_error']['effective_value']=effective.get('sbf_vpec_error',effective['vpec_error'])
selection=json.loads(pinned(J/'SELECTION_V01_IDENTIFIERS.json'))
struct=obj(P/'STRUCTURE_AUDIT.json')
vdisp=Decimal(effective['vpec_error'])
sbf_vdisp=Decimal(config['sbf_vpec_error']['effective_value'])
intrinsic=Decimal(str(config['sn1a_intrinsic']['value']))
check('V01_defaults_and_flags',intrinsic==0 and config['sn1a_ignore_offdiag']['value'] is False and config['sn1a_IR']['value'] is False and config['mm_dz']['value'] is True)
check('no_flow_cuts',config['z_range_sn1a']['value'] is False and config['z_range_sbf']['value'] is False)
def selected_fields(path,ncols,fields):
    raw=pinned(path)
    # Noncapturing tokens skip every unapproved central column.
    names={i:name for name,i in fields.items()}
    pattern=re.compile(rb'^\s*'+rb'\s+'.join((rb'(?P<'+names[i].encode()+rb'>\S+)' if i in names else rb'\S+') for i in range(ncols))+rb'\s*$')
    out=[]
    for no,line in enumerate(raw.splitlines(),1):
        stripped=re.split(rb'[#;]',line,maxsplit=1)[0].strip()
        if not stripped:continue
        match=pattern.match(stripped)
        assert match,'Column-count mismatch:'+path.name+':'+str(no)
        record={k:v.decode('utf-8') for k,v in match.groupdict().items()}
        record.update(line=no,row_id='data/'+path.name+':L'+str(no))
        out.append(record)
    return out
def numeric(record,key,nonnegative=False):
    v=Decimal(record[key])
    assert v.is_finite() and (not nonnegative or v>=0)
    return v
sn_all=selected_fields(JU/'data/sn1a_calib.dat',5,{'ordinal':0,'host':1,'sn':2,'sigma_mag':4})
sn_byline={x['line']:x for x in sn_all}
sn=[]
for r in selection['v01']['sn_calibrators']:
    x=sn_byline[r['line']]
    check('SN_identity:'+r['row_id'],x['host']==r['host'] and x['sn']==r['sn'])
    sig=numeric(x,'sigma_mag',True)
    sn.append({**x,'variance_mag2_upstream':str(sig*sig+intrinsic*intrinsic)})
sbf_all=selected_fields(JU/'data/sbf_calib.dat',5,{'host':0,'sigma_M110_mag':2,'sigma_m110_mag':4})
sbf_byline={x['line']:x for x in sbf_all}
sbf=[]
for r in selection['v01']['sbf_calibrators']:
    x=sbf_byline[r['line']]
    check('SBF_identity:'+r['row_id'],x['host']==r['host'])
    sm=numeric(x,'sigma_m110_mag',True);sM=numeric(x,'sigma_M110_mag',True)
    sbf.append({**x,'variance_mag2_upstream':str(sm*sm+sM*sM)})
grp_all=selected_fields(U/'data/groups.dat',3,{'group':0,'host':1,'sigma_depth_mag':2})
grp_byline={x['line']:x for x in grp_all}
groups=[]
for r in selection['v01']['groups']:
    x=grp_byline[r['line']]
    check('group_identity:'+r['row_id'],x['host']==r['host'] and x['group']==r['group'])
    sigma=numeric(x,'sigma_depth_mag',True)
    groups.append({**x,'variance_mag2_upstream':str(sigma*sigma)})
sn_hf=selected_fields(JU/'data/sn1a_hf_pp.dat',9,{'sn':0,'sigma_mb_mag_not_used_with_cov':2,'zcmb':4,'vpec_2mpp_km_s':8})
for x in sn_hf:
    numeric(x,'sigma_mb_mag_not_used_with_cov',True);numeric(x,'zcmb')
    numeric(x,'vpec_2mpp_km_s')
sbf_hf=selected_fields(JU/'data/sbf_hf.dat',7,{'host':0,'sigma_M110_mag_unused_upstream':2,'sigma_m110_mag':4,'v2mpp_km_s':6})
for x in sbf_hf:
    numeric(x,'sigma_M110_mag_unused_upstream',True);numeric(x,'sigma_m110_mag',True)
    assert numeric(x,'v2mpp_km_s')>0
mm=selected_fields(JU/'data/megamaser.dat',14,{'name':0,'distance_minus_Mpc':2,'distance_plus_Mpc':3,'sigma_v_km_s':5,'v_corr_2mpp_km_s':7})
for x in mm:
    sd=(abs(numeric(x,'distance_minus_Mpc'))+abs(numeric(x,'distance_plus_Mpc')))/2
    sv=numeric(x,'sigma_v_km_s',True);v=numeric(x,'v_corr_2mpp_km_s')
    assert v>0
    x.update(sigma_distance_Mpc_upstream=str(sd),distance_centre_converted=False,variance_logH2=None,
             required_unconverted_field='distance, zero-based column 1; needed only for sigma_D/D in later authorized propagation')
cov_path=U/'data/sn1a_covar_pp.dat'
cov_raw=pinned(cov_path)
# Shape header only. Existing covariance diagnostic receipt is reused, not rerun.
cov_header=Decimal(cov_raw.splitlines()[0].decode('ascii'))
assert cov_header.is_finite() and cov_header>0 and cov_header==cov_header.to_integral_value()
cov_dimension=int(cov_header)
check('SN_covariance_row_alignment',cov_dimension==len(sn_hf)==struct['supplied_sn_covariance']['dimension'])
check('requested_block_counts',(len(sn),len(sbf),len(groups),len(mm))==(55,14,13,5))
overlap={'SN_calibrator_vs_flow_names':sorted({r['sn'] for r in sn}&{r['sn'] for r in sn_hf}),
         'SBF_calibrator_vs_flow_exact_identifiers':sorted({r['host'] for r in sbf}&{r['host'] for r in sbf_hf}),
         'SN_flow_rows':len(sn_hf),'SN_flow_distinct_names':len({r['sn'] for r in sn_hf}),
         'SBF_flow_rows':len(sbf_hf),'SBF_flow_distinct_names':len({r['host'] for r in sbf_hf}),
         'limitation':'Exact name overlap only; no coordinates or new cross-catalog identity resolution. Nonoverlap does not prove systematic independence.'}
output={'at':datetime.now(timezone.utc).isoformat(),'status':'ERROR_METADATA_CANDIDATE_NOT_GLOBAL_C_OR_V1',
'upstream_commit':selection['upstream_commit'],'selection_pin':sources[str(J/'SELECTION_V01_IDENTIFIERS.json')],
'config':config,'counts':{'stellar_context_only':178,'SN_calibrators':len(sn),'SBF_calibrators':len(sbf),'group_equations':len(groups),'intercepts':2,'megamasers':len(mm),'nonstellar_equations':len(sn)+len(sbf)+len(groups)+len(mm)+2},
'SN_calibrators':sn,'SBF_calibrators':sbf,'group_equations':groups,'SN_flow_error_inputs':sn_hf,'SBF_flow_error_inputs':sbf_hf,'megamaser_error_inputs':mm,
'flow_covariance':{'source':sources[str(cov_path)],'order':'One file row per flow record in original order, including repeated SN names; never collapse by name without covariance transformation.',
'units':'mag^2','dimension_header':cov_dimension,'existing_diagnostic_receipt':sources[str(P/'STRUCTURE_AUDIT.json')],
'previous_diagnostics_not_repeated':struct['supplied_sn_covariance'],'central_values_not_present_in_this_file':True,
'original_survey_covariance_conventions':'Upstream-supplied public matrix; detailed decomposition/velocity inclusion not re-audited here.'},
'identity_overlap':overlap,'guards':{'upstream_executed':False,'centres_converted':False,'intercept_centres_calculated':False,'intercept_uncertainties_calculated':False,'total_C_constructed':False,'stellar_C_constructed':False,'S_g_H0_evidence_fit':False},
'checks':checks,'sources':list(sources.values())}
atomic(OUT/'METADADOS_ERROS_NAO_ESTELARES_V01.json',json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'counts':output['counts'],'identity_overlap':overlap,'all_checks_passed':all(x['passed'] for x in checks),'sources_pinned':len(sources),'receipt':metadata(OUT/'METADADOS_ERROS_NAO_ESTELARES_V01.json')[0]},ensure_ascii=False))
