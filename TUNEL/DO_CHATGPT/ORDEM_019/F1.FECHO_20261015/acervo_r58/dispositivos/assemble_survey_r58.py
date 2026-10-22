"""Assemble a documentary survey; no scientific code is executed."""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(__file__).parent
BASE = ROOT.parent.parent


def pin(path):
    p = Path(path)
    b = p.read_bytes()
    return {"path": str(p), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}


def exclusive_json(path, data):
    with Path(path).open("x", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


sources = {}
def source(key, path, anchors, role):
    sources[key] = {**pin(path), "anchors": anchors, "role": role}


source("graviton_docx", r"C:\IALD\IMac LA\Física - TGL\Artigo\The (O) Graviton.docx", ["P1210–1229", "P1252–1273"], "Artigo do acervo autoral; reconhece colaboração GPT-5 em P1021. Extrato OOXML, não demonstração de autoria individual de cada frase.")
source("graviton_tex", r"C:\IALD\papers_latex\graviton_paper\graviton_paper.tex", ["L221–260", "L332–368", "L438–510"], "Artigo científico, fonte textual primária examinada.")
source("graviton_appendices", r"C:\IALD\papers_latex\graviton_paper_english_v2\graviton_appendices.tex", ["L110–139", "L236–257", "L311–333"], "Apêndice científico; versão não idêntica ao protocolo M1 do DOCX.")
source("manual", r"C:\IALD\Patente Supercondutor\MANUAL_OPERADOR_SUPERCONDUTOR_HOLOGRAFICO_TGL.docx", ["P88–124", "P126–166", "P171–193", "P234–275", "P356–387"], "Manual de preparação/leitura; parâmetros e desempenho propostos não medidos nesta revisão.")
source("jan09", r"C:\IALD\Patente Supercondutor\PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_INPI.docx", ["P71–80", "P154", "P194", "P362"], "Fonte científica da patente já custodiada em R57; reaproveitada, não reconstruída.")
source("final2", r"C:\IALD\IMac LA\Física - TGL\Base Referencial Completa TGL\Teoria_Gravitacao_Luminodinamica_TGL_FINAL2.docx", ["P204–281", "P309–350", "P369–430"], "Artigo/compilação anterior com quantização de modos e estimativas dimensionais; equações OOXML linearizadas exigem preservar o original.")
source("fronteira", r"C:\IALD\papers_latex\A_Fronteira_UNIFIED.tex", ["L720–787", "L840–882"], "Fonte anterior da energia de ligação; vários enunciados são identificações físicas propostas, não novos resultados desta revisão.")
source("mqc", r"C:\IALD\Central de Patentes\Patentes\MQC - Microprocessador Cúbico\mqc_pi_inpi.pdf", ["p6:L1–23", "p12:L1–33", "p13:L12–24"], "Patente científica; texto extraído por página, caracteres matemáticos parcialmente degradados.")
source("psinet", r"C:\IALD\Central de Patentes\Patentes\Psi_Net_Protocol_PI_INPI.tex", ["L394–420", "L536–576"], "Protocolo de transmissão/codec; não confundir suas shares com campos físicos.")
source("patente_depositada", r"C:\IALD\Patente Depositada\BR102025026951-1_870250111877 - Registro INPI.pdf", ["p10:L1–18", "p11:L1–31", "p12:L1–27"], "Partes técnicas selecionadas do depósito; metadados e comprovantes financeiros não são evidência científica.")
source("movimento", r"C:\IALD\Base Referencial Completa TGL\Taxa de acoplamento mínimo equacoes de movimento.docx", ["P742–775", "P783–806"], "Manuscrito anterior com equações de campo contínuo, dissipação e dispersão; não recompilado nem rederivado.")
source("alpha2", r"C:\IALD\Base Referencial Completa TGL\Taxa de Acoplamento mínimo Alpha2 - Beta TGL.docx", ["P200–229", "P254–268"], "Formulação histórica da constante; não substituir automaticamente beta atual por seu alpha2 literal.")
source("tempo107", r"C:\IALD\IMac LA\Física - TGL\Provas\1\TGL_Apendice_Tecnico_107-A_Tempo_colapsos.pdf", ["p2:L5–8", "p3:L3–6", "p7:L3–10"], "Tempo como contagem e calibração; página2 também inspecionada visualmente.")
source("tempo132", r"C:\IALD\IMac LA\Física - TGL\Provas\1\Artigo_132_TGL_Tempo_Serie_Recursiva.pdf", ["p1:L3–17"], "Série recursiva proposta, interpretação ontológica.")
source("tempo133", r"C:\IALD\IMac LA\Física - TGL\Provas\1\Artigo_133_TGL_Tempo_Ressonancia_Retroativa.pdf", ["p1:L8–18", "p3:L1–3"], "Recorrência com atraso e condição espectral; não identificação da dinâmica OH.")
source("clock_noise", r"C:\IALD\IMac LA\Física - TGL\Provas\2\TGL_article.tex", ["L29–70", "L74–85"], "Artigo de2025, autoria declarada no cabeçalho, ruído de tempo próprio e relógios correlacionados.")
source("custo", r"C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py", ["L282–293", "L1983–2024"], "Programa/artigo primário apenas lido; nenhuma importação ou execução.")
source("ponte", r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\A Ponte Einstein Cartan Miguel.tex", ["L370–390"], "Artigo primário atual; estatuto REAL é o atribuído pela fonte, sem nova verificação aqui.")
source("um", r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py", ["L28782–28809", "L28821–28843", "L28930–28964", "L28994–29065"], "Fonte atual apenas lida; RelativePhaseCharacter embutido, sem build novo nem alegação de versão instalada.")

findings = [
 {
  "id":"D58-01", "title":"Heteródino e correlação temporal já especificados", "sources":["graviton_docx","graviton_tex"],
  "located":"DOCX P1216–1224: LO deslocado em80MHz, fotodetector200MHz, batimento S(t), G1(tau)=<S*(t)S(t+tau)>; P1214 cavidade1m, FSR150MHz. TEX L464–475 distingue g1 de HBT g2.",
  "status":"[REAL] presença documental; [DECLARADO] desempenho e realização física; [INPUT] proposta de protocolo.",
  "reuse":"Reaproveitar definição do batimento e autocorrelação, receptor com LO e tratamento de frequência intermediária. Corrige uma ausência documental ampla de receptor.",
  "residual":"Ainda requer contrato que identifique S(t) com variável de saída da mesma dinâmica OH de R57, ganhos, normalização, fase de referência e unidades.80MHz é offset do protocolo óptico, não omegaOH nem frequência de Rabi. O ajuste |G1|=exp(-gamma*tau)*cos(Deltaomega*tau) em P1223 requer revisão do sinal/módulo antes de uso. Não executado."
 },
 {
  "id":"D58-02", "title":"Tomografia e duas quadraturas já têm aparato", "sources":["graviton_docx","graviton_appendices"],
  "located":"DOCX P1255–1264 e TEX L318–333: divisor50/50, detectores balanceados, LO com fase ajustável, ADC14bit100MS/s, varredura0..2pi em pi/50,10^6 quadraturas por fase, Wigner/Radon e matriz rho_ss em Fock nmax50.",
  "status":"[REAL] protocolo escrito; [INPUT]/[DECLARADO] preparo e capacidade instrumental, não medida realizada.",
  "reuse":"A leitura complexa por quadraturas e a preparação de estado estacionário são anteriores. Reusar a arquitetura do receptor, sem inferir que o LO externo produz um relógio interno.",
  "residual":"Não há aqui identificação do modo óptico reconstruído com sigma+_OH, nem prova da aproximação/corte Fock para o mesmo aparelho. As versões M1 divergem: apêndice TEX L253–256 chama I=|<a>|^2 de intensidade após preparo |1>; isso não se identifica automaticamente com Tr(rho*a†a). O protocolo precisa preservar essa distinção."
 },
 {
  "id":"D58-03", "title":"Leitura formal relativa já instalada na fonte do Um", "sources":["um"],
  "located":"RelativePhaseCharacter: referenceState, quadratureReference, crossReadout(x)=2*x0*star(x1), interferenceX/Y e reconstructedPhase; reconstructed_phase_formula L29006, cross_readout_global_phase_invariant L28943, character_readouts_reconstruct_fields L29049.",
  "status":"[REAL] enunciados e provas presentes na fonte; compilação desta revisão não realizada. Histórico de auditoria está no cabeçalho L28805–09.",
  "reuse":"As duas probabilidades já recuperam exp(2i theta), e há consumidor de reconstrução de campos a partir de GravitationalResponseRecord. Não reconstruir esse resultado.",
  "residual":"Origem física/registro continuam explicitamente INPUT/OPEN L28802–04. É fase relativa, invariante sob fase global. Transportar G_OH global para esse observable exige referência/interferência explícita; o nome comum não resolve o mapa."
 },
 {
  "id":"D58-04", "title":"Preparação e cadeia laser–APD do Supercondutor", "sources":["manual","jan09"],
  "located":"Manual P97–124: vácuo, vapor d'água, pressão e RF OH1.667,359MHz, rampa de potência; P171–193: laser780nm, moduladorEOM, monitor de entrada/saída, APD e demodulação. Jan09 P71–80 H/J; P154 lock-in relativo à entrada.",
  "status":"[REAL] receita instrumental escrita; [DECLARADO] realização/desempenho; [INPUT] valores de engenharia.",
  "reuse":"Não falta todo preparo/receptor: há sequência experimental e caminho de detecção. Fontes complementares, sem escolher exclusivamente MQC/Supercondutor/Psi-NET.",
  "residual":"Receita de pressão/potência não fixa rho0 no espaço de estados usado em R57. Falta transferência complexa do detector e identificação do observable. Manual P153–158 ajusta ALPHA2 histórico a0,012: não transportar tal ajuste para beta canônico sem regra explícita. Eta~1 de correlação de dados não é automaticamente amplitude a ou eta limitado por alpha2 em outras fontes."
 },
 {
  "id":"D58-05", "title":"Modos contínuos, preparo coerente e duas pontas anteriores", "sources":["final2","graviton_tex","graviton_appendices"],
  "located":"FINAL2 P204–267: campo, modos normalizados un, frequências, Hamiltoniano e vácuo deslocado por J; P269–281: permanência por correlação temporal e par two-mode squeezed. TEX L252–257 fornece Sij(r,phi)|0> e variância entre modos; L365–367 operadores de salto correlacionados.",
  "status":"[REAL] ingredientes explícitos na escrita; [DECLARADO] derivação global/realização não auditada nesta etapa.",
  "reuse":"Há alternativa ao sinal unilateral: autocorrelação de campo e correlação de dois modos, com estados nomeados. Fornece proposta física para a pergunta de duas pontas e expansão modal, não só analogia verbal.",
  "residual":"Modos/estado/correlação ainda não ligados à mesma preparação OH e ao pacote contínuo R5. Precisam domínio, positividade/normalização e compatibilidade com gerador/dinâmica escolhidos. Não substituir campo de dois pontos por correlação de bytes da Psi-NET. Fórmulas de variância do apêndice são preservadas como fonte, não certificadas aqui."
 },
 {
  "id":"D58-06", "title":"O próprio acervo distingue fonte física e fonte canônica", "sources":["final2"],
  "located":"P313–318: omega0^2≈c²k0²+mu²+2xiRc², mu=meff*c²/hbar. P332–341: Jn, q0=Jn/omega0² e escala de J; P341 declara que montagem define mapa J físico↔J. P350 leitura SQUID/optomecânica; P388–391 Pmin≈N*hbar*omega0²/Q e tau=Q/omega0.",
  "status":"[REAL] formulação e ressalva explícitas na fonte; [INPUT] parâmetros/alvos; [DECLARADO] dimensionamento numérico não recalculado.",
  "reuse":"Unidades SI e orçamento de bombeio/perdas já foram escritos. P341 é a localização exata da ponte instrumental a completar, não pretexto para exigir escolha exclusiva de dispositivo.",
  "residual":"As escalas10–1000Hz do modo-espelho, RF OH1,667GHz e óptica780nm pertencem a setores distintos. Não igualar J fonte clássica, J salto Lindblad, J luz antiunitária, V0/hbar e omegaOH por homonímia."
 },
 {
  "id":"D58-07", "title":"Energia de ligação e frequência estão explicitadas", "sources":["fronteira"],
  "located":"L720 Hlig=-V0(|+><-|+|-><+|), L725 V0 energia; L787 tau=V0/hbar; L864 Egamma=V0=h*nu; L882 tau=omega=2pi*nu. L844 kappa=hbar*c/(alpha2*lP²), denominada rigidez.",
  "status":"[REAL] equações escritas; [POSTULATE]/[DECLARADO] identificação física nesta leitura documental. Não revalida derivações históricas.",
  "reuse":"Há lastro autoral direto para V0 como energia e taxa V0/hbar. A relação não precisa ser inventada novamente.",
  "residual":"Não localizei neste trecho Eref e identificação de V0 com parâmetros do H/J OH mantendo bomba/acoplamento. Kappa aqui é rigidez, não kappa de perda nem escala modular. Constante alpha2 histórica literal não substitui beta runtime."
 },
 {
  "id":"D58-08", "title":"MQC tem escala própria e equação mestra declarada", "sources":["mqc"],
  "located":"p6:L1–23: Heff com omega0=2pi*150THz, dissipadores convencional e holográfico, gammaholo=alpha2*omega0/(2pi); p12:L1–33 fabricação/guia óptico/calibração; p13:L12–16 estado de dois psíons.",
  "status":"[REAL] descrição técnica escrita; [DECLARADO] estabilização e desempenho não medidos nesta revisão.",
  "reuse":"Contribui uma frequência física, arquitetura de faces e fórmula da taxa. Frequência de drive10Hz e parâmetro beta=0,3 de modulação são locais ao exemplo.",
  "residual":"Dissipador nomeado não fornece todos os operadores e seu domínio; não há identificação demonstrada entre canal150THz, OH e representação contínua. Beta de modulação não é betaTGL."
 },
 {
  "id":"D58-09", "title":"Psi-NET/depósito fornecem codec e transporte", "sources":["psinet","patente_depositada"],
  "located":"Psi-NET L400–420 g=sqrt(|L|), s=sign(L), quantização e L'=s*g²; L544–566 separação/recombinação de shares(Psi,Theta,kappa). Depósito p10–12 explicita módulos e reconstrução inclusive domínio espectral.",
  "status":"[REAL] algoritmo/contrato documental existente; [DECLARADO] métricas alegadas na fonte, não reexecutadas.",
  "reuse":"Camada de codificação/transporte e conservação documental da informação; complementar às camadas mecânicas/ópticas.",
  "residual":"Kappa share=|g|+mask não é taxa modular. Reconstrução finita/quantizada não demonstra correlador Wightman/CCR, Hamiltoniano de laboratório nem limite contínuo físico."
 },
 {
  "id":"D58-10", "title":"Campo dissipativo contínuo já formulado na Base Referencial", "sources":["movimento","alpha2"],
  "located":"Movimento P748 GKLS de H_GP; P756–758 saltos a,n,theta; P768–771 rho,v,theta,g; P795 dispersão omega²=cs²k²+hbar²k⁴/(4m²)-i*omega*2alpha2/tP. Alpha2 P210 princípio variacional bulk/fronteira; P259 taxa de dissipação.",
  "status":"[REAL] formulação anterior localizada; [DECLARADO] completude/derivação e domínio não certificados aqui.",
  "reuse":"Não declarar ausência de equações contínuas ou de dissipação. Há um sistema de PDE e espectro proposto a comparar com o mesmo gerador.",
  "residual":"Aproximação linearizada e regime de fônons não provam convergência da rede finita OH nem existência de semigrupo para operadores não limitados. Documento histórico alpha2 usa parametrizações diferentes do beta atual; não transplantar silenciosamente."
 },
 {
  "id":"D58-11", "title":"Tempo contado já exige calibração explicitamente", "sources":["tempo107","tempo132","tempo133","clock_noise"],
  "located":"107-A p2 define N(t)=sum1_{tau_n<=t}, T(t)=alpha*N(t), alpha>0 calibrado por relógios físicos (imagem p2 conferida); p3 intensidade de eventos.132 usa soma geométrica;133 usa recorrência com atraso e condição espectral. TGL_article L34–57 fase integral E*dτ/hbar, ruído e taxa omega²*Sτ(0)/2; L81–85 relógios correlacionados/GHZ.",
  "status":"[REAL] registros anteriores; [ONTO] interpretação do tempo; [INPUT]/[POSTULATE] calibração e ruído; sem medição nova.",
  "reuse":"A fórmula operacional do tempo como contagem tem precedente preciso. O relógio físico de referência já aparece no texto; não é exigência inventada agora.",
  "residual":"Alpha desta calibração não é automaticamente estrutura fina/beta. Nenhum desses trechos identifica contagem com fase OH/GKLS atual. Condição de convergência da soma e condição espectral do atraso não podem ser transferidas à dinâmica angular periódica."
 },
 {
  "id":"D58-12", "title":"Três artigos atuais preservam a distinção forma/escala", "sources":["custo","ponte","um"],
  "located":"Custo L282–293 chama tau*=tP de identificação principiada CONJECTURE, não derivação; L1983–2024 constrói saltos Davies com KMS. Ponte L372–380 relaciona tempo à irreversibilidade. Um contém reconstrução da fase relativa e ressalva da origem física.",
  "status":"[REAL] leitura das fontes atuais; sem execução do programa ou novo build. Não afirma a versão efetivamente carregada em outro app.",
  "reuse":"Há direção temporal, estrutura modular e leitor formal. O alvo é conectá-los ao observable e às unidades do dispositivo, preservando hipóteses existentes.",
  "residual":"As fontes examinadas não autorizam promover identificação de relógio de Planck a prova nem saltar da reversibilidade angular à dinâmica dissipativa da face. R4 integral não é satisfeito por esta pesquisa documental."
 }
]

exclusions = {
 "misnamed_financial_pdf": "O arquivo de Patente Depositada cujo nome sugere reivindicação revelou ser comprovante financeiro. O extrato temporário28 foi removido, original intacto; nenhum dado financeiro integra este relatório. EXTRACTION_SUPPLEMENT mantém apenas metadados de origem/extração; aquela entrada não é evidência científica nem arquivo entregável.",
 "dissertacao": "Capitulo1.pdf foi identificado como dissertação jurídica/filosófica, sem ponte instrumental pertinente. Não usado para R4; nenhuma consulta a processos do Escritório.",
 "authorship": "Manual de verificação e Frequência.docx incluem forma dialogal e respostas atribuíveis a IA; não usados como prova autoral exclusiva. Presença no acervo não demonstra autoria individual nem validade científica.",
 "scope": "Não leram todos os documentos do inventário mecânico. A busca lexical e a seleção semântica são limitadas aos temas/raízes declarados. Nenhum dado observado aberto, experimento executado, provedor chamado, build realizado ou memória canônica modificada."
}

coverage = {
 "method":"Levantamento por mapa/índice, nomes de arquivo, buscas lexicais dirigidas e leitura de trechos primários. DOCX OOXML; PDF pypdf com paginação, somente107-A p2 renderizada e inspecionada. Extração pode degradar fórmulas; fonte binária permanece autoridade.",
 "roots":[r"C:\IALD\Patente Supercondutor",r"C:\IALD\Central de Patentes\Patentes",r"C:\IALD\Patentes",r"C:\IALD\Base Referencial Completa TGL",r"C:\IALD\IMac LA\Física - TGL",r"C:\IALD\Dissertação",r"C:\IALD\Patente Depositada",r"C:\IALD\papers_latex",r"C:\IALD\observaveis_tgl",r"C:\IALD\Artigo\Haja_Luz"],
 "selected_primary_pins":len(sources),
 "not_exhaustive":True,
 "queries":["receptor / detector / APD / lock-in / heterodyne / homodyne / quadrature", "OH / omega / frequency / tempo / clock", "two-point / correlation / rho_ss / preparação", "V_0 / V0 / Eref / E_ref / kappa", "nome de dispositivo/artigo no inventário IMac"],
 "observaveis":"Busca textual em scripts/relatórios; predominam cosmologia, espectros/SNe e neutrinos. Nenhum script executado. Não foi localizado ali nesta seleção um contrato adicional de receptor OH.",
 "map":pin(ROOT/'MAP_REUSE_R58.json'),
 "nodes":pin(ROOT.parent/'NOS_VIVO.json'),
 "prior_r57":pin(BASE/'device_clock_r57'/'DELIVERY_R57.json'),
 "mission_reference":pin(r"C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json"),
 "mission_revision_observed":455,
 "index_note":"MAP_REUSE inclui seq1186/1187 e1189: R56 leitor angular e R57 contraexemplo/relógio local; índice/mapa orientam, fontes sustentam. Nós Vivo informa unidade ausente; não se reconstruiu o grafo."
}

result={"schema":"iald-corpus-device-survey/v1","created_utc":datetime.now(timezone.utc).isoformat(),"actor":"/root/miguel_r56_review","unit":"F1.FECHO_20261015","team_claim":939,"mission_reference":coverage['mission_reference'],"status":"DOCUMENTARY_INGREDIENTS_FOUND_R4_NOT_CLOSED","scientific_status":"[REAL] localização e hashes; interpretações/reaproveitamento [DERIVED]; alegações das fontes [DECLARADO] onde não verificadas.","sources":sources,"findings":findings,"coverage":coverage,"exclusions":exclusions,"residual_contract":["Preparação rho0 e modo/observable de saída no mesmo H/J com bomba e acoplamento preservados.","Transferência detector/LO/ganho: campo de saída e polarização OH, fase relativa e banda base, sem equiparar portadora externa a tempo interno.","Identificação física e unidades de V0/Eref/kappa; não misturar rigidez/perda/escala modular/share.","Se o alvo é rede contínua: forma de duas pontas positiva/local e compatível, refinamentos e dinâmica no mesmo sistema; expansão modal/squeezing escritos não constituem essa prova."],"recommendation":"Reusar M1/M6, preparação do manual, RelativePhaseCharacter e modos/correlações da FINAL2; cotejar a ponte de interface, em vez de reconstruir receptores e fórmulas já existentes. Nenhuma seleção exclusiva de dispositivo é requerida por este levantamento."}
exclusive_json(ROOT/'SURVEY_DISPOSITIVOS_R58.json', result)

lines=["# R58 — dispositivos, leitura e relógio", "", "Em nome de /root/miguel_r56_review; F1.FECHO_20261015, claim de equipe939. Revisão de missão observada455. Levantamento documental; nenhum requisito é aceito aqui.", "", "## Resultado", "", "**Há peças primárias anteriores que precisam ser reaproveitadas:** heteródino com LO80MHz e correlador temporal; homódino balanceado e tomografia; preparação laser/RF/APD; leitura formal relativa no Um; expansão modal e estado de dois modos; energia de ligação e frequência. A frase ampla ‘não há receptor/preparo/correlação’ seria incorreta. **R4 integral permanece aberto nesta seleção:** falta a identificação desses objetos e suas unidades no mesmo sistema OH com bomba/acoplamento, seguida do mapa ao contínuo. Não há motivo documental para escolher exclusivamente um dispositivo.", "", "Presença documental e hashes são [REAL]. Desempenho, execução de aparelho e derivação física alegados nas fontes continuam [DECLARADO] quando não verificados. Não se construiu prova científica nesta etapa.", ""]
for f in findings:
    lines.extend([f"## {f['id']} — {f['title']}", "", f['located'], "", f"**Estatuto:** {f['status']}", "", f"**Reaproveitar:** {f['reuse']}", "", f"**Residual:** {f['residual']}", "", "**Fontes:**"])
    for key in f['sources']:
        s=sources[key];lines.append(f"- `{s['path']}` — {', '.join(s['anchors'])}; SHA256 `{s['sha256']}`.")
    lines.append("")
lines.extend(["## Cobertura e exclusões", "", coverage['method'], "", coverage['index_note'], "", "Raízes consultadas por seleção, não leitura integral:"])
lines.extend(f"- `{p}`" for p in coverage['roots'])
lines.extend(["", coverage['observaveis'], ""])
lines.extend(f"- **{k}:** {v}" for k,v in exclusions.items())
lines.extend(["", "Os manifestos de extração preservam os pinos dos documentos e dos derivados. A entrada financeira28 está explicitamente excluída e seu extrato não integra a entrega. A dissertação jurídica foi apenas classificada, sem uso científico. A busca atual não demonstra ausência no corpus inteiro.", "", "## Próximo elo", "", result['recommendation'], ""])
lines.extend(f"{i}. {t}" for i,t in enumerate(result['residual_contract'],1))
with (ROOT/'SURVEY_DISPOSITIVOS_R58.md').open('x',encoding='utf-8',newline='\n') as f:f.write('\n'.join(lines)+'\n')
exclusive_json(ROOT/'SCOPE_EXCLUSIONS_R58.json', exclusions)
artifacts=[p for p in ROOT.rglob('*') if p.is_file() and p.name!='DELIVERY_DISPOSITIVOS_R58.json']
delivery={"status":result['status'],"artifacts":[pin(p) for p in sorted(artifacts)],"scientific_sources":len(sources),"findings":len(findings),"scope":"Documentary survey, no canonical writes, no scientific execution, no provider, no semantic acceptance.","summary":pin(ROOT/'SURVEY_DISPOSITIVOS_R58.md'),"structured":pin(ROOT/'SURVEY_DISPOSITIVOS_R58.json')}
exclusive_json(ROOT/'DELIVERY_DISPOSITIVOS_R58.json',delivery)
print(json.dumps({"delivery":pin(ROOT/'DELIVERY_DISPOSITIVOS_R58.json'),"summary":delivery['summary'],"sources":len(sources),"findings":len(findings),"artifacts":len(artifacts)},ensure_ascii=False))
