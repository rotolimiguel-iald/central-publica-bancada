"""Small fail-closed checks for the F5.2 staging candidate; no Bancada import."""
import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import neff_canal as channel


FROZEN_TEXT = '''NEFF_SM = 3.044
MEDIDAS = [
    (2.92, 0.19, "Planck 2018", "arXiv:1807.06209", True),
    (2.97, 0.12, "SPT-3G D1 + Planck + ACT (CMB-SPA)", "arXiv:2506.20707", True),
]
PROJECOES = [(0.045, "SO-ASO", "arXiv:2503.00636", "~2030")]
'''
UM_TEXT = 'ALPHA_FINE_CODATA_2018 = 0.0072973525693\n'


class CandidateTest(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.frozen = root / "frozen.py"
        self.um = root / "um.py"
        self.source = root / "2506.20707v2.html"
        self.frozen.write_text(FROZEN_TEXT, encoding="utf-8")
        self.um.write_text(UM_TEXT, encoding="utf-8")
        self.source.write_bytes(b"custodied-html-test-fixture")
        self.patch_frozen = patch.object(channel, "FROZEN_SHA256", channel._sha(self.frozen))
        self.patch_source = patch.object(channel, "SPT_V2_SHA256", channel._sha(self.source))
        self.patch_frozen.start()
        self.patch_source.start()
        self.addCleanup(self.patch_frozen.stop)
        self.addCleanup(self.patch_source.stop)

    def call(self):
        return channel.canal(frozen=str(self.frozen), um=str(self.um), source=str(self.source))

    def test_two_distinct_yp_lines_without_decisory_center(self):
        result = self.call()
        lines = result["opcoes_CMB_SPA_Yp"]
        self.assertEqual([(x["yp"], x["N_eff_obs"]) for x in lines],
                         [("BBN_CONSISTENCY", 2.82), ("FREE", 2.96)])
        self.assertEqual((lines[1]["sigma_plus"], lines[1]["sigma_minus"]), (0.21, 0.24))
        self.assertIsNone(lines[1]["sigma"])
        self.assertTrue(all(x["source_sha256"] == channel._sha(self.source) for x in lines))
        self.assertIn("[OPEN", result["escolha_Yp"])
        self.assertFalse(any("CMB-SPA" in x["rotulo"] for x in result["medidas"]))
        self.assertNotIn("tens_now", result)
        self.assertFalse(any("quando_declarado" in x for x in result["projecoes"]))

    def test_source_pin_mismatch_fails(self):
        self.source.write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "SHA-256 divergente"):
            self.call()

    def test_frozen_pin_mismatch_fails(self):
        self.frozen.write_text(FROZEN_TEXT + "# changed\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "SHA-256 divergente"):
            self.call()

    def test_changed_frozen_label_fails_after_new_pin(self):
        self.frozen.write_text(FROZEN_TEXT.replace("2.97, 0.12", "2.91, 0.12"), encoding="utf-8")
        with patch.object(channel, "FROZEN_SHA256", channel._sha(self.frozen)):
            with self.assertRaisesRegex(ValueError, "linha CMB-SPA congelada mudou"):
                self.call()

    def test_missing_frozen_row_fails_after_new_pin(self):
        self.frozen.write_text(FROZEN_TEXT.replace("CMB-SPA", "not the expected label"), encoding="utf-8")
        with patch.object(channel, "FROZEN_SHA256", channel._sha(self.frozen)):
            with self.assertRaisesRegex(ValueError, "CMB-SPA deve aparecer uma vez"):
                self.call()


if __name__ == "__main__":
    unittest.main()
