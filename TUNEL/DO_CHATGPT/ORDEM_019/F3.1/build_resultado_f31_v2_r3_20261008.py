# -*- coding: utf-8 -*-
"""Pin additive F3.1 V2 R3 diff and validation receipt."""
from __future__ import annotations
import difflib, hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
OLD=HERE/"PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V2_RASCUNHO_F31_20261008_R2.json"
NEW=HERE/"PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V2_RASCUNHO_F31_20261008_R3.json"
STEM="PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V2_RASCUNHO_F31_20261008_R3"
DIFF=HERE/"DIFF_V2_R2_R3_F31_20261008.patch"
TEST=HERE/"TESTE_F31_R3_SINTETICO_20261008.json"
RESULT=HERE/"RESULTADO_F31_V2_R3_20261008.json"
GEN=HERE/"generate_fase9_v2_draft_f31_20261008_R3.py"
TEST_SCRIPT=HERE/"test_f31_v2_r3_verdict.py"
MANIFEST=HERE/"GERACAO_V2_RASCUNHO_F31_20261008_R3.json"
MD=HERE/(STEM+".md")
def h(data): return hashlib.sha256(data).hexdigest()
def pretty(x): return (json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
def new_file(path,data):
    if path.exists(): raise FileExistsError(path)
    fd,temp=tempfile.mkstemp(prefix=path.name+".",suffix=".tmp",dir=path.parent)
    try:
        with os.fdopen(fd,"wb") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        if Path(temp).stat().st_size!=len(data): raise IOError("temp size")
        os.replace(temp,path)
        if h(path.read_bytes())!=h(data): raise IOError("hash mismatch")
    finally:
        if os.path.exists(temp): os.unlink(temp)
def main():
    for path in (DIFF,TEST,RESULT):
        if path.exists(): raise FileExistsError(path)
    old_bytes=OLD.read_bytes(); new_bytes=NEW.read_bytes()
    old=json.loads(old_bytes.decode("utf-8"))["spec"]
    new=json.loads(new_bytes.decode("utf-8"))["spec"]
    diff="".join(difflib.unified_diff(
        (json.dumps(old,ensure_ascii=False,sort_keys=True,indent=2)+"\n").splitlines(True),
        (json.dumps(new,ensure_ascii=False,sort_keys=True,indent=2)+"\n").splitlines(True),
        fromfile=f"R2_spec_sha256_{h(old_bytes)}",tofile=f"R3_spec_sha256_{h(new_bytes)}"))
    p=subprocess.run([sys.executable,"-B","-X","utf8",str(TEST_SCRIPT)],
                     cwd=HERE,capture_output=True,text=True,encoding="utf-8",check=False)
    if p.returncode!=0: raise RuntimeError(f"synthetic test failed: {p.stderr}")
    test=json.loads(p.stdout)
    if test["passed"]!=11 or test["real_targets_opened"]: raise ValueError("synthetic test invariant")
    restored=("base","contaminacao_declarada","decisoes_padrao_da_gerencia",
        "especificacao_do_runner","estado","estatisticas","fontes_lidas_sha256",
        "funcao_de_veredito","hipoteses","nao_decide","novidade_de_uso",
        "sistematicas","supersede","token_base_provisorio","token_estado")
    if len(restored)!=15 or not set(restored)<=set(new): raise ValueError("V1 sections missing")
    if new["funcao_de_veredito"]["sha256"]!=h(new["funcao_de_veredito"]["fonte"].encode()):
        raise ValueError("verdict source hash mismatch")
    if new["runner_contract"]["n_alvos_declarados_rule"]["current_count"]!=2:
        raise ValueError("inventory count mismatch")
    if abs(new["D5_sensitivities_from_c1_audit"]["five_sigma3p9_R3"]-5.695)>0.001:
        raise ValueError("five-reader sigma 3.9 sensitivity mismatch")
    new_file(DIFF,diff.encode("utf-8"))
    new_file(TEST,pretty(test))
    items=[GEN,NEW,MD,MANIFEST,DIFF,TEST_SCRIPT,TEST]
    receipt={"unit":"F3.1","stage":"V2_R3_DRAFT_UNFROZEN","state":"ENTREGUE_PARA_REAUDITORIA",
       "input_R2":{"path":str(OLD),"sha256":h(old_bytes)},
       "artifacts":[{"path":str(x),"sha256":h(x.read_bytes()),"bytes":x.stat().st_size} for x in items],
       "checks":{"V1_sections_restored":list(restored),"synthetic_branches_passed":11,
          "five_sigma_min":new["covariancia"]["five_masers_decision"]["minimum"]["sigma_comb"],
          "five_sigma_max":new["covariancia"]["five_masers_decision"]["maximum"]["sigma_comb"],
          "five_TDCOSMO_sigma_3p9_BG1":new["D5_sensitivities_from_c1_audit"]["five_sigma3p9_R3"],
          "inventory_declared":new["runner_contract"]["n_alvos_declarados_rule"]["current_ids"],
          "diff_R2_R3_lines":len(diff.splitlines())},
       "real_data_opened":False,"frozen":False,"gate_changed":False}
    new_file(RESULT,pretty(receipt))
    print(json.dumps({"result_path":str(RESULT),"result_sha256":h(RESULT.read_bytes()),
       "diff_sha256":h(DIFF.read_bytes()),"test_sha256":h(TEST.read_bytes()),
       "synthetic_branches_passed":11},ensure_ascii=False,indent=2))
if __name__=="__main__": main()