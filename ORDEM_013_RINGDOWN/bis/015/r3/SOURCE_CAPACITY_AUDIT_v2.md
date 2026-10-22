[REAL — leitura de fonte C custodiada; DERIVED — condição de índice; OPEN — equivalência com binário e efeito do patch]

Supersedes `SOURCE_CAPACITY_AUDIT.md`, SHA256 `907bb9ef35e771fd02dcbd602e39ea889c9da9c4b47c034a592677fb9f2f7bcb`. Data: 27/09/2026. Esta nota é preparação somente-leitura de R3; o T04-C ainda está em curso. Nenhum build, patch ou uso científico foi feito.

Fontes locais lidas sem edição:

- `bis/e3_pilot_failure_diagnostic/sources/LALSimIMRSpinAlignedEOB.c`, SHA256 `ae813273982c51a8aaa5d3d9ee0f15caa34791a943ef36ee324ceb40131a4b6b`;
- `bis/e3_pilot_failure_diagnostic/sources/LALSimIMREOBHybridRingdown.c`, SHA256 `659aded0ae1d5cdd257713361ac70048caf31c33d0a5179d79d5d72252b4581e`;
- `cache/source_evidence/lal_generator_source_gitlab/LALSimIMRSpinAlignedEOB.c`, SHA256 `6b7969bb7cbe714c4937a691838b0b82a7fcc2a199c03ee2bf5215738f1ce1b3`. Esta última tem proveniência declarada para commit `2c00d8c200308422036d0a23b7c0394f7c73faad`; reprodução byte a byte do binário instalado ainda não demonstrada.

No gerador, a versão 4112 estabelece `TGRflag=1` e `use_hm=1` (linhas 951–959). Com `use_hm`, `modeFreq` recebe a frequência **550** nas linhas 1246–1258. O comprimento dos quatro vetores de alta resolução usa `retLen + ceil(20 max(1,1+dtau220)/(Im omega_550 deltaTHigh))` (linhas 2060–2097). Portanto, a explicação de `ORDEM_015` §2.2 item 6 que identifica o denominador desse buffer com `Im omega_220` está **errada no caminho HM/4112**. A grade empírica de 122 pontos não é invalidada por essa correção; o declive teórico ali atribuído a `2 Im omega_440/Im omega_220` precisa ser recalculado com o denominador efetivo e os índices de anexação medidos.

Na rotina de anexação, `TGRflag=1` dá `Nrdwave = (INT4)(EOB_RD_EFOLDS / Im omega_lm / dt)` (linhas 1261–1267). Para o modo 440, `Im omega_440` já foi dividido por `1+dtau440` (linhas 1079–1082). A escrita percorre `i=0..Nrdwave-1` em `signal1/2->data[i+indAmax]` sem verificação local de capacidade (linhas 1392–1396). Assim, a condição necessária para os vetores de sinais é `indAmax + Nrdwave <= signal.length`, com validação prévia de finitude, positividade, conversões inteiras e overflow. `retLen`, `indAmax` e `Nrdwave` da falha concreta ainda não foram instrumentados; por isso a igualdade exata com o limite observado permanece [OPEN].

O comprimento também dimensiona `hLMAllHi` e a saída posterior (`LALSimIMRSpinAlignedEOB.c` linhas 2428, 3128–3130, 3192–3204, 3631–3634). Uma substituição das alocações por `max_lm(1+dtau_lm)` pode evitar escrita fora do vetor, mas **não está demonstrado que preserve a forma de onda, o suporte temporal ou a likelihood**. A qualificação R3 exige comparação numérica com o binário original onde este é finito, além da grade de 122 pontos, limites explícitos e proveniência de build. O uso científico continua dependente da decisão do operador na ORDEM015.

Conferência independente de texto: [fonte oficial LALSuite 7.26 da rotina de anexação](https://lscsoft.docs.ligo.org/lalsuite/7.26/lalsimulation/_l_a_l_sim_i_m_r_e_o_b_hybrid_ringdown_8c_source.html), linhas C 1071–1082, 1261–1267 e 1392–1396. Essa documentação não prova identidade byte a byte com o binário lalsuite 7.26.15 instalado.
