"""Static archival inventory only. Never imports original project modules or runs fits."""
from pathlib import Path
import ast, hashlib, json, os, datetime, difflib
ROOT=Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\reproducao_fase45_conjunta")
BANK=Path(r"C:\IALD\Bancada_Um")
D1=Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\d1_camb\v3")
ROOT.mkdir(parents=True,exist_ok=True)
def sha(b): return hashlib.sha256(b).hexdigest()
def write_new(name,obj):
    p=ROOT/name; assert not p.exists(),str(p)
    b=(json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode()
    t=p.with_suffix(p.suffix+".tmp"); t.write_bytes(b); assert t.read_bytes()==b; os.replace(t,p)
    return {"path":str(p),"bytes":len(b),"sha256":sha(b)}
def safe(n):
    if isinstance(n,ast.Call):
        if isinstance(n.func,ast.Name) and n.func.id=="dict": return {k.arg:safe(k.value) for k in n.keywords}
        if isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=="np" and n.func.attr=="array": return safe(n.args[0])
    if isinstance(n,ast.BinOp):
        a,b=safe(n.left),safe(n.right)
        if isinstance(n.op,ast.Add): return a+b
        if isinstance(n.op,ast.Div): return a/b
    if isinstance(n,ast.List): return [safe(e) for e in n.elts]
    if isinstance(n,ast.Tuple): return tuple(safe(e) for e in n.elts)
    return ast.literal_eval(n)
def assignment(tree,name):
    return next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
paths={}
for phase,tag in [("fase4_desvio_30set","FASE4_DESVIO_20260930"),("fase5_sh0es_01out","FASE5_SH0ES_20261001")]:
    base=BANK/"investigacao"/phase
    for name in ["PREREGISTRO_"+tag+".json","RESULTADO_"+tag+".json","RELATORIO_"+tag+".md", "rodar_fase"+("4" if "fase4" in phase else "5")+".py"]:
        paths[phase+"/"+name]=base/name
for name in ["motor.py","evidencia.py","fontes.py","fundo_gpu.py","camb_tabela.py","pantheon_cov.py","amostrador.py","regua.py",
             "motor.py.bak_20261001_123905_sh0es","motor.py.bak_20261001_163715_cccov","motor.py.bak_20261001_163751_cccov",
             "evidencia.py.bak_20261001_123905_sh0es","fontes.py.bak_20261001_123905_sh0es","fontes.py.bak_20261001_163715_cccov",
             "fundo_gpu.py.bak_20261001_123905_sh0es","pantheon_cov.py.bak_20261001_123905_sh0es"]:
    paths["bancada/"+name]=BANK/"bancada"/name
for name in ["evidencia_bayes.py","patch_fase4_desvio.py","patch_sh0es_calibradores.py"]:
    paths["ferramentas/"+name]=BANK/"ferramentas"/name
for name in ["d1_v3_pipeline.py","MANIFESTO_D1_V3.json","saida/D1_CAMB_V3_REAL_RESULT.json"]:
    paths["d1/"+name]=D1/name
for name in ["camb_lcdm_v1.npz","camb_lcdm_v1.json"]:
    paths["tabelas/"+name]=BANK/"tabelas"/name
for name in ["moresco_2022_cc.json","chen_huang_wang_2019_1808.05724.pdf"]:
    paths["fontes_externas/"+name]=BANK/"fontes_externas"/name
base=Path(r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\_originais")
for name in ["desi_gaussian_bao_ALL_GCcomb_mean.txt","desi_gaussian_bao_ALL_GCcomb_cov.txt"]: paths["dr2/"+name]=base/name
paths["pantheon/table"]=Path(r"C:\IALD\observaveis_tgl\tgl_data_cache\pantheon\Pantheon+SH0ES.dat")
paths["pantheon/cov"]=Path(r"C:\IALD\projetos_pyhton\acom\tgl_data_cache\pantheon_covariance.dat")
paths["pantheon/local_table"]=ROOT.parent/"reproducao_fase5"/"Pantheon+SH0ES.dat"
paths["pantheon/local_cov"]=ROOT.parent/"reproducao_fase5"/"pantheon_covariance.dat"
paths["ordem018"]=ROOT.parent.parent.parent/"PARA_CHATGPT"/"ORDEM_018_o_discriminante.md"
inventory={}; texts={}; trees={}
for key,p in paths.items():
    b=p.read_bytes(); inventory[key]={"path":str(p),"bytes":len(b),"sha256":sha(b)}
    if ".py" in p.name:
        txt=b.decode("utf-8-sig"); tree=ast.parse(txt); texts[key]=txt; trees[key]=tree
        inventory[key]["definitions"]=[{"name":n.name,"start":n.lineno,"end":n.end_lineno} for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.ClassDef))]
checks={}
p4=json.loads(paths["fase4_desvio_30set/PREREGISTRO_FASE4_DESVIO_20260930.json"].read_bytes())
r4=json.loads(paths["fase4_desvio_30set/RESULTADO_FASE4_DESVIO_20260930.json"].read_bytes())
p5=json.loads(paths["fase5_sh0es_01out/PREREGISTRO_FASE5_SH0ES_20261001.json"].read_bytes())
r5=json.loads(paths["fase5_sh0es_01out/RESULTADO_FASE5_SH0ES_20261001.json"].read_bytes())
checks["phase4_preregister"]=r4["preregistro_sha256"]==inventory["fase4_desvio_30set/PREREGISTRO_FASE4_DESVIO_20260930.json"]["sha256"]
checks["phase5_preregister"]=r5["preregistro_sha256"]==inventory["fase5_sh0es_01out/PREREGISTRO_FASE5_SH0ES_20261001.json"]["sha256"]
man=json.loads(paths["d1/MANIFESTO_D1_V3.json"].read_bytes())
checks["pipeline_pin"]=man["arquivos"]["d1_v3_pipeline.py"]==inventory["d1/d1_v3_pipeline.py"]["sha256"]
dr=json.loads(paths["d1/saida/D1_CAMB_V3_REAL_RESULT.json"].read_bytes())
checks["pipeline_result_pin"]=dr["scripts"]["pipeline"]==inventory["d1/d1_v3_pipeline.py"]["sha256"]
cam=json.loads(paths["tabelas/camb_lcdm_v1.json"].read_bytes())
checks["table_pin"]=cam["sha256"]==inventory["tabelas/camb_lcdm_v1.npz"]["sha256"]
for typ in ["table","cov"]: checks["pantheon_local_"+typ]=inventory["pantheon/"+typ]["sha256"]==inventory["pantheon/local_"+typ]["sha256"]
checks["pantheon_archived_table"]=r5["pantheon_sh0es"]["fonte"]["sha256"]==inventory["pantheon/table"]["sha256"]
checks["pantheon_archived_cov"]=r5["pantheon_sh0es"]["proveniencia"]["covariancia"]["fonte_sha256"]==inventory["pantheon/cov"]["sha256"]
checks["cc_archived"]=r4["cc"]["json_sha256"]==inventory["fontes_externas/moresco_2022_cc.json"]["sha256"]
tree=trees["d1/d1_v3_pipeline.py"]
lim=safe(assignment(tree,"LIMITES")); alpha=safe(assignment(tree,"ALPHA_FINE_CODATA_2018")); rows=safe(assignment(tree,"DESI_ROWS"))
fn=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=="_dados_reais")
observed=safe(next(n for n in ast.walk(fn) if isinstance(n,ast.Return)).value)
source=trees["bancada/fontes.py"]
rho=safe(assignment(source,"rho")); sig=safe(assignment(source,"sig")); corr=safe(assignment(source,"DR1_CORRELACOES"))
pcov=[[rho[i][j]*sig[i]*sig[j] for j in range(3)] for i in range(3)]
dcov=[[0.0]*len(rows) for _ in rows]
for i,(zi,ti,si) in enumerate(rows):
    dcov[i][i]=si*si
    for j,(zj,tj,sj) in enumerate(rows[:i]):
        if abs(zi-zj)<1e-6 and {ti,tj}=={0,1}: dcov[i][j]=dcov[j][i]=corr[round(zi,3)]*si*sj
cc=json.loads(paths["fontes_externas/moresco_2022_cc.json"].read_bytes())
inputs={"status":"STATIC_READ_AND_DETERMINISTIC_COVARIANCE_ASSEMBLY_NOT_A_FIT","alpha_codata2018":alpha,"beta_rule":"ALPHA_FINE_CODATA_2018 * sqrt(e), runtime only",
        "limits_declared":lim,"planck_mean":observed["planck_mean"],"planck_cov_chen2019":pcov,"planck_cov_recipe":{"sigma":sig,"correlation":rho,"source":"fontes.py:163-174"},
        "desi_dr1_rows_z_kind_sigma":rows,"desi_dr1_values":observed["desi_vals"],"desi_dr1_cov":dcov,"desi_dr1_corr":corr,
        "sh0es_local":{"mean":observed["sh0es_mean"],"sigma":safe(assignment(tree,"SH0ES_SIGMA"))},
        "cc_data_z_H_sigma":cc["data"],"cc_cov_diagonal":[[row[2]**2 if i==j else 0.0 for j in range(len(cc["data"]))] for i,row in enumerate(cc["data"])],
        "camb_manifest":cam,"camb_effective_bounds":{k:[v[0]+(v[1]-v[0])/(v[2]-1),v[1]-(v[1]-v[0])/(v[2]-1)] for k,v in cam["grade"].items()}}
covreceipt=write_new("ENTRADAS_HISTORICAS_E_COVARIANCIAS.json",inputs)
targets={}
for phase,p,r in [("fase4",p4,r4),("fase5",p5,r5)]:
    families={}
    for name,spec in p["familias"].items():
        f=r["familias"][name]; grouping="nucleos" if phase=="fase4" else "leituras"
        families[name]={"datasets":spec["conjuntos"],"contains_ladder":any(x in spec["conjuntos"] for x in ["sh0es_local","pantheon_sh0es"]),
                        "historical_role":spec["papel"],"historic_blinding_declaration":spec["cego"],
                        "groups":{g:{"options":v["opcoes"],"target_json_path":"/familias/"+name+"/"+grouping+"/"+g,"statistics_keys":[k for k in v if k not in ["segundos_comparar","segundos"]],"evidence_prior":v.get("evidencia",{}).get("prior")} for g,v in f.get(grouping,{}).items()},
                        "posterior_present":any(k.startswith("posterior") for k in f)}
    targets[phase]={"families":families,"z_star_fixed":p["z_star"],"other_keys":[k for k in r if k not in ["familias","veredito"]]}
diffs={}
for stem,old in [("motor","motor.py.bak_20261001_163715_cccov"),("motor","motor.py.bak_20261001_123905_sh0es"),
                 ("evidencia","evidencia.py.bak_20261001_123905_sh0es"),("fontes","fontes.py.bak_20261001_163715_cccov"),
                 ("fundo_gpu","fundo_gpu.py.bak_20261001_123905_sh0es")]:
    oldkey="bancada/"+old; newkey="bancada/"+stem+".py"
    diffs[old]=list(difflib.unified_diff(texts[oldkey].splitlines(),texts[newkey].splitlines(),fromfile=old,tofile=stem+".py",lineterm=""))
receipt=write_new("AUDITORIA_E_CONTRATOS.json",{"created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"identity":"chatgpt-codex/ordem-018/derivacoes",
 "scope":"PLAN_ONLY_F1b_HISTORICAL_REPRODUCTION","files":inventory,"checks":checks,"derived_covariance_artifact":covreceipt,"target_contracts":targets,
 "source_diffs":diffs,"executed_originals":False,"fits_executed":False,"new_data_downloaded":False})
print(json.dumps({"audit":receipt,"inputs":covreceipt,"checks":checks,"all_checks":all(checks.values()),"source_count":len(inventory)},ensure_ascii=False))
