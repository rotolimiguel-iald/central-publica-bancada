"""Write new F1.3 v3.2 evidence and map input without overwriting artifacts."""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path

UNIT = Path(__file__).resolve().parent
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F1.3")
MD = UNIT / "COMPLEMENTO_V3_2_ENUNCIADO_D1A3_20261008.md"
LEAN = UNIT / "ENUNCIADO_D1A3_BGL_V3_2_20261008.lean"
LOG = UNIT / "ENUNCIADO_D1A3_BGL_V3_2_20261008.build.log"
RESULT = UNIT / "RESULTADO_V3_2_ENUNCIADO_D1A3_20261008.json"
MAP = UNIT / "MAPA_F13_V3_2_ENUNCIADO_D1A3_20261008.json"


def art(path: Path) -> dict:
    data = path.read_bytes()
    return {"caminho": str(path), "sha256": sha256(data).hexdigest(), "bytes": len(data)}


def write_new(path: Path, value: dict) -> dict:
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert path.read_bytes() == data
    return art(path)


def main() -> None:
    if RESULT.exists() or MAP.exists():
        raise RuntimeError("v3.2 evidence already exists; do not overwrite")
    md = MD.read_text(encoding="utf-8")
    required = ("D1a3OutputBGL", "LightNetStandardWedgeDataBGL", "IsTomitaSquare", "ModularGroupIsBoost", "[OPEN]")
    if any(token not in md for token in required):
        raise RuntimeError("typed output or open obligation missing from v3.2 note")
    probe = AUDIT / "art_ad949e97" / "sandbox" / "F13v31_D1a3_bgl.lean"
    if LEAN.read_bytes() != probe.read_bytes():
        raise RuntimeError("Lean probe copy differs from c1 source")
    if art(LEAN)["sha256"] != "e4da9e865d00bdcb1c112fade347fe4a169e7e9d0e80227c81267861e6b9e540":
        raise RuntimeError("unexpected Lean probe hash")
    if art(LOG)["sha256"] != "551efbbb4210041e6f6580e7f519646c1617af8d2f3576b9337d555287eb0556":
        raise RuntimeError("unexpected c1 build log hash")
    backups = sorted(UNIT.glob(MD.name + ".bak_*"))
    if not backups:
        raise RuntimeError("byte backup of edited new MD missing")
    paths = [
        MD, LEAN, LOG, *backups,
        UNIT / "COMPLEMENTO_V3_1_FACTIBILIDADE_20261008.md",
        UNIT / "GRAFO_DEGRAUS_V3.md",
        AUDIT / "AUDITORIA_F1_3_C1_ad949e97.md",
        AUDIT / "AUDITORIA_F1_3_V3_C1_ab8cb3e7.md",
    ]
    artifacts = [art(p) for p in paths]
    result = {
        "schema": "iald.f1_3.v3_2_typed_D1a3.v1",
        "unit": "F1.3",
        "time_utc": datetime.now(timezone.utc).isoformat(),
        "status": "ENTREGUE_PARA_REAUDITORIA_C1",
        "existing_work": "v3.1 already supplies the mathlib table, Fubini L2 gap, genericTomita H1 references, EO/LRT and corrected inventory line range; c1 reaudited 1/4/5/6 as met, 3 partial, 2 unmet.",
        "v3_2_change": "Adopts c1 sandbox Lean type D1a3OutputBGL and LightNetStandardWedgeDataBGL as conditional output and typed operator-queue proposal; no kernel installation or inhabitant.",
        "semantic_boundary": "KWR is constructed from supplied SW data; Delta is a field uniquely characterized by the S-dagger-S graph, not a new def; ModularGroupIsBoost is a field for exp(it sigma) after Fourier and does not yet construct unbounded Delta^(it). Positivity and physical Fub/J/T/sigma remain OPEN.",
        "probe": {"lean": art(LEAN), "build_log": art(LOG), "axioms": ["propext", "Classical.choice", "Quot.sound"], "sorry": 0, "meaning": "conditional typechecking only"},
        "scope": {"new_MiMo_call": False, "other_provider_call": False, "kernel_changed": False, "um_py_changed": False, "gate_effect": "NONE", "operator_queue_edited": False},
        "artifacts": artifacts,
    }
    result_art = write_new(RESULT, result)
    entry = {
        "tipo": "ANOTACAO",
        "rota_id": "formal.f1_3.reconcile_v376_mathlib_plan",
        "dominio": "FORMAL",
        "titulo": "F1.3 v3.2: enunciado D1a.3 tipado a partir da sonda c1, sem habitante",
        "pergunta": "A saída D1a.3 e a proposta de fortalecer LightNetData podem ser escritas como tipos Lean no pin atual?",
        "dados": ["v3.1 já atende tabela mathlib, Fubini, Tomita genérico, EO/LRT e linhas do inventário", "c1 auditou v3.1: pedido 2 faltante, 3 parcial", "sonda Lean c1 copiada byte a byte com log EXIT 0/trio"],
        "metodo": "Consulta ao Nós Vivo; confronto da reauditoria com a v3.1; cópia fiel da sonda compilada c1 e do log; nota curta com distinção entre tipo condicional e habitante; arquivos anteriores preservados.",
        "resultado": "D1a3OutputBGL tipa Fub, J, T, sigma, propriedades de SW, Delta caracterizado por S-dagger-S e multiplicador; KWR é construído condicionalmente; LightNetStandardWedgeDataBGL tipa a colagem da cunha direita. Nenhuma potência Delta^(it) ilimitada, positividade física ou habitante foi construída.",
        "veredito": "F13_V32_TYPED_D1A3_OUTPUT__CONDITIONAL_CONTRACT__NO_INHABITANT__GATE_NONE",
        "estatuto": "REAL cópia e tipagem do probe c1; DERIVED proposta de interface; OPEN construção física",
        "status": "EXAMINADA_COM_DEFEITO",
        "olhou_dados": False,
        "defeito": "Fubini L2 vetorial, J_W, T positivo com domínio, símbolo e identificação funcional Delta^(it)=B0 seguem campos/obrigações; proposta à fila do operador depende da gerência c1. A v3.2 ainda pede reauditoria independente.",
        "nao_refazer": "Não repetir MiMo, a tabela §3 do mathlib, as 35 referências ou as provas condicionais do probe c1; não instalar tipo no kernel por esta nota.",
        "proximo_passo": "c1 reaudita somente pedidos 2 e 3 e decide FECHADA; gerência encaminha proposta tipada à fila do operador se aprovada.",
        "onde": str(UNIT),
        "artefatos": [result_art] + [art(MD), art(LEAN), art(LOG), art(AUDIT / "AUDITORIA_F1_3_C1_ad949e97.md")],
        "refs": ["formal.f1_1.o16_class2_wiring_caveat"],
        "nota": "F1.1 já FECHADA e não editada neste ciclo; F1.3 permanece separada. NOT_FALSIFIED não é creditação.",
    }
    map_art = write_new(MAP, entry)
    print(json.dumps({"result": result_art, "map_input": map_art, "artifacts": len(artifacts)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
