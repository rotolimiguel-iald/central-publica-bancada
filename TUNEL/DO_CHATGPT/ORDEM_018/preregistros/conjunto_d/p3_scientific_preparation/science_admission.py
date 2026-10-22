"""Pure admission for a future exact synthetic P3 decision; no scientific imports."""
import hashlib
import json
import os
from pathlib import Path
import sys
import uuid

PREPARATION_ID = "3249312d-d7b6-4a04-93d6-81f65d4f4945"
EXPECTED_LINUX_ROOT = "/mnt/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/p3_scientific_preparation"
ACTION = "EXECUTE_EXACT_TWO_SYNTHETIC_JOBS"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _hash(value):
    if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise ValueError("Canonical SHA256 required")
    return value


def _check_file(path, row):
    data = Path(path).read_bytes()
    if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
        raise ValueError("Exact input bytes differ: " + str(path))


def admit(root, contract_hash, decision_hash, *, job_id=None):
    root = Path(root).resolve()
    _hash(contract_hash)
    _hash(decision_hash)
    if sys.platform != "linux" or not sys.flags.isolated or not sys.dont_write_bytecode:
        raise RuntimeError("Isolated Linux -I -B invocation required")
    if os.getuid() != 65534 or os.geteuid() != 65534:
        raise RuntimeError("Existing nobody identity required; never change account")
    if root != Path(EXPECTED_LINUX_ROOT):
        raise ValueError("Scientific package root binding differs")
    cp = root / "CONTRATO_P3.json"
    dp = root / "ROOT_DECISION.json"
    if digest(cp) != contract_hash or digest(dp) != decision_hash:
        raise ValueError("Pinned contract/ROOT decision required")
    contract = json.loads(cp.read_bytes())
    decision = json.loads(dp.read_bytes())
    keys = {"approved", "action", "preparation_id", "execution_id", "contract_sha256",
            "manifest_sha256", "root_linux", "execution_directory", "jobs", "data_access"}
    if set(decision) != keys:
        raise ValueError("Exact external ROOT decision schema required")
    if (decision["approved"] is not True or decision["action"] != ACTION
            or decision["preparation_id"] != PREPARATION_ID
            or contract["preparation_id"] != PREPARATION_ID
            or contract["state"] != "PREPARED_NOT_EXECUTED"
            or contract["mode"] != "SYNTHETIC_ONLY"
            or contract["observed_data_allowed"] is not False):
        raise ValueError("Only this exact future synthetic qualification can be admitted")
    if contract["consumption_justification"]["status"] != "JUSTIFIED_BY_SEPARATE_REVIEW":
        raise RuntimeError("NOT_JUSTIFIED_UNDER_INHERITED_ENVELOPE: new reviewed contract required")
    execution_id = decision["execution_id"]
    if not isinstance(execution_id, str) or str(uuid.UUID(execution_id)) != execution_id:
        raise ValueError("Fresh canonical execution UUID required")
    planned = [job["id"] for job in contract["jobs"]]
    if (len(planned) != 2 or len(set(planned)) != 2 or decision["jobs"] != planned
            or [job["label"] for job in contract["jobs"]] != ["GR_GAUSS", "RB_GAUSS"]):
        raise ValueError("Only the two ordered frozen synthetic cases")
    if job_id is not None and job_id not in planned:
        raise ValueError("Unregistered job")
    if (decision["contract_sha256"] != contract_hash
            or decision["root_linux"] != str(root)
            or contract["expected_linux_root"] != str(root)
            or decision["execution_directory"] != contract["execution_directory"]
            or decision["data_access"] != "EXACT_PINNED_SYNTHETIC_AND_DECLARED_INITIALIZATION_INPUTS_ONLY"):
        raise ValueError("Root/output/data binding differs")
    run = root / contract["execution_directory"]
    if run.parent != root or run.name != contract["execution_directory"]:
        raise ValueError("Single exact execution directory required")
    manifest_path = root / "MANIFESTO_PREPARACAO.json"
    if digest(manifest_path) != _hash(decision["manifest_sha256"]):
        raise ValueError("Prepared package manifest differs")
    manifest = json.loads(manifest_path.read_bytes())
    if manifest["preparation_id"] != PREPARATION_ID:
        raise ValueError("Manifest preparation identity differs")
    seen = set()
    for row in manifest["files"]:
        path = (root / row["relative_path"]).resolve()
        if root not in path.parents or path in seen:
            raise ValueError("Manifest path outside package or duplicate")
        seen.add(path)
        _check_file(path, row)
    # External bytes are deliberately not inspected by preparation. They may be
    # read only in a separately approved future invocation after all bindings above.
    for name, row in contract["inputs"].items():
        _check_file((root / name).resolve(), row)
    interpreter = json.loads((root / "INTERPRETER_PIN.json").read_bytes())
    if Path(sys.executable).resolve() != Path(interpreter["path"]).resolve():
        raise ValueError("Interpreter identity differs")
    _check_file(sys.executable, interpreter)
    evidence = contract["imports_qualification_evidence"]
    accepted = json.loads((root / evidence["acceptance_relative_path"]).read_bytes())
    if (accepted.get("qualification_id") != evidence["qualification_id"]
            or accepted.get("status") != "ACCEPTED_IMPORTS_ONLY_COMPLETE_NOT_SCIENTIFIC_QUALIFICATION"
            or accepted.get("external_exit_code") != 0 or accepted.get("child_exit_code") != 0
            or accepted.get("PE_jobs") != 0 or accepted.get("scientific_functions_called") != 0):
        raise ValueError("Pinned prior imports evidence differs; it is not a live object")
    return contract, decision
