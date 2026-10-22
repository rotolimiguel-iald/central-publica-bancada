"""PROPOSAL for v372: custody readers, not new mathematics or a gate decision.

Place beside P1_QUADRO.json and P2_COMPILACAO.json in the sealed package.
Every counted predicate has an executed negative control. Identities created
by definitions are reported separately. Management must ratify exact types.
"""
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
TRIO = frozenset({"propext", "Classical.choice", "Quot.sound"})
# Set by the incorporating management module, outside this sealed package.
# Embedding PRONTO's own hash in a file hashed by PRONTO would be circular.
EXPECTED_MANAGEMENT_PACKAGE_SHA256 = None


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _inside(relative):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError("ARTIFACT_OUTSIDE_PACKAGE")
    return path


def _check(name, predicate, actual, negative, description):
    return {
        "name": name,
        "passed": bool(predicate(actual)),
        "negative_control_passed": not bool(predicate(negative)),
        "description": description + " | CONTROLE: " + name + " adulterado deve falhar",
    }


def _read_stone(item, ONE):
    """Engineering acceptance only. Never infer physical discharge from rc=0."""
    try:
        if not EXPECTED_MANAGEMENT_PACKAGE_SHA256:
            return {"item": item, "all_verified": False,
                    "verdict": "MANAGEMENT_PIN_REQUIRED", "gate_changed": False}
        ready_path = ROOT / "PRONTO.json"
        if _sha(ready_path) != EXPECTED_MANAGEMENT_PACKAGE_SHA256:
            raise ValueError("MANAGEMENT_PIN_MISMATCH")
        ready = json.loads(ready_path.read_bytes())
        for name in ("P1_QUADRO.json", "P2_COMPILACAO.json", "CONSTANTS.json"):
            if _sha(ROOT / name) != ready["files"][name]:
                raise ValueError("PACKAGE_INDEX_HASH_MISMATCH: " + name)
        index = json.loads((ROOT / "P1_QUADRO.json").read_bytes())
        row = next(x for x in index["items"] if x["item"] == item)
        compilation = json.loads((ROOT / "P2_COMPILACAO.json").read_bytes())
        units = [x for x in compilation["units"]
                 if x.get("item") == item or item in x.get("also_items", [])]
        constants = json.loads((ROOT / "CONSTANTS.json").read_bytes())
        ALPHA_FINE_CODATA_2018 = constants["ALPHA_FINE_CODATA_2018"]
        beta_tgl = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
        checks = [_check("inscription", lambda x: type(x) in (int, float) and x == 1,
                         ONE, 0, "Inscrição externa do Um; não é evidência científica")]
        usable = [u for u in units if u.get("rc") == 0]
        checks.append(_check("nonempty_evidence", bool, usable, [],
                             "Existência de unidades recompiladas no item"))
        for unit in units:
            module = unit["module"]
            checks.append(_check(module + ":rc", lambda x: type(x) is int and x == 0,
                                 unit.get("rc"), 1, "Código real do compilador"))
            for kind in ("source", "log", "receipt"):
                actual = _sha(_inside(unit[kind]))
                expected = unit[kind + "_sha256"]
                if expected != ready["files"][unit[kind]]:
                    raise ValueError("UNIT_MANIFEST_DISAGREES_WITH_PINNED_PACKAGE")
                checks.append(_check(module + ":" + kind, lambda x, a=actual: a == x,
                                     expected, "0" * 64, "Custódia SHA256 " + kind))
            receipt_data = json.loads(_inside(unit["receipt"]).read_bytes())
            receipt_matches = lambda x: isinstance(x, dict) and type(x.get("rc")) is int and (
                x["rc"] == unit["rc"] == 0 and
                x.get("source_sha256") == unit["source_sha256"] and
                x.get("log_sha256") == unit["log_sha256"])
            checks.append(_check(module + ":receipt_binding", receipt_matches,
                receipt_data, dict(receipt_data, rc=1), "Índice cruzado com o recibo real"))
            log_axioms = {}
            log_kinds = {}
            for line in _inside(unit["log"]).read_text("utf-8").splitlines():
                if line.startswith("BENCH_DECL\t"):
                    _, name, kind, names = line.split("\t")
                    if kind == "axiom" or name in log_axioms:
                        raise ValueError("INVALID_DECLARATION_AUDIT")
                    log_axioms[name] = list(filter(None, names.split(",")))
                    log_kinds[name] = kind
            axioms = unit.get("axioms")
            checks.append(_check(module + ":axiom_log_binding", lambda x: x == log_axioms,
                axioms, {"tampered": ["sorryAx"]}, "Índice cruzado com as declarações do log"))
            checks.append(_check(module + ":declaration_count", lambda x: type(x) is int and x == len(log_axioms),
                unit.get("audited_declaration_count"), len(log_axioms) + 1, "Contagem das declarações efetivamente exportadas, inclusive auxiliares importados"))
            checks.append(_check(module + ":declaration_kinds", lambda x: x == log_kinds,
                unit.get("declaration_kinds"), {"tampered": "axiom"}, "Tipo de cada declaração cruzado com o log"))
            predicate = lambda x: isinstance(x, dict) and bool(x) and all(
                isinstance(v, list) and set(v) <= TRIO for v in x.values())
            # Pure import/audit adapters have no new declarations. Their type
            # queries are checked by compilation; no vacuous axiom check counted.
            if log_axioms:
                checks.append(_check(module + ":axioms", predicate, axioms,
                    {"tampered": ["sorryAx"]}, "Axiomas de todas as declarações próprias"))
        all_verified = all(c["passed"] and c["negative_control_passed"] for c in checks)
        return {
            "item": item, "statute": row["status"],
            "all_verified": all_verified,
            "all_verified_scope": "ARTIFACT_CUSTODY_AND_COMPILATION_CONTROLS_ONLY",
            "checks": checks,
            "identities_by_construction": row.get("identities_by_construction", []),
            "named_open_hypotheses": row.get("named_open_hypotheses", []),
            "beta_tgl": beta_tgl,
            "verdict": "BENCH_ARTIFACT_CHECKED" if all_verified else "BENCH_ARTIFACT_REFUSED",
            "physical_contract_inhabitant": False,
            "gate_changed": False,
        }
    except (OSError, ValueError, KeyError, TypeError, StopIteration) as exc:
        return {"item": item, "all_verified": False, "verdict": "BENCH_READ_FAILURE",
                "error": type(exc).__name__ + ": " + str(exc), "gate_changed": False}


def prove_a0_preconditions_v372(ONE): return _read_stone("A0", ONE)
def prove_a1_local_contract_v372(ONE): return _read_stone("A1", ONE)
def prove_a2_operator_transform_v372(ONE): return _read_stone("A2", ONE)
def prove_a3_orbital_geometry_v372(ONE): return _read_stone("A3", ONE)
def prove_a4_kms_calibration_v372(ONE): return _read_stone("A4", ONE)
def prove_a5_teleological_response_v372(ONE): return _read_stone("A5", ONE)
def prove_a6_equation_of_truth_v372(ONE): return _read_stone("A6", ONE)
def prove_a7_interacting_scope_v372(ONE): return _read_stone("A7", ONE)
def prove_a8_exact_reader_v372(ONE): return _read_stone("A8", ONE)
def prove_c1_canonical_reproduction_v372(ONE): return _read_stone("C1", ONE)
def prove_c2_strip_width_v372(ONE): return _read_stone("C2", ONE)
def prove_c3_integrated_truth_v372(ONE): return _read_stone("C3", ONE)
def prove_c4_transverse_cocycle_v372(ONE): return _read_stone("C4", ONE)
def prove_c5_regional_kms_scope_v372(ONE): return _read_stone("C5", ONE)
def prove_c6_ward_scope_v372(ONE): return _read_stone("C6", ONE)
def prove_d1prime_photon_characters_v372(ONE): return _read_stone("D1prime", ONE)
def prove_d2prime_maxwell_tensor_v372(ONE): return _read_stone("D2prime", ONE)
def prove_d3prime_conjugated_form_v372(ONE): return _read_stone("D3prime", ONE)
def prove_d4_name_weight_v372(ONE): return _read_stone("D4", ONE)
def prove_d5_dilation_v372(ONE): return _read_stone("D5", ONE)
def prove_d6_content_recognition_v372(ONE): return _read_stone("D6", ONE)
