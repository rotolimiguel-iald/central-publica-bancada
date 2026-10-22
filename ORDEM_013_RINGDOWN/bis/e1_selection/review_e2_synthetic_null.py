"""Static/deterministic algebra audit only. Zero random draws, no MC execution."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import ast,hashlib,json,math,sys,types
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
B=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
source=B/'bis/e2_code/synthetic_null.py';raw=source.read_bytes();tree=ast.parse(raw.decode())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(x,msg):
    if not x:raise ValueError(msg)
def new(p,b):
    with p.open('xb') as f:f.write(b)
doc=B/'bis/E2_SYNTHETIC_NULL_REVIEW.md';output=O/'E2_SYNTHETIC_NULL_CONTROLS.json'
require(not doc.exists() and not output.exists(),'Review output exists')
for path,pin in [(B.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_B1_portao_e_nuisance.md','c33f4f36eedc9060859ae38bdd3f9993b59fada62cee489e8c964975b792a3e8'),(B/'NUISANCE_V1.json','83f860bbfa904c0048005c8b0f1b367814032052f352e780af7d77ed1f257b85')]:
    require(sha(path)==pin,'B1 seal mismatch')
nu=json.loads((B/'NUISANCE_V1.json').read_bytes())
ns={'np':np};functions=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
exec(compile(ast.Module(body=[n for n in functions if n.name=='projected_components'],type_ignores=[]),str(source),'exec',optimize=1),ns)
delta=np.array([-.018,-.021,-.025,-.023,-.016]);sigma=np.array([.04,.08,.11,.16,.25]);X=np.column_stack((np.ones(5),sigma))
V0=np.array(nu['synthetic_E2_nuisance_INPUT']['sigma_model']['covariance'])
fixtures=[('zero',np.zeros((2,2))),('sealed_local_cov_INPUT',V0),('rank_one',np.array([[.002,.004],[.004,.008]])),('diagonal',np.diag([.003,.02]))]
checks=[]
for name,V in fixtures:
    got=ns['projected_components'](delta,sigma,X,V)
    C=np.diag(sigma*sigma)+X@V@X.T
    solved=np.linalg.solve(C,delta);information=float(delta@solved);w=solved/math.sqrt(information)
    exact={'noise_variance_fraction':float(w@np.diag(sigma*sigma)@w),'nuisance_variance_fraction':float(w@X@V@X.T@w),'signal_information_with_nuisance':information,'max_squared_signal_fraction':float(max((w*delta)**2)/sum((w*delta)**2))}
    errors={k:abs(v-exact[k]) for k,v in got.items()}
    require(max(errors.values())<1e-10,'Dense/Woodbury disagreement')
    checks.append({'fixture':name,'production_AST_values':got,'dense_oracle_values':exact,'max_abs_error':max(errors.values()),'X_transpose_w':(X.T@w).tolist()})
negatives=[]
def rejected(label,fn):
    try:fn()
    except ValueError:negatives.append(label)
    else:raise ValueError('Mutation not rejected '+label)
rejected('nonpositive sigma',lambda:ns['projected_components'](delta,sigma*0,X,V0))
rejected('nonfinite delta',lambda:ns['projected_components'](delta*np.nan,sigma,X,V0))
rejected('nonPSD covariance',lambda:ns['projected_components'](delta,sigma,X,-np.eye(2)))
rejected('asymmetric covariance',lambda:ns['projected_components'](delta,sigma,X,np.array([[1.,.1],[.2,1.]])))
rejected('zero signal',lambda:ns['projected_components'](delta*0,sigma,X,V0))
# Only execute the actual validation prefix, stopping BEFORE any RNG construction.
simulation=next(n for n in functions if n.name=='simulate_projection')
prefix=[]
for statement in simulation.body:
    if isinstance(statement,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='rng' for t in statement.targets):break
    prefix.append(statement)
prefix.append(ast.Return(value=ast.Constant(True)))
prefix_node=ast.FunctionDef(name='validation_prefix',args=simulation.args,body=prefix,decorator_list=[])
exec(compile(ast.fix_missing_locations(ast.Module(body=[prefix_node],type_ignores=[])),str(source),'exec',optimize=1),ns)
base={'noise_variance_fraction':.7,'nuisance_variance_fraction':.3}
unguarded={}
for label,kw in [('draws1',{'draws':1}),('zero_chunk',{'chunk':0}),('negative_chunk',{'chunk':-1}),('fractional_chunk',{'chunk':.5}),('entropy_seed_None',{'seed':None})]:
    args={'components':base,'draws':10,'seed':123,'model':'gaussian','time_guard':lambda:None,'chunk':4};args.update(kw)
    unguarded[label]=ns['validation_prefix'](**args)
require(all(unguarded.values()),'Unexpected changed validation')
# Deterministic state transition for chunk0: n=0 and used never increments; do not execute loop.
require(min(0,10)==0,'chunk0 reasoning')
require(any(isinstance(n,ast.BinOp) and isinstance(n.op,ast.Div) and ast.unparse(n.right)=='used - 1' for n in ast.walk(simulation)),'ddof1 denominator locator')
binfn=next(n for n in functions if n.name=='binomial_result')
require('alpha' not in ast.unparse(binfn.body[0].test),'alpha currently lacks validation')
# No beta quantile/production binomial execution; exact analytic zero-success upper bound.
p5=.5*math.erfc(5/math.sqrt(2));theta=math.atan(5/math.sqrt(3))
t5tail=(8/(3*math.pi))*(3*(math.pi/2-theta)/8-math.sin(2*theta)/4-math.sin(4*theta)/32)
tails={'Gaussian_one_sided_Z_gt5':p5,'Gaussian_100million_expected_exceedances':1e8*p5,'Gaussian_100million_relative_binomial_SE':math.sqrt((1-p5)/(1e8*p5)),
    'zero_successes_one_sided95_upper_1million':-math.expm1(math.log(.05)/1e6),
    'zero_successes_one_sided95_upper_100million':-math.expm1(math.log(.05)/1e8),
    'minimum_trials_if_zero_successes_to_upper95_below_Gaussian_p5':math.ceil(math.log(.05)/math.log1p(-p5)),
    'unit_variance_t5_measurement_only_Z_gt5':t5tail,
    'formula_t5':'T=G*sqrt(3/U5), unit variance. Direct closed-form integral of t5 density, no sampling.',
    'one_million_scope':'Zero successes still has upper95 > p5; cannot certify five-sigma tail empirically.'}
result={'status':'GAUSSIAN_ALGEBRA_PASS__SCOPE_AND_GUARD_CORRECTIONS_BEFORE_CAMPAIGN','utc':datetime.now(timezone.utc).isoformat(),'code_under_review_sha256':sha(source),'code_under_review_bytes':len(raw),'review_code_sha256':sha(Path(__file__)),'optimize':sys.flags.optimize,
    'dense_vs_Woodbury_fixtures':checks,'rejected_projection_mutations':negatives,'validation_prefix_accepts_invalid_execution_inputs':unguarded,'analytic_tail_controls':tails,
    'MC_draws_generated':0,'full_simulate_projection_called':False,'production_imported':False,'prior_covariance_statute':nu['synthetic_E2_nuisance_INPUT']['status'],
    'findings':[{'id':'E2-SN-R1','priority':'P2','kind':'model description','detail':'Current t5 acts on measurement noise only; nuisance Gaussian term independent. Full scalar is t5-plus-normal convolution, not a full-covariance elliptical t5 when nuisance_fraction>0. Register exact generative equation and name.'},
    {'id':'E2-SN-R2','priority':'P2','kind':'execution guard','detail':'Before RNG require draws>=2, positive integer chunk, fixed integer seed (no bool/None), callable guard, finite fractions and valid alpha. chunk0 does not progress; draws1 ends in division byzero after draws. CI labels hardcode95 although alpha public.'}],
    'no_campaign_authorization':'User requires E2 registration and new explicit order; none executed','input_source_unchanged':sha(source)==hashlib.sha256(raw).hexdigest()}
new(output,(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
md=f'''# E2 — revisão independente de synthetic_null.py

[REAL — álgebra determinística/AST; INPUT — covariance e modelo sintético; OPEN — calibração física]

**Álgebra gaussiana aprovada no modelo declarado; corrigir R1/R2 antes da campanha. Nenhum Monte Carlo executado.** Arquivo examinado SHA256 `{sha(source)}`, {len(raw)} bytes. Os hashes B1 e NUISANCE_V1 conferem com os comunicados. O censo e o adendoGR para E2 já estão em `bis/e1_selection/CALIBRATION_AND_CANDIDATE_CENSUS.*` e `GR_O4A_ADENDO.*`: calibração33+18−12=39, O4b13 candidatos elegíveis ausentes do corpus; O4a10 adicionais, sem afirmar ausência universal/cegamento.

## Gaussian exact marginal e significado de projected GLS

Se D=diag(σ_i²), η∼N(0,V) e ε∼N(0,D) são independentes, o resíduo centrado r=Xη+ε tem C=D+XVXᵀ. Para sinal fixo δ, I=δᵀC⁻¹δ e w=C⁻¹δ/√I dão Z=wᵀr∼N(0,1). O código implementa C⁻¹δ por Woodbury, inclusive V semidefinida/singular, sem inverter V. As frações a=wᵀDw e b=wᵀXVXᵀw somam1. Quatro matrizes determinísticas comparadas com solução densa independente passaram (erro absoluto máximo {max(c['max_abs_error'] for c in checks):.3g}); cinco entradas inválidas foram recusadas sob−O.

Isso é **marginalização gaussiana de nuisance aleatório com V fixada**, não projeção que elimina intercepto/slope arbitrários: Xᵀw em geral não zera. Se a média de nuisance é a estimativa c0,k, o resíduo observado deve subtrair X·média registrada; η representa sua perturbação centrada. Reajustar nuisance ao catálogo de teste ou chamar isso de perfil GLS irrestrito mudaria a estatística e exigiria outra calibração.

O NUISANCE selado marca V como **INPUT da curvatura local gaussiana apenas para nulo sintético**, não covariance fisicamente calibrada. O enunciado normal exato é condicional a D,X,V e δ congelados: não inclui seleção, incerteza de σ, estimação de V, correlação com dados usados para estimá-la, banda KDE ou erro de waveform. O campo `max_squared_signal_fraction` é diagnóstico específico de(w_iδ_i)²; não é por si só número efetivo de eventos nem a participação de Fisher aditiva com correlação.

## E2-SN-R1 — P2: declarar exatamente onde atua a escala t5

O ramo atual simula **Z=√a·G·√(3/U₅)+√b·H**, com G,H∼N(0,1) e U₅∼χ²₅ independentes. É a projeção exata de **ruído de medição t5 elíptico com uma escala compartilhada por catálogo**, somado a nuisance gaussiano independente. Não são t_i independentes por evento; cada entrada do array representa um catálogo inteiro. O fator3 (ν−2) mantém variância1 do ruído padronizado. A convenção de escala da t está na [documentação primária SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html).

**Com b>0, o vetor total não é, em geral, uma t5 elíptica de covariance C; Z é convolução t5+normal.** Uma única escala aplicada ao catálogo inteiro, inclusive nuisance, seria Z=(√a G+√b H)√(3/U₅), outra lei e outra cauda. Shape e covariance tampouco são sinônimos: para t5 de covariance C, shape=(3/5)C. [Definição multivariada](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.multivariate_t.html).

Correção exata recomendada, preservando as contas pretendidas: renomear/declarar o controle como `elliptical_t5_measurement_plus_gaussian_nuisance`, registrar a equação acima, ν=5, unidade de uma escala por catálogo e independência do nuisance. O cabeçalho atual “multivariate elliptical Student t model” precisa desse qualificador; não anunciar t5 de toda C. Se o registro optar pela escala também no nuisance, será mudança de modelo explícita, não mera renomeação.

## E2-SN-R2 — P2: guardas antes do RNG e confiança do recibo

O prefixo real de validação, extraído por AST e encerrado **antes** de construir RNG, aceita `draws=1`, `chunk=0`, `chunk<0`, `chunk=0.5` e `seed=None`. Nenhum draw foi gerado para demonstrar isso. Com chunk0, n=0/used=0 a cada volta: a rotina não progride até eventual recusa do time_guard. Com draws1, o retorno divide por used−1=0 depois de gastar o draw. SeedNone escolhe entropia externa e não assegura replay pelo recibo. O código também não valida α; nomes `one_sided_upper95`/`central95` permanecem95 mesmo quando α≠0,05.

Correção ao lado: exigir antes do RNG inteiros não booleanos `draws≥2`, `chunk≥1`, seed inteiro não negativo e `time_guard` callable; componentes finitos, não negativos e soma1 na tolerância registrada. Em binomial_result exigir α finito em(0,1), inteiros não booleanos k,n e publicar `confidence_level=1−alpha` com nomes genéricos, ou restringir explicitamente α=0,05. Testar recusas sob−O com RNG que lança se alcançado; zero draws nas negativas. Isso não exige campanha.

## Planejamento100M+100M e rotaIV separada

No gaussiano, P(Z>5)={p5:.12g};100 milhões geram em média {1e8*p5:.6f} excedências, com EP relativo aproximadamente {100*tails['Gaussian_100million_relative_binomial_SE']:.2f}%. É resolução útil para conferir a cauda dentro do modelo, sem alta precisão relativa. O Clopper–Pearson usado por quantis beta é a fórmula correta para contagens IID; sobα=0,05, distingue limite superior unilateral e intervalo central. Não é banda simultânea sobre todas as leituras/modelos. Se o critério exigir upper95≤p5 no próprio limiar teórico5, a aprovação não ocorre normalmente quando p verdadeiro=p5: registrar o critério antes de contar, sem ajustá-lo ao resultado.

No controle de medição t5 puro (b=0), a integral analítica dá P(Z>5)={t5tail:.12g}, muito acima do normal. Isso é consequência do INPUT não gaussiano, não falha da implementação nem “cinco sigma” físico. Com nuisance gaussiano, a cauda depende de a,b. A projeção reduzida é válida para esse modelo compartilhado; não reproduz uma população de t_i independentes ou catálogos que reestimem a covariance em cada realização.

**O nulo heterogêneo da rotaIV é outro ensaio:** µ perfilado, variância intrínseca≥0 e LRT>25. `synthetic_null.py` não implementa essa estatística; não transportar os100M escalares para seu recibo. O milhão planejado deve rodar a implementação separada pinada, com σ_i/população/µ/nuisance/sigma_sys e seeds registrados, reportando k, N e limite empírico. Se k=0 em1M, upper95=1−0,05^(1/N)={tails['zero_successes_one_sided95_upper_1million']:.12g}, **maior** que p5; nem zero falsos positivos certifica cauda5σ com esse tamanho. Seriam necessários ao menos {tails['minimum_trials_if_zero_successes_to_upper95_below_Gaussian_p5']:,} draws sem excedência para esse limite unilateral ficar abaixo de p5. LRT25 não é5σ sem calibração; não assumir Wilks com parâmetro de variância na borda e heterogeneidade.

O módulo não contém sozinho o agendamento100M/100M, o runner do milhão rotaIV, as seeds/células ou o recibo E2. Esses números permanecem **planejados, não executados/verificados como campanha**. O registro deve fixar unilateralidade/direção, tratamento de várias leituras e covariance INPUT; o wrapper autorizado deve verificar os pins antes de qualquer chamada. A leitura pontual de registration_guard/run_controlled não constituiu auditoria integral da árvore PE.

**Não autorizado aqui executar MC:** aguardar registro E2 e a ordem explícita solicitada pelo usuário. Sem PE, posterior novo, strain, waveform, alteração do código examinado ou de resultados selados.

Controle determinístico: `bis/e1_selection/review_e2_synthetic_null.py`; recibo `E2_SYNTHETIC_NULL_CONTROLS.json`. Zero chamadas a simulate_projection completo, zero RNG, zero Monte Carlo. Axiomas N/A.
'''
new(doc,md.encode());require(sha(source)==hashlib.sha256(raw).hexdigest(),'Production source changed during review')
print(json.dumps({'findings':result['findings'],'max_dense_error':max(c['max_abs_error'] for c in checks),'tails':tails,'MC_draws':0}))
