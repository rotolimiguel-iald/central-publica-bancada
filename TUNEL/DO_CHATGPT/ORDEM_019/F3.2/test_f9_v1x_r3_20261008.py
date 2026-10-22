"""R3 adversarial and synthetic-only checks; no observational data opening."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import tempfile
import unittest

import f9_reader_gate_v1x_r3 as gate
import f9_runner_v1x_preflight_r3 as pre
import f9_runner_v1x_staged_r3 as run


HERE = Path(__file__).resolve().parent
BINDING = HERE / "VINCULO_DOCUMENTAL_V1X_R3_20261008.json"
FIXTURE = HERE / "FIXTURE_SINTETICO_V1X_R3_20261008.json"
SOURCE_ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
SPEC_SHA = "21a624f5c6e716b3b9a1b9301747b94ae74b82bed2502654885a0709ec9d0dcb"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(binding: Path = BINDING, spec_sha: str | None = SPEC_SHA) -> dict:
    return gate.verify_v1x_binding(
        binding, expected_binding_sha256=sha(binding),
        allowed_source_root=SOURCE_ROOT, expected_spec_sha256=spec_sha,
    )


class F9R3Tests(unittest.TestCase):
    def test_valid_gate_has_six_documentary_and_two_declared(self) -> None:
        verified = check()["verified_readers"]
        self.assertEqual(sum(v["status"] == "REAL_DOCUMENTARY_HASH_ONLY"
                             for v in verified.values()), 6)
        self.assertEqual(pre.declared_inventory_ids(verified), [
            "L1b_sh0es_r25", "L6_sirenes"
        ])

    def _coherent_swap(self, reader_id: str) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            binding = json.loads(BINDING.read_bytes())
            draft = json.loads(Path(binding["draft_v2"]["path"]).read_bytes())
            metadata = draft["spec"]["leitores"][reader_id]
            metadata["sigma_plus"], metadata["sigma_minus"] = (
                metadata["sigma_minus"], metadata["sigma_plus"]
            )
            spec_raw = json.dumps(draft["spec"], sort_keys=True,
                                  ensure_ascii=False, separators=(",", ":")).encode()
            draft["spec_sha256"] = hashlib.sha256(spec_raw).hexdigest()
            draft_path = base / "tampered_draft.json"
            draft_raw = json.dumps(draft, ensure_ascii=False).encode()
            draft_path.write_bytes(draft_raw)
            binding["draft_v2"] = {
                "path": str(draft_path), "bytes": len(draft_raw),
                "sha256": hashlib.sha256(draft_raw).hexdigest(),
            }
            binding["spec_sha256"] = draft["spec_sha256"]
            record = next(r for r in binding["readers"]
                          if r["reader_id"] == reader_id)
            record["draft_metadata"] = metadata
            record["sigma_published_components"].reverse()
            record["asymmetric_sigma"]["plus"], record["asymmetric_sigma"]["minus"] = (
                record["asymmetric_sigma"]["minus"],
                record["asymmetric_sigma"]["plus"],
            )
            record["numeric_windows"]["sigma_components"].reverse()
            binding_path = base / "tampered_binding.json"
            binding_path.write_bytes(json.dumps(binding, ensure_ascii=False).encode())
            with self.assertRaisesRegex(gate.ReaderGateError, "source signs"):
                check(binding_path, None)

    def test_coherent_plus_minus_swap_masers_refused(self) -> None:
        self._coherent_swap("L4_masers_5")

    def test_coherent_plus_minus_swap_tdcosmo_refused(self) -> None:
        self._coherent_swap("L5_tdcosmo")

    def test_bare_cchp_133_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            binding = json.loads(BINDING.read_bytes())
            record = next(r for r in binding["readers"]
                          if r["reader_id"] == "L2_cchp")
            record["numeric_windows"]["sigma_components"][1]["literal"] = "1.33"
            path = Path(temp) / "bare.json"
            path.write_bytes(json.dumps(binding, ensure_ascii=False).encode())
            with self.assertRaisesRegex(gate.ReaderGateError, "minimum source context"):
                check(path)

    def test_inventory_rule_and_covariance_replicas(self) -> None:
        preliminary = pre.prepare_v1x(
            BINDING, expected_binding_sha256=sha(BINDING),
            allowed_source_root=SOURCE_ROOT, expected_spec_sha256=SPEC_SHA,
        )
        self.assertEqual(preliminary["n_alvos_declarados"], 2)
        with self.assertRaisesRegex(gate.ReaderGateError, "no pinned D-H admission parser"):
            pre.declared_inventory_ids(check()["verified_readers"],
                                       admitted_ids={"L1b_sh0es_r25"})
        spec = check()["spec_snapshot"]
        r25 = spec["familias"]["R_r25"]["ids"]
        sirens = spec["familias"]["S_com_sirenes"]["ids"]
        c25 = run.covariance(spec, r25, 0.5, 0.5)
        c6 = run.covariance(spec, sirens, 0.5, 0.5)
        self.assertGreater(c25[r25.index("L1b_sh0es_r25")][r25.index("L2_cchp")], 0)
        i = sirens.index("L6_sirenes")
        self.assertTrue(all(c6[i][j] == 0 for j in range(len(sirens)) if j != i))

    def test_synthetic_free_background_and_real_mode_refusal(self) -> None:
        result = run.run_synthetic(
            BINDING, sha(BINDING), SOURCE_ROOT, SPEC_SHA,
            FIXTURE, sha(FIXTURE), mode="synthetic_only",
        )
        self.assertFalse(result["data_opened"])
        self.assertIsNone(result["verdict"])
        self.assertEqual(result["n_alvos_declarados"], 2)
        self.assertEqual(result["synthetic_proposed_rule_output"]["classification"],
                         "INCONCLUSIVE_SYSTEMATICS")
        self.assertEqual(result["primary_rule1_if_applied"],
                         "INCONCLUSIVE_SYSTEMATICS")
        self.assertIn("R_r25", result["synthetic_statistics"])
        self.assertIn("S_com_sirenes", result["synthetic_statistics"])
        for family in result["synthetic_statistics"].values():
            for side in family.values():
                self.assertTrue(math.isfinite(side["lnB_TGL_free_background_n100"]))
                self.assertLess(
                    side["free_background_synthetic_mock"]["quadrature_abs_diff"], 1e-10
                )
        with self.assertRaisesRegex(gate.ReaderGateError, "mode refused"):
            run.run_synthetic(
                BINDING, sha(BINDING), SOURCE_ROOT, SPEC_SHA,
                FIXTURE, sha(FIXTURE), mode="real",
            )


    def test_pinned_verdict_other_branches_and_adverse_endpoints(self) -> None:
        result = run.run_synthetic(
            BINDING, sha(BINDING), SOURCE_ROOT, SPEC_SHA,
            FIXTURE, sha(FIXTURE), mode="synthetic_only",
        )
        spec = check()["spec_snapshot"]
        fn, digest = run.load_pinned_proposed_verdict(spec)
        self.assertEqual(digest, result["synthetic_proposed_rule_output"]["function_sha256"])
        args = json.loads(json.dumps(result["synthetic_proposed_rule_output"]["input"]))
        high = result["synthetic_statistics"]["P_primaria"]["maximum"]
        self.assertEqual(args["maximum"]["lnB_lcdm"], high["lnB_TGL_LCDM"])
        self.assertEqual(args["maximum"]["lnB_livre"], high["lnB_TGL_beta_free_n100"])
        self.assertEqual(args["minimum"]["z_delta"],
                         result["synthetic_statistics"]["P_primaria"]["minimum"]["z_delta_profile_logdet"])
        args["n_alvos_declarados"] = 0
        args["required_sources_admitted"] = True  # synthetic branch probe only
        args["beta_livre_no_limite"] = False
        args["dispersao_endpoints"] = {
            "minimum": {"chi2_por_gl": 0.0, "p": 1.0},
            "maximum": {"chi2_por_gl": 0.0, "p": 1.0},
        }
        args["minimum"]["z_delta"] = 5.1
        self.assertIn("FALSIFIED_AT_5SIGMA", fn(args))
        args["minimum"]["z_delta"] = 0.2
        args["maximum"].update({
            "poder_previo": 6.0, "z_disc": 6.0,
            "lnB_lcdm": 6.0, "lnB_livre": 0.0,
            "lnB_shift": 2.0, "lnB_fundo_livre": 2.0,
        })
        self.assertIn("DISCRIMINATES_FROM_LCDM", fn(args))


if __name__ == "__main__":
    unittest.main()