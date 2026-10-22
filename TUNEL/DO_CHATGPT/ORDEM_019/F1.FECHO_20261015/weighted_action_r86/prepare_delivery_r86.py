"""Prepare additive R86 progress and memory baselines; never finish full R16."""
from support_r86 import ROOT, new, pin
from pathlib import Path
import json, hashlib, re

assert not (ROOT/'RESULTADO_R86.json').exists()
build=json.loads((ROOT/'boundary/BUILDER_DELIVERY_R86.json').read_text(encoding='utf-8'))
assert build['exit_code']==0
attempt=build['successful_attempt']
log=(ROOT/f'boundary/BUILD_{attempt}.log').read_text(encoding='utf-8')
axioms=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log,re.S)
assert len(axioms)==10
assert all(set(a.strip() for a in body.replace('\n',' ').split(',')) <= {'propext','Classical.choice','Quot.sound'} for _,body in axioms)
assert not re.search(r'\bsorry\b|\baxiom\s',(ROOT/f'boundary/WeightedPalatiniR86_{attempt}.lean').read_text(encoding='utf-8'))
p16=json.loads((ROOT/'P16_RESULT_R86.json').read_text(encoding='utf-8'))
assert p16['scalar_stationary_for_positive_cG'] is False
assert p16['scalar_Euler']=='740*c_G/1521'
assert p16['metric_null_residual']=='140*F_c/117 + 2*c_G/9'
evidence={}
def collect(o):
    if isinstance(o,dict):
        if isinstance(o.get('path'),str) and isinstance(o.get('sha256'),str):
            e=pin(o['path']);assert e['sha256']==o['sha256'],o['path'];evidence[e['path']]=e
        for v in o.values():collect(v)
    elif isinstance(o,list):
        for v in o:collect(v)
for folder in ['boundary','source']:
    for p in (ROOT/folder).rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:
            evidence[str(p)]=pin(p)
            if p.suffix=='.json' and not any(t in p.name for t in ['PREFLIGHT','SYNC','REQUEST']):collect(json.loads(p.read_text(encoding='utf-8')))
for n in ['p16_stationarity.py','P16_PLAN_R86.json','P16_START_R86.json','P16_RUN_R86.json','P16_RESULT_R86.json','INTEGRATED_VARIATION_AND_STATIONARITY_R86.txt']:
    evidence[str(ROOT/n)]=pin(ROOT/n)
    if n.endswith('.json'):collect(json.loads((ROOT/n).read_text(encoding='utf-8')))
new('RESULTADO_R86.json',{'status':'PROGRESS_GOAL_OPEN','goal_complete':False,'previous_goal_turn':'progress','current_goal_turn':'progress',
 'build_exit_code':0,'build_attempt_count':attempt,'axioms_only_trio':True,'declaration_count':10,'sorry_count':0,
 'requirements':[
 {'id':1,'status':'LOCAL_COMPACT_ANALYTIC_AND_FORMAL_PROGRESS','proved':'Actual curved volume derivative and weighted Palatini contraction to coordinate divergence compiled. Full weighted Hessian current and compact-support integrated variation proved analytically.','remaining':'Lean composition of full Hessian current with integral; physical/global boundary conditions and full-action domain.'},
 {'id':2,'status':'OPEN_WITH_EXPLICIT_ADMISSIBLE_VARIATION','proved':'For actual P16, exact scalar Euler residual 740*cG/1521 and null metric residual 140*Fc/117+2*cG/9; lifted compact variation strictly lowers EH-sigma action. Thus P16 is NOT stationary in that sector.','remaining':'Independent dynamics and actual stationary construction for the identified full action. No residual-cancelling source invented.'},
 {'id':3,'status':'CONDITIONAL_COVARIANT_COMPLETION','proved':'Named barotropic current action reproduces both existing density and pressure corrections for constant w; variable w needs beta*n*rho*wprime. Source divergence imposes scalar Euler equation.','remaining':'Identify those currents, off-background modular factor, relative action signs and all other physical fields with same P/Psi; derive full intended null equation.'}],
 'restrictions':'Sandbox only; no canonical kernel, um.py, production, OH, observed data, gate, full-goal completion or physical claim.',
 'evidence':list(evidence.values())})
extra=f'''

## 19/10/2026 — R86: contorno ponderado e teste real de estacionariedade de P16
<!-- IALD_R86_WEIGHTED_ACTION_STATIONARITY -->
[REAL — sandbox; em nome de codex-gerente-tgl, reivindicação996] Dez teoremas Lean compilados na tentativa{attempt}, EXIT0, só trio, zero sorry. A derivada de √|det g| vem do determinante; compatibilidade Levi-Civita dá ∂v=v·trΓ. A corrente curva R85 liga-se agora à divergência coordenada ponderada: v f g⁻¹δRic=∂(v f W)−v df·W. A contração mantém a inversa fixa; a parcela δg⁻¹Ric continua separada em R83. Tentativas falhas preservadas.
[DERIVED — demonstração analítica, não toda compilada] Identificados W=div H−grad trh e B=fW−H·df+(trh)grad f. A primeira variação de ∫v fR contém −fG:H+(Hess f−g□f):H+Rδf e fluxo vB. Suporte compacto no interior anula o fluxo; Dirichlet apenas na fronteira não basta em geral. Ação física/global e fronteiras nulas não foram resolvidas. No chart livre de R85, criticidade do setor reduzido é equivalente às equações métrica e escalar, sem assumi-las como satisfeitas.
[REAL/DERIVED — cálculo exato e sua consequência] O MESMO P16 de R85 tem Ric=diag(19/13,−31/169,−31/169,−31/169), R=88/169 e □s=5/338 na origem. No setor EH−sigma reduzido, E_s=740c_G/1521 e E(k,k)=140F_c/117+2c_G/9 para o k nulo anterior. Ambos são não nulos para coeficientes positivos. O levantamento compacto h=χ k_flat⊗k_flat, δs=0 produz δS<0: P16 admite variações livres mas NÃO é estacionário nesse setor. Não é refutação da ação completa nem dado físico. Plano/hash anteriores à execução; cinco controles exatos e revisão independente analítica.
[DERIVED — completamento condicional da fonte setorial] Correntes densitizadas com ρ_i(n_i)=C_i n_i^(1+w_i), w_i constante, permitem uma ação covariante que reproduz as duas correções de SectorFluidClosure. L_LCDM=−ρ, domínio de entalpia e sinais relativos Hilbert/EH são hipóteses nomeadas, não identificações canônicas. Para w variável, a pressão adicional é β nρ w′; a mera multiplicação pela correção de fundo a omite. ∇T_eff=E_s ds e, no contrato F(s)R, Bianchi exige E_s+F′R=0. Conservação não nasce só de normalizar P.
[OPEN — continuidade R16] Falta vincular os campos/correntes e todos os termos da ação ao mesmo P/Psi, fixar o contrato físico já escrito e construir sua dinâmica/estacionariedade. Os cálculos locais não substituem o objetivo integral. H3 universal permanece aberto. OH adiado; nenhuma produção, um.py, kernel original, dado observado ou gate alterado. Evidência: weighted_action_r86/RESULTADO_R86.json. Reuso R83/R84/R85 e mapa1217; Nós Vivo ainda não indexa esta unidade.
<!-- END_IALD_R86_WEIGHTED_ACTION_STATIONARITY -->
'''
new('MEMORY_APPEND_R86.txt',extra)
append=(ROOT/'MEMORY_APPEND_R86.txt').read_bytes()
old=json.loads((ROOT.parent/'selection_variation_r85/MEMORY_PLAN_R85.json').read_text(encoding='utf-8'))
surfaces=[]
for row in old['surfaces']:
    p=row['before']['path'];raw=Path(p).read_bytes();surfaces.append({'before':pin(p),'after_sha256':hashlib.sha256(raw+append).hexdigest()})
new('MEMORY_PLAN_R86.json',{'claim':996,'append':pin(ROOT/'MEMORY_APPEND_R86.txt'),'surfaces':surfaces})
print({'evidence_pins':len(evidence),'surfaces':len(surfaces),'goal_complete':False})
