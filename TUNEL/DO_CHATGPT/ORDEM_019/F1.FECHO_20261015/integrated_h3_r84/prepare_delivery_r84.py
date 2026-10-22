"""Prepare reviewed incremental delivery, without completing the full R16 goal."""
from support_r84 import ROOT, new, pin
from pathlib import Path
import json, hashlib, re

bd=json.loads((ROOT/'action_builder/BUILDER_DELIVERY_R84.json').read_text(encoding='utf-8'))
for e in bd['files']: assert pin(e['path']) == e
src=(ROOT/'action_builder/IntegratedDensityR84_1.lean').read_text(encoding='utf-8')
log=(ROOT/'action_builder/BUILD_1.log').read_text(encoding='utf-8')
groups=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log)
assert len(groups)==11 and all(set(a.replace('\n','').split(', ')) <= {'propext','Classical.choice','Quot.sound'} for _,a in groups)
assert not re.search(r'\bsorry\b',src) and 'sorryAx' not in log
assert bd['exit_code']==0
new('FINAL_BUILD_R84.json',{'exit_code':0,'attempt_count':1,'definitions':6,'theorems':5,'axioms_only_trio':True,'sorry_count':0,'evidence':bd['files']})
pd=json.loads((ROOT/'p_variations/DELIVERY_P_VARIATIONS_R84.json').read_text(encoding='utf-8'))
for e in pd['evidence']: assert pin(e['path'])==e
new('P_VARIATIONS_VERIFIED_R84.json',{'status':'PINS_VERIFIED_ANALYTIC_CANDIDATE','evidence':pd['evidence']})

extra='''

## 19/10/2026 — R84: integral, contorno e alcance real das variações P
<!-- IALD_R84_INTEGRATED_ACTION_P -->
[REAL — sandbox, em nome de codex-gerente-tgl; reivindicação993] Cinco teoremas/seis definições compilados na primeira tentativa, EXIT0, só trio, zero sorry: derivada sob integral da densidadeR83 com hipóteses de dominação/mensurabilidade/integrabilidade, combinação fR−densidade escalar e divergência/fluxo em caixa4D. O fluxo genérico não é ainda identificado formalmente à corrente gravitacional; a decomposição curva foi derivada analiticamente em INTEGRATED_DERIVATION_R84.txt. Três controles polinomiais exatos verificam integração por partes: fluxo0 com primeiro jato de h nulo, fluxo96 no controle sem essa condição. Não são física nem prova geral curva.
[DERIVED — achado material] O diferencial de P→(g,phi) e sua adjunta foram explicitados. Com cinco probabilidades de rank4, todas as variações são pullbacks/difeomorfismos locais: a ação difeocovariante pode ser estacionária por Noether sem equação métrica. Rank10 dos jets num ponto não prova alcance de campos compactamente suportados. Na família conservada P6 com sigma em S1(1/sqrt3)×S2(sqrt(2/3)), duas direções nulas exigem C*c_G=2 e7/2 simultaneamente. Mesma P produz g e T; a conservação decorre de □phi=(3/a²)phi. Isso demonstra insuficiência desses dados/tipos para H3 universal, não refutação física da TGL. A família esferaP5 permanece rota positiva sob coeficiente identificado C*c_G=4, não ajustado.
[REAL/DERIVED — fonte e sinais] tgl_paper_unified.py:10331–10338 escreve −1/2|Dphi|², coerente com a subtração formalR84 para o setor escalar. Fonte sigma não é automaticamente a fonte integral de Dirac, Yang–Mills, Phi, potencial e termo modular. Psi escalar/Psi_mu e sua ligação à sigma exigem identificação de tipos. A fonte não minimal escalar contém −2xi*u*G+2xi(Hess(u)−g□u); a norma de covetor agrega −2xi*R*w⊗w sob as convenções explicitadas.
[OPEN — objetivo integral preservado] Identificar a corrente curva no kernel e eliminar contorno nas classes admitidas; selecionar dinamicamente P; provar alcance das variações, ao menos testes nulos compactos com matéria controlada; compor a fonte completa da mesma ação. R16 permanece em trabalho, sem submit/aceite de conclusão. A condição de seleção não será substituída por H3 como hipótese disfarçada. OH adiado; sem dados, kernel canônico, um.py, produção ou gate alterados.
[REAL — processo] Autorização humana explícita associou /root/r68_independent_review a r68_independent_review; o próprio revisor registrou aceite documentalR13 na revisão563, com recibo accept_authorized_20261019/R81_ACCEPT_AUTH_VERIFIED.json. H3 não foi fechado por esse aceite. NosVivo ainda não indexa a unidade; busca de rota por frase exata vazia não significa ausência do acervo: reutilizados R83, Selected*, VariationalInhabitant e fontes primárias.
<!-- END_IALD_R84_INTEGRATED_ACTION_P -->
'''
p=new('MEMORY_APPEND_R84.txt',extra); raw=p.read_bytes()
previous=json.loads((ROOT.parent/'density_h3_r83/MEMORY_PLAN_R83.json').read_text(encoding='utf-8'))
rows=[]
for row in previous['surfaces']:
    q=Path(row['before']['path']); before=q.read_bytes()
    assert b'IALD_R84_INTEGRATED_ACTION_P' not in before
    rows.append({'before':pin(q),'after_sha256':hashlib.sha256(before+raw).hexdigest()})
new('MEMORY_PLAN_R84.json',{'claim':993,'append':pin(p),'surfaces':rows})
print('Verified build/provenance; prepared eight-surface memory plan, not applied.')
