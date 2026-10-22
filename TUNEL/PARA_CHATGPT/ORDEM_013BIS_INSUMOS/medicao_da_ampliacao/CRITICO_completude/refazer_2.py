# -*- coding: utf-8 -*-
"""MC complementar do critico: poder do LRT (sigma_jit 0.0228, N 36-42), fator N90/N5, SNR equivalente ao corte
sigma<=0.06/0.10 (ajuste de B), anos de O5 por taxa. Gera REFEITOS_2.json. Mesmo codigo rodado inline em 22/09/2026."""
import json, math, numpy as np
from scipy import stats
rng=np.random.default_rng(7)
sm=0.013636117181334192
def lrt_vec(Y, s2m, grid):
    N=Y.shape[1]; mu=Y.mean(axis=1,keepdims=True); ss=((Y-mu)**2).sum(axis=1)
    l0=-0.5*(ss/s2m+N*math.log(s2m)); best=l0.copy()
    for s2 in grid:
        v=s2m+s2; best=np.maximum(best,-0.5*(ss/v+N*math.log(v)))
    return 2*(best-l0)
grid=np.geomspace(1e-7,0.5,300)
out={}
for sj in (0.0228,):
    for N in (36,37,38,39,40,41,42):
        Y=rng.normal(0,math.sqrt(sm**2+sj**2),size=(8000,N)); L=lrt_vec(Y,sm**2,grid)
        out[f"sj={sj},N={N}"]=float((L>25).mean())
f90=((5+stats.norm.ppf(0.9))/5)**2
out["fator_N90_sobre_N5_filtro_casado"]=f90
out["N90_RB"]={"GW250114_like_O4":213.2*f90,"mistura31_O4":2062*f90,"GW250114_like_O5_banda":[50*f90,87*f90]}
A,p=3.026648868069853,-0.8599154128207724
out["SNR_rede_para_sigma_0p06_ajuste_B"]=(0.06/A)**(1/p)
out["SNR_rede_para_sigma_0p10_ajuste_B"]=(0.10/A)**(1/p)
for g in (1.5625,1.7857):
    out[f"anos_O5_RB_mistura_g={g}"]=[646.7/(14.4828*g**3), 864.4/(14.4828*g**3)]
print(json.dumps(out,indent=1))
json.dump(out,open("REFEITOS_2.json","w"),indent=1)
