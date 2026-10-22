"""Compile frozen E45A receipts only: no likelihood import, grid, fit, or new data."""
import json,math,pathlib,hashlib,datetime,os
ROOT=pathlib.Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_new(n,b):
 p=ROOT/n;assert not p.exists(),n
 temp=p.with_suffix(p.suffix+".tmp");temp.write_bytes(b);assert temp.read_bytes()==b;os.replace(temp,p)
 return dict(name=n,bytes=len(b),sha256=sha(p))
def json_new(n,obj):return write_new(n,(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode())
def main():
 state=read("E45A_ESTADO_CAMPANHA_V2.json");camp=read("E45A_CONTINUACAO_CAMPANHA_V2.json")
 assert state["status"]=="COMPLETE" and state["next_index"]==11 and state["current_index"] is None
 assert state["campaign_sha256"]==sha(ROOT/"E45A_CONTINUACAO_CAMPANHA_V2.json")
 assert all(u["status"]=="COMPLETE_VERIFIED" and all(u["checks"].values()) for u in state["units"])
 for p in camp["source_pins"]:assert sha(ROOT/p["name"])==p["sha256"],p["name"]
 for u in state["units"]:assert sha(ROOT/u["unit"])==u["result_sha256"],u["unit"]
 old=read("P45_ALVOS_HISTORICOS.json");cfg=read("E45_PROTOCOLO_PILOTO_E_GRADE.json");tol=cfg["tolerances"]
 families={};files=[];raw={};pairs={"tgl_vs_lcdm":("tgl","lcdm"),"livre_vs_lcdm":("livre","lcdm"),"tgl_vs_livre":("tgl","livre")}
 for family in ("P4_d1b","P5_sombra"):
  hist=old[family]["evidencia"];f={"models":{},"lnB":{},"savage_dickey":{},"beta_marginal":{}}
  for model in ("lcdm","tgl","livre"):
   vals={}
   for n in (25,35):
    name=f"E45A_GRID_{family}_{model}_n{n}.json";p=ROOT/name;d=read(name);raw[name]=d
    assert d["status"]=="EXACT_SINGLE_GRID_COMPLETE_NO_VERDICT" and d["observational_integral_completed"]
    assert d["processed_nodes"]==d["total_nodes"]==n**(4 if model=="livre" else 3)
    assert d["finite_nodes"]==n**3*(n-2 if model=="livre" else 1)
    assert d["resources"]["wall"]<600 and d["resources"]["peak_bytes"]<512*1024**2 and d["environment"]["threads"]==1
    assert math.isfinite(d["lnZ"]) and not d["fits_rerun"] and not d["originals_executed"] and not d["monte_carlo"] and d["scientific_verdict"] is None
    files.append(dict(name=name,bytes=p.stat().st_size,sha256=sha(p)))
    vals[str(n)]={k:d[k] for k in ("lnZ","laplace_diag_lnZ","resources","processed_nodes","finite_nodes","backgrounds_evaluated","bounds","steps")}
    vals[str(n)]["laplace_diag_minus_grid"]=d["laplace_diag_lnZ"]-d["lnZ"]
    if model=="livre":
     f["savage_dickey"][str(n)]=dict(d["savage_dickey"])
     f["beta_marginal"][str(n)]=d["beta_marginal"]
   delta=vals["35"]["lnZ"]-vals["25"]["lnZ"]
   f["models"][model]={"archive_n25_lnZ":hist["lnZ"][model],"grids":vals,"n25_minus_archive":vals["25"]["lnZ"]-hist["lnZ"][model],
    "n35_minus_n25":delta,"abs_grid_difference":abs(delta),"archive_n25_tolerance_pass":abs(vals["25"]["lnZ"]-hist["lnZ"][model])<=tol["future_lnZ_abs"],
    "discretization_diagnostic_pass":abs(delta)<=tol["future_grid_difference_diagnostic_threshold"]}
  for key,(a,b) in pairs.items():
   v25=f["models"][a]["grids"]["25"]["lnZ"]-f["models"][b]["grids"]["25"]["lnZ"]
   v35=f["models"][a]["grids"]["35"]["lnZ"]-f["models"][b]["grids"]["35"]["lnZ"]
   f["lnB"][key]={"n25":v25,"n35":v35,"archive_n25":hist["lnB"][key],"n25_minus_archive":v25-hist["lnB"][key],"n35_minus_n25":v35-v25,
    "archive_tolerance_pass":abs(v25-hist["lnB"][key])<=tol["future_lnB_abs"]}
  for n in ("25","35"):
   sd=f["savage_dickey"][n]
   direct={"tgl_vs_livre":f["lnB"]["tgl_vs_livre"]["n"+n],"lcdm_vs_livre":-f["lnB"]["livre_vs_lcdm"]["n"+n]}
   f["savage_dickey"][n]={"values":sd,"minus_direct_grid_lnB":{k:sd[k]-direct[k] for k in sd}}
  f["savage_dickey"]["n25_minus_archive"]={k:f["savage_dickey"]["25"]["values"][k]-hist["savage_dickey"][k] for k in hist["savage_dickey"]}
  f["savage_dickey"]["archive_tolerance_pass"]=all(abs(x)<=tol["future_SD_against_archival_abs"] for x in f["savage_dickey"]["n25_minus_archive"].values())
  f["savage_dickey"]["n35_minus_n25"]={k:f["savage_dickey"]["35"]["values"][k]-f["savage_dickey"]["25"]["values"][k] for k in hist["savage_dickey"]}
  maxdiff=max(x["abs_grid_difference"] for x in f["models"].values())
  f["max_grid_difference"]={"measured":maxdiff,"archive":hist["erro_quadratura_max"],"difference":maxdiff-hist["erro_quadratura_max"],"engineering_tolerance_0_001_pass":abs(maxdiff-hist["erro_quadratura_max"])<=.001}
  f["resources"]={"wall_sum":sum(d["resources"]["wall"] for k,d in raw.items() if k.startswith("E45A_GRID_"+family+"_")),
    "cpu_sum":sum(d["resources"]["cpu"] for k,d in raw.items() if k.startswith("E45A_GRID_"+family+"_")),
    "peak_bytes_max":max(d["resources"]["peak_bytes"] for k,d in raw.items() if k.startswith("E45A_GRID_"+family+"_"))}
  families[family]=f
 checks={"all_units_complete":True,"all_source_pins_intact":True,"all_result_hashes_match":True,"all_limits_pass":True,
 "all_n25_lnZ_reproduced":all(m["archive_n25_tolerance_pass"] for f in families.values() for m in f["models"].values()),
 "all_n25_lnB_reproduced":all(v["archive_tolerance_pass"] for f in families.values() for v in f["lnB"].values()),
 "all_n25_SD_reproduced":all(f["savage_dickey"]["archive_tolerance_pass"] for f in families.values()),
 "n25_n35_diagnostic_below_threshold":all(m["discretization_diagnostic_pass"] for f in families.values() for m in f["models"].values()),
 "max_grid_difference_reproduced":all(f["max_grid_difference"]["engineering_tolerance_0_001_pass"] for f in families.values())}
 out={"identity":"chatgpt-codex/ordem-018/derivacoes","created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "status":"HISTORICAL_RELATIVE_EVIDENCE_REPRODUCTION_COMPLETE_NO_SCIENTIFIC_VERDICT" if all(checks.values()) else "HISTORICAL_REPRODUCTION_WITH_PRESERVED_NUMERICAL_DISCREPANCY_NO_VERDICT",
 "compiler_sha256":sha(pathlib.Path(__file__)),"checks":checks,"tolerances_frozen":tol,"families":families,
 "grid_files":files,"total_grids":12,"new_campaign_grids":11,"earlier_P4_tgl_n25_reused":True,"total_processed_nodes":sum(d["processed_nodes"] for d in raw.values()),
 "resources":{"all12_wall_sum":sum(d["resources"]["wall"] for d in raw.values()),"all12_cpu_sum":sum(d["resources"]["cpu"] for d in raw.values()),
 "new11_wall_sum":sum(u["resources"]["wall"] for u in state["units"]),"new11_controller_wall_sum":sum(u["controller_wall"] for u in state["units"]),
 "peak_bytes_max":max(d["resources"]["peak_bytes"] for d in raw.values()),"projected_new11_wall":camp["projected_remaining_seconds"],"projected_margin2x":camp["remaining_margin2x_seconds"]},
 "uncertainty":{"n35_minus_n25":"Observed discretization diagnostic of the same truncated grid; not a rigorous error bound.",
 "tails":"NOT_MEASURED. No bounds on omitted prior-domain tails from model-specific fitted +/-6sigma boxes. Neither small25/35 difference nor formal Gaussian6sigma tail probability certifies non-Gaussian likelihood tails.",
 "support":"Same broad normalized priors; likelihood zero outside historical CAMB support. No renormalization to table or fitted box.",
 "SD":"Node-density interpolation at beta_tgl and node CDF are resolution dependent. Formal Savage-Dickey equality also requires common conditional nuisance prior/support; model-specific numerical fit boxes need not be identical. Direct vsSD mismatch retained, no calibration.",
 "laplace":"Historical diagonal-Laplace uses product marginal sigmas, not determinant covariance. Separate approximation, never substituted for grid.",
 "grid_geometry":"Independent P45 centers/sigmas reused without refit. Historical reducedJSON did not retain original evidence-refit centers/sigmas; byte-identical grid geometry not claimed."},
 "likelihood":{"P4_d1b":"Planck compressed + DESI DR2 + scalar GaussianSH0ES.","P5_sombra":"Planck compressed + DESI DR2 + full Pantheon+SH0ES with77Cepheidcalibrators; no extra scalarSH0ES.",
 "covariance":"Full within-block Planck3,DR213,SN1657 matrices; cross-block covariance unavailable => historical factorization INPUT. CC not in these families.",
 "normalization":"Reduced lnZ omits common data Gaussian constants; M is profiled. Relative within-family ratios retain meaning for common nuisance measure/broad compatible Mprior limit. Not a normalized absolute data evidence.",
 "no_joint_F4_F5":"Shared data; no multiplication of these families or cross-dataset absolute lnZ interpretation."},
 "historical_opening_correction":"The ORDEM018 opening combines P5 ladder diagnostics5.26sigma/-0.38sigma with P4 lnB8.02037/2.24596. Keep these as separate historical families, not one result. sqrt(delta chi2) is joint-likelihood statistic and z_beta is a free-beta diagnostic, neither a ladder-free background prediction residual.",
 "control_failure":{"preserved_receipt":"E45A_FALHA_CONTROLE_CAMPANHA.json","new_scientific_processes_before_correction":0,"resume_map_seq":431},
 "scientific_verdict":None,"new_fit":False,"MCMC":False,"F9":False,"accumulated_grid":False}
 jrec=json_new("E45A_RESULTADO_CONSOLIDADO.json",out)
 lines=["# E45A — reprodução histórica relativa P4 / P5 sombra","","[REAL — reprodução numérica local] Concluídas12grades: a primeiraP4/TGLn25 foi reutilizada;11unidades novas, sequenciais, uma thread e limites600s/512MiB. Nenhum fit, MCMC, F9 ou grade acumulada. Os números abaixo reproduzem o contrato histórico; não são veredito científico.","","## Integrais reduzidas","",
 "| Família | Modelo | lnZ n25 | lnZ n35 | Δ35−25 | Δ25−arquivo |","|---|---|---:|---:|---:|---:|"]
 for family,f in families.items():
  for model,m in f["models"].items():
   lines.append(f'| {family} | {model} | {m["grids"]["25"]["lnZ"]:.12f} | {m["grids"]["35"]["lnZ"]:.12f} | {m["n35_minus_n25"]:.9g} | {m["n25_minus_archive"]:.9g} |')
 lines+=["","## Razões na mesma família","","| Família | Razão | lnB n25 | lnB n35 | Δ25−arquivo |","|---|---|---:|---:|---:|"]
 for family,f in families.items():
  for key,v in f["lnB"].items():lines.append(f'| {family} | {key} | {v["n25"]:.12f} | {v["n35"]:.12f} | {v["n25_minus_archive"]:.9g} |')
 lines+=["","## Savage–Dickey e discretização","","| Família | Razão | SD n25 | SD n35 | SD25−grade25 | SD35−grade35 |","|---|---|---:|---:|---:|---:|"]
 for family,f in families.items():
  for key in ("tgl_vs_livre","lcdm_vs_livre"):
   sd=f["savage_dickey"];lines.append(f'| {family} | {key} | {sd["25"]["values"][key]:.12f} | {sd["35"]["values"][key]:.12f} | {sd["25"]["minus_direct_grid_lnB"][key]:.9g} | {sd["35"]["minus_direct_grid_lnB"][key]:.9g} |')
 lines+=["","[REAL] As diferençasSD são preservadas. A interpolação pontual de uma marginal grosseira não tem a mesma precisão da sua integral; os quantis de CDF de nós também dependem da malha. OJSON conserva as densidades e quantis25/35. Igualdade exata Savage–Dickey exige suporte/prior condicional comum: as caixas numéricas centradas em fits de cada modelo são adicionais ao prior amplo.",""]
 for family,f in families.items():
  er=f["max_grid_difference"];lines.append(f'- {family}: maior |ΔlnZ35−25|={er["measured"]:.12g}; arquivo={er["archive"]:.12g}; diferença={er["difference"]:.9g}.')
 lines+=["","[OPEN — caudas não medidas] O desenho histórico integra caixas ±6σ nos três parâmetros de fundo e todo o prior emβ. A comparação25/35 não limita a massa de probabilidade omitida fora dessas caixas. O suporteCAMB menor também foi preservado. Nenhuma ampliação ou correção de cauda foi introduzida.","","## Alcance estatístico","","[INPUT] P4 inclui Planck+DR2+SH0ES gaussiano. P5 sombra inclui Planck+DR2+Pantheon+SH0ES,77calibradores e1580SNnão-calibradoras; não duplica o escalarSH0ES. Matrizes completas dentro dos blocos; covariância cruzada ausente e fatorização histórica explícita. CC está fora de ambas. Não são famílias sem escada e não devem ser multiplicadas como dados independentes.","","[DERIVED] lnZ é reduzido pelas constantes gaussianas omitidas; em P5 M é perfilado. As constantes comuns cancelam nas razões da mesma família sob a mesma medida deM/limite de prior amplo compatível. Não se reivindica evidência absoluta normalizada. O diagnóstico diagonal-Laplace usa produto das variâncias marginais, não determinante da covariância completa; permanece separado noJSON.","","[CORREÇÃO AO LADO — proveniência histórica] A abertura daORDEM018 associa os diagnósticos de escada5,26σ/−0,38σ deP5 aos lnB8,02037 e2,24596 deP4. São famílias distintas: a tabela acima mantém essa identidade. √Δχ² é estatística conjunta, e zβ é diagnóstico do ajusteβlivre; nenhum é resíduo de previsão de fundo sem escada. Esses diagnósticos não foram recalculados aqui.","","[REAL/DECLARADO] Foram reutilizados os centros e sigmasP45 independentes. O arquivo histórico reduzido não armazenou todos os centros/sigmas dos refits internos da evidência; a concordância é numérica no contrato, sem alegar geometria byte a byte idêntica.","","## Custo e rastreio",""]
 res=out["resources"]
 lines +=[f'Wall somado das11novasunidades: {res["new11_wall_sum"]:.3f}s; projeção anterior {res["projected_new11_wall"]:.3f}s, margem2× {res["projected_margin2x"]:.3f}s.',
 f'Das12grades, wall={res["all12_wall_sum"]:.3f}s, CPU={res["all12_cpu_sum"]:.3f}s; pico máximo={res["peak_bytes_max"]/1024**2:.3f}MiB. Tempos somados de processamento não incluem esperas de coordenação.',
 f'Nós processados totais: {out["total_processed_nodes"]}. Checks: '+json.dumps(checks,ensure_ascii=False)+".",
 "","A falha NameError do controladorv1 ocorreu antes de qualquer subprocesso científico. Ficou preservada com backup/recibo; controladorv2 corrigiu apenas pathlib.Path e arquivos de continuação/estado. Pré-checagem pura e autorização posterior antecederam a retomada (mapas430/431). Nenhuma grade científica foi repetida.","",
 "Fontes, hashes de cada grade, entradas, estado de campanha, ambiente e recibos individuais estão no manifesto eJSON consolidados. Kernel, originais e gate preservados."]
 note="\n".join(lines)+"\n"
 for a,b in {"Concluídas12grades":"Concluídas 12 grades","primeiraP4/TGLn25":"primeira P4/TGL n25","11unidades":"11 unidades","600s/512MiB":"600 s/512 MiB","diferençasSD":"diferenças SD","quantis25/35":"quantis 25/35","suporteCAMB":"suporte CAMB","77calibradores":"77 calibradores","1580SNnão-calibradoras":"1580 SN não-calibradoras","escalarSH0ES":"escalar SH0ES","deM/limite":"de M/limite","sigmasP45":"sigmas P45","das11novasunidades":"das 11 novas unidades","Das12grades":"Das 12 grades","controladorv1":"controlador v1","controladorv2":"controlador v2","mapas430/431":"mapas 430/431","daORDEM018":"da ORDEM018","escada5,26σ/−0,38σ deP5":"escada 5,26σ/−0,38σ de P5","lnB8,02037":"lnB 8,02037","deP4":"de P4","ajusteβlivre":"ajuste β livre","CDF de nós":"CDF de nós","noJSON":"no JSON","eJSON":"e JSON"}.items():note=note.replace(a,b)
 mrec=write_new("E45A_NOTA_CONSOLIDADA.md",note.encode())
 ancillary=["E45A_CONTINUACAO_CAMPANHA_V2.json","E45A_ESTADO_CAMPANHA_V2.json","E45A_PRECHECK_V2.json","E45A_campanha_unidade_v2.py","E45A_FALHA_CONTROLE_CAMPANHA.json","E45A_compilar_resultados.py","E45A_RECIBO_P4_TGL_N25.json"]
 manifest={"created_utc":out["created_utc"],"identity":out["identity"],"outputs":[jrec,mrec],"grids":files,"inputs":camp["source_pins"],
 "control":[dict(name=n,bytes=(ROOT/n).stat().st_size,sha256=sha(ROOT/n)) for n in ancillary],"status":out["status"]}
 mf=json_new("E45A_MANIFESTO_CONSOLIDADO.json",manifest)
 print(json.dumps({"status":out["status"],"checks":checks,"resources":out["resources"],"lnB":{k:v["lnB"] for k,v in families.items()},"outputs":[jrec,mrec,mf]},ensure_ascii=False))
if __name__=="__main__":main()
