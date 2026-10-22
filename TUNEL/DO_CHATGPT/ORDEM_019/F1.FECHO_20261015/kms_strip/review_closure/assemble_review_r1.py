"""Immutable source-level review receipt for the root's KMS closure lemmas."""
from pathlib import Path
import datetime, hashlib, json, re
HERE = Path(__file__).resolve().parent
BASE = HERE.parent
NAMES = ['StripMaximumR2','StripUniformLimitR2','StripBoundaryLimitR1',
         'UnitaryCoefficientsUniformR2','KMSGraphClosureR3']
def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
items=[]
for name in NAMES:
    src=BASE/(name+'.lean'); raw=src.read_bytes()
    assert not re.search(rb'\b(sorry|admit|axiom)\b',raw)
    accepted=[]
    for receipt in (BASE/'attempts').glob('*/RECEIPT.json'):
        snap=receipt.parent/src.name
        if not snap.is_file() or snap.read_bytes()!=raw: continue
        meta=json.loads(receipt.read_bytes())
        if meta['exit_code']==0: accepted.append((receipt,meta))
    assert accepted,name
    receipt,meta=sorted(accepted,key=lambda x:str(x[0]))[-1]
    for artifact in meta['artifacts']:
        assert pin(Path(artifact['path']))==artifact
    ax=receipt.parent/'AXIOMS.txt'; txt=ax.read_text(encoding='utf-8')
    assert 'sorryAx' not in txt
    lines=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",txt,re.S)
    assert lines,name
    assert all(set(x.strip() for x in a.split(',') if x.strip()) <=
               {'propext','Classical.choice','Quot.sound'} for _,a in lines)
    items.append({'source':pin(src),'builder_receipt':pin(receipt),
                  'builder_exit':meta['exit_code'],'builder_seconds':meta['seconds'],
                  'axiom_prints':len(lines),'axioms':pin(ax)})
review={
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'author':'codex-atrator-skeptic','unit':'F1.FECHO_20261015','claim':845,
 'verdict':'PASS_WITH_STATED_SCOPE',
 'method':'Independent mathematical source review and byte verification of builder evidence; no new rebuild.',
 'independent_rebuild':False,'sources':items,'material_findings':[],
 'reasoning':[
  'Rotation z=iw reduces the horizontal strip to the existing three-lines theorem. Global boundedness and a common nonnegative bound on both edges are consumed.',
  'Each pairwise difference is bounded and holomorphic. Uniform Cauchy estimates on both edges control the full closed strip; completeness is used only for scalar values.',
  'Uniform convergence preserves boundary continuity and interior holomorphy. A single approximant plus error 1 supplies boundedness of the limit.',
  'Cauchy-Schwarz and exact unitary norm preservation give uniform coefficient convergence in the whole time parameter, without assuming continuity of the family.',
  'Graph closure uses simultaneous convergence of (A Omega,A* Omega), separately in each argument; it does not replace that with ordinary cyclic density or assume bounded approximating operator norms.'
 ],
 'scope':'Generic closure theorem. The concrete generator KMS proof, graph density, and final canonical consumer are separate dependencies; this receipt does not certify them.',
 'production_modified':False,'gate_changed':False}
def save(p,b):
    if isinstance(b,str): b=b.encode('utf-8')
    with p.open('xb') as f:f.write(b)
    assert p.read_bytes()==b
save(HERE/'REVISAO_FECHO_KMS_R1.json',json.dumps(review,ensure_ascii=False,indent=2)+'\n')
save(HERE/'REVISAO_FECHO_KMS_R1.md',
 '# Revisão independente do fecho KMS\n\n'
 '[REAL — leitura matemática e conferência de bytes] PASSA no alcance declarado.\n\n'
 'Foram lidos cinco módulos da raiz; nove impressões de axiomas dos builds aceitos ficam no trio. Não houve recompilação independente nesta revisão.\n\n'
 'A prova usa as duas bordas da faixa, a limitação global de cada aproximante e convergência conjunta do vetor e do vetor adjunto. A cota uniforme dos coeficientes decorre da unitariedade. Nenhuma aproximação em norma dos operadores é presumida.\n\n'
 'A passagem de funções limitadas e holomorfas para o limite conserva as duas bordas, a continuidade no fecho e a analiticidade interior. O resultado é um lema genérico de fecho; não fornece por si os geradores KMS ou a densidade de grafos concretos.\n\n'
 'Nenhum achado material. Fontes, hashes, tempos, recibos e alcance estão no JSON ao lado. Nada move o gate.\n')
print(json.dumps(pin(HERE/'REVISAO_FECHO_KMS_R1.json')))
