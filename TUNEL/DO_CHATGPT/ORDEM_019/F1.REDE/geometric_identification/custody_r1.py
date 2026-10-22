"""Pin the exact geometric identification; never overwrite an existing receipt."""
from pathlib import Path
import datetime, hashlib, json, os, re
BASE=Path(__file__).resolve().parent
FINAL={"FourierConjugation":"20261013T221637_926790Z","GeometricIdentification":"20261013T221808_560069Z","AuditGeometric":"20261013T221858_425532Z"}
def pin(p):
    return {"path":str(p),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
def save(name,data):
    p=BASE/name
    if p.exists(): raise FileExistsError(p)
    tmp=BASE/(name+'.tmp')
    with tmp.open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    if tmp.read_bytes()!=data: raise OSError('byte mismatch')
    tmp.rename(p)
    return pin(p)
def main():
    artifacts=[]; modules=[]; deps={}
    for module,stamp in FINAL.items():
        d=BASE/'attempts'/stamp
        r=json.loads((d/'RECEIPT.json').read_text(encoding='utf-8'))
        if r['exit_code']!=0: raise RuntimeError(module)
        if (d/(module+'.lean')).read_bytes()!=(BASE/(module+'.lean')).read_bytes(): raise RuntimeError('source changed')
        modules.append({'module':module,'receipt':pin(d/'RECEIPT.json'),'source':pin(d/(module+'.lean')),'exit_code':r['exit_code'],'seconds':r['seconds'],'start_utc':r['start_utc'],'end_utc':r['end_utc']})
        artifacts += [pin(p) for p in sorted(d.iterdir()) if p.is_file()]
        for dep in r['read_only_dependency_paths']:
            p=Path(dep)/'RECEIPT.json'
            if p.is_file(): deps[str(p)]=pin(p)
    raw=(BASE/'attempts'/FINAL['AuditGeometric']/'AXIOMS.txt').read_text(encoding='utf-8')
    matches=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",raw)
    decl=json.loads((BASE/'LOCAL_DECLARATIONS.json').read_text(encoding='utf-8'))
    if {n for n,_ in matches}!=set(decl['names']): raise RuntimeError('incomplete audit')
    allowed={'propext','Classical.choice','Quot.sound'}
    for n,axs in matches:
        if not {s.strip() for s in axs.split(',')}<=allowed: raise RuntimeError(n)
    if 'sorryAx' in raw or 'error:' in raw: raise RuntimeError('axiom failure')
    report='''# F1.REDE — identificação geométrica da conjugação

[REAL — Lean 4.31.0, sandbox] Duas fontes novas e a sonda de axiomas compilam com EXIT 0. Todas as 22 declarações locais usam só propext, Classical.choice e Quot.sound; zero sorry. Os recibos incluem início, fim, segundos, comando, toolchain, LEAN_PATH literal e hashes.

FourierConjugation prova, para antiunitária involutiva num Hilbert complexo, F(Cf)(xi)=C(Ff(-xi)). A identidade é demonstrada primeiro no integral de Bochner e nas funções de Schwartz, depois estendida a todo L² por densidade e continuidade. A relação com Fourier não é hipótese.

GeometricIdentification constrói productJ independentemente do Jcandidate anterior: reflexão do vetor transversal q, conjugação das componentes e troca de helicidades, mantendo a rapidez r. A medida produto é preservada. A currificação de Fubini entrelaça essa ação com a antiunitária da fibra.

Resultados exatos: Jcandidate_rapidity e Jcandidate_eq_geometricJ identificam operadores L²; Jcandidate_rapidity_coordinates prova, quase em toda parte na medida produto, (toRapidity(Jcandidate f))(q,r,i)=star((toRapidity f)(-q,r,helicitySwap i)). O H1 e a carta canônica não foram alterados.

[OPEN] A covariância completa de Poincare, a identificação da localização dos subespaços em todas as cunhas e a rede 4D são obrigações posteriores. Esta entrega paga a fórmula geométrica da antiunitária na carta de rapidez. Não integra produção, não altera o kernel, memória, quadro ou gate; a raiz coordena os registros e a revisão independente.
'''
    rep=save('RELATORIO_GEOMETRIC_R1.md',report.encode('utf-8'))
    artifacts += [pin(p) for p in sorted(BASE.glob('*.py'))]+[pin(BASE/'LOCAL_DECLARATIONS.json')]
    result={'unit':'F1.REDE','stage':'exact geometric identification of spectral antiunitary','status':'REAL_COMPILED_SANDBOX__INDEPENDENT_REVIEW_PENDING','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'modules':modules,'axiom_count':len(matches),'allowed_axioms':sorted(allowed),'sorry':0,'report':rep,'artifacts':artifacts,'dependency_receipts':list(deps.values()),'proved':['Fourier-pointwise antiunitary identity on entire L2 via Schwartz density','canonicalFub_productJ: equality of L2 operators','Jcandidate_rapidity: toRapidity(Jcandidate f)=productJ(toRapidity f)','Jcandidate_eq_geometricJ, with independently defined geometricJ','Jcandidate_rapidity_coordinates: q negated, r fixed, components conjugated and swapped'],'open':['full Poincare covariance','geometric localization in all wedges','four-dimensional net'],'source_changes_to_previous_delivery':False,'kernel_changed':False,'gate_changed':False,'memory_changed':False}
    out=save('RESULTADO_GEOMETRIC_R1.json',(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    print(json.dumps(out,ensure_ascii=False));print(json.dumps(rep,ensure_ascii=False))
if __name__=='__main__':main()
