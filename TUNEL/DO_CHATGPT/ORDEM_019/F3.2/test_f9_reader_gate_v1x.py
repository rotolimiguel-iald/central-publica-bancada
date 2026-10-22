"""Adversarial documentary tests for the non-frozen Fase 9 V1.x binding."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import f9_reader_gate_v1x as gate


HERE = Path(__file__).resolve().parent
BINDING = HERE / "VINCULO_DOCUMENTAL_V1X_R2_20261008.json"
SOURCE_ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
SPEC_SHA256 = "d29f2035f6bfa6bb339495c583df928853f4e4021748a121e20b913a501f8022"


class GateV1xTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.binding = json.loads(BINDING.read_bytes().decode("utf-8"))
        self.binding_path = self.work / "binding.json"
        self._save()

    def _save(self) -> None:
        raw = json.dumps(self.binding, ensure_ascii=False, sort_keys=True).encode("utf-8")
        self.binding_path.write_bytes(raw)
        self.pin = hashlib.sha256(raw).hexdigest()

    def _check(self) -> dict:
        return gate.verify_v1x_binding(
            self.binding_path,
            expected_binding_sha256=self.pin,
            allowed_source_root=SOURCE_ROOT,
            expected_spec_sha256=SPEC_SHA256,
        )

    def _record(self, reader_id: str) -> dict:
        return next(record for record in self.binding["readers"] if record["reader_id"] == reader_id)

    def test_valid_documentary_draft_preserves_status_and_snapshot(self) -> None:
        result = self._check()
        self.assertEqual(set(result["verified_readers"]), gate.EXPECTED_READER_IDS)
        for reader_id in gate.PRIMARY_READER_IDS:
            self.assertEqual(result["verified_readers"][reader_id]["status"], "REAL_DOCUMENTARY_HASH_ONLY")
        self.assertEqual(result["verified_readers"]["L4_masers_6"]["status"], "REAL_DOCUMENTARY_HASH_ONLY")
        for reader_id in gate.DECLARED_ONLY_IDS:
            self.assertEqual(result["verified_readers"][reader_id]["status"], "DECLARADO_UNVERIFIED")
        self.assertFalse(result["v2_frozen"])
        self.assertEqual(result["statistical_admission"], "OPEN")
        self.assertEqual(result["source_admission"], "OPEN")
        self.assertEqual(result["spec_sha256"], SPEC_SHA256)
        self.assertEqual(set(result["spec_snapshot"]["familias"]["P_primaria"]["ids"]), gate.PRIMARY_READER_IDS)

    def test_generic_anchor_refused(self) -> None:
        self._record("L4_masers_5")["numeric_windows"]["H0"] = {
            "literal": "arXiv", "numeric_literal": "73.6"
        }
        self._save()
        with self.assertRaises(gate.ReaderGateError):
            self._check()

    def test_table_row_missing_minus_side_refused(self) -> None:
        self._record("L4_masers_5")["numeric_windows"]["sigma_components"][1]["literal"] = "NGC 4258\n73.6+3.1"
        self._save()
        with self.assertRaisesRegex(gate.ReaderGateError, "sigma row missing"):
            self._check()

    def test_asymmetric_sides_reversed_refused(self) -> None:
        self._record("L4_masers_5")["asymmetric_sigma"] = {"plus": 3.0, "minus": 3.1}
        self._save()
        with self.assertRaisesRegex(gate.ReaderGateError, "asymmetric sigma sides changed"):
            self._check()

    def test_source_pdf_pin_change_refused(self) -> None:
        self._record("L4_masers_5")["source"]["sha256"] = "0" * 64
        self._save()
        with self.assertRaises(gate.ReaderGateError):
            self._check()

    def test_missing_reader_key_is_typed_refusal(self) -> None:
        del self._record("L2_cchp")["sigma_published_components"]
        self._save()
        with self.assertRaises(gate.ReaderGateError):
            self._check()

    def test_missing_binding_key_is_typed_refusal(self) -> None:
        del self.binding["readers"]
        self._save()
        with self.assertRaises(gate.ReaderGateError):
            self._check()

    def test_historical_v1_pin_refused(self) -> None:
        self.binding["draft_v2"]["sha256"] = gate.HISTORICAL_V1_SHA256
        self._save()
        with self.assertRaisesRegex(gate.ReaderGateError, "historical V1"):
            self._check()

    def test_admission_claim_refused(self) -> None:
        self.binding["source_admission_decided"] = True
        self._save()
        with self.assertRaisesRegex(gate.ReaderGateError, "claims admission"):
            self._check()

    def test_unverified_replica_cannot_claim_source(self) -> None:
        self._record("L1b_sh0es_r25")["source"] = copy.deepcopy(self._record("L1_sh0es_r22")["source"])
        self._save()
        with self.assertRaisesRegex(gate.ReaderGateError, "unverified reader claims"):
            self._check()

    def test_draft_read_once(self) -> None:
        draft = Path(self.binding["draft_v2"]["path"]).resolve()
        original = gate.base._read_json
        paths = []

        def counted(path):
            paths.append(Path(path).resolve())
            return original(path)

        with mock.patch.object(gate.base, "_read_json", side_effect=counted):
            self._check()
        self.assertEqual(paths.count(draft), 1)

    def test_duplicate_json_key_refused(self) -> None:
        raw = self.binding_path.read_bytes().replace(b'"schema":', b'"schema":"duplicate","schema":', 1)
        self.binding_path.write_bytes(raw)
        self.pin = hashlib.sha256(raw).hexdigest()
        with self.assertRaisesRegex(gate.ReaderGateError, "duplicate JSON key"):
            self._check()


if __name__ == "__main__":
    unittest.main()
