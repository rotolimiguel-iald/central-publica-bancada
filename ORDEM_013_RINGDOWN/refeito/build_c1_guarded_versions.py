"""Versioned copies implementing review B1/B2, without altering audited originals."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def change(s,a,b):
    if s.count(a)!=1:
        raise ValueError('Nonunique patch anchor: '+a[:90])
    return s.replace(a,b,1)

def save(name,s):
    p=ROOT/'refeito'/name
    if p.exists(): raise FileExistsError(p)
    compile(s,str(p),'exec')
    raw=s.encode('utf-8');tmp=p.with_suffix('.tmp')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise RuntimeError('Write mismatch')
    tmp.replace(p)

s=(ROOT/'refeito/measure_c1_013bis.py').read_text(encoding='utf-8')
s=change(s,'import qnm','import qnm\nfrom c1_evidence_guards import require, finite, validate_inputs, validate_clock')
s=change(s,"    assert core['P2']['verdict']=='P2_EXCLUDED_IN_READING'\n    assert core['tau_star_alternatives']['unruh_g_excluded'] is True",'    clock_flags=validate_clock(core)')
s=change(s,"    assert all(v.v==(one if k=='R-PROP' else w).v for k,v in dims.items())","    require(all(v.v==(one if k=='R-PROP' else w).v for k,v in dims.items()), 'Derived units differ')")
s=change(s,"    saved={(r['event'],r['reading']):r for r in csv.DictReader(csvpath.open(encoding='utf-8-sig'))}","    with csvpath.open(encoding='utf-8-sig') as f:\n        raw_rows=list(csv.DictReader(f))\n    saved=validate_inputs(raw_rows,cat)")
s=change(s,"                actual=fresh[newkey]; baseline=float(public[oldkey])","                actual=finite(fresh[newkey],newkey); baseline=finite(public[oldkey],oldkey)")
s=change(s,"            assert max(errors.values())<1e-12,(ev['event'],reading,errors)","            require(all(math.isfinite(v) and 0<=v<1e-12 for v in errors.values()), str((ev['event'],reading,errors)))")
s=change(s,"            ROOT/'cache/casa/um_absoluto.json',Path(__file__)]})","            ROOT/'cache/casa/um_absoluto.json',Path(__file__),ROOT/'refeito/c1_evidence_guards.py']})")
s=change(s,"    target=ROOT/'bis/C1_NUMERICAL_CONTROLS.json'\n    with target.open('x',encoding='utf-8') as f: json.dump(report,f,ensure_ascii=False,indent=2); f.write('\\n')\n    assert oldpath.read_bytes()==old", "    target=ROOT/'bis/C1_NUMERICAL_CONTROLS_v2.json'\n    require(not target.exists(),'Output already exists')\n    raw=(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\\n').encode('utf-8')\n    tmp=target.with_suffix('.tmp')\n    with tmp.open('xb') as f:f.write(raw)\n    require(tmp.read_bytes()==raw,'Output bytes differ')\n    tmp.replace(target)\n    require(oldpath.read_bytes()==old,'Historical v1 changed')")
save('measure_c1_013bis_v2.py',s)

s=(ROOT/'refeito/record_c1_013bis.py').read_text(encoding='utf-8')
s=change(s,'import hashlib,json','import hashlib,json\nfrom c1_evidence_guards import validate_evidence, require')
s=s.replace('C1_NUMERICAL_CONTROLS.json','C1_NUMERICAL_CONTROLS_v2.json')
s=change(s,"    stamp=datetime.now(timezone.utc).isoformat()", "    core=json.loads((ROOT/'cache/casa/um_absoluto.json').read_bytes())['core']['clock_test_result_v369']\n    validated=validate_evidence(ROOT,measured,core)\n    for row in refs:\n        if row.get('sha256'):\n            require(sha(ROOT/row['path'])==row['sha256'],'Primary source changed')\n    stamp=datetime.now(timezone.utc).isoformat()")
s=change(s,"supersedes=original.name,supersedes_sha256=sha(original),updated_utc=stamp,", "supersedes='C1_LEITURAS_v2.json',supersedes_sha256=sha(ROOT/'C1_LEITURAS_v2.json'),updated_utc=stamp,\n                origin_generator_sha256=data.pop('generator_sha256'),\n                v3_generator=dict(path=str(Path(__file__)),sha256=sha(Path(__file__))),")
s=s.replace('excluded_if_universal_P1_matter=False',"excluded_if_universal_P1_matter=validated['clock']['P1_excluded']")
s=s.replace('excluded_if_universal_P2_independent_arm_light_modes=True',"excluded_if_universal_P2_independent_arm_light_modes=validated['clock']['P2_excluded']")
s=s.replace('row.update(excluded_if_universal=True',"row.update(excluded_if_universal=validated['clock']['unruh_g_excluded']")
s=s.replace('C1_LEITURAS_v2.json','C1_LEITURAS_v3.json')
# The previous replacements also touched the supersedes target; restore it explicitly.
s=s.replace("supersedes='C1_LEITURAS_v3.json',supersedes_sha256=sha(ROOT/'C1_LEITURAS_v3.json')", "supersedes='C1_LEITURAS_v2.json',supersedes_sha256=sha(ROOT/'C1_LEITURAS_v2.json')")
s=s.replace('C1_ADENDO_CORRECOES_013BIS.md','C1_ADENDO_CORRECOES_013BIS_v2.md')
s=s.replace('REAPROVEITAMENTO_C1.md','REAPROVEITAMENTO_C1_v2.md')
s=s.replace('refeito/measure_c1_013bis.py','refeito/measure_c1_013bis_v2.py')
s=s.replace("format(measured['P2_tau_star_bound_tP'],'.12g')+'.'", "format(measured['P2_tau_star_bound_tP'],'.12g')+'. Cota da série mediana, com margem de calibração; sem nível de confiança atribuído.'")
s=s.replace('ν=ω−mΩH','ν=ω_R−mΩH')
s=s.replace('Passo 2 [DERIVED condicional]: assumindo', 'κ=√(1−χ²)/[2t_M(1+√(1−χ²))] e ν=ω_R−mΩH têm unidade s⁻¹; −Im ω determina τ_GR separadamente. Passo 2 [DERIVED condicional]: assumindo')
s=s.replace('; o acesso à página editorial também falhou pela ferramenta web','; a página recebida não contém o artigo')
s=change(s,"'Recalculadas 264/264 linhas do CSV, inclusive as 99 linhas pequenas solicitadas. O contador de 132 inclui também as 33 linhas R-GLOBAL de efeito exatamente nulo.", "f\"Recalculadas {validated['checked']}/{validated['checked']} linhas do CSV, inclusive as {validated['small']} linhas pequenas solicitadas. O contador de {validated['sub_resolution']} inclui também as {validated['zero']} linhas R-GLOBAL de efeito exatamente nulo.")
s=s.replace("não uma segunda derivação independente de todas as leis.',",'não uma segunda derivação independente de todas as leis.\",')
s=s.replace('tgl_ringdown_prediction.py:18 (β em runtime), :47 (BCW), :64 (prediction), :108 (R-MOD)', 'tgl_ringdown_prediction.py:16 (β em runtime), :48 (BCW), :73 (prediction), :109 (R-MOD)')
s=change(s,"    assert original.read_bytes()==before","    require(original.read_bytes()==before,'Historical v1 changed')")
save('record_c1_013bis_v3.py',s)
print('Versioned scripts built, originals preserved')
