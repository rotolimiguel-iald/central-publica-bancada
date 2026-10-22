"""Additive custody of canonical translation reflection, separate from geometric R1."""
from custody_r1 import BASE, pin, save
import json, re

def latest(module):
    rs=[]
    for p in (BASE/'attempts').glob('*/RECEIPT.json'):
        r=json.loads(p.read_text(encoding='utf-8'))
        if r['exit_code']==0 and r['command'][-1].endswith(module+'.lean'):
            rs.append((p,r))
    return max(rs,key=lambda t:t[0].parent.name)

def main():
    p,r=latest('WedgeReflectionTranslations')
    a,ar=latest('AuditTranslations')
    src=p.parent/'WedgeReflectionTranslations.lean'
    if src.read_bytes()!=(BASE/src.name).read_bytes(): raise RuntimeError('source changed')
    raw=(a.parent/'AXIOMS.txt').read_text(encoding='utf-8')
    matches=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",raw)
    allowed={'propext','Classical.choice','Quot.sound'}
    if len(matches)!=8: raise RuntimeError('expected eight declarations')
    for n,axs in matches:
        if not {s.strip() for s in axs.split(',')}<=allowed: raise RuntimeError(n)
    report='''# Reflexão da cunha e translações canônicas

[REAL — Lean 4.31.0, sandbox] WedgeReflectionTranslations prova Jcandidate(U1(a)(Jcandidate f))=U1(jW a)f no H1 original. U1 é o operador canônico, e jW a=(-a0,-a1,a2,a3) é a reflexão diag(-1,-1,+1,+1).

A prova usa a identificação geométrica já entregue, a fase orbital explícita, o pairing (+---), a carta de rapidez e preservação de medida. O sinal da fase é derivado por conjugação complexa; não é assumida covariância como hipótese.

O resultado é uma lei geométrica concreta de reflexão para todas as quatro componentes das translações. Não afirma a representação de Poincare completa nem isotonia/localização da rede de cunhas. Oito declarações auditadas no trio, zero sorry, EXIT 0; logs reais e tentativas preservados. Nenhuma fonte pinada anterior foi alterada.
'''
    rep=save('RELATORIO_TRANSLATIONS_R1.md',report.encode('utf-8'))
    failed=[]
    for q in sorted((BASE/'attempts').glob('*/RECEIPT.json')):
        d=json.loads(q.read_text(encoding='utf-8'))
        if d['exit_code']!=0 and d['command'][-1].endswith('WedgeReflectionTranslations.lean'):
            failed.append({'receipt':pin(q),'log':pin(q.parent/'BUILD.log'),'source':pin(q.parent/src.name)})
    artifacts=[pin(q) for folder in [p.parent,a.parent] for q in sorted(folder.iterdir()) if q.is_file()]
    artifacts += [pin(BASE/n) for n in ['build_translations.py','build_translation_audit.py','custody_translations_r1.py']]
    out={'unit':'F1.REDE','stage':'canonical translation reflection covariance','status':'REAL_COMPILED_SANDBOX__INDEPENDENT_REVIEW_PENDING','build':pin(p),'start_utc':r['start_utc'],'end_utc':r['end_utc'],'seconds':r['seconds'],'exit_code':r['exit_code'],'audit':pin(a),'axiom_count':len(matches),'allowed_axioms':sorted(allowed),'sorry':0,'source':pin(src),'report':rep,'dependency':pin(BASE/'RESULTADO_GEOMETRIC_R1.json'),'artifacts':artifacts,'failed_attempts':failed,'statement':'forall a f, Jcandidate (U1 a (Jcandidate f)) = U1 (wedgeReflection a) f','wedgeReflection':'diag(-1,-1,+1,+1)','scope':'canonical H1 and U1 preserved; full Poincare net not asserted','production_changed':False,'gate_changed':False}
    print(json.dumps(save('RESULTADO_TRANSLATIONS_R1.json',(json.dumps(out,ensure_ascii=False,indent=2)+'\n').encode('utf-8')),ensure_ascii=False))
if __name__=='__main__':main()
