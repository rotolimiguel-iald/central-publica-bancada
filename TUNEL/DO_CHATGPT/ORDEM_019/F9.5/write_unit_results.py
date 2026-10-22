"""Produce evidence manifests for the claimed ORDEM 019 units."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT")
HERE = BASE / "ORDEM_019"
OLD = BASE / "ORDEM_018"
KERNEL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt")
INVENTORY = Path(r"C:\IALD\Central de Patentes\memory\INVENTARIO_BANCADA_CHATGPT.md")


def checksum(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    data = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


UNITS = {
    "F1.1": {
        "done": "Inventário de cada ligação científica efetivamente consumida pela cadeia QG, com pedra, classe e estimativa de formalização.",
        "numbers": {"rows": 12},
        "statute": "REAL_SOURCE_AUDIT_AND_ESTIMATED_EFFORT",
        "not_done": "Sem novo habitante Fock/Maxwell, compilação Lean ou mudança do gate; estimativas não são medição de desenvolvimento.",
        "why": "Escopo de inventário e preservação dos originais.",
        "files": [HERE / "F1.1" / "INVENTARIO.md", INVENTORY,
                  KERNEL / "QGCitationDischarge.lean", KERNEL / "QGSolutionComplete.lean",
                  KERNEL / "TheImportedSecondQuantization.lean", KERNEL / "TheImportedEquilibrium.lean",
                  KERNEL / "LightOneParticleByTerm.lean"],
    },
    "F1.2": {
        "done": "Reaproveitamento dos termos A1 e contrato regular v351; dois lemas algébricos de conjugação dos geradores matriciais compilados no sandbox.",
        "numbers": {"reused_delivery_notes": 3, "new_sandbox_lean_files": 1, "compiled_algebraic_theorems": 2},
        "statute": "REAL_KERNEL_REUSE_AND_SANDBOX_ALGEBRAIC_TERMS_WITH_OPEN_ANALYTIC_BRIDGE",
        "not_done": "Sem equivalência analítica do produto cruzado matricial contínuo, transporte do traço normal semifinito ou alteração do kernel canônico.",
        "why": "A prova nova cobre somente a conjugação algébrica; fechamento L2/von Neumann e fiação ao RegularCoreTraceData exigem passos próprios.",
        "files": [HERE / "F1.2" / "REAPROVEITAMENTO.md",
                  HERE / "F1.2" / "PONTE_MATRICIAL_CONTRATO.md",
                  HERE / "F1.2" / "SANDBOX_RESULT.md",
                  HERE / "F1.2" / "sandbox" / "MatrixInnerGauge.lean",
                  HERE / "F1.2" / "sandbox" / "COMPILE_RESULT.json",
                  BASE / "ENTREGA_011_A1_escala_dual_do_peso_limite_no_mesmo_core.md",
                  BASE / "ENTREGA_011_A1_escala_dual_do_mesmo_gerador_regular.md",
                  BASE / "ENTREGA_011_A1_contrato_forte_e_peso_dual.md",
                  KERNEL / "V351RegularCoreTraceConstruction.lean",
                  KERNEL / "V351InverseLimitScaling.lean",
                  KERNEL / "V351RegularGeneratorDualScaling.lean",
                  KERNEL / "FiniteCrossedProduct.lean", KERNEL / "GlobalLiftLadder.lean"],
    },
    "F4.2": {
        "done": "Preparação do contrato de entrada, congelamento e gate do PE do conjunto D.",
        "numbers": {"preparation_files_in_manifest": 9, "new_waveforms": 0, "new_injections": 0, "new_PE": 0},
        "statute": "REAL_PREPARATION_AWAITS_OPERATOR",
        "not_done": "Observações D não abertas; nenhuma injeção ou PE executado; V1/holds intactos.",
        "why": "Aprovação do operador e pré-registro ratificado são pré-condições da execução.",
        "files": [HERE / "F4.2" / "PREPARACAO_GATE.md",
                  OLD / "preregistros" / "conjunto_d" / "MANIFESTO_CONJUNTO_D.json",
                  OLD / "preregistros" / "conjunto_d" / "PROPOSTA_MANIFESTO_METADATA_D.json"],
    },
    "F5.1": {
        "done": "Contrato de código candidato, versão, taxas, expansão S(T), validação e medição de custo BBN.",
        "numbers": {"candidate_codes": 1, "installed_codes_verified_here": 0, "BBN_TGL_runs": 0},
        "statute": "REAL_PREPARATION_AWAITS_OPERATOR_INSTALLATION",
        "not_done": "PRIMAT não instalado, código não modificado, nenhuma previsão Y_p/D-H ou covariância executada.",
        "why": "A ORDEM 019 atribui a instalação do código de terceiros ao operador.",
        "files": [HERE / "F5.1" / "CONTRATO_BBN.md",
                  OLD / "f9_integrated_bootstrap_preparation" / "BBN_METADATA.json",
                  BASE.parent / "PARA_CHATGPT" / "ORDEM_018_ADENDO_001_era_da_radiacao.md"],
    },
    "F9.5": {
        "done": "ESTADO.md curto, INDICE.md e livro encadeado dos recibos legados; 130 backups históricos do transporte arquivados por data com SHA-256 antes/depois.",
        "numbers": {"legacy_receipts_indexed": 117, "transport_backups_archived": 130, "current_session_backup_adjacent": 1},
        "statute": "REAL_GENERATED_STATE_RECEIPT_CHAIN_AND_VERIFIED_BACKUP_ARCHIVE",
        "not_done": "Não foi feita auditoria científica de cada recibo legado, nem alteração de originais científicos ou do guia de transporte ativo.",
        "why": "O índice atesta bytes e localização; a avaliação do conteúdo é ato próprio da gerência.",
        "files": [HERE / "F9.5" / "build_order18_state.py",
                  HERE / "F9.5" / "archive_transport_backups.py",
                  HERE / "F9.5" / "BACKUP_ARCHIVE_PLAN.json",
                  HERE / "F9.5" / "BACKUP_ARCHIVE_RESULT.json",
                  OLD / "ESTADO.md", OLD / "INDICE.md", OLD / "recibos.jsonl"],
    },
}


def atomic(path: Path, data: bytes) -> None:
    old = path.read_bytes() if path.exists() else None
    if old is not None:
        suffix = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup = path.with_name(path.name + ".bak_" + suffix)
        with backup.open("xb") as handle:
            handle.write(old)
        if backup.read_bytes() != old:
            raise RuntimeError("backup differs")
    temp = path.with_name(path.name + ".tmp_" + str(os.getpid()))
    with temp.open("xb") as handle:
        handle.write(data)
    if temp.stat().st_size != len(data):
        raise RuntimeError("temporary size differs")
    os.replace(temp, path)
    if path.read_bytes() != data:
        raise RuntimeError("replacement differs")


def main() -> None:
    selected = sys.argv[1:] or list(UNITS)
    for unit in selected:
        spec = UNITS[unit]
        result = {
            "unidade": unit,
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "feito": spec["done"],
            "numeros": spec["numbers"],
            "hashes_lidos": [checksum(path) for path in spec["files"]],
            "estatuto": spec["statute"],
            "nao_feito": spec["not_done"],
            "motivo": spec["why"],
        }
        destination = HERE / unit / "RESULTADO.json"
        atomic(destination, (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        print(unit, checksum(destination)["sha256"])


if __name__ == "__main__":
    main()
