"""Apply the manager's two exact scientific amendments before admission."""

import hashlib
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.safe_files import save_json, utc_now

HERE = Path(__file__).resolve().parent
CATALOG_PATH = HERE / "D10_CMB_BAO_PREPARED_UNITS.json"
BUNDLE_PATH = BASE.parent / "TGL_BANCADA_OFICIAL" / "state" / "D10_CMB_BAO_SOURCE_EXCERPTS.json"


def sha(data):
    return hashlib.sha256(data).hexdigest()


catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
if catalog.get("revision") != 2 or catalog["status"] != "REVISED_LOCAL_REVIEW_ONLY_NO_PROVIDER_CALLS":
    raise RuntimeError("Expected manager-reviewed revision 2 only")
bundle_raw = BUNDLE_PATH.read_bytes()
if sha(bundle_raw) != catalog["source_bundle_sha256"]:
    raise RuntimeError("Source bundle changed")
entries = json.loads(bundle_raw)["entries"]
for e in entries:
    for z in e["excerpts"]:
        if sha(z["text"].encode("utf-8")) != z["utf8_sha256"]:
            raise RuntimeError("Excerpt hash mismatch")


def excerpt(source_idx, excerpt_idx):
    e = entries[source_idx]
    z = e["excerpts"][excerpt_idx]
    return (f"\n\n=== VERIFIED LOCAL EXCERPT: {e['source_path']} "
            f"source_SHA256={e['source_sha256']} lines={z['first_line']}-{z['last_line']} "
            f"excerpt_UTF8_SHA256={z['utf8_sha256']} ===\n{z['text']}\n=== END EXCERPT ===\n")


kimi = catalog["units"]["kimi"]
old_phrase = "rejection of that rival by this contrast is impossible"
new_phrase = ("the observable family may be included in the rival; verify the signed likelihood "
              "inequality and that, with uniformly controlled type-I error, power at included TGL "
              "points cannot exceed the test size. Distinguish absence of discriminating power "
              "from the possibility of a type-I rejection")
if kimi["prompt"].count(old_phrase) != 1:
    raise RuntimeError("Kimi target sentence missing or duplicated")
old_kimi = kimi["prompt"]
kimi["prompt"] = old_kimi.replace(old_phrase, new_phrase)

mimo = catalog["units"]["mimo"]
old_mimo = mimo["prompt"]
mimo["prompt"] = (old_mimo + "\nMANAGER-REQUESTED ADDITION: inspect the full historical D10 "
                  "function excerpt and the frozen N2 selection below. These are source excerpts, "
                  "not proof of current canonical equivalence or independent data.\n"
                  + excerpt(0, 1) + excerpt(2, 0))

runtime = Runtime(recover=False)
out = {}
for provider, unit, old_prompt in (("kimi", kimi, old_kimi), ("mimo", mimo, old_mimo)):
    if unit["status"] != "DRAFT_MANAGER_REVIEW_NOT_SUBMITTED":
        raise RuntimeError("Unit was already submitted")
    if sha(old_prompt.encode("utf-8")) != unit["prompt_sha256"]:
        raise RuntimeError("Version 2 prompt integrity failed")
    prompt = unit["prompt"]
    preview = runtime.preview(prompt, unit["execution_constraints"])
    if preview.get("selected") != provider:
        raise RuntimeError(f"Required {provider} not selected")
    unit.update(status="MANAGER_ADMITTED_READY_TO_SUBMIT", prompt_sha256=sha(prompt.encode("utf-8")),
                prompt_chars=len(prompt), prior_prompt_sha256=sha(old_prompt.encode("utf-8")),
                preview_selected=preview["selected"],
                canonical_packet_sha256=preview["canonical_memory"]["packet_sha256"],
                canonical_context_bytes=preview["canonical_memory"]["context_bytes"])
    if provider == "mimo":
        unit["source_excerpt_refs"] += [{"source_sha256": entries[i]["source_sha256"],
                                        "first_line": entries[i]["excerpts"][j]["first_line"],
                                        "last_line": entries[i]["excerpts"][j]["last_line"],
                                        "utf8_sha256": entries[i]["excerpts"][j]["utf8_sha256"]}
                                       for i, j in ((0, 1), (2, 0))]
    out[provider] = {"request_id": unit["request_id"], "prompt_sha256": unit["prompt_sha256"],
                     "prompt_chars": unit["prompt_chars"], "selected": preview["selected"],
                     "canonical_packet_sha256": unit["canonical_packet_sha256"]}
catalog.update(status="MANAGER_ADMITTED_FINAL_PAYLOADS_NOT_SUBMITTED", revision=3,
               finalized_at=utc_now(), manager_authorization_scope="Distinct D10 Kimi/MiMo scientific critique units; single call each; no retry of prior terminal unit")
save_json(CATALOG_PATH, catalog)
print(json.dumps(out, ensure_ascii=False))
