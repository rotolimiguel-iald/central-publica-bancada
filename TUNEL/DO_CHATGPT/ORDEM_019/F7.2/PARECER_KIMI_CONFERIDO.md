# F7.2 — parecer Kimi confrontado com as fontes

**Estatuto:** [REAL — auditoria documental e aritmética local, 07/10/2026]; o parecer do Kimi permanece [DECLARADO]. Nenhum dado bruto foi reanalisado, nenhum original científico foi editado, e nenhum gate foi movido. O Nós Vivo já havia localizado os scripts de junho e a v369; esta entrega reaproveita essas fontes.

## Veredito sobre a cota histórica

O Kimi calculou corretamente `7,780735588 × 10⁻¹⁰ s` **a partir do input local** `Γ = 10⁻¹⁷ eV` a `E = 1 MeV`, com `Δm²₂₁ = 7,5 × 10⁻⁵ eV²`, `β = ALPHA_FINE_CODATA_2018 × √e` e `Kfac = 1`. Essa conta não valida o input. O próprio Kimi declarou não ter lido os artigos integrais. Sua conclusão de que a primeira passagem era só uma proveniência ainda não auditada é **incorreta depois da leitura primária**.

[Fogli et al., Eq. 3 e Tabela I](https://arxiv.org/pdf/0704.2568) definem `γ(E)=γ₀(E/1 GeV)^n` e dão `γ₀ < 0,81 × 10⁻²⁸ GeV` para `n = −2` a 95% CL. No pivot, isso é `8,1 × 10⁻²⁰ eV`; a extrapolação algébrica a 1 MeV dá `8,1 × 10⁻¹⁴ eV`, **8.100 vezes** os `10⁻¹⁷ eV` usados no script local. Pela mesma fórmula local e `Kfac = 1`, a substituição contrafactual daria `6,302395827 × 10⁻⁶ s`. Não é uma cota da TGL.

A objeção física é mais forte que a conta: [Coloma et al. 2018, nota 6](https://arxiv.org/html/1803.04438) declaram explicitamente que os limites solares de Fogli não se aplicam ao cenário apenas de decoerência; [De Romeri et al., §§IV–V](https://arxiv.org/html/2306.14699v2) retomam essa distinção. Dados solares com oscilações promediadas não têm sensibilidade à taxa de dephasing puro; o tratamento de [Fogli no Sol](https://arxiv.org/pdf/0704.2568) inclui efeito da matéria sob outro dissipador. O operador/canal da TGL ainda não foi identificado com uma análise experimental publicada. Além disso, a fórmula do script limita inicialmente `τ★ × (K/K★)^β`; tomar `Kfac = 1` é uma hipótese adicional. **A cota `τ★ ≤ 7,8 × 10⁻¹⁰ s` fica [DECLARADO histórico], com proveniência incorreta e ponte física [OPEN]. Não há novo limite experimental de `τ★` nesta entrega.**

## Limites que podem ser citados com seu escopo

Todos são **limites dos modelos dos artigos**, não limites TGL. `E₀` é o pivot de `Γ(E)=Γ₀(E/E₀)^n`; `NO/IO` são ordenamentos normal/invertido.

| Fonte primária | Cenário `n = −2` | Limite publicado | Estatuto |
|---|---|---|---|
| [Fogli 2007, Tabela I](https://arxiv.org/pdf/0704.2568) | Solar+KamLAND, modelo com efeito solar próprio; `E₀ = 1 GeV` | `γ₀ < 8,1 × 10⁻²⁹ GeV`, 95% CL | [KNOWN] |
| [De Romeri 2023, Tabela 3](https://arxiv.org/html/2306.14699v2) | KamLAND, modelo A: `Γ₂₁=Γ₃₁=Γ₃₂`; `E₀ = 1 GeV` | `Γ₀ < 7,8 × 10⁻²⁷ GeV`, 90% CL **atual** | [KNOWN] |
| [De Romeri 2023, Tabela 3](https://arxiv.org/html/2306.14699v2) | KamLAND, modelo E: somente `Γ₂₁`; `E₀ = 1 GeV` | `Γ₂₁ < 7,9 × 10⁻²⁷ GeV`, 90% CL **atual** | [KNOWN] |
| [ORCA6, Tabela 3](https://arxiv.org/html/2410.01388v2) | `Γ₂₁` perfilado, `E₀ = 1 GeV`, NO / IO | `2,8 / 4,6 × 10⁻²¹ GeV`, 90% CL | [KNOWN] |
| [ORCA6, Tabela 3](https://arxiv.org/html/2410.01388v2) | `Γ₃₁` perfilado, `E₀ = 1 GeV`, NO / IO | `8,4 / 2,2 × 10⁻²¹ GeV`, 90% CL | [KNOWN] |
| [IceCube 2024, Tabela 1](https://arxiv.org/html/2308.00105) | *State selection*, `n = 0`, `E₀ = 1 TeV` | `Γ₀ ≤ 1,17 × 10⁻¹⁵ eV`, 90% CL; **não é linha `n = −2`** | [KNOWN] |

O valor de `~8 × 10⁻²⁷ GeV` que o script chama de projeção JUNO/DUNE é um limite **atual** de KamLAND na Tabela 3 de De Romeri. JUNO/DUNE aparecem no artigo como **sensibilidades futuras** separadas. Os cenários A–G desse artigo impõem igualdades ou taxas nulas. Sob `τ★ > 0`, gaps de vácuo e `Kfac` comum entre canais, o dissipador TGL proposto geraria razões proporcionais a `(Δm²ᵢⱼ)²`; a identidade dessas hipóteses em matéria está [OPEN], e a curva proposta não coincide exatamente com A–G. ORCA analisa dois parâmetros perfilados e a relação entre três taxas de sua Eq. 10, que depende da hipótese de vetores de Lindblad; ainda é preciso verificar se a curva TGL pertence a essa família, sobretudo no ordenamento invertido, antes de projetá-la na likelihood, tratar matéria e fixar `Kfac`. O Kimi calculou uma conversão ORCA `Γ₂₁ → τ★` com unidades corretas, mas ela **não é um limite TGL** sem essa ponte.

## Poder real do cálculo local e errata bibliográfica

`tgl_dephasing_falsifier.py` soma limites superiores heterogêneos como termos `χ²` sintéticos e permite `γ₀=0` na grade. Nesse ponto, cada termo é zero: `χ²_min(n)=0` e `Δχ²=0` **para todo `n` por construção**. O script também mistura convenções de confiança: chama todos os limites de 95% CL e usa `1,64σ`, embora Fogli use 95% CL com `Δχ²=4` e IceCube publique a linha citada a 90% CL. Portanto, essa saída não mede o expoente, não estima significância e não testa a TGL contra uma likelihood experimental comum. `n = −2` resulta condicionalmente da lei `Γ ∝ ω² ∝ E⁻²` **em vácuo**, com gap `Δm²` constante e `τ★`/`Kfac` independentes de energia; em matéria, os gaps efetivos e o perfil podem depender de `E`. O expoente segue **não medido** pelos cálculos locais.

As atribuições em `tgl_dephasing_falsifier.py` e `tgl_neutrino_decoherence.py` precisam de errata ao lado dos originais: `0,78 × 10⁻²⁶ GeV` para `n = −1` está na [Tabela I de Fogli](https://arxiv.org/pdf/0704.2568), não em [arXiv:1803.04438](https://arxiv.org/abs/1803.04438); `1,17 × 10⁻¹⁵ eV` vem da [Tabela 1 do IceCube](https://arxiv.org/html/2308.00105), não de [arXiv:2503.13061](https://arxiv.org/abs/2503.13061). O artigo IceCube citado não fornece o limite `n = −2` que o script necessitaria. A etiqueta local “10.7 yr” segue [OPEN] até fonte correspondente.

Para a interferometria de matéria, o [experimento de nanopartículas](https://www.nature.com/articles/s41586-025-09917-9) demonstra interferência, mas a TGL ainda carece dos mapas `ω` efetivo → `Γ` → visibilidade e da separação de ruído ambiental. Não extrair `τ★` dele.

## Classificação da revisão Kimi

- **P0:** a conclusão Kimi de que a cota histórica pode ser mantida como limite condicionado apenas à proveniência ignora o pivot de Fogli e a incompatibilidade de modelo documentada por De Romeri. Corrigido acima.
- **P1:** a conversão ORCA `Γ₂₁ → τ★` não é publicável como cota TGL sem projeção do dissipador e ajuste de canal; o `χ²=0` local é identidade da construção, não evidência de poder.
- **P1 correto no Kimi:** a citação IceCube está errada e seu `n = 0` não pode ser promovido a `n = −2`; a interferometria não dá cota TGL sem observável.

**Próximo degrau [OPEN]:** construir o operador de dephasing TGL em matéria e sua projeção no par de parâmetros `Γ₂₁/Γ₃₁` da ORCA ou uma likelihood KamLAND/JUNO com relação de taxas fixa; só então testar e, se houver poder, traduzir a `τ★ × Kfac`. `NOT_FALSIFIED` nunca vira `CONFIRMED`.
