# -*- coding: utf-8 -*-
"""Generate additive and unfrozen F3.1 V2 R3 from the pinned R2 and V1."""
from __future__ import annotations
import copy, hashlib, importlib.util, json, math, os, tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
R2_SCRIPT=HERE/"generate_fase9_v2_draft_f31_20261008_R2.py"
R2_JSON=HERE/"PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V2_RASCUNHO_F31_20261008_R2.json"
V1=Path(r"C:\IALD\Bancada_Um\investigacao\preregistro_fase9_hubble\PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.json")
BINDING=HERE.parent/"F3.2"/"VINCULO_DOCUMENTAL_V1X_R2_20261008.json"
CCHP=Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\h0dn_documentary_review\jagb_extension\residual_systematics\sources\cchp_overview.txt")
STEM="PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V2_RASCUNHO_F31_20261008_R3"
RESTORED=("base","contaminacao_declarada","decisoes_padrao_da_gerencia",
 "especificacao_do_runner","estado","estatisticas","fontes_lidas_sha256",
 "funcao_de_veredito","hipoteses","nao_decide","novidade_de_uso",
 "sistematicas","supersede","token_base_provisorio","token_estado")
def h(b): return hashlib.sha256(b).hexdigest()
def pretty(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
def read(p,expected=None):
 b=p.read_bytes(); actual=h(b)
 if expected and actual!=expected: raise ValueError(f"pin mismatch {p}: {actual}")
 return b,actual
def r2_module():
 info=importlib.util.spec_from_file_location("f31_r2",R2_SCRIPT)
 module=importlib.util.module_from_spec(info); info.loader.exec_module(module)
 return module
VERDICT='''def veredito_fase9_v2_r3_proposta(r):
    """Draft only. D-J names final token; use minimum and maximum covariance endpoints."""
    import math
    def f(x): return ("M" if x<0 else "P")+("%.1f"%abs(x)).replace(".","P")
    base="TGL_FASE9_RAZAO_DE_HUBBLE_V2_R3_DRAFT__"
    suf=("__D1B__FUNDO_%s__NOT_BLIND_TO_DATA_STATED"
         "__NOT_A_CONFIRMATION__GATE_UNTOUCHED")%r["fundo"]
    if (r["n_alvos_declarados"]>0 or not r["required_sources_admitted"]
        or r["beta_livre_no_limite"]
        or any(e["chi2_por_gl"]>2 or e["p"]<0.01
               for e in r["dispersao_endpoints"].values())):
        return base+"INCONCLUSIVE_SYSTEMATICS"+suf
    low,high=r["minimum"],r["maximum"]
    zd=abs(low["z_delta"])
    if zd>=5 or any(s<=1 and abs(z)>=5 for s,z in low["sigma_z_por_alvo"]):
        return base+"FALSIFIED_AT_5SIGMA"+suf
    if zd>=3: return base+"TENSION_3_TO_5_SIGMA"+suf
    if high["poder_previo"]<5:
        return base+"NOT_FALSIFIED_UNDERPOWERED__POWER_%s_OF_5_SIGMA"%f(high["poder_previo"])+suf
    if high["z_disc"]>=5 and zd<3 and high["lnB_lcdm"]>=5 and high["lnB_livre"]>=-1:
        t=(base+"NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_%dSIGMA"
           "__ZERO_FREE_PARAMETERS"%int(math.floor(high["z_disc"])))
        t+="__USE_NOVEL" if r["use_novel_parametros"] else "__USE_NOVELTY_PENDING"
        t+="__VS_LADDER_SYSTEMATIC_LNB_%s__VS_FREE_BACKGROUND_LNB_%s"%(f(high["lnB_shift"]),f(high["lnB_fundo_livre"]))
        if high["lnB_shift"]<0 and high["poder_nao_cefeida"]>=5:
            t+="__NOT_DISCRIMINATED_FROM_LADDER_SYSTEMATIC"
        if abs(high["lnB_fundo_livre"])<1:
            t+="__NOT_DISCRIMINATED_FROM_FREE_BACKGROUND"
        return t+suf
    t=base+"NOT_FALSIFIED_POWERED__"+("DEVIATION_CONSISTENT_WITHIN_1SIGMA" if zd<1 else "DEVIATION_1_TO_3_SIGMA")
    if high["z_disc"]<5: t+="__NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY"
    return t+suf
'''
def build():
 r2=r2_module(); doc2,_=r2.build()
 b2,s2=read(R2_JSON)
 if json.loads(b2.decode())!=doc2: raise ValueError("registered R2 mismatch")
 bv1,sv1=read(V1,r2.PINS[V1]); old=json.loads(bv1.decode())["spec"]
 bb,sb=read(BINDING); binding=json.loads(bb.decode())
 bc,sc=read(CCHP)
 if b"TRGB (JWST)" not in bc or b"TRGB (HST + JWST)" not in bc:
    raise ValueError("Table 6 row distinction absent")
 spec=copy.deepcopy(doc2["spec"]); spec["id"]="PREREG_FASE9_RAZAO_DE_HUBBLE_V2_DRAFT_F31_20261008_R3"
 spec["generated_from"].update({"R2_registered":{"path":str(R2_JSON),"sha256":s2},
  "V1x_binding_R2":{"path":str(BINDING),"sha256":sb},
  "CCHP_Table6":{"path":str(CCHP),"sha256":sc}})
 records={x["reader_id"]:x for x in binding["readers"]}
 if set(records)!=set(spec["leitores"]): raise ValueError("inventory mismatch")
 missing=[]
 for name,item in spec["leitores"].items():
    src=records[name]; status=src["documentary_status"]
    item["documentary_gate_status"]=status; item["source_admission"]="PENDING_D_H"
    if status=="REAL_DOCUMENTARY_HASH_ONLY":
        item["estatuto_hoje"]="[REAL documental por hash no vínculo; admissão D-H PENDENTE]"
        item["documentary_source"]={"path":src["source"]["path"],"sha256":src["source"]["sha256"]}
    else:
        missing.append(name)
        item["estatuto_hoje"]="[DECLARADO: fonte sem bytes pinados; admissão D-H PENDENTE]"
 missing.sort()
 if missing!=["L1b_sh0es_r25","L6_sirenes"]: raise ValueError(f"declared inventory changed: {missing}")
 c=spec["covariancia"]
 c["components"]["CCHP_Table6_note_a"]={"source_sha256":sc,"source_path":str(CCHP),
  "marked_row":"TRGB (JWST) 1.9%","decisory_row":"TRGB (HST+JWST) 1.9%; note a absent",
  "HST_anchor_count":4,"split_1p33_into_N_T":"DERIVED_INFERENTIAL_CEILING_NOT_PUBLISHED"}
 c["components"]["SBF_0p031"]={"value":0.031,"meaning":"Operational 3.1%; implied H0=2.3/0.031=74.193548",
  "status":"INPUT_DECLARADO_NOT_VERIFIED_IN_SBF_SECTION_III_3","R2_amplitudes_retained":True}
 c["shared_lambda_N_rule"]="One common lambda_N for L1N-L2N, L1N-L3N and L2N-L3N, also six-maser diagnostic."
 c["R2_independent_box_c1"]={"shared_sigma_max":0.94929,"independent_four_terms_sigma_max":0.94946,
  "shared_power_BG1":5.7218,"independent_power_BG1":5.7208,"status":"DERIVED_C1_FOR_R2_NOT_R3"}
 bg1=float(spec["fundos"]["BG1"]["H0"]); sigmas={k:float(v["sigma"]) for k,v in spec["leitores"].items()}
 amps=c["amplitudes_km_s_Mpc"]; mag=math.log(10)/5*math.hypot(0.024,0.022)
 for key,reader in (("L1N","L1_sh0es_r22"),("L1bN","L1b_sh0es_r25"),("L4N","L4_masers_6")):
    amps[key]=min(sigmas[reader],bg1*mag)
 c["NGC4258_conversion_scale"]={"value":bg1,"source":"BG1 bare background",
  "replaces":"K*BG1, which was the TGL prediction","status":"INPUT_NOT_PREDICTION_NOT_LOCAL_CENTER"}
 c["matrix_rule"]=("One shared lambda_N: C12=L1N*L2N, C13=L1N*L3N, C23_N=L2N*L3N; "
  "lambda_T multiplies C23_T=L2T*L3T. Five masers have zero NGC4258 coupling. "
  "Six-maser diagnostic adds lambda_N*LiN*L4N for i=1..3. "
  "R_r25 substitutes L1bN for L1N and adds L1bN-L2N and L1bN-L3N NGC4258 cross terms; "
  "L1bN capped at sigma=0.93. L6 sirens independent in this sensitivity box; unknown cross terms OPEN.")
 c["R_r25_L1b_NGC4258_coupling"]={"amplitude_key":"L1bN","links":["L2N","L3N"],"sigma_cap":0.93}
 c["S_com_sirenes"]={"L6_cross_terms":0.0,"status":"BOX_ASSUMPTION_OTHER_CROSS_TERMS_OPEN"}
 K=float(spec["lei"]["K_recomputed"])
 def power(s,bg):
    x=spec["fundos"][bg]; return (K-1)*float(x["H0"])/math.hypot(s,K*float(x["sigma"]))
 ids5=r2.IDS5
 variants={"five_masers_decision":(ids5,False),
   "six_masers_diagnostic":(tuple("L4_masers_6" if i=="L4_masers_5" else i for i in ids5),True),
   "without_cepheids_diagnostic":(tuple(i for i in ids5 if i!="L1_sh0es_r22"),False)}
 for name,(ids,six) in variants.items():
    result=r2.endpoints(ids,sigmas,amps,six)
    for end in ("minimum","maximum"):
        result[end]["power_only_sigma"]={bg:power(result[end]["sigma_comb"],bg) for bg in ("BG1","BG2","BG3")}
    c[name]=result
 for attr,key in (("primary_five","five_masers_decision"),("six_diagnostic","six_masers_diagnostic"),
                  ("no_cepheids_diagnostic","without_cepheids_diagnostic")):
    spec["poder_previo"][attr]={e:c[key][e]["power_only_sigma"] for e in ("minimum","maximum")}
 five39=r2.endpoints(ids5,dict(sigmas,L5_tdcosmo=3.9),amps,False)
 p39=power(five39["maximum"]["sigma_comb"],"BG1")
 spec["D5_sensitivities_from_c1_audit"].update({"five_sigma3p9_c1_R2":5.695,"five_sigma3p9_R3":p39,
   "note":"5.695 is five decisory, 5.439 six diagnostic in R2 audit; R3 is recalculated."})
 inv={"universe":"whole V1.x inventory, not active family",
  "predicate":"NOT gate_verified AND NOT operator_admitted_in_pinned_D_H_register",
  "current_ids":missing,"current_count":2,"same_in":["preflight","staged_runner"],
  "primary_result":"INCONCLUSIVE_SYSTEMATICS until L1b/L6 gate verification/admission; D-H separately blocks opening"}
 v=spec["funcao_de_veredito_proposta"]
 v["n_alvos_declarados"]=inv["predicate"]+" over "+inv["universe"]
 v["n_alvos_declarados_rule"]=inv
 v["single_reader_trigger"]["by_family"]={"P_primaria":{"active":False,"min_sigma":1.04},
   "R_r25":{"active":True,"reader_id":"L1b_sh0es_r25","sigma":0.93,"diagnostic_only":True}}
 v["thresholds"]={"dispersion_chi2_per_dof_gt":2.0,"dispersion_p_lt":0.01,
  "beta_free_prior_edge":"INCONCLUSIVE_SYSTEMATICS","single_reader_sigma_le":1.0,
  "falsification_abs_z_ge":5.0,"tension_abs_z_ge":3.0,"power_ge":5.0,
  "discrimination_z_ge":5.0,"lnB_lcdm_ge":5.0,"lnB_beta_free_ge":-1.0,
  "free_background_abs_lnB_lt":1.0}
 v["order"]=["INCONCLUSIVE if whole-inventory count>0, D-H missing, beta-free at prior edge, or dispersion fails either endpoint",
  "FALSIFIED if abs(z_delta_min)>=5 or active reader sigma<=1 and abs(z_i_min)>=5",
  "TENSION if abs(z_delta_min)>=3","UNDERPOWERED if power_max<5",
  "DISCRIMINATES if z_disc_max>=5, abs(z_delta_min)<3, lnB_lcdm>=5 and lnB_beta_free>=-1; both diagnostic suffixes",
  "otherwise NOT_FALSIFIED_POWERED"]
 spec["runner_contract"]["n_alvos_declarados_rule"]=inv
 for key in RESTORED: spec[key]=copy.deepcopy(old[key])
 spec["base"]={"V1_sha256":sv1,"R2_sha256":s2,"state":"RASCUNHO_NAO_CONGELADO","gate":"UNTOUCHED"}
 spec["estado"]="RASCUNHO_NAO_CONGELADO; F3.4/NAT22 before freeze; D-H before opening"
 spec["hipoteses"]["H_TGL"]="bare BG1 plus fixed K=E(z*)^(2beta/3), beta=ALPHA_FINE_CODATA_2018*sqrt(e) at runtime"
 spec["hipoteses"]["H_shift_cefeidas"]="Only L1 or replacement L1b receives shift s~U[-0.15,0.15]; CCHP TRGB-only does not"
 spec["hipoteses"]["H_beta_livre"]+="; fitted beta at prior edge => INCONCLUSIVE_SYSTEMATICS"
 spec["decisoes_padrao_da_gerencia"]["D-H"]="Six sources pinned documentally, L1b/L6 declared; all D-H admissions pending"
 spec["decisoes_padrao_da_gerencia"]["D-J"]="Final token name operator decision, pending"
 spec["decisoes_padrao_da_gerencia"]["NAT22_X13"]="Observed executor deviations stated, operator decision pending"
 spec["estatisticas"]={"background":"marginalized by observed executor; NAT22 pending",
  "z_delta":"profile -2lnL including log determinant at minimum-sigma endpoint",
  "z_disc":"quadratic form at maximum-sigma endpoint",
  "lnB":"n>=100 quadrature, check n=100/200; compare LCDM, beta-free, shift, free background",
  "dispersao":"chi2/(n-1)>2 OR p<0.01 at EITHER endpoint gives INCONCLUSIVE",
  "z_i":"active family; sigma<=1 and |z_i|>=5; R25 L1b has sigma 0.93",
  "sigma_beta":"mean asymmetric sides, local Gaussian"}
 spec["sistematicas"]["covariancia"]="Cauchy-Schwarz sensitivity box, common lambda_N and lambda_T; SN/Pantheon cross terms OPEN"
 spec["sistematicas"]["fundo"]="BG1 preselected, BG2/BG3 diagnostic; executor marginalizes background"
 spec["sistematicas"]["free_background"]="NOT_DISCRIMINATED_FROM_FREE_BACKGROUND if abs(lnB_TGL_vs_free)<1"
 spec["sistematicas"]["ladder"]="ladder suffix requires lnB_shift<0 AND no-Cepheid power>=5"
 spec["novidade_de_uso"]["etiqueta"]="retrodição sem ajuste; no theory parameter fit to local H0"
 spec["contaminacao_declarada"]["R3"]="non-blind; no target opened or real composite run"
 spec["nao_decide"].extend(["D-H admission","F3.4 governing specification","NAT22/X13"])
 spec["funcao_de_veredito"]={"nome":"veredito_fase9_v2_r3_proposta","fonte":VERDICT,
  "sha256":h(VERDICT.encode()),"estatuto":"PROPOSTA_SINTETICA_NAO_CONGELADA",
  "thresholds":v["thresholds"],"n_alvos_declarados_rule":inv,"final_token":"D_J_PENDING"}
 spec["especificacao_do_runner"]=["R0 pin V2 R3 spec/function/runner before real composite, no freeze now",
  "R1 inventory-wide n_alvos with the same predicate in preflight and staged",
  "R2 recompute BG1 and beta/K at runtime, fail on mismatch",
  "R3 power from sigmas at both covariance endpoints before local centers",
  "R4 real opening only after F3.4, NAT22/X13, D-H, c1 audit and operator act",
  "R5 five hypotheses, GLS/dispersion both endpoints, four lnB incl free background, pinned verdict",
  "R6 R_r25 and S_com_sirenes diagnostics, their own covariance; never sum replacements",
  "R7 subsequent changes new version beside, no overwrite"]
 spec["fontes_lidas_sha256"]={"V1":sv1,"R2":s2,"V1x_binding":sb,"CCHP_Table6":sc,
  "status":"DOCUMENTARY_ONLY_D_H_PENDING_NO_TARGET_OPENED"}
 spec["supersede"]={"draft_R2_only":str(R2_JSON),"R2_sha256":s2,"V1_remains_frozen":True}
 spec["token_base_provisorio"]="TGL_FASE9_RAZAO_DE_HUBBLE_V2_R3_DRAFT__LAW_D1B__BG1"
 spec["token_estado"]="RASCUNHO_NAO_CONGELADO__F3_4_NAT22_D_J_PENDING__GATE_UNTOUCHED"
 sh=h(canon(spec)); doc={"id":spec["id"],"state":spec["state"],"spec_sha256":sh,"spec":spec}
 lines=["# Fase 9 V2 R3 autossuficiente — rascunho não congelado","",
  "Spec sha256: "+sh+". V1 "+sv1+"; R2 "+s2+"; vínculo "+sb+".","",
  "[REAL documental] Quinze seções V1 recompostas com texto V2. Nenhum alvo, composto real, congelamento ou gate tocado.","",
  "## Correções quantitativas","",
  "- [DERIVED inferência] Nota a CCHP Table 6 marca TRGB (JWST) 1,9%, não HST+JWST; N/T do 1,33 é teto inferido.",
  "- [INPUT DECLARADO] SBF 0,031 é fator operacional 3,1%, H0 implícito 74,19; não verificado como constante publicada.",
  f"- [DERIVED] L1N/L1bN/L4N usam BG1 nu {bg1:.3f}, não K*BG1; L1bN={amps['L1bN']:.6f}, cap 0,93.",
  "- [DERIVED c1 R2] λ_N comum deu sigma máximo 0,94929; quatro termos independentes 0,94946. R3 recompõe pontas.",
  f"- [DERIVED c1] TDCOSMO sigma 3,9: cinco 5,695, seis 5,439 (R2); cinco R3 {p39:.6f}.",
  "- [REAL documental] Seis leitores pinados; L1b/L6 declarados; D-H pendente para todos.",
  "- [INPUT/DERIVED] n_alvos_declarados inventário inteiro=2, primário INCONCLUSIVE; preflight=staged.",
  "- [DERIVED] R25 L1b sigma 0,93 aciona gatilho e liga L1bN a L2N/L3N; réplica diagnóstica.",""]
 for key in RESTORED:
    lines+=["## "+key,"",pretty(spec[key]).rstrip(),""]
 lines+=["## Função completa proposta","",VERDICT.rstrip(),"",
  "F3.4 e NAT22/X13 antecedem congelamento; D-H antecede abertura; D-J nomeia token. NOT_FALSIFIED não credita.",""]
 outputs={STEM+".json":pretty(doc).encode(),STEM+".md":"\n".join(lines).encode()}
 manifest={"state":"RASCUNHO_NAO_CONGELADO","spec_sha256":sh,"restored_sections":list(RESTORED),
  "verdict_sha256":spec["funcao_de_veredito"]["sha256"],
  "outputs":{k:{"sha256":h(b),"bytes":len(b)} for k,b in outputs.items()},
  "frozen":False,"real_data_opened":False,"gate_changed":False}
 outputs["GERACAO_V2_RASCUNHO_F31_20261008_R3.json"]=pretty(manifest).encode()
 return doc,outputs
def create(path,data):
 if path.exists(): raise FileExistsError(path)
 fd,tmp=tempfile.mkstemp(prefix=path.name+".",suffix=".tmp",dir=path.parent)
 try:
    with os.fdopen(fd,"wb") as f: f.write(data); f.flush(); os.fsync(f.fileno())
    if Path(tmp).stat().st_size!=len(data): raise IOError("temporary size mismatch")
    os.replace(tmp,path)
    if h(path.read_bytes())!=h(data): raise IOError("hash mismatch")
 finally:
    if os.path.exists(tmp): os.unlink(tmp)
def main():
 doc,outputs=build()
 if "--check-only" not in os.sys.argv[1:]:
    for name in outputs:
        if (HERE/name).exists(): raise FileExistsError(HERE/name)
    for name,data in outputs.items(): create(HERE/name,data)
 print(pretty({"mode":"check_only" if "--check-only" in os.sys.argv[1:] else "written",
  "spec_sha256":doc["spec_sha256"],"outputs":{k:h(v) for k,v in outputs.items()},
  "five_sigma_min":doc["spec"]["covariancia"]["five_masers_decision"]["minimum"]["sigma_comb"],
  "five_sigma_max":doc["spec"]["covariancia"]["five_masers_decision"]["maximum"]["sigma_comb"]}))
if __name__=="__main__": main()