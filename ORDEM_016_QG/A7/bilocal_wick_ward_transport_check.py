"""Exact finite Grassmann test of the two-slot Wick/Ward transport identity."""
from pathlib import Path
from datetime import datetime, timezone
import ast, json, time
import sympy as s
from deliver_nonminimal_wick_and_mimo_audit import H, OUT, sha, write, put, append

D=H/'bilocal_wick_ward_transport'

def main():
    D.mkdir(exist_ok=False)
    src=H/'antifield_quadratic_primitive_check.py'
    paths=[Path(__file__),src,H/'wick_arity_one_graded_commutator/results.json',
           H/'linear_anomaly_insertion/results.json',H/'linear_slot_distributional_normalization/results.json']
    now=datetime.now(timezone.utc)
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        target='Two-slot Ward source transport with both arity-one corrections retained',
        hypotheses=['Free q is a linear odd derivation',
            'Wick contraction operators are even constant-coefficient second derivatives',
            'Same W used in single-slot, cross-slot and output normal ordering'],
        model='Two copies of one bosonic Euler field with antifield and spectator ghost pair; finite graded coefficient control only',
        negative_controls=['Omit input R_x','Omit input R_y','Mismatch output Wick contraction'],
        exclusions=['Not the full BRST complex','Not extension of delta times a singular propagator',
                    'Not proof of a global equivariant state or complete A2'],
        sources=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    start=time.process_time()
    names={'clean','add','scale','mul','atom'}
    nodes=[n for n in ast.parse(src.read_text('utf-8')).body
           if isinstance(n,ast.FunctionDef) and n.name in names]
    ns={'s':s};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),ns)
    clean,add,scale,mul,atom=[ns[n] for n in ['clean','add','scale','mul','atom']]
    even=lambda a:clean({():a})
    hx,hy,m,t=s.symbols('hx hy m t')
    wx,wy,wxy,wg,fh,fg=s.symbols('wx wy wxy wg fh fg')
    # Global odd ordering implements the graded tensor product automatically.
    cx,bx,ax,cy,by,ay=[atom(i) for i in range(6)]
    def de(a,v):return clean({k:s.diff(c,v) for k,c in a.items()})
    def do(a,i):
        out={}
        for mon,c in a.items():
            if i in mon:
                j=mon.index(i);key=mon[:j]+mon[j+1:]
                out[key]=out.get(key,0)+(-1)**j*c
        return clean(out)
    def q(a):return add(scale(do(a,2),m*hx),scale(do(a,5),m*hy))
    def CWx(a):return scale(de(de(a,hx),hx),wx/2)
    def CWy(a):return scale(de(de(a,hy),hy),wy/2)
    # Cross ghost contraction convention: c_x barc_y -> +wg,
    # barc_x c_y -> -wg. It is graded symmetric under exchanging slots.
    def cross(a,hh,ghost):
        return add(scale(de(de(a,hx),hy),hh),
                   scale(do(do(a,0),4),ghost),scale(do(do(a,1),3),-ghost))
    BW=lambda a:cross(a,wxy,wg)
    BF=lambda a:cross(a,fh,fg)
    BH=lambda a:add(BF(a),scale(BW(a),-1))
    CW=lambda a:add(CWx(a),CWy(a),BW(a))
    def comm(C,a):return add(q(C(a)),scale(C(q(a)),-1))
    Rx=lambda a:comm(CWx,a)
    Ry=lambda a:comm(CWy,a)
    RW=lambda a:comm(CW,a)
    RF=lambda a:comm(BF,a)
    def expB(a):
        out=a;term=a
        for n in range(1,6):
            term=BH(term)
            if not term:return out
            out=add(out,scale(term,t**n/s.factorial(n)))
        raise AssertionError('polynomial degree bound insufficient')
    checks=[]
    def eq(label,a,b=None):
        assert not add(a,scale(b or {},-1)),(label,a,b)
        checks.append(label)
    def rendered(a):return [dict(odd=list(k),coefficient=str(v)) for k,v in a.items()]
    Xaf=mul(mul(ax,even(hx)),cx);Yaf=mul(mul(ay,even(hy)),cy)
    Xgh=mul(mul(bx,even(hx)),cx);Ygh=mul(mul(by,even(hy)),cy)
    X=add(Xaf,Xgh);Y=add(Yaf,Ygh)
    eq('X arity-one Euler correction',Rx(X),scale(cx,-m*wx))
    eq('Y arity-one Euler correction',Ry(Y),scale(cy,-m*wy))
    probes=[('af-gh',mul(Xaf,Ygh)),('gh-af',mul(Xgh,Yaf)),
            ('combined',mul(X,Y)),('af-af',mul(Xaf,Yaf)),
            ('unequal polynomial',mul(add(X,even(hx**3)),add(Y,even(hy**2))))]
    missing={}
    for label,a in probes:
        eq('nilpotent '+label,q(q(a)))
        eq('constant commutator '+label,add(BH(RW(a)),scale(RW(BH(a)),-1)))
        eq('transported generator nilpotent '+label,
           add(q(q(a)),scale(q(RW(a)),t),scale(RW(q(a)),t),scale(RW(RW(a)),t*t)))
        qin=add(q(a),scale(add(Rx(a),Ry(a)),t))
        out=expB(a)
        lhs=add(q(out),scale(RW(out),t),scale(expB(qin),-1))
        rhs=scale(expB(RF(a)),t)
        eq('bilocal Ward transport '+label,lhs,rhs)
        # Isolate the first-order Ward source before its cross-contraction dressing.
        first=add(comm(BH,a),comm(BW,a))
        eq('W-independent source '+label,first,RF(a))
        if label=='combined':
            for name,Rslot in [('x',Rx),('y',Ry)]:
                defect=scale(expB(Rslot(a)),t)
                assert defect,(name,defect)
                checks.append('missing input correction rejected '+name)
                missing[name]=rendered(defect)
            wrong_output=scale(expB(comm(BW,a)),-t)
            assert wrong_output
            checks.append('output normal ordering mismatch rejected')
            missing['output']=rendered(wrong_output)
    # The dressing remains W dependent: source independence is not A2 independence.
    dressed=scale(expB(RF(mul(X,Y))),t)
    dependence=clean({k:s.diff(v,wg) for k,v in dressed.items()})
    assert dependence
    checks.append('dressed contact need not be W independent')
    data=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),
        cpu_seconds=time.process_time()-start,
        identity='(q+t R_W,total) exp(t B_H) - exp(t B_H)(q+t R_W,x+t R_W,y) = t exp(t B_H)[q,B_F]',
        definitions='B_H=B_F-B_W,cross; R_W,total=[q,C_W,x+C_W,y+B_W,cross]',
        source_identity='[q,B_H]+R_W,cross=[q,B_F]',
        negative_residuals=missing,
        interpretation='Input arity-one terms cancel the spurious cross Wick-change source, not the full dressed contact',
        remaining_contact='exp(t B_H)[q,B_F] contains singular composite Euler contacts requiring the declared extension',
        full_Q2=False,gate_changed=False)
    put(D/'results.json',data)
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[INPUT/ONTO — fala do operador; DERIVED+CAS — transporte de Ward entre duas entradas]

Fala do operador, verbatim: «Exatamente, aquilo que satisfaz a leitura do conteúdo para afirmá-lo como reconhecido pela forma».

O reconhecimento é aqui aplicado como compatibilidade entre a leitura de Wick
e o diferencial livre. Não acrescentamos um operador ao motor. Conservamos
as correções de uma entrada já identificadas, inclusive nos dois argumentos.

Escreva t=i hbar e decomponha a contração suave W em Cx+Cy+BW, sendo BW
a contração cruzada. Ponha RW=[q,Cx+Cy+BW], Rx=[q,Cx], Ry=[q,Cy].
O produto temporal, expresso na leitura local H, contém exp(t BH), com
BH=BF-BW. BF é a contração temporal na referência anterior; não é a ação
efetiva 1PI. Esta escrita exige a mesma W nas entradas e na saída.

Como q é linear e as contrações são operadores pares de segunda ordem com
coeficientes independentes dos campos, os comutadores com q são de segunda
ordem e comutam com essas contrações. Portanto, por conjugação exata,

 (q+t RW) exp(t BH) - exp(t BH)(q+t Rx+t Ry)
 =t exp(t BH)([q,BH]+[q,BW])
 =t exp(t BH)[q,BF].

Essa é uma igualdade de operadores no produto tensorial graduado, antes da
multiplicação dos campos. A multiplicação transporta RW total à correção
de Wick na saída. O termo do lado direito é a fonte de Ward temporal;
quando BF usa o Green livre adequado, inclui os contatos de Euler.

A identidade mostra exatamente onde entram AS DUAS correções A1: a fonte
espúria -[q,BW] é compensada por +[q,BW]. Omitir Rx ou Ry deixa, respectivamente,
t exp(t BH)Rx ou t exp(t BH)Ry. No modelo finito de controle ambos são não
zero. É inadequado comparar representações com apenas uma dessas correções.

Precisão essencial: só a FONTE [q,BF] perdeu W. O fator exp(t BH) ainda
depende da representação. O CAS também rejeita a afirmação mais forte de
independência total. Na teoria distribucional esse fator aplicado ao contato
produz produtos do tipo delta vezes propagador: ainda é preciso estendê-los
na mesma prescrição e juntar os contatos radiais de duas linhas já medidos.
O cálculo não autoriza substituir todo esse objeto por zero.

Controle finito: duas cópias de um campo bosônico h, anticampo ímpar hdag
e par ghost espectador; q(hdag)=m h. É um setor de Euler nilpotente, não o
complexo BRST completo nem um Green de espaço-tempo. Incluímos vértices
hdag*h*c e barc*h*c para tornar ambas as omissões detectáveis. Resultado:
{data['checks']} controles exatos, CPU {data['cpu_seconds']}s, rc0.

Próximo passo A7.b: identificar/estender a fonte de Euler composta na família
já fixada; o transporte algébrico das duas inserções A1 foi explicitado.
Q2 completa OPEN. Sem nova chamada externa, alteração de original ou gate.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode('utf-8'))
    write(OUT/'ENTREGA_016_MEDIDA_Ward_transporte_duas_entradas.md',note.encode('utf-8'))
    paths += [D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']
    put(D/'manifest.json',dict(at=now.isoformat(),opening_sha256=opening,
        artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],full_Q2=False,gate_changed=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),target='A7.b',
        event='BILOCAL_WICK_WARD_TRANSPORT',checks=data['checks'],cpu_seconds=data['cpu_seconds'],
        remote_call=False,manifest_sha256=sha(D/'manifest.json')),ensure_ascii=False)+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f"\n{now.isoformat()} A7.b PROGRESS: transporte das duas correções A1 cancela a fonte espúria da mudança de Wick; contato composto permanece. {data['checks']} controles, CPU {data['cpu_seconds']}s. Sem chamada remota nova. AberturaSHA256={opening}.\n")
    p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes())
    state.setdefault('head_history',[]).append({k:state.get(k) for k in
        ['at','previous_goal_turn','completed_this_turn','next','pending_orchestration']})
    state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',completed_this_turn=[
        'Operator content/form recognition sentence preserved verbatim',
        'Two-slot Wick transport derived with both A1 corrections; missing-slot negative controls nonzero'],
        next=['Identify and extend the composite Euler Ward source in the same family; no assumption that delta times a propagator is zero',
              'Assemble composite source and existing two-line radial contacts, keeping curvature and cutoff terms',
              'Receive MiMo57e independent BV review and authorized Kimi responses',
              'A7b deadline20:32UTC; A7c/d,A8,PartB/final remain'])
    state['bilocal_wick_transport_update']=dict(manifest=str(D/'manifest.json'),full_Q2=False)
    put(p,state,True)
    for a in json.loads((D/'manifest.json').read_bytes())['artifacts']:
        assert sha(Path(a['path']))==a['sha256']
    print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=data['checks'],
                         cpu_seconds=data['cpu_seconds'],full_Q2=False),ensure_ascii=False))

if __name__=='__main__':main()
