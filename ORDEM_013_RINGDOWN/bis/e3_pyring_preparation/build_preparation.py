"""Read-only source inspection + exclusive preparation artifacts; no science.

Only stdlib. Never imports pyRing, E2 production modules, NumPy or prepared code.
No strain bytes are opened. Data pins are inherited explicitly from draft003.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,configparser,hashlib,json,math,tarfile,time

HERE=Path(__file__).resolve().parent;B=HERE.parents[1];ROOT=B.parent


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def write_new(path,obj):
    raw=(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    with path.open('xb') as f:f.write(raw)
    if path.stat().st_size!=len(raw):raise OSError('Incomplete artifact')


def main():
    started=time.perf_counter()
    for name in ('CONFIG.json','SOURCE_REVIEW.json','MANIFEST.json'):
        if (HERE/name).exists():raise FileExistsError('Preserve existing preparation: '+name)
    vendor=B/'cache/pyring_oracle/vendor/pyRing'
    source_tar=B/'cache/source_distributions/pyRingGW-2.7.0.tar.gz'
    vendor_names=('pyRing.py','initialise.py','waveform.pyx','likelihood.pyx','noise.py','data/NR_data/berti_qnm_fits.txt')
    matches={}
    with tarfile.open(source_tar,'r:gz') as archive:
        for name in vendor_names:
            member=archive.getmember('pyRingGW-2.7.0/pyRing/'+name)
            if not member.isfile() or member.issym() or member.size>4_000_000:raise ValueError('Unexpected source archive member')
            raw=archive.extractfile(member).read()
            if raw!=(vendor/name).read_bytes():raise ValueError('Installed text differs from source archive')
            matches[name]=hashlib.sha256(raw).hexdigest()
    ini=B/'cache/public/17018009/selected/26f158d16a946d97.ini'
    parsed=configparser.ConfigParser();parsed.read(ini,encoding='utf-8')
    draft_path=B/'bis/E2_DESIGN_DRAFT_003.json'
    draft=json.loads(draft_path.read_bytes());pilot=draft['pe_jobs']['GW250114_PILOT']
    target=B/'cache/public/17018009/selected/b0e560a83a0d3d5f.dat'
    with target.open(encoding='utf-8') as f:header=f.readline().strip()
    expected=['psi','Mf','af','cosiota','A2220_1','A2220_2','phi2220_1','phi2220_2','logL']
    if header.lstrip('# ').split()!=expected:raise ValueError('Published schema changed')
    rows=[line.split() for line in (vendor/'data/NR_data/berti_qnm_fits.txt').read_text().splitlines()[1:] if line.strip()]
    coefficients=[list(map(float,row[3:])) for row in rows if list(map(int,row[:3]))==[2,2,0]]
    if len(coefficients)!=1 or len(coefficients[0])!=6:raise ValueError('Ambiguous QNM coefficients')
    if parsed.get('input','amp-non-prec-sym')!='0' or parsed.getfloat('input','max-Kerr-amp-ratio')!=0 or parsed.get('input','spheroidal')!='0':
        raise ValueError('Unimplemented branch/model contract')
    if ast.literal_eval(parsed.get('input','kerr-modes'))!=[(2,2,2,0)]:raise ValueError('Not Kerr220')
    if parsed.getfloat('Priors','fix-phi')!=0:raise ValueError('Azimuth must be zero')
    index_path=B/'cache/public/17018009/archive_index.json'
    index=json.loads(index_path.read_bytes())
    public_members=[r for r in index['members'] if r['name'].endswith(('_H1_psd.dat','_L1_psd.dat'))]
    comparison_path=B/'C6_PYRING_START_COMPARISON.json'
    comparison=json.loads(comparison_path.read_bytes())
    references=[x for x in comparison['results'] if x['start_tM']==10 and x['release_model']=='Fundamental 220']
    if len(references)!=1 or references[0]['source_sha256']!=sha(target):raise ValueError('Released target provenance changed')
    cfg=dict(status='PREPARED_NOT_EXECUTED',event=pilot['event'],mode='calibration',
      trigger_GPS=parsed.getfloat('input','trigtime'),start_offset_s=parsed.getfloat('Priors','fix-t'),
      reference_detector=parsed.get('input','ref-det'),detectors=['H1','L1'],
      ra=parsed.getfloat('Priors','fix-ra'),dec=parsed.getfloat('Priors','fix-dec'),
      sample_rate_hz=parsed.getfloat('input','sampling-rate'),
      analysis_duration_s=parsed.getfloat('input','analysis-duration'),
      band_hz=[parsed.getfloat('input','f-min-bp'),parsed.getfloat('input','f-max-bp')],
      reference_amplitude=parsed.getfloat('input','reference-amplitude'),qnm_coefficients=coefficients[0],
      model='Kerr220_two_independent_complex_branches_with_explicit_inclination_harmonics',
      priors={'psi':[0.,math.pi],'Mf':[10.,500.],'af':[0.,.99],'cosiota':[-1.,1.],
        'A2220_1':[0.,50.],'A2220_2':[0.,50.],'phi2220_1':[0.,2*math.pi],'phi2220_2':[0.,2*math.pi]},
      read_start_GPS=1420878137.,read_duration_s=8.,noise_chunk_s=4.,psd_duration_s=256,
      offsource_exclusion_s=16.,quality_required=pilot['quality_required'],
      injection_flags_required=pilot['injection_flags_required'],data=pilot['data'],
      data_pin_status='INHERITED_FROM_DRAFT003; strain bytes not read or rehashed in preparation; verified on authorized execution',
      variants=['welch'],public_psd={},public_psd_status='NOT_EXTRACTED_NOT_PINNED_DISABLED',
      public_psd_members=public_members,wall_envelope_seconds=7200,
      variant_wall_seconds={'welch':4800,'public_psd':1800},
      sampler=dict(seed=1234,workers=1,nlive=512,walks=50,dlogz=.1,maxcall=1_000_000,
        minimum_effective_samples=100,minimum_posterior_samples=1000),
      runtime_manifest_path=draft['runtime_manifest_relative_to_Chatgpt'],
      budget_path='ORDEM_013_RINGDOWN/bis/PART_B_BUDGET_START.json',
      output_relative_to_Chatgpt='ORDEM_013_RINGDOWN/cache/E3_KERR220_CALIBRATION_V1',
      reference_posterior_path=target.relative_to(ROOT).as_posix(),reference_posterior_sha256=sha(target),
      limitations=['Exact released pyRing version unverified; 2.7.0 source and actual posterior header anchor model',
        'GWOSC strain not shown identical to released C00_AR GWF',
        'Off-source Welch PSD not released external PSD; public NRSur PSD identity also UNKNOWN',
        'Data-only bandpass follows pyRing2.7; model-bandpass equivalence near edges unverified',
        '512 live points versus published 4096; no claim of converged modes before execution/review',
        'No posterior run in preparation; equal-weight released interpretation retains merge-provenance uncertainty',
        'Same event, no independent evidence or calibrated significance'])
    write_new(HERE/'CONFIG.json',cfg)
    sources=[ini,draft_path,target,index_path,comparison_path,source_tar,
      B/'cache/pyring_oracle/PREPARATION.json',
      ROOT/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md',
      ROOT/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/auditoria_da_gerencia/aud_2_C6.txt']
    sources += [vendor/name for name in vendor_names]
    # Execution helpers only; hash every imported local production dependency.
    sources += [B/'bis/e2_code'/name for name in ('pe_runner.py','registration_guard.py','strain_io.py','run_controlled.py')]
    sources += [ROOT/cfg['runtime_manifest_path'],ROOT/cfg['budget_path'],HERE/'PLAN.md',HERE/'CONFIG.json']
    pins={p.relative_to(ROOT).as_posix():sha(p) for p in sources}
    excerpts={}
    ranges={'pyRing.py':[(677,681),(745,754),(861,874),(1060,1084),(1182,1197)],
      'waveform.pyx':[(241,246),(889,931),(1084,1104),(1190,1228),(1301,1308)],
      'initialise.py':[(220,234),(289,294)],'noise.py':[(219,225),(728,748)],
      'likelihood.pyx':[(284,293),(423,448)]}
    for name,spans in ranges.items():
        lines=(vendor/name).read_text().splitlines()
        excerpts[name]=[dict(start_line=a,end_line=b,text='\n'.join(lines[a-1:b])) for a,b in spans]
    review=dict(status='SOURCE_AND_SCHEMA_INSPECTION_ONLY',utc=datetime.now(timezone.utc).isoformat(),
      source_sha256=pins,source_distribution_matches=matches,
      posterior_read_scope='Header interpreted; full bytes hashed, no posterior values parsed',
      posterior_header=header,public_psd_read_scope='Archive index only; PSD values and file hashes not read',
      public_psd_members=public_members,existing_reference_summary=references[0],
      reference_summary_status='INHERITED_ALREADY_EXISTING_NOT_RECALCULATED',
      excerpts=excerpts,
      live_docs='https://lscsoft.docs.ligo.org/pyring/model_inputs/',
      live_docs_scope='Read separately via browser; mutable/current, not proof of release version; no hash claimed',
      axioms='N/A',new_theorems=0)
    write_new(HERE/'SOURCE_REVIEW.json',review)
    code={}
    for p in HERE.glob('*.py'):
        ast.parse(p.read_text(),filename=str(p));code[p.name]=sha(p)
    pins[(HERE/'SOURCE_REVIEW.json').relative_to(ROOT).as_posix()]=sha(HERE/'SOURCE_REVIEW.json')
    manifest=dict(status='PREPARED_NOT_EXECUTED_CALIBRATION_ONLY',created_utc=datetime.now(timezone.utc).isoformat(),
      code_sha256=code,source_and_config_pins=pins,calibration_only=True,
      wall_envelope_seconds=7200,preparation_wall_seconds=time.perf_counter()-started,
      checks=['stdlib builder only','six pyRing source texts byte-identical to sdist','published posterior header matches eight free parameters',
        'reference posterior hash matches existing comparison','source AST parsed without import'],
      not_done=['No strain bytes read','No waveform generated','No likelihood evaluated','No sampler executed','No calibration authorization created'],
      files_written=[p.name for p in sorted(HERE.iterdir()) if p.is_file()]+['MANIFEST.json'],
      upstream_E2_sources_modified=False,acceptance_E3_1='NAO_PAGO_EXECUTION_AND_REVIEW_PENDING')
    write_new(HERE/'MANIFEST.json',manifest)
    print(json.dumps(dict(status=manifest['status'],manifest_sha256=sha(HERE/'MANIFEST.json'),files=manifest['files_written'],
      source_matches=len(matches),syntax_checked=len(code),preparation_wall_seconds=manifest['preparation_wall_seconds']),indent=2))


if __name__=='__main__':main()
