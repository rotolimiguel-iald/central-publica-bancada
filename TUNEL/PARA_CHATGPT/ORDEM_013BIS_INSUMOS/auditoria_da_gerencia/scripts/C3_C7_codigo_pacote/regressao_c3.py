"""Auditoria C3: regressao do modulo (copia) contra per_series[2] do V2 lido do caminho canonico."""
import sys, json, hashlib, math, re
sys.path.insert(0, r'C:/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/ordem013/auditoria/C3_C7_codigo_pacote/mod')
import tgl_ringdown_prediction as P
V2J = r'C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/cache/gw/RINGDOWN_DEPHASING_V2_RESULT.json'
V2P = r'C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/eco_ancorado_v1/ringdown_dephasing_v2.py'
raw = open(V2J,'rb').read(); print('V2 json sha16', hashlib.sha256(raw).hexdigest()[:16])
src = open(V2P,'rb').read(); print('V2 py sha16', hashlib.sha256(src).hexdigest()[:16])
lines = src.decode('utf-8').splitlines()
print('V2 l.22:', lines[21]); print('V2 l.23:', lines[22])
# extrair constantes da l.22-23 por regex (nao de memoria)
ns = {}
exec(chr(10).join(['import math', lines[21], lines[22]]), ns)
print('constantes lidas: ALPHA',ns['ALPHA'],'G',ns['G'],'C',ns['C'],'MSUN',ns['MSUN'],'HBAR',ns['HBAR'],'T_PLANCK',ns['T_PLANCK'])
r = json.loads(raw)['per_series'][2]
print('per_series[2]', r['key'], 'Mf_det', r['Mf_det'], 'a_f', r['a_f'])
out = {}
for L in ('A','B'):
    p = P.prediction(r['Mf_det'], r['a_f'], 'R-'+L, profile='LEGACY_V346')
    tgt = r['delta_pred_'+L]
    rel = abs(p['delta_tau_linear']-tgt)/abs(tgt)
    rel_exact = abs(p['delta_tau']-tgt)/abs(tgt)
    out[L] = dict(target=tgt, module_linear=p['delta_tau_linear'], rel_linear=rel, module_exact=p['delta_tau'], rel_exact_vs_linear_target=rel_exact)
    print(L, out[L])
# reimplementacao independente com as constantes da V2
G,Cc,MSUN,HBAR,BETA = ns['G'],ns['C'],ns['MSUN'],ns['HBAR'],ns['ALPHA']*math.sqrt(math.e)
TP = math.sqrt(HBAR*G/Cc**5)
a = min(max(r['a_f'],0.0),0.998); mw = 1.5251-1.1568*(1-a)**0.1292; q = 0.7000+1.4187*(1-a)**(-0.4990)
f0 = mw*Cc**3/(2*math.pi*G*r['Mf_det']*MSUN); tau = q/(math.pi*f0); w = 2*math.pi*f0; gm = G*r['Mf_det']*MSUN/Cc**3
dB = -0.5*BETA*gm*w**2*tau; dA = -0.5*BETA*TP*w**2*tau
print('reimpl B', dB, abs(dB-r['delta_pred_B'])/abs(r['delta_pred_B']))
print('reimpl A', dA, abs(dA-r['delta_pred_A'])/abs(r['delta_pred_A']))
# perfil CODATA
for L in ('A','B'):
    pc = P.prediction(r['Mf_det'], r['a_f'], 'R-'+L, profile='CODATA2018_IAU2015')
    pl = P.prediction(r['Mf_det'], r['a_f'], 'R-'+L, profile='LEGACY_V346')
    print('perfil CODATA vs LEGACY',L, pc['delta_tau_linear'], pl['delta_tau_linear'], (pc['delta_tau_linear']-pl['delta_tau_linear'])/pl['delta_tau_linear'])
# todas as series OK do V2 (varredura extra, nao pedida)
worst = {'A':0,'B':0}; n=0; skipped=0
for s in json.loads(raw)['per_series']:
    if s.get('status')!='OK' or 'delta_pred_B' not in s: continue
    if not (0 <= s['a_f'] < 0.998): skipped+=1; continue
    n+=1
    for L in ('A','B'):
        p = P.prediction(s['Mf_det'], s['a_f'], 'R-'+L, profile='LEGACY_V346')
        worst[L] = max(worst[L], abs(p['delta_tau_linear']-s['delta_pred_'+L])/abs(s['delta_pred_'+L]))
print('varredura todas as series OK:', n, 'pior rel', worst, 'puladas', skipped)
# beta
print('beta runtime', P.beta_tgl(), 'alpha*sqrt(e) indep', 7.2973525693e-3*math.sqrt(math.e))
