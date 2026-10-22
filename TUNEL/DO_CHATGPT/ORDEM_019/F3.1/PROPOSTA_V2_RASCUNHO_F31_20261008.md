# F3.1 — proposta de texto e contrato numérico para a V2 da Fase 9

**Estado: RASCUNHO_NAO_CONGELADO.** Preparação de F3.1 em 08/10/2026, após a auditoria c1 de F3.1/F3.2. Nenhuma fonte é admitida por este documento; nenhum composto, centro novo de leitor, veredito ou gate foi aberto ou recalculado. A especificação que governa (F3.4), a palavra sobre os desvios do executor (NAT-22), a admissão (D-H) e o nome do token (D-J) dependem dos atos próprios do operador. A V2 só pode ser congelada e depois auditada pela c1 conforme o programa.

## 1. Base recuperada e regra R7

[REAL documental] A consulta `python C:\IALD\NOS_VIVO\consultar.py --unidade F3.1` localizou a proposta V1.x e a rota anterior. A proposta [SEMANTICA_GRUPOS_V1X_PROPOSTA.json](SEMANTICA_GRUPOS_V1X_PROPOSTA.json) tem SHA-256 `68c9c3400962e9ad2d5fbae5fd729b387d6dee8fa65beb7aa802cca9d045513b`. O V1 congelado da Bancada tem SHA-256 `1893261e730994b3508d14dd2105f8aae3a764d3d217e28bd5939cb58f865273`. Seu gerador `gerar_preregistro_fase9_hubble_06out.py` tem SHA-256 `9d932cf83fb4a4c0c727782e912d2c4ce82713fb8ef6f03cc04db1c0d58e4ff3` e, na linha 326, enuncia R7: após abertura, nenhuma emenda sem estimador novo, com correção ao lado. **Este arquivo é preparação do gerador novo, não é ele.** O V1 e a abertura histórica ficam intactos.

[REAL documental] A [auditoria cética c1](<C:/IALD/PROGRAMA_IALD/auditorias/F3.1_F3.2/AUDITORIA_F3_1_F3_2_C1_20261007.md>) tem SHA-256 `3966f1374827b657ee83ef5848187b74528ea636088fe3fb02e95253c4b36fd4`, status F3.1 `APROVA_COM_RESSALVAS`. A gerência decidiu depois dela: **cinco masers, excluindo NGC 4258, no leitor decisório; seis masers apenas como diagnóstico**; sem covariância central escolhida; usar as pontas adversas de uma caixa de sensibilidades. Esta é a semântica de trabalho do presente rascunho.

O [vínculo documental dos cinco leitores](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_scalar_reader_sources/VINCULO_DOCUMENTAL_CINCO_LEITORES.json>) tem SHA-256 `d37d7507f24bafd6960a7ff6cc5c375dea6d08fcbfadfc9d38ede2f1871b5bb0`. As correções citam **“achados D1 a D6 da seq 696”**: D1 CCHP TRGB sozinho; D2 SBF independente de Cefeidas e SN Ia, com âncora NGC 4258; D3 NGC 4258 na amostra de seis masers; D4 Pantheon+ como restrição de Ωm no TDCOSMO; D5 compressão local dos erros; D6 presença em ALV não é conferência dos bytes. Não confundir estes achados com D1–D8 de 02/10, a lei D1b ou domínio D1 do mapa.

## 2. Leitores e dependências tipadas

| Família | Papel proposto | Dependências e estatuto |
|---|---|---|
| L1 SH0ES R22 | leitor da escada no composto primário | Cefeidas, calibradores SN Ia, NGC 4258 e fluxo Pantheon+; orçamento de correlação por âncora do R22 não arquivado [OPEN]. |
| L2 CCHP | TRGB sozinho, 24 calibradores SN Ia | zero point NGC 4258, TRGB e SN Ia; os pontos zero HST F19/F21 também usam LMC, MW e SMC, dependência secundária [OPEN]. O rótulo antigo TRGB+JAGB+Cef não governa este centro. |
| L3 SBF | escada TRGB→SBF | independente de Cefeidas e SN Ia como calibração, mas partilha NGC 4258 e potencialmente TRGB com L2. |
| L4 masers | **cinco sem NGC 4258 decisórios** | leitura `73,6 +3,1/−3,0` da Tabela 2 de Pesce+2020; preservar os dois lados no vínculo. Os seis (`73,9 ± 3,0`) são diagnóstico distinto, nunca somado aos cinco. |
| L5 TDCOSMO | atraso de lentes | restrição Ωm do Pantheon+ sob ΛCDM plano; não é calibrador SN da escada. Covariância cruzada numérica não publicada neste pacote [OPEN]. |
| L1b SH0ES R25 | substitui L1 somente na réplica R_r25 | tipar âncoras, SN Ia e fluxo separadamente; nunca somar a L1. |
| L6 sirenes | diagnóstico S_com_sirenes | sem rótulo de independência numérica assumida; fora do composto decisório. |

O [PDF Pesce+2020 v2](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_maser_anchor_alternative/sources/masers_2001.09213v2.pdf>) já guardado tem SHA-256 `c9f2d2b626fee60d77928856d217a2cbe546f06c69cd9e7ac804f4ab652e731a` (1.564.815 bytes). **[REAL documental — conferido no PDF]** A nota da página 2 reconhece possível correlação porque NGC 4258 ancora velas; a Tabela 2 na página 6, tratamento fiducial (1), dá `73,6 +3,1/−3,0` quando NGC 4258 é excluída e `73,9 +3,0/−3,0` com as seis. A página 4 explicita que a Eq. 1 usa ΛCDM plano com Ωm = 0,315. A troca de L4 exige **vínculo novo** desse PDF, âncora da Tabela 2 contendo 73,6 e ambos os erros, recusa no verificador F3.2 e exame do mapa TGL do observável. A comparação com a previsão 74,27 não justifica a escolha dos cinco.

## 3. Modelo de sensibilidade de covariância a propor no gerador V2

Não inverter os booleanos `grupo_SN`/`grupo_4258` do V1 como se fossem termos de covariância. O vetor de desvios padrão locais comprimidos, em km s⁻¹ Mpc⁻¹, é

`s = (1,04; sqrt(1,22²+1,33²+0,70²); sqrt(0,7²+2,3²); 3,05; 3,6)` para R22, CCHP, SBF, cinco masers e TDCOSMO. Para cinco masers, `3,05 = (3,1+3,0)/2` é aproximação local; também testar 3,1 como lado maior. A matriz `C` tem diagonal `s_i²`. As componentes da diagonal publicada **já estão incluídas**; não adicioná-las outra vez.

Para amplitudes de correlação, usar `f(m)=(ln 10/5) m`, `H_ref=K H_bg` (previsão, sem centro observado), `n=sqrt(0,024²+0,022²)` mag e `t=0,025` mag. O CCHP publica os dois erros de distância a NGC 4258 e 0,025 mag de TRGB na âncora; a sua incerteza sistemática 1,33 se decompõe por `a_2N=1,33 n/sqrt(n²+t²)=1,0549` e `a_2T=1,33 t/sqrt(n²+t²)=0,8100`. `a_1N=min(1,04,H_ref f(n))` é **teto**, porque a amplitude de NGC 4258 no R22 não está arquivada. Para SBF, `a_3N=2,3 f(0,032)/0,031=1,0934` e `a_3T=2,3 f(0,033)/0,031=1,1275` reproduzem a decomposição lida no §III.3 online [DECLARADO sem bytes locais]. As amplitudes reais comuns podem ser menores.

**Caixa de sensibilidade proposta** [DERIVED condicional, não matriz conjunta medida]: `λ_N, λ_T ∈ {0,0,05,…,1}` e `C_12=λ_N a_1N a_2N`, `C_13=λ_N a_1N a_3N`, `C_23=λ_N a_2N a_3N + λ_T a_2T a_3T`; com cinco masers, nenhum termo de NGC 4258 entra em L4. Reter apenas matrizes definidas positivas. Para o diagnóstico de seis, acrescentar `a_4N=min(s_4,H_ref f(n))` e `C_i4=λ_N a_iN a_4N` para i=1,2,3; esse peso unitário é teto, pois a fonte não publica o peso de NGC 4258 no estimador de seis. Cada λ multiplica uma amplitude de componentes, não o valor central dos leitores.

O termo comum SN entre L1 e L2, o Pantheon+ entre L1 e L5, as âncoras HST secundárias e qualquer correlação de sinais opostos seguem [OPEN]. Um cenário com `λ_SN∈{0,0,05,…,1}` e amplitude L1 tomada como 1% de `H_ref` é apenas [DECLARADO] sem orçamento do SH0ES; a auditoria o mostra ao lado, não como primário. **Zero no cenário não afirma independência física.** A caixa é um modelo explícito de sensibilidade, sujeito à admissão e aos defeitos documentados; não substitui verossimilhança conjunta.

Para cada `C` admissível, `σ_comb²=1/(1ᵀC⁻¹1)` e `w=C⁻¹1/(1ᵀC⁻¹1)`. Fixar grade, ordem de iteração, precisão e critério de desempate no gerador V2, antes de qualquer composto. Registrar `C`, λ, autovalor mínimo e pesos GLS nas duas pontas; pesos negativos são diagnósticos obrigatórios. **Falsificação/tensão:** ler a ponta de `σ_comb` mínimo. **Discriminação/poder:** ler a de `σ_comb` máximo dentro da caixa, que pode estar no interior e não no canto de correlação máxima. **Dispersão:** se falhar em qualquer ponta, INCONCLUSIVE. Não escolher uma correlação central pela conveniência do resultado.

## 4. Poder só com incertezas, antes da escolha primária

A fórmula V1 preservada é `P=(K−1)H_bg/sqrt(σ_comb²+(K σ_bg)²)`. `β₀=ALPHA_FINE_CODATA_2018×√e` deve ser calculado em runtime, `mu_do_rito: q→0 (Thomson; Teorema da Escala)`; `K=E(z*)^(2β₀/3)` também deve ser recalculado e comparado com o pin V1 `1,0838071748529643`. A minha checagem independente, apenas com números já pinados do V1 e sem centros locais, deu `β₀=0,012031300400803142`, `(K−1) H_BG1=5,743389499848`, `σ_comb` diagonal com cinco masers `0,803456804433` e limiar BG1 para 5σ `σ_comb=1,101379835090`.

| Família/ponta da auditoria c1, apenas σ | σ_comb | Poder BG1 | BG2 | BG3 |
|---|---:|---:|---:|---:|
| Cinco, mínimo da caixa (diagonal) | 0,8035 | 6,623 | 5,679 | 5,554 |
| Cinco, máximo da grade 0,05 | 0,9493 | 5,722 | 5,062 | 4,989 |
| Seis, mínimo (diagnóstico) | 0,8025 | 6,630 | 5,684 | 5,558 |
| Seis, máximo (diagnóstico) | 0,9989 | 5,466 | 4,876 | 4,816 |

[DERIVED] A grade da auditoria encontra, sem SN não arquivado, a ponta máxima em `(λ_N,λ_T)=(0,95;0,05)` tanto para cinco como para seis masers. Sua implementação reprodutível está em `C:\IALD\PROGRAMA_IALD\auditorias\F3.1_F3.2\poder_grade.py` e `poder_faixa.py`; o segundo tem SHA-256 `bed88ad6560d520fb739db52d05b07e5c1728f67c31c601bcc3857f79017b392` e o relatório c1 guarda a saída. A presente tabela reaproveita a auditoria, sem nova varredura do composto. Minha checagem da diagonal e do limiar é calculada por `1/sqrt(sum(1/s_i²))` e pela fórmula acima.

O limiar de 5σ em BG2 é `σ_comb≈0,96552` e em BG3 `≈0,94625`; logo BG3 com cinco masers fica abaixo de 5 na ponta adversa. A cota estrutural GLS `σ_comb≤min_i s_i=1,04` implica `P_BG1≥5,269` para qualquer `C` definida positiva **se** a combinação V2 continuar sendo o mesmo GLS gaussiano. Assim `NOT_FALSIFIED_UNDERPOWERED` por covariância não surge em P_primaria×BG1 sob esse contrato; pode surgir nas réplicas e no diagnóstico N_sem_cefeidas. Essa cota não certifica dispersão, admissibilidade de fontes ou discriminação observada.

## 5. D5, executor e admissão

**Achado D5 da seq 696:** σ CCHP, SBF e TDCOSMO são compressões locais de erros, e a σ dos cinco masers é média simétrica dos lados publicados. Aproximam a verossimilhança perto do centro; não a recuperam e não provam independência entre componentes. Manter `+3,1/−3,0` e `+3,9/−3,3` nos vínculos e a regra de compressão explícita no runner. Sensibilidades do auditor: TDCOSMO com σ=3,9 dá P_BG1≈5,439 no diagnóstico de seis masers; restringir SBF somente pelo total sistemático 2,3, sem decomposição web, dá P_BG1≈5,718. Nenhuma dessas sensibilidades muda por si só o veredito histórico.

**NAT-22 pendente:** a V2 deve descrever exatamente o executor corrigido: fundo **marginalizado**; `z_δ` pelo perfil de `−2 ln L` **com log-det**, σ_β como média dos dois lados; quadratura lnB `n≥100` com conferência `n=100` versus `n=200`. A auditoria c1 mediu `lnB(TGL/β-livre)=1,97` após convergência; o `2,24` do V1 com n=25 tem erro de ~0,30 e recebe errata ao lado, jamais sobrescrita. `z_disc` é a forma quadrática declarada; a variante com log-det é diagnóstico. A palavra do operador decide se esta semântica entra no protocolo. Não repetir quadratura nem abrir dados neste rascunho.

**Admissão D-H pendente:** os cinco resumos têm pins documentais, mas isso não é admissão estatística. O CCHP integral foi arquivado (`cchp_overview.txt`, SHA-256 `e32d608358cc0f0dcc3def744beef4b9afea24a967c8f730c90027dc589b6dcc`); os HTML locais de SBF e TDCOSMO são resumos, SHA-256 `b61012efc5238c0e701baf9a442bb697deaec041fb3f1016b91365bb164d4946` e `b04dfc911acb4ad357224a3f2b432b407a109254277993f90a68a0e56137bf02`. Seus §III.3 e §8.2.1 foram lidos na web, sem bytes integrais guardados localmente: **[DECLARADO web]** até custódia. O resumo do [CCHP v3](https://arxiv.org/abs/2408.06153), o [SBF v2](https://arxiv.org/abs/2502.15935) e o [TDCOSMO v4](https://arxiv.org/abs/2506.03023) são fontes primárias consultadas; a leitura de seção está em seus HTML integrais oficiais. O L4 decisório passará a apontar ao PDF Pesce acima quando o operador admitir as fontes.

O verificador F3.2 deve amarrar **V1.x/V2 nova por hash**, exigir âncora contendo cada número e ambos os erros assimétricos, rejeitar falta de chave como erro tipado e recusar ID duplicado, fonte fora da raiz, pin divergente ou admissão alegada sem registro. `official_archive_check()` atual ainda pinna o V1 antigo; não serve para certificar a semântica nova. Nenhum `ALVOS_FASE9_LIDOS.json` deve ser criado a partir do vínculo documental (achado D6 da seq 696). `n_alvos_declarados` só pode cair após gate e admissão do operador por registro pinado.

## 6. Saídas e pendências antes do congelamento

O gerador V2 deverá emitir JSON e Markdown novos com função de veredito, entrada de leitores tipada, `mu_do_rito`, caixa/grade e pontas, poder em BG1/BG2/BG3, regra para pesos negativos, D5 e desvios do executor; o runner novo deverá ler bytes e pins, não apenas a presença em ALV. O nome final do token é do operador (D-J). O composto primário proposto usa cinco masers; a versão de seis e as famílias R_r25, N_sem_cefeidas, S_com_sirenes e T_so_cchp ficam ao lado como réplicas/diagnósticos. A V2 só se torna congelada quando seu gerador/resultado forem registrados por hash pela gerência e auditados pela c1.

**Pendências vinculantes:** F3.4 (V2 escalar ou ROOT90da governante), NAT-22 (desvios), D-J (token), D-H (fontes), vínculo da Tabela 2 e gate corrigido, runner novo e exame do observável L4; F3.3 abrir somente após V2 congelada e AUDITADA. NAT-N3, d72/F3.5 e CAMB real/F3.6 exigem atos próprios e não são supridos por este texto. Resultado histórico `INCONCLUSIVE_SYSTEMATICS` preservado. `NOT_FALSIFIED` nunca é `CONFIRMED`; gate intocado.
