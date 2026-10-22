"""Append the audited F4.3/F5.2 errata to four memory surfaces, with byte backups."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path


ROOT = Path(r"C:\IALD\Central de Patentes")
ORDER = ROOT / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_019"
SURFACES = (
    ROOT / "memory" / "TGL_ATLAS.md",
    ROOT / "memory" / "TGL_INDICE_VIVO.md",
    ROOT / "memory" / "TGL_CORE_MEMORY.md",
    ORDER / "AVISO_GERENCIA.md",
)
MARKER = b"<!-- ORDEM019_AUDITORIA_F43_F52_C1_20261008 -->"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_digest(path: Path) -> str:
    return digest(path.read_bytes())


def atomic_write(path: Path, data: bytes) -> None:
    tmp = path.with_name(path.name + ".tmp_f43_f52_c1")
    if tmp.exists():
        raise RuntimeError(f"Temporary path already exists: {tmp}")
    try:
        with tmp.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if tmp.stat().st_size != len(data):
            raise RuntimeError(f"Short temporary write: {tmp}")
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--f52-result", type=Path, required=True)
    parser.add_argument("--f52-errata", type=Path, required=True)
    parser.add_argument("--f52-candidate", type=Path, required=True)
    parser.add_argument("--f52-map-seq", type=int, required=True)
    parser.add_argument("--f52-event", type=int, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    f43_plan = ORDER / "F4.3" / "PLANO_E_PREREGISTRO.md"
    f43_prereg = ORDER / "F4.3" / "PREREGISTRO_F4_3_V2.json"
    f43_result = ORDER / "F4.3" / "RESULTADO_C1_F43_V2_20261008.json"
    audit = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F4.3_F5.2\AUDITORIA_F4_3_F5_2_C1_20261007.md")
    evidence = {
        "audit": file_digest(audit),
        "f43_plan": file_digest(f43_plan),
        "f43_prereg": file_digest(f43_prereg),
        "f43_result": file_digest(f43_result),
        "f52_errata": file_digest(args.f52_errata),
        "f52_candidate": file_digest(args.f52_candidate),
        "f52_result": file_digest(args.f52_result),
    }

    note = f"""

## 08/10/2026 — ORDEM 019, erratas auditadas F4.3 e F5.2 (ao lado)

{MARKER.decode()}

[REAL documental/DERIVED/OPEN — F4.3] A auditoria c1 mostrou que a premissa histórica de absorção do 220 isolado, o lnB −0,0026 do C6, o Fisher B2_K e o proxy de 0,06σ do 440 foram obtidos com k=1. No relógio V1, k=2π/κ̂ fica de 28,5 a 30,2; δτ̂_220 fica de −0,34 a −0,39 e δτ̂_440 de fonte fixa, de −0,69 a −0,74. O Q_220 exigido pela RG (1,98–2,01) cai abaixo do mínimo da grade PRÓGRADA (2,100). [DECLARADO — correção da gerência/cético B] O ramo CONTRA-ROTANTE pode absorver f e Q do 220 isolado com χ≈0,10–0,22 e M≈0,58–0,72 M_f; o controle C3 com IMR completo fecha essa alternativa. O 220+440 permanece diagnóstico subordinado ao primário IMR do V1, com controle conjunto de erro, manifesto e portão de poder antes de qualquer conjunto D. O diagnóstico linear SVD/η não extrapola para x≈0,6; exige injeção exata. Plano aditivo SHA-256 {evidence['f43_plan']}; pré-registro V2 {evidence['f43_prereg']}; recibo {evidence['f43_result']}. Mapa seq 842; quadro ENTREGUE evento 315. Pedido de autorização F4.3 ao operador suspenso até reauditoria c1.

[REAL documental/KNOWN/OPEN — F5.2] A Tabela 5 de arXiv:2506.20707 dá CMB-SPA com Yₚ pela BBN: 2,81±0,12 (v1) e 2,82±0,12 (v2). Na v2, CMB-SPA com Yₚ livre é 2,96 (+0,21/−0,24); o 2,97 (+0,40/−0,64) da v1 pertence a SPT-3G D1 sozinho com Yₚ livre. A atribuição congelada «CMB-SPA 2,97±0,12» em 10_frozen_neff_v1.py:46 e no pré-registro V1 da Fase 8 fica corrigida AO LADO; originais intactos. O candidato da Bancada apresenta as duas linhas por hash e deixa a escolha X16 aberta, SEM instalação. O 0,045 do SO é fim do levantamento 2025–2034; o CMB-S4 revisto começaria em 2033 e alcançaria 0,030 por volta de 2042, mas o projeto foi encerrado: não fiar «quando». O anúncio de 09/07/2025 foi de DOE/NSF. Admissão das fontes primárias por SHA-256 é ato do operador D8/X16. Errata SHA-256 {evidence['f52_errata']}; candidato {evidence['f52_candidate']}; recibo {evidence['f52_result']}. Mapa seq {args.f52_map_seq}; quadro ENTREGUE evento {args.f52_event}. F5.3 teve reivindicação liberada no evento 310 e continua BLOQUEADA.

[REAL — custódia] Auditoria c1 SHA-256 {evidence['audit']}. Estas entradas corrigem as afirmações anteriores sem apagá-las. Nenhum dado observacional foi aberto, nenhum canal da Bancada foi instalado e nenhum gate mudou; NOT_FALSIFIED não é CONFIRMED.
"""
    addition = note.encode("utf-8")
    reads: dict[Path, bytes] = {}
    for path in SURFACES:
        before = path.read_bytes()
        if MARKER in before:
            raise RuntimeError(f"Marker already present: {path}")
        reads[path] = before
    if args.receipt.exists():
        raise RuntimeError(f"Receipt already exists: {args.receipt}")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    records = []
    for path, before in reads.items():
        backup = path.with_name(path.name + f".bak_{stamp}")
        if backup.exists():
            raise RuntimeError(f"Backup already exists: {backup}")
        with backup.open("xb") as stream:
            stream.write(before)
            stream.flush()
            os.fsync(stream.fileno())
        if backup.read_bytes() != before:
            raise RuntimeError(f"Backup mismatch: {path}")
        after = before + addition
        atomic_write(path, after)
        if path.read_bytes() != after:
            atomic_write(path, before)
            raise RuntimeError(f"Append mismatch: {path}")
        records.append({
            "path": str(path),
            "backup": str(backup),
            "sha256_before": digest(before),
            "sha256_backup": file_digest(backup),
            "sha256_after": digest(after),
            "size_before": len(before),
            "size_after": len(after),
        })

    receipt = {
        "marker": MARKER.decode(),
        "memory_unit": "F0.3",
        "memory_claim_event": 311,
        "evidence": evidence,
        "surfaces": records,
    }
    raw = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    atomic_write(args.receipt, raw)
    print(json.dumps({"ok": True, "receipt": str(args.receipt), "sha256": digest(raw), "surfaces": len(records)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
