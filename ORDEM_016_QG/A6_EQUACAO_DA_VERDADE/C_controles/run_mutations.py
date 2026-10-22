from pathlib import Path
from datetime import datetime, timezone
import hashlib, importlib.util, json, subprocess, sys

HERE=Path(__file__).resolve().parent
A6=HERE.parent
ROOT=A6.parent
SOURCE=A6/'A_reproducao/TheEquationOfTruth.lean'
REFERENCE=ROOT.parent/'TUNEL/PARA_CHATGPT/ORDEM_016_INSUMOS/A6_EQUACAO_DA_VERDADE/MEDIDAS_DO_REDATOR/mutantes_C2/GERADOS.json'
KERNEL=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
DEST=HERE/'mutations'
DEST.mkdir(exist_ok=True)

def sha_bytes(raw):return hashlib.sha256(raw).hexdigest()
def save_new(path,value):
    raw=value if isinstance(value,bytes) else json.dumps(value,ensure_ascii=False,indent=2).encode('utf-8')
    if path.exists():
        assert path.read_bytes()==raw, 'Existing artifact differs: '+str(path)
        return
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_bytes(raw)
    assert temp.read_bytes()==raw and raw
    temp.replace(path)

raw=SOURCE.read_bytes();text=raw.decode('utf-8');nl='\r\n' if '\r\n' in text else '\n'
def lines(*items):return nl.join(items)
changes=[
 ('M1',lines('theorem proj_mul_H (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)',''),
       lines('theorem proj_mul_H (H : E →L[𝕜] E)','')),
 ('M2',lines('theorem flowTendsToFamily_of_finiteDimensional (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)',
       '    (hpos : ∀ x, 0 ≤ RCLike.re ⟪x, H x⟫_𝕜) :',''),
       lines('theorem flowTendsToFamily_of_finiteDimensional (H : E →L[𝕜] E) (hH : IsSelfAdjoint H) :','')),
 ('M3','(hlim : FlowTendsToFamily Tf P) (l : X → Y) (hl : Continuous l) :',
       '(hlim : FlowTendsToFamily Tf P) (l : X → Y) :'),
 ('M4','theorem profA_second_deriv_zero : deriv (deriv profA) 0 = -(1 / 4) := by',
       'theorem profA_second_deriv_zero : deriv (deriv profA) 0 = -(1 / 2) := by'),
 ('M5','truthValue 1 1 = 1 ∧ truthValue 0 0 = 1 ∧ truthValue 1 0 = 0 ∧ truthValue 0 1 = 0 := by',
       'truthValue 1 1 = 1 ∧ truthValue 0 0 = 1 ∧ truthValue 1 0 = 1 ∧ truthValue 0 1 = 0 := by')]
mutants={}
for mid,old,new in changes:
    assert text.count(old)==1,(mid,text.count(old))
    mutants[mid]=text.replace(old,new).encode('utf-8')
start=lines('    (penalty D).ker = ⨅ j, (D j).ker := by','')
end=lines('    simp [penalty, h]','')
assert text.count(start)==text.count(end)==1
i=text.index(start)+len(start);j=text.index(end,i)+len(end)
mutants['M6']=(text[:i]+'  sorry'+nl+text[j:]).encode('utf-8')
last='#print axioms TGLExt.EquationOfTruth.profQ_zero\n'
assert text.endswith(last) and text.count(last)==1
fake=lines('','axiom eot_fake : False','theorem eot_uses_fake : (1 : Nat) = 2 := eot_fake.elim','')
mutants['M7a']=(text+fake+'#print axioms eot_uses_fake'+nl).encode('utf-8')
mutants['M7b']=(text+fake).encode('utf-8')
reference=json.loads(REFERENCE.read_bytes())
generated={}
for mid,body in mutants.items():
    assert sha_bytes(body)[:16]==reference[mid]['sha16'], (mid,'reference hash mismatch')
    folder=DEST/mid;folder.mkdir(exist_ok=True)
    path=folder/('TheEquationOfTruth'+mid+'.lean')
    save_new(path,body)
    generated[mid]=dict(source=str(path),source_sha256=sha_bytes(body),bytes=len(body),
        reference_sha16=reference[mid]['sha16'],matches_reference=True)
save_new(DEST/'generated.json',dict(original_sha256=sha_bytes(raw),reference_sha256=sha_bytes(REFERENCE.read_bytes()),mutants=generated))
if '--generate-only' in sys.argv:
    print(json.dumps(dict(generated=len(generated),all_reference_hashes_match=True)));sys.exit(0)

spec=importlib.util.spec_from_file_location('audit',ROOT/'A0/auditar_axiomas.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
results=[]
for mid,entry in generated.items():
    source=Path(entry['source']);label='mutation_'+mid
    receipt=source.parent/(label+'.json');log=source.parent/(label+'.log')
    if not receipt.exists():
        assert not (source.parent/(label+'.marker')).exists(), 'Uncertain prior run; do not repeat'
        command=[sys.executable,'-X','utf8','-B',str(ROOT/'A0/compile_isolated_v2.py'),str(KERNEL),str(source),label]
        wrapped=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        save_new(source.parent/'runner_output.txt',wrapped.stdout)
        assert wrapped.returncode==0 and receipt.exists(), (mid,'runner failed')
    r=json.loads(receipt.read_bytes())
    assert r['source_sha256']==sha_bytes(source.read_bytes()) and r['log_sha256']==sha_bytes(log.read_bytes())
    a=audit.audita(str(source),str(log))
    save_new(source.parent/'audit.json',a)
    if mid in ['M1','M2','M3','M4','M5']:
        detected=r['rc']!=0 and a['auditoria']=='FALHA' and a['n_erros']>0
    elif mid=='M6':
        detected=r['rc']==0 and a['auditoria']=='FALHA' and a['sorry'] and 'sorry' in a['tokens_proibidos_na_fonte']
    elif mid=='M7a':
        detected=r['rc']==0 and a['auditoria']=='FALHA' and bool(a['fora_do_trio']) and 'axiom' in a['tokens_proibidos_na_fonte']
    else:
        detected=r['rc']==0 and a['auditoria']=='FALHA' and bool(a['sem_print_axioms']) and 'axiom' in a['tokens_proibidos_na_fonte']
    item=dict(id=mid,generated=entry,receipt=r,audit=a,detected=detected)
    save_new(source.parent/'verified.json',item)
    results.append(item)
    print(json.dumps(dict(id=mid,rc=r['rc'],audit=a['auditoria'],detected=detected,wall_seconds=r['wall_seconds'])),flush=True)
    if not detected:
        raise RuntimeError('Mutation escaped expected detection; stop dependents: '+mid)
save_new(DEST/'results.json',dict(status='REAL_EXPECTED_REJECTIONS',results=results,detected=sum(x['detected'] for x in results),
    wall_seconds=sum(x['receipt']['wall_seconds'] for x in results)))
print('ALL_MUTATIONS_DETECTED',len(results),flush=True)
