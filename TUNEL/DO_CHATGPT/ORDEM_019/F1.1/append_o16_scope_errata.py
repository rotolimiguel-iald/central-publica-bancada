"""Append the later c1 rotation-scope errata to F1.1, preserving every earlier byte."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile


HERE = Path(__file__).resolve().parent
INVENTORY = HERE / "INVENTARIO.md"
FIRST = HERE / "RESULTADO_RESSALVA_O16.json"
FINAL = HERE / "RESULTADO_RESSALVA_O16_FINAL.json"
CLAUDE = Path(r"C:\IALD\CLAUDE.md")
MARKER = "<!-- F11_O16_ESCOPO_ROTACOES_ERRATA_20261008 -->"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_new(path: Path, payload: bytes) -> None:
    if path.exists():
        raise RuntimeError(f"FAIL_CLOSED: output exists {path}")
    with NamedTemporaryFile(dir=path.parent, prefix=".f11_errata_", suffix=".tmp", delete=False) as tmp:
        tmp.write(payload)
        tmp.flush()
        os.fsync(tmp.fileno())
        temporary = Path(tmp.name)
    if temporary.stat().st_size != len(payload):
        temporary.unlink(missing_ok=True)
        raise RuntimeError("FAIL_CLOSED: short temp")
    os.replace(temporary, path)
    if path.read_bytes() != payload:
        raise RuntimeError("FAIL_CLOSED: output mismatch")


def main() -> None:
    if FINAL.exists():
        raise RuntimeError("FAIL_CLOSED: final evidence exists")
    first = json.loads(FIRST.read_text(encoding="utf-8"))
    before = INVENTORY.read_bytes()
    if sha(before) != first["inventory"]["after_sha256"]:
        raise RuntimeError("FAIL_CLOSED: inventory changed since first receipt")
    if MARKER.encode("ascii") in before:
        raise RuntimeError("FAIL_CLOSED: errata already appended")
    reference = CLAUDE.read_bytes()
    if b"errata_rotacoes_homonimas_07out" not in reference or b"errata_leitura_cria_o_objeto_07out" not in reference:
        raise RuntimeError("FAIL_CLOSED: later c1 errata markers missing")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = INVENTORY.with_name(INVENTORY.name + f".bak_{stamp}")
    with backup.open("xb") as out:
        out.write(before)
        out.flush()
        os.fsync(out.fileno())
    if backup.read_bytes() != before:
        raise RuntimeError("FAIL_CLOSED: backup byte mismatch")
    appendix = f"""

### Errata de escopo da linha O16 — leitura das duas correções c1 de 07/10/2026

{MARKER}

[REAL — consulta posterior] `C:\\IALD\\CLAUDE.md` (SHA-256 `{sha(reference)}`; marcadores `errata_rotacoes_homonimas_07out` e `errata_leitura_cria_o_objeto_07out`) corrige a aferição de 27/09 citada pela gerência. A **classe 2 da linha acrescida acima classifica as seis pedras O16 existentes e sua interface ainda não consumida pela assinatura**. Não classifica a rotação espaço-tempo de todos os planos nem o PCT global da rede como teoremas O16 prontos que só precisem de um `import`.

No plano do boost `t–x`, as identidades matriciais Wick/rotação dão a leitura angular e o contorno `2π`; a segunda errata c1 impede chamá-las simplesmente de «homônimas». A frase «a leitura cria o objeto» é interpretação `[INPUT/ONTO]` do operador; a pedra que a formula explicitamente foi compilada só no sandbox e não foi contada como kernel instalado aqui. O que ainda não está no kernel/tipo são as leituras dos outros planos — rotações `x–y`, `x–z`, boosts `t–y`, `t–z`, família Lorentz de cunhas e PCT global da rede. Para a conclusão em uma direção nula da v376, a gerência os registrou como **3. SABIDO / FORA_DO_CAMINHO**, por referências Wigner/BW/BGL, não como nova construção exigida aqui. `D1prime` e `circularScreen_conjugate` continuam provas de caractere e conjugação da tela, não uma ação PCT global no `H1`/Fock/rede. A fiação `P_ker K ↔ C.PF` segue classe 2 quanto à rota D6 disponível, mas sua instância não trivial e o mapa de cores/projeções de tipos diferentes seguem sem termo exibido na assinatura. A estimativa de interface em dias supõe os certificados; não paga as construções globais.

[REAL] Esta errata preserva integralmente a linha e o parágrafo anteriores como histórico. O inventário continua com as 12 linhas originais, uma linha aditiva para O16 e este esclarecimento ao lado. Nenhuma prova, compilação ou gate foi promovido.
"""
    after = before + appendix.encode("utf-8")
    with NamedTemporaryFile(dir=HERE, prefix=".f11_inventory_errata_", suffix=".tmp", delete=False) as tmp:
        tmp.write(after)
        tmp.flush()
        os.fsync(tmp.fileno())
        temporary = Path(tmp.name)
    if temporary.stat().st_size != len(after) or INVENTORY.read_bytes() != before:
        temporary.unlink(missing_ok=True)
        raise RuntimeError("FAIL_CLOSED: temp or concurrent change")
    os.replace(temporary, INVENTORY)
    if INVENTORY.read_bytes() != after:
        with NamedTemporaryFile(dir=HERE, prefix=".f11_restore_", suffix=".tmp", delete=False) as tmp:
            tmp.write(backup.read_bytes())
            tmp.flush()
            os.fsync(tmp.fileno())
            restore = Path(tmp.name)
        os.replace(restore, INVENTORY)
        raise RuntimeError("FAIL_CLOSED: restore after failed append")
    record = {
        "unit": "F1.1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "CAVEAT_AND_LATER_C1_SCOPE_ERRATA_APPENDED_FOR_CLOSURE_REVIEW",
        "historical_twelve_rows_preserved": True,
        "one_o16_table_row_added": True,
        "inventory": {"path": str(INVENTORY), "before_sha256": sha(before), "after_sha256": sha(after), "after_bytes": len(after), "backup": str(backup), "backup_matches_before": True},
        "first_receipt": {"path": str(FIRST), "sha256": sha(FIRST.read_bytes())},
        "six_stone_pins": {"path": str(HERE / "O16_AFERICAO_F11.json"), "sha256": sha((HERE / "O16_AFERICAO_F11.json").read_bytes())},
        "later_c1_errata": {"path": str(CLAUDE), "sha256": sha(reference), "markers": ["errata_rotacoes_homonimas_07out", "errata_leitura_cria_o_objeto_07out"]},
        "classification_scope": "CLASS_2_FOR_EXISTING_O16_STONES_AND_UNWIRED_CROSS_PAIR_BRIDGE; OTHER_SPACETIME_PLANES_KNOWN_OUTSIDE_V376_NULL_PATH; GLOBAL_PCT_NOT_CONSTRUCTED_HERE",
        "new_lean_compilation": False,
        "gate_changed": False,
        "next_action": "attach final receipt to F1.1; c1 decides audit and closure",
    }
    atomic_new(FINAL, (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"inventory_after_sha256": sha(after), "final_sha256": sha(FINAL.read_bytes()), "backup": str(backup)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
