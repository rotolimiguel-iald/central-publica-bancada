"""Apply second-review guard fixes as new, side-by-side script versions."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def change(s,a,b):
    if s.count(a)!=1:raise ValueError('Nonunique anchor '+a[:70])
    return s.replace(a,b,1)
def save(name,s):
    p=ROOT/'refeito'/name
    if p.exists():raise FileExistsError(p)
    compile(s,str(p),'exec');raw=s.encode();tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise RuntimeError('Output mismatch')
    tmp.replace(p)
s=(ROOT/'refeito/c1_evidence_guards.py').read_text()
s=change(s,'import hashlib','import hashlib\nimport csv\nimport json')
s=change(s,"    rows=measured['csv_checks']; keys(rows,'measured evidence')", "    with (root/'C7_INDEPENDENT/tables/event_reading_predictions.csv').open(encoding='utf-8-sig') as f:\n        raw=list(csv.DictReader(f))\n    catalog=json.loads((root/'C4_CATALOG_220.json').read_bytes())\n    validated_csv=validate_inputs(raw,catalog)\n    rows=measured['csv_checks']\n    require(keys(rows,'measured evidence')==set(validated_csv),'Evidence keys differ from hashed sources')")
s=change(s,"    for row in spins:\n        for k,v in row.items():", "    for row in spins:\n        require(set(row)=={'spin','exact_qnm','delta_mod','delta_root_zero','delta_mod_bcw_control','mod_bcw_relative_error'},'Incomplete spin schema')\n        pair=row['exact_qnm']\n        require(isinstance(pair,list) and len(pair)==2,'Incomplete QNM pair')\n        require(finite(pair[0],'QNM real')>0 and finite(pair[1],'QNM imaginary')<0,'QNM convention differs')\n        for k,v in row.items():")
s=change(s,"    for row in measured['profile_comparison']:\n        for k in", "    profiles=measured['profile_comparison']\n    require(len(profiles)==5 and {r['reading'] for r in profiles}=={'R-A','R-B','R-RAIZ-EP4','R-RAIZ-REST','R-LIN'},'Incomplete or duplicate profiles')\n    for row in profiles:\n        require(set(row)=={'reading','comparison_redshift','gamma_legacy_over_modern_minus_one','delta_legacy_over_modern_minus_one'},'Incomplete profile schema')\n        require(row['comparison_redshift']==0,'Comparison is not at z=0')\n        for k in")
save('c1_evidence_guards_v2.py',s)
s=(ROOT/'refeito/record_c1_013bis_v3.py').read_text(encoding='utf-8')
s=s.replace('from c1_evidence_guards import','from c1_evidence_guards_v2 import')
s=change(s,'    assert tmp.read_bytes()==raw',"    require(tmp.read_bytes()==raw,'Output bytes differ')")
s=s.replace("supersedes='C1_LEITURAS_v2.json',supersedes_sha256=sha(ROOT/'C1_LEITURAS_v2.json')", "supersedes='C1_LEITURAS_v3.json',supersedes_sha256=sha(ROOT/'C1_LEITURAS_v3.json')")
s=s.replace("v3_generator=dict(path=str(Path(__file__)),sha256=sha(Path(__file__))),", "v4_generator=dict(path=str(Path(__file__)),sha256=sha(Path(__file__))),\n                evidence_validator=dict(path='refeito/c1_evidence_guards_v2.py',sha256=sha(ROOT/'refeito/c1_evidence_guards_v2.py')),")
s=s.replace("target=ROOT/'C1_LEITURAS_v3.json'", "target=ROOT/'C1_LEITURAS_v4.json'")
s=s.replace("f'- C1_LEITURAS_v3.json:","f'- C1_LEITURAS_v4.json:")
s=s.replace('C1_ADENDO_CORRECOES_013BIS_v2.md','C1_ADENDO_CORRECOES_013BIS_v3.md')
s=s.replace('REAPROVEITAMENTO_C1_v2.md','REAPROVEITAMENTO_C1_v3.md')
save('record_c1_013bis_v4.py',s)

s=(ROOT/'refeito/measure_power_gate_013bis.py').read_text(encoding='utf-8')
s=change(s,"    if p.exists():raise FileExistsError(p)","    if p.exists():\n        if p.name not in ('F4_GW250114_WINDOW_POWER_NORM.json','C5_FISHER_v2.json'):\n            raise FileExistsError(p)\n        if json.loads(p.read_bytes())!=d:\n            raise ValueError('Existing partial evidence differs: '+str(p))\n        print('Reused identical partial evidence',p.name,sha(p))\n        return")
s=change(s,"    for row in recovery['results']:\n        key=", "    for row in recovery['results']:\n        if row['injected_a']!=0:continue\n        key=")
s=change(s,"    for (psd,family),snr in sorted(unique.items()):\n        bases.append", "    for (psd,family),snr in sorted(unique.items()):\n        injected={r['reading']:r['reference_SNR_403Mpc'] for r in recovery['results'] if r['psd']==psd and r['injection_family']==family and r['injected_a']==1}\n        bases.append")
s=change(s,"            rho=snr,scale_from_SNR40=snr/40,frame=", "            rho=snr,scale_from_SNR40=snr/40,rho_a1_by_reading=injected,\n            full_reference_range=[min([snr]+list(injected.values())),max([snr]+list(injected.values()))],\n            frame=")
s=change(s,"                rho=base['rho'],delta_L_reference_shape=delta,fixed_source=fixed,", "                rho=base['rho'],delta_L_reference_shape=delta,fixed_source=fixed,\n                rho_a1_same_distance=base.get('rho_a1_by_reading',{}).get(reading),\n                z_at_a1_same_distance=(fixed['z_max_local']*base['rho_a1_by_reading'][reading]/base['rho'] if reading in base.get('rho_a1_by_reading',{}) else None),")
s=change(s,"        conventions='Power here means", "        failed_attempt='measure_power_gate_013bis.py refused mixing GR and deformed-injection reference SNR; norm and Fisher outputs preserved and checked equal before reuse. Both SNR conventions now explicit.',\n        conventions='Reference rho is the GR injection; deformed a=1 SNR at the same distance is provided by reading alongside. Power here means")
save('measure_power_gate_013bis_v2.py',s)
print('Created validator v2, recorder v4, gate builder v2; cited originals unchanged')
