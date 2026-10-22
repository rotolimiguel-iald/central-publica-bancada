"""One read-only final custody check; creates reviewer evidence only."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import uuid

ROOT = Path(__file__).resolve().parent
REFERENCE = Path(r"C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json")
PINS = {}


def pin(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    value = {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest()}
    PINS[str(path)] = value
    return value


def read(name):
    p = ROOT / name
    pin(p)
    return json.loads(p.read_text(encoding="utf-8"))


def verify(item):
    assert pin(item["path"]) == {k: item[k] for k in ("path", "sha256")}, item


def new(path, value):
    assert not path.exists(), path
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temp = path.with_name(path.name + ".tmp_" + uuid.uuid4().hex)
    with temp.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert temp.read_bytes() == raw
    temp.rename(path)


def main():
    plan = read("MEMORY_PLAN_R57.json")
    review = read("MEMORY_REVIEW_R57.json")
    applied = read("MEMORY_APPLIED_R57.json")
    intent = read("MEMORY_INTENT_R57.json")
    registration = read("REGISTRATION_CONSOLIDATED_R57.json")
    delivery = read("DELIVERY_CONSOLIDATED_R57.json")
    assert applied["status"] == "APPLIED_VERIFIED"
    assert len(plan["surfaces"]) == len(applied["surfaces"]) == 8
    for p in [review["plan"], review["applier"], review["support"], applied["plan"], applied["review"],
              *intent.values(), *registration.values(), delivery["reference"], *delivery["evidence"]]:
        verify(p)
    preflight = json.loads(Path(intent["preflight"]["path"]).read_text(encoding="utf-8"))
    assert preflight["exit_code"] == 0 and preflight["result"]["ok"]
    expected = {row["path"]: row for row in plan["surfaces"]}
    assert len(expected) == 8
    surfaces = []
    for i, row in enumerate(applied["surfaces"]):
        p = Path(row["after"]["path"])
        planned = expected[str(p)]
        backup = Path(row["backup"]["path"])
        before = backup.read_bytes()
        after = p.read_bytes()
        extra = Path(row["append"]["path"]).read_bytes()
        assert backup.parent == p.parent
        assert row["before"] == planned["before"]
        assert len(before) == planned["before_bytes"]
        assert hashlib.sha256(before).hexdigest() == planned["before"]["sha256"]
        assert after == before + extra
        assert row["after"]["sha256"] == planned["after_sha256"]
        assert row["append"] == planned["append"]
        assert row["growth_bytes"] == len(extra) == len(after) - len(before)
        for field in ("after", "backup", "append"):
            verify(row[field])
        single = read(f"memory_surfaces/SURFACE_{i:02d}_R57.json")
        assert single == row
        surfaces.append({"destination": pin(p), "backup": pin(backup), "append": row["append"],
                         "before_bytes": len(before), "after_bytes": len(after), "growth_bytes": len(extra),
                         "same_directory_backup": True, "backup_equals_baseline": True,
                         "prefix_preserved": True, "exact_reviewed_append_only": True})

    map_result = read("MAP_REGISTER_CONSOLIDATED_R57_RESULT.json")
    board_result = read("BOARD_REGISTER_CONSOLIDATED_R57_RESULT.json")
    map_data = json.loads(map_result["stdout"])
    board_data = json.loads(board_result["stdout"])
    assert map_result["exit_code"] == board_result["exit_code"] == 0
    assert map_data["ok"] and board_data["ok"]
    assert board_data["unidade"] == "F1.FECHO_20261015" and board_data["para"] == "EM_CURSO"
    transition_path = ROOT / "receipts/FINAL_CUSTODY_TRANSITION_20261017T161326_495891Z_RESULT.json"
    request_path = ROOT / "receipts/FINAL_CUSTODY_TRANSITION_20261017T161326_495891Z_REQUEST.json"
    transition = read(transition_path)
    request = read(request_path)
    assert transition["exit_code"] == 0 and transition["result"]["ok"]
    transition_receipt = transition["result"]["result"]
    assert request["reference"] == str(REFERENCE)
    assert request["operation"] == "transition"
    for record in request["changes"]["records"]:
        for source in record["sources"]:
            assert source["kind"] == "artifact"
            assert pin(source["ref"])["sha256"] == source["sha256"]
    assert delivery["full_R4_satisfied"] is False and delivery["full_R5_satisfied"] is False
    assert (delivery["symbolic_checks"], delivery["axiom_reports"], delivery["lean_components"]) == (34, 37, 4)

    req = {"operation": "project", "reference": str(REFERENCE),
           "actor": {"kind": "agent", "id": "codex-mission-memory-review"}, "max_chars": 200000}
    proc = subprocess.run([r"C:\Python314\python.exe", "-B", "-X", "utf8", r"C:\IALD\MEMORIA_IALD\mission_cli.py"],
                          input=json.dumps(req), text=True, encoding="utf-8", capture_output=True)
    current = json.loads(proc.stdout)
    assert proc.returncode == 0 and current["ok"], proc.stderr
    now = datetime.datetime.now(datetime.timezone.utc)
    project_path = ROOT / ("FINAL_CUSTODY_REVIEW_PROJECT_" + now.strftime("%Y%m%dT%H%M%S_%fZ") + ".json")
    new(project_path, current)
    project = current["result"]["projection"]
    previous_path = ROOT / "MEMORY_REVIEW_PROJECT_FINAL_20261017T160725_739611Z.json"
    previous = read(previous_path)["result"]["projection"]
    assert project["context_id"] == previous["context_id"] == transition_receipt["context_id"]
    assert project["revision"] >= transition_receipt["revision"]
    active = {x["id"]: x for x in project["active"]}
    for old in previous["active"]:
        assert active[old["id"]]["criterion"] == old["criterion"]
        assert active[old["id"]]["depends_on"] == old["depends_on"]
    assert project["settled"] == previous["settled"]
    for key in ["R4", "R5"]:
        assert active[key]["status"] != "satisfied"
    records = {x["id"]: x for x in project["current_records"]}
    for record in request["changes"]["records"]:
        assert records[record["id"]] == record
    for key, value in request["changes"]["flow"].items():
        assert project["flow"][key] == value
    report = {
        "schema": "iald-r57-final-custody-independent-review/v1",
        "created_utc": now.isoformat(), "status": "PASS_WITH_SCOPE", "reviewer": "codex-mission-memory-review",
        "reference": pin(REFERENCE), "claim": 939, "application": pin(ROOT / "MEMORY_APPLIED_R57.json"),
        "plan_review": pin(ROOT / "MEMORY_REVIEW_R57.json"), "plan": pin(ROOT / "MEMORY_PLAN_R57.json"),
        "delivery": pin(ROOT / "DELIVERY_CONSOLIDATED_R57.json"),
        "registration": pin(ROOT / "REGISTRATION_CONSOLIDATED_R57.json"),
        "surfaces": surfaces, "surface_count": 8, "growth_each_bytes": 3165,
        "map": {"receipt": pin(ROOT / "MAP_REGISTER_CONSOLIDATED_R57_RESULT.json"), "result": map_data},
        "board": {"receipt": pin(ROOT / "BOARD_REGISTER_CONSOLIDATED_R57_RESULT.json"), "result": board_data},
        "transition": {"request": pin(request_path), "receipt": pin(transition_path), "result": transition_receipt},
        "mission": {"project": pin(project_path), "revision": project["revision"], "state_sha256": project["state_sha256"],
                    "criteria_and_dependencies_preserved": True, "all_settled_requirements_preserved": True,
                    "active_statuses": {key: active[key]["status"] for key in active},
                    "q_material_record_verified": records["r57-reviewed-components-custodied"],
                    "flow": request["changes"]["flow"], "R4_R5_accepted": False},
        "pins_verified": list(PINS.values()), "runner": pin(__file__), "findings": [],
        "limits": ["Verificação única dos recibos e bytes finais; nenhum rebuild, provedor ou nova avaliação científica.",
                   "O quadro permanece EM_CURSO; este parecer não é AUDITADA/FECHADA nem aceite integral R4/R5.",
                   "As limitações cooperativas/falha parcial do parecer do plano permanecem; a execução observada concluiu as oito superfícies.",
                   "Só artefatos novos de revisão e projeção foram escritos pelo revisor; memórias canônicas não foram alteradas por ele."]}
    dest = ROOT / "FINAL_CUSTODY_REVIEW_R57.json"
    new(dest, report)
    print(json.dumps({"review": pin(dest), "status": report["status"], "revision": project["revision"],
                      "surfaces": 8, "map_seq": map_data["gravados"][0]["seq"],
                      "board_event": board_data["evento"], "board_status": board_data["para"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
