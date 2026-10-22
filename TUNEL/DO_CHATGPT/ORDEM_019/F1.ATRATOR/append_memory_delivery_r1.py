"""Append only to the three surfaces named in claim 664, with byte backups."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess

BASE = Path(__file__).resolve().parent
MEMORY = Path(r"C:\IALD\Central de Patentes\memory")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def exclusive(path, data):
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert path.read_bytes() == data


def main():
    receipt_path = BASE / "MEMORY_APPEND_R1.json"
    journal_path = BASE / "MEMORY_APPEND_JOURNAL_R1.jsonl"
    assert not receipt_path.exists() and not journal_path.exists(), "Do not repeat a partial memory append"
    board = subprocess.run([r"C:\Python314\python.exe", "-B", "-X", "utf8", r"C:\IALD\PROGRAMA_IALD\iald.py", "ver", "F1.ATRATOR"], capture_output=True, check=True)
    claim = json.loads(board.stdout)["reivindicacao"]
    assert claim["quem"] == "codex-gerente-tgl"
    assert datetime.datetime.fromisoformat(claim["vence_em"]) > datetime.datetime.now(datetime.timezone.utc)
    result_path = BASE / "RESULTADO_F1_ATRATOR_R1.json"
    result_bytes = result_path.read_bytes()
    result = json.loads(result_bytes)
    assert result["verdict"] == "PASSA_NO_ESCOPO_MATEMATICO_PREREGISTRADO"
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    marker = "<!-- F1_ATRATOR_ENTREGA_R1_20261010 -->"
    text = f"""\n\n## 10/10/2026 — F1.ATRATOR: leitura do atrator, entrega de sandbox
{marker}
Autor: codex-gerente-tgl, sob reivindicação F1.ATRATOR nº 664, que nomeia Atlas, Índice Vivo e TGL_CORE_MEMORY. Correção de leituras anteriores permanece ao lado; nenhum original científico foi alterado.

[REAL] Pré-registro por hash antes do ensaio e compilação. A1–A4 PASSA no canal sintético C=𝒟∘Ad(S)∘𝒟/populações |S|², com β=ALPHA_FINE_CODATA_2018·√e calculado em runtime. A1 forte na família espectral, Cesàro no Hilbert geral; RT=TR=R; R²=R e R=starProjection(Fix T); dimensão fixa 1 sob contração estrita no complemento de e≠0 fixo. A leitura via letra usa A=I−T e q(A)/q(0), reaproveitando ExactWitness/WordExistence. O nome PALAVRA está em candidata work, não em módulo instalado no kernel consultado.

[REAL] Principal Lean 4.31, EXIT 0, 20 teoremas/14 impressões; ponte matricial, EXIT 0, 15/15. Só propext, Classical.choice, Quot.sound; zero sorry. Revisão independente numérica e formal com recompilação: ver arquivos review/REVISAO_* no pacote. Identidade e dephasing conjugado exibem dimensão 2 sem hipótese; x↦x+1 não tem ponto fixo e falha A1, declarado fora de CPTP finito. Habitante formal em ℂ² com λ=1/2 não é β literal; aplicação óptica é paramétrica. Resíduos float64 finais ~5,34e−13/9,09e−13; Cesàro em 4096≈0,010146 segue cota O(1/N).

[DERIVED] β determina a taxa de relaxação nesta família; R sozinho não discrimina β. A ponte matricial é exata, sem alegar novo transporte CLM completo. [ONTO] A cunhagem da singularidade como leitura permanece ontológica. PASSA é validade no escopo, sem creditação física ou sigma observado. O agregado numérico R3 documenta o controle afim analiticamente; revisão iterou a recorrência e a ponte Lean prova ausência de ponto fixo.

Reaproveitamento: mapa seq 1000/pre-registro, MeanErgodic, SMatrix, GlobalLiftLadder, fluxo P+exp(−t)(I−P), pilar GKLS v384/v385 arquivado. Evidência nova: {result_path}; SHA256 {sha(result_bytes)}. Relatório: RELATORIO_F1_ATRATOR_R1.md. Recebe auditoria da c1; esta escrita não declara FECHADA. Integração no um.py fica para o apanhado geral. Nós, um.py, produção, dado observado e gate não foram modificados por esta unidade.
"""
    rows = []
    with journal_path.open("xb") as journal:
        for name in ("TGL_ATLAS.md", "TGL_INDICE_VIVO.md", "TGL_CORE_MEMORY.md"):
            path = MEMORY / name
            before = path.read_bytes()
            assert marker.encode() not in before, f"Marker already present: {path}"
            backup = path.with_name(path.name + ".bak_" + stamp)
            exclusive(backup, before)
            newline_text = text.replace("\n", "\r\n") if b"\r\n" in before else text
            after = before + newline_text.encode("utf-8")
            temporary = path.with_name(path.name + ".tmp_F1_ATRATOR_" + stamp)
            exclusive(temporary, after)
            assert path.read_bytes() == before, "Concurrent memory modification; preserved backup/temp"
            os.replace(temporary, path)
            actual = path.read_bytes()
            assert actual == after and actual.startswith(before) and len(actual) > len(before)
            row = {"path": str(path), "backup": str(backup), "before_sha256": sha(before), "after_sha256": sha(actual), "before_bytes": len(before), "after_bytes": len(actual), "pure_append": True}
            rows.append(row)
            journal.write((json.dumps(row, ensure_ascii=False) + "\n").encode())
            journal.flush()
            os.fsync(journal.fileno())
    receipt = {"unit": "F1.ATRATOR", "claim": 664, "author": "codex-gerente-tgl", "at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "result_sha256": sha(result_bytes), "surfaces": rows}
    exclusive(receipt_path, (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode())
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == "__main__":
    main()
