# -*- coding: utf-8 -*-
"""RINGDOWN_DEPHASING_V2 — EMENDA pre-registrada da V1, escrita DEPOIS da autopsia da V1 e ANTES de olhar o dado da V2.
Autopsia da V1 (RINGDOWN_DEPHASING_V1_RESULT.json, lida por hash pelo um.py): das 23 series usadas na janela de 3 ms, 6 tinham
delta = 2,2101 identico (tau_obs na borda superior da grade refinada, 2,5 x e^0,25 = 3,21 tau_GR), todas com SNR de ringdown
entre 5,1 e 6,2, e carregavam ~52% do peso do empilhamento; delta_f co-movia negativo (-13%). O pico era o argmax da envoltoria
em +-50 ms do GPS do catalogo (GPS grosseiro): para eventos fracos o argmax cai em ruido ou antes do merger, a janela apanha
merger/ruido e o ajuste foge para a borda. As RECUSAS da V1 (18 < 20 series na janela de 6 ms; sistematica 3 vs 6 ms) ficam.
O que muda na V2 (cada item responde a um fato da autopsia):
  1. PICO por FILTRO CASADO: template IMRPhenomXAS (lalsimulation) com (m1, m2, chi_eff) do catalogo (massas no detector), branqueado
     com a PSD do evento, correlacionado com o dado em +-100 ms do GPS; t_pico = pico da envoltoria do template deslocado; exige
     SNR de ancoragem >= 8 (a inspiral inteira fixa o tempo, nao um maximo de ruido).
  2. GRADE mais larga (f_GR x [0,6; 1,4], 17; tau_GR x [0,3; 4,0] log, 21) com refino 9 x 9 dentro de +-1 passo grosso, e EXCLUSAO
     DE BORDA: ajuste grosso na borda de f ou de tau -> serie nao usada (on_edge). Nenhum delta identico por construcao.
  3. CORTE DE IDENTIFICACAO DO MODO: |delta_f| <= 0,3 (o que se mede e o 220 de Kerr previsto; fora disso nao e o modo).
  4. min_series = 8 por janela (SNR >= 8 por detector reduz a amostra; o numero e fixado aqui, antes do dado).
O resto e identico a V1: PSD Welch; janela [t_pico + 3 ms, + 6 tau_GR] e secundaria a 6 ms; seno amortecido branqueado; nulos por
injecao fora da fonte (40 janelas); empilhamento por variancia inversa; criterios (exclude_z 5, power_min 5, bias 0,2, sistematica 1 sigma).
beta = alpha*sqrt(e) em runtime. O VEREDITO e do um.py."""
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
ANCHOR_SNR_MIN = 8.0; ANCHOR_WIN_S = 0.1; DF_MAX = 0.3; TEMPLATE = 'IMRPhenomXAS'
F_SPAN, F_N = (0.6, 1.4), 17; T_SPAN, T_N = (0.3, 4.0), 21
_tpl_cache = {}
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
def fd_waveform(m1_det, m2_det, chi, n):
    df = FS / n; fmax = FS / 2
    try:
        appr = ls.GetApproximantFromString(TEMPLATE)
        hp, hc = ls.SimInspiralFD(m1_det * lal.MSUN_SI, m2_det * lal.MSUN_SI, 0.0, 0.0, chi, 0.0, 0.0, chi, 500e6 * lal.PC_SI, 0.0, 0.0, 0.0, 0.0, 0.0, df, 15.0, fmax, 20.0, lal.CreateDict(), appr)
        H = np.array(hp.data.data, dtype=complex); nf = n // 2 + 1; dfr = float(hp.deltaF)
        if abs(dfr - df) > 1e-9:
            fr_src = np.arange(len(H)) * dfr; fr_dst = np.arange(nf) * df
            amp = np.interp(fr_dst, fr_src, np.abs(H), left=0.0, right=0.0); ph = np.interp(fr_dst, fr_src, np.unwrap(np.angle(H)))
            H = amp * np.exp(1j * ph)
        if len(H) < nf: H = np.concatenate([H, np.zeros(nf - len(H), dtype=complex)])
        return H[:nf]
    except Exception:
        return None
def template_w(m1_det, m2_det, chi, f_psd, P_psd, n, psd_id):
    key = (round(m1_det, 5), round(m2_det, 5), round(chi, 4), n, psd_id)
    if key in _tpl_cache: return _tpl_cache[key]
    fr = np.fft.rfftfreq(n, 1 / FS); H = fd_waveform(m1_det, m2_det, chi, n)
    if H is None or not np.isfinite(H).all() or np.abs(H).max() == 0:
        _tpl_cache[key] = None; return None
    Pi = np.maximum(np.interp(fr, f_psd, P_psd, left=P_psd[1], right=P_psd[-1]), 1e-50)
    Hw = H * np.exp(-2j * np.pi * fr * T_PEAK) / np.sqrt(Pi * FS / 2) * band_mask(fr, F_LO, F_HI)
    h = np.fft.irfft(Hw, n); h = h / (np.sqrt(np.sum(h ** 2)) + 1e-300); ha = analytic(h); ipk = int(np.argmax(np.abs(ha)))
    if abs(ipk / FS - T_PEAK) > 0.5:
        h2 = np.fft.irfft(np.conj(H) * np.exp(-2j * np.pi * fr * T_PEAK) / np.sqrt(Pi * FS / 2) * band_mask(fr, F_LO, F_HI), n)
        h2 = h2 / (np.sqrt(np.sum(h2 ** 2)) + 1e-300); ha2 = analytic(h2); ipk2 = int(np.argmax(np.abs(ha2)))
        if abs(ipk2 / FS - T_PEAK) < abs(ipk / FS - T_PEAK): h, ha, ipk = h2, ha2, ipk2
    _tpl_cache[key] = (h, ha, ipk); return _tpl_cache[key]
def anchor(d, ha, ipk, t_guess, win_s):
    n = len(d); Fd = np.fft.fft(d); Fh = np.fft.fft(ha); corr = np.fft.ifft(Fd * np.conj(Fh)); norm = float(np.sum(np.abs(ha) ** 2))
    snr2 = np.abs(corr) ** 2 / norm; c = int(round(t_guess)); wn = int(win_s * FS); lo, hi = max(0, c - wn), min(n, c + wn)
    idx = np.arange(n); sel = (idx >= lo) & (idx < hi); s = int(idx[sel][np.argmax(snr2[sel])])
    return s, float(np.sqrt(snr2[s]))
class Fitter:
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
        for i, f in enumerate(fgrid):
            for j, tau in enumerate(tgrid):
                c, s = self.basis(f, tau); G11, G12, G22 = c @ c, c @ s, s @ s; r1, r2 = c @ yy, s @ yy; det = G11 * G22 - G12 ** 2
                if det <= 1e-30: continue
                a1 = (G22 * r1 - G12 * r2) / det; a2 = (G11 * r2 - G12 * r1) / det; ss = a1 * r1 + a2 * r2
                if best is None or ss > best[0]: best = (ss, f, tau, a1, a2, i, j)
        return best
    def fit2(self, y, f_c, tau_c):
        fg = f_c * np.linspace(F_SPAN[0], F_SPAN[1], F_N); tg = tau_c * np.exp(np.linspace(math.log(T_SPAN[0]), math.log(T_SPAN[1]), T_N))
        b = self.fit(y, fg, tg)
        if b is None: return None
        on_edge = bool(b[5] in (0, F_N - 1) or b[6] in (0, T_N - 1))
        df = f_c * (F_SPAN[1] - F_SPAN[0]) / (F_N - 1); lr = (math.log(T_SPAN[1]) - math.log(T_SPAN[0])) / (T_N - 1)
        b2 = self.fit(y, b[1] + np.linspace(-df, df, 9), b[2] * np.exp(np.linspace(-lr, lr, 9)))
        r = b2 if b2 else b
        return (r[0], r[1], r[2], r[3], r[4], on_edge)
    def model(self, f, tau, a1, a2):
        c, s = self.basis(f, tau); m = np.zeros(self.n); m[self.i0:self.i1] = a1 * c + a2 * s; return m
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--events', default=''); ap.add_argument('--out', default=os.path.join(OUT_DIR, 'RINGDOWN_DEPHASING_V2_RESULT.json')); ap.add_argument('--n_off', type=int, default=40)
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
            events.append(dict(name=r['commonName'], gps=gps, m1=m1, m2=m2, z=z, chi_eff=chi, Mf_det=Mf_det, a_f=af))
    n_seg = int(SEG_S * FS); rows = []; sources = {}; n_edge = {str(sm): 0 for sm in START_MS}; n_anchor_fail = 0
    for ev in events:
        f_gr, tau_gr, q_gr = berti(ev['Mf_det'], ev['a_f']); w_gr = 2 * math.pi * f_gr
        gm = G * ev['Mf_det'] * MSUN / C ** 3
        delta_B = -0.5 * BETA * gm * w_gr ** 2 * tau_gr; delta_A = -0.5 * BETA * T_PLANCK * w_gr ** 2 * tau_gr
        z1 = 1 + ev['z']; m1d, m2d = ev['m1'] * z1, ev['m2'] * z1; chi = min(max(ev['chi_eff'], -0.99), 0.99)
        for det in ('H1', 'L1'):
            p = os.path.join(SRC, '%s_%s_4096_32s.npz' % (ev['name'], det)); key = '%s_%s' % (ev['name'], det)
            if not os.path.exists(p): continue
            dd = np.load(p); t = dd['t']; s32 = dd['strain'].astype(float); fs = float(dd['fs'])
            if np.isnan(s32).any() or abs(fs - FS) > 1e-6: rows.append(dict(key=key, status='NAN_OR_FS')); continue
            sources[os.path.basename(p)] = sha256_file(p)
            trel = t - ev['gps']; f_psd, P_psd = welch(s32[trel < -2.0], fs); w32 = whiten32(s32, fs, f_psd, P_psd); psd_id = id(P_psd)
            def seg_at(t0_rel):
                i0 = int(round((t0_rel - T_PEAK - trel[0]) * fs)); return w32[i0:i0 + n_seg]
            d = seg_at(0.0)
            if len(d) < n_seg: rows.append(dict(key=key, status='SHORT')); continue
            sd = float(np.std(w32[(trel > -15) & (trel < -3)])); peak = float(np.max(np.abs(d[:int(1.8 * fs)])) / sd)
            tpl = template_w(m1d, m2d, chi, f_psd, P_psd, n_seg, psd_id)
            if tpl is None: rows.append(dict(key=key, status='NO_TEMPLATE')); n_anchor_fail += 1; continue
            h, ha, ipk_t = tpl; s_shift, snr_anc = anchor(d, ha, ipk_t, T_PEAK * fs - ipk_t, ANCHOR_WIN_S); ipk = ipk_t + s_shift
            rec = dict(key=key, event=ev['name'], det=det, status='OK', Mf_det=ev['Mf_det'], a_f=ev['a_f'], f_gr=f_gr, tau_gr_ms=tau_gr * 1e3, q_gr=q_gr,
                       delta_pred_A=delta_A, delta_pred_B=delta_B, peak_over_sd=peak, ipk=int(ipk), anchor_snr=snr_anc, anchor_offset_ms=(ipk - T_PEAK * fs) / fs * 1e3,
                       anchor_ok=bool(snr_anc >= ANCHOR_SNR_MIN), starts={})
            offs = np.arange(OFF_START, OFF_END, OFF_STEP)[:args.n_off]
            for sm in START_MS:
                i0 = int(ipk + int(sm / 1000 * fs)); i1 = min(n_seg, i0 + int(6 * tau_gr * fs)); i1 = max(i1, i0 + 24)
                F = Fitter(f_psd, P_psd, n_seg, i0, i1); b = F.fit2(d, f_gr, tau_gr)
                if b is None: rec['starts'][str(sm)] = dict(used=False, reason='NO_FIT'); continue
                ss, f_obs, tau_obs, a1, a2, on_edge = b; m = F.model(f_obs, tau_obs, a1, a2); snr = float(math.sqrt(max(ss, 0.0)))
                tau_rec, f_rec = [], []
                for ts in offs:
                    dk = seg_at(ts)
                    if len(dk) < n_seg: continue
                    bk = F.fit2(dk + m, f_gr, tau_gr)
                    if bk: f_rec.append(bk[1]); tau_rec.append(bk[2])
                tau_rec = np.array(tau_rec); f_rec = np.array(f_rec)
                bias_t = float(np.mean(tau_rec) / tau_obs - 1) if len(tau_rec) else float('nan'); sig_t = float(np.std(tau_rec, ddof=1) / tau_obs) if len(tau_rec) > 2 else float('nan')
                d_f = f_obs / f_gr - 1
                reasons = [r for r, bad in (('ANCHOR_SNR', snr_anc < ANCHOR_SNR_MIN), ('ON_EDGE', on_edge), ('RD_SNR', snr < SNR_MIN), ('TRANSIENT', peak > TRANSIENT_SD), ('DF', abs(d_f) > DF_MAX), ('NO_SIGMA', not (np.isfinite(sig_t) and sig_t > 0))) if bad]
                if on_edge: n_edge[str(sm)] += 1
                rec['starts'][str(sm)] = dict(f_obs=f_obs, tau_obs_ms=tau_obs * 1e3, snr=snr, delta_obs=tau_obs / tau_gr - 1, delta_f=d_f, on_edge=on_edge,
                                              bias_rel=bias_t, sigma_rel=sig_t, n_off=int(len(tau_rec)), f_rec_rel_sd=(float(np.std(f_rec, ddof=1) / f_obs) if len(f_rec) > 2 else None),
                                              used=(not reasons), reason=(','.join(reasons) if reasons else 'USED'))
            rows.append(rec)
            s3 = rec['starts'].get('3.0', {}); s6 = rec['starts'].get('6.0', {})
            print('  %-22s anc=%5.1f off=%+6.1fms f_GR=%5.0f tau_GR=%5.2fms | 3ms: f=%s tau=%s snr=%s delta=%s+-%s %s | 6ms: delta=%s %s' % (rec['key'], snr_anc, rec['anchor_offset_ms'], f_gr, tau_gr * 1e3,
                  ('%.0f' % s3['f_obs']) if s3.get('f_obs') else 'NA', ('%.2f' % s3['tau_obs_ms']) if s3.get('tau_obs_ms') else 'NA', ('%.1f' % s3['snr']) if s3.get('snr') else 'NA',
                  ('%.3f' % s3['delta_obs']) if s3.get('delta_obs') is not None else 'NA', ('%.3f' % s3['sigma_rel']) if s3.get('sigma_rel') else 'NA', s3.get('reason'), ('%.3f' % s6['delta_obs']) if s6.get('delta_obs') is not None else 'NA', s6.get('reason')), flush=True)
    stacks = {}
    for sm in START_MS:
        k = str(sm); use = [r for r in rows if r.get('status') == 'OK' and (r['starts'].get(k) or {}).get('used')]
        if not use: stacks[k] = dict(n_used=0); continue
        dlt = np.array([r['starts'][k]['delta_obs'] - r['starts'][k]['bias_rel'] for r in use]); sg = np.array([r['starts'][k]['sigma_rel'] for r in use]); wg = 1 / sg ** 2
        d_c = float(np.sum(wg * dlt) / wg.sum()); s_c = float(1 / math.sqrt(wg.sum()))
        pB = float(np.sum(wg * np.array([r['delta_pred_B'] for r in use])) / wg.sum()); pA = float(np.sum(wg * np.array([r['delta_pred_A'] for r in use])) / wg.sum())
        df = np.array([r['starts'][k]['delta_f'] for r in use]); sf = np.array([r['starts'][k]['f_rec_rel_sd'] or 1.0 for r in use]); wf = 1 / sf ** 2
        chi2 = float(np.sum(wg * (dlt - d_c) ** 2)); dof = max(len(use) - 1, 1)
        stacks[k] = dict(n_used=len(use), delta_tau=d_c, sigma=s_c, z_vs_GR=d_c / s_c, delta_pred_B=pB, delta_pred_A=pA, z_vs_B=(d_c - pB) / s_c, power_B=abs(pB) / s_c,
                         delta_f=float(np.sum(wf * df) / wf.sum()), sigma_f=float(1 / math.sqrt(wf.sum())), mean_snr=float(np.mean([r['starts'][k]['snr'] for r in use])), mean_bias_rel=float(np.mean([r['starts'][k]['bias_rel'] for r in use])),
                         mean_anchor_snr=float(np.mean([r['anchor_snr'] for r in use])), chi2_dof=chi2 / dof, n_on_edge_excluded=n_edge[k], max_weight_share=float(wg.max() / wg.sum()))
        print('STACK inicio %s ms: n=%d delta_tau=%.4f+-%.4f (z vs RG %.2f) | previsao ramo B %.4f (z vs B %.2f; poder %.2f) | ramo A %.1e | delta_f=%.4f+-%.4f | SNR medio %.1f | chi2/dof %.2f | borda excluidas %d' % (k, len(use), d_c, s_c, d_c / s_c, pB, (d_c - pB) / s_c, abs(pB) / s_c, pA, stacks[k]['delta_f'], stacks[k]['sigma_f'], stacks[k]['mean_snr'], chi2 / dof, n_edge[k]))
    syst = (abs(stacks['3.0']['delta_tau'] - stacks['6.0']['delta_tau']) if all(stacks[k].get('n_used') for k in ('3.0', '6.0')) else None)
    out = dict(version='RINGDOWN_DEPHASING_V2', amendment_of='RINGDOWN_DEPHASING_V1', executed=time.strftime('%Y-%m-%dT%H:%M:%S'), runtime_s=time.time() - t_start,
               instrument=dict(lalsuite=lal.__version__, final_state='SimIMREOBFinalMassSpin (SEOBNRv4) de (m1, m2, chi_eff) do catalogo', qnm='Berti-Cardoso-Will 2006 (l=m=2, n=0)', anchor_template=TEMPLATE, python=sys.version.split()[0], env='WSL Ubuntu /opt/lal_env'),
               beta=BETA, t_planck=T_PLANCK, prediction='tau_obs/tau_GR - 1 = -(1/2) beta tau* omega^2 tau_GR; ramo A tau*=t_Planck; ramo B tau*=G M_f/c^3',
               pipeline=dict(fs=FS, seg_s=SEG_S, band=[F_LO, F_HI], start_ms=START_MS, window='6 tau_GR', peak='filtro casado IMRPhenomXAS em +-100 ms do GPS', anchor_snr_min=ANCHOR_SNR_MIN,
                             grid='f x[0.6,1.4] (17), tau x[0.3,4.0] log (21), refino 9x9 em +-1 passo', edge_exclusion=True, df_max=DF_MAX, snr_min=SNR_MIN, transient_sd=TRANSIENT_SD, n_off=args.n_off, systematics='|delta(3ms) - delta(6ms)|'),
               catalog=dict(path=CAT, sha256=sha256_file(CAT)), sources_sha256=sources, n_events=len(events), n_no_template=n_anchor_fail, n_on_edge=n_edge, stacks=stacks, start_systematic=syst, per_series=rows)
    os.makedirs(OUT_DIR, exist_ok=True); tmp = args.out + '.tmp'
    json.dump(out, open(tmp, 'w', encoding='utf-8'), indent=1, default=lambda o: (float(o) if isinstance(o, (np.floating,)) else (o.tolist() if hasattr(o, 'tolist') else str(o))))
    os.replace(tmp, args.out); print('OK ->', args.out, '| %.0fs' % (time.time() - t_start))
if __name__ == '__main__':
    main()
