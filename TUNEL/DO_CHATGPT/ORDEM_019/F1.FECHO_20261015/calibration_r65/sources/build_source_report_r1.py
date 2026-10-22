"""R65 documentary assembly only. Never imports or executes scientific sources."""
from pathlib import Path
import hashlib
import json
import os
import re
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent
REFERENCE = Path(r"C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json")

def pin(path):
    path = Path(path)
    b = path.read_bytes()
    return {"path": str(path), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}

def write_new(name, value):
    target = HERE / name
    if target.exists():
        raise FileExistsError(target)
    b = value.encode("utf-8") if isinstance(value, str) else (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temp = target.with_name(target.name + ".tmp")
    with temp.open("xb") as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    assert temp.read_bytes() == b
    temp.rename(target)
    return pin(target)

RANGES = {
    "patent": [(38,41),(304,354),(356,370),(372,404),(431,444),(474,517),(778,828),(833,864)],
    "appendices": [(236,258),(311,334)],
    "graviton": [(343,368)],
    "Custo": [(217,227),(282,294),(11054,11066),(11190,11237),(11759,11801),(12074,12113),(17751,17757),(18231,18295),(18389,18395)],
    "Ponte": [(804,829),(2230,2241)],
    "Um_article": [(551,554)],
    "um_program": [(207133,207142),(207163,207194),(217035,217055),(217089,217101),(217332,217344),(217498,217508)],
    "R7": [(18,33),(44,79),(82,88),(92,110),(113,141)],
    "finite_pre": [(73,110)],
    "finite": [(147,156),(163,172),(184,193)],
    "JAN09": [(64,91),(179,184)],
}
PATTERNS = {
    "gamma_lambda": r"(?:gamma|Gamma|γ|Γ)[_\\{}\s]*(?:Lambda|Λ)",
    "gamma_holo": r"(?:gamma|Gamma|γ|Γ)[_\\{}\s]*holo",
    "gamma_min": r"(?:gamma|Gamma|γ|Γ)[_\\{}\s]*min",
    "tau_star": r"tau_star|tau[_\\{}\s]*(?:star|ast)|τ\s*\*",
}

def ref(source, first, last):
    return {"source_id": source, "line_start": first, "line_end": last}

def main():
    discovery = json.loads((HERE / "FOCAL_DISCOVERY_R1.json").read_text(encoding="utf-8"))
    sources = []
    for item in discovery["sources"]:
        p = Path(item["path"])
        actual = pin(p)
        if actual["sha256"] != item["sha256"] or actual["bytes"] != item["bytes"]:
            raise RuntimeError("Source drift: " + item["id"])
        lines = p.read_bytes().decode("utf-8-sig").splitlines()
        search = {}
        for name, pattern in PATTERNS.items():
            hits = [{"line": i, "text": line} for i, line in enumerate(lines, 1) if re.search(pattern, line, re.I)]
            search[name] = {"count": len(hits), "lines": [h["line"] for h in hits]}
        excerpts = []
        for a, b in RANGES[item["id"]]:
            text = "\n".join(lines[a-1:b])
            excerpts.append({"line_start": a, "line_end": b, "text": text,
                             "excerpt_utf8_lf_sha256": hashlib.sha256(text.encode()).hexdigest()})
        sources.append({"id": item["id"], **actual, "line_count": len(lines), "lexical_scan": search,
                        "read_ranges": RANGES[item["id"]], "excerpts": excerpts,
                        "role": "extrato custodiado da fonte Word, numeração física do TXT e parágrafos [n] conservados" if item["id"] == "JAN09" else "fonte textual primária ou contrato/implementação local identificado"})
    contextual = []
    for relative in ["output_field_r64/sources/DELIVERY_R1.json", "output_field_r64/sources/OUTPUT_FIELD_SOURCE_REPORT_R1.json", "output_field_r64/sources/FOCAL_SOURCE_PINS_R1.json", "physical_receiver_r63/sources/PHYSICAL_RECEIVER_MAP_R1.json", "calibration_r65/NOS_VIVO_R65.json", "calibration_r65/MAP_R65.json", "calibration_r65/IDENTIFIABILITY_COMPLETION_R65.txt", "calibration_r65/THERMAL_ROUTE_SOURCE_R65.json", "calibration_r65/THERMAL_ROUTE_SCOPE_R65.txt"]:
        contextual.append(pin(OUT / relative))
    source_pin = write_new("SOURCE_PINS_AND_ANCHORS_R1.json", {
        "schema": "r65-source-pins-v1", "created_utc": datetime.now(timezone.utc).isoformat(),
        "author": "/root/maxwell_covariance_review", "mission_reference": str(REFERENCE),
        "source_count": len(sources), "scientific_sources": sources, "contextual_evidence": contextual,
        "patterns": PATTERNS, "method": "Leitura UTF-8 de bytes, busca lexical orientadora e inspeção das faixas. Nenhum programa científico importado/executado; nenhum teste, simulação, provedor ou dado experimental aberto.",
        "coverage_limit": "Onze fontes nomeadas, mais os recibos de navegação. A busca lexical não demonstra ausência universal nem substitui a leitura semântica. DOI/bibliografia citados nas fontes não foram revalidados externamente nesta rodada.",
    })
    findings = [
        {"id":"A1", "category":"A_FONTE_EXPLICITA", "status":"DECLARADO documental; fórmula encontrada, calibração independente não localizada nesta cobertura",
         "claim":"A patente e JAN09 escrevem tanto gamma_min=alpha2*kB*T/hbar quanto L_holo=alpha2*gammaLambda*D[J], J=a_out†sigma_-+sigma_+a_in. Não escrevem uma igualdade entre gamma_min, gammaLambda ou a escala do mesmo J.",
         "anchors":[ref("patent",304,354),ref("JAN09",64,79)],
         "notation":"A macro alphaii é alpha^2 (patente39); JAN09 escreve alpha_2. São rótulos históricos do coeficiente chamado beta_TGL, não licença para substituir beta pelo quadrado de alpha_FINE. Custo11792–11801/12105–12113 registra a migração alpha2≡betaTGL; no finite beta é ALPHA_FINE_CODATA_2018*sqrt(e) em runtime.",
         "scope":"O decimal histórico0,012 e a instrução de potência da patente789–791 são proposta de especificação/controle, não medida nem ajuste admitido do beta atual."},
        {"id":"A2", "category":"A_FONTE_EXPLICITA", "status":"DECLARADO na fonte; rota térmica precisa de hipótese de classe e de ligação ao canal",
         "claim":"Custo11775–11783/12089–12096 apresenta a mesma taxa mínima via estado Gibbs, entropia finita e minimização de F. O trecho não identifica J do OH, banho, temperatura física do aparelho, saturação ou igualdade gamma_eff=gammaLambda. A estabilidade/estacionariedade mencionada não é, por si, medição da taxa.",
         "anchors":[ref("Custo",11759,11801),ref("Custo",12074,12113),ref("patent",372,404)],
         "temperature":"T kelvin em kB*T/hbar não é automaticamente T_eff=1-eta de patente403–404/JAN09[92], que é adimensional. Exige escala e mesmo significado físico.",
         "existing_ratio":"Patente377–383 já traz alpha2*gamma_eff/(kappa+gamma_phi)>1, com gamma_eff taxa OH-campo; não é igualdade que determine gammaLambda."},
        {"id":"A3", "category":"A_FONTE_EXPLICITA", "status":"DECLARADO/INPUT nas fontes; rota espectral explícita reutilizável",
         "claim":"Custo11190–11216 já dá V=ΣA_alpha⊗B_alpha, gamma_alpha_beta(omega) como transformada da correlação do banho, e KMS. É uma rota concreta de taxa independente por banho, com Hs=K_boundary, beta_KMS=1 e gamma(omega) proporcional a betaTGL no caso escolhido. Nenhum espectro de banho OH ou mapa A_alpha(omega)→J é fornecido nesses trechos.",
         "anchors":[ref("Custo",11190,11237)],
         "distinction":"Proporcionalidade, normalização modular e nome gamma não fixam a constante dimensional gammaLambda do dispositivo. Não se promove aqui a redução compacta escrita na fonte a nova prova para o salto J."},
        {"id":"A4", "category":"A_FONTE_EXPLICITA", "status":"CONJECTURE/PRINCIPLED IDENTIFICATION explícita; não calibração medida",
         "claim":"Custo282–293 escolhe tau_star=sqrt(hbar*G/c^5) e declara literalmente second postulate, NOT a derivation. Ponte822–826 e Um553 reaproveitam a lei Gamma_omega=(beta/2)*tau_star*omega² e limites por relógios. Isso fornece uma escala proposta, não medição independente de tau_star do OH.",
         "anchors":[ref("Custo",217,227),ref("Custo",282,294),ref("Custo",18231,18295),ref("Ponte",804,829),ref("Ponte",2230,2241),ref("Um_article",551,554)],
         "historical_precedence":"O trecho histórico Custo18291 sobre theorem III1 aberto não reabre R7/R8 aceitos da missão. O objeto dimensional e sua ligação ao aparelho são questões distintas."},
        {"id":"A5", "category":"A_FONTE_EXPLICITA", "status":"INPUT de especificação e de simulação; nenhuma execução nesta rodada",
         "claim":"Patente356–370 especifica H/OH/micro-ondas;506–517 dá G_OH=exp(i*omegaOH*t)*tanh(P_MW/P_th), sem determinar P_th→Omega_R→gammaLambda. Patente778–864 especifica aparelhos e preparo do meio, não uma matriz densidade conjunta nem taxas medidas. AppendixM1/M6 propõe preparação e leitura/tomografia; não relata execução que calibre gammaLambda.",
         "anchors":[ref("patent",356,370),ref("patent",474,517),ref("patent",778,864),ref("appendices",236,258),ref("appendices",311,334),ref("finite_pre",73,110),ref("finite",147,172)],
         "finite_input":"omega_c=1,omega_OH=1.2,gJC=.15,Omega=.07,gammaLambda∈{0,.3,1},kappa_i=.03,kappa_o=.04,gammaOH=.02,gamma_phi=.01 são all dimensionless INPUT; not physical calibration. Z-dephasing usa gamma_phi*D[Z], amortecimento da coerência2*gamma_phi.",
         "r63_preserved":"O contraste R63 entre as razões1.2 e frequência OH/780nm, e a necessidade de quadro/detunings, permanecem. Não se resolve com uma unidade de tempo comum. A ressalva APD/coerência versus contagem de R63 também permanece, sem repetir teste."},
        {"id":"B1", "category":"B_CALIBRACAO_COMPOSTA", "status":"DERIVED condicional; igualdade não adotada como calibração",
         "claim":"Com J_phys=s*J0 e mesma convenção de tempo, D[sJ0]=|s|²D[J0]; o coeficiente do canal escrito é lambda=beta*Gamma, Gamma:=gammaLambda*|s|². Para obter Gamma=kB*T/hbar pela rota térmica, são necessárias H_same_channel (gamma_min é a taxa lambda desse canal, não taxa total/gap), saturação, T kelvin e normalização operacional de J0. Só com s conhecido se obtém gammaLambda.",
         "anchors":[ref("patent",321,354),ref("finite",163,172),ref("R7",22,30)],
         "other_reading":"Igualar gammaLambda diretamente a gamma_min produziria outra atribuição/fator beta; a fonte não escolhe essa leitura. Não confundir as duas.",
         "thermal_limit":"Este relatório não repete a sonda da raiz nem a promove a refutação da TGL. A necessidade é provar a classe restrita e sua ligação ao mesmo termo físico."},
        {"id":"B2", "category":"B_CALIBRACAO_COMPOSTA", "status":"DERIVED condicional já existente em R7",
         "claim":"R7 já resolve o submodelo H=L_conv=0, preparação|100>,lambda=beta*gammaLambda: média de absorção2/lambda. Identificá-la com tau≈tP/beta da patente exige gammaLambda=2/tP (normalização J0 do contrato). A identificação não foi derivada; não é tempo APD, atraso de grupo, nem o gerador completo.",
         "anchors":[ref("R7",92,110),ref("patent",431,444),ref("JAN09",179,184)]},
        {"id":"B3", "category":"B_CALIBRACAO_COMPOSTA", "status":"DECLARADO na fonte + DERIVED condicional; escala de perda reutilizável",
         "claim":"Graviton352 já fornece L_loss=sqrt(kappa)*a e kappa=omega/Q. Isso permite converter Q/frequência independentes em uma escala de perda sob a convenção desse canal; não fornece Q medido do mesmo aparelho ou gammaLambda. A razão Gamma/kappa pode servir ao contrato somente se canais, modo, relógio e normalização estiverem identificados.",
         "anchors":[ref("graviton",343,368),ref("R7",58,79),ref("patent",372,388)],
         "detector":"R7 usa C=eta_det*kappa_out para contagem. kappa de linewidth/perda total não pode substituir automaticamente taxa da porta monitorada; eficiência e fração coletada não se extraem do ganho APD50–200. Também não é a kappa geométrica/Killing."},
        {"id":"C1", "category":"C_IDENTIFICABILIDADE", "status":"DERIVED condicional; restrito ao canal em exame",
         "claim":"Se o gerador e receptor R64 dependem de beta e gammaLambda somente por lambda=beta*gammaLambda*|s|², variar beta e compensar gammaLambda deixa esse modelo inalterado. Uma medida da resposta não separa os fatores sem taxa/normalização independente. Isso não afirma que toda a TGL dependa só do produto.",
         "anchors":[ref("finite",184,193),ref("R7",22,30),ref("R7",58,79)],
         "boundary":"Beta permanece fixo pelo axioma/regra vigente; a calibração independente é requisito para um ensaio discriminante da dependência, não autorização para ajustar beta ao sinal. Correntes múltiplas/mais tempos não removem a degenerescência exata se toda dependência continuar pelo mesmo produto."},
        {"id":"C2", "category":"C_IDENTIFICABILIDADE", "status":"DERIVED documental já registrado no programa; sem nova execução",
         "claim":"Um207133–140 já registra identificabilidade apenas de tau_star*Kfac;207184 mantém tau=tP,Kfac=1 como hipóteses. Inverter Gamma_omega=(beta/2)*tau_star*Kfac*omega² dá só tau_eff=2Gamma_omega/(beta*omega²); para tau_star isolado exige Kfac independente e a mesma leitura física. Limite superior sobre excesso de decoerência dá limite condicional, não valor medido de tau_star.",
         "anchors":[ref("um_program",207133,207142),ref("um_program",207184,207194),ref("Custo",18231,18295),ref("um_program",217498,217508)],
         "errata":"Um207172–180 corrige Custo18393:7,8e-10 era INPUT histórico e não cota calculada/medida; o canal posterior registra tau_star_limit=null/SEM_LIMITE_TGL. O ranking histórico do Th229 em Um553/Custo não é adotado: Um217504 diz que plataformas fornecem cotas superiores e largura/omega² decide. Nenhuma literatura externa foi revalidada nem dado aberto nesta rodada."},
        {"id":"C3", "category":"C_IDENTIFICABILIDADE", "status":"DERIVED condicional existente; alternativa não transportada por homônimo",
         "claim":"Um217089–101 e R7:113–141 já dão k=E*tau_star/hbar e taxa-raiz beta*(sqrt(E+)-sqrt(E-))²/(2hbar), na qual tau_star cancela. Sob H_SAME_ENERGY, gamma/|nu|=(beta/2)*|sqrt(E+)-sqrt(E-)|/(sqrt(E+)+sqrt(E-))≤beta/2; depende do mesmo espectro e do zero de energia.",
         "anchors":[ref("um_program",217089,217101),ref("um_program",217332,217344),ref("R7",113,141),ref("R7",82,88)],
         "limit":"É alternativa concreta independente de tau_star após transposição, não calibração de gammaLambda. D[J](I)≠0 na cascata de uma excitação, D[sqrtK](I)=0: não se identificam só por conjugação unitária. Redução/dilatação/consumidor comum ainda são necessários; a sonda2D de R7 tem receptor diferente de n_out."},
        {"id":"D1", "category":"D_LACUNA_DOCUMENTADA", "status":"OPEN dentro da cobertura",
         "claim":"Não foi localizado nas onze fontes um recibo de calibração independente da taxa Gamma do mesmo J/canal óptico-OH nem de sua razão com a perda da porta, com estado conjunto, normalização, quadro e instrumento identificados. Foram localizadas fórmulas, especificações, protocolos propostos e INPUTs; estas peças evitam reconstrução, mas não equivalem à calibração realizada.",
         "anchors":[ref("R7",44,79),ref("patent",833,864),ref("appendices",311,334),ref("finite_pre",84,102)],
         "shortest_next_step":"Fixar contrato independente Gamma=gammaLambda|s|² (ou Gamma/kappa para o mesmo modo/porta) e o preparo conjunto. Reutilizar a rota Davies com banho/acoplamento nomeados ou uma calibração de perdas/relaxação/drive com convenção e quadro explícitos. A rota térmica é candidata condicionada à prova da classe, saturação e mesmo canal; não inserir gammaLambda=kBT/hbar como fato. Usar o gerador e receptor já construídos sem outra simulação nesta etapa."},
    ]
    report = {
        "schema":"r65-calibration-source-report-v1", "author":"/root/maxwell_covariance_review", "status":"CANDIDATE_DECLARADO_AWAITING_INDEPENDENT_REVIEW",
        "mission_reference":str(REFERENCE), "requirement_id":"R4", "requirement_satisfied":False,
        "claim_scope":"R4/R5 critérios integrais preservados; R6/R7/R8 aceitos não reabertos.",
        "project_start":pin(HERE / "PROJECT_START_R1.json"), "project_resume":pin(HERE / "PROJECT_RESUME_R1.json"),
        "source_pins":source_pin, "source_count":len(sources), "findings":findings,
        "value_classification":{
            "measured_here":[],
            "published_measurements_quoted_by_source":"Custo18245–47 cita frequências/coerência de relógios; nesta rodada apenas presença documental, não verificação externa ou medição da TGL/OH.",
            "specification":"Patente frequências/potências/pressões/ganho; gravitonappendices aparato, preparo e LO; todos proposta sem recibo de realização nesta cobertura.",
            "simulation_input":"Finite todos coeficientes dimensionless INPUT; gammaLambda0/.3/1 e preparo escolhido não calibração.",
            "derived_conditional":"Conversões térmica/composição J, perda omega/Q, média do submodelo, inversão da lei de dephasing, razão lei-raiz. Hipóteses listadas em cada achado.",
        },
        "preserved_limits":["Sem testes/simulações/builds, chamadas de provedor, dados observados novos, importação/execução de fontes científicas ou alterações canônicas.","Nenhuma transição de missão/quadro, claim próprio, memória ou gate por este agente.","Não alegada ausência universal:11 fontes textuais nomeadas, faixas/hashes e padrões preservados.","Igualdade de nomes gamma/tau/kappa/J não é ponte entre operador modular, campo Maxwell, salto OH e receptor físico."],
    }
    report_pin = write_new("CALIBRATION_SOURCE_REPORT_R1.json", report)
    lines = ["R65 — fontes de calibração: candidato documental, aguardando revisão independente", "Referência: " + str(REFERENCE),
             "R4 permanece aberto. Onze fontes; nenhuma simulação, execução científica, provider, dado observado ou mutação de missão/memória.", ""]
    for f in findings:
        lines += [f["id"] + " | " + f["category"] + " | " + f["status"], f["claim"]]
        for key in ["notation","scope","temperature","existing_ratio","distinction","historical_precedence","finite_input","r63_preserved","other_reading","thermal_limit","detector","boundary","errata","limit","shortest_next_step"]:
            if key in f: lines.append(key + ": " + f[key])
        lines.append("Âncoras: " + "; ".join(a["source_id"] + ":" + str(a["line_start"]) + "–" + str(a["line_end"]) for a in f["anchors"]))
        lines.append("")
    lines += ["FONTES — hashes dos bytes e caminhos completos"]
    lines += [x["id"] + " | " + x["path"] + " | SHA256 " + x["sha256"] for x in sources]
    text_pin = write_new("CALIBRATION_SOURCE_REPORT_R1.txt", "\n".join(lines) + "\n")
    print(json.dumps({"source_pins":source_pin,"report":report_pin,"text":text_pin,"sources":len(sources),"findings":len(findings)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
