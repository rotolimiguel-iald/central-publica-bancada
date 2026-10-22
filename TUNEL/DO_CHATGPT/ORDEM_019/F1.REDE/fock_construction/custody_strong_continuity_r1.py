"""Custody of the new strong continuity theorem; existing files are read only."""
from pathlib import Path
import hashlib, json, os
BASE=Path(__file__).resolve().parent
FINAL=BASE/'attempts/20261013T223240_502652Z'
DEPENDENCY=BASE/'attempts/20261013T222510_079512Z'

def pin(p):
    return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def save(name,data):
    p=BASE/name
    if p.exists(): raise FileExistsError(p)
    tmp=BASE/(name+'.tmp')
    with tmp.open('xb') as f:
        f.write(data);f.flush();os.fsync(f.fileno())
    if tmp.read_bytes()!=data:raise OSError('byte mismatch')
    tmp.rename(p)
    return pin(p)

def main():
    receipt=json.loads((FINAL/'RECEIPT.json').read_text(encoding='utf-8'))
    if receipt['exit_code']!=0:raise RuntimeError('compile failed')
    source=FINAL/'SectorStrongContinuity.lean'
    if source.read_bytes()!=(BASE/source.name).read_bytes():raise RuntimeError('source changed')
    if (DEPENDENCY/'SectorDirectSum.lean').read_bytes()!=(BASE/'SectorDirectSum.lean').read_bytes():
        raise RuntimeError('frozen dependency changed')
    raw=(FINAL/'AXIOMS.txt').read_text(encoding='utf-8')
    decls=[line.split('\t') for line in raw.splitlines() if line.startswith('LOCAL_DECL\t')]
    if len(decls)!=4 or 'sorryAx' in raw or 'error:' in raw:raise RuntimeError('axiom audit failed')
    allowed={'propext','Classical.choice','Quot.sound'}
    for _,name,axs in decls:
        if not set(axs.split(','))<=allowed:raise RuntimeError(name)
    failed=[]
    for p in sorted((BASE/'attempts').glob('*/RECEIPT.json')):
        r=json.loads(p.read_text(encoding='utf-8'))
        if r['exit_code']!=0 and r['command'][-1].endswith('SectorStrongContinuity.lean'):
            failed.append({'receipt':pin(p),'log':pin(p.parent/'BUILD.log'),'source':pin(p.parent/source.name)})
    report='''# Continuidade forte da soma diagonal de setores

[REAL — Lean 4.31.0, sandbox] SectorStrongContinuity.diagonal_strongly_continuous prova: para A topológico arbitrário e E_n Hilbert completos, se a ação unitária u(a,n) é fortemente contínua em a para cada setor n, então a ação diagonal sobre lp E 2 é fortemente contínua para todo vetor da soma completada.

A prova não assume uniformidade em n. Usa a identidade da norma quadrática como série, a majorante somável 4*norm(f n)^2, Tannery e a continuidade da raiz quadrada. A soma direta congelada é importada sem alterações.

Quatro teoremas locais auditados automaticamente: somente propext, Classical.choice e Quot.sound, zero sorry, EXIT 0. Os avisos de linter indicam hipóteses estruturais não utilizadas em lemas auxiliares; não há erro de compilação. O resultado é condicional à continuidade nos setores, explicitada no enunciado; não fornece por si a construção desses setores.

O recibo de compilação contém comando, toolchain, LEAN_PATH literal, início, fim, segundos e exit code. Duas tentativas falhas anteriores foram preservadas. Memória, quadro, kernel e produção não foram alterados.
'''
    rep=save('RELATORIO_STRONG_CONTINUITY_R1.md',report.encode('utf-8'))
    result={'unit':'F1.REDE','stage':'strong continuity of diagonal sector action','status':'REAL_COMPILED_SANDBOX__REVIEW_PENDING','receipt':pin(FINAL/'RECEIPT.json'),'source':pin(source),'report':rep,'start_utc':receipt['start_utc'],'end_utc':receipt['end_utc'],'seconds':receipt['seconds'],'exit_code':0,'declarations':[d[1] for d in decls],'axioms':sorted(allowed),'sorry':0,'dependency':[pin(DEPENDENCY/n) for n in ['SectorDirectSum.lean','SectorDirectSum.olean','RECEIPT.json']],'artifacts':[pin(p) for p in sorted(FINAL.iterdir()) if p.is_file()]+[pin(BASE/'build_strong_continuity.py'),pin(Path(__file__).resolve())],'failed_attempts':failed,'scope':'Sectorwise strong continuity is an explicit hypothesis. No uniform continuity in the sector index or operator norm is assumed or claimed.','kernel_changed':False,'memory_changed':False,'gate_changed':False}
    print(json.dumps(save('RESULTADO_STRONG_CONTINUITY_R1.json',(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8')),ensure_ascii=False))

if __name__=='__main__':main()
