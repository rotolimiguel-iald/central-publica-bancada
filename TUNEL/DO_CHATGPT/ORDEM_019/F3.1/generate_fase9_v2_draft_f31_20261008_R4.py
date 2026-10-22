# -*- coding: utf-8 -*-
"""Build an additive, unfrozen F3.1 V2 R4 from the registered R3 and V1.

This generator reads only pinned documentary inputs and covariance sigmas.
It does not read observed H0 centers from source files, open a real composite,
freeze a preregistration, or write outside its own F3.1 delivery directory.
"""
from __future__ import annotations

import copy
import difflib
import hashlib
import importlib.util
import json
import math
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
R3 = HERE / "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V2_RASCUNHO_F31_20261008_R3.json"
R3_GENERATOR = HERE / "generate_fase9_v2_draft_f31_20261008_R3.py"
V1 = Path(r"C:\IALD\Bancada_Um\investigacao\preregistro_fase9_hubble\PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.json")
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F3.1\AUDITORIA_F3_1_C1_a543370e.md")
STAGED_R3 = HERE.parent / "F3.2" / "f9_runner_v1x_staged_r3.py"
PINS = {
    R3: "34ee2e2004e72a83cb52dd40b38dc5faa4d1940baa429d3278a2f72ce5f30e50",
    R3_GENERATOR: "d0f998fd2a7198b4e3d8af9e77051631b622b6b92abbccc07c4294f48248e991",
    V1: "1893261e730994b3508d14dd2105f8aae3a764d3d217e28bd5939cb58f865273",
    AUDIT: "a80783503f79ee478ebc591606d9a07f8c1017686d5310bbfc209ea7c20cafb1",
}
STEM = "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V2_RASCUNHO_F31_20261008_R4"
VERDICT_NAME = "veredito_fase9_v2_r4_proposta"
VERDICT = '''def veredito_fase9_v2_r4_proposta(r):
    """Draft only: minimum for falsification, maximum for power and discrimination."""
    import math
    def f(x): return ("M" if x < 0 else "P") + ("%.1f" % abs(x)).replace(".", "P")
    base = "TGL_FASE9_RAZAO_DE_HUBBLE_V2_R4_DRAFT__"
    suf = ("__D1B__FUNDO_%s__NOT_BLIND_TO_DATA_STATED"
           "__NOT_A_CONFIRMATION__GATE_UNTOUCHED") % r["fundo"]
    if (r["n_alvos_declarados"] > 0 or not r["required_sources_admitted"]
        or r["beta_livre_no_limite"]
        or (r["n_local"] > 1 and
            any(e["chi2_por_gl"] > 2 or e["p"] < 0.01
                for e in r["dispersao_endpoints"].values()))):
        return base + "INCONCLUSIVE_SYSTEMATICS" + suf
    low, high = r["minimum"], r["maximum"]
    zd = abs(low["z_delta"])
    if zd >= 5 or any(s <= 1 and abs(z) >= 5 for s, z in low["sigma_z_por_alvo"]):
        return base + "FALSIFIED_AT_5SIGMA" + suf
    if zd >= 3: return base + "TENSION_3_TO_5_SIGMA" + suf
    if high["poder_previo"] < 5:
        return base + "NOT_FALSIFIED_UNDERPOWERED__POWER_%s_OF_5_SIGMA" % f(high["poder_previo"]) + suf
    if high["z_disc"] >= 5 and zd < 3 and high["lnB_lcdm"] >= 5 and high["lnB_livre"] >= -1:
        t = (base + "NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_%dSIGMA"
             "__ZERO_FREE_PARAMETERS" % int(math.floor(high["z_disc"])))
        t += "__USE_NOVEL" if r["use_novel_parametros"] else "__USE_NOVELTY_PENDING"
        t += "__VS_LADDER_SYSTEMATIC_LNB_%s__VS_FREE_BACKGROUND_LNB_%s" % (
            f(high["lnB_shift"]), f(high["lnB_fundo_livre"]))
        if high["lnB_shift"] < 0 and high["poder_nao_cefeida"] >= 5:
            t += "__NOT_DISCRIMINATED_FROM_LADDER_SYSTEMATIC"
        if abs(high["lnB_fundo_livre"]) < 1:
            t += "__NOT_DISCRIMINATED_FROM_FREE_BACKGROUND"
        return t + suf
    t = base + "NOT_FALSIFIED_POWERED__" + (
        "DEVIATION_CONSISTENT_WITHIN_1SIGMA" if zd < 1 else "DEVIATION_1_TO_3_SIGMA")
    if high["z_disc"] < 5:
        t += "__NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY"
    return t + suf
'''


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def read(path: Path, expected: str | None = None) -> tuple[bytes, str]:
    data = path.read_bytes()
    actual = sha(data)
    if expected and actual != expected:
        raise ValueError(f"pin mismatch: {path}: {actual} != {expected}")
    return data, actual


def write_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(path)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if Path(tmp).stat().st_size != len(data):
            raise IOError("temporary size mismatch")
        os.replace(tmp, path)
        if sha(path.read_bytes()) != sha(data):
            raise IOError("written file mismatch")
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def import_staged():
    raw, staged_sha = read(STAGED_R3)
    del raw
    sys.path.insert(0, str(STAGED_R3.parent))
    info = importlib.util.spec_from_file_location("f31_r4_staged_r3", STAGED_R3)
    assert info and info.loader
    module = importlib.util.module_from_spec(info)
    info.loader.exec_module(module)
    return module, staged_sha


def baseline(n_local: int = 5) -> dict:
    return {
        "fundo": "BG1", "n_local": n_local, "n_alvos_declarados": 0,
        "required_sources_admitted": True, "beta_livre_no_limite": False,
        "use_novel_parametros": True,
        "dispersao_endpoints": {
            "minimum": {"chi2_por_gl": 1.0, "p": 0.5},
            "maximum": {"chi2_por_gl": 1.0, "p": 0.5}},
        "minimum": {"z_delta": 0.5, "sigma_z_por_alvo": [(1.04, 0.0)]},
        "maximum": {
            "poder_previo": 6.0, "z_disc": 6.2, "lnB_lcdm": 6.0,
            "lnB_livre": 0.0, "lnB_shift": 2.0,
            "lnB_fundo_livre": 0.5, "poder_nao_cefeida": 4.0},
    }


def branch_tests(source: str) -> tuple[dict, list[dict]]:
    namespace: dict = {}
    exec(compile(source, "<F3.1-R4-pinned-verdict>", "exec"), namespace)
    decide = namespace[VERDICT_NAME]
    cases = []
    def run(name: str, modify, expected: str, n_local: int = 5):
        args = baseline(n_local)
        modify(args)
        token = decide(args)
        if expected not in token:
            raise AssertionError(f"{name}: {token} lacks {expected}")
        cases.append({"name": name, "expected": expected, "token": token})
    run("inventory_declared", lambda x: x.update(n_alvos_declarados=2), "INCONCLUSIVE_SYSTEMATICS")
    run("D_H_guard", lambda x: x.update(required_sources_admitted=False), "INCONCLUSIVE_SYSTEMATICS")
    run("beta_prior_edge", lambda x: x.update(beta_livre_no_limite=True), "INCONCLUSIVE_SYSTEMATICS")
    run("dispersion_maximum", lambda x: x["dispersao_endpoints"]["maximum"].update(chi2_por_gl=2.1), "INCONCLUSIVE_SYSTEMATICS")
    run("dispersion_p_minimum", lambda x: x["dispersao_endpoints"]["minimum"].update(p=0.009), "INCONCLUSIVE_SYSTEMATICS")
    run("n_local_one_ignores_dispersion", lambda x: x["dispersao_endpoints"]["maximum"].update(p=0.009), "DISCRIMINATES_FROM_LCDM", 1)
    run("falsified_minimum", lambda x: x["minimum"].update(z_delta=5.0), "FALSIFIED_AT_5SIGMA")
    run("single_reader_R25", lambda x: x["minimum"].update(sigma_z_por_alvo=[(0.93, 5.0)]), "FALSIFIED_AT_5SIGMA")
    run("tension_minimum", lambda x: x["minimum"].update(z_delta=3.5), "TENSION_3_TO_5_SIGMA")
    run("underpowered_maximum", lambda x: x["maximum"].update(poder_previo=4.0), "NOT_FALSIFIED_UNDERPOWERED")
    run("free_background_suffix", lambda x: None, "NOT_DISCRIMINATED_FROM_FREE_BACKGROUND")
    run("no_discrimination", lambda x: x["maximum"].update(z_disc=4.0), "NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY")
    cases_by_name = {x["name"]: x["token"] for x in cases}
    return cases_by_name, cases


def build() -> tuple[dict, dict[str, bytes]]:
    for path, pin in PINS.items():
        read(path, pin)
    raw_r3, r3_sha = read(R3, PINS[R3])
    raw_v1, v1_sha = read(V1, PINS[V1])
    old_doc = json.loads(raw_r3)
    old = json.loads(raw_v1)["spec"]
    spec = copy.deepcopy(old_doc["spec"])
    spec["id"] = "PREREG_FASE9_RAZAO_DE_HUBBLE_V2_DRAFT_F31_20261008_R4"
    spec["state"] = "RASCUNHO_NAO_CONGELADO"
    spec["estado"] = "RASCUNHO_NAO_CONGELADO; F3.4 and X13 before freeze; D-H before opening"
    spec["generated_from"]["R3_registered"] = {"path": str(R3), "sha256": r3_sha}
    spec["generated_from"]["audit_a543370e"] = {"path": str(AUDIT), "sha256": PINS[AUDIT]}

    # Keep historical pins exactly as V1 recorded them. The active program and
    # seal have advanced, so current hashes are separately measured below.
    historical = copy.deepcopy(old["fontes_lidas_sha256"])
    if len(historical) != 14:
        raise ValueError("V1 did not carry 14 historical source pins")
    pin_check = {}
    for path, expected in historical.items():
        p = Path(path)
        actual = sha(p.read_bytes()) if p.is_file() else None
        pin_check[path] = {
            "historical_v1_sha256": expected,
            "current_sha256": actual,
            "status": "MATCH" if actual == expected else ("DRIFT" if actual else "UNAVAILABLE"),
        }
    if sum(x["status"] == "MATCH" for x in pin_check.values()) != 12:
        raise ValueError("unexpected change in historical source pins")
    spec["fontes_lidas_sha256"] = {
        **historical, "V1": v1_sha, "R2": spec["base"]["R2_sha256"],
        "R3": r3_sha, "V1x_binding": old_doc["spec"]["fontes_lidas_sha256"]["V1x_binding"],
        "CCHP_Table6": old_doc["spec"]["fontes_lidas_sha256"]["CCHP_Table6"],
    }
    spec["source_pin_verification_R4"] = {
        "historical_count": 14, "matching_current": 12, "drift_current": 2,
        "meaning": "V1 pins are historical source evidence; current um.py and seal differ by later versions, without changing V1 bytes",
        "entries": pin_check, "source_admission": "D_H_PENDING",
    }
    spec["base"] = {
        **spec["base"],
        "V1_um_py_sha256": historical[next(p for p in historical if p.endswith("\\um.py"))],
        "V1_seal_sha256": historical[next(p for p in historical if p.endswith("\\um_absoluto_selo.json"))],
        "R3_sha256": r3_sha,
        "historical_pin_scope": "V1 at 2026-10-05; current program/seal hashes are separately recorded in source_pin_verification_R4",
    }
    spec["estatisticas"] = {
        **spec["estatisticas"],
        "z_TGL_composto": "GLS of active local readers versus K*H0_BG1 at both covariance endpoints; report beside the decisive z_delta and z_disc",
        "lnB": "Four comparisons by quadrature n>=100, check n=100/200; Jeffreys/Kass-Raftery V1 scale [INPUT]: <1 inconclusive, 1–2.5 weak, 2.5–5 moderate, >=5 strong. Only thresholds explicitly in verdict decide.",
        "dispersao": "If n_local>1, chi2/(n-1)>2 OR p<0.01 at EITHER endpoint gives INCONCLUSIVE; with n_local<=1 dispersion is not evaluated",
    }
    spec["novidade_de_uso"]["etiqueta"] = "retrodição sem ajuste (novidade de uso; precedente: o periélio de Mercúrio)"
    spec["novidade_de_uso"]["precedente_estatuto"] = "[KNOWN] historical analogy; not a statement that nature confirmed TGL"

    # The 0.031 is an explicit input of the R2 generator, not a published
    # factor recovered from the archived SBF source. A numerical coincidence
    # with 2.3/73.8 is diagnostic and does not establish provenance.
    staged, staged_sha = import_staged()
    amp = spec["covariancia"]["amplitudes_km_s_Mpc"]
    original = staged.grid_endpoints(spec, spec["familias"]["P_primaria"]["ids"])
    alternate = copy.deepcopy(spec)
    relative_budget = 2.3 / 73.8
    fraction = lambda mag: math.log(10) / 5 * mag
    alternate["covariancia"]["amplitudes_km_s_Mpc"]["L3N"] = 2.3 * fraction(0.032) / relative_budget
    alternate["covariancia"]["amplitudes_km_s_Mpc"]["L3T"] = 2.3 * fraction(0.033) / relative_budget
    sensitivity = staged.grid_endpoints(alternate, alternate["familias"]["P_primaria"]["ids"])
    if abs(original["maximum"]["sigma_comb"] - 0.9493551670628468) > 1e-10:
        raise ValueError("R3 primary maximum sigma changed")
    spec["covariancia"]["components"]["SBF_0p031"] = {
        "value": 0.031,
        "literal_source": {"path": str(HERE / "generate_fase9_v2_draft_f31_20261008_R2.py"), "line": 126},
        "status": "[INPUT] operational denominator, not verified as a published SBF constant",
        "interpretation": "[DERIVED] 2.3/73.8 = %.12f, which rounds to 0.031 at three decimals; this coincidence does not prove why the factor was chosen" % relative_budget,
        "bibliographic_origin": "[OPEN]",
        "sigma_max_original": original["maximum"]["sigma_comb"],
        "sigma_max_with_ratio_2p3_over_73p8": sensitivity["maximum"]["sigma_comb"],
        "effect_status": "[DERIVED] numerically negligible in this sigma-only covariance box; not a likelihood result",
    }
    for family in ("R_r25", "S_com_sirenes"):
        ids = spec["familias"][family]["ids"]
        endpoint = staged.grid_endpoints(spec, ids)
        spec["covariancia"].setdefault("pinned_family_endpoints_R4", {})[family] = {
            "reader_ids": ids,
            "minimum": {k: endpoint["minimum"][k] for k in ("lambda_N", "lambda_T", "sigma_comb", "gls_weights", "negative_weights")},
            "maximum": {k: endpoint["maximum"][k] for k in ("lambda_N", "lambda_T", "sigma_comb", "gls_weights", "negative_weights")},
            "accepted_grid_points": endpoint["accepted"],
            "method": "f9_runner_v1x_staged_r3.grid_endpoints, sigma-only",
            "method_sha256": staged_sha,
            "status": "[DERIVED] diagnostic family endpoints; no local H0 centers opened",
        }
    d5 = spec["D5_sensitivities_from_c1_audit"]
    d5["five_sigma3p9_R3_status"] = "[DERIVED] recalculated by the R3 generator"
    d5["five_sigma3p9_c1_R2_status"] = "[DECLARADO] value reported by c1 auditor; not recomputed in this R4"
    d5["status"] = "MIXED_AS_MARKED_PER_VALUE"

    source_sha = sha(VERDICT.encode("utf-8"))
    branches, cases = branch_tests(VERDICT)
    current = baseline()
    current["n_alvos_declarados"] = 2
    current["required_sources_admitted"] = False
    namespace: dict = {}
    exec(compile(VERDICT, "<F3.1-R4-pinned-verdict>", "exec"), namespace)
    current_token = namespace[VERDICT_NAME](current)
    spec["funcao_de_veredito"] = {
        **spec["funcao_de_veredito"],
        "nome": VERDICT_NAME,
        "fonte": VERDICT,
        "sha256": source_sha,
        "regra": "The future runner must execute THIS exact UTF-8 source after checking sha256; no independently rewritten copy",
        "testes_sinteticos_de_ramo": branches,
        "se_abrir_hoje": {
            "token_counterfactual_synthetic": current_token,
            "cause": "inventory count 2 (L1b and L6) and D-H admissions pending",
            "real_opening_permitted": False,
        },
        "n_local_guard": "n_local>1 before dispersion chi2/(n-1) or p; strict greater-than thresholds",
    }
    spec["funcao_de_veredito_proposta"]["n_local_guard"] = "n_local>1 before both dispersion endpoint checks"
    spec["especificacao_do_runner"] = [
        "R0 pin V2 R4 spec, exact function source/hash and R4 runner before any real composite; not frozen now",
        "R1 same inventory-wide n_alvos predicate in preflight and staged; do not create ALVOS_FASE9_LIDOS.json from documentary binding",
        "R2 recompute BG1 in Bancada from Planck comp + DESI DR2 and require |H0-68.531|<0.01; recompute beta=ALPHA_FINE_CODATA_2018*sqrt(e), K at runtime and compare frozen K",
        "R3 write PODER_FASE9_ANTES_DE_ABRIR.json and pin sha256 using only sigmas at both covariance endpoints, before local H0 centers",
        "R4 only operator act after F3.4, X13/NAT22, D-H, c1 audit may open P_primaria versus BG1",
        "R5 five hypotheses, GLS/dispersion both endpoints with n_local>1 guard, four lnB incl free background, exact pinned verdict",
        "R6 R_r25 and S_com_sirenes diagnostics use their pinned sigma endpoints and never sum replacements",
        "R7 subsequent changes get a new version beside this one",
    ]
    spec["runner_contract"].update({
        "BG1_H0_tolerance": {"target": 68.531, "strict_abs_difference_lt": 0.01, "status": "[INPUT] V1 control, not a measured result here"},
        "PODER_ANTES_DE_ABRIR": {"filename": "PODER_FASE9_ANTES_DE_ABRIR.json", "before": "local H0 center read or real composite", "inputs": "sigmas and frozen covariance box only", "pin_sha256": True},
        "n_local_guard": "n_local>1 for dispersion; n_local must be passed by staged runner",
        "R4_staged_required": "staged R3 pins old function/name and is historical only; F3.2 R4 must pin this R4 source",
    })
    spec["token_base_provisorio"] = "TGL_FASE9_RAZAO_DE_HUBBLE_V2_R4_DRAFT__LAW_D1B__BG1"
    spec["token_estado"] = "RASCUNHO_NAO_CONGELADO__F3_4_X13_D_J_PENDING__GATE_UNTOUCHED"

    spec_sha = sha(canonical(spec))
    doc = {"id": spec["id"], "state": "RASCUNHO_NAO_CONGELADO", "spec_sha256": spec_sha, "spec": spec}
    notes = [
        "# Fase 9 V2 R4 — rascunho aditivo, sem congelamento",
        "",
        f"Spec sha256: {spec_sha}. R3 sha256: {r3_sha}. V1 sha256: {v1_sha}.",
        "",
        "[REAL documental] As partes do V1 perdidas na substituição R3 estão incorporadas no JSON R4: estatísticas, função completa, base e 14 pins históricos, runner, novidade de uso e guarda n_local>1.",
        "[REAL documental] Dos 14 pins históricos, 12 coincidem com os bytes atuais. um.py e selo têm hashes atuais diferentes por versões posteriores. A R4 preserva o V1 sem atribuir seus pins ao pacote ativo.",
        "",
        "## SBF 0,031",
        "",
        f"[INPUT] Literal do gerador R2:126, usado para normalizar as amplitudes SBF. A origem bibliográfica é [OPEN]. [DERIVED] 2,3/73,8={relative_budget:.12f}, que arredonda a 0,031, mas essa coincidência não demonstra a origem.",
        f"[DERIVED] Na caixa só com sigma, sigma_max é {original['maximum']['sigma_comb']:.9f} com 0,031 e {sensitivity['maximum']['sigma_comb']:.9f} com 2,3/73,8. O efeito no teste desta sensibilidade é desprezível; nenhuma verossimilhança original foi recuperada.",
        "",
        "## Pontas diagnósticas",
        "",
    ]
    for family in ("R_r25", "S_com_sirenes"):
        ep = spec["covariancia"]["pinned_family_endpoints_R4"][family]
        notes.append(f"- [DERIVED] {family}: sigma_min={ep['minimum']['sigma_comb']:.9f}; sigma_max={ep['maximum']['sigma_comb']:.9f}; apenas sigma.")
    notes += [
        "", "## Regra e limite",
        "",
        f"Função proposta {VERDICT_NAME}, sha256 {source_sha}; 12 ramos sintéticos passaram. O texto exato fica dentro do JSON.",
        "n_local>1 antecede qualquer avaliação de dispersão. O caso de um leitor com p pequeno foi exercitado sinteticamente e não foi classificado por dispersão.",
        f"Se a regra recebesse hoje o inventário documental, o token seria {current_token}; isso é simulação, não abertura.",
        "F3.4 e X13 antecedem congelamento; D-H antecede abertura; D-J nomeia o token final. NOT_FALSIFIED não credita e nenhum gate foi movido.",
        "",
    ]
    outputs = {
        STEM + ".json": pretty(doc),
        STEM + ".md": ("\n".join(notes)).encode("utf-8"),
        "TESTE_F31_R4_SINTETICO_20261008.json": pretty({
            "function_sha256": source_sha, "passed": len(cases), "cases": cases,
            "synthetic_only": True, "real_data_opened": False,
        }),
    }
    patch = "".join(difflib.unified_diff(
        raw_r3.decode("utf-8").splitlines(keepends=True),
        outputs[STEM + ".json"].decode("utf-8").splitlines(keepends=True),
        fromfile="F3.1/V2_R3.json", tofile="F3.1/V2_R4.json"))
    outputs["DIFF_V2_R3_R4_F31_20261008.patch"] = patch.encode("utf-8")
    outputs["GERACAO_V2_RASCUNHO_F31_20261008_R4.json"] = pretty({
        "state": "RASCUNHO_NAO_CONGELADO", "spec_sha256": spec_sha,
        "verdict_sha256": source_sha, "historical_v1_source_pins": len(historical),
        "source_pin_match_current": 12, "source_pin_drift_current": 2,
        "outputs": {name: {"sha256": sha(data), "bytes": len(data)} for name, data in outputs.items()},
        "frozen": False, "real_data_opened": False, "gate_changed": False,
    })
    return doc, outputs


def main() -> None:
    doc, outputs = build()
    mode = "check_only" if "--check-only" in sys.argv[1:] else "write"
    if mode == "write":
        for name in outputs:
            if (HERE / name).exists():
                raise FileExistsError(HERE / name)
        for name, data in outputs.items():
            write_new(HERE / name, data)
    print(json.dumps({
        "mode": mode, "spec_sha256": doc["spec_sha256"],
        "function_sha256": doc["spec"]["funcao_de_veredito"]["sha256"],
        "outputs": {name: sha(data) for name, data in outputs.items()},
        "primary_sigma_max": doc["spec"]["covariancia"]["components"]["SBF_0p031"]["sigma_max_original"],
        "r25_sigma_max": doc["spec"]["covariancia"]["pinned_family_endpoints_R4"]["R_r25"]["maximum"]["sigma_comb"],
        "siren_sigma_max": doc["spec"]["covariancia"]["pinned_family_endpoints_R4"]["S_com_sirenes"]["maximum"]["sigma_comb"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
