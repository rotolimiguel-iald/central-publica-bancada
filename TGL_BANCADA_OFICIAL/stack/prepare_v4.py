import json
import uuid
from pathlib import Path
from datetime import datetime, timezone
from prepare_v3_requests import atomic, BASE

HERE = Path(__file__).resolve().parent
for name, provider, brief in (("kimi_ram", "kimi", "BRIEF_V4_KIMI_RAM.md"),
                              ("mimo_domains", "mimo", "BRIEF_V4_MIMO_DOMAINS.md")):
    marker = HERE / (name + ".request_id")
    rid = marker.read_text().strip() if marker.exists() else str(uuid.uuid4())
    uuid.UUID(rid)
    if not marker.exists(): atomic(marker, rid.encode())
    constraints = {"mission_id":"TGL_BANCADA_OFICIAL", "branch_id":"universe-v4",
                   "lemma_id":name, "role":"skeptic", "required_provider":provider, "max_calls":1}
    prompt = (HERE / brief).read_text(encoding="utf-8")
    request = {"operation":"submit_execution", "request_id":rid, "prompt":prompt,
               "execution_constraints":constraints}
    atomic(HERE / (name + ".submit.json"), json.dumps(request,ensure_ascii=False).encode())
    receipt = BASE / "state" / "session_requests" / (rid + ".json")
    if not receipt.exists():
        atomic(receipt,json.dumps({**request,"origin":str(HERE.parent),"created_utc":datetime.now(timezone.utc).isoformat(),
                                  "status":"prepared_not_submitted"},ensure_ascii=False).encode())
    print(name, rid)
