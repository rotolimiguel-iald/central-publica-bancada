"""Create v3_2 beside v3_1 to address independent C7 findings."""
from pathlib import Path
import ast
B=Path(__file__).resolve().parents[1];R=B/'refeito'
def change(s,a,b):
    if s.count(a)!=1:raise ValueError('Anchor count '+a[:70])
    return s.replace(a,b)
def save(name,s):
    ast.parse(s)
    with (R/name).open('xb') as f:f.write(s.encode())
s=(R/'reproduce_c6_v3.py').read_text(encoding='utf-8')
s=change(s,'import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile','import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile,math')
s=change(s,'def main():','''def invalid_constant(value):raise ValueError('Nonfinite JSON token: '+value)
def load_json(path):return json.loads(path.read_bytes(),parse_constant=invalid_constant)
def compare_results(reference,actual):
    def indexed(doc):
        rows=doc['results']
        if not isinstance(rows,list) or not rows:raise ValueError('Empty/invalid result table')
        result={}
        for row in rows:
            for field in ('start_tM','amplitude_prior_sd_strain','lnB_vs_GR'):
                value=row[field]
                if type(value) not in (int,float) or not math.isfinite(value):raise ValueError('Nonfinite/nonnumeric '+field)
            if not isinstance(row['reading'],str) or not row['reading']:raise ValueError('Invalid reading key')
            key=(row['start_tM'],row['reading'],row['amplitude_prior_sd_strain'])
            if key in result:raise ValueError('Duplicate row')
            result[key]=row
        return result
    wanted=indexed(reference);found=indexed(actual)
    if wanted.keys()!=found.keys():raise ValueError('Result coverage differs')
    error=max(abs(found[k]['lnB_vs_GR']-wanted[k]['lnB_vs_GR']) for k in wanted)
    if not math.isfinite(error) or error>1e-5:raise ValueError('Numeric reproduction differs')
    return len(found),error
def main():''')
for path in ["ROOT/'MANIFEST.json'","run/'C6_DOWNLOADS.json'","ROOT/'evidence/C6_RESULTS.json'","run/'C6_RESULTS.json'"]:
    s=s.replace('json.loads(('+path+').read_bytes())','load_json('+path+')')
start=s.index('        key=lambda r:');end=s.index("        if not permit_status",start)
s=s[:start]+"        count,error=compare_results(reference,actual)\n        if actual['registration_sha256']!=reference['registration_sha256']:raise ValueError('Registration differs')\n"+s[end:]
s=s.replace('rows=len(found)','rows=count')
s=change(s,"    if not parent.is_relative_to(workroot) or parent==workroot:raise ValueError('Unsafe temporary path')\n    os.chmod(parent,0o755);run=parent/'ORDEM_013_RINGDOWN';logs={};report=dict(status='REPRODUCTION_INTERRUPTED')\n    try:","    run=parent/'ORDEM_013_RINGDOWN';logs={};report=dict(status='REPRODUCTION_INTERRUPTED')\n    try:\n        if not parent.is_relative_to(workroot) or parent==workroot:raise ValueError('Unsafe temporary path')\n        os.chmod(parent,0o755)")
save('reproduce_c6_v3_2.py',s)
s=(R/'package_unit_checks_v3.py').read_text(encoding='utf-8')
s=change(s,'    times=np.arange(128)/4096', '''    from reproduce_c6 import compare_results,permit_status,invalid_constant
    import copy
    reference={'results':[dict(start_tM=i+1,reading='R-B',amplitude_prior_sd_strain=1e-20,lnB_vs_GR=.01*i) for i in range(3)]}
    require(compare_results(reference,copy.deepcopy(reference))==(3,0.0),'Ordinary comparison')
    probes=0
    for i in range(3):
        for key in ('start_tM','amplitude_prior_sd_strain','lnB_vs_GR'):
            for value in (float('nan'),float('inf'),float('-inf'),True,'0'):
                bad=copy.deepcopy(reference);bad['results'][i][key]=value
                refuses(lambda:compare_results(reference,bad));probes+=1
    for token in ('NaN','Infinity','-Infinity'):refuses(lambda:json.loads(token,parse_constant=invalid_constant))
    require(permit_status('NOT_VERIFIED') and permit_status('INCONCLUSIVE_SYSTEMATICS'),'Downgrade rejected')
    require(not permit_status('CONFIRMED'),'Promotion accepted')
    q=json.loads((ROOT/'tables/reference_QNM.json').read_bytes())
    mod=prediction(68.1,.68,'R-MOD',qnm_dimensionless=complex(q['omega_real'],q['omega_imag']))
    marker='CONJECTURE \\u2014 management hypothesis, not TGL canon'
    require(marker in mod['scope'],'R-MOD runtime marker corrupted')
    for name in ('README.md','OVERVIEW.md','tables/reading_scope.csv','tables/reading_scope.json'):
        require(marker in (ROOT/name).read_text(encoding='utf-8'),'R-MOD surface marker corrupted')
    times=np.arange(128)/4096''')
s=s.replace('guard_controls=5','guard_controls=5,nonfinite_and_type_controls=probes+3')
save('package_unit_checks_v3_2.py',s)
s=(R/'build_independent_v3_1_013bis.py').read_text(encoding='utf-8')
# The old builder had been decoded with the Windows default before being copied.
s=s.encode('cp1252').decode('utf-8')
s=s.replace('C7_INDEPENDENT_v3_1','C7_INDEPENDENT_v3_2').replace('C7_V3_1_BUILD.json','C7_V3_2_BUILD.json').replace('reproduce_c6_v3.py','reproduce_c6_v3_2.py').replace('package_unit_checks_v3.py','package_unit_checks_v3_2.py')
s=change(s,"for n,raw in sorted(content.items()):put(n,raw)",'''# Ship verifiable documentary licence sources, without relicensing research code.
ledger=B/'cache/MANIFESTO_DOWNLOADS_013BIS_v2.json'
content['provenance/DOWNLOAD_LICENSE_LEDGER.json']=ledger.read_bytes()
for rid in ('17018009','21454847','17461225'):
    content['provenance/zenodo_'+rid+'_record.json']=(B/('cache/public/'+rid+'/record.json')).read_bytes()
content['provenance/GWOSC_acknowledgement.html']=(B/'cache/literature/gwosc_acknowledgement_013bis.html').read_bytes()
licence_rows=[]
for n,raw in content.items():
    isnoise='/cache/empirical_noise/' in n
    licence_rows.append(dict(path=n,sha256=hashlib.sha256(raw).hexdigest(),
      licence_id='cc-by-4.0' if isnoise else None,
      scope='Derived GWOSC off-source noise; upstream policy and original data hashes in frozen empirical-noise receipt' if isnoise else 'Research code, derived reports or archival text: no blanket licence inferred; data-source licences are in documentary ledger',
      provenance='provenance/GWOSC_acknowledgement.html' if isnoise else 'provenance/DOWNLOAD_LICENSE_LEDGER.json'))
content['provenance/SHIPPED_ATTRIBUTIONS.json']=encoded(dict(files=licence_rows,ledger_sha256=sha(ledger),scope='Per-file attribution; licence references are not a legal determination for research code'))
for n in ('README.md','OVERVIEW.md'):
    text=content[n].decode()
    text=text.replace('Original current-evidence JSONs retain the per-event intervals and derivations.', 'Per-event catalogue intervals are retained in evidence/C4_CATALOG_220.json; aggregate diagnostics are in current_evidence/F2_ALL_READING_TABLES_v2.json.')
    text=text.replace('Each upstream licence is preserved separately;', 'Upstream licence declarations and source records are shipped under provenance/, with SHIPPED_ATTRIBUTIONS.json linking each file hash; full legal licence texts are externally referenced, not all reproduced;')
    text+='\\nPortuguese current-evidence addenda are original source documents, not the English entry-point guidance. English scope and limitations are fully stated in this README and the generated table.\\n'
    content[n]=text.encode()
for n,raw in sorted(content.items()):put(n,raw)''')
save('build_independent_v3_2_013bis.py',s)
s=(R/'validate_package_v3_013bis.py').read_text(encoding='utf-8')
s=s.replace('v3_1','v3_2').replace('V3_1','V3_2')
s=change(s,"    parent=Path(tempfile.mkdtemp(prefix='v3clean_',dir=cache)).resolve()\n    if not parent.is_relative_to(cache) or parent==cache:raise ValueError('Unsafe temporary')\n    out=B/'bis/C7_V3_2_CLEAN_VALIDATION.json'\n    if out.exists():raise FileExistsError(out)","    out=B/'bis/C7_V3_2_CLEAN_VALIDATION.json'\n    if out.exists():raise FileExistsError(out)")
s=change(s,"directory=str(parent))\n    try:","directory=None)\n    parent=Path(tempfile.mkdtemp(prefix='v3clean_',dir=cache)).resolve()\n    try:\n        if not parent.is_relative_to(cache) or parent==cache:raise ValueError('Unsafe temporary')\n        receipt['directory']=str(parent)")
save('validate_package_v3_2_013bis.py',s)
