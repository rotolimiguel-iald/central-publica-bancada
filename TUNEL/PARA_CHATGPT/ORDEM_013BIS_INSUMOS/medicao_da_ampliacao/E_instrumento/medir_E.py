"""Frente E (ORDEM 013-bis): instrumento, custo e reaproveitamento - medicao por script.
So leitura na bancada; escreve apenas nesta pasta. beta em runtime, nunca literal.
"""
import os, sys, json, math, hashlib, subprocess, time, datetime, re
ROOT = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
OUT = os.path.dirname(os.path.abspath(__file__))
SCR = OUT  # gwosc_*.json vivem nesta pasta (frente E)
CASA_LOG = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\eco_ancorado_v1\echo_pe_v2_full.log"
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)


def sha16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def J(p):
    return json.load(open(p, 'rb'))


R = {"date_utc": datetime.datetime.utcnow().isoformat() + "Z", "beta_runtime": beta, "fontes": {}}


def src(rel):
    p = os.path.join(ROOT, rel) if not os.path.isabs(rel) else rel
    R["fontes"][rel] = sha16(p)
    return p


# ---------- (3) jobs vivos ----------
st = J(src("STATUS_ORDEM_013.json"))
jobs = []
cmd = "ps -eo pid,ppid,etime,pcpu,rss,args | grep -E 'run_|audit' | grep -v grep; echo ==; free -m | head -2; nproc; cat /proc/loadavg"
try:
    ps = subprocess.run(["wsl.exe", "-d", "Ubuntu-24.04", "-e", "bash", "-lc", cmd], capture_output=True, text=True,
                        timeout=90, env=dict(os.environ, MSYS_NO_PATHCONV="1")).stdout
except Exception as e:
    ps = "ERR " + str(e)
R["ps_snapshot"] = ps
groups = {}
for line in ps.splitlines():
    parts = line.split()
    if len(parts) >= 7 and parts[0].isdigit():
        pid, ppid, et, cpu, rss = parts[:5]
        args = " ".join(parts[6:])
        g = groups.setdefault(args, {"n": 0, "rss_mb": 0.0, "pids": [], "etime": et})
        g["n"] += 1
        g["rss_mb"] += int(rss) / 1024.0
        g["pids"].append(int(pid))
R["ps_groups"] = {k: {"processos": v["n"], "rss_GB": round(v["rss_mb"] / 1024, 2), "etime_exemplo": v["etime"]} for k, v in groups.items()}
R["rss_total_GB"] = round(sum(v["rss_mb"] for v in groups.values()) / 1024, 2)
now = time.time()
for ap in st["active_processes"]:
    folder = os.path.join(ROOT, ap["folder"].replace("\\", os.sep))
    prog = os.path.join(folder, "PROGRESS.json")
    rec = {"session_id": ap["session_id"], "kind": ap["kind"], "workers": ap["workers"], "folder": ap["folder"]}
    if os.path.exists(prog) and ap["kind"] != "rate_audit":
        pg = J(prog)
        done = pg.get("done", pg.get("completed"))
        tot = pg.get("valid_draws")
        sec = pg.get("seconds")
        rate = done / sec if sec else None
        rec.update(done=done, total=tot, seconds=sec, rate_per_s=rate, frac=round(done / tot, 4) if tot else None,
                   eta_h=round((tot - done) / rate / 3600, 2) if rate else None, progress_utc=pg.get("date_utc"),
                   progress_age_min=round((now - os.path.getmtime(prog)) / 60, 1))
        fam = "SEOBNRv4HM" if "SEOBNRv4HM" in ap["folder"] else "IMRPhenomXPHM"
        if ap["kind"] == "continuous_source":
            rec["vivo_em_ps"] = any(("run_continuous_source_curves" in k and fam in k) for k in groups)
        else:
            rec["vivo_em_ps"] = any("run_real_phase_importance" in k for k in groups)
    if ap["kind"] == "rate_audit":
        ar = os.path.join(folder, "AUDIT_RATE.json")
        rec["AUDIT_RATE_json_exists"] = os.path.exists(ar)
        if os.path.exists(ar):
            a = J(ar)
            rec.update(audit_status=a.get("status"), rate_control_pass=a.get("rate_control_pass"),
                       rate_checks=len(a.get("rate_checks", [])), max_active_rate_difference=a.get("max_active_rate_difference"),
                       audit_mtime_utc=datetime.datetime.utcfromtimestamp(os.path.getmtime(ar)).isoformat() + "Z",
                       passed_precision=a.get("passed_precision"), draws=a.get("draws"), inside=a.get("inside"))
        rec["vivo_em_ps"] = any("audit" in k for k in groups)
    jobs.append(rec)
R["jobs"] = jobs
seob = J(src("C5_SEOB_REPEAT_AND_MIXTURE.json"))
R["C5_SEOB_REPEAT_AND_MIXTURE"] = {"status": seob["status"],
                                  "seob": {k: seob["seob"][k] for k in ("draws", "evaluations", "datasets", "passing_precision", "failing_precision", "ESS_range", "density_status")},
                                  "mixture": {k: seob["mixture"][k] for k in ("status", "datasets", "passing_both_and_mixture_MC", "full_cells_passing", "cells", "scientific_acceptance")}}
ce = J(src("C5_CONTINUOUS_ENDPOINTS_BOTH_RUNNING.json"))
R["resource_observation_bancada"] = ce["resource_observation"]
R["continuous_registrations"] = []
for f in ["cache/source_evidence/continuous_source_curves/SEOBNRv4HM_seed130942_N16384/REGISTRATION.json",
          "cache/source_evidence/continuous_source_curves/IMRPhenomXPHM_seed130972_N32768/REGISTRATION.json"]:
    g = J(src(f))
    R["continuous_registrations"].append({k: g[k] for k in ("family", "draws", "inside_draws", "targets", "strengths", "reading", "waveform_hz", "scientific_acceptance")})

# ---------- (1) instrumento (sondado so leitura, 22/09/2026 ~14:05Z) ----------
R["instrumento"] = {
    "pycbc_env": {"python": "3.12.3", "pycbc": "2.11.0", "lalsimulation": "6.2.1", "lal": "7.7.1", "numpy": "2.3.5", "scipy": "1.16.3", "h5py": "3.16.0",
                  "bilby": "AUSENTE", "dynesty": "AUSENTE", "pyseobnr": "AUSENTE", "pyRing": "AUSENTE", "gwpy": "AUSENTE", "qnm": "AUSENTE"},
    "lal_env": {"python": "3.12.3", "lalsimulation": "6.2.1", "bilby": "2.8.2", "dynesty": "3.1.0", "gwpy": "4.0.2", "gwosc": "0.8.3", "emcee": "3.1.6",
                "numpy": "2.5.3", "scipy": "1.18.1", "pycbc": "AUSENTE", "pyseobnr": "AUSENTE", "pyRing": "AUSENTE", "qnm": "AUSENTE"},
    "vendor_no_cache": {"cache/vendor": ["qnm-0.4.4", "numba-0.67.0", "llvmlite-0.49.0", "numpy-2.5.3", "scipy-1.18.1", "tqdm-4.70.1"],
                        "cache/pyring_oracle/vendor": ["pyringgw-2.7.0 (fonte; so o AST aritmetico e executado, cf. pyring_readout.py)", "Cython-3.0.12"]},
    "pypi_read_only": {"pyseobnr": "0.3.7 disponivel", "pyRing": "0.0.12 disponivel", "dynesty": "3.1.0"},
    "aproximantes_lalsimulation_6.2.1_ok_t_onda_s": {"IMRPhenomXPHM": 0.033, "IMRPhenomXAS": 0.007, "SEOBNRv4HM_PA": 0.131, "SEOBNRv4HM": 0.592, "pSEOBNRv4HM_PA": 0.095, "SEOBNRv4PHM": 1.686},
    "aproximantes_falham_sem_LAL_DATA_PATH": ["NRSur7dq4", "SEOBNRv5HM_ROM", "SEOBNRv5_ROM"],
    "pSEOBNRv4HM_PA_deformacao_pos_pico": {"DTau220": True, "DOmega220": True, "DTau440": True,
                                            "teste_dtau220": {"razao_taxa_dtau_-0.02": 1.0208, "esperado": round(1 / 0.98, 4), "razao_taxa_dtau_+0.5": 0.6128, "esperado_+0.5": round(1 / 1.5, 4),
                                                              "escopo": "ajuste da envoltoria 10-30 t_M apos o pico, 39+33 Msun, 8192 Hz; 440/overtones contaminam o ajuste em +0.5"},
                                            "cronometro_s": {"dtau=0": 0.0975, "dtau=-0.02": 0.1136, "dtau=+0.5": 0.1158}},
    "cpu": 48, "mem_total_GB": 125, "mem_used_GB_snapshot": 73,
    "disco": {"C:": "3.7T total, 1.2T livre (69% usado)", "WSL /": "1007G, 953G livre"},
    "medicao": "[REAL - sondado so leitura; cronometros com nice 19, 1 thread; 18 workers da bancada ocupados ao mesmo tempo]",
}

# ---------- (4) reaproveitavel ----------
reuse = [
    ("tgl_ringdown_prediction.py", "modulo de predicao por evento: (M_det, chi, leitura) -> Gamma, delta_tau=-x/(1+x), delta_f=0; beta em runtime; QNM exato via QNM_GRID; perfil LEGACY_V346 reproduz o rito v346 a 1e-16"),
    ("tgl_ringdown_template.py", "seno amortecido 220 (+ modos com QNM exato) com parametro deformation (0=RG,1=leitura); convencao LVK eq.1; consumivel pelo bilby.WaveformGenerator (C3_BILBY_CONSUMER PASS)"),
    ("tgl_ringdown_likelihood.py", "verossimilhanca gaussiana de intervalo finito com amplitudes lineares marginalizadas/perfiladas (base branqueada)"),
    ("tgl_ringdown_unravelings.py", "desenrolamentos opcionais (Cauchy, campo raiz-coerente finito) - API numpy"),
    ("c6_engine.py", "motor da C6: janela pos-pico, Toeplitz, 220+440 Kerr exatos, M/chi marginalizados, guarda por hash do registro"),
    ("run_c6_grid.py", "runner dos inicios/refinos da C6 (grade 6..12 t_M) - ~122 s para 75 linhas"),
    ("fetch_c6_strain.py", "baixa strain GWOSC so apos conferir o hash do registro (fail-closed)"),
    ("fetch_public.py", "download Zenodo com hash + atomic_json"),
    ("prepare_empirical_noise.py", "PSD off-source + verossimilhanca causal de intervalo finito (treino 2048 s, hold-out 2048 s)"),
    ("prepare_recolored_noise.py", "recoloracao dos residuos O4 para O5/ET/CE (quociente de intervalo finito)"),
    ("prepare_imr_controls.py", "gera controles IMR SEOBNRv4HM e IMRPhenomXPHM via PyCBC + remanescente (SimIMREOBFinalMassSpin / PhenomX / UIB2016)"),
    ("empirical_imr_recovery.py", "injecao-recuperacao C5 em dados hold-out H1/L1, duas familias, remanescente fixo (calibracao por injecao)"),
    ("calibrate_imr_recovery.py", "recuperacao da forma IMR completa (adequacao de forma de onda, duas familias)"),
    ("coherent_imr_model.py", "modelo IMR alinhado com polarizacoes coerentes em rede (sem amplitudes livres por detector/harmonico)"),
    ("coherent_imr_likelihood.py", "integral exata distancia/polarizacao sobre o modelo coerente"),
    ("nonlinear_coherent_recovery.py", "controle construtivo de degenerescencia: acha fontes RG que imitam IMR desfasado"),
    ("fisher_forecast.py", "Fisher local (PSD de referencia): z por leitura/SNR/cenario; checa nao-identificabilidade 220 com M,chi livres"),
    ("forecast_recolored_imr.py", "distribuicoes de ln B com ruido recolorido (O5/ET/CE), duas familias, 6 SNR, 3 modelos de recuperacao"),
    ("trajectory_recovery.py", "C2: distribuicoes de realizacao unica (tremor de delta_f) com/sem ruido colorido sintetico"),
    ("catalog_220_readout.py", "extrator de posteriores pSEOB GWTC-5.0 (33 eventos): densidade em (df220, dtau220) na curva g(spin)"),
    ("posterior_220_readout.py", "leitura 220 do GW250114 com setor 440 livre (identidade de densidade, Jacobiano 1)"),
    ("gwtc3_posterior_readout.py", "extrator GWTC-3 pSEOB220 (18 produtos) + reconciliacao por GPS entre releases"),
    ("combine_catalog.py", "combinacao hierarquica (deformacao comum) por importance sampling de KDEs - 31/33 eventos"),
    ("combine_gwtc3.py", "combinacao GWTC-3 (18 e 10 eventos) - controle separado"),
    ("free_clock_posterior.py", "relogio livre tau in [t_P, t_M] integrado com pesos KDE - 220 so"),
    ("joint_modes_posterior.py", "evidencia conjunta 220+440 do GW250114 (4 coordenadas de deformacao)"),
    ("pyring_readout.py", "robustez com posterior TEOB do pyRing (remanescente por AST do pyRingGW 2.7.0)"),
    ("verify_bilby_consumer.py", "prova de consumo do template pelo Bilby 2.8.2"),
    ("build_native_waveform_package.py", "empacota C7_NATIVE_SEOB_WAVEFORM (SEOB41 completo com 22/44 pos-pico deformados)"),
    ("C7_NATIVE_SEOB_WAVEFORM/tgl_native_ringdown.py", "API: prepare_ringdown(coords,times)+polarizations(reading,strength,distance,psi) - IMR SEOBNRv4HM nativo com h_a = h_all + (e^{-a*G220*t}-1)h22 + (e^{-a*G440*t}-1)h44; 8192 Hz"),
    ("C7_NATIVE_SEOB_WAVEFORM/native_seob_phase_source.py", "fonte de fase nativa SEOB (copia byte-identica)"),
    ("C7_NATIVE_SEOB_WAVEFORM/stable_peak_imr_model.py", "modelo IMR de pico estavel (copia byte-identica)"),
    ("C7_NATIVE_SEOB_WAVEFORM/direct_seob_modes.py", "modos SEOB diretos via LAL (corpos verbatim AST)"),
    ("cache/source_evidence/run_real_phase_importance.py", "integrador de fonte por importancia (proposals congeladas) - o que roda hoje (34860)"),
    ("cache/source_evidence/run_continuous_source_curves.py", "curvas logZ(a) em 17 forcas a in[-4,4] para 1200 mocks - o que roda hoje (19681, 43367)"),
    ("cache/source_evidence/combine_continuous_source_curves.py", "mistura das familias (so com curvas COMPLETAS) - registrado, nao iniciado"),
    ("cache/source_evidence/audit_phase_source.py", "auditoria aritmetica/taxa independente do piloto de fase"),
    ("QNM_GRID.json", "grade QNM exata (qnm 0.4.4) 220/440/221"),
    ("C4_CATALOG_220.json", "33 posteriores pSEOB GWTC-5.0 lidos (quantis, densidades) - insumo direto da combinacao"),
    ("C4_GWTC3_220.json", "18 produtos pSEOB GWTC-3 lidos"),
    ("C7_GWTC3_EVENT_READINGS.csv", "predicoes por evento x leitura (GWTC-3)"),
    ("C5_IMR_CONTROLS.json", "versoes pycbc 2.11.0 / lalsimulation 6.2.1 e controles IMR hasheados"),
]
R["reaproveitavel"] = []
for rel, desc in reuse:
    p = os.path.join(ROOT, rel)
    R["reaproveitavel"].append({"arquivo": rel, "sha16": sha16(p) if os.path.exists(p) else "NAO ENCONTRADO", "faz": desc})
R["C3_BILBY_CONSUMER"] = J(src("C3_BILBY_CONSUMER.json"))
R["C7_NATIVE_SEOB"] = {"package": J(src("C7_NATIVE_SEOB_WAVEFORM_PACKAGE.json")), "replay": J(src("C7_NATIVE_SEOB_REPLAY_VALIDATION.json"))}
imrc = J(src("C5_IMR_CONTROLS.json"))
R["C5_IMR_CONTROLS"] = {k: imrc[k] for k in ("status", "pycbc_version", "lalsimulation_version", "parameters")}
R["C5_IMR_CONTROLS"]["families"] = [{k: f[k] for k in ("family", "remnant_mass_detector_solar", "remnant_spin", "remnant_method")} for f in imrc["families"]]

# ---------- (5) armazenamento ----------
tot = 0; n = 0; cache = 0; ncache = 0; big = []
LP = "\\\\?\\" + ROOT
for dp, dn, fn in os.walk(LP):
    for f in fn:
        p = os.path.join(dp, f)
        try:
            s = os.path.getsize(p)
        except OSError:
            continue
        tot += s; n += 1
        rel = os.path.relpath(p, LP)
        if rel.startswith("cache" + os.sep):
            cache += s; ncache += 1
        elif s > 25 * 1024 * 1024:
            big.append((s, rel))
A = {"total_bytes": tot, "total_GB": round(tot / 1e9, 3), "arquivos": n, "cache_bytes": cache, "cache_GB": round(cache / 1e9, 3), "cache_arquivos": ncache,
     "fora_do_cache_maiores_25MB": len(big), "fora_do_cache_maiores_25MB_GB": round(sum(s for s, _ in big) / 1e9, 3), "onde_estao": {}, "zips_C7_bytes": {}}
for s, rel in big:
    top = rel.split(os.sep)[0]
    A["onde_estao"][top] = A["onde_estao"].get(top, 0) + 1
for z in os.listdir(os.path.join(ROOT, "cache")):
    if z.endswith(".zip"):
        A["zips_C7_bytes"][z] = os.path.getsize(os.path.join(ROOT, "cache", z))
c6d = J(src("C6_DOWNLOADS.json"))
strain_bytes = sum(f["bytes"] for f in c6d["files"])
A["strain_on_source_GW250114_bytes_2det_4kHz_4096s"] = strain_bytes
# tamanho dos produtos dos jobs (chunks ja gravados)
def dsize(rel):
    t = 0
    for dp, dn, fn in os.walk("\\\\?\\" + os.path.join(ROOT, rel).replace("/", "\\")):
        for f in fn:
            try: t += os.path.getsize(os.path.join(dp, f))
            except OSError: pass
    return t
A["source_evidence_GB"] = round(dsize("cache/source_evidence") / 1e9, 3)
A["continuous_source_curves_GB_parcial"] = round(dsize("cache/source_evidence/continuous_source_curves") / 1e9, 3)
A["cache_public_GB"] = round(dsize("cache/public") / 1e9, 3)
R["armazenamento"] = A

# ---------- (2)+(tabela) custo e 5 sigma ----------
fis = J(src("C5_FISHER.json")); fe = J(src("C5_FISHER_EMPIRICAL.json"))
z40 = {}
for r in fis["records"]:
    if r["psd"] == "O4" and r["scenario"] == "MASS_SPIN_FIXED_OPTIMISTIC" and abs(r["snr_ringdown"] - 40) < 1e-9:
        z40[r["reading"]] = {"delta": r["delta_exact"], "sigma": r["sigma_delta_local"], "z": r["z_local"], "N_identicos_5sigma_bancada": r["identical_independent_events_for_median_5sigma"]}
R["fisher_O4_SNR40_fonte_fixa"] = z40
R["fisher_same_source_R_B"] = fis["same_source_R_B"]
R["fisher_mass_spin_free"] = fis["mass_spin_free"]["status"]
R["fisher_empirical_R_B_SNR40"] = fe["same_source_R_B"]
R["fisher_snr_grid"] = sorted({r["snr_ringdown"] for r in fis["records"]})
raw = J(os.path.join(SCR, "gwosc_catalogs_raw.json")); R["fontes"]["scratch/gwosc_catalogs_raw.json"] = sha16(os.path.join(SCR, "gwosc_catalogs_raw.json"))
sf = J(os.path.join(SCR, "gwosc_strain_files_snr12.json")); R["fontes"]["scratch/gwosc_strain_files_snr12.json"] = sha16(os.path.join(SCR, "gwosc_strain_files_snr12.json"))
cat = {}
for c, rows in raw.items():
    s = [r[2] for r in rows if r[2]]
    cat[c] = {"n": len(rows), "snr>=8": sum(1 for x in s if x >= 8), "snr>=12": sum(1 for x in s if x >= 12), "snr>=15": sum(1 for x in s if x >= 15),
              "snr>=20": sum(1 for x in s if x >= 20), "snr>=30": sum(1 for x in s if x >= 30), "max": max(s) if s else None}
R["gwosc_catalogos"] = cat
R["gwosc_strain_publico_snr12_gwtc5"] = {"eventos": len(sf), "com_strain_files": sum(1 for o in sf if o.get("n_files", 0) > 0),
                                          "HL_ou_HLV": sum(1 for o in sf if 'H1' in o.get('detectors', []) and 'L1' in o.get('detectors', [])),
                                          "Mf>=40": sum(1 for o in sf if (o.get("mf") or 0) >= 40)}
frac_gw250114 = 40.0 / 78.6
rows = [o for o in sf if o.get("snr")]


def pop(zr, frac, mf_min=0.0):
    sel = [o for o in rows if (o.get("mf") or 0) >= mf_min]
    S = sum((frac * o["snr"] / 40.0) ** 2 for o in sel)
    return {"z_pop": round(zr * math.sqrt(S), 3), "soma_(SNR_RD/40)^2": round(S, 3), "n_eventos": len(sel),
            "eventos_SNR_RD40_equivalentes_faltando_para_5sigma": max(0.0, round((5.0 / zr) ** 2 - S, 1))}


tab = []
for rd, v in z40.items():
    if v["z"] < 1e-6:
        continue
    tab.append({"leitura": rd, "z_SNR40_O4_fonte_fixa": round(v["z"], 3), "sigma": round(v["sigma"], 4), "delta": round(v["delta"], 4),
                "N_identicos_SNR_RD40_5sigma": math.ceil((5.0 / v["z"]) ** 2), "SNR_RD_unico_evento_5sigma": round(40 * 5.0 / v["z"], 0),
                "GWTC5_snr>=12_45ev_frac_RD=0.509": pop(v["z"], frac_gw250114), "GWTC5_45ev_frac_RD=1.0_teto": pop(v["z"], 1.0),
                "GWTC5_Mf>=40_frac_0.509": pop(v["z"], frac_gw250114, 40.0)})
R["tabela_5sigma_escala_linear"] = {"hipotese": "z_i = z40*(SNR_RD,i/40), fonte fixa (M,chi fixos; otimista; NON_IDENTIFIABLE se livres); SNR_RD = 0.509*SNR_rede (fracao lida do GW250114: 40/78.6); soma em quadratura; sem sistematica de familia; [DERIVED]", "linhas": tab}
R["cenarios_mesma_fonte_R_B"] = [{"psd": s["psd"], "z": round(s["z_local"], 3), "N_identicos_5sigma": math.ceil((5 / s["z_local"]) ** 2)} for s in fis["same_source_R_B"]]
# custo medido na casa (log v347)
R["fontes"]["casa/echo_pe_v2_full.log"] = sha16(CASA_LOG)
log = open(CASA_LOG, encoding="utf-8", errors="replace").read()
secs = [int(m.group(1)) for m in re.finditer(r"\s(\d+)s OK", log)]
total = re.findall(r"\|\s*(\d+)s\s*$", log, re.M)
R["custo_medido_v347"] = {"corridas_OK": len(secs), "s_por_corrida_min": min(secs) if secs else None, "s_por_corrida_max": max(secs) if secs else None,
                          "s_por_corrida_mediana": sorted(secs)[len(secs) // 2] if secs else None, "rodada_total_s": total[-1] if total else None,
                          "config": "bilby+dynesty nlive 300, IMRPhenomD, amplitude marginalizada analiticamente, pool 40 a 1 thread BLAS; ringdown-eco, poucas dimensoes [REAL - log]"}
# custo PE IMR por evento (estimativa)
tw = {"pSEOBNRv4HM_PA": 0.0975, "IMRPhenomXPHM": 0.033, "SEOBNRv4HM_PA": 0.131, "SEOBNRv4HM": 0.592}
lo, hi = 3e6, 2e7
custo = []
for appr, t in tw.items():
    custo.append({"aproximante": appr, "t_onda_s": t, "cpu_h_por_evento": [round(lo * t / 3600), round(hi * t / 3600)],
                  "wall_h_22workers": [round(lo * t / 3600 / 22, 1), round(hi * t / 3600 / 22, 1)], "wall_h_28workers": [round(lo * t / 3600 / 28, 1), round(hi * t / 3600 / 28, 1)]})
R["custo_PE_IMR_por_evento"] = {"escopo": "[DERIVED] t_onda medido [REAL] x n de avaliacoes da verossimilhanca [KNOWN ordem de grandeza, 3e6-2e7 p/ dynesty nlive~1000, ~15 D, sem ROQ]; ignora overhead de FFT/verossimilhanca (+30-100%)", "linhas": custo}
amp = []
for N in (10, 31, 45):
    for mode, cpu_h in (("PE IMR pSEOBNRv4HM_PA", (lo * 0.0975 / 3600, hi * 0.0975 / 3600)), ("PE IMR IMRPhenomXPHM", (lo * 0.033 / 3600, hi * 0.033 / 3600)),
                        ("ringdown-only C6-like (prior inspiral externo; 122 s/75 linhas)", (0.03, 0.2)), ("v347-like (nlive 300, amplitude analitica; mediana/max do log por corrida)", (R["custo_medido_v347"]["s_por_corrida_mediana"] / 3600, R["custo_medido_v347"]["s_por_corrida_max"] / 3600))):
        amp.append({"N": N, "rota": mode, "cpu_h_total": [round(N * cpu_h[0]), round(N * cpu_h[1])], "wall_h_22w": [round(N * cpu_h[0] / 22, 1), round(N * cpu_h[1] / 22, 1)],
                    "strain_GB_4kHz": round(N * strain_bytes / 1e9, 2), "strain_GB_16kHz": round(N * strain_bytes * 4 / 1e9, 2), "saida_PE_GB_est_0.2-1_por_evento_KNOWN": [round(0.2 * N, 1), N]})
R["ampliacao_custo_por_N"] = amp
json.dump(R, open(os.path.join(OUT, "MEDICAO_E.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)
keys = ("jobs", "ps_groups", "rss_total_GB", "armazenamento", "fisher_O4_SNR40_fonte_fixa", "cenarios_mesma_fonte_R_B", "gwosc_catalogos",
        "gwosc_strain_publico_snr12_gwtc5", "tabela_5sigma_escala_linear", "custo_medido_v347", "custo_PE_IMR_por_evento", "ampliacao_custo_por_N")
print(json.dumps({k: R[k] for k in keys}, indent=1, ensure_ascii=False, default=str))
print("REAPROVEITAVEL:")
for r in R["reaproveitavel"]:
    print(" ", r["sha16"], r["arquivo"], "|", r["faz"])
print("FONTES:")
for k, v in R["fontes"].items():
    print(" ", v, k)
print("beta_runtime", beta)
print("MEDICAO_E.json sha16", sha16(os.path.join(OUT, "MEDICAO_E.json")))
