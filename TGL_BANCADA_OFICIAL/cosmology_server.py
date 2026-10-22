"""Independent local cosmology service; never restarts the resident GW worker."""
from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

import cosmology_runtime
import cosmology_scenarios
import cosmology_exports
import gpu_status

HERE = Path(__file__).resolve().parent
SERVICE_ID = "tgl-cosmology-resident-v1"
EXPORTS_ROUTE = "/api/cosmology/exports"
SCENARIOS_ROUTE = "/api/cosmology/scenarios"
STATIC = {
    "/": ("universe-map.html", "text/html"),
    "/explore": ("universe-map.html", "text/html"),
    "/universe-map.css": ("universe-map.css", "text/css"),
    "/universe-map.js": ("universe-map.js", "text/javascript"),
    "/cosmos-lessons.js": ("cosmos-lessons.js", "text/javascript"),
    "/cosmos-teaching-model.js": ("cosmos-teaching-model.js", "text/javascript"),
    "/cosmos": ("cosmos.html", "text/html"),
    "/cosmos.js": ("cosmos.js", "text/javascript"),
    "/cosmos.css": ("cosmos.css", "text/css"),
    "/favicon.ico": ("favicon.ico", "image/x-icon"),
    "/TGL.svg": ("TGL.svg", "image/svg+xml"),
}


def _json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Chave JSON repetida: " + key)
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError("Constante JSON inválida: " + value)


class CosmologyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        if sys.stderr is not None:
            super().log_message(format, *args)

    def send_bytes(self, code, body, mime):
        self.send_response(code)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def respond(self, code, data):
        self.send_bytes(code, json.dumps(data, ensure_ascii=False, allow_nan=False).encode(),
                        "application/json; charset=utf-8")

    def fail(self, code, message):
        self.respond(code, {"status": "error", "error": str(message)})

    def local_path(self):
        # Exact authority blocks DNS rebinding and ambiguous duplicate headers.
        authority = f"127.0.0.1:{self.server.server_port}"
        if self.headers.get_all("Host", []) != [authority]:
            raise ValueError("Host local não autorizado")
        origins = self.headers.get_all("Origin", [])
        if origins and origins != [f"http://{authority}"]:
            raise ValueError("Origem não autorizada")
        if not self.path.startswith("/") or self.path.startswith("//"):
            raise ValueError("Caminho local obrigatório")
        return urlsplit(self.path).path

    def json_body(self):
        content_types = self.headers.get_all("Content-Type", [])
        if (len(content_types) != 1
                or content_types[0].split(";", 1)[0].strip().lower() != "application/json"):
            raise ValueError("Content-Type application/json obrigatório")
        lengths = self.headers.get_all("Content-Length", [])
        if self.headers.get_all("Transfer-Encoding") or len(lengths) != 1:
            raise ValueError("Content-Length único obrigatório; Transfer-Encoding não permitido")
        if not lengths[0].isascii() or not lengths[0].isdigit():
            raise ValueError("Content-Length inválido")
        length = int(lengths[0])
        if not 0 < length <= 8192:
            raise ValueError("Corpo inválido ou muito grande")
        raw = self.rfile.read(length)
        if len(raw) != length:
            raise ValueError("Corpo incompleto")
        payload = json.loads(raw.decode("utf-8"), object_pairs_hook=_json_object,
                             parse_constant=_invalid_constant)
        if not isinstance(payload, dict):
            raise ValueError("Objeto JSON obrigatório")
        return payload

    def do_GET(self):
        try:
            path = self.local_path()
        except ValueError as exc:
            self.fail(400, exc)
            return
        try:
            if path == "/api/cosmology/health":
                self.respond(200, {"service": SERVICE_ID, "status": "RUNNING"})
            elif path == "/api/cosmology/status":
                result = cosmology_runtime.overview()
                self.respond(503 if result.get("status") == "error" else 200, result)
            elif path == "/api/lab/gpu":
                self.respond(200, gpu_status.status())
            elif path.startswith(EXPORTS_ROUTE + "/"):
                self.respond(200, cosmology_exports.get_export(path[len(EXPORTS_ROUTE) + 1:]))
            elif path == SCENARIOS_ROUTE:
                self.respond(200, {"scenarios": cosmology_scenarios.list_scenarios()})
            elif path.startswith(SCENARIOS_ROUTE + "/"):
                identifier = path[len(SCENARIOS_ROUTE) + 1:]
                record = cosmology_scenarios.get_scenario(identifier)
                self.respond(200, record)
            elif path in STATIC:
                name, mime = STATIC[path]
                self.send_bytes(200, (HERE / "static" / name).read_bytes(), mime + "; charset=utf-8")
            else:
                self.fail(404, "Rota ausente")
        except cosmology_scenarios.ScenarioNotFoundError:
            self.fail(404, "Cenário não encontrado")
        except cosmology_scenarios.ScenarioValidationError as exc:
            self.fail(400, exc)
        except cosmology_scenarios.ScenarioIntegrityError as exc:
            self.fail(503, exc)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            self.fail(503, exc)

    def do_POST(self):
        try:
            path = self.local_path()
            if path not in ("/api/cosmology/evaluate", SCENARIOS_ROUTE, EXPORTS_ROUTE):
                self.fail(404, "Rota ausente")
                return
            payload = self.json_body()
            if path == EXPORTS_ROUTE:
                if set(payload) == {"scenario_id"}:
                    cosmology_scenarios._identifier(payload["scenario_id"])
                elif set(payload) == {"reference_parameters", "current_parameters"}:
                    if not all(isinstance(value, dict) for value in payload.values()):
                        raise ValueError("Parâmetros da comparação devem ser objetos")
                else:
                    raise ValueError("Exportação aceita scenario_id ou os dois conjuntos de parâmetros")
                parameters = None
            elif path == SCENARIOS_ROUTE:
                if set(payload) != {"label", "parameters"}:
                    raise ValueError("Cenário aceita somente label e parameters")
                label = payload["label"]
                if (not isinstance(label, str) or not 1 <= len(label) <= 120
                        or not label.strip()
                        or any(unicodedata.category(c).startswith("C") for c in label)):
                    raise ValueError("label deve ter 1..120 caracteres, sem controles e não vazio")
                if not isinstance(payload["parameters"], dict):
                    raise ValueError("parameters deve ser um objeto JSON")
                parameters = payload["parameters"]
            else:
                parameters = payload
        except (ValueError, OSError, TypeError, OverflowError, RecursionError) as exc:
            self.fail(400, exc)
            return

        try:
            if path == EXPORTS_ROUTE:
                if "scenario_id" in payload:
                    exported = cosmology_exports.export_scenario(payload["scenario_id"])
                else:
                    exported = cosmology_exports.export_comparison(payload["reference_parameters"], payload["current_parameters"])
                self.respond(201, exported)
                return
            result = cosmology_runtime.evaluate(parameters)
            if not isinstance(result, dict):
                raise ValueError("Resposta inválida do executor")
            if result.get("status") == "error" or "error" in result:
                error = result.get("error")
                code = 400 if isinstance(error, dict) and error.get("code") == "INVALID_INPUT" else 503
                self.respond(code, {**result, "status": "error"})
                return
            if result.get("status") != "ok":
                raise ValueError("Executor não confirmou a avaliação")
            if path == SCENARIOS_ROUTE:
                # Only this fresh, trusted result reaches persistence. The client
                # cannot supply an evaluation, identifier, or database path.
                summary = cosmology_scenarios.save_scenario(label, result)
                self.respond(201, summary)
            else:
                self.respond(200, result)
        except cosmology_scenarios.ScenarioNotFoundError:
            self.fail(404, "Cenário não encontrado")
        except (OSError, ValueError, TypeError, KeyError, OverflowError) as exc:
            # User input has already been validated. This includes invalid
            # backend provenance and corrupt/unavailable scenario storage.
            self.fail(503, exc)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=18766)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), CosmologyHandler)
    print(f"TGL cosmology: http://127.0.0.1:{args.port}/cosmos", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
