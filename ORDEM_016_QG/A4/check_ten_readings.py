"""Exact algebra for A4k.6; reads registration and never amends it."""
from pathlib import Path
from datetime import datetime, timezone
from statistics import NormalDist
import hashlib, json, math, sys, time
import sympy as sp

HERE=Path(__file__).resolve().parent
CHATGPT=HERE.parents[1]
INPUT=CHATGPT/'TUNEL/PARA_CHATGPT/ORDEM_016_INSUMOS'
RING=CHATGPT/'ORDEM_013_RINGDOWN'
start=time.perf_counter()
cpu=time.process_time()
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(path,raw):
    if isinstance(raw,str):raw=raw.encode('utf-8')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if path.exists():
        before=path.read_bytes();bak=path.with_name(path.name+'.bak_'+stamp)
        with bak.open('xb') as f:f.write(before)
        assert bak.read_bytes()==before
    tmp=path.with_name(path.name+'.tmp_'+stamp)
    with tmp.open('xb') as f:f.write(raw)
    assert raw and tmp.read_bytes()==raw
    tmp.replace(path)

paths=[INPUT/'ESTADO_RINGDOWN_LEITURAS.json',RING/'C1_LEITURAS_v4.json',RING/'RINGDOWN_5SIGMA_V1.json']
before={str(p):digest(p) for p in paths}
state,c1,reg=[json.loads(p.read_bytes()) for p in paths]
assert digest(paths[1])==state['fontes']['C1_LEITURAS_v4_sha256']
assert digest(paths[2])==state['fontes']['registro_V1_sha256']
assert len(state['leituras'])==len(c1['rows'])==len(reg['readings'])==10
source_rows={r['reading']:r for r in c1['rows']}
planning={r['reading']:r for r in reg['planning_targets'] if r['population']==state['populacao']}

beta,omega,kappa,tau,tP,tM,G,M,c,hbar,omega0,occupationMean,T,pathIntegral=sp.symbols(
    'beta omega kappa tau tP tM G M c hbar omega0 C_N T J_z',positive=True)
z=sp.symbols('z',nonnegative=True)
m,Omega=sp.symbols('m Omega',real=True)
period=2*sp.pi/kappa
canonical=beta*tau*omega**2/2
kms=canonical.subs(tau,period)
rootDen=(sp.sqrt(omega0+omega)+sp.sqrt(omega0))**2
laws={
 'R-A':beta*(1+z)*tP*omega**2/2,
 'R-B':beta*tM*omega**2/2,
 'R-MOD':sp.pi*beta*(omega-m*Omega)**2/kappa,
 'R-RAIZ-0':beta*omega/2,
 'R-RAIZ-EP4':beta*omega**2/(2*rootDen.subs(omega0,1/(4*tP*(1+z)))),
 'R-RAIZ-REST':beta*omega**2/(2*rootDen.subs(omega0,M*c**2/(hbar*(1+z)))),
 'R-RAIZ-COHERENT':beta*omega*occupationMean/2,
 'R-LIN':beta*omega,
 'R-GLOBAL':sp.Integer(0),
 'R-PROP':beta*tP*omega**2*pathIntegral/2,
}
checks={
 'nonrotating_R_MOD':sp.simplify(laws['R-MOD'].subs(Omega,0)-kms)==0,
 'corotating_gap_substitution':sp.simplify(kms.subs(omega,omega-m*Omega)-laws['R-MOD'])==0,
 'Schwarzschild_clock_ratio_8pi':sp.simplify(period.subs(kappa,c**3/(4*G*M))/(G*M/c**3)-8*sp.pi)==0,
 'R_B_frequency_conversion':sp.simplify((beta*sp.Symbol('w')**2/(2*tM)).subs(sp.Symbol('w'),omega*tM)-laws['R-B'])==0,
 'root_rationalization':sp.simplify((sp.sqrt(omega0+omega)-sp.sqrt(omega0))**2-omega**2/rootDen)==0,
 'source_detector_scaling':sp.simplify((beta*(1+z)*tau*(omega/(1+z))**2/2)-canonical/(1+z))==0,
 'KMS_period_frame_scaling':sp.simplify(period.subs(kappa,kappa/(1+z))-(1+z)*period)==0,
}
notes={
 'R-A':'Não por H_tauStar_eq_KMS_period sozinho: requer (1+z)tP=2pi/kappa no mesmo referencial.',
 'R-B':'Não: requer tM=2pi/kappa. No Schwarzschild o período é 8pi*tM; as taxas diferem por 8pi.',
 'R-MOD':'Sim sob Omega_H=0; em rotação requer substituir a frequência por omega-m*Omega_H e justificar fisicamente o gerador/coerência.',
 'R-RAIZ-0':'Não como função universal: coincidência pontual exige omega=kappa/(2pi), para beta,omega,kappa>0.',
 'R-RAIZ-EP4':'Não: relógio efetivo depende de omega0 e omega; exige 1/(sqrt(omega0+omega)+sqrt(omega0))^2=2pi/kappa.',
 'R-RAIZ-REST':'Não: mesma condição do offset, agora omega0=Msrc*c^2/(hbar*(1+z)); identificação de massa é hipótese adicional.',
 'R-RAIZ-COHERENT':'Não: C_N é esperança Poisson dependente da ocupação; exige C_N=2pi*omega/kappa. É inclinação inicial, não lei exponencial geral.',
 'R-LIN':'Não como função universal: coincidência pontual exige omega=kappa/pi.',
 'R-GLOBAL':'Não para beta,omega,kappa>0: a taxa relativa é zero sob a partição relacional declarada.',
 'R-PROP':'Objetos diferentes: Xi é expoente integrado, Gamma é taxa. Se comparados Xi e Gamma*T, seria preciso tP*J_z=(2pi/kappa)*T, além do modelo de propagação.',
}
rows=[]
for row in state['leituras']:
    name=row['leitura']; original=source_rows[name]; plan=planning[name]
    assert name in reg['readings']
    assert row['lei_ou_expoente']==original['rate_or_spectral_exponent']
    assert row['estatuto_do_relogio']==original['clock_status']
    assert row['excluded_if_universal']==original['excluded_if_universal']
    assert row['I_tau_alvo90']==plan['I_tau_expected_target90']
    assert row['N90_mistura_O4']==plan['N90_mixture_illustration_not_selection']
    info=row['I_tau_alvo90']; n90=row['N90_mistura_O4']
    fraction=None if info is None else state['I_atual_lido_da_ORDEM_015']/info
    ceiling=None if n90 is None else math.ceil(n90)
    if info is not None:
        assert math.isclose(fraction,row['fracao_do_alvo_hoje'],rel_tol=1e-13)
        assert ceiling==row['N90_mistura_O4_teto']
    denominator=kms*T if name=='R-PROP' else kms
    ratio=sp.simplify(laws[name]/denominator)
    rows.append(dict(reading=name,law_original=row['lei_ou_expoente'],
        law_sympy=str(laws[name]),ratio_to_kms_or_kms_times_T=str(ratio),
        conditional_comparison=notes[name],clock_statute=row['estatuto_do_relogio'],
        excluded_if_universal=row['excluded_if_universal'],
        exclusion_scope=original['exclusion_scope'],I90=info,N90=n90,N90_ceiling=ceiling,
        fraction=fraction,planning_only=True,systematic_gate_green=plan['systematic_gate_green']))

assert all(checks.values()),checks
p5=reg['statistics']['one_sided_p5'];k=state['k']
assert p5==state['p5_um_lado_do_registro'] and k==len(state['leituras_testaveis_com_alvo'])
normal=NormalDist();z5=-normal.inv_cdf(p5);zbonf=-normal.inv_cdf(p5/k);z90=normal.inv_cdf(.9)
factor=((zbonf+z90)/(z5+z90))**2
assert math.isclose(factor,state['fator_N_bonferroni_sobre_leitura_unica'],rel_tol=1e-9)
extremes=max(r['N90'] for r in rows if r['N90'])/min(r['N90'] for r in rows if r['N90'])
assert math.isclose(extremes,state['razao_N90_extremos'],rel_tol=1e-13)
assert before=={str(p):digest(p) for p in paths}
result=dict(status='DERIVED_EXACT_ALGEBRA_AND_HISTORICAL_PLANNING_RECHECK',
    at=datetime.now(timezone.utc).isoformat(),python=sys.executable,sympy_version=sp.__version__,
    script_sha256=digest(Path(__file__)),input_hashes=before,checks=checks,
    named_hypothesis='H_tauStar_eq_KMS_period',hypothesis_derived_here=False,
    selected_reading=None,rows=rows,statistics=dict(p5=p5,k=k,z5=z5,z_bonferroni=zbonf,z90=z90,
        bonferroni_N_factor=factor,N90_extreme_ratio=extremes,
        I_historical=state['I_atual_lido_da_ORDEM_015'],
        note='Targets copied from the unchanged registration and cross-checked, not new PE or power fit. '
             'A future single pre-registered reading can avoid this multiplicity penalty; no V1 amendment, no selection and no observed significance.'),
    elapsed_seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu,
    originals_unchanged=True,gate_changed=False)
save(HERE/'ten_readings_checked.json',json.dumps(result,ensure_ascii=False,indent=2))
text=['[DERIVED — álgebra exata; relógio físico OPEN; números históricos de planejamento]',
      '', '# Dez leituras sob H_tauStar_eq_KMS_period', '',
      'Hipótese: tauStar=2pi/kappa_H, no MESMO horizonte e referencial. Ela não é demonstrada pelo círculo.',
      'Beta permanece simbólico. C_N designa a esperança Poisson; J_z a integral de propagação.', '',
      '| Leitura | Lei original | Razão à taxa KMS (R-PROP: ao expoente Gamma*T) | Comparação |',
      '|---|---|---|---|']
for r in rows:text.append(f'| {r["reading"]} | `{r["law_original"]}` | `{r["ratio_to_kms_or_kms_times_T"]}` | {r["conditional_comparison"]} |')
text += ['', '| Leitura | Estatuto do relógio | Excluída se universal | I90 | N90 (teto) | 887/I90 |',
         '|---|---|---|---:|---:|---:|']
for r in rows:
    info='—' if r['I90'] is None else f'{r["I90"]:.6f}'
    n='—' if r['N90'] is None else f'{r["N90"]:.6f} ({r["N90_ceiling"]})'
    fraction='—' if r['fraction'] is None else f'{100*r["fraction"]:.6f}%'
    excluded='não informado agregado; ver partição' if r['excluded_if_universal'] is None else str(r['excluded_if_universal'])
    text.append(f'| {r["reading"]} | {r["clock_statute"]} | {excluded} | {info} | {n} | {fraction} |')
text += ['', f'Bonferroni: z(p5/4)={zbonf:.12f}; fator N90={factor:.12f}.',
         'Os N90 são o planejamento ilustrativo registrado, com sistemáticas ainda não liberadas; '
         'as frações não são sigmas nem probabilidade de confirmação. Nenhuma leitura foi escolhida.', '',
         '## Proveniência', '']
for p,h in before.items():text.append(f'- `{p}` — `{h}`')
save(HERE/'ten_readings_table.md','\n'.join(text)+'\n')
print(json.dumps(dict(checks=checks,rows=len(rows),factor=factor,extreme_ratio=extremes,
    elapsed_seconds=result['elapsed_seconds'],originals_unchanged=True),ensure_ascii=False))
