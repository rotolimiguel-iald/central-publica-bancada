"""Bounded, read-only exploration of installed scientific files.

No scientific source is copied or imported as executable code. FITS tables are read
by their published binary layout, using only the standard library.
"""

from __future__ import annotations

import csv
import ast
import ctypes
import hashlib
import math
import re
import struct
from pathlib import Path

import hdf5_bridge


ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
BAO_ROOT = Path(r"C:\IALD\Artigo\frente_alpha")
BAO_MEAN = "desi_gaussian_bao_ALL_GCcomb_mean.txt"
BAO_COV = "desi_gaussian_bao_ALL_GCcomb_cov.txt"
SOURCES = (
    ("DESI BAO: média e covariância", BAO_ROOT),
    ("UM: cache científica canônica", Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache")),
    ("UM: cache local da edição viva", Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\cache")),
    ("Snapshot v350: cache científica", ROOT / "TETELESTAI_V350_KERNEL_20260911" / "r" / "cache"),
    ("GWOSC: strain", ROOT / "ORDEM_013_RINGDOWN" / "cache" / "gwosc"),
    ("GW: posteriores públicos", ROOT / "ORDEM_013_RINGDOWN" / "cache" / "public"),
    ("GW: strain da bancada 013BIS", ROOT / "ORDEM_013_RINGDOWN" / "bis" / "015" / "t07" / "strain"),
    ("GWTC-3: leituras", ROOT / "ORDEM_013_RINGDOWN" / "C7_GWTC3_REPRODUCTION_v3_2" / "evidence"),
)
EXTENSIONS = {".fits", ".csv", ".dat", ".txt", ".npy", ".npz", ".h5", ".hdf5"}
MAX_FILES = 3000
MAX_POINTS = 1200


class _MemoryStatus(ctypes.Structure):
    _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong),
                ("total_phys", ctypes.c_ulonglong), ("avail_phys", ctypes.c_ulonglong),
                ("total_page", ctypes.c_ulonglong), ("avail_page", ctypes.c_ulonglong),
                ("total_virtual", ctypes.c_ulonglong), ("avail_virtual", ctypes.c_ulonglong),
                ("avail_extended", ctypes.c_ulonglong)]


def memory_status() -> dict:
    status = _MemoryStatus()
    status.length = ctypes.sizeof(status)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
        raise OSError("Windows memory status unavailable")
    # The cap is a conservative interactive default, not a hardware limit.
    suggested = min(64 * 1024**3, int(status.avail_phys * 0.35))
    return {"total_bytes": status.total_phys, "available_bytes": status.avail_phys,
            "interactive_budget_bytes": suggested, "browser_point_limit": MAX_POINTS,
            "policy": "Leitura por metadados e amostragem limitada; arquivos permanecem em disco."}


def file_id(path: Path) -> str:
    return hashlib.sha256(str(path).encode("utf-8")).hexdigest()[:24]


def catalog() -> list[dict]:
    results = []
    seen = set()
    for label, root in SOURCES:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if len(results) >= MAX_FILES:
                return results
            if path.suffix.lower() not in EXTENSIONS or path.is_symlink() or not path.is_file():
                continue
            # Exclude duplicate nested delivery/reproduction trees and private cache.
            parts = {part.lower() for part in path.relative_to(root).parts}
            if "e2_private" in parts or "vendor" in parts or "delivery_v2_fresh_20260922_032436_194092" in parts:
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            try:
                size = path.stat().st_size
            except OSError:
                continue
            if root == BAO_ROOT and path.name not in (BAO_MEAN, BAO_COV):
                continue
            results.append({"id": file_id(resolved), "name": path.name, "path": str(resolved),
                            "group": label, "bytes": size, "format": path.suffix.lower(),
                            "interactive": (path.suffix.lower() in {".fits", ".csv", ".dat", ".txt", ".npy", ".h5", ".hdf5"}
                                            and path.name != BAO_COV),
                            "status": "INSTALLED_SOURCE_NOT_VALIDATED"})
    return sorted(results, key=lambda item: (item["group"], -item["bytes"], item["name"]))


def selected(identifier: str) -> Path:
    if not re.fullmatch(r"[0-9a-f]{24}", identifier):
        raise ValueError("Invalid data identifier")
    for item in catalog():
        if item["id"] == identifier:
            return Path(item["path"])
    raise ValueError("Data source not found in allowlisted catalog")


def _fits_header(source) -> tuple[dict, int]:
    cards = []
    while True:
        block = source.read(2880)
        if len(block) != 2880:
            raise ValueError("Incomplete FITS header")
        for offset in range(0, 2880, 80):
            card = block[offset:offset + 80].decode("ascii", "replace")
            if card[:8].strip() == "END":
                data = {}
                for raw in cards:
                    if raw[8:10] == "= ":
                        value = raw[10:80].split("/", 1)[0].strip()
                        data[raw[:8].strip()] = value.strip("'").strip()
                return data, source.tell()
            cards.append(card)
        if len(cards) > 100000:
            raise ValueError("FITS header too large")


def _fits_table(path: Path) -> dict:
    with path.open("rb") as source:
        for _ in range(16):
            header, start = _fits_header(source)
            if header.get("XTENSION", "").strip() == "BINTABLE":
                width = int(header["NAXIS1"])
                rows = int(header["NAXIS2"])
                if width <= 0 or rows < 0:
                    raise ValueError("Invalid FITS table dimensions")
                offset = 0
                columns = []
                size_map = {"A": 1, "L": 1, "B": 1, "I": 2, "J": 4, "K": 8,
                            "E": 4, "D": 8, "C": 8, "M": 16, "P": 8, "Q": 16, "X": 0}
                for n in range(1, int(header.get("TFIELDS", "0")) + 1):
                    form = header.get(f"TFORM{n}", "")
                    match = re.fullmatch(r"(\d*)([ALBIJKEDCMPQX])", form)
                    if not match:
                        raise ValueError(f"Unsupported FITS field layout: {form}")
                    repeat, kind = int(match.group(1) or "1"), match.group(2)
                    name = header.get(f"TTYPE{n}", f"COL{n}")
                    size = math.ceil(repeat / 8) if kind == "X" else repeat * size_map[kind]
                    if repeat == 1 and kind in "BIJKED":
                        columns.append({"name": name, "offset": offset, "kind": kind,
                                        "unit": header.get(f"TUNIT{n}", "")})
                    offset += size
                if offset > width:
                    raise ValueError("FITS columns exceed declared row width")
                return {"format": "FITS_BINTABLE", "start": start, "row_bytes": width,
                        "rows": rows, "columns": columns}
            axes = [int(header.get(f"NAXIS{i}", "0")) for i in range(1, int(header.get("NAXIS", "0")) + 1)]
            count = math.prod(axes) if axes else 0
            payload = (abs(int(header.get("BITPIX", "8"))) // 8) * count
            payload = (payload + int(header.get("PCOUNT", "0"))) * int(header.get("GCOUNT", "1"))
            source.seek(start + math.ceil(payload / 2880) * 2880)
    raise ValueError("No binary table in this FITS file; image/HEALPix adapter pending")


def _text_columns(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as source:
        lines = (line for line in source if line.strip() and not line.lstrip().startswith("#"))
        first = next(lines, "")
        if not first:
            raise ValueError("Empty text dataset")
        delim = "," if path.suffix.lower() == ".csv" else None
        cells = next(csv.reader([first])) if delim else first.split()
        numeric = all(_finite(value) is not None for value in cells)
        names = [f"col_{n+1}" for n in range(len(cells))] if numeric else [v.strip() for v in cells]
        return {"format": "CSV" if delim else "TEXT_TABLE", "columns":
                [{"name": name, "unit": ""} for name in names], "rows": None,
                "header": not numeric, "delimiter": delim}


def _bao_mean(path: Path) -> dict:
    measurements = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = line.split()
        if len(fields) != 3 or fields[2] not in ("DV_over_rs", "DM_over_rs", "DH_over_rs"):
            raise ValueError("Unexpected DESI BAO observation row")
        z, value = float(fields[0]), float(fields[1])
        if not math.isfinite(z) or not math.isfinite(value):
            raise ValueError("Nonfinite DESI BAO observation")
        measurements.append({"z": z, "value": value, "quantity": fields[2]})
    covariance_path = path.with_name(BAO_COV)
    covariance = []
    for line in covariance_path.read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.lstrip().startswith("#"):
            covariance.append([float(v) for v in line.split()])
    n = len(measurements)
    if n != 13 or len(covariance) != n or any(len(row) != n for row in covariance):
        raise ValueError("DESI BAO mean/covariance dimensions do not match 13 observations")
    for i in range(n):
        if not math.isfinite(covariance[i][i]) or covariance[i][i] <= 0:
            raise ValueError("DESI BAO covariance diagonal invalid")
        for j in range(i):
            if not math.isclose(covariance[i][j], covariance[j][i], rel_tol=1e-8, abs_tol=1e-10):
                raise ValueError("DESI BAO covariance is not symmetric")
        measurements[i]["sigma"] = math.sqrt(covariance[i][i])
    return {"format": "DESI_BAO_MEAN_WITH_COVARIANCE", "rows": n,
            "columns": [{"name": "z", "unit": "redshift"}, {"name": "value", "unit": "distance / sound horizon"}],
            "observations": measurements, "covariance": covariance,
            "covariance_path": str(covariance_path),
            "mean_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "covariance_sha256": hashlib.sha256(covariance_path.read_bytes()).hexdigest()}


def _npy_array(path: Path) -> dict:
    with path.open("rb") as source:
        magic = source.read(8)
        if len(magic) != 8 or magic[:6] != b"\x93NUMPY":
            raise ValueError("Invalid NPY magic")
        version = magic[6]
        if version not in (1, 2, 3):
            raise ValueError("Unsupported NPY version")
        size_bytes = 2 if version == 1 else 4
        length = int.from_bytes(source.read(size_bytes), "little")
        if length > 65536:
            raise ValueError("NPY header too large")
        header = ast.literal_eval(source.read(length).decode("latin1" if version < 3 else "utf-8"))
        dtype = header.get("descr")
        if not isinstance(dtype, str):
            raise ValueError("Structured/object NPY dtype not supported")
        match = re.fullmatch(r"([<>=|])([fiucb])(\d+)", dtype)
        if not match:
            raise ValueError(f"Unsupported NPY dtype: {dtype}")
        endian, kind, width_text = match.groups()
        width = int(width_text)
        if (kind == "f" and width not in (2, 4, 8)) or (kind in "iu" and width not in (1, 2, 4, 8)) or (kind == "c" and width not in (8, 16)) or (kind == "b" and width != 1):
            raise ValueError(f"Unsupported NPY value width: {dtype}")
        shape = header.get("shape")
        if not isinstance(shape, tuple) or len(shape) not in (1, 2) or any(not isinstance(v, int) or v < 0 for v in shape):
            raise ValueError("Only 1D/2D NPY arrays are previewable")
        rows, count = shape[0], (shape[1] if len(shape) == 2 else 1)
        if bool(header.get("fortran_order")):
            raise ValueError("Fortran-ordered NPY preview pending")
        required = rows * count * width
        if source.tell() + required > path.stat().st_size:
            raise ValueError("Truncated NPY data")
        columns = []
        if len(shape) == 1:
            columns.append({"name": "index", "unit": "row", "column": -1, "part": "index"})
        for col in range(min(count, 128)):
            name = "value" if len(shape) == 1 else f"col_{col}"
            if kind == "c":
                for part in ("real", "imag", "abs"):
                    columns.append({"name": f"{name}_{part}", "unit": "", "column": col, "part": part})
            else:
                columns.append({"name": name, "unit": "", "column": col, "part": "value"})
        return {"format": "NPY", "start": source.tell(), "rows": rows, "count": count,
                "width": width, "kind": kind, "endian": endian, "columns": columns,
                "shape": shape, "dtype": dtype}


def _npy_value(source, info: dict, row: int, column: dict) -> float:
    if column["part"] == "index":
        return float(row)
    source.seek(info["start"] + (row * info["count"] + column["column"]) * info["width"])
    raw = source.read(info["width"])
    if len(raw) != info["width"]:
        raise ValueError("Truncated NPY value")
    endian = "<" if info["endian"] in "<=|" else ">"
    kind, width = info["kind"], info["width"]
    if kind == "c":
        code = "f" if width == 8 else "d"
        real, imag = struct.unpack(endian + code * 2, raw)
        return float(real if column["part"] == "real" else imag if column["part"] == "imag" else math.hypot(real, imag))
    code = {("f", 2): "e", ("f", 4): "f", ("f", 8): "d",
            ("i", 1): "b", ("i", 2): "h", ("i", 4): "i", ("i", 8): "q",
            ("u", 1): "B", ("u", 2): "H", ("u", 4): "I", ("u", 8): "Q",
            ("b", 1): "?"}[(kind, width)]
    return float(struct.unpack(endian + code, raw)[0])


def _finite(value: str) -> float | None:
    try:
        number = float(value)
    except (ValueError, TypeError):
        return None
    return number if math.isfinite(number) else None


def describe(path: Path) -> dict:
    if path.name == BAO_MEAN and path.parent.resolve() == BAO_ROOT.resolve():
        info = _bao_mean(path)
    elif path.suffix.lower() == ".fits":
        info = _fits_table(path)
    elif path.suffix.lower() == ".npy":
        info = _npy_array(path)
    elif path.suffix.lower() in {".h5", ".hdf5"}:
        info = hdf5_bridge.call(path, "describe")
    elif path.suffix.lower() in {".csv", ".dat", ".txt"}:
        info = _text_columns(path)
    else:
        raise ValueError("Metadata reader pending for this format")
    return {"id": file_id(path.resolve()), "path": str(path), "bytes": path.stat().st_size,
            "format": info["format"], "rows": info["rows"], "columns":
            [{"name": column["name"], "unit": column.get("unit", "")} for column in info["columns"]],
            "read_mode": "READ_ONLY_BOUNDED_SAMPLE", "_internal": info}


def preview(path: Path, x: str, y: str, limit: int = 800) -> dict:
    if not 1 <= limit <= MAX_POINTS:
        raise ValueError("Point limit out of range")
    metadata = describe(path)
    info = metadata.pop("_internal")
    names = [col["name"] for col in info["columns"]]
    if x not in names or y not in names or x == y:
        raise ValueError("Choose two different catalogued columns")
    ix, iy = names.index(x), names.index(y)
    points = []
    sampled_rows = 0
    if info["format"] == "DESI_BAO_MEAN_WITH_COVARIANCE":
        points = [[item[x], item[y]] for item in info["observations"]]
        sampled_rows = len(points)
    elif info["format"] == "HDF5_NUMERIC":
        sample = hdf5_bridge.call(path, "preview", x=x, y=y, limit=limit)
        points = sample["points"]
        sampled_rows = sample["sampled_rows"]
    elif info["format"] == "NPY":
        stride = max(1, math.ceil(info["rows"] / limit))
        with path.open("rb") as source:
            for row in range(0, info["rows"], stride):
                sampled_rows += 1
                values = [_npy_value(source, info, row, info["columns"][index]) for index in (ix, iy)]
                if all(math.isfinite(v) for v in values):
                    points.append(values)
    elif info["format"] == "FITS_BINTABLE":
        formats = {"B": ">B", "I": ">h", "J": ">i", "K": ">q", "E": ">f", "D": ">d"}
        stride = max(1, math.ceil(info["rows"] / limit))
        with path.open("rb") as source:
            for row in range(0, info["rows"], stride):
                sampled_rows += 1
                values = []
                for column in (info["columns"][ix], info["columns"][iy]):
                    code = formats[column["kind"]]
                    source.seek(info["start"] + row * info["row_bytes"] + column["offset"])
                    values.append(float(struct.unpack(code, source.read(struct.calcsize(code)))[0]))
                if all(math.isfinite(v) for v in values):
                    points.append(values)
    else:
        with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as source:
            rows = (line for line in source if line.strip() and not line.lstrip().startswith("#"))
            if info["header"]:
                next(rows, None)
            for line in rows:
                sampled_rows += 1
                if sampled_rows > 1_000_000:
                    break
                fields = next(csv.reader([line])) if info["delimiter"] else line.split()
                if max(ix, iy) < len(fields):
                    a, b = _finite(fields[ix]), _finite(fields[iy])
                    if a is not None and b is not None:
                        if len(points) < limit:
                            points.append([a, b])
                        else:
                            # Deterministic hash reservoir; bounded RAM, no random seed.
                            slot = int(hashlib.blake2s(str(sampled_rows).encode(), digest_size=4).hexdigest(), 16) % sampled_rows
                            if slot < limit:
                                points[slot] = [a, b]
    result = {"source": metadata, "x": x, "y": y, "points": points,
            "sampled_rows": sampled_rows, "sample_method":
            "FULL_13_POINT_BAO_SUMMARY" if info["format"] == "DESI_BAO_MEAN_WITH_COVARIANCE" else
            "HDF5_STRIDED_HYPERSLAB_MAX_1200" if info["format"] == "HDF5_NUMERIC" else
            "UNIFORM_ROW_STRIDE" if info["format"] in ("FITS_BINTABLE", "NPY") else "DETERMINISTIC_RESERVOIR_MAX_1M_ROWS",
            "status": "DATA_PREVIEW_NOT_MODEL_FIT", "source_mtime_ns": path.stat().st_mtime_ns}
    if info["format"] == "DESI_BAO_MEAN_WITH_COVARIANCE":
        result["observations"] = info["observations"]
        result["covariance"] = info["covariance"]
        result["covariance_path"] = info["covariance_path"]
        result["mean_sha256"] = info["mean_sha256"]
        result["covariance_sha256"] = info["covariance_sha256"]
        result["covariance_note"] = "Diagonal square roots shown as error bars; off-diagonal terms retained in source, not used for a fit."
    if info["format"] == "HDF5_NUMERIC":
        result["dropped_nonfinite_pairs"] = sample["dropped_nonfinite_pairs"]
        result["coverage"] = sample["coverage"]
        result["frequency_inference"] = sample["frequency_inference"]
        result["sample_index"] = sample["sample_index"]
    return result
