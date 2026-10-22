"""Append the c1 F2.3/F1.1.E1 audit correction to four memory surfaces.

This script preserves the original bytes, creates a same-folder backup before
each replacement, checks for concurrent edits, and writes a receipt.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile


ROOT = Path(r"C:\IALD\Central de Patentes")
PATHS = [
    ROOT / "memory" / "TGL_ATLAS.md",
    ROOT / "memory" / "TGL_INDICE_VIVO.md",
    ROOT / "memory" / "TGL_CORE_MEMORY.md",
    ROOT / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_019" / "AVISO_GERENCIA.md",
]
AUDIT = Path(
    r"C:\IALD\PROGRAMA_IALD\auditorias\F2.3_F1.1_temperatura"
    r"\AUDITORIA_F2_3_F1_1_temperatura_C1_abe2cbdf.md"
)
RECEIPT = (
    ROOT / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_019" / "F2.3"
    / "MEMORIA_ERRATA_AUDITORIA_TEMPERATURA_F11_20261008.json"
)
MARKER = "ORDEM019_F23_F11E1_C1_TEMPERATURE_AUDIT_20261008"
ENTRY = """

## 08/10/2026 — F2.3 e F1.1.E1: auditoria c1 da temperatura e da leitura (errata ao lado)

<!-- ORDEM019_F23_F11E1_C1_TEMPERATURE_AUDIT_20261008 -->

[REAL — auditoria c1, SHA-256 `6a8ce1ef046a0a0fe7ed14de85df3fa30925fc00e76932340311151f62a1115a`] A pedra `LiganteLeiCampoCurvoTemperaturaStandalone.lean` compilou em sandbox, com .olean reproduzido byte a byte e axiomas só no trio; veredito **APROVA_COM_RESSALVAS, NÃO integrar na v392**. O teorema final é corolário do ligante F2.3 já auditado: a ponte `hH3_from_reading` é logicamente equivalente ao H3 global nomeado, pois as três igualdades térmicas já seguem da leitura fiel. As sondas c1 mostram `observer_boost`/`observer_boost_eq` e boost, `null_expand`, `metric_lorentz`, `state_boost`, `net_covariant` sem consumo na prova. Para a mesma cunha, qualquer taxa positiva admite leitura fiel com período diferente; `1/P=κ/(2π)` é relativo ao relógio, e o defeito plano já define o fator κ/(2π). O período é da projeção angular, não da face hiperbólica. Fonte Maxwell identificada, conservação curva, outras direções nulas e H3 seguem `[INPUT]`; não há existência global de solução demonstrada.

[REAL — fiação já no kernel para a cunha padrão] `lightH2 C N` usa o mesmo certificado Fock; `polar_period_matches_contract` liga `1/P` a `C.unruhTemperature`, `unruh_is_kms_temperature` dá o KMS do fluxo de Killing do contrato, `same_normalization_same_angular_period` fixa P para o mesmo N, e `data_temperature_from_same_period` leva a igualdade ao dado H3 da mesma direção. Isso exige o contrato H2/H3, leitura fiel e normalização N; não fabrica habitantes Fock/Maxwell nem a família em todas as direções. A Standalone não consumiu essa fiação. A candidata gerencial tem nome vigente **PALAVRA**; `TheReadingCreatesTheObject` é nome histórico, e esta correção não a instala.

[REAL — F1.1, classe relativa] O quociente polar e as identidades Wick estão **classe 1 dentro do O16**; para a assinatura de `qg_solution_end_to_end` são **classe 2, fiação**, sem consumidor no fecho de imports. Os consumidores O16 omitidos eram `polar_period_matches_contract` e `data_temperature_from_same_period`; não se deve dizer que inexiste ligação à temperatura do contrato na cunha padrão. Em `TheObserverReadsTheAngle.lean:112–113`, a frase literal é: «A primeira leitura identifica; a segunda confirma que a operação não altera.» A expressão anterior «a primeira leitura identifica; reler não acrescenta» era composição do título com a docstring, não citação literal. A leitura do operador nomeia PALAVRA `[INPUT/ONTO]`; a idempotência `observing_adds_nothing` não constrói rotações globais da rede.

[PROCESSO — assinatura da correção] A auditoria c1 registra que acréscimos anteriores de memória ocorreram sem unidade específica de memória: na F2.3 havia reivindicação de trabalho vigente; na F1.1 principal, já FECHADA, `reivindicar` foi recusado. Isso permanece como história, sem autorização retroativa. Esta correção é feita em nome de `codex-gerente-tgl`, sob a reivindicação F2.3 renovada no evento 347 e a unidade derivada F1.1.E1 reivindicada no evento 349; a F1.1 principal permanece FECHADA. A frase anterior «auditoria semântica independente» sem artefato tem estatuto `[DECLARADO]`; a presente auditoria c1 está documentada no arquivo acima. Nenhum `um.py`, kernel original, v392, dado observacional ou gate foi alterado por esta escrita; `NOT_FALSIFIED` não é `CONFIRMED`.
"""


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sync_write_new(path: Path, data: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        path.unlink(missing_ok=True)
        raise


def main() -> None:
    audit_hash = sha(AUDIT.read_bytes())
    expected = "6a8ce1ef046a0a0fe7ed14de85df3fa30925fc00e76932340311151f62a1115a"
    if audit_hash != expected:
        raise RuntimeError(f"Audit hash differs: {audit_hash}")
    if RECEIPT.exists():
        raise FileExistsError(RECEIPT)
    stamp = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d_%H%M%S")
    addition = ENTRY.encode("utf-8")
    rows = []
    for path in PATHS:
        original = path.read_bytes()
        if MARKER.encode("ascii") in original:
            raise RuntimeError(f"Marker already exists: {path}")
        backup = path.with_name(path.name + f".bak_{stamp}")
        sync_write_new(backup, original)
        if backup.read_bytes() != original:
            raise RuntimeError(f"Backup differs: {backup}")
        updated = original + addition
        with NamedTemporaryFile(dir=path.parent, prefix=path.name + ".tmp_", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(updated)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            if temporary.stat().st_size != len(updated):
                raise RuntimeError(f"Temporary size differs: {temporary}")
            if sha(path.read_bytes()) != sha(original):
                raise RuntimeError(f"Concurrent edit detected: {path}")
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)
        actual = path.read_bytes()
        if actual != updated or not actual.startswith(original):
            raise RuntimeError(f"Append verification failed: {path}")
        rows.append({
            "path": str(path),
            "backup": str(backup),
            "before_bytes": len(original),
            "after_bytes": len(actual),
            "before_sha256": sha(original),
            "backup_sha256": sha(backup.read_bytes()),
            "after_sha256": sha(actual),
            "prefix_preserved": actual.startswith(original),
            "marker_count": actual.count(MARKER.encode("ascii")),
        })
    receipt = {
        "unit": ["F2.3", "F1.1.E1"],
        "owner": "codex-gerente-tgl",
        "claim_events": [347, 349],
        "audit": str(AUDIT),
        "audit_sha256": audit_hash,
        "marker": MARKER,
        "entry_sha256": sha(addition),
        "entry_bytes": len(addition),
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "files": rows,
    }
    sync_write_new(RECEIPT, (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"receipt": str(RECEIPT), "receipt_sha256": sha(RECEIPT.read_bytes()), "files": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
