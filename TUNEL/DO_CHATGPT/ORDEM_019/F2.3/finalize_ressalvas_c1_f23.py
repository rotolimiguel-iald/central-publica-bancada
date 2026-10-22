"""Create immutable F2.3 c1 correction receipts and map input."""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path

UNIT = Path(__file__).resolve().parent
AUDIT1 = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F2.3\AUDITORIA_F2_3_C1_20261007.md")
AUDIT2 = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F2.3_F7.2_adendos\AUDITORIA_F2_3_F7_2_adendos_C1_ae22d8a4.md")
SOURCE = UNIT / "LiganteLeiCampoCurvo.lean"
NEW = UNIT / "LiganteLeiCampoCurvoAuditoriaC1.lean"
KERNEL_COPY = UNIT / "kernel" / "TGLExt" / "LiganteLeiCampoCurvoAuditoriaC1.lean"
OLEAN = UNIT / "LiganteLeiCampoCurvoAuditoriaC1.olean"
LOG = UNIT / "BUILD_AUDITORIA_C1_FINAL_20261008.log"
FAILED_NEW = UNIT / "BUILD_AUDITORIA_C1_20261008.log"
FAILED = UNIT / "BUILD_FIRST_ATTEMPT.log"
MEMORY = UNIT / "MEMORIA_RESSALVAS_C1_F23_20261008.json"
MANIFEST = UNIT / "HASHES_RESSALVAS_C1_F23_20261008.json"
RESULT = UNIT / "RESULTADO_RESSALVAS_C1_F23_20261008.json"
MAP = UNIT / "MAPA_RESSALVAS_C1_F23_20261008.json"


def art(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": sha256(data).hexdigest()}


def new_json(path: Path, value: dict) -> dict:
    encoded = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with path.open("xb") as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())
    if path.read_bytes() != encoded:
        raise OSError(f"written JSON differs: {path}")
    return art(path)


def remove_first_docstring(data: bytes) -> bytes:
    begin = data.index(b"/-!")
    end = data.index(b"-/", begin) + 2
    return data[:begin] + data[end:]


def main() -> None:
    if MANIFEST.exists() or RESULT.exists() or MAP.exists():
        raise RuntimeError("immutable correction evidence already exists")
    if remove_first_docstring(SOURCE.read_bytes()) != remove_first_docstring(NEW.read_bytes()):
        raise RuntimeError("new Lean version changed more than the docstring")
    if KERNEL_COPY.read_bytes() != NEW.read_bytes():
        raise RuntimeError("sandbox source copy differs")
    doc = NEW.read_text(encoding="utf-8").split("-/", 1)[0]
    for term in ("S2–S4", "Jacobson", "Lorentz wedge", "StressTensorData", "MaxwellCertificate", "metric or solution"):
        if term not in doc:
            raise RuntimeError(f"scope limit missing from new docstring: {term}")
    build = LOG.read_text(encoding="utf-8")
    for term in ("toolchain", "LEAN_PATH=", "command=", "exit_code", "elapsed"):
        if term not in build:
            raise RuntimeError(f"actual build log missing: {term}")
    if not any(line.startswith("exit_code") and line.split("=", 1)[-1].strip() == "0" for line in build.splitlines()):
        raise RuntimeError("build exit is not zero")
    if "[propext, Classical.choice, Quot.sound]" not in build or "passage_h3_to_connected_smooth_atlas_einstein" not in build:
        raise RuntimeError("axiom transcript absent")
    if art(FAILED)["sha256"] != "832d445f29976fa43ddef68e314387a33ca865e98806d754190e4484614a50bb":
        raise RuntimeError("first failed attempt changed")
    if art(AUDIT1)["sha256"] != "f718620ec89c61d408ba9bf03ac0cfc1b53f31aa6486f57fae41d183e3a86624":
        raise RuntimeError("c1 audit changed")
    memory = json.loads(MEMORY.read_text(encoding="utf-8"))
    if memory["memory_claim_event"] != 306 or len(memory["rows"]) != 4:
        raise RuntimeError("memory receipt incomplete")
    files = [SOURCE, NEW, KERNEL_COPY, OLEAN, LOG, FAILED_NEW, FAILED, MEMORY, AUDIT1, AUDIT2,
             UNIT / "BUILD.log", UNIT / "AXIOMAS.txt"]
    artifacts = [art(path) for path in files]
    manifest = new_json(MANIFEST, {"schema": "iald.f2_3.c1_corrections.hashes.v1", "unit": "F2.3",
                                   "algorithm": "sha256_bytes", "artifacts": artifacts})
    result = new_json(RESULT, {
        "schema": "iald.f2_3.c1_corrections.v1", "unit": "F2.3",
        "time_utc": datetime.now(timezone.utc).isoformat(), "status": "ENTREGUE_PARA_REAUDITORIA_C1",
        "already_exists": "Original branch C theorem audited by c1, event 262 and map seq 804; later RamoC and Temperatura are separate audited additions.",
        "corrections": [
            "Actual fresh build log for the docstring-only Lean version: command, toolchain, literal LEAN_PATH, elapsed time, exit 0 and axiom transcript.",
            "Historical first failed build attempt and the new path-related failed attempt pinned separately, without overwriting the old 255-byte BUILD.log and AXIOMAS.txt.",
            "Four Central memory surfaces corrected beside the prior text with immediate byte backups; historical independent-review claim marked DECLARADO; c1 S2-S4 and map seq 804 recorded after claiming memory unit F0.3 event 306.",
            "New Lean docstring names all five scope limits. No original theorem body or import changed."
        ],
        "scope": {"H3": "named input", "foundation_passage": "logically idle by c1 S2-S4",
                  "global_solution": False, "kernel_changed": False, "um_py_changed": False, "gate_effect": "NONE"},
        "memory_board_events": [306, 307, 308], "original_audit_event": 262,
        "original_audit_map_seq": 804, "artifacts": artifacts + [manifest]
    })
    entry = {
        "tipo": "ANOTACAO", "rota_id": "formal.f2_3.curved_field_ligand", "dominio": "FORMAL",
        "titulo": "F2.3: ressalvas c1 escrituradas com build completo, memória e docstring",
        "pergunta": "O recibo da pedra auditada explicita o build real, a tentativa falha, a ociosidade da passagem e os limites do enunciado?",
        "dados": ["Auditoria c1 seq 804 e sondas S2–S4", "build novo da cópia com docstring, sem alterar o corpo", "quatro erratas de memória após reivindicação F0.3"],
        "metodo": "Hash de bytes dos originais; comparação da fonte Lean removendo só a primeira docstring; build em sandbox; backups de bytes e append atômico; recibos imutáveis.",
        "resultado": "Log registra comando, toolchain, LEAN_PATH literal, exit e duração; tentativas falhas pinadas. A docstring declara as cinco limitações e a passagem ociosa. Memórias classificam a antiga alegação de revisão como DECLARADO e citam a auditoria c1 seq 804.",
        "veredito": "F23_C1_R1_R3_DOCUMENTED__PASSAGE_IDLE__NAMED_H3__GATE_NONE",
        "estatuto": "REAL documental e build; INPUT H3; KNOWN identificação física com Jacobson; OPEN realização",
        "status": "EXAMINADA_COM_DEFEITO", "olhou_dados": False,
        "defeito": "O H3 não foi derivado do estado ou da Fundação; a identidade com o H3 físico não é teorema nesta pedra. A integração canônica permanece com a c1.",
        "nao_refazer": "Não repetir sondas S2–S8 nem builds posteriores do Ramo C e da Temperatura; não editar os originais já pinados.",
        "proximo_passo": "c1 reaudita esta camada documental e decide a integração v392 da pedra auditada.",
        "onde": str(UNIT), "artefatos": [result, manifest, art(NEW), art(LOG), art(FAILED_NEW), art(FAILED), art(MEMORY)],
        "refs": ["formal.f2_3.curved_field_ligand"], "nota": "Sem dado real, kernel, um.py ou gate alterado."
    }
    map_art = new_json(MAP, entry)
    print(json.dumps({"manifest": manifest, "result": result, "map_input": map_art}, ensure_ascii=False))


if __name__ == "__main__":
    main()
