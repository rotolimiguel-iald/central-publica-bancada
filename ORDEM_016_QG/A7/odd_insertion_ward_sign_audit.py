"""Audit the parity convention before reusing the previously computed graphs."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,time
import sympy as s
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append
from classical_current_jet_engine import current
from localized_brst_flux_engine import gauge_matrix,v2,add as vadd,neg,dot
from position_metric_bubble_engine import BASIS
from logarithmic_contact_engine import Q

D=H/'odd_insertion_ward_sign_audit'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    paths=[Path(__file__),H/'classical_insertion_euler_v2/results.json',
        H/'classical_insertion_euler_check_v2.py',H/'classical_insertion_euler_run_v2.log',
        H/'classical_insertion_euler_engine.py',H/'classical_current_jet_engine.py',
        H/'localized_brst_flux_engine.py',H/'antifield_quadratic_primitive_check.py']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        source='Frob arXiv:1803.10235v3, equations154-157; equation155 has MINUS the anomaly with an odd distinguished insertion.',
        diagnosis_seen='Previous lhs+rhs vanishes; this observation does not choose a convention.',
        independent_controls=['Nilpotent finite Grassmann differential and arbitrary even bilinear contraction',
            'q0 of the metric classical current equals plus E_h[G,chi]w',
            'Only after controls, reuse immutable matrices; no graph coefficient changed'],
        target='Principal flat metric/ghost localized Ward consistency in the two previously computed cutoff orders',
        excludes=['Curvature-dependent a1 normalization','Scalar loop','All possible cutoff jets','Full causal Lorentzian family'],
        sources=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    start=time.process_time();checks=[]
    names={'clean','add','scale','mul','atom'}
    nodes=[n for n in ast.parse(paths[-1].read_text('utf8')).body if isinstance(n,ast.FunctionDef) and n.name in names]
    ns={'s':s};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(paths[-1]),'exec'),ns)
    clean,add,scale,mul,atom=[ns[n] for n in ['clean','add','scale','mul','atom']]
    x,y=s.symbols('x y');c,a,d=[atom(i) for i in range(3)]
    def de(P,z):return clean({k:s.diff(v,z) for k,v in P.items()})
    def do(P,i):
        out={}
        for w,v in P.items():
            if i in w:
                j=w.index(i);key=w[:j]+w[j+1:];out[key]=out.get(key,0)+(-1)**j*v
        return clean(out)
    def q(P):return add(mul(c,de(P,x)),scale(do(P,1),y))
    def T(F,G):return scale(mul(de(de(F,y),y),de(de(G,y),y)),s.Rational(1,2))
    def C(F,G,p):return add(q(T(F,G)),scale(T(q(F),G),-1),scale(T(F,q(G)),-(-1)**p))
    def eq(name,L,R):
        assert not add(L,scale(R,-1)),name
        checks.append(name)
    samples=[]
    for i in (1,2,3):
        for j in (2,3):
            F=scale(mul(a,d),x**i*y);G={():x**j*y**3}
            eq('q squared F',q(q(F)),{});eq('q squared G',q(q(G)),{})
            for A,B,p in [(F,G,0),(q(F),G,1),(F,q(G),0)]:
                if not A or not B:continue
                eq('q is odd derivation',q(mul(A,B)),add(mul(q(A),B),scale(mul(A,q(B)),(-1)**p)))
            lhs=q(C(F,G,0));raw=add(C(q(F),G,1),C(F,q(G),0))
            eq('odd commutator anticommutes with q',lhs,scale(raw,-1))
            assert lhs and add(lhs,scale(raw,-1));checks.append('wrong same-sign odd convention rejected')
            # Frob equation155: the distinguished odd insertion enters with -A.
            corrected=scale(raw,-1)
            eq('Frob odd-insertion convention gives plus consistency RHS',lhs,corrected)
            samples.append(dict(i=i,j=j,lhs={str(k):str(v) for k,v in lhs.items()}))
    # Independently check the sign of the already constructed classical current.
    classical=[]
    for p,r,lam,u_index,v_index in [((1,2,-1,0),(0,1,2,-1),(1,-1,0,0),0,1),
        ((2,0,1,-1),(1,-2,0,1),(0,1,1,0),2,3)]:
        k=neg(vadd(p,r,lam));u=tuple(int(i==u_index) for i in range(4));v=tuple(int(i==v_index) for i in range(4))
        w=tuple(dot(u,r)*v[i]-dot(v,p)*u[i] for i in range(4))
        for h in BASIS:
            J1=current(gauge_matrix(p,u),p,h,k,v_index,r)
            J2=current(gauge_matrix(r,v),r,h,k,u_index,p)
            lhs=dot(lam,tuple(a-b for a,b in zip(J1,J2)))
            rhs=-2*v2(gauge_matrix(lam,w),neg(k),h,k)
            assert lhs==rhs,(lhs,rhs);checks.append('q metric current equals plus Euler commutator')
            classical.append(str(lhs))
    # Reuse matrices only after deriving the relative sign above.
    old=json.loads(paths[1].read_bytes());loc={str(z):z for z in Q}
    mat=lambda x:s.Matrix([[s.sympify(v,locals=loc) for v in row] for row in x])
    lhs=mat(old['lhs']);raw_rhs=mat(old['rhs']);correct_rhs=-raw_rhs
    residual=(lhs-correct_rhs).applyfunc(s.expand)
    for v in residual:assert v==0,v;checks.append('localized principal consistency component')
    assert sum(v!=0 for v in (lhs-raw_rhs).applyfunc(s.expand))==16
    checks.append('old parity convention fails all16 components')
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        finite_models=samples,classical_current_controls=classical,nonzero_residual=0,
        old_nonzero_residual=16,graphs_recomputed=False,coefficients_fitted=False,
        corrected_RHS='minus classical_insertion_euler_v2 RHS, by odd distinguished insertion convention',
        corrected_residual=[[str(v) for v in row] for row in residual.tolist()],
        full_Q2=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — correção da leitura de paridade; consistência principal localizada]

A eq.155 de Fröb, arXiv:1803.10235v3, tem menos A para a inserção
distinguida ímpar. A fórmula com duas entradas pares não pode ser aplicada
a (q0V,V) mantendo o sinal de A. Essa é a origem do sinal global invertido
na entrega v2; os três motores de grafos e seus coeficientes ficam intactos.

Controle independente: para qualquer mapa bilinear par T e q ímpar nilpotente,
C(F,G)=qT(F,G)-T(qF,G)-(-1)^|F|T(F,qG) satisfaz
 qC(F,G)=-C(qF,G)-(-1)^|F|C(F,qG).
Isto resulta expandindo e cancelando q² e os dois termos cruzados.
Na convenção da identidade de consistência da fonte, A com uma entrada
ímpar recebe o sinal oposto ao C. Assim qA(V,V) tem PLUS as duas
inserções A(qV,V), exatamente como o Teorema7 escreve. Se se usar C
uniformemente, a condição equivalente tem MINUS; não se misturam as duas.

Seis modelos de Grassmann não triviais conferiram a identidade e rejeitaram
a cópia do sinal par. Vinte polarizações do vértice clássico conferiram
q0 I_metric=+E_h[G,chi]w no setor sem b, evitando corrigir o sinal errado.

Reaplicação às matrizes INALTERADAS: residual0/16, antes16/16. O sinal foi
obtido da identidade e do controle de paridade, não por ajuste de pesos.
Isso paga a consistência do setor principal plano métrico/ghost nos dois
jatos de cutoff calculados. NÃO paga o setor curvo/escalares, a identidade
universal para todos os cutoffs ou a construção causal completa.
Os termos a1 dependentes da curvatura ainda precisam do mesmo dicionário
de paridade antes de entrarem na soma final.

{len(checks)} controles; CPU{result['cpu_seconds']}s,rc0. Nenhuma chamada
remota nesta auditoria. Gate/originais intactos. AberturaSHA256={opening}.
Fonte: https://arxiv.org/pdf/1803.10235v3,eqs154-157.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_paridade_insercao_Ward.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='ODD_INSERTION_WARD_PARITY_AUDIT',target='A7.b',checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: convenção ímpar derivada da fonte+Grassmann;residual principal0/16 sem mudar grafos;{len(checks)}controles CPU{result["cpu_seconds"]}s. Curvatura/escalaresOPEN.AberturaSHA256={opening}.\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['finite_models','classical_current_controls','corrected_residual']}),flush=True)

if __name__=='__main__':main()
