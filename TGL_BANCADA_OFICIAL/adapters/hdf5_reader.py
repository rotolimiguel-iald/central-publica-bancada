"""Bounded HDF5 reader invoked by the local bench in an existing WSL venv."""
from __future__ import annotations

import json
import math
import sys

import h5py
import numpy as np

MAX_VISITS = 512
MAX_COLUMNS = 128


def unit_of(dataset) -> str:
    for key in ("units", "unit", "Unit", "Units"):
        if key in dataset.attrs:
            value = dataset.attrs[key]
            if isinstance(value, bytes):
                value = value.decode("utf-8", "replace")
            if isinstance(value, (str, int, float)):
                return str(value)[:100]
    return ""


def columns_of(source) -> list[dict]:
    columns = []
    visits = 0
    seen = set()

    def visit(group, prefix: str, depth: int) -> None:
        nonlocal visits
        if depth > 8:
            return
        for name in sorted(group.keys()):
            visits += 1
            if visits > MAX_VISITS or len(columns) >= MAX_COLUMNS:
                return
            if not isinstance(group.get(name, getlink=True), h5py.HardLink):
                continue  # No soft/external link traversal.
            obj = group[name]
            if obj.id in seen:
                continue
            seen.add(obj.id)
            path = prefix + "/" + name
            if isinstance(obj, h5py.Group):
                visit(obj, path, depth + 1)
                continue
            if not isinstance(obj, h5py.Dataset) or obj.dtype.kind not in "biufc":
                continue
            if obj.id.get_create_plist().get_external_count():
                raise ValueError("External-storage HDF5 dataset refused")
            if obj.ndim == 1:
                columns.append({"name": path, "unit": unit_of(obj), "path": path,
                                "column": None, "rows": int(obj.shape[0])})
            elif obj.ndim == 2:
                for col in range(min(int(obj.shape[1]), 8, MAX_COLUMNS - len(columns))):
                    columns.append({"name": f"{path}[{col}]", "unit": unit_of(obj),
                                    "path": path, "column": col, "rows": int(obj.shape[0])})

    visit(source, "", 0)
    return columns


def read_values(source, column: dict, stride: int, rows: int) -> np.ndarray:
    if column["name"] == "index":
        return np.arange(0, rows, stride, dtype=np.float64)
    dataset = source[column["path"]]
    if column["column"] is None:
        values = dataset[:rows:stride]
    else:
        values = dataset[:rows:stride, column["column"]]
    if np.iscomplexobj(values):
        raise ValueError("Complex HDF5 requires an explicit component adapter")
    return np.asarray(values, dtype=np.float64)


def main() -> None:
    request = json.load(sys.stdin)
    with h5py.File(request["path"], "r") as source:
        columns = columns_of(source)
        if not columns:
            raise ValueError("No numeric 1D/2D datasets found in bounded HDF5 traversal")
        rows = max(item["rows"] for item in columns)
        public = ([{"name": "index", "unit": "sample_index", "origin": "SYNTHETIC_INDEX_NOT_PHYSICAL_TIME"}] +
                  [{"name": item["name"], "unit": item["unit"]} for item in columns])
        if request["operation"] == "describe":
            result = {"format": "HDF5_NUMERIC", "rows": rows, "columns": public,
                      "dataset_count": len(columns), "scan_limit": MAX_VISITS}
        elif request["operation"] == "preview":
            x, y, limit = request["x"], request["y"], int(request["limit"])
            if not 1 <= limit <= 1200 or x == y:
                raise ValueError("Invalid preview columns or limit")
            available = {item["name"]: item for item in columns}
            available["index"] = {"name": "index", "rows": rows}
            if x not in available or y not in available:
                raise ValueError("Column absent from HDF5 schema")
            a, b = available[x], available[y]
            if x != "index" and y != "index" and a["rows"] != b["rows"]:
                raise ValueError("HDF5 datasets have different row counts")
            count = b["rows"] if x == "index" else a["rows"] if y == "index" else a["rows"]
            stride = max(1, math.ceil(count / limit))
            xa, ya = read_values(source, a, stride, count), read_values(source, b, stride, count)
            mask = np.isfinite(xa) & np.isfinite(ya)
            result = {"format": "HDF5_NUMERIC", "rows": count,
                      "sampled_rows": int(xa.size),
                      "finite_points": int(mask.sum()),
                      "dropped_nonfinite_pairs": int(mask.size - mask.sum()),
                      "coverage": "STRIDED_PREVIEW_NOT_ANALYSIS",
                      "frequency_inference": "FORBIDDEN_WITHOUT_ANTIALIAS_AND_TIME_METADATA",
                      "sample_index": "SYNTHETIC_INDEX_NOT_PHYSICAL_TIME",
                      "points": np.column_stack((xa[mask], ya[mask])).tolist(),
                      "sample_method": "HDF5_STRIDED_HYPERSLAB_MAX_1200"}
        else:
            raise ValueError("Unknown HDF5 operation")
    print(json.dumps(result, allow_nan=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"error": str(exc)[:300]}))
        raise SystemExit(2)
