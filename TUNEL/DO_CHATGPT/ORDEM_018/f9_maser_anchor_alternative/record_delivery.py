from pathlib import Path
import sys, json, hashlib
sys.path.insert(0, r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923")
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now
ROOT = Path(__file__).resolve().parents[1]
BASE = Path(__file__).resolve().parent
MEM = Path(r"C:\IALD\Central de Patentes\memory")
REVIEW = ROOT / "f9_maser_anchor_alternative_review" / "RECIBO_REVISAO.json"
MARKER = "IALD_F9_MASER_ANCHOR_ALTERNATIVE_REVIEWED_20261006"

def pin(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def verify(entry):
    actual = pin(Path(entry["path"]))
    assert actual["bytes"] == entry["bytes"] and actual["sha256"] == entry["sha256"], entry["path"]
    return actual

review = json.loads(REVIEW.read_bytes())
assert review["status"] == "PASS_DOCUMENTARY_ONLY", review.get("status")
manifest = json.loads((BASE / "MANIFESTO.json").read_bytes())
verified = [verify(x) for x in manifest["files"]]
evidence = json.loads((BASE / "EVIDENCIA.json").read_bytes())
frozen = [verify(x) for x in evidence["frozen_inputs_before"]]
notice_path = BASE / "MANAGER_PUBLIC_NOTICE.json"
notice = json.loads(notice_path.read_bytes())
assert notice["status"] in ("SENT_OFFICIAL_TOOL_SUCCESS", "NOT_SENT_REVIEW_COMPLETE", "SEND_UNCERTAIN_NO_RETRY")
now = utc_now()
receipt_path = ROOT / "RECIBO_F9_MASER_ANCHOR_ALTERNATIVE_20261006.json"
assert not receipt_path.exists(), "Existing receipt: inspect recovery; do not rerun blindly"
receipt = {"schema": "iald.ordem018.maser_anchor_alternative.v1", "at": now,
    "status": "ACCEPTED_DOCUMENTARY_ALTERNATIVE_ONLY", "manifest": pin(BASE / "MANIFESTO.json"),
    "report": pin(BASE / "PARECER_DOCUMENTAL.md"), "review": pin(REVIEW),
    "independent_review_status": review["status"], "verified_manifest_members": len(verified),
    "frozen_unchanged": frozen, "source": pin(BASE / "sources" / "masers_2001.09213v2.pdf"),
    "scientific_execution": False, "new_statistical_admission": False, "covariance_calculation": False,
    "official_verdict_changed": False, "map_registered": False, "map_egress_rejection_preserved": True,
    "manager_public_notice": pin(notice_path), "manager_scientific_response_received": False,
    "approvals_unchanged": ["d72", "P3_A02", "v389_two_native_counts"],
    "next_action": "Manager may assess the published five-maser alternative for a future explicit specification. No replacement of frozen V1 and no repeat of this source audit. Joint F1/F3 remain required."}
save_json(receipt_path, receipt)
receipt_pin = pin(receipt_path)
append = ("\n\n### 06/10/2026 — Masers: alternativa publicada sem NGC4258\n\n<!-- " + MARKER + " -->\n\n"
    "[REAL — documental] PDF público de Pesce et al., arXiv:2001.09213v2, arquivado por bytes; Tabela 2/p.6 conferida visualmente e em revisão independente PASS_DOCUMENTARY_ONLY. "
    "[KNOWN — publicação] O tratamento fiducial (1) publica H0=73,6 (+3,1/−3,0) km/s/Mpc sem NGC4258, com percentis 16–84. "
    "[DERIVED — alternativa, não decisão] Pode-se examinar o leitor sem o fator de distância desta âncora, ou manter as seis galáxias com dependência explícita. "
    "Nunca somar os dois ajustes como independentes; a exclusão não elimina os outros sistemáticos ou a âncora entre as demais escalas. "
    "A escolha deve ser metodológica, não pelo centro/significância. [OPEN] Especificação futura, mapa do observável e dependências restantes; F1 conjunta/F3/F4 continuam incompletos. "
    "V1 e resultado congelados intactos; nenhuma execução, covariância ou novo veredito. Mapa ainda não registrado, sem contornar a recusa anterior.\n\n"
    "Evidência: " + str(receipt_path) + " (SHA256 " + receipt_pin["sha256"] + "). "
    "Fonte: https://arxiv.org/pdf/2001.09213v2. As aprovações d72/P3 e contagens do app permanecem inalteradas.\n")
changed = []
for path in [MEM / "TGL_ATLAS.md", MEM / "TGL_INDICE_VIVO.md", MEM / "TGL_CORE_MEMORY.md", ROOT / "ENTREGA_018_F1_HUBBLE.md", ROOT / "ENTREGA_018_RELATORIO_FINAL.md"]:
    old = path.read_bytes()
    assert MARKER.encode() not in old, str(path)
    addition = append.replace("\n", "\r\n").encode("utf-8") if b"\r\n" in old else append.encode("utf-8")
    assert path.read_bytes() == old
    replace_bytes(path, old + addition)
    assert len(path.read_bytes()) > len(old)
    changed.append(pin(path))
summary = {"at": now, "status": receipt["status"], "receipt": receipt_pin, "review": pin(REVIEW),
    "official_verdict_changed": False, "statistical_admission": False, "map_registered": False,
    "manager_public_notice_sent": notice["status"] == "SENT_OFFICIAL_TOOL_SUCCESS", "manager_response_received": False}
for path, field in [(ROOT / "CONTINUIDADE.json", "F9_maser_anchor_alternative"),
    (Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\state\handoffs\slot_management.json"), "ordem018_F9_maser_anchor_alternative")]:
    old = path.read_bytes(); d = json.loads(old)
    assert field not in d
    d[field] = summary; d["updated_at"] = now
    if path.name == "CONTINUIDADE.json":
        d["status"] = "ACTIVE_MASER_ANCHOR_ALTERNATIVE_REVIEWED_JOINT_F1_F3_APPROVALS_PENDING"
        d["last_goal_turn_classification"] = "MEANINGFUL_PUBLISHED_MASER_ALTERNATIVE_VERIFIED_NOT_SCIENTIFIC_COMPLETION"
        d["previous_goal_turn_revalidation"] = {"classification": "NO_PROGRESS", "reason": "Recheck of already-completed app model assessment only; no scientific state change."}
        d["next_steps"][0] = receipt["next_action"]
    assert path.read_bytes() == old; save_json(path, d); changed.append(pin(path))
manifest_path = ROOT / "MANIFESTO_CONSOLIDACAO_PARCIAL.json"
old = manifest_path.read_bytes(); d = json.loads(old)
new_paths = [Path(x["path"]) for x in verified] + [REVIEW, REVIEW.parent / "PARECER.md", receipt_path, notice_path, Path(__file__).resolve()] + [Path(x["path"]) for x in changed]
updates = {str(x): pin(x) for x in new_paths}
by_path = {x["path"]: x for x in d["files"]}; by_path.update(updates)
d["files"] = list(by_path.values()); d["updated_at"] = now
d["latest_F9_maser_anchor_alternative"] = receipt_pin
d["latest_F9_maser_anchor_alternative_scope"] = "Reviewed documentary alternative only; not final scientific F4 approval."
assert manifest_path.read_bytes() == old; save_json(manifest_path, d)
for x in updates.values(): verify(x)
for x in frozen: verify(x)
print(json.dumps({"status": receipt["status"], "receipt": receipt_pin, "updated_pins_verified": len(updates), "consolidation": pin(manifest_path)}, ensure_ascii=False, indent=2))
