"""Finalize both preselected PSD branches; stdlib, metadata and text only."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,ast,math,time,os
HERE=Path(__file__).resolve().parent;B=HERE.parents[1];ROOT=B.parent


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
    return h.hexdigest()


def replace_snapshotted(path,value):
    snapshot=HERE/'snapshots/pre_public_psd_001'/path.name
    if not snapshot.is_file():raise ValueError('Required previous-byte snapshot absent')
    raw=(json.dumps(value,indent=2,allow_nan=False,ensure_ascii=False)+'\n').encode()
    temp=path.with_name(path.name+'.final_pending')
    with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if temp.stat().st_size!=len(raw):raise OSError('Incomplete temporary')
    temp.replace(path)


def main():
    started=time.perf_counter()
    cfg=json.loads((HERE/'CONFIG.json').read_bytes())
    if cfg['public_psd_status']!='NOT_EXTRACTED_NOT_PINNED_DISABLED':raise FileExistsError('Already finalized: preserve final products')
    receipt=json.loads((HERE/'PSD_EXTRACTION.json').read_bytes())
    if receipt['status']!='TWO_PUBLIC_PSD_TEXTS_EXTRACTED_AND_ARCHIVE_PIN_VERIFIED':raise ValueError('PSD integrity not established')
    schemas={}
    for item in receipt['files']:
        path=ROOT/item['relative_to_Chatgpt']
        if not path.resolve().is_relative_to((B/'cache/E3_KERR220_PSD_INPUTS').resolve()) or sha(path)!=item['sha256']:
            raise ValueError('PSD path/pin differs')
        detector=next((d for d in ('H1','L1') if path.name.endswith('_'+d+'_psd.dat')),None)
        if detector is None or detector in schemas:raise ValueError('PSD detector ambiguous')
        count=0;previous=-math.inf;first=None;last=None;positive=True
        with path.open(encoding='utf-8') as stream:
            for line in stream:
                if not line.strip() or line.startswith('#'):continue
                row=line.split()
                if len(row)!=2:raise ValueError('PSD schema differs')
                f,p=map(float,row)
                if not math.isfinite(f) or not math.isfinite(p) or f<=previous:raise ValueError('Invalid PSD text')
                positive=positive and p>0;previous=f;first=f if first is None else first;last=f;count+=1
        if not positive:raise ValueError('PSD input not strictly positive')
        schemas[detector]=dict(rows=count,columns=['Frequency','Strain'],frequency_min=first,frequency_max=last,
          all_values_finite=True,frequencies_strictly_increasing=True,PSD_positive=True,
          interpretation='PSD, per released pesummary/psds member; not assumed identical to external pyRing PSD')
        cfg['public_psd'][detector]={k:item[k] for k in ('relative_to_Chatgpt','sha256','archive_member')}
    if set(schemas)!={'H1','L1'}:raise ValueError('Incomplete public PSD pair')
    cfg['variants']=['welch','public_psd']
    cfg['public_psd_status']='EXTRACTED_PINNED_PRESELECTED_ROBUSTNESS_NOT_PROVEN_IDENTICAL_RELEASE'
    replace_snapshotted(HERE/'CONFIG.json',cfg)
    review=json.loads((HERE/'SOURCE_REVIEW.json').read_bytes())
    review.update(public_psd_read_scope='Two PSD text files extracted and statically inspected; no FFT/likelihood/strain/waveform executed',
      public_psd_schemas=schemas,public_psd_sha256={k:v['sha256'] for k,v in cfg['public_psd'].items()},
      finalization_utc=datetime.now(timezone.utc).isoformat(),exact_release_version='OPEN',exact_PSD_or_C00_AR_identity='NOT_ESTABLISHED')
    manifest=json.loads((HERE/'MANIFEST.json').read_bytes())
    source_key=(HERE/'SOURCE_REVIEW.json').relative_to(ROOT).as_posix()
    pins={key:sha(ROOT/key) for key in manifest['source_and_config_pins'] if key!=source_key}
    for p in [HERE/'PSD_EXTRACTION.json']+[ROOT/item['relative_to_Chatgpt'] for item in receipt['files']]:
        pins[p.relative_to(ROOT).as_posix()]=sha(p)
    review['source_sha256']=dict(pins)
    replace_snapshotted(HERE/'SOURCE_REVIEW.json',review)
    pins[source_key]=sha(HERE/'SOURCE_REVIEW.json')
    code={}
    for path in HERE.glob('*.py'):
        ast.parse(path.read_text(),filename=str(path));code[path.name]=sha(path)
    # Independent-of-science static invariants.
    if sum(cfg['variant_wall_seconds'][v] for v in cfg['variants'])>cfg['wall_envelope_seconds']-30:
        raise ValueError('No cleanup margin in shared envelope')
    if set(cfg['priors'])!={'psi','Mf','af','cosiota','A2220_1','A2220_2','phi2220_1','phi2220_2'}:
        raise ValueError('Published free parameter schema differs')
    checks=['All prepared Python ASTs parse without import','Two positive finite monotonically sampled PSD texts pinned',
      'Fixed Welch then public PSD order, no posterior selection','6600s allocated within7200s shared envelope',
      'Eight free parameters matching existing released header','Latest E2 activation guard dependency hash included']
    finalized=dict(status='PREPARED_NOT_EXECUTED_BOTH_PSD_BRANCHES',created_utc=datetime.now(timezone.utc).isoformat(),
      checks=checks,PSD_schemas=schemas,PSD_extraction_wall_seconds=receipt['wall_seconds'],
      metadata_finalization_wall_seconds=time.perf_counter()-started,
      code_sha256=code,unpaid=['PE and posterior compatibility','Identity to external pyRing PSD and C00_AR','Exact released source version'],
      E2_source_edits_this_finalization=False)
    finalpath=HERE/'FINALIZATION.json'
    with finalpath.open('x',encoding='utf-8') as f:json.dump(finalized,f,indent=2);f.write('\n')
    pins[finalpath.relative_to(ROOT).as_posix()]=sha(finalpath)
    manifest.update(code_sha256=code,source_and_config_pins=pins,created_utc=datetime.now(timezone.utc).isoformat(),
      revision='FINAL_WITH_TWO_PINNED_PSD_BRANCHES',checks=manifest['checks']+checks,
      finalization_receipt_sha256=sha(finalpath),
      files_written=[p.relative_to(ROOT).as_posix() for p in sorted(HERE.rglob('*')) if p.is_file()]+[item['relative_to_Chatgpt'] for item in receipt['files']],
      writes_scope='Kerr preparation and two PSD texts only; preceding E2 activation exception documented separately',
      total_preparation_wall_seconds=manifest['preparation_wall_seconds']+receipt['wall_seconds']+time.perf_counter()-started)
    replace_snapshotted(HERE/'MANIFEST.json',manifest)
    # Verify the complete final graph after writing, without invoking runtime.
    for key,pin in manifest['source_and_config_pins'].items():
        if sha(ROOT/key)!=pin:raise ValueError('Final pin drift '+key)
    for key,pin in code.items():
        if sha(HERE/key)!=pin:raise ValueError('Final code drift '+key)
    print(json.dumps(dict(manifest_sha256=sha(HERE/'MANIFEST.json'),status=manifest['status'],revision=manifest['revision'],
      written_files=len(manifest['files_written']),code_files=len(code),checks=checks,
      E2_activation_guard_sha256=pins['ORDEM_013_RINGDOWN/bis/e2_code/registration_guard.py'],
      total_preparation_wall_seconds=manifest['total_preparation_wall_seconds']),indent=2))


if __name__=='__main__':main()
