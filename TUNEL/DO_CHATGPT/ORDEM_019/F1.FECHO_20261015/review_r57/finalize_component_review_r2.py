"""Seal the focused independent review after the final R5 receipt arrives.

Only reads scientific files/mission and creates new reviewer artifacts. No build,
provider call, acceptance, or transition is available in this script.
"""
from pathlib import Path
import argparse
import datetime
import json
import subprocess
import verify_layer2_pins_r1 as checks

OUT = Path(__file__).resolve().parent.parent
REF = Path(r"C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json")
ACTOR = {"kind": "agent", "id": "codex-mission-memory-review"}


def measured(rel):
    return checks.pin(OUT / rel)


def anchor(rel, first, last):
    return {**measured(rel), "line_start": first, "line_end": last}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--r5-delivery", required=True)
    parser.add_argument("--complex-receipt", required=True)
    args = parser.parse_args()
    delivery_path = Path(args.r5_delivery).resolve()
    receipt_path = Path(args.complex_receipt).resolve()
    assert delivery_path.is_relative_to(OUT) and receipt_path.is_relative_to(OUT)
    delivery = json.loads(delivery_path.read_text(encoding="utf-8"))
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    checks.walk(delivery)
    checks.walk(receipt)
    assert receipt["exit_code"] == 0 and receipt["source_unchanged"]
    snapshot = Path(receipt["source"]["path"])
    original = Path(receipt["source_original"]["path"])
    assert snapshot.read_bytes() == original.read_bytes()
    start_path = receipt_path.parent / "START_RECEIPT.json"
    start = json.loads(start_path.read_text(encoding="utf-8"))
    assert start["source"] == receipt["source"] and start["source_original"] == receipt["source_original"]
    log = next(x for x in receipt["artifacts"] if Path(x["path"]).name == "BUILD.log")
    axioms = checks.axiom_report(Path(log["path"]).read_text(encoding="utf-8"), 8)
    for item in receipt["dependencies"]:
        if Path(item["path"]).stem in {"CompactPacketRefinementR1", "PhysicalCanonicalNetCompleteR1"}:
            checks.verify(item)
    assert not checks.MISMATCHES, checks.MISMATCHES

    base_path = OUT / "review_r57/PIN_VERIFICATION_LAYER2_BASE_R1.json"
    base = json.loads(base_path.read_text(encoding="utf-8"))
    assert base["ok"]
    request = {"operation": "project", "reference": str(REF), "actor": ACTOR, "max_chars": 200000}
    result = subprocess.run([r"C:\Python314\python.exe", "-B", "-X", "utf8", r"C:\IALD\MEMORIA_IALD\mission_cli.py"],
                            input=json.dumps(request), text=True, encoding="utf-8", capture_output=True)
    now = datetime.datetime.now(datetime.timezone.utc)
    project_path = OUT / "review_r57" / ("PROJECT_LAYER2_FINAL_" + now.strftime("%Y%m%dT%H%M%S_%fZ") + ".json")
    with project_path.open("x", encoding="utf-8", newline="\n") as f:
        f.write(result.stdout)
    project_result = json.loads(result.stdout)
    assert result.returncode == 0 and project_result["ok"], result.stderr
    projection = project_result["result"]["projection"]
    begin_path = OUT / "review_r57/PROJECT_LAYER2_REANCHORED_20261017T155202_188151Z.json"
    begin = json.loads(begin_path.read_text(encoding="utf-8"))["result"]["projection"]
    active = {x["id"]: x for x in projection["active"]}
    before = {x["id"]: x for x in begin["active"]}
    for key in ["R4", "R5"]:
        assert active[key]["criterion"] == before[key]["criterion"]
        assert active[key]["status"] != "satisfied"
    settled = {x["id"]: x["status"] for x in projection["settled"]}
    for item in begin["settled"]:
        assert settled.get(item["id"]) == item["status"]

    r4 = "device_clock_r57/"
    r5 = "device_continuum_r57/"
    report = {
        "schema": "iald-r57-independent-final-component-review/v1",
        "created_utc": now.isoformat(), "reviewer": ACTOR,
        "verdict": "PASS_COMPONENT_WITH_SCOPE", "requirement_satisfied": {"R4": False, "R5": False},
        "mission": {"reference": checks.pin(REF), "context_id": projection["context_id"],
                    "start_project": checks.pin(begin_path), "start_revision": begin["revision"],
                    "final_project": checks.pin(project_path), "final_revision": projection["revision"],
                    "state_sha256": projection["state_sha256"],
                    "criteria": {key: active[key]["criterion"] for key in ["R4", "R5"]},
                    "criteria_unchanged": True, "previously_satisfied_preserved": settled,
                    "mission_mutation_by_reviewer": False},
        "method": "Revisão focal de fontes, enunciados e cadeia de pinos/recibos. Nenhum novo build, provedor ou repetição das 34 verificações simbólicas/23 controles independentes anteriores.",
        "prior_reviews_preserved": [measured("review_r57/R57_CLOCK_AND_CUSTODY_REVIEW_R1.json"),
                                    measured("review_r57/R57_TABLE_CUSTODY_REVIEW_ADDENDUM_R1.json")],
        "pin_verification": {"base": checks.pin(base_path), "base_unique_files": base["unique_files_measured"],
                             "final_additional_unique_files": len(checks.CHECKED),
                             "final_pins": list(checks.CHECKED.values()), "mismatches": checks.MISMATCHES,
                             "scope": "Bytes dos artefatos, snapshots e fornecedores selecionados conferidos. Estabilidade integral das dependências é informação dos recibos do construtor; não houve novo build ou reauditoria de todo o grafo."},
        "deliveries": [measured(r4 + "DELIVERY_R57.json"), checks.pin(delivery_path)],
        "builds": base["builds"] + [{"receipt": checks.pin(receipt_path), "start": checks.pin(start_path),
                                      "source": receipt["source"], "source_original": receipt["source_original"],
                                      "exit_code": 0, "seconds": receipt["seconds"], "axioms": axioms,
                                      "start_final_source_pins_equal": True, "snapshot_equals_current": True,
                                      "readonly_dependencies_unchanged_reported_by_builder": receipt["readonly_dependencies_unchanged"]}],
        "printed_axiom_checks": 37,
        "R4": {
            "finite_model": {"statute": "REAL/DERIVED", "finding": "As 34 verificações originais e os 23 controles independentes anteriores são reutilizados. O complemento restringe z', z'' e phi'' ao modelo 2x2x2 com todos os termos; não transfere a CCR do cutoff ao modelo bosônico.",
                             "anchor": anchor(r4 + "COMPLEMENTO_DOMINIO_RELOGIO_LOCAL_R57.md", 7, 27)},
            "bosonic_core": {"statute": "DERIVED — leitura algébrica, sem semigrupo", "finding": "No núcleo finito de partículas, a expectativa no vácuo/estado fundamental do termo de bomba é i*Omega. Livre, JC e dissipadores têm expectativa zero nesse vetor. Isso exclui a identidade de eigenobservável universal com bomba positiva nesse núcleo; não prova geração de semigrupo não limitado."},
            "local_clock": {"statute": "DERIVED — análise finita local, não teorema Lean desta entrega", "finding": "Analiticidade de exp(tL), z(0)=a>0 e phi'(0)=omegaOH>0 dão ramo local de Log e inversa real. Com C=Omega*(gamma+lambda)/a, phi=omegaOH*t+C*t^2+O(t^3) implica t=phi/omegaOH-C*phi^2/omegaOH^3+O(phi^3). Não fornece tamanho do intervalo, calibração em segundos, monotonicidade global ou leitura instrumental.",
                            "anchor": anchor(r4 + "COMPLEMENTO_DOMINIO_RELOGIO_LOCAL_R57.md", 29, 54)},
            "demodulation": {"statute": "DERIVED — sob LAB_PHASE_LOCKED_DRIVE e misturador ideal", "finding": "b=exp(-i*omega_d*t)*z_lab=z_rot cancela a portadora de referência; envelope estacionário gera sinal relativo constante. A declaração documental de lock-in 1Hz–100MHz não implementa recepção direta de 1,667GHz. Conversão óptica, misturador, filtros, banda, ruído e observável permanecem abertos.",
                             "anchor": anchor(r4 + "COMPLEMENTO_DOMINIO_RELOGIO_LOCAL_R57.md", 56, 78)},
            "fixed_boundary": {"statute": "REAL — Lean EXIT0, 6 prints trio", "finding": "A_beta(z)=z*S(thetaMiguel beta) lê z*exp(i thetaMiguel), permite reconstrução e releitura idempotente. Para 0<=beta<=1, os pesos são normSq(z)*beta e normSq(z)*(1-beta). Razão normalizada/fase requerem sinal não nulo; zero dá matriz zero. Nenhuma hipótese de G_OH dinâmico é disfarçada em construção de detector.",
                               "anchor": anchor(r4 + "MiguelFixedBoundaryScalarReadingR57R2.lean", 18, 79)},
            "remaining": "Mapa físico receptor/observável, preparação e contrato lab–rotante, calibração e ligação de V0/Eref/Killing-kappa/omegaOH com unidades e domínio no mesmo sistema. R4 integral não satisfeito."},
        "R5": {
            "tower": {"statute": "REAL — Lean EXIT0, 3 prints trio", "finding": "V:TorreProduto(P)->L[complex]H1 e V(modularFlow P(clock s)x)=B0 s(Vx) implicam V=0. Cada eigenvetor local vai a zero por B0_no_eigen; totalidade e continuidade fecham a prova. Arbitrária reparametrização clock não altera a obstrução. Exclui entrelaçador isométrico dessa torre, não todo dispositivo, estado não produto, limite de escala ou ação Fock.",
                      "anchor": anchor(r5 + "TowerBoostObstructionR2.lean", 18, 64)},
            "real_packets": {"statute": "REAL — Lean EXIT0, 20 prints trio", "finding": "Finsets de circularSmear de testes Maxwell reais compactos geram subespaços reais finitos do mesmo H1. Inclusões literais isométricas e união dirigida recuperam compactLocalized O após fecho. U1 e helicityUnitary transportam níveis e regiões, com quadrados de refinamento e boosts=B0; não tornam cada nível finito invariante.",
                             "anchors": [anchor(r5 + "CompactPacketRefinementR1.lean", 19, 101), anchor(r5 + "CompactPacketRefinementR1.lean", 103, 210)]},
            "complex_packets": {"statute": "REAL — Lean EXIT0, 8 prints trio", "finding": "Span complexo das mesmas listas possui inclusões isométricas compatíveis, é dirigido e sua união na cunha direita é densa no mesmo H1. Consome densidade e igualdade de cunha já construídas. É uma família concreta de aproximação no alvo canônico, não uma identificação do Hilbert de células nem uma nova localização complexa.",
                                "source": checks.pin(original), "line_start": 14, "line_end": 98},
            "reused_suppliers": [anchor("orbital_rotation/PhysicalCompactNetCovarianceR1.lean", 15, 21),
                                 anchor("orbital_rotation/PhysicalCompactNetCovarianceR1.lean", 58, 66),
                                 anchor("orbital_rotation/PhysicalCompactNetCovarianceR1.lean", 109, 114),
                                 anchor("orbital_rotation/PhysicalCanonicalWedgeEqualityR3.lean", 19, 29)],
            "remaining": "Construir a partir dos observáveis físicos a forma de duas pontas, o mapa para circularSmear, refinamentos compatíveis, convergência de estados/correlações e ações/geradores/localização no mesmo limite. Q6 exata por região não é substituída por convergência assintótica. O contrato residual é plano tipado de construção, não alteração do critério original.",
            "residual_contract": measured(r5 + "RESIDUAL_TYPED_CONTRACT_R1.txt"),
            "packet_chain": measured(r5 + "PACKET_CHAIN_R57_R1.json")},
        "documentary_custody": {"paragraph_custody": measured("continuity_r57/SOURCE_JAN09_CUSTODY_R57.json"),
                               "table_custody": measured("continuity_r57/SOURCE_JAN09_TABLE_CUSTODY_R57.json"),
                               "table_text": measured("continuity_r57/sources/SUPERCONDUTOR_JAN09_TABLES_R57.txt"),
                               "scope": "R1 e adendo já verificaram extrações/trechos. A tabela de correspondências acrescenta proveniência documental; não fornece o entrelaçador físico ou confirmação experimental."},
        "findings": [{"severity": "LOW", "id": "PACKET_PREFREEZE_HISTORY", "blocking": False,
                      "finding": "Leitura histórica citava 8.332 bytes. Candidato pinado, início, snapshot compilado, recibo final e fonte atual coincidem em 9.139 bytes. O autor declarou adição pré-freeze de movePacket_mono/packetMove_refinement; não foi localizado artefato de 8.332 bytes, portanto não se inventa hash ou custódia retroativa. A aprovação do componente refere-se somente aos bytes efetivamente compilados."},
                     {"severity": "LOW", "id": "UNUSED_SIMP_ARGUMENTS", "blocking": False,
                      "finding": "Avisos de argumento simp não usado em CompactPacketRefinementR1:120 e ComplexPacketLimitR1:89 preservados. Sem alteração de fontes ou nova rodada de compilação por esses avisos."}],
        "limits": ["R4 e R5 integrais continuam abertos; nenhuma transição de aceite pelo revisor.",
                   "Não houve provider, rebuild, edição de fonte, memória canônica, kernel, gate ou dados.",
                   "Correspondência documental, derivação finita, prova Lean e realização física têm alcances distintos.",
                   "Papéis complementares MQC/Supercondutor/Psi-NET preservados; nenhum aparelho singular escolhido por inferência.",
                   "O parecer não afirma confirmação da TGL, realização física experimental, nem Lindblad nos pesos."],
        "review_runner": checks.pin(__file__)}
    dest = OUT / "review_r57/R57_FINAL_COMPONENT_REVIEW_R2.json"
    with dest.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(json.dumps({"review": checks.pin(dest), "verdict": report["verdict"], "revision": projection["revision"],
                      "printed_axiom_checks": 37, "requirements_satisfied": report["requirement_satisfied"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
