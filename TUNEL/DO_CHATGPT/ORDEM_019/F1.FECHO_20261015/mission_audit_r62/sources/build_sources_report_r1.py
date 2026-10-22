"""Read-only R62 source audit and local documentary custody; never import models."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import uuid

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent.parent
ORDER = OUT.parent
REF = Path(r"C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json")
CENTRAL = Path(r"C:\IALD\Central de Patentes")


def pin(path):
    p = Path(path)
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}


def save(name, value):
    p = ROOT / name
    assert p.parent == ROOT and not p.exists(), p
    data = ((value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)) + "\n").encode("utf8")
    temp = p.with_name(p.name + ".tmp_" + uuid.uuid4().hex)
    with temp.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    assert temp.read_bytes() == data
    os.rename(temp, p)
    return pin(p)


def main():
    finite = ORDER / "F1.REDE/finite_device"
    custody = json.loads((OUT / "oh_pair_dynamics_r61/CUSTODY_R61.json").read_text(encoding="utf8"))
    rechecks = []
    for s in custody["verified_sources"]:
        actual = pin(s["path"])
        assert actual["sha256"] == s["sha256"] and actual["bytes"] == s["bytes"], s["path"]
        rechecks.append({**actual, "matches_R61": True})
    paths = {
        "patent_v2": (CENTRAL / "Patentes/PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex", [(338, 370), (474, 516), (800, 828), (833, 885)]),
        "patent_JAN09_extract": (OUT / "continuity_r57/sources/SUPERCONDUTOR_JAN09_EXTRACT_R57.txt", [(71, 79), (143, 184)]),
        "graviton": (Path(r"C:\IALD\papers_latex\graviton_paper\graviton_paper.tex"), [(250, 260), (355, 368), (464, 475), (505, 510)]),
        "graviton_appendices": (Path(r"C:\IALD\papers_latex\graviton_paper_english_v2\graviton_appendices.tex"), [(110, 139), (311, 333)]),
        "finite_runner": (finite / "run_finite_device.py", [(25, 26), (101, 127), (163, 206)]),
        "finite_preregister": (finite / "PREREGISTRO_DEVICE_R1.json", []),
        "finite_receipt": (finite / "RUN_RECEIPT_DEVICE_R1.json", []),
        "finite_result": (finite / "RESULTADO_DEVICE_R1.json", []),
        "finite_freeze": (finite / "FREEZE_DEVICE_R1.json", []),
        "finite_log": (finite / "RUN_DEVICE_R1.log", []),
        "old_superconductor": (CENTRAL / "patents/BR102026003450-9_SUPERCONDUTOR/runner/one_supercondutor.py", [(103, 116), (190, 206)]),
        "R57_derivation": (OUT / "device_clock_r57/DERIVACAO_R57.md", [(11, 46), (53, 66), (118, 129), (149, 158), (198, 221)]),
        "R57_runner": (OUT / "device_clock_r57/derive_polarization_r57.py", [(84, 103), (126, 149)]),
        "R61_pair_runner": (OUT / "oh_pair_dynamics_r61/sources/explore_pairs_r59.py", [(7, 39), (40, 48)]),
        "R61_pair_result": (OUT / "oh_pair_dynamics_r61/sources/EXPLORATION_R59.json", []),
        "R61_report": (OUT / "oh_pair_dynamics_r61/RELATORIO_CANDIDATO_R61.md", []),
        "R61_review": (OUT / "oh_pair_dynamics_r61/FINAL_REVIEW_R61.json", []),
        "R61_custody": (OUT / "oh_pair_dynamics_r61/CUSTODY_R61.json", []),
        "R58_map": (OUT / "acervo_r58/dispositivos/SURVEY_DISPOSITIVOS_R58.json", []),
        "R60_report": (OUT / "relational_readout_r60/sources/RELATIONAL_BETA_REPORT_R1.json", []),
        "R59_squeezing": (OUT / "pair_covariance_r59/squeezing/DERIVATION_R1.txt", []),
        "nos_vivo": (ROOT.parent / "NOS_VIVO_R62.txt", []),
    }
    sources = []
    for key, (p, ranges) in paths.items():
        lines = p.read_text(encoding="utf-8-sig").splitlines()
        for a, b in ranges:
            assert 1 <= a <= b <= len(lines), (key, a, b, len(lines))
        sources.append({"id": key, **pin(p), "lines": len(lines), "read_ranges": ranges,
                        "excerpts": [{"first": a, "last": b, "text": "\n".join(f"{i}: {lines[i-1]}" for i in range(a, b+1))} for a, b in ranges]})
    rec = json.loads((finite / "RUN_RECEIPT_DEVICE_R1.json").read_text(encoding="utf8"))
    result = json.loads((finite / "RESULTADO_DEVICE_R1.json").read_text(encoding="utf8"))
    for field, name in [("log_sha256", "RUN_DEVICE_R1.log"), ("result_sha256", "RESULTADO_DEVICE_R1.json"), ("freeze_sha256", "FREEZE_DEVICE_R1.json")]:
        assert rec[field] == pin(finite / name)["sha256"]
    for field, name in [("runner_sha256", "run_finite_device.py"), ("preregister_sha256", "PREREGISTRO_DEVICE_R1.json"), ("freeze_sha256", "FREEZE_DEVICE_R1.json")]:
        assert result[field] == pin(finite / name)["sha256"]
    old_runner_pin = json.loads((finite / "PREREGISTRO_DEVICE_R1.json").read_text(encoding="utf8"))["source_pins"]["prior_superconductor_runner"]
    assert pin(old_runner_pin["path"])["sha256"] == old_runner_pin["sha256"]
    source_receipt = save("SOURCE_PINS_AND_ANCHORS_R1.json", {"status": "READ_ONLY_BYTE_CHECKED", "sources": sources, "R61_rechecks": rechecks,
        "existing_execution_receipt": {"exit_code": rec["exit_code"], "seconds": rec["seconds"], "checks_passed": result["checks_passed"], "checks_total": result["checks_total"], "rerun": False},
        "coverage": "Directed sources only: selected R58/R60/R61, explicit finite_device and device_clock_r57, pinned patent and articles. Not all archive; not a lexical universal absence proof."})
    findings = [
        {"id": "R62-S1", "class": "EXISTE_LIGADO_FINITO", "anchors": ["finite_runner:101-108", "finite_runner:163-186", "finite_runner:201-206"],
         "fact": "Hilbert dimension8; vectorized density dimension64. Existing liouvillian(h,jumps) constructs the full64x64 generator, retaining OH, JC, pump and five jumps. Existing expm(t*gen) propagates the full joint state.",
         "scope": "Bounded hard-core2x2x2 model. The existing142 checks are synthetic prior evidence; not rerun here. Conventional dissipators and dimensionless rates are INPUT, patent specifies H and holographic J but does not fix all rate values."},
        {"id": "R62-S2", "class": "REDUNDANCIA_EVITAVEL", "anchors": ["finite_runner:25-26", "finite_runner:101-114", "R61_pair_runner:19-26"],
         "fact": "A complete64-observable moment representation is a basis transform of the existing density generator, or a representation of its adjoint. It does not construct new dynamics or solve the physical reduction by itself.",
         "scope": "For moments m_A=Tr(rho A), define T rows vec(A^T)^T; if full basis, M=T L T^-1. Complex non-Hermitian coordinates require this bilinear trace convention, not an unqualified conjugate transpose. No matrixM or rank was computed here. A minimal invariant/Krylov subspace would be genuinely additional, but not necessary for full-state readout."},
        {"id": "R62-S3", "class": "EXISTE_PREPARO_INPUT_NAO_FISICO", "anchors": ["finite_runner:174-181", "R61_pair_runner:32-39", "R61_report:section4", "R57_runner:126-149"],
         "fact": "Existing finite tests use synthetic mixed/pure/basis states. R59/R61 already specifies psi_q=(|00>+q|11>)/sqrt(1+q^2) tensor one of five OH states. R57 uses optical vacuum tensor a named OH density.",
         "scope": "These are complete joint mathematical preparations, no need to invent another. They are not derived preparation channels of the patented apparatus; product structure and q are INPUT. Correlated rho+/- fromR61 demonstrate why marginals alone do not determine subsequent reduced evolution."},
        {"id": "R62-S4", "class": "EXISTE_PROTOCOLO_MATERIAL_NAO_DENSIDADE", "anchors": ["patent_v2:833-885", "patent_JAN09_extract:157-175"],
         "fact": "Patent prescribes purge/vacuum, water injection, RF excitation and plasma activation, followed by modulated light input. It names OH/optical hardware and operational sequence.",
         "scope": "No joint normalized optical-OH density, preparation channel, initial correlation control or assurance of the R61 product preparation was located in these passages. This is a bounded documentary finding, not absence throughout C:\\IALD."},
        {"id": "R62-S5", "class": "EXISTE_INGREDIENTE_RECEPTOR", "anchors": ["graviton_appendices:311-333", "graviton:464-475", "graviton:505-510", "patent_JAN09_extract:153-184", "patent_v2:800-828"],
         "fact": "Articles prescribe balanced50/50 homodyne, adjustable phase-locked LO, quadrature scanning and density tomography; heterodyne g1 and HBTg2 are distinct proposals. Patent specifies laser/EOM/APD/lock-in, including relative output/input phase.",
         "scope": "Two synchronized channel quadratures and their relation to OH-device C/B are not thereby implemented. eta(tau) inJAN09 is a normalized voltage correlation at two times, not automatically either equal-time C or B. C, B, g1, g2 and sigma+ must stay distinct; article modes are Psi modes, not an already demonstrated optical/OH identification."},
        {"id": "R62-S6", "class": "PROXIMA_PONTE_TIPADA", "anchors": ["graviton_appendices:124-127", "graviton_appendices:318-331", "R61_report:section2"],
         "fact": "Shortest next component: specify X_j(theta)=(exp(-i theta)a_j+exp(i theta)a_j_dagger)/sqrt2 and read H(theta,eta)=Tr(rho X_i(theta)X_o(eta)) on the same joint state. Four phase pairs (0,0),(0,pi/2),(pi/2,0),(pi/2,pi/2) can be used to verify a linear inverse for C/B.",
         "scope": "Proposed algebraic adapter for explicit synthetic state, pending its own verification; not a located ready physical detector equation. Requires phase convention, calibration/gain/loss/noise and two-channel access. For truncated operators, a physical homodyne POVM/compression needs its own justification; do not silently declare finite spin quadrature to be the full bosonic detector."},
        {"id": "R62-S7", "class": "EXISTE_OBSTRUCAO_REDUZIDA_NAO_GLOBAL", "anchors": ["R61_report:sections3-5", "R61_pair_runner:14-31", "R57_derivation:118-129"],
         "fact": "R61 gives Ldag C=-(d+2i wc)C-i g Zi ao sigma-, Ldag B=-dB+i g Zi ao sigma+, d=(ki+ko+lambda)/2. The full density propagation already transports those auxiliary correlations.",
         "scope": "No need to close C/B alone; zeroing pump/coupling or discarding OH would change the source. Finite CCR is [a,a_dagger]=Z, notI; lambda/2 and n(1-n) must not be transplanted into infinite bosonic formulas."},
        {"id": "R62-S8", "class": "RESIDUO_FISICO_EXPLICITO", "anchors": ["patent_v2:474-516", "old_superconductor:103-116", "old_superconductor:190-206", "R57_derivation:198-221", "R61_report:section6"],
         "fact": "G_OH=e^(i omegaOH t)tanh(PMW/Pth) is written multiplicatively in the patent; the older runner samples tanh/approach-to-plateau laws directly. These do not derive the signal from the joint GKLS.",
         "scope": "Retain unproved mapping of physical preparation/readout, units/gammaLambda/loss separation, V0/Eref/kappa and Maxwell/network identification. A detector adapter plus full finite propagation is useful progress; no R4/R5 completion or beta measurement follows."},
    ]
    report = {"kind": "R62_DIRECTED_PREPARATION_READOUT_REUSE", "author": "codex-directed-sources-r62", "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
              "status": "DECLARADO_PENDING_INDEPENDENT_REVIEW", "mission_reference": pin(REF), "requirement_satisfied": False, "sources": source_receipt, "findings": findings,
              "next_step": "Reuse existing full generator and a named R61 joint preparation. Verify only the two-channel quadrature/C-B readout adapter and its phase convention, then compare its traces against the same full state. Keep physical realization and calibrated units explicit. Do not reconstruct full64-moment dynamics merely to rediscover closure.",
              "execution": {"simulation": False, "source_import_or_execution": False, "new_math_tests": 0, "providers": 0, "observed_data": False, "original_changes": False, "mission_or_memory_changes": False}}
    save("DIRECTED_REUSE_REPORT_R1.json", report)
    save("DIRECTED_REUSE_REPORT_R1.txt", """R62 — levantamento dirigido: preparação conjunta, receptor e fecho finito
DECLARADO; revisão independente pendente. R4/R5 integrais não satisfeitos.
1. O Liouvilliano completo já existe: run_finite_device.py101–108,163–186; H8x8, L64x64, OH+JC+bombeamento+cinco saltos; exp(tL)201–206. Recibo antigo e142checks pinados, sem repetição.
2. Matriz completa de64momentos seria mudança de base/dual do mesmo gerador. Não acrescenta uma dinâmica nem resolve a identificação física. Um subespaço invariante mínimo seria etapa nova, desnecessária para propagar rho integral.
3. Preparo matemático conjunto já existe: R59/R61, (|00>+q|11>)/sqrt(1+q²) tensor cinco opçõesOH. É INPUT, não canal de preparo derivado da patente; não descartar correlaçõesOH arbitrárias.
4. Patente v2:833–885 e JAN09:157–175 dão preparação material/RF/plasma/luz modulada; não fixam a densidade conjunta ou a hipótese produto dessas simulações.
5. Homódino balanceado comLOajustável e tomografia já escritos: graviton_appendices311–333; heteródino g1/HBTg2: graviton464–475. Não equivalem entre si ou a sigma+.
6. JAN09:153 especifica lock-in relativo;182–184 define eta(tau) de tensões em duas épocas. Não é automaticamente B=<ai†ao> ou C=<ai ao> em tempos iguais. Dois canais/fases sincronizados requerem contrato explícito.
7. Próxima peça curta: adaptador das quatro correlações de quadraturas para C/B, sob estado conjunto já nomeado e convenção de fases; usar o gerador existente, sem reconstruir matriz64. O colega prepara este plano, sem execução nesta revisão.
8. Domínio do corte e receptor físico permanecem separados: quadraturas de dois níveis não conferem por nome uma POVM homódina bosônica. CampoPsi/artigo, laser/patente eOH não se identificam automaticamente.
9. G_OH=e^(iomegaOH t)tanh(PMW/Pth) é prescrição documental; runner antigo também aplica tanh/platô. Receptor não deriva essa lei nem beta. Unidades, gammaLambda, perdas, V0/Eref/kappa e redeMaxwell continuam explícitos.
Pinos/trechos emSOURCE_PINS_AND_ANCHORS_R1.json. Cobertura dirigida, sem ausência universal, simulação, execução/import de fontes, provedor, dado observado, alteração original/ACOM/memória.
""")
    request = {"operation": "project", "reference": str(REF), "max_chars": 400000}
    proc = subprocess.run([r"C:\Python314\python.exe", "-B", "-X", "utf8", r"C:\IALD\MEMORIA_IALD\mission_cli.py"], input=json.dumps(request), text=True, encoding="utf8", capture_output=True)
    response = json.loads(proc.stdout)
    assert proc.returncode == 0 and response["ok"]
    save("PROJECT_RETURN_R1.json", {"request": request, "response": response, "exit_code": proc.returncode, "stderr": proc.stderr})
    for s in sources:
        assert pin(s["path"])["sha256"] == s["sha256"]
    names = ["build_sources_report_r1.py", "DIRECTED_REUSE_REPORT_R1.json", "DIRECTED_REUSE_REPORT_R1.txt", "SOURCE_PINS_AND_ANCHORS_R1.json", "PROJECT_START_R1.json", "PROJECT_RETURN_R1.json"]
    delivery = save("DELIVERY_R1.json", {"kind": "R62_SOURCES_DELIVERY", "author": "codex-directed-sources-r62", "status": "DECLARADO_PENDING_INDEPENDENT_REVIEW", "requirement_satisfied": False,
        "mission_reference": pin(REF), "revision_final": response["result"]["receipt"]["revision"], "files": [pin(ROOT / n) for n in names], "source_count": len(sources), "R61_source_rechecks": len(rechecks), "findings": len(findings), "sources_rechecked_at_return": True, "simulations": 0, "new_tests": 0, "providers": 0, "original_or_memory_mutations": False})
    print(json.dumps({"delivery": delivery, "sources": len(sources), "R61_rechecks": len(rechecks), "findings": len(findings), "revision": response["result"]["receipt"]["revision"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
