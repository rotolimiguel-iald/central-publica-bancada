"""Pin the independent semantic review; no Lean rebuild is claimed."""
from pathlib import Path
import datetime, hashlib, json, re
BASE=Path(__file__).resolve().parent
SRC=BASE.parent/'gns_coefficient_tomita'
receipt=SRC/'GAUSSIAN_REGULARIZATION_RECEIPT_R1.json'
def pin(p):
    p=Path(p); b=p.read_bytes()
    return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def write(p,b):
    if p.exists(): raise RuntimeError('Existing evidence refused')
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b
    tmp.rename(p)
j=json.loads(receipt.read_bytes()); checked={}
def check(x):
    if isinstance(x,dict):
        if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str):
            actual=pin(x['path'])
            if actual['sha256']!=x['sha256']:raise RuntimeError(('Pin changed',x['path']))
            checked[x['path']]=actual
        for v in x.values():check(v)
    elif isinstance(x,list):
        for v in x:check(v)
check(j)
mods=['ResolventPhaseIntegralR2','ResolventScaledPhaseIntegralR1','GaussianLogScalarR4',
 'GaussianProbabilityKernelR4','GaussianResolventSymbolR2','StrongUnitaryAverageR1',
 'GroupAverageApproximationR2','GaussianResolventRegularizerR4','GaussianResolventAverageR6']
for m in mods:
    b=(SRC/(m+'.lean')).read_text(encoding='utf-8')
    assert not re.search(r'\bsorry\b',b)
assert all(r['exit_code']==0 for r in j['records'])
assert j['axioms_only_trio'] and j['all_local_decl_count']==len(j['all_local_declarations'])
findings=[
 'Sem achado material nos nove fontes e no delta final R5→R6, que apenas explicita a coerção de escala real/complexa.',
 'O núcleo real gaussiano tem integral um; a transformada angular exp(-(c*l)^2/4) foi derivada da integral gaussiana, com normalização explícita.',
 'A função compactificada tem valores zero nos extremos. Continuidade e fatoração por R são provadas para b>0; c=0 é excluído da igualdade espectral usada, e a sequência 1/(n+1) nunca é zero.',
 'A igualdade média=CFC é primeiro provada na imagem de R(1−R) e estendida por continuidade/densidade; R e 1−R injetivos são hipóteses explícitas indispensáveis.',
 'A faixa 0≤R≤1 e a fatoração spectral=R*cfc(factor) fornecem alcance no domínio da raiz exata. Não se assume a suavização como campo.',
 'A convergência forte usa continuidade forte das órbitas e convergência dominada, sem exigir continuidade do grupo na norma de operadores.',
 'A preservação de grafos reais usa peso real e invariância explícita; não estabelece sozinha igualdade entre o grafo GNS e o grafo de coeficientes.'
]
report='# Revisão independente da regularização gaussiana — R1\n\n**PASS_WITH_STATED_SCOPE.** Revisão semântica de fontes; sem recompilação independente nesta revisão.\n\n'+'\n'.join('- '+s for s in findings)+'\n\nTodos os pinos do recibo foram relidos dos bytes. As compilações e o auditor de 87 declarações são os do construtor, conferidos por seus recibos. Nenhuma promoção canônica ou igualdade GNS é afirmada.\n'
md=BASE/'REVISAO_GAUSSIAN_REGULARIZATION_R1.md';write(md,report.encode('utf-8'))
result=dict(status='PASS_WITH_STATED_SCOPE',reviewer='codex-atrator-skeptic',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),unit='F1.FECHO_20261015',claim=845,
 review_type='INDEPENDENT_SEMANTIC_SOURCE_REVIEW_NO_REBUILD',delivery=pin(receipt),source_files_read=[pin(SRC/(m+'.lean')) for m in mods],
 checked_pins=list(checked.values()),checked_pin_count=len(checked),builder_all_local_decl_count=j['all_local_decl_count'],independent_rebuild=False,findings=findings,
 report=pin(md),script=pin(__file__),production_modified=False,memory_modified=False,gate_modified=False)
out=BASE/'REVISAO_GAUSSIAN_REGULARIZATION_R1.json';write(out,(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps(dict(review=pin(out),checked_pins=len(checked)),ensure_ascii=False))
