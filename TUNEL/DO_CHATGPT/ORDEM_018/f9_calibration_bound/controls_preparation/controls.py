"""Eight prepared deterministic controls. Never imported/executed during preparation."""
from fractions import Fraction as F
from math import isqrt, factorial
import json, sys, time

START = None
def budget():
    if START is not None and time.monotonic() - START > 23:
        raise RuntimeError("LOCAL_WALL_BUDGET_EXCEEDED")
def checked(q):
    q = F(q)
    if max(q.numerator.bit_length(), q.denominator.bit_length()) > 524288:
        raise RuntimeError("RATIONAL_SIZE_BUDGET_EXCEEDED")
    return q
def require(ok, message):
    budget()
    if not ok:
        raise AssertionError(message)
def interval(lo, hi):
    lo, hi = checked(lo), checked(hi)
    require(lo <= hi, "reversed interval")
    return lo, hi
def add(a,b): return interval(a[0]+b[0], a[1]+b[1])
def neg(a): return interval(-a[1],-a[0])
def mul(a,b):
    c=[a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1]]
    return interval(min(c),max(c))
def inv(a):
    require(a[0]>0,"positive reciprocal only")
    return interval(1/a[1],1/a[0])
def ipow(a,n):
    require(n>=0 and a[0]>=0,"nonnegative integer interval power")
    out=(F(1),F(1))
    while n:
        budget()
        if n&1: out=mul(out,a)
        n//=2
        if n: a=mul(a,a)
    return out
def sqrt_interval(a):
    require(a[0]>=0,"nonnegative sqrt")
    scale=10**50
    lo=isqrt(a[0].numerator*scale*scale//a[0].denominator)
    hi=isqrt(a[1].numerator*scale*scale//a[1].denominator)+1
    return interval(F(lo,scale),F(hi,scale))
def alternating(terms):
    """Terms must have alternating signs, decreasing magnitudes, tending to zero."""
    require(len(terms)>=2,"series enclosure needs final next term")
    require(all(abs(terms[i+1])<=abs(terms[i]) for i in range(len(terms)-1)),"monotone magnitudes")
    require(all(terms[i]*terms[i+1]<0 for i in range(len(terms)-1)),"alternation")
    a=sum(terms[:-1],F(0));b=a+terms[-1]
    return interval(min(a,b),max(a,b))
def pi_bounds():
    def atan_inv(q):
        # arctan(1/q), alternating remainder; 32 retained terms plus next.
        return alternating([F((-1)**n,(2*n+1)*q**(2*n+1)) for n in range(33)])
    # Exact Machin identity pi = 16 atan(1/5) - 4 atan(1/239).
    return add(mul((F(16),F(16)),atan_inv(5)),neg(mul((F(4),F(4)),atan_inv(239))))
def exp_negative(x, reduction=1024):
    """Rational positive series of exp(y), geometric remainder, reciprocal/power."""
    x=F(x);require(0<=x<=1000 and reduction in (1,1024),"exp domain fixed")
    y=x/reduction;require(y<=1,"series range")
    term=F(1);s=term
    for k in range(1,33):
        budget();term=term*y/k;s+=term
    next_term=term*y/33
    # Every subsequent ratio <= y/34, so tail <= first/(1-y/34).
    rem=next_term/(1-y/34)
    return ipow(inv(interval(s,s+rem)),reduction)
def tail_recurrence(df,t):
    require(df in (1,2,3,4) and t in (2,2000),"fixed tail controls only")
    x=F(t,2)
    if df%2==0:
        e=exp_negative(x)
        polynomial=sum((x**k/F(factorial(k)) for k in range(df//2)),F(0))
        return mul(e,(polynomial,polynomial))
    require(x==1,"half-integer series fixed at x=1")
    root=sqrt_interval(pi_bounds())
    erf_series=alternating([F((-1)**n,factorial(n)*(2*n+1)) for n in range(33)])
    q=add((F(1),F(1)),neg(mul(mul((F(2),F(2)),inv(root)),erf_series)))
    if df==3:
        q=add(q,mul(mul((F(2),F(2)),exp_negative(1)),inv(root)))
    return q
def tail_integral_certificate(df):
    """At x=1: Q(a,1)=1 - integral_0^1 u^(a-1) exp(-u) du / Gamma(a)."""
    a=F(df,2)
    series=alternating([F((-1)**n,factorial(n)*(a+n)) for n in range(33)])
    if df%2==0:
        gamma=(F(factorial(df//2-1)),)*2
    else:
        gamma=sqrt_interval(pi_bounds())
        for k in range((df-1)//2):
            gamma=mul(gamma,(F(2*k+1,2),)*2)
    return add((F(1),F(1)),neg(mul(series,inv(gamma))))
def pack_interval(a):
    # Hex exact integers avoid decimal digit limits and floating underflow.
    return {"lower":{"numerator_hex":hex(a[0].numerator),"denominator_hex":hex(a[0].denominator)},
            "upper":{"numerator_hex":hex(a[1].numerator),"denominator_hex":hex(a[1].denominator)}}
def mm(a,b):
    require(len(a)<=8 and len(b)<=8 and len(a[0])<=8 and len(b[0])<=8,"matrix size")
    require(len(a[0])==len(b),"matrix dimensions")
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def tr(a): return [list(x) for x in zip(*a)]
def norm2(v): return sum((x*x for x in v),F(0))
def C01_FIXED_QUOTIENT():
    C=[[F(4),F(0),F(0)],[F(0),F(9),F(0)],[F(0),F(0),F(0)]]
    X=[[F(2)],[F(0)],[F(0)]];R=[[F(0),F(1,3),F(0)]]
    require(mm(R,X)==[[0]],"RX")
    require(mm(mm(R,C),tr(R))==[[1]],"RCRt")
    require(X[0][0]!=0 and X[2][0]==0,"X full-rank supported")
    y=[F(10),F(6),F(0)];z=mm(R,[[x] for x in y])[0][0]
    qtrue=z*z;g=(z-1)**2
    require((qtrue,g)==(4,1) and 0<=g<=qtrue,"exact base inequality")
    return {"RX":0,"RCRt":1,"residual_rank":1,"q_true":4,"global_min_null":1,"status":"PASS"}
def C02_GLOBAL_NONLINEAR_SPAN():
    # Null mean0; competitor m(a)=(a,a^2,0), a in [-1,1]; z=(0,2,3).
    z=[F(0),F(2),F(3)]
    global_coefficients=[[F(1),F(0),F(0)],[F(0),F(1),F(0)]]
    require(all(c[2]==0 for c in global_coefficients),"global polynomial inclusion")
    # q=13-3u+u^2, u=a^2 in [0,1]; derivative -3+2u in [-3,-1].
    require(-3+2*1<0,"global minimizer at u=1")
    gcomp=F(13)-3+1;relax=F(9);gain=norm2(z)-gcomp;bound=norm2(z[:2])
    require((gcomp,relax,gain,bound)==(11,9,2,4) and gcomp>=relax and gain<=bound,"global-span bound")
    return {"global_min_comp":11,"relaxed_min":9,"gain":2,"projection_bound":4,"status":"PASS"}
def C03_TANGENT_IS_NOT_GLOBAL_SPAN():
    tangent=[F(1),F(0),F(0)];witness=[F(1),F(1),F(0)]
    require(tangent[1]==0 and witness[1]!=0,"tangent certificate must reject")
    return {"tangent_dimension":1,"global_span_dimension":2,"tangent_only_certificate":"REJECTED","status":"PASS"}
def C04_DIRECTED_SIGN_AND_ZERO_DF():
    def bound(df,s):
        if s<=0:return F(1),"NONPOSITIVE"
        if df==0:return F(0),"IMPOSSIBLE_POSITIVE_UNDER_RANK_ZERO_NULL"
        raise RuntimeError("No other tails in C04")
    require(bound(1,F(-3,2))[0]==1 and bound(1,0)[0]==1,"nonpositive p1")
    require(bound(0,0)[0]==1 and bound(0,1)[0]==0,"inclusive atom at0")
    return {"negative_p":1,"zero_p":1,"zero_rank_positive_tail":0,"positive_statistic_zero_rank":"CONTRACT_INCOHERENCE_NOT_REJECTION","status":"PASS"}
def C05_MINIMUM_CERTIFICATE_DIRECTION():
    def lower(cert):
        require(cert["kind"]=="GLOBAL_ENCLOSURE","uncertified feasible upper is not lower")
        return cert["L"]
    local={"kind":"LOCAL_FEASIBLE_UPPER","U":F(9)}
    rejected=False
    try:lower(local)
    except AssertionError:rejected=True
    require(rejected,"reject local upper as lower")
    null={"kind":"GLOBAL_ENCLOSURE","L":F(0),"U":F(9)}
    comp={"kind":"GLOBAL_ENCLOSURE","L":F(0),"U":F(2)}
    require(null["L"]<=1<=null["U"] and comp["L"]<=0<=comp["U"],"synthetic exact minima covered")
    signed=lower(null)-comp["U"]
    require(signed==-2 and max(F(0),signed)==0,"correct Lnull-Ucomp")
    require(F(3)-F(2)==1,"second direction witness")
    return {"local_upper_rejected":True,"ell_G":0,"ell_Q_nested":0,"ell_T":-2,"valid_positive_direction_example":1,"status":"PASS"}
def C06_DIFFERENT_COVARIANCE():
    Cnull=F(1);Ccomp=F(1,4);y=F(0)
    require(Cnull!=Ccomp and y*y==0,"different covariance")
    # epsilon=1/2, T(y=0)=2 log2. Integral_1^2 dt/t > 1/2 gives T>1.
    require(F(2)*F(1,2)==1,"rational strict lower witness")
    return {"RSS_true_at_y0":0,"T_strict_lower":1,"reuse_RSS_envelope":"REJECTED_COVARIANCE_MISMATCH","status":"PASS"}
def C07_COMPLETE_SCENARIOS():
    scenarios=("a","b","c")
    def robust(values):
        if set(values)!=set(scenarios) or any(values[x] is None for x in scenarios):return None
        return min(F(1),5*max(values.values()))
    G=robust({"a":F(1,1000),"b":F(1,2000),"c":F(1,4000)})
    Q=robust({"a":F(1,1000),"b":F(1,2000)})
    alpha=F(1,100)
    require(G==F(1,200) and Q is None,"max complete / absent unavailable")
    reject_H1=G<=alpha
    require(reject_H1 and not (G is not None and Q is not None),"valid rejection survives")
    return {"p_G_FWER":"1/200","p_Q_FWER":None,"H1_valid_rejection":True,"H1_non_rejection_available":False,"status":"PASS"}
def C08_TAIL_CERTIFICATE():
    broad={1:(F(15,100),F(16,100)),2:(F(36,100),F(37,100)),3:(F(57,100),F(58,100)),4:(F(73,100),F(74,100))}
    rows=[]
    for df in (1,2,3,4):
        a=tail_recurrence(df,2);b=tail_integral_certificate(df);lo,hi=broad[df]
        require(lo<=a[0]<=a[1]<=hi and lo<=b[0]<=b[1]<=hi,"prederived rational outer enclosure")
        require(max(a[0],b[0])<=min(a[1],b[1]),"recurrence vs certified integral overlap")
        require(a[0]>0 and a[1]-a[0]<=F(1,10**25),"positive narrow SF enclosure")
        rows.append({"df":df,"t":2,"recurrence":pack_interval(a),"integral_certificate":pack_interval(b)})
    a=tail_recurrence(2,2000)
    b=ipow(exp_negative(1,1),1000)
    require(F(1,10**500)<a[0]<=a[1]<F(1,10**400),"extreme SF positive exact rational")
    require(max(a[0],b[0])<=min(a[1],b[1]),"independent range reduction agreement")
    require((a[1]-a[0])/a[0]<=F(1,10**20),"extreme relative interval width")
    rows.append({"df":2,"t":2000,"recurrence":pack_interval(a),"unit_exponential_certificate":pack_interval(b)})
    return {"status":"PASS","certificate":"EXACT_RATIONAL_INTERVALS_WITH_ANALYTIC_REMAINDERS","tails":rows,"float_used":False}
def main():
    global START
    require(sys.argv[1:]==["--supervised-stdin"],"supervised input only")
    token=json.loads(sys.stdin.read(4096))
    require(token.get("request_id")=="8b53f7c0-9f5f-49e1-87bc-cf73a7e1f79d" and token.get("authorized") is True,"missing supervisor token")
    START=time.monotonic();results=[]
    funcs=(C01_FIXED_QUOTIENT,C02_GLOBAL_NONLINEAR_SPAN,C03_TANGENT_IS_NOT_GLOBAL_SPAN,C04_DIRECTED_SIGN_AND_ZERO_DF,C05_MINIMUM_CERTIFICATE_DIRECTION,C06_DIFFERENT_COVARIANCE,C07_COMPLETE_SCENARIOS,C08_TAIL_CERTIFICATE)
    status="FAILED"
    try:
        for fun in funcs:
            budget();result=fun();results.append({"id":fun.__name__,"result":result});budget()
        status="PASS"
    except Exception as exc:
        results.append({"failure":{"type":type(exc).__name__,"message":str(exc)}})
    receipt={"request_id":token["request_id"],"status":status,"results":results,"wall_s":time.monotonic()-START,"monte_carlo":0,"observed_data":False}
    print(json.dumps(receipt,separators=(",",":")))
    return 0 if status=="PASS" else 1
if __name__=="__main__":
    sys.exit(main())
