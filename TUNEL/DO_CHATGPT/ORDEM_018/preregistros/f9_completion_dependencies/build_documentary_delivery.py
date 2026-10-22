"""Documentary assembly only: read/hash pinned docs and prepare a dependency matrix.
No candidate imports, numerical controls, data opening, network, AUTH or CLAIM.
"""
from pathlib import Path
import json
import hashlib
import os
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
def readj(p):
    return json.loads(p.read_text(encoding="utf-8"))
def pin(p):
    b=p.read_bytes()
    return {"path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def create(name, data):
    dst=HERE/name
    if dst.exists():
        raise RuntimeError("DOCUMENT_ALREADY_EXISTS_NO_OVERWRITE:"+name)
    b=data.encode("utf-8") if isinstance(data,str) else (json.dumps(data,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    tmp=HERE/(name+".tmp")
    with tmp.open("xb") as h:
        h.write(b)
        h.flush()
        os.fsync(h.fileno())
    if tmp.read_bytes()!=b:
        raise RuntimeError("TEMP_VERIFY_FAILED:"+name)
    os.replace(tmp,dst)
    if dst.read_bytes()!=b:
        raise RuntimeError("FINAL_VERIFY_FAILED:"+name)
    return pin(dst)

incoming=readj(HERE/"BUILD_INPUT.json")
cfg=readj(HERE/"SOURCE_AND_MAP_INPUT.json")
deps=incoming["dependencies"]
sources={}
for key,rel in cfg["sources"].items():
    p=(ROOT/rel).resolve()
    if not p.is_file():
        raise FileNotFoundError(str(p))
    sources[key]={**pin(p),"read_scope":"DOCUMENTARY_SOURCE_BYTES_ONLY_NO_SCIENTIFIC_EXECUTION"}
checks=[]
def check(label, condition):
    checks.append({"id":label,"passed":bool(condition)})
    if not condition:
        raise RuntimeError("DOCUMENTARY_CHECK_FAILED:"+label)
check("unique_dependency_ids",len({d["id"] for d in deps})==len(deps))
check("six_implementation",sum(d["group"]=="IMPLEMENTACAO_AGORA" for d in deps)==6)
check("three_qualification",sum(d["group"]=="QUALIFICACAO_NUMERICA_FUTURA" for d in deps)==3)
check("four_operator",sum(d["group"]=="ESCOLHA_CIENTIFICA_OPERADOR" for d in deps)==4)
for d in deps:
    check(d["id"]+"_two_alternatives",len(d["alternatives"])>=2)
    check(d["id"]+"_all_sources_resolve",all(s in sources for s in d["sources"]))
expected={
    "c435":"ENGINEERING_PREDICTIONS_VERIFIED_ONCE",
    "calibration_receipt":"EIGHT_FIXED_SYNTHETIC_CONTROLS_PASSED_ONCE",
    "tail_receipt":"EIGHT_PRIMARY_AND_NINE_NEGATIVE_SYNTHETIC_GROUPS_PASSED_ONCE",
    "nc02_failure":"TERMINAL_UNQUALIFIED_UNPINNED_IMPORTED_MODULE"
}
status_snapshots={}
for key,status in expected.items():
    obj=readj(Path(sources[key]["path"]))
    check(key+"_receipt_status",obj["status"]==status)
    status_snapshots[key]={k:obj[k] for k in ("request_id","status","scope","repeat_allowed","retry_authorized","automatic_retry") if k in obj}
resolver=readj(Path(sources["resolver"]["path"]))
check("resolver_not_frozen",resolver["frozen_V1"] is False)
check("resolver_not_opening",resolver["opening_authorized"] is False)
check("resolver_not_complete",resolver["F1_complete"] is False)
mm=readj(Path(sources["mm_contract"]["path"]))
check("MM_not_ratified",mm["ratified"] is False)
check("MM_five_preserved",len(mm["rows"])==5)
for row in mm["rows"]:
    check("MM_references_closed_"+row["id"], all(x is None for x in row["protected_references"].values()))
when=datetime.now(timezone.utc).isoformat()
delivered={"schema":"F9_COMPLETION_DEPENDENCIES_DOCUMENTARY_V1","at":when,
    "scope":"ORDEM018 F1e, confronto documental solicitado por ROOT",
    "status":"DOCUMENTARY_DEPENDENCY_MAP_NOT_FROZEN_V1_NOT_AUTHORIZATION",
    "map_cutoff":577,"categories":{"IMPLEMENTACAO_AGORA":6,"QUALIFICACAO_NUMERICA_FUTURA":3,"ESCOLHA_CIENTIFICA_OPERADOR":4},
    "science_executed":False,"new_measurements":False,"observed_data_opened":False,
    "candidate_imports":0,"new_scientific_requests":0,"AUTH_created":False,"CLAIM_created":False,
    "shared_memories_or_ledger_changed":False,"upstream_changed":False,
    "source_pin_file":"FONTES_E_PINS.json","dependencies":deps,
    "scope_distinctions":{
        "V1_ratifiable":"Complete reviewable algorithm, source/code/runtime pins, candidate choices and conditions; ratification remains operator act.",
        "data_dependent_checks":"Freeze recipe/identity/failure behavior before opening; evaluate protected references only after operator release.",
        "engineering":"Implementations and estimates with honest ENGINEERING_ONLY/UNBOUNDED_THEORY_ERROR are useful without a uniform certificate.",
        "calibrated_claim":"A particular conservative p/significance claim needs its model/support/domain/minimum/tail/family prerequisites; absence is unavailable, not zero or non-rejection.",
        "complete_F1":"This dependency memo is not final F1; chronological and historical reproduction contributions remain separate inherited deliveries.",
        "latest_preparations":"f820 delegated per ROOT/map574; request status is a preparation snapshot, not dispatch receipt. ad025 and bf6d are in progress at cutoff576/577, not accepted numerical results."
    },
    "do_not_repeat":[
        "c4359a48-bf7c-4dd5-a753-8c3413774cdf: consumed theoretical evaluation",
        "8b53f7c0-9f5f-49e1-87bc-cf73a7e1f79d: C01-C08 consumed",
        "4893d182-7efc-419f-ac8a-ec6803ea8d7a: tail primary/negative groups consumed",
        "c8909840-5b14-4bf5-bc2b-dfc71dbdbcaa: NC02 terminal failure",
        "ffd6ccba-cd70-4747-aceb-a10003dfb7f4: predecessor terminal, not reopened by c435",
        "No consumed checks or old preparation builders rerun by this task"
    ],
    "receipt_status_snapshots":status_snapshots}
create("FONTES_E_PINS.json",{"schema":"DOCUMENTARY_SOURCE_PINS","at":when,"raw_observed_source_hashes_reread":False,"note":"Hashes calculados dos documentos/recibos enumerados. Referências a dados contidas neles são herdadas; não foram relidos catálogos, y/C, centros ou saídas observadas.","sources":sources})
create("MAPA_ANTES.json",cfg["map"])
create("QUADRO_DEPENDENCIAS_F9.json",delivered)
intro="""# F9 — dependências concretas até um V1 ratificável

[REAL — confronto documental; nenhuma nova execução científica] O caminho restante não começa do zero: c435 verificou uma predição teórica e a montagem H1–H5 em um ponto; as revisões563/573 aceitaram estaticamente o consumidor e os priors extras. Faltam a ligação executável completa, a montagem integral dos cenários/C e os produtores de integrais/perfis/saída, seguidos de qualificação limitada ao que mudou e das decisões científicas explícitas. Serviços f820, integral θ ad025 e redutor bf6d já estão atribuídos: não duplicá-los.

Este quadro não modifica o resolutor nem declara F1 concluída. O retrato do mapa termina na seq577; novas entregas posteriores substituem o estado “em preparação” somente com seus próprios recibos. Os pins completos lidos nesta unidade estão em FONTES_E_PINS.json; as fontes são identificadas por IDs abaixo.

## O que já reduz as lacunas do rascunho

| Peça | Evidência consultada | Alcance que permanece |
|---|---|---|
| Montagem teórica H1–H5 | c435, seq572: uma chamada de engenharia verificada, 283 linhas/63 nuisance/sete escalas | Um θ; nenhuma likelihood observada, ajuste, integral em θ ou precisão uniforme |
| Consumidor da likelihood comum | a987, revisão563 sem bloqueador estático | Ty/TCTt, offsets, suporte/normalização e κ relativos implementados; cadeia concreta ainda não qualificada numericamente por esse parecer |
| Integração dos extras | df482, revisão573 sem bloqueador estático | H3/H4/H5 em θ fixo; serviços de precisão injetados, θ não integrado |
| Cota gaussiana e função tail | C01–C08/seq490 e tail8+9/seq524 consumidos uma vez | Prova condicional e controles delimitados; não são certificados físicos do composto |
| Megamasers | contrato511/revisão513 | Modelo simbólico concreto, não ratificado; referências e variâncias numéricas seguem fechadas |
| Interface de mínimos/integrais | contrato520/revisão525 | Separa engenharia/certificados; o ensaio NC02 posterior falhou terminalmente, sem resultado aritmético aceito |
| Próximos módulos | f820/seq574, ad025/seq576, bf6d/seq577 | Preparações em curso, não novas evidências de execução |

As cláusulas históricas C02/C03/C07/C10/C11 do resolutor não devem ser lidas como se nada dessas peças existisse. Esta comparação é uma atualização **ao lado**, sem alterar o rascunho selado. Três detalhes precisam acompanhar a próxima consolidação: (a) “oito controles futuros” é estado histórico; (b) a API tail vigente recusa d=0 com limite positivo como INVALID/null, embora a cauda abstrata χ²₀ seja outra identidade; (c) q=rd/rd_CAMB no documento e q=1/rd em df482 são coordenadas alternativas do mesmo prior H5, com seus Jacobianos respectivos, não rivais diferentes.

## Caminho mais curto

1. Receber/revisar f820; ligar a987+df482 ao produtor teórico existente, sem novo solver gaussiano e sem tratar o request c435 consumido como autorização para novas avaliações.
2. Concluir o builder puro da C/família e as preparações já abertas de θ/redutor. O perfil dos extras pode usar a mesma geometria afim; H4 usa B/A no mínimo da likelihood e B−λ somente no integrando com prior.
3. Qualificar apenas as junções novas e seus limites de engenharia. Não repetir C01–C08, tail17, o ponto c435 ou NC02 por rotina. Esta nota não manda executar nenhum caso nem todas as listas históricas de controles.
4. Entregar V1 único com escolhas, recursos/tolerâncias, fontes/código/runtime, função e estados de saída fixados. Referências protegidas necessárias à instanciação da C ficam para o estágio autorizado; sua receita e sua falha por ausência ficam fixadas antes.
5. Ratificação e abertura para veredito são decisões distintas do operador, conforme §6 da ORDEM018. Nenhuma medição favorável, poder alto ou certificado uniforme de toda a teoria é condição artificial para preparar o instrumento.

## Quadro por natureza da dependência

"""
group_names={"IMPLEMENTACAO_AGORA":"1. Código implementável com as interfaces atuais","QUALIFICACAO_NUMERICA_FUTURA":"2. Qualificação numérica ainda necessária, sem repetição","ESCOLHA_CIENTIFICA_OPERADOR":"3. Escolhas científicas e abertura reservadas ao operador"}
md=intro
for group,title in group_names.items():
    md+="### "+title+"\n\n"
    md+="| ID | Dependência concreta | Responsável/estado |\n|---|---|---|\n"
    for d in deps:
        if d["group"]==group:
            md+="| "+d["id"]+" | "+d["title"]+" | "+d["owner"]+" |\n"
    md+="\n"
    for d in deps:
        if d["group"]!=group: continue
        md+="#### "+d["id"]+" — "+d["title"]+"\n\n"
        md+="**Já disponível:** "+d["already"]+"\n\n"
        md+="**Objeto mínimo faltante:** "+d["deliverable"]+"\n\n"
        md+="**Alternativa A:** "+d["alternatives"][0]+"\n\n**Alternativa B:** "+d["alternatives"][1]+"\n\n"
        md+="**Encaminhamento proposto:** "+d["recommendation"]+"\n\n"
        md+="**Critério de fechamento:** "+d["closure"]+"\n\n"
        md+="**Fronteira:** "+d["authorization_boundary"]+"\n\n"
        md+="Fontes: "+", ".join(d["sources"])+"; cláusulas "+", ".join(d["clauses"])+".\n\n"
md+="""## O que não se transforma em barreira nova

ENGINEERING_ONLY é uma entrega válida quando declara o que calculou e os erros que não limitou. Concordância de resoluções, diferença entre níveis ou um nome de módulo não são certificados; essa distinção não impede a implementação. O contrato numérico já permite engenharia primeiro e uma interface certificada separada.

Para a cauda que pretenda sustentar significância, as hipóteses reais da prova continuam necessárias. Uma cota inferior L=0 e p superior1 podem ser válidos e frouxos se alvo, suporte, identidade e família estiverem completamente qualificados. Não servem para cobrir modelo desconhecido, cenário faltante ou falha. Uma não-rejeição pela cota frouxa não demonstra que o p exato seja grande nem confirma o modelo.

Não é preciso resolver antecipadamente todos os cenários físicos possíveis: é preciso declarar os admitidos e não chamar a família finita de universal. Não se exigem63 priors nuisance novos onde a medida relativa comum já foi especificada. O poder permanece saída separada, só com informações permitidas; o preflight262 não passa a ser poder global e sua exclusão preparatória dos cinco MM não altera a seleção267.

A cronologia de novidade de uso e a reprodução E45 permanecem contribuições históricas distintas. Não precisam ser refeitas para esta ligação técnica; também não constituem evidência da nova likelihood conjunta. A leitura da ordem não adota seus números históricos como resultado novo.

## Custódia e limite desta nota

Somente documentos, contratos, pareceres e recibos nomeados foram lidos/pinados. Nenhum catálogo bruto, centro observado, C observada ou conjuntoD foi aberto; zero importações de candidatos/NumPy/SciPy/backend, controles científicos, WSL, rede e provedores. O auxiliar desta pasta só monta texto/JSON e verifica estrutura/pins. Não criou unidade científica, AUTH, CLAIM nem escreveu memórias, ledger ou pacotes consumidos. A qualificação nova descrita acima é dependência futura concreta, não campanha criada nesta entrega.

"""
md+="## Fontes e pins de entrada\n\nIDs usados no quadro; os SHA256 completos e tamanhos estão no JSON de fontes. As leituras são documentais; hashes herdados de dados dentro dessas fontes não foram revalidados nos originais.\n\n"
for key,s in sources.items():
    md+="- **"+key+"**: ["+Path(s["path"]).name+"](<"+s["path"].replace("\\","/")+">) — "+str(s["bytes"])+" bytes; SHA256 "+s["sha256"]+".\n"
create("QUADRO_F9_ATE_V1.md",md)
receipt={"schema":"DOCUMENTARY_INTEGRITY_RECEIPT","at":when,"checks":checks,"checks_count":len(checks),"checks_failed":sum(not x["passed"] for x in checks),"source_count":len(sources),"dependency_count":len(deps),"scientific_execution":False,"candidate_imports":0,"observed_data_opened":False,"new_AUTH_or_CLAIM":False,"upstream_and_memories_changed":False,"meaning":"Only metadata/JSON/pin consistency; no numerical or scientific validation.","source_pins":sources}
create("RECIBO_DOCUMENTAL.json",receipt)
# Re-read all sources after rendering. No old source is rewritten.
for key,s in sources.items():
    if pin(Path(s["path"]))!= {k:s[k] for k in ("path","bytes","sha256")}:
        raise RuntimeError("SOURCE_DRIFT:"+key)
members={p.name:pin(p) for p in sorted(HERE.iterdir()) if p.is_file() and ".tmp" not in p.name and p.name!="MANIFESTO_ENTREGA.json"}
manifest={"schema":"F9_COMPLETION_DEPENDENCIES_MANIFEST","at":when,"status":"DOCUMENTARY_ONLY_NOT_V1_NOT_AUTHORIZATION","members":members,"source_pin_file":"FONTES_E_PINS.json","zero_scientific_execution":True,"map_after_will_be_separate_supplement":True}
m=create("MANIFESTO_ENTREGA.json",manifest)
for item in members.values():
    if pin(Path(item["path"]))!=item:
        raise RuntimeError("MEMBER_DRIFT")
print(json.dumps({"manifest":m,"members":len(members),"sources":len(sources),"documentary_checks":len(checks),"md":pin(HERE/"QUADRO_F9_ATE_V1.md")},ensure_ascii=False))
