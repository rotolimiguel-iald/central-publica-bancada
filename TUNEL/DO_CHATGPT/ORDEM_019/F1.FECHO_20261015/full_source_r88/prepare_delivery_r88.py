"""Pin reviewed components and prepare additive memory; do not accept R16."""
from support_r88 import ROOT, new, pin
from pathlib import Path
import json, hashlib, re

assert not (ROOT/'RESULTADO_R88.json').exists()
receipts = ['BUILDER_DELIVERY_R88.json', 'HESSIAN_DELIVERY_R88.json', 'FULL_DENSITY_DELIVERY_R88.json']
evidence = {}

def collect(o):
    if isinstance(o, dict):
        if isinstance(o.get('path'), str) and isinstance(o.get('sha256'), str):
            actual = pin(o['path'])
            assert actual['sha256'] == o['sha256'], o['path']
            evidence[actual['path']] = actual
        for value in o.values(): collect(value)
    elif isinstance(o, list):
        for value in o: collect(value)

builds=[]
for name in receipts:
    path=ROOT/'boundary'/name
    data=json.loads(path.read_text(encoding='utf-8'))
    collect(data)
    assert data.get('exit_code',0)==0 and data['axioms_only_trio'] is True
    builds.append({'receipt':pin(path),'theorem_count':data['theorem_count'],
                   'definition_count':data['definition_count']})

for folder in ['boundary', 'source', 'spectral_reuse']:
    for path in (ROOT/folder).rglob('*'):
        if path.is_file() and '__pycache__' not in path.parts:
            evidence[str(path)]=pin(path)
            if path.suffix=='.json' and not any(t in path.name for t in ['PREFLIGHT','SYNC','REQUEST']):
                collect(json.loads(path.read_text(encoding='utf-8')))
for name in ['P5_COVARIANT_STATIONARITY_R88.txt','P5_DOMAIN_QUALIFIER_R88.txt',
             'OPERATOR_SPECTRAL_RULE_REPLY_R88.json','OPERATOR_STEERING_R88.txt']:
    evidence[str(ROOT/name)]=pin(ROOT/name)
new('RESULTADO_R88.json',{
 'status':'PROGRESS_GOAL_OPEN','goal_complete':False,'build_exit_code':0,
 'axioms_only_trio':True,'build_components':builds,
 'requirements':[
  {'id':1,'status':'INTEGRATED_FIRST_VARIATION_PROVED_WITH_EXPLICIT_HYPOTHESES',
   'proved':'Actual raised-field and trace derivatives, weighted Hessian boundary current, full-density variation and integrated derivative are composed in Lean. The integrated theorem retains the boundary divergence and explicit R84 domination, support, measurability and integrability hypotheses.',
   'scope_limit':'No vanishing boundary flux or stationarity inferred. A global physical boundary prescription is not constructed by this local/integrated identity.'},
  {'id':2,'status':'P5_COVARIANT_STATIONARY_BRANCH_DERIVED_FULL_ACTION_OPEN',
   'proved':'Every admissible nonempty rank-four P5 chart locally pulls back the existing S3 Einstein-sigma solution; ambient stationarity with kappa*c=4 and Lambda=3/4. No new numerical run.',
   'remaining':'Stationarity of the complete intended action, not inferred from preservation of a selected reading or restricted P variations.'},
  {'id':3,'status':'SPECTRAL_RULE_REUSED_NAMED_ONE_FORM_SOURCE_DERIVED',
   'proved':'Existing spectral commutator and jump sqrt(beta)*sqrt(K) compose an explicit negative-gradient flow and its fixed-space projection. Named one-form branch gives metric-dependent u variation, nonminimal stress, Euler and Noether identities. 98 exact local identities and 24 rejected omission controls.',
   'remaining':'Consume the concrete spectral representation in the same-P full-action field and source, without identifying different operators by name. All-null H3 remains open.'}],
 'human_correction':'The rule is already given. The scalar/one-form question is answered as source direction and is not pending operator. Recover and compose the existing spectral operation; do not repeat the abstract identity question.',
 'statutes':{'lean':'REAL sandbox builds','spectral_composition':'DERIVED finite face; existing source read without rebuild',
             'P5_transport':'DERIVED under named model constants and nonempty domain',
             'one_form_full_source':'DERIVED named branch, not canonical field identification',
             'exact_controls':'REAL pointwise symbolic checks; not independent full EOM/Noether tests'},
 'restrictions':'No provider, canonical kernel, um.py, production, OH, observed data, gate or full-goal completion.',
 'evidence':list(evidence.values())})
extra='''

## 19/10/2026 — R88: satisfação espectral reaproveitada, Hessiana e fonte
<!-- IALD_R88_SPECTRAL_SATISFACTION_AND_DENSITY -->
[INPUT — correção humana; registro em nome de codex-gerente-tgl, reivindicação996] A regra de satisfação já foi dada: resultado da operação corresponde ao objeto devido, pela mesma operação do espectro de gradiente negativo. A pergunta abstrata sobre identidade/representação foi repetida indevidamente. Resposta integral em full_source_r88/OPERATOR_SPECTRAL_RULE_REPLY_R88.json; ACOM revisão573. Não há pergunta pendente ao operador para recunhar essa regra. A tarefa é recuperar e consumir sua realização existente.
[DERIVED — operação concreta recuperada] DecisionCommutation fornece comutador ponderado pelos gaps, decisão por blocos e fluxo de gradiente. Com o salto já escrito sqrt(beta)*sqrt(K), D=sqrt(K), o dissipador é menos o gradiente de Phi_D(X)=beta||[D,X]||²_HS/4. Para beta>0 na face finita, o limite E_D é a projeção por blocos espectrais: E_D²=E_D e E_D T_t=E_D. A satisfação concreta é E_D(X)=Y, com Y no espaço fixo; zerar contraste sozinho não escolhe o alvo. Essa composição reaproveita a regra e não pede uma nova definição. Recuperados também o comutador diferencial do Dirac do círculo e a conexão escalar q/2 dκ. Representações distintas não foram identificadas pelo nome. O mapa à Psi_mu da mesma ação permanece por consumir/localizar; cobertura da busca é delimitada no relatório, não ausência universal.
[REAL — formalização sandbox] RaisedBoundaryR88 e HessianBoundaryR88 compõem derivadas reais do campo levantado e do traço, Levi-Civita, corrente Palatini e Hessiana: vf g^{-1}:deltaRic=div(vB)+v[H:Hess(f)-tr(g^{-1}h)Box(f)], B=fW-Hdf+tr(g^{-1}h)grad(f). FullDensityR88 acrescenta delta_v, delta_g^{-1}, delta_F e prova a derivada da integral da densidade completa, reutilizando R84 sob suporte a.e., dominação Lipschitz, mensurabilidade e integrabilidade explícitos. Assim a primeira variação integrada está ligada nesse contrato, com divergência retida; não se presume fluxo nulo ou estacionariedade. Fontes, tentativas, toolchain, LEAN_PATH, tempos e axiomas ficam pinados separadamente; só trio, zero sorry. Nenhuma equação de campo é pressuposta nesta identidade variacional.
[DERIVED — estacionariedade já existente ampliada por reuso] Todo P5 positivo normalizado de posto4 é localmente uma carta do simplex: o ramo curvo Einstein-sigma de09/09 transporta-se por difeomorfismo. No domínio não vazio, a igualdade nula requer kappa*c=4 e a equação completa requer também Lambda=3/4. São constantes escolhidas do modelo, não calibração de G_N ou Lambda física. O ramo P16/S14 e a ação completa continuam distintos; a regra não torna qualquer P estacionário.
[DERIVED/REAL — fonte nomeada] Para a leitura da ação como 1-forma independente da métrica, a variação de u=g^{-1}(A,A) acrescenta o termo não minimal R A⊗A; Euler e Noether foram derivados com a mesma convenção de sinais. 98 identidades algébricas pontuais e24 controles negativos da omissão de delta_u passaram em uma execução registrada. Esses testes não são uma verificação integral independente das EOM/Noether. A identificação canônica do campo e os termos restantes da ação não foram presumidos.
[REAL — continuidade] R16 permanece working; a fonte completa ligada ao mesmo registro e H3 em toda direção nula permanecem abertos. Reuso espectral substitui a repetição da pergunta de identidade. Nenhum provedor, kernel original, um.py, produção, OH, dado observado ou gate alterado. Evidência: full_source_r88/RESULTADO_R88.json e recibos de cada componente.
<!-- END_IALD_R88_SPECTRAL_SATISFACTION_AND_DENSITY -->
'''
new('MEMORY_APPEND_R88.txt',extra)
append=(ROOT/'MEMORY_APPEND_R88.txt').read_bytes()
old=json.loads((ROOT.parent/'canonical_action_r87/MEMORY_PLAN_R87.json').read_text(encoding='utf-8'))
surfaces=[]
for row in old['surfaces']:
    path=row['before']['path']; raw=Path(path).read_bytes()
    surfaces.append({'before':pin(path),'after_sha256':hashlib.sha256(raw+append).hexdigest()})
new('MEMORY_PLAN_R88.json',{'claim':996,'append':pin(ROOT/'MEMORY_APPEND_R88.txt'),'surfaces':surfaces})
print({'pins':len(evidence),'surfaces':len(surfaces),'goal_complete':False,'build_components':builds})
