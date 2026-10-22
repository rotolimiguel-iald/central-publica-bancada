"""Static preparation audit only. No candidate/numpy/backend/service imports."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import os
import time

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
OUT = ROOT / "f9_physical_prior_preparation"
START = time.perf_counter()
CHECKS = []
PINS = []


def check(name, ok, detail=None):
    CHECKS.append({"name": name, "passed": bool(ok), "detail": detail})
    if not ok:
        raise RuntimeError("STATIC_CHECK_FAILED:" + name)


def pin(path):
    b = path.read_bytes()
    p = {"path": str(path), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
    PINS.append(p)
    return b, p


def constants(tree, names):
    return {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body
            if isinstance(n, ast.Assign) and len(n.targets) == 1
            and isinstance(n.targets[0], ast.Name) and n.targets[0].id in names}


raw, code_pin = pin(OUT / "physical_prior.py")
tree = ast.parse(raw)
check("candidate AST parses without import", isinstance(tree, ast.Module))
const = constants(tree, {"REQUEST_ID","SOURCE_PINS","MODELS","BETA_LIMITS","S_LIMITS","RD_LIMITS"})
check("request identity", const["REQUEST_ID"] == "df482198-56c4-4169-ae5e-3908f5d12f2c")
source_doc = json.loads(pin(OUT / "PIN_FONTES.json")[0])
for label, expected in source_doc["sources"].items():
    _, actual = pin(Path(expected["path"]))
    check("source custody " + label, actual == expected)
for key, pin_value in const["SOURCE_PINS"].items():
    check("candidate source pin " + key, pin_value == source_doc["sources"][key])
upstream = ast.parse((ROOT / "f9_five_model_assembly_preparation/five_model_assembly.py").read_bytes())
upconst = constants(upstream, {"BOUNDS","MODELS"})
check("same model family", const["MODELS"] == upconst["MODELS"])
for name, key in (("BETA_LIMITS","beta"),("S_LIMITS","s"),("RD_LIMITS","rd_Mpc")):
    check("unchanged prior bounds " + key, const[name] == upconst["BOUNDS"][key])
imports=[]
for n in ast.walk(tree):
    if isinstance(n,ast.Import):imports.extend(a.name for a in n.names)
    if isinstance(n,ast.ImportFrom):imports.append(n.module)
check("candidate imports only math", imports == ["math"])
calls=[ast.unparse(n.func) for n in ast.walk(tree) if isinstance(n,ast.Call)]
for bad in ("open","eval","exec","compile","__import__","np.linalg.eigh","np.linalg.svd",
            "np.linalg.inv","np.linalg.pinv","assemble_five","c.prepare_joint","np.load",
            "camb.get_results","scipy.integrate.quad"):
    check("no new solver/import/I/O call " + bad, bad not in calls)
check("reuse consumer complete packet once", calls.count("joint.evaluate_five") == 1)
check("reuse backend residualization twice", calls.count("engine.residualize") == 2)
check("reuse backend log integral", calls.count("engine.log_integral") == 1)
functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
check("single public integration function", "integrate_at_fixed_theta" in functions)
check("explicit keyword arguments", [v.arg for v in functions["integrate_at_fixed_theta"].args.kwonlyargs] ==
      ["assembly_sha256","background_json","consumer_module","precision_json","precision_sha256","services"])
check("no implicit dependency defaults", all(v is None for v in functions["integrate_at_fixed_theta"].args.kw_defaults))
text=raw.decode("utf-8")
invariants=[
 'self.a = float(projected @ projected)',
 'self.b = float(r @ projected)',
 'self.a != 0 or exact_float_zero',
 '"CURVATURE_UNDERFLOW"',
 'engine.residualize(direction[:, None])',
 'engine.residualize(residual[:, None])',
 'mu - joint._origin' if False else 'self.mean(x) - joint._origin',
 'k = math.fsum((self.b, prior_linear))',
 'h = math.fsum((curve.b, prior_linear, -curve.a * shift))',
 'prior_linear * peak',
 '-math.log(BETA_LIMITS[1] - BETA_LIMITS[0])',
 'math.log(lam / (S_LIMITS[1] - S_LIMITS[0]))',
 '_analytic(curves["H4_Cepheid"], -lam,',
 'direction5[3:16] = vectors["H5_rd_free"][3:16] * p5',
 '(I / math.log(10)) * ah',
 'dlo = -5 * math.log1p(S_LIMITS[1]) / math.log(10)',
 'dhi = -5 * math.log1p(S_LIMITS[0]) / math.log(10)',
 '1 / p5, 1 / RD_LIMITS[1], 1 / RD_LIMITS[0]',
 'math.log(width_q), -math.log(width_rd), -2 * math.log(qlo)',
 '2 * math.log(qlo / q)',
 'failure["exception"] = exc',
 'raise PriorError("QUADRATURE_CALLBACK_FAILED", "latched callback failure")',
 'counters["integrand_calls"] < precision["max_quadrature_evaluations"]',
 'result["evaluations"] == counters["integrand_calls"]',
 'area > 0',
 'counters["underflowed_nodes"] += 1',
 '"base_theta_prior": {"density_exact": "50/3", "applied": False, "integrated": False}',
 '"MM_status": "CONDITIONAL_UNRATIFIED"',
 '"theta_integrated_evidence": None',
 '"lnB": None, "p": None, "sigma": None, "verdict": None',
]
for fragment in invariants:
    check("source invariant " + fragment, fragment in text)
rd_func=functions["_rd_quadrature"]
check("H5 likelihood peak does not apply prior-linear shift",
      "peak = curve.peak()" in ast.unparse(rd_func))
for index,h in enumerate(n for n in ast.walk(tree) if isinstance(n,ast.ExceptHandler)):
    check("exception handler raises, never returns zero " + str(index),
          any(isinstance(n,ast.Raise) for n in ast.walk(h)) and
          not any(isinstance(n,ast.Return) for n in ast.walk(h)))
contract=json.loads(pin(OUT/"CONTRATO_API.json")[0])
check("contract persistent identity", contract["request_id"]==const["REQUEST_ID"])
check("no execution authority", contract["authorization"] is False and contract["claim"] is False)
check("no imports/observations/execution reported", contract["observed_reads"]==0 and
      contract["candidate_imports"]==0 and contract["scientific_executions"]==0)
check("both services explicitly not qualified here",
      contract["services"]["log_exp_quad_interval"]["not_implemented_or_qualified_here"] is True and
      contract["services"]["positive_quad_1d"]["not_implemented_or_qualified_here"] is True)
check("no proposed campaign", contract["does_not_propose_campaign"] is True)
for name in ("IDENTIDADE_PREPARACAO.json","ALTERNATIVAS_ANTES_IMPLEMENTACAO.json","DERIVACAO.md","API_CONTRATO.md"):
    pin(OUT/name)
manifest_path=ROOT/"f9_likelihood_consumer_preparation/MANIFESTO_PREPARACAO.json"
manifest=json.loads(manifest_path.read_bytes())
for expected in manifest["artifacts"]:
    _,actual=pin(Path(expected["path"]))
    check("frozen consumer artifact " + expected["relative"],
          all(actual[k]==expected[k] for k in ("path","bytes","sha256")))
receipt={
 "schema":"F9_PHYSICAL_PRIOR_STATIC_RECEIPT_V1","request_id":const["REQUEST_ID"],
 "created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "statute":"REAL_BYTES_AST_ONLY_NOT_NUMERICAL_TESTS",
 "checks":CHECKS,"all_passed":all(c["passed"] for c in CHECKS),"pins_read":PINS,
 "candidate_pin":code_pin,"candidate_imports":0,"numpy_scipy_backend_imports":0,
 "controls_run":0,"observed_reads":0,"science_calls":0,"claims":0,"authorizations":0,
 "own_static_audit_seconds_before_persistence":time.perf_counter()-START,
 "preparation_auxiliary_error":"First source-key writer used Windows separator keys and raised KeyError before any candidate/source-pin files were written; corrected to relative.as_posix. No scientific execution.",
 "limitation":"AST/source fragments and custody checks do not exercise formulas, tails, priors, geometry or precision services."
}
p=OUT/"RECIBO_ESTATICO.json"
assert not p.exists()
b=(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
t=p.with_name(p.name+".tmp")
with t.open("xb") as f:f.write(b);f.flush();os.fsync(f.fileno())
assert t.read_bytes()==b
os.replace(t,p)
print(json.dumps({"checks":len(CHECKS),"all_passed":receipt["all_passed"],
 "receipt_bytes":len(b),"receipt_sha256":hashlib.sha256(b).hexdigest(),
 "candidate_imports":0,"science_calls":0},ensure_ascii=False))
