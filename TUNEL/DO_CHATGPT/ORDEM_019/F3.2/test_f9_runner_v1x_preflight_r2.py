"""Integration checks for the documentary V1.x preflight; no data opening."""

from __future__ import annotations

from pathlib import Path
import unittest

from f9_runner_v1x_preflight import ReaderGateError, prepare_v1x


ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.2")
BINDING = ROOT / "VINCULO_DOCUMENTAL_V1X_R2_20261008.json"
SOURCE_ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
BINDING_SHA256 = "885efb944728efb41b62b47fa653c6d3a3956bd1cb086cb8595b958b6a410c52"
SPEC_SHA256 = "d29f2035f6bfa6bb339495c583df928853f4e4021748a121e20b913a501f8022"


class PreflightTests(unittest.TestCase):
    def run_preflight(self, *, binding_sha256: str = BINDING_SHA256,
                      spec_sha256: str = SPEC_SHA256) -> dict:
        return prepare_v1x(
            BINDING,
            expected_binding_sha256=binding_sha256,
            allowed_source_root=SOURCE_ROOT,
            expected_spec_sha256=spec_sha256,
        )

    def test_documentary_preflight_keeps_data_closed(self) -> None:
        result = self.run_preflight()
        self.assertEqual(result["stage"], "V1X_DOCUMENTARY_PREFLIGHT_ONLY")
        self.assertFalse(result["data_opened"])
        self.assertFalse(result["v2_frozen"])
        self.assertIsNone(result["verdict"])
        self.assertEqual(result["source_admission"], "OPEN")
        self.assertEqual(result["n_alvos_declarados"], 2)
        self.assertEqual(result["declared_unverified_reader_ids"], ["L1b_sh0es_r25", "L6_sirenes"])
        self.assertEqual(len(result["verified_reader_ids"]), 6)
        self.assertIn("L4_masers_5", result["primary_reader_ids"])
        self.assertNotIn("L4_masers_6", result["primary_reader_ids"])

    def test_wrong_binding_pin_refused(self) -> None:
        with self.assertRaises(ReaderGateError):
            self.run_preflight(binding_sha256="0" * 64)

    def test_wrong_spec_pin_refused(self) -> None:
        with self.assertRaises(ReaderGateError):
            self.run_preflight(spec_sha256="0" * 64)


if __name__ == "__main__":
    unittest.main()
