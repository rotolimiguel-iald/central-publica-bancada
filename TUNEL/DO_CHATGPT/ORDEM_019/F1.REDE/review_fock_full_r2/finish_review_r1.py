"""Finalize the single independent review of four frozen new Fock-construction modules."""
from pathlib import Path
import json, hashlib, datetime as dt, os
BASE=Path(__file__).resolve().parent; ROOT=BASE.parent; SRC=ROOT/'fock_construction'
KERNEL=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p): return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(p,b):
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert p.read_bytes()==b
modules=['BosonicSectors','SectorInfiniteDimension','SectorStrongContinuity','BosonicFock']
builds=[json.loads((BASE/(m+'_RECEIPT.json')).read_text()) for m in modules]
assert all(b['exit_code']==0 for b in builds)
manifests=[SRC/'DELIVERY_FOCK_KINEMATICS_R2.json',SRC/'DELIVERY_SECTORS_R1.json',SRC/'RESULTADO_STRONG_CONTINUITY_R1.json',SRC/'attempts/20261013T223456_898217Z/RECEIPT.json',ROOT/'review_fock_r2/CORE_DEPENDENCY_PINS_R1.json']
assert sha(manifests[0])=='bf83baa489ea04ab80980864a47e4f333db5f8052e087b469e0fe1f3cb9ec641'
for prefix in ['20261013T223204','20261013T223245']:
    found=list((SRC/'attempts').glob(prefix+'*/RECEIPT.json')); assert len(found)==1
    manifests+=found
queue=manifests+[BASE/(m+'_RECEIPT.json') for m in modules]; seen=set(); pins={}
def walk(x):
    if isinstance(x,dict):
        if 'path' in x and 'sha256' in x:
            p=Path(x['path']); got=pin(p); assert got['sha256']==x['sha256'],str(p)
            if 'bytes' in x: assert got['bytes']==x['bytes'],str(p)
            pins[(str(p),x['sha256'])]=got
            if p.suffix.lower()=='.json': queue.append(p)
        for v in x.values(): walk(v)
    elif isinstance(x,list):
        for v in x: walk(v)
while queue:
    p=queue.pop()
    if str(p) not in seen:
        seen.add(str(p)); walk(json.loads(p.read_text(encoding='utf-8-sig')))
newdeps=[]
for module in ['Analysis/Normed/Group/Tannery','Analysis/InnerProductSpace/Orthonormal','LinearAlgebra/Dimension/Finite']:
    newdeps += [pin(KERNEL/'.lake/packages/mathlib/Mathlib'/(module+'.lean')),pin(KERNEL/'.lake/packages/mathlib/.lake/build/lib/lean/Mathlib'/(module+'.olean'))]
comparisons=[]
for m,stamp in [('BosonicSectors','20261013T223041_528152Z'),('SectorInfiniteDimension','20261013T223024_713492Z'),('SectorStrongContinuity','20261013T223240_502652Z'),('BosonicFock','20261013T223456_898217Z')]:
    original=SRC/f'attempts/{stamp}/{m}.olean'; rebuilt=BASE/'sandbox'/(m+'.olean')
    comparisons.append({'module':m,'original':pin(original),'rebuilt':pin(rebuilt),'byte_identical':original.read_bytes()==rebuilt.read_bytes()})
claims=[
 'Each sector n is constructed as the closed complex span of diagonal pure tensors inside the completed recursively bracketed tensor power of unchanged H1.',
 'Every sector has a nonzero pure-tensor witness; gammaSector is an actual unitary functor with identity, composition, vacuum and one-particle embedding laws.',
 'BosonicFock.F specializes the completed l2 sum to these actual sectors; vacuum has norm one, gamma fixes it, and the canonical H1 embeds isometrically and intertwines gamma.',
 'The concrete Fock space is infinite dimensional: one normalized H1 vector supplies a unit vector in each mutually orthogonal sector.',
 'The generic diagonal strong-continuity theorem uses honest sectorwise continuity and summable majorant 4*norm(f n)^2; it assumes no uniform-in-n continuity.'
]
limits=[
 'The equality between the closed span of diagonal powers and the permutation-fixed presentation has not been formalized here, including identification with the earlier flip-defined two-particle sector.',
 'The generic diagonal continuity theorem is conditional on sectorwise strong continuity; these four files do not supply or specialize that hypothesis to gamma.',
 'gamma here lifts linear unitaries. No antiunitary second quantization, Weyl CCR/local algebra, modular second-quantization theorem, FockCertificate or MaxwellCertificate is inferred.'
]
report='# Revisão independente — setores e espaço de Fock\n\nPASSA no escopo declarado, sem achado material. Foram lidos e recompilados em cópias novas os quatro módulos listados no JSON; dependências anteriores apenas em leitura.\n\n'+ '\n'.join('- '+c for c in claims)+'\n\nLimites explícitos:\n\n'+'\n'.join('- '+s for s in limits)+'\n\nTodas as compilações terminaram com exit 0. A verificação de todas as constantes locais e das duas declarações de infinitude ficou somente no trio, sem sorry. Tempos, comandos, toolchain, LEAN_PATH, hashes, tentativas anteriores preservadas e comparação binária constam dos recibos. Nada foi escrito no kernel, em produção, memória, quadro ou gate.\n'
save(BASE/'REVIEW_FOCK_FULL_R1.md',report.encode())
result={'unit':'F1.REDE','status':'PASS_FORMAL_SCOPE__NO_MATERIAL_FINDING','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'reviewer':'codex-independent-modular-review','claims_checked':claims,'limitations':limits,'builds':builds,'build_count':len(builds),'compile_seconds':sum(b['seconds'] for b in builds),'all_local_constant_counts':{b['module']:len(b['local_constants']) for b in builds},'infinite_dimension_printed_theorems':builds[1]['printed_axiom_count'],'only_trio':True,'zero_sorry':True,'checked_pin_count':len(pins),'pins':list(pins.values()),'additional_mathlib_dependency_pins':newdeps,'olean_comparison':comparisons,'evidence':[pin(p) for p in manifests]+[pin(Path(__file__)),pin(BASE/'build_stage_r1.py'),pin(BASE/'REVIEW_FOCK_FULL_R1.md')],'production_writes':False}
save(BASE/'REVIEW_FOCK_FULL_R1.json',(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'path':str(BASE/'REVIEW_FOCK_FULL_R1.json'),'sha256':sha(BASE/'REVIEW_FOCK_FULL_R1.json'),'pins':len(pins),'seconds':result['compile_seconds'],'local_counts':result['all_local_constant_counts'],'olean_identical':sum(x['byte_identical'] for x in comparisons)}))
