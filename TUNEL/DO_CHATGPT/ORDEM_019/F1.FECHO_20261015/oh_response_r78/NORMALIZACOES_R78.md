# R78 — normalização do radical e escala material OH

**[DERIVED — candidato analítico/documental, NOT_LEAN]** r69_locality_bridge, 18/10/2026. Reivindicação967/escopo981; referência exata FECHO_MISSION_REFERENCE.json; project e check R4 ready na revisão529, lease ef9aacd9-793b-4b41-9c3a-75e83694f0b5. Nenhum teste físico/numérico, provedor, memória, original ou gate foi alterado. Preserva a interpretação OH/espelhamento do operador em ORIGEM_R77; ORIGEM_R78 autoriza recuperar normalizações e calcular a resposta do modelo.

## 1. Peças já existentes e o que determinam

Presença em arquivo é [REAL documental]. Propostas físicas não verificadas aqui mantêm [DECLARADO]/[INPUT]; não são medições do aparelho.

| Fonte e linhas | Peça reaproveitada | Alcance efetivamente localizado |
|---|---|---|
| luz.tex:316–346 | F₀² definido pelo campo de fundo típico; expansão de campo fraco e sugestão F_min | Uma referência de campo já existe; não fornece valor independente de F_min nem área/tempo da face OH. A expansão pressupõe invariante de fundo não nulo e ramo de sinal controlado; não justifica atravessar F²=0 pelo mesmo Taylor. |
| luz.tex:983–999 | w=1/√(ρ/ρ₀), no trecho cosmológico | O quociente já explicita uma referência de densidade. Não localiza valor de ρ₀ nem sua identificação com o meio OH. A linha995 usa kg/m³, enquanto208 nomeia energia por volume: para comparar é preciso preservar a distinção massa/energia, com c² quando pertinente. |
| luz.tex:208–218 | [√ρ]=M^(1/2)L^(−1/2)T^(−1), seguida de identificação com ação/área | A primeira unidade está correta para energia/volume; a segunda identificação requer um fator dimensional. O marcador de prova em218 continua preservado. F₀ e ρ₀ localizados ao lado não bastam para demonstrar o fator. |
| A_Fronteira_UNIFIED.tex:1057–1095 | Radicalização e interpretação holográfica [L⁴]→[L²] | Recupera a motivação do autor, mas não define o mapa material OH nem um coeficiente de ação/área. Potência de unidade, dimensão geométrica e dimensão linear de estados precisam continuar separadas. |
| A_Fronteira_UNIFIED.tex:862–882 | V₀=Eγ=hν=ℏω e leitura de frequência | Fornece a relação dimensional ENERGIA↔FREQUÊNCIA se o fóton/estado e a energia de ligação tiverem sido identificados. Não determina por si qual frequência material, a área efetiva, nem o acoplamento ao modo receptor. Não reaudita nesta nota a derivação anterior da tensão de paridade. |
| tgl_paper_unified.py:224–227,282–293 | t_P=√(ℏG/c⁵), τ⋆ identificado a t_P | A própria fonte marca PRINCIPLED IDENTIFICATION [CONJECTURE — NOT a derivation] e τ⋆ como bounded INPUT no setor de falsificadores. Não promover esse relógio a tempo material OH derivado. |
| tgl_paper_unified.py:1918–1949 | Temperatura modular1 e discretização Rindler finita | Normalização espectral/modelo declarados; não calibração SI do gerador do dispositivo. |
| Patente v2:506–517,686–710 | ωOH, P/Pth, L≈9cm, A=6L², V=L³ | EXISTEM tempo de fase e geometria de projeto; não afirmar que falta toda escala. A0=A, ρ0=energia/volume e tempo de relaxação não são identificados por essas linhas. A área macroscópica do cubo não é automaticamente a área material efetiva do acoplamento. |
| Patente v2:487–496 | Integral de tensor de projeção sobre área orientada | Para exponencial dimensionalmente válida, o produto integrado deve ser adimensional. Isso requer unidades e normalização de σμν; seu nome sozinho não fixa esse contrato. Não se identifica σμν com a densidade escalar de ação abaixo. |
| R58, achados D58-01/04/05 | Receptor heteródino, preparo OH, expansão modal e correlações já descritos | Reuso documental, sem repetir rede/Fock. As remissões já distinguem receita de preparo, estado e resposta calibrada. |

## 2. Normalização admissível, sem inventar uma lei

Se ρ é densidade **de energia**, [ρ]=M L⁻¹T⁻², e ρ₀>0 possui a mesma unidade, a quantidade r=√(|ρ|/ρ₀) é adimensional. Esta é uma normalização bem definida, não uma determinação de ρ₀. Se ρ for o invariante lagrangiano com sinal, não o substituir silenciosamente pela densidade positiva de energia. O módulo não retém o sinal/fase; a informação necessária à reconstrução permanece em seu ramo ou referência separados, como R77 já exige.

Para um alvo cuja unidade é ação/área, pode-se ESCREVER o exemplo dimensional

    Σ_S = Σ₀ √(|ρ|/ρ₀),  [Σ₀]=ação/área.
    Σ₀ = ℏ/A₀,  A₀>0 área de referência.

Então [Σ_S]=M T⁻¹. Equivalentemente Σ_S=C√|ρ| com C=ℏ/(A₀√ρ₀), cuja dimensão é √(M L), precisamente o fator que faltava à identificação de luz.tex:214. Isso confirma consistência de unidades do EXEMPLO proposto pela coordenação; não o promove a lei nova da TGL, não deriva ℏ/A₀ do radical e não seleciona A₀ ou ρ₀ do aparelho.

Para uma densidade lagrangiana de **volume**, o prefator teria de ter a unidade dessa densidade (por exemplo L₀ r), diferente de Σ₀. Integrar uma densidade superficial de ação em dA já dá ação; integrá-la também em dt dá ação×tempo, salvo redefinição do integrando. É necessário declarar qual objeto e medida a expressão representa. Uma raiz de escalar não constrói sozinha um mapa de campos bulk→superfície nem seu decoder.

### Mudança de referência versus mudança física

Para s>0, trocar ρ₀ por ρ₀'=sρ₀ produz r'=r/√s. A mesma Σ_S é preservada se Σ₀'=√sΣ₀, ou, no exemplo com ℏ fixo, A₀'=A₀/√s. Assim C permanece constante. Se ρ₀ muda mantendo A₀ fixo, a previsão muda: isso não é mera renomeação de unidade. Uma razão entre duas leituras não nulas da MESMA lei/prefator cancela Σ₀ e ρ₀, mas não recupera sua escala absoluta nem a geometria/material a partir do cancelamento.

Mudar a unidade SI usada para escrever números não muda os objetos físicos de referência: números e unidades se transformam juntos. Já escolher uma nova densidade ou área de referência exige a compensação acima para representar a mesma lei. Nenhuma dessas operações altera dimensão de Hilbert, número de modos ou localização causal.

## 3. Relógio OH e gerador: o reaproveitamento correto

A patente fornece uma frequência de fase: ωOH=2πfOH. Pode-se escolher t₀=1/ωOH como unidade temporal, ou o período 1/fOH; diferem por2π e não devem ser misturados. A escolha não demonstra que τ⋆, tempo de relaxação, tempo de percurso ou tempo de bombeamento sejam iguais a t₀.

Para t=t₀u, o gerador mestre físico

    dρ/dt = −i[H/ℏ,ρ] + Σγj D[Lj]ρ

fica

    dρ/du = −i[t₀H/ℏ,ρ] + Σ(t₀γj)D[Lj]ρ.

Portanto todos os coeficientes precisam ser transportados juntos. Fixar ωOH em SI não determina os γj, a frequência de Rabi, o fator de preenchimento espacial nem a conversão W→amplitude do drive. P/Pth é adimensional, mas Pth precisa ser identificado/calibrado e o ansatz tanh não segue somente da dimensionalização. A separação de fase portadora/abertura e os sinais do quadro já estão na R74; nenhuma renomeação resolve a incompatibilidade de unidades/modos antiga.

## 4. Resultado e cobertura

[DERIVED] Fecha-se a forma dimensional admissível e sua invariância de referência. [REAL documental] F₀, ρ₀, energia–frequência e escalas de engenharia existem e são reaproveitadas. [OPEN] Não foi localizada, nos trechos/consultas desta entrega, uma identificação que fixe conjuntamente C ou (A₀,ρ₀), a superfície material OH e as taxas físicas do MESMO gerador. Não é alegação de ausência em todo C:\IALD, nem motivo para refazer a rede.

Cobertura: leitura focal dos intervalos das fontes primárias pinadas; consulta das remissões R58; consulta textual das 69 extrações já existentes R67, 2414 parágrafos, pelos padrões exatos no manifesto (zero correspondências textuais relevantes). Essa consulta não lê fórmulas em imagem, anexos, OCR, cabeçalhos ou acervo não extraído. Não executou/importou tgl_paper_unified.py nem um.py. A fonte Python é a cópia autoral localizada no inventário R58; não foi tratada como versão implantada do um.py. Os hashes abaixo são dos bytes atuais, recalculados.

## 5. Fontes por bytes

| ID | Caminho | SHA256 atual |
|---|---|---|
| luz | `C:\IALD\papers_latex\luz\luz.tex` | `6ff7e19509b066bbe981af1774cab47fa35e5ae675f8f393c110618bd9ee919b` |
| unified | `C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py` | `29c92b66b2fd6b4d589adbef4de86a67f979e03964b3f7ae892732a40ab395cd` |
| fronteira | `C:\IALD\papers_latex\A_Fronteira_UNIFIED.tex` | `90ed85500e3298b2b42282cf23f03d99989bf58ddbb2904d18086b6e3161ab28` |
| patente | `C:\IALD\Central de Patentes\Patentes\PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex` | `93fdeb35554597ae7bb248249d8f3a243f6cc01468167c40dccd097b6778979e` |
| r77 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\oh_mirror_contract_r77\RELATORIO_R77.md` | `7bc0c3a3ba984604faf0547e183225dd2fb0b4b1374bc7e93bad1842a6942302` |
| r58 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\acervo_r58\dispositivos\SURVEY_DISPOSITIVOS_R58.json` | `2da911cac3527369f5a65dfa90777fb9d7abb8bbcfb26a9b586a640a17f20b84` |
| r67 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\acervo_conjugacao_r67\SUPPLEMENT_R67.json` | `6f7916f4956ab4d546f2dc17d2a8ada88c6f5be932528284b7a83187298eb8a9` |
| origem77 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\oh_mirror_contract_r77\ORIGEM_R77.txt` | `7507b041e608f99de1490e26a99f67d6f1b807b6fc1d44a3694201e4e1985c85` |
| origem78 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\oh_response_r78\ORIGEM_R78.txt` | `83d7077a42af2c100029e6d05ed12823729951d726a97b044689f24e12ca3415` |
