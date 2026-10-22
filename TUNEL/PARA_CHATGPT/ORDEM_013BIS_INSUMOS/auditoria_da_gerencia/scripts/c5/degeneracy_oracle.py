# Auditor C5: single-220 degeneracy, independent of bancada code. BCW (PRD 73,064030) l=m=2,n=0.
import math
ALPHA_FINE_CODATA_2018=7.2973525693e-3
beta=ALPHA_FINE_CODATA_2018*math.sqrt(math.e)
f1,f2,f3=1.5251,-1.1568,0.1292
q1,q2,q3=0.7000,1.4187,-0.4990
F=lambda a: f1+f2*(1-a)**f3          # M*omega_R
Q=lambda a: q1+q2*(1-a)**q3
wI=lambda a: F(a)/(2*Q(a))            # M*|omega_I|
for a in (0.0,0.68,0.9):
    x=beta*F(a)*Q(a)                  # R-B: Gamma*tau = 1/2 beta tau* omega^2 tau, tau*=M
    print("a=%.2f  x_RB(linear)=%.5f  delta_exact=%.5f"%(a,x,-x/(1+x)))
a=0.68
x=beta*F(a)*Q(a); dlntau=math.log(1/(1+x))   # tau -> tau/(1+x)
h=1e-6
dlnF=(math.log(F(a+h))-math.log(F(a-h)))/(2*h)
dlnQ=(math.log(Q(a+h))-math.log(Q(a-h)))/(2*h)
# ln f = ln F - ln M ; ln tau = ln M - ln wI = ln M - ln F + ln(2Q)
# hold f fixed: dlnM = dlnF*dchi ; dln tau = dlnM - dlnF*dchi + dlnQ*dchi = dlnQ*dchi
dchi=dlntau/dlnQ; dlnM=dlnF*dchi
print("mimic at a=0.68: dchi=%.4f  dM/M=%.4f  (Q=%.4f, dlnQ/dchi=%.4f)"%(dchi,math.expm1(dlnM),Q(a),dlnQ))
# GW250114 published remnant: chi_f=0.68+-0.01 (90%), Mf_det 68.1 +0.8/-0.9 (90%)
s_chi=0.01/1.645; s_M=0.85/1.645/68.1
print("in units of the published 1-sigma (gaussian from 90%%): dchi %.2f sigma, dM %.2f sigma"%(dchi/s_chi, math.expm1(dlnM)/s_M))
# SNR thresholds
for z40,lab in ((0.4083,'fixed source Fisher'),(0.0346,'free source min Phenom'),(0.0659,'free source max Phenom')):
    print(lab,"z@40=%.4f  SNR_5sigma=%.0f  N_events@SNR40=%.0f"%(z40,40*5/z40,25/z40**2))
for r in (0.1449,0.5979):
    print("nonlinear residual r=%.4f -> SNR for r=5: %.0f ; for 90%% power r=6.28: %.0f"%(r,40*5/r,40*6.2816/r))
