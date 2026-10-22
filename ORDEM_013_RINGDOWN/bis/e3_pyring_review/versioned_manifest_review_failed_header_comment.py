"""Read-only documentary closure; never open strain or parse posterior values."""
import ast,hashlib,json,math,re,tarfile,time
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
HERE=Path(__file__).resolve().parent;B=HERE.parents[1];ROOT=B.parent
S=HERE/'snapshot_002';PREP=B/'bis/e3_pyring_preparation'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
checks=[]
def check(name,ok,detail=None):
    if not ok:raise RuntimeError(name)
    checks.append(dict(name=name,passed=True,detail=detail))
def main():
    started=time.perf_counter();output=HERE/'MANIFEST_V2_INDEPENDENT_RECEIPT.json'
    if output.exists():raise FileExistsError(output)
    manifest=json.loads((S/'MANIFEST_v2.json').read_text());old=json.loads((S/'MANIFEST.json').read_text())
    check('v2_current_manifest',sha(S/'MANIFEST_v2.json')==sha(PREP/'MANIFEST_v2.json'))
    check('original_manifest_preserved',sha(S/'MANIFEST.json')==sha(HERE/'snapshot_001/MANIFEST.json')==sha(PREP/'MANIFEST.json'))
    own={p.name:sha(p) for p in PREP.glob('*.py')}
    check('all_current_code_pins',own==manifest['code_sha256'])
    for p in PREP.glob('*.py'):ast.parse(p.read_text())
    for n in ('kerr_model.py','conditioning.py','CONFIG.json','PLAN.md'):
        check('science_input_unchanged_'+n,sha(S/n)==sha(HERE/'snapshot_001'/n)==sha(PREP/n))
    class Substitute(ast.NodeTransformer):
        def visit_Call(self,node):
            if ast.dump(node,include_attributes=False)==ast.dump(ast.parse("sha(HERE/'MANIFEST.json')",mode='eval').body,include_attributes=False):
                return ast.copy_location(ast.parse("auth['manifest_sha256']",mode='eval').body,node)
            return self.generic_visit(node)
    for n in ('runner.py','controller.py'):
        old_tree=Substitute().visit(ast.parse((HERE/'snapshot_001'/n).read_text()))
        check(n+'_only_verified_hash_transport_changed',ast.dump(old_tree,include_attributes=False)==ast.dump(ast.parse((S/n).read_text()),include_attributes=False))
    pin_results={}
    for name,wanted in manifest['source_and_config_pins'].items():
        path=(ROOT/name).resolve()
        if not path.is_relative_to(ROOT.resolve()):raise ValueError('Escaping manifest pin')
        if path.suffix.lower() in ('.h5','.hdf5','.gwf'):raise ValueError('This review must not read strain')
        actual=sha(path);pin_results[name]=dict(expected=wanted,actual=actual)
        check('pin_'+name,actual==wanted)
    delta={n:dict(old=h,new=manifest['source_and_config_pins'].get(n)) for n,h in old['source_and_config_pins'].items() if manifest['source_and_config_pins'].get(n)!=h}
    check('only_external_repin_is_guard',set(delta)=={'ORDEM_013_RINGDOWN/bis/e2_code/registration_guard.py'})
    # Extract only lexical/path validators, no runtime verify or launch.
    tree=ast.parse((S/'custody.py').read_text());names={'contained','selected_manifest','strict_json'}
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    ns=dict(Path=Path,HERE=PREP,re=re,json=json)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(S/'custody.py'),'exec',optimize=1),ns)
    for value in [None,'MANIFEST.json','MANIFEST_v2.json','MANIFEST_v12.json']:
        auth={} if value is None else dict(manifest_filename=value)
        expected=PREP/(value or 'MANIFEST.json')
        check('selector_accept_'+str(value),ns['selected_manifest'](auth)==expected.resolve())
    for value in ['../MANIFEST_v2.json','x/MANIFEST_v2.json','MANIFEST_v0.json','MANIFEST_v02.json','MANIFEST_V2.json','MANIFEST_v-1.json','/tmp/MANIFEST.json','MANIFEST_v2.json\n',2,True,None]:
        try:ns['selected_manifest'](dict(manifest_filename=value))
        except ValueError:check('selector_refuse_'+repr(value),True)
        else:raise RuntimeError('Unsafe selector accepted')
    for payload in ['{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}']:
        try:ns['strict_json'](payload)
        except ValueError:check('strict_JSON_'+payload,True)
        else:raise RuntimeError('Non-strict JSON')
    check('legacy_manifest_refuses_new_sources',old['code_sha256']!=own)
    # Verify primary source identity against cached source distribution, no imports.
    vendor=B/'cache/pyring_oracle/vendor/pyRing'
    with tarfile.open(B/'cache/source_distributions/pyRingGW-2.7.0.tar.gz','r:gz') as tf:
        members=tf.getmembers()
        for name in ('pyRing.py','initialise.py','waveform.pyx','likelihood.pyx','noise.py','data/NR_data/berti_qnm_fits.txt'):
            candidates=[m for m in members if m.name.endswith('/pyRing/'+name)]
            if len(candidates)!=1:raise RuntimeError('Ambiguous source member')
            blob=tf.extractfile(candidates[0]).read()
            check('primary_sdist_'+name,hashlib.sha256(blob).hexdigest()==sha(vendor/name))
    cfg=json.loads((S/'CONFIG.json').read_text());extraction=json.loads((S/'PSD_EXTRACTION.json').read_text());psd=[]
    for det,spec in cfg['public_psd'].items():
        path=ROOT/spec['relative_to_Chatgpt'];h=sha(path)
        row=next(x for x in extraction['files'] if x['relative_to_Chatgpt']==spec['relative_to_Chatgpt'])
        check('PSD_crosshash_'+det,h==spec['sha256']==row['sha256'] and path.stat().st_size==row['bytes'])
        # Public PSD schema/extrapolation check only; do not compute ACF, likelihood or posterior.
        table=np.loadtxt(path);f,p=table.T
        check('PSD_schema_'+det,table.shape==(16384,2) and np.isfinite(table).all() and np.all(np.diff(f)>0) and np.all(p>0))
        mask=(f>20)&(f<2038);ff,pp=f[mask],p[mask]
        left=pp[0]+(0-ff[0])*(pp[1]-pp[0])/(ff[1]-ff[0])
        right=pp[-1]+(2048-ff[-1])*(pp[-1]-pp[-2])/(ff[-1]-ff[-2])
        psd.append(dict(detector=det,sha256=h,rows=len(f),extrapolated_zero_Hz=float(left),extrapolated_Nyquist=float(right),positive_extrapolation=bool(min(left,right)>0),scope='PSD text diagnostic only, not strain or posterior'))
    # No new comparison statistics from the calibration posterior: header only.
    with (ROOT/cfg['reference_posterior_path']).open() as stream:header=stream.readline().strip().split()
    check('published_header_matches_eight_plus_logL',set(header)==set(cfg['priors'])|{'logL'})
    result=dict(status='MANIFEST_V2_DOCUMENTARY_CHECKED_NOT_EXECUTION_AUTHORIZATION',utc=datetime.now(timezone.utc).isoformat(),
        manifest_filename='MANIFEST_v2.json',manifest_sha256=sha(PREP/'MANIFEST_v2.json'),code_sha256=own,source_pins=pin_results,
        checks=checks,dependency_delta=delta,public_PSD_diagnostics=psd,source_header=header,script_sha256=sha(__file__),
        wall_seconds=time.perf_counter()-started,no_strain_read=True,no_PE=True,no_physical_wave=True,posterior_values_parsed=False,
        source_repin_scope='Current guard bytes checked, not a re-review of C3 marker semantics or E2 authorization',
        finite_review_receipt_sha256=sha(HERE/'FINITE_REVIEW_001.json'))
    with output.open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2,allow_nan=False)
    print(json.dumps(dict(checks=len(checks),manifest_sha256=result['manifest_sha256'],public_PSD_diagnostics=psd,wall_seconds=result['wall_seconds'])))

if __name__=='__main__':main()
