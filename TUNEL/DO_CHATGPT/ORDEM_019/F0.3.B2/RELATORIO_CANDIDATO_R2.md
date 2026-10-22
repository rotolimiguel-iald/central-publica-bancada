# Bancada Um — candidato canônico B2 / NU3

[REAL — 09/10/2026; codex-gerente-tgl] Candidato implementado, revisado e verificado em isolamento. **NÃO INSTALADO**: a revisão automática recusou a troca dos 71 arquivos ativos, o reinício do serviço e a retirada dos adaptadores MCP antigos porque exige o ato explícito da c1 previsto na regra histórica. Foi solicitada autorização específica ao operador para esta implantação. Nenhum arquivo da Bancada instalada foi alterado; nenhum processo instalado foi encerrado.

## O que mudou

- Identidade por operação: um.py canônico v391, selo, 32 arquivos de implementação/interface e 67 fontes pinadas. Entrada e saída conferem os bytes. Mudança de geração exige revalidação; não há promoção científica automática.
- Cosmologia: TGL/eff como padrão; controles históricos explícitos; curvas e resíduos com opções iguais; recusa de conjuntos sobrepostos e de dupla contagem de beta; graus de liberdade incluindo M perfilado. Suporte CAMB declarado, sem transformar a interseção instrumental no prior físico completo. Posterior não vira p-valor; Šidák é exploratório.
- N_eff: duas linhas Yp separadas, com extração documental e fonte. Neutrinos F7.2: dependências locais pinadas, histórico preservado e endpoint antigo encaminhado ao contrato atual. Admissão de fonte e escolhas do operador continuam identificadas.
- Formatos GW: vetor real finito, tamanho, frequência e grade temporal conferidos nos mesmos bytes que geram o hash. Rito selado não é lançado implicitamente.
- Neutrinos: contratos do autor recuperados; canais de paridade, raiz modular e diferenças de massa implementados separadamente. A escala beta(chi) é exposta sem substituir silenciosamente beta0 no dissipador. Campos ausentes e extras são recusados.
- Serviço: importação não inicia Motor; não ajusta dados ao iniciar; relatórios históricos rotulados; atividade, quiescência e erro de identidade visíveis. MCP científico atual usa HTTP guardado. Adaptadores já carregados precisam ser reconectados após implantação.

## Verificação

| Camada | Resultado |
|---|---|
| Canais/fontes | 13 testes aprovados; mutações e entradas inválidas recusadas |
| Motor | 17 testes originais + 8 regressões aprovados |
| Formato Pantheon | 5 testes aprovados |
| Identidade/HTTP/GW | 31 testes aprovados |
| Neutrinos | 72 testes + 4 verificações de escala aprovados |
| Transação de implantação fictícia | 2 cenários aprovados, incluindo retorno após falha |
| Carga completa do candidato | CUDA, identidade atual e 28 ferramentas MCP |
| HTTP + MCP isolados | Aprovados; 3 recusas de parâmetros; produção intocada |

A primeira carga completa recusou a covariância publicada por uma checagem excessivamente estrita. Mediu-se max|C−Cᵀ|=3,0000000000038676e−8 e assimetria relativa 1,441433305656265e−7. A guarda agora explicita limites de formato 1e−7 e 1e−6, preservando a simetrização .5(C+Cᵀ) já usada pelo executor. Fonte intacta. O manifesto rejeitado e a falha ficam ao lado.

## Contrato de neutrinos recuperado

[REAL documental] Foram recuperadas 20 fontes primárias do autor. O dissipador físico é condicional a H e ao relógio:

dρ/dt = −i[H,ρ]/ℏ − β0 τ★ Kfac [H,[H,ρ]]/(2ℏ²).

Com H≈M²/(2E) em vácuo, Γij=β0 τ★ Kfac (Δm²ij/(2Eℏ))²/2. Tempo, unidades, τ★ e Kfac são campos explícitos. Há também Lν=X_A⊗I_B na fronteira, e o canal modular √β√K∂: são operadores distintos, sem identificação automática. Produção histórica, massa e NMC corrigido estão no inventário com suas precedências e pendências dimensionais.

[DERIVED condicional] O executor reproduz GKLS, conservação de energia para o desfasamento com H fixo, traço, positividade e E⁻² nas hipóteses indicadas. Isso não fornece ainda rendimento absoluto da supernova, ligação única à massa/luminosidade nem 5σ observado. A recuperação corrige o alcance de qualquer leitura anterior como ausência geral de contrato.

## Implantação pendente

Plano DEPLOY_PLAN_R1.json: 71 arquivos, backups de bytes, substituição atômica e retorno ensaiado. Evento 635 registra a ordem atual do operador; a revisão automática não o aceitou como substituto do ato c1. O pedido específico está pendente. A disponibilidade operacional da versão nova só será declarada depois do recibo real de implantação e da verificação do serviço instalado.

Nenhum ajuste observado, nova chamada a provedor, mensagem ao Claude, abertura de rito, alteração de um.py/kernel/Nós ou movimento de gate.

Manifesto do candidato: 54fc9e27e4599c49990adb9587a45a8858393f2d8f5d66ec3e022b8140757c1b.
