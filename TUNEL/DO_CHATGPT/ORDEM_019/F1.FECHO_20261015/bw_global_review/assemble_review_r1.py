"""Independent semantic review of the vacuum-sector and full Fock BW composition."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
OUT = BASE.parent
TARGETS = {
    "CanonicalZeroSectorResolventR1": "20261015T214232_162810Z",
    "CanonicalZeroSectorFlowR3": "20261015T215928_934484Z",
    "CanonicalFockBWR2": "20261015T220139_437497Z",
}
def pin(p):
    p = Path(p); b = p.read_bytes()
    return {"path": str(p), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
def new(p,b):
    if p.exists(): raise RuntimeError(f"Existing evidence: {p}")
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f: f.write(b)
    if tmp.read_bytes()!=b: raise RuntimeError('Bytes differ')
    tmp.rename(p)
report=BASE/'REVISAO_BW_GLOBAL_R1.md'
receipt=BASE/'REVISAO_BW_GLOBAL_R1.json'
if report.exists() or receipt.exists(): raise RuntimeError('Existing output')
builds=[]; checked={}; print_count=0
for name,attempt in TARGETS.items():
    src=OUT/'tensor_l2'/(name+'.lean')
    if re.search(r'\bsorry\b',src.read_text(encoding='utf-8')): raise RuntimeError('Sorry refused')
    rp=OUT/'kms_strip'/'attempts'/attempt/'RECEIPT.json'
    r=json.loads(rp.read_text(encoding='utf-8'))
    if r['exit_code']!=0 or not r['readonly_dependencies_unchanged']: raise RuntimeError('Build not accepted')
    if pin(src)['sha256']!=r['source']['sha256']: raise RuntimeError('Source differs')
    for e in [r['source'],*r['dependencies'],*r['artifacts']]:
        if pin(e['path'])['sha256']!=e['sha256']: raise RuntimeError('Dependency pin differs')
        checked[e['path']]=e
    ax=(rp.parent/'AXIOMS.txt').read_text(encoding='utf-8')
    prints=re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",ax,re.S)
    if len(prints)!=5: raise RuntimeError('Unexpected print count')
    for n,a in prints:
        if not set(x.strip() for x in a.split(',') if x.strip())<={'propext','Classical.choice','Quot.sound'}:
            raise RuntimeError('Non-trio axioms')
    print_count+=len(prints)
    builds.append({'source':pin(src),'receipt':pin(rp),'exit_code':r['exit_code'],
                   'seconds':r['seconds'],'prints':[n for n,a in prints]})

support=[OUT/'tensor_l2'/'CanonicalTensorResolventR3.lean',
         OUT/'tensor_l2'/'ImaginaryPowerIntertwiningR2.lean',
         OUT/'gamma_unbounded'/'CanonicalFockModularFlowR2.lean',
         OUT/'network_review'/'POSITIVE_SECTOR_BW_SEMANTIC_REVIEW_R1.json']
findings=[
 'Nenhum achado material na composição revisada.',
 'No setor zero, a ação tensorial de qualquer operador limitado é identidade por densidade da inclusão na completação. GA e GB agem como identidade nessa componente, sem hipótese de preservação de setores do resolvente.',
 'A equação real do resolvente fornece 2*(modularR x)_0=x_0, portanto Q0 R=(1/2)Q0. O valor 1/2 é derivado da equação; não é premissa espectral.',
 'O entrelaçamento limitado passa pelo cálculo funcional contínuo da função amortecida: em 1/2, o amortecimento e a fase regularizada valem 1/4. A imagem densa do amortecimento estende a igualdade ao fluxo em todo vetor, sem inverter um operador de inversa limitada não demonstrada.',
 'O setor zero de Gamma(u) é identidade para qualquer u. lp.ext e a decomposição n=0 ou n+1 combinam a nova igualdade com positive_component_modularFlow e identificam os operadores em toda a Fock existente.',
 'canonical_pair_tomita substitui a igualdade provada em actual_spectral_pair_measured. O grafo e os domínios reais da construção anterior permanecem os mesmos; nenhum campo equivalente à conclusão é introduzido.',
 'O sinal modular é B0(-(2*pi*t)); o KMS físico com B0(+(2*pi*t)) é uma convenção distinta já provada em outra cadeia, não trocada nesta composição.'
]
limits=[
 'Revisão matemática independente por leitura de fontes e conferência de bytes dos recibos/artefatos/dependências. Não houve recompilação independente nesta revisão.',
 'A revisão dos setores positivos é herdada do parecer de tempo_math_review, pinado; os três módulos de vácuo/composição foram lidos integralmente nesta revisão.',
 'Não afirma representação global de Poincare/helicidade, rede global, dinâmica modular do peso dual, traço escalado ou realização experimental.',
 'Nenhum arquivo canônico, memória, quadro, dado observado ou gate foi alterado.'
]
md='# Revisão independente — BW na Fock completa\n\n[REAL — fonte e integridade conferidas; sem recompilação independente.]\n\n**PASS_WITH_STATED_SCOPE**\n\n'
md+='\n'.join('- '+f for f in findings)+'\n\n## Alcance\n\n'+'\n'.join('- '+s for s in limits)+'\n'
new(report,md.encode('utf-8'))
data={'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'unit':'F1.FECHO_20261015','claim':845,
      'reviewer':'atrator_skeptic','status':'PASS_WITH_STATED_SCOPE','method':'Independent semantic source reading and hash verification of builder receipts; no independent rebuild.',
      'builds':builds,'printed_axioms_count':print_count,'axioms_only_trio':True,'zero_sorry':True,
      'findings':findings,'scope_limits':limits,'support_read':list(map(pin,support)),
      'checked_artifacts':list(checked.values()),'report':pin(report),'review_script':pin(__file__),
      'independent_rebuild':False,'production_modified':False,'memory_modified':False}
new(receipt,(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'receipt':pin(receipt),'checked_count':len(checked),'prints':print_count},ensure_ascii=False))
