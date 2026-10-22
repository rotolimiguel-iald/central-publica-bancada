"""Append the F3.6 post-close audit errata with byte-exact memory backups."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path


ROOT = Path(r"C:\IALD\Central de Patentes")
ORDER = ROOT / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_019"
F36 = ORDER / "F3.6"
SURFACES = (
    ROOT / "memory" / "TGL_ATLAS.md",
    ROOT / "memory" / "TGL_INDICE_VIVO.md",
    ROOT / "memory" / "TGL_CORE_MEMORY.md",
    ORDER / "AVISO_GERENCIA.md",
)
MARKER = b"<!-- ORDEM019_F36_E1_ERRATA_20261008 -->"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pin(path: Path) -> str:
    return sha(path.read_bytes())


def atomic(path: Path, data: bytes) -> None:
    temp = path.with_name(path.name + ".tmp_f36_e1")
    if temp.exists():
        raise RuntimeError(f"Temporary path exists: {temp}")
    try:
        with temp.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if temp.stat().st_size != len(data):
            raise RuntimeError(f"Short write: {temp}")
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--result", type=Path, required=True)
    ap.add_argument("--seq-chronology", type=int, required=True)
    ap.add_argument("--seq-withdrawal", type=int, required=True)
    ap.add_argument("--event-withdrawal", type=int, required=True)
    ap.add_argument("--event-delivery", type=int, required=True)
    ap.add_argument("--receipt", type=Path, required=True)
    args = ap.parse_args()
    evidence = {
        "audit": pin(Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F3.6\AUDITORIA_F3_6_ASIMOV_C1_a809cda3.md")),
        "errata": pin(F36 / "ERRATA_POS_FECHO_E1_20261008.md"),
        "prereg_append": pin(F36 / "PRE_REGISTRO_CONDICIONAL.md"),
        "map_f36": pin(F36 / "MAPA_F36.json"),
        "seal_script": pin(F36 / "selar_f36.py"),
        "result": pin(args.result),
    }
    note = f"""

## 08/10/2026 — F3.6, errata de custódia pós-fecho (ao lado)

{MARKER.decode()}

[REAL numérico local/DERIVED — auditoria c1] A F3.6 permanece FECHADA por PAREDE MEDIDA no Asimov em Λ, base nua: β de comparação em runtime = α(0)√e = 0,012031300400803142; σβ principal = 0,018043479 (1,50β), com intervalo de passos de 0,017900698 a 0,018362135. A reprodução independente sem CAMB deu 0,018225; correlações β–w0 = 0,694 e β–wa = −0,804. Nenhum dado observado foi processado ou ajustado. O controle é explicitamente NÃO-CEGO pela exposição incidental de médias publicadas na leitura de fontes/código, sem uso dessas médias no Fisher.

[REAL documental — errata ao lado] A frase antiga «primeira execução local deu 0,01804348» está errada. A rodada 1, às 03:23, usou o núcleo β do FundoV3 e deu 0,018020762. Às 03:25:42 só o núcleo β mudou para ρ do CAMB (D1F-V1) e âncora hoje, após ver σ; a rodada 2, às 03:26, deu 0,018043479 (+0,13%). Selftest às 03:28; FREEZE às 03:31:28; rodada 3 às 03:32 reproduziu a segunda. As erratas D1F-01/03/V1 entraram na primária, com a covariância V3 como sensibilidade, inversamente à recomendação inicial da gerência. Na base efetiva, σβ≈24–30 e, pelo complemento de Schur, σ(β|w0,wa)≥σ(β). `MAPA_F36.json` SHA-256 {evidence['map_f36']}; `selar_f36.py` SHA-256 {evidence['seal_script']}.

[INPUT — retirada documental] A pergunta `call_92df0866…` de 04:59:15Z ao operador está RETIRADA/SUPERADA para o portão F3.6 pela parede medida; não houve resposta registrada e não se afirma cancelamento técnico do cartão da interface. X18, sobre a leitura da autorização do CAMB sintético, segue separado. D1F-04 (+0,96% em σβ), CPL fora de Λ, CMB completo e eventual controle DESI DR2 são rotas próprias [OPEN]; o σβ≈0,94β do DR2 é [CONJECTURE], de incertezas lembradas de memória, e requer unidade e pré-registro novos. Mapa seq {args.seq_chronology}/{args.seq_withdrawal}; quadro evento {args.event_withdrawal} para a retirada e {args.event_delivery} para F3.6.E1 ENTREGUE. Auditoria SHA-256 {evidence['audit']}; errata {evidence['errata']}; pré-registro acrescido {evidence['prereg_append']}; recibo {evidence['result']}. Nenhum dado foi aberto e nenhum gate mudou.
""".encode("utf-8")

    originals: dict[Path, bytes] = {}
    for path in SURFACES:
        data = path.read_bytes()
        if MARKER in data:
            raise RuntimeError(f"Marker already present: {path}")
        originals[path] = data
    if args.receipt.exists():
        raise RuntimeError(f"Receipt exists: {args.receipt}")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    records = []
    for path, data in originals.items():
        backup = path.with_name(path.name + f".bak_{stamp}")
        if backup.exists():
            raise RuntimeError(f"Backup exists: {backup}")
        with backup.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if backup.read_bytes() != data:
            raise RuntimeError(f"Backup mismatch: {path}")
        after = data + note
        atomic(path, after)
        if path.read_bytes() != after:
            atomic(path, data)
            raise RuntimeError(f"Memory mismatch: {path}")
        records.append({
            "path": str(path), "backup": str(backup),
            "sha256_before": sha(data), "sha256_backup": pin(backup),
            "sha256_after": pin(path),
            "size_before": len(data), "size_after": len(after),
        })

    receipt = {
        "memory_unit": "F0.3", "memory_claim_event": 323,
        "errata_unit": "F3.6.E1", "marker": MARKER.decode(),
        "evidence": evidence, "surfaces": records,
    }
    raw = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    atomic(args.receipt, raw)
    print(json.dumps({"ok": True, "surfaces": len(records), "receipt": str(args.receipt), "sha256": sha(raw)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
