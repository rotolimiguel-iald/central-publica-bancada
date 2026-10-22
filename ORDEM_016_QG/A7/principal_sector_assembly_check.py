"""Join the computed metric/ghost and scalar principal representatives."""
from pathlib import Path
from datetime import datetime,timezone
import json,time
import sympy as s
from logarithmic_contact_engine import Q
from position_metric_bubble_engine import LABELS
from euler_ghost_descendant_contact_engine import weighted_defect
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

D=H/'principal_sector_assembly'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    paths=[Path(__file__),H/'balanced_euler_constant_cutoff/results.json',H/'balanced_scalar_euler_v2/MATRICES.json',
        H/'balanced_scalar_euler_v2/results.json',H/'odd_insertion_ward_sign_audit/results.json',
        H/'classical_insertion_euler_v2/results.json',H/'balanced_flat_primitive/results.json']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        target='Assemble existing principal flat graphs and verify scalar current analytically; do not compute a new phenomenological function',
        scope='Normalized Euler two-line representative, one common temporal prefactor; constant coupling primitive and sampled localized consistency',
        no_fit=True,curvature_included=False,
        sources=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    cpu=time.process_time();checks=[];loc={str(q):q for q in Q}
    mat=lambda a:s.Matrix([[s.sympify(t,locals=loc) for t in row] for row in a])
    g=json.loads(paths[1].read_bytes());sm=json.loads(paths[2].read_bytes());sc=json.loads(paths[3].read_bytes())
    A=mat(g['total'])+mat(sm['constant']);q2=sum(q*q for q in Q)
    co=[s.Rational(g['O4_decomposition'][0][k])+s.Rational(sc['coefficients'][z]) for k,z in [('a','aa'),('b','bb'),('c','cc')]]
    for t,(i,j) in enumerate(LABELS):
        for r in range(4):
            expected=(co[0]*int(i==j)*Q[r]*q2*q2+co[1]*(int(i==r)*Q[j]+int(j==r)*Q[i])*q2*q2+co[2]*Q[i]*Q[j]*Q[r]*q2)*(1 if i==j else 2)
            assert s.expand(A[t,r]-expected)==0;checks.append('sum of computed tensor components')
    # Arbitrary smooth scalar and vector fields: no numerical jets or equations of motion.
    x=s.symbols('x0:4');phi=s.Function('phi')(*x);c=[s.Function('c'+str(i))(*x) for i in range(4)];chi=s.Function('chi')(*x);cm=s.Symbol('cm')
    dp=[s.diff(phi,z) for z in x];dc=s.Matrix(4,4,lambda i,j:s.diff(c[j],x[i]))
    grad2=sum(v*v for v in dp);adv=sum(c[i]*dp[i] for i in range(4))
    tr=sum(dc[i,i] for i in range(4));Sc=tr*s.eye(4)-dc-dc.T
    variation=cm*s.Rational(1,2)*sum(Sc[i,j]*dp[i]*dp[j] for i in range(4) for j in range(4))-cm*sum(s.diff(phi,z,2) for z in x)*adv
    J=[cm*c[i]*grad2/2-cm*dp[i]*adv for i in range(4)]
    assert s.expand(variation-sum(s.diff(J[i],x[i]) for i in range(4)))==0;checks.append('general scalar BV current identity')
    I=-sum(s.diff(chi,x[i])*J[i] for i in range(4))
    assert s.expand(chi*variation-I-sum(s.diff(chi*J[i],x[i]) for i in range(4)))==0;checks.append('general localized current by parts')
    L=(2,-1,0,0)
    met=json.loads(paths[5].read_bytes());total_lhs=mat(met['lhs'])+mat(sm['lhs']);total_rhs=-mat(met['rhs'])+mat(sm['rhs'])
    residual=(total_lhs-total_rhs).applyfunc(s.expand)
    for v in residual:assert v==0;checks.append('combined localized consistency component')
    # A local primitive follows linearly from the two already verified symmetric Hessians.
    primitive=dict(trace_box2_trace=str(co[0]/4),h_box2_h=str(co[1]/2),double_divergence_squared=str(co[2]/4))
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-cpu,
        per_order_coefficients=dict(A=str(co[0]),B=str(co[1]),C=str(co[2])),
        two_order_coefficients=dict(A=str(2*co[0]),B=str(2*co[1]),C=str(2*co[2])),
        per_order_primitive_density=primitive,localized_nonzero_residual=sum(v!=0 for v in residual),
        localized_nonzero_lhs=sum(v!=0 for v in total_lhs),flavors=3,
        scope='PRINCIPAL_FLAT_hc_FREE_BRST_REPRESENTATIVE_IN_R_BAL; neither the full curved anomaly nor interacting state',
        counterterm_adopted=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — soma dos setores já calculados; não a Q2 curva completa]

As três flutuações escalares foram acrescentadas aos grafos métrico/ghost.
A corrente escalar também foi conferida para funções suaves ARBITRÁRIAS,
sem equações de movimento: q0V_scalar=divJ, J_mu=cm[c_mu(dphi)²/2
-dmu_phi(c.dphi)]. Logo I_chi=-dchi.J módulo divergência. Esta verificação
justifica o vértice usado, além do controle de consistência das matrizes.

Por colocação ordenada no limite de cutoff constante, o representante
normalizado por CE tem coeficientes{result['per_order_coefficients']} na
base O4 já registrada. Para a soma das duas colocações, multiplicar por2.
Uma primitiva por colocação é a integral de
 {primitive['trace_box2_trace']} tr(h)box²tr(h)
+{primitive['h_box2_h']} h_ij box²h_ij
+{primitive['double_divergence_squared']}(divdiv h)².
As direções homogêneas dos contratermos permanecem livres; não adotamos
esta subtração como escolha física nem alteramos produtos temporais.

Nos dois cutoffs testados, a condição INHOMOGÊNEA tem lhs não nulo em
{result['localized_nonzero_lhs']}/16 e residual{result['localized_nonzero_residual']}/16 após
incluir as inserções clássicas e o sinal ímpar. Não é a afirmação falsa
de que o representante localizado isolado tenha q0 quadrado zero.

PAGO neste recorte: coeficientes principais planos, corrente escalar,
primitiva de acoplamento constante e a comparação localizada registrada.
NÃO PAGO aqui: coeficientes curvos K/K² na mesma família balanceada,
normalização de todas as aridades e a construção causal lorentziana.
As antigas primitivas curvas condicionais não fornecem esses coeficientes.
{len(checks)}controles,CPU{result['cpu_seconds']}s,rc0. Gate/originais intactos.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_soma_principal_Einstein_sigma.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='PRINCIPAL_EINSTEIN_SIGMA_ASSEMBLY',target='A7.b',checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: Einstein+3sigma somados no setor principal;consistência localizada0/16,primitiva plana explícita;{len(checks)}controles CPU{result["cpu_seconds"]}s.Q2curvaOPEN.AberturaSHA256={opening}.\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
