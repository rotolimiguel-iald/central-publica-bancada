"""Read-only source browser and reproducible local calculations for the TGL bench."""

from __future__ import annotations

import hashlib
import json
import math
import re
import sqlite3
import struct
import sys
import unicodedata
import data_lab
import gpu_status
import treatment
import treatment_coverage
import resident_bridge
from contextlib import closing
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


HERE = Path(__file__).resolve().parent
CHATGPT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
STRUCTURE = CHATGPT / "APP_ESTRUTURA_V368_20260919" / "estrutura_v368.json"
PROOF = CHATGPT / "APP_ESTRUTURA_V368_20260919" / "proof_manifest.json"
REPORT_A = CHATGPT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_016_RELATORIO_FINAL.md"
REPORT_B = CHATGPT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_015_RELATORIO_FINAL.md"
ATLAS = Path(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md")
GW_CACHE = CHATGPT / "ORDEM_013_RINGDOWN" / "cache"
DB = HERE / "state" / "runs.sqlite3"
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
STATIC = HERE / "static"
CANONICAL_FORM = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_forma_canonica.md")
LIVE_UM = CANONICAL_FORM.with_name("um.py")
BAO_D9_SOURCE = Path(r"C:\IALD\Artigo\frente_alpha\tgl_multiprobe_v3.py")
BAO_D9_REPORT = Path(r"C:\IALD\Artigo\frente_alpha\output_v3\multiprobe_v3_report_20260522_135856.json")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def source_record(path: Path, label: str, status: str) -> dict:
    if not path.is_file():
        return {"label": label, "status": "UNAVAILABLE", "path": str(path)}
    return {"label": label, "status": status, "path": str(path),
            "size_bytes": path.stat().st_size, "sha256": digest(path)}


def read_bao_report() -> dict:
    if not BAO_D9_REPORT.is_file() or not BAO_D9_SOURCE.is_file():
        raise FileNotFoundError("D9 historical report or model source unavailable")
    if BAO_D9_REPORT.stat().st_size > 100_000:
        raise ValueError("D9 report exceeds expected size")
    with BAO_D9_REPORT.open(encoding="utf-8") as source:
        report = json.load(source)
    result = report["main_body"]["D9"]
    if result.get("name") != "D9_DESI_DR2_BAO" or result.get("N_measurements") != 13 or result.get("DOF") != 11:
        raise ValueError("Unexpected D9 report structure")
    lcdm, tgl = result["LCDM_bestfit"], result["TGL_bestfit"]
    numbers = [lcdm[key] for key in ("Om0", "rd_Mpc", "chi2", "chi2_reduced")]
    numbers += [tgl[key] for key in ("Om0", "rd_Mpc", "chi2", "chi2_reduced")]
    numbers.append(result["delta_chi2_TGL_minus_LCDM"])
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value)
           for value in numbers):
        raise ValueError("D9 report has nonfinite or nonnumeric values")
    if not math.isclose(tgl["chi2"] - lcdm["chi2"], result["delta_chi2_TGL_minus_LCDM"], abs_tol=1e-9):
        raise ValueError("D9 report delta chi2 does not match its best fits")
    return {"status": "HISTORICAL_REPORT_NOT_REEXECUTED", "observations": 13,
            "degrees_of_freedom": result["DOF"], "lcdm": lcdm, "tgl": tgl,
            "delta_chi2_tgl_minus_lcdm": result["delta_chi2_TGL_minus_LCDM"],
            "reported_timestamp_utc": report.get("metadata", {}).get("timestamp_utc"),
            "report": source_record(BAO_D9_REPORT, "Relatório D9", "HISTORICAL_REPORT"),
            "model_source_now": source_record(BAO_D9_SOURCE, "Script D9 atual", "SOURCE_NOT_REEXECUTED"),
            "scope": "χ² e parâmetros lidos do relatório histórico. O relatório não fixa o hash do script que o produziu; o hash atual do script não prova reprodução. A transformação antiga de Δχ² em σ/veredito não é exibida como significância calibrada."}


def load_index() -> dict:
    if not STRUCTURE.is_file():
        raise FileNotFoundError(f"Formal index unavailable: {STRUCTURE}")
    with STRUCTURE.open(encoding="utf-8") as source:
        return json.load(source)


def initialize_db() -> None:
    DB.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DB)) as conn, conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_utc TEXT NOT NULL,
            operation TEXT NOT NULL,
            parameters_json TEXT NOT NULL,
            result_json TEXT NOT NULL,
            source_sha256 TEXT NOT NULL,
            status TEXT NOT NULL
        )""")
        conn.execute("""CREATE TRIGGER IF NOT EXISTS runs_no_update BEFORE UPDATE ON runs
                     BEGIN SELECT RAISE(ABORT, 'runs are append-only'); END""")
        conn.execute("""CREATE TRIGGER IF NOT EXISTS runs_no_delete BEFORE DELETE ON runs
                     BEGIN SELECT RAISE(ABORT, 'runs are append-only'); END""")
        conn.execute("""CREATE TABLE IF NOT EXISTS inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_utc TEXT NOT NULL,
            question TEXT NOT NULL,
            hypothesis TEXT NOT NULL,
            falsifier TEXT NOT NULL,
            result_json TEXT NOT NULL,
            source_sha256 TEXT NOT NULL,
            status TEXT NOT NULL
        )""")
        conn.execute("""CREATE TRIGGER IF NOT EXISTS inquiries_no_update BEFORE UPDATE ON inquiries
                     BEGIN SELECT RAISE(ABORT, 'inquiries are append-only'); END""")
        conn.execute("""CREATE TRIGGER IF NOT EXISTS inquiries_no_delete BEFORE DELETE ON inquiries
                     BEGIN SELECT RAISE(ABORT, 'inquiries are append-only'); END""")
        conn.execute("""CREATE TABLE IF NOT EXISTS inquiry_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_utc TEXT NOT NULL,
            inquiry_id INTEGER NOT NULL REFERENCES inquiries(id),
            event_type TEXT NOT NULL,
            note TEXT NOT NULL,
            related_inquiry_id INTEGER REFERENCES inquiries(id)
        )""")
        conn.execute("""CREATE TRIGGER IF NOT EXISTS inquiry_events_no_update BEFORE UPDATE ON inquiry_events
                     BEGIN SELECT RAISE(ABORT, 'inquiry events are append-only'); END""")
        conn.execute("""CREATE TRIGGER IF NOT EXISTS inquiry_events_no_delete BEFORE DELETE ON inquiry_events
                     BEGIN SELECT RAISE(ABORT, 'inquiry events are append-only'); END""")


def number(payload: dict, key: str, minimum: float, maximum: float) -> float:
    value = payload.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key}: número obrigatório")
    value = float(value)
    if not math.isfinite(value) or not minimum <= value <= maximum:
        raise ValueError(f"{key}: fora do intervalo [{minimum}, {maximum}]")
    return value


def calculate(payload: dict) -> dict:
    operation = payload.get("operation")
    beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
    if operation == "identity_chain":
        theta = math.asin(math.sqrt(beta))
        return {
            "operation": operation, "status": "DERIVED_WITH_INPUT",
            "values": {"alpha_input": ALPHA_FINE_CODATA_2018,
                       "half_nat": 0.5, "sqrt_e": math.sqrt(math.e),
                       "beta": beta, "theta_rad": theta,
                       "reflection_probability": beta,
                       "transmission_probability": 1 - beta,
                       "unitarity_residual": abs(beta + (1 - beta) - 1)},
            "scope": "Conta algébrica; alpha é entrada CODATA 2018. Não testa a natureza."
        }
    if operation == "dephasing":
        omega = number(payload, "omega_rad_s", 0, 1e40)
        tau = number(payload, "tau_s", 0, 1e10)
        duration = number(payload, "duration_s", 0, 1e10)
        gamma = 0.5 * beta * tau * omega * omega
        if not math.isfinite(gamma):
            raise ValueError("Gamma não finito para esses parâmetros")
        exponent = gamma * duration
        if not math.isfinite(exponent):
            raise ValueError("Gamma × duração não finito para esses parâmetros")
        values = [math.exp(-exponent * i / 50) if exponent * i / 50 < 745 else 0.0
                  for i in range(51)]
        return {
            "operation": operation, "status": "CONDITIONAL_MODEL_CALCULATION",
            "values": {"beta": beta, "gamma_per_s": gamma,
                       "coherence_fraction": values[-1], "curve": values},
            "scope": "Gamma=beta*tau*omega^2/2. tau e omega são entradas; a conta não identifica um sistema físico nem calibra significância."
        }
    raise ValueError("Operação não permitida")


def list_data() -> list[dict]:
    groups = [
        ("GWOSC strain local", GW_CACHE / "gwosc", "*.hdf5", "OFFICIAL_ORIGIN_RECEIPT_CHECK_REQUIRED"),
        ("GWTC-3 ringdown metadata", GW_CACHE / "gwtc3_220", "*.json", "LOCAL_METADATA_ORIGIN_TO_VERIFY"),
        ("PSD e curvas de projeto", GW_CACHE / "psd", "*", "MIXED_OBSERVED_AND_DESIGN_INPUTS"),
    ]
    output = []
    for label, root, pattern, status in groups:
        files = []
        if root.is_dir():
            for path in sorted(root.rglob(pattern)):
                if path.is_file() and not path.is_symlink():
                    files.append({"name": path.name, "path": str(path),
                                  "bytes": path.stat().st_size,
                                  "receipt": path.with_name(path.name + ".receipt.json").is_file()})
        output.append({"label": label, "status": status, "root": str(root),
                       "count": len(files), "files": files[:100],
                       "truncated": len(files) > 100})
    return output


def list_protocols() -> list[dict]:
    output = []
    pattern = re.compile(r"^\|\s*(?:\*\*)?(A[0-8]|T(?:0[1-9]|1[0-9]))(?:\*\*)?\s*\|\s*(.*?)\s*\|")
    for report, family in ((REPORT_A, "ORDEM016"), (REPORT_B, "ORDEM015")):
        if not report.is_file():
            continue
        report_hash = digest(report)
        for line_no, line in enumerate(report.read_text(encoding="utf-8").splitlines(), 1):
            match = pattern.match(line)
            if not match:
                continue
            target, raw = match.groups()
            status = "MEDIDA" if family == "ORDEM016" else re.sub(r"[*`]", "", raw).strip()[:90]
            output.append({"target": target, "family": family, "reported_status": status,
                           "summary": re.sub(r"[*`]", "", raw).strip()[:400],
                           "source_path": str(report), "source_line": line_no,
                           "source_sha256": report_hash,
                           "replay_status": "NOT_CONNECTED_TO_THIS_BENCH"})
    return output


STOPWORDS = {"a", "as", "o", "os", "de", "do", "da", "dos", "das", "e", "em", "no", "na",
             "um", "uma", "como", "qual", "quais", "para", "por", "com", "que", "sobre",
             "the", "and", "from", "does", "entre", "isso", "esta", "este", "ser",
             "onde", "encontro", "existe", "existem", "pode", "podem", "sera", "tgl"}


def terms_of(value: str) -> list[str]:
    normalized = unicodedata.normalize("NFKD", value.casefold())
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return [word for word in dict.fromkeys(re.findall(r"[a-z0-9_]+", normalized))
            if len(word) > 2 and word not in STOPWORDS][:10]


def investigate(index: dict, payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("Objeto JSON obrigatório")
    fields = {}
    for key, maximum in (("question", 500), ("hypothesis", 500), ("falsifier", 500),
                         ("alternative", 500), ("instrumental", 500), ("discriminator", 500)):
        value = payload.get(key, "")
        if not isinstance(value, str) or len(value) > maximum:
            raise ValueError(f"{key}: texto inválido ou maior que {maximum} caracteres")
        fields[key] = value.strip()
    if len(fields["question"]) < 8:
        raise ValueError("A pergunta deve conter ao menos 8 caracteres")
    words = terms_of(fields["question"])
    if not words:
        raise ValueError("A pergunta precisa de um termo de pesquisa específico")

    formal = []
    for module_name, module in index.get("modules", {}).items():
        declarations = module.get("declarations", [])
        title = " ".join(terms_of(module_name))
        matching = [d for d in declarations
                    if any(word in " ".join(terms_of(str(d.get("short_name", "")))) for word in words)]
        score = sum(word in title for word in words) * 2 + min(len(matching), 4)
        if score:
            formal.append({"module": module_name, "path": module.get("path"),
                           "declarations": matching[:4], "score": score,
                           "status": "SOURCE_LOCATOR_NOT_RECOMPILED"})
    formal.sort(key=lambda item: (-item["score"], item["module"]))

    protocols = []
    for item in list_protocols():
        text = " ".join(terms_of(item["summary"] + " " + item["target"]))
        score = sum(word in text for word in words)
        if score:
            protocols.append({"target": item["target"], "family": item["family"],
                              "summary": item["summary"], "source_path": item["source_path"],
                              "source_line": item["source_line"], "source_sha256": item["source_sha256"],
                              "replay_status": item["replay_status"], "score": score})
    protocols.sort(key=lambda item: (-item["score"], item["target"]))

    datasets = []
    for group in list_data():
        labels = " ".join(terms_of(group["label"] + " " + " ".join(f["name"] for f in group["files"][:100])))
        score = sum(word in labels for word in words)
        if score:
            datasets.append({"label": group["label"], "root": group["root"],
                             "count": group["count"], "status": group["status"],
                             "score": score})
    datasets.sort(key=lambda item: -item["score"])

    return {
        **fields,
        "terms": words,
        "formal": formal[:8], "formal_total": len(formal),
        "protocols": protocols[:6], "protocol_total": len(protocols),
        "datasets": datasets[:3],
        "index_release": index.get("release"),
        "source_sha256": digest(STRUCTURE),
        "status": "EXPLORATORY_SOURCE_MAP",
        "analysis_stage": "EXPLORATORY_NOT_PREREGISTERED",
        "open_items": (["Hipótese ainda não formulada"] if not fields["hypothesis"] else []) +
                      (["Resultado que a refutaria ainda não formulado"] if not fields["falsifier"] else []) +
                      (["Explicação rival ainda não formulada"] if not fields["alternative"] else []) +
                      (["Possível efeito instrumental ainda não examinado"] if not fields["instrumental"] else []) +
                      (["Medição ou cálculo discriminante ainda não escolhido"] if not fields["discriminator"] else []) +
                      (["Nenhuma fonte localizada; refine os termos"] if not formal and not protocols and not datasets else []),
        "method": "Busca lexical determinística em índice histórico, relatórios e catálogo local; correspondência não prova relação causal ou física.",
    }


class BenchHandler(BaseHTTPRequestHandler):
    index: dict = {}

    def log_message(self, format: str, *args) -> None:
        # pythonw without redirected stderr has no console stream.
        if sys.stderr is not None:
            super().log_message(format, *args)

    def respond(self, status: int, data: dict | list) -> None:
        body = json.dumps(data, ensure_ascii=False, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        request = urlparse(self.path)
        params = parse_qs(request.query)
        if request.path.startswith('/api/universe/'):
            try:
                if request.path=='/api/universe/domains': result=resident_bridge.domains()
                elif request.path=='/api/universe/status': result=resident_bridge.status()
                elif request.path=='/api/universe/view': result=resident_bridge.view(params)
                elif request.path=='/api/universe/event': result=resident_bridge.event_metadata()
                else: raise ValueError('Unknown universe endpoint')
                self.respond(200,result)
            except (ValueError,OSError,TypeError) as exc:self.respond(400,{'error':str(exc)})
        elif request.path == "/api/overview":
            modules = self.index.get("modules", {})
            declarations = sum(len(item.get("declarations", [])) for item in modules.values())
            self.respond(200, {
                "name": "Bancada Oficial TGL — protótipo local",
                "index_release": self.index.get("release"),
                "index_scope": "Snapshot v368; não é compilação atual nem instalação canônica.",
                "module_count": len(modules), "declaration_count": declarations,
                "route_count": len(self.index.get("routes", [])),
                "sources": [source_record(STRUCTURE, "Índice formal v368", "HISTORICAL_SNAPSHOT"),
                            source_record(PROOF, "Manifesto de prova v368", "HISTORICAL_SNAPSHOT"),
                            source_record(REPORT_A, "Relatório ORDEM016", "DOCUMENTARY_REPORT"),
                            source_record(REPORT_B, "Relatório ORDEM015", "DOCUMENTARY_REPORT"),
                            source_record(ATLAS, "Atlas documental TGL", "VOCABULARY_AND_STATUS")],
                "gate": "READ_ONLY: a bancada não altera nem promove o gate."
            })
        elif request.path == "/api/relations":
            query = params.get("q", [""])[0].strip().lower()[:100]
            try:
                limit = min(max(int(params.get("limit", ["50"])[0]), 1), 100)
            except ValueError:
                self.respond(400, {"error": "limit inválido"})
                return
            matches = []
            for module_name, module in self.index.get("modules", {}).items():
                declarations = module.get("declarations", [])
                if query in module_name.lower() or any(query in str(d.get("short_name", "")).lower() for d in declarations):
                    selected = [d for d in declarations if not query or query in str(d.get("short_name", "")).lower()]
                    matches.append({"module": module_name, "path": module.get("path"),
                                    "imports": module.get("imports", [])[:12],
                                    "declarations": selected[:12], "declaration_count": len(declarations),
                                    "status": "SOURCE_LOCATOR_NOT_RECOMPILED"})
                    if len(matches) >= limit:
                        break
            self.respond(200, {"query": query, "matches": matches, "limited": len(matches) == limit})
        elif request.path == "/api/routes":
            self.respond(200, self.index.get("routes", []))
        elif request.path == "/api/data":
            self.respond(200, list_data())
        elif request.path == "/api/lab/memory":
            try:
                self.respond(200, data_lab.memory_status())
            except OSError as exc:
                self.respond(503, {"error": str(exc)})
        elif request.path == "/api/lab/gpu":
            self.respond(200, gpu_status.status())
        elif request.path == "/api/lab/catalog":
            items = data_lab.catalog()
            self.respond(200, {"items": items, "count": len(items),
                               "bytes": sum(item["bytes"] for item in items),
                               "status": "INSTALLED_FILES_NOT_PHYSICALLY_VALIDATED"})
        elif request.path == "/api/lab/coverage":
            self.respond(200, treatment_coverage.coverage_report())
        elif request.path == "/api/lab/canonical":
            if not CANONICAL_FORM.is_file() or not LIVE_UM.is_file():
                self.respond(503, {"error": "Forma canônica ou programa vivo indisponível"})
                return
            content = CANONICAL_FORM.read_text(encoding="utf-8")
            first_block = re.search(r"## A cadeia canônica[^\n]*\n\s*```\s*\n(.*?)\n```", content, re.S)
            headings = re.findall(r"^##\s+(.+)$", content, re.M)
            self.respond(200, {"form": source_record(CANONICAL_FORM, "Forma canônica viva", "DOCUMENTARY_FORM"),
                               "program": source_record(LIVE_UM, "um.py vivo", "SOURCE_NOT_EXECUTED_BY_BENCH"),
                               "chain_excerpt": first_block.group(1)[:6500] if first_block else "",
                               "section_count": len(headings), "latest_sections": headings[-8:],
                               "bao_model": source_record(BAO_D9_SOURCE, "D9: previsão BAO TGL e ΛCDM", "EXISTING_MODEL_NOT_EXECUTED_BY_BENCH"),
                               "status": "READ_ONLY_SOURCE_NOT_RECOMPUTED_HERE"})
        elif request.path == "/api/lab/bao-report":
            try:
                self.respond(200, read_bao_report())
            except (FileNotFoundError, ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as exc:
                self.respond(503, {"error": str(exc)})
        elif request.path == "/api/lab/treatment":
            try:
                path = data_lab.selected(params.get("id", [""])[0])
                self.respond(200, treatment.record(path))
            except (ValueError, OSError) as exc:
                self.respond(400, {"error": str(exc)})
        elif request.path in ("/api/lab/describe", "/api/lab/preview"):
            try:
                identifier = params.get("id", [""])[0]
                path = data_lab.selected(identifier)
                if request.path.endswith("describe"):
                    metadata = data_lab.describe(path)
                    metadata.pop("_internal")
                    self.respond(200, metadata)
                else:
                    x, y = params.get("x", [""])[0], params.get("y", [""])[0]
                    limit = int(params.get("limit", ["800"])[0])
                    self.respond(200, data_lab.preview(path, x, y, limit))
            except (ValueError, KeyError, OSError, struct.error) as exc:
                self.respond(400, {"error": str(exc)})
        elif request.path == "/api/protocols":
            self.respond(200, list_protocols())
        elif request.path == "/api/runs":
            with closing(sqlite3.connect(DB)) as conn:
                conn.row_factory = sqlite3.Row
                rows = [dict(row) for row in conn.execute("SELECT id, created_utc, operation, parameters_json, result_json, source_sha256, status FROM runs ORDER BY id DESC LIMIT 40")]
            output = []
            for row in rows:
                row["parameters"] = json.loads(row.pop("parameters_json"))
                row["result"] = json.loads(row.pop("result_json"))
                output.append(row)
            self.respond(200, output)
        elif request.path == "/api/inquiries":
            with closing(sqlite3.connect(DB)) as conn:
                conn.row_factory = sqlite3.Row
                rows = [dict(row) for row in conn.execute(
                    "SELECT id, created_utc, question, hypothesis, falsifier, result_json, source_sha256, status "
                    "FROM inquiries ORDER BY id DESC LIMIT 20")]
                ids = {row["id"] for row in rows}
                events = [dict(row) for row in conn.execute(
                    "SELECT id, created_utc, inquiry_id, event_type, note, related_inquiry_id "
                    "FROM inquiry_events ORDER BY id") if row["inquiry_id"] in ids]
            for row in rows:
                row["result"] = json.loads(row.pop("result_json"))
                row["events"] = [event for event in events if event["inquiry_id"] == row["id"]]
            self.respond(200, rows)
        elif request.path in ("/", "/universe", "/universe.js", "/universe.css", "/app.js", "/style.css", "/protocols.css", "/TGL.svg", "/favicon.ico"):
            name = "index.html" if request.path == "/" else "universe.html" if request.path=='/universe' else request.path[1:]
            path = STATIC / name
            if not path.is_file():
                self.respond(404, {"error": "Recurso ausente"})
                return
            body = path.read_bytes()
            mime = {"index.html": "text/html", "universe.html":"text/html", "universe.js":"text/javascript", "universe.css":"text/css", "app.js": "text/javascript", "style.css": "text/css", "protocols.css": "text/css", "TGL.svg": "image/svg+xml", "favicon.ico": "image/x-icon"}[name]
            self.send_response(200)
            self.send_header("Content-Type", mime + "; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.respond(404, {"error": "Rota ausente"})

    def do_POST(self) -> None:
        if self.path not in ("/api/run", "/api/inquiry", "/api/universe/load", "/api/universe/model", "/api/universe/release", "/api/universe/event_view"):
            self.respond(404, {"error": "Rota ausente"})
            return
        try:
            origin = self.headers.get("Origin", "")
            if origin and origin != f"http://127.0.0.1:{self.server.server_port}":
                raise ValueError("Origem não autorizada")
            if self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower() != "application/json":
                raise ValueError("Content-Type application/json obrigatório")
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 8192:
                raise ValueError("Corpo inválido ou muito grande")
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("Objeto JSON obrigatório")
            if self.path.startswith('/api/universe/'):
                if self.path.endswith('/load'): result=resident_bridge.load(payload.get('domain'))
                elif self.path.endswith('/model'): result=resident_bridge.model(payload)
                elif self.path.endswith('/event_view'): result=resident_bridge.event_view(payload)
                else: result=resident_bridge.release()
                self.respond(200,result)
                return
            if self.path == "/api/inquiry":
                result = investigate(self.index, payload)
                with closing(sqlite3.connect(DB)) as conn, conn:
                    cursor = conn.execute(
                        "INSERT INTO inquiries(created_utc, question, hypothesis, falsifier, result_json, source_sha256, status) "
                        "VALUES (?,?,?,?,?,?,?)",
                        (utc_now(), result["question"], result["hypothesis"], result["falsifier"],
                         json.dumps(result, ensure_ascii=False), result["source_sha256"], result["status"]))
                    inquiry_id = cursor.lastrowid
                self.respond(201, {"inquiry_id": inquiry_id, "result": result})
                return
            result = calculate(payload)
            result["engine_sha256"] = digest(Path(__file__))
            result["constant_origin"] = "CODATA 2018 alpha input; TGL_ATLAS.md §I.3"
            result["atlas_sha256"] = digest(ATLAS) if ATLAS.is_file() else None
            source_hash = digest(STRUCTURE)
            with closing(sqlite3.connect(DB)) as conn, conn:
                cursor = conn.execute("INSERT INTO runs(created_utc, operation, parameters_json, result_json, source_sha256, status) VALUES (?,?,?,?,?,?)",
                                      (utc_now(), result["operation"], json.dumps(payload, sort_keys=True),
                                       json.dumps(result, sort_keys=True), source_hash, result["status"]))
                run_id = cursor.lastrowid
            self.respond(201, {"run_id": run_id, "result": result, "source_sha256": source_hash})
        except (ValueError, TypeError, OSError, json.JSONDecodeError, OverflowError) as exc:
            self.respond(400, {"error": str(exc)})


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Bancada local da TGL")
    parser.add_argument("--port", type=int, default=18765)
    args = parser.parse_args()
    BenchHandler.index = load_index()
    initialize_db()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), BenchHandler)
    print(f"Bancada TGL: http://127.0.0.1:{server.server_port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
