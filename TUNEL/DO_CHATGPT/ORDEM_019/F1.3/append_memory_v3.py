"""Append the F1.3 v3 correction to local memory with byte backups."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile


ROOT = Path(r"C:\IALD\Central de Patentes")
UNIT = ROOT / "Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.3"
MARKER = "<!-- F13_D1A_V3_20261008 -->"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def append_atomic(path: Path, addition: str, stamp: str) -> dict[str, object]:
    original = path.read_bytes()
    if MARKER.encode("ascii") in original:
        raise RuntimeError(f"FAIL_CLOSED: marker already exists in {path}")
    backup = path.with_name(path.name + f".bak_{stamp}")
    with backup.open("xb") as out:
        out.write(original)
        out.flush()
        os.fsync(out.fileno())
    if backup.read_bytes() != original:
        raise RuntimeError(f"FAIL_CLOSED: byte backup mismatch for {path}")
    payload = original + addition.encode("utf-8")
    with NamedTemporaryFile(dir=path.parent, prefix=".f13_v3_", suffix=".tmp", delete=False) as temp:
        temp.write(payload)
        temp.flush()
        os.fsync(temp.fileno())
        temp_path = Path(temp.name)
    if temp_path.stat().st_size != len(payload):
        temp_path.unlink(missing_ok=True)
        raise RuntimeError(f"FAIL_CLOSED: incomplete temp for {path}")
    if path.read_bytes() != original:
        temp_path.unlink(missing_ok=True)
        raise RuntimeError(f"FAIL_CLOSED: concurrent change detected in {path}")
    os.replace(temp_path, path)
    written = path.read_bytes()
    if written != payload or len(written) <= len(original):
        with NamedTemporaryFile(dir=path.parent, prefix=".f13_restore_", suffix=".tmp", delete=False) as temp:
            temp.write(backup.read_bytes())
            temp.flush()
            os.fsync(temp.fileno())
            restore = Path(temp.name)
        os.replace(restore, path)
        raise RuntimeError(f"FAIL_CLOSED: post-write mismatch; restored {path}")
    return {
        "path": str(path),
        "backup": str(backup),
        "before_bytes": len(original),
        "after_bytes": len(written),
        "before_sha256": hashlib.sha256(original).hexdigest(),
        "after_sha256": hashlib.sha256(written).hexdigest(),
        "backup_matches_original": True,
    }


def main() -> None:
    graph = sha(UNIT / "GRAFO_DEGRAUS_V3.md")
    result = sha(UNIT / "RESULTADO_V3.json")
    probe = sha(UNIT / "SOURCE_PROBE_V3B.json")
    errata = sha(UNIT / "MIMO_RECIBO_ERRATA_V3.json")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    atlas = f"""

## 08/10/2026 — F1.3 v3: primeiro degrau físico antinulo, com reaproveitamento O16

{MARKER}

[REAL — auditoria documental] A auditoria c1 reprovou o grafo v2: D0.5 já estava medido no core v391 e na reprodução c1; o contrato `LightNetData` aceitava a rede nula. A v3 preserva essa auditoria e a revisão MiMo única [DECLARADO], sem nova chamada. O transporte orbital `H1 = Lp Fib 2 (orbitalMeasure 0)` para coordenadas de rapidez, sua medida, inversas e o entrelaçamento de `B0` com o shift já são termos genéricos em O16 (`OrbitalRapidityTransport_v3`, `OrbitalL2Equivalence_v2`, `OrbitalBoostTransport`, `OrbitalBoostUnitary_v2`): D1a.0 é [REAL], não primeiro alvo novo.

[DERIVED — plano, OPEN — realização] O primeiro alvo novo é D1a.1: Fourier parcial na rapidez com fibra transversal e `J_W` antiunitário no MESMO `H1`. Depois, construir `Δ_W^{{1/2}}` fechado em domínio denso e obter `K(W_R) : StandardSubspace H1` por `closedAntilinearStandardSubspace`, com vetor não nulo e `Δ_K^{{it}}=B0(−2πt)` demonstrado para seu Tomita. A saída D1b exige colagem tipada `D.K rightWedge = (K(W_R)).toClosedSubmodule.toSubmodule`; sem ela um certificado separado deixaria `D.K≡⊥`. A decisão de fortalecer o próprio tipo do kernel cabe ao operador. Araki e segunda quantização dão atalhos [KNOWN] condicionais após Fock/Weyl concreto no mesmo par; a aplicação local, o core físico e `P_F^core` seguem [OPEN].

[EVIDÊNCIA] `GRAFO_DEGRAUS_V3.md` SHA-256 {graph}; `SOURCE_PROBE_V3B.json` {probe}; `MIMO_RECIBO_ERRATA_V3.json` {errata}; `RESULTADO_V3.json` {result}. Mapa de Rotas seq 786; quadro F1.3 ENTREGUE, reauditoria c1 pendente. Nenhum kernel, `um.py`, original científico ou gate mudou. NOT_FALSIFIED nunca é CONFIRMED.
"""
    index = f"""

## 08/10/2026 — F1.3 v3 devolvida à auditoria c1

{MARKER}

[REAL/DERIVED/OPEN] D0.5 e o transporte H1–rapidez/boost O16 já pagos; primeiro alvo novo D1a.1 é Fourier parcial com fibra e `J_W` físico. A saída exige cunha padrão não nula, modularidade `B0(−2πt)` e colagem ao `D.K rightWedge`; Araki/Γ são atalhos [KNOWN] condicionais, sem habitante Fock local. Grafo SHA-256 {graph}; resultado {result}; probe {probe}; mapa seq 786. Quadro ENTREGUE; reauditoria c1 pendente. MiMo único [DECLARADO], core/canto físicos [OPEN], gate intacto.
"""
    notice = f"""

## 08/10/2026 — F1.3 v3 ENTREGUE para reauditoria c1

{MARKER}

[REAL] O grafo F1.3 v2 reprovado foi corrigido em `F1.3/GRAFO_DEGRAUS_V3.md` (SHA-256 {graph}). D0.5 e o transporte orbital O16 são [REAL] já pagos. O primeiro alvo novo é Fourier parcial na rapidez com fibra e `J_W` no mesmo H1 [OPEN]; a saída exige `K(W_R)` padrão não nulo e colagem tipada a `D.K rightWedge`, barrando a rede nula. A tabela mathlib por degrau e A1/A3/D4/§4 do inventário estão no grafo. A errata do MiMo registra SHA integral e cabeçalho [DECLARADO] sem repetir chamada; `F1.3/MIMO_RECIBO_ERRATA_V3.json` SHA-256 {errata}. Revisão interna somente leitura PASS, c1 ainda não reauditorou.

[EVIDÊNCIA] `F1.3/RESULTADO_V3.json` SHA-256 {result}; `F1.3/SOURCE_PROBE_V3B.json` {probe}; Mapa seq 786; quadro ENTREGUE evento 238. Nenhum kernel, `um.py`, original ou gate foi alterado. `AUDITADA`/`FECHADA` reservados à gerência.
"""
    targets = [
        (ROOT / "memory/TGL_ATLAS.md", atlas),
        (ROOT / "memory/TGL_INDICE_VIVO.md", index),
        (ROOT / "Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md", notice),
    ]
    records = [append_atomic(path, addition, stamp) for path, addition in targets]
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
