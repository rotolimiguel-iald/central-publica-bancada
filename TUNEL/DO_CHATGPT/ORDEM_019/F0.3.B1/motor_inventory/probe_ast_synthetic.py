"""Execute selected AST functions with symbolic mocks, not the original module or data."""
from pathlib import Path
import ast,datetime,hashlib,json,types
ROOT=Path(__file__).resolve().parent
BENCH=Path(r"C:\IALD\Bancada_Um\bancada")
inv=json.loads((ROOT/"INVENTARIO_MOTOR_20261009.json").read_text(encoding="utf-8"))
expected={s["path"]:s["sha256"] for s in inv["sources"]}

def checked_ast(name):
 p=BENCH/name;b=p.read_bytes();h=hashlib.sha256(b).hexdigest()
 if h!=expected[str(p)]:raise ValueError("source changed")
 return ast.parse(b.decode("utf-8-sig")),h

motor,mh=checked_ast("motor.py");evid,eh=checked_ast("evidencia.py")
selected=[]
for node in motor.body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id.startswith(("OPCOES_","_OPCOES_")) for t in node.targets):selected.append(node)
 if isinstance(node,ast.FunctionDef) and node.name=="opcoes_de":selected.append(node)
for node in evid.body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="CONJUNTOS" for t in node.targets):selected.append(node)
 if isinstance(node,ast.FunctionDef) and node.name=="_conj":selected.append(node)
 if isinstance(node,ast.ClassDef) and node.name=="Evidencia":
  curves=next(n for n in node.body if isinstance(n,ast.FunctionDef) and n.name=="_curvas")
  evaluate=next(n for n in node.body if isinstance(n,ast.FunctionDef) and n.name=="avaliar")
  selected.append(curves)
env={}
exec(compile(ast.Module(body=selected,type_ignores=[]),"<extracted-source-AST>","exec"),env)

class ProbeHit(Exception):pass
class Columns:
 def __init__(self,row):self.row=row
 def __getitem__(self,key):return self.row[key[1]]
class Fondo:
 def fundo(self,H0,wb,wc,beta,c):raise ProbeHit({"H0":H0,"wb":wb,"wc":wc,"beta":beta,"c":c})
mock_torch=types.SimpleNamespace(float64="symbolic_float64",linspace=lambda *a,**k:"unused_symbolic_z")
env["torch"]=mock_torch
beta=inv["constants"]["beta_runtime"]
self=types.SimpleNamespace(m=types.SimpleNamespace(dev="symbolic_no_GPU",_t=lambda th:Columns(th),tab=lambda *args:({},True),fundo=Fondo()))
row=[67.5,.02237,.1200,beta,0.0]
try:env["_curvas"](self,row)
except ProbeHit as hit:actual=hit.args[0]
else:raise AssertionError("probe did not intercept first background call")
opt=env["opcoes_de"]({"modo":"artigo"})
expected_beta=0.0 if opt["beta_no_fundo"]=="nao" else beta
calls=[n for n in ast.walk(evaluate) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="_curvas"]
all_sets=env["_conj"](env["CONJUNTOS"])
duplicates=env["_conj"](["sh0es","sh0es"])
overlap=env["_conj"](["pantheon","pantheon_sh0es","sh0es","sh0es_local","desi_dr1","desi_dr2"])
result={"unit":"F0.3.B1","when_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"mode":"AST_WITH_SYMBOLIC_MOCKS",
"sources_sha256":{"motor.py":mh,"evidencia.py":eh},"imports_of_originals":False,"real_data_or_scientific_fit":False,
"curve_probe":{"source_lines":[52,64,69],"caller_curve_argument_counts":[len(c.args) for c in calls],"artigo_options":opt,"expected_background_beta":expected_beta,"actual_first_background_call":actual,"material_mode_mismatch_reproduced":actual["beta"]!=expected_beta,"scope":"intercepts first FundoV3Lote call, does not calculate any distance or chi2"},
"selection_probe":{"all_default_evaluate_sets":all_sets,"overlap_list_accepted":overlap,"duplicates_accepted":duplicates,"scope":"chi2 membership avoids duplicating the SAME identifier, but n_dados sums input IDs; distinct overlapping datasets have separate terms"},
"no_bench_write":True}
out=ROOT/"PROBE_AST_SINTETICO_20261009.json"
with out.open("x",encoding="utf-8",newline="\n") as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write("\n")
print(json.dumps({"path":str(out),"sha256":hashlib.sha256(out.read_bytes()).hexdigest(),"curve_bug":result["curve_probe"]["material_mode_mismatch_reproduced"],"expected":expected_beta,"actual":actual["beta"],"overlap_accepted":overlap},ensure_ascii=False))
