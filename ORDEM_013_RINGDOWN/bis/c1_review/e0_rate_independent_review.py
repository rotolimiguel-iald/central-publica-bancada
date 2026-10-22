"""Read-only arithmetic review of rate scenarios; pure-Python Poisson inversion."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,time
B=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((B/p).read_bytes())
def require(x,m):
    if not x:raise ValueError(m)
def equal(x,y,m):require(math.isclose(x,y,rel_tol=5e-12,abs_tol=1e-300),m)
def cdf(n,mean):
    term=math.exp(-mean);terms=[term]
    for k in range(1,n+1):term*=mean/k;terms.append(term)
    return math.fsum(terms)
def solve_mean(n,target):
    lo,hi=0.,100.
    for _ in range(64):
        mid=(lo+hi)/2
        if cdf(n,mid)>target:lo=mid
        else:hi=mid
    return (lo+hi)/2
def poisson_interval(n,t):
    require(type(n)is int and n>=0 and math.isfinite(t) and t>0,'Invalid count/exposure')
    return [solve_mean(n-1,.95)/t if n else 0.,solve_mean(n,.05)/t]

start=time.perf_counter()
path='bis/E0_RATE_O5_SCENARIOS.json';code='refeito/e0_rate_and_o5_scenarios_013bis.py';d=read(path)
for p,h in d['sources'].items():require(sha(B/p)==h,'Source hash '+p)
require(sha(B/code)==d['code_sha256'],'Code hash')
inv=read('bis/e0_metadata/GWOSC_INVENTORY.json');core=read('bis/e0_core/E0_CORE.json');fit=read('bis/E0_SNR_INFORMATION_FIT.json')
runs=read('cache/e0_metadata/gwosc_runs.json')['results'];sc=read('bis/e0_metadata/SCENARIOS_AND_SCHEDULES.json')['o5_gain']
periods=[r for r in runs if r['name'] in ['O4a','O4b']]
require(len(periods)==2 and d['source_intervals']==periods,'Intervals')
seconds=sum(r['gps_end']-r['gps_start'] for r in periods);years=seconds/31557600
expected_rare={r['event'] for r in inv['events'] if r['run'] in ['O4a','O4b'] and r['network_matched_filter_snr'] is not None and r['network_matched_filter_snr']>=78}
rs=next(r['rows'] for r in fit['fits'] if r['population']=='GWTC5_31');expected_cal={r['event'] for r in rs if r['run'] in ['O4a','O4b']}
require(len(expected_rare)==1 and len(expected_cal)==21,'Observed metadata populations')
poisson_checks=[]
for n,(rate,t) in enumerate(zip(d['rates'],[1.45,years])):
    equal(rate['exposure']['years'],t,'Exposure')
    require(set(rate['rare_events'])==expected_rare,'Rare set')
    require(set(rate['calibration_events'])==expected_cal and len(rate['calibration_events'])==21,'Calibration set')
    for key,count in [('rare_SNR_ge78',1),('calibration_O4_subset',21)]:
        x=rate[key];require(x['N']==count,'N');equal(x['rate_mle_per_year'],count/t,'Rate')
        ci=poisson_interval(count,t)
        for a,z in zip(ci,x['rate_CI90_per_year']):equal(a,z,'Poisson CI')
        poisson_checks.append(dict(exposure_years=t,count=count,rate=count/t,ci90_independent=ci))
gains=dict(O5_BBH_LOW=2500/1600,O5_BBH_HIGH=2500/1400,O5_C5_PSD=sc['c5_ratio'],BNS_ONLY_UPPER_CONTROL=330/160)
comb=core['combinations']['GWTC5_31']['std_ddof1'];readings=set(comb)-{'GR_FALSE_FALSIFIER'}
require(len(readings)==10 and len(d['forecasts'])==80,'10 readings x4 x2')
seen=set();summary=[]
for f in d['forecasts']:
    key=(f['exposure_status'],f['gain_label'],f['reading']);require(key not in seen,'Duplicate scenario');seen.add(key)
    require(f['reading'] in readings and f['gain_label'] in gains,'Unknown scenario')
    g=gains[f['gain_label']];equal(g,f['gain'],'Gain')
    rate=next(r for r in d['rates'] if r['exposure']['status']==f['exposure_status']);t=rate['exposure']['years']
    c=comb[f['reading']];expected=3*21/t*g**3;ci=[x*3*g**3 for x in poisson_interval(21,t)]
    equal(f['count_expected_3_scenario_years'],expected,'Expected count')
    for a,z in zip(f['count_CI90_from_Poisson_rate'],ci):equal(a,z,'Count rate CI')
    if c['z_comb'] is None:
        require(all(f[k] is None for k in ['z_optimistic_same_source_quality_plus_volume','z_optimistic_CI90_rate_only','z_detection_threshold_quality_invariant_control']),'Null z transport')
    else:
        z=c['z_comb'];n=c['N_events']
        equal(f['z_optimistic_same_source_quality_plus_volume'],math.sqrt(z*z/n*expected*g*g),'Optimistic z')
        equal(f['z_detection_threshold_quality_invariant_control'],math.sqrt(z*z/n*expected),'Rate-only z')
        for a,x in zip(f['z_optimistic_CI90_rate_only'],ci):equal(a,z*g*math.sqrt(x/n),'z rate band')
    operational=c.get('delta_weighted') is not None and abs(c['delta_weighted'])>=1e-12
    if operational and c['N90'] is not None:equal(f['N90_at_fixed_source_improved_sigma'],c['N90']/g**2,'N90 scaling')
    else:require(f['N90_at_fixed_source_improved_sigma'] is None,'Null N90')
    require(f['operational_information_target']==(c['I_tau_target90'] if operational else None),'Information target')
    require(f['systematic_gate']=='NOT_CALIBRATED_RED' and f['test_verdict'] is None,'Scope gate')
    if f['reading']==sorted(readings)[0]:summary.append(dict(exposure=rate['exposure']['status'],gain_label=f['gain_label'],gain=g,expected_count_3years=expected,CI90_on_mean_count=ci))
require(seen=={(r['exposure']['status'],g,k) for r in d['rates'] for g in gains for k in readings},'Full Cartesian coverage')
zero=poisson_interval(0,1);equal(zero[1],-math.log(.05),'Zero count')
neg=[]
for n,t in [(-1,1),(1,0),(1,float('nan'))]:
    try:poisson_interval(n,t)
    except ValueError:neg.append(dict(case=str((n,t)),rejected=True))
    else:raise ValueError('Own guard failure')
result=dict(status='PASS_ARITHMETIC_AND_DECLARED_SCOPE__NOT_PHYSICAL_FORECAST_APPROVAL',utc=datetime.now(timezone.utc).isoformat(),
    sources={**d['sources'],path:sha(B/path),code:sha(B/code)},code_sha256=sha(Path(__file__)),threads=1,elapsed_s=time.perf_counter()-start,
    archive_seconds=seconds,archive_days=seconds/86400,archive_years=years,nominal_years=1.45,
    nominal_relative_rate_over_archive=years/1.45-1,poisson_checks=poisson_checks,zero_count_ci90=zero,
    own_negative_checks=neg,forecast_rows_checked=len(seen),reading_count=len(readings),count_summaries=summary,
    no_OLS_or_MC_or_Fisher_rerun=True)
p=B/'bis/c1_review/e0_rate_independent_results.json'
with p.open('xb') as f:f.write((json.dumps(result,indent=2,allow_nan=False)+'\n').encode())
lines=['| exposição | N | taxa/ano | IC90 da taxa |','|---|---:|---:|---|']
for x in poisson_checks:lines.append(f"| {x['exposure_years']:.9f} anos | {x['count']} | {x['rate']:.9f} | [{x['ci90_independent'][0]:.9f}, {x['ci90_independent'][1]:.9f}] |")
doc=f'''# E0 — revisão independente das taxas e cenários O5

[REAL de contas leves; cenários INPUT/DERIVED; NÃO-CEGO]

UTC {result['utc']}. **Sem erro aritmético ou bloqueante novo encontrado no recorte solicitado.** As ressalvas presentes impedem tratar as projeções como taxa observacional corrigida, previsão física aceita ou data de alcance5σ. Conferi hashes das cinco entradas/código, intervalos e conjuntos, Poisson e todas as80 linhas (dez leituras × quatro fatores × duas exposições), sem executar o builder, refazer OLS, MC, Fisher ou PE. Controle próprio: {result['elapsed_s']:.4f}s, uma thread.

## Poisson e exposição

Reobtive os limites centrais Garwood90% por **inversão direta da CDF Poisson**, sem usar os quantis chi-quadrado do construtor. Para N>0: CDF(N−1,lambda_lo)=0,95; CDF(N,lambda_hi)=0,05; divide-se por T. Para N=0: [0,−ln(0,05)/T]. Essa é inferência sobre taxa com exposição tratada como conhecida, compatível com a definição de [intervalo de taxa Poisson](https://www.stat.math.ethz.ch/R-manual/R-patched/RHOME/library/stats/html/poisson.test.html).

{chr(10).join(lines)}

O conjunto raro tem1 evento, GW250114_082203, pelo corte SNR_GWOSC≥78 em O4a+b; não inclui a discovery O4c. Isso não certifica larguraδτ=0,058 para qualquer evento de mesma SNR. O conjunto calibrador contém21 eventos O4 dentre os31 produtos históricos; conferi todos os nomes com as linhas do fit e o inventário.

A soma GPS é **{seconds} s = {seconds/86400:.9f} dias = {years:.12f} anos julianos**, contra o INPUT nominal1,45. O uso de1,45 eleva as taxas em **{(years/1.45-1)*100:.6f}%** relativamente ao denominador GPS. As duas alternativas estão identificadas corretamente. Limites de arquivo podem incluir engineering e **não são live time**. Poisson estacionário para esse universo publicado é hipótese; falta função de seleção/exposição efetiva para inferir taxa física. Não se adicionou O4c ao numerador com denominador O4a+b.

## Ganhos, qualidade e volume

As contas usam g=2500/1600, 2500/1400, fator C5 arquivado e330/160. O5_C5_PSD continua um resultado de fonte/projeção e PSD individual, não fator medido de toda a população. BNS_ONLY_UPPER_CONTROL está explicitamente marcado como **controle, não forecast BBH**. Os três anos são duração de cenário, sem data de início prometida.

N_esperado=3 R g³ e banda=3 IC(R) g³ conferem. `count_CI90_from_Poisson_rate` é intervalo para a **média esperada** induzido pela incerteza da taxa: não é intervalo preditivo para a futura contagem, nem inclui incerteza em g, seleção, duty cycle ou população.

O cenário otimista dá z=z_base g sqrt(N_esperado/31), assumindo tanto volume g³ quanto qualidade das novas fontes igual à qualidade melhorada de fontes fixas. A hipótese forte está escrita no próprio JSON; não é uma identidade física. O controle de qualidade invariante retira o fator g de z e representa o caso idealizado em que mais detecções vêm de fontes mais distantes, junto ao limiar. As duas expressões conferem. Não aplicar novamente g aos números já escalados. N90/g² é diagnóstico do cenário de fonte fixa, não o N90 heteroscedástico da rotaIV MC.

As dez leituras estão presentes; R-RAIZ-COHERENT e R-PROP mantêm z/N90 nulos, R-GLOBAL mantém z0/N90null, e os regimes pequenos mantêm o diagnóstico sub-resolução via N90 operacional nulo. Nenhuma leitura escolhida, nenhum test_verdict preenchido, todos os gates permanecem NOT_CALIBRATED_RED. `operational_information_target` é transportado do core, cuja hipótese de efeito/população precisa acompanhar o uso.

## Cuidados de transporte documental, sem novo bloqueio

1. As projeções usam a mistura de qualidade das31 fontes, mas a taxa das21 O4. Isso está declarado; não rotular tudo “amostra O4 homogênea”. As larguras calibradoras não podem virar inclusão de eventos de teste.
2. Na ficha pública conservar a origem **calibração com offset zero PROIBIDA_COMO_TESTE**, que está no core e não reaparece literalmente em cada linha de forecast. Os z são diagnósticos de separação com sistemáticas ainda abertas, não significância observada.
3. Conservar os estatutos próprios das leituras, especialmente R-MOD conjectural e os nulos sem observável único. O gate genérico vermelho não substitui esse contexto.
4. Não usar a coluna com tetoBNS para anunciar BBH, nem as bandas da taxa como previsão de contagem realizada. Não há integração da incerteza do fit sigma(SNR) neste escalonamento; tampouco é afirmada.

Este parecer fecha a revisão **das contas e dos escopos declarados neste artefato**, não o portão E0.7 inteiro. SYSTEMATICS_ADENDO é revisão distinta; E1 não foi executado por mim nem pressuposto aqui. CritérioMf/chi_f continua no rascunho separado aguardando revisão do principal.

## Custódia

Artefato: `{sha(B/path)}`. Builder lido: `{sha(B/code)}`. Controle independente: `{sha(Path(__file__))}`. Resultado: `{sha(p)}`. Hashes de cada entrada e contas em `bis/c1_review/e0_rate_independent_results.json`. Nenhum arquivo de produção alterado.
'''
target=B/'bis/E0_RATE_O5_INDEPENDENT_REVIEW.md'
with target.open('xb') as f:f.write(doc.encode())
print(json.dumps(dict(report=str(target),report_sha256=sha(target),rows=len(seen),archive_years=years,poisson=poisson_checks)))
