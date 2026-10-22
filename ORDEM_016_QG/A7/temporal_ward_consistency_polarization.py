"""Extract the two-input, one-loop condition from Frob Theorem 7."""
from datetime import datetime, timezone
from pathlib import Path
import json, time
import sympy as s
from deliver_nonminimal_wick_and_mimo_audit import H, OUT, sha, write, put, append

D=H/'temporal_ward_consistency_polarization'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    source=dict(url='https://arxiv.org/pdf/1803.10235v3',title='Anomalies in time-ordered products and applications to the BV-BRST formulation of quantum gauge theories',
        author='Markus B. Frob',locator='Theorem 7, printed pages36-37; Eq154 page36',
        accessed_at=now.isoformat(),read='WEB_PRIMARY_TEXT_READ',local_pdf_hash=None,
        distinction='HTML conversion stops early; PDF primary text was read. No PDF download/hash claimed.')
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),source=source,script_sha256=sha(Path(__file__)),
        target='Extract hbar*a*b coefficient while retaining a1, a2 on classical insertions, and independent even cutoff parameters',
        hypotheses=['Free BRST square zero','One consistent family of time-ordered products satisfying hypotheses of Theorem7','Anomaly starts at order hbar','No scalar-field quotient or vanishing a1 assumed'],
        exclusions=['This coefficient extraction does not verify the distributional hypotheses','No numerical choice of counterterm','No physical A2 value obtained']))
    start=time.process_time();a,b,h=s.symbols('a b h')
    # Independent symbols stand for the output of each distinct operation.
    labels=['q_ax','q_ay','q_axy','vx_ax','vx_ay','vy_ax','vy_ay',
        'a_ix','a_iy','a_bxx','a_bxy','a_byy','a_ix_x','a_ix_y','a_iy_x','a_iy_y']
    v=dict(zip(labels,s.symbols(' '.join(labels))))
    lhs=h*(a*v['q_ax']+b*v['q_ay']+a*b*v['q_axy']+a*a*v['vx_ax']+
        a*b*(v['vx_ay']+v['vy_ax'])+b*b*v['vy_ay'])
    # I(F)=a Ix+b Iy+a²/2 (Vx,Vx)+ab(Vx,Vy)+b²/2(Vy,Vy).
    rhs=h*(a*v['a_ix']+b*v['a_iy']+a*a*v['a_bxx']/2+a*b*v['a_bxy']+b*b*v['a_byy']/2+
        a*a*v['a_ix_x']+a*b*(v['a_ix_y']+v['a_iy_x'])+b*b*v['a_iy_y'])
    checks=[]
    def coefficient(expr,i,j):return s.expand(expr).coeff(h,1).coeff(a,i).coeff(b,j)
    def eq(label,expr):assert s.expand(expr)==0,(label,expr);checks.append(label)
    eq('linear X',coefficient(lhs-rhs,1,0)-(v['q_ax']-v['a_ix']))
    eq('linear Y',coefficient(lhs-rhs,0,1)-(v['q_ay']-v['a_iy']))
    target=v['q_axy']+v['vx_ay']+v['vy_ax']-v['a_bxy']-v['a_ix_y']-v['a_iy_x']
    eq('mixed two-input coefficient',coefficient(lhs-rhs,1,1)-target)
    # Independently recover equal-input polarization with the 1/2 convention.
    replacements={v['q_ay']:v['q_ax'],v['vy_ay']:v['vx_ax'],v['vx_ay']:v['vx_ax'],v['vy_ax']:v['vx_ax'],
        v['a_iy']:v['a_ix'],v['a_byy']:v['a_bxx'],v['a_bxy']:v['a_bxx'],
        v['a_ix_y']:v['a_ix_x'],v['a_iy_x']:v['a_ix_x'],v['a_iy_y']:v['a_ix_x']}
    xx=coefficient(lhs-rhs,2,0)+v['q_axy']/2
    eq('equal-input factorial',target.subs(replacements)-2*xx)
    for term in ['vx_ay','vy_ax','a_bxy','a_ix_y','a_iy_x']:
        assert s.diff(target,v[term])!=0;checks.append('omitted '+term+' detected')
    # Nested anomalies have two powers of hbar, regardless of input arity.
    nested=h*h*s.Symbol('nested_anomaly')
    eq('nested anomaly absent at one loop',coefficient(nested,0,0))
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        coefficient=str(target),condition='s0 a2(Vx,Vy)+(Vx,a1(Vy))+(Vy,a1(Vx)) = a1((Vx,Vy))+a2(s0Vx,Vy)+a2(s0Vy,Vx)',
        source=source,full_Q2=False,gate_changed=False,
        new_diagrams_computed=False,scope='Conditional arity/loop bookkeeping, separately typed from effective-action defect')
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[KNOWN — Fröb, Teorema7; DERIVED+CAS — extração polarizada; coeficientes físicos OPEN]

Fonte primária conferida: Markus B. Fröb, arXiv:1803.10235v3,
Teorema7, pp.36–37, https://arxiv.org/pdf/1803.10235v3 . A identidade geradora
usa os produtos temporais da mesma família e conserva a quebra clássica
I(F)=s0F+(F,F)/2. Ela não é uma avaliação do coeficiente na TGL.

Para derivar a condição pertinente, escreva A=hbar a+O(hbar²),
a[e^F]=a1(F)+a2(F,F)/2+..., F=u Vx+v Vy, com u,v pares independentes.
O termo aninhado A[A[e^F]⊗e^F] só contribui a partir de hbar².
A extração de hbar*u*v fornece:

 s0 a2(Vx,Vy)+(Vx,a1(Vy))+(Vy,a1(Vx))
 =a1((Vx,Vy))+a2(s0Vx,Vy)+a2(s0Vy,Vx).                    (*)

Na primeira aridade: s0a1(V)=a1(s0V). Para Vx=Vy=V, (*) tem
2(V,a1(V)) à esquerda e2a2(s0V,V) à direita, além de a1((V,V)).
As duas fórmulas têm fatores compatíveis com a expansão exponencial.

Esta separação evita uma troca de objetos na revisão Kimi: W1 da ação
efetiva não é a1, nem a inserção (I,W) é automaticamente o a2(s0V,V)
de produtos temporais. A fórmula de Jacobi auditada antes permanece válida
para seu objeto; (*) é a condição apropriada à família temporal escolhida.

Aplicação à bancada: o defeito das16componentes do SUBTOTAL não é ainda
o lado esquerdo de (*). Para efetuar a comparação, devem estar na mesma
normalização os termos a1 de uma entrada, o composto a1((Vx,Vy)) e as
duas inserções a2(s0Vx,Vy). s0V inclui as correntes de cutoff e o termo
-hdag[G,chi]w já derivado; não se pode impor s0V=0 para chi variável.
Os dois kernels Euler calculados são apenas parte dessas inserções.
O teste de posto2→3 não é, portanto, teste de toda esta identidade.

Não criamos novos operadores físicos nem ajustamos pesos para anular o
resíduo. Esta é a ordem de montagem que deve ser usada pelos leitores.
{len(checks)} controles algébricos de fatores/omissões, CPU{result['cpu_seconds']}s,
rc0. Nenhum diagrama adicional foi calculado neste script. Hipóteses globais
e coeficiente total continuam por conferir. Originais/gate intactos.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_condicao_temporal_polarizada.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']],source=source))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='TEMPORAL_WARD_CONSISTENCY_POLARIZED',target='A7.b',checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,source=source,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: Teorema7 conferido; condição temporal hbar*u*v separada da ação efetiva, {len(checks)} controles, CPU{result["cpu_seconds"]}s. Q2OPEN. AberturaSHA256={opening}.\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
