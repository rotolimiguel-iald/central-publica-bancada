# Independent Fisher oracle (auditor C5). Read-only on bancada files.
import numpy as np, math, json, hashlib
ROOT=r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
ALPHA_FINE_CODATA_2018=7.2973525693e-3
beta=ALPHA_FINE_CODATA_2018*math.sqrt(math.e)
print("beta runtime",beta)
G=6.67430e-11; c=299792458.0; Msun=1.98840987e30  # CODATA2018 G, IAU nominal GM_sun/G approx
inp=json.load(open(ROOT+r"\FISHER_INPUTS.json",encoding="utf-8"))
q=[r for r in inp['mode_220'] if r['spin']==0.68][0]
wR,wI=q['omega_real'],abs(q['omega_imag'])
M=68.1*G*Msun/c**3
f0=wR/(2*math.pi*M); tau=M/wI; d=1/tau
x=0.5*beta*wR**2/wI  # R-B: Gamma*tau with tau*=GM/c^3
print("f220 %.3f Hz tau %.5f s Q %.4f x_RB %.6f delta_exact %.6f"%(f0,tau,math.pi*f0*tau,x,-x/(1+x)))
# PSD
raw=np.loadtxt(ROOT+r"\cache\psd\aLIGO_O4_high_asd.txt")
f=np.arange(20.,2048.0001,0.125); df=0.125
psd=np.exp(np.interp(np.log(f),np.log(raw[:,0]),np.log(raw[:,1])))**2
def H(A,phi,lf,ld):
    fr=math.exp(lf); dd=math.exp(ld)
    # h(t)=A e^{-dd t} cos(2pi fr t + phi), t>=0 ; analytic FT
    zm=dd+2j*np.pi*(f-fr); zp=dd+2j*np.pi*(f+fr)
    return A*0.5*(np.exp(1j*phi)/zm+np.exp(-1j*phi)/zp)
def inner(u,v): return float(np.sum(4*df*(u.conj()*v).real/psd))
p0=np.array([1.0,0.0,math.log(f0),math.log(d)])
h0=H(*p0); nrm=math.sqrt(inner(h0,h0))
eps=[1e-6,1e-6,1e-7,1e-7]
D=[]
for i in range(4):
    pp=p0.copy(); pm=p0.copy(); pp[i]+=eps[i]; pm[i]-=eps[i]
    D.append((H(*pp)-H(*pm))/(2*eps[i])/nrm)
F=np.array([[inner(a,b) for b in D] for a in D])
out={}
for snr in [10,20,40,80,200,600]:
    Fs=F*snr**2
    fixed=Fs[3,3]-Fs[3,:2]@np.linalg.solve(Fs[:2,:2],Fs[:2,3])
    ffree=Fs[3,3]-Fs[3,:3]@np.linalg.solve(Fs[:3,:3],Fs[:3,3])
    s1=1/math.sqrt(fixed); s2=1/math.sqrt(ffree)
    z1=x/s1; z2=x/s2
    out[snr]=(s1,s2,z1,z2,math.ceil(25/z1**2),math.ceil(25/z2**2))
    print("SNR %4d sigma_fixed %.5f sigma_ffree %.5f z %.4f %.4f  N5 %d %d  lnB+ %.4f  analytic 2/rho %.5f"%(snr,s1,s2,z1,z2,out[snr][4],out[snr][5],z1*z1/2,2/snr))
# compare with bancada
B=json.load(open(ROOT+r"\C5_FISHER.json",encoding="utf-8"))
for r in B['records']:
    if r['psd']=='O4' and r['reading']=='R-B':
        mine=out[int(r['snr_ringdown'])]
        s=mine[0] if r['scenario'].startswith('MASS') else mine[1]
        print(r['snr_ringdown'],r['scenario'][:10],"bancada sigma %.6f mine %.6f rel %.2e | bancada z %.5f"%(r['sigma_delta_local'],s,(r['sigma_delta_local']-s)/s,r['z_local']))
# SNR for 5 sigma (median) single event, fixed source
print("SNR_5sigma_fixed (R-B) =", 5/ (x/(out[40][0]*40)))
