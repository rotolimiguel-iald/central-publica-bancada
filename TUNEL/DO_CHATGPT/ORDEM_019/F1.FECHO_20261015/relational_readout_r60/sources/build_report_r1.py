"""R60 documentary survey over an explicit scientific allowlist; no execution of sources."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import re
import uuid

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent.parent
REFERENCE = Path(r"C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json")


def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}


def save_new(name, obj):
    p = ROOT / name
    assert p.parent.resolve() == ROOT
    if p.exists():
        raise FileExistsError(p)
    b = ((obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False, indent=2)) + "\n").encode("utf-8")
    temp = p.with_name(p.name + ".tmp_" + uuid.uuid4().hex)
    with temp.open("xb") as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    assert temp.read_bytes() == b
    os.rename(temp, p)
    return pin(p)


def main():
    previous = OUT / "acervo_r58/rede/REDE_CONTINUO_REPORT_R1.json"
    old = json.loads(previous.read_text(encoding="utf8"))
    selected = ["squeezed", "tratado", "custo", "ponte", "um_artigo", "state067", "fock073", "diamond", "bancada_index", "q6", "contract"]
    paths = {key: Path(old["sources"][key]["path"]) for key in selected}
    paths["graviton_appendices"] = Path(r"C:\IALD\papers_latex\graviton_paper_english_v2\graviton_appendices.tex")
    tratado = Path(r"C:\IALD\Artigo\Tratado")
    for key, name in {
        "tratado_main": "tratado_tgl.tex", "tratado_foundation": "secao_01_fundamentos.tex",
        "tratado_cosmology": "secao_02_cosmologia.tex", "tratado_waves": "secao_04_ondas_gravitacionais.tex",
        "tratado_information": "secao_05_informacao.tex", "tratado_recursion": "secao_06_luz_recursao.tex",
        "tratado_validation": "secao_08_validacao.tex", "tratado_technology": "secao_09_tecnologia.tex",
        "tratado_appendices": "apendices.tex",
    }.items():
        paths[key] = tratado / name
    patterns = {
        "beta_labels": r"beta|bTGL",
        "alpha2_historical": r"alpha_2|alpha_\{2\}|alpha2",
        "alpha_squared": r"alpha\^\{?2|alpha\*\*2",
        "pair_quadrature": r"squeez|comprimid|quadratur|homody|homód|condensad.{0,20}par",
        "phase_reflection": r"phase|fase|reflex|reflect|varphi|theta_R|theta_T",
        "hyperbolic_beta_nearby": r"(?:tanh|atanh|sinh|cosh|squeez).{0,150}(?:beta|bTGL)|(?:beta|bTGL).{0,150}(?:tanh|atanh|sinh|cosh|squeez)",
    }
    regex = {k: re.compile(v, re.I) for k, v in patterns.items()}
    ranges = {
        "squeezed": [(202, 216), (239, 260), (713, 725)],
        "graviton_appendices": [(110, 140), (311, 333)],
        "tratado": [(112, 137), (168, 173), (228, 239), (630, 635)],
        "tratado_foundation": [(599, 612), (627, 657)],
        "tratado_recursion": [(87, 98)],
        "tratado_appendices": [(68, 75)],
        "custo": [(11557, 11599), (12105, 12112), (19356, 19369), (19426, 19449), (19466, 19477)],
        "ponte": [(666, 731)],
        "um_artigo": [(149, 149), (165, 181), (1288, 1288)],
    }
    rows = []
    for key, path in paths.items():
        p = pin(path)
        text = path.read_bytes().decode("utf-8-sig")
        lines = text.splitlines()
        hits = []
        counts = {k: 0 for k in regex}
        for number, line in enumerate(lines, 1):
            found = [k for k, expr in regex.items() if expr.search(line)]
            if found:
                for k in found:
                    counts[k] += 1
                hits.append({"line": number, "categories": found, "text": line})
        anchors = []
        for first, last in ranges.get(key, []):
            assert 1 <= first <= last <= len(lines)
            anchors.append({"first": first, "last": last,
                            "text": "\n".join(f"{i}: {lines[i-1]}" for i in range(first, last+1))})
        prior = old["sources"].get(key)
        if prior:
            assert prior["sha256"] == p["sha256"], (key, "R58 source drift")
        rows.append({"id": key, **p, "line_count": len(lines), "counts": counts,
                     "semantic_read_ranges": ranges.get(key, []), "anchors": anchors,
                     "lexical_hits": hits, "matches_R58_pin": True if prior else None})
    coverage = {
        "files": len(rows), "bytes": sum(x["bytes"] for x in rows),
        "lines": sum(x["line_count"] for x in rows),
        "lexical_hit_lines": sum(len(x["lexical_hits"]) for x in rows),
        "selected_R58_sources_rechecked": len(selected),
        "semantic_read_ranges": sum(len(x["anchors"]) for x in rows),
        "method": "Explicit allowlist. Lexical whole-file scan plus semantic reading of recorded ranges; no new broad crawl.",
        "limits": ["Corpus is not all of C:\\IALD; negative findings are coverage-limited.",
                   "Tratado scientific sections01-06,08-09,main and appendices; prolegomena, consciousness, ethics/legal and conclusion not rescanned.",
                   "Existing paper source read as bytes only; tgl_paper_unified.py was never imported or run.",
                   "No DOCX/PDF re-extraction, no observed data, tests, dynamics, providers or Lean builds.",
                   "Historical source labels and statements are preserved; this report does not revalidate every historical theorem or numerical claim."]}
    sources = save_new("SOURCE_COVERAGE_R1.json", {"kind": "R60_EXPLICIT_DOCUMENTARY_COVERAGE", "previous_R58": pin(previous), "patterns": patterns, "coverage": coverage, "sources": rows})
    findings = [
        {"id": "R60-01", "classification": "EXISTE_LIGADO_DOCUMENTAL", "anchors": ["ponte:711-729", "custo:19426-19449"],
         "relation": "Boundary passive matrix on H_obs (+) H_hid: [[sqrt(1-beta)e^(i theta_T),sqrt(beta)e^(i theta_R)],[-sqrt(beta)e^(-i theta_R),sqrt(1-beta)e^(-i theta_T)]], with beta=|R|^2=sin^2(theta_M).",
         "status_exact": "Source explicitly conditional: REAL dado |R|^2=beta; finite-to-gravitational-boundary transfer remains CONJECTURE. Unitarity fixes the sum, not the chosen value beta by itself.",
         "limit": "The relation b=beta exists in the written architecture. It does not prove physical access to both hidden/observable input and output channels, nor identify the device realization of this matrix."},
        {"id": "R60-02", "classification": "EXISTE_LIGADO_DOCUMENTAL", "anchors": ["custo:11557-11599", "tratado_foundation:637-657"],
         "relation": "<P_2D>_(rho*)=beta and <Q>_(rho*)=1-beta; theta_M=arcsin(sqrt(beta)).",
         "status_exact": "The source says beta is primary and the angle is derived; sin^2+cos^2=1 alone is normalization, not a derivation of beta.",
         "limit": "No identification P_2D with the actual pair number/quadrature observable or detector POVM is supplied in these passages."},
        {"id": "R60-03", "classification": "EXISTE_NAO_IDENTIFICADO_AO_SQUEEZE", "anchors": ["um_artigo:149", "um_artigo:165-181", "um_artigo:1288"],
         "relation": "alpha=sech(chi/2), q=tanh(chi/2), q^2+alpha^2=1; beta=sqrt(e)alpha; a separate SO(2) coefficient transport relates EM and gravitational matrices.",
         "status_exact": "The later caveat at1288 marks alpha_obs=sech as ONTO and keeps CODATA as INPUT. The source describes coefficient transport, not alpha-free derivation.",
         "limit": "chi, q and the two-face transmission model are not identified with rho or the bosonic pair number distribution of R59. Repeated hyperbolic functions do not establish equality of objects."},
        {"id": "R60-04", "classification": "DISTINCAO_DE_NOTACAO", "anchors": ["squeezed:713-725", "tratado:168-173", "tratado:630-635", "custo:12105-12112"],
         "relation": "beta_halo~2-3 is the halo slope; beta_C=1/T_C and beta=1/(k_B T) are thermal; beta_2=1 is a Betti number; historical alpha_2 is declared renamed beta_TGL.",
         "status_exact": "The historical alpha_2 subscript is not alpha^2, the squared fine-structure constant. beta_TGL is alpha_FINE_CODATA_2018*sqrt(e) in the adopted runtime convention.",
         "limit": "No literal local beta or shared Greek letter transfers its value to beta_TGL. Historical naming statement located, not a newly proved physical identification."},
        {"id": "R60-05", "classification": "EXISTE_LEITURA_RELACIONAL", "anchors": ["graviton_appendices:110-133", "graviton_appendices:311-333", "squeezed:250-260"],
         "relation": "Two-mode squeezed state, normalized quadratures, homodyne tomography with phase-locked adjustable local oscillator and phase scan are explicitly prescribed.",
         "status_exact": "Documentary preparation/readout protocol and prediction, not evidence it was performed. This directly supports relative pair/quadrature reading even when linear means vanish.",
         "limit": "The tomography section reconstructs rho_ss/Name subspace. It supplies no equality between recovered squeezing parameters and beta_TGL."},
        {"id": "R60-06", "classification": "DIVERGENCIA_MATERIAL_LOCALIZADA", "anchors": ["graviton_appendices:121-139", "R59:DERIVATION_R1.txt sections4-5"],
         "relation": "Appendix133 gives Var(Xi-Xj)=exp(-2r) but Var(Pi+Pj)=exp(+2r);139 assigns uncertainty bound>=1/2 to that EPR pair.",
         "status_exact": "For the written S and aligned phase, R59 gives both variances exp(-2r). Xi-Xj and Pi+Pj commute. The source also mixes variances and standard deviations in139.",
         "limit": "This mismatch is an erratum candidate beside the source, not removal of the squeezed state or tomography route. No source edited and no new test round."},
        {"id": "R60-07", "classification": "DIVERGENCIA_DE_CONVENCAO_PRESERVADA", "anchors": ["squeezed:252", "graviton_appendices:121", "tratado:236-239", "R59:DERIVATION_R1.txt sections1,5"],
         "relation": "Graviton coefficient rho=r; Tratado coefficient rho=r/2; same aligned dimensionless variance exp(-2rho) is exp(-r) in the latter.",
         "status_exact": "R59 already derived this; the two written r symbols cannot be equated without conversion.",
         "limit": "Neither convention supplies rho(beta), phi(beta) or a calibration of physical units."},
        {"id": "R60-08", "classification": "DERIVED_REUSE_NOT_NEW_DYNAMICS", "anchors": ["R59:DERIVATION_R1.txt sections4,6,8"],
         "relation": "Within the pure squeezed family: rho_eff=asinh(sqrt(n))=asinh(2|m|)/2, phi=arg(m), consistency |m|^2=n(n+1); phi unidentifiable at rho=0.",
         "status_exact": "State tomography relative to quadrature phase reference, not a derivation of rho(beta), theory fitting, or a measurement performed here.",
         "limit": "A mixed state can fail the pure equality; phase reconstruction alone does not identify the preparation/model. No rho=atanh(sqrt(beta)) is inferred."},
        {"id": "R60-09", "classification": "DISTINCAO_DE_OPERADORES", "anchors": ["ponte:675-709", "ponte:711-729", "squeezed:252", "R59:DERIVATION_R1.txt section8"],
         "relation": "Passive angular matrix mixes annihilation modes linearly and preserves number; active squeezing mixes annihilation and creation hyperbolically. Tomita S=J Delta^(1/2), modular cocycle and scattering S are separately typed in the source.",
         "status_exact": "R59 supplies real symplectic Bogoliubov map k_rho, not a complex one-particle unitary. Shared letter S or identities involving tanh/sech do not identify these operators.",
         "limit": "Even an eventual composition of active preparation with passive readout needs the actual channel map and admissible states; neither beta alone nor unitarity fixes the source squeeze."},
        {"id": "R60-10", "classification": "NAO_LOCALIZADO_NA_COBERTURA", "anchors": ["SOURCE_COVERAGE_R1.json", "ponte:712-729", "custo:19443-19449"],
         "relation": "No explicit physical equation relating the R59 covariance (n,m or rho,phi) to the particular beta_TGL reflection channel was located in the scanned sources.",
         "status_exact": "There IS a documentary reflection/projection relation with beta. What remains is its identification with this pair, this preparation and physically accessible observables.",
         "limit": "No universal absence claim. R5 remains open; no R4 dynamics, recovery, reset or acceptance attempted."},
    ]
    report = {
        "kind": "R60_RELATIONAL_BETA_DOCUMENTARY_SURVEY", "author": "codex-relational-sources-r60",
        "status": "DECLARADO_PENDING_INDEPENDENT_REVIEW", "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "mission_reference": pin(REFERENCE), "requirement": "R5", "requirement_satisfied": False,
        "coverage": coverage, "source_manifest": sources,
        "reuse_R59": [pin(OUT / "pair_covariance_r59/squeezing" / n) for n in ("DERIVATION_R1.txt", "SYMBOLIC_RESULTS_R1.json", "DELIVERY_R1.json")],
        "findings": findings,
        "precise_residual": "Identify, from the same device modes and state preparation, the actual observable/POVM implementing the obs/hidden reflection readout, its input/output access and normalization, and prove its value equals the source beta_TGL. Do not assume beta=n/(n+1), rho=atanh(sqrt(beta)), chi/2=rho or equal scattering/squeezing phases. Refinement, dynamics and Maxwell/H1 identification remain distinct R5 obligations.",
        "execution": {"source_execution": False, "new_math_or_dynamics": False, "tests": 0, "providers": 0, "builds": 0, "observed_data": False, "original_modifications": False, "memory_or_mission_mutations": False, "R4_actions": False},
    }
    rp = save_new("RELATIONAL_BETA_REPORT_R1.json", report)
    txt = """R60 — LEITURA RELACIONAL DE BETA; LEVANTAMENTO DOCUMENTAL R5
DECLARADO, revisão independente pendente; requisito R5 integral permanece aberto.

1. A ponte documental existe. Ponte:711–729 e Custo:19426–19449 escrevem a matriz passiva de fronteira em H_obs⊕H_hid com |R|²=beta=sin²(theta_M). Custo19443 explicita: REAL dado |R|²=beta; transporte finito→fronteira gravitacional CONJECTURE. Unitariedade fixa a soma reflexão+transmissão; não seleciona beta sozinha. O texto não demonstra acesso físico às duas entradas/saídas, particularmente ao canal oculto.
2. Custo:11557–11599 atribui <P_2D>_(rho*)=beta e deriva o ângulo de beta, declarando que a identidade pitagórica não deriva o acoplamento. Falta identificar esse projetor com observável/POVM efetivo da leitura de pares. Não é ausência de toda relação com beta.
3. Um:149,165–181 fornece alpha=sech(chi/2), q=tanh(chi/2), beta=sqrt(e)alpha e transporte de coeficiente entre matrizesSO(2). A ressalva1288 preserva alpha_obs=sech como ONTO e CODATA como INPUT. Não identifica chi/2 com o squeeze rho de R59 nem q com distribuição de ocupação bosônica.
4. As notações têm tipos diferentes: beta do halo≈2–3 em graviton:715–725; beta térmico=1/(k_B T), beta_C=1/T_C; beta_2 de Betti; alpha_2 histórico explicitamente renomeado beta_TGL em Custo:12105–12112. Alpha_2 não é alpha². Beta_TGL conserva alpha_FINE_CODATA_2018*sqrt(e), sem literal novo.
5. O apêndice110–133 prescreve S squeezed e quadraturas;311–333 já descreve homodinagem com oscilador local travado em fase e varreduraLO. É rota documental de tomografia, não medição realizada. A média linear zero não elimina a fase de m=<ab>.
6. Achado ao lado: apêndice133 dá e^{-2r} para X_i−X_j e e^{+2r} para P_i+P_j. R59, com o mesmo S e fase alinhada, dá e^{-2r} para ambos; o par EPR comuta. O limite≥1/2 e a multiplicação de desvios/variâncias na139 não seguem dessas definições. Original preservado; sem nova bateria de testes.
7. A convenção do Tratado:236 usa r/2 e a239 mantém e^{-2r}; R59 demonstra e^{-r} para a mesma variância alinhada. Esta diferença já está custodiada; não serve para fixar rho(beta).
8. R59 permite reconstruir rho_eff=asinh(sqrt(n)) e phi=arg(m), com consistência pura |m|²=n(n+1); rho=0 não identifica fase. Isto é tomografia do estado, não derivação rho(beta), ajuste da teoria ou inferência rho=atanh(sqrt(beta)).
9. Preservar as categorias: S angular/passivo, S de squeezing ativo hiperbólico, S de Tomita e espalhamento do cociclo são objetos diferentes. A fonte já separa os três últimos papéis modulares em Ponte675–709; R59 fornece o mapa real simplético do squeeze. A fase de preparação não é automaticamente theta_R ou theta_T de espalhamento.
10. Resíduo localizado: mapear preparação e observáveis das mesmas cavidades à leitura obs/hid de reflexão, com acesso, unidades e normalização; demonstrar a igualdade dessa leitura com beta_TGL. Identificação com Maxwell/H1, refinamentos e dinâmica continuam obrigações próprias. Nenhuma ausência universal é afirmada.

Cobertura e pinos exatos: SOURCE_COVERAGE_R1.json. Consulta por lista explícita das fontesR58, apêndice solicitado e seções científicas do Tratado; fontes Python apenas texto. Zero novas provas dinâmicas, testes, builds, provedores, dados observados, mudanças de originais/memórias/ACOM e ações em R4.
"""
    tp = save_new("RELATIONAL_BETA_REPORT_R1.txt", txt)
    print(json.dumps({"report": rp, "text": tp, "sources": sources, "coverage": coverage}, ensure_ascii=False))


if __name__ == "__main__":
    main()
