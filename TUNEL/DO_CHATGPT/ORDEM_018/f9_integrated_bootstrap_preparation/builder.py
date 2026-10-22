"""Explicit F9 covariance assembly; preparation only, no implicit IO or solver.

All scientific arrays, runtime objects, admissions and references are caller-owned.
This module assembles covariances; PSD/rank/support/normalization remain duties of
the existing SupportGaussian / FlatNuisanceGaussian and a separately admitted run.
"""
import hashlib
import json
import math
from fractions import Fraction

REQUEST_ID = "f200dee1-0ecf-4a51-9b38-4c32d7eb0696"
METADATA_SHA256 = "39b0b41a99711cd24491b5680ff579707547e3c45c8718d9edb66f73ddb89849"
BLOCKS = ("PLANCK", "DESI", "STELLAR", "GROUP", "SN_CAL", "SBF_CAL",
          "SN_HF", "SBF_HF", "MM")
COMMON = ("PLANCK", "DESI", "GROUP", "SN_CAL", "SBF_CAL", "SN_HF")
MM_RECIPE = "H0DN_MM_DZ_UPSTREAM_SYMMETRIC"
MM_STATUS = "CONDITIONAL_UNRATIFIED"
STATUS = "ENGINEERING_ONLY_UNQUALIFIED_COVARIANCE"


class CovarianceError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(code + ": " + message)


def _require(condition, code, message):
    if not condition:
        raise CovarianceError(code, message)


def _keys(value, names, label):
    _require(type(value) is dict and set(value) == set(names),
             "SCHEMA_ERROR", label)


def _text(value, label):
    _require(type(value) is str and 0 < len(value) <= 2048,
             "SCHEMA_ERROR", label)
    return value


def _digest(value):
    _require(type(value) is str and len(value) == 64 and
             all(c in "0123456789abcdef" for c in value), "PIN_ERROR", "SHA256")
    return value


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def _ref(value, label):
    _keys(value, ("artifact_sha256", "clause", "status"), label)
    _digest(value["artifact_sha256"])
    _text(value["clause"], label)
    _require(value["status"] in ("INPUT_CONDITIONAL", "SYNTHETIC_FIXTURE",
                                 "REVIEWED_IMPLEMENTATION"), "REFERENCE_ERROR", label)
    return dict(value)


def _pairs(items):
    result = {}
    for key, value in items:
        _require(key not in result, "SCHEMA_ERROR", "duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(value):
    raise CovarianceError("SCHEMA_ERROR", "nonfinite JSON: " + value)


def _json(raw, expected, maximum):
    _require(type(raw) is bytes and 0 < len(raw) <= maximum,
             "SCHEMA_ERROR", "bounded explicit JSON bytes")
    _require(_sha(raw) == _digest(expected), "PIN_ERROR", "explicit JSON bytes")
    try:
        return json.loads(raw, object_pairs_hook=_pairs, parse_constant=_reject_constant)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise CovarianceError("SCHEMA_ERROR", str(exc)) from exc


def _positive(value, label):
    _require(type(value) in (int, float) and not isinstance(value, bool),
             "SCHEMA_ERROR", label)
    _require(math.isfinite(value) and value > 0, "VALUE_ERROR", label)
    return float(value)


class JointCovarianceBuilder:
    """Trusted-runtime API; constructor performs metadata checks, no matrices.

    block_correlation must be the pinned existing primitive with its numpy global
    bound to the injected runtime. A receipt documents caller verification; flags
    cannot authenticate arbitrary Python objects or establish a physical model.
    """
    def __init__(self, metadata_json, *, numpy_module, block_correlation,
                 runtime_receipt_json, runtime_receipt_sha256):
        self._meta = _json(metadata_json, METADATA_SHA256, 500000)
        self._np = numpy_module
        self._correlation = block_correlation
        receipt = _json(runtime_receipt_json, runtime_receipt_sha256, 65536)
        _keys(receipt, ("schema", "primitive_source_sha256", "primitive_name",
                        "primitive_module", "runtime_reference",
                        "loaded_callable_and_numpy_global_reference"), "runtime receipt")
        expected = self._meta["source_pins"]["covariance_support/qualify_stellar_family.py"]["sha256"]
        _require(receipt["schema"] == "F9_COVARIANCE_PRIMITIVE_BINDING_V1" and
                 receipt["primitive_source_sha256"] == expected and
                 receipt["primitive_name"] == "block_correlation",
                 "PIN_ERROR", "reused primitive")
        _require(getattr(block_correlation, "__name__", None) == receipt["primitive_name"] and
                 getattr(block_correlation, "__module__", None) == receipt["primitive_module"] and
                 getattr(numpy_module, "__name__", None) == "numpy",
                 "RUNTIME_ERROR", "caller-injected runtime metadata")
        _ref(receipt["runtime_reference"], "numpy runtime")
        _ref(receipt["loaded_callable_and_numpy_global_reference"], "actual primitive binding")
        self._runtime_sha = runtime_receipt_sha256
        self._by_label = {x["label"]: x for x in self._meta["family_labels"]}
        self._block_ids = {x["name"]: tuple(x["row_ids"]) for x in self._meta["blocks"]}
        self._slices = {x["name"]: slice(x["start"], x["stop"]) for x in self._meta["blocks"]}
        self._cross_names = tuple(a + "|" + b for i, a in enumerate(BLOCKS) for b in BLOCKS[i+1:])

    def family_metadata(self):
        """A defensive copy of all 600 labels; no deduplication or evaluation."""
        return json.loads(_canonical(self._meta["family_labels"]))

    def _label(self, label):
        _require(type(label) is str and label in self._by_label,
                 "FAMILY_ERROR", "unknown label")
        return self._by_label[label]

    def _array(self, values, shape, label):
        np = self._np
        array = np.array(values, dtype="<f8", copy=True, order="C")
        _require(array.shape == shape and bool(np.isfinite(array).all()),
                 "MATRIX_ERROR", label + ": shape/nonfinite")
        return array

    def _matrix_record(self, supplied, left, right):
        _keys(supplied, ("values", "row_ids", "column_ids", "coordinates",
                         "values_f64le_sha256", "reference", "zero_policy"), left + "|" + right)
        _require(tuple(supplied["row_ids"]) == self._block_ids[left] and
                 tuple(supplied["column_ids"]) == self._block_ids[right] and
                 supplied["coordinates"] == "NATIVE_F9_283",
                 "ROW_OR_UNIT_ERROR", left + "|" + right)
        reference = _ref(supplied["reference"], left + "|" + right)
        array = self._array(supplied["values"],
                            (len(self._block_ids[left]), len(self._block_ids[right])), left + "|" + right)
        digest = _sha(array.tobytes(order="C"))
        _require(digest == _digest(supplied["values_f64le_sha256"]),
                 "PIN_ERROR", left + "|" + right)
        all_zero = bool((array == 0).all())
        _require(supplied["zero_policy"] ==
                 ("EXPLICIT_INPUT_ZERO" if all_zero else "EXPLICIT_MATRIX"),
                 "DEPENDENCE_ERROR", "zero is not an inferred independence: " + left + "|" + right)
        if left == right:
            _require(bool((self._np.diag(array) > 0).all()), "MATRIX_ERROR", "positive diagonal")
        return array, {"f64le_sha256": digest, "reference": reference,
                       "zero_policy": supplied["zero_policy"]}

    def _stellar(self, supplied, scenario):
        _keys(supplied, ("sigma_by_primitive", "sigma_f64le_sha256", "reference",
                         "D0_policy", "D0_reference"), "stellar inputs")
        _require(supplied["D0_policy"] == "EXPLICIT_ZERO_BASELINE_RECIPE",
                 "MODEL_COMPONENT_ERROR", "no new D0 budget inferred")
        refs = {"error_budget": _ref(supplied["reference"], "stellar error budget"),
                "D0": _ref(supplied["D0_reference"], "D0 explicit baseline")}
        _keys(supplied["sigma_by_primitive"], ("anchor", "MAS", "HMS"), "primitive sigma maps")
        _keys(supplied["sigma_f64le_sha256"], ("anchor", "MAS", "HMS"), "primitive sigma pins")
        np = self._np
        keys = self._meta["primitive_keys"]
        sigma, sigma_pins = {}, {}
        for kind in ("anchor", "MAS", "HMS"):
            values = supplied["sigma_by_primitive"][kind]
            _keys(values, keys[kind], kind + " exact keys")
            vector = self._array([_positive(values[k], kind) for k in keys[kind]],
                                 (len(keys[kind]),), kind)
            digest = _sha(vector.tobytes(order="C"))
            _require(digest == _digest(supplied["sigma_f64le_sha256"][kind]),
                     "PIN_ERROR", kind + " sigma")
            sigma[kind], sigma_pins[kind] = vector, digest
        # Incidences are structural zeros/ones, not unreported covariance assumptions.
        graph = self._meta["stellar_graph"]
        factors = {}
        for kind, field in (("anchor", "anchor"), ("MAS", "MAS"), ("HMS", "HMS")):
            indexes = [keys[kind].index(row[field]) for row in graph]
            factors[kind] = np.eye(len(keys[kind]), dtype="<f8")[indexes] * sigma[kind]
        groups = self._meta["groups"]
        sign = scenario["sign_scenario"]
        specs = (("MAS", groups["MAS_same_program_at_N4258"]),
                 ("MAS", [groups["MAS_JAGB_reference_pair"]]),
                 ("HMS", groups["HMS_by_eleven_hosts"]),
                 ("HMS", [groups["HMS_N5643_JAGB_pair"]]))
        matrices = []
        for kind, partition in specs:
            value = self._correlation(list(keys[kind]), partition, sign)
            matrix = self._array(value, (len(keys[kind]), len(keys[kind])), kind + " primitive")
            _require(bool(np.array_equal(matrix, matrix.T)) and
                     bool((np.diag(matrix) == 1).all()), "PRIMITIVE_ERROR", kind)
            matrices.append(matrix)
        u, v, p, q = [float(Fraction(x)) for x in scenario["fraction_strings"]]
        rm = (1-u-v)*np.eye(len(keys["MAS"])) + u*matrices[0] + v*matrices[1]
        rh = (1-p-q)*np.eye(len(keys["HMS"])) + p*matrices[2] + q*matrices[3]
        anchor, mas, hms = factors["anchor"], factors["MAS"], factors["HMS"]
        covariance = anchor @ anchor.T + mas @ rm @ mas.T + hms @ rh @ hms.T
        # No averaging, clipping, jitter, eigensolver or implicit extra error budget.
        covariance = self._array(covariance, (178, 178), "stellar construction")
        return covariance, {"sigma_f64le_sha256": sigma_pins, "references": refs,
                             "D0_policy": supplied["D0_policy"]}

    def _mm(self, supplied):
        _keys(supplied, ("recipe", "rows", "dependence_policy", "dependence_reference",
                         "reference_endogeneity_reference"), "MM")
        _require(supplied["recipe"] == MM_RECIPE and
                 supplied["dependence_policy"] == "EXPLICIT_DIAGONAL_WORKING_INPUT",
                 "OPEN_MODEL_COMPONENT", "only conditional MM alternative A is implemented")
        _require(type(supplied["rows"]) is list and len(supplied["rows"]) == 5,
                 "MM_ERROR", "all five MM rows required")
        variances, evidence = [], []
        for row, expected_id in zip(supplied["rows"], self._block_ids["MM"]):
            _keys(row, ("row_id", "variance_dex2", "distance_reference_mpc",
                        "velocity_reference_km_s", "U_reference_km_s",
                        "fixed_reference", "variance_recipe_reference"), "MM row")
            _require(row["row_id"] == expected_id, "ROW_OR_UNIT_ERROR", "MM order")
            variance = _positive(row["variance_dex2"], "MM supplied variance dex2")
            for key in ("distance_reference_mpc", "velocity_reference_km_s", "U_reference_km_s"):
                _positive(row[key], key)
            _ref(row["fixed_reference"], "MM reference values/units/endogeneity")
            _ref(row["variance_recipe_reference"], "MM variance propagation")
            variances.append(variance)
            evidence.append(json.loads(_canonical(row)))
        covariance = self._np.diag(self._np.array(variances, dtype="<f8"))
        return covariance, {"recipe": supplied["recipe"], "rows": evidence,
            "dependence_policy": supplied["dependence_policy"],
            "dependence_reference": _ref(supplied["dependence_reference"], "MM off-diagonal zero INPUT"),
            "reference_endogeneity_reference": _ref(supplied["reference_endogeneity_reference"], "MM endogeneity")}

    def _binding(self, supplied):
        _keys(supplied, ("family_common_input_sha256", "five_model_response_sha256",
                        "consumer_structure_sha256", "fixed_affine_support_reference",
                        "normalization_recipe_reference", "common_measure_id",
                        "model_and_O01_O02_reference", "compression_reference"), "case bindings")
        for key in ("family_common_input_sha256", "five_model_response_sha256",
                    "consumer_structure_sha256"):
            _digest(supplied[key])
        for key in ("fixed_affine_support_reference", "normalization_recipe_reference",
                    "model_and_O01_O02_reference", "compression_reference"):
            _ref(supplied[key], key)
        _text(supplied["common_measure_id"], "common kappa d_eta")
        return json.loads(_canonical(supplied))

    def build_case(self, label, *, common_blocks, cross_blocks, stellar, sbf, mm, bindings):
        """Assemble one native-unit C from complete explicit components.

        Does not evaluate a likelihood, certify PSD/support/rank or create an
        admission. Missing inputs raise OPEN_MODEL_COMPONENT; no row is removed.
        """
        scenario = self._label(label)
        missing = [name for name, value in (("common_blocks", common_blocks),
                   ("cross_blocks", cross_blocks), ("stellar", stellar), ("sbf", sbf),
                   ("mm", mm), ("bindings", bindings)) if value is None]
        _require(not missing, "OPEN_MODEL_COMPONENT", ", ".join(missing))
        _keys(common_blocks, COMMON, "complete common blocks")
        _keys(cross_blocks, self._cross_names, "all 36 explicit cross blocks")
        binding = self._binding(bindings)
        np = self._np
        covariance = np.full((283, 283), np.nan, dtype="<f8")
        provenance = {"common": {}, "cross": {}}
        for name in COMMON:
            matrix, rec = self._matrix_record(common_blocks[name], name, name)
            covariance[self._slices[name], self._slices[name]] = matrix
            provenance["common"][name] = rec
        star, provenance["stellar"] = self._stellar(stellar, scenario)
        covariance[self._slices["STELLAR"], self._slices["STELLAR"]] = star
        _keys(sbf, ("recipe_id", "variance_dex2", "variance_reference",
                    "compression_reference"), "SBF")
        _require(sbf["recipe_id"] == scenario["sbf_id"], "FAMILY_ERROR", "SBF label/recipe mismatch")
        sbf_variance = _positive(sbf["variance_dex2"], "SBF compressed variance dex2")
        _ref(sbf["variance_reference"], "SBF variance")
        _ref(sbf["compression_reference"], "SBF compression/weights/offset conventions")
        covariance[self._slices["SBF_HF"], self._slices["SBF_HF"]] = sbf_variance
        provenance["sbf"] = json.loads(_canonical(sbf))
        mm_matrix, provenance["mm"] = self._mm(mm)
        covariance[self._slices["MM"], self._slices["MM"]] = mm_matrix
        for key in self._cross_names:
            left, right = key.split("|")
            matrix, rec = self._matrix_record(cross_blocks[key], left, right)
            if right == "MM":
                _require(bool((matrix == 0).all()), "OPEN_MODEL_COMPONENT",
                         "conditional MM alternative A requires explicit zero MM-rest block")
            covariance[self._slices[left], self._slices[right]] = matrix
            covariance[self._slices[right], self._slices[left]] = matrix.T
            provenance["cross"][key] = rec
        _require(bool(np.isfinite(covariance).all()), "MATRIX_ERROR", "unfilled/nonfinite covariance")
        # Symmetry tolerance and any roundoff symmetrization belong exclusively
        # to the existing SupportGaussian, with explicit caller tolerances.
        # Floating products may be slightly asymmetric; preserve those bytes.
        _require(bool((np.diag(covariance) > 0).all()), "MATRIX_ERROR", "joint diagonal")
        native_digest = _sha(covariance.tobytes(order="C"))
        covariance.setflags(write=False)
        record = self._record_base(scenario, binding)
        invariants = {"common": provenance["common"], "stellar": provenance["stellar"],
                      "mm": provenance["mm"],
                      "non_sbf_cross": {k: v for k, v in provenance["cross"].items()
                                       if "SBF_HF" not in k.split("|")}}
        record.update(status=STATUS, C_native_f64le_sha256=native_digest,
                      family_invariants_sha256=_sha(_canonical(invariants)),
                      input_components_sha256=_sha(_canonical(provenance)),
                      input_components=provenance, support_receipt=None,
                      normalization_receipt=None, actual_rank=None)
        record["record_sha256"] = _sha(_canonical(record))
        return {"C_native": covariance, "row_ids": tuple(self._meta["projection"]["row_ids"]),
                "record": record}

    def _record_base(self, scenario, binding):
        return {"schema": "F9_JOINT_COVARIANCE_RECORD_V1", "request_id": REQUEST_ID,
                "label": scenario["label"], "metadata_sha256": METADATA_SHA256,
                "runtime_receipt_sha256": self._runtime_sha,
                "coordinates": "NATIVE_F9_283", "rows": 283, "nuisance_columns": 63,
                "MM_rows": 5, "MM_status": MM_STATUS, "O01_O02_ratified": False,
                "family_scope": self._meta["family_scope"], "deduplicated": False,
                "bindings": binding, "transformation_owner": "likelihood_consumer.prepare_joint",
                "native_to_output_row_scale": self._meta["projection"]["native_to_output_row_scale"]}

    def open_record(self, label, *, missing_components, bindings):
        """Represent an unavailable full case; no substitute C or numeric result."""
        scenario = self._label(label)
        _require(type(missing_components) is list and len(missing_components) > 0,
                 "SCHEMA_ERROR", "explicit missing components")
        for name in missing_components:
            _text(name, "missing component")
        record = self._record_base(scenario, self._binding(bindings))
        record.update(status="OPEN_MODEL_COMPONENT", missing_components=list(missing_components),
                      C_native_f64le_sha256=None, input_components_sha256=None,
                      family_invariants_sha256=None,
                      support_receipt=None, normalization_receipt=None, actual_rank=None)
        record["record_sha256"] = _sha(_canonical(record))
        return record

    def summarize_family(self, records):
        """Validate all 600 records in fixed order, without dropping open cases.

        This binds the full ordered label map, not merely a claimed family hash.
        It never certifies the physical support or interprets labels as replicas.
        """
        _require(type(records) is list and len(records) == 600,
                 "FAMILY_ERROR", "all 600 records required")
        result, open_labels = [], []
        common_binding = None
        numeric_invariants = None
        sbf_variants = {}
        for scenario, record in zip(self._meta["family_labels"], records):
            _require(type(record) is dict and record.get("label") == scenario["label"],
                     "FAMILY_ERROR", "missing/reordered/duplicate label")
            raw = dict(record)
            saved_digest = raw.pop("record_sha256", None)
            _require(_sha(_canonical(raw)) == _digest(saved_digest), "PIN_ERROR", "case record")
            binding = self._binding(record["bindings"])
            _require(record["metadata_sha256"] == METADATA_SHA256 and
                     record["request_id"] == REQUEST_ID and
                     record["runtime_receipt_sha256"] == self._runtime_sha and
                     record["MM_status"] == MM_STATUS and record["rows"] == 283 and
                     record["nuisance_columns"] == 63 and record["MM_rows"] == 5 and
                     record["O01_O02_ratified"] is False and record["deduplicated"] is False,
                     "FAMILY_ERROR", "case identity/status")
            # Statistical references may differ by scenario. Physical response, eta
            # measure and frozen common input identity may not silently drift.
            key = tuple(binding[x] for x in ("family_common_input_sha256",
                        "five_model_response_sha256", "consumer_structure_sha256", "common_measure_id"))
            if common_binding is None:
                common_binding = key
            _require(key == common_binding, "FAMILY_ERROR", "common identity changed")
            if record["status"] == "OPEN_MODEL_COMPONENT":
                _require(record["C_native_f64le_sha256"] is None, "FAMILY_ERROR", "open case has C")
                open_labels.append(record["label"])
            else:
                _require(record["status"] == STATUS, "FAMILY_ERROR", "unrecognized case status")
                _digest(record["C_native_f64le_sha256"])
                components = record["input_components"]
                _require(_sha(_canonical(components)) == record["input_components_sha256"],
                         "PIN_ERROR", "input component record")
                _require(components["sbf"]["recipe_id"] == scenario["sbf_id"],
                         "FAMILY_ERROR", "case label versus recorded SBF recipe")
                invariant_payload = {"common": components["common"], "stellar": components["stellar"],
                    "mm": components["mm"], "non_sbf_cross": {
                        k: v for k, v in components["cross"].items() if "SBF_HF" not in k.split("|")}}
                inv = _digest(record["family_invariants_sha256"])
                _require(_sha(_canonical(invariant_payload)) == inv,
                         "PIN_ERROR", "family invariants linked to input components")
                if numeric_invariants is None:
                    numeric_invariants = inv
                _require(inv == numeric_invariants, "FAMILY_ERROR",
                         "fixed common blocks/errors/MM/non-SBF cross terms drifted")
                sbf_payload = {"sbf": record["input_components"]["sbf"],
                    "cross": {k: v for k, v in record["input_components"]["cross"].items()
                              if "SBF_HF" in k.split("|")}}
                sbf_digest = _sha(_canonical(sbf_payload))
                sbf_id = scenario["sbf_id"]
                if sbf_id not in sbf_variants:
                    sbf_variants[sbf_id] = sbf_digest
                _require(sbf_variants[sbf_id] == sbf_digest, "FAMILY_ERROR",
                         "same SBF recipe drifts between stellar labels")
            _require(record["support_receipt"] is None and record["normalization_receipt"] is None and
                     record["actual_rank"] is None, "SCOPE_ERROR", "qualification belongs to backend")
            result.append({"label": record["label"], "status": record["status"],
                           "record_sha256": saved_digest, "C_native_f64le_sha256": record["C_native_f64le_sha256"],
                           "response_binding": binding["five_model_response_sha256"],
                           "support_reference": binding["fixed_affine_support_reference"],
                           "normalization_reference": binding["normalization_recipe_reference"],
                           "support_and_normalization_status": "PENDING_BACKEND_QUALIFICATION"})
        return {"schema": "F9_COMPLETE_COVARIANCE_LABEL_MAP_V1", "request_id": REQUEST_ID,
                "metadata_sha256": METADATA_SHA256, "labels": result,
                "label_count": 600, "deduplication": "NONE",
                "ordered_map_sha256": _sha(_canonical(result)),
                "status": ("COMPLETE_LABEL_MAP_WITH_OPEN_COMPONENTS" if open_labels else
                           "ALL_600_ASSEMBLED_UNQUALIFIED_ENGINEERING_ONLY"),
                "open_labels": open_labels, "family_scope": self._meta["family_scope"],
                "O01_O02_ratified": False, "scientific_verdict": None}
