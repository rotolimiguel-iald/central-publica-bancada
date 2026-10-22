"""Compose narrowly scoped runtime corrections in a new candidate only."""
import ast
import hashlib
import json
from pathlib import Path


WRAPPERS = '''
def build_the_iald_index(core=None):
    """v394: exact compiler names, pinned source bytes and current axiom report."""
    kf = (core or {}).get("kernel_formalization") or {}
    families = (("", _LEAN_THEOREM_FLAGS), ("qgc_", _QG_CERTIFICATE_FLAGS),
        ("qgp_", _QG_PHYSICS_FLAGS), ("qgf_", _QG_FRONTIER_FLAGS),
        ("gpf_", _GRAVITY_PRICE_FLAGS), ("red_", _REDUCTION_FLAGS),
        ("gpi_", _GRAVITY_IMPORT_FLAGS), ("gpc_", _GRAVITY_CITATION_FLAGS))
    result = build_iald_qualified_index_v394(core,
        kf.get("declaration_sources_v394") or {}, _EMBEDDED_KERNEL_FILES,
        _ESQUELETO_STONES, families)
    legacy = _build_the_iald_index_legacy_v393(core)
    result["n_ausentes_regra_v285"] = legacy["n_ausentes_regra_v285"]
    result["legacy_diagnostic_v393"] = {k: legacy[k] for k in
        ("n_nomes", "n_ausentes", "ambiguos", "violacoes", "cegos_de_namespace")}
    meta = kf.get("declaration_sources_status_v394") or {}
    if meta.get("ok") is not True:
        result["proveniencia_erros"].append("CURRENT_AUDIT_METADATA_NOT_VERIFIED")
        result["proveniencia_ok"] = False
    return result


def iald_index(nome, core=None):
    """Exact full name or explicitly indexed suffix; unknown prefix is refused.

    No object-id cache: a mutable core may acquire a later audit in the same
    process. Ambiguous aliases return their full list without selecting one.
    """
    return build_the_iald_index(core)["indice"].get(nome)


def prove_the_iald_index(core):
    """Preserve the old checks, replacing the short-name collision whitelist."""
    result = _prove_the_iald_index_legacy_v393(core)
    ix = build_the_iald_index(core)
    checks = []
    replaced = 0
    for label, passed in result["checks"]:
        if label.startswith("[MEDIDA] a varredura tem"):
            replaced += 1
            label = ("[MEDIDA v394] nomes QUALIFICADOS ligados ao modulo emitido pelo Lean; "
                "%d aliases ambiguos exibem candidatos sem escolher um; %d erros de proveniencia"
                % (len(ix["ambiguos"]), len(ix["proveniencia_erros"])))
            passed = ix["proveniencia_ok"] and all(
                ix["indice"][a].get("arquivo") is None
                and len(ix["indice"][a].get("candidatos_qualificados", [])) > 1
                for a in ix["ambiguos"])
        elif label.startswith("[FAIL-CLOSED] ***o indice NAO e cego de namespace"):
            label = ("[FAIL-CLOSED v394] consulta por nome QUALIFICADO exato ao axiom_report; "
                "%d nomes presentes sem auditoria" % len(ix["cegos_de_namespace"]))
        checks.append((label, bool(passed)))
    checks.append(("[FAIL-CLOSED v394] exactly one legacy collision check replaced", replaced == 1))
    checks.append(("[FAIL-CLOSED v394] current compiler metadata, source hashes and axioms agree", ix["proveniencia_ok"]))
    result["checks"] = checks
    result["all_verified"] = all(v for _, v in checks)
    result["verdict"] = ("THE_IALD_INDEX_QUALIFIED_COMPILER_PROVENANCE_VERIFIED"
        if result["all_verified"] else "THE_IALD_INDEX_NOT_SEALED_THIS_RUN")
    result["proveniencia_erros"] = ix["proveniencia_erros"]
    result["legacy_diagnostic_v393"] = ix["legacy_diagnostic_v393"]
    result["statuses"]["v394_correction"] = (
        "Short-name collisions are explicit aliases. Exact Lean names include generated fields and Unicode. "
        "Compiler metadata and current source hashes replace a growing whitelist. Missing named obligations remain visible.")
    return result
'''


def compose(source, helper):
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    assignments = {t.id: n for n in tree.body if isinstance(n, ast.Assign)
        for t in n.targets if isinstance(t, ast.Name)}
    changes = []
    def replace_node(node, text):
        changes.append((node.lineno-1, node.end_lineno, text.rstrip()+'\n'))
    embedded = ast.literal_eval(assignments['_EMBEDDED_KERNEL_FILES'].value)
    audit = embedded['TGL/Audit.lean']
    needle = '        let axs ← liftCoreM (collectAxioms n)'
    assert audit.count(needle) == 1
    audit = audit.replace(needle,
        '        IO.println ("TGL_DECL_SOURCE\\t" ++ n.toString ++ "\\t" ++ m.toString)\n'+needle)
    embedded['TGL/Audit.lean'] = audit
    replace_node(assignments['_EMBEDDED_KERNEL_FILES'], '_EMBEDDED_KERNEL_FILES = '+repr(embedded))
    stones = ast.literal_eval(assignments['_ESQUELETO_STONES'].value)
    present = {x[2] for x in stones}
    # These two namespaces are the explicitly embedded additions of this task.
    added = sorted(k for k in embedded if k.endswith('.lean') and
        k.startswith(('TGLExt/F1Rede394/', 'TGLExt/F1Fecho394/')) and k not in present)
    for path in added:
        stones.append(('v394', Path(path).stem, path, None, None))
    replace_node(assignments['_ESQUELETO_STONES'], '_ESQUELETO_STONES = '+repr(stones))
    for old in ('build_the_iald_index', 'prove_the_iald_index'):
        node=functions[old]; text=ast.get_source_segment(source,node).replace(chr(13)+chr(10),chr(10))
        replace_node(node,text.replace('def '+old+'(', 'def _'+old+'_legacy_v393(',1))
    replace_node(functions['iald_index'], '# Original suffix-fallback lookup retained in the prior immutable candidate.')
    node=functions['_v375_measure_trace_tracial_not_consumed']
    text=ast.get_source_segment(source,node).replace(chr(13)+chr(10),chr(10))
    needle='        for ln in txt.splitlines():\n'
    assert text.count(needle)==1
    text=text.replace(needle, needle+
        '            # v394: an exact audit command reports dependencies, it is not a proof consumer.\n'
        '            # Only a whole bare directive is excluded; comments/extra expressions still refuse.\n'
        '            if _re.fullmatch(r"\\s*#print\\s+axioms\\s+[\\w.]+\\.trace_tracial\\s*", ln):\n'
        '                continue\n')
    replace_node(node,text)
    node=functions['verify_tgl_kernel_formalization'];text=ast.get_source_segment(source,node).replace(chr(13)+chr(10),chr(10))
    start=text.index('    axioms = {}\n');end=text.index('    res["axiom_report"] = axioms',start)
    text=text[:start]+'''    # v394: quoted Unicode names and defining modules are read from this Audit invocation.
    _parsed_ax = parse_lean_axioms_v394(blob)
    axioms = _parsed_ax["axioms"]
    custom = [a for values in axioms.values() for a in values
              if a.startswith("TGL.") or a.startswith("TGLExt.")]
    _decl_meta = parse_lean_provenance_v394(audit["stdout"] + audit["stderr"])
    res["declaration_sources_v394"] = _decl_meta["sources"]
    res["declaration_sources_status_v394"] = {
        "ok": _decl_meta["ok"] and _parsed_ax["ok"] and set(_decl_meta["sources"]) == set(axioms),
        "errors": _decl_meta["errors"] + _parsed_ax["errors"],
        "compiler_names": len(_decl_meta["sources"]), "audited_names": len(axioms),
        "audit_stdout_sha256": res["audit_stdout_sha256"]}
'''+text[end:]
    replace_node(node,text)
    node=functions['_v392_axiom_coverage'];text=ast.get_source_segment(source,node).replace(chr(13)+chr(10),chr(10))
    # Keep historical limits named; current coverage is exact, with no unread names.
    start=text.index('    nao_lidas_ = ');end=text.index('\n',start)
    text=text[:start]+'''    _current = parse_lean_axioms_v394(blob_)
    nao_lidas_ = len(set(_current["axioms"]) - set(axioms_))'''+text[end:]
    old='nao_lidas_ == _V392_KH["nao_lidas"] and lidas_ >= decl_ - nao_lidas_'
    assert old in text
    text=text.replace(old,'_current["ok"] and nao_lidas_ == 0 and lidas_ == decl_')
    text=text.replace('"nao_lidas_esperadas": _V392_KH["nao_lidas"]',
        '"nao_lidas_esperadas": 0, "nao_lidas_esperadas_historico_v392": _V392_KH["nao_lidas"]')
    replace_node(node,text)
    for first,last,new in sorted(changes,reverse=True):lines[first:last]=[new]
    result=''.join(lines)
    # Insert helpers and wrappers before any execution, while preserving main.
    guards = [n for n in ast.parse(result).body if isinstance(n, ast.If)
        and isinstance(n.test, ast.Compare) and isinstance(n.test.left, ast.Name)
        and n.test.left.id == '__name__' and len(n.test.comparators) == 1
        and isinstance(n.test.comparators[0], ast.Constant)
        and n.test.comparators[0].value == '__main__']
    assert len(guards) == 1
    parts = result.splitlines(keepends=True)
    parts.insert(guards[0].lineno-1, helper+'\n'+WRAPPERS+'\n')
    result = ''.join(parts)
    ast.parse(result)
    return result, {'ledger_added':added,'runtime_function_changes':[
        'build_the_iald_index','prove_the_iald_index','iald_index',
        '_v375_measure_trace_tracial_not_consumed','verify_tgl_kernel_formalization','_v392_axiom_coverage'],
        'embedded_changes':['TGL/Audit.lean'],
        'scope':'No scientific coefficient, observation, gate function, original or prior candidate changed. Full rerun is still required.'}
