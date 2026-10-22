"""One ordered E_h[G,chi]w -- Vghost contact; normalization diagnostic only."""
from functools import lru_cache
import sympy as s
from logarithmic_contact_engine import differentiated,residue,A,Q
from mixed_b_h_current_engine_v3 import current_terms
from position_metric_bubble_engine import LABELS

TAU=s.Symbol('tau')
SIG=(1,1,1,1)

@lru_cache(None)
def euler_line_contact(euler_word,ghost_word):
    """Finite part [(box z^(tau*a-1)) derivatives * derivatives z^((1-tau)*a-1)] / CE.

    box coefficient vanishes at a=0, so only its -4*tau*a term times the
    simple-pole residue contributes. Other derivative coefficients evaluated at a=0.
    Derivatives are all positive d/d(X-Y); endpoint minus signs supplied separately.
    """
    answer=s.Integer(0)
    for (n,xp),c in differentiated(2,tuple(euler_word),SIG).items():
        for (m,yp),v in differentiated(1,tuple(ghost_word),SIG).items():
            power=tuple(x+y for x,y in zip(xp,yp))
            answer+=c.subs(A,0)*v.subs(A,0)*residue(n+m,power,SIG)
    return s.expand(-4*TAU*answer)

def ordered_descendant(lam,eta):
    """Return B_ur(D) in integral exp((lam+eta).x) c_u B_ur(D)c_r.

    Raw product I_E,X Vghost,Y, not the effective-action sign or expansion factorial.
    I_E=sum_A E_A [G,chi]w_A. E_A is derivative w.r.t. independent h_A.
    Vghost has original odd ordering barc,c. Both w contractions are kept.
    No antibracket multiplier, exchange of cutoffs or final projection inserted.
    """
    lam=tuple(lam);eta=tuple(eta);L=tuple(lam[i]+eta[i] for i in range(4))
    B=s.zeros(4);count=0
    for r in range(4):
        for mu in range(4):
            e=tuple(int(i==mu) for i in range(4))
            for (bar,Aidx,hw,kw),zcoef in current_terms(r,e).items():
                i,j=LABELS[Aidx]
                for nu,scale in [(j,lam[i]),(i,lam[j])]:
                    if not scale:continue
                    for rho in range(4):
                        cases=[]
                        # c_rho d_rho c_nu barc c_r: first pairing crosses one odd field.
                        if rho==bar:cases.append((nu,(rho,),(),-1))
                        if nu==bar:cases.append((rho,(),(rho,),1))
                        for u,external_word,internal_word,wick_sign in cases:
                            for bw,cutoff_scale in [((mu,),1),((),eta[mu])]:
                                if not cutoff_scale:continue
                                coef=-s.Rational(zcoef)*scale*cutoff_scale*wick_sign
                                coef*=(-1)**(len(hw)+len(bw))
                                kernel=euler_line_contact(tuple(sorted(hw)),tuple(sorted(internal_word+bw)))
                                # Move cutoff_X through delta, then shift derivatives from left c to right c.
                                local=kernel.subs({Q[k]:Q[k]+eta[k] for k in range(4)},simultaneous=True)
                                local*=s.prod(-Q[k]-L[k] for k in external_word)*s.prod(Q[k] for k in kw)
                                B[u,r]+=coef*local;count+=1
    return B.applyfunc(s.expand),count

def weighted_defect(B,L):
    adj=B.T.applyfunc(lambda f:s.expand(f.subs({Q[i]:-Q[i]-L[i] for i in range(4)},simultaneous=True)))
    return (B-adj).applyfunc(s.expand)
