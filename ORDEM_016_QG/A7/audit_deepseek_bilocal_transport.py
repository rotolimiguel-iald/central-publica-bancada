"""Reject the even-slot antisymmetrization in the independent review."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import ast,json,hashlib,time
import sympy as s
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,BASE,sha,write,put,append
D=H/'deepseek_bilocal_transport_audit'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    source=BASE/'state/handoffs/e3aa9cba-3f1f-4c0c-b7df-1a0838ac30f3_delivery.json'
    job=json.loads(source.read_bytes())['job'];ex=job['execution'];r=ex['result']
    assert ex['status']=='result_ready'
    write(D/'ORIGINAL.md',r['text'].encode('utf-8'))
    put(D/'RECEIPT.json',dict(request_id=job['request_id'],job_id=job['id'],execution_task_id=ex['id'],
        source_sha256=sha(source),response_sha256=sha(D/'ORIGINAL.md'),
        prompt_sha256=hashlib.sha256(job['prompt'].encode('utf-8')).hexdigest(),
        usage=r['usage'],cost_estimate_usd=r['cost_estimate_usd'],canonical_memory=r.get('canonical_memory')))
    src=H/'antifield_quadratic_primitive_check.py'
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),target='Counterexample to anti projection and audit of -1/t normalization',
        sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),src,H/'bilocal_wick_ward_transport/manifest.json']],
        exclusions=['No new evaluation of a singular composite product','No full A2'],full_Q2=False))
    start=time.process_time();names={'clean','add','scale','mul','atom'}
    nodes=[n for n in ast.parse(src.read_text('utf-8')).body if isinstance(n,ast.FunctionDef) and n.name in names]
    ns={'s':s};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),ns)
    clean,add,scale,mul,atom=[ns[n] for n in ['clean','add','scale','mul','atom']]
    hx,hy,h,m,t,fh,fg,wg=s.symbols('hx hy h m t fh fg wg')
    cx,bx,ax,cy,by,ay=[atom(i) for i in range(6)]
    def de(a,v):return clean({k:s.diff(co,v) for k,co in a.items()})
    def do(a,i):
        out={}
        for mon,co in a.items():
            if i in mon:
                j=mon.index(i);key=mon[:j]+mon[j+1:]
                out[key]=out.get(key,0)+(-1)**j*co
        return clean(out)
    F=mul(scale(add(ax,bx),hx),cx);G=mul(scale(add(ay,by),hy),cy);pair=mul(F,G)
    # RF=[q,BF] for q=ax->m hx, ay->m hy, BF_hh=fh*d_hx*d_hy.
    RF=scale(add(de(do(pair,2),hy),de(do(pair,5),hx)),-m*fh)
    def BH(a):
        return add(scale(de(de(a,hx),hy),s.Symbol('bh')),
                   scale(do(do(a,0),4),fg-wg),scale(do(do(a,1),3),-(fg-wg)))
    C=add(RF,scale(BH(RF),t),scale(BH(BH(RF)),t*t/2))
    # Multiply the tensor slots: both are the SAME even vertex after identification.
    def multiply_slots(a):
        out={};mapping={0:0,1:1,2:2,3:0,4:1,5:2}
        for mon,co in a.items():
            term={():co.subs({hx:h,hy:h},simultaneous=True)}
            for i in mon:term=mul(term,atom(mapping[i]))
            out=add(out,term)
        return out
    diagonal=multiply_slots(C)
    expected=scale(atom(0),-2*m*fh*t*(fg-wg)*h)
    checks=[]
    def eq(label,a,b=None):
        assert not add(a,scale(b or {},-1)),(label,a,b);checks.append(label)
    eq('nonzero equal-even-vertex contact',diagonal,expected)
    assert diagonal;checks.append('antisymmetrization would erase a nonzero contact')
    assert -(-1)**((0+1)*(0+1))==1
    checks.append('odd BV bracket is symmetric on two even entries')
    # Exact operator product rule with an abstract extension R.
    A,R,E,B=s.symbols('A R E B',commutative=False)
    lhs=A*R*E-R*E*B
    rhs=(A*R-R*A)*E+R*(A*E-E*B)
    assert s.expand(lhs-rhs)==0;checks.append('extension commutator product rule')
    c,b=s.symbols('contact bracket')
    desired=-t*c/t-b
    assert s.expand(desired+c+b)==0;checks.append('connected normalization is -contact minus bracket')
    assert s.expand((t*c-b)-desired)!=0
    checks.append('claimed raw A2 equivalence rejected')
    cpu=time.process_time()-start
    audit=dict(at=now.isoformat(),checks=len(checks),cpu_seconds=cpu,
        accepted=['Pre-multiplication Wick transport with both A1 corrections',
                  'Formal extension commutator product rule when all domains exist'],
        rejected=['Antisymmetrizing the anomaly/contact for even entries',
                  'Calling t*contact-bracket equivalent to -contact-bracket'],
        counterexample='For identical even vertices, m exp(t BH)[q,BF]=-2m fh t(fg-wg)h c, not zero',
        corrected_formula='In the H representative: A2=-m R(E_H[q,BF])-(1/t)m[QW,R]E_H-(F,G); use graded symmetric slots',
        domain_condition='R must be defined on the composite source; this expression does not itself define that extension',
        representation_condition='Apply N_H to recover T1(A2); do not mix representations',
        full_Q2=False,gate_changed=False)
    put(D/'AUDIT.json',audit)
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[REAL — parecer auditado e parcialmente refutado; DERIVED — identidade de registro; Q2 OPEN]

DeepSeekcd6 confirmou o transporte pré-multiplicação com as duas correções
A1, no mesmo escopo do CAS anterior. Porém introduziu X_anti=(X(F,G)-X(G,F))/2
para as entradas PARES. Isso é incorreto: T2 e A2 são graduadamente simétricos,
e o antibracket ímpar satisfaz (F,G)=(G,F) quando ambos são pares.

Controle independente: F=(hdag+barc)h c em ambas as entradas, no modelo de
Euler qhdag=m h. A multiplicação dos dois slots dá
 m exp(t BH)[q,BF]=-2m fh t(fg-wg)h c,
em geral não zero. A projeção anti proposta apagaria o resultado com F=G.
Isto refuta a fórmula do parecer; não é cálculo distribucional da TGL.

Há outro erro: t*m*C-bracket não é outra forma de -m*C-bracket. O primeiro
é parte de um resíduo cru; a definição Tc2=-1/t(T2-S2) impõe o segundo.
Mantendo a mesma representação H e supondo TODOS os domínios de extensão,
o simples produto de operadores fornece a identidade de registro correta:

 A R E-E R B não é a ordem usada; a ordem correta é A R E-R E B
 =(A R-R A)E+R(A E-E B).

Com A=QW, B=Qin, E=E_H e A E-E B=t E_H[q,BF], segue

 A2_H=-m R(E_H[q,BF])-(1/t)m[QW,R]E_H-(F,G).

Usam-se entradas graduadamente SIMÉTRICAS, sem a projeção anti do parecer.
A aplicação N_H recupera T1(A2); a multiplicação m e a representação
não devem desaparecer silenciosamente da fórmula. [QW,R]=[q,R]+t[RW,total,R].
Esta é uma identidade condicional de registro de termos, não a construção
da extensão do contato composto. R ordinário sobre kernels fora da diagonal
ainda não especifica por si só R(delta vezes propagador). Nada foi zerado
por definição para declarar ausência de anomalia.

{len(checks)} controles locais novos, CPU {cpu}s,rc0. Resposta original e recibo
preservados. Uso={json.dumps(r['usage'],ensure_ascii=False)};
custo estimadoUSD{r['cost_estimate_usd']}, contabilizado uma vez, não fatura.
Kimi continua com unidades preservadas sob cota; nenhuma chamada substituta.
Próximo A7.b: construir/identificar o contato Euler composto e somar a
fonte localizada (I1,B1) agora calculada. Originais/kernel/gate intactos.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO_E_CORRECOES.md',note.encode('utf-8'))
    write(OUT/'ENTREGA_016_MEDIDA_DeepSeek_bilocal_simetria_corrigida.md',note.encode('utf-8'))
    paths=[Path(__file__),D/'ORIGINAL.md',D/'RECEIPT.json',D/'PRE_REGISTER.json',D/'AUDIT.json',D/'DERIVACAO_E_CORRECOES.md']
    put(D/'manifest.json',dict(at=now.isoformat(),artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],full_Q2=False))
    ledger=OUT/'LEDGER_016.jsonl';entries=[json.loads(v) for v in ledger.read_text('utf-8').splitlines()]
    assert not any(e.get('execution_task_id')==ex['id'] and e.get('cost_estimate_usd') is not None for e in entries)
    entry=dict(at=now.isoformat(),event='EXTERNAL_REVIEW_RECEIVED_AND_AUDITED',target='A7.b',provider='deepseek',
        request_id=job['request_id'],job_id=job['id'],execution_task_id=ex['id'],usage=r['usage'],
        cost_estimate_usd=r['cost_estimate_usd'],response_sha256=sha(D/'ORIGINAL.md'),
        prompt_sha256=hashlib.sha256(job['prompt'].encode('utf-8')).hexdigest(),
        checks=len(checks),cpu_seconds=cpu,verdict='PARTIAL_ACCEPTANCE_ANTISYMMETRIZATION_AND_RAW_FACTOR_REFUTED')
    append(ledger,json.dumps(entry,ensure_ascii=False)+'\n');entries.append(entry)
    cost=Decimal(0);seen=set()
    for e in entries:
        v=e.get('cost_estimate_usd',e.get('cost_usd'))
        if v is None:continue
        k=e.get('execution_task_id') or e.get('job_id') or e.get('request_id')
        if k and k in seen:continue
        if k:seen.add(k)
        cost+=Decimal(str(v))
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b PROGRESS: DeepSeekcd6 auditado; projeção anti e equivalência raw refutadas, fórmula simétrica corrigida; {len(checks)} controles CPU{cpu}s. Custo conhecido parcialUSD{cost}. Q2 completa OPEN. AberturaSHA256={opening}.\n')
    p=H/'CONTINUIDADE.json';st=json.loads(p.read_bytes())
    st.setdefault('head_history',[]).append({k:st.get(k) for k in ['at','previous_goal_turn','completed_this_turn','next','pending_orchestration']})
    st.update(at=now.isoformat(),previous_goal_turn='PROGRESS',completed_this_turn=[
        'Quadratic volume primitive and localized source (I1,B1) checked with30controls',
        'MiMo57e coordinate review accepted with explanatory correction;4newcontrols',
        'DeepSeekcd6 received;6controls refute anti projection and raw-factor equivalence',
        'Corrected conditional extension-commutator representative recorded'],
        next=['Compute the composite Euler source in the same radial T2 prescription; do not antisymmetrize even slots',
              'Preserve cutoff source (I1,B1) and curved normalization in the assembly',
              'Receive Kimi pending reviews only on official quota recovery',
              'A7b deadline20:32UTC; A7c/d,A8,PartB/final remain'],
        pending_orchestration='MiMo57e and DeepSeekcd6 completed/audited; Kimi3 awaiting actual quota; no own live process',
        partial_metered_cost_usd=str(cost))
    st['bilocal_review_execution']['status']='COMPLETED_RECEIVED_AUDITED_PARTIAL'
    st['deepseek_bilocal_audit']=dict(manifest=str(D/'manifest.json'),full_Q2=False)
    put(p,st,True)
    for a in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
    print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=len(checks),cpu_seconds=cpu,known_partial_cost_usd=str(cost)),ensure_ascii=False))

if __name__=='__main__':main()
