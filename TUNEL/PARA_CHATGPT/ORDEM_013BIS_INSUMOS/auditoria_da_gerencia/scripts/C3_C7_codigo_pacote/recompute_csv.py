import sys, json, csv, math
sys.path.insert(0, r'C:/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/ordem013/auditoria/C3_C7_codigo_pacote/mod')
import numpy as np
import tgl_ringdown_prediction as P
from scipy.optimize import fsolve
import importlib.util
spec = importlib.util.spec_from_file_location('lv', r'C:/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/ordem013/auditoria/C3_C7_codigo_pacote/leaver_indep.py')
B = r'C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/'
cat = json.load(open(B+'C4_CATALOG_220.json', encoding='utf-8'))
rows = list(csv.DictReader(open(B+'C7_INDEPENDENT/tables/event_reading_predictions.csv', encoding='utf-8')))
tab = {(r['event'], r['reading']): r for r in rows}
# exact QNM via bancada grid spline would be their method; use own Leaver instead (independent)
src = open(r'C:/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/ordem013/auditoria/C3_C7_codigo_pacote/leaver_indep.py', encoding='utf-8').read().split("B = r'")[0]
ns = {}; exec(src, ns); leaver = ns['qnm']
worst = {}; n = 0
for ev in cat['rows']:
    qd = ev['quantiles']; m, a, z = qd['mass_detector'][1], qd['spin'][1], qd['redshift'][1]
    for rd in ('R-A', 'R-B', 'R-RAIZ-0', 'R-LIN', 'R-MOD'):
        kw = {}
        if rd == 'R-MOD':
            w, _ = leaver(a, complex(1.5251-1.1568*(1-a)**0.1292, -0.08), 4+0j); kw['qnm_dimensionless'] = w
        p = P.prediction(m, a, rd, redshift=z, **kw)
        c = float(tab[(ev['event'], rd)]['delta_tau'])
        rel = abs(p['delta_tau']-c)/abs(c) if c != 0 else abs(p['delta_tau'])
        worst[rd] = max(worst.get(rd, 0), rel); n += 1
print('linhas recomputadas', n, 'pior erro relativo por leitura', json.dumps(worst))
