# -*- coding: utf-8 -*-
"""Synthetic branch tests for the unfrozen F3.1 R3 verdict proposal."""
import copy, hashlib, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
SPEC=HERE/"PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V2_RASCUNHO_F31_20261008_R3.json"
data=SPEC.read_bytes()
doc=json.loads(data.decode("utf-8"))
source=doc["spec"]["funcao_de_veredito"]["fonte"]
assert hashlib.sha256(source.encode()).hexdigest()==doc["spec"]["funcao_de_veredito"]["sha256"]
namespace={}
exec(compile(source,str(SPEC),"exec"),namespace)
decide=namespace["veredito_fase9_v2_r3_proposta"]

def baseline():
    return {"fundo":"BG1","n_alvos_declarados":0,"required_sources_admitted":True,
      "beta_livre_no_limite":False,"use_novel_parametros":True,
      "dispersao_endpoints":{"minimum":{"chi2_por_gl":1.0,"p":0.5},
                             "maximum":{"chi2_por_gl":1.0,"p":0.5}},
      "minimum":{"z_delta":0.5,"sigma_z_por_alvo":[(1.04,0.0)]},
      "maximum":{"poder_previo":6.0,"z_disc":6.2,"lnB_lcdm":6.0,"lnB_livre":0.0,
                 "lnB_shift":2.0,"lnB_fundo_livre":0.5,"poder_nao_cefeida":4.0}}

cases=[]
def run(name,modify,expected):
    row=baseline()
    modify(row)
    result=decide(row)
    if expected not in result: raise AssertionError(f"{name}: {result} lacks {expected}")
    cases.append({"name":name,"expected":expected,"result":result})
run("inventory_declared",lambda r:r.update(n_alvos_declarados=2),"INCONCLUSIVE_SYSTEMATICS")
run("D_H_guard",lambda r:r.update(required_sources_admitted=False),"INCONCLUSIVE_SYSTEMATICS")
run("beta_prior_boundary",lambda r:r.update(beta_livre_no_limite=True),"INCONCLUSIVE_SYSTEMATICS")
run("dispersion_maximum",lambda r:r["dispersao_endpoints"]["maximum"].update(chi2_por_gl=2.1),"INCONCLUSIVE_SYSTEMATICS")
run("dispersion_p_minimum",lambda r:r["dispersao_endpoints"]["minimum"].update(p=0.009),"INCONCLUSIVE_SYSTEMATICS")
run("falsification_minimum",lambda r:r["minimum"].update(z_delta=5.0),"FALSIFIED_AT_5SIGMA")
run("single_reader_R25",lambda r:r["minimum"].update(sigma_z_por_alvo=[(0.93,5.0)]),"FALSIFIED_AT_5SIGMA")
run("tension_minimum",lambda r:r["minimum"].update(z_delta=3.5),"TENSION_3_TO_5_SIGMA")
run("underpowered_maximum",lambda r:r["maximum"].update(poder_previo=4.0),"NOT_FALSIFIED_UNDERPOWERED")
run("free_background_suffix",lambda r:None,"NOT_DISCRIMINATED_FROM_FREE_BACKGROUND")
run("no_discrimination",lambda r:r["maximum"].update(z_disc=4.0),"NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY")
print(json.dumps({"synthetic_only":True,"real_targets_opened":False,"spec_sha256":hashlib.sha256(data).hexdigest(),
                  "passed":len(cases),"cases":cases},ensure_ascii=False,indent=2))