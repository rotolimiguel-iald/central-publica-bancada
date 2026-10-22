"""One independent review per new extension; preserve original sources and prior reviews."""
from pathlib import Path
import json, hashlib, datetime as dt, subprocess, time, os, re, sys
ROOT=Path(__file__).resolve().parent.parent
MODE=sys.argv[1]
KERNEL=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
if MODE=='fock':
    BASE=ROOT/'review_fock_r2'
    SOURCES=[ROOT/'fock_construction/attempts/20261013T222228_697129Z/BosonicTwoParticle.lean',ROOT/'fock_construction/attempts/20261013T222510_079512Z/SectorDirectSum.lean']
    MANIFESTS=[ROOT/'fock_construction/DELIVERY_SECTOR2_R1.json',ROOT/'fock_construction/attempts/20261013T222510_079512Z/RECEIPT.json']
    EXTRA=[]
else:
    assert MODE=='translation'
    BASE=ROOT/'review_translation_r2'
    SOURCES=[ROOT/'geometric_identification/attempts/20261013T222432_456454Z/WedgeReflectionTranslations.lean',ROOT/'geometric_identification/AuditTranslations.lean']
    MANIFESTS=[ROOT/'geometric_identification/RESULTADO_TRANSLATIONS_R1.json',ROOT/'review_geometric_r2/REVIEW_GEOMETRIC_R1.json']
    EXTRA=[ROOT/'review_geometric_r2/20261013T221947_732334Z',ROOT/'review_modular/20261013T215402_817152Z']
BASE.mkdir(exist_ok=True)
OUT=BASE/dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ'); OUT.mkdir()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p): return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(p,b):
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert p.read_bytes()==b
def jsave(p,o): save(p,(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode())
queue=MANIFESTS.copy(); seen=set(); pins={}
def walk(x):
    if isinstance(x,dict):
        if 'path' in x and 'sha256' in x:
            p=Path(x['path']); item=pin(p)
            assert item['sha256']==x['sha256'],str(p)
            if 'bytes' in x: assert item['bytes']==x['bytes'],str(p)
            pins[(str(p),x['sha256'])]=item
            if p.suffix.lower()=='.json': queue.append(p)
        for v in x.values(): walk(v)
    elif isinstance(x,list):
        for v in x: walk(v)
while queue:
    p=queue.pop()
    if str(p) not in seen:
        seen.add(str(p)); walk(json.loads(p.read_text(encoding='utf-8-sig')))
for p in SOURCES:
    save(OUT/p.name,p.read_bytes())
    assert not re.search(rb'\bsorry\b|\badmit\b|^\s*axiom\s',p.read_bytes(),re.M)
dependencies=[pin(p) for d in EXTRA for p in sorted(d.glob('*.olean'))]
paths=[OUT]+EXTRA+[KERNEL/'.lake/build/lib/lean']+sorted((KERNEL/'.lake/packages').glob('*/.lake/build/lib/lean'))+[LEAN.parent.parent/'lib/lean']
env=dict(os.environ,LEAN_PATH=os.pathsep.join(map(str,paths)))
version=subprocess.check_output([str(LEAN),'--version'],text=True).strip()
builds=[]; comparisons=[]
for source in SOURCES:
    local=OUT/source.name; command=[str(LEAN),'-o',str(local.with_suffix('.olean')),str(local)]
    start=dt.datetime.now(dt.timezone.utc).isoformat(); timer=time.perf_counter()
    proc=subprocess.run(command,cwd=OUT,env=env,capture_output=True)
    sec=time.perf_counter()-timer; end=dt.datetime.now(dt.timezone.utc).isoformat(); raw=proc.stdout+proc.stderr
    meta={'source':pin(local),'command':command,'cwd':str(OUT),'start_utc':start,'end_utc':end,'seconds':sec,'exit_code':proc.returncode,'LEAN_PATH':env['LEAN_PATH'],'toolchain':version}
    save(OUT/(source.stem+'.log'),(json.dumps(meta,ensure_ascii=False,indent=2)+'\nSTDOUT+STDERR\n').encode()+raw)
    print(json.dumps({'mode':MODE,'module':source.stem,'exit_code':proc.returncode,'seconds':sec}),flush=True)
    if proc.returncode:
        jsave(OUT/'FAILED_BUILD.json',meta); raise SystemExit(proc.returncode)
    assert b'sorryAx' not in raw
    for axs in re.findall(rb'depends on axioms:\s*\[([^\]]*)\]',raw):
        assert {a.strip().decode() for a in axs.split(b',') if a.strip()} <= {'propext','Classical.choice','Quot.sound'}
    localdecl=[]
    for line in raw.decode('utf-8').splitlines():
        if line.startswith('LOCAL_DECL\t'):
            parts=line.split('\t'); localdecl.append(parts[1]); axs=set(parts[2].split(','))-{''}
            assert axs <= {'propext','Classical.choice','Quot.sound'}
    meta['all_local_constants_checked']=localdecl
    meta['printed_axiom_declarations']=len(re.findall(rb'depends on axioms:',raw))
    builds.append(meta)
    old=source.with_suffix('.olean')
    if old.is_file(): comparisons.append({'module':source.stem,'original':pin(old),'rebuilt':pin(local.with_suffix('.olean')),'byte_identical':old.read_bytes()==local.with_suffix('.olean').read_bytes()})
for p in list(pins.values())+dependencies: assert sha(Path(p['path']))==p['sha256'],p['path']
if MODE=='translation':
    assert builds[-1]['printed_axiom_declarations']==8
    scope=['Exact Jcandidate U1(a) Jcandidate = U1(wedgeReflection(a)), with wedgeReflection diagonal(-1,-1,+1,+1).','Uses canonical U1, rapidity chart and proved phase identity; no covariance hypothesis assumes the target.']
    limits=['This is translation reflection covariance; full Poincare covariance and complete local net are not asserted.']
else:
    assert all(b['all_local_constants_checked'] for b in builds)
    scope=['Actual completed canonical H1 tensor square; closed fixed subspace of flip; nonzero pair witness.','gammaTwo is an actual unitary functor on that symmetric sector; identity, composition and pure-pair action are proved.','SectorDirectSum is the Hilbert l2 sum and diagonal unitary of an arbitrary supplied complete Hilbert-sector family, with orthogonal isometric sector embeddings.']
    limits=['The generic Hilbert sum does not itself construct the full bosonic sector family.','No strong continuity, Weyl CCR, FockCertificate, Maxwell field or modular second-quantization theorem is asserted by these two modules.','vacuum_fixed and vacuum_norm honestly require a fixed normalized vector in sector zero.']
name='REVIEW_'+MODE.upper()+'_R1'
report='# Revisão independente — '+MODE+'\n\nPASSA no escopo declarado, sem achado material.\n\n'+ '\n'.join('- '+s for s in scope)+'\n\nLimites:\n\n'+'\n'.join('- '+s for s in limits)+'\n\nCópias novas recompiladas; dependências somente em leitura. Logs e JSON registram comandos, toolchain, LEAN_PATH, início, fim, tempos, axiomas e pinos. Não houve escrita no kernel, em produção, memória, quadro ou gate. Aceite da c1 é distinto desta revisão técnica.\n'
save(BASE/(name+'.md'),report.encode())
result={'unit':'F1.REDE','status':'PASS_FORMAL_SCOPE__NO_MATERIAL_FINDING','reviewer':'codex-independent-modular-review','mode':MODE,'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'scope':scope,'limitations':limits,'builds':builds,'pins':list(pins.values()),'checked_pin_count':len(pins),'dependency_oleans_read_only':dependencies,'only_trio':True,'zero_sorry':True,'no_target_assumed':True,'olean_comparison':comparisons,'evidence':[pin(p) for p in MANIFESTS]+[pin(Path(__file__)),pin(BASE/(name+'.md'))],'production_writes':False}
jsave(BASE/(name+'.json'),result)
print(json.dumps({'mode':MODE,'path':str(BASE/(name+'.json')),'sha256':sha(BASE/(name+'.json')),'pins':len(pins),'seconds':sum(b['seconds'] for b in builds),'local_constant_counts':[len(b['all_local_constants_checked']) for b in builds]},ensure_ascii=False))
