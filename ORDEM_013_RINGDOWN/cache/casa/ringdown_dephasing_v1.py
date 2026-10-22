# -*- coding: utf-8 -*-
"""RINGDOWN_DEPHASING_V1 — o amortecimento do ringdown contra a RG e contra a lei de dephasing da TGL (protocolo de outubro de 2025,
`test_gw_ringdown`/`measure_ringdown_damping`, que aguardava gwpy/lalsuite). Roda no WSL (/opt/lal_env). Fixado ANTES de olhar o dado:
  * Previsao de Kerr por evento [KNOWN]: massa e spin finais pelo ajuste EOB do lalsuite (SimIMREOBFinalMassSpin, SEOBNRv4) a partir de
    (m1, m2, chi_eff) do catalogo; f_220 e Q_220 pelos ajustes de Berti-Cardoso-Will (2006); tau_GR = Q/(pi f). Massa no detector = (1+z).
  * Previsao da TGL [REAL na forma; INPUT tau*]: Gamma = (1/2) beta tau* omega^2 somado a taxa de decaimento: tau_obs/tau_GR - 1 ~ -Gamma tau_GR.
    Ramo A: tau* = t_Planck (invisivel, ~1e-40); ramo B: tau* = G M_f/c^3 (o ramo que o §20 marcou como «provavelmente excluido» sem medir).
  * Medida: strain branqueado (PSD Welch dos 14 s pre-evento; banda [20, 1024] Hz); pico da envoltoria em +-50 ms do GPS; janela do
    ringdown [t_pico + 3 ms, t_pico + 6 tau_GR]; template = seno amortecido gerado no dominio do tempo, branqueado com a MESMA PSD e
    restrito a janela; grade (f em f_GR x [0.7, 1.3], tau em tau_GR x [0.4, 2.5] log) com ajuste linear de 2 parametros; refinamento local.
  * Nulos por injecao fora da fonte (40 janelas): o ringdown ajustado injetado em ruido -> vies e sigma de tau (e de f); recuperacao.
  * Sistematica pre-registrada: inicio da janela a 3 ms (primario) e 6 ms (secundario): a diferenca de tau entra como sistematica.
  * Empilhamento por variancia inversa de delta = tau_obs/tau_GR - 1; z contra a RG (delta = 0) e contra o ramo B (delta_pred por evento).
Serie usada se SNR do ringdown >= 5 e sem transiente. beta = alpha*sqrt(e) em runtime. O VEREDITO e do um.py."""
import os, sys, csv, json, math, time, hashlib, argparse
import numpy as np
import lal, lalsimulation as ls
ALPHA = 7.2973525693e-3; BETA = ALPHA * math.sqrt(math.e)
G = 6.674e-11; C = 2.99792458e8; MSUN = 1.98892e30; HBAR = 1.054571817e-34; T_PLANCK = math.sqrt(HBAR * G / C ** 5)
ROOT = os.environ.get('ECHO_ROOT', '/mnt/c')
IALD = os.path.join(ROOT, 'IALD/projetos_pyhton/IALD'); SRC = os.path.join(IALD, 'strain_cache'); CAT = os.path.join(IALD, 'gwtc_full_catalog.csv')
OUT_DIR = os.path.join(ROOT, 'IALD/Artigo/Haja_Luz/A Ponte e o Um/cache/gw')
FS = 4096.0; SEG_S = 2.5; T_PEAK = 2.0; F_LO, F_HI = 20.0, 1024.0
OFF_START, OFF_END, OFF_STEP = -15.5, -3.0, 0.3
SNR_MIN, TRANSIENT_SD = 5.0, 10.0; START_MS = (3.0, 6.0)
def sha256_file(p, bs=1 << 22):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(bs), b''): h.update(b)
    return h.hexdigest()
def berti(Mf_det, a):
    a = min(max(a, 0.0), 0.998); mw = 1.5251 - 1.1568 * (1 - a) ** 0.1292; q = 0.7000 + 1.4187 * (1 - a) ** (-0.4990)
    f0 = mw * C ** 3 / (2 * math.pi * G * Mf_det * MSUN); return f0, q / (math.pi * f0), q
def welch(x, fs, seg=4 * 4096):
    w = np.hanning(seg); step = seg // 2; n = (len(x) - seg) // step + 1; P = np.zeros(seg // 2 + 1)
    for i in range(n):
        xs = x[i * step:i * step + seg]; P += np.abs(np.fft.rfft((xs - xs.mean()) * w)) ** 2
    P *= 2.0 / (n * fs * np.sum(w ** 2)); return np.fft.rfftfreq(seg, 1 / fs), P
def band_mask(fr, lo, hi, ramp_lo=4.0, ramp_hi=50.0):
    m = np.ones_like(fr); m[fr < lo - ramp_lo] = 0; m[fr > hi + ramp_hi] = 0
    a = (fr >= lo - ramp_lo) & (fr < lo + ramp_lo); m[a] = 0.5 * (1 - np.cos(np.pi * (fr[a] - (lo - ramp_lo)) / (2 * ramp_lo)))
    b = (fr > hi - ramp_hi) & (fr <= hi + ramp_hi); m[b] = 0.5 * (1 + np.cos(np.pi * (fr[b] - (hi - ramp_hi)) / (2 * ramp_hi)))
    return m
def whiten32(x, fs, f, P):
    N = len(x); fr = np.fft.rfftfreq(N, 1 / fs); ft = np.fft.rfft(x)
    Pi = np.maximum(np.interp(fr, f, P, left=P[1], right=P[-1]), 1e-50)
    return np.fft.irfft(ft / np.sqrt(Pi * fs / 2) * band_mask(fr, F_LO, F_HI), n=N)
def whiten_seg(x, f, P):
    n = len(x); fr = np.fft.rfftfreq(n, 1 / FS); Pi = np.maximum(np.interp(fr, f, P, left=P[1], right=P[-1]), 1e-50)
    return np.fft.irfft(np.fft.rfft(x) / np.sqrt(Pi * FS / 2) * band_mask(fr, F_LO, F_HI), n=n)
def analytic(x):
    X = np.fft.fft(x); n = len(x); hh = np.zeros(n); hh[0] = 1; hh[1:n // 2] = 2; hh[n // 2] = 1
    return np.fft.ifft(X * hh)
class Fitter:
    """templates de seno amortecido (cos, sin) que comecam em i0, branqueados com a PSD do evento, restritos a janela [i0, i1]."""
    def __init__(self, f_psd, P_psd, n, i0, i1):
        self.f, self.P, self.n, self.i0, self.i1 = f_psd, P_psd, n, i0, i1; self.cache = {}
    def basis(self, f, tau):
        key = (round(f, 3), round(tau, 6))
        if key in self.cache: return self.cache[key]
        t = np.arange(self.n) / FS; tt = t - self.i0 / FS; env = np.where(tt >= 0, np.exp(-np.maximum(tt, 0) / tau), 0.0)
        c = whiten_seg(env * np.cos(2 * np.pi * f * tt), self.f, self.P)[self.i0:self.i1]; s = whiten_seg(env * np.sin(2 * np.pi * f * tt), self.f, self.P)[self.i0:self.i1]
        self.cache[key] = (c, s); return self.cache[key]
    def fit(self, y, fgrid, tgrid):
        yy = y[self.i0:self.i1]; best = None
        for f in fgrid:
            for tau in tgrid:
                c, s = self.basis(f, tau); G11, G12, G22 = c @ c, c @ s, s @ s; r1, r2 = c @ yy, s @ yy; det = G11 * G22 - G12 ** 2
                if det <= 1e-30: continue
                a1 = (G22 * r1 - G12 * r2) / det; a2 = (G11 * r2 - G12 * r1) / det; ss = a1 * r1 + a2 * r2
                if best is None or ss > best[0]: best = (ss, f, tau, a1, a2)
        return best
    def fit2(self, y, f_c, tau_c):
        b = self.fit(y, f_c * np.linspace(0.7, 1.3, 13), tau_c * np.exp(np.linspace(math.log(0.4), math.log(2.5), 15)))
        if b is None: return None
        f1, t1 = b[1], b[2]; b2 = self.fit(y, f1 * np.linspace(0.93, 1.07, 9), t1 * np.exp(np.linspace(-0.25, 0.25, 9)))
        return b2 if b2 else b
    def model(self, f, tau, a1, a2):
        c, s = self.basis(f, tau); m = np.zeros(self.n); m[self.i0:self.i1] = a1 * c + a2 * s; return m
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--events', default=''); ap.add_argument('--out', default=os.path.join(OUT_DIR, 'RINGDOWN_DEPHASING_V1_RESULT.json')); ap.add_argument('--n_off', type=int, default=40)
    args = ap.parse_args(); only = set(x for x in args.events.split(',') if x); t_start = time.time()
    events = []
    with open(CAT, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            try:
                z = float(r['redshift']); gps = float(r['GPS']); m1 = float(r['mass_1_source']); m2 = float(r['mass_2_source'])
            except Exception: continue
            if only and r['commonName'] not in only: continue
            chi = float(r['chi_eff']) if r.get('chi_eff') not in (None, '') else 0.0
            st, mfrac, af = ls.SimIMREOBFinalMassSpin(m1, m2, [0.0, 0.0, chi], [0.0, 0.0, chi], ls.SEOBNRv4)
            Mf_det = mfrac * (m1 + m2) * (1 + z)
            events.append(dict(name=r['commonName'], gps=gps, m1=m1, m2=m2, z=z, chi_eff=chi, Mf_det=Mf_det, a_f=af, Mf_cat=(float(r['final_mass_source']) * (1 + z) if r.get('final_mass_source') else None)))
    n_seg = int(SEG_S * FS); rows = []; sources = {}
    for ev in events:
        f_gr, tau_gr, q_gr = berti(ev['Mf_det'], ev['a_f']); w_gr = 2 * math.pi * f_gr
        gm = G * ev['Mf_det'] * MSUN / C ** 3
        delta_B = -0.5 * BETA * gm * w_gr ** 2 * tau_gr; delta_A = -0.5 * BETA * T_PLANCK * w_gr ** 2 * tau_gr
        for det in ('H1', 'L1'):
            p = os.path.join(SRC, '%s_%s_4096_32s.npz' % (ev['name'], det))
            if not os.path.exists(p): continue
            dd = np.load(p); t = dd['t']; s32 = dd['strain'].astype(float); fs = float(dd['fs'])
            if np.isnan(s32).any() or abs(fs - FS) > 1e-6: rows.append(dict(key='%s_%s' % (ev['name'], det), status='NAN_OR_FS')); continue
            sources[os.path.basename(p)] = sha256_file(p)
            trel = t - ev['gps']; f_psd, P_psd = welch(s32[trel < -2.0], fs); w32 = whiten32(s32, fs, f_psd, P_psd)
            def seg_at(t0_rel):
                i0 = int(round((t0_rel - T_PEAK - trel[0]) * fs)); return w32[i0:i0 + n_seg]
            d = seg_at(0.0)
            if len(d) < n_seg: rows.append(dict(key='%s_%s' % (ev['name'], det), status='SHORT')); continue
            sd = float(np.std(w32[(trel > -15) & (trel < -3)])); peak = float(np.max(np.abs(d[:int(1.8 * fs)])) / sd)
            env = np.abs(analytic(d)); c0 = int(T_PEAK * fs); wn = int(0.05 * fs); ipk = c0 - wn + int(np.argmax(env[c0 - wn:c0 + wn]))
            rec = dict(key='%s_%s' % (ev['name'], det), event=ev['name'], det=det, status='OK', Mf_det=ev['Mf_det'], a_f=ev['a_f'], f_gr=f_gr, tau_gr_ms=tau_gr * 1e3, q_gr=q_gr,
                       delta_pred_A=delta_A, delta_pred_B=delta_B, peak_over_sd=peak, ipk=ipk, starts={})
            offs = np.arange(OFF_START, OFF_END, OFF_STEP)[:args.n_off]
            for sm in START_MS:
                i0 = ipk + int(sm / 1000 * fs); i1 = min(n_seg, i0 + int(6 * tau_gr * fs)); i1 = max(i1, i0 + 24)
                F = Fitter(f_psd, P_psd, n_seg, i0, i1); b = F.fit2(d, f_gr, tau_gr)
                if b is None: rec['starts'][str(sm)] = dict(used=False); continue
                ss, f_obs, tau_obs, a1, a2 = b; m = F.model(f_obs, tau_obs, a1, a2); snr = float(math.sqrt(max(ss, 0.0)))
                tau_rec, f_rec = [], []
                for ts in offs:
                    dk = seg_at(ts)
                    if len(dk) < n_seg: continue
                    bk = F.fit2(dk + m, f_gr, tau_gr)
                    if bk: f_rec.append(bk[1]); tau_rec.append(bk[2])
                tau_rec = np.array(tau_rec); f_rec = np.array(f_rec)
                bias_t = float(np.mean(tau_rec) / tau_obs - 1) if len(tau_rec) else float('nan'); sig_t = float(np.std(tau_rec, ddof=1) / tau_obs) if len(tau_rec) > 2 else float('nan')
                rec['starts'][str(sm)] = dict(f_obs=f_obs, tau_obs_ms=tau_obs * 1e3, snr=snr, delta_obs=tau_obs / tau_gr - 1, delta_f=f_obs / f_gr - 1,
                                              bias_rel=bias_t, sigma_rel=sig_t, n_off=int(len(tau_rec)), f_rec_rel_sd=(float(np.std(f_rec, ddof=1) / f_obs) if len(f_rec) > 2 else None),
                                              used=bool(snr >= SNR_MIN and peak <= TRANSIENT_SD and np.isfinite(sig_t) and sig_t > 0))
            rows.append(rec)
            s3 = rec['starts'].get('3.0', {}); s6 = rec['starts'].get('6.0', {})
            print('  %-22s f_GR=%5.0f tau_GR=%5.2fms a_f=%.3f | 3ms: f=%s tau=%s snr=%s delta=%s+-%s used=%s | 6ms: delta=%s' % (rec['key'], f_gr, tau_gr * 1e3, ev['a_f'],
                  ('%.0f' % s3['f_obs']) if s3.get('f_obs') else 'NA', ('%.2f' % s3['tau_obs_ms']) if s3.get('tau_obs_ms') else 'NA', ('%.1f' % s3['snr']) if s3.get('snr') else 'NA',
                  ('%.3f' % s3['delta_obs']) if s3.get('delta_obs') is not None else 'NA', ('%.3f' % s3['sigma_rel']) if s3.get('sigma_rel') else 'NA', s3.get('used'), ('%.3f' % s6['delta_obs']) if s6.get('delta_obs') is not None else 'NA'), flush=True)
    stacks = {}
    for sm in START_MS:
        k = str(sm); use = [r for r in rows if r.get('status') == 'OK' and (r['starts'].get(k) or {}).get('used')]
        if not use: stacks[k] = dict(n_used=0); continue
        dlt = np.array([r['starts'][k]['delta_obs'] - r['starts'][k]['bias_rel'] for r in use]); sg = np.array([r['starts'][k]['sigma_rel'] for r in use]); wg = 1 / sg ** 2
        d_c = float(np.sum(wg * dlt) / wg.sum()); s_c = float(1 / math.sqrt(wg.sum()))
        pB = float(np.sum(wg * np.array([r['delta_pred_B'] for r in use])) / wg.sum()); pA = float(np.sum(wg * np.array([r['delta_pred_A'] for r in use])) / wg.sum())
        df = np.array([r['starts'][k]['delta_f'] for r in use]); sf = np.array([r['starts'][k]['f_rec_rel_sd'] or 1.0 for r in use]); wf = 1 / sf ** 2
        stacks[k] = dict(n_used=len(use), delta_tau=d_c, sigma=s_c, z_vs_GR=d_c / s_c, delta_pred_B=pB, delta_pred_A=pA, z_vs_B=(d_c - pB) / s_c, power_B=abs(pB) / s_c,
                         delta_f=float(np.sum(wf * df) / wf.sum()), sigma_f=float(1 / math.sqrt(wf.sum())), mean_snr=float(np.mean([r['starts'][k]['snr'] for r in use])), mean_bias_rel=float(np.mean([r['starts'][k]['bias_rel'] for r in use])))
        print('STACK inicio %s ms: n=%d delta_tau=%.4f+-%.4f (z vs RG %.2f) | previsao ramo B %.4f (z vs B %.2f; poder %.2f) | ramo A %.1e | delta_f=%.4f+-%.4f | SNR medio %.1f' % (k, len(use), d_c, s_c, d_c / s_c, pB, (d_c - pB) / s_c, abs(pB) / s_c, pA, stacks[k]['delta_f'], stacks[k]['sigma_f'], stacks[k]['mean_snr']))
    syst = (abs(stacks['3.0']['delta_tau'] - stacks['6.0']['delta_tau']) if all(stacks[k].get('n_used') for k in ('3.0', '6.0')) else None)
    out = dict(version='RINGDOWN_DEPHASING_V1', executed=time.strftime('%Y-%m-%dT%H:%M:%S'), runtime_s=time.time() - t_start,
               instrument=dict(lalsuite=lal.__version__, final_state='SimIMREOBFinalMassSpin (SEOBNRv4) de (m1, m2, chi_eff) do catalogo', qnm='Berti-Cardoso-Will 2006 (l=m=2, n=0)', python=sys.version.split()[0], env='WSL Ubuntu /opt/lal_env'),
               beta=BETA, t_planck=T_PLANCK, prediction='tau_obs/tau_GR - 1 = -(1/2) beta tau* omega^2 tau_GR; ramo A tau*=t_Planck; ramo B tau*=G M_f/c^3',
               pipeline=dict(fs=FS, seg_s=SEG_S, band=[F_LO, F_HI], start_ms=START_MS, window='6 tau_GR', grid='f x[0.7,1.3] (13), tau x[0.4,2.5] log (15), refino 9x9', snr_min=SNR_MIN, transient_sd=TRANSIENT_SD, n_off=args.n_off, systematics='|delta(3ms) - delta(6ms)|'),
               catalog=dict(path=CAT, sha256=sha256_file(CAT)), sources_sha256=sources, n_events=len(events), stacks=stacks, start_systematic=syst, per_series=rows)
    os.makedirs(OUT_DIR, exist_ok=True); tmp = args.out + '.tmp'
    json.dump(out, open(tmp, 'w', encoding='utf-8'), indent=1, default=lambda o: (float(o) if isinstance(o, (np.floating,)) else (o.tolist() if hasattr(o, 'tolist') else str(o))))
    os.replace(tmp, args.out); print('OK ->', args.out, '| %.0fs' % (time.time() - t_start))
if __name__ == '__main__':
    main()
