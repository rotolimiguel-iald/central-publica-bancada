"""Build a new additive package; original delivered artifacts stay immutable."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,csv,io,zipfile
B=Path(__file__).resolve().parents[1];OLD=B/'C7_INDEPENDENT';OUT=B/'C7_INDEPENDENT_v3_3'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def encoded(d):return (json.dumps(d,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
def put(name,data):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(data)
if OUT.exists():raise FileExistsError(OUT)
old=json.loads((OLD/'MANIFEST.json').read_bytes());content={}
for r in old['files']:
    p=OLD/r['path']
    if p.stat().st_size!=r['bytes'] or sha(p)!=r['sha256']:raise ValueError('Original package changed '+r['path'])
    content[r['path']]=p.read_bytes()
content['historical/README_v1.md']=content['README.md']
content['reproduce_c6.py']=(B/'refeito/reproduce_c6_v3_2.py').read_bytes()
content['verify_delivery.py']=(B/'refeito/verify_delivery_v3.py').read_bytes()
content['verify_manifest.py']=content['verify_delivery.py']
content['unit_checks.py']=(B/'refeito/package_unit_checks_v3_2.py').read_bytes()
# The unmodified frozen C6 modules remain under reproduction/ and retain their pins.
src=content['tgl_ringdown_prediction.py'].decode()
src=src.replace("scope = 'CONJECTURE_RESTRICTED_KMS_AND_MODULAR_CLOCK__NO_GLOBAL_KERR_HARTLE_HAWKING'", "scope = 'CONJECTURE — management hypothesis, not TGL canon; physical Kerr state and nonuniversal laboratory partition remain OPEN'")
if 'management hypothesis, not TGL canon' not in src:
    # Add a public scope field without changing the existing result structure/numbers.
    anchor="    elif reading=='R-MOD':"
    if src.count(anchor)!=1:raise ValueError('R-MOD anchor')
    src=src.replace(anchor,anchor+"\n        # CONJECTURE — management hypothesis, not TGL canon; Kerr-state and laboratory-partition walls remain OPEN.")
content['tgl_ringdown_prediction.py']=src.encode()
fixture=B/'cache/casa/RINGDOWN_DEPHASING_V2_RESULT.json'
content['fixtures/legacy_per_series_2.json']=encoded(dict(source='RINGDOWN_DEPHASING_V2_RESULT.json',source_sha256=sha(fixture),selector='per_series[2]',value=json.loads(fixture.read_bytes())['per_series'][2]))
evidence=['C1_LEITURAS_v4.json','C1_ADENDO_CORRECOES_013BIS_v3.md','C2_ADENDO_OBSERVAVEL_v2.md','C3_README_013BIS.md','C3_ADENDO_RMOD_RPROP_013BIS.md',
 'C6_ADENDO_REALIZADO_v2.json','C5_FISHER_v3.json','PORTAO_DO_PODER_013_v2.json','bis/F2_ALL_READING_TABLES_v2.json','bis/F2_ALL_READING_TABLES_v2.csv',
 'bis/F2_FREE_CLOCK_EXTENDED_v2.json','bis/F2_INDEPENDENT_GAUSSIAN_DENSITY.json','bis/C1_NUMERICAL_CONTROLS_v2.json','bis/C3_C6_TIMING_013BIS.json']
for n in evidence:content['current_evidence/'+Path(n).name]=(B/n).read_bytes()
c1=json.loads((B/'C1_LEITURAS_v4.json').read_bytes());c4=json.loads((B/'bis/F2_ALL_READING_TABLES_v2.json').read_bytes());c6=json.loads((B/'C6_ADENDO_REALIZADO_v2.json').read_bytes())
if len(c1['rows'])!=10 or len(c4['rows'])!=60 or len(c6['rows'])!=10:raise ValueError('Coverage')
lines=[];scope_rows=[]
for r in c1['rows']:
    name=r['reading'];state=r['clock_status']
    if name=='R-MOD':state='CONJECTURE — management hypothesis, not TGL canon'
    ex={k:v for k,v in r.items() if k.startswith('excluded_if_universal')}
    lines.append(f"| {name} | {state} | {r['rate_or_spectral_exponent']} | {json.dumps(ex,ensure_ascii=False)} |")
    for q in [x for x in c4['rows'] if x['reading']==name]:
        scope_rows.append(dict(**q,reading_status=state,EXCLUDED_IF_UNIVERSAL=json.dumps(ex,ensure_ascii=False),C1_scope=r['canonical_scope'],C6_pre_lnB=next(x['lnB_220plus440'] for x in c6['rows'] if x['reading']==name)))
content['tables/reading_scope.json']=encoded(dict(nonblind=True,rows=scope_rows,scope='Conditional 220 sector with higher Kerr modes; 440 fixed to GR in 32/33 GWTC5 products; no selected reading',sources={n:sha(B/n) for n in ['C1_LEITURAS_v4.json','bis/F2_ALL_READING_TABLES_v2.json','C6_ADENDO_REALIZADO_v2.json']}))
cols=list(dict.fromkeys(k for r in scope_rows for k in r));stream=io.StringIO();writer=csv.DictWriter(stream,fieldnames=cols);writer.writeheader();writer.writerows(scope_rows)
content['tables/reading_scope.csv']=stream.getvalue().encode()
readme='''# Conditional ringdown research package v3

NONBLIND. This is an internal reproducible research handoff, with no selected physical reading. Theory attribution: Luiz Antonio Rotoli Miguel. Original canonical programs and private files are not shipped or modified.

Run `python -B verify_delivery.py` and `python -B -O unit_checks.py` in a scientific Python environment with NumPy. `python -B run_demo.py` is an illustrative waveform, not an observational fit. Dependencies are listed in the requirements files; installation is the recipient's choice.

## Scientific scope, generated from C1/C4/C6-pre

Every catalogue ln B applies to the **conditional 220 sector with higher Kerr modes**, with 440 fixed to GR in 32/33 GWTC5 products (`HIGHER_MODE_DEVIATIONS_FIXED_TO_GR`); GW250114 uses free-440 nuisance parameters. This is not a full multimode deformed likelihood. C4 and C6-pre cover the ensemble only. A detector observes one realization, and the physical unraveling mapping remains OPEN. A universal `realization` prediction returning calibrated mean delta-tau and width of delta-f is NOT PAID; named stochastic demonstrations do not settle that mapping.

`tables/reading_scope.json` and `.csv` contain all ten readings across six datasets, ln B, bands, predicted shifts (5–95% where retained by the source), GR z and HPD, conditional verdicts, nulls and analytic-scenario labels. For catalogues, a weighted median-based prediction is not a new 5–95% posterior interval. Sigma/z are labelled diagnostics, never conversions from ln B. Original current-evidence JSONs retain the per-event intervals and derivations.

| Reading | Status | Conditional rate/exponent | EXCLUDED_IF_UNIVERSAL |
|---|---|---|---|
'''+ '\n'.join(lines)+'''

R-MOD is **[CONJECTURE — management hypothesis, not TGL canon]**. Its positive corotating oscillator is not a global Kerr thermal state. The nonuniversal rule that would distinguish a horizon clock from excluded laboratory clock identifications remains OPEN. The modular double-commutator clock is an additional postulate, not the positive-root generator in disguise. R-RAIZ-0 is a vacuum-to-one-quantum coherence; assigning it to a macroscopic classical strain is a type/observable bridge, not a theorem. Propagation with the source mass clock is dimensionally consistent but requires an unproved rule transporting that clock along the path; a large conditional attenuation is not a local R-B exclusion. H(z) must be supplied explicitly; no cosmology is selected by the propagation function.

Gamma damps ensemble amplitude, not energy. With x=Gamma*tau_GR, delta_tau=-x/(1+x). Beta is ALPHA_FINE_CODATA_2018*sqrt(e) in runtime. The default constants profile is CODATA2018_IAU2015. LEGACY_V346 is a different, non-CODATA/IAU profile; the legacy regression uses `delta_tau_linear`, not the exact additive-rate shift. The exact/BCW comparison and units checks are in current_evidence/C1_NUMERICAL_CONTROLS_v2.json. Non-220 modes require externally supplied exact QNMs and angular factors; no BCW extrapolation is silently used.

Time is seconds, mass detector-frame solar masses, strain dimensionless. Phase is referenced to `t_start`; plus uses cosine and cross sine, with h_plus-i*h_cross the negative-frequency face-on convention. Before onset both polarizations vanish. This supplies arrays for Bilby/PyCBC consumers, not a pyRing likelihood plugin. The C6 timing table records actual detector sample cuts; identical L1 cuts at requested 10 and 10.5 t_M are not independent measurements. C5's common overtone damping convention differs from the per-mode template law; do not conflate them.

The C5 FULL_IMR calibration failed and is closed as a measured wall. MATCHED_RINGDOWN successes are separate closed-set numerical recovery controls. Low-SNR injection tables may have positive mean ln B from prior volume (Occam effect), including null injections; this is not a detection. C6-pre remains a pre-power-gate, uncalibrated nonblind diagnostic; near-zero ln B is not confirmation. Only R-GLOBAL is an exact relational identity in its declared implementation. The old lost template version is not byte-reproducible from its historical checks. The README under historical/ is a dated record superseded here, not current guidance.

## Clean C6-pre reproduction

Provide the two already downloaded public GWOSC files identified in `reproduction/ORDEM_013_RINGDOWN/C6_DOWNLOADS.json`. The wrapper verifies their SHA256 before copying them. It does not download or read any secret configuration.

```sh
python -B reproduce_c6.py
python -B reproduce_c6.py --run --source-cache /path/to/verified/on_source --work-root /short/work --output /short/results/C6_v3.json
```

Output must be outside the package. Every window is computed from verified strain in a fresh temporary directory; saved grids are refused. The wrapper compares numbers and accepts an explicit downgrade to an inconclusive/awaiting-data status; the scientific verdict is not fixed to one token. A numerical match does not calibrate the scientific model. Logs are preserved beside the output and temporaries are removed in finally, including failures. Frozen C6 code and registration are unchanged under reproduction/.

**Windows MAX_PATH:** use a short extraction/work path (for example C:\\rdv3) or a long-path-enabled Python/OS. Deep paths can exceed legacy 260-character limits; no deep-path success is claimed. Minimum legacy fixture is `fixtures/legacy_per_series_2.json`, with source hash and selector. Unit checks include exact rate conversion, a=0/a=1, onset, legacy regression and invalid-input refusals, including under Python -O.

## Attribution and evidence

Public observations are by LIGO Scientific Collaboration, Virgo Collaboration and KAGRA Collaboration. Each upstream licence is preserved separately; there is no blanket licence inferred for this research code. GWOSC strain is CC BY 4.0; Zenodo 17018009 is MIT; 21454847 and 17461225 are CC BY 4.0. Source receipts identify those releases. Manifest hashes certify bytes, not proofs. No Lean is executed here and no gate changes. Independent review, calibration and physical interpretation retain the limitations in current_evidence.
'''
content['README.md']=readme.encode();content['OVERVIEW.md']=content['README.md']
# Ship verifiable documentary licence sources, without relicensing research code.
ledger=B/'cache/MANIFESTO_DOWNLOADS_013BIS_v2.json'
content['provenance/DOWNLOAD_LICENSE_LEDGER.json']=ledger.read_bytes()
for rid in ('17018009','21454847','17461225'):
    content['provenance/zenodo_'+rid+'_record.json']=(B/('cache/public/'+rid+'/record.json')).read_bytes()
content['provenance/GWOSC_acknowledgement.html']=(B/'cache/literature/gwosc_acknowledgement_013bis.html').read_bytes()
for n in ('README.md','OVERVIEW.md'):
    text=content[n].decode()
    text=text.replace('Original current-evidence JSONs retain the per-event intervals and derivations.', 'Per-event catalogue intervals are retained in evidence/C4_CATALOG_220.json; aggregate diagnostics are in current_evidence/F2_ALL_READING_TABLES_v2.json.')
    text=text.replace('Each upstream licence is preserved separately;', 'Upstream licence declarations and source records are shipped under provenance/, with SHIPPED_ATTRIBUTIONS.json linking each file hash; full legal licence texts are externally referenced, not all reproduced;')
    text+='\nPortuguese current-evidence addenda are original source documents, not the English entry-point guidance. English scope and limitations are fully stated in this README and the generated table.\n'
    content[n]=text.encode()
licence_rows=[]
for n,raw in content.items():
    isnoise='/cache/empirical_noise/' in n
    licence_rows.append(dict(path=n,sha256=hashlib.sha256(raw).hexdigest(),
      licence_id='cc-by-4.0' if isnoise else None,
      scope='Derived GWOSC off-source noise; upstream policy and original data hashes in frozen empirical-noise receipt' if isnoise else 'Research code, derived reports or archival text: no blanket licence inferred; data-source licences are in documentary ledger',
      provenance='provenance/GWOSC_acknowledgement.html' if isnoise else 'provenance/DOWNLOAD_LICENSE_LEDGER.json'))
content['provenance/SHIPPED_ATTRIBUTIONS.json']=encoded(dict(files=licence_rows,ledger_sha256=sha(ledger),scope='Per-file attribution; licence references are not a legal determination for research code'))
attributions=json.loads(content['provenance/SHIPPED_ATTRIBUTIONS.json'])['files']
expected=set(content)-{'provenance/SHIPPED_ATTRIBUTIONS.json'}
names=[r['path'] for r in attributions]
if len(names)!=len(set(names)) or set(names)!=expected:raise ValueError('Attribution coverage/duplicates')
for row in attributions:
    if row['sha256']!=hashlib.sha256(content[row['path']]).hexdigest():raise ValueError('Attribution bytes differ')
for n,raw in sorted(content.items()):put(n,raw)
manifest=dict(status='NONBLIND_CONDITIONAL_RESEARCH_PACKAGE_V3',utc=datetime.now(timezone.utc).isoformat(),supersedes_manifest_sha256=sha(OLD/'MANIFEST.json'),builder_sha256=sha(Path(__file__)),files=[dict(path=n,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()) for n,raw in sorted(content.items())])
put('MANIFEST.json',encoded(manifest))
archive=B/'cache/C7_INDEPENDENT_v3_3.zip'
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():z.write(p,'C7_INDEPENDENT_v3_3/'+p.relative_to(OUT).as_posix())
receipt=dict(status='BUILT_NOT_YET_EXECUTED',package=OUT.name,archive=str(archive.relative_to(B)),archive_sha256=sha(archive),manifest_sha256=sha(OUT/'MANIFEST.json'),files=len(manifest['files']))
with (B/'bis/C7_V3_3_BUILD.json').open('xb') as f:f.write(encoded(receipt))
print(json.dumps(receipt))
