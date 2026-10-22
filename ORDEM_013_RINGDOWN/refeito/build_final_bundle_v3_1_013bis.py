"""One English entry point over all new packages, followed by a clean byte check."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import json,hashlib,zipfile,subprocess,sys,tempfile,shutil
B=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
def main():
    archive=B/'cache/TGL_RINGDOWN_DELIVERY_v3_1.zip';out=B/'bis/C7_FINAL_BUNDLE_V3_1_VALIDATION.json'
    if archive.exists() or out.exists():raise FileExistsError('Preserve earlier bundle and receipt')
    packages=['C7_INDEPENDENT_v3_3','C7_POSTERIOR_REPRODUCTION_v3_2','C7_GWTC3_REPRODUCTION_v3_2','C7_INJECTION_REPRODUCTION_v3_2','C7_IMR_RECOVERY_REPRODUCTION_v3','C7_COHERENT_SOURCE_REPRODUCTION_v3','C7_NATIVE_SEOB_WAVEFORM_v3']
    content={};sources=[]
    for name in packages:
        root=B/name;manifest=json.loads((root/'MANIFEST.json').read_bytes());rows=manifest.get('files',manifest.get('shipped_files'))
        for r in rows:
            p=root/r['path']
            if sha(p)!=r['sha256'] or p.stat().st_size!=r['bytes']:raise ValueError('Changed package '+str(p))
            content[name+'/'+r['path']]=p.read_bytes()
        content[name+'/MANIFEST.json']=(root/'MANIFEST.json').read_bytes()
        z=B/'cache'/(name+'.zip')
        sources.append(dict(package=name,archive=str(z.relative_to(B)),sha256=sha(z),manifest_sha256=sha(root/'MANIFEST.json')))
    guide=(B/'C7_INDEPENDENT_v3_3/README.md').read_text(encoding='utf-8')
    guide='''# Unified conditional ringdown research delivery v3_1

NONBLIND. Current English entry point, created after all seven new packages. Numerical reproducibility, model calibration, and physical confirmation are separate. No reading is selected and no canonical gate is changed. The original Portuguese documentary sources are preserved as source evidence inside the packages; they are not additional English operating instructions.

Run `python -B verify_delivery.py` first. The primary package is `C7_INDEPENDENT_v3_3/`; run its unit_checks.py and reproduce_c6.py using the commands below with that directory prefix. Work and output roots must be outside the entire immutable delivery, preferably short paths. The primary C6-pre reproduction uses existing verified H1/L1 source files. All calculation outputs are external; nothing overwrites a shipped reference. Windows MAX_PATH warning applies throughout.

The three posterior/injection supplements accept stage plus explicit external work/output roots and remove temporary data in finally. The IMR/coherent/native supplements default to hash verification; --prepare-only checks preparation without scientific execution; --run is a separate future authorized numerical replay. **Do not launch a new C5 campaign in ORDEM013BIS:** the C5 wall remains closed. Historical scripts live under reproduce_legacy.py only to preserve their numeric definitions and are intended to be called by the guarded wrapper, not directly.

The recorded fresh C6-pre replay of v3_2, whose complete execution tree is byte-identical to v3_3, has 75 rows and zero maximum lnB difference. This verifies the frozen implementation's output, not the adequacy of its physical likelihood. Its scientific status remains INCONCLUSIVE_SYSTEMATICS. The finite-number/type guards, downgrades and cleanup controls are separate from this ordinary replay. Full posterior/injection science has not been rerun merely to repackage cleanup changes; earlier scientific receipts remain dated evidence.

Licences: primary provenance/SHIPPED_ATTRIBUTIONS.json maps shipped hashes to documentary sources; DOWNLOAD_LICENSE_LEDGER.json carries per-input licences and source-record hashes. MIT applies to Zenodo17018009, CC BY4.0 to records21454847/17461225 and GWOSC public data. These declarations do not assign an open licence to all research code or every derived report. Full legal texts are external references unless included explicitly. Public observations are attributed to the LIGO Scientific, Virgo and KAGRA Collaborations. Theory attribution: Luiz Antonio Rotoli Miguel.

## Packages

'''+''.join('- '+p+'\n' for p in packages)+'\n## Primary scientific and reproduction guide\n\n'+guide
    content['README.md']=guide.encode();content['OVERVIEW.md']=content['README.md']
    content['verify_delivery.py']=(B/'refeito/verify_delivery_v3.py').read_bytes()
    receipts=['bis/C7_V3_2_C6_REPLAY.json','bis/C7_V3_2_CLEAN_VALIDATION.json','bis/C7_V3_3_DOCUMENTARY_VALIDATION.json','bis/C7_SUPPLEMENTS_V3_CLEANUP_CONTROLS.json','bis/C7_SUPPLEMENTS_V3_2_BUILD.json','bis/C7_OTHER_V3_BUILD.json','bis/F7_POST_REMOVAL_CHECK.json','bis/F7_NAMED_TEMPORARIES_REMOVED.json']
    for n in receipts:content['validation/'+Path(n).name]=(B/n).read_bytes()
    manifest=dict(status='NONBLIND_RESEARCH_DELIVERY__CALIBRATION_NOT_PASSED',utc=datetime.now(timezone.utc).isoformat(),source_packages=sources,builder_sha256=sha(Path(__file__)),files=[dict(path=n,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()) for n,raw in sorted(content.items())])
    content['MANIFEST.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for n,raw in content.items():z.writestr('TGL_RINGDOWN_DELIVERY_v3_1/'+n,raw)
    receipt=dict(status='INCOMPLETE',archive=str(archive.relative_to(B)),archive_sha256=sha(archive),files=len(manifest['files']),source_packages=sources)
    cache=(B/'cache').resolve();temporary=Path(tempfile.mkdtemp(prefix='bundle_v3_',dir=cache)).resolve()
    try:
        if not temporary.is_relative_to(cache) or temporary==cache:raise ValueError('Unsafe temporary')
        with zipfile.ZipFile(archive) as z:
            if z.testzip() is not None:raise ValueError('CRC failure')
            for info in z.infolist():
                rel=PurePosixPath(info.filename)
                if rel.is_absolute() or '..' in rel.parts or '\\' in info.filename:raise ValueError('Unsafe ZIP')
                new(temporary/rel,z.read(info))
        root=temporary/'TGL_RINGDOWN_DELIVERY_v3_1'
        p=subprocess.run([sys.executable,'-B',str(root/'verify_delivery.py')],capture_output=True,cwd=root)
        new(B/'bis/C7_FINAL_BUNDLE_V3_1_VERIFY.log',p.stdout+p.stderr)
        if p.returncode:raise RuntimeError('Clean verifier failed')
        receipt['verification']=json.loads(p.stdout);receipt['status']='PASS_CLEAN_BUNDLE_BYTE_VERIFICATION'
    finally:
        if not temporary.is_relative_to(cache) or temporary==cache:raise ValueError('Unsafe cleanup')
        shutil.rmtree(temporary);receipt['temporary_removed']=not temporary.exists()
        receipt['finished_utc']=datetime.now(timezone.utc).isoformat()
        new(out,(json.dumps(receipt,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in receipt.items() if k!='source_packages'}))
if __name__=='__main__':main()
