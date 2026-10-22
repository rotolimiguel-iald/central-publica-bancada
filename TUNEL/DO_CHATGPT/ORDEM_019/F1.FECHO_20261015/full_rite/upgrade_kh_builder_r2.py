"""Generate a new R2 builder; preserve the recorded R1 byte-for-byte."""
from pathlib import Path
import ast, hashlib, os
BASE = Path(__file__).resolve().parent
old = BASE / "build_kh_n1_patch_r1.py"
new = BASE / "build_kh_n1_patch_r2.py"
raw = old.read_bytes(); source = raw.decode("utf-8"); lines = source.splitlines(keepends=True)
node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == "validate_contract")
replacement = r'''
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
    read_pinned(prepared["plan"], "bundle plan")
    return expected_files
'''
lines[node.lineno-1:node.end_lineno] = [replacement + "\n"]
result = "".join(lines).replace("Build an additive v394 coverage patch", "R2: build an additive v394 coverage patch")
ast.parse(result)
with new.open("xb") as f:
    f.write(result.encode()); f.flush(); os.fsync(f.fileno())
assert old.read_bytes() == raw
print(new)
print(hashlib.sha256(new.read_bytes()).hexdigest())
