"""Calculate the scalar fluctuation Euler graphs, not a classical sigma quotient."""
from pathlib import Path
from datetime import datetime,timezone
import json,time
import sympy as s
from balanced_tensor_transport_engine import balanced_euler_line
from position_metric_bubble_engine import BASIS,LABELS
from logarithmic_contact_engine import Q
from euler_ghost_descendant_contact_engine import weighted_defect
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

D=H/'balanced_scalar_euler_v2';N=3

def tensor(B):
    B=s.Matrix(4,4,B);return s.eye(4)*s.trace(B)/2-B

def kernel(T,r,shift):
    value=sum(T[i,j]*balanced_euler_line((i,),tuple(sorted((j,r)))) for i in range(4) for j in range(4))
    return s.expand(value.subs({Q[i]:Q[i]+shift[i] for i in range(4)},simultaneous=True))

def vertex(lam):
    return s.Matrix([[N*kernel(tensor(B),r,lam) for r in range(4)] for B in BASIS])

def insertion(lam,eta):
    # qVaf at X; I_scalar at Y. Outputs are c_X^u c_Y^r.
    def G(r):return s.Matrix(4,4,lambda i,j:eta[i]*int(j==r)+eta[j]*int(i==r))
    return s.Matrix(4,4,lambda u,r:N*kernel(tensor(tuple(G(r))),u,eta))

def q0(A,L):
    B=s.zeros(4)
    for a,(i,j) in enumerate(LABELS):
        for r in range(4):
            B[j,r]-=(Q[i]+L[i])*A[a,r]
            B[i,r]-=(Q[j]+L[j])*A[a,r]
    return weighted_defect(B,L)

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    paths=[Path(__file__),H/'balanced_scalar_euler_check.py',H/'balanced_scalar_euler_run.log',H/'sigma_restriction/results.json',H/'balanced_tensor_transport_engine.py',
        H/'odd_insertion_ward_sign_audit/results.json',H/'balanced_flat_primitive/results.json']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        vertices=['V_hphiphi=cm/2*(tr(h)/2 delta-h) dphi.dphi, three target tangent flavors',
            'Vaf_phi=phi_dagger c.dphi; q0 phi_dagger=-cm Box phi; Hphi=-f/cm',
            'I_scalar=-dchi.J, J_mu=cm/2 c_mu(dphi)^2-cm dmu_phi c.dphi'],
        contraction='Two Wick placements at V cancel its Hessian1/2; cm cancels the ordinary scalar propagator. No scalar modes discarded.',
        extension='Existing R_bal, unchanged; phi background constant does not remove phi fluctuations',
        comparisons=['Constant cutoff q0 closure and explicit symmetric quadratic primitive',
            'Two localized cutoff orders including classical scalar current; parity from previous audit'],
        excluded='Curvature/log corrections, complete causal normalization and all-cutoff polynomial proof',
        sources=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    start=time.process_time();checks=[];zero=(0,)*4
    A0=vertex(zero);square=q0(2*A0,zero)
    for x in square:assert x==0,x;checks.append('scalar constant cutoff q0 square')
    # Decompose the measured O(4)-covariant symbol; verify every coefficient afterward.
    q2=sum(q*q for q in Q);aa,bb,cc=s.symbols('aa bb cc')
    def pattern(i,j,r):
        return aa*int(i==j)*Q[r]*q2*q2+bb*(int(i==r)*Q[j]+int(j==r)*Q[i])*q2*q2+cc*Q[i]*Q[j]*Q[r]*q2
    expected=s.Matrix([[pattern(i,j,r)*(1 if i==j else 2) for r in range(4)] for i,j in LABELS])
    # Parameter extraction is coordinate decomposition, not cancellation by a counterterm.
    equations=[]
    for x in A0-expected:equations.extend(s.Poly(s.expand(x),*Q).coeffs())
    sol=s.solve(equations,[aa,bb,cc]);assert set(sol)=={aa,bb,cc}
    for x in (A0-expected.subs(sol)).applyfunc(s.expand):assert x==0;checks.append('scalar O4 coefficient decomposition')
    # General explicit primitive for these three coefficients, with u=v=0 for display only.
    M=s.MutableDenseNDimArray.zeros(4,4,4,4)
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    M[i,j,k,l]=sol[aa]/2*int(i==j)*int(k==l)*q2*q2+sol[bb]/2*(int(i==k)*int(j==l)+int(i==l)*int(j==k))*q2*q2+sol[cc]/2*Q[i]*Q[j]*Q[k]*Q[l]
    for i,j in LABELS:
        for r in range(4):
            val=sum(M[i,j,k,l]*(Q[k]*int(l==r)+Q[l]*int(k==r)) for k in range(4) for l in range(4))
            assert s.expand(val-pattern(i,j,r).subs(sol))==0;checks.append('scalar primitive M G')
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):assert s.expand(M[i,j,k,l]-M[k,l,i,j])==0;checks.append('scalar Hessian symmetry')
    lam=(1,-1,0,0);eta=(1,0,0,0);L=tuple(lam[i]+eta[i] for i in range(4))
    A1,A2=vertex(lam),vertex(eta);B1,B2=insertion(lam,eta),insertion(eta,lam)
    lhs=q0(A1+A2,L);rhs=-weighted_defect(B1+B2,L);res=(lhs-rhs).applyfunc(s.expand)
    put(D/'MATRICES.json',dict(constant=[[str(v) for v in row] for row in A0.tolist()],
        ordered=[[[str(v) for v in row] for row in a.tolist()] for a in [A1,A2]],
        insertions=[[[str(v) for v in row] for row in a.tolist()] for a in [B1,B2]],
        lhs=[[str(v) for v in row] for row in lhs.tolist()],rhs=[[str(v) for v in row] for row in rhs.tolist()],
        residual=[[str(v) for v in row] for row in res.tolist()]))
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        coefficients={str(k):str(v) for k,v in sol.items()},constant_nonzero=sum(x!=0 for x in A0),
        localized_residual_nonzero=sum(x!=0 for x in res),localized_lhs_nonzero=sum(x!=0 for x in lhs),
        constant_closed=True,constant_primitive=True,flavors=N,full_Q2=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — contribuição das três flutuações escalares no setor principal plano]

A primeira tentativa falhou: a Hessiana candidata tinha um q² excedente
no termo cc, produzindo ordem6 em vez de4. V2 corrige somente essa
expressão dimensionada; os grafos e a tentativa original são preservados.

O fundo sigma constante tem stress clássico zero, mas conserva três
propagadores tangentes. Calculamos o grafo (E_phi c.dphi)×(h dphi dphi)
para esses três modos na MESMA R_bal. cm cancela entre vértice e
propagador; os dois emparelhamentos removem o1/2 da Hessiana escalar.

Para cutoff constante, há{result['constant_nonzero']}/40 componentes
não nulas. O símbolo covariante tem coeficientes{result['coefficients']}
na base aa delta_ij q_r(q²)² + bb(delta_ir q_j+delta_jr q_i)(q²)²
+ cc q_i q_j q_r q², com peso2 nos h_ij fora da diagonal.
Seu q0 quadrado é zero e uma Hessiana local simétrica M satisfaz MG=A.
Isto dá primitiva quadrática deste representante, não da Q2 curva inteira.

Para cutoffs localizados também calculamos I_scalar=-dchi.J_scalar e
os dois canais qVaf_scalar×I_scalar. Com o sinal de inserção ímpar
derivado anteriormente, a comparação tem residual
{result['localized_residual_nonzero']}/16; lhs não nulo em
{result['localized_lhs_nonzero']}/16. Matrizes preservadas mesmo se falhar.

{len(checks)}controles,CPU{result['cpu_seconds']}s,rc0. Não inclui
curvatura, logs, família causal global ou escolha do horizonte físico.
Nenhum novo parâmetro físico, chamada remota ou mudança do gate.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_Euler_escalar_principal_v2.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths+[D/'PRE_REGISTER.json',D/'MATRICES.json',D/'results.json',D/'DERIVACAO.md']],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='BALANCED_SCALAR_EULER_GRAPHS',target='A7.b',checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: três flutuações escalares calculadas;primitiva plana paga,consistência localizada residual{result["localized_residual_nonzero"]}/16;{len(checks)}controles CPU{result["cpu_seconds"]}s.Q2curvaOPEN.AberturaSHA256={opening}.\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
