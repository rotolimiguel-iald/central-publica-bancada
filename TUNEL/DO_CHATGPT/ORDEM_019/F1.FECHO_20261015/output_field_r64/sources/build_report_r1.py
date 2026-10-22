"""R64 focal source lookup, at most eight scientific sources; no source execution."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import uuid

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent.parent
ORDER = OUT.parent
REF = Path(r"C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json")


def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}


def save(name, obj):
    p = ROOT / name
    assert p.parent == ROOT and not p.exists(), p
    data = ((obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False, indent=2)) + "\n").encode("utf8")
    temp = p.with_name(p.name + ".tmp_" + uuid.uuid4().hex)
    with temp.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    assert temp.read_bytes() == data
    os.rename(temp, p)
    return pin(p)


def main():
    r58 = OUT / "acervo_r58/rede/FOCUSED_SEARCH_R2.json"
    index = json.loads(r58.read_text(encoding="utf8"))
    r63 = OUT / "physical_receiver_r63/sources/SOURCE_PINS_AND_ANCHORS_R1.json"
    old = json.loads(r63.read_text(encoding="utf8"))
    known = {s["path"]: s["sha256"] for s in old["sources"]}
    known.update({s["path"]: s["sha256"] for s in index["source_pins"]})
    files = {
        "Custo": (Path(r"C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py"), [(5644, 5656), (12882, 12893)]),
        "graviton": (Path(r"C:\IALD\papers_latex\graviton_paper\graviton_paper.tex"), [(202, 216), (347, 368), (464, 475)]),
        "appendices": (Path(r"C:\IALD\papers_latex\graviton_paper_english_v2\graviton_appendices.tex"), [(236, 257), (311, 331)]),
        "patent": (Path(r"C:\IALD\Central de Patentes\Patentes\PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex"), [(338, 370), (474, 516)]),
        "finite": (ORDER / "F1.REDE/finite_device/run_finite_device.py", [(101, 127), (163, 186), (200, 206)]),
        "R57": (OUT / "device_clock_r57/DERIVACAO_R57.md", [(28, 49), (160, 199), (203, 221)]),
        "R7": (ORDER / "F1.TEMPO.LEITURA_20261015/DISPOSITIVO_E_ESPECTRO_R7/CONTRATO_DISPOSITIVO_E_LEI_RAIZ_R7.txt", [(44, 90)]),
        "cascade": (Path(r"C:\IALD\Artigo\BANCADA_TOE\kernel_bancada\TheCascadeOfObservers.lean"), [(50, 62), (67, 85), (94, 108)]),
    }
    assert len(files) == 8
    patterns = {
        "output_temporal": r"\bQRT\b|quantum.?regression|regress[aã]o.qu[aâ]ntica|two.time|dois.tempos|Langevin|Hudson|Parthasarathy|input.{0,15}output|output.{0,15}field|temporal.{0,8}mode|modo.{0,8}temporal|\bb(?:_|\\|\s|\{).{0,20}out",
        "dilation_cascade": r"Stinespring|dilatation|dilation|dilata[çc][aã]o|cascad|campo.coletado|campo.de.sa[ií]da",
    }
    compiled = {k: re.compile(v, re.I) for k, v in patterns.items()}
    rows = []
    for name, (path, ranges) in files.items():
        p = pin(path)
        assert known.get(str(path)) == p["sha256"], (name, "pin absent or drifted")
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        for a, b in ranges:
            assert 1 <= a <= b <= len(lines)
        hits = {k: [{"line": i, "text": line} for i, line in enumerate(lines, 1) if rx.search(line)] for k, rx in compiled.items()}
        rows.append({"id": name, **p, "matches_prior_pin": True, "line_count": len(lines), "hits": hits,
                     "anchors": [{"first": a, "last": b, "text": "\n".join(f"{i}: {lines[i-1]}" for i in range(a, b+1))} for a, b in ranges]})
    navigation_hits = [s for s in index["source_pins"] if re.search(r"Langevin|Hudson|Parthasarathy|input.?output|regression|cascad|quantum.?noise|open.?system|stochast|campo.?saida|output.?field", s["path"], re.I)]
    source_receipt = save("FOCAL_SOURCE_PINS_R1.json", {"kind": "R64_EIGHT_SOURCE_LOOKUP", "sources": rows, "patterns": patterns,
        "navigation_only": [{**pin(r58), "named_candidates": navigation_hits, "scope": "Cached5423-source filename catalogue and157 stored lexical hit groups were inspected; source corpus was not rescanned. Its old search pattern was not an output-field completeness search."}, pin(r63)],
        "coverage": {"scientific_sources": len(rows), "total_lines": sum(s["line_count"] for s in rows), "total_bytes": sum(s["bytes"] for s in rows), "primary_and_derived_source_text_only": True, "no_universal_absence_claim": True}})
    channels = [
        {"id": "in_loss", "source_pair": "(kappa_in, a_i)", "collapse": "sqrt(kappa_in) a_i", "role": "Input-labelled internal mode loss", "rotating_transform": "exp(-i omega_d t) L_i"},
        {"id": "out_loss", "source_pair": "(kappa_out, a_o)", "collapse": "sqrt(kappa_out) a_o", "role": "Output-labelled internal mode loss", "rotating_transform": "exp(-i omega_d t) L_o"},
        {"id": "OH_relaxation", "source_pair": "(gamma_OH, sigma_minus)", "collapse": "sqrt(gamma_OH) sigma_minus", "role": "OH relaxation", "rotating_transform": "exp(-i omega_d t) L_OH"},
        {"id": "OH_dephasing", "source_pair": "(gamma_dephasing, Z_OH)", "collapse": "sqrt(gamma_dephasing) Z_OH", "role": "OH dephasing; off-diagonal damping2*gamma_dephasing under D[Z]", "rotating_transform": "unchanged"},
        {"id": "holographic", "source_pair": "(beta*gamma_Lambda, J)", "collapse": "sqrt(lambda) (a_o_dagger sigma_minus + sigma_plus a_i), lambda=beta*gamma_Lambda", "role": "Joint holographic channel", "rotating_transform": "unchanged"},
    ]
    findings = [
        {"id": "R64-01", "classification": "EXISTE_GERADOR_NAO_DILATACAO", "anchors": ["finite:101-114", "finite:163-186", "finite:201-206"], "statement": "Full64x64 finite GKLS and exp(tL) already exist. Collapse representation fixes five weighted system channels; implementation does not construct exterior bosonic fields, a joint system-bath unitary, measured output algebra or temporal wave packets."},
        {"id": "R64-02", "classification": "EXISTE_RESPOSTA_CAUSAL_CONDICIONAL", "anchors": ["R7:44-80"], "statement": "R7 contains microwave-source B(rho)=-i[sigma_x,rho], count detector Cdet*n_o, Duhamel kernel and resolvent. This is causal linear response about assumed stationary rho_star, not a QRT formula for output-field correlations, not a bath dilation, and not a chosen temporal mode."},
        {"id": "R64-03", "classification": "EXISTE_QUADRO_CONDICIONAL", "anchors": ["R57:160-199"], "statement": "Under LAB_PHASE_LOCKED_DRIVE, R(t)=exp(i omega_d t N_total) changes absolute frequencies to detunings, while jump phases cancel in D[L]. R57 explicitly says the patent did not specify that frame. A detector or exterior LO must be transformed as well; phase cancellation of dissipators does not make the readout phase disappear."},
        {"id": "R64-04", "classification": "EXISTEM_INGREDIENTES_RECEPTOR", "anchors": ["graviton:347-368", "graviton:464-475", "appendices:311-331", "patent:474-516"], "statement": "Loss amplitude sqrt(kappa)a, homodyneLO, heterodyne/HBT and multiplicative G_OH are written. They do not by themselves specify b_out, bath input, shot-noise normalization, time ordering, a filter or operator-valued output distribution."},
        {"id": "R64-05", "classification": "HOMONIMOS_DESCARTADOS_POR_LEITURA", "anchors": ["cascade:50-85", "Custo:5644-5656", "Custo:12882-12893", "R7:82-90"], "statement": "TheCascadeOfObservers defines a successor relation on four labelled levels, with its own explicit ONTO scope; it is not cascaded optical systems. Custo's Lindblad cascade concerns weight-matrix fractalisation/registration, not the device bath. Patent temporal dilation is metric time dilation. R7 merely allows future reduction/dilation after proving a narrow unitality obstruction; it does not construct one."},
        {"id": "R64-06", "classification": "NAO_LOCALIZADO_NA_COBERTURA", "anchors": ["FOCAL_SOURCE_PINS_R1.json"], "statement": "No ready input-output/QRT/Hudson-Parthasarathy/Langevin or temporal-mode implementation located in these eight texts and checked R58 index candidates. Lexical non-hits are not proof about all IALD. This report does not certify mathematical absence or forbid another implementation elsewhere."},
    ]
    report = {"kind": "R64_OUTPUT_FIELD_FOCAL_SOURCE_SURVEY", "author": "codex-output-sources-r64", "status": "DECLARADO_PENDING_INDEPENDENT_REVIEW", "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "mission_reference": pin(REF), "source_manifest": source_receipt,
        "five_channels": channels, "channel_anchors": ["finite:167-172", "finite:184-186", "R57:175-186"],
        "frame_hypothesis": "LAB_PHASE_LOCKED_DRIVE: h_lab(t)=h0+OmegaR(exp(-i omega_d t)sigma_plus+exp(i omega_d t)sigma_minus); R=exp(i omega_d t Ntotal), rho_rot=R rho_lab R_dagger. This is extra named modeling inR57, not hidden reinterpretation of patent absolute frequencies.",
        "findings": findings,
        "next_step": "Reuse H, five collapse operators and full semigroup; construct only the named output dilation/readout contract. State bath input (e.g. independent vacuum only as explicit hypothesis), scattering/port assignment, monitored fractions, LO phase and temporal test functions; justify conditional two-time regression and distributional shot-noise term. A GKLS representation alone does not uniquely identify physical output channels. No need to rebuildL64.",
        "requirement_satisfied": False, "execution": {"tests": 0, "simulations": 0, "builds": 0, "providers": 0, "source_imports": 0, "observed_data": False, "originals_modified": False, "memory_board_mission_mutations": False}}
    save("OUTPUT_FIELD_SOURCE_REPORT_R1.json", report)
    save("OUTPUT_FIELD_SOURCE_REPORT_R1.txt", """R64 — campo exterior: busca focal em oito fontes
DECLARADO; revisão independente pendente. R4 integral permanece aberto.
1. Gerador completo, cinco canais e exp(tL) já implementados emfinite_device:101–114,163–186,201–206. Não reconstruirL64.
2. Canais: sqrt(ki)ai; sqrt(ko)ao; sqrt(gammaOH)sigma-; sqrt(gammaPhi)ZOH; sqrt(lambda)(ao†sigma-+sigma+ai), lambda=beta*gammaLambda. D[Z] amortece offdiagonal a2gammaPhi. Código armazena pares(taxa,operador), sem raiz duplicada.
3. R7:44–80 já contém resposta causal/resolvente micro-ondas→contagem para estado estacionário assumido. Não é QRT/correlação do campo exterior nem dilatação.
4. R57:160–199 dá quadro girante sob LAB_PHASE_LOCKED_DRIVE. Três abaixadores recebem e^(-iomega_dt); Z eJ invariantes; fases cancelam nos dissipadores. Observável/LO ainda devem acompanhar o quadro. Patente original usa frequências absolutas.
5. Perda sqrt(kappa)a e homódino/heteródino/HBT existem; não identificam por si campo coletado, vácuo incidente, termo delta de shotnoise, filtros ou modos temporais.
6. Homônimos conferidos: TheCascadeOfObservers é relação de quatro níveis; Lindblad cascade doCusto trata de fractalização de matrizes de pesos. Nenhum fornece cascata óptica. R7 menciona dilatação futura, não a constrói.
7. Não localizada implementação pronta input-output/QRT/HP/Langevin/modo temporal nas oito fontes e candidatos do índiceR58 consultados. Não é ausência universal; índice antigo foi usado só para navegação e não recobria lexicalmente todo esse alvo.
8. Próximo elo: construir contrato de dilatação/saída com bath, portos, faseLO, frações monitoradas e funções temporais explícitos; reutilizar o gerador completo. Independência/vácuo dos baths e identificação física não vêm automaticamente do GKLS.
Fonte+linhas+hashes: FOCAL_SOURCE_PINS_R1.json. Nenhum teste/simulação/build/provedor/import de modelo/dado observado/mutação de originais ou memória.
""")
    request = {"operation": "project", "reference": str(REF), "max_chars": 400000}
    proc = subprocess.run([r"C:\Python314\python.exe", "-B", "-X", "utf8", r"C:\IALD\MEMORIA_IALD\mission_cli.py"], input=json.dumps(request), text=True, encoding="utf8", capture_output=True)
    response = json.loads(proc.stdout)
    assert proc.returncode == 0 and response["ok"]
    save("PROJECT_RETURN_R1.json", {"request": request, "response": response, "exit_code": proc.returncode, "stderr": proc.stderr})
    for s in rows:
        assert pin(s["path"])["sha256"] == s["sha256"]
    names = ["build_report_r1.py", "OUTPUT_FIELD_SOURCE_REPORT_R1.json", "OUTPUT_FIELD_SOURCE_REPORT_R1.txt", "FOCAL_SOURCE_PINS_R1.json", "PROJECT_START_R1.json", "PROJECT_RETURN_R1.json"]
    delivery = save("DELIVERY_R1.json", {"kind": "R64_FOCAL_SOURCES_DELIVERY", "author": report["author"], "status": report["status"], "mission_reference": pin(REF), "revision_final": response["result"]["receipt"]["revision"], "files": [pin(ROOT/n) for n in names], "scientific_sources": 8, "source_hashes_rechecked": True, "findings": len(findings), "requirement_satisfied": False, "execution": report["execution"]})
    print(json.dumps({"delivery": delivery, "sources": 8, "findings": len(findings), "revision": response["result"]["receipt"]["revision"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
