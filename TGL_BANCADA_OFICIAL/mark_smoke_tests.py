"""Annotate the first HTTP smoke tests and append the lexical-search correction."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

import app

EXPECTED = {
    1: "Ward e GWOSC",
    2: "O ringdown GWTC3",
}


def main() -> None:
    app.initialize_db()
    index = app.load_index()
    backup = app.DB.with_name(app.DB.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    with sqlite3.connect(app.DB) as source, sqlite3.connect(backup) as dest:
        source.backup(dest)
    with sqlite3.connect(app.DB) as conn:
        conn.row_factory = sqlite3.Row
        old = {}
        for inquiry_id, prefix in EXPECTED.items():
            row = conn.execute("SELECT * FROM inquiries WHERE id=?", (inquiry_id,)).fetchone()
            if row is None or not row["question"].startswith(prefix):
                raise ValueError(f"Smoke-test record #{inquiry_id} differs; no annotation written")
            old[inquiry_id] = row
        old_result = json.loads(old[2]["result_json"])
        if old_result["formal_total"] != len(index["modules"]):
            raise ValueError("The expected lexical-search defect is absent; no erratum written")
        existing = conn.execute("SELECT related_inquiry_id FROM inquiry_events WHERE inquiry_id=2 AND event_type='ERRATUM'").fetchone()
        if existing:
            print(f"Erratum already recorded: #2 → #{existing[0]}; backup {backup}")
            return
        revised = app.investigate(index, {
            "question": old[2]["question"], "hypothesis": old[2]["hypothesis"],
            "falsifier": old[2]["falsifier"],
            "alternative": "GR explica a forma de onda sem setor adicional",
            "instrumental": "A PSD ou calibracao gera desvio aparente",
            "discriminator": "Comparar previsoes e incertezas por evento e detector",
        })
        if revised["formal_total"] >= len(index["modules"]) // 2:
            raise ValueError("Revised search still matches too much of the tower")
        with conn:
            cursor = conn.execute(
                "INSERT INTO inquiries(created_utc, question, hypothesis, falsifier, result_json, source_sha256, status) "
                "VALUES (?,?,?,?,?,?,?)",
                (app.utc_now(), revised["question"], revised["hypothesis"], revised["falsifier"],
                 json.dumps(revised, ensure_ascii=False), revised["source_sha256"], revised["status"]))
            corrected_id = cursor.lastrowid
            for inquiry_id in (1, 2, corrected_id):
                conn.execute("INSERT INTO inquiry_events(created_utc, inquiry_id, event_type, note, related_inquiry_id) "
                             "VALUES (?,?,?,?,NULL)",
                             (app.utc_now(), inquiry_id, "SMOKE_TEST",
                              "Registro criado para verificar a interface; não é análise física."))
            conn.execute("INSERT INTO inquiry_events(created_utc, inquiry_id, event_type, note, related_inquiry_id) "
                         "VALUES (?,?,?,?,?)",
                         (app.utc_now(), 2, "ERRATUM",
                          "A palavra genérica TGL fez a busca antiga corresponder aos 1.018 módulos. A busca corrigida exclui esse termo do filtro lexical; o resultado anterior permanece para auditoria.",
                          corrected_id))
    print(f"Annotated smoke tests; erratum #2 → #{corrected_id}; corrected formal matches={revised['formal_total']}; backup {backup}")


if __name__ == "__main__":
    main()
