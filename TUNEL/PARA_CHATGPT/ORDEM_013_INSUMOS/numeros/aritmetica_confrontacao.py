# Aritmetica de conferencia (nao e artefato canonico). Constantes CODATA 2018 / IAU 2015 nominal.
import math
ALPHA = 7.2973525693e-3
beta = ALPHA*math.sqrt(math.e)            # runtime, nunca literal
G = 6.67430e-11; hbar = 1.054571817e-34; c = 299792458.0
GMsun = 1.3271244e20
Msun = GMsun/G
MPl = math.sqrt(hbar*c/G); tPl = math.sqrt(hbar*G/c**5)
print("beta =", beta)
M = 60*Msun
print("60 Msun: M/M_Pl =", M/MPl, " (M/M_Pl)^2 =", (M/MPl)**2)
# 'M/M_Pl^2' em unidades naturais (hbar=c=1) = G M (dimensao de TEMPO/COMPRIMENTO, nao de taxa)
t_GM = G*M/c**3
print("G M/c^3 [s] =", t_GM, " em tempos de Planck =", t_GM/tPl)
print("beta * (G M/c^3) [s] =", beta*t_GM, "  -> e um TEMPO; como 'taxa' exigiria 1/(tempo)")
print("beta / (G M/c^3) [1/s] =", beta/t_GM)
# GW250114: pSEOBNR (2509.08099): dtau220 = -0.01 (+0.10,-0.09) 90% ; tau220 = 4.09 (+0.42,-0.38) ms
tau = 4.09e-3
dlo = -0.01-0.09
# taxa extra Gamma_x: 1/tau = 1/tau_GR + Gamma_x  => (1+dtau) = 1/(1+Gamma_x tau_GR) => Gamma_x = (1/(1+dtau)-1)/tau_GR
Gx = (1/(1+dlo)-1)/tau
print("limite 90% (unilateral inferior de dtau=-0.10): Gamma_extra <~", Gx, "1/s  (mapeamento condicional: dephasing classico = amortecimento extra)")
# lei canonica declarada da TGL (a conferir por outra frente): Gamma_omega = 0.5*beta*tau_star*omega^2, tau_star ~ t_Planck
f220 = 251.7; w = 2*math.pi*f220
print("Gamma_TGL(omega_220; tau*=t_Pl) =", 0.5*beta*tPl*w**2, "1/s  [condicional a lei declarada]")
print("razao Gamma_extra_bound / Gamma_TGL =", Gx/(0.5*beta*tPl*w**2))

# Hipotese de mapeamento (NAO e predicao da TGL): Gamma = beta * c^3/(G M_det), remanescente GW250114
Mdet = 68.1*Msun; chi = 0.68
tM = G*Mdet/c**3
f1,f2,f3 = 1.5251,-1.1568,0.1292; q1,q2,q3 = 0.7000,1.4187,-0.4990   # BCW 2006 l=m=2 n=0
F = f1+f2*(1-chi)**f3; Q = q1+q2*(1-chi)**q3
omega = F/tM; tauGR = 2*Q/omega
Gam = beta/tM
dtau = 1/(1+Gam*tauGR)-1
print("GW250114 hip.: t_M=",tM,"s tauGR(BCW)=",tauGR,"s Gamma=beta/t_M=",Gam,"1/s  dtau_pred=",dtau)
sig = 0.095/1.645  # aproximacao gaussiana da semi-largura 90% (-0.09,+0.10)
print("distancia aprox a mediana -0.01 em sigmas (gauss aprox):", (dtau-(-0.01))/sig)

# Tentativas de reproduzir o "10^76" do texto colado (M = 60 Msun)
eV = 1.602176634e-19; GeV = 1e9*eV
M_GeV = M*c**2/GeV; MPl_GeV = MPl*c**2/GeV; MPlred_GeV = MPl_GeV/math.sqrt(8*math.pi)
cands = {
 "M/M_Pl (adim)": M/MPl,
 "(M/M_Pl)^2 (adim)": (M/MPl)**2,
 "4pi (M/M_Pl)^2 = S_BH/k_B (Schwarzschild)": 4*math.pi*(M/MPl)**2,
 "M/M_Pl^2 [GeV^-1]": M_GeV/MPl_GeV**2,
 "M/M_Pl,red^2 [GeV^-1]": M_GeV/MPlred_GeV**2,
 "M/M_Pl^2 [eV^-1]": (M_GeV*1e9)/(MPl_GeV*1e9)**2,
 "M/M_Pl^2 [kg^-1]": M/MPl**2,
 "GM/c^3 / t_Pl": (G*M/c**3)/tPl,
}
for k,v in cands.items(): print(f"{k:45s} = {v:.3e}  (log10 = {math.log10(v):.2f})")
