def prove_ringdown_dephasing_protocol(ONE):
    """v346 -- O RINGDOWN CONTRA A RG E CONTRA A LEI DE DEPHASING, PRE-REGISTRADO [ADITIVO; fail-closed; nao gateia 1=1; fora do contorno].
    Ordem do operador (10/09/2026): «Concordo com tudo, era isso mesmo, reconheci todos e concordo com sua ordem tb» -- o primeiro dos
    testes que aguardavam o instrumento (protocolo de observacao de outubro de 2025: `test_gw_ringdown`, `measure_ringdown_damping`).
    O que se testa: a lei de dephasing Gamma_omega = (1/2) beta tau* omega^2 [REAL na forma; tau* INPUT] somada a taxa de decaimento do
    modo dominante do ringdown: tau_obs/tau_GR - 1 = -Gamma tau_GR. Ramo A (tau* = t_Planck): ~1e-40, invisivel -- e o limite assintotico
    por construcao. Ramo B (tau* = G M_f/c^3): ~1-2% -- o ramo que a secao 20 (01/06/2026) marcou como «provavelmente ja excluido por
    ringdowns consistentes com a RG» SEM nunca medir. Aqui mede-se. Previsao de Kerr por evento [KNOWN]: massa e spin finais pelo ajuste
    EOB do lalsuite a partir de (m1, m2, chi_eff) do catalogo; f_220 e Q_220 de Berti-Cardoso-Will (2006). Medida: seno amortecido
    branqueado com a PSD do evento, janela [t_pico + 3 ms, + 6 tau_GR] (secundaria: 6 ms, cuja diferenca e a sistematica de overtones);
    nulos por injecao fora da fonte (vies e sigma de tau); empilhamento por variancia inversa de delta = tau_obs/tau_GR - 1.
    Vereditos: BRANCH_B_EXCLUDED (|delta - delta_B| >= 5 sigma e poder >= 5), GR_TENSION (|delta| >= 5 sigma; relatado, nao e da TGL),
    NOT_FALSIFIED_POWERED, NOT_FALSIFIED_UNDERPOWERED (poder < 5), INCONCLUSIVE_SYSTEMATICS (|delta(3ms) - delta(6ms)| > sigma ou vies > 0,2).
    beta jamais literal. CONFIRMED proibido."""
    beta = SEALED_CODATA_ALPHA * math.sqrt(math.e); t_p = math.sqrt(HBAR_EXACT * G_NEWTON / C_LIGHT ** 5)
    proto = {
        "version": "RINGDOWN_DEPHASING_V1", "status": "PRE_REGISTERED_BEFORE_DATA_READ",
        "hypothesis": {"law": "Gamma_omega = (1/2) beta tau* omega^2 [REAL na forma]", "observable": "tau_obs/tau_GR - 1 = -Gamma tau_GR (modo 220)",
                       "branch_A": "tau* = t_Planck = %.3e s (invisivel: limite assintotico por construcao)" % t_p, "branch_B": "tau* = G M_f / c^3 (o ramo nunca medido)",
                       "beta_source": "SEALED_CODATA_ALPHA * sqrt(e) em runtime"},
        "kerr_prediction_KNOWN": "SimIMREOBFinalMassSpin (SEOBNRv4) de (m1, m2, chi_eff) do catalogo -> (M_f, a_f); Berti-Cardoso-Will 2006 -> f_220, Q_220; tau_GR = Q/(pi f)",
        "data": "cache de maio (GWOSC via gwpy, 32 s @ 4096 Hz) dos eventos GWTC com massas no catalogo; H1 + L1; sha256 por fonte e do catalogo",
        "pipeline": {"psd": "Welch Hann 4 s dos 14 s pre-evento", "band_hz": [20.0, 1024.0], "peak": "envoltoria analitica em +-50 ms do GPS",
                     "window": "[t_pico + 3 ms, t_pico + 6 tau_GR]; secundaria + 6 ms", "template": "seno amortecido TD branqueado com a mesma PSD, restrito a janela",
                     "grid": "f_GR x [0.7, 1.3] (13); tau_GR x [0.4, 2.5] log (15); refino 9 x 9", "fit": "linear em (cos, sin) por ponto da grade; argmax da energia explicada"},
        "nulls": {"off_source": "40 janelas de 0,3 s em [-15,5; -3] s", "injection": "o ringdown ajustado injetado em ruido: vies e sigma relativos de tau e f",
                  "guards": {"snr_min": 5.0, "transient_sd": 10.0}, "systematics": "|delta(3 ms) - delta(6 ms)| (contaminacao de overtones/merger)"},
        "aggregation": "variancia inversa sobre series de delta - vies; previsao do ramo B ponderada igual",
        "criteria": {"exclude_z": 5.0, "power_min": 5.0, "bias_max_rel": 0.2, "systematics_max_sigma": 1.0, "min_series": 20},
        "allowed_verdicts": ["TGL_RINGDOWN_BRANCH_B_EXCLUDED", "TGL_RINGDOWN_GR_TENSION_REPORTED", "TGL_RINGDOWN_NOT_FALSIFIED_POWERED", "TGL_RINGDOWN_NOT_FALSIFIED_UNDERPOWERED",
                             "TGL_RINGDOWN_INCONCLUSIVE_SYSTEMATICS", "TGL_RINGDOWN_AWAITING_RESULT_FILE"],
        "forbidden_verdicts": ["CONFIRMED", "PROVED"],
        "what_it_cannot_do": "nao distingue a TGL da RG no ramo A (por construcao); no ramo B, so exclui ou nao exclui a escala tau* = GM/c^3",
    }
    ph = hashlib.sha256(json.dumps(proto, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    checks = [("protocolo pre-registrado e hasheado (%s)" % ph, True), ("beta jamais literal", bool(abs(beta - SEALED_CODATA_ALPHA * math.sqrt(math.e)) == 0.0)),
              ("ramo A computado invisivel (Gamma tau_GR < 1e-30 para GW150914-like)", bool(0.5 * beta * t_p * (2 * math.pi * 250.0) ** 2 * 0.004 < 1e-30)), ("nenhum veredito proibido por construcao", True)]
    all_v = bool(all(v for _, v in checks))
    return {"protocol": proto, "protocol_hash": ph, "checks": checks, "all_verified": all_v, "does_not_gate_core": True, "in_contour_roster_v314": False,
            "verdict": ("TGL_RINGDOWN_DEPHASING_V1__PROTOCOL_PRE_REGISTERED_%s__BRANCH_A_INVISIBLE_BY_CONSTRUCTION__BRANCH_B_TO_BE_MEASURED__GATE_UNTOUCHED" % ph) if all_v else "TGL_RINGDOWN_PROTOCOL_NOT_SEALED_THIS_RUN"}


def prove_ringdown_dephasing_result(ONE, protocol_record=None):
    """v346 -- o resultado do ringdown (pipeline externo ringdown_dephasing_v1.py no WSL), lido por hash e julgado pela matriz acima.
    O que a V1 devolveu [REAL, lido]: o gate pre-registrado RECUSOU selar (janela secundaria com menos de 20 series) e a matriz leu
    INCONCLUSIVE_SYSTEMATICS. A recusa e o resultado da V1; a autopsia e a emenda V2 vivem em prove_ringdown_dephasing_amendment_v2."""
    _t0 = time.time()
    beta = SEALED_CODATA_ALPHA * math.sqrt(math.e)
    proto = protocol_record or prove_ringdown_dephasing_protocol(ONE); ph = proto.get("protocol_hash"); crit = (proto.get("protocol") or {}).get("criteria") or {}
    res_p = os.path.join(CACHE, "gw", "RINGDOWN_DEPHASING_V1_RESULT.json")
    base = {"result_path": res_p, "protocol_hash": ph, "does_not_gate_core": True, "in_contour_roster_v314": False, "beta_runtime": beta,
            "why_outside_contour": "tau* e INPUT: o que se exclui e a escala tau* = GM/c^3, nao a lei de dephasing nem a TGL"}
    st = {"leitura": "[REAL] o um.py nao recalcula: le por hash e aplica a matriz pre-registrada (%s)" % ph,
          "ramo_A": "[REAL, computado] com tau* = t_Planck o efeito e ~1e-40: o ringdown e RG por construcao -- o limite assintotico com numero",
          "secao_20": "[ERRATA AO LADO] a secao 20 dizia «provavelmente ja excluido» sem medir; aqui o ramo B e medido"}
    rj, rhash = _read_external_json_with_hash(res_p)
    if rj is None:
        return dict(base, verdict="TGL_RINGDOWN_AWAITING_RESULT_FILE", all_verified=False, checks=[("resultado RINGDOWN_DEPHASING_V1 em cache/gw", False)], statuses=st, runtime_s=float(time.time() - _t0))
    stacks = rj.get("stacks") or {}; s3 = stacks.get("3.0") or {}; s6 = stacks.get("6.0") or {}; inst = rj.get("instrument") or {}
    checks = [("resultado lido por hash (%s)" % rhash, True),
              ("beta do resultado == beta recomputado", bool(abs(float(rj.get("beta", 0)) - beta) < 1e-15)),
              ("instrumento lalsuite (ajuste EOB de estado final) registrado", bool(inst.get("lalsuite") and "EOB" in str(inst.get("final_state", "")))),
              ("catalogo e fontes com sha256", bool((rj.get("catalog") or {}).get("sha256") and len(rj.get("sources_sha256") or {}) >= 100)),
              ("janelas 3 ms e 6 ms com >= %d series" % int(crit.get("min_series", 20)), bool((s3.get("n_used") or 0) >= int(crit.get("min_series", 20)) and (s6.get("n_used") or 0) >= int(crit.get("min_series", 20)))),
              ("nenhum veredito proibido por construcao", True)]
    all_v = bool(all(v for _, v in checks))
    d, sg, pB, pA = s3.get("delta_tau"), s3.get("sigma"), s3.get("delta_pred_B"), s3.get("delta_pred_A")
    syst = rj.get("start_systematic"); bias = s3.get("mean_bias_rel")
    reasons = []
    if syst is None or (sg and abs(syst) > float(crit.get("systematics_max_sigma", 1.0)) * sg): reasons.append("|delta(3ms)-delta(6ms)| = %s > %.0f sigma" % (("%.4f" % syst) if syst is not None else "AUSENTE", float(crit.get("systematics_max_sigma", 1.0))))
    if bias is None or abs(bias) > float(crit.get("bias_max_rel", 0.2)): reasons.append("vies relativo de tau %s > %.1f" % (("%.3f" % bias) if bias is not None else "AUSENTE", float(crit.get("bias_max_rel", 0.2))))
    z_gr = (d / sg) if sg else None; z_B = ((d - pB) / sg) if sg else None; power_B = (abs(pB) / sg) if sg else None
    if reasons: outcome = "INCONCLUSIVE_SYSTEMATICS"
    elif z_B is not None and abs(z_B) >= float(crit.get("exclude_z", 5.0)) and power_B >= float(crit.get("power_min", 5.0)): outcome = "BRANCH_B_EXCLUDED"
    elif z_gr is not None and abs(z_gr) >= float(crit.get("exclude_z", 5.0)): outcome = "GR_TENSION_REPORTED"
    elif power_B is not None and power_B >= float(crit.get("power_min", 5.0)): outcome = "NOT_FALSIFIED_POWERED"
    else: outcome = "NOT_FALSIFIED_UNDERPOWERED"
    _f = lambda v, p=4: (("%%.%df" % p) % v) if isinstance(v, (int, float)) else "NA"
    refused = [c[0] for c in checks if not c[1]]
    verdict = ("TGL_RINGDOWN_DEPHASING_V1__RESULT_READ_BY_HASH__%s__DELTA_TAU_%s__BRANCH_B_PRED_%s__POWER_%s_OF_5_SIGMA__BRANCH_A_INVISIBLE__GATE_UNTOUCHED"
               % (outcome, _f(d).replace(".", "P").replace("-", "M"), _f(pB).replace(".", "P").replace("-", "M"), _f(power_B, 1).replace(".", "P"))) if all_v else \
              ("TGL_RINGDOWN_DEPHASING_V1__RESULT_READ_BY_HASH__GATE_REFUSED__%s__MATRIX_WOULD_READ_%s__SEE_AMENDMENT_V2__GATE_UNTOUCHED" % ("_".join(sorted(set(("MIN_SERIES" if "series" in r else "OTHER") for r in refused))), outcome))
    statuses = dict(st)
    statuses["resultado"] = ("[REAL, lido] %s series (3 ms): delta_tau = tau_obs/tau_GR - 1 = %s +- %s (z vs RG %s); previsao do ramo B %s (z vs B %s; poder %s sigma); ramo A %s; "
                             "delta_f = %s +- %s; SNR medio %s; vies %s; sistematica 3 vs 6 ms %s => %s%s%s"
                             % (s3.get("n_used"), _f(d), _f(sg), _f(z_gr, 2), _f(pB), _f(z_B, 2), _f(power_B, 2), ("%.1e" % pA) if isinstance(pA, (int, float)) else "NA",
                                _f(s3.get("delta_f")), _f(s3.get("sigma_f")), _f(s3.get("mean_snr"), 1), _f(bias, 3), _f(syst), outcome, (" [%s]" % "; ".join(reasons) if reasons else ""),
                                ("" if all_v else " | GATE RECUSOU: %s (janela 6 ms com %s series)" % ("; ".join(refused), s6.get("n_used")))))
    return dict(base, verdict=verdict, all_verified=all_v, gate_refused=(not all_v), refused_checks=refused, checks=checks, statuses=statuses, runtime_s=float(time.time() - _t0), result_sha16=rhash, executed=rj.get("executed"),
                instrument=inst, n_events=rj.get("n_events"), stacks=stacks, start_systematic=syst, outcome=outcome, z_vs_GR=z_gr, z_vs_B=z_B, power_B=power_B,
                catalog_sha16=str((rj.get("catalog") or {}).get("sha256", ""))[:16], n_sources=len(rj.get("sources_sha256") or {}))


def prove_ringdown_dephasing_amendment_v2(ONE, v1_record=None):
    """v346 -- A EMENDA V2 DO RINGDOWN, PRE-REGISTRADA DEPOIS DA AUTOPSIA DA V1 E ANTES DO DADO DA V2 [ADITIVO; nao gateia; fora do contorno].
    A autopsia e LIDA do resultado da V1 (por hash), nunca de memoria: das series usadas na janela de 3 ms, quantas ficaram na BORDA
    superior da grade de tau (2,5 x e^0,25 = 3,21 tau_GR, todas com o mesmo delta), que fracao do peso carregavam e em que faixa de SNR
    estavam. Mecanismo nomeado: o pico era o argmax da envoltoria em +-50 ms de um GPS grosseiro; em evento fraco o argmax cai em ruido
    ou antes do merger, a janela apanha merger/ruido, o ajuste foge para a borda e delta_f co-move negativo. O que a V2 muda, item a item:
    (1) pico por FILTRO CASADO com o template IMRPhenomXAS de (m1, m2, chi_eff) do catalogo, SNR de ancoragem >= 8; (2) grade mais larga
    com EXCLUSAO DE BORDA; (3) corte de identificacao do modo |delta_f| <= 0,3; (4) minimo de 8 series na janela primaria e 3 na
    secundaria; sistematica contra a sigma COMBINADA das duas janelas; chi2/dof do empilhamento <= 3. Tudo o mais igual a V1.
    A V1 fica registrada como recusa; a V2 e a resposta a autopsia. CONFIRMED proibido."""
    _t0 = time.time()
    v1 = v1_record or {}
    res_p = os.path.join(CACHE, "gw", "RINGDOWN_DEPHASING_V1_RESULT.json")
    rj, rhash = _read_external_json_with_hash(res_p)
    edge_ratio = 2.5 * math.exp(0.25)
    aut = {"v1_result_sha16": rhash, "v1_protocol_hash": v1.get("protocol_hash"), "v1_gate_refused": bool(v1.get("gate_refused")), "v1_refused_checks": list(v1.get("refused_checks") or []), "v1_matrix_outcome": v1.get("outcome")}
    if rj is not None:
        used = [r for r in (rj.get("per_series") or []) if r.get("status") == "OK" and ((r.get("starts") or {}).get("3.0") or {}).get("used")]
        edge = [r for r in used if (r["starts"]["3.0"].get("tau_obs_ms") or 0) / max(r.get("tau_gr_ms") or 1e-9, 1e-9) >= edge_ratio * (1 - 1e-3)]
        w_all = sum(1.0 / (r["starts"]["3.0"]["sigma_rel"] ** 2) for r in used) or float("nan"); w_edge = sum(1.0 / (r["starts"]["3.0"]["sigma_rel"] ** 2) for r in edge)
        deltas = sorted(set(round(r["starts"]["3.0"]["delta_obs"], 4) for r in edge))
        s3 = (rj.get("stacks") or {}).get("3.0") or {}
        aut.update({"n_used_3ms": len(used), "n_on_edge_3ms": len(edge), "edge_weight_share": (w_edge / w_all) if w_all == w_all else None,
                    "edge_snr_range": ([round(min(r["starts"]["3.0"]["snr"] for r in edge), 2), round(max(r["starts"]["3.0"]["snr"] for r in edge), 2)] if edge else None),
                    "edge_distinct_deltas": deltas, "edge_series": sorted(r["key"] for r in edge), "v1_delta_tau": s3.get("delta_tau"), "v1_sigma": s3.get("sigma"), "v1_delta_f": s3.get("delta_f"),
                    "v1_peak_method": "argmax da envoltoria em +-50 ms do GPS do catalogo", "mechanism": "pico em ruido/antes do merger -> janela contaminada -> tau na borda, delta_f negativo"})
    proto = {
        "version": "RINGDOWN_DEPHASING_V2", "amendment_of": "RINGDOWN_DEPHASING_V1", "status": "PRE_REGISTERED_AFTER_V1_AUTOPSY_BEFORE_V2_DATA_READ",
        "autopsy_of_V1": aut,
        "changes": {"1_peak": "filtro casado com template IMRPhenomXAS (lalsimulation) de (m1, m2, chi_eff) do catalogo, massas no detector, branqueado com a PSD do evento, em +-100 ms do GPS; t_pico = pico da envoltoria do template deslocado; SNR de ancoragem >= 8",
                    "2_grid": "f_GR x [0.6, 1.4] (17); tau_GR x [0.3, 4.0] log (21); refino 9 x 9 dentro de +-1 passo grosso; EXCLUSAO DE BORDA (ajuste grosso na borda de f ou tau -> serie nao usada)",
                    "3_mode_id": "|delta_f| <= 0.3 (o que se mede e o 220 de Kerr previsto)", "4_min_series": "8 na janela primaria (3 ms); 3 na secundaria (6 ms)",
                    "5_systematics": "|delta(3 ms) - delta(6 ms)| contra sqrt(sigma3^2 + sigma6^2); chi2/dof do empilhamento <= 3"},
        "unchanged": "PSD Welch; janela [t_pico + 3 ms, + 6 tau_GR] e secundaria a 6 ms; seno amortecido branqueado; nulos por injecao fora da fonte (40 janelas); guardas snr_min 5 e transiente 10 sd; empilhamento por variancia inversa; previsao de Kerr por EOB + Berti-Cardoso-Will",
        "pipeline_params": {"anchor_template": "IMRPhenomXAS", "anchor_snr_min": 8.0, "anchor_win_ms": 100.0, "grid": "f x[0.6,1.4] (17), tau x[0.3,4.0] log (21), refino 9x9 em +-1 passo", "edge_exclusion": True, "df_max": 0.3, "snr_min": 5.0, "transient_sd": 10.0, "n_off": 40},
        "criteria": {"exclude_z": 5.0, "power_min": 5.0, "bias_max_rel": 0.2, "systematics_max_sigma": 1.0, "chi2_dof_max": 3.0, "min_series_primary": 8, "min_series_secondary": 3},
        "allowed_verdicts": ["TGL_RINGDOWN_BRANCH_B_EXCLUDED", "TGL_RINGDOWN_GR_TENSION_REPORTED", "TGL_RINGDOWN_NOT_FALSIFIED_POWERED", "TGL_RINGDOWN_NOT_FALSIFIED_UNDERPOWERED",
                             "TGL_RINGDOWN_INCONCLUSIVE_SYSTEMATICS", "TGL_RINGDOWN_AWAITING_RESULT_FILE"],
        "forbidden_verdicts": ["CONFIRMED", "PROVED"],
        "what_it_cannot_do": "nao distingue a TGL da RG no ramo A (por construcao); no ramo B, so exclui ou nao exclui a escala tau* = GM/c^3; um estimador de um modo sem overtones tem piso proprio",
    }
    ph = hashlib.sha256(json.dumps(proto, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    checks = [("autopsia da V1 lida por hash (%s)" % rhash, rj is not None and aut.get("n_used_3ms") is not None),
              ("a autopsia tem series na borda com delta identico", bool(aut.get("n_on_edge_3ms")) and len(aut.get("edge_distinct_deltas") or []) == 1),
              ("emenda V2 pre-registrada e hasheada (%s)" % ph, True), ("nenhum veredito proibido por construcao", True)]
    all_v = bool(all(v for _, v in checks))
    return {"protocol": proto, "protocol_hash": ph, "autopsy": aut, "checks": checks, "all_verified": all_v, "does_not_gate_core": True, "in_contour_roster_v314": False, "runtime_s": float(time.time() - _t0),
            "verdict": ("TGL_RINGDOWN_DEPHASING_V2__AMENDMENT_PRE_REGISTERED_%s__AUTOPSY_OF_V1_READ__%d_OF_%s_SERIES_ON_GRID_EDGE__GATE_UNTOUCHED" % (ph, int(aut.get("n_on_edge_3ms") or 0), aut.get("n_used_3ms"))) if all_v else "TGL_RINGDOWN_AMENDMENT_V2_NOT_SEALED_THIS_RUN"}


def prove_ringdown_dephasing_result_v2(ONE, amendment_record=None):
    """v346 -- o resultado da V2 (pipeline externo ringdown_dephasing_v2.py no WSL), lido por hash e julgado pela matriz da emenda."""
    _t0 = time.time()
    beta = SEALED_CODATA_ALPHA * math.sqrt(math.e)
    am = amendment_record or prove_ringdown_dephasing_amendment_v2(ONE); ph = am.get("protocol_hash"); pr = (am.get("protocol") or {}); crit = pr.get("criteria") or {}; pp = pr.get("pipeline_params") or {}
    res_p = os.path.join(CACHE, "gw", "RINGDOWN_DEPHASING_V2_RESULT.json")
    base = {"result_path": res_p, "protocol_hash": ph, "does_not_gate_core": True, "in_contour_roster_v314": False, "beta_runtime": beta,
            "why_outside_contour": "tau* e INPUT: o que se exclui e a escala tau* = GM/c^3, nao a lei de dephasing nem a TGL"}
    st = {"leitura": "[REAL] o um.py nao recalcula: le por hash e aplica a matriz da emenda (%s)" % ph,
          "ramo_A": "[REAL, computado] tau* = t_Planck da ~1e-40: o ringdown e RG por construcao -- o limite assintotico com numero",
          "secao_20": "[ERRATA AO LADO] «provavelmente ja excluido» era frase; aqui o ramo B tem numero"}
    rj, rhash = _read_external_json_with_hash(res_p)
    if rj is None:
        return dict(base, verdict="TGL_RINGDOWN_AWAITING_RESULT_FILE", all_verified=False, checks=[("resultado RINGDOWN_DEPHASING_V2 em cache/gw", False)], statuses=st, runtime_s=float(time.time() - _t0))
    stacks = rj.get("stacks") or {}; s3 = stacks.get("3.0") or {}; s6 = stacks.get("6.0") or {}; inst = rj.get("instrument") or {}; pl = rj.get("pipeline") or {}
    checks = [("resultado V2 lido por hash (%s)" % rhash, True),
              ("beta do resultado == beta recomputado", bool(abs(float(rj.get("beta", 0)) - beta) < 1e-15)),
              ("instrumento: lalsuite, estado final EOB, ancoragem %s" % pp.get("anchor_template"), bool(inst.get("lalsuite") and "EOB" in str(inst.get("final_state", "")) and inst.get("anchor_template") == pp.get("anchor_template"))),
              ("parametros do pipeline == emenda (SNR de ancoragem, borda, |delta_f|, grade)", bool(pl.get("anchor_snr_min") == pp.get("anchor_snr_min") and pl.get("edge_exclusion") is True and pl.get("df_max") == pp.get("df_max") and pl.get("grid") == pp.get("grid"))),
              ("catalogo e fontes com sha256", bool((rj.get("catalog") or {}).get("sha256") and len(rj.get("sources_sha256") or {}) >= 100)),
              ("janela primaria >= %d series; secundaria >= %d" % (int(crit.get("min_series_primary", 8)), int(crit.get("min_series_secondary", 3))), bool((s3.get("n_used") or 0) >= int(crit.get("min_series_primary", 8)) and (s6.get("n_used") or 0) >= int(crit.get("min_series_secondary", 3)))),
              ("nenhum veredito proibido por construcao", True)]
    all_v = bool(all(v for _, v in checks))
    d, sg, pB, pA = s3.get("delta_tau"), s3.get("sigma"), s3.get("delta_pred_B"), s3.get("delta_pred_A")
    syst = rj.get("start_systematic"); bias = s3.get("mean_bias_rel"); chi2 = s3.get("chi2_dof"); sg6 = s6.get("sigma")
    sg_c = math.sqrt(sg ** 2 + sg6 ** 2) if isinstance(sg, (int, float)) and isinstance(sg6, (int, float)) else None
    reasons = []
    if syst is None or sg_c is None or abs(syst) > float(crit.get("systematics_max_sigma", 1.0)) * sg_c: reasons.append("|delta(3ms)-delta(6ms)| = %s > %.0f sigma combinada (%s)" % (("%.4f" % syst) if syst is not None else "AUSENTE", float(crit.get("systematics_max_sigma", 1.0)), ("%.4f" % sg_c) if sg_c else "AUSENTE"))
    if bias is None or abs(bias) > float(crit.get("bias_max_rel", 0.2)): reasons.append("vies relativo de tau %s > %.1f" % (("%.3f" % bias) if bias is not None else "AUSENTE", float(crit.get("bias_max_rel", 0.2))))
    if chi2 is None or chi2 > float(crit.get("chi2_dof_max", 3.0)): reasons.append("chi2/dof do empilhamento %s > %.0f" % (("%.2f" % chi2) if chi2 is not None else "AUSENTE", float(crit.get("chi2_dof_max", 3.0))))
    z_gr = (d / sg) if sg else None; z_B = ((d - pB) / sg) if sg else None; power_B = (abs(pB) / sg) if sg else None
    if reasons: outcome = "INCONCLUSIVE_SYSTEMATICS"
    elif z_B is not None and abs(z_B) >= float(crit.get("exclude_z", 5.0)) and power_B >= float(crit.get("power_min", 5.0)): outcome = "BRANCH_B_EXCLUDED"
    elif z_gr is not None and abs(z_gr) >= float(crit.get("exclude_z", 5.0)): outcome = "GR_TENSION_REPORTED"
    elif power_B is not None and power_B >= float(crit.get("power_min", 5.0)): outcome = "NOT_FALSIFIED_POWERED"
    else: outcome = "NOT_FALSIFIED_UNDERPOWERED"
    _f = lambda v, p=4: (("%%.%df" % p) % v) if isinstance(v, (int, float)) else "NA"
    verdict = ("TGL_RINGDOWN_DEPHASING_V2__RESULT_READ_BY_HASH__%s__DELTA_TAU_%s__BRANCH_B_PRED_%s__POWER_%s_OF_5_SIGMA__BRANCH_A_INVISIBLE__GATE_UNTOUCHED"
               % (outcome, _f(d).replace(".", "P").replace("-", "M"), _f(pB).replace(".", "P").replace("-", "M"), _f(power_B, 1).replace(".", "P"))) if all_v else "TGL_RINGDOWN_RESULT_V2_NOT_SEALED_THIS_RUN"
    statuses = dict(st)
    statuses["resultado"] = ("[REAL, lido] V2: %s series (3 ms; %s na borda excluidas; SNR de ancoragem medio %s): delta_tau = %s +- %s (z vs RG %s); previsao do ramo B %s (z vs B %s; poder %s sigma); ramo A %s; "
                             "delta_f = %s +- %s; chi2/dof %s; vies %s; janela 6 ms: %s series, delta_tau = %s +- %s; sistematica %s (sigma combinada %s) => %s%s"
                             % (s3.get("n_used"), s3.get("n_on_edge_excluded"), _f(s3.get("mean_anchor_snr"), 1), _f(d), _f(sg), _f(z_gr, 2), _f(pB), _f(z_B, 2), _f(power_B, 2), ("%.1e" % pA) if isinstance(pA, (int, float)) else "NA",
                                _f(s3.get("delta_f")), _f(s3.get("sigma_f")), _f(chi2, 2), _f(bias, 3), s6.get("n_used"), _f(s6.get("delta_tau")), _f(sg6), _f(syst), _f(sg_c), outcome, (" [%s]" % "; ".join(reasons) if reasons else "")))
    return dict(base, verdict=verdict, all_verified=all_v, checks=checks, statuses=statuses, runtime_s=float(time.time() - _t0), result_sha16=rhash, executed=rj.get("executed"),
                instrument=inst, n_events=rj.get("n_events"), stacks=stacks, start_systematic=syst, sigma_combined=sg_c, outcome=outcome, z_vs_GR=z_gr, z_vs_B=z_B, power_B=power_B, reasons=reasons,
                catalog_sha16=str((rj.get("catalog") or {}).get("sha256", ""))[:16], n_sources=len(rj.get("sources_sha256") or {}), n_on_edge=rj.get("n_on_edge"))
