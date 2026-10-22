"""Build an additive v394 coverage patch from a prior, pinned whole-kernel audit.

Never imports/runs um.py. No fallback counts and no runtime-derived expectation.
Contract schema is documented by validate_contract. Output paths must be new.
"""
from pathlib import Path
import argparse
import ast
import copy
import datetime as dt
import hashlib
import json
import os
import pprint
import re

SCHEMA = "tgl-v394-whole-kernel-coverage/v1"

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def exclusive(path, raw):
    path = Path(path)
    tmp = path.with_name(path.name + ".tmp")
    if path.exists() or tmp.exists():
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tmp.open("xb") as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    if tmp.stat().st_size != len(raw):
        raise RuntimeError("Short write")
    tmp.rename(path)

def literal(tree, name):
    nodes = [n for n in tree.body if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)]
    if len(nodes) != 1:
        raise ValueError(f"Expected one literal assignment: {name}")
    return nodes[0], ast.literal_eval(nodes[0].value)

def validate_contract(c, embedded):
    if c.get("schema") != SCHEMA or c.get("version") != "v394":
        raise ValueError("Wrong coverage contract schema/version")
    if c.get("whole_closure_audit") is not True or c.get("audit_exit_code") != 0:
        raise ValueError("A successful, whole-closure pre-audit is required")
    for key in ("decl", "thm", "axiom_report_entries", "nao_lidas_pelo_regex", "fora_do_trio", "sorryAx_no_log_do_audit"):
        if type(c.get(key)) is not int or c[key] < 0:
            raise ValueError(f"Non-negative non-boolean integer required: {key}")
    if not (c["decl"] >= c["thm"] > 0 and c["decl"] - c["axiom_report_entries"] == c["nao_lidas_pelo_regex"]):
        raise ValueError("Inconsistent pre-audit counts")
    if c["fora_do_trio"] or c["sorryAx_no_log_do_audit"]:
        raise ValueError("New axioms or sorryAx in pre-audit")
    embedded_files = {name: digest(text.encode("utf-8")) for name, text in embedded.items()}
    expected_files = c.get("formal_files_sha256")
    if not isinstance(expected_files, dict) or any(expected_files.get(k) != v for k, v in embedded_files.items()):
        raise ValueError("The pre-audited source set differs from the complete embedded source set")
    extras = set(expected_files) - set(embedded_files)
    if not extras <= {"_check_damming.lean"}:
        raise ValueError("Only the explicitly pinned historical _check_damming.lean is permitted as an extra")
    extra_meta = c.get("additional_formal_sources", {})
    if set(extra_meta) != extras:
        raise ValueError("Extra materialized formal sources require explicit provenance")
    for key in extras:
        meta = extra_meta[key]
        if digest(Path(meta["path"]).read_bytes()) != expected_files[key] or not meta.get("reason"):
            raise ValueError(f"Additional formal source pin/provenance failed: {key}")
    for key in ("audit_log", "audit_receipt"):
        meta = c[key]
        raw = Path(meta["path"]).read_bytes()
        if digest(raw) != meta["sha256"]:
            raise ValueError(f"Pre-audit artifact pin mismatch: {key}")
    log = Path(c["audit_log"]["path"]).read_text(encoding="utf-8")
    if "sorryAx" in log:
        raise ValueError("sorryAx text present in audit log")
    return expected_files

def compose(source, contract, contract_path, contract_raw):
    tree = ast.parse(source)
    embedded_node, embedded = literal(tree, "_EMBEDDED_KERNEL_FILES")
    expected_files = validate_contract(contract, embedded)
    specs_node, specs = literal(tree, "_V393_SPECS")
    names_node, names = literal(tree, "_V393_NOMES_REGISTROS")
    sources_node, sources = literal(tree, "_V393_FONTES")
    historical = next(s for s in specs if s["nome"] == "kh_n1_cobertura_v393")
    original = copy.deepcopy(historical)
    for ck in historical["checks"]:
        if ck["id"] in ("h2", "h3"):
            ck["op"] = "maior_igual"
            ck["descricao"] = "Compatibilidade por inclusao na v394: piso historico v393; nao revalida a contagem exata v393"
    historical["veredito_sufixo"] = "HISTORICAL_V393_PIN_AND_INCLUSION_FLOOR_CHECKED__EXACT_CURRENT_COUNTS_ARE_IN_KH_N1_V394__GATE_UNMOVED"
    historical["estatuto"] = "[REAL] recibo historico v393 preservado; na v394 h2/h3 verificam inclusao por pisos, nao a igualdade da contagem antiga"
    historical["extras"]["v393_original_spec_preserved"] = original
    historical["erratas"].append({"ao_lado_de": "h2/h3 da cobertura v393",
        "agora": "Pisos de compatibilidade por inclusao; igualdades exatas da copia atual cobradas no registro v394 com pre-auditoria pinada.",
        "estatuto": "[DERIVED] escopo de compatibilidade explicito", "assinatura": "codex-gerente-tgl, F1.FECHO_20261015, claim845"})
    historical["diz"] = ["o recibo historico v393 confere e a cobertura atual inclui os pisos v393; a igualdade atual e cobrada separadamente na v394"]
    def check(identifier, path, expected, op="igual"):
        return {"id": identifier, "descricao": "Comparacao com a pre-auditoria integral v394 pinada antes do rito",
                "onde": "kf", "caminho": path, "op": op, "valor": expected, "estatuto": "[REAL]"}
    current = {"nome": "kh_n1_cobertura_v394", "veredito_prefixo": "TGL_KH_N1_COBERTURA_V394",
        "veredito_sufixo": "EXACT_PREAUDITED_CLOSURE_AND_SOURCES_MATCH__NONE_OUTSIDE_THE_TRIO__GATE_UNMOVED",
        "estatuto": "[REAL] totais exatos e conjunto integral de fontes pre-medidos antes do rito; a rodada atual apenas os verifica",
        "fontes": ["kh_n1_v394"], "kernel_flags": [], "kernel_decls": [],
        "checks": [check("h1", ["axiom_coverage_v392", "ok"], True, "verdadeiro"),
                   *[check("h_" + key, ["axiom_coverage_v392", key], contract[key])
                     for key in ("decl", "thm", "fora_do_trio", "nao_lidas_pelo_regex")],
                   check("h_report_exact", ["axiom_report"], contract["axiom_report_entries"], "tamanho_igual"),
                   check("h_sources_exact", ["formal_files_sha256"], expected_files),
                   check("h_forbidden_absent", ["source_forbidden_tokens_absent"], True, "verdadeiro")],
        "erratas": [], "limites": ["validade no kernel nao e creditacao; nenhum gate se move", "nao redefine a expectativa pelos valores do proprio rito"],
        "diz": ["o Audit desta rodada cobriu exatamente as fontes e os totais pre-auditados da copia v394"],
        "nao_diz": ["que o resultado matematico seja uma medicao fisica"], "leituras_do_operador": [],
        "extras": {"preaudit_contract_sha256": digest(contract_raw), "signature": "codex-gerente-tgl, claim845"}}
    specs.append(current)
    names.append(current["nome"])
    sources["kh_n1_v394"] = {"arquivo": str(Path(contract_path).resolve()), "bytes": len(contract_raw),
        "sha256": digest(contract_raw), "papel": "pre-auditoria integral imutavel da copia v394, anterior ao rito"}
    replacements = [(specs_node, "_V393_SPECS", specs), (names_node, "_V393_NOMES_REGISTROS", names),
                    (sources_node, "_V393_FONTES", sources)]
    lines = source.splitlines(keepends=True)
    spans = []
    for node, name, value in sorted(replacements, key=lambda x: x[0].lineno, reverse=True):
        before = "".join(lines[node.lineno - 1:node.end_lineno])
        after = name + " = " + pprint.pformat(value, width=140, sort_dicts=False) + "\n"
        lines[node.lineno - 1:node.end_lineno] = [after]
        spans.append({"name": name, "start_line": node.lineno, "end_line": node.end_lineno,
                      "before_sha256": digest(before.encode()), "after_sha256": digest(after.encode()),
                      "before_ast_sha256": digest(ast.dump(node, include_attributes=False).encode())})
    result = "".join(lines)
    ast.parse(result)
    return result, {"original_v393_coverage_spec": original, "replacements": spans,
                    "embedded_source_count": len(embedded), "contract_sha256": digest(contract_raw)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True); ap.add_argument("--contract", required=True)
    ap.add_argument("--destination", required=True); ap.add_argument("--receipt", required=True)
    args = ap.parse_args()
    for target in (Path(args.destination), Path(args.receipt)):
        if target.exists(): raise FileExistsError(target)
    raw = Path(args.source).read_bytes(); contract_raw = Path(args.contract).read_bytes()
    new, detail = compose(raw.decode("utf-8"), json.loads(contract_raw), args.contract, contract_raw)
    new_raw = new.encode("utf-8")
    exclusive(args.destination, new_raw)
    receipt = {"unit": "F1.FECHO_20261015", "claim": 845, "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source": str(Path(args.source).resolve()), "source_sha256": digest(raw),
        "destination": str(Path(args.destination).resolve()), "destination_sha256": digest(new_raw),
        "scope": "AST data assignments only; no program execution or expectation derived from the upcoming rite", **detail}
    exclusive(args.receipt, (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode())
    print(json.dumps({"receipt": args.receipt, "destination_sha256": digest(new_raw)}))

if __name__ == "__main__":
    main()
