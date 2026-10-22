"""Canonical smooth-times-distribution completion, without changing singular f/f graphs."""
from pathlib import Path
from datetime import datetime, timezone
from itertools import combinations_with_replacement
from functools import lru_cache
import json,time
import sympy as s
import balanced_log_pair_engine as E
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

D=H/'smooth_line_compatibility'

@lru_cache(None)
def derivative(w,word):
    for i in word:w=s.diff(w,E.x[i])
    return s.expand(w)

def multiply(w,local):
    """Multiplication x_i d^alpha delta = -alpha_i d^(alpha-e_i) delta."""
    out=0
    for powers,c in s.Poly(w,*E.x).terms():
        a=local
        for i,n in enumerate(powers):a=(-1)**n*s.diff(a,E.Q[i],n)
        out+=c*a
    return s.expand(out)

@lru_cache(None)
def correction(profile,w,u,v):
    # Rraw commutes with smooth polynomial multiplication. The required
    # extension is (D^v w) D^u Rraw(F), rather than Rraw[(D^u F)(D^v w)].
    return -multiply(derivative(w,v),E.contact(E.line(*profile,()),u))

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc);start=time.process_time()
    sources=[Path(__file__),H/'balanced_log_pair_engine.py',H/'logarithmic_contact_engine.py',
        H/'balanced_log_pair_v3/manifest.json',H/'balanced_log_pair_v3/results.json']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        rule='For a smooth polynomial W, N[(D^u F)(D^v W)] = (D^v W) D^u Rraw(F)',
        prior_defect='naive balanced extension gives E(f,1)=3/4 and E(1,f)=-1/4',
        expected_constant_line=[1,0,0],
        limitations='Completion restricted to one smooth line; global overlap compatibility with singular/log pairs not established',
        sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
    checks=[]
    def eq(name,a,b=0):
        assert s.expand(a-b)==0,(name,a,b);checks.append(name)
    words=[tuple(w) for n in range(4) for w in combinations_with_replacement(range(4),n)]
    smooth=[s.Integer(1)]+list(E.x)+[E.x[i]*E.x[j] for i in range(4) for j in range(i,4)]
    for profile in [(1,0),(0,1)]:
        for w in smooth:
            for u in words:
                for v in words:
                    if len(u)+len(v)>3:continue
                    value=correction(profile,w,u,v)
                    # Independent polynomial Leibniz expansion of D^u R(F).
                    # More importantly, test the total derivative against raw product contacts.
                    if not derivative(w,v):eq('zero derivative on smooth line',value,0)
                    if len(u)+len(v)<=2:
                        raw=E.line(*profile,u)*derivative(w,v)
                        for i in range(4):
                            lhs=correction(profile,w,tuple(sorted(u+(i,))),v)+correction(profile,w,u,tuple(sorted(v+(i,))))-E.Q[i]*value
                            eq('smooth product total derivative identity',lhs,-E.contact(s.expand(raw),(i,)))
            print(json.dumps(dict(profile=profile,smooth=str(w),checks=len(checks),cpu_seconds=time.process_time()-start)),flush=True)
    f,lg,one=(1,0),(0,1),(0,0)
    ef1=sum(correction(f,s.Integer(1),(i,i),()) for i in range(4))
    e1f=sum(correction(f,s.Integer(1),(),(i,i)) for i in range(4))
    cross=sum(correction(f,s.Integer(1),(i,),(i,)) for i in range(4))
    eq('Euler singular line times one',ef1,1)
    eq('Euler one times singular line',e1f,0)
    eq('cross with derivative of one',cross,0)
    # Expose the actual finite change from the naive smooth subfamily.
    changes=[s.expand(ef1-E.euler_correction(f,one)),s.expand(e1f-E.euler_correction(one,f)),
        s.expand(cross-sum(E.correction(f,one,(i,),(i,)) for i in range(4)))]
    for a,b in zip(changes,[s.Rational(1,4),s.Rational(1,4),-s.Rational(1,4)]):eq('explicit smooth subfamily finite change',a,b)
    eq('total derivative normalization unchanged',changes[0]+changes[1]+2*changes[2],0)
    old=json.loads((H/'balanced_log_pair_v3/results.json').read_bytes())
    e0=E.euler_correction(f,f);geometry=s.sympify(old['geometric_operator_contact'])
    radial=s.expand(ef1/4-E.euler_correction(f,lg)/2-E.euler_correction(lg,f)/2+geometry)
    eq('smooth-compatible radial O(K) zerojet',radial,s.Rational(1,8))
    # sqrt(g)=1-K*z/2; multiply z into the already extended flat contact.
    density_shift=-multiply(sum(x*x for x in E.x),e0)/2
    eq('density conversion',density_shift,s.Rational(3,8))
    densitized=s.expand(radial+density_shift)
    eq('densitized radial zerojet',densitized,s.Rational(1,2))
    # Euler smooth remainder itself is zero for a constant W0, but W0 times
    # the delta source on the singular line is retained, not discarded.
    w0=s.symbols('W0')
    eq('constant smooth reference dependence',w0*ef1,w0)
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        smooth_monomials=len(smooth),profile_count=2,Euler_constant_line=list(map(str,[ef1,e1f,cross])),
        finite_change_from_naive=list(map(str,changes)),
        radial_scalar_Euler_zerojet_K=str(radial),density_shift_K=str(density_shift),densitized_zerojet_K=str(densitized),
        W0_contribution='W0*CE*delta',pure_singular_pair_changed=False,
        global_family_admissibility=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — compatibilidade com multiplicação por linha suave; extensão parcial]

Uma linha constante tem derivada zero antes e depois da extensão.
A subfamília ingênua não respeitava isso: E(f,1)=3/4,E(1,f)=-1/4.
O produto de uma distribuição com função suave já está definido.
Portanto N[(D^u F)(D^v W)]=(D^v W)D^u Rraw(F) impõe a diferença
Delta=- (D^v W) [Rraw(D^u F)-D^u Rraw(F)]. Isto não é escolha de
vácuo nem ajuste para anular uma anomalia. É compatibilidade com o
produto suave, ainda faltando verificar uma família temporal completa.

Para W=1, Euler na primeira linha=1, na segunda=0, cruzado=0 (em CE).
A mudança finita relativa à subfamília ingênua é (+1/4,+1/4,-1/4).
Sua soma de Leibniz é zero. Os grafos f/f planos não foram recalculados
nem modificados. {len(smooth)}monômios suaves até grau2 e os perfis
f e log foram conferidos com derivadas de ordem total até3.

Com H=1/z+K/4-K log(mu²z)/2, o cálculo RADIAL sem derivadas adicionais
conserva o contato geométrico -1/8. A parcela de ordemK torna-se
CE*K/8; converter Box_g a sqrt(g)Box_g acrescenta3CE*K/8,
totalizando CE*K/2. Uma constante suave W0 acrescenta CE*W0.
Essas contas distinguem operador, densidade e estado; não selecionam W0.
Continuam ausentes a família covariante completa, os jatos bilocais
e os vértices de curvatura. Não são o valor da anomalia Q2 inteira.

{len(checks)}controles; CPU{result['cpu_seconds']}s; rc0.
Sem chamada externa, kernel ou gate. AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_compatibilidade_linha_suave.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='SMOOTH_LINE_COMPATIBILITY',target='A7.b',checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: compatibilidade produto suave auditada; contato radial K/8, densitizado K/2, normalizadosCE;{len(checks)}controles CPU{result["cpu_seconds"]}s. FamíliaQ2completaOPEN. AberturaSHA256={opening}.\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
