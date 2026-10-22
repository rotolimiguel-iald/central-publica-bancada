# Bancada TGL — desenho do cockpit de pesquisa

**27/09/2026.** Este documento descreve o programa local de pesquisa. Não é selo científico nem proposta de alterar o gate do `um.py`.

## O que já funciona [REAL]

- Atalho `TGL` na área de trabalho com ícone próprio; lança ou reutiliza o servidor canônico em `127.0.0.1:18765`.
- Busca no índice formal **histórico v368**, catálogo GWOSC/GWTC-3/PSD, inventário documental de 28 protocolos, cadeia algébrica β e conta condicional de dephasing.
- Pergunta digitada ou ditada, transcrição corrigível, campos de hipótese principal, contraprova, explicação rival, efeito instrumental e medição discriminante; localização lexical nas fontes já catalogadas e registro append-only em SQLite. Leitura em voz alta usa recursos do navegador quando disponíveis.
- Originais científicos e bancos observacionais são lidos; não são alterados por esta bancada. Nenhum sigma conjunto ou confirmação física é calculado pela interface atual.

`SOURCE_LOCATOR` é localização; `COMPILED` exigiria recibo de build; `REPRODUCED` exigiria reexecução; `PHYSICALLY_CONFIRMED` exige análise observacional própria. Um campo preenchido pelo usuário não muda automaticamente nenhum desses estados. As investigações da aba são `EXPLORATORY_NOT_PREREGISTERED`.

## Contribuições consultadas no stack [DECLARADO]

A fila única da IALD concluiu quatro unidades de desenho. O pacote integral, com request/job IDs, autores reais e recibos, está em `C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\state\handoffs\cockpit_design_bundle.json`. A primeira unidade usou Codex e assistência ChatGPT Work/Física; as complementares foram selecionadas para Claude (grafo), Gemini/Antigravity (voz/HCI) e Codex (crítica). O roteador desta missão não permitiu travar Kimi, MiMo ou DeepSeek sem rotulá-la indevidamente como ORDEM_016; eles **não responderam** a essas quatro unidades. Nenhuma ideia textual é prova implementada.

O consenso útil para o produto é: pergunta → alternativas explícitas → fonte com versão → operação permitida → resultado e controle → revisão humana. A crítica adversarial indicou três riscos de primeira ordem: reutilizar dados de seleção como validação, somar sigmas de canais dependentes e apresentar o snapshot v368 como o kernel vigente. A proposta do grafo recomendou guardar **arestas com localizadores**, sem reindexar ou copiar o corpus. A proposta de voz recomendou fala como transcrição corrigível e comandos restritos; a atual API de reconhecimento do navegador pode depender de serviço do navegador, portanto ainda não é STT local verificado.

## Motor mínimo, sem novas camadas redundantes [PROPOSTA]

O `um.py` e o kernel continuam fontes e executores próprios. A bancada mantém apenas três responsabilidades:

1. **Perguntar** — registrar a pergunta e versões do plano. Cada revisão é um novo evento. Antes de inspecionar dados, fixar qual resultado diferenciaria TGL, modelo rival e explicação instrumental; revisão posterior permanece exploratória.
2. **Encontrar** — usar o índice formal já existente, seus hashes e relatórios; acrescentar somente arestas justificadas por uma linha de fonte lida. Se a fonte muda, mostrar `STALE`. Se só o nome foi encontrado, mostrar `INDEXED_ONLY`.
3. **Executar e observar** — catálogo de operações permitidas com parâmetros, recibos, dados e saídas. Falta de PSD, calibração, covariância ou previsão quantitativa resulta em `NEEDS_DATA`/`INCONCLUSIVE`; não se substitui silêncio por sigma.

O assistente de IA conversa **sobre** o plano e pode sugerir hipóteses, controles e a pergunta de maior ganho informacional. Toda sugestão aparece como sugestão atribuída ao executor, nunca como evidência. O operador decide o plano; código recebido do modelo não é executado diretamente. A arquitetura usa a fila/worker existente, sem novo agendador.

## Sequência de construção [OPEN]

1. **Fonte vigente**: ligar o pacote formal corrente com manifesto, versão, hash e recibo de compilação, separando “consultado” de “instalado”. A busca v368 permanece acessível como história.
2. **Grafo rastreável**: navegar `DEPENDS_ON`, `ASSUMES`, `TESTS`, `ERRATA_OF` com arestas justificadas. Um caminho sem linha-fonte para em lacuna; `ONTO` não cria observável e build formal não cria confirmação física.
3. **Primeira análise controlada**: escolher um evento e um controle reais do inventário, conferir strain/PSD/calibração/janela e previsão quantitativa TGL versus GR. Só então conectar replay físico. O registro de seleção e dependência entre canais antecede qualquer combinação estatística.
4. **Conversa por voz contínua**: integrar fala, texto e resposta da IALD com o mesmo plano e estatutos; medir latência, disponibilidade e privacidade do motor de áudio escolhido. O navegador atual fornece ditado e leitura opcionais, não conversa contínua.

Exemplo de uso presente: “Ward e GWOSC: onde encontro a relação entre a torre e os dados?” localiza declarações e um catálogo, mas não inventa uma previsão observacional entre eles. O próximo passo intelectual é escrever a previsão quantitativa e escolher um dado que a separaria de GR e de sistemática instrumental. Enquanto isso não existir, a resposta honesta é localização exploratória.

## Errata de busca na própria bancada [REAL — teste de interface]

Um teste com a pergunta sobre ringdown devolveu **1.018 módulos** porque o termo de namespace “TGL” estava em quase todos os nomes. Esse resultado é um falso elo lexical; o número corrigiu a interface. O termo genérico foi excluído, entrou um teste de regressão e a consulta corretiva devolveu **zero módulos formais** para essa pergunta. O registro #2 guarda o resultado antigo e uma errata que aponta para #3. Todos os registros #1–#3 são marcados `SMOKE_TEST`, nunca análise física. O catálogo GWTC-3 continua localizado, com estatuto próprio.


<!-- TGL_UNIVERSE_EDUCATIONAL_MAP_d480ccbf21105694 -->
## 28/09/2026 08:48 — Universo educativo, mapa livre + percurso guiado

[INPUT] O operador pediu que o sistema funcione como um programa de curso astrofísico/cosmológico, mostrando matéria bariônica, matéria escura, energia escura, CMB, expansão e estruturas, para facilitar a interação. Escolheu explicitamente “Mapa livre + percurso guiado”.

[REAL — interface instalada] Entrada http://127.0.0.1:18766/explore, oito temas com questões, explicações, experiências, fontes primárias e links aos laboratórios existentes. Navegação livre, Anterior/Próximo, marcação explícita de leitura e progresso no navegador. O atalho TGL conserva seu alvo launch.py e passa a abrir o mapa se Cosmos responder; fallback para GW preservado. Menus Cosmos/GW retornam ao mapa. Apenas Cosmos reiniciou; banco GW não reiniciado.

[REAL / DIDÁTICO] Diagrama interativo de frações de densidade, histórico logarítmico em 1+z, presets de época e controles Ωb/Ωc/Ωr; ΩΛ por fechamento. Modelo FLRW plano idealizado: matéria a^-3, radiação a^-4, Λ constante. Valores arredondados de ensino, domínio z0..100000, sem idade física, formação, perturbações ou recombinação calculada. Frações não são regiões espaciais. Fonte matemática WMAP e demais fontes primárias em EDUCACAO_FONTES.md/static/cosmos-lessons.js. Este módulo não redefine a Ωm agregada do V3 nem fornece espectros TGL. Sem novo sigma ou mudança do gate.

[REAL — verificação] 67 testes Python e 7 testes Node aprovados; rotas instaladas conferidas byte a byte, geração científica preservada 8fd20dbe0d994caedbf592065b7a0132b9d611509b096d5401e434ae485be1d0, cálculo V3 padrão idêntico ao recibo anterior. UI conferida: oito temas, percurso/progresso após reload, z1100 e z10000, recusa de composição inválida e recuperação. Revisão independente achou e foram corrigidos dois bugs: histórico velho após sequência redshift inválido→alterar composição→redshift válido; link interno recarregando e perdendo cenário. Fluxo corrigido conferido no navegador. Valores pequenos positivos são mostrados como <0,0001%, sem anunciar zero exato.

[REAL — preservação] GW 180/180 arquivos, 24165092160 bytes, mesmo load_id 8560b710-3ad7-402b-a12e-9a0b1fdf1ad3 e hashes. Memórias com backup imediato de bytes e append atômico. App local TGL somente; conversa pública/iOS/Android não modificados, builds não aplicáveis. Código por agentes locais: modelo didático/testes, roteamento/launcher, fontes primárias; coordenação: integração visual, correções, instalação e verificação. Nenhuma nova chamada externa Kimi/MiMo/DeepSeek nesta entrega.

[OPEN] Temas CMB/estruturas estão organizados para ensino; mapas e Cℓ CMB, catálogos 3D, crescimento/lentes ainda não foram conectados a essa interface. BAO e GW usam os laboratórios reais já existentes. Voz, integração de todas as sondas e teste global D10 seguem no planejamento anterior.

Guia: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\MAPA_EDUCATIVO.md`. Recibo: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\state\education_validation_20260928_084800.json`, SHA256 846b9d421ad65b775e68340dc625ee31687263572004198288ef3fea4cb2a7a7. Originais científicos intactos.



<!-- TGL_EXTREME_REGIMES_7fa2c44bca8a96e3 -->
## 28/09/2026 09:04 — Regimes extremos visíveis e métricas condicionais

[INPUT] Operador: “Inclusive eu preciso ver os locais de regime extremo com maior facilidade, porque é lá onde a TGL vai se manifestar em maior evidência”. Implementada navegação por ambientes, eventos e cenários, preservando como hipótese investigativa a relação entre regime extremo e maior evidência. Não há ranking de sigma sem medida de sensibilidade.

[REAL — interface] Seção destacada `/explore#extreme-regimes`, com seis rotas: Universo jovem/acústica (prioridade D10), horizontes/ringdown (GW250114), spin elevado, modos de maior frequência, vazios/contrastes e partículas/coerência. Cada seleção mostra o que variar, efeito a comparar, estado da sensibilidade e acesso disponível. CMB alto-z permanece didático; BAO abre o V3 existente z≤3. Vazios/partículas identificados como integração pendente. Sem coordenadas celestes inventadas.

[REAL — cenários] Links allowlist `?regime=high-spin#ringdown` e `?regime=high-frequency#ringdown` preparam apenas controles `model-*`, nunca o evento. Cenário spin: massa fonte65, spin0,95, z0,1, duração0,12s; frequência: massa fonte20, spin0,7, mesmo z/duração. Não selecionam relógio; leitura exigida do usuário. Banner deixa explícito cenário exploratório, não ajuste ao evento. Valores desconhecidos/duplicados de regime não aplicam preset.

[REAL / CONDICIONAL] UI lê do executor Γ, x=Γτ_GR, delta_tau_ensemble_exact, modo e método QNM; nenhuma fórmula física nova no navegador. Dados ausentes são indisponíveis; números minúsculos usam notação científica; R-GLOBAL exibe zero real. Seis controles HTTP medidos no executor existente: R-B referência x=0.02115589140876138, delta_tau=-0.020717592276312716; spin0,95 x=0.06251370332366527, delta_tau=-0.058835667839497216. Massa20: frequência 785.7033607931457Hz, Γ=15.886628475296325s^-1, x=0.021155891408761382 igual à referência dentro da precisão. R-A conserva efeito muito pequeno e a escala inversa com massa; R-GLOBAL zero. São previsões de ensemble sob hipóteses explícitas, sem fit, curva de sensibilidade ou sigma.

[REAL — verificação] Navegador conferiu seis cartões, deep link spin com campos corretos, relógio vazio e botão de cálculo desabilitado, seleção R-B e valores do executor, R-A não arredondado a zero, R-GLOBAL com zero, método/mode retornados, sem erros JS ou overflow horizontal. Revisão física independente examinou escalas da fonte e limites. Nenhum novo serviço nem reinício: preservada carga GW 180/180, 24165092160bytes, load_id 8560b710-3ad7-402b-a12e-9a0b1fdf1ad3 e hashes. Alteração somente da bancada local; web pública/iOS/Android não afetados. Nenhum original científico ou gate alterado.

Guia: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\REGIMES_EXTREMOS.md`. Recibo: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\state\extremes_validation_20260928_090052.json`, SHA256 a7dac6857bd7289c0e32f922a9ed93bba34bfe28636ca824885f77db83f1204b. Memórias com backup imediato de bytes e append atômico. Sensibilidade global, mapas CMB/estrutura, vazios e partículas seguem nas pendências explicitadas.



<!-- TGL_INVESTIGATION_20260928_99e70f454eccdcf7 -->
## 28/09/2026 — Investigação da bancada com agentes, sem novo sigma

[INPUT] Operador pediu examinar o sistema residente e investigar com agentes onde há melhores condições de testar a TGL.

[REAL] Três agentes locais concluídos e verificações independentes PASS: 21 cenários BAO; 29 fontes GW e inversão de Q; sete blocos canônicos e trechos do programa. MiMo concluiu parecer, preservado como DECLARADO com correções matemáticas/estatísticas ao lado. Kimi falhou sem resposta aceita, sem repetição. Nenhum resultado novo atribuído a Claude/DeepSeek nesta rodada.

[REAL — sistema] 180/180 arquivos GW, 22,50550 GiB de arrays, swap zero, seis vistas em 31–80 ms, mesmo load_id e nenhuma releitura. É ensaio em uma série, não benchmark de ajuste/concorrência. Catálogo 1.350 arquivos/~72 GiB inclui duplicatas. BAO residente contém 13 pontos e covariância 13x13; não representa todos os catálogos/mapas. GPU atende renderização; cálculo científico em GPU não medido.

[REAL/DERIVED — achados] Na comparação BAO, escala e densidade reduzem d² de 0,55873894 para 0,00473259 (99,153% da distância quadrática), exemplo entre modelos, não fit/sigma. Um modo de ringdown é compensável por massa/spin na aproximação exploratória BCW. C6 segue INCONCLUSIVE_SYSTEMATICS, lnB primário -0,002595.

[CORREÇÃO AO LADO — ACT V9] Fisher compara delta_c=-0,95, s1=1, pisos 0 e beta. O perfil é >=0,05>beta: os dois modelos são idênticos antes do ruído, F=0 estrutural nesse ensaio. Fonte e linhas conferidas; controle positivo delta_c=-1 ativa o piso, mas é diagnóstico, não nova previsão/inferência. A grade de likelihood posterior é distinta e não foi declarada toda cega. Preservado o UNDERPOWERED histórico; sua causa não pode ser atribuída somente à sensibilidade do ACT. Nenhum original alterado.

[PLANO] D10 CMB–BAO mantém prioridade estratégica: ligar tradução perturbativa/r_d e likelihoods existentes com covariâncias/overlaps. Auditar primeiro a sensibilidade ACT em cópia; para GW, diagnóstico 220+440 do mesmo remanescente na métrica de ruído, projetando nuisance e exigindo amplitude informativa. Neutrino é confronto condicionado; ecos exigem recuperação qualificada; relógios P1 têm déficit de sensibilidade no protocolo atual. Nenhuma rota recebeu poder 5sigma global demonstrado.

[ESCOPO] Relatório `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\INVESTIGACAO_PRIORIDADES_20260928.md` (SHA256 99e70f454eccdcf772607afa4bc1da92a6626432f7a46abdfce5a0f13b0c6bed). Evidências/manifesto em `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\state\investigation_20260928`; hashes calculados por script. Serviços/RAM preservados, sem alteração de original científico, kernel, gate, interface, app público/mobile. Memórias operacionais desta bancada e índices centrais recebem append com backup de bytes; linhagem científica Nós não tocada porque nenhuma versão foi selada.

