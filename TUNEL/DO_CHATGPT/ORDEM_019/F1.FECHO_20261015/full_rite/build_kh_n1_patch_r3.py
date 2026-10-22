"""R3: build an additive v394 coverage patch from a prior, pinned whole-kernel audit.

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


def read_pinned(meta, label):
    raw = Path(meta["path"]).read_bytes()
    if digest(raw) != meta["sha256"] or ("bytes" in meta and len(raw) != meta["bytes"]):
        raise ValueError(f"Artifact pin mismatch: {label}")
    return raw


def parse_audit_log(log):
    """Rebuild runtime, broad-receipt and complete reports from the actual log."""
    trio = {"propext", "Classical.choice", "Quot.sound"}
    totals = re.findall(r"(?m)^TGL_AXIOM_COVERAGE_TOTAL decl=([0-9]+) thm=([0-9]+) fora_do_trio=([0-9]+)\s*$", log)
    if len(totals) != 1:
        raise ValueError("Exactly one whole-kernel TOTAL line is required")
    decl, thm, outside = map(int, totals[0])
    if not (decl >= thm > 0):
        raise ValueError("Invalid TOTAL counts")
    reports = {}
    for label, name_regex in (("runtime", r"[\w.']+"), ("receipt", r"[^']+"), ("complete", r"[^\r\n]+")):
        report = {}
        pattern = "'(" + name_regex + r")' depends on axioms:\s*\[([^]]*)\]"
        for name, values in re.findall(pattern, log, re.S):
            axioms = [v.strip() for v in values.replace("\n", " ").split(",") if v.strip()]
            if name in report and set(report[name]) != set(axioms):
                raise ValueError("Conflicting axiom rows for " + name)
            report[name] = axioms
        for name in re.findall("'(" + name_regex + ")' does not depend on any axioms", log):
            if name in report and report[name]:
                raise ValueError("Conflicting axiom-free row for " + name)
            report.setdefault(name, [])
        reports[label] = report
    unread = len(re.findall(r"(?m)^'[^'\n]*[\u00ab\u00bb][^'\n]*' (?:depends on axioms|does not depend on any axioms)", log))
    parsed_outside = {n: a for n,a in reports["complete"].items() if not set(a) <= trio}
    if "sorryAx" in log or "Lean.trustCompiler" in log or outside or parsed_outside:
        raise ValueError("Audit includes an axiom outside the allowed trio")
    if len(reports["complete"]) != decl or len(reports["runtime"]) + unread != decl:
        raise ValueError("TOTAL does not agree with parsed declaration rows")
    return {"decl": decl, "thm": thm, "fora_do_trio": outside,
            "axiom_report_entries": len(reports["runtime"]), "nao_lidas_pelo_regex": unread,
            "sorryAx_no_log_do_audit": 0, "reports": reports}


def validate_contract(c, embedded):
    if c.get("schema") != SCHEMA or c.get("version") != "v394":
        raise ValueError("Wrong coverage contract schema/version")
    if c.get("whole_closure_audit") is not True or type(c.get("audit_exit_code")) is not int or c["audit_exit_code"] != 0:
        raise ValueError("A successful, whole-closure pre-audit is required")
    keys = ("decl", "thm", "axiom_report_entries", "nao_lidas_pelo_regex", "fora_do_trio", "sorryAx_no_log_do_audit")
    for key in keys:
        if type(c.get(key)) is not int or c[key] < 0:
            raise ValueError(f"Non-negative non-boolean integer required: {key}")
    embedded_files = {name: digest(text.encode("utf-8")) for name, text in embedded.items()}
    expected_files = c.get("formal_files_sha256")
    if not isinstance(expected_files, dict) or any(expected_files.get(k) != v for k,v in embedded_files.items()):
        raise ValueError("Pre-audited source set differs from the complete embedded source set")
    extras = set(expected_files) - set(embedded_files)
    if not extras <= {"_check_damming.lean"}:
        raise ValueError("Unexpected additional formal source")
    extra_meta = c.get("additional_formal_sources", {})
    if set(extra_meta) != extras:
        raise ValueError("Additional formal sources require explicit provenance")
    for key in extras:
        if digest(Path(extra_meta[key]["path"]).read_bytes()) != expected_files[key] or not extra_meta[key].get("reason"):
            raise ValueError("Additional source pin/provenance failed: " + key)
    log_raw = read_pinned(c["audit_log"], "audit log")
    parsed = parse_audit_log(log_raw.decode("utf-8"))
    if any(c[key] != parsed[key] for key in keys):
        raise ValueError("Contract counts do not match counts reconstructed from the actual audit log")
    audit = json.loads(read_pinned(c["audit_receipt"], "audit receipt"))
    if audit.get("module") != "TGL/Audit" or type(audit.get("exit_code")) is not int or audit["exit_code"] != 0 or audit.get("passed") is not True:
        raise ValueError("Audit receipt is not a successful TGL/Audit build")
    if read_pinned(audit["stdout"], "audit stdout") != log_raw:
        raise ValueError("Audit receipt points to different output bytes")
    if audit.get("axiom_report") != parsed["reports"]["receipt"]:
        raise ValueError("Audit receipt axiom report differs from its reconstructed grammar")
    if digest(read_pinned(audit["source"], "TGL/Audit source")) != expected_files["TGL/Audit.lean"]:
        raise ValueError("Audit was compiled from another Audit source")
    command = audit.get("command", [])
    if not command or Path(command[-1]).resolve() != Path(audit["source"]["path"]).resolve():
        raise ValueError("Audit command does not name the pinned Audit source")
    measured = json.loads(read_pinned(c["measured_coverage_receipt"], "whole closure receipt"))
    if measured.get("passed") is not True:
        raise ValueError("Whole closure pre-audit failed")
    for k, parsed_key in (("total_declarations", "decl"), ("total_theorems", "thm"), ("outside_trio", "fora_do_trio")):
        if type(measured.get(k)) is not int or measured[k] != parsed[parsed_key]:
            raise ValueError("Whole closure totals do not match the actual log: " + k)
    if measured.get("axiom_report_count") != len(parsed["reports"]["receipt"]):
        raise ValueError("Whole closure receipt report count does not match its parser")
    builds = [json.loads(read_pinned(meta, "whole closure build")) for meta in measured["builds"]]
    if {b.get("module") for b in builds} != {"TGLExt", "TGL/Audit"} or len(builds) != 2:
        raise ValueError("Both aggregate roots must be compiled")
    if not any(b == audit for b in builds):
        raise ValueError("Pinned Audit is not part of the whole-closure build set")
    for b in builds:
        if type(b.get("exit_code")) is not int or b["exit_code"] != 0 or b.get("passed") is not True:
            raise ValueError("A root build failed")
        key = b["module"] + ".lean"
        if digest(read_pinned(b["source"], "root source")) != expected_files[key]:
            raise ValueError("Whole closure root source mismatch: " + key)
        if read_pinned(b["source"], "root source") != read_pinned(measured["sources"][b["module"]], "measured root source"):
            raise ValueError("Whole closure source record mismatch")
        read_pinned(b["stdout"], "root stdout"); read_pinned(b["stderr"], "root stderr")
        read_pinned(b["object"], "root olean")
    prepared = json.loads(read_pinned(measured["prepared"], "prepared source closure"))
    compiled = json.loads(read_pinned(measured["compiled_bundle"], "compiled bundle"))
    if compiled.get("passed") is not True or compiled.get("plan") != prepared.get("plan"):
        raise ValueError("Compiled bundle and prepared closure are not the same plan")
    plan = json.loads(read_pinned(prepared["plan"], "bundle plan"))
    if plan.get("baseline") != prepared.get("baseline"):
        raise ValueError("Prepared closure and bundle have different baselines")
    baseline = read_pinned(prepared["baseline"], "pre-audit baseline program")
    _, baseline_embedded = literal(ast.parse(baseline.decode("utf-8")), "_EMBEDDED_KERNEL_FILES")
    reconstructed = {k: digest(v.encode("utf-8")) for k,v in baseline_embedded.items()}
    modules = compiled.get("modules", [])
    expected_modules = {row["module"]: row["transposed_source"] for row in plan["modules"]}
    expected_modules[plan["audit_module"]] = plan["audit"]
    if len(modules) != len(expected_modules) or {r.get("module") for r in modules} != set(expected_modules):
        raise ValueError("Compiled module set differs from the pre-audited plan")
    for row in modules:
        if row.get("passed") is not True or type(row.get("exit_code")) is not int or row["exit_code"] != 0:
            raise ValueError("Compiled bundle contains a failed module")
        if row["source"] != expected_modules[row["module"]]:
            raise ValueError("Compiled module source differs from the plan")
        raw_source = read_pinned(row["source"], "compiled module source")
        read_pinned(row["object"], "compiled module object")
        read_pinned(row["stdout"], "compiled module stdout")
        read_pinned(row["stderr"], "compiled module stderr")
        reconstructed[row["module"].replace(".", "/") + ".lean"] = digest(raw_source)
    for root in ("TGLExt", "TGL/Audit"):
        root_raw = read_pinned(prepared["sources"][root], "prepared root")
        if root_raw != read_pinned(measured["sources"][root], "measured root"):
            raise ValueError("Prepared and measured roots differ")
        reconstructed[root + ".lean"] = digest(root_raw)
    if reconstructed != embedded_files:
        raise ValueError("Embedded sources do not equal the baseline plus the actually compiled additions and roots")
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
