"""Prepare reviewed additive progress; never complete R16 or replace evidence."""
from support_r84 import ROOT, new, pin
import json, hashlib, re

assert not (ROOT/'RESULTADO_R85.json').exists()
assert list((ROOT/'selection').glob('*ADENDO*')) or list((ROOT/'selection').glob('*Adendo*'))
build=json.loads((ROOT/'boundary_builder/BUILDER_DELIVERY_R85.json').read_text(encoding='utf-8'))
assert build['exit_code']==0 and build['successful_attempt']==3
log=(ROOT/'boundary_builder/BUILD_3.log').read_text(encoding='utf-8')
axioms=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log,re.S)
assert len(axioms)==8
assert all(set(a.strip() for a in body.replace('\n',' ').split(',')) <= {'propext','Classical.choice','Quot.sound'} for _,body in axioms)
assert not re.search(r'\bsorry\b|\baxiom\s', (ROOT/'boundary_builder/PalatiniBoundaryR85_3.lean').read_text(encoding='utf-8'))

evidence={}
def collect(obj):
    if isinstance(obj,dict):
        if isinstance(obj.get('path'),str) and isinstance(obj.get('sha256'),str):
            measured=pin(obj['path']);assert measured['sha256']==obj['sha256'],obj['path']
            evidence[measured['path']]=measured
        for v in obj.values():collect(v)
    elif isinstance(obj,list):
        for v in obj:collect(v)
for folder in ['boundary_builder','selection']:
    for p in (ROOT/folder).rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:
            evidence[str(p)]=pin(p)
            if p.suffix=='.json' and not any(t in p.name for t in ['PREFLIGHT','SYNC','REQUEST']):
                collect(json.loads(p.read_text(encoding='utf-8')))
for n in ['SOURCE_COMPLETENESS_R85.txt','SOURCE_EXCERPTS_R85.json','SOURCE_OFFSHELL_RESULT.json','source_offshell_control.py']:
    evidence[str(ROOT/n)]=pin(ROOT/n)
    if n.endswith('.json'):collect(json.loads((ROOT/n).read_text(encoding='utf-8')))
new('RESULTADO_R85.json',{'status':'PROGRESS_GOAL_OPEN','goal_complete':False,'previous_goal_turn':'progress','current_goal_turn':'progress',
    'build_exit_code':0,'build_attempt_count':3,'axioms_only_trio':True,'declaration_count':8,'sorry_count':0,
    'requirements':[
        {'id':1,'status':'PARTIAL','proved':'Actual curved metric Ricci variation contracted at fixed inverse metric equals covariant divergence of explicit Palatini current. R83 separately handles inverse variation.','remaining':'Weighted current W-to-H identification, volume divergence and Hessian-f connection; boundary/domain hypotheses in the same system.'},
        {'id':2,'status':'OPEN_WITH_OBSTRUCTION','proved':'Existing Gibbs/lock/GKLS criteria differ from integrated action stationarity. Pure sigma on-shell radial condition incompatible with ten free normal second forms.','remaining':'Derive stationarity of the identified full action from an independent selection law; do not assume stationary.'},
        {'id':3,'status':'PARTIAL_CONSTRUCTIVE_AND_DIAGNOSTIC','proved':'Explicit P16 has local smooth compact metric lifts with fixed selected probability. Sigma varies; composed sigma action reduces to A(s)+B(s)q with a distinct Hilbert source.','remaining':'Full physical sectors, off-background modular response and their induced variations; original null equation not established.'}],
    'restrictions':'No original kernel, um.py, production, OH, observed data, gate or goal completion. P16 analytic proof plus symbolic validation, not Lean inhabitant.',
    'evidence':list(evidence.values())})

extra='''

## 19/10/2026 — R85: corrente curva, alcance P16 e fonte da ação composta
<!-- IALD_R85_PALATINI_P16_SOURCE -->
[REAL — sandbox; em nome de codex-gerente-tgl, reivindicação996] Seis teoremas/duas definições Lean compilados na tentativa3, EXIT0, só trio, zero sorry. Palatini da conexão métrica real g+t h e contração g^{ab}δRic_ab=∇W, com compatibilidade da inversa derivada do kernel. O inverso fica fixo nessa contração; R83 contém a parcela δg^{-1}Ric. Duas tentativas falhas preservadas. Ainda faltam W em termos de H/tr(h), volume, corrente ponderada e Hess(f); regularidade de C é hipótese explícita.
[DERIVED — demonstração analítica e controle exato] P16 positivo local foi construído: P(0)=(1/4,1/20,...,1/20), dez normais com componente selecionada zero, matriz normal→δg de posto10/determinante−1024. A inversa suave e a ortogonalidade produzem levantamento de campos métricos compactos, não só jets; curva normalizada preserva admissibilidade. Não é habitante Lean nem solução física. Sigma muda junto. Manter sigma fixa impede qualquer teste nulo não zero: restrição espacial teria posto3 ou0 contra posto1.
[ERRATA AO LADO — em nome de codex-gerente-tgl] A condição suficiente E_sigma radial indicada na nota P16 não tem habitante no setor puramente cinético com esse alcance normal completo: M invertível impede g^{ab}M_ab=0. O ADENDO preserva a nota e explicita a incompatibilidade. Não usar rank10 como prova de H3 ou de equação material.
[DERIVED — fonte identificada no setor composto, não fonte física completa] Para s=P_s, q=g^{-1}(ds,ds), L_sigma=−c_G tr_g(Σdphi²)/2 reduz EXATAMENTE a A+Bq, A=c_G/[4(1−s)], B=c_G/[8s(1−s)²]. Na convenção Hilbert negativa, T_eff=(A+Bq)g−2B ds⊗ds. Em P16 na origem, para k=(1,sqrt(13)/3,0,0), T_sigma(k,k)=22c_G/9 e T_eff(k,k)=−4c_G/9. São duas operações variacionais distintas; a ação EH−sigma composta não admite trocar essas fontes. Nenhuma estacionariedade ou refutação da TGL completa foi anunciada. Outros setores e acoplamentos precisam ser identificados e variados.
[DERIVED — acervo e limite] VariationalInhabitant seleciona Gibbs para energia fornecida; h=−logP e resetGKLS construído de P mostram que criticidade/atração isoladas não selecionam geometria. A resposta cosmológica w_eff(z) não determina sua derivada métrica fora do fundo; controle local de extensões iguais em valor/diferentes fontes e de |1+w| não diferenciável no cruzamento registrados. Busca focal com fontes/linhas/pinos, sem alegar ausência em todo o PC.
[OPEN] Objetivo R16 integral permanece working: ligar a corrente ponderada ao integral, derivar seleção dinâmica/estacionariedade da ação completa, identificar fonte e concluir a equação em todas direções nulas. P16 resolve uma possibilidade geométrica, não todas as condições simultâneas. OH adiado; nenhum um.py, kernel original, produção, dado observado ou gate alterado. Evidência: F1.FECHO_20261015/selection_variation_r85/RESULTADO_R85.json e entregas locais revisadas. Nós Vivo não indexa a unidade; reuso veio das fontes diretas e R84/mapa1216.
<!-- END_IALD_R85_PALATINI_P16_SOURCE -->
'''
new('MEMORY_APPEND_R85.txt',extra)
append=(ROOT/'MEMORY_APPEND_R85.txt').read_bytes()
old=json.loads((ROOT.parent/'integrated_h3_r84/MEMORY_PLAN_R84.json').read_text(encoding='utf-8'))
surfaces=[]
for row in old['surfaces']:
    p=row['before']['path'];raw=__import__('pathlib').Path(p).read_bytes()
    surfaces.append({'before':pin(p),'after_sha256':hashlib.sha256(raw+append).hexdigest()})
new('MEMORY_PLAN_R85.json',{'claim':996,'append':pin(ROOT/'MEMORY_APPEND_R85.txt'),'surfaces':surfaces})
print({'evidence_pins':len(evidence),'surfaces':len(surfaces),'goal_complete':False})
