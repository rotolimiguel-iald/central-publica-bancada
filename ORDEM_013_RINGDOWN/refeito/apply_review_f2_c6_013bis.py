"""Create additive builders addressing T1, T2 and C6-R1; preserve prior bytes."""
from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1]
def replace_once(s,a,b):
    if s.count(a)!=1:raise ValueError('Nonunique edit: '+a[:80])
    return s.replace(a,b)
def save(name,s):
    ast.parse(s)
    p=ROOT/'refeito'/name
    with p.open('xb') as f:f.write(s.encode())
s=(ROOT/'refeito/summarize_f2_tables_013bis.py').read_text(encoding='utf-8')
s=replace_once(s,'rows=[]', '''EXPECTED_COMPUTED=set(readings)-{'R-PROP','R-RAIZ-COHERENT'}
PYRING_COMPUTED={'R-B','R-RAIZ-0','R-LIN','R-MOD'}
def require_coverage(event, expected):
    found=[r['reading'] for r in event['rows']]
    if len(found)!=len(set(found)) or set(found)!=expected:
        raise ValueError('Computed reading coverage missing, extra or duplicated')
for event in cat['rows']+old['rows']:require_coverage(event,EXPECTED_COMPUTED)
require_coverage(py,PYRING_COMPUTED)
# Negative guard runs before any writes, independent of Python assertions/-O.
probe=dict(py,rows=[r for r in py['rows'] if r['reading']!='R-MOD'])
try:require_coverage(probe,PYRING_COMPUTED)
except ValueError:pass
else:raise RuntimeError('Missing R-MOD silently accepted')
rows=[]''')
s=replace_once(s,'        analytic=not matches',"        expected=EXPECTED_COMPUTED if name.endswith('pSEOB') else PYRING_COMPUTED\n        analytic=reading in (set(readings)-expected)\n        if bool(matches)==analytic:raise ValueError('Computed/analytic coverage inconsistent')")
s=replace_once(s,"new('bis/F2_ALL_READING_TABLES.json'", "new('bis/F2_ALL_READING_TABLES_v2.json'")
s=replace_once(s,"new('bis/F2_ALL_READING_TABLES.csv'", "new('bis/F2_ALL_READING_TABLES_v2.csv'")
s=replace_once(s,"opening=ROOT.parent/",'''for r in rows:
    r['nonblind']=True
    r['source_conditional_verdict']=r['verdict']
    r['physical_status']='INCONCLUSIVE_SYSTEMATICS__NO_PHYSICAL_CONFIRMATION'
    r['z_scope']='Gaussian diagnostic (observed median-based center minus conditional prediction)/stated sigma; not calibrated significance, and never converted from lnB'
    if r['reading']=='R-GLOBAL':
        r['result_type']='RELATIONAL_IDENTITY_IN_DECLARED_IMPLEMENTATION'
        r['analytic_scope']='Global common phase cancels by construction in the chosen relational observable; not a universal physical conclusion'
    elif r['reading'] in ('R-PROP','R-RAIZ-COHERENT'):
        r['result_type']='CONDITIONAL_NUMERICAL_EQUIVALENCE__PHYSICAL_MAPPING_OPEN'
        r['analytic_scope']='Zero is a declared small-effect scenario only; physical mapping remains OPEN'
    elif r['analytic']:
        r['result_type']='CONDITIONAL_NUMERICAL_EQUIVALENCE__BELOW_RESOLUTION'
        r['analytic_scope']='Planck-scale effect represented as zero at the diagnostic resolution; not an exact waveform identity'
    else:r['result_type']='COMPUTED_CONDITIONAL_DENSITY'
opening=ROOT.parent/''')
s=replace_once(s,"source_sha256=sources,code_sha256", "supersedes='bis/F2_ALL_READING_TABLES.json',supersedes_sha256=sha(ROOT/'bis/F2_ALL_READING_TABLES.json'),source_sha256=sources,code_sha256")
s=replace_once(s,"'verdict','sigma_scope']", "'verdict','sigma_scope','analytic','analytic_scope','scope','nonblind','physical_status','z_scope','source_conditional_verdict','result_type','reason','companion_json','companion_json_sha256']")
s=replace_once(s,'buf=io.StringIO();writer=',"for r in rows:\n    r['companion_json']='F2_ALL_READING_TABLES_v2.json';r['companion_json_sha256']=sha(ROOT/'bis/F2_ALL_READING_TABLES_v2.json')\nbuf=io.StringIO();writer=")
save('summarize_f2_tables_013bis_v2.py',s)
s=(ROOT/'refeito/record_c6pre_013bis.py').read_text(encoding='utf-8')
s=replace_once(s,'p=prediction(mass,spin,reading,qnm_dimensionless=',"p=prediction(mass,spin,reading,redshift=reg['reference_redshift'],profile='CODATA2018_IAU2015',qnm_dimensionless=")
s=replace_once(s,'primary_reference=dict(mass_detector_solar=mass,spin=spin,',"primary_reference=dict(mass_detector_solar=mass,spin=spin,redshift=reg['reference_redshift'],constants_profile='CODATA2018_IAU2015',")
s=replace_once(s,"supersedes='C6_RESULTS.json',supersedes_sha256=sources['C6_RESULTS.json'],", "supersedes='C6_ADENDO_REALIZADO.json',supersedes_sha256=sha(ROOT/'C6_ADENDO_REALIZADO.json'),historical_result_sha256=sources['C6_RESULTS.json'],")
s=s.replace('C6_ADENDO_REALIZADO.json','C6_ADENDO_REALIZADO_v2.json')
s=s.replace("supersedes='C6_ADENDO_REALIZADO_v2.json',supersedes_sha256=sha(ROOT/'C6_ADENDO_REALIZADO_v2.json')", "supersedes='C6_ADENDO_REALIZADO.json',supersedes_sha256=sha(ROOT/'C6_ADENDO_REALIZADO.json')")
s=s.replace('REAPROVEITAMENTO_C6.md','REAPROVEITAMENTO_C6_v2.md').replace('refeito/record_c6pre_013bis.py em','refeito/record_c6pre_013bis_v2.py em')
save('record_c6pre_013bis_v2.py',s)
