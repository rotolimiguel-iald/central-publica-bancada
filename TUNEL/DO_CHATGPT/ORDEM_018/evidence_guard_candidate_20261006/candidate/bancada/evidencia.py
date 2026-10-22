# -*- coding: utf-8 -*-
"""evidencia.py -- as OPERAÇÕES de evidência da Bancada Um sobre o motor residente: avaliar, ajustar, comparar, amostrar.
Toda operação devolve o seu ESTATUTO; ajustar/comparar/amostrar entram no LIVRO (família de teste) e trazem a significância local ao lado
de uma ilustração de Šidák; significância global não calibrada fica indisponível."""
import math
import threading
import time
import uuid

import numpy as np
import torch

from .amostrador import amostrar, resumo
from .motor import NOMES_THETA, opcoes_de, rotulo_opcoes
from .regua import ESTATUTOS, guarda, p_de_z, z_de_p
from .evidence_checks import finite_number, nested_deltas, validate_fit

CONJUNTOS = ("planck_comp", "desi_dr1", "desi_dr2", "sh0es", "pantheon", "sh0es_local", "cc_moresco", "pantheon_sh0es")   # 30/09: + Pantheon+ (cov completa, M profilado); + sh0es_local (Fase 2, lei D1a)
FIDUCIAL = dict(H0=67.5, ombh2=0.02237, omch2=0.1200, beta=0.0, c=0.0)
ESCALA = dict(H0=1.0, ombh2=0.0005, omch2=0.005, beta=0.005, c=0.005)


def _conj(c):
    c = list(c or ("planck_comp", "desi_dr1"))
    ruins = [x for x in c if x not in CONJUNTOS]
    if ruins:
        raise ValueError("conjunto desconhecido: %s (válidos: %s)" % (ruins, CONJUNTOS))
    return c


class Evidencia:
    def __init__(self, motor, livro):
        self.m = motor
        self.livro = livro
        self.tarefas = {}

    def _beta(self, beta):
        if beta in (None, "livre"):
            return None
        if beta == "tgl":
            return self.m.beta_tgl
        if beta in ("zero", "lcdm"):
            return 0.0
        return float(beta)

    # ---------- avaliar ----------
    def avaliar(self, theta, conjuntos=None, curvas=True, opcoes=None):
        cj = _conj(conjuntos or CONJUNTOS)
        o = opcoes_de(opcoes)
        th = np.array([[float(theta.get(k, FIDUCIAL[k])) if k != "beta" or theta.get(k) != "tgl" else self.m.beta_tgl for k in NOMES_THETA]])
        with self.m.lock:
            tot, partes, p = self.m.chi2(th, cj, o)
            curv = self._curvas(th) if curvas else None
        out = dict(theta=dict(zip(NOMES_THETA, th[0].tolist())), conjuntos=cj, opcoes=o, modo=rotulo_opcoes(o), chi2_total=float(tot[0]),
                   chi2=dict((k, float(v[0])) for k, v in partes.items()), n_dados=self.m.n_dados(cj),
                   predito=dict(planck=p["planck"][0].tolist(), desi_dr1=p["dr1"][0].tolist(), desi_dr2=p["dr2"][0].tolist(), H0=float(p["H0"][0]), H0_local=float(p["H0_local"][0]), K_lei=float(p["K_lei"][0]), I_lei=float(p["I_lei"][0]),
                                pantheon=dict(n=self.m.pantheon.n, M_hat=float(self.m.pantheon.M_hat(p["pantheon_mu"])[0])),
                                pantheon_sh0es=dict(n=self.m.pantheon_sh0es.n, M_hat=float(self.m.pantheon_sh0es.M_hat(p["pantheon_sh0es_mu"])[0]))),
                   derivados=dict(Omega_L=float(p["OL"][0]), r_drag=float(p["r_drag"][0]), r_star=float(p["r_star"][0]), z_star=float(p["z_star"][0]),
                                  E0_menos_1=float(p["E0"][0]) - 1.0, residuo_fecho=float(p["res_fecho"][0]), autoverif_DM_camb=float(p["selfcheck"][0]),
                                  dentro_dos_limites=bool(p["dentro"][0])),
                   curvas=curv, estatuto="DIAGNOSTICO_DE_AVALIACAO", estatuto_texto=ESTATUTOS["DIAGNOSTICO_DE_AVALIACAO"])
        return guarda(out)

    def _curvas(self, th):
        z = torch.linspace(0.02, 2.6, 160, device=self.m.dev, dtype=torch.float64)
        T = self.m._t(th)
        H0, ombh2, omch2, beta, c = [T[:, j] for j in range(5)]
        cam, _ = self.m.tab(H0, ombh2, omch2)
        fd = self.m.fundo.fundo(H0, ombh2, omch2, beta, c)
        z0 = torch.zeros_like(beta)
        fl = self.m.fundo.fundo(H0, ombh2, omch2, z0, z0)
        rd = cam["r_drag"] * self.m.fundo.rs_int(fd, cam["z_drag"]) / self.m.fundo.rs_int(fl, cam["z_drag"])
        zz = z[None, :]
        DM = self.m.fundo.DM(fd, zz)[0]
        DH = 299792.458 / (H0[:, None] * self.m.fundo.Ez(fd, zz))[0]
        DV = (z * DM * DM * DH) ** (1.0 / 3.0)
        # a curva ΛCDM de referência com os MESMOS (H0, ω_b, ω_c): mostra só o efeito de β e c
        rdl = cam["r_drag"]
        DMl = self.m.fundo.DM(fl, zz)[0]
        DHl = 299792.458 / (H0[:, None] * self.m.fundo.Ez(fl, zz))[0]
        DVl = (z * DMl * DMl * DHl) ** (1.0 / 3.0)
        f = lambda t: [float(v) for v in t.cpu()]
        Phi = fd["Phi"][0]
        xg = self.m.fundo.x2
        sel = (xg <= 0.0) & (xg >= -math.log(1.0 + 3.0))
        return dict(z=f(z), DM_rd=f(DM / rd[0]), DH_rd=f(DH / rd[0]), DV_rd=f(DV / rd[0]),
                    lcdm=dict(DM_rd=f(DMl / rdl[0]), DH_rd=f(DHl / rdl[0]), DV_rd=f(DVl / rdl[0])),
                    Phi=dict(z=f(torch.expm1(-xg[sel])), Phi=f(Phi[sel])))

    # ---------- ajustar ----------
    def _ajuste(self, cj, beta_fixo, c_livre, x0=None, opcoes=None):
        from scipy.optimize import least_squares
        o = opcoes_de(opcoes)
        livres = ["H0", "ombh2", "omch2"] + (["beta"] if beta_fixo is None else []) + (["c"] if c_livre else [])
        base = np.array([FIDUCIAL[k] for k in NOMES_THETA])
        if beta_fixo is not None:
            base[3] = beta_fixo
        esc = np.array([ESCALA[k] for k in livres])
        idx = [NOMES_THETA.index(k) for k in livres]
        lim = self.m.limites
        lo = np.array([(lim[k][0] - base[i]) / e for k, i, e in zip(livres, idx, esc)]) * 0.999
        hi = np.array([(lim[k][1] - base[i]) / e for k, i, e in zip(livres, idx, esc)]) * 0.999
        ini = np.zeros(len(livres)) if x0 is None else (np.asarray(x0)[idx] - base[idx]) / esc

        def monta(Y):
            T = np.tile(base, (Y.shape[0], 1))
            T[:, idx] = base[idx] + Y * esc
            return T

        cache = {}

        def residuos_e_jac(y):
            key = tuple(np.round(y, 14))
            if key in cache:
                return cache[key]
            hstep = 1e-3
            Y = np.vstack([y] + [y + hstep * np.eye(len(y))[i] for i in range(len(y))] + [y - hstep * np.eye(len(y))[i] for i in range(len(y))])
            with self.m.lock:
                R, _ = self.m.residuos(monta(Y), cj, o)
            R = R.cpu().numpy()
            n = len(y)
            J = (R[1:1 + n] - R[1 + n:]).T / (2 * hstep)
            cache.clear(); cache[key] = (R[0], J)
            return R[0], J

        res = least_squares(lambda y: residuos_e_jac(y)[0], ini, jac=lambda y: residuos_e_jac(y)[1], bounds=(lo, hi), method="trf",
                            x_scale=1.0, xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=200)
        th = monta(res.x[None, :])[0]
        r0, J = residuos_e_jac(res.x)
        chi2 = float(r0 @ r0)
        try:
            cov = np.linalg.inv(J.T @ J) * np.outer(esc, esc)
            sig = {k: float(math.sqrt(cov[i, i])) for i, k in enumerate(livres)}
        except np.linalg.LinAlgError:
            sig = {}
        return dict(theta=dict(zip(NOMES_THETA, th.tolist())), chi2=chi2, livres=livres, sigma_JtJ=sig, sucesso=bool(res.success),
                    nfev=int(res.nfev), n_dados=self.m.n_dados(cj), gl=self.m.n_dados(cj) - len(livres), opcoes=o)

    def ajustar(self, conjuntos=None, beta="livre", c_livre=False, cliente="?", opcoes=None):
        cj = _conj(conjuntos)
        o = opcoes_de(opcoes)
        bf = self._ajuste(cj, self._beta(beta), bool(c_livre), opcoes=o)
        modelo = dict(beta=str(beta), c_livre=bool(c_livre), opcoes=o)
        self._fit_or_fail(bf, "ajustar", cj, modelo, cliente, "fit")
        out = dict(conjuntos=cj, beta=beta, c_livre=bool(c_livre), opcoes=o, modo=rotulo_opcoes(o), ajuste=bf, beta_tgl=self.m.beta_tgl,
                   estatuto="AJUSTE_DE_MAXIMA_VEROSSIMILHANCA", estatuto_texto=ESTATUTOS["AJUSTE_DE_MAXIMA_VEROSSIMILHANCA"])
        if self._beta(beta) is None and "beta" in bf["sigma_JtJ"]:
            try:
                s = finite_number(bf["sigma_JtJ"]["beta"], "sigma_beta", positive=True)
                b = bf["theta"]["beta"]
                z = finite_number((self.m.beta_tgl - b) / s, "wald_z")
            except ValueError as exc:
                self._evidence_failure("ajustar", cj, modelo, cliente, str(exc))
                raise
            out["beta_tgl_em_sigma_JtJ"] = z
            out["significancia"] = self.livro.corrige(p_de_z(z), self.livro.familia("ajustar", cj, modelo))
        guarda(out)
        self.livro.registra(cliente, "ajustar", cj, modelo, dict(conjuntos=cj), out, out["estatuto"],
                            bf["chi2"], out.get("significancia", {}).get("p_local"))
        return out

    def _evidence_failure(self, operation, cj, model, client, reason):
        failure = dict(estatuto="DIAGNOSTICO_INVALIDO_SEM_SIGNIFICANCIA",
                       reason=reason, significancia=None)
        guarda(failure)
        self.livro.registra(client, operation, cj, model, dict(conjuntos=cj),
                            failure, failure["estatuto"], None, None)

    def _fit_or_fail(self, fit, operation, cj, model, client, label):
        try:
            return validate_fit(fit, NOMES_THETA)
        except ValueError as exc:
            reason = label + ": " + str(exc)
            self._evidence_failure(operation, cj, model, client, reason)
            raise ValueError(reason) from exc

    def comparar(self, conjuntos=None, c_livre=False, cliente="?", opcoes=None):
        cj = _conj(conjuntos)
        o = opcoes_de(opcoes)
        modelo = dict(c_livre=bool(c_livre), opcoes=o)
        l = self._ajuste(cj, 0.0, bool(c_livre), opcoes=o)
        self._fit_or_fail(l, "comparar", cj, modelo, cliente, "LCDM")
        initial = [l["theta"][k] for k in NOMES_THETA]
        t = self._ajuste(cj, self.m.beta_tgl, bool(c_livre), x0=initial, opcoes=o)
        self._fit_or_fail(t, "comparar", cj, modelo, cliente, "fixed TGL")
        f = self._ajuste(cj, None, bool(c_livre), x0=initial, opcoes=o)
        self._fit_or_fail(f, "comparar", cj, modelo, cliente, "free beta")
        try:
            d_tgl_livre, d_lcdm_livre = nested_deltas(l, t, f)
        except ValueError as exc:
            self._evidence_failure("comparar", cj, modelo, cliente, str(exc))
            raise
        p_tgl = float(math.erfc(math.sqrt(d_tgl_livre / 2.0)))
        out = dict(conjuntos=cj, c_livre=bool(c_livre), opcoes=o, modo=rotulo_opcoes(o),
                   lcdm=l, tgl_beta_fixo=t, beta_livre=f, beta_tgl=self.m.beta_tgl,
                   delta_chi2=dict(tgl_menos_lcdm=t["chi2"] - l["chi2"],
                                   tgl_menos_livre=d_tgl_livre, lcdm_menos_livre=d_lcdm_livre),
                   leitura=("Δχ²(TGL fixa contra β livre) = %.3f; z equivalente local = %.2f "
                            "(Wilks condicional, 1 g.l.; regularidade não validada aqui). "
                            "Δχ²(ΛCDM contra β livre) = %.3f. TGL−ΛCDM permanece assinada, sem conversão em sigma. [%s]"
                            % (d_tgl_livre, math.sqrt(d_tgl_livre), d_lcdm_livre, rotulo_opcoes(o))),
                   hipoteses_significancia=dict(nula="TGL_BETA_FIXO", alternativa="BETA_LIVRE",
                                                graus_liberdade=1, regularidade_verificada=False),
                   significancia=self.livro.corrige(p_tgl, self.livro.familia("comparar", cj, modelo)),
                   estatuto="COMPARACAO_DE_MODELOS_DELTA_CHI2",
                   estatuto_texto=ESTATUTOS["COMPARACAO_DE_MODELOS_DELTA_CHI2"])
        guarda(out)
        self.livro.registra(cliente, "comparar", cj, modelo, dict(conjuntos=cj),
                            out, out["estatuto"], d_tgl_livre, p_tgl)
        return out

    # ---------- amostrar (tarefa assíncrona) ----------
    def amostrar(self, conjuntos=None, c_livre=False, walkers=256, passos=2000, queima=500, semente=42, cliente="?", opcoes=None):
        cj = _conj(conjuntos)
        o = opcoes_de(opcoes)
        walkers = int(min(max(walkers, 16), 4096)) // 2 * 2
        passos = int(min(max(passos, 100), 20000))
        queima = int(min(max(queima, 0), passos - 50))
        tid = uuid.uuid4().hex[:12]
        t = dict(id=tid, estado="na_fila", progresso=0, conjuntos=cj, c_livre=bool(c_livre), opcoes=o, modo=rotulo_opcoes(o), walkers=walkers,
                 passos=passos, queima=queima, semente=int(semente), criada=time.strftime("%H:%M:%S"), resultado=None, erro=None)
        self.tarefas[tid] = t
        threading.Thread(target=self._roda, args=(t, cliente), daemon=True).start()
        return dict(tarefa=tid)

    def _roda(self, t, cliente):
        try:
            t["estado"] = "rodando"
            nd = 5 if t["c_livre"] else 4
            nomes = list(NOMES_THETA[:nd])
            fid = np.array([FIDUCIAL[k] for k in nomes]); larg = np.array([ESCALA[k] for k in nomes]); larg[0] = 1.0
            rng = np.random.default_rng(t["semente"])
            p0 = fid + rng.normal(0, 1, size=(t["walkers"], nd)) * larg

            def logp(tt):
                th = tt if nd == 5 else torch.cat([tt, torch.zeros_like(tt[:, :1])], 1)
                with self.m.lock:
                    tot, _, _ = self.m.chi2(th, t["conjuntos"], t["opcoes"])
                return -0.5 * tot

            def ao_passo(s, n, seg):
                t["progresso"] = s / n; t["segundos"] = round(seg, 1)

            cadeia, lps, acc, seg = amostrar(logp, torch.tensor(p0, device=self.m.dev, dtype=torch.float64), t["passos"], t["semente"], ao_passo=ao_passo)
            res, taus, plano = resumo(cadeia, t["queima"], nomes)
            b = plano[:, 3]
            frac = float(np.mean(b >= self.m.beta_tgl)); frac0 = float(np.mean(b >= 0.0))
            p2 = 2.0 * min(frac, 1.0 - frac) if 0 < frac < 1 else 1.0 / plano.shape[0]
            hb, eb = np.histogram(b, bins=70)
            h2, ex, ey = np.histogram2d(b, plano[:, 0], bins=48)
            modelo = dict(c_livre=t["c_livre"], opcoes=t["opcoes"])
            out = dict(conjuntos=t["conjuntos"], c_livre=t["c_livre"], opcoes=t["opcoes"], modo=t["modo"], walkers=t["walkers"], passos=t["passos"],
                       queima=t["queima"], semente=t["semente"],
                       segundos=round(seg, 1), aceitacao_media=float(acc.mean()), tau=dict(zip(nomes, taus)),
                       amostras_efetivas=float(plano.shape[0] / max(taus)), resumo=res, beta_tgl=self.m.beta_tgl,
                       fracao_beta_acima_de_beta_tgl=frac, fracao_beta_acima_de_zero=frac0,
                       beta_tgl_pela_cauda=dict(p_bilateral=p2, z=z_de_p(p2), nota="pela fração do posterior além de α√e (bilateral)"),
                       significancia=self.livro.corrige(p2, self.livro.familia("amostrar", t["conjuntos"], modelo)),
                       hist_beta=dict(contagens=hb.tolist(), bordas=eb.tolist()),
                       hist_beta_H0=dict(contagens=h2.tolist(), bordas_beta=ex.tolist(), bordas_H0=ey.tolist()),
                       estatuto="POSTERIOR_CONDICIONAL_AO_MODELO_E_AOS_DADOS", estatuto_texto=ESTATUTOS["POSTERIOR_CONDICIONAL_AO_MODELO_E_AOS_DADOS"])
            guarda(out)
            self.livro.registra(cliente, "amostrar", t["conjuntos"], modelo,
                                dict(walkers=t["walkers"], passos=t["passos"], queima=t["queima"], semente=t["semente"]), out, out["estatuto"],
                                res["beta"]["median"], p2)
            t["resultado"] = out; t["estado"] = "pronta"; t["progresso"] = 1.0
        except Exception as e:  # falha visível, nunca «ok» falso
            t["estado"] = "falhou"; t["erro"] = repr(e)
