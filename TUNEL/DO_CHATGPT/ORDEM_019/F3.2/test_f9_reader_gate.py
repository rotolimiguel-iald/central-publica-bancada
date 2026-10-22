"""Adversarial checks for the R1 source gate; no composite is executed."""

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from f9_reader_gate import (
    EXPECTED_BINDING_SHA256,
    ReaderGateError,
    verify_readers,
)


ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
BINDING = ROOT / "f9_scalar_reader_sources" / "VINCULO_DOCUMENTAL_CINCO_LEITORES.json"


class ReaderGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.binding = json.loads(BINDING.read_bytes())
        cls.first_source = Path(cls.binding["readers"][0]["source"]["path"]).resolve()

    def _check(self, binding=BINDING, pin=EXPECTED_BINDING_SHA256):
        return verify_readers(
            binding,
            expected_binding_sha256=pin,
            allowed_source_root=ROOT,
        )

    def _modified_binding(self, change):
        modified = copy.deepcopy(self.binding)
        change(modified)
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "binding.json"
        data = json.dumps(modified, ensure_ascii=False).encode("utf-8")
        path.write_bytes(data)
        return path, hashlib.sha256(data).hexdigest()

    def test_valid_archive_verifies_five_without_statistical_admission(self):
        result = self._check()
        self.assertEqual(len(result["verified_readers"]), 5)
        self.assertEqual(result["statistical_admission"], "OPEN")

    def test_changed_source_bytes_are_rejected(self):
        original_read = Path.read_bytes
        target = self.first_source

        def altered(path):
            data = original_read(path)
            return data + b"tampered" if Path(path).resolve() == target else data

        with mock.patch.object(Path, "read_bytes", altered):
            with self.assertRaisesRegex(ReaderGateError, "bytes/hash mismatch"):
                self._check()

    def test_missing_source_is_rejected(self):
        original_read = Path.read_bytes
        target = self.first_source

        def missing(path):
            if Path(path).resolve() == target:
                raise FileNotFoundError("simulated missing source")
            return original_read(path)

        with mock.patch.object(Path, "read_bytes", missing):
            with self.assertRaisesRegex(ReaderGateError, "source unreadable"):
                self._check()

    def test_membership_with_wrong_anchor_is_rejected(self):
        def change(data):
            data["readers"][0]["short_literal_anchor"] = "value not in archived bytes"

        path, pin = self._modified_binding(change)
        with self.assertRaisesRegex(ReaderGateError, "literal anchor absent"):
            self._check(path, pin)

    def test_numeric_spoof_is_rejected(self):
        def change(data):
            data["readers"][0]["H0_published"] += 1

        path, pin = self._modified_binding(change)
        with self.assertRaisesRegex(ReaderGateError, "H0 transcription mismatch"):
            self._check(path, pin)

    def test_unpinned_binding_is_rejected(self):
        with self.assertRaisesRegex(ReaderGateError, "binding hash mismatch"):
            self._check(pin="0" * 64)


if __name__ == "__main__":
    unittest.main()
