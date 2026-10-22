"""Assemble new F1.ATRATOR evidence; never overwrite registered artifacts."""
from pathlib import Path
import datetime
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent


def load(relative):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def pin(path):
    path = Path(path)
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def new(path, data):
    data = data.encode("utf-8") if isinstance(data, str) else data
    with path.open("xb") as stream:
        stream.write(data)
    assert path.read_bytes() == data


def main():
    outputs = [BASE / name for name in ("RELATORIO_F1_ATRATOR_R1.md", "RESULTADO_F1_ATRATOR_R1.json")]
    assert all(not path.exists() for path in outputs), "Existing delivery; use a new revision"
    numeric = load("numerical/RESULTADOS_NUMERICOS_R3.json")
    formal = load("lean_candidate/FINAL_LEAN_RECEIPT_R1.json")
    optical = load("lean_optical_bridge/FINAL_OPTICAL_RECEIPT_R1.json")
    assert (BASE / "review/REVISAO_LEAN_R1.json").is_file()
    assert (BASE / "review/REVISAO_LEAN_R1.md").is_file()
    review = load("review/REVISAO_LEAN_R1.json")
    assert review["verdict"] == "PASSA" and not review["material_findings"]
    assert review["olean_equality_main"] and review["olean_equality_optical"]
    assert numeric["all_expected_outcomes_met"]
    assert formal["build"]["exit_code"] == optical["build"]["exit_code"] == 0
    for receipt in (formal, optical):
        for item in receipt["artifacts"]:
            assert pin(item["path"])["sha256"] == item["sha256"], item["path"]
    sources = []
    for item in load("PREREGISTRO_R1.json")["source_pins"]:
        current = pin(item["path"])
        assert current["sha256"] == item["sha256"], item["path"]
        sources.append(current)
    for source in ("lean_candidate/TheSingularityReadsTheAttractor.lean", "lean_optical_bridge/OpticalPopulationBridgeR2.lean"):
        assert not re.search(r"\b(sorry|admit|axiom)\b", (BASE / source).read_text(encoding="utf-8"))
    pop = numeric["models"]["primary_population"]
    density = numeric["models"]["primary_density"]
    theorem_total = formal["printed_count"] + optical["theorems_checked"]
    report = f"""# F1.ATRATOR — entrega R1

Autor: codex-gerente-tgl, sob reivindicação 664. Data: 10/10/2026. Entrega técnica para auditoria da c1; AUDITADA/FECHADA são atos da gerência.

## Resultado

**A1–A4 PASSAM no sistema e nas hipóteses especificadas.** [REAL — ensaio e compilação; DERIVED — interpretação matemática]. A cunhagem do operador permanece [ONTO]. Nenhuma creditação física é inferida.

| Item | Ensaio primário | Termo Lean e alcance |
|---|---|---|
| A1 | PASSA em populações e densidades | `A1_cesaro`: Hilbert completo e norma(T)≤1 dão convergência das médias. `A1_face_orbit`: potências convergem na família P+λ(I−P), sob norma(λ)<1. |
| A2 | PASSA: RT=TR=R | `A2_reading_stationary`, com R definido como starProjection de Fix(T); norma(T)≤1 para RT=R. |
| A3 | PASSA: projeção espectral, idempotência e letra | `A3_reading_idempotent`, `A3_reading_is_fixed_space_projection`, `A3_normalized_letter` e `A3_letter_exists_finite`. |
| A4 | PASSA: dimensão fixa 1 | `StrictComplementContraction`: e≠0, Te=e e contração estrita no complemento ortogonal de span(e). `A4_fixedSpace_eq_span` e `A4_dimension_one`. |

Não vacuidade: o núcleo formal exibe e=(1,0) em ℂ² e λ=1/2, uma testemunha exata da hipótese. A família formal é paramétrica; esse 1/2 não substitui β. No ensaio, os estados fixos normalizados são p=(1/2,1/2) e ρ=I/2. Um subespaço fixo de dimensão 1 ainda contém todos os múltiplos do vetor; a unicidade do estado requer soma/traço 1.

## Levantamento reaproveitado

O mapa foi consultado antes da construção (MAPA_LEVANTAMENTO.json); o pré-registro entrou na rota `formal.singularidade_le_atrator`, seq 1000. F1.ATRATOR ainda não estava no índice Nós Vivo: `NOS_CONSULTA_RECIBO_R1.json` conserva stdout, stderr e exit1. A consulta vazia não foi tratada como prova de ausência de material.

- SMatrix: matriz angular unitária, reflexão −sinθ e peso sin²θ; inventário da Bancada relaciona o peso a β.
- GlobalLiftLadder: dephasing conjugado e sua convergência; reutilizado como controle com dois modos fixos.
- TheAxiomAndTheFalseWitness: fluxo P+exp(−t)(I−P) já construído.
- ExactWitness e WordExistence: projeção e palavra aniquiladora normalizada; TheObserverReadsTheAngle: `observing_adds_nothing`.
- Mathlib `Analysis/InnerProductSpace/MeanErgodic.lean:96`: teorema ergódico médio já existente.
- GKLS v384/v385: resultados arquivados T2 672/672, T4 21100/21100 e controles degenerados, apenas relidos. Não foram repetidos nem convertidos em um teorema geral sobre saltos não comutantes.

Hashes e linhas estão em `source_survey/FONTES_R1.json` e `lean_survey/SOURCE_HASHES_R1.json`. PALAVRA foi encontrada como candidata no work, não como módulo instalado no kernel consultado. A ligação usa os teoremas existentes ExactWitness/WordExistence; o nome PALAVRA não cria uma importação inexistente.

## Canal e duas leituras

β=ALPHA_FINE_CODATA_2018·√e foi calculado em runtime: **{numeric['beta_runtime']:.18g}**. A constante foi extraída dos bytes pinados do um.py sem executar o programa. A linha está no módulo embutido, conferida contra a constante selada da AST externa.

S=[[√(1−β),√β],[−√β,√(1−β)]]. O sistema aberto adotado explicitamente é C=D∘Ad(S)∘D, com dephasing completo antes/depois de cada espalhamento. Nas populações, T=|S|²=R+λ(I−R), R=J/2 e λ=1−2β={numeric['lambda_runtime']:.16g}. A dissipação não é deduzida da unitariedade de S.

A ponte `OpticalPopulationBridgeR2.lean` prova a decomposição, RT/TR, R², a conjugação pela base soma/diferença com inversa explícita e o intervalo estrito de λ. A ponte matricial é exata; o transporte completo como equivalência de operadores contínuos de Hilbert não foi acrescentado ao tipo Lean. A correspondência de coordenadas está explicitada no complemento numérico e nas identidades matriciais.

A representação populacional T=exp[a(X−I)], a=−logλ/2, foi conferida. Ela é uma exponencial hiperbólica normalizada deste canal; não identifica todos os boosts canônicos. O canal completo C tem autovalores zero e não é anunciado como uma exponencial GKLS em tempo finito. θ permanece leitura angular fixa, sem limite angular solicitado.

Para a letra, A=I−T e q(z)=z−2β: R=q(A)/q(0), enquanto (Xq)(A)=0. Na face de densidades, q(z)=(z−1)(z−2β). A palavra completa Xq aniquila A; q aniquila seu complemento transitório. `observing_adds_nothing` fornece o padrão formal de releitura idempotente, sem identificar por homônimo P₊ angular e R dissipativo.

## Números e controles

Tolerância absoluta/relativa: 1e−10, fixada antes. Semente: 20261010; 258 populações e 260 densidades, além das verificações de operadores.

| Quantidade | Populações | Densidades |
|---|---:|---:|
| dim Fix(T) | {pop['fixed_dimension']} | {density['fixed_dimension']} |
| norma(T⁴⁰⁹⁶−R), float64 | {pop['powers'][-1]['distance_to_R']:.9g} | {density['powers'][-1]['distance_to_R']:.9g} |
| distância Cesàro, N=4096 | {pop['cesaro'][-1]['distance_to_R']:.12g} | {density['cesaro'][-1]['distance_to_R']:.12g} |

A cota exata λ⁴⁰⁹⁶ é aproximadamente 4,70e−44; o resíduo float64 mede o piso de arredondamento. Cesàro foi conferida pela fórmula/cota O(1/N), não por distância final 1e−10. A universalidade matemática decorre dos termos, não da amostragem finita.

| Controle | A1 | A2/A3 | A4 |
|---|---|---|---|
| T=I₂ | PASSA | PASSA | FALHA_SEM_HIPOTESE, dimensão 2 |
| Dephasing rotacionado sFrame | PASSA | PASSA | FALHA_SEM_HIPOTESE, dimensão 2 |
| x↦x+1 em ℝ | FALHA direta e Cesàro | Não aplicável | Não aplicável |

A translação é explicitamente externa à classe linear/CPTP finita, que possui ponto fixo. O runner R3 registra sua contraprova analítica; a revisão independente itera todos os 4097 valores e as médias, e a ponte Lean prova `affine_no_fixed`. `ADENDO_CONTROLE_AFIM_R1.json` registra que o agregador R3 não incluía um predicado numérico desse controle. O literal `probability_loss_per_step=0` é uma identidade esperada; os resíduos de preservação de traço foram medidos nos campos TP.

Nesta família, β determina a taxa de relaxação e não a projeção final. O resultado não discrimina valores de β por R sozinho.

## Compilação, revisão e custódia

Lean 4.31.0; Mathlib pinado; LEAN_PATH literal nos recibos, somente leitura no .lake do Nós. Candidata principal: EXIT0 em {formal['build']['seconds']:.3f}s, {formal['printed_count']} declarações impressas. Ponte: EXIT0 em {optical['build']['seconds']:.3f}s, {optical['theorems_checked']} declarações impressas. Total: {theorem_total} declarações impressas, só propext/Classical.choice/Quot.sound, zero sorry nos dois fontes aceitos. O principal contém {formal['theorem_count_source']} teoremas (as 14 impressas não são a contagem total de declarações).

`review/REVISAO_NUMERICA_R1` reproduz o cálculo sem importar o runner e em coordenadas diferentes. `review/REVISAO_LEAN_R1` contém revisão semântica e recompilação independente. Esses pareceres técnicos não substituem a auditoria da c1.

O pré-registro foi congelado às 13:08:19 UTC, antes de qualquer teste novo. R1/R2 numéricos recusaram antes das matrizes por escopo AST e CRLF; R3 corrigiu somente o leitor. Principal Lean tentativas001–003 e ponte001 falharam e estão preservadas com fontes/logs/recibos; somente as tentativas004/002 são aceitas. Logs inválidos podem conter sorryAx da recuperação de erros do elaborador; não são provas aceitas.

As 14 fontes pré-registradas foram relidas por hash antes/depois e na consolidação. Não se alterou um.py, kernel do Nós, Bancada de produção ou dado observado. Arquivos novos no túnel; memória sob reivindicação 664 com backups de bytes. Nenhum gate mudou. A integração no um.py permanece para o apanhado geral autorizado separadamente.
"""
    new(outputs[0], report)
    artifacts = []
    excluded = {path.name for path in outputs[1:]}
    for path in sorted(BASE.rglob("*")):
        assert not path.is_symlink(), f"Unexpected link: {path}"
        if path.is_file() and path.name not in excluded:
            assert "__pycache__" not in path.parts, path
            artifacts.append(pin(path))
    result = {
        "unit": "F1.ATRATOR", "author": "codex-gerente-tgl", "claim": 664,
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "verdict": "PASSA_NO_ESCOPO_MATEMATICO_PREREGISTRADO", "management_status_requested": "ENTREGUE",
        "claims": {key: {"population": pop["claims"][key], "density": density["claims"][key], "formal": "PASSA_CONDICIONAL"} for key in ("A1", "A2", "A3", "A4")},
        "controls": {name: value["claims"] for name, value in numeric["models"].items() if name not in ("primary_population", "primary_density")},
        "affine_control": numeric["no_fixed_affine"]["claims"],
        "formal_main": formal, "formal_optical": optical,
        "source_pins_rechecked": sources, "artifacts_at_delivery_preparation": artifacts,
        "ontology": "ONTO", "physical_sigma": None, "gate_changed": False,
        "integration": "NOT_INSTALLED; management/operator general bench consolidation",
        "scope_notes": ["Unique normalized state under named hypothesis", "No full Hilbert CLM transport from matrix coordinates claimed", "Float64 residual is not exact decay", "Affine control numerically checked by independent review", "AUDITADA/FECHADA reserved to c1"]
    }
    new(outputs[1], json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"result": pin(outputs[1]), "report": pin(outputs[0]), "artifact_count": len(artifacts)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
