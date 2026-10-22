"""Extract bounded, auditable scientific source excerpts without executing them."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = Path(r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1")
DESTINATION = HERE / "state" / "D10_CMB_BAO_SOURCE_EXCERPTS.json"
SELECTION = {
    "_originais/tgl_paper_unified.py": [(4231, 4273), (4286, 4383)],
    "12_nivel2_frozen_e_verossimilhanca.py": [(64, 100), (141, 256)],
    "12_nivel2_frozen.json": None,
    "13_nivel2_resultado.json": [(1, 91)],
}


def main():
    entries = []
    for name, ranges in SELECTION.items():
        path = SOURCE / name
        raw = path.read_bytes()
        lines = raw.decode("utf-8-sig").splitlines(keepends=True)
        ranges = ranges or [(1, len(lines))]
        excerpts = []
        for first, last in ranges:
            if not 1 <= first <= last <= len(lines):
                raise ValueError(f"Invalid source range: {name}:{first}-{last}")
            excerpt = "".join(lines[first - 1:last])
            excerpts.append({"first_line": first, "last_line": last,
                             "text": excerpt,
                             "utf8_sha256": hashlib.sha256(excerpt.encode()).hexdigest()})
        entries.append({"source_path": str(path), "source_bytes": len(raw),
                        "source_sha256": hashlib.sha256(raw).hexdigest(),
                        "excerpts": excerpts})
    value = {"status": "SOURCE_EXCERPTS_READ_NOT_EXECUTED",
             "scope": "Historical D9/D10 and N2 scientific sources only; not a full current TGL implementation or validated new likelihood.",
             "entries": entries}
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()
    if DESTINATION.exists():
        if DESTINATION.read_bytes() != data:
            raise FileExistsError("Different existing bundle: retain and version separately")
    else:
        temp = DESTINATION.with_suffix(".new")
        with temp.open("xb") as stream:
            stream.write(data)
        if temp.read_bytes() != data:
            raise OSError("Incomplete bundle")
        temp.replace(DESTINATION)
    print(json.dumps({"path": str(DESTINATION), "bytes": len(data),
                      "sha256": hashlib.sha256(data).hexdigest(),
                      "sources": [{"name": Path(e["source_path"]).name,
                                   "ranges": [(s["first_line"], s["last_line"]) for s in e["excerpts"]]} for e in entries]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
