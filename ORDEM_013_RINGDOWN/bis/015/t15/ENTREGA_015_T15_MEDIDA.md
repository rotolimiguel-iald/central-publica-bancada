# T-15 — MEDIDA instrumental, pré-registro sem disparo

**Estatuto:** [REAL] leitura e cálculo reprodutível dos artefatos pinados; [DERIVED] custo projetado; [OPEN] dispersão de recuperação. **Não-cego.** O pré-registro `T15_PRE_REG.json` precedeu `T15_MEDIDA.json`; o script `t15_diagnose.py` conferiu os hashes das fontes antes de calcular. Zero injeções e zero posteriores T-15 foram executados. `σ_jit,rec = null`, `σ_sys(δf̂) = null`; gate intacto.

## Resposta

**Não é factível recuperar `δf̂` em 50 injeções Brownian com o instrumento Kerr V2 atual, nas condições registradas.** O tempo projetado caberia no 1 h reservado ao T-15 sob paralelismo ideal, mas três pré-condições científicas falham:

1. **Ruído real H1+L1:** o T10-B2 mediu condição H1 `1.0095493105457432×10¹²`, **0,954931% acima** do limite pré-registrado `10¹²`. L1 `2.0857589152395008×10⁹` passa. A regularização B3 de H1 foi classificada `REGULARIZED_INPUT_NOT_PHYSICAL_NO_PE`; não equivale à covariância real qualificada.
2. **Observável:** o ajuste Kerr V2 do T10-A estima `dtau220`; T-15 pede `δf̂`. `brownian_phase`/`phase_factor` realizam incrementos de fase com variância `2ΓΔt`, sem deslocamento determinístico de frequência. A predição para a realização deixa `delta_f` e `frequency_scatter` indeterminados até definir desenrolamento, janela, estimador e ruído. É preciso codificar e congelar um estimador de `δf̂` e os pares Brownian/RG antes de qualquer dispersão de recuperação.
3. **Identificabilidade:** no 220 isolado, `log f220` e `log τ220` dão no máximo dois observáveis intrínsecos para `Mf`, `af` e `δf220` livres (três parâmetros; nulidade estrutural ≥ 1). No T10-A, o análogo com `dtau220` mostrou posterior livre com desvio padrão `0,313422` em uma realização; com prior IMR, `0,154037`. Essas larguras **não** são dispersão entre injeções. O T10-A′ mediu posto 3 apenas para uma matriz 220+440 hipotética; a injeção tinha amplitude 440 zero e nenhuma PE multimodo foi paga. O banco T10-C contém 10 formas de duas famílias, sem recuperação.

## Custo numérico

O `ORCAMENTO_015_v12.json` registra teto total `35,017243 h`, consumo `13,221246 h` e alocação específica T-15 de `1,000000 h`. A diferença aritmética total é `21,795997 h`, **não saldo livre**: o orçamento todo já está alocado. A estimativa T-15 usa no máximo 28 workers. O tempo medido de `456,876205 s` vem de **um posterior sintético de `dtau220`** T10-A; `638,34 s` é o proxy Kerr V2 citado na ordem, ambos [INPUT/DERIVED] para Brownian em ruído real.

| Trabalho | 456,876 s/posterior: série / ondas de 28 | 638,34 s/posterior: série / ondas de 28 |
|---|---:|---:|
| 50 Brownian, uma recuperação cada | 6,346 h / 0,254 h | 8,866 h / 0,355 h |
| 50 Brownian + 50 RG pareadas, 100 recuperações | 12,691 h / 0,508 h | 17,732 h / 0,709 h |

As horas de ondas são pisos otimistas sem custo de preparação, contenção, falha, convergência ou aumento de tempo pela nova dimensão `δf`. O custo real da recuperação proposta segue [OPEN]. O piloto de duas injeções foi barrado pelo pré-registro antes de qualquer job pesado; não se usa esse custo projetado como evidência de viabilidade.

## Menor emenda operacional suficiente

Não há troca de um único número que resolva as três falhas. Para manter a meta **H1+L1 real e `Mf/af` livres**, a menor emenda é: (i) achar e qualificar um bloco off-source H1 sob o limiar já fixado, sem promover B3 a dado físico; (ii) acrescentar `δf220` e congelar sua definição, janela, semente, ajuste RG pareado e verificação de convergência; (iii) injetar um segundo modo **não nulo** (221 ou 440) e demonstrar identificabilidade com PE multimodo em um piloto. Isso muda o modelo instrumental e exige novo pré-registro e custo medido, ainda sujeito a 1 h de T-15 ou realocação testemunhada.

O caminho de menor implementação seria usar **só L1** e um prior independente de `Mf/af` vindo da inspiral, além do estimador `δf`. Ele muda o alvo para L1/IMR–RD e requer rotulagem e pré-registro próprios; não quita o T-15 H1+L1 com remanescente livre. pSEOB só-220 também não oferece fuga medida: o T04 não entregou posterior convergido aceito.

**Fontes primárias e hashes SHA-256:** ordem T-15 `c903681d01eec5ed8d55b7fe69e061a79b3a7b73eecede8f895cfb2d127f75a3`; orçamento v12 `e54fb7a0de69e2ba834ef805c26dc103496d3e6f2cec09583e3d646dff39fd1d`; T10 final `689806ca4917868b066f8b5ffd0dcd9df5aad2470cef3c341adc18b010c72fce`; T10-B `321ae1e1a6ee6b3d0bd61306f0effb696350426c498caf54cc14c341dd08457a`; T10 posterior `cd04f281fe55e2ae1ed718af9e1b8d4b0aacfc5bdd872aafe6d2196b69b13582`; código de desenrolamento `2858efdbf0e1f8ba2b8419e9f2a987c340ae02e2e5825495f0d3381b2d26e830`; template `16d7fbc25e94b0351e7050aa5055db421365953782cec1a668d68f11e5cc5132`; predição `fd0fc446e1c732f3d782210c6effa7cb7faeaeb7a51a434d4f397f1da89bd652`. A lista completa está no pré-registro, conferida pelo script.
