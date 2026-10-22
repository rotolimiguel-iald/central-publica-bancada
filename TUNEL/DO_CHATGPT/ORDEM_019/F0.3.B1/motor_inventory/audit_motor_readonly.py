"""Static audit only: no import of originals, likelihood call, scientific fit, or Bench write."""
from pathlib import Path
import ast, datetime, hashlib, json, math, re
ROOT=Path(__file__).resolve().parent
BENCH=Path(r"C:\IALD\Bancada_Um")
NOS=Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
D1=NOS.parent/"cache/d1_camb/v3"
RANGES={
"bancada/fontes.py":[(51,62),(65,92),(95,117),(126,136),(142,174),(177,193),(196,210)],
"bancada/motor.py":[(24,44),(47,61),(64,95),(102,126),(156,215),(225,295)],
"bancada/fundo_gpu.py":[(2,15),(21,28),(60,110),(112,134),(151,165)],
"bancada/camb_tabela.py":[(2,6),(17,35),(50,82)],
"bancada/regua.py":[(2,26),(38,51),(67,69),(80,97)],
"bancada/evidencia.py":[(17,27),(36,88),(139,174),(209,229)],
"bancada/pantheon_cov.py":[(2,6),(26,45),(50,79)],
"ferramentas/validar_tudo.py":[(20,74)],
"ferramentas/validar_corrigido.py":[(2,4),(18,39),(49,65)],
}
FILES=list(RANGES)+[
"estado/validacao_bancada.json","estado/validacao_corrigido.json",
"estado/validacao_pantheon.json","estado/validacao_mcmc_d1.json",
"ferramentas/validar_pantheon.py","ferramentas/validar_mcmc_d1.py",
"tabelas/camb_lcdm_v1.json","tabelas/camb_lcdm_v1.npz",
"investigacao/fase1_eff_30set/CONFIRMACAO_OPERADOR_MAPA_R_30SET.json",
]

def digest(p):
    b=p.read_bytes(); return b, hashlib.sha256(b).hexdigest()

def record(p,ranges=()):
    b,h=digest(p); r={"path":str(p),"sha256":h,"bytes":len(b),"mtime_ns":p.stat().st_mtime_ns}
    if ranges:
        lines=b.decode("utf-8-sig").splitlines(); r["line_count"]=len(lines); r["excerpts"]=[]
        for first,last in ranges:
            last=min(last,len(lines))
            if not 1<=first<=last: raise ValueError((p,first,last))
            r["excerpts"].append({"first":first,"last":last,"text":"\n".join(f"{i}: {lines[i-1]}" for i in range(first,last+1))})
    return r

def literal_assign(text,name):
    tree=ast.parse(text)
    nodes=[n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)]
    if len(nodes)!=1:raise ValueError((name,len(nodes)))
    n=nodes[0]
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="dict":return {k.arg:ast.literal_eval(k.value) for k in n.keywords}
    return ast.literal_eval(n)

def main():
    output=ROOT/"INVENTARIO_MOTOR_20261009.json"
    if output.exists():raise FileExistsError(output)
    sources=[record(BENCH/rel,RANGES.get(rel,())) for rel in FILES]
    um,umh=digest(NOS/"um.py"); ums=um.decode("utf-8-sig")
    matches=list(re.finditer(r"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)",ums,re.M))
    if len(matches)!=1:raise ValueError("alpha source count")
    alpha=float(matches[0].group(1))
    pipeline=D1/"d1_v3_pipeline.py"; pb,ph=digest(pipeline)
    manifest=json.loads((D1/"MANIFESTO_D1_V3.json").read_text(encoding="utf-8-sig"))
    palpha=literal_assign(pb.decode("utf-8-sig"),"ALPHA_FINE_CODATA_2018")
    priors=literal_assign(pb.decode("utf-8-sig"),"LIMITES")
    for p in [pipeline,D1/"MANIFESTO_D1_V3.json",D1/"tgl_camb_worker_v3.py"]:sources.append(record(p))
    sources.append(record(NOS/"um.py",[(96,96),(165419,165421),(166227,166232),(194754,194764)]))
    table=json.loads((BENCH/"tabelas/camb_lcdm_v1.json").read_text(encoding="utf-8"))
    tb,th=digest(BENCH/"tabelas/camb_lcdm_v1.npz")
    support={}
    for name,(lo,hi,n) in table["grade"].items():
        step=(hi-lo)/(n-1);support[name]=[lo+step,hi-step]
    vol_prior=math.prod(priors[k][1]-priors[k][0] for k in support)
    intersect=math.prod(max(0,min(priors[k][1],support[k][1])-max(priors[k][0],support[k][0])) for k in support)
    motor=(BENCH/"bancada/motor.py").read_text(encoding="utf-8-sig")
    presets={n:literal_assign(motor,n) for n in ["OPCOES_SELADO","OPCOES_CORRIGIDO","OPCOES_TGL","OPCOES_ARTIGO"]}
    vb=json.loads((BENCH/"estado/validacao_bancada.json").read_text(encoding="utf-8-sig"))
    vc=json.loads((BENCH/"estado/validacao_corrigido.json").read_text(encoding="utf-8-sig"))
    result={"unit":"F0.3.B1","claim_event":621,"created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "author":"codex-gerente-tgl / nu2_theory_sources","mode":"STATIC_READONLY_NO_MODEL_IMPORT_NO_NEW_FIT",
      "source_exposure":"read code and historical validation reports; did not parse observed dataset files, run likelihood or fit",
      "sources":sources,"um_version_literal":literal_assign(ums,"UM_VERSION"),"um_sha256":umh,
      "constants":{"alpha_source":alpha,"beta_runtime":alpha*math.sqrt(math.e),"alpha_matches_pipeline":alpha==palpha,"alpha_line":ums[:matches[0].start()].count("\n")+1},
      "checks":{"pipeline_matches_manifest":ph==manifest["arquivos"][pipeline.name],"table_matches_manifest":th==table["sha256"]},
      "presets":presets,"table_config":table,"table_useful_support":support,"pipeline_prior_limits":priors,
      "table_fraction_of_pipeline_3d_prior_volume":intersect/vol_prior,
      "table_fraction_is_not_posterior_mass":True,
      "existing_validations":{"reproduction":{"when":vb.get("quando"),"summary":vb.get("resumo_curto")},"corrected":{"when":vc.get("quando"),"verdict":vc.get("veredito"),"cases":{k:v.get("passa") for k,v in vc.get("casos",{}).items()}}},
      "no_bench_write":True,"no_runtime_resident_verification":True,"new_empirical_significance":None}
    with output.open("x",encoding="utf-8",newline="\n") as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write("\n")
    print(json.dumps({"path":str(output),"sha256":hashlib.sha256(output.read_bytes()).hexdigest(),"sources":len(sources),"checks":result["checks"],"presets":presets,"prior":priors,"support":support,"fraction":intersect/vol_prior},ensure_ascii=False))
if __name__=="__main__":main()
