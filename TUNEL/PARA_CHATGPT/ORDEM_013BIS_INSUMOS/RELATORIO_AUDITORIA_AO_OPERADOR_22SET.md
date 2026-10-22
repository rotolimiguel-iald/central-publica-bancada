# O relatório da gerência ao operador (22/09/2026, manhã) — o «tudo» com que o operador concordou

> Transcrição do relatório entregue pela gerência (Claude) ao operador na sessão da Central de Patentes, após a auditoria da entrega da ORDEM 013 por seis auditores independentes. O operador respondeu, verbatim: «Concordo com tudo, com uma exceção quanto a congelar, os eventos, podemos amplia-los para alcançar o 5sigma». A exceção está incorporada na ORDEM 013-bis; o resto vale como está aqui.

**Não, a bancada não entregou tudo.** O arquivo de estado dela mesma, `STATUS_ORDEM_013.json`, diz `WORK_RESUMED_NOT_COMPLETE`. Ela também não parou no M1, como a ordem mandava. Seis auditores independentes conferiram a entrega só lendo, sem tocar nos 4 cálculos que ainda rodam.

## 1. O que foi entregue e conferido `[REAL — refeito pelos auditores]`

**Segurança e régua estão em ordem.**
- Nada foi escrito fora de `Chatgpt\`.
- O um.py continua `d9f5bd5dffc3333d`, e o `/opt` do WSL não foi tocado.
- As 29 fontes e os 37 insumos estão intactos.
- Nenhum CONFIRMED ou PROVED aparece, e nenhuma leitura foi escolhida.
- A RG foi tratada como limite clássico (regra relativa).
- O fato de a análise não ser cega está dito.

**Números reproduzidos exatamente:**

| Etapa | Resultado |
|---|---|
| C0 | 38/38 linhas do texto externo cobertas |
| C1 | 10 leituras; nenhuma escolhida |
| C2 | Mapeamento analítico entregue |
| C3 | Módulo e forma de onda modificada; regressão de 3,5×10⁻¹⁶ |
| C4, GW250114 | Ramo B: ln B = 0,029 (\|ln B\| ≲ 0,1 em todos os estimadores). A correção vale 0,34σ, abaixo do ruído. |
| C4, GWTC-5.0 (31 eventos) | Desvio comum δτ̂ = +0,072 [+0,015; +0,134] (90%). A RG fica na borda (HPD 0,983). ln B: R-B −1,81, R-MOD −3,56, R-RAIZ-0 −3,66, R-LIN −8,22. Todos INCONCLUSIVE_SYSTEMATICS. |
| C6, no sinal bruto | Registro gravado 55 s antes de ler o dado. Todos os \|ln B\| ≤ 0,25, ou seja, ruído. |
| C7 | Integridade dos pacotes: 52/52, 125/125, 194/194 |

## 2. O que falta ou falhou

- **C5 (calibração) falhou onde importa.** No ramo B com SNR 40, o viés chega a 0,92 e a cobertura fica em 0,75. A marginalização da fonte não passou (só 444/1200 e 238/1200 casos aceitos).
- **Não há portão numérico do poder,** o teste que diz se o dado tem sensibilidade para decidir algo. A C6 rodou antes dele e a C4 antes do M1.
- **Faltam as notas de fechamento M1–M6** e as fichas REAPROVEITAMENTO.
- **O `reproduce_c6` da C7 tem um bug** que bloqueia a publicação.
- **R-MOD:** a bandeira está `null`, apresentada como paga sem estar; os passos 1 e 5 continuam abertos.
- **C2:** o observável físico não foi declarado.
- **C4:** faltam o tratamento de δτ̂ > 0; as tabelas por leitura; a checagem hierárquica da LVK; as injeções.
- **C6:** a rota é degenerada por construção (item 3.2) e não foi testada por injeção.
- **Higiene:** no GWTC-3, a seleção de 10 dos 18 eventos foi feita **depois** de ver o resultado, sem dizer isso; uma versão da forma de onda citada por hash se perdeu; há 53 arquivos acima de 25 MB fora do `cache\` e 4 pastas temporárias ilegíveis.

## 3. O que isso acrescentou ao nosso progresso

**3.1. O alarme do texto externo caiu.** O «10⁷⁶» é dimensionalmente falso, e a TGL não está falsificada pelo O4. As quatro exigências do texto foram respondidas: Γ(M, a, D) por leitura; Γ ≪ ω em todas as leituras, o que é verdade mas não decide nada; o ln B esperado; a forma de onda modificada, rodada no dado atual.

**3.2. O achado mais valioso: com um único modo, o ringdown não distingue a TGL.** A bancada chamou isso de `NON_IDENTIFIABLE_SINGLE_220`. Com só o modo 220 e massa e spin livres, o efeito do ramo B é imitado por um buraco negro de Kerr cerca de 1,25% mais leve. Um teste feito só com o ringdown dá ln B ≈ 0 por construção. Para quebrar isso, é preciso massa e spin vindos da inspiral (a onda completa, IMR) ou um segundo modo.

**3.3. O observável certo mudou.** Num evento único, a marca do dephasing aparece sobretudo como um tremor de cerca de 2% em δf̂, e só um terço do desvio médio em δτ̂. O teste certo é a **largura populacional de δf̂**, não a média de δτ̂.

**3.4. O poder foi medido, e a resposta é honesta.** Com o dado do O4, o ringdown não mede β. Um resultado a 5σ exigiria SNR de ringdown ≈ 490 ou cerca de 150 eventos. O5 chega a z ≈ 0,8; Einstein Telescope a 3,9; Cosmic Explorer a 7,0. Com a fonte desconhecida, o poder cai para z ≈ 0,04–0,07. A diferença entre famílias de forma de onda (~0,9 do efeito) é maior que a própria correção β.

**3.5. A partição ficou mais estreita.** Todo relógio τ★ universal já é decidido pelos relógios de laboratório da v369. O ringdown só testa relógios escalados pela fonte, R-B e R-MOD, que têm tendências **opostas** com o spin. Essa diferença é um discriminador em princípio.

**3.6. Uma pista sobre o δτ̂ > 0 do catálogo** `[CONJECTURE]`. O estimador tem viés de +0,03 em δτ̂ com SNR baixa, o que pode explicar parte desse desvio.

**Estatuto:** nada foi excluído e nada foi confirmado; o resultado é NOT_FALSIFIED.

## 4. Precisa de ordem nova? Sim: uma ORDEM 013-bis de fechamento, não de refação

- Congelar o escopo; nada físico novo. **[← a exceção do operador: os eventos ampliam-se até o 5σ]**
- Escrever as notas M1–M6 formais no contrato do túnel.
- Fazer o portão do poder numérico com hash, registrando que todas as leituras ficam abaixo de 5σ.
- Reclassificar a C6 como «C6-pre», rodada antes do portão.
- Fechar a C5 como parede medida.
- Corrigir tudo o que a seção 2 lista, dando os dois resultados do GWTC-3 (18 e 10 eventos).

À parte, uma **ORDEM 014** é opcional e depende do operador: é a rota que tem poder real. Ela usaria a onda completa (IMR) com deformação depois do pico, miraria O5 e os detectores de 3ª geração, e faria o teste da largura populacional de δf̂.

## 5. Erros da gerência na ORDEM 013, reconhecidos

- A «média da razão condicional» pedida não é fator de Bayes. A bancada acertou ao usar a identidade correta.
- O teto posto no prior de τ★ (GM_f/c³) fez o limite do relógio livre depender do prior.
- Presumiu-se licença CC BY no Zenodo 17018009, mas ela é MIT.

## Decisões que são do operador (postas ao operador nesse relatório)

1. Os 4 cálculos que ainda rodam (73 de 125 GB de RAM; 5 a 31 h pela frente; pela auditoria não podem mudar nenhum veredito): parar ou deixar terminar?
2. O estado da bancada diz «user requested continuation». O operador autorizou o Codex a seguir além do M1?
3. Escrever e publicar a 013-bis?
4. A ORDEM 014, a da rota com poder real?
5. A partição: qual relógio, se ele é universal e se o modo 440 também se deforma. Depois da C4 ela já não é cega.
