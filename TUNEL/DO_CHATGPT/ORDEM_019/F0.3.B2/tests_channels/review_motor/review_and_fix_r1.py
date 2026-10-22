"""Capture review findings and apply parent-authorized candidate-only fixes."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import importlib.util
import json
import subprocess
import sys
import time
import ast
from unittest.mock import Mock
import numpy as np
import torch

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
UNIT=HERE.parents[1]
STAGE=UNIT/"candidate"
NAMES=("motor.py","evidencia.py","regua.py","camb_tabela.py","pantheon_cov.py","fontes.py","amostrador.py")
if (HERE/"REVIEW_AND_FIX_R1.json").exists():
    raise FileExistsError("review evidence already exists")
def sha(raw):return hashlib.sha256(raw).hexdigest()
def new(path,raw):
    with path.open("xb") as stream:stream.write(raw)
    if path.read_bytes()!=raw:raise OSError("written bytes differ")
    return {"path":str(path),"sha256":sha(raw),"bytes":len(raw)}
before={name:(STAGE/"bancada"/name).read_bytes() for name in NAMES}
before_pins={name:{"sha256":sha(raw),"bytes":len(raw)} for name,raw in before.items()}

# Reproduce metadata/convention defects using the existing synthetic fixture.
spec=importlib.util.spec_from_file_location("motor_review_before",UNIT/"tests_motor/test_motor_synthetic.py")
fixture=importlib.util.module_from_spec(spec);sys.modules[spec.name]=fixture;spec.loader.exec_module(fixture)
m=fixture.DummyMotor();m.n_dados=lambda selected:6
design=np.array([[1,0,0],[0,1,0],[0,0,1],[-1,0,0],[0,-1,0],[0,0,-1]],float)
def residual(th,selected,options):
    y=(np.asarray(th)[:,:3]-np.array([67.5,.02237,.12]))/np.array([1.,.0005,.005])
    return torch.tensor(y@design.T,dtype=torch.float64),{}
m.residuos=residual
e=fixture.evidencia.Evidencia(m,Mock(),canonical_guard=fixture.receipt)
old_result=e._ajuste(["pantheon"],0.,False)
old_options=fixture.motor.opcoes_de(None)
old_label=fixture.motor.rotulo_opcoes({"modo":"selado","beta_no_fundo":"nao","mapa_R":"eff"})
pre_probes={"profiled_M":{"n_observations":6,"n_free_parameters":3,"profiled_nuisance_count":1,
                          "reported_gl":old_result["gl"],"correct_gl":2,"residuals":"SYNTHETIC_CENTERED_DESIGN"},
            "default_local_combination":{"selected":fixture.motor.conjuntos_validos(["cc_moresco"]),"options":old_options},
            "mixed_label":old_label}

motor=before["motor.py"].decode("utf-8")
start=motor.index("def rotulo_opcoes(o):")
end=motor.index("\n\nCONJUNTOS =",start)
motor=motor[:start]+'''def rotulo_opcoes(o):
    """Name a preset only when every option matches it; otherwise show the mix."""
    o = opcoes_de(o)
    if o == OPCOES_ARTIGO:
        modo = "artigo (fundo ΛCDM; β só na lei)"
    elif o == OPCOES_TGL:
        modo = "tgl (corrigido + mapa de R efetivo, ratificado 30/09)"
    elif o == OPCOES_CORRIGIDO:
        modo = "corrigido"
    elif o == OPCOES_SELADO:
        modo = "selado"
    else:
        modo = "misto (não equivale a preset)"
    return modo + " · " + "; ".join(k + "=" + str(v) for k,v in sorted(o.items()))
''' + motor[end:]
at=motor.index("\n\nclass Motor:")
helper='''

def validar_modelo_para_conjuntos(conjuntos, opcoes=None):
    """Validate interacting model choices only when their consumer is selected.

    TGL/eff with Planck+DESI remains the default. Accumulated/local transport
    and a beta-modified background cannot be charged together in one reader.
    The plain Pantheon implementation does not consume lei_sn.
    """
    cj = conjuntos_validos(conjuntos)
    o = opcoes_de(opcoes)
    if "pantheon" in cj and o["lei_sn"] != "nenhuma":
        raise ValueError("lei_sn não implementada no Pantheon só-cosmologia; opção sem consumidor")
    conflicts = []
    if o["beta_no_fundo"] == "sim":
        if "cc_moresco" in cj and o["lei_cc"] == "acumulada":
            conflicts.append("cc_moresco/lei_cc=acumulada")
        if "sh0es_local" in cj:
            conflicts.append("sh0es_local/transporte")
        if "pantheon_sh0es" in cj and o["lei_sn"] != "nenhuma":
            conflicts.append("pantheon_sh0es/lei_sn=" + o["lei_sn"])
    if conflicts:
        raise ValueError("dupla contagem de β: fundo modificado e transporte no mesmo leitor: " + ", ".join(conflicts))
    return o
'''
motor=motor[:at]+helper+motor[at:]
needle='        conjuntos = conjuntos_validos(conjuntos)\n        o = opcoes_de(opcoes)\n'
if motor.count(needle)!=2:raise ValueError("motor validation patch count differs")
motor=motor.replace(needle,'        conjuntos = conjuntos_validos(conjuntos)\n        o = validar_modelo_para_conjuntos(conjuntos, opcoes)\n')

evidence=before["evidencia.py"].decode("utf-8")
evidence=evidence.replace('rotulo_opcoes, conjuntos_validos','rotulo_opcoes, conjuntos_validos, validar_modelo_para_conjuntos',1)
needle='        cj = _conj(conjuntos)\n        o = opcoes_de(opcoes)\n'
if evidence.count(needle)!=4:raise ValueError("facade validation patch count differs")
evidence=evidence.replace(needle,'        cj = _conj(conjuntos)\n        o = validar_modelo_para_conjuntos(cj, opcoes)\n')
needle='        from scipy.optimize import least_squares\n        o = opcoes_de(opcoes)'
if evidence.count(needle)!=1:raise ValueError("fit validation patch count differs")
evidence=evidence.replace(needle,'        from scipy.optimize import least_squares\n        cj = _conj(cj)\n        o = validar_modelo_para_conjuntos(cj, opcoes)')
needle='        return dict(theta=dict(zip(NOMES_THETA, th.tolist())), chi2=chi2, livres=livres, sigma_JtJ=sig, sucesso=bool(res.success),'
if evidence.count(needle)!=1:raise ValueError("dof return patch count differs")
evidence=evidence.replace(needle,'        profiled = ["M_supernova"] if set(cj) & {"pantheon", "pantheon_sh0es"} else []\n'+needle)
evidence=evidence.replace('gl=self.m.n_dados(cj) - len(livres), opcoes=o)',
    'gl=self.m.n_dados(cj) - len(livres) - len(profiled),\n                    n_parametros_perfilados=len(profiled), parametros_perfilados=profiled, opcoes=o)')

sources=before["fontes.py"].decode("utf-8")
needle='                correlacoes=usadas, nota="a diagonal é a do pipeline selado; as 5 correlações DM–DH entram; nada mais")'
replacement='''                correlacoes=usadas, estatuto_origem="DECLARADO", fonte_primaria_sha256=None,
                admissao_primaria_verificada=False,
                nota="a diagonal é do pipeline pinado; as 5 correlações são transcrição histórica em código. Custódia do código não substitui pino/admissão da fonte primária")'''
if sources.count(needle)!=1:raise ValueError("DR1 provenance patch count differs")
sources=sources.replace(needle,replacement)
changes={"motor.py":motor,"evidencia.py":evidence,"fontes.py":sources}
for name,source in changes.items():ast.parse(source,filename=name)
for name,source in changes.items():
    path=STAGE/"bancada"/name
    if path.read_bytes()!=before[name]:raise ValueError("candidate changed during review: "+name)
    new(HERE/(name+".before_r1"),before[name])
    temp=path.with_name(path.name+".review_r1.tmp")
    new(temp,source.encode("utf-8"));temp.replace(path)

runs=[]
for filename,test in (("INDEPENDENT_MOTOR_HARNESS_R1.log",UNIT/"tests_motor/test_motor_synthetic.py"),
                      ("MATERIAL_REGRESSIONS_R1.log",HERE/"test_material_r1.py")):
    command=[sys.executable,"-B","-X","utf8",str(test)]
    start=datetime.now(timezone.utc).isoformat();timer=time.perf_counter()
    result=subprocess.run(command,capture_output=True,encoding="utf-8",errors="replace",check=False)
    elapsed=time.perf_counter()-timer;end=datetime.now(timezone.utc).isoformat()
    text="COMMAND: "+repr(command)+"\nSTART: "+start+"\nEND: "+end+"\nSECONDS: "+repr(elapsed)+"\nEXIT: "+str(result.returncode)+"\n"+result.stdout+result.stderr
    record=new(HERE/filename,text.encode("utf-8"))
    runs.append({"command":command,"start":start,"end":end,"seconds":elapsed,"exit":result.returncode,"log":record})
after={name:{"sha256":sha((STAGE/"bancada"/name).read_bytes()),"bytes":(STAGE/"bancada"/name).stat().st_size} for name in NAMES}
anchors={}
for name,patterns in {"motor.py":["def rotulo_opcoes","def validar_modelo","dupla contagem","não implementada","validar_modelo_para_conjuntos(conjuntos, opcoes)"],
                      "evidencia.py":["profiled =","n_parametros_perfilados","gl=self.m.n_dados","validar_modelo_para_conjuntos(cj, opcoes)"],
                      "fontes.py":["estatuto_origem=","admissao_primaria_verificada="]}.items():
    anchors[name]=[{"line":i,"text":line} for i,line in enumerate((STAGE/"bancada"/name).read_text(encoding="utf-8").splitlines(),1) if any(p in line for p in patterns)]
report={"unit":"F0.3.B2","claim_event":632,"reviewer":"nu2_data_sources",
        "authorization":"Parent explicitly authorized fixes to motor/evidencia and DR1 provenance after independent findings",
        "status":"FIXED_CANDIDATE_TESTS_PASS" if all(r["exit"]==0 for r in runs) else "TEST_FAILURE_REQUIRES_FOLLOWUP",
        "before":before_pins,"pre_fix_synthetic_probes":pre_probes,"after":after,"anchors":anchors,"runs":runs,
        "changes":["Subtract one M_supernova nuisance from gl for either supernova reader",
                   "Reject beta-background plus local/accumulated transport only for selected consuming readers",
                   "Reject unsupported lei_sn on plain Pantheon instead of silently ignoring it",
                   "Name artigo only for the exact preset; expose all mixed options",
                   "Mark DR1 primary-origin transcription DECLARADO, no primary SHA claimed"],
        "limits":"No observed fit, original Motor construction, new CAMB, source admission or scientific confirmation. Canonical identity was mocked in synthetic harness; root owns final manifest/integration.",
        "bancada_write":False,"candidate_modified":sorted(changes),"gate_effect":"NONE"}
json_art=new(HERE/"REVIEW_AND_FIX_R1.json",(json.dumps(report,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
note=f'''# F0.3.B2 — revisão independente do motor e correção candidata

[REAL — sondas sintéticas e código] Reivindicação 632. Revisão dos sete módulos, seguida de correções expressamente autorizadas pela coordenação. Os bytes anteriores dos três módulos alterados ficam ao lado (`*.before_r1`). O candidato foi modificado; nenhum original da Bancada ou memória foi tocado.

## Achados e tratamento

1. **Graus de liberdade:** em um modelo sintético de seis observações, três parâmetros livres e uma magnitude perfilada, a saída dizia gl={old_result['gl']}; o valor coerente é 2. Agora o retorno subtrai e nomeia `M_supernova` nos dois leitores de supernova.
2. **Combinação de convenções:** o default com fundo contendo β podia ser cobrado junto com transporte local/acumulado, que o próprio contrato descreve como dupla contagem. A validação conjunta atua só no leitor selecionado. TGL/eff + Planck/DESI foi preservado. Pantheon simples recusa uma lei SN que seu código não implementa.
3. **Rótulo:** uma combinação mista era chamada de artigo só por ter beta_no_fundo=nao. Agora artigo exige equivalência integral ao preset; a combinação mista exibe as opções.
4. **Fonte DR1:** os cinco coeficientes tinham citação histórica, mas não pino primário no contrato da função. O recibo agora declara `DECLARADO`, SHA primário nulo e admissão não verificada. Nenhum valor foi alterado nem houve nova admissão.

## Verificação

Estado: `{report['status']}`. Harness original e regressões materiais foram executados em subprocessos novos com `-B`; logs incluem comando, início, fim, segundos e saída. Só foram usados resíduos e centros sintéticos. A extração de arquivos e os pins não equivalem a validação física.

O JSON contém hashes anteriores/atuais, linhas das correções e recibos. A guarda canônica foi simulada pelo harness; a integração com manifesto real fica com a coordenação. Não houve ajuste observado, CAMB novo, abertura de rito nem mudança de gate.
'''
md_art=new(HERE/"REVIEW_AND_FIX_R1.md",note.encode("utf-8"))
print(json.dumps({"status":report["status"],"runs":[{"exit":r["exit"],"log":r["log"]} for r in runs],"after":after,"json":json_art,"markdown":md_art},ensure_ascii=False,indent=2))
raise SystemExit(0 if all(r["exit"]==0 for r in runs) else 1)
