"""Append the F1.1 O16 caveat to local memory with immediate byte backups."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile


ROOT = Path(r"C:\IALD\Central de Patentes")
UNIT = ROOT / "Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.1"
MARKER = "<!-- F11_O16_CAVEAT_20261008 -->"


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
    with NamedTemporaryFile(dir=path.parent, prefix=".f11_o16_memory_", suffix=".tmp", delete=False) as tmp:
        tmp.write(payload)
        tmp.flush()
        os.fsync(tmp.fileno())
        temporary = Path(tmp.name)
    if temporary.stat().st_size != len(payload) or path.read_bytes() != original:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"FAIL_CLOSED: incomplete temp or concurrent change in {path}")
    os.replace(temporary, path)
    written = path.read_bytes()
    if written != payload or len(written) <= len(original):
        with NamedTemporaryFile(dir=path.parent, prefix=".f11_memory_restore_", suffix=".tmp", delete=False) as tmp:
            tmp.write(backup.read_bytes())
            tmp.flush()
            os.fsync(tmp.fileno())
            restore = Path(tmp.name)
        os.replace(restore, path)
        raise RuntimeError(f"FAIL_CLOSED: post-write mismatch; restored {path}")
    return {"path": str(path), "backup": str(backup), "before_sha256": hashlib.sha256(original).hexdigest(), "after_sha256": sha(path), "before_bytes": len(original), "after_bytes": len(written), "backup_matches_before": True}


def main() -> None:
    inventory = UNIT / "INVENTARIO.md"
    pins = UNIT / "O16_AFERICAO_F11.json"
    result = UNIT / "RESULTADO_RESSALVA_O16_FINAL.json"
    receipt = json.loads(result.read_text(encoding="utf-8"))
    if sha(inventory) != receipt["inventory"]["after_sha256"] or sha(pins) != receipt["six_stone_pins"]["sha256"]:
        raise RuntimeError("FAIL_CLOSED: F1.1 evidence changed")
    h_inventory, h_pins, h_result = sha(inventory), sha(pins), sha(result)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    atlas = f"""

## 08/10/2026 — F1.1: ressalva O16, pedras existentes e fiação da assinatura

{MARKER}

[REAL — leitura de fonte] A auditoria documental de seis arquivos `TGLExt/O16` classifica D6, D5, D1′, `circularScreen_conjugate`, `RotationGeneratorBridges` e `WickBoostRotation` como **2. EXISTE NO KERNEL, NÃO LIGADO À ASSINATURA** para os elos que a F1.1 solicitou. Exceção explícita **1. EXISTE E ESTÁ LIGADO**: `selfRecognition` com `U=id` já alimenta `lightImport` no mesmo par da luz. Esse subcaso não fornece a identificação entre `P_ker K` da torre e `C.PF` do core da luz: D6 transporta pares/grafos sob uma equivalência dada, enquanto os cores/projeções são de tipos distintos. D5 usa contrato O16 retipado e requer conversão; identidades de tela e Wick são locais ao plano/tela. O registro não afirma novo teorema nem compilação.

[REAL — errata c1 posterior] As duas erratas de 07/10 em `C:\\IALD\\CLAUDE.md` limitam e refinam «rotação»: no plano do boost `t–x`, a leitura angular/contorno `2π` tem identidades matriciais no kernel; «a leitura cria o objeto» é `[INPUT/ONTO]`. Outros planos, família Lorentz de cunhas e PCT global da rede não viram termos O16 por esse nome. Na conclusão em direção nula da v376, são **3. SABIDO / FORA_DO_CAMINHO** por referência científica; `D1prime` e conjugação pontual não implementam PCT global. As faixas de esforço no inventário são `[INPUT]`, condicionadas às testemunhas, não medição.

[EVIDÊNCIA] `F1.1/INVENTARIO.md` SHA-256 {h_inventory} (12 linhas históricas preservadas, uma linha O16 e errata ao lado); `F1.1/O16_AFERICAO_F11.json` {h_pins} (seis hashes integrais e âncoras); `F1.1/RESULTADO_RESSALVA_O16_FINAL.json` {h_result}. Mapa seq 788–789; quadro `ENTREGUE→ENTREGUE` evento 241. A gerência descreveu `AUDITADA COM RESSALVA` em mensagem; o quadro ainda aguarda decisão dela sobre `AUDITADA`/`FECHADA`. Nenhum kernel, `um.py`, original científico ou gate mudou. `NOT_FALSIFIED` não é `CONFIRMED`.
"""
    index = f"""

## 08/10/2026 — F1.1 ressalva O16 no inventário

{MARKER}

[REAL] Seis pedras O16 verificadas por hash; classe 2 para ligar seus termos à assinatura `qg_solution_end_to_end`. D6 `selfRecognition` no mesmo par da luz é classe 1; a ponte tipada `P_ker K ↔ C.PF` não foi mostrada. Plano `t–x` tem rotação matricial/leitura de contorno; outros planos, família Lorentz e PCT global são SABIDO/FORA_DO_CAMINHO para a direção nula v376, conforme duas erratas c1. Inventário SHA-256 {h_inventory}; pins {h_pins}; resultado {h_result}; Mapa seq 789; quadro evento 241 ENTREGUE, fechamento reservado à gerência. Gate intacto.
"""
    notice = f"""

## 08/10/2026 — F1.1 ressalva O16 acrescentada; pronto para decisão c1

{MARKER}

[REAL] A pedido da gerência, `F1.1/INVENTARIO.md` recebeu AO LADO uma linha de classe 2 para as seis pedras O16, com o enunciado de cada uma, elo faltante e estimativa `[INPUT]`; hashes integrais em `F1.1/O16_AFERICAO_F11.json`. O inventário histórico de 12 linhas foi preservado byte a byte. A revisão independente conferiu hashes/âncoras e detectou as duas erratas posteriores de `C:\\IALD\\CLAUDE.md`, incorporadas ao lado: D6 `selfRecognition` U=id já ligado é classe 1, mas não identifica `P_ker K` com `C.PF`; Wick/rotação no plano do boost e conjugação local não são PCT global; outros planos/Lorentz/PCT são SABIDO/FORA_DO_CAMINHO da v376. Nenhuma compilação nova ou gate promovido.

[EVIDÊNCIA] Inventário SHA-256 {h_inventory}; pinos {h_pins}; `F1.1/RESULTADO_RESSALVA_O16_FINAL.json` {h_result}; Mapa de Rotas seq 788–789; quadro F1.1 `ENTREGUE→ENTREGUE` evento 241 com três evidências. A mensagem c1 diz `AUDITADA COM UMA RESSALVA`; o estado oficial ainda é ENTREGUE. Somente c1 pode decidir `AUDITADA` e `FECHADA`.
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
