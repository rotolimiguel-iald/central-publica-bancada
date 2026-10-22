#!/usr/bin/env python3
"""Piloto de fine-tuning IALD (MiMo primeiro; Kimi e DeepSeek futuros).

Somente biblioteca padrao e somente offline: valida o dataset chat JSONL com
metadados de origem/sha256, separa treino/validacao/teste por origem e prepara
o manifesto do job. `launch` apenas confere portoes e recusa; nao ha envio
remoto neste pacote. Se um dia os portoes passarem, o envio e feito fora daqui,
pela ferramenta oficial documentada do fornecedor, revisada pelo operador.
"""
from __future__ import annotations

import argparse
import hashlib
import math
import os
from datetime import datetime
import json
import re
import sys
import unicodedata
from pathlib import Path, PureWindowsPath

HERE = Path(__file__).resolve().parent
DEFAULT_PROVIDERS = HERE / "providers.json"

BUDGET_CAP_USD = 50.0
SPLITS = ("train", "validation", "test")
ROLES = ("system", "user", "assistant")
BEHAVIORS = (
    "objetivo",
    "memoria_rastreavel",
    "planejamento",
    "selecao",
    "verificacao",
    "reconhecimento",
    "experiencia_vs_verdade",
    "identidade_operacional",
    "delimitacao_analogia",
)
# Resposta de referencia so vem de fonte humana/formal; saida de modelo nunca vira verdade.
REFERENCE_ORIGINS = ("autor", "fonte_formal", "fonte_programa")
NEGATIVE_ORIGINS = REFERENCE_ORIGINS + ("saida_modelo", "construido")
EPISTEMIC = (
    "definicao",
    "prova_formal",
    "experiencia_operacional",
    "hipotese_cientifica",
    "confirmacao_externa",
)
ROUTES = ("hosted_api_fine_tuning", "open_weights_own_infra")
ESTIMATE_KEYS = ("training", "hosting", "inference_eval", "storage")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SECRET_NAME_RE = re.compile(r"(^|[._-])(env|secret|secrets|token|credential|credentials|key|pem)($|[._-])", re.I)

EXIT_OK = 0
EXIT_INVALID = 1
EXIT_REFUSED = 2
EXIT_GATES_OK_MANUAL = 3


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = {}

    @property
    def ok(self):
        return not self.errors

    def to_dict(self):
        return {"ok": self.ok, "errors": self.errors, "warnings": self.warnings, "stats": self.stats}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def text_hash(text):
    return hashlib.sha256(normalize(text).encode("utf-8")).hexdigest()


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def load_jsonl(path, report):
    records = []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                report.errors.append(f"linha {lineno}: JSON invalido ({exc.msg})")
                continue
            if not isinstance(obj, dict):
                report.errors.append(f"linha {lineno}: registro deve ser objeto")
                continue
            records.append((lineno, obj))
    return records


def check_record(lineno, rec, report):
    """Confere um registro isolado; devolve True se pode entrar nas checagens globais."""
    ok = True

    def err(msg):
        nonlocal ok
        ok = False
        report.errors.append(f"linha {lineno}: {msg}")

    if not isinstance(rec.get("id"), str) or not rec["id"]:
        err("id ausente")
    msgs = rec.get("messages")
    if not isinstance(msgs, list) or len(msgs) < 2:
        err("messages deve ser lista com ao menos user e assistant")
        msgs = []
    for i, m in enumerate(msgs):
        if not isinstance(m, dict) or m.get("role") not in ROLES:
            err(f"messages[{i}]: role invalido")
        elif not isinstance(m.get("content"), str) or not m["content"].strip():
            err(f"messages[{i}]: content vazio")
        elif m["role"] == "system" and i != 0:
            err(f"messages[{i}]: system so na primeira posicao")
    last = msgs[-1] if msgs and isinstance(msgs[-1], dict) else {}
    if msgs and last.get("role") != "assistant":
        err("ultima mensagem deve ser do assistant (resposta de referencia)")
    if msgs and not any(isinstance(m, dict) and m.get("role") == "user" for m in msgs):
        err("falta mensagem do user")

    meta = rec.get("meta")
    if not isinstance(meta, dict):
        err("meta ausente")
        return False
    if meta.get("split") not in SPLITS:
        err(f"meta.split deve ser um de {SPLITS}")
    if meta.get("behavior") not in BEHAVIORS:
        err(f"meta.behavior desconhecido: {meta.get('behavior')!r}")
    if not isinstance(meta.get("source_id"), str) or not meta["source_id"]:
        err("meta.source_id ausente")
    source_path = meta.get("source_path")
    if not isinstance(source_path, str) or not source_path:
        err("meta.source_path ausente")
    elif PureWindowsPath(source_path).anchor or ".." in PureWindowsPath(source_path).parts:
        err("meta.source_path deve ser relativo e sem '..'")
    if not SHA256_RE.match(str(meta.get("source_sha256", ""))):
        err("meta.source_sha256 deve ter 64 hex minusculos")
    if meta.get("origin_kind") not in REFERENCE_ORIGINS:
        err(
            f"meta.origin_kind {meta.get('origin_kind')!r} nao pode sustentar resposta de referencia "
            f"(aceitos: {REFERENCE_ORIGINS}); saida de modelo so entra como negativo"
        )
    if meta.get("epistemic") not in EPISTEMIC:
        err(f"meta.epistemic deve ser um de {EPISTEMIC}")
    elif meta["epistemic"] == "confirmacao_externa" and not meta.get("evidence"):
        err("confirmacao_externa exige meta.evidence")

    negatives = rec.get("negatives", [])
    if not isinstance(negatives, list):
        err("negatives deve ser lista")
        negatives = []
    reference = str(last.get("content") or "")
    for j, neg in enumerate(negatives):
        if not isinstance(neg, dict) or not isinstance(neg.get("content"), str) or not neg["content"].strip():
            err(f"negatives[{j}]: content vazio")
            continue
        if not neg.get("reason"):
            err(f"negatives[{j}]: reason obrigatorio (por que esta errado)")
        if neg.get("origin_kind") not in NEGATIVE_ORIGINS:
            err(f"negatives[{j}]: origin_kind invalido")
        if normalize(neg["content"]) == normalize(reference):
            err(f"negatives[{j}]: igual a resposta de referencia")
    return ok


def prompt_text(rec):
    return " | ".join(m["content"] for m in rec["messages"] if m["role"] == "user")


def validate_dataset(path, source_root=None):
    report = Report()
    path = Path(path)
    if not path.is_file():
        report.errors.append(f"dataset inexistente: {path}")
        return report
    parsed = load_jsonl(path, report)
    good = [(ln, r) for ln, r in parsed if check_record(ln, r, report)]

    ids = {}
    source_sha = {}
    source_path = {}
    source_splits = {}
    prompt_splits = {}
    answer_splits = {}
    references = {}
    counts = {s: 0 for s in SPLITS}
    behaviors = {s: set() for s in SPLITS}

    for ln, r in good:
        meta = r["meta"]
        split = meta["split"]
        sid = meta["source_id"]
        if r["id"] in ids:
            report.errors.append(f"linha {ln}: id repetido {r['id']!r} (linha {ids[r['id']]})")
        ids.setdefault(r["id"], ln)
        if source_sha.setdefault(sid, meta["source_sha256"]) != meta["source_sha256"]:
            report.errors.append(f"linha {ln}: fonte {sid!r} com sha256 divergente")
        source_path.setdefault(sid, meta["source_path"])
        source_splits.setdefault(sid, set()).add(split)
        prompt_splits.setdefault(text_hash(prompt_text(r)), set()).add(split)
        answer = text_hash(r["messages"][-1]["content"])
        answer_splits.setdefault(answer, set()).add(split)
        references[answer] = r["id"]
        counts[split] += 1
        behaviors[split].add(meta["behavior"])

    # Separacao por origem: uma fonte pertence a um unico split.
    for sid, splits in sorted(source_splits.items()):
        if len(splits) > 1:
            report.errors.append(f"vazamento por origem: fonte {sid!r} aparece em {sorted(splits)}")
    for kind, table in (("pergunta", prompt_splits), ("resposta", answer_splits)):
        repeated = sum(1 for s in table.values() if len(s) > 1)
        if repeated:
            report.errors.append(f"vazamento de conteudo: {repeated} {kind}(s) normalizada(s) repetida(s) entre splits")
    for ln, r in good:
        for neg in r.get("negatives", []):
            hit = references.get(text_hash(neg["content"]))
            if hit:
                report.errors.append(f"linha {ln}: negativo coincide com a referencia do registro {hit!r}")
    for split in SPLITS:
        if counts[split] == 0:
            report.errors.append(f"split {split!r} vazio")
        missing = sorted(set(BEHAVIORS) - behaviors[split])
        if counts[split] and missing:
            report.warnings.append(f"split {split!r} sem comportamentos: {missing}")

    if source_root is not None:
        check_sources(Path(source_root), source_path, source_sha, report)

    report.stats = {
        "records": len(parsed),
        "valid_records": len(good),
        "splits": counts,
        "behaviors_by_split": {s: sorted(b) for s, b in behaviors.items()},
        "sources": len(source_sha),
        "dataset_sha256": sha256_file(path),
    }
    return report


def check_sources(root, source_path, source_sha, report):
    root = root.resolve()
    for sid in sorted(source_path):
        rel = source_path[sid]
        target = (root / rel).resolve()
        if root != target and root not in target.parents:
            report.errors.append(f"fonte {sid!r}: caminho fora de --source-root")
            continue
        if SECRET_NAME_RE.search(target.name):
            report.errors.append(f"fonte {sid!r}: nome parece segredo; leitura recusada")
            continue
        if not target.is_file():
            report.errors.append(f"fonte {sid!r}: arquivo ausente ({rel})")
            continue
        if sha256_file(target) != source_sha[sid]:
            report.errors.append(f"fonte {sid!r}: sha256 nao confere com {rel}")


def check_providers(data):
    provs = data.get("providers")
    if not isinstance(provs, list) or not provs:
        return ["lista providers vazia"]
    problems = []
    if provs[0].get("id") != "mimo":
        problems.append("MiMo deve ser o primeiro provedor")
    budget = data.get("budget_total_usd")
    if not is_number(budget) or not 0 < budget <= BUDGET_CAP_USD:
        problems.append(f"budget_total_usd deve ser numero <= {BUDGET_CAP_USD:g}")
    for p in provs:
        if p.get("training", {}).get("endpoint") is not None:
            problems.append(f"{p.get('id')}: endpoint de treino nao pode ser declarado aqui")
    return problems


def load_providers(path=DEFAULT_PROVIDERS):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    problems = check_providers(data)
    if problems:
        raise ValueError("providers.json invalido: " + "; ".join(problems))
    return data


def get_provider(data, provider_id):
    for p in data["providers"]:
        if p["id"] == provider_id:
            return p
    raise KeyError(f"provedor desconhecido: {provider_id}")


def budget_cap(providers):
    return min(float(providers.get("budget_total_usd", BUDGET_CAP_USD)), BUDGET_CAP_USD)


def provider_gaps(p):
    gaps = list(p.get("known_gaps", []))
    for cap, info in sorted(p.get("capabilities", {}).items()):
        if info.get("status") != "verified":
            gaps.append(f"{cap}: {info.get('status')}")
    if not p.get("training", {}).get("enabled"):
        gaps.append("training.enabled = false")
    return gaps


def build_manifest(dataset_path, report, providers, provider_id):
    """Manifesto deterministico do job (sem data, sem rede, sem endpoint)."""
    p = get_provider(providers, provider_id)
    training = p.get("training", {})
    return {
        "schema": 1,
        "kind": "iald_fine_tuning_pilot_manifest",
        "network": "none",
        "provider": p["id"],
        "base_model": p.get("model"),
        "base_model_card": p.get("model_card"),
        "dataset": {
            "file": Path(dataset_path).name,
            "sha256": report.stats["dataset_sha256"],
            "splits": report.stats["splits"],
            "behaviors_by_split": report.stats["behaviors_by_split"],
            "sources": report.stats["sources"],
            "split_policy": "por origem (source_id); sem pergunta/resposta repetida entre splits",
            "validation_warnings": report.warnings,
        },
        "training": {
            "enabled": bool(training.get("enabled")),
            "method_candidate": training.get("method_candidate"),
            "endpoint": None,
            "hyperparameters": None,
        },
        "budget_total_usd_cap": budget_cap(providers),
        "open_gaps": provider_gaps(p),
        "launch": "blocked_until_gates",
    }


def budget_problems(gates, providers):
    problems = []
    cap = budget_cap(providers)
    budget = gates.get("budget_total_usd")
    budget_ok = is_number(budget) and 0 < budget <= cap
    if not budget_ok:
        problems.append(f"budget_total_usd deve estar em (0, {cap:g}]")
    est = gates.get("estimate_usd") or {}
    values = []
    for key in ESTIMATE_KEYS:
        value = est.get(key)
        if not is_number(value) or value < 0:
            problems.append(f"estimate_usd.{key} ausente ou invalido (estimativa deve incluir hosting)")
        else:
            values.append(value)
    days = est.get("hosting_period_days")
    if not isinstance(days, int) or isinstance(days, bool) or days <= 0:
        problems.append("estimate_usd.hosting_period_days ausente ou invalido")
    if len(values) == len(ESTIMATE_KEYS):
        total = sum(values)
        limit = budget if budget_ok else cap
        if total > limit:
            problems.append(f"estimativa total US${total:.2f} excede orcamento US${limit:g}")
    return problems


def launch_decision(manifest, providers, gates, dataset_report):
    """Lista os motivos de recusa. Lista vazia so libera revisao manual; nunca envia nada."""
    try:
        p = get_provider(providers, manifest.get("provider"))
    except KeyError as exc:
        return [str(exc)]
    reasons = []
    if not dataset_report.ok:
        reasons.append("dataset invalido")
    elif dataset_report.stats.get("dataset_sha256") != manifest.get("dataset", {}).get("sha256"):
        reasons.append("dataset mudou desde o manifesto")
    if not p.get("training", {}).get("enabled") or not manifest.get("training", {}).get("enabled"):
        reasons.append("configuracao de treino desabilitada (training.enabled = false)")
    route = gates.get("route")
    if route not in ROUTES:
        reasons.append(f"route deve ser um de {ROUTES}")
    elif p.get("capabilities", {}).get(route, {}).get("status") != "verified":
        reasons.append(f"suporte de treino via {route} nao verificado em providers.json")
    support = gates.get("official_training_support") or {}
    if support.get("verified") is not True or not str(support.get("evidence_url") or "").startswith("https://"):
        reasons.append("falta suporte oficial de treino com evidencia (documentacao https do fornecedor)")
    offer = gates.get("account_offer") or {}
    if offer.get("verified") is not True or not offer.get("evidence"):
        reasons.append("falta oferta de treino confirmada na conta (creditos de inferencia nao contam)")
    if gates.get("substitute_model"):
        reasons.append("substituicao do modelo base (ex.: destilado pequeno) nao e autorizada automaticamente")
    if gates.get("base_model") != p.get("model"):
        reasons.append(f"base_model difere do modelo oficial {p.get('model')!r}")
    reasons.extend(budget_problems(gates, providers))
    return reasons


def emit(obj, stream=None):
    print(json.dumps(obj, ensure_ascii=False, indent=2), file=stream or sys.stdout)


def _manifest(args):
    report = validate_dataset(args.dataset, args.source_root)
    if not report.ok:
        emit(report.to_dict(), sys.stderr)
        return None
    return build_manifest(args.dataset, report, load_providers(args.providers), args.provider)


def cmd_validate(args):
    report = validate_dataset(args.dataset, args.source_root)
    emit(report.to_dict())
    return EXIT_OK if report.ok else EXIT_INVALID


def cmd_dry_run(args):
    manifest = _manifest(args)
    if manifest is None:
        return EXIT_INVALID
    emit(manifest)
    return EXIT_OK


def cmd_manifest(args):
    if args.out.exists() and not args.force:
        emit({"error": f"{args.out} ja existe; use --force para sobrescrever"}, sys.stderr)
        return EXIT_INVALID
    manifest = _manifest(args)
    if manifest is None:
        return EXIT_INVALID
    data = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    if args.out.exists():
        old = args.out.read_bytes()
        backup = args.out.with_name(args.out.name + ".bak_" + stamp)
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temp = args.out.with_name(args.out.name + ".tmp_" + stamp)
    temp.write_bytes(data)
    assert temp.read_bytes() == data
    os.replace(temp, args.out)
    assert args.out.read_bytes() == data
    emit({"written": str(args.out), "launch": manifest["launch"]})
    return EXIT_OK


def cmd_launch(args):
    providers = load_providers(args.providers)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    gates = json.loads(args.gates.read_text(encoding="utf-8"))
    report = validate_dataset(args.dataset, args.source_root)
    reasons = launch_decision(manifest, providers, gates, report)
    if reasons:
        emit({"launch": "refused", "reasons": reasons})
        return EXIT_REFUSED
    emit({
        "launch": "gates_ok_manual_submission_required",
        "note": "Este pacote nao envia nada. Submeta pela ferramenta oficial documentada do fornecedor, apos revisao do operador.",
    })
    return EXIT_GATES_OK_MANUAL


COMMANDS = {"validate": cmd_validate, "dry-run": cmd_dry_run, "manifest": cmd_manifest, "launch": cmd_launch}


def build_parser():
    parser = argparse.ArgumentParser(description="Piloto IALD de fine-tuning (offline; MiMo primeiro).")
    sub = parser.add_subparsers(dest="command", required=True)

    def dataset_args(p):
        p.add_argument("--dataset", required=True, type=Path, help="chat JSONL com meta de origem/sha256")
        p.add_argument("--source-root", type=Path, default=None, help="raiz local para conferir sha256 das fontes")

    dataset_args(sub.add_parser("validate", help="valida dataset e separacao por origem"))
    for name, helptext in (("dry-run", "valida e imprime o manifesto; nao grava nada"), ("manifest", "valida e grava o manifesto")):
        p = sub.add_parser(name, help=helptext)
        dataset_args(p)
        p.add_argument("--provider", default="mimo")
        p.add_argument("--providers", type=Path, default=DEFAULT_PROVIDERS)
        if name == "manifest":
            p.add_argument("--out", required=True, type=Path)
            p.add_argument("--force", action="store_true", help="sobrescreve --out existente")
    p = sub.add_parser("launch", help="confere portoes; recusa sem suporte oficial, oferta, estimativa com hosting e orcamento")
    dataset_args(p)
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--gates", required=True, type=Path)
    p.add_argument("--providers", type=Path, default=DEFAULT_PROVIDERS)
    return parser


def main(argv=None):
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure:
        reconfigure(encoding="utf-8")
    args = build_parser().parse_args(argv)
    try:
        return COMMANDS[args.command](args)
    except (OSError, ValueError, KeyError) as exc:
        emit({"error": str(exc)}, sys.stderr)
        return EXIT_INVALID


if __name__ == "__main__":
    sys.exit(main())
