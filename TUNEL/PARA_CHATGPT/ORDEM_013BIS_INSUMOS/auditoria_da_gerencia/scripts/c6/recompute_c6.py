"""Auditor's independent re-computation of C6 lnB (read-only on bancada files).

Own implementation of: window selection, readings' Gamma, 220+440 basis,
Gaussian amplitude marginalization and (M, chi) trapezoid integration.
Only DATA inputs are taken from the bancada: registry JSON, whitener npz,
QNM grid JSON and the public GWOSC HDF5 (opened read-only).
beta is computed at runtime: alpha CODATA 2018 * sqrt(e).
"""
import json, math, sys, hashlib
import numpy as np, h5py
from scipy.interpolate import CubicSpline
from scipy.special import logsumexp

B = "/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/"
ALPHA = 7.2973525693e-3          # CODATA 2018
BETA = ALPHA * math.sqrt(math.e)
C = 299792458.0
GM_SUN = 1.3271244e20            # IAU 2015 nominal (same profile the bancada declares)

reg_raw = open(B + "REGISTRO_C6.json", "rb").read()
reg = json.loads(reg_raw)
print("registry sha256", hashlib.sha256(reg_raw).hexdigest())
print("beta runtime", BETA)
W = {d: np.load(B + f"cache/empirical_noise/{d}_noise.npz")["whitener_scaled"] for d in ("H1", "L1")}
Q = json.load(open(B + "QNM_GRID.json"))["modes"]
spl = {k: CubicSpline(Q[k]["spins"], np.asarray(Q[k]["real"]) + 1j * np.asarray(Q[k]["imag"]), extrapolate=False) for k in ("220", "440")}
M_OF = {"220": 2, "440": 4}

def window(det, start):
    fn = {"H1": "H-H1", "L1": "L-L1"}[det] + "_GWOSC_O4b_4KHZ_R1-1420877824-4096.hdf5"
    with h5py.File(B + "cache/gwosc/on_source/" + fn, "r") as h:
        gps0 = float(h["meta/GPSstart"][()]); raw = h["strain/Strain"]
        fs = 1.0 / float(raw.attrs["Xspacing"])
        req = reg["reference_peak_GPS"][det] + start * reg["reference_tM_seconds"]
        first = int(np.ceil((req - gps0) * fs))
        n = reg["interval_samples"]; st = reg["sample_stride"]
        x = np.asarray(raw[first:first + n * st:st], dtype=float) * 1e21
    return x, first, gps0 + first / fs, req

def gamma(reading, w, tm, chi, m):
    if reading == "R-GLOBAL": return 0.0
    if reading == "R-B": return BETA * tm * w * w / 2
    if reading == "R-RAIZ-0": return BETA * w / 2
    if reading == "R-LIN": return BETA * w
    if reading == "R-MOD":
        r = math.sqrt(1 - chi * chi); oh = chi / (2 * tm * (1 + r)); kap = r / (2 * tm * (1 + r))
        eff = w - m * oh
        if eff <= 0: raise ValueError("non-corotating")
        return BETA * (2 * math.pi / kap) * eff * eff / 2
    raise ValueError(reading)

def loglike_grid(y, Wd, masses, spins, reading, sd, deform=("220", "440")):
    t = np.arange(reg["interval_samples"]) / reg["analysis_sample_rate_hz"]
    out = np.empty(len(masses))
    for i, (mm, ch) in enumerate(zip(masses, spins)):
        tm = mm * GM_SUN / C**3
        cols = []
        for k in ("220", "440"):
            q = complex(spl[k](ch)); wr, dmp = q.real, -q.imag
            w = wr / tm; tau = tm / dmp
            g = gamma(reading, w, tm, ch, M_OF[k]) if k in deform else 0.0
            env = np.exp(-(1 / tau + g) * t)
            cols += [env * np.cos(w * t), env * np.sin(w * t)]
        Bm = Wd @ np.stack(cols, axis=1)
        G = Bm.T @ Bm; b = Bm.T @ y
        A = G + np.eye(4) / sd**2
        _, ld = np.linalg.slogdet(A * sd**2)
        out[i] = 0.5 * b @ np.linalg.solve(A, b) - 0.5 * ld
    return out

def grid(level):
    n0, n1 = reg["quadrature_grids"][level]
    m = np.linspace(*reg["mass_detector_prior_solar"], n0); s = np.linspace(*reg["spin_prior"], n1)
    M, S = np.meshgrid(m, s, indexing="ij")
    w = np.ones((n0, n1)); w[[0, -1], :] *= .5; w[:, [0, -1]] *= .5; w /= w.sum()
    return M.ravel(), S.ravel(), np.log(w.ravel())

if __name__ == "__main__":
    start = float(sys.argv[1]); level = int(sys.argv[2]); mode = sys.argv[3] if len(sys.argv) > 3 else "free"
    sd = 10.0
    ys = {}
    for d in ("H1", "L1"):
        x, first, g1, req = window(d, start)
        ys[d] = W[d] @ x
        print(d, "first_index", first, "first_GPS %.6f" % g1, "norm2 %.6f" % float(ys[d] @ ys[d]))
    readings = ["R-GLOBAL", "R-B", "R-RAIZ-0", "R-LIN", "R-MOD"]
    if mode == "free":
        M, S, lw = grid(level)
        res = {}
        for r in readings:
            ll = sum(loglike_grid(ys[d], W[d], M, S, r, sd) for d in ys)
            res[r] = float(logsumexp(ll + lw))
        ref = res["R-GLOBAL"]
        print(json.dumps({r: {"lnZ": res[r], "lnB": res[r] - ref} for r in readings}, indent=1))
        # variant: only 220 deformed (440 kept Kerr)
        res2 = {}
        for r in readings:
            ll = sum(loglike_grid(ys[d], W[d], M, S, r, sd, deform=("220",)) for d in ys)
            res2[r] = float(logsumexp(ll + lw))
        print("ONLY_220_DEFORMED", json.dumps({r: res2[r] - res2["R-GLOBAL"] for r in readings}))
    else:
        # diagnostic: remnant fixed at a declared point (auditor diagnostic, not registered)
        mm, ch = [float(v) for v in mode.split(",")]
        res = {}
        for r in readings:
            res[r] = float(sum(loglike_grid(ys[d], W[d], np.array([mm]), np.array([ch]), r, sd)[0] for d in ys))
        print("FIXED", mm, ch, json.dumps({r: res[r] - res["R-GLOBAL"] for r in readings}))
