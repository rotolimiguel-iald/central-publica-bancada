"""Read-only source/data audit; no original imports, fitting, or network access."""
import ast
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1")
FILES = {
    "historical_program": ROOT / "_originais/tgl_paper_unified.py",
    "historical_n2": ROOT / "12_nivel2_frozen_e_verossimilhanca.py",
    "local_mean": ROOT / "_originais/desi_gaussian_bao_ALL_GCcomb_mean.txt",
    "local_covariance": ROOT / "_originais/desi_gaussian_bao_ALL_GCcomb_cov.txt",
    "current_cache": Path(r"C:\Users\rotol\.tgl_cache\desi_dr2_bao_compressed.json"),
}


def assignment(tree, name):
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name for target in node.targets
        ):
            return node.value, node.lineno
    raise KeyError(name)


def numeric_rows(text):
    return [line.split() for line in text.splitlines()
            if line.strip() and not line.lstrip().startswith("#")]


def cholesky(matrix):
    n = len(matrix)
    lower = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            value = matrix[i][j] - sum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                if value <= 0:
                    raise ValueError("Covariance has nonpositive Cholesky pivot")
                lower[i][j] = math.sqrt(value)
            else:
                lower[i][j] = value / lower[j][j]
    return lower


def save_new(path, raw):
    if path.exists():
        if path.read_bytes() != raw:
            raise FileExistsError("Audit differs; retain existing receipt and version separately")
        return
    temp = path.with_suffix(path.suffix + ".new")
    with temp.open("xb") as stream:
        stream.write(raw)
    if temp.read_bytes() != raw:
        raise OSError("Incomplete receipt")
    temp.replace(path)


def main():
    raw = {name: path.read_bytes() for name, path in FILES.items()}
    text = {name: value.decode("utf-8-sig") for name, value in raw.items()}
    old_tree = ast.parse(text["historical_program"])
    n2_tree = ast.parse(text["historical_n2"])
    fallback_node, fallback_line = assignment(old_tree, "_DESI_FALLBACK")
    fallback = ast.literal_eval(fallback_node)
    n2_node, n2_line = assignment(n2_tree, "DESI")
    if not (isinstance(n2_node, ast.Call) and isinstance(n2_node.func, ast.Attribute)
            and isinstance(n2_node.func.value, ast.Name)
            and n2_node.func.value.id == "np" and n2_node.func.attr == "array"):
        raise ValueError("Unexpected N2 array definition")
    kinds = {0: "DM_over_rd", 1: "DH_over_rd", 2: "DV_over_rd"}
    n2 = [[z, kinds[kind], value, error]
          for z, kind, value, error in ast.literal_eval(n2_node.args[0])]
    means = [[float(z), kind.replace("_rs", "_rd"), float(value)]
             for z, value, kind in numeric_rows(text["local_mean"])]
    cov = [[float(v) for v in row] for row in numeric_rows(text["local_covariance"])]
    n = len(means)
    if len(cov) != n or any(len(row) != n for row in cov):
        raise ValueError("Covariance/mean dimensions differ")
    if not all(math.isfinite(v) for row in cov for v in row):
        raise ValueError("Nonfinite covariance")
    symmetry = max(abs(cov[i][j] - cov[j][i]) for i in range(n) for j in range(n))
    if symmetry > 1e-12:
        raise ValueError("Asymmetric covariance")
    lower = cholesky(cov)
    reconstruction_error = max(abs(cov[i][j] - sum(lower[i][k] * lower[j][k]
                                  for k in range(n))) for i in range(n) for j in range(n))
    live = [row + [math.sqrt(cov[i][i])] for i, row in enumerate(means)]
    cache = json.loads(text["current_cache"])
    cache_rows = cache["measurements"]
    if len(cache_rows) != n or any(a[:2] != b[:2] for a, b in zip(live, cache_rows)):
        raise ValueError("Cache/mean keys differ")
    cache_delta = max(abs(a[k] - b[k]) for a, b in zip(live, cache_rows) for k in (2, 3))
    live_by_key = {tuple(row[:2]): row for row in live}
    n2_by_key = {tuple(row[:2]): row for row in n2}
    if len(live_by_key) != len(live) or len(n2_by_key) != len(n2):
        raise ValueError("Repeated measurement keys")
    common = sorted(live_by_key.keys() & n2_by_key.keys())
    correlations = sorted([
        {"first": live[i][:2], "second": live[j][:2],
         "correlation": cov[i][j] / math.sqrt(cov[i][i] * cov[j][j])}
        for i in range(n) for j in range(i) if cov[i][j] != 0
    ], key=lambda item: abs(item["correlation"]), reverse=True)
    sm_node, sm_line = assignment(n2_tree, "NEFF_SM")
    sm = ast.literal_eval(sm_node)
    f_nu = (7 / 8) * (4 / 11) ** (4 / 3)
    dndb = (4 / 3) * (1 + f_nu * sm) / f_nu
    report = {
        "status": "READ_ONLY_LINEAGE_AND_COVARIANCE_CHECK_NOT_COSMOLOGICAL_FIT",
        "sources": {name: {"path": str(FILES[name]), "sha256": hashlib.sha256(value).hexdigest(),
                           "bytes": len(value)} for name, value in raw.items()},
        "historical_n2": {"line": n2_line, "rows": n2, "count": len(n2),
                          "equals_first_12_fallback_rows": n2 == fallback[:12]},
        "fallback": {"line": fallback_line, "count": len(fallback), "rows": fallback},
        "local_dr2_files": {"count": n, "distinct_redshifts": len({r[0] for r in live}),
                            "rows": live, "cache_provenance_declared": cache.get("provenance"),
                            "cache_max_value_or_error_rounding_difference": cache_delta,
                            "cache_matches_to_5_decimal_rounding": cache_delta <= 5.0001e-6},
        "comparison": {"common_keys": [list(k) for k in common], "common_key_count": len(common),
                       "exact_common_rows": sum(live_by_key[k] == n2_by_key[k] for k in common),
                       "n2_only_keys": [list(k) for k in sorted(n2_by_key.keys() - live_by_key.keys())],
                       "dr2_only_keys": [list(k) for k in sorted(live_by_key.keys() - n2_by_key.keys())]},
        "covariance": {"shape": [n, n], "symmetry_error": symmetry,
                       "positive_cholesky_pivots": True,
                       "reconstruction_error": reconstruction_error,
                       "nonzero_offdiagonal_pairs": len(correlations), "correlations": correlations},
        "historical_S": {"NEFF_SM": sm, "NEFF_SM_source_line": sm_line,
                         "DNDB_evaluated_from_source_formula": dndb,
                         "jacobian_beta_omegac_to_neff_omegac_eff": "DNDB*(1+beta)",
                         "jacobian_min_on_beta_support_closure": dndb * 0.95,
                         "omega_c_eff_infimum_on_source_support": 0.08 - 0.05 * (0.028 + 0.08),
                         "omega_c_eff_supremum_on_source_support": 0.17 + 0.10 * (0.028 + 0.17)},
        "limits": ["Current cache does not establish inputs of any historical execution.",
                   "Local filenames/provenance are not verification of a remote release commit.",
                   "Covariance belongs to its accompanying ordered 13-row mean, not the N2 fallback.",
                   "No originals imported/executed; no spectra, fits, null simulations or significance computed."]
    }
    destination = HERE / "state/D10_BAO_LINEAGE_AUDIT.json"
    save_new(destination, (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode())
    print(json.dumps({"path": str(destination), "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
                      "n2_equals_fallback_prefix": report["historical_n2"]["equals_first_12_fallback_rows"],
                      "common_keys": len(common), "live_redshifts": report["local_dr2_files"]["distinct_redshifts"],
                      "covariance": {k: v for k, v in report["covariance"].items() if k != "correlations"},
                      "largest_correlations": correlations[:3], "S": report["historical_S"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
