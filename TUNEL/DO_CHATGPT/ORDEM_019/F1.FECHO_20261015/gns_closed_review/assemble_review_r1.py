"""Independent source review and recheck of the eight newly delivered GNS sources."""
from pathlib import Path
import datetime, hashlib, json, re

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'takesaki_fock'
DELIVERY=BASE/'FOCK_GNS_CLOSED_TOMITA_RECEIPT_R1.json'

def pin(p):
    raw=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}

def check(p):
    actual=pin(Path(p['path']))
    assert actual==p,(actual,p)

delivery=json.loads(DELIVERY.read_bytes())
assert len(delivery['records'])==8
assert delivery['printed_declarations']==73
for dep in delivery['checked_dependencies']: check(dep)
rows=[]
count=0
for rec in delivery['records']:
    for key in ('source','receipt','build','axioms','olean'): check(rec[key])
    src=Path(rec['source']['path'])
    assert not re.search(rb'\b(sorry|admit|axiom)\b',src.read_bytes()),src
    meta=json.loads(Path(rec['receipt']['path']).read_bytes())
    assert meta['exit_code']==0 and meta['readonly_dependencies_unchanged']
    assert Path(meta['source']['path']).read_bytes()==src.read_bytes()
    check(meta['source'])
    for p in meta['artifacts']+meta['dependencies']: check(p)
    for declaration,axioms in rec['printed_axioms'].items():
        assert set(axioms)<={'propext','Classical.choice','Quot.sound'},declaration
    assert 'sorryAx' not in Path(rec['axioms']['path']).read_text(encoding='utf-8')
    count+=len(rec['printed_axioms'])
    rows.append({'source':rec['source'],'builder_receipt':rec['receipt'],
                 'builder_exit':0,'builder_start':meta['start_utc'],'builder_end':meta['end_utc'],
                 'builder_seconds':meta['seconds'],'axiom_prints':len(rec['printed_axioms'])})
assert count==73
support_names=['CanonicalFockGNSR5','RegularScalarGNSRepresentationR2',
               'CanonicalFockRightAverageR3','RegularScalarTomitaClosureR2',
               'RegularScalarGaussianGNSR2']
report={
    'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'unit':'F1.FECHO_20261015','claim':845,'author':'codex-atrator-skeptic',
    'verdict':'PASS_WITH_STATED_SCOPE','material_findings':[],
    'method':'Independent semantic reading of all eight newly delivered sources and five supporting sources; reread hashes of builder artifacts and all 198 pinned dependencies. No new Lean invocation.',
    'independent_rebuild':False,'delivery':pin(DELIVERY),'sources':rows,
    'additional_sources_read':[pin(BASE/(n+'.lean')) for n in support_names],
    'axiom_prints_checked':count,'dependency_pins_checked':len(delivery['checked_dependencies']),
    'reasoning':[
        'The concrete weight context supplies faithfulness from the existing actual scalar dual weight. The GNS space is the closure of its orbit embedding; it is not declared equal to the original Fock Hilbert space.',
        'A represented operator equal to zero annihilates every element of the uniform finite-square ideal. Applying actual finite averages that converge strongly to identity forces the original core operator to vanish; faithfulness is derived.',
        'Right regularization of every scalar-finite-square vector converges in the actual GNS L2 norm. The integrable majorant is four times the original squared orbit norm, and dominated convergence pays the difference between strong density and GNS-norm density.',
        'The reverse inclusion of completions uses inclusion of the uniform finite ideal in the scalar-weight ideal. Neither equality of completions nor GNS density is taken as a field.',
        'Left regularization by adjoint averages lies in the finite star-core. Uniform bounds and strong convergence transfer to the concrete GNS representation; thus that star-core has dense image.',
        'Closability is transported to an auxiliary vector Tomita graph by a continuous injective Gaussian multiplication map. This does not require Gaussian multiplication to preserve the original GNS subspace or its inverse to be bounded.',
        'The closure is single-valued; its domain is the first projection of that closed graph. Conjugate scalar stability constructs the antilinear operator, and swap invariance proves domain preservation and involutivity. The concrete star-domain density is separately consumed.',
        'The nonzero graph input is an actual finite-average square with scalar weight one, propagated by injectivity of the GNS embedding; it is not a vacuous named witness.'
    ],
    'scope_limits':[
        'A faithful representation and a closed densely defined antilinear involution for the initial finite star-core of the actual scalar dual weight.',
        'No equality of the closed graph with the maximal graph from every element of the full scalar-weight star-domain is asserted by these sources.',
        'No polar decomposition or identification of this GNS modular flow with regular conjugation/geometric boost is proved by this batch.',
        'The invariant scalar dual weight is not the exp(-s)-scaled trace. No scaled trace, new full-certificate inhabitant, physical result, or gate change follows here.'
    ],
    'production_modified':False,'gate_changed':False
}
outputs={
 'REVISAO_GNS_FECHADO_R1.json':json.dumps(report,ensure_ascii=False,indent=2)+'\n',
 'REVISAO_GNS_FECHADO_R1.md':'''# Revisão do GNS e do Tomita fechado do peso escalar

[REAL — revisão de fontes e bytes] PASSA no alcance declarado; nenhum achado material.

Foram lidos os oito módulos novos e cinco suportes. Os recibos aceitos, 73 impressões no trio e 198 pinos de dependência foram relidos e conferidos. Não houve recompilação independente nesta rodada.

A representação GNS é fiel por aniquilação do ideal e aproximação forte por médias finitas reais. A igualdade das completações é provada em norma GNS por convergência dominada, com majorante 4‖f(s)‖². A densidade do domínio estrela usa regularização à esquerda e convergência da representação sob limite forte uniformemente limitado.

A closabilidade usa uma aplicação gaussiana contínua e injetiva ao grafo auxiliar separante. O domínio fechado é definido pela projeção do grafo fechado; estabilidade antilinear e simetria por troca dão o operador fechado, densamente definido e involutivo. A não vacuidade tem testemunha de peso um.

O Hilbert GNS é outra construção do mesmo núcleo regular, não o Fock original por identidade declarada. Esta entrega não identifica o grafo com todo domínio estrela do peso escalar, não identifica o fluxo modular desse GNS e não fornece traço escalado. O peso dual invariante conserva seu próprio estatuto. Nada move o gate.
'''
}
for name,text in outputs.items():
    raw=text.encode('utf-8')
    with (HERE/name).open('xb') as f:f.write(raw)
    assert (HERE/name).read_bytes()==raw
print(json.dumps(pin(HERE/'REVISAO_GNS_FECHADO_R1.json')))
