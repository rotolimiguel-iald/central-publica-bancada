# -*- coding: utf-8 -*-
"""Reconciliacao entre as cinco frentes (A..E) para o portao do poder da ampliacao.
Le os JSON das frentes (so leitura), calcula beta em runtime, sha16 de cada fonte
e as contas que resolvem (ou deixam abertas) as contradicoes entre frentes.
Nao toca a pasta da bancada. Calculos leves (numpy)."""
import hashlib, json, math, os, sys
import numpy as np

ROOT = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\ordem013\bis\medir"
OUT = os.path.join(ROOT, "S_sintese")
os.makedirs(OUT, exist_ok=True)

ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)

def sha16(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()[:16]

fontes = {
    "A": os.path.join(ROOT, "A_poder_eventos", "A_poder_eventos.json"),
    "A_csv": os.path.join(ROOT, "A_poder_eventos", "A1_por_evento.csv"),
    "B": os.path.join(ROOT, "B_catalogos", "RENDIMENTO_E_5SIGMA.json"),
    "B_N5": os.path.join(ROOT, "B_catalogos", "N5SIGMA_FROM_CATALOG.json"),
    "C": os.path.join(ROOT, "C_piso_sistematico", "C_piso_medicoes.json"),
    "C_cat": os.path.join(ROOT, "C_piso_sistematico", "C_piso_sinais_catalogo.json"),
    "D": os.path.join(ROOT, "D_realizacao_unica", "D_consolidado.json"),
    "D2": os.path.join(ROOT, "D_realizacao_unica", "d2_resultado.json"),
    "E": os.path.join(ROOT, "E_instrumento", "MEDICAO_E.json"),
}
hashes = {k: (sha16(p) if os.path.exists(p) else "NAO ENCONTRADO") for k, p in fontes.items()}

res = {"beta_runtime": beta, "sha16_fontes": {k: [fontes[k], hashes[k]] for k in fontes}}

# ---- 1. Leitura direta dos z_comb da frente A (conferencia) ----
A = json.load(open(fontes["A"], encoding="utf-8"))
res["A_keys_top"] = list(A.keys())[:40]

# ---- 2. Leis de escala compartilhadas ----
# z_i por evento GW250114-like (frente A), por leitura
z_gw = {"R-B": 0.343, "R-MOD": 0.637, "R-RAIZ-0": 0.641, "R-LIN": 1.237}
# z_comb sel31 offset=0 (frente A)
z31 = {"R-B": 0.606, "R-MOD": 1.076, "R-RAIZ-0": 1.120, "R-LIN": 2.159}
z39 = {"R-B": 0.654, "R-MOD": 1.167, "R-RAIZ-0": 1.205, "R-LIN": 2.322}
# Fisher da bancada, fonte fixa SNR_RD 40 (C5_FISHER, lido pelas frentes C/E)
z_f40 = {"R-B": 0.408, "R-MOD": 0.764, "R-RAIZ-0": 0.775, "R-LIN": 1.551}

N5 = lambda z: 25.0 / z**2

tab = {}
for L in z_gw:
    tab[L] = {
        "N5_GW250114_like_O4": N5(z_gw[L]),                 # frente A: 212/62/61/16
        "N5_mistura31_O4": 31 * N5(z31[L]),                 # frente A: 2108/669/618/166
        "N5_fisher_SNR40_fixo": N5(z_f40[L]),               # bancada: 150/43/42/11
        "z_com_39_acumulados_O4c": z31[L] * math.sqrt(39 / 31),  # GWTC-6 cenario da frente B (+8 pSEOBNR)
        "z_uniao39_hoje": z39[L],
    }
res["escala"] = tab

# ---- 3. Contradicao Fisher 150 vs 212: sigma 0.0497 vs 0.058 ----
res["fisher_vs_real"] = {
    "sigma_fisher_SNR40": 0.0497, "sigma_real_GW250114": 0.0580,
    "razao_N": (0.0580 / 0.0497) ** 2,
    "N150_reescalado": 150 * (0.0580 / 0.0497) ** 2,
    "SNR_RD_equiv_GW250114": 40 * 0.0497 / 0.0580,
    "SNR_RD_5sigma_1evento_ancora_fisher": 40 * 0.0497 / (0.01985 / 5),
    "SNR_RD_5sigma_1evento_ancora_real": 40 * 0.0580 / (0.01985 / 5),
}

# ---- 4. Contradicao O5: fator de SNR x1.99 (C5 PSD) vs x1.56-1.79 (alcances) ----
f_o5 = {"C5_PSD": 1.987, "alcance_BBH_min": 2500 / 1600, "alcance_BBH_max": 2500 / 1400,
        "alcance_BNS_min": 330 / 190, "alcance_BNS_max": 330 / 160}
res["fator_O5"] = f_o5
band = (min(f_o5.values()), max(f_o5.values()))
res["fator_O5_banda"] = band
o5 = {}
for L in z_gw:
    n_gw = [N5(z_gw[L]) / f**2 for f in band]
    n_mix = [31 * N5(z31[L]) / f**2 for f in band]
    o5[L] = {"N5_GW250114_like_O5": n_gw, "N5_mistura31_O5": n_mix}
res["O5_N5"] = o5

# ---- 5. Quantos eventos O5 rende (frente B: 55-83 pSEOBNR/ano; O5 ~3 anos) ----
uteis_ano = (55.0, 83.0); anos_o5 = 3.0
N_o5 = [u * anos_o5 for u in uteis_ano]
z_o5 = {}
for L in z_gw:
    zs = []
    for Nn in N_o5:
        for f in band:
            zs.append(5 * math.sqrt(Nn / (31 * N5(z31[L]) / f**2)))
    z_o5[L] = {"z_min": min(zs), "z_max": max(zs), "N_eventos_O5_3anos": N_o5}
res["O5_z_3anos_mistura"] = z_o5

# ---- 6. Taxa de eventos GW250114-like: contagem no proprio catalogo (frente A CSV) ----
# le sigma(dtau) por evento do CSV da frente A
import csv
sig = []
with open(fontes["A_csv"], encoding="utf-8") as f:
    rd = csv.DictReader(f)
    cols = rd.fieldnames
    for row in rd:
        sig.append(row)
res["A_csv_colunas"] = cols
# procura a coluna de sigma dtau
cand = [c for c in cols if "sig" in c.lower() and "tau" in c.lower()]
res["A_csv_col_sigma_dtau"] = cand
if cand:
    c = cand[0]
    vals = []
    for row in sig:
        try:
            vals.append((row.get("event") or row.get("evento") or row.get("label") or "", float(row[c])))
        except Exception:
            pass
    vals_s = sorted(vals, key=lambda t: t[1])
    res["sigma_dtau_ordenado_10_menores"] = vals_s[:10]
    res["n_eventos_sigma_le_0p06"] = sum(1 for _, v in vals if v <= 0.06)
    res["n_eventos_sigma_le_0p10"] = sum(1 for _, v in vals if v <= 0.10)
    res["n_eventos_sigma_le_0p15"] = sum(1 for _, v in vals if v <= 0.15)
    res["n_total_csv"] = len(vals)

# O4 durou ~ (mai/2023 - nov/2025) com pausas; frente B da 14.5 uteis/ano e 31 pSEOBNR (O1-O4b) -> 21 em O4a+O4b.
# taxa GW250114-like (sigma<=0.06): 1 evento em O4a+O4b (~1.45 ano de dado util = 21/14.5)
anos_o4ab = 21 / 14.5
res["taxa_GW250114_like_O4"] = {"anos_O4a_O4b_equiv": anos_o4ab, "eventos_sigma_le_0p06": 1,
                                 "taxa_por_ano": 1 / anos_o4ab}
# O5: N_det x3.8-5.7 (frente B) e SNR x1.56-1.99 -> eventos 'GW250114-like' (sigma<=0.058) crescem ~ (f_SNR)^3 em volume
taxa_gw_o5 = [(1 / anos_o4ab) * f**3 for f in band]
res["taxa_GW250114_like_O5_por_ano"] = taxa_gw_o5
res["anos_O5_para_N5_RB_GW250114_like"] = [o5["R-B"]["N5_GW250114_like_O5"][i] / taxa_gw_o5[i] for i in range(2)]

# ---- 7. Jitter (frente A vs D): 28 (E[z]=5) vs 33/59 (poder 50/90) ----
res["jitter"] = {
    "A_N_Ez5_sdjit0.019": 28, "D_N_poder50_sdjit0.019": 33, "D_N_poder90_sdjit0.019": 59,
    "D_N_poder50_90_sdjit0.0228": [20, 35], "sd_jit_valores": {"bancada_C2_N50": 0.0192, "D_N600": 0.0228, "auditor1_N1500": 0.0226},
    "leitura": "E[z]=5 ~ poder 50%; o pre-registro usa poder 90% -> 59 (0.019) ou 35 (0.0228) eventos com sigma_df<=0.0136",
}

# ---- 8. Piso sistematico (frente C) vs efeito, por leitura ----
efeito = {"R-B": 0.01985, "R-MOD": 0.03684, "R-RAIZ-0": 0.03706, "R-LIN": 0.07148}
piso = {L: abs(v) / 5 for L, v in efeito.items()}
sist = {"familia_mesma_fonte_mediana": 0.029, "familia_outras_fontes_max": 0.097, "QNM_sum_min": 0.0125, "QNM_sum_max": 0.062,
        "t0_so_ringdown": 0.075, "estimador_SNR40": 0.0083, "estimador_SNR200": 0.0011, "catalogo_shift": 0.067}
razoes = {L: {k: v / piso[L] for k, v in sist.items()} for L in piso}
res["piso"] = {"efeito": efeito, "piso_delta_sobre_5": piso, "sistematicas": sist, "razao_sist_sobre_piso": razoes}

# ---- 9. E (45 eventos SNR>=12, teto linear) vs A (39 posteriores reais) ----
res["E_vs_A"] = {"E_zpop_45_teto": {"R-B": 0.756, "R-MOD": 1.415, "R-RAIZ-0": 1.436, "R-LIN": 2.872},
                 "A_zcomb_39_real": z39,
                 "razao_teto_sobre_real": {L: 0.756 / z39["R-B"] if L == "R-B" else None for L in ["R-B"]}}
res["E_vs_A"]["razao_teto_sobre_real"] = {L: {"R-B": 0.756, "R-MOD": 1.415, "R-RAIZ-0": 1.436, "R-LIN": 2.872}[L] / z39[L] for L in z39}

# ---- 10. 3G: B (taxas Berti) vs A (escala de SNR) ----
res["3G"] = {
    "A_N5_RB_GW250114_like": {"ET": 2.3, "CE": 0.7}, "A_N5_RB_mediana": {"ET": 37, "CE": 11},
    "B_N5_RB_SNRRD_ge50": 131, "B_N5_RB_SNRRD_ge100": 33, "B_taxas": "10^2/ano SNR_RD>=50; O(10)/ano SNR_RD>=100 [KNOWN Berti/Bhagwat]",
    "bancada_z_1evento_fonte_fixa": {"ET": 3.86, "CE": 7.03},
    "leitura": "coerentes: 1 evento de fonte fixa em ET (SNR_RD ~382) ja da 3.9 sigma; a populacao 3G com SNR_RD>=50 pede ~130 eventos (~1.3 ano)",
}

json.dump(res, open(os.path.join(OUT, "reconciliacao.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)
print(json.dumps(res, indent=1, ensure_ascii=False, default=str))
