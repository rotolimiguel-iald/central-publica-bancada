"""Explicit pre-audit import phase B. No scientific function is called here."""
import hashlib
import importlib
import sys
import sysconfig
from pathlib import Path

TARGETS = ("lal", "lalsimulation", "bilby.gw.source", "temporal_contract")


def file_pin(path):
    path = Path(path)
    data = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def require_pin(path, expected):
    actual = file_pin(path)
    if actual["bytes"] != expected["bytes"] or actual["sha256"] != expected["sha256"]:
        raise ValueError("Pinned bytes differ: " + str(path))
    return actual


def _module_pin(module, expected_path, expected):
    path = Path(module.__file__).resolve()
    if path != Path(expected_path).resolve():
        raise ValueError("Unexpected loaded module origin: " + module.__name__)
    pin = require_pin(path, expected)
    spec = getattr(module, "__spec__", None)
    if spec is None or Path(spec.origin).resolve() != path:
        raise ValueError("Loaded module spec/file mismatch")
    return dict(pin, module=module.__name__,
                loader=type(spec.loader).__module__ + "." + type(spec.loader).__qualname__)


def preload_known_imports(root, runtime, plan, source, adapter):
    """Called before the strict P3 hook; does not install or weaken that hook."""
    root = Path(root).resolve()
    if plan["targets"] != list(TARGETS) or plan["alternative"] != "B":
        raise ValueError("Only the frozen four-target phase B is supported")
    if not sys.dont_write_bytecode or sys.pycache_prefix != str(root / "UNUSED_BYTECODE_CACHE"):
        raise ValueError("Source-loading bytecode policy must precede imports")
    runtime_index = {str(Path(row["path"]).resolve()): row for row in runtime["files"]}
    if len(runtime_index) != len(runtime["files"]):
        raise ValueError("Duplicate runtime pin")
    if sys.modules.get("pseob_source") is not source or "src.pseob_source" in sys.modules:
        raise ValueError("A single canonical source module is required")
    if sys.modules.get("synthetic_adapter_v2") is not adapter:
        raise ValueError("Adapter module identity differs")
    if adapter.pseob_frequency_domain is not source.pseob_frequency_domain:
        raise ValueError("Adapter/source function binding differs")
    if adapter.parameter_conversion is not source.parameter_conversion:
        raise ValueError("Adapter/source conversion binding differs")
    local_pins = plan["local_modules"]
    loaded = [_module_pin(source, root / "src/pseob_source.py", local_pins["pseob_source"]),
              _module_pin(adapter, root / "src/synthetic_adapter_v2.py",
                          local_pins["synthetic_adapter_v2"])]
    for name, function in (("pseob_frequency_domain", source.pseob_frequency_domain),
                           ("parameter_conversion", source.parameter_conversion)):
        if function.__globals__ is not source.__dict__:
            raise ValueError("Source function globals differ: " + name)
        if Path(function.__code__.co_filename).resolve() != root / "src/pseob_source.py":
            raise ValueError("Source code origin differs: " + name)
    if source.AUDIT_CHECKPOINT is not None:
        raise ValueError("Phase B must precede source checkpoint installation")
    before = set(sys.modules)
    for name in TARGETS:
        target = plan["target_pins"][name]
        path = root / target["relative_path"] if "relative_path" in target else Path(target["path"])
        require_pin(path, target)
        module = importlib.import_module(name)
        loaded.append(_module_pin(module, path, target))
    temporal = sys.modules["temporal_contract"]
    if Path(temporal.validate_time_contract.__code__.co_filename).resolve() != root / "src/temporal_contract.py":
        raise ValueError("Temporal function code origin differs")
    if not callable(sys.modules["bilby.gw.source"].lal_binary_black_hole):
        raise ValueError("Expected Bilby source function is absent")

    # Account for actual file-backed modules. Runtime metadata remains historical
    # until these exact files are read here. Python stdlib is a distinct class.
    stdlib = Path(sysconfig.get_path("stdlib")).resolve()
    rows = []
    for name, module in sorted(tuple(sys.modules.items())):
        origin = getattr(module, "__file__", None)
        if not origin:
            continue
        path = Path(origin).resolve()
        if str(path) in runtime_index:
            row = require_pin(path, runtime_index[str(path)])
            scope = "HISTORICAL_RUNTIME_PIN_RECHECKED"
        elif path == root or root in path.parents:
            relative = path.relative_to(root).as_posix()
            expected = plan["package_python_pins"].get(relative)
            if expected is None:
                raise ValueError("Unregistered local module: " + relative)
            row = require_pin(path, expected)
            scope = "PACKAGE_PIN_RECHECKED"
        elif (path == stdlib or stdlib in path.parents) and not any(
                part in ("site-packages", "dist-packages") for part in path.parts):
            row = file_pin(path)
            scope = "STDLIB_FRESH_METADATA_NOT_HISTORICAL_PIN"
        else:
            raise ValueError("Loaded file is outside pinned runtime/package/stdlib: " + str(path))
        rows.append(dict(row, module=name, scope=scope, new_during_phase_B=name not in before))
    return {
        "status": "EXPLICIT_PREHOOK_IMPORTS_COMPLETE",
        "alternative": "B",
        "audit_boundary": "Imports above occurred BEFORE the strict P3 Python audit hook",
        "targets": loaded,
        "file_backed_loaded_modules": rows,
        "source_adapter_same_function": True,
        "source_checkpoint_installed_yet": False,
        "scientific_functions_called_by_this_module": 0,
        "native_initialization_possible_during_import": True,
        "transitive_native_syscalls_contained": False,
        "later_import_closure_proved": False,
        "scientific_qualification": False
    }
