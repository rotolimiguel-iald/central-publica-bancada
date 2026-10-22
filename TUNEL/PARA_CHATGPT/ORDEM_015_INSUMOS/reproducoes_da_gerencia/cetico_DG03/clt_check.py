# Cetico DG-03: soma padronizada de N=3328 termos t5 INDEPENDENTES (curtose por evento) vs t5 com escala COMPARTILHADA (modelo da bancada).
import numpy as np, scipy.stats as st, json
rng=np.random.default_rng(13220002); N=3328; draws=2_000_000; chunk=10_000
c_ind=c_sh=0
for _ in range(draws//chunk):
    g=rng.standard_normal((chunk,N))
    z_ind=(g*np.sqrt(3/rng.chisquare(5,(chunk,N)))).sum(1)/np.sqrt(N)
    z_sh=(g.sum(1)/np.sqrt(N))*np.sqrt(3/rng.chisquare(5,chunk))
    c_ind+=int((z_ind>=3.7837).sum()); c_sh+=int((z_sh>=3.7837).sum())
out={"N":N,"draws":draws,"threshold":3.7837,"FPR_independent_t5":c_ind/draws,"FPR_shared_t5":c_sh/draws,
     "gaussian_p_3.7837":float(st.norm.sf(3.7837)),"nota":"independente ~ gaussiano (CLT); compartilhado = cauda pesada; bancada mediu 7.727e-5 em z>=5 com escala compartilhada"}
print(json.dumps(out,indent=1)); json.dump(out,open("CLT_CHECK.json","w"),indent=1)
