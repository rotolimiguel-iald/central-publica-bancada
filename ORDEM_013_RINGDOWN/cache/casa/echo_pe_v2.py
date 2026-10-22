# -*- coding: utf-8 -*-
"""ECHO_PE_V2 — EMENDA pre-registrada da V1 (autopsia da V1 lida do proprio resultado, hash da emenda ANTES do dado da V2).
O que a V1 mostrou: injecoes ausentes (janela fora da fonte em t0 = -12 s cai fora do cache de 32 s); medianas do posterior coladas na
borda do prior de tempo (±100 ms; o GPS do catalogo e grosseiro) e de massa (m2 -> 1 Msun, m1 -> 458 Msun) em 8 de 21 eventos (MAY);
um unico evento (GW190521, 3 ciclos, m2 na borda) com 42% do peso e jackknife de 4,5 sigma. O que muda na V2: (1) prior de tempo
centrado na ancoragem por filtro casado (PhenomD nos parametros do catalogo) com meia-largura 20 ms; (2) priors de massa alargados 1,5x
com piso de 3 Msun; (3) EXCLUSAO de eventos com mediana a < 5% da borda do prior em qualquer parametro (PRIOR_EDGE); (4) janela de
injecao em t0 = -9,5 s; (5) criterios de robustez: jackknife (grade) <= 2 sigma e peso maximo de um evento <= 0,5. O resto e a V1:
ECHO_PE_V1 — a forma bayesiana do protocolo ancorado (ECHO_ANCHORED, hash 1e94f77689b5017e): o eco como termo do modelo, com os
parametros do primario MARGINALIZADOS por amostragem (bilby + dynesty), de modo que o descasamento de template — que deu
INCONCLUSIVE_SYSTEMATICS nas V1/V2 (v344/v345) — entre no posterior em vez de entrar como sistematica. Roda no WSL (/opt/lal_env).
Fixado ANTES de olhar o dado:
  * Modelo por detector d: s_d(t) = Re[z_d · (p(t - dt_d) + a·S·sqrt(beta)·e(t - dt_d))], onde p = template IMRPhenomD [KNOWN] de (m1, m2, chi_eff),
    branqueado com a PSD do evento; e = copia de p a partir do seu pico, atrasada de tau (lei MAY: 2GM_f/c^3·ln(1/beta); lei KMS: 2pi/kappa
    de Kerr com o (M_f, a_f) AMOSTRADO pelo ajuste EOB do lalsuite); S = -1 e sqrt(beta) sao do kernel (v341); a = 1 e a previsao da TGL.
  * Parametros amostrados: m1, m2 (detector), chi_eff, dt_d por detector, a. A amplitude complexa z_d (distancia, inclinacao, polarizacao,
    ceu, fase) e MARGINALIZADA ANALITICAMENTE (prior plano): ln L = 1/2 r^T G^-1 r - 1/2 ln det G.
  * Priors: m1, m2 uniformes no intervalo de 90% do catalogo alargado 2x; chi_eff idem (±0,2 se ausente); dt_d uniforme em ±100 ms do GPS;
    a uniforme em [-3, 3]. Amostrador: dynesty (nlive 300, rwalk, dlogz 0,3) via bilby.
  * Eventos: Mc_det >= 10 (sem enrolamento no segmento de 6 s); detector entra se o SNR de ancoragem (filtro casado PhenomD nos parametros do
    catalogo) >= 6; evento entra se algum detector >= 8.
  * Por evento e lei: posterior de a (media, sigma, quantis), ln Z, ln B (Savage-Dickey em a = 0). Combinacao: soma dos log-posteriores de a
    numa grade comum (prior plano comum) -> a_comb ± sigma_comb; z contra 0 e contra 1; poder = 1/sigma_comb.
  * NULOS por injecao (eventos com SNR de ancoragem >= 10, ate 10): em ruido fora da fonte (t0 = -12 s), (i) a = 0 primario-so, (ii) a = 1 com
    PhenomD, (iii) a = 1 com SEOBNRv4 (nulo de familia); recuperacao pela MESMA PE.
beta = alpha*sqrt(e) em runtime. O VEREDITO e do um.py."""
import os, sys, csv, json, math, time, hashlib, argparse, warnings
import numpy as np
import lal, lalsimulation as ls
warnings.filterwarnings('ignore')
ALPHA = 7.2973525693e-3; BETA = ALPHA * math.sqrt(math.e); A_PRED = math.sqrt(BETA); SIGN = -1.0
G = 6.674e-11; C = 2.99792458e8; MSUN = 1.98892e30
ROOT = os.environ.get('ECHO_ROOT', '/mnt/c')
IALD = os.path.join(ROOT, 'IALD/projetos_pyhton/IALD'); SRC = os.path.join(IALD, 'strain_cache'); CAT = os.path.join(IALD, 'gwtc_full_catalog.csv')
OUT_DIR = os.path.join(ROOT, 'IALD/Artigo/Haja_Luz/A Ponte e o Um/cache/gw')
FS = 4096.0; SEG_S = 6.0; T_PEAK = 5.0; F_LO, F_HI = 20.0, 1024.0; F_MIN_TPL = 20.0
MC_MIN = 10.0; ANCHOR_DET_MIN, ANCHOR_EV_MIN, INJ_SNR_MIN, INJ_MAX = 6.0, 8.0, 10.0, 10
DT_MAX = 0.1; A_LO, A_HI = -3.0, 3.0; PRIOR_WIDEN = 1.5; CHI_DEFAULT = 0.2; M_FLOOR = 3.0; DT_HALF = 0.02; EDGE_FRAC = 0.05
NLIVE, WALKS, DLOGZ = 300, 30, 0.3
FAMILIES = {'A': 'IMRPhenomD', 'B': 'SEOBNRv4'}; INJ_T0 = -9.5
def sha256_file(p, bs=1 << 22):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(bs), b''): h.update(b)
    return h.hexdigest()
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
def analytic(x):
    X = np.fft.fft(x); n = len(x); hh = np.zeros(n); hh[0] = 1; hh[1:n // 2] = 2; hh[n // 2] = 1
    return np.fft.ifft(X * hh)
def fd_waveform(fam, m1_det, m2_det, chi, n):
    df = FS / n; fmax = FS / 2
    try:
        appr = ls.GetApproximantFromString(FAMILIES[fam])
        hp, hc = ls.SimInspiralFD(m1_det * lal.MSUN_SI, m2_det * lal.MSUN_SI, 0.0, 0.0, chi, 0.0, 0.0, chi, 500e6 * lal.PC_SI, 0.0, 0.0, 0.0, 0.0, 0.0, df, F_MIN_TPL, fmax, F_MIN_TPL, lal.CreateDict(), appr)
        H = np.array(hp.data.data, dtype=complex); nf = n // 2 + 1; dfr = float(hp.deltaF)
        if abs(dfr - df) > 1e-9:
            fr_src = np.arange(len(H)) * dfr; fr_dst = np.arange(nf) * df
            amp = np.interp(fr_dst, fr_src, np.abs(H), left=0.0, right=0.0); ph = np.interp(fr_dst, fr_src, np.unwrap(np.angle(H)))
            H = amp * np.exp(1j * ph)
        if len(H) < nf: H = np.concatenate([H, np.zeros(nf - len(H), dtype=complex)])
        H = H[:nf]
        if not np.isfinite(H).all() or np.abs(H).max() == 0: return None
        return H
    except Exception:
        return None
class Det:
    """um detector: dado branqueado (segmento), PSD interpolada no grid do segmento, fator de branqueamento em FD."""
    def __init__(self, name, d, f_psd, P_psd, n):
        self.name = name; self.d = d; fr = np.fft.rfftfreq(n, 1 / FS)
        Pi = np.maximum(np.interp(fr, f_psd, P_psd, left=P_psd[1], right=P_psd[-1]), 1e-50)
        self.W = band_mask(fr, F_LO, F_HI) / np.sqrt(Pi * FS / 2); self.fr = fr; self.n = n
        self.conj = None
    def tpl(self, H, dt):
        """template branqueado no tempo com o pico em T_PEAK + dt; devolve (h, ha, ipk)."""
        Hs = H * self.W * np.exp(-2j * np.pi * self.fr * (T_PEAK + dt))
        if self.conj is None:
            h = np.fft.irfft(Hs, self.n); ha = analytic(h); ipk = int(np.argmax(np.abs(ha)))
            h2 = np.fft.irfft(np.conj(H) * self.W * np.exp(-2j * np.pi * self.fr * (T_PEAK + dt)), self.n); ha2 = analytic(h2); ipk2 = int(np.argmax(np.abs(ha2)))
            self.conj = abs(ipk2 / FS - T_PEAK - dt) < abs(ipk / FS - T_PEAK - dt)
            if self.conj: h, ha, ipk = h2, ha2, ipk2
        else:
            if self.conj: Hs = np.conj(H) * self.W * np.exp(-2j * np.pi * self.fr * (T_PEAK + dt))
            h = np.fft.irfft(Hs, self.n); ha = analytic(h); ipk = int(np.argmax(np.abs(ha)))
        nrm = math.sqrt(float(np.sum(h ** 2))) + 1e-300
        return h / nrm, ha / nrm, ipk
def basis(ha, ipk, lag):
    n = len(ha); hr = np.real(ha); hi = -np.imag(ha)
    br = np.zeros(n); bi = np.zeros(n); br[ipk:] = hr[ipk:]; bi[ipk:] = hi[ipk:]
    if lag > 0:
        br = np.roll(br, lag); bi = np.roll(bi, lag); br[:lag] = 0; bi[:lag] = 0
    return hr, hi, br, bi
def marg_lnL(d, ur, ui):
    G11 = float(ur @ ur); G12 = float(ur @ ui); G22 = float(ui @ ui); r1 = float(ur @ d); r2 = float(ui @ d); det = G11 * G22 - G12 ** 2
    if not np.isfinite(det) or det <= 1e-12 * (G11 * G22 + 1e-300): return -np.inf, (0.0, 0.0)
    c1 = (G22 * r1 - G12 * r2) / det; c2 = (G11 * r2 - G12 * r1) / det
    return 0.5 * (c1 * r1 + c2 * r2) - 0.5 * math.log(det), (c1, c2)
def final_state(m1, m2, chi):
    st, mfrac, af = ls.SimIMREOBFinalMassSpin(m1, m2, [0.0, 0.0, chi], [0.0, 0.0, chi], ls.SEOBNRv4); return mfrac, min(max(af, 0.0), 0.998)
def delay_s(law, Mf_det, af):
    gm = G * Mf_det * MSUN / C ** 3
    if law == 'MAY': return 2.0 * gm * math.log(1.0 / BETA)
    sq = math.sqrt(1 - af ** 2); return 4 * math.pi * (1 + sq) / sq * gm
def model_parts(dets, H, params, law, a):
    """devolve por detector (ur, ui) do modelo u = p + a S sqrt(beta) e, e o atraso usado."""
    m1, m2, chi = params['m1'], params['m2'], params['chi']
    mfrac, af = final_state(m1, m2, chi); Mf = mfrac * (m1 + m2); tau = delay_s(law, Mf, af); lag = int(round(tau * FS))
    out = []
    for D in dets:
        h, ha, ipk = D.tpl(H, params['dt_' + D.name]); hr, hi, br, bi = basis(ha, ipk, lag)
        out.append((hr + a * SIGN * A_PRED * br, hi + a * SIGN * A_PRED * bi, (hr, hi, br, bi)))
    return out, tau
import bilby
bilby.core.utils.logger.setLevel('ERROR')
class EchoLikelihood(bilby.Likelihood):
    def __init__(self, dets, law, fam='A'):
        self.dets = dets; self.law = law; self.fam = fam; self.n = dets[0].n
        super().__init__(parameters={k: None for k in ['m1', 'm2', 'chi', 'a'] + ['dt_' + D.name for D in dets]})
    def log_likelihood(self):
        p = dict(self.parameters); m1, m2 = (p['m1'], p['m2']) if p['m1'] >= p['m2'] else (p['m2'], p['m1']); p['m1'], p['m2'] = m1, m2
        H = fd_waveform(self.fam, m1, m2, p['chi'], self.n)
        if H is None: return -np.inf
        parts, tau = model_parts(self.dets, H, p, self.law, p['a']); tot = 0.0
        for D, (ur, ui, _) in zip(self.dets, parts):
            l, _ = marg_lnL(D.d, ur, ui)
            if not np.isfinite(l): return -np.inf
            tot += l
        return tot
def anchor_snr(D, H):
    h, ha, ipk = D.tpl(H, 0.0); Fd = np.fft.fft(D.d); Fh = np.fft.fft(ha); corr = np.fft.ifft(Fd * np.conj(Fh)); norm = float(np.sum(np.abs(ha) ** 2))
    snr2 = np.abs(corr) ** 2 / norm; c = int(T_PEAK * FS) - ipk; wn = int(DT_MAX * FS); idx = np.arange(D.n); sel = (idx >= c - wn) & (idx < c + wn)
    s = int(idx[sel][np.argmax(snr2[sel])]); return float(math.sqrt(snr2[s])), (ipk + s - T_PEAK * FS) / FS
def make_priors(ev, dets):
    pr = bilby.core.prior.PriorDict()
    z1 = 1 + ev['z']
    pr['m1'] = bilby.core.prior.Uniform(max(M_FLOOR, (ev['m1'] - PRIOR_WIDEN * ev['m1_lo']) * z1), (ev['m1'] + PRIOR_WIDEN * ev['m1_hi']) * z1, name='m1')
    pr['m2'] = bilby.core.prior.Uniform(max(M_FLOOR, (ev['m2'] - PRIOR_WIDEN * ev['m2_lo']) * z1), (ev['m2'] + PRIOR_WIDEN * ev['m2_hi']) * z1, name='m2')
    pr['chi'] = bilby.core.prior.Uniform(max(-0.99, ev['chi'] - PRIOR_WIDEN * ev['chi_lo']), min(0.99, ev['chi'] + PRIOR_WIDEN * ev['chi_hi']), name='chi')
    pr['a'] = bilby.core.prior.Uniform(A_LO, A_HI, name='a')
    for D in dets:
        tc = float((ev.get('t_anc') or {}).get(D.name, 0.0)); pr['dt_' + D.name] = bilby.core.prior.Uniform(tc - DT_HALF, tc + DT_HALF, name='dt_' + D.name)
    return pr
def run_pe(dets, ev, law, label, outdir, nlive, fam='A'):
    lk = EchoLikelihood(dets, law, fam); pr = make_priors(ev, dets)
    res = bilby.run_sampler(likelihood=lk, priors=pr, sampler='dynesty', nlive=nlive, sample='rwalk', walks=WALKS, dlogz=DLOGZ, outdir=outdir, label=label,
                            save=False, plot=False, print_progress=False, resume=False, check_point=False, npool=1, verbose=False, print_method='none')
    post = res.posterior; a = np.asarray(post['a'].values, dtype=float)
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(a); p0 = float(kde(0.0)[0]); prior0 = 1.0 / (A_HI - A_LO)
    lnB = math.log(max(p0, 1e-300)) - math.log(prior0)   # ln B_{sem eco / com eco} (Savage-Dickey em a = 0); negativo favorece eco
    grid = np.linspace(A_LO, A_HI, 601); lp = np.log(np.maximum(kde(grid), 1e-300))
    med = {k: float(np.median(post[k].values)) for k in pr.keys()}
    edge = []
    for k in pr.keys():
        if k == 'a': continue
        lo, hi = float(pr[k].minimum), float(pr[k].maximum); x = (med[k] - lo) / max(hi - lo, 1e-300)
        if x < EDGE_FRAC or x > 1 - EDGE_FRAC: edge.append(k)
    return dict(a_mean=float(a.mean()), a_std=float(a.std(ddof=1)), a_q05=float(np.quantile(a, 0.05)), a_q50=float(np.median(a)), a_q95=float(np.quantile(a, 0.95)),
                lnZ=float(res.log_evidence), lnZ_err=float(res.log_evidence_err), lnB_noecho_over_echo=lnB, max_lnL=float(np.max(post['log_likelihood'].values)),
                n_samples=int(len(a)), medians=med, prior_edge=edge, log_post_grid=lp.tolist()), med
def inject_model(dets, ev, med, law, a_inj, fam):
    """constroi, nos parametros medianos on-source, o sinal (primario [+ eco a_inj]) com a amplitude/tempo ajustados on-source, por detector."""
    n = dets[0].n; H = fd_waveform(fam, med['m1'], med['m2'], med['chi'], n)
    if H is None: return None
    out = []
    parts, tau = model_parts(dets, H, med, law, 1.0)
    for D, (ur, ui, (hr, hi, br, bi)) in zip(dets, parts):
        # coeficientes do primario ajustados ao dado on-source com o eco no valor mediano de a
        ur_m = hr + med['a'] * SIGN * A_PRED * br; ui_m = hi + med['a'] * SIGN * A_PRED * bi
        _, (c1, c2) = marg_lnL(D.d, ur_m, ui_m)
        out.append(c1 * (hr + a_inj * SIGN * A_PRED * br) + c2 * (hi + a_inj * SIGN * A_PRED * bi))
    return out
def job(args):
    (key, ev, det_payload, law, kind, nlive, outdir) = args
    dets = [Det(name, d, f, P, len(d)) for (name, d, f, P) in det_payload]
    t0 = time.time()
    try:
        r, med = run_pe(dets, ev, law, '%s_%s_%s' % (ev['name'], law, kind), outdir, nlive)
        r['runtime_s'] = time.time() - t0; r['status'] = 'OK'
    except Exception as e:
        r = dict(status='ERROR', error=repr(e)[:300], runtime_s=time.time() - t0); med = None
    return key, law, kind, r, med
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--events', default=''); ap.add_argument('--laws', default='MAY,KMS'); ap.add_argument('--nlive', type=int, default=NLIVE)
    ap.add_argument('--out', default=os.path.join(OUT_DIR, 'ECHO_PE_V2_RESULT.json')); ap.add_argument('--pool', type=int, default=40); ap.add_argument('--no_inj', action='store_true'); ap.add_argument('--max_events', type=int, default=0)
    args = ap.parse_args(); only = set(x for x in args.events.split(',') if x); laws = [l for l in args.laws.split(',') if l]; t_start = time.time()
    outdir = '/tmp/echo_pe_out'; os.makedirs(outdir, exist_ok=True)
    events = []
    with open(CAT, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            try:
                z = float(r['redshift']); gps = float(r['GPS']); m1 = float(r['mass_1_source']); m2 = float(r['mass_2_source'])
            except Exception: continue
            if only and r['commonName'] not in only: continue
            mc_det = (m1 * m2) ** 0.6 / (m1 + m2) ** 0.2 * (1 + z)
            if mc_det < MC_MIN: continue
            def _e(k, default):
                try: return abs(float(r[k]))
                except Exception: return default
            chi = float(r['chi_eff']) if r.get('chi_eff') not in (None, '') else 0.0
            events.append(dict(name=r['commonName'], gps=gps, m1=m1, m2=m2, z=z, chi=chi, m1_lo=_e('mass_1_source_lower', 0.1 * m1), m1_hi=_e('mass_1_source_upper', 0.1 * m1),
                               m2_lo=_e('mass_2_source_lower', 0.1 * m2), m2_hi=_e('mass_2_source_upper', 0.1 * m2), chi_lo=_e('chi_eff_lower', CHI_DEFAULT) or CHI_DEFAULT, chi_hi=_e('chi_eff_upper', CHI_DEFAULT) or CHI_DEFAULT,
                               mc_det=mc_det, snr_net=(float(r['network_matched_filter_snr']) if r['network_matched_filter_snr'] else None)))
    n_seg = int(SEG_S * FS); sources = {}; prepared = []; skipped = []
    for ev in events:
        z1 = 1 + ev['z']; H0 = fd_waveform('A', ev['m1'] * z1, ev['m2'] * z1, min(max(ev['chi'], -0.99), 0.99), n_seg)
        if H0 is None: skipped.append((ev['name'], 'NO_TEMPLATE')); continue
        dets = []; anc = {}; off = {}
        for det in ('H1', 'L1'):
            p = os.path.join(SRC, '%s_%s_4096_32s.npz' % (ev['name'], det))
            if not os.path.exists(p): continue
            dd = np.load(p); t = dd['t']; s32 = dd['strain'].astype(float); fs = float(dd['fs'])
            if np.isnan(s32).any() or abs(fs - FS) > 1e-6: continue
            sources[os.path.basename(p)] = sha256_file(p)
            trel = t - ev['gps']; f_psd, P_psd = welch(s32[trel < -2.0], fs); w32 = whiten32(s32, fs, f_psd, P_psd)
            i0 = int(round((0.0 - T_PEAK - trel[0]) * fs)); d = w32[i0:i0 + n_seg]
            if len(d) < n_seg: continue
            j0 = int(round((INJ_T0 - T_PEAK - trel[0]) * fs)); d_off = w32[j0:j0 + n_seg]
            D = Det(det, d, f_psd, P_psd, n_seg); s_anc, t_anc = anchor_snr(D, H0)
            if s_anc >= ANCHOR_DET_MIN: dets.append((det, d, f_psd, P_psd)); anc[det] = s_anc; off[det] = (d_off if len(d_off) == n_seg else None); ev.setdefault('t_anc', {})[det] = float(t_anc)
        if not dets or max(anc.values()) < ANCHOR_EV_MIN: skipped.append((ev['name'], 'ANCHOR_SNR_%s' % {k: round(v, 1) for k, v in anc.items()})); continue
        prepared.append((ev, dets, anc, off))
    if args.max_events: prepared = prepared[:args.max_events]
    print('eventos preparados: %d | pulados: %d' % (len(prepared), len(skipped)), flush=True)
    for ev, dets, anc, off in prepared: print('  %-22s Mc_det=%5.1f dets=%s anc=%s t_anc_ms=%s' % (ev['name'], ev['mc_det'], [d[0] for d in dets], {k: round(v, 1) for k, v in anc.items()}, {k: round(v * 1e3, 1) for k, v in (ev.get('t_anc') or {}).items()}), flush=True)
    import multiprocessing as mp
    jobs = [(ev['name'], ev, dets, law, 'on', args.nlive, outdir) for ev, dets, anc, off in prepared for law in laws]
    results = {ev['name']: dict(mc_det=ev['mc_det'], snr_net=ev['snr_net'], anchor_snr=anc, t_anc=ev.get('t_anc'), dets=[d[0] for d in dets], laws={}) for ev, dets, anc, off in prepared}
    ctx = mp.get_context('fork')
    with ctx.Pool(min(args.pool, max(1, len(jobs)))) as pool:
        for key, law, kind, r, med in pool.imap_unordered(job, jobs):
            results[key]['laws'].setdefault(law, {})['on'] = r; results[key]['laws'][law]['_med'] = med
            print('  ON  %-22s %s a=%s+-%s lnB=%s %.0fs %s edge=%s' % (key, law, ('%.3f' % r['a_mean']) if r.get('a_mean') is not None else 'NA', ('%.3f' % r['a_std']) if r.get('a_std') is not None else 'NA', ('%.2f' % r['lnB_noecho_over_echo']) if r.get('lnB_noecho_over_echo') is not None else 'NA', r.get('runtime_s', 0), r['status'], r.get('prior_edge')), flush=True)
    inj_jobs = []
    if not args.no_inj:
        cand = [(ev, dets, anc, off) for ev, dets, anc, off in prepared if max(anc.values()) >= INJ_SNR_MIN and all(off.get(d[0]) is not None for d in dets)]
        cand = sorted(cand, key=lambda x: -max(x[2].values()))[:INJ_MAX]
        for ev, dets, anc, off in cand:
            for law in laws:
                med = results[ev['name']]['laws'].get(law, {}).get('_med')
                if not med or (results[ev['name']]['laws'][law].get('on') or {}).get('prior_edge'): continue
                D0 = [Det(name, d, f, P, n_seg) for (name, d, f, P) in dets]
                for kind, a_inj, fam in (('inj_a0', 0.0, 'A'), ('inj_a1_A', 1.0, 'A'), ('inj_a1_B', 1.0, 'B')):
                    sig = inject_model(D0, ev, med, law, a_inj, fam)
                    if sig is None: results[ev['name']]['laws'][law][kind] = dict(status='NO_TEMPLATE'); continue
                    payload = [(name, off[name] + s, f, P) for (name, d, f, P), s in zip(dets, sig)]
                    inj_jobs.append((ev['name'], ev, payload, law, kind, args.nlive, outdir))
        with ctx.Pool(min(args.pool, max(1, len(inj_jobs)))) as pool:
            for key, law, kind, r, med in pool.imap_unordered(job, inj_jobs):
                results[key]['laws'][law][kind] = r
                print('  %-8s %-22s %s a=%s+-%s %.0fs %s' % (kind, key, law, ('%.3f' % r['a_mean']) if r.get('a_mean') is not None else 'NA', ('%.3f' % r['a_std']) if r.get('a_std') is not None else 'NA', r.get('runtime_s', 0), r['status']), flush=True)
    grid = np.linspace(A_LO, A_HI, 601); combined = {}
    for law in laws:
        lp = np.zeros_like(grid); n_ev = 0; lnB = 0.0; per = []; lps = []; keys = []; n_edge = 0
        for key, R in results.items():
            r = R['laws'].get(law, {}).get('on')
            if not r or r.get('status') != 'OK': continue
            if r.get('prior_edge'): n_edge += 1; r['used_in_combination'] = False; continue
            r['used_in_combination'] = True
            lp += np.array(r['log_post_grid']); lps.append(np.array(r['log_post_grid'])); keys.append(key); n_ev += 1; lnB += r['lnB_noecho_over_echo']; per.append((r['a_mean'], r['a_std']))
        if n_ev == 0: combined[law] = dict(n_events=0, n_prior_edge_excluded=n_edge); continue
        def _comb(lpx):
            wx = np.exp(lpx - lpx.max()); wx /= np.trapezoid(wx, grid); ax = float(np.trapezoid(grid * wx, grid)); sx = float(math.sqrt(max(np.trapezoid((grid - ax) ** 2 * wx, grid), 1e-300))); return ax, sx
        a_c, s_c = _comb(lp)
        ivw = np.array([1 / s ** 2 for _, s in per]); a_iv = float(np.sum(ivw * np.array([m for m, _ in per])) / ivw.sum()); s_iv = float(1 / math.sqrt(ivw.sum()))
        shares = ivw / ivw.sum(); i_max = int(np.argmax(shares)); jack_g = []; jack_i = []
        for i in range(n_ev):
            if n_ev < 2: break
            ai, si = _comb(lp - lps[i]); jack_g.append((abs(a_c - ai) / si, keys[i], ai, si))
            m = np.ones(n_ev, bool); m[i] = False; aj = float(np.sum(ivw[m] * np.array([mm for mm, _ in per])[m]) / ivw[m].sum()); sj = float(1 / math.sqrt(ivw[m].sum())); jack_i.append((abs(a_iv - aj) / sj, keys[i], aj, sj))
        jack_g.sort(reverse=True); jack_i.sort(reverse=True)
        for k_, sh_ in zip(keys, shares): results[k_]['laws'][law]['on']['weight_share'] = float(sh_)
        inj = {k: [] for k in ('inj_a0', 'inj_a1_A', 'inj_a1_B')}
        for key, R in results.items():
            for k in inj:
                r = R['laws'].get(law, {}).get(k)
                if r and r.get('status') == 'OK': inj[k].append((r['a_mean'], r['a_std']))
        def _iv(lst):
            if not lst: return None, None, 0
            wv = np.array([1 / s ** 2 for _, s in lst]); return float(np.sum(wv * np.array([m for m, _ in lst])) / wv.sum()), float(1 / math.sqrt(wv.sum())), len(lst)
        a0, s0, n0 = _iv(inj['inj_a0']); a1, s1, n1 = _iv(inj['inj_a1_A']); aB, sB, nB = _iv(inj['inj_a1_B'])
        combined[law] = dict(n_events=n_ev, n_prior_edge_excluded=n_edge, a_comb=a_c, sigma_comb=s_c, z_vs_0=a_c / s_c, z_vs_1=(a_c - 1.0) / s_c, power=1.0 / s_c, a_ivw=a_iv, sigma_ivw=s_iv, lnB_noecho_over_echo_total=lnB,
                             max_weight_share=float(shares[i_max]), max_weight_event=keys[i_max], jack_grid_max_shift_sigma=(jack_g[0][0] if jack_g else None), jack_grid_event=(jack_g[0][1] if jack_g else None), jack_grid_without=((jack_g[0][2], jack_g[0][3]) if jack_g else None),
                             jack_ivw_max_shift_sigma=(jack_i[0][0] if jack_i else None), jack_ivw_event=(jack_i[0][1] if jack_i else None),
                             inj_a0_mean=a0, inj_a0_sigma=s0, inj_a0_n=n0, inj_a1_mean=a1, inj_a1_sigma=s1, inj_a1_n=n1, inj_a1_bias=(a1 - 1.0) if a1 is not None else None,
                             inj_a1_B_mean=aB, inj_a1_B_sigma=sB, inj_a1_B_n=nB, family_diff=((aB - a1) if (aB is not None and a1 is not None) else None))
        print('COMBINADO %s: n=%d (borda excluidos %d) a=%.4f+-%.4f (z vs 0 %.2f; z vs 1 %.2f; poder %.2f) | ivw %.4f+-%.4f | peso max %.2f (%s) | jackknife grade %.2f sigma (%s) | lnB(sem/com) total %.2f | inj a0 %s+-%s (n=%d) | inj a1 %s+-%s (n=%d) | familia B %s+-%s (n=%d)' % (
            law, n_ev, n_edge, a_c, s_c, a_c / s_c, (a_c - 1) / s_c, 1 / s_c, a_iv, s_iv, shares[i_max], keys[i_max], (jack_g[0][0] if jack_g else float('nan')), (jack_g[0][1] if jack_g else 'NA'), lnB, ('%.3f' % a0) if a0 is not None else 'NA', ('%.3f' % s0) if s0 is not None else 'NA', n0,
            ('%.3f' % a1) if a1 is not None else 'NA', ('%.3f' % s1) if s1 is not None else 'NA', n1, ('%.3f' % aB) if aB is not None else 'NA', ('%.3f' % sB) if sB is not None else 'NA', nB), flush=True)
    for key, R in results.items():
        for law in R['laws']: R['laws'][law].pop('_med', None)
    out = dict(version='ECHO_PE_V2', amendment_of='ECHO_PE_V1', executed=time.strftime('%Y-%m-%dT%H:%M:%S'), runtime_s=time.time() - t_start,
               instrument=dict(lalsuite=lal.__version__, bilby=bilby.__version__, dynesty=__import__('dynesty').__version__, sampler='dynesty rwalk', families=FAMILIES, primary='A', final_state='SimIMREOBFinalMassSpin (SEOBNRv4)', python=sys.version.split()[0], env='WSL Ubuntu /opt/lal_env'),
               beta=BETA, a_pred=A_PRED, sign=SIGN, laws=laws, prediction='a = 1 (amplitude sqrt(beta), sinal -1, do kernel); a = 0 = sem eco',
               pipeline=dict(fs=FS, seg_s=SEG_S, t_peak=T_PEAK, band=[F_LO, F_HI], f_min_tpl=F_MIN_TPL, mc_det_min=MC_MIN, anchor_det_min=ANCHOR_DET_MIN, anchor_ev_min=ANCHOR_EV_MIN, dt_max=DT_MAX, dt_half=DT_HALF, m_floor=M_FLOOR, edge_frac=EDGE_FRAC, a_prior=[A_LO, A_HI], prior_widen=PRIOR_WIDEN,
                             nlive=args.nlive, walks=WALKS, dlogz=DLOGZ, marginalized='amplitude complexa por detector (prior plano)', inj=dict(t0=INJ_T0, snr_min=INJ_SNR_MIN, max_events=INJ_MAX, kinds=['a0', 'a1_A', 'a1_B'])),
               catalog=dict(path=CAT, sha256=sha256_file(CAT)), sources_sha256=sources, n_events_catalog=len(events), n_events_used=len(prepared), skipped=skipped, combined=combined, per_event=results)
    os.makedirs(OUT_DIR, exist_ok=True); tmp = args.out + '.tmp'
    json.dump(out, open(tmp, 'w', encoding='utf-8'), indent=1, default=lambda o: (float(o) if isinstance(o, (np.floating,)) else (o.tolist() if hasattr(o, 'tolist') else str(o))))
    os.replace(tmp, args.out); print('OK ->', args.out, '| %.0fs' % (time.time() - t_start), flush=True)
if __name__ == '__main__':
    main()
