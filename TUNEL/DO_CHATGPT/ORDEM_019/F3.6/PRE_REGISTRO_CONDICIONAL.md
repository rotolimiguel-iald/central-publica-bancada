# F3.6 — controle 2 D1: pré-registro condicional e plano de execução

**Estatuto:** [INPUT] desenho C16 reaproveitado; [REAL] fontes e guarda lógica conferidas; [OPEN] modelo físico CPL e σ(β | w₀, wₐ). Este documento fixa a função do portão e a ordem dos testes **antes do dado**. Não é o congelamento integral do modelo: faltam definições físicas e faixas de w₀, wₐ, que precisam ter hash antes do Asimov físico. Nenhum dado observado foi aberto nesta entrega.

## O que já existe

- Consulta Nós Vivo F3.6: rota d1.controle2_w0wa, seq. 52, PROPOSTA; D1 V3; C16. O controle 1, por jackknife, já foi registrado. Não repetir a rodada real V3.
- tgl_camb_worker_v3.py e d1_v3_pipeline.py têm primitiva de fundo com vácuo w = −1, CAMB de referência, covariância Planck comprimida, erros DESI DR1, autoverificações, injeção e recuperação. C16 pede uma cópia, não mudança desses originais.
- SINTESE.md C16 determina: se σ(β | w₀, wₐ) ≥ β, registrar parede de poder e **não** abrir o dado.
- MAPA_VERIFICADO_COM_CETICOS.txt §C16 corrige a síntese: mudar apenas set_dark_energy em CAMB não constrói o fundo TGL com CPL. A própria correção classifica o item como CONSTRUCAO_PENDENTE + DECISAO_DO_OPERADOR.

## Quatro decisões tipadas que antecedem o worker físico

1. **Posição da CPL no mapa [INPUT].** Φ_total = 1 + β|1 + w_eff| inclui ρ_DE(a) e p_DE(a) dinâmicas no total, ou a CPL modifica apenas a referência? Fixar também o mesmo mapa nos setores comparados.
2. **Cruzamento phantom [INPUT].** Fixar a avaliação ponto a ponto de |1 + w_eff| quando ρ+p cruza zero. A primitiva da V3 Λ usou integrando não negativo porque ρ+p ≥ 0; não se pode transplantá-lo sem reexaminar o sinal.
3. **Âncora da primitiva [INPUT].** Fixar o substituto de P(a→∞)=ρ_Λ, incluindo C e o fecho H(a=1)=H₀. Extrapolar CPL ao futuro infinito não é consequência da V3.
4. **Faixas e fiduciais [INPUT].** Fixar priors de w₀, wₐ, pontos de injeção fora do limite Λ e domínio onde E²>0. A σ marginalizada depende destas escolhas. D1–D8/R1–R6 ratificadas em 02/10, consultadas, não responderam esta definição específica.

A ordem de executar C16 autoriza a preparação. Não fornece os quatro conteúdos acima. Até sua fixação, não existe σ(β | w₀, wₐ) numérica honesta.

## Ordem do ensaio, com função de veredito pré-fixada

1. Copiar ambos scripts V3 para sandbox; conferir hashes dos originais. Congelar um JSON de modelo CPL com as decisões, autor, data e SHA-256. Falta/divergência de qualquer escolha recusa a execução.
2. Implementar a extensão completa de FundoV3: ρ_DE e ρ+p, primitiva/cauda e fecho, E(z), distâncias e horizonte sonoro; atualizar CAMB de referência coerentemente. O caso w₀=−1 e wₐ=0 deve reproduzir o worker V3. Falha de raiz, E²≤0 ou autoverificação falha fica explícita.
3. Injetar apenas observáveis **sintéticos** em β=0 e β=ALPHA_FINE_CODATA_2018 × √e calculado em runtime, no fiducial CPL congelado e em ao menos um ponto CPL diferente. As médias observadas não são carregadas. Reusar, se aplicáveis, covariância/erros, sementes 1000+s e K=48 da V3. Validação V3: Asimov |β̂−β_inj|<0,1σ e χ²<10⁻³; |E(0)−1|<10⁻⁸; resíduo da segunda equação <10⁻⁶; β=0/CAMB <5×10⁻³; média dos pulls <3/√K; desvio dos pulls entre 0,7 e 1,3; todas realizações ajustadas. Eventual mudança para CPL deve ser registrada **antes** do ensaio, não após ver resultado.
4. Calcular Fisher branqueado do Asimov com β, w₀ e wₐ livres **juntos**, além de H₀, ω_b, ω_c; C somente se a definição congelada o admitir. σ(β | w₀,wₐ) = √[(JᵀJ)⁻¹]ββ na escala física. Matriz singular, Hessiana não finita, β no limite do prior ou checagem falha: INCONCLUSIVE_SYSTEMATICS, sem pseudoinversa que simule poder. Registrar correlações, versões, hashes e todas recusas.
5. Portão C16: σ≥β → UNDERPOWERED_DO_NOT_OPEN_DATA; σ<β → POWER_GATE_PASSED_PENDING_SEPARATE_OPERATOR_DATA_DECISION. A igualdade bloqueia. σ ausente, zero, negativa, NaN ou infinita não passa. A abertura real é outro ato do operador, mesmo com portão favorável.

**Poder antes do dado:** limiar σ/β<1, apenas diagnóstico. Hoje σ/β = NAO_MEDIDO. Não converter o controle em teste novo da teoria, nem mover o veredito da V3, o kernel ou o gate.

## Entrega atual

portao_poder.py implementa somente a desigualdade e a recusa de entrada inválida. Seu selftest usa números artificiais e lê zero dados; **não é Asimov cosmológico, não é injeção-recuperação CPL e não cumpre o critério de FECHADA da F3.6**. A receita executável espera as quatro decisões tipadas.


<!-- F36_LAMBDA_C1_20261008 -->
## Errata ao lado — 08/10/2026: portão local no ponto Λ

[REAL, auditoria c1; INPUT técnico do controle] A auditoria `AUDITORIA_F3_6_C1_20261007.md` corrige a frase acima «até sua fixação, não existe σ numérica honesta». Para o **Fisher tangente no ponto Λ** (β=0, w₀=−1, wₐ=0), as composições A e B′ e as escolhas de cruzamento/âncora dão a mesma derivada após o fecho H(1)=H₀. As escolhas ainda são necessárias para o modelo CPL fora desse ponto, mas não antecedem este diagnóstico de poder.

[INPUT congelado no cálculo local] Fiducial H₀=67,5, ω_b=0,02237, ω_c=0,1200, mν=0,06 eV, c=0; seis parâmetros livres juntos: (H₀, ω_b, ω_c, β, w₀, wₐ). Primário da V3: Planck comprimido (R,l_A,ω_b) + 12 observáveis DESI DR1, **sem SH0ES** e sem priors planos no Fisher. β de comparação é calculado em runtime como `ALPHA_FINE_CODATA_2018 × √e`. O valor central sintético é a previsão CAMB no fiducial, não a média observada.

[ERRATA D1F-01/03/V1] A matriz corrigida usa os cinco blocos D_M–D_H da Tabela 1 DESI 2024 VI, com ρ=−0,445/−0,420/−0,389/−0,444/−0,477; e a inversa 3×3 de Chen, Huang & Wang 2019, apêndice A, para Planck. A matriz diagonal V3 permanece só como sensibilidade. A resposta de β é construída de `ρ_total=E_CAMB²` e `ρ+p=(1/3)dρ/dln(1+z)`, com a evolução do neutrino massivo do próprio CAMB; mν=0 é controle. Isto corrige a dupla contagem do FundoV3 no **tangente Λ**, sem reivindicar um worker CPL completo.

[INPUT da base] O mapa **nu** de R da V3 é comparação histórica e recebe a σ principal do controle 2. O mapa **efetivo** `R ∝ √[(1+β)Ω_m]` é a escolha posterior do operador; sua σ é relatada ao lado, sem misturar as bases nem alterar a V3 selada. A covariância não usa médias observadas. Fontes primárias: https://arxiv.org/html/2404.03002 (Tabela 1) e https://arxiv.org/html/1808.05724 (Apêndice A).

[REAL numérico exploratório, antes do selo final] A primeira execução local deu σβ=0,01804348 (nu, covariâncias corrigidas, mν=0,06), β_runtime≈0,01203130, σ/β≈1,4997; posto do Fisher 6, condição da Jacobiana branqueada≈743,9. A e B′ coincidiram na derivada de β; o portão C16 dá `UNDERPOWERED_DO_NOT_OPEN_DATA`. Os passos escalados 0,005/0,01/0,02 deram σ no intervalo 0,01790070–0,01836213: a exigência experimental de estabilidade de 0,5% **falhou** (até 1,77%), mas o menor σ ainda excede β por 48,8%. A medição não é precisão subpercentual; relatar o intervalo. A execução com fonte congelada após este adendo será recibo de reprodutibilidade, não uma segunda tentativa independente ou nova inferência.

[REGRA DO PORTÃO] Para este diagnóstico, σβ≥β fecha por falta de poder; nenhum dado observado é ajustado e nenhuma pergunta sobre o modelo CPL fora de Λ precisa ser elevada para decidir o portão. A execução no dado continua vedada. A construção CPL completa e a injeção-recuperação fora de Λ não foram feitas.

[ERRATA DE ESCOPO] Durante a inspeção da estrutura do pipeline V3, a leitura de linhas exibiu incidentalmente o literal `_dados_reais()` com médias publicadas embutidas. A função não foi chamada e tais médias não entraram no cálculo. Portanto, onde este documento diz «nenhum dado observado foi aberto», leia-se: **nenhum dado observado foi processado/ajustado; houve exposição visual incidental do literal no código**. O Asimov usa somente média sintética no fiducial e covariâncias/erros publicados.


# F3.6.E1 — errata ao lado após o fecho de C16

<!-- F36_E1_POS_FECHO_20261008 -->

**Data:** 08/10/2026. **Estatuto:** [REAL] cronologia e pins conferidos na auditoria c1; [DERIVED] desigualdade de Fisher; [OPEN] rotas posteriores. A F3.6 está **FECHADA pelo critério**, com `UNDERPOWERED_DO_NOT_OPEN_DATA` no Asimov sintético em Λ. Esta camada corrige a escrituração; não refaz o cálculo, não altera o FREEZE e não move o gate.

## História efetiva das três rodadas

| Hora local | Ocorrência auditada | σβ na base nua, covariância corrigida |
|---|---|---:|
| 03:23 | Primeira rodada WSL, núcleo β do FundoV3: dupla contagem do neutrino, integração a partir do futuro. O valor foi exibido antes do FREEZE. | 0,018020762 |
| 03:25:42 | Reescrita do núcleo β com ρ do CAMB, correção D1F-V1 e âncora hoje. | — |
| 03:26 | Segunda rodada WSL. A entalpia da energia escura foi fixada em zero no ponto Λ às 03:26:03, tornando A = B′ por construção. | 0,018043479 |
| 03:28 | Selftest dos passos sobre código anterior ao FREEZE; a auditoria verificou sua equivalência com o congelado, salvo uma frase de limitação. | intervalo 0,017900698–0,018362135 |
| 03:31:28 | Gravação do `FREEZE_PRE_RUN.json`, **depois** de duas rodadas e do selftest. | — |
| 03:32 | Terceira rodada; recibo congelado com números idênticos aos da segunda. | 0,018043479 |

**Correção [REAL]:** a frase do `PRE_REGISTRO_CONDICIONAL.md` «A primeira execução local deu σβ=0,01804348» é falsa. Esse valor é da **segunda** rodada. Após ver σ, a alteração física que afetou a conta foi a troca do núcleo β, incluindo sua âncora, com mudança de σ de aproximadamente **+0,13%**. A auditoria também registra a fixação da entalpia escura em zero no ponto Λ; A = B′ não é validação independente de dois modelos fora de Λ. O FREEZE antecede só o recibo da terceira rodada; não se deve chamá-lo de congelamento prévio à primeira execução.

## Escopo da parede medida

- **NÃO-CEGO [REAL]:** a inspeção expôs incidentalmente médias publicadas no literal `_dados_reais()` do pipeline V3 e em páginas consultadas. As médias observadas não foram processadas nem ajustadas; o Asimov usa previsão sintética no fiducial Λ. CAMB 2.0.4 no WSL foi usado nas três rodadas do `asimov_lambda.py` e em dois selftests. O relatório original já descrevia a exposição, mas omitia este rótulo.
- **Base nua [REAL]:** β de comparação saiu em runtime de `ALPHA_FINE_CODATA_2018 × √e`, dando 0,012031300400803142. A segunda/terceira rodada obteve σβ = 0,018043478961412125 = 1,4997β. O menor σ nos passos foi 0,017900698 > β. A reprodução independente sem CAMB encontrou σβ ≈ 0,018225 e correlações β–w₀ ≈ 0,694, β–wₐ ≈ −0,804. O controle mede falta de poder no DR1 para esta especificação; não cobra a teoria.
- **Base efetiva [REAL/DERIVED]:** na execução principal com mν=0,06 eV, σβ ficou aproximadamente **24,39** com a covariância corrigida e **29,24** com a V3. Está degenerada. Para Fisher positivo definido, marginalizar w₀,wₐ não pode reduzir a variância: **σ(β|w₀,wₐ) ≥ σ(β)**, na notação de controle da casa. A desigualdade do complemento de Schur não substitui os números medidos.
- **Escolha de covariância [REAL]:** D1F-01, D1F-03 e D1F-V1 de 28/09 entraram na **primária**; a covariância da V3 selada ficou como **sensibilidade**. Essa ordem inverte a recomendação da gerência, foi declarada e não altera o portão. D1F-04, a convenção de l_A, pertence à rota de reajuste da V3 (+0,96% em σβ na aferição da c1).

## Pendências separadas

- **Pergunta `call_92df0866…` (04:59:15Z):** RETIRADA da pauta da F3.6 por ter sido prematura. Esta é retirada **documental**: não há evidência de cancelamento técnico do cartão nem resposta do operador. A pendência X18 não é apagada por esta errata.
- **[OPEN]** CPL fora de Λ e CMB completo requerem rotas próprias. Controle 2 com DESI DR2 seria unidade nova, com levantamento e pré-registro próprios; σβ ≈ 0,94β é somente [CONJECTURE] do auditor com incertezas DR2 anotadas de memória, não medição nem autorização de abertura.
- Nenhum dado real do controle 2 foi aberto; nenhuma execução adicional é autorizada por este documento.

## Pins medidos nesta camada

| Artefato | SHA-256 |
|---|---|
| `MAPA_F36.json` | `7b3e8d20e5099252eb8a2207a14c55bb989ca8e39d759dff488629bd45c7d0d0` |
| `selar_f36.py` | `271e56053c751f003305d497fdafd14d22adaafb2aa08eafbc98cb6ede754dfc` |
| `ASIMOV_LAMBDA_SANDBOX/FREEZE_PRE_RUN.json` | `349e8acf4407bfe9ac9642cce3d0ec3ae340f192e5e953387c8e7b843e40aaa2` |
| `ASIMOV_LAMBDA_SANDBOX/BUILD_LOG.txt` | `668f57ba0f65e8b18e347580deb0dcd0ca69e5d3dde64c8a7e3173af200c4a05` |
| `ASIMOV_LAMBDA_SANDBOX/SELFTEST_LOG.txt` | `5e37a133b1b06f5ae8edbb8408347ffb7eb072abfc08dc8f785fdc063d91388a` |
| `AUDITORIA_F3_6_ASIMOV_C1_a809cda3.md` | `bc3bd77fba3eb555f95e33620ba29814613c3e6e324baaf39500bff859b7ed5f` |
| `linha_do_tempo_f36.json` | `e02465940f0cb3af4232cf7f228871749f8e7ce2d19f966ee3ade307bd6b99dd` |

O pin do `PRE_REGISTRO_CONDICIONAL.md` guardado no FREEZE (`9ec666ad…`) continua histórico. A terceira camada é **append após o fecho** com backup de bytes; seu hash atual é registrado em `RESULTADO_E1_20261008.json`.
