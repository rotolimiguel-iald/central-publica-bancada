"""Static context-model assessment. No app import, SDK, credentials, network or send."""
from pathlib import Path
from datetime import datetime, timezone
import ast, copy, hashlib, json, os, re

D = Path(__file__).resolve().parent
W = D.parent
S = W / "memory_stage"
A = Path(r"C:\IALD\projetos_pyhton\IALD")
MODEL = "claude-sonnet-5-5"
NAMES = ("iald_kernel_verification", "iald_kernel_search", "iald_kernel_read",
         "iald_kernel_list", "iald_public_read", "search_tgl", "fetch_tgl")
def digest(raw):
    return hashlib.sha256(raw).hexdigest()
def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "sha256": digest(b)}
def read(p):
    return json.loads(Path(p).read_bytes())
def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf8")
def fresh(name, raw):
    p = D / name
    assert not p.exists(), "Existing evidence; no automatic overwrite"
    tmp = p.with_name(p.name + ".tmp")
    with tmp.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.read_bytes() == raw
    os.replace(tmp, p)
def save(name, value):
    fresh(name, encode(value))
def fn(path, name):
    tree = ast.parse(Path(path).read_bytes(), filename=str(path))
    matches = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
    assert len(matches) == 1
    return matches[0]
def public_definitions():
    # AST literals only; no compilation/eval/exec/import of application code.
    k = fn(A / "iald_kernel.py", "tool_definitions")
    specs = ast.literal_eval(next(n.value for n in k.body if isinstance(n, ast.Assign)))
    defs = [{"type": "function", "function": {
        "name": n, "description": d, "parameters": {"type": "object", "properties": p,
        "required": r, "additionalProperties": False}}} for n, d, p, r in specs]
    p = fn(A / "iald_fontes_publicas.py", "tool_definitions")
    ret = copy.deepcopy(next(n.value for n in p.body if isinstance(n, ast.Return)))
    comps = [n for n in ast.walk(ret) if isinstance(n, ast.ListComp)]
    assert len(comps) == 1
    assert ast.unparse(comps[0]) == "[item['id'] for item in catalog()['entries']]"
    ids = [x["id"] for x in read(A / "iald_fontes_publicas.json")["entries"]]
    class LiteralCatalog(ast.NodeTransformer):
        def visit_ListComp(self, node):
            return ast.List(elts=[ast.Constant(x) for x in ids], ctx=ast.Load())
    defs += ast.literal_eval(LiteralCatalog().visit(ret))
    c = fn(W / "delta_app01/iald_core_indexado.py", "tool_definitions")
    defs += ast.literal_eval(next(n.value for n in c.body if isinstance(n, ast.Return)))
    assert tuple(x["function"]["name"] for x in defs) == NAMES
    return defs, [{"path": str(pth), "start_line": node.lineno, "end_line": node.end_lineno}
                  for pth, node in [(A/"iald_kernel.py", k),
                  (A/"iald_fontes_publicas.py", p),
                  (W/"delta_app01/iald_core_indexado.py", c)]]
def main():
    before = {str(p): pin(p) for folder in ("delta_native02", "delta_selective03")
              for p in (W / folder).iterdir() if p.is_file()}
    manifest = read(S / "manifest_staged.json")
    meta = read(S / "public_metadata.json")
    raw = (S / "public_prefix.md").read_bytes()
    prefix = raw.decode("utf8")
    assert digest(raw) == meta["context_sha256"]
    assert meta["private_atlas_included"] is False and "<ATLAS_CANONICO" not in prefix
    components = {}
    for name in ("mother_instruction", "operational_core", "active_cluster"):
        p = Path(manifest[name]["path"])
        assert p.resolve().is_relative_to(S.resolve())
        got = pin(p)
        assert got["sha256"] == manifest[name]["sha256"]
        assert p.read_bytes().decode("utf-8-sig") in prefix
        components[name] = dict(got, exact_text_in_prefix=True)
    local = read(S/"LOCAL_SEALED_MANIFEST.json")
    assert pin(S/"LOCAL_SEALED_MANIFEST.json")["sha256"] == manifest["local_release"]["sha256"]
    members = []
    for rel, record in local["files"].items():
        p = (S/rel).resolve()
        assert p.is_relative_to(S.resolve()) and p.is_file()
        got = pin(p)
        assert got["sha256"] == record["sha256"] and got["bytes"] == record["bytes"]
        members.append(got)
    kernel = read(S/"kernel/kernel_manifest.json")
    kernel_pins = []
    for rec in kernel["files"]:
        p = (S/"kernel"/rec["path"]).resolve()
        assert p.is_relative_to((S/"kernel").resolve())
        got = pin(p)
        assert got["sha256"] == rec["sha256"] and got["bytes"] == rec["bytes"]
        kernel_pins.append(got)
    assert kernel["source_sha256"] == local["source_sha256"] == manifest["active_cluster"]["release_source_sha256"]
    source_pin = pin(S/"release/um.py")
    assert source_pin["sha256"] == local["source_sha256"]
    result = read(S/"release/um_absoluto.json")
    topics = re.findall(r"(?m)^Fonte: resultado_publicado_integral /core/([^\r\n]+)$",
                        (S/"TGL_CLUSTER_v388.md").read_bytes().decode("utf8"))
    assert len(topics) == len(set(topics)) == len(result["core"]) == 377
    assert set(topics) == set(result["core"])
    formal = []
    for rec in meta["fixed_hypothesis_sources"]:
        got = pin(S/"kernel"/rec["path"])
        assert got["sha256"] == rec["sha256"] and got["bytes"] == rec["bytes"]
        formal.append(dict(got, id=rec["id"],
            complete_file_literal_in_public_prefix=(S/"kernel"/rec["path"]).read_bytes().decode("utf8") in prefix))
    docs = []
    for entry in manifest["entries"]:
        p = Path(entry["path"])
        assert p.resolve().is_relative_to(S.resolve())
        got = pin(p)
        assert got["sha256"] == entry["public_sha256"]
        docs.append(dict(got, id=entry["id"], role=entry["role"], source_scope=entry.get("source_scope")))
    defs, def_locations = public_definitions()
    # Corresponds to converter_pedido's native tool projection; eager is transport-only.
    tools = [{"name": d["function"]["name"], "description": d["function"]["description"],
              "input_schema": d["function"]["parameters"]} for d in defs]
    old_reference = read(W/"delta_native02/FUTURE_COUNT_REFERENCE.json")
    assert tools == old_reference["tools"], "Pinned schema drift"
    wire_tools = [dict(x, eager_input_streaming=True) for x in tools]
    wire_sha = digest(json.dumps(wire_tools, sort_keys=True, ensure_ascii=False).encode())
    assert wire_sha == read(W/"COUNT_RESULT.json")["native_tools_sha256"]
    base = {"model": MODEL, "system": [{"type": "text", "text": prefix,
               "cache_control": {"type": "ephemeral"}}],
            "thinking": {"type": "adaptive"}, "output_config": {"effort": "high"}}
    minimal = dict(copy.deepcopy(base), messages=[{"role": "user", "content": "."}])
    reference = dict(copy.deepcopy(base), messages=copy.deepcopy(old_reference["messages"]),
                     tools=tools, cache_control=copy.deepcopy(old_reference["cache_control"]))
    assert "tool_choice" not in minimal and "tool_choice" not in reference
    save("FUTURE_COUNT_MINIMAL.json", minimal)
    save("FUTURE_COUNT_REFERENCE.json", reference)
    code_names = [
        "claude_profiles.py", "claude_account_policy.py", "claude_server_selection.py",
        "claude_route_bridge.py", "claude_memory_package.py", "claude_context_snapshot.py",
        "claude_request_guard.py", "claude_profile_pipeline.py", "claude_guarded_transport.py",
        "claude_native_counter.py", "claude_tool_budget.py", "claude_native_account.py",
        "iald_motor_claude.py", "iald_web_server.py", "iald_motores.py",
        "iald_memoria_canonica.py", "iald_kernel.py", "iald_fontes_publicas.py",
        "iald_fontes_publicas.json", "app/iald.js", "iald-app/capacitor.config.json",
        "iald-app/sincronizar_app.ps1"]
    code = []
    for name in code_names:
        p = A/name
        got = pin(p)
        if p.suffix == ".py":
            tree = ast.parse(p.read_bytes(), filename=str(p))
            got["ast_parsed"] = True
            got["top_level_api"] = [{"name": n.name, "line": n.lineno, "end_line": n.end_lineno}
                for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
        code.append(got)
    clients = []
    for rel in ["app/iald.js", "iald-app/www/iald.js", "iald-app/ios/App/App/public/iald.js",
                "iald-app/android/app/src/main/assets/public/iald.js"]:
        p = A/rel
        clients.append(pin(p) if p.exists() else {"path": str(p), "status": "ABSENT"})
    package_files = [S/x for x in ["manifest_staged.json", "manifest_install.json",
        "public_prefix.md", "public_metadata.json", "LOCAL_SEALED_MANIFEST.json",
        "TGL_CLUSTER_v388.md", "kernel/kernel_manifest.json", "kernel_verification.json",
        "cluster_dedup.json", "cluster_exposition_projection.json", "prepared.json",
        "science_binding.json", "release/tgl_kernel_proof_manifest.json", "release/um_absoluto_selo.json"]]
    stale_meta = meta["active_cluster"]["local_release"]["sha256"] != manifest["local_release"]["sha256"]
    save("INVENTARIO_LOCAL.json", {
        "schema": "iald.context_model04.static_inventory.v1",
        "measured_utc": datetime.now(timezone.utc).isoformat(),
        "status": "STATIC_ONLY_NO_MIGRATION_NO_NATIVE_MEASUREMENT",
        "source_identity": source_pin, "components": components, "documents": docs,
        "kernel": {"files": len(kernel_pins), "total_bytes": sum(p["bytes"] for p in kernel_pins),
                   "pins": kernel_pins, "compilation_rerun": False},
        "local_snapshot": {"files": len(members), "pins": members},
        "public_context": dict(pin(S/"public_prefix.md"),
            native_tokens_sonnet=None, stored_o200k_proxy=meta["context_tokens"],
            topic_count=len(topics), topic_set_exact=True,
            added_topics=read(S/"prepared.json")["added_topics"],
            formal_source_pins=formal,
            coverage="FULL_EXISTING_PUBLIC_ASSEMBLY_NOT_FULL_CORPUS",
            document_mode="retrievable",
            old_local_release_pin_in_public_metadata=meta["active_cluster"]["local_release"]["sha256"],
            authoritative_local_release_pin=manifest["local_release"]["sha256"],
            metadata_needs_rebinding=stale_meta,
            either_local_release_hash_present_in_prefix=any(h in prefix for h in [
                meta["active_cluster"]["local_release"]["sha256"], manifest["local_release"]["sha256"]])),
        "artifacts": [pin(p) for p in package_files],
        "code": code, "clients": clients,
        "schema_sources": def_locations,
        "tools": {"names": NAMES, "native_wire_sha256": wire_sha,
                  "count_tools_sha256": digest(json.dumps(tools, sort_keys=True, ensure_ascii=False).encode()),
                  "unchanged_from_first_haiku_count": True},
        "previous_count": pin(W/"COUNT_RESULT.json"),
        "previous_count_certifies_sonnet": False,
        "sealed_B_A_unchanged": all(pin(Path(p)) == got for p, got in before.items()),
        "sealed_B_A_pins": list(before.values()),
        "credentials_read": False, "effective_private_config_read": False,
        "app_imported": False, "provider_calls": 0, "science_executed": False})
    save("FUTURE_COUNT_PLAN.json", {
        "status": "NOT_AUTHORIZED_NOT_SENT", "model": MODEL,
        "future_count_requests": 2, "count_requests_sent": 0, "generation_requests": 0,
        "prefix": pin(S/"public_prefix.md"),
        "payloads": [pin(D/n) for n in ("FUTURE_COUNT_MINIMAL.json","FUTURE_COUNT_REFERENCE.json")],
        "source_identity": source_pin, "native_wire_tools_sha256": wire_sha,
        "parameters": {"thinking": {"type":"adaptive"}, "output_config":{"effort":"high"},
                       "tool_choice": "OMITTED_AUTO_DEFAULT", "system_cache": "ephemeral_5m",
                       "reference_tail_cache": reference["cache_control"]},
        "count_contract": "Count fields match the observed adapter; no max_tokens or metadata; eager_input_streaming stripped only from tools.",
        "future_generation_reservation_proposal_INPUT": {"output_tokens":4096,
            "margin_tokens":1024, "minimum_dynamic_remaining":10000,
            "minimum_permanent_tokens":180000, "window_tokens":1000000},
        "acceptance_formula": "permanent >=180000 AND whole>=permanent AND 1000000-whole-4096-1024 >=10000; source/tool/model/receipt pins exact",
        "native_counts": {"permanent": None, "reference": None, "remaining": None},
        "previous_haiku_overhead_is_not_transferred": True,
        "minimal_scope": "Exact public system + user dot + adaptive/high; excludes tool schemas. Provider overhead remains part of this measurement.",
        "reference_scope": "Same public system + same seven ordered public schemas + fixed question, adaptive/high, automatic tail cache. No histories, images, tool results or user profile.",
        "production_differences": [
            "Current Sonnet route builds variable internal/public context and generic tools; proposed route must pin this public system and seven schemas.",
            "Current Sonnet bypasses post_guarded/native request accounting and can crop by proxy; successor required.",
            "Current package loader/snapshot binds Haiku only; measured Sonnet package does not exist.",
            "Per-request variable system/history/profile/tool result content requires count of final wire; these two counts are not a certificate for arbitrary requests.",
            "public_metadata has a stale local_release sub-pin; successor metadata must bind current manifest, prefix bytes currently contain neither sub-pin.",
            "No live account/model access or SDK acceptance of this exact payload has been tested."],
        "authorization_policy": "ROOT review then explicit authorization of these exact two files. No previous count approval transfers. Official existing client only; no retry after uncertain send.",
        "reproduction": "This stdlib-only builder reads pinned sources and creates local files once; it contains no send function."
    })
    print(json.dumps({"inventory": pin(D/"INVENTARIO_LOCAL.json"),
        "payloads":[pin(D/n) for n in ("FUTURE_COUNT_MINIMAL.json","FUTURE_COUNT_REFERENCE.json")],
        "kernel_files":len(kernel_pins), "snapshot_files":len(members),
        "formal_full":[x["complete_file_literal_in_public_prefix"] for x in formal],
        "clients":clients, "native_tokens":None}, ensure_ascii=False))
if __name__ == "__main__":
    main()