"""Construct the quadratic local primitive of the measured constant-cutoff flat tensor."""
from pathlib import Path
from datetime import datetime,timezone
import json,time
import sympy as s
from full_loop_extension_engine import Q
from position_metric_bubble_engine import LABELS
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

D=H/'balanced_flat_primitive'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    src=H/'balanced_euler_constant_cutoff/results.json';data=json.loads(src.read_bytes())
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        target='Explicit local quadratic primitive for the actual balanced Euler sum at zero cutoff jets',
        ansatz='Self-adjoint parity-even O4 Hessian of degree4, five tensor structures; coefficients from exact measured tensor',
        scope='Local free-BRST cohomology in the flat quadratic constant-coupling sector only',
        not_adopted='No physical counterterm, no curved or variable-cutoff cancellation, no additional normalization fit',
        sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),src,H/'local_quadratic_ward_primitive/results.json']]))
    start=time.process_time();checks=[];q2=sum(q*q for q in Q)
    A,B,C=[s.Rational(data['O4_decomposition'][0][k]) for k in ['a','b','c']]
    u,v=s.symbols('u v');d=lambda i,j:int(i==j)
    coeff=[A/2-u,B-2*v,u,v,C/2-u-2*v]
    def M(i,j,k,l):
        a,b,c,d0,e=coeff
        return (a*d(i,j)*d(k,l)+b*(d(i,k)*d(j,l)+d(i,l)*d(j,k))/2)*q2**2+\
            c*(d(i,j)*Q[k]*Q[l]+d(k,l)*Q[i]*Q[j])*q2+\
            d0*(d(i,k)*Q[j]*Q[l]+d(j,k)*Q[i]*Q[l]+d(i,l)*Q[j]*Q[k]+d(j,l)*Q[i]*Q[k])*q2+\
            e*Q[i]*Q[j]*Q[k]*Q[l]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    for label,value in [('first symmetry',M(i,j,k,l)-M(j,i,k,l)),
                        ('pair self-adjointness',M(i,j,k,l)-M(k,l,i,j))]:
                        assert s.expand(value)==0;checks.append(label)
    loc={str(q):q for q in Q};target=s.Matrix([[s.sympify(t,locals=loc) for t in row] for row in data['total']])
    for a,(i,j) in enumerate(LABELS):
        for r in range(4):
            value=2*sum(M(i,j,k,r)*Q[k] for k in range(4))*(1 if i==j else 2)
            assert s.expand(value-target[a,r])==0;checks.append('primitive image '+str((a,r)))
    # The homogeneous two directions really are in the kernel of the Ward map.
    for parameter in [u,v]:
        for i in range(4):
            for j in range(i,4):
                for r in range(4):
                    assert s.expand(sum(s.diff(M(i,j,k,r),parameter)*Q[k] for k in range(4)))==0
                    checks.append('homogeneous direction '+str((parameter,i,j,r)))
    # Negative control: the measured localized representative has nonzero square,
    # so no q-exact functional alone can equal it off shell.
    varying=json.loads((H/'balanced_current_source/results.json').read_bytes())
    assert varying['nonzero_defect_components']>0
    checks.append('constant-coupling primitive is not claimed as full localized primitive')
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        measured_tensor=dict(A=str(A),B=str(B),C=str(C)),Hessian_coefficients=list(map(str,coeff)),
        particular_density=dict(trace_box2_trace=str(A/4),h_box2_h=str(B/2),double_divergence_squared=str(C/4)),
        scope='PRINCIPAL_FLAT_QUADRATIC_CONSTANT_COUPLING_FREE_BRST_EXACT',
        cohomology='Zero class for this representative in the stated restricted H^1(q0|d), not a conclusion about complete interacting H^1 or Q2.',
        free_parameters=['u','v'],counterterm_adopted=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — primitiva local do representante principal plano delimitado]

Na normalização R_bal/CE e no limite de jatos de cutoff constantes, os
três grafos Euler deram o tensor h_ij c_r com coeficientes
A={A}, B={B}, C={C} na base registrada no cálculo anterior.
Foi encontrada e conferida uma Hessiana local autoadjunta M de ordem4:

 M=a delta_ij delta_kl(q²)²+b I_ij,kl(q²)²
  +u(delta_ij q_k q_l+delta_kl q_i q_j)q²
  +v(delta_ik q_j q_l+delta_jk q_i q_l
     +delta_il q_j q_k+delta_jl q_i q_k)q²+e q_i q_j q_k q_l,
 a=A/2-u, b=B-2v, e=C/2-u-2v.

Para B_local=1/2 int h M h, q0h=G c dá
q0 B_local=int h M Gc. O CAS confere todas40 componentes desse resultado
contra os grafos medidos, para u e v SIMBÓLICOS; ambas as direções livres
estão no núcleo de M G. Nenhum valor dessas liberdades foi adotado.
Um exemplo matemático de primitiva (u=v=0) é

 B_local=int[{A/4} tr(h) box² tr(h)
             +{B/2} h_ij box² h_ij
             +{C/4}(partial_i partial_j h_ij)²].

As integrações por partes usam campos/testes apropriados no setor local.
Logo ESSE representante tem classe zero no problema de cohomologia livre,
plano, quadrático e de acoplamento constante. Ele é não nulo antes da
primitiva; sua exatidão não é declaração de que toda Q2 já desapareceu.

Não transportar a conclusão aos cutoffs variáveis: o representante
localizado anteriormente medido tem quadrado BV não nulo e sua identidade
é INHOMOGÊNEA, com inserções clássicas q0V. Um único q0 B não pode produzir
essa expressão inteira, pois q0²=0. A família de contratermos, curvatura,
setores escalares e referência física continuam separados.
{len(checks)} controles, CPU{result['cpu_seconds']}s,rc0; originais/gate intactos.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_primitiva_Euler_plana_balanceada.md',note.encode())
    paths=[Path(__file__),src,H/'balanced_current_source/results.json',D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='BALANCED_FLAT_EULER_PRIMITIVE',target='A7.b',
        checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: representante Euler plano constante é q0-exato; primitivaquadrática e2direções homogêneas conferidas. {len(checks)}controles CPU{result["cpu_seconds"]}s; nãoéQ2curva completa. AberturaSHA256={opening}.\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
