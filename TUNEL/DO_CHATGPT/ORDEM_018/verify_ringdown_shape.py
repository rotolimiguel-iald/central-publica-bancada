"""Independent QR check of a nuisance projection, frozen calibration design only."""
import json,time
import numpy as np
from audit_inputs import ROOT,save_json,file_info
start=time.perf_counter()
audit_path=ROOT/'preregistros'/'AUDITORIA_PREREGISTROS_F3.json'
a=json.loads(audit_path.read_bytes())
source=ROOT.parents[1]/'PARA_CHATGPT'/'ORDEM_018_INSUMOS'/'RAMO_B_V1__PREREGISTRO_RAMO_B_RINGDOWN_V1.json'
s=json.loads(source.read_bytes());rows=s['sigma_por_evento_A31_so_sigma_e_spin']
# Cross-check stored frozen theoretical predictions independently of the generator.
d=np.array([r['delta_exato'] for r in rows],dtype=float)
sig=np.array([r['sigma_std'] for r in rows],dtype=float)
out=[]
for ref in a['ringdown_nuisance_design_diagnostic']['profiles']:
 sy=ref['sigma_sys_diagonal_scenario'];sd=np.sqrt(sig**2+sy**2)
 X=np.column_stack([np.ones(len(sig)),sig])/sd[:,None]
 Q,R=np.linalg.qr(X,mode='reduced')
 projected=d/sd-Q@(Q.T@(d/sd));norm=float(np.linalg.norm(projected))
 expected=ref['after_free_c0_plus_kc_sigma_norm']
 assert abs(norm-expected)<1e-10
 assert np.linalg.norm(X.T@projected)<1e-10
 out.append(dict(systematic_diagonal=sy,qr_norm=norm,absolute_difference=abs(norm-expected)))
save_json(ROOT/'VERIFICACAO_INDEPENDENTE_RINGDOWN_SHAPE.json',{'statute':'REAL_LOCAL_QR_CROSSCHECK_CONDITIONAL_DESIGN_ONLY','source':file_info(source),'audit':file_info(audit_path),'script':file_info(__file__),'cases':out,'all_pass':True,'D_opened':False,'observed_dtau_used':False,'assumption':'Unconstrained c0 and kc; no auxiliary calibration. Not an observed significance or physical verdict.','elapsed_seconds':time.perf_counter()-start})
print(out)
