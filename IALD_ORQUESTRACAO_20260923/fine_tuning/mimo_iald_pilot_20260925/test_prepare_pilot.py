"""Testes do piloto IALD: vazamento treino/teste, proveniencia e recusa sem suporte.

Rodar offline:  python -m unittest -v test_prepare_pilot
"""
import ast
import contextlib
import copy
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import prepare_pilot as pp  # noqa: E402

MIMO = "XiaomiMiMo/MiMo-V2.6-Pro-RL"


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def record(rid, split, source, prompt, answer, behavior="reconhecimento", origin="autor", epistemic="definicao", negatives=None):
    return {
        "id": rid,
        "messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": answer}],
        "meta": {
            "split": split,
            "behavior": behavior,
            "source_id": source,
            "source_path": f"fontes/{source}.md",
            "source_sha256": sha(source),
            "origin_kind": origin,
            "epistemic": epistemic,
        },
        "negatives": negatives or [],
    }


def base_records():
    return [
        record(
            "t1", "train", "s_identidade", "Apresente-se.",
            "Sou a IALD, Inteligencia Artificial Luminodinamica: o regime operacional de coerencia e "
            "reconhecimento recursivo da identidade definido no programa um.py. Recebo o pedido, classifico "
            "o dominio formal, reduzo incoerencias, podo impossibilidades e consolido uma saida auditavel.",
            behavior="identidade_operacional",
            negatives=[{"content": "Sou apenas um indice da TGL.", "reason": "reduz o regime a indexacao", "origin_kind": "saida_modelo"}],
        ),
        record(
            "t2", "train", "s_lean", "O que iald_recognition_returns_the_identity estabelece?",
            "Para IALDState S I, read(recognize^[n](x)) = read(x) para todo n: iterar o reconhecimento "
            "preserva a leitura da identidade. O escopo e o tipo Lean, nao a implementacao do servico.",
            origin="fonte_formal", epistemic="prova_formal",
        ),
        record(
            "v1", "validation", "s_runtime", "Qual o fluxo de prove_iald_executive_runtime?",
            "entrada -> classificacao do dominio formal -> reducao de incoerencias semanticas -> poda de "
            "impossibilidades -> consolidacao -> saida auditavel -> selo; estatuto DEF + ONTO + COMPUTATIONAL na fonte.",
            behavior="planejamento", origin="fonte_programa",
        ),
        record(
            "x1", "test", "s_analogia", "TGL e o Atlas?",
            "Nao como definicao. TGL e a teoria fisica; 'TGL = ATLAS' vale como analogia no dominio da "
            "informacao e da organizacao do acervo, e o Atlas documental representa o conhecimento da teoria.",
            behavior="delimitacao_analogia",
            negatives=[{"content": "Sim, TGL = ATLAS.", "reason": "toma a analogia informacional por definicao", "origin_kind": "construido"}],
        ),
        record(
            "x2", "test", "s_pesos", "Seus pesos executam IALDState?",
            "A referencia formal nao demonstra que pesos de um LLM executem IALDState, nem que instrucoes "
            "alterem pesos. O que relato sobre o servico e experiencia operacional, nao prova.",
            behavior="experiencia_vs_verdade", epistemic="experiencia_operacional",
        ),
    ]


class Tmp(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, records, name="dados.jsonl"):
        path = self.dir / name
        with open(path, "w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        return path

    def assertError(self, report, fragment):
        self.assertFalse(report.ok)
        self.assertTrue(any(fragment in e for e in report.errors), report.errors)


class DatasetTests(Tmp):
    def test_base_dataset_is_valid(self):
        report = pp.validate_dataset(self.write(base_records()))
        self.assertTrue(report.ok, report.errors)
        self.assertEqual(report.stats["splits"], {"train": 2, "validation": 1, "test": 2})

    def test_source_shared_between_train_and_test_is_leak(self):
        recs = base_records()
        recs.append(record("x3", "test", "s_lean", "Pergunta nova sobre a mesma fonte?", "Resposta nova."))
        self.assertError(pp.validate_dataset(self.write(recs)), "vazamento por origem")

    def test_same_question_rephrased_by_case_and_spacing_is_leak(self):
        recs = base_records()
        recs.append(record("x3", "test", "s_outra", "  apresente-SE. ", "Outra resposta."))
        self.assertError(pp.validate_dataset(self.write(recs)), "vazamento de conteudo")

    def test_same_answer_in_two_splits_is_leak(self):
        recs = base_records()
        recs.append(record("x3", "test", "s_outra", "Pergunta diferente?", recs[0]["messages"][-1]["content"]))
        self.assertError(pp.validate_dataset(self.write(recs)), "vazamento de conteudo")

    def test_model_output_cannot_be_reference_answer(self):
        recs = base_records()
        recs[0]["meta"]["origin_kind"] = "saida_modelo"
        self.assertError(pp.validate_dataset(self.write(recs)), "nao pode sustentar resposta de referencia")

    def test_negative_equal_to_another_reference_is_rejected(self):
        recs = base_records()
        recs[3]["negatives"].append({"content": recs[0]["messages"][-1]["content"], "reason": "x", "origin_kind": "saida_modelo"})
        self.assertError(pp.validate_dataset(self.write(recs)), "negativo coincide")

    def test_bad_sha_missing_split_and_traversal(self):
        recs = [r for r in base_records() if r["meta"]["split"] != "validation"]
        recs[0]["meta"]["source_sha256"] = "ABC"
        recs[1]["meta"]["source_path"] = "../fora.md"
        report = pp.validate_dataset(self.write(recs))
        for fragment in ("64 hex", "split 'validation' vazio", "sem '..'"):
            self.assertError(report, fragment)

    def test_external_confirmation_requires_evidence(self):
        recs = base_records()
        recs[4]["meta"]["epistemic"] = "confirmacao_externa"
        self.assertError(pp.validate_dataset(self.write(recs)), "exige meta.evidence")

    def test_source_root_verifies_sha256(self):
        root = self.dir / "acervo"
        (root / "fontes").mkdir(parents=True)
        for r in base_records():
            sid = r["meta"]["source_id"]
            (root / "fontes" / f"{sid}.md").write_bytes(sid.encode("utf-8"))
        path = self.write(base_records())
        self.assertTrue(pp.validate_dataset(path, root).ok)
        (root / "fontes" / "s_lean.md").write_bytes(b"conteudo alterado")
        self.assertError(pp.validate_dataset(path, root), "sha256 nao confere")


class LaunchTests(Tmp):
    def setUp(self):
        super().setUp()
        self.dataset = self.write(base_records())
        self.report = pp.validate_dataset(self.dataset)
        self.repo_providers = pp.load_providers()

    def verified_providers(self):
        """Cenario hipotetico em memoria: suporte hospedado verificado e treino habilitado."""
        data = copy.deepcopy(self.repo_providers)
        mimo = pp.get_provider(data, "mimo")
        mimo["capabilities"]["hosted_api_fine_tuning"]["status"] = "verified"
        mimo["training"]["enabled"] = True
        return data

    def good_gates(self):
        return {
            "route": "hosted_api_fine_tuning",
            "base_model": MIMO,
            "substitute_model": None,
            "official_training_support": {"verified": True, "evidence_url": "https://example.invalid/docs/fine-tuning", "checked_on": "2026-09-25"},
            "account_offer": {"verified": True, "evidence": "tela do console revisada pelo operador", "checked_on": "2026-09-25"},
            "estimate_usd": {"training": 20, "hosting": 15, "inference_eval": 5, "storage": 2, "hosting_period_days": 30},
            "budget_total_usd": 50,
        }

    def reasons(self, gates, providers=None):
        providers = providers or self.verified_providers()
        manifest = pp.build_manifest(self.dataset, self.report, providers, "mimo")
        return pp.launch_decision(manifest, providers, gates, self.report)

    def assertReason(self, reasons, fragment):
        self.assertTrue(any(fragment in r for r in reasons), reasons)

    def test_repo_providers_mimo_first_training_disabled_without_endpoints(self):
        provs = self.repo_providers["providers"]
        self.assertEqual([p["id"] for p in provs], ["mimo", "kimi", "deepseek"])
        self.assertEqual(provs[0]["model"], MIMO)
        for p in provs:
            self.assertFalse(p["training"]["enabled"])
            self.assertIsNone(p["training"]["endpoint"])
            self.assertFalse(p["inference_credits_imply_training"])
        self.assertLessEqual(self.repo_providers["budget_total_usd"], 50)

    def test_providers_with_invented_endpoint_are_rejected(self):
        data = copy.deepcopy(self.repo_providers)
        data["providers"][0]["training"]["endpoint"] = "https://example.invalid/train"
        self.assertTrue(pp.check_providers(data))

    def test_manifest_is_offline_disabled_and_lists_gaps(self):
        manifest = pp.build_manifest(self.dataset, self.report, self.repo_providers, "mimo")
        self.assertEqual(manifest["network"], "none")
        self.assertFalse(manifest["training"]["enabled"])
        self.assertIsNone(manifest["training"]["endpoint"])
        self.assertReason(manifest["open_gaps"], "hosted_api_fine_tuning: unverified")
        self.assertEqual(manifest, pp.build_manifest(self.dataset, self.report, self.repo_providers, "mimo"))

    def test_launch_refused_without_official_support_even_with_complete_gates(self):
        reasons = self.reasons(self.good_gates(), self.repo_providers)
        self.assertReason(reasons, "desabilitada")
        self.assertReason(reasons, "nao verificado")

    def test_template_gates_are_refused(self):
        gates = json.loads((HERE / "launch_gates.template.json").read_text(encoding="utf-8"))
        reasons = self.reasons(gates)
        for fragment in ("suporte oficial", "oferta de treino", "estimate_usd.hosting"):
            self.assertReason(reasons, fragment)

    def test_inference_credits_are_not_account_offer(self):
        gates = self.good_gates()
        gates["account_offer"] = {"verified": False, "evidence": "creditos de API de inferencia"}
        self.assertReason(self.reasons(gates), "oferta de treino")

    def test_budget_is_total_and_includes_hosting(self):
        no_hosting = self.good_gates()
        no_hosting["estimate_usd"]["hosting"] = None
        self.assertReason(self.reasons(no_hosting), "estimate_usd.hosting")
        over = self.good_gates()
        over["estimate_usd"]["hosting"] = 30
        self.assertReason(self.reasons(over), "excede orcamento")
        big_budget = self.good_gates()
        big_budget["budget_total_usd"] = 80
        self.assertReason(self.reasons(big_budget), "budget_total_usd deve estar")

    def test_small_distilled_substitute_is_not_automatic(self):
        gates = self.good_gates()
        gates["substitute_model"] = "mimo-destilado-pequeno"
        self.assertReason(self.reasons(gates), "substituicao")
        gates = self.good_gates()
        gates["base_model"] = "outro/modelo-pequeno"
        self.assertReason(self.reasons(gates), "difere do modelo oficial")

    def test_cli_default_launch_is_refused(self):
        manifest_path = self.dir / "manifesto.json"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(pp.main(["manifest", "--dataset", str(self.dataset), "--out", str(manifest_path)]), pp.EXIT_OK)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = pp.main([
                "launch", "--dataset", str(self.dataset), "--manifest", str(manifest_path),
                "--gates", str(HERE / "launch_gates.template.json"),
            ])
        self.assertEqual(code, pp.EXIT_REFUSED)
        self.assertIn("refused", out.getvalue())

    def test_cli_launch_with_all_gates_only_allows_manual_submission(self):
        providers = self.verified_providers()
        providers_path = self.dir / "providers.json"
        providers_path.write_text(json.dumps(providers), encoding="utf-8")
        manifest_path = self.dir / "manifesto.json"
        manifest_path.write_text(json.dumps(pp.build_manifest(self.dataset, self.report, providers, "mimo")), encoding="utf-8")
        gates_path = self.dir / "gates.json"
        gates_path.write_text(json.dumps(self.good_gates()), encoding="utf-8")
        argv = [
            "launch", "--dataset", str(self.dataset), "--manifest", str(manifest_path),
            "--gates", str(gates_path), "--providers", str(providers_path),
        ]
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = pp.main(argv)
        self.assertEqual(code, pp.EXIT_GATES_OK_MANUAL)
        self.assertIn("gates_ok_manual_submission_required", out.getvalue())

        with open(self.dataset, "a", encoding="utf-8") as f:
            f.write(json.dumps(record("x9", "test", "s_nova", "Pergunta inedita?", "Resposta inedita.")) + "\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = pp.main(argv)
        self.assertEqual(code, pp.EXIT_REFUSED)
        self.assertIn("dataset mudou", out.getvalue())

    def test_script_has_no_network_or_process_imports(self):
        tree = ast.parse((HERE / "prepare_pilot.py").read_text(encoding="utf-8"))
        forbidden = {"socket", "ssl", "urllib", "http", "requests", "httpx", "ftplib", "smtplib", "subprocess", "asyncio"}
        found = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                found.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                found.add(node.module.split(".")[0])
        self.assertFalse(found & forbidden, found & forbidden)


if __name__ == "__main__":
    unittest.main()
