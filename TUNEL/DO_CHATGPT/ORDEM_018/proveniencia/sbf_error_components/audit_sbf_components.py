"""Bounded read-only SBF error documentary audit; no upstream imports or scientific execution."""
from pathlib import Path
import datetime, hashlib, json, sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from audit_provenance import atomic,metadata
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
P=ROOT/'h0dn_documentary_review'
U=P/'upstream'
J=P/'jagb_extension'
def read_record(path,expected=None,ranges=()):
    m,b=metadata(path)
    if expected is not None:
        assert m['sha256']==expected,(str(path),'PIN_MISMATCH')
    lines=b.decode('utf-8-sig').splitlines()
    m['pin_matches_inherited_manifest']=expected is not None
    m['excerpts']=[{'first_line':a,'last_line':z,'text':'\n'.join(lines[a-1:z])} for a,z in ranges]
    return m
um=json.loads((P/'UPSTREAM_MANIFEST.json').read_text(encoding='utf-8'))
jm=json.loads((J/'SOURCES.json').read_text(encoding='utf-8'))
up={x['path']:x['sha256'] for x in um['files']}
jp={x['upstream_path']:x['sha256'] for x in jm['files']}
sources=[
read_record(P/'UPSTREAM_MANIFEST.json'),
read_record(J/'SOURCES.json'),
read_record(U/'idlcode/org_v3p9.pro',up['idlcode/org_v3p9.pro'],[(1782,1811),(1817,1827),(1830,1833),(1843,1872)]),
read_record(U/'h0_constrainer/h0_constrainer/equations.py',up['h0_constrainer/h0_constrainer/equations.py'],[(255,266),(445,458),(594,625)]),
read_record(U/'h0_constrainer/h0_constrainer/data_loader.py',up['h0_constrainer/h0_constrainer/data_loader.py'],[(255,284)]),
read_record(U/'h0_constrainer/h0_constrainer/intercept.py',up['h0_constrainer/h0_constrainer/intercept.py'],[(131,165)]),
read_record(U/'data/README.md',up['data/README.md'],[(9,14),(63,70)]),
read_record(J/'residual_systematics/sources/h0dn.txt',ranges=[(488,490),(1821,1845),(1964,1966)])]
# Only headers of raw SBF tables enter this documentary artifact; all rows remain unconverted/unexposed.
for rel in ['data/sbf_hf.dat','data/sbf_calib.dat']:
    m,b=metadata(J/'upstream'/rel)
    assert m['sha256']==jp[rel]
    m['pin_matches_inherited_manifest']=True
    m['headers']=[x.decode('utf-8') for x in b.splitlines() if x.lstrip().startswith(b'#')]
    m['numeric_fields_parsed']=False
    sources.append(m)
prior=HERE.parent/'h0dn_nonstellar_errors'
for name in ['CONTRATO_ERROS_NAO_ESTELARES_V01.json','METADADOS_ERROS_NAO_ESTELARES_V01.json','NOTA_ERROS_NAO_ESTELARES_V01.md','MANIFESTO_ERROS_NAO_ESTELARES.json']:
    sources.append(read_record(prior/name))
record={
'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
'scope':'DOCUMENTARY_SBF_ERROR_COMPONENTS_ONLY_NO_CENTERS_NO_FIT_NO_UPSTREAM_EXECUTION',
'upstream_commit':um['commit'],'sources':sources,
'inventory_examined':{'upstream_manifest_files':[x['path'] for x in um['files']],
'jagb_extension_manifest_files':[x['upstream_path'] for x in jm['files']],
'claim_limit':'These admitted snapshots contain the loader, consumer and explanatory IDL. No numerical constructor for e(M110) was established in this bounded examination. This is not a claim about all remote repository contents.'},
'findings':[
{'id':'NS01-A','status':'REAL_CODE_AND_DECLARED_INTENT','finding':'IDL 1817-1824 describes color propagation plus intrinsic width; 1849 explicitly excludes absolute distance calibration uncertainty, allocated to m_offset at 1858-1859.'},
{'id':'NS01-B','status':'REAL','finding':'Both IDL1867 and Python603 pass only apparent-magnitude error to SBF HF intercept. Calibrators combine M110_error and m110_error. Free common offset does not represent differential object errors.'},
{'id':'NS01-C','status':'OPEN_NUMERICAL_DECOMPOSITION','finding':'No verified per-row decomposition identifies color, intrinsic width, slope uncertainty and common contributions in supplied e(M110). Cannot quantify predominance or subtract common pieces uniquely.'}],
'components':[
{'component':'absolute calibration / common zero point','intended_treatment':'free M110_offset, constrained jointly by calibrators; avoid readding same external zero-point prior','basis':'IDL1849,1858-1859; Python255-266'},
{'component':'object color measurement / extinction contribution','intended_treatment':'propagated through color slope; not removed by common offset','basis':'IDL1821-1824; Jensen2025 sec3.1'},
{'component':'intrinsic SBF width at fixed color','intended_treatment':'residual per-object term in documented diagonal approximation; actual amplitude in column unverified','basis':'IDL1822-1824,1846-1854'},
{'component':'slope and internal calibration parameter uncertainty','intended_treatment':'potential shared nonconstant low-rank covariance; explicitly neglected as subdominant in upstream comments','basis':'IDL1851-1856'},
{'component':'apparent-magnitude photometry','intended_treatment':'e(m110), already propagated in both source implementations','basis':'IDL1850; Python603'}],
'alternatives':[
{'id':'A','status':'FINITE_EXACT_UPSTREAM_REPRODUCTION_WITH_EXPLICIT_LIMIT','prescription':'Preserve observed code: HF mag_err=e(m110); calib variance=e(m110)^2+e(M110)^2; common free offset. Clearly declare residual e(M110) omitted in HF, not absorbed by offset. This is reproducibility, not proof that the uncertainty is complete.'},
{'id':'B','status':'FINITE_CONDITIONAL_RECONSTRUCTION_NOT_ADOPTED','prescription':'At fixed calibration coefficients, residual var_i=sigma_m_i^2+b^2*sigma_color_i^2+sigma_int_i^2-2*b*Cov(m_i,color_i). Add only separately established shared parameter covariance or explicit nuisance parameters. Avoid same calibration data twice. Supplied eM quadrature may define a declared diagonal sensitivity variant under IDL intent, but is not yet an independently reconstructed decomposition.'}],
'not_done':['No means, magnitudes, distances or H0 centers calculated','No observational C assembled','No intercept, S, g, fit, likelihood or evidence','No upstream imports/execution','No real D or remote model executor','No numerical counterexample needed: algebraic difference/common-mode argument suffices'],
'web_archive_limitation':{
'public_sources_read_via_web':['https://arxiv.org/html/2502.15935v2','https://github.com/jjensen-uvu/sbf_distances_2021'],
'external_bytes_pinned':False,
'network_download_default':'Four urllib reads failed due sandbox network denial; WEB_SOURCES.json preserves errors.',
'escalation':'Auto-review rejected download as outside visible heartbeat authorization and driven by untrusted agent context. No elevated command executed. No retry or alternate download.',
'parent_instruction':'Close using pinned local primary source and already-read public references; archival is unnecessary for this unit.'}}
atomic(HERE/'EVIDENCIA_COMPONENTES_SBF.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
m,_=metadata(HERE/'EVIDENCIA_COMPONENTES_SBF.json')
print(json.dumps({'receipt':m,'local_sources':len(sources),'upstream_pins_verified':sum(x['pin_matches_inherited_manifest'] for x in sources),'numeric_centers_parsed':False},ensure_ascii=False))
