"""Append F2.3's conditional sandbox result to local memory with byte backups."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile


ROOT = Path(r"C:\IALD\Central de Patentes")
UNIT = ROOT / "Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F2.3"
MARKER = "<!-- F23_CURVED_FIELD_LIGAND_20261008 -->"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def append_atomic(path: Path, addition: str, stamp: str) -> dict[str, object]:
    original = path.read_bytes()
    if MARKER.encode("ascii") in original:
        raise RuntimeError(f"FAIL_CLOSED: marker already exists: {path}")
    backup = path.with_name(path.name + f".bak_{stamp}")
    with backup.open("xb") as out:
        out.write(original)
        out.flush()
        os.fsync(out.fileno())
    if backup.read_bytes() != original:
        raise RuntimeError(f"FAIL_CLOSED: backup mismatch: {path}")
    payload = original + addition.encode("utf-8")
    with NamedTemporaryFile(dir=path.parent, prefix=".f23_memory_", suffix=".tmp", delete=False) as tmp:
        tmp.write(payload)
        tmp.flush()
        os.fsync(tmp.fileno())
        temporary = Path(tmp.name)
    if temporary.stat().st_size != len(payload) or path.read_bytes() != original:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"FAIL_CLOSED: temp or concurrent change: {path}")
    os.replace(temporary, path)
    if path.read_bytes() != payload or len(payload) <= len(original):
        with NamedTemporaryFile(dir=path.parent, prefix=".f23_restore_", suffix=".tmp", delete=False) as tmp:
            tmp.write(backup.read_bytes())
            tmp.flush()
            os.fsync(tmp.fileno())
            restore = Path(tmp.name)
        os.replace(restore, path)
        raise RuntimeError(f"FAIL_CLOSED: post-write mismatch; restored {path}")
    return {"path": str(path), "backup": str(backup), "before_sha256": hashlib.sha256(original).hexdigest(), "after_sha256": sha(path), "before_bytes": len(original), "after_bytes": len(payload), "backup_matches_before": True}


def main() -> None:
    result_path = UNIT / "RESULTADO.json"
    result = json.loads(result_path.read_text(encoding="utf-8"))
    wanted = {"propext", "Classical.choice", "Quot.sound"}
    if result.get("build", {}).get("exit_code_observed_by_command_tool") != 0:
        raise RuntimeError("FAIL_CLOSED: build not green")
    if any(set(axioms) != wanted for axioms in result["build"]["axioms"].values()):
        raise RuntimeError("FAIL_CLOSED: axioms not restricted to trio")
    h_lean = sha(UNIT / "LiganteLeiCampoCurvo.lean")
    h_log = sha(UNIT / "BUILD.log")
    h_axioms = sha(UNIT / "AXIOMAS.txt")
    h_hashes = sha(UNIT / "HASHES.json")
    h_diag = sha(UNIT / "DIAGNOSTICO_TIPADO.md")
    h_result = sha(result_path)
    if h_log != h_axioms:
        raise RuntimeError("FAIL_CLOSED: axioms transcript differs from log")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    atlas = f"""

## 08/10/2026 — F2.3: ligante condicional da lei de campo no curvo, só no sandbox

{MARKER}

[REAL — fontes] O QG-03 do levantamento confirma que as pedras v338 `GeneralMetricClausius`, `GravitationalChartGluing`, `TopologicalAtlasGluing` e `SmoothSelectedAtlasGluing` já eram termos no build guarda-chuva `TGLExt.lean`, mas não estavam no fecho de imports das declarações QG. `Fundacao.the_post_lives_in_the_passage` é identidade de expectativa em matriz finita; `lightH3` da luz cobre a direção `nullDir` na cunha. Nenhum dos dois fornece por si Clausius/área para TODA tela nula de cada carta curva. `horizon_einstein_reconstruction` já importado exige lápis de horizonte em toda direção.

[REAL — teorema condicional na CÓPIA; INPUT — ponte H3] `ChatgptAudit.F23CurvedFieldLigand.passage_h3_to_connected_smooth_atlas_einstein` usa a conclusão da passagem como entrada de `hH3 : passagem → NamedAtlasH3`, que fornece a lei de área/Clausius em todo ponto e direção nula. A partir de registros, telas, conservação e transições suaves igualmente nomeados, constrói `AreaChart` e aplica `connected_smooth_atlas_einstein`: existe um **único** Λ comum com `G_μν + Λg_μν = 8πG T_μν` nas cartas fornecidas; `η=(4G)⁻¹` e `2π/η=8πG` pelo lema já existente. Como a passagem já é teorema sob suas premissas, `hH3` carrega integralmente o elo físico faltante e é logicamente equivalente ali ao H3 nomeado. Não se derivou H3 do estado, nem se construiu solução global.

[EVIDÊNCIA] `F2.3/LiganteLeiCampoCurvo.lean` SHA-256 {h_lean}; `BUILD.log` {h_log}; `AXIOMAS.txt` {h_axioms}; `HASHES.json` {h_hashes}; `DIAGNOSTICO_TIPADO.md` {h_diag}; `RESULTADO.json` {h_result}. Lean v4.31.0 compilou o módulo na cópia, exit 0, zero `sorry`/`admit`/`axiom` novo, `#print axioms` dos dois nomes só `[propext, Classical.choice, Quot.sound]`; revisão independente de tipos e log. Quadro F2.3 ENTREGUE evento 243; Mapa seq 790–791. O Nós original, o `um.py`, o gate e a declaração histórica v390 NÃO mudaram; a integração canônica v392 cabe à gerência c1.
"""
    index = f"""

## 08/10/2026 — F2.3 entregue: ligante condicional do campo curvo

{MARKER}

[REAL sandbox / INPUT H3] Teorema `passage_h3_to_connected_smooth_atlas_einstein` compilado na cópia do kernel: passagem finita → H3 de todas as telas **por hipótese nomeada** → AreaChart → Einstein em atlas suave com Λ único e `2π/η=8πG`. `lightH3` não supre sozinho todos os nulos; sem solução global ou alteração do kernel canônico. Fonte SHA-256 {h_lean}; log {h_log}; resultado {h_result}; hashes {h_hashes}. Quadro ENTREGUE evento 243, Mapa seq 791; c1 integra na v392 se aceitar.
"""
    core = f"""

## 08/10/2026 — F2.3: lei de campo no curvo ligada condicionalmente em sandbox

{MARKER}

[REAL] Pedra F2.3 na cópia do kernel, Lean exit 0, dois `#print axioms` somente no trio, zero `sorry`. Fonte SHA-256 {h_lean}, log {h_log}, recibo {h_result}. As quatro pedras v338 já estão no build guarda-chuva; a nova pedra ainda não entrou no fecho canônico. `[INPUT]` hH3 transporta a passagem finita para Clausius/área em cada ponto e direção nula; esse elo NÃO decorre do estado ou do ContratoH3 da luz, que fixa `nullDir`. A saída é implicação com Λ único no atlas fornecido e η=(4G)⁻¹, sem solução global construída. Quadro F2.3 ENTREGUE evento 243; Mapa seq 791. Integração v392 e auditoria reservadas à gerência; gate intacto.
"""
    notice = f"""

## 08/10/2026 — F2.3 ENTREGUE: ligante condicional do campo curvo para auditoria c1

{MARKER}

[REAL] A F2.3 reivindicada (evento 242) foi entregue no evento 243 com seis evidências. `F2.3/LiganteLeiCampoCurvo.lean` SHA-256 {h_lean} compilou na CÓPIA do kernel (Lean 4.31.0, exit 0), `BUILD.log` SHA {h_log}, `AXIOMAS.txt` SHA {h_axioms}: só propext, Classical.choice, Quot.sound; zero sorry. `HASHES.json` {h_hashes}, `DIAGNOSTICO_TIPADO.md` {h_diag}, `RESULTADO.json` {h_result}; Mapa seq 790–791.

[ALCANCE] Rota C da árvore anti-parede: Fundação prova identidade finita; `hH3` `[INPUT]` recebe essa identidade e fornece área/Clausius em TODAS as telas nulas de cada carta. Com registros, conservação e transições explícitos, o teorema conclui Einstein em atlas suave, Λ único, `η=(4G)⁻¹` e `2π/η=8πG`. Essa hipótese contém o elo físico, não o deriva; `lightH3` apenas cobre `nullDir`. O Nós original, `um.py`, selo e gate seguem intocados. Integração canônica na v392 e decisão `AUDITADA`/`FECHADA` cabem à gerência.
"""
    targets = [
        (ROOT / "memory/TGL_ATLAS.md", atlas),
        (ROOT / "memory/TGL_INDICE_VIVO.md", index),
        (ROOT / "memory/TGL_CORE_MEMORY.md", core),
        (ROOT / "Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md", notice),
    ]
    records = [append_atomic(path, addition, stamp) for path, addition in targets]
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
