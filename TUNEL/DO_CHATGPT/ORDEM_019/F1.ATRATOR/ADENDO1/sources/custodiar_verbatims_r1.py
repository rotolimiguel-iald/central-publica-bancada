"""Custody four authorized verbatims without changing source bytes or running tests."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import unicodedata

BASE = Path(__file__).resolve().parent
SOURCES = [
    (Path(r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_singularidade_verbatim.txt"), "1d9dd9a65fdacf68"),
    (Path(r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_TGL_unidade_verbatim.txt"), "87a3752d8c8e5dd3"),
    (Path(r"C:\IALD\Central de Patentes\work\f9_pergunta_08out\OPERADOR_08out_resposta_verbatim.txt"), "a9cecc12"),
    (Path(r"C:\IALD\PROGRAMA_IALD\OPERADOR_07out_leitura_cria_o_objeto_verbatim.txt"), "f2a4b509946edc05"),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save_new(path, data):
    with path.open("xb") as stream:
        stream.write(data)
    assert path.read_bytes() == data


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def main():
    started = datetime.now(timezone.utc).isoformat()
    names = [p.name for p, _ in SOURCES] + [
        "CUSTODIA_VERBATIMS_R1.json", "RELATORIO_CUSTODIA_R1.md",
        "VERBATIMS_DOCSTRING_FRAGMENT_R1.txt", "FINAL_SOURCES_RECEIPT_R1.json",
    ]
    for name in names:
        if (BASE / name).exists():
            raise FileExistsError(BASE / name)
    entries = []
    for number, (source, expected_prefix) in enumerate(SOURCES, 1):
        raw = source.read_bytes()
        digest = sha(raw)
        if not digest.startswith(expected_prefix):
            raise ValueError(f"SHA-256 mismatch: {source}")
        text = raw.decode("utf-8", errors="strict")
        if text.encode("utf-8") != raw:
            raise ValueError(f"UTF-8 roundtrip failed: {source}")
        if "/-" in text or "-/" in text or "\x00" in text:
            raise ValueError(f"Unsafe Lean comment delimiter or NUL: {source}")
        entry = {
            "id": f"V{number}", "source": str(source),
            "custody": str(BASE / source.name), "sha256": digest,
            "expected_sha_prefix": expected_prefix, "prefix_matches": True,
            "bytes": len(raw), "unicode_codepoints": len(text),
            "encoding": "UTF-8, strict decode", "utf8_bom": raw.startswith(b"\xef\xbb\xbf"),
            "crlf_count": raw.count(b"\r\n"),
            "lf_only_count": raw.count(b"\n") - raw.count(b"\r\n"),
            "bare_cr_count": raw.count(b"\r") - raw.count(b"\r\n"),
            "ends_with_newline": raw.endswith(b"\n"),
            "nul_count": raw.count(b"\x00"),
            "lean_comment_open_count": text.count("/-"),
            "lean_comment_close_count": text.count("-/"),
            "max_backtick_run": max((len(x) for x in re.findall(r"`+", text)), default=0),
            "is_nfc": text == unicodedata.normalize("NFC", text),
            "normalization_applied": False,
            "verbatim_utf8": text,
        }
        entries.append((entry, raw))
    # All inputs validated before any custody file is created.
    for entry, raw in entries:
        save_new(Path(entry["custody"]), raw)

    report = bytearray((
        "# F1.ATRATOR — ADENDO1: custódia integral das quatro cunhagens\n\n"
        "[REAL — custódia documental] Bytes lidos das quatro fontes autorizadas e copiados "
        "sem alteração. Os quatro prefixos SHA-256 conferem. Todos os textos decodificam "
        "estritamente em UTF-8, sem BOM; nenhum contém os delimitadores de comentário Lean "
        "`/-` ou `-/`, NUL ou crases. Não foi aplicada normalização Unicode nem de fim de linha.\n\n"
        "[ONTO — conteúdo das cunhagens] A reprodução integral abaixo preserva a palavra "
        "do operador; a custódia não promove seus enunciados a resultados matemáticos. "
        "Esta etapa não executa A5/A6.\n\n"
        "## Inserção no pré-registro, na pedra e no relatório\n\n"
        "A inclusão integral é viável em Markdown UTF-8 e em comentário de documentação "
        "Lean UTF-8. O fragmento vizinho usa `/-! ... -/`, sem declarações Lean. "
        "É uma verificação de texto e delimitadores; a compilação cabe à montagem da pedra. "
        "Os campos `verbatim_utf8` no JSON reconstituem os bytes originais por UTF-8. "
        "As cópias `.txt` são a custódia byte a byte. Os offsets no JSON delimitam cada "
        "original dentro deste relatório e do fragmento; a extração por esses offsets "
        "reproduz o SHA-256 da fonte. A quebra de linha que separa um original sem LF final "
        "do fechamento da cerca/comentário é formatação externa e fica fora do intervalo.\n\n"
        "| Fonte | Bytes | LF | LF final | SHA-256 |\n"
        "|---|---:|---:|---|---|\n"
    ).encode("utf-8"))
    for entry, _ in entries:
        report.extend(f"| {entry['id']} — {Path(entry['source']).name} | {entry['bytes']} | {entry['lf_only_count']} | {'sim' if entry['ends_with_newline'] else 'não'} | `{entry['sha256']}` |\n".encode("utf-8"))
    fragment = bytearray((
        "/-!\n# Cunhagens integrais — F1.ATRATOR, ADENDO1\n\n"
        "[ONTO] Palavra do operador, integral e custodiada por SHA-256. "
        "O comentário não atribui ao kernel a prova do conteúdo ontológico.\n"
    ).encode("utf-8"))
    for entry, raw in entries:
        report.extend(f"\n## {entry['id']} — {Path(entry['source']).name}\n\nFonte: `{entry['source']}`\n\nSHA-256: `{entry['sha256']}`\n\n```text\n".encode("utf-8"))
        start = len(report)
        report.extend(raw)
        entry["report_original_byte_range"] = [start, len(report)]
        if not raw.endswith(b"\n"):
            report.extend(b"\n")
        report.extend(b"```\n")
        fragment.extend(f"\n## {entry['id']} — {Path(entry['source']).name}\nFonte: {entry['source']}\nSHA-256: {entry['sha256']}\n\n".encode("utf-8"))
        start = len(fragment)
        fragment.extend(raw)
        entry["lean_fragment_original_byte_range"] = [start, len(fragment)]
        if not raw.endswith(b"\n"):
            fragment.extend(b"\n")
    fragment.extend(b"-/\n")
    for entry, raw in entries:
        a, b = entry["report_original_byte_range"]
        c, d = entry["lean_fragment_original_byte_range"]
        assert bytes(report[a:b]) == raw == bytes(fragment[c:d])
        assert Path(entry["source"]).read_bytes() == raw
    save_new(BASE / "RELATORIO_CUSTODIA_R1.md", bytes(report))
    save_new(BASE / "VERBATIMS_DOCSTRING_FRAGMENT_R1.txt", bytes(fragment))
    metadata = {
        "schema": "F1.ATRATOR.ADENDO1.verbatim-custody/v1",
        "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
        "claim": 668, "statute": "REAL: byte custody; ONTO: quoted conceptual content",
        "scope": "sources only; no A5/A6 run; no scientific or memory originals changed",
        "offset_convention": "zero-based half-open UTF-8 byte ranges [start,end)",
        "sources": [entry for entry, _ in entries],
    }
    save_new(BASE / "CUSTODIA_VERBATIMS_R1.json", json_bytes(metadata))
    artifacts = []
    for name in names[:-1] + [Path(__file__).name]:
        path = BASE / name
        raw = path.read_bytes()
        artifacts.append({"path": str(path), "bytes": len(raw), "sha256": sha(raw)})
    receipt = {
        "schema": "F1.ATRATOR.ADENDO1.source-receipt/v1", "finished_utc": datetime.now(timezone.utc).isoformat(),
        "verdict": "PASSA_CUSTODIA_INTEGRAL_4_FONTES", "sources_rechecked_after_write": True,
        "verbatim_report_and_lean_fragment_ranges_verified": True,
        "artifacts": artifacts,
    }
    save_new(BASE / "FINAL_SOURCES_RECEIPT_R1.json", json_bytes(receipt))
    print(json.dumps({"verdict": receipt["verdict"], "receipt": str(BASE / "FINAL_SOURCES_RECEIPT_R1.json"), "sha256": sha((BASE / "FINAL_SOURCES_RECEIPT_R1.json").read_bytes()), "sources": [{k:e[k] for k in ("id","bytes","sha256")} for e,_ in entries]},ensure_ascii=False))


if __name__ == "__main__":
    main()
