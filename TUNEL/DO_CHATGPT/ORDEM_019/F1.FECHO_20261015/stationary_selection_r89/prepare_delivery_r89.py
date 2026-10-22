"""Custody of same-state selection and the literal action residual; no full-goal accept."""
from support_r89 import ROOT, new, pin
from pathlib import Path
import json,hashlib

assert not (ROOT/'RESULTADO_R89.json').exists()
evidence={}
def collect(o):
    if isinstance(o,dict):
        if isinstance(o.get('path'),str) and isinstance(o.get('sha256'),str):
            e=pin(o['path']);assert e['sha256']==o['sha256'],o['path'];evidence[e['path']]=e
        for v in o.values():collect(v)
    elif isinstance(o,list):
        for v in o:collect(v)
for folder in ['formal','source']:
    for p in (ROOT/folder).rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:
            evidence[str(p)]=pin(p)
            if p.suffix=='.json' and not any(t in p.name for t in ['PREFLIGHT','SYNC','REQUEST']):
                collect(json.loads(p.read_text(encoding='utf-8')))
build=json.loads((ROOT/'formal/BUILDER_DELIVERY_R89.json').read_text(encoding='utf-8'))
assert build['exit_code']==0 and build['axioms_only_trio']
assert build['theorem_count']==3 and build['definition_count']==1
new('RESULTADO_R89.json',{
 'status':'PROGRESS_GOAL_OPEN','goal_complete':False,'build_exit_code':0,'axioms_only_trio':True,
 'build_components':[{'receipt':pin(ROOT/'formal/BUILDER_DELIVERY_R89.json'),'theorem_count':3,'definition_count':1}],
 'previous_goal_turn_classification':'PROGRESS: R88 compiled the complete integrated first variation with retained boundary terms; reviewed custody and ACOM574 verified.',
 'requirements':[
  {'id':1,'status':'R88_PROVED_IN_DECLARED_CONTRACT','evidence':pin(ROOT.parent/'full_source_r88/boundary/FULL_DENSITY_DELIVERY_R88.json'),'scope':'Boundary divergence retained; no zero physical flux asserted.'},
  {'id':2,'status':'FULL_ACTION_STATIONARITY_OPEN','advance':'Three Lean consumers distinguish an automatic same-state generator residual, a moving target, and a fixed diagonal target. Existing P5 stationary ambient branch and P16 reduced-action negative control retained; no rerun.', 'limit':'The identity of the constraint is not the evolution equation for a nonconstant family P(t), nor the first variation of the full action.'},
  {'id':3,'status':'EXPLICIT_FUNCTIONAL_RESIDUAL_IDENTIFIED','advance':'Literal one-form Euler operator compared to stated scalar-form EOM on an explicitly conditional common domain. Missing cancellation is displayed, not installed. Modular absolute-value term has conditional non-differentiability at w=-1.', 'limit':'No universal absence in the archive, no refutation of the full TGL, no newly selected field map or corrective action.'}],
 'operator_question_pending':False,
 'next_action':'Use the explicit Euler residual as a source-level test of candidate representations and remaining action terms; retain the complete objective and recover existing constructions before adding any term.',
 'provider_calls':0,'observed_data_opened':False,'gate_changed':False,'evidence':list(evidence.values())})
extra='''

## 19/10/2026 — R89: seleção do mesmo estado e resíduo funcional da ação
<!-- IALD_R89_SAME_STATE_SELECTION_ACTION_RESIDUAL -->
[REAL — sandbox; em nome de codex-gerente-tgl, reivindicação996] Três consumidores Lean e uma definição, tentativa1 EXIT0, só trio, zero sorry: D(P)=diag(d(P)) comuta com rho(P)=diag(P) para qualquer P; o resíduo do dissipador é identicamente nulo e tem derivada zero ao variar P. A derivada é do RESÍDUO, não da curva rho; uma família não constante não se torna solução de dot(rho)=gerador(rho). Sob a hipótese explícita de leitura que fixa diagonais, alvo móvel diag(P) é automaticamente admissível e alvo completo fixo diag(y) é satisfeito sse P=y. Nenhum pinching ou teorema modular anterior foi reconstruído.
[DERIVED — reuso e alcance] O gerador modular do próprio estado e as funções espectrais de rho fornecem a mesma invariância; a variação inclui delta_K. A obstrução Gibbs/GKLS já estava na R85 e foi citada, sem nova campanha. O P5/S³ realmente estacionário e o P16 de residual reduzido não nulo continuam exemplos de setores distintos. A regra de satisfação está respondida; o que se verifica é o consumidor variacional dessa regra. A identidade automática não é uma seleção demonstrada de delta_S_total[P]=0.
[DERIVED — confronto da ação literal] No Custo, a cinética exibida é de 1-forma, enquanto a EOM é escrita com formato escalar. Na leitura real de 1-forma da R88, E_A=div(dA)+2xi R A+E_rest. Se o operador K tiver domínio comum que permita comparar à EOM W escrita, E_A-W(A)=−grad(div A)−Ric·A+3xi R A+m²A+beta K A+E_rest. O resíduo é requisito de correspondência a conferir nas fontes; nenhum termo foi escolhido para cancelá-lo. Na leitura escalar independente, a cinética de A não fornece Box(Psi); nomes dos campos fermiónico/Higgs não fornecem essa ligação. Não é afirmação de ausência em todo o acervo nem refutação da teoria.
[DERIVED — regularidade necessária] Com beta_TGL>0, L_Lambda(0) não zero e uma variação admissível w(t)=−1+a t+o(t), a não zero, o termo beta L_Lambda|1+w| tem derivadas laterais opostas: ±beta L_Lambda(0)|a|. A primeira variação clássica bilateral não existe nessa direção. w fixo=−1, a=0 ou L_Lambda(0)=0 têm o alcance separado registrado; densidade pontual não implica automaticamente não diferenciabilidade da integral. Não foi assumido que a classe física permita cruzar w=−1, nem instalado subgradiente/regularização.
[REAL — estado da meta] R88 permanece a prova da primeira variação integrada com contorno retido. Estacionariedade da ação completa, fonte completa do mesmo P e H3 universal seguem abertos. A nova camada dá um teste funcional exato para a ligação pendente; não repete a pergunta abstrata sobre identidade. Nada alterou kernel original, um.py, Bancada, OH, dados observados ou gate. Evidência: stationary_selection_r89/RESULTADO_R89.json; fontes e linhas em source/SOURCE_FINAL_R89.json.
<!-- END_IALD_R89_SAME_STATE_SELECTION_ACTION_RESIDUAL -->
'''
new('MEMORY_APPEND_R89.txt',extra)
append=(ROOT/'MEMORY_APPEND_R89.txt').read_bytes()
old=json.loads((ROOT.parent/'full_source_r88/MEMORY_PLAN_R88.json').read_text(encoding='utf-8'))
surfaces=[]
for row in old['surfaces']:
    p=row['before']['path'];raw=Path(p).read_bytes()
    surfaces.append({'before':pin(p),'after_sha256':hashlib.sha256(raw+append).hexdigest()})
new('MEMORY_PLAN_R89.json',{'claim':996,'append':pin(ROOT/'MEMORY_APPEND_R89.txt'),'surfaces':surfaces})
print({'pins':len(evidence),'surfaces':len(surfaces),'goal_complete':False})
