"""Audit localized BV consistency without assuming a vanishing one-vertex term."""
from pathlib import Path
from datetime import datetime, timezone
import ast, json, time, hashlib
import sympy as s
from deliver_nonminimal_wick_and_mimo_audit import H, OUT, BASE, sha, write, put, append

D = H / 'kimi_localized_consistency_audit'

def main():
    D.mkdir(exist_ok=False)
    now = datetime.now(timezone.utc)
    source = BASE / 'state/handoffs/d41046ee-a069-4545-a6ba-9c322662af46_delivery.json'
    job = json.loads(source.read_bytes())['job']
    execution = job['execution']; result = execution['result']
    assert execution['status'] == 'result_ready'
    write(D / 'KIMI_ORIGINAL.md', result['text'].encode('utf-8'))
    put(D / 'RECEIPT.json', dict(at=now.isoformat(), request_id=job['request_id'],
        job_id=job['id'], execution_task_id=execution['id'], source_sha256=sha(source),
        prompt_sha256=hashlib.sha256(job['prompt'].encode()).hexdigest(),
        response_sha256=sha(D/'KIMI_ORIGINAL.md'), usage=result['usage'],
        elapsed_seconds=result.get('elapsed_seconds'), cost_estimate_usd=result.get('cost_estimate_usd'),
        cost_status='SUBSCRIPTION_COST_NOT_REPORTED_NOT_ZERO', model=result['model']))
    sources = [Path(__file__), H/'antifield_quadratic_primitive_check.py',
        H/'bv_antifield_coordinate/results.json', H/'localized_volume_consistency/results.json']
    put(D/'PRE_REGISTER.json', dict(at=now.isoformat(), sources=[dict(path=str(p),sha256=sha(p)) for p in sources],
        target='Test Jacobi, BV Laplacian sign, coupling order with W1 retained, affine-cutoff polarization, and differential commutator components',
        exclusions='Finite canonical algebra is a sign/order counterexample, not a spacetime renormalization or Q2 proof'))
    started = time.process_time(); checks=[]
    nodes=[n for n in ast.parse(sources[1].read_text('utf-8')).body if isinstance(n,ast.FunctionDef) and n.name in {'clean','add','scale','mul','atom'}]
    ns={'s':s};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(sources[1]),'exec'),ns)
    clean,add,scale,mul,atom=[ns[n] for n in ['clean','add','scale','mul','atom']]
    E=lambda f:clean({():f})
    x,y,k,a,b=s.symbols('x y k a b'); xs=[x,y]
    def de(F,z):return clean({m:s.diff(v,z) for m,v in F.items()})
    def do(F,i,right=False):
        out={}
        for m,v in F.items():
            if i in m:
                j=m.index(i);sign=(-1)**j
                if right:sign*=(-1)**(len(m)+1)
                out[m[:j]+m[j+1:]]=v*sign
        return clean(out)
    def bracket(F,G):
        return add(*(add(mul(de(F,z),do(G,i)),scale(mul(do(F,i,True),de(G,z)),-1)) for i,z in enumerate(xs)))
    def lap(F):return add(*(de(do(F,i),z) for i,z in enumerate(xs)))
    def eq(name,F,G=None):
        assert not add(F,scale(G or {},-1)),(name,F,G)
        checks.append(name)
    def coeff(F,z,n):return clean({m:s.expand(v).coeff(z,n) for m,v in F.items()})
    def serial(F):return {str(m):str(v) for m,v in F.items()}
    S0=E((x*x+y*y)/2); V=scale(mul(atom(0),atom(1)),x*y)
    W1=E(x*x); W2=E(y*y+x*y); S=add(S0,scale(V,k)); W=add(scale(W1,k),scale(W2,k*k))
    I=scale(bracket(S,S),s.Rational(1,2)); A=add(bracket(S,W),scale(lap(S),-s.I))
    eq('free master equation',bracket(S0,S0))
    for F in [E(x),E(y),atom(0),atom(1),W1,W2,V,S]:
        eq('Jacobi square',bracket(S,bracket(S,F)),bracket(I,F))
        eq('Laplacian square',lap(lap(F)))
    eq('Delta I equals minus bracket S Delta S',lap(I),scale(bracket(S,lap(S)),-1))
    eq('full inhomogeneous consistency including measure',bracket(S,A),add(bracket(I,W),scale(lap(I),s.I)))
    I1=coeff(I,k,1); I2=coeff(I,k,2); A1=coeff(A,k,1); A2=coeff(A,k,2)
    order2=add(bracket(S0,A2),bracket(V,A1)); rhs2=add(bracket(I1,W1),scale(lap(I2),s.I))
    eq('order two keeps one-vertex W1 and A1',order2,rhs2)
    eq('explicit order-two classical insertion',bracket(I1,W1),E(2*x*x*y*y))
    assert bracket(S0,A2);checks.append('claimed homogeneous order two rejected in explicit model')
    # Polarize only the interaction, never the affine full action as if linear.
    Vx=V; Vy=add(V,E(x*y)); St=add(S0,scale(Vx,a),scale(Vy,b))
    Wt=add(scale(W1,a),scale(W2,b),scale(E(x*y*y),a*b))
    It=scale(bracket(St,St),s.Rational(1,2)); At=add(bracket(St,Wt),scale(lap(St),-s.I))
    at0=lambda F:clean({m:v.subs({a:0,b:0}) for m,v in F.items()})
    cxy=lambda F:at0(de(de(F,a),b)); cx=lambda F:at0(de(F,a)); cy=lambda F:at0(de(F,b))
    eq('polarized classical quadratic term',cxy(It),bracket(Vx,Vy))
    eq('polarized order-two consistency',add(bracket(S0,cxy(At)),bracket(Vx,cy(At)),bracket(Vy,cx(At))),
       add(bracket(cx(It),cy(Wt)),bracket(cy(It),cx(Wt)),scale(lap(cxy(It)),s.I)))
    def classical(U):return scale(bracket(U,U),s.Rational(1,2))
    wrong=add(classical(add(S0,Vx)),bracket(add(S0,Vx),add(S0,Vy)),classical(add(S0,Vy)))
    actual=classical(add(S0,Vx,Vy))
    mismatch=add(wrong,scale(actual,-1));assert mismatch;checks.append('affine full-action polarization rejected')
    # Check the individual differential expressions, not only their sum.
    z=s.symbols('z0:4'); chi=1+z[0]**2+z[1]*z[2]
    w=s.Matrix([z[i]**2+z[(i+1)%4]*z[(i+2)%4]+i*z[3] for i in range(4)])
    G=lambda f:s.Matrix(4,4,lambda i,j:s.diff(f[j],z[i])+s.diff(f[i],z[j]))
    C=lambda h:s.Matrix([sum(s.diff(h[i,j],z[i]) for i in range(4))-s.diff(s.trace(h),z[j])/2 for j in range(4)])
    box=lambda f:sum(s.diff(f,zz,2) for zz in z)
    grad=[s.diff(chi,zz) for zz in z]; div=sum(s.diff(w[i],z[i]) for i in range(4))
    first=C(G(chi*w)-chi*G(w)); second=C(chi*G(w))-chi*C(G(w))
    first_formula=s.Matrix([box(chi)*w[j]+sum(grad[i]*s.diff(w[j],z[i]) for i in range(4)) +grad[j]*div-sum(grad[i]*s.diff(w[i],z[j]) for i in range(4)) for j in range(4)])
    second_formula=s.Matrix([sum(grad[i]*(s.diff(w[j],z[i])+s.diff(w[i],z[j])) for i in range(4))-grad[j]*div for j in range(4)])
    for j in range(4):
        eq('C G commutator component',E(first[j]),E(first_formula[j]))
        eq('C commutator G component',E(second[j]),E(second_formula[j]))
        eq('factorization component',E(first[j]+second[j]),E(box(chi)*w[j]+2*sum(grad[i]*s.diff(w[j],z[i]) for i in range(4))))
    wrong_second=s.Matrix([sum(grad[i]*s.diff(w[j],z[i]) for i in range(4)) for j in range(4)])
    mismatch_second=(second-wrong_second).applyfunc(s.expand)
    assert any(mismatch_second);checks.append('Kimi simplified second component rejected')
    result_local=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-started,
        accepted=['Jacobi square with nonzero classical defect','Need composite insertions before sector projection','No cohomological obstruction inferred from isolated residue'],
        corrections=['Unbroken QME cannot hold at order zero with I nonzero','Standard BV Laplacian gives Delta I=-(S,Delta S)',
          'W1 cannot be dropped without proof; order-two source (I1,W1) survives',
          'Polarize interaction using independent parameters, not affine full action',
          'Individual cutoff commutator components omitted transverse terms',
          'Ghost Leibniz signs in intermediate Bloco A disagree with its final correct expression',
          'Uniform cutoff does not complete a truncated Einstein interaction by nilpotency of s1 alone',
          'Antifield change is parity-dependent in existing audited convention, not a common minus sign'],
        order_two_source=serial(bracket(I1,W1)),homogeneous_counterexample=serial(bracket(S0,A2)),
        affine_polarization_mismatch=serial(mismatch),commutator_mismatch=list(map(str,mismatch_second)),
        full_Q2=False,gate_changed=False,weights_fitted=False)
    put(D/'AUDIT.json',result_local)
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — auditoria da revisão Kimi; coeficiente A2 físico continua OPEN]

Aceita-se s²=(I,·), I=(S,S)/2, e a necessidade de manter a inserção clássica
antes de projetar. A resposta não é adotada integralmente. Com a convenção
canônica explícita do teste, Delta I=-(S,Delta S). Para a QUEBRA formal
B(Gamma)=(Gamma,Gamma)/2-i hbar Delta Gamma=I+hbar A+...:

 (S,A)=(I,W)+i Delta I,  Gamma=S+hbar W+... .

Não se pode escrever a QME sem quebra e ao mesmo tempo I!=0. Se houver uma
inserção renormalizada J(I)=I+hbar J1(I)+..., A acima é J1(I)+a, não apenas
a anomalia a. Seu teste exige também J1; a identidade algébrica não calcula J1.

S=S0+kV, W=kW1+k²W2+..., A=kA1+k²A2+..., I=kI1+k²I2 dão

 s0 A2+(V,A1)=(I1,W1)+i Delta I2.

Portanto o primeiro termo de W não pode ser omitido sem uma condição
demonstrada. O Kimi começou W em k², mas a bancada já tem uma contribuição
de aridade1 no auxiliar curvo e não impôs essa normalização. No contracontrole
finito S0=(x²+y²)/2,V=xy theta1 theta2,W1=x², (I1,W1)=2x²y²!=0.

A polarização correta usa S=S0+aVx+bVy. O coeficiente ab obedece
 s0 Axy+(Vx,Ay)+(Vy,Ax)=(Ix,Wy)+(Iy,Wx)+i Delta(Vx,Vy).
Aqui Ix=(S0,Vx),Iy=(S0,Vy). Isso não identifica estes coeficientes de
ação efetiva com o A2 de produtos temporais sem o dicionário correspondente.

Também foram corrigidas as componentes de C[G,chi] e [C,chi]G: os termos
grad(chi)*grad(w) transversais cancelam NA SOMA, não individualmente. O
termo-fonte -hdag[G,chi]w já existe na derivação local anterior; não requer
inventar uma nova fonte independente. A troca de antifields depende da
paridade, conforme a auditoria existente, e não de um menos comum.

{len(checks)} controles, CPU {result_local['cpu_seconds']}s, rc0. Modelo finito
testa signos/ordens; não prova a renormalização de espaço-tempo nem Q2.
Kimi: {result['usage']['total_tokens']} tokens; assinatura sem custo unitário
informado, não zero. Originais/kernel/gate intactos. AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode('utf-8'));write(OUT/'ENTREGA_016_MEDIDA_consistencia_localizada_Kimi_auditada.md',note.encode('utf-8'))
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'KIMI_ORIGINAL.md',D/'RECEIPT.json',D/'PRE_REGISTER.json',D/'AUDIT.json',D/'DERIVACAO.md']],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='KIMI_LOCALIZED_CONSISTENCY_AUDITED',target='A7.b',request_id=job['request_id'],job_id=job['id'],execution_task_id=execution['id'],provider='kimi',usage=result['usage'],cost_estimate_usd=None,cost_status='SUBSCRIPTION_NOT_REPORTED',prompt_sha256=hashlib.sha256(job['prompt'].encode()).hexdigest(),response_sha256=sha(D/'KIMI_ORIGINAL.md'),checks=len(checks),cpu_seconds=result_local['cpu_seconds'],manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: Kimi e710 auditado; Jacobi aceito, contagem em acoplamento e polarização corrigidas. {len(checks)} controles, CPU{result_local["cpu_seconds"]}s. Sem novo custo remoto medido; assinatura desconhecida. Q2OPEN. AberturaSHA256={opening}.\n')
    print(json.dumps(result_local),flush=True)

if __name__=='__main__':main()
