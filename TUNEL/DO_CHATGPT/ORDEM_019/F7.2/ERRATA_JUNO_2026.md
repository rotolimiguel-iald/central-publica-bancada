# F7.2 — adendo ao lado: primeira análise JUNO de dephasing n = −2

**08/10/2026.** [REAL documental] A tabela F7.2 já custodiada (SHA-256 `e848eeba67900a5812d4045c68b3005dd71a7119af2ac8e0ae4d31a0e13a6ae0`) permanece intacta. Ela não incluía [Beccaria e Ternes, arXiv:2606.13362v1, 11/06/2026](https://arxiv.org/html/2606.13362). O PDF v1 está custodiado na auditoria c1, SHA-256 `9212cd391d88846ee8065ac3ebf8ccb17be297417a86a22482fca858ed3be107`. Trata-se de análise fenomenológica das autoras sobre os primeiros dados JUNO, não de um limite assinado pela Colaboração JUNO.

| Canal/modelo publicado | Resultado da fonte | Estatuto para a TGL |
|---|---|---|
| Beccaria–Ternes 2026, primeiros dados JUNO; dephasing ambiental `D_ij(E,L)=γ_ij L(E/E₀)^n`, `E₀=1 GeV`; hipótese `γ₂₁=γ₃₁=γ`, `γ₃₂=0`, `n=−2` | **γ < 4,1×10⁻²⁷ GeV**, 90% CL (`Δχ²=2,71`), com penalidade externa solar para `sin²θ₁₂`. Fonte: §III.2 Eq. 6, §IV.2 Eq. 13 e Tabela 1. | [KNOWN] cota do modelo dos autores. `τ★_limite=null`, `SEM_LIMITE_TGL` [OPEN]: expoente igual não identifica operador, base dissipativa, normalização ou `Kfac` da TGL. |

O artigo usa 59,1 dias vivos dos primeiros dados e considera apenas a oscilação lenta `Δm²₂₁`; a hipótese de taxas difere das linhas KamLAND/ORCA na tabela anterior. Portanto os valores em GeV não são ordenados como se fossem uma única cota comum. O `NO DETECTION` e `n UNMEASURED` dos scripts históricos não são revisados por esta leitura: o limite publicado é sobre `γ` sob a família fenomenológica escolhida, não uma medição do expoente da TGL.

**Ligação operacional [REAL]:** `neutrino_canal_f72` foi instalado na Bancada em disco e auditado pela c1. Não há esse nome no `um.py` atual; o processo MCP antigo não foi recarregado. A atualização de catálogo documental aqui não declara a ferramenta ativa nem abre dados observacionais. Próximo passo físico, se autorizado: mapa do dissipador TGL em matéria para `γ₂₁/γ₃₁`, ordenamento, `Kfac` e likelihood, pré-registrados antes de traduzir a cota em `τ★`. Nenhum gate muda.
