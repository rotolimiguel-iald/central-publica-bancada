"""Prepare reviewed additive progress; no acceptance of the full R16 goal."""
from support_r87 import ROOT, new, pin
from pathlib import Path
import json, hashlib, re

assert not (ROOT/'RESULTADO_R87.json').exists()
build=json.loads((ROOT/'boundary/BUILD_2.json').read_text(encoding='utf-8'))
assert build['exit_code']==0
log=(ROOT/'boundary/BUILD_2.log').read_text(encoding='utf-8')
axioms=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log,re.S)
assert len(axioms)==5
assert all(set(a.strip() for a in body.replace('\n',' ').split(',')) <= {'propext','Classical.choice','Quot.sound'} for _,body in axioms)
assert not re.search(r'\bsorry\b|\baxiom\s',(ROOT/'boundary/SymmetricBoundaryR87_2.lean').read_text(encoding='utf-8'))
historical=Path(r'C:\IALD\Central de Patentes\Chatgpt\HABITANTE_CURVO_SIGMA_20260909_202000')
receipt=json.loads((historical/'VERIFICACAO_SIMBOLICA.json').read_text(encoding='utf-8'))
assert len(receipt['checks'])==14 and all(c['passed'] for c in receipt['checks'].values())
evidence={}
def collect(o):
    if isinstance(o,dict):
        if isinstance(o.get('path'),str) and isinstance(o.get('sha256'),str):
            e=pin(o['path']);assert e['sha256']==o['sha256'],o['path'];evidence[e['path']]=e
        for v in o.values():collect(v)
    elif isinstance(o,list):
        for v in o:collect(v)
for folder in ['boundary','canonical_sources']:
    for p in (ROOT/folder).rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:
            evidence[str(p)]=pin(p)
            if p.suffix=='.json' and not any(t in p.name for t in ['PREFLIGHT','SYNC','REQUEST']):collect(json.loads(p.read_text(encoding='utf-8')))
for p in [ROOT/'REUSE_STATIONARY_BRANCH_R87.txt',historical/'HABITANTE_CURVO_SIGMA_E_AREA.md',historical/'VERIFICACAO_SIMBOLICA.json',ROOT.parent/'mirror_h3_r81/accept_authorized_20261019/R81_ACCEPT_AUTH_VERIFIED.json']:
    evidence[str(p)]=pin(p)
    if p.suffix=='.json':collect(json.loads(p.read_text(encoding='utf-8')))
new('RESULTADO_R87.json',{'status':'PROGRESS_GOAL_OPEN','goal_complete':False,
 'build_exit_code':0,'build_attempt_count':2,'axioms_only_trio':True,'declaration_count':5,'sorry_count':0,
 'canonical_baseline':'Current um.py bytes matched seal by source audit; no execution.',
 'requirements':[
 {'id':1,'status':'FORMAL_COVARIANT_CURRENT_PROGRESS','proved':'Actual Levi-Civita variation expressed in covariant jets of h; same Palatini W contracted explicitly.','remaining':'Formal raised-field/trace derivative identities, Hessian weighted current and integrated composition; physical/global boundaries.'},
 {'id':2,'status':'EXISTING_STATIONARY_BRANCH_REUSED_FULL_ACTION_OPEN','proved':'Existing P5/S3 curved inhabitant satisfies independent ambient Einstein-sigma Euler equations with named chosen constants. Compact integrated stationarity follows. Historical 14 exact symbolic checks reused, not rerun.','remaining':'Identify full intended action and its same-P stationary dynamics; model constants are not physical calibration. P16/S14 is a different class.'},
 {'id':3,'status':'CANONICAL_CONTRACT_RECOVERED_WITH_TYPED_GAPS','proved':'19 source matrix and focused 69-extraction search distinguish scalar Psi, 1-form potential, normalized sigma and algebraic density. Current canonical source retains corresponding INPUT.','remaining':'Map intended Psi representation and complete off-background modular/material source to same P, including all-null compatibility.'}],
 'R13_acceptance':'Already registered at revision563, all four receipt pins reverified; no duplicate acceptance.',
 'restrictions':'No canonical kernel, um.py, production, OH, observed data, gate, or full-goal completion.',
 'evidence':list(evidence.values())})
extra='''

## 19/10/2026 — R87: ação canônica recuperada e corrente covariante
<!-- IALD_R87_CANONICAL_ACTION -->
[REAL — sandbox; em nome de codex-gerente-tgl, reivindicação996] Cinco teoremas Lean na tentativa2, EXIT0, só trio, zero sorry: a variação da conexão métrica real é q·lowerChristoffel(∇h), e a MESMA corrente Palatini deR85/R86 é expressa pelas contrações de ∇h. Primeira tentativa falha preservada. Ainda faltam a identificação formal das derivadas do campo levantado/traço e a composição Hess(f)/integral completa; a expressão analíticaR86 permanece com seu alcance.
[DERIVED — reuso, não reconstrução] O habitante curvo P5/S³ de09/09 já satisfaz as equações AMBIENTES independentes da ação −EH+sigma, com Lambda=3/4 e kappa=4/c escolhidos no exemplo. A variação integrada compacta liga esses coeficientes nulos à estacionariedade local; Ric(k,k)=4H e T(k,k)=cH para toda direção nula. Reutilizado recibo histórico de14controles exatos, sem rerun nem nova provaLean do habitante. Não dizer que falta qualquer habitante estacionário: falta o da ação COMPLETA pretendida. Escolhas do exemplo não determinam G_N, unidades Fisher ou Lambda física.
[DERIVED — distinções materiais] P5 restrito admite só difeomorfismos locais; sua estacionariedade restrita não implica equações ambientes, embora o exemplo as satisfaça separadamente. P16 livre/R85 tem alvoS14, não S³; residualR86 não contradiz o ramo09/09. Troca GLOBAL de sinal não muda pontos críticos; Lambda*g não cancela residual nulo.
[REAL/OPEN — fonte atual] Matriz de19fontes pinadas: o um.py corrente confere com seu selo, sem execução, e conserva identificação Psi escalar/Psi_mu/sigma e Cartan/métrica como INPUT. Custo escreve cinética dPsi de1-forma e EOM/rótulo escalar; mapa tipado falta nos trechos examinados. Gradiente puro implicaria d²psi=0, sem Maxwell não trivial; isso não exclui outras identificações. SectorFluidClosure não identifica correntes comP. Busca focal de69extraçõesR67/2414parágrafos tem cobertura dita, não ausência provada em todo o acervo.
[REAL — processo] Aceite documentalR13 já registrado na revisão563, associação autorizada e quatro pinos do recibo conferidos; não foi repetido nem convertido emH3. R16 permanece working, H3 universal aberto. Nenhum kernel original, um.py, produção, OH, dado observado ou gate alterado. Evidência: canonical_action_r87/RESULTADO_R87.json. Próximo passo: ligação tipada entre ação completa e registro selecionado; reaproveitar o ramo ambiente existente.
<!-- END_IALD_R87_CANONICAL_ACTION -->
'''
new('MEMORY_APPEND_R87.txt',extra)
append=(ROOT/'MEMORY_APPEND_R87.txt').read_bytes()
old=json.loads((ROOT.parent/'weighted_action_r86/MEMORY_PLAN_R86.json').read_text(encoding='utf-8'))
surfaces=[]
for row in old['surfaces']:
    p=row['before']['path'];raw=Path(p).read_bytes();surfaces.append({'before':pin(p),'after_sha256':hashlib.sha256(raw+append).hexdigest()})
new('MEMORY_PLAN_R87.json',{'claim':996,'append':pin(ROOT/'MEMORY_APPEND_R87.txt'),'surfaces':surfaces})
print({'pins':len(evidence),'surfaces':len(surfaces),'goal_complete':False})
