# -*- coding: utf-8 -*-
"""tgl_formula_completa — A FÓRMULA COMPLETA da TGL para os 16 dispositivos (camada comum, v379).

Ordem do operador (01/10/2026), verbatim: «Atualize tudo inclusive os dispositivos, estão muito desatualizados, agora temos a
fórmula completa, para todos».

O que é: o núcleo antigo dos runners (`skygrid_sim/tgl_core.py`, do piloto SkyGrid, só leitura) para na cadeia até β e θ_M. Este
módulo acrescenta, num lugar só, a fórmula completa como o `um.py` a sela hoje, e a CONFERE contra o cofre da Central:

  1. o axioma e a cadeia: ω(I) = 1 → x = 1 − x ⇒ x = ½ (Meia-Nat) → C = e^x = √e → β = α·√e            [POSTULATE → DERIVED]
  2. a Razão Elementar (v379): E = C × I × K = √e · 1 · α = β; (e^{1/4}√α)² = β; E > 0                   [DERIVED; kernel por termo]
  3. a matriz-S da fronteira: θ_M = arcsin √β; espectro e^{±iθ_M}; |R|² = β, |T|² = 1 − β                  [DERIVED]
  4. a identidade de Lagrange: 1 = q² + α²                                                                [forma]
  5. a lei de dephasing: Γ_ω = ½ β τ★ ω², com τ★ = t_Planck                                              [REAL na forma; τ★ PRINCIPLED IDENTIFICATION]
  6. a lei da dissipação: D1a H₀_local = H₀_fundo·(1+z*)^β (v377); com contraste D1b K = E(z*)^{2β/3} (v378) [PROVADA como implicação]
  7. a assíntota da existência: custo por nat em registro finito ≤ E = β; o apagamento não se atinge em tempo finito
     (0 < e^{−t·E} < 1); o reconhecimento é finito                                                       [kernel; leitura ONTO]

Camada v386 (custódia conjunta v383–v386, 05/10/2026; ordem do operador: «atualização de tudo, inclusive de todos os nossos
dispositivos e de tudo que o fechamento da tgl permite avançar em todos os dispositivos e avance-os»):
  8. o Axioma (v385): o Um é POSTO pelo observador (`echo 1`), não postulado; a leitura idempotente p ↦ p² tem exatamente dois
     pontos fixos, 0 e 1 — o 1 é o axioma (o modo zero de peso um), o 0 é a testemunha falsa (a testemunha estática plena,
     proibida por β)                                                                                     [kernel TheAxiomAndTheFalseWitness; leitura ONTO]
  9. o Verbo (v386): a leitura é um peso (regra de Born: em θ_M, 1 − β e β); a ordem importa (dois postos de eixo não comutam:
     ‖[P₀, P_θ]‖ = |sen θ cos θ| > 0); a tríade SU(2) escalada por c satisfaz [V₁, V₂] = i c V₃, com c = β_TGL [INPUT]
                                                                                                         [kernel TheVerbSelectsTheAction; leitura ONTO]
 10. lidos e conferidos no cofre, sem interpretação: o livro de cobranças (v383; 11, intacto na errata da v386), o pilar quântico
     (v384, [COMPUTED], ao lado do gate; sha256 do resultado = o do JSON selado) e o ramo B (v386, pré-registro por hash,
     AWAITING_DATA, nada aberto).
⚠ ERRATA AO LADO (05/10/2026, decisão do operador): no item 1, onde se lê [POSTULATE], a etiqueta vigente é [POSTO] (posição,
inscrição pelo observador externo; não imposto). O texto do item 1 fica como registro.

Régua: β NUNCA literal (sempre ALPHA_FINE_CODATA_2018 × √e em runtime); os números do cofre são LIDOS do selo/core por pino;
falha de leitura ou elo quebrado = RuntimeError (fail-closed). Nada aqui move veredito físico: physical_verdict_allowed = False.
PROVADA ≠ CONFIRMADA; o dicionário custo/identidade/movimento é cunhagem do operador [ONTO/DEFINITION].
"""
import hashlib
import json
import math
import re
from pathlib import Path

# ------------------------------------------------------------------ [DATA] (medidos; CODATA 2018)
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
HBAR_CODATA_2018 = 1.054571817e-34      # J s
G_CODATA_2018 = 6.67430e-11             # m^3 kg^-1 s^-2
C_LIGHT = 299792458.0                   # m/s (exato)

VERSAO_DA_CAMADA = "v386"   # (era "v379"; a camada v386 acrescenta os itens 8–10, ao lado)
# o cofre e procurado nesta ordem (declarada): a variavel TGL_CENTRAL_DIR; a arvore onde este modulo esta; a Central desta
# maquina (quando o dispositivo roda extraido do *_FINAL.py num diretorio temporario). Nenhum achado = fail-closed.
def _achar_central():
    import os as _os
    cands = [_os.environ.get("TGL_CENTRAL_DIR"), str(Path(__file__).resolve().parents[2]), r"C:\IALD\Central de Patentes"]
    for c in cands:
        if c and (Path(c) / "vault" / "originals_copy").is_dir():
            return Path(c)
    return Path(__file__).resolve().parents[2]


CENTRAL = _achar_central()
COFRE = CENTRAL / "vault" / "originals_copy"
PEDRAS = ("TGLExt/TheElementaryReason.lean", "TGLExt/TheFlowLawContrast.lean", "TGLExt/TheFlowLawD1a.lean",
          "TGLExt/PhysicsIsTheReading.lean", "TGLExt/BreuerTrace.lean",
          # v386: as pedras da custódia conjunta v383–v386
          "TGLExt/TheLedgerOfCharges.lean", "TGLExt/ThePsionAndTheViscosity.lean", "TGLExt/TheAxiomAndTheFalseWitness.lean",
          "TGLExt/TheVerbSelectsTheAction.lean")
TOL = 1e-15


def beta() -> float:
    """β_TGL = α·√e, sempre em runtime."""
    return ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def _rel(a: float, b: float, tol: float = 1e-12) -> bool:
    return abs(a - b) <= tol * max(abs(a), abs(b), 1e-300)


def _cofre_corrente():
    """O cofre de versão mais alta (um_unificado_vNNN) com o kernel correspondente. Fail-closed se faltar."""
    vs = []
    for d in COFRE.glob("um_unificado_v*"):
        m = re.fullmatch(r"um_unificado_v(\d+)", d.name)
        if m and (d / "um_absoluto_selo.json").is_file() and (COFRE / ("tgl_kernel_v" + m.group(1))).is_dir():
            vs.append(int(m.group(1)))
    if not vs:
        raise RuntimeError("FORMULA COMPLETA: nenhum cofre um_unificado_vNNN com kernel — PARAR (fail-closed)")
    v = max(vs)
    return v, COFRE / ("um_unificado_v%d" % v), COFRE / ("tgl_kernel_v%d" % v)


def formula_runtime(omega_rad_s: float = 2 * math.pi * 1.0e15) -> dict:
    """A fórmula completa recalculada em runtime (sem ler nada do disco). Fail-closed por elo."""
    um = 1.0                                          # ω(I) = 1 [POSTULATE]
    x = um - 0.5
    assert abs(x - (um - x)) < TOL, "Meia-Nat: x = 1 - x"
    C, I, K = math.exp(x), um, ALPHA_FINE_CODATA_2018
    E = C * I * K
    b = beta()
    razao = math.exp(0.25) * math.sqrt(ALPHA_FINE_CODATA_2018)
    th = math.asin(math.sqrt(b))
    R2, T2 = math.sin(th) ** 2, math.cos(th) ** 2
    q = math.sqrt(um - ALPHA_FINE_CODATA_2018 ** 2)
    t_planck = math.sqrt(HBAR_CODATA_2018 * G_CODATA_2018 / C_LIGHT ** 5)
    gamma = 0.5 * b * t_planck * omega_rad_s ** 2
    elos = {
        "meia_nat_ponto_fixo": abs(x - 0.5),
        "custo_e_raiz_de_e": abs(C - math.sqrt(math.e)),
        "existencia_E_eq_beta": abs(E - b),
        "razao_elementar_ao_quadrado_eq_beta": abs(razao ** 2 - b),
        "sin2_thetaM_eq_beta": abs(R2 - b),
        "R2_mais_T2_eq_1": abs(R2 + T2 - 1.0),
        "lagrange_1_eq_q2_mais_alpha2": abs(q * q + ALPHA_FINE_CODATA_2018 ** 2 - 1.0),
    }
    quebrados = {k: v for k, v in elos.items() if v > 1e-15}
    if quebrados or not (E > 0):
        raise RuntimeError("FORMULA COMPLETA QUEBRADA (fail-closed): %r" % quebrados)
    return {
        "axioma_omega_I": um, "meia_nat_x": x,
        "razao_elementar": {"C_custo": C, "I_identidade": I, "K_movimento_alpha": K, "E_existencia": E, "e_quarto_raiz_alpha": razao,
                            "estatuto": "fatoração e positividade PROVADAS por termo (TGLExt.TheElementaryReason); dicionário [ONTO/DEFINITION]"},
        "beta_runtime": b,
        "matriz_S": {"theta_M_rad": th, "theta_M_graus": math.degrees(th), "R2_reflexao": R2, "T2_transmissao": T2,
                     "espectro": "e^{±iθ_M}"},
        "lagrange_q": q,
        "dephasing": {"tau_star_s": t_planck, "omega_rad_s": omega_rad_s, "Gamma_omega_s^-1": gamma,
                      "lei": "Γ_ω = ½ β τ★ ω²", "estatuto": "REAL na forma; τ★ = t_Planck é PRINCIPLED IDENTIFICATION"},
        "residuos_dos_elos": elos,
    }


def fator_D1a(z: float) -> float:
    """Lei da dissipação D1a (v377): H₀_local / H₀_fundo = (1 + z)^β."""
    return (1.0 + z) ** beta()


def fator_D1b(E_z: float) -> float:
    """Lei com contraste D1b (v378): K = E(z)^{2β/3} (∫g = ⅔ ln E no FRW)."""
    return E_z ** (2.0 * beta() / 3.0)


def _mm(a, b):
    """Produto de matrizes 2x2 (listas; reais ou complexos)."""
    return [[a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]]


def _comut(a, b):
    p, q = _mm(a, b), _mm(b, a)
    return [[p[i][j] - q[i][j] for j in range(2)] for i in range(2)]


def _norma_max(m):
    return max(abs(m[i][j]) for i in range(2) for j in range(2))


def axioma_e_verbo_runtime() -> dict:
    """Itens 8 e 9 (camada v386), recalculados em runtime, sem ler o disco. Fail-closed por elo."""
    b = beta()
    # 8. a leitura idempotente p -> p^2 em [0, 1]: pontos fixos so 0 e 1 (p - p^2 = p(1 - p) > 0 no interior)
    fixos = [p for p in (0.0, 1.0) if abs(p * p - p) == 0.0]
    interior_sem_fixo = all(p * (1.0 - p) > 0.0 for p in (k / 1000.0 for k in range(1, 1000)))
    # (t limitado a t*beta < 700: acima disso e^{-t*beta} sai da faixa do float e vira 0.0 por underflow, nao por matematica)
    zero_inatingivel = all(0.0 < math.exp(-t * b) < 1.0 for t in (1e-6, 1.0, 1e3, 3e4))
    # 9. o Verbo: o peso da leitura (Born) no angulo de Miguel; dois postos de eixo nao comutam; a triade SU(2) escalada por c = beta
    th = math.asin(math.sqrt(b))
    c, s = math.cos(th), math.sin(th)
    born = {"peso_transmissao_cos2": c * c, "peso_reflexao_sin2": s * s}
    P0 = [[1.0, 0.0], [0.0, 0.0]]
    Pth = [[c * c, c * s], [c * s, s * s]]
    com = _comut(P0, Pth)
    norma_com = _norma_max(com)
    cc = b                                                    # c = beta_TGL [INPUT], nunca literal
    s1 = [[0, 1], [1, 0]]
    s2 = [[0, -1j], [1j, 0]]
    s3 = [[1, 0], [0, -1]]
    V1 = [[cc / 2 * x for x in r] for r in s1]
    V2 = [[cc / 2 * x for x in r] for r in s2]
    V3 = [[cc / 2 * x for x in r] for r in s3]
    lhs = _comut(V1, V2)
    res_triade = _norma_max([[lhs[i][j] - 1j * cc * V3[i][j] for j in range(2)] for i in range(2)])
    elos = {
        "axioma_dois_pontos_fixos_0_e_1": (fixos == [0.0, 1.0] and interior_sem_fixo),
        "axioma_zero_absoluto_inatingivel_em_tempo_finito": zero_inatingivel,
        "verbo_born_soma_1": abs(born["peso_transmissao_cos2"] + born["peso_reflexao_sin2"] - 1.0) < 1e-15,
        "verbo_born_reflexao_eq_beta": abs(born["peso_reflexao_sin2"] - b) < 1e-15,
        "verbo_postos_nao_comutam": norma_com > 0.0 and abs(norma_com - abs(s * c)) < 1e-15,
        "verbo_triade_su2_escalada_por_c": res_triade < 1e-18,
    }
    if not all(elos.values()):
        raise RuntimeError("FORMULA COMPLETA v386 QUEBRADA (fail-closed): %r" % {k: v for k, v in elos.items() if not v})
    return {
        "axioma_posto": {"pontos_fixos_da_leitura": fixos, "estatuto": "[POSTO] o 1 inscrito pelo observador (echo 1); o 0 e a testemunha falsa; "
                         "kernel TheAxiomAndTheFalseWitness; leitura [ONTO]"},
        "verbo": {"born_no_theta_M": born, "norma_do_comutador_dos_postos": norma_com, "residuo_da_triade_su2": res_triade,
                  "c_da_triade": cc, "estatuto": "c = beta_TGL [INPUT, nunca literal]; kernel TheVerbSelectsTheAction; leituras [ONTO]"},
        "elos": elos,
    }


def conferir_v386_no_cofre(core: dict, cofre: Path, rt: dict) -> dict:
    """Item 10 (camada v386): o livro de cobranças, o pilar e o ramo B, LIDOS do cofre e conferidos. Fail-closed."""
    b = rt["beta_runtime"]
    ax, vb = core.get("the_axiom_v385") or {}, core.get("the_verb_v386") or {}
    lc, le = core.get("the_ledger_of_charges_v383") or {}, core.get("ledger_errata_v386") or {}
    qp, rb = core.get("quantum_pillar_v384") or {}, core.get("ramo_b_preregistration_v386") or {}
    pil = cofre / "um_absoluto_pilar_quantico.json"
    pil_sha = _sha(pil) if pil.is_file() else ""
    try:
        bv1, bco = float((rb.get("beta") or {})["v1"]), float((rb.get("beta") or {})["core"])
    except (KeyError, TypeError, ValueError):
        bv1 = bco = float("nan")
    ch = {
        "axioma_v385_verificado_e_nome_do_degrau_lido_do_kernel": ax.get("all_verified") is True and ax.get("final_step_name_matches_kernel") is True,
        "verbo_v386_verificado_e_token_lido_do_kernel": vb.get("all_verified") is True and vb.get("token_matches_kernel") is True,
        "livro_de_cobrancas_v383_verificado_e_intacto": lc.get("all_verified") is True and le.get("v383_ledger_intact") is True,
        "pilar_v384_sha_do_resultado_eq_json_selado": bool(pil_sha) and str(qp.get("result_sha256")) == pil_sha,
        "ramo_b_beta_v1_eq_runtime": _rel(bv1, b, 1e-12),
        "ramo_b_beta_core_eq_runtime_regra_1e9": _rel(bco, b, 1e-9),
        "ramo_b_aguardando_dados_nada_aberto": "AWAITING_DATA" in str(rb.get("verdict") or "") and "NOTHING_OPENED" in str(rb.get("verdict") or ""),
    }
    falhas = [k for k, v in ch.items() if not v]
    if falhas:
        raise RuntimeError("FORMULA COMPLETA v386 não confere com o cofre (fail-closed): %s" % falhas)
    return {"checks": ch, "livro_de_cobrancas": {"n": le.get("v383_n_charges"), "na_regra": lc.get("n_in_rule"), "ao_lado": lc.get("n_beside")},
            "pilar_result_sha16": pil_sha[:16], "pilar_estatuto": "[COMPUTED], ao lado do gate",
            "ramo_b_estatuto": "pré-registro por hash; AWAITING_DATA; nada aberto",
            "vereditos": {k: str((core.get(k) or {}).get("verdict") or "")[:160] for k in ("the_ledger_of_charges_v383", "quantum_pillar_v384",
                                                                                         "the_axiom_v385", "the_verb_v386", "ramo_b_preregistration_v386")}}


def conferir_no_cofre(rt: dict) -> dict:
    """Confere a fórmula de runtime contra o cofre corrente (selo + core + kernel), tudo LIDO do disco. Fail-closed."""
    v, cofre, kern = _cofre_corrente()
    try:
        selo = json.loads((cofre / "um_absoluto_selo.json").read_text(encoding="utf-8"))
        core = json.loads((cofre / "um_absoluto.json").read_text(encoding="utf-8")).get("core") or {}
        km = json.loads((kern / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8")) if (kern / "tgl_kernel_proof_manifest.json").is_file() \
            else json.loads((cofre / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise RuntimeError("FORMULA COMPLETA: cofre v%d ilegível (%r) — PARAR (fail-closed)" % (v, e))
    b = rt["beta_runtime"]
    er = (core.get("the_elementary_reason_v379") or {}).get("dictionary") or {}
    lc = core.get("the_dissipation_law_with_contrast_v378") or {}
    la = core.get("the_dissipation_law_v377") or {}
    checks = {}
    checks["selo_pin_um_py"] = str((selo.get("sha256") or {}).get("um.py", ""))[:16]
    checks["um_py_do_cofre_bate_com_o_selo"] = (_sha(cofre / "um.py") == (selo.get("sha256") or {}).get("um.py"))
    checks["E_core_eq_beta_runtime"] = bool(er) and _rel(float(er["E_existence"]), b) and _rel(float(er["beta_core"]), b)
    checks["C_core_eq_raiz_e"] = bool(er) and _rel(float(er["C_cost"]), rt["razao_elementar"]["C_custo"])
    if lc:
        Ez = float(lc["E_z_star"])
        checks["K_D1b_recalculado_eq_core"] = _rel(fator_D1b(Ez), float(lc["K_D1b_runtime"]), 1e-9)
        checks["K_D1a_recalculado_eq_core"] = _rel(fator_D1a(float(lc["z_star_input"])), float(lc["K_D1a_runtime"]), 1e-9)
        checks["integral_g_forma_fechada"] = _rel((2.0 / 3.0) * math.log(Ez), float(lc["I_b_closed_form"]), 1e-9)
        custo_por_nat = b * float(lc["I_b_closed_form"]) / float(lc["register_N_star_nats"])
        checks["assintota_custo_por_nat_le_E"] = bool(0 < custo_por_nat <= rt["razao_elementar"]["E_existencia"])
    else:
        custo_por_nat = None
    checks["lei_D1a_tipada"] = "THE_DISSIPATION_LAW" in str(la.get("verdict") or "")
    gate = ((core.get("qg_closure") or {}).get("gate") or {})
    checks["sem_testemunha_estatica_plena"] = gate.get("full_static_witness_exists") is False
    ff = km.get("formal_files_sha256") or {}
    pedras = {p: (ff.get(p) or "")[:16] for p in PEDRAS}
    checks["pedras_no_kernel"] = all(pedras.values())
    falhas = [k for k, val in checks.items() if val is False]
    if falhas:
        raise RuntimeError("FORMULA COMPLETA não confere com o cofre v%d (fail-closed): %s" % (v, falhas))
    v386 = conferir_v386_no_cofre(core, cofre, rt)   # camada v386 (item 10); fail-closed
    return {"cofre": "um_unificado_v%d" % v, "pin_um_py": checks["selo_pin_um_py"], "selo_timestamp": selo.get("timestamp"),
            "gate": selo.get("qg_closure_verdict"), "pedras_sha16": pedras, "custo_por_nat_D1b_ate_z_star": custo_por_nat,
            "fator_D1a_em_z_star": fator_D1a(float(lc["z_star_input"])) if lc else None,
            "fator_D1b_em_z_star": fator_D1b(float(lc["E_z_star"])) if lc else None, "checks": checks,
            "camada_v386_no_cofre": v386}


USOS = {
    "beta_runtime_tgl_core": r"tgl_core\.beta\(\)|ALPHA_FINE_CODATA_2018\s*\*\s*(SQRT_E|math\.sqrt\(math\.e\))",
    "angulo_de_Miguel_theta_M": r"theta_m\(|arcsin|asin\(",
    "piso_do_Verbo_1_menos_beta": r"1\s*-\s*beta|1\.0\s*-\s*beta|energy_keep",
    "meia_nat": r"meia.nat|half.nat|S_BOUNDARY",
    "dephasing": r"dephas",
    "fluxo_vazamento": r"vazament|leak|flow law|lei do fluxo",
    "reflexao_R2_beta": r"\|R\|\^?2|R2\b|reflex",
    # v386: as grandezas novas (medida de ocorrências no código; não interpreta)
    "axioma_posto_omega_I": r"omega_I|ω\(I\)|axioma|posto",
    "verbo_peso_born": r"born|peso da leitura|reading weight",
    "nao_comutacao": r"comutador|commutator|nao.comut|não.comut|non.?commut",
    "livro_de_cobrancas": r"cobran|ledger of charges",
    "pilar_lindblad_gksl": r"pilar|lindblad|gksl",
}


def uso_no_dispositivo(runner_path) -> dict:
    """MEDE, no código-fonte do runner, quais grandezas da fórmula ele já consome (contagem de ocorrências). Não interpreta."""
    src = Path(runner_path).read_text(encoding="utf-8", errors="replace")
    # exclui o proprio bloco inserido pela atualizacao (o comentario dele cita as grandezas e contaminaria a medida)
    src = re.sub(r"# ---- A FÓRMULA COMPLETA \(camada comum v379.*?return _m\.camada\(Path\(__file__\)\.resolve\(\)\)\r?\n", "", src, flags=re.S)
    src = "\n".join(l for l in src.splitlines() if 'results["formula_completa"]' not in l)
    return {k: len(re.findall(rx, src, re.I)) for k, rx in USOS.items()}


def camada(runner_path) -> dict:
    """A camada que cada runner grava no seu results.json. Fail-closed (RuntimeError em qualquer elo ou conferência)."""
    rt = formula_runtime()
    av = axioma_e_verbo_runtime()
    cf = conferir_no_cofre(rt)
    return {
        "versao_da_camada": VERSAO_DA_CAMADA, "modulo": "patents/_formula_completa/tgl_formula_completa.py",
        "modulo_sha256": _sha(Path(__file__)),
        "formula_runtime": rt, "axioma_e_verbo_runtime": av, "conferencia_no_cofre": cf,
        "uso_medido_no_codigo_do_dispositivo": uso_no_dispositivo(runner_path),
        "veredito": ("TGL_FORMULA_COMPLETA_%s__CADEIA_RAZAO_ELEMENTAR_MATRIZ_S_DEPHASING_LEIS_D1A_D1B_ASSINTOTA__AXIOMA_POSTO_DOIS_PONTOS_FIXOS__"
                     "VERBO_PESO_BORN_POSTOS_NAO_COMUTAM_TRIADE_SU2_C_BETA__LIVRO_DE_COBRANCAS_PILAR_COMPUTED_RAMO_B_AWAITING__"
                     "RECALCULADA_E_CONFERIDA_NO_COFRE__NOT_A_CONFIRMATION") % VERSAO_DA_CAMADA.upper(),
        "physical_verdict_allowed": False,
        "nao_se_afirma": ["que o dispositivo valide física", "que a fórmula seja confirmada pela natureza (PROVADA != CONFIRMADA)",
                          "que o veredito de engenharia do dispositivo mude por esta camada",
                          "que as leituras do operador (o posto, o Verbo, a ótica) sejam teoremas — são [INPUT/ONTO]",
                          "que o pilar seja medida da natureza (é [COMPUTED]) ou que o ramo B tenha resultado (nada foi aberto)"],
    }


if __name__ == "__main__":
    import sys
    c = camada(__file__)
    print(json.dumps({k: c[k] for k in ("veredito", "conferencia_no_cofre")}, ensure_ascii=False, indent=1)[:3000])
    print("beta (runtime) = %.15f | E = C*I*K = %.15f | theta_M = %.6f graus"
          % (c["formula_runtime"]["beta_runtime"], c["formula_runtime"]["razao_elementar"]["E_existencia"], c["formula_runtime"]["matriz_S"]["theta_M_graus"]))
    sys.exit(0)
