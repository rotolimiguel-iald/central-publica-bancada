# Sanity check: Berti-Cardoso-Will 2006 (gr-qc/0512160, Table tab:fitQNMsl2, l=m=2,n=0) vs GW250114 numbers.
import math
GM_sun = 1.3271244e20   # m^3 s^-2 (IAU 2015 nominal)
c = 299792458.0
tsun = GM_sun / c**3
f1,f2,f3 = 1.5251,-1.1568,0.1292
q1,q2,q3 = 0.7000,1.4187,-0.4990
def qnm(Mdet, j):
    F = f1 + f2*(1-j)**f3          # M*omega
    Q = q1 + q2*(1-j)**q3          # Q = pi f tau
    omega = F/(Mdet*tsun)
    f = omega/(2*math.pi)
    tau = Q/(math.pi*f)
    return F, Q, f, tau
for M,j in [(68.1,0.68),(67.2,0.67),(68.9,0.69)]:
    F,Q,f,tau = qnm(M,j)
    print(f"Mdet={M} Msun chi={j}: M*omega={F:.4f} Q={Q:.3f} f220={f:.1f} Hz tau220={tau*1e3:.3f} ms gamma=1/tau={1/tau:.1f} Hz  Gamma/omega=1/(2Q)={1/(2*Q):.4f}")
print("t_Msun =", tsun)
