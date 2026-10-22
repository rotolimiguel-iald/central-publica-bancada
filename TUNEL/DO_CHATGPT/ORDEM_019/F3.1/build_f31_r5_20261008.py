"""Build the additive F3.1 R5 draft from the pinned F3.4 projection.

Only new files in this delivery directory are written. No real data, Bancada
files, memory surfaces, or frozen preregistration are read or changed.
"""

from __future__ import annotations

import copy
import difflib
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCALAR_R4_F34 = HERE / "PREREGISTRO_FASE9_V2_R4_F34_DUAS_TESTEMUNHAS_20261008.json"
JOINT_R4_F34 = HERE / "ROOT90DA_F34_DUAS_TESTEMUNHAS_20261008.json"
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F3.1\AUDITORIA_F3_1_C1_aab519bd.md")
PINS = {
    SCALAR_R4_F34: "ca59870c4e840bf6c87b7b5051cc1b4e6ff25a88d026fca38893291fdd14153f",
    JOINT_R4_F34: "a493cd0fca8d8c5a41d5740422d2371bec57b3feb99bcc9a14ec73cf22400200",
    AUDIT: "e135d7d3ada1c3d70c8b4ad02c538e65c0e8cdba5e57f47dc080549401ef0373",
}

VERDICT_NAME = "veredito_fase9_v2_r5_proposta"
VERDICT = '''def veredito_fase9_v2_r5_proposta(r):
    """Draft: minimum for falsification; maximum for power/discrimination."""
    import math
    from decimal import Decimal, ROUND_DOWN

    def label(x):
        if not math.isfinite(x):
            raise ValueError("non-finite verdict input")
        magnitude = Decimal(str(abs(x))).quantize(Decimal("0.1"), rounding=ROUND_DOWN)
        return ("M" if x < 0 else "P") + format(magnitude, ".1f").replace(".", "P")

    base = "TGL_FASE9_RAZAO_DE_HUBBLE_V2_R5_DRAFT__"
    suffix = ("__D1B__FUNDO_%s__NOT_BLIND_TO_DATA_STATED"
              "__NOT_A_CONFIRMATION__GATE_UNTOUCHED") % r["fundo"]
    if (r["n_alvos_declarados"] > 0 or not r["required_sources_admitted"]
            or r["beta_livre_no_limite"]):
        return base + "INCONCLUSIVE_SYSTEMATICS" + suffix

    if r["n_local"] > 1:
        endpoints = r.get("dispersao_endpoints")
        if not isinstance(endpoints, dict) or set(endpoints) != {"minimum", "maximum"}:
            return base + "INCONCLUSIVE_SYSTEMATICS" + suffix
        for point in ("minimum", "maximum"):
            row = endpoints[point]
            if not isinstance(row, dict) or "chi2_por_gl" not in row or "p" not in row:
                return base + "INCONCLUSIVE_SYSTEMATICS" + suffix
            chi2, p = row["chi2_por_gl"], row["p"]
            if (not isinstance(chi2, (int, float)) or not isinstance(p, (int, float))
                    or not math.isfinite(chi2) or not math.isfinite(p)
                    or chi2 < 0 or not 0 <= p <= 1):
                return base + "INCONCLUSIVE_SYSTEMATICS" + suffix
            if chi2 > 2 or p < 0.01:
                return base + "INCONCLUSIVE_SYSTEMATICS" + suffix

    low, high = r["minimum"], r["maximum"]
    zd = abs(low["z_delta"])
    if zd >= 5 or any(s <= 1 and abs(z) >= 5 for s, z in low["sigma_z_por_alvo"]):
        return base + "FALSIFIED_AT_5SIGMA" + suffix
    if zd >= 3:
        return base + "TENSION_3_TO_5_SIGMA" + suffix
    if high["poder_previo"] < 5:
        return (base + "NOT_FALSIFIED_UNDERPOWERED__POWER_%s_OF_5_SIGMA"
                % label(high["poder_previo"]) + suffix)
    if (high["z_disc"] >= 5 and high["lnB_lcdm"] >= 5
            and high["lnB_livre"] >= -1):
        token = (base + "NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_%dSIGMA"
                 "__ZERO_FREE_PARAMETERS" % int(math.floor(high["z_disc"])))
        token += "__USE_NOVEL" if r["use_novel_parametros"] else "__USE_NOVELTY_PENDING"
        token += "__VS_LADDER_SYSTEMATIC_LNB_%s__VS_FREE_BACKGROUND_LNB_%s" % (
            label(high["lnB_shift"]), label(high["lnB_fundo_livre"]))
        if high["lnB_shift"] < 0 and high["poder_nao_cefeida"] >= 5:
            token += "__NOT_DISCRIMINATED_FROM_LADDER_SYSTEMATIC"
        if abs(high["lnB_fundo_livre"]) < 1:
            token += "__NOT_DISCRIMINATED_FROM_FREE_BACKGROUND"
        return token + suffix

    token = base + "NOT_FALSIFIED_POWERED__" + (
        "DEVIATION_CONSISTENT_WITHIN_1SIGMA" if zd < 1 else "DEVIATION_1_TO_3_SIGMA")
    if high["z_disc"] < 5:
        token += "__NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY"
    if high["lnB_lcdm"] < 5:
        token += "__NOT_DISCRIMINATED_FROM_LCDM_LNB_BELOW_5"
    if high["lnB_livre"] < -1:
        token += "__NOT_DISCRIMINATED_FROM_LCDM_BETA_FREE_LNB_BELOW_MINUS_1"
    return token + suffix
'''


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def pin(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    actual = digest(data)
    if path in PINS and actual != PINS[path]:
        raise ValueError(f"source pin changed: {path}: {actual}")
    return {"path": str(path), "sha256": actual, "bytes": len(data)}


def write_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(path)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if Path(temporary).stat().st_size != len(data):
            raise OSError("temporary size mismatch")
        os.replace(temporary, path)
        if path.read_bytes() != data:
            raise OSError("new file round-trip mismatch")
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def baseline(n_local: int = 5) -> dict:
    return {
        "fundo": "BG1", "n_local": n_local, "n_alvos_declarados": 0,
        "required_sources_admitted": True, "beta_livre_no_limite": False,
        "use_novel_parametros": True,
        "dispersao_endpoints": {
            "minimum": {"chi2_por_gl": 1.0, "p": 0.5},
            "maximum": {"chi2_por_gl": 1.0, "p": 0.5},
        },
        "minimum": {"z_delta": 0.5, "sigma_z_por_alvo": [(1.04, 0.0)]},
        "maximum": {
            "poder_previo": 6.0, "z_disc": 6.2, "lnB_lcdm": 6.0,
            "lnB_livre": 0.0, "lnB_shift": 2.0,
            "lnB_fundo_livre": 0.5, "poder_nao_cefeida": 4.0,
        },
    }


def exercise() -> list[dict[str, str]]:
    namespace: dict = {}
    exec(compile(VERDICT, "<F3.1-R5-verdict>", "exec"), namespace)
    decide = namespace[VERDICT_NAME]
    cases: list[dict[str, str]] = []

    def run(name: str, mutate, contains: str, excludes: str | None = None, n_local: int = 5) -> None:
        row = baseline(n_local)
        mutate(row)
        token = decide(row)
        if contains not in token or (excludes and excludes in token):
            raise AssertionError(f"{name}: {token}")
        cases.append({"name": name, "expected": contains, "token": token})

    run("source_admission_pending", lambda r: r.update(required_sources_admitted=False), "INCONCLUSIVE_SYSTEMATICS")
    run("inventory_pending", lambda r: r.update(n_alvos_declarados=2), "INCONCLUSIVE_SYSTEMATICS")
    run("beta_prior_edge", lambda r: r.update(beta_livre_no_limite=True), "INCONCLUSIVE_SYSTEMATICS")
    run("dispersion_empty", lambda r: r.update(dispersao_endpoints={}), "INCONCLUSIVE_SYSTEMATICS")
    run("dispersion_one_endpoint", lambda r: r["dispersao_endpoints"].pop("maximum"), "INCONCLUSIVE_SYSTEMATICS")
    run("dispersion_missing_p", lambda r: r["dispersao_endpoints"]["minimum"].pop("p"), "INCONCLUSIVE_SYSTEMATICS")
    run("dispersion_invalid_p", lambda r: r["dispersao_endpoints"]["minimum"].update(p=float("nan")), "INCONCLUSIVE_SYSTEMATICS")
    run("dispersion_high_chi2", lambda r: r["dispersao_endpoints"]["maximum"].update(chi2_por_gl=2.1), "INCONCLUSIVE_SYSTEMATICS")
    run("dispersion_low_p", lambda r: r["dispersao_endpoints"]["minimum"].update(p=0.009), "INCONCLUSIVE_SYSTEMATICS")
    run("one_reader_no_dispersion", lambda r: r.update(dispersao_endpoints={}), "DISCRIMINATES_FROM_LCDM", n_local=1)
    run("falsification", lambda r: r["minimum"].update(z_delta=5.0), "FALSIFIED_AT_5SIGMA")
    run("tension", lambda r: r["minimum"].update(z_delta=3.2), "TENSION_3_TO_5_SIGMA")
    for value in (4.95, 4.999, 4.9999):
        run(f"power_truncation_{value}", lambda r, x=value: r["maximum"].update(poder_previo=x),
            "NOT_FALSIFIED_UNDERPOWERED__POWER_P4P9_OF_5_SIGMA", "POWER_P5P0")
    run("power_boundary_5", lambda r: r["maximum"].update(poder_previo=5.0), "NOT_FALSIFIED_POWERED")
    run("lnB_below_5_at_z6", lambda r: r["maximum"].update(lnB_lcdm=4.9),
        "NOT_DISCRIMINATED_FROM_LCDM_LNB_BELOW_5", "__DISCRIMINATES_FROM_LCDM_AT_")
    run("lnB_free_below_minus_1", lambda r: r["maximum"].update(lnB_livre=-1.1),
        "NOT_DISCRIMINATED_FROM_LCDM_BETA_FREE_LNB_BELOW_MINUS_1", "__DISCRIMINATES_FROM_LCDM_AT_")
    run("z_below_5", lambda r: r["maximum"].update(z_disc=4.9),
        "NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY")
    run("free_background_suffix", lambda r: None, "NOT_DISCRIMINATED_FROM_FREE_BACKGROUND")
    return cases


def build() -> dict[str, bytes]:
    sources = {"scalar_r4_f34": pin(SCALAR_R4_F34), "joint_r4_f34": pin(JOINT_R4_F34),
               "audit_aab519bd": pin(AUDIT)}
    previous = json.loads(SCALAR_R4_F34.read_text(encoding="utf-8"))
    joint_previous = json.loads(JOINT_R4_F34.read_text(encoding="utf-8"))
    spec = copy.deepcopy(previous["spec"])
    assert previous["spec_sha256"] == digest(compact(spec))
    assert spec["funcao_de_veredito"]["sha256"] == digest(spec["funcao_de_veredito"]["fonte"].encode("utf-8"))
    assert spec["covariancia"]["components"]["SBF_0p031"]["value"] == 0.031
    assert spec["covariancia"]["components"]["SBF_0p031"]["bibliographic_origin"] == "[OPEN]"

    cases = exercise()
    function_hash = digest(VERDICT.encode("utf-8"))
    scalar = copy.deepcopy(previous)
    scalar["id"] = "PREREG_FASE9_RAZAO_DE_HUBBLE_V2_DRAFT_F31_20261008_R5"
    scalar["state"] = "RASCUNHO_DOCUMENTAL_R5_NAO_CONGELADO"
    scalar["derived_from"] = sources["scalar_r4_f34"]
    scalar["integration_note"] = (
        "R5 corrigida para reauditoria c1. F3.2 ainda precisa pinar a especificacao e a funcao "
        "R5 auditadas antes de qualquer composto; X13 antes do congelamento e D-H antes da abertura."
    )
    spec = scalar["spec"]
    spec["id"] = scalar["id"]
    spec["generated_from"]["F34_R4_projection"] = sources["scalar_r4_f34"]
    spec["generated_from"]["audit_aab519bd"] = sources["audit_aab519bd"]
    spec["funcao_de_veredito"]["fonte"] = VERDICT
    spec["funcao_de_veredito"]["sha256"] = function_hash
    spec["funcao_de_veredito"]["nome"] = VERDICT_NAME
    spec["funcao_de_veredito"]["testes_sinteticos_de_ramo"] = {c["name"]: c["token"] for c in cases}
    spec["funcao_de_veredito"]["n_local_guard"] = (
        "n_local>1 requires exactly minimum and maximum dispersion endpoints, finite chi2/p; "
        "missing or malformed endpoints yield INCONCLUSIVE_SYSTEMATICS"
    )
    spec["funcao_de_veredito"]["truncamento_rotulos"] = (
        "One decimal toward zero, never rounding: power 4.95..4.9999 -> POWER_P4P9_OF_5_SIGMA"
    )
    spec["funcao_de_veredito"]["lnB_lcdm_guard"] = (
        "z_disc>=5 with lnB_lcdm<5 is NOT_DISCRIMINATED_FROM_LCDM_LNB_BELOW_5"
    )
    spec["funcao_de_veredito"]["se_abrir_hoje"]["token_counterfactual_synthetic"] = next(
        c["token"] for c in cases if c["name"] == "inventory_pending"
    )
    spec["funcao_de_veredito_proposta"]["n_local_guard"] = spec["funcao_de_veredito"]["n_local_guard"]
    spec["funcao_de_veredito_proposta"]["order"][-1] = (
        "otherwise NOT_FALSIFIED_POWERED with an explicit NOT_DISCRIMINATED_FROM_LCDM suffix "
        "for z_disc<5, lnB_lcdm<5 or lnB_beta_free<-1"
    )
    spec["token_base_provisorio"] = "TGL_FASE9_RAZAO_DE_HUBBLE_V2_R5_DRAFT__LAW_D1B__BG1"
    spec["token_estado"] = "RASCUNHO_R5_NAO_CONGELADO__F3_4_RESOLVED__X13_D_H_D72_PENDING__GATE_UNTOUCHED"
    spec["f34_duas_testemunhas"]["token_D_J"] = "permanece D_J_PENDING na R5, sem cunhagem por este adendo"
    if "d72 qualification in Codex interface" not in spec["pending_operator_decisions"]:
        spec["pending_operator_decisions"].append("d72 qualification in Codex interface")
    scalar["spec_sha256"] = digest(compact(spec))

    joint = copy.deepcopy(joint_previous)
    joint["schema"] = "ROOT90DA_F34_TWO_WITNESSES_ADDENDUM_R5"
    joint["derived_from"] = sources["joint_r4_f34"]
    joint["scalar_witness"]["derived_spec_sha256"] = scalar["spec_sha256"]
    joint["scalar_witness"]["r5_verdict_function_sha256"] = function_hash
    if "d72" not in joint["other_operator_acts"]:
        joint["other_operator_acts"].insert(2, "d72")
    assert joint["other_operator_acts"] == ["X13", "D-H", "d72", "F3.3 abertura"]

    scalar_name = "PREREGISTRO_FASE9_V2_R5_F31_20261008.json"
    joint_name = "ROOT90DA_F34_R5_D72_20261008.json"
    tests_name = "TESTE_F31_R5_SINTETICO_20261008.json"
    diff_name = "DIFF_F31_F34_R4_R5_20261008.patch"
    note_name = "NOTA_F31_R5_20261008.md"
    result_name = "RESULTADO_F31_V2_R5_20261008.json"
    scalar_bytes = pretty(scalar)
    joint_bytes = pretty(joint)
    tests_bytes = pretty({"schema": "F31_R5_SYNTHETIC_TESTS_V1", "function_sha256": function_hash,
                          "synthetic_only": True, "real_data_opened": False,
                          "passed": len(cases), "cases": cases})
    old_lines = SCALAR_R4_F34.read_text(encoding="utf-8").splitlines(keepends=True)
    new_lines = scalar_bytes.decode("utf-8").splitlines(keepends=True)
    diff_bytes = "".join(difflib.unified_diff(old_lines, new_lines, fromfile=SCALAR_R4_F34.name,
                                              tofile=scalar_name)).encode("utf-8")
    note_bytes = ("# F3.1 R5 — correções ao lado\n\n"
                  "[REAL documental] O Nós Vivo F3.1 aponta a V2 R4, a camada F3.4, o V1 e a auditoria; "
                  "a R5 reaproveita essas fontes pinadas. A função de veredito foi corrigida para truncar "
                  "rótulos em um decimal, exigir as duas pontas de dispersão com n_local>1 e explicitar "
                  "a não discriminação quando z_disc>=5 mas lnB_lcdm<5. A d72 entrou nos atos do operador "
                  "do adendo ROOT90da.\n\n"
                  "[OPEN] A origem bibliográfica do fator 0,031 permanece aberta. X13 precede "
                  "o congelamento; D-H precede a abertura; d72 e a abertura são atos do operador. "
                  "F3.2 ainda requer novo pin após auditoria da R5. Nenhum composto real ou gate foi movido.\n"
                  ).encode("utf-8")
    artifact_bytes = {scalar_name: scalar_bytes, joint_name: joint_bytes,
                      tests_name: tests_bytes, diff_name: diff_bytes, note_name: note_bytes}
    result = {
        "schema": "F31_V2_R5_RESULT_V1", "unit": "F3.1",
        "status": "ENTREGUE_PARA_REAUDITORIA_C1", "sources": sources,
        "generator": pin(Path(__file__)),
        "new_artifacts": {name: {"sha256": digest(data), "bytes": len(data)}
                          for name, data in artifact_bytes.items()},
        "scalar_spec_sha256": scalar["spec_sha256"],
        "scalar_verdict_function_sha256": function_hash,
        "synthetic_tests_passed": len(cases),
        "power_4p95_truncated_to_4p9": True,
        "dispersion_missing_endpoint_fail_closed": True,
        "lnB_below_5_non_discrimination_suffix": True,
        "d72_in_other_operator_acts": True,
        "factor_0p031_bibliographic_origin": "OPEN",
        "frozen": False, "real_data_opened": False,
        "compound_computed": False, "gate_changed": False,
    }
    artifact_bytes[result_name] = pretty(result)
    return artifact_bytes


def main() -> None:
    files = build()
    check = "--check" in sys.argv[1:]
    for name, data in files.items():
        path = HERE / name
        if check:
            if path.read_bytes() != data:
                raise AssertionError(f"generated bytes differ: {path}")
        else:
            write_new(path, data)
    print(json.dumps({"mode": "check" if check else "create",
                      "artifacts": {name: digest(data) for name, data in files.items()}}, indent=2))


if __name__ == "__main__":
    main()
