"""HTTP checks: ephemeral server, real temporary SQLite, synthetic science only."""
from __future__ import annotations

import copy
import hashlib
import http.client
import importlib.util
import json
from pathlib import Path
import sys
import sqlite3
import tempfile
import threading
import types
import unittest
import uuid
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


class CosmologyHttpTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.temp = Path(temporary.name)
        self.db = self.temp / "scenarios.sqlite3"
        store_spec = importlib.util.spec_from_file_location(
            "_cosmology_http_store", ROOT / "cosmology_scenarios.py")
        self.store = importlib.util.module_from_spec(store_spec)
        store_spec.loader.exec_module(self.store)
        self.store.DB_PATH = self.db
        self.runtime = types.ModuleType("cosmology_runtime")
        engine = self.temp / "fixture_runtime.py"
        engine.write_bytes(b"# HTTP fixture only; never executed.\n")
        self.runtime.__file__ = str(engine)
        self.runtime.ENGINE_SHA256 = hashlib.sha256(engine.read_bytes()).hexdigest()
        self.runtime.MEAN_FILE, self.runtime.COV_FILE = "mean.txt", "cov.txt"
        self.runtime.EXPECTED_SHA256 = {}
        for name, content in (("mean.txt", b"HTTP synthetic mean"),
                              ("cov.txt", b"HTTP synthetic covariance")):
            fixture = self.temp / name
            fixture.write_bytes(content)
            self.runtime.EXPECTED_SHA256[name] = hashlib.sha256(fixture.read_bytes()).hexdigest()
        model = {"id": "HTTP_TEST_BACKGROUND", "status": "TEST_ONLY_NOT_SCIENCE"}
        points = [{"z": z, "type": "DM_over_rd", "observed": 10.0, "sigma": 1.0}
                  for z in (0.5, 1.0)]
        self.overview = {
            "schema_version": "cosmology_background_v1", "status": "ok", "model": model,
            "engine_sha256": self.runtime.ENGINE_SHA256,
            "parameters": {
                "H0": {"min": 40, "max": 100, "default": 67.4, "unit": "km/s/Mpc"},
                "omega_m": {"min": 0.1, "max": 0.5, "default": 0.315, "unit": "dimensionless"},
                "rd_mpc": {"min": 120, "max": 170, "default": 147.09, "unit": "Mpc"},
                "w0": {"min": -1.5, "max": -0.5, "default": -1, "unit": "dimensionless"},
                "wa": {"min": -1, "max": 1, "default": 0, "unit": "dimensionless"},
                "redshift": {"min": 0.001, "max": 3, "default": 0.5, "unit": "dimensionless"}},
            "memory": {"load_id": "http-fixture", "source_reads_since_load": 0},
            "dataset": {"id": "HTTP_SYNTHETIC", "n_points": len(points), "points": points,
                        "covariance": [[1, 0], [0, 1]], "release_commit_verified": False,
                        "mean_sha256": self.runtime.EXPECTED_SHA256["mean.txt"],
                        "covariance_sha256": self.runtime.EXPECTED_SHA256["cov.txt"]},
            "evaluation_status": "VISUAL_DIAGNOSTIC_NOT_FIT_OR_SIGMA",
        }
        self.evaluation = {
            "schema_version": "cosmology_background_v1", "status": "ok", "model": model,
            "engine_sha256": self.runtime.ENGINE_SHA256,
            "data_hashes": {key: self.overview["dataset"][key]
                            for key in ("mean_sha256", "covariance_sha256")},
            "parameters": {key: rule["default"] for key, rule in self.overview["parameters"].items()},
            "memory": self.overview["memory"],
            "dataset_id": "HTTP_SYNTHETIC", "cursor": {"z": 0.5, "dm_over_rd": 11.0},
            "series": [{"z": 0, "dm_over_rd": 0}, {"z": 0.5, "dm_over_rd": 11.0}],
            "observations": [{**point, "predicted": 11.0, "residual": 1.0} for point in points],
            "residual_definition": "predicted_minus_observed", "quadrature": {"method": "SYNTHETIC"},
            "chi2": {"value": 2.0, "n_points": len(points), "method": "SYNTHETIC",
                     "status": "VISUAL_DIAGNOSTIC_NOT_FIT_OR_SIGMA"}, "elapsed_ms": 0.1,
        }
        self.runtime.overview = mock.Mock(return_value=copy.deepcopy(self.overview))
        self.runtime.evaluate = mock.Mock(return_value=copy.deepcopy(self.evaluation))
        gpu = types.ModuleType("gpu_status")
        gpu.status = mock.Mock(return_value={"available": False})
        modules = mock.patch.dict(sys.modules, {
            "cosmology_runtime": self.runtime, "cosmology_scenarios": self.store, "gpu_status": gpu,
            "resident_bridge": None,
        })
        modules.start()
        self.addCleanup(modules.stop)
        spec = importlib.util.spec_from_file_location(
            "_cosmology_http_audit", ROOT / "cosmology_server.py")
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        logging = mock.patch.object(self.module.CosmologyHandler, "log_message")
        logging.start()
        self.addCleanup(logging.stop)
        self.server = self.module.ThreadingHTTPServer(
            ("127.0.0.1", 0), self.module.CosmologyHandler)
        self.thread = threading.Thread(
            target=self.server.serve_forever,
            kwargs={"poll_interval": 0.01}, daemon=True)
        self.thread.start()
        self.addCleanup(self.close_server)
        self.origin = f"http://127.0.0.1:{self.server.server_port}"
        self.headers = {"Origin": self.origin, "Content-Type": "application/json"}

    def close_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def request(self, method, path, body=None, headers=None, *, decode_json=True):
        connection = http.client.HTTPConnection(
            "127.0.0.1", self.server.server_port, timeout=2)
        try:
            connection.request(method, path, body=body, headers=headers or {})
            response = connection.getresponse()
            raw = response.read()
            return response.status, dict(response.getheaders()), json.loads(raw) if decode_json else raw
        finally:
            connection.close()

    def raw_request(self, method, path, headers, body=b""):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=2)
        try:
            connection.putrequest(method, path, skip_host=True, skip_accept_encoding=True)
            for name, value in headers:
                connection.putheader(name, value)
            connection.endheaders(body)
            response = connection.getresponse()
            return response.status, json.loads(response.read())
        finally:
            connection.close()

    def save(self, payload=None):
        if payload is None:
            payload = {"label": "Referência A", "parameters": self.evaluation["parameters"]}
        return self.request("POST", "/api/cosmology/scenarios", json.dumps(payload), self.headers)

    def test_health_has_separate_identity_without_evaluation(self):
        status, headers, body = self.request("GET", "/api/cosmology/health")
        self.assertEqual(status, 200)
        self.assertEqual(body, {"service": "tgl-cosmology-resident-v1", "status": "RUNNING"})
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.runtime.overview.assert_not_called()
        self.runtime.evaluate.assert_not_called()

    def test_explore_and_teaching_assets_have_correct_routing_and_mime(self):
        # UI is owned by other contributors. Serve distinct temporary fixtures
        # so routing tests do not depend on those files having arrived yet.
        static = self.temp / "static"
        static.mkdir()
        routes = {
            "/": ("universe-map.html", "text/html"),
            "/explore": ("universe-map.html", "text/html"),
            "/explore?lesson=expansion": ("universe-map.html", "text/html"),
            "/universe-map.css": ("universe-map.css", "text/css"),
            "/universe-map.js": ("universe-map.js", "text/javascript"),
            "/cosmos-lessons.js": ("cosmos-lessons.js", "text/javascript"),
            "/cosmos-teaching-model.js": ("cosmos-teaching-model.js", "text/javascript"),
            "/cosmos": ("cosmos.html", "text/html"),
            "/cosmos.js": ("cosmos.js", "text/javascript"),
            "/cosmos.css": ("cosmos.css", "text/css"),
        }
        fixtures = {name: ("HTTP fixture · " + name).encode("utf-8") for name, _ in routes.values()}
        for name, body in fixtures.items():
            (static / name).write_bytes(body)
        with mock.patch.object(self.module, "HERE", self.temp):
            for route, (name, mime) in routes.items():
                with self.subTest(route=route):
                    status, headers, body = self.request("GET", route, headers={"Origin": self.origin},
                                                         decode_json=False)
                    self.assertEqual(status, 200)
                    self.assertEqual(body, fixtures[name])
                    self.assertEqual(headers["Content-Type"], mime + "; charset=utf-8")
                    self.assertEqual(int(headers["Content-Length"]), len(body))
                    self.assertEqual(headers["Cache-Control"], "no-store")
                    self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.runtime.overview.assert_not_called()
        self.runtime.evaluate.assert_not_called()

    def test_missing_explore_asset_and_unlisted_paths_fail_visibly(self):
        with mock.patch.object(self.module, "HERE", self.temp):
            for route in ("/explore", "/cosmos-lessons.js", "/cosmos-teaching-model.js"):
                with self.subTest(route=route):
                    status, _, body = self.request("GET", route)
                    self.assertEqual(status, 503)
                    self.assertEqual(body["status"], "error")
            for route in ("/missing.js", "/../launch.py", "/%2e%2e/launch.py"):
                with self.subTest(route=route):
                    status, _, body = self.request("GET", route)
                    self.assertEqual(status, 404)
                    self.assertEqual(body["status"], "error")
        self.runtime.evaluate.assert_not_called()

    def test_evaluate_guards_and_integrity_failure(self):
        headers = {"Origin": self.origin, "Content-Type": "application/json"}
        cases = [
            (b"{}", {**headers, "Origin": "http://localhost:18766"}),
            (b"{}", {**headers, "Origin": "null"}),
            (b"{}", {**headers, "Origin": "https://example.invalid"}),
            (b"{}", {**headers, "Content-Type": "text/plain"}),
            (b"{}", {**headers, "Content-Length": "invalid"}),
            (b"{}" + b" " * 8191, headers),
            (b"", headers), (b"[]", headers), (b"{", headers),
        ]
        for body, request_headers in cases:
            with self.subTest(headers=request_headers, size=len(body)):
                status, _, result = self.request(
                    "POST", "/api/cosmology/evaluate", body, request_headers)
                self.assertEqual(status, 400)
                self.assertIn("error", result)
                self.runtime.evaluate.assert_not_called()
        status, _, _ = self.request(
            "POST", "/api/cosmology/evaluate", b"{}", headers)
        self.assertEqual(status, 200)
        self.runtime.evaluate.assert_called_once_with({})
        self.runtime.evaluate.return_value = {
            "status": "error", "error": {"code": "DATA_INTEGRITY"}}
        status, _, result = self.request(
            "POST", "/api/cosmology/evaluate", b"{}", headers)
        self.assertEqual(status, 503)
        self.assertEqual(result["error"]["code"], "DATA_INTEGRITY")

    def test_scenario_roundtrip_recomputes_and_preserves_receipt(self):
        status, _, empty = self.request("GET", "/api/cosmology/scenarios")
        self.assertEqual((status, empty), (200, {"scenarios": []}))
        self.assertFalse(self.db.exists())
        self.runtime.evaluate.assert_not_called()
        status, headers, body = self.save()
        self.assertEqual(status, 201)
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.runtime.evaluate.assert_called_once_with(self.evaluation["parameters"])
        summary = body
        self.assertNotIn("scenario", summary)
        self.assertNotIn("summary", summary)
        identifier = summary["id"]
        self.assertEqual(str(uuid.UUID(identifier)), identifier)
        self.assertEqual(summary["parameters"], self.evaluation["parameters"])
        self.assertNotIn("evaluation", summary)
        self.runtime.evaluate.reset_mock()
        self.runtime.overview.reset_mock()
        status, _, listing = self.request("GET", "/api/cosmology/scenarios")
        self.assertEqual((status, listing), (200, {"scenarios": [summary]}))
        status, _, full = self.request("GET", "/api/cosmology/scenarios/" + identifier)
        self.assertEqual(status, 200)
        record = full
        self.assertNotIn("scenario", record)
        self.assertNotIn("record", record)
        self.assertEqual(record["evaluation"], self.evaluation)
        self.assertEqual(record["overview"], self.overview)
        self.assertEqual(record["inputs"], self.evaluation["parameters"])
        self.assertEqual(record["sha256"], summary["sha256"])
        self.runtime.evaluate.assert_not_called()
        self.runtime.overview.assert_not_called()
        changed = copy.deepcopy(self.evaluation)
        changed["parameters"]["H0"] = 72.0
        self.runtime.evaluate.return_value = changed
        status, _, second = self.save({"label": "Referência A", "parameters": changed["parameters"]})
        self.assertEqual(status, 201)
        self.runtime.evaluate.assert_called_once_with(changed["parameters"])
        self.assertNotEqual(second["id"], identifier)
        _, _, full = self.request("GET", "/api/cosmology/scenarios/" + identifier)
        self.assertEqual(full["evaluation"], self.evaluation)

    def test_optional_model_id_is_passed_to_runtime_inside_parameters(self):
        parameters = {**self.evaluation["parameters"], "model_id": "HTTP_V3_FIXTURE"}
        evaluated = copy.deepcopy(self.evaluation)
        evaluated["model"]["id"] = parameters["model_id"]
        self.runtime.evaluate.return_value = evaluated
        status, _, summary = self.save({"label": "Modelo B", "parameters": parameters})
        self.assertEqual(status, 201)
        self.runtime.evaluate.assert_called_once_with(parameters)
        self.assertEqual(summary["model_id"], parameters["model_id"])
        self.assertEqual(summary["parameters"], self.evaluation["parameters"])
        status, _, full = self.request("GET", "/api/cosmology/scenarios/" + summary["id"])
        self.assertEqual(status, 200)
        self.assertEqual(full["evaluation"], evaluated)
        self.assertEqual(full["inputs"], self.evaluation["parameters"])
        self.assertNotIn("model_id", full["inputs"])

    def test_scenario_rejects_forged_result_path_and_invalid_envelope(self):
        valid = {"label": "B", "parameters": {}}
        invalid = [{}, {"label": "B"}, {"parameters": {}},
                   {**valid, "parameters": []}, {**valid, "parameters": None}]
        for key in ("result", "evaluation", "path", "db_path", "id", "chi2", "model_id", "model"):
            invalid.append({**valid, key: self.evaluation if key in ("result", "evaluation") else "forged"})
        for label in (None, "", " ", "x" * 121, "a\nb", "a\x00b", "a\u202eb"):
            invalid.append({**valid, "label": label})
        with mock.patch.object(self.store, "save_scenario", wraps=self.store.save_scenario) as persist:
            for payload in invalid:
                with self.subTest(payload=payload):
                    status, _, body = self.save(payload)
                    self.assertEqual(status, 400)
                    self.assertEqual(body["status"], "error")
            persist.assert_not_called()
        self.runtime.evaluate.assert_not_called()
        self.assertFalse(self.db.exists())

    def test_scenario_json_and_framing_guards(self):
        valid = b'{"label":"A","parameters":{}}'
        cases = [
            (valid, {**self.headers, "Content-Type": "text/plain"}),
            (valid, {**self.headers, "Content-Length": "-1"}),
            (valid, {**self.headers, "Transfer-Encoding": "chunked"}),
            (b" " * 8193, self.headers), (b"", self.headers), (b"[]", self.headers),
            (b"{", self.headers), (b"\xff", self.headers),
            (b'{"label":"A","label":"B","parameters":{}}', self.headers),
            (b'{"label":"A","parameters":{"H0":67,"H0":72}}', self.headers),
            (b'{"label":"A","parameters":{"H0":NaN}}', self.headers),
        ]
        for body, headers in cases:
            with self.subTest(body=body[:100], headers=headers):
                status, _, response = self.request("POST", "/api/cosmology/scenarios", body, headers)
                self.assertEqual(status, 400)
                self.assertEqual(response["status"], "error")
        self.runtime.evaluate.assert_not_called()
        self.assertFalse(self.db.exists())

    def test_source_or_model_error_never_saves(self):
        failures = [
            ({"status": "error", "error": {"code": "INVALID_INPUT", "message": "bad H0"}}, 400),
            ({"status": "error", "error": {"code": "DATA_INTEGRITY", "message": "bad source"}}, 503),
            ({"error": "source unreadable"}, 503),
            ({"status": "ok", "error": "source unreadable"}, 503),
            ({"status": "ok", "error": None}, 503),
            ({"status": "error"}, 503), ({"status": "unknown"}, 503), (None, 503),
        ]
        with mock.patch.object(self.store, "save_scenario", wraps=self.store.save_scenario) as persist:
            for result, expected in failures:
                with self.subTest(result=result):
                    self.runtime.evaluate.return_value = result
                    status, _, body = self.save()
                    self.assertEqual(status, expected)
                    self.assertEqual(body["status"], "error")
            self.runtime.evaluate.side_effect = OSError("source unavailable")
            status, _, body = self.save()
            self.assertEqual(status, 503)
            self.assertEqual(body["status"], "error")
            persist.assert_not_called()
        self.assertFalse(self.db.exists())

    def test_source_failure_during_snapshot_does_not_create_database(self):
        self.runtime.overview.return_value = {"status": "error", "error": "source changed"}
        status, _, body = self.save()
        self.assertEqual(status, 503)
        self.assertEqual(body["status"], "error")
        self.assertFalse(self.db.exists())

    def test_v3_unavailable_returns_503_without_fallback_or_save(self):
        parameters = {**self.evaluation["parameters"], "model_id": "HTTP_V3_FIXTURE"}
        failure = {"status": "error", "error": {"code": "V3_UNAVAILABLE",
                                                  "message": "Synthetic worker unavailable"}}
        routes = (("/api/cosmology/evaluate", parameters),
                  ("/api/cosmology/scenarios", {"label": "V3", "parameters": parameters}))
        with mock.patch.object(self.store, "save_scenario", wraps=self.store.save_scenario) as persist:
            for path, payload in routes:
                with self.subTest(path=path):
                    self.runtime.evaluate.reset_mock()
                    # A retry/fallback could return success: assert it is never attempted.
                    self.runtime.evaluate.side_effect = [copy.deepcopy(failure), self.evaluation]
                    status, _, body = self.request("POST", path, json.dumps(payload), self.headers)
                    self.assertEqual(status, 503)
                    self.assertEqual(body, failure)
                    self.runtime.evaluate.assert_called_once_with(parameters)
            persist.assert_not_called()
        self.runtime.overview.assert_not_called()
        self.assertFalse(self.db.exists())

    def test_scenario_missing_and_invalid_uuid(self):
        status, _, body = self.request("GET", "/api/cosmology/scenarios/" + str(uuid.uuid4()))
        self.assertEqual(status, 404)
        self.assertEqual(body["status"], "error")
        for identifier in ("not-a-uuid", "../cosmology_runtime.py", "", str(uuid.uuid4()).upper()):
            with self.subTest(identifier=identifier):
                status, _, body = self.request("GET", "/api/cosmology/scenarios/" + identifier)
                self.assertEqual(status, 400)
                self.assertEqual(body["status"], "error")
        self.runtime.evaluate.assert_not_called()
        self.assertFalse(self.db.exists())

    def test_corrupt_record_fails_get_and_list(self):
        status, _, saved = self.save()
        self.assertEqual(status, 201)
        connection = sqlite3.connect(self.db)
        try:
            connection.execute("DROP TRIGGER scenarios_no_update")
            connection.execute("UPDATE scenarios SET record_json='{}'")
            connection.commit()
        finally:
            connection.close()
        for path in ("/api/cosmology/scenarios", "/api/cosmology/scenarios/" + saved["id"]):
            with self.subTest(path=path):
                status, _, body = self.request("GET", path)
                self.assertEqual(status, 503)
                self.assertEqual(body["status"], "error")
                self.assertNotIn("scenario", body)
                self.assertNotIn("scenarios", body)

    def test_corrupt_database_fails_list_get_and_save(self):
        self.db.write_bytes(b"corrupt SQLite fixture")
        for path in ("/api/cosmology/scenarios", "/api/cosmology/scenarios/" + str(uuid.uuid4())):
            with self.subTest(path=path):
                status, _, body = self.request("GET", path)
                self.assertEqual(status, 503)
                self.assertEqual(body["status"], "error")
        status, _, body = self.save()
        self.assertEqual(status, 503)
        self.assertEqual(body["status"], "error")
        self.assertEqual(self.db.read_bytes(), b"corrupt SQLite fixture")

    def test_host_and_origin_guards_apply_to_all_routes(self):
        cases = [
            {"Host": "foreign.invalid"}, {"Host": "127.0.0.1:1"},
            {"Host": f"localhost:{self.server.server_port}"}, {"Host": ""},
            {"Origin": "https://foreign.invalid"}, {"Origin": "null"},
            {"Origin": self.origin + "/"}, {"Origin": self.origin + ".foreign.invalid"},
        ]
        for method, path in (("GET", "/api/cosmology/health"),
                             ("GET", "/api/cosmology/status"),
                             ("GET", "/api/cosmology/scenarios"),
                             ("GET", "/cosmos"),
                             ("GET", "/explore"),
                             ("GET", "/universe-map.css"),
                             ("GET", "/universe-map.js"),
                             ("GET", "/cosmos-lessons.js"),
                             ("GET", "/cosmos-teaching-model.js"),
                             ("POST", "/api/cosmology/scenarios"),
                             ("POST", "/api/cosmology/evaluate")):
            for bad_headers in cases:
                with self.subTest(method=method, path=path, headers=bad_headers):
                    # No body is needed to test rejection at the header boundary.
                    # Avoid racing a second client send with the server's early close.
                    status, _, body = self.request(method, path, headers={**self.headers, **bad_headers})
                    self.assertEqual(status, 400)
                    self.assertEqual(body["status"], "error")
                    self.assertIn("Host" if "Host" in bad_headers else "Origem", body["error"])
        self.runtime.evaluate.assert_not_called()
        self.runtime.overview.assert_not_called()
        self.assertFalse(self.db.exists())

    def test_missing_duplicate_headers_and_absolute_targets_rejected(self):
        authority = f"127.0.0.1:{self.server.server_port}"
        for headers in ([], [("Host", authority), ("Host", authority)],
                        [("Host", authority), ("Origin", self.origin), ("Origin", self.origin)]):
            with self.subTest(headers=headers):
                status, body = self.raw_request("GET", "/api/cosmology/scenarios", headers)
                self.assertEqual(status, 400)
                self.assertEqual(body["status"], "error")
        for key in ("Content-Length", "Content-Type"):
            headers = [("Host", authority), ("Content-Type", "application/json"), ("Content-Length", "2")]
            headers.append((key, "2" if key == "Content-Length" else "application/json"))
            status, _ = self.raw_request("POST", "/api/cosmology/scenarios", headers, b"{}")
            self.assertEqual(status, 400)
        status, _ = self.raw_request("GET", "http://foreign.invalid/api/cosmology/scenarios",
                                     [("Host", authority)])
        self.assertEqual(status, 400)
        self.runtime.evaluate.assert_not_called()

    def test_local_origin_and_headerless_cli_remain_supported(self):
        for headers in ({}, {"Origin": self.origin}):
            status, _, body = self.request("GET", "/api/cosmology/scenarios", headers=headers)
            self.assertEqual((status, body), (200, {"scenarios": []}))
        status, _, body = self.request("POST", "/api/cosmology/evaluate", b"{}",
                                      {"Content-Type": "application/json; charset=utf-8"})
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "ok")


if __name__ == "__main__":
    unittest.main()
