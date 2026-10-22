import sys, json, math
sys.path.insert(0, r'C:/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/ordem013/auditoria/C3_C7_codigo_pacote/mod')
sys.path.insert(0, r'C:/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/ordem013/auditoria/C3_C7_codigo_pacote')
import numpy as np
import tgl_ringdown_prediction as P
from leaver_indep import qnm as leaver
G = json.load(open(r'C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013_INSUMOS/revisao_da_gerencia/revisao_numeros_result.json', encoding='utf-8'))['g']
w, A = 0.3737-0.0890j, 4+0j
rows = []
for chi in [0.0, 0.5, 0.68, 0.6784704444609746, 0.9, 0.98, 0.99]:
    w, A = leaver(chi, w, A)
    mw = 1.5251-1.1568*(1-chi)**0.1292; q = 0.7+1.4187*(1-chi)**(-0.4990)
    bcw = complex(mw, -mw/(2*q))
    pe = P.prediction(68.1, chi, 'R-MOD', qnm_dimensionless=w)
    pb = P.prediction(68.1, chi, 'R-MOD', qnm_dimensionless=bcw)
    rb = P.prediction(68.1, chi, 'R-B') if chi>=0 else None
    rbe = P.prediction(68.1, chi, 'R-B', qnm_dimensionless=w)
    r = dict(chi=chi, RMOD_exact=pe['delta_tau'], RMOD_bcw=pb['delta_tau'], ratio_bcw_exact=pb['delta_tau']/pe['delta_tau'],
             RB_bcw=rb['delta_tau'], RB_exact=rbe['delta_tau'])
    key = f'{chi}'
    if key in G:
        r['gerencia_leaver_dex_co'] = G[key]['leaver']['dex_co']; r['gerencia_bcw_dex_co'] = G[key]['bcw']['dex_co']
    rows.append(r); print(json.dumps(r))
