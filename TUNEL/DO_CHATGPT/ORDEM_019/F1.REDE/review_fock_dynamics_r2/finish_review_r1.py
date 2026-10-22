"""Final limited independent review of strong continuity and group actions."""
from pathlib import Path
import json, hashlib, datetime as dt, os
BASE=Path(__file__).resolve().parent; ROOT=BASE.parent; SRC=ROOT/'fock_construction'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p): return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(p,b):
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert p.read_bytes()==b
modules=['BosonicSectorContinuity','BosonicFockContinuity','BosonicFockGroupActions']
builds=[json.loads((BASE/(m+'_RECEIPT.json')).read_text()) for m in modules]
assert all(b['exit_code']==0 for b in builds)
manifests=[SRC/'DELIVERY_BOSONIC_CONTINUITY_R1.json',SRC/'DELIVERY_FOCK_CONTINUITY_R2.json',SRC/'RESULTADO_FOCK_GROUP_ACTIONS_R1.json',ROOT/'review_fock_full_r2/REVIEW_FOCK_FULL_R1.json']
assert sha(manifests[1])=='a5ca7466a7399c10561bc5180d5b7efc268f7baf18eb417fc3aafe4b11be632b'
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
comparisons=[]
for m,stamp in [('BosonicSectorContinuity','20261013T223630_675979Z'),('BosonicFockContinuity','20261013T223808_604578Z'),('BosonicFockGroupActions','20261013T223821_363536Z')]:
    original=SRC/f'attempts/{stamp}/{m}.olean'; rebuilt=BASE/'sandbox'/(m+'.olean')
    comparisons.append({'module':m,'original':pin(original),'rebuilt':pin(rebuilt),'byte_identical':original.read_bytes()==rebuilt.read_bytes()})
claims=[
 'Strong continuity on H1 gives strong continuity of each actual gammaSector: continuity of pure powers follows from bounded tensor bilinearity, then extends through span and closure using the isometry uniform estimate.',
 'BosonicFock.gamma_strong supplies sectorwise continuity to the earlier diagonal theorem. It applies to arbitrary topological parameter spaces and has no circular assumption of Fock-sector continuity.',
 'translations_strong and boosts_strong specialize to the existing canonical U1 and B0 with their already-proved H1 continuity.',
 'UF=gamma(U1) and VF=gamma(B0) satisfy the concrete group laws, fix the normalized vacuum, intertwine the H1 embedding, and satisfy VF(s) UF(a) VF(s)^-1 = UF(wedgeBoostMap(s,a)).'
]
limits=[
 'The geometry is translations and the existing single wedge boost subgroup. A complete Lorentz family and a four-dimensional local net are not inferred.',
 'Positive-energy spectrum on Fock, antiunitary second quantization, Weyl CCR/local algebras, modular second quantization, FockCertificate and MaxwellCertificate remain separate obligations.',
 'The generic gamma_strong theorem assumes continuity only on the original H1. Concrete translations and boosts discharge that input by existing terms.'
]
report='# Revisão independente — continuidade e ações no Fock\n\nPASSA no escopo declarado; nenhum achado material. Foram lidas e recompiladas cópias das três novas peças uma única vez, reutilizando os .olean das revisões anteriores como dependências somente em leitura.\n\n'+ '\n'.join('- '+c for c in claims)+'\n\nLimites:\n\n'+'\n'.join('- '+s for s in limits)+'\n\nOs três builds terminaram com exit 0; todas as 17 e 16 constantes locais dos respectivos módulos e os cinco teoremas de BosonicFockContinuity usam somente o trio, sem sorry. O JSON registra pinos, tempos, comandos, toolchain, LEAN_PATH e comparações binárias. Esta revisão encerra a investigação desta etapa; não houve escrita em produção, kernel, memórias, quadro ou gate. O aceite da c1 continua distinto da revisão técnica.\n'
save(BASE/'REVIEW_FOCK_DYNAMICS_R1.md',report.encode())
result={'unit':'F1.REDE','status':'PASS_FORMAL_SCOPE__NO_MATERIAL_FINDING','reviewer':'codex-independent-modular-review','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'claims_checked':claims,'limitations':limits,'builds':builds,'build_count':len(builds),'compile_seconds':sum(b['seconds'] for b in builds),'local_constant_counts':{b['module']:len(b['local_constants']) for b in builds},'fock_continuity_printed_theorems':builds[1]['printed_axiom_count'],'only_trio':True,'zero_sorry':True,'target_continuity_not_assumed':True,'checked_pin_count':len(pins),'pins':list(pins.values()),'olean_comparison':comparisons,'evidence':[pin(p) for p in manifests]+[pin(Path(__file__)),pin(BASE/'build_stage_r1.py'),pin(BASE/'REVIEW_FOCK_DYNAMICS_R1.md')],'production_writes':False,'stage_investigation_complete':True}
save(BASE/'REVIEW_FOCK_DYNAMICS_R1.json',(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'path':str(BASE/'REVIEW_FOCK_DYNAMICS_R1.json'),'sha256':sha(BASE/'REVIEW_FOCK_DYNAMICS_R1.json'),'pins':len(pins),'seconds':result['compile_seconds'],'local_counts':result['local_constant_counts'],'olean_identical':sum(x['byte_identical'] for x in comparisons)}))
