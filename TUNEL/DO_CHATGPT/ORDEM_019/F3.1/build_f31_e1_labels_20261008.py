"""Write an additive F3.1.E1 projection correcting R5.2 test labels only."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "PREREGISTRO_FASE9_V2_R5_2_F31_20261008.json"
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F3.1\AUDITORIA_F3_1_C1_a9f3787c.md")
PINS = {
    SOURCE: "6b6769da821b03dd96728202b478d3c0920b51f68cb6ca013916899390c517cd",
    AUDIT: "b3bcd f5f7b33fc957731d83c15b62b5315085f066a844672d81f8fcafa79ef20".replace(" ", ""),
}
OLD = "TGL_FASE9_RAZAO_DE_HUBBLE_V2_R5_DRAFT__"
NEW = "TGL_FASE9_RAZAO_DE_HUBBLE_V2_R5_2_DRAFT__"
ERROR = "ValueError:INVALID_NUMERIC_INPUT:r.dispersao_endpoints.minimum.p"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(obj: object) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty(obj: object) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def pin(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    actual = sha(data)
    if path in PINS and actual != PINS[path]:
        raise ValueError(f"source pin changed: {path}: {actual}")
    return {"path": str(path), "sha256": actual, "bytes": len(data)}


def write_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(path)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as output:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())
        if Path(temporary).stat().st_size != len(data):
            raise OSError("temporary size mismatch")
        os.replace(temporary, path)
        if path.read_bytes() != data:
            raise OSError("written bytes differ")
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def baseline() -> dict:
    return {
        "fundo": "BG1", "n_local": 5, "n_alvos_declarados": 0,
        "required_sources_admitted": True, "beta_livre_no_limite": False,
        "use_novel_parametros": True,
        "dispersao_endpoints": {
            "minimum": {"chi2_por_gl": 1.0, "p": 0.5},
            "maximum": {"chi2_por_gl": 1.0, "p": 0.5},
        },
        "minimum": {"z_delta": 0.5, "sigma_z_por_alvo": [(1.04, 0.0)]},
        "maximum": {"poder_previo": 6.0, "z_disc": 6.2, "lnB_lcdm": 6.0,
                    "lnB_livre": 0.0, "lnB_shift": 2.0,
                    "lnB_fundo_livre": 0.5, "poder_nao_cefeida": 4.0},
    }


def build() -> dict[str, bytes]:
    sources = {"r5_2_registered": pin(SOURCE), "audit_a9f3787c": pin(AUDIT)}
    previous = json.loads(SOURCE.read_text(encoding="utf-8"))
    spec_old = previous["spec"]
    assert previous["spec_sha256"] == sha(compact(spec_old))
    fn_old = spec_old["funcao_de_veredito"]["fonte"]
    fn_hash = spec_old["funcao_de_veredito"]["sha256"]
    assert sha(fn_old.encode("utf-8")) == fn_hash
    before = spec_old["funcao_de_veredito"]["testes_sinteticos_de_ramo"]
    if len(before) != 20 or sum(OLD in v for v in before.values()) != 20:
        raise ValueError("expected exactly 20 inherited R5 test labels")
    if "dispersion_invalid_p" not in before:
        raise ValueError("numeric rejection row missing")

    after = {name: (ERROR if name == "dispersion_invalid_p" else token.replace(OLD, NEW, 1))
             for name, token in before.items()}
    if any(OLD in value for value in after.values()):
        raise AssertionError("old label remains")
    if sum(value.startswith(NEW) for value in after.values()) != 19:
        raise AssertionError("unexpected token count")
    if after["dispersion_invalid_p"] != ERROR:
        raise AssertionError("invalid p misclassified")

    projection = copy.deepcopy(previous)
    projection["derived_from"] = sources["r5_2_registered"]
    projection["integration_note"] = (
        "F3.1.E1: 19 valid inherited branch tokens relabeled from V2_R5_DRAFT to "
        "V2_R5_2_DRAFT; the twentieth, dispersion_invalid_p, is a visible ValueError "
        "under the unchanged R5.2 numeric guard. This is documentary only and "
        "must be audited before any downstream pin moves."
    )
    projection["spec"]["funcao_de_veredito"]["testes_sinteticos_de_ramo"] = after
    projection["spec_sha256"] = sha(compact(projection["spec"]))
    assert projection["spec"]["funcao_de_veredito"]["fonte"] == fn_old
    assert projection["spec"]["funcao_de_veredito"]["sha256"] == fn_hash
    spec_without_tests = copy.deepcopy(projection["spec"])
    spec_without_tests["funcao_de_veredito"]["testes_sinteticos_de_ramo"] = before
    assert spec_without_tests == spec_old

    namespace: dict = {}
    exec(compile(fn_old, "<F3.1.E1-R5.2-verdict>", "exec"), namespace)
    decide = namespace[spec_old["funcao_de_veredito"]["nome"]]
    valid_token = decide(baseline())
    if valid_token != after["free_background_suffix"]:
        raise AssertionError("valid branch token does not match function")
    invalid = baseline()
    invalid["dispersao_endpoints"]["minimum"]["p"] = float("nan")
    try:
        decide(invalid)
    except ValueError as exc:
        if "ValueError:" + str(exc) != ERROR:
            raise AssertionError("numeric rejection changed") from exc
    else:
        raise AssertionError("invalid p produced a token")

    spec_name = "PREREGISTRO_FASE9_V2_R5_2_F31_LABELS_E1_20261008.json"
    test_name = "TESTE_F31_E1_LABELS_20261008.json"
    note_name = "ERRATA_F31_E1_LABELS_R5_2_20261008.md"
    result_name = "RESULTADO_F31_E1_LABELS_20261008.json"
    outputs = {
        spec_name: pretty(projection),
        test_name: pretty({
            "schema": "F31_E1_LABEL_TEST_V1", "old_labels": 20,
            "new_r5_2_tokens": 19, "numeric_rejection_rows": 1,
            "valid_branch_exact_match": True, "invalid_p_visible_rejection": True,
            "function_sha256_unchanged": fn_hash, "spec_sha256": projection["spec_sha256"],
            "real_data_opened": False,
        }),
        note_name: (
            "# F3.1.E1 — errata aditiva dos rótulos R5.2\n\n"
            "[REAL documental] A spec pinada R5.2 conserva 20 rótulos `V2_R5_DRAFT` "
            "na tabela de testes, embora a função pinada emita `V2_R5_2_DRAFT`. "
            "Nesta projeção, 19 tokens recebem o rótulo vigente. O caso "
            "`dispersion_invalid_p` passa a registrar o `ValueError` que a função de fato "
            "lança antes da precedência. A fonte e o hash da função científica permanecem "
            "idênticos aos da R5.2.\n\n"
            "[OPEN] X13 e D-H antes do congelamento; d72 e abertura como atos separados. "
            "O fator SBF 0,031 segue sem origem bibliográfica verificada. Nenhum dado real "
            "foi aberto e nenhum gate mudou.\n"
        ).encode("utf-8"),
    }
    result = {
        "schema": "F31_E1_LABEL_RESULT_V1", "unit": "F3.1.E1",
        "status": "ENTREGUE_PARA_AUDITORIA_C1", "sources": sources,
        "generator": pin(Path(__file__)),
        "new_artifacts": {name: {"sha256": sha(data), "bytes": len(data)} for name, data in outputs.items()},
        "old_labels_removed": 20, "new_r5_2_tokens": 19, "numeric_rejection_rows": 1,
        "scalar_spec_sha256": projection["spec_sha256"],
        "scientific_verdict_function_sha256_unchanged": fn_hash,
        "real_data_opened": False, "frozen": False, "gate_changed": False,
    }
    outputs[result_name] = pretty(result)
    return outputs


def main() -> None:
    outputs = build()
    check = "--check" in sys.argv[1:]
    for name, data in outputs.items():
        path = HERE / name
        if check:
            if path.read_bytes() != data:
                raise AssertionError(f"generated bytes differ: {path}")
        else:
            write_new(path, data)
    print(json.dumps({"mode": "check" if check else "create",
                      "artifacts": {name: sha(data) for name, data in outputs.items()}}, indent=2))


if __name__ == "__main__":
    main()
