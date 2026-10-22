"""Version prepared D10 prompts with manager-provided source excerpts; no submission."""

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
EXPECTED_BUNDLE = "1ce69ffaa4bc1e93b654341f8285fba0f68ac11b0e98235b3b4b1e236153d6fb"


def sha(data):
    return hashlib.sha256(data).hexdigest()


catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
if catalog["status"] != "PREPARED_LOCAL_REVIEW_ONLY_NO_PROVIDER_CALLS" or catalog.get("revision"):
    raise RuntimeError("Draft already revised or dispatched; no automatic rewrite")
raw = BUNDLE_PATH.read_bytes()
if sha(raw) != EXPECTED_BUNDLE:
    raise RuntimeError("Source bundle hash mismatch")
bundle = json.loads(raw)
if bundle["status"] != "SOURCE_EXCERPTS_VERIFIED_LOCAL_READ_ONLY":
    # Preserve source content as data; check only an exact verified status if supplied.
    print("bundle status:", bundle["status"])
entries = bundle["entries"]
if len(entries) != 4:
    raise RuntimeError("Unexpected source count")
for e in entries:
    if not e["source_sha256"] or not e["source_bytes"]:
        raise RuntimeError("Source provenance incomplete")
    for z in e["excerpts"]:
        if sha(z["text"].encode("utf-8")) != z["utf8_sha256"]:
            raise RuntimeError("Excerpt hash mismatch")


def excerpt(source_idx, excerpt_idx):
    e = entries[source_idx]
    z = e["excerpts"][excerpt_idx]
    return (f"\n\n=== VERIFIED LOCAL EXCERPT: {e['source_path']} "
            f"source_SHA256={e['source_sha256']} lines={z['first_line']}-{z['last_line']} "
            f"excerpt_UTF8_SHA256={z['utf8_sha256']} ===\n{z['text']}\n=== END EXCERPT ===\n")


runtime = Runtime(recover=False)
receipts = {}
for provider in ("kimi", "mimo"):
    unit = catalog["units"][provider]
    if unit["status"] != "DRAFT_MANAGER_REVIEW_NOT_SUBMITTED":
        raise RuntimeError("Unit no longer an unsubmitted draft")
    old_prompt = unit["prompt"]
    if sha(old_prompt.encode("utf-8")) != unit["prompt_sha256"]:
        raise RuntimeError("Original draft prompt mismatch")
    if provider == "kimi":
        selected = [(1, 1), (2, 0)]
        instruction = (
            "\nSOURCE-SPECIFIC TEST: Historical variant S sends CAMB only nnu=NEFF_SM+DNDB*beta "
            "and omch2_eff=omch2+beta*(ombh2+omch2), with usual remaining parameters and mnu=.06. "
            "Determine whether its observable predictions lie within a rival ΛCDM+Neff(+mnu) "
            "family for admissible parameter domains, in which case sup logL rival >= sup logL historical "
            "fixed-S and rejection of that rival by this contrast is impossible. This is a conditional "
            "identifiability check, not a refutation of the current canonical TGL. Source is the historical "
            "N2 implementation; do not infer absence of a different derivation elsewhere.\n"
        )
    else:
        selected = [(0, 0), (1, 1)]
        instruction = (
            "\nSOURCE-SPECIFIC AUDIT: Historical LikeN2.log_post adds BAO with "
            "np.sum(((bao-DESI[:,2])/DESI[:,3])**2), a diagonal-error likelihood; "
            "it is not full covariance. Trace 13 D9 DESI DR2 measurements versus 12 N2 points "
            "by actual release/measurement identity before combination. Do not invent a missing "
            "cross-covariance or count the two sets as independent. Distinguish this historical "
            "implementation from any later canonical one.\n"
        )
    prompt = old_prompt + instruction + "".join(excerpt(*pair) for pair in selected)
    if len(prompt) > 24000:
        raise RuntimeError(f"{provider} revised prompt too long: {len(prompt)}")
    preview = runtime.preview(prompt, unit["execution_constraints"])
    if preview.get("selected") != provider:
        raise RuntimeError(f"{provider} no longer selected")
    unit.update(prompt=prompt, prompt_sha256=sha(prompt.encode("utf-8")),
                prompt_chars=len(prompt), preview_selected=preview["selected"],
                canonical_packet_sha256=preview["canonical_memory"]["packet_sha256"],
                canonical_context_bytes=preview["canonical_memory"]["context_bytes"],
                canonical_coverage=preview["canonical_memory"]["coverage"],
                prior_prompt_sha256=sha(old_prompt.encode("utf-8")),
                source_excerpt_refs=[{"source_sha256": entries[i]["source_sha256"],
                                      "first_line": entries[i]["excerpts"][j]["first_line"],
                                      "last_line": entries[i]["excerpts"][j]["last_line"],
                                      "utf8_sha256": entries[i]["excerpts"][j]["utf8_sha256"]}
                                     for i, j in selected])
    receipts[provider] = {"request_id": unit["request_id"], "prompt_sha256": unit["prompt_sha256"],
                          "prompt_chars": len(prompt), "preview_selected": preview["selected"]}
catalog.update(revision=2, revised_at=utc_now(), source_bundle_path=str(BUNDLE_PATH),
               source_bundle_sha256=EXPECTED_BUNDLE,
               source_access_limit="Manager-provided byte/hash/line verified excerpt bundle; worker still cannot directly read C:/IALD/Artigo originals",
               status="REVISED_LOCAL_REVIEW_ONLY_NO_PROVIDER_CALLS")
save_json(CATALOG_PATH, catalog)
print(json.dumps(receipts, ensure_ascii=False))
