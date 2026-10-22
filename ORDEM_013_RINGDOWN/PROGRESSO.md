
[REAL — progresso parcial, objetivo integral ativo]

## Rodada 2026-09-21T23:22:04.732264+00:00

A auditoria cobre 24 itens e todas as 38 linhas não vazias exigidas. O módulo recupera os dois ramos V346; a derivação GKSL diferencia taxa de salto, coerência, amplitude e potência. Os modos exatos qnm concordam com Leaver, e quatro curvas PSD foram usadas no forecast, com controles PyCBC/LAL em arquivo separado. O C5_FISHER conserva o retrato anterior em sua lista not_done; os controles foram pagos depois dele e estão em PSD_CONTROLS.json.

No primeiro confronto público (40776 amostras), ramo B: ln B=0.029026162, bootstrap 95% de ln B=[-0.03364357129888176, 0.027358577656555028, 0.09183101867182289]. Desvio previsto mediano em tau=-0.019845285; correção/erro marginal=0.343377. A quadratura tridimensional independente difere por -1.13e-06 em ln B. Isso é comparação do 220 mantendo 440 livre, sob hipótese de amortecimento de ensemble; não é confirmação nem decisão sobre a teoria inteira.

**Ainda falta**

- C0: arquivar fontes primárias consultadas, com hash; não alegar leitura integral dos cinco relatórios de gerência.
- C1: tabela completa de todas as leituras, relógios, partições, unidades, efeitos de distância e exclusões condicionais da v369.
- C2: distribuição dos estimadores em trajetórias com ruído colorido; tratar lei linear/Cauchy e raiz sem impor desenrolamento browniano.
- C3: verificar integração com consumidor de inferência; campo coerente-raiz não é exponencial; optional 221 não implementado.
- C4: R-MOD em grade exata, priors livres de tau, pyRing, catálogo sem duplicação, versão do fit de remanescente, hipóteses 220+440.
- C5: injeção/recuperação N>=50 por célula, viés/cobertura e duas famílias; Fisher com massa/spin livres requer informação adicional.
- C6: registro próprio antes de ler strain na janela; PSD fora da fonte; execução registrada e comparação de tempos.
- C7: pacote independente em inglês, manifesto e reprodução final, apenas após completar a matriz de evidências.

**Falhas e correções preservadas**

- WSL sem elevação retornou E_ACCESSDENIED; acesso científico somente leitura foi autorizado e funcionou.
- Rede sandbox retornou WinError10051; download público autorizado concluiu e checksum confere.
- qnm sem numba falhou; dependências instaladas somente em cache/vendor, /opt preservado.
- Quadratura inicial atingiu limite de subdivisões; resolução aumentada, resultado anterior preservado em backup; novo teste sem aviso.
- Controle PSD inicial recusou zero em Nyquist; a convenção foi explicitada, apenas esse endpoint excluído, interiores validados.

Memória de retomada: STATUS_ORDEM_013.json contém os caminhos, hashes lidos, estados e próxima ação. Nenhum processo permanece rodando nesta gravação; arquivos de resultados não são prova de processo vivo. Nenhum strain da janela do evento foi lido.


[REAL — resultados computacionais condicionais; objetivo integral ATIVO]

## Rodada 2026-09-22T00:19:41.076557+00:00

Controle pyRing: 84701 amostras; ramo B ln B=0.141139410 (pSEOB primário: 0.029026162). Mesmo evento, sem multiplicação das evidências. As três amostras de spin negativo foram mantidas e verificadas por qnm e Leaver. A versão 2.7.0 é do ambiente de figuras; procedência integral do binário/mesclagem é ressalva explícita.

Catálogo já calculado foi consolidado: 33 produtos, seleção literal primária de 31. Conteúdo HPD da RG na combinação primária: 0.983710937; RG fora de 95%, portanto o critério registrado conserva INCONCLUSIVE_SYSTEMATICS. Nem esse conteúdo HPD nem ln B são sigma de descoberta.

Relógio livre integrado com os dois priors previamente registrados, sem tratá-lo como Bayes de ponto. Limites condicionais de 95% (segundos na fonte): uniform: 0.00029209333, log_uniform: 3.34417752e-06. A coordenada de prior permanece quase uniforme; a grande diferença não é evidência de medição precisa. Quadratura independente aprovada em C4_FREE_CLOCK_ORACLE.json.

Trajetórias: 1100 ajustes em 22 células, 50 por célula, 0 falhas de otimizador, 0 contatos com limites. Incluem Wiener, Cauchy e Poisson coerente N=4/64/256. Ruído OU sintético, sem alegação de C5 empírico; o ajuste de uma trajetória não é igual ao ajuste da média de ensemble.

Manifesto de downloads: 70 arquivos com hash recalculado, falhas de obtenção preservadas. Nenhum strain da janela foi lido. Memórias canônicas e um.py não alterados.

**Pendências integrais**

- C0: três downloads de literatura falharam (403/406), registrados; não equiparar resumo/abstract a leitura integral.
- C2/C3: escolhas de desenrolamento continuam hipóteses físicas; portar/explicitar interfaces de Cauchy e soma de Poisson no pacote. O teste atual usa ruído sintético, não off-source.
- C4: hipóteses conjuntas 220+440 e tratamento dos demais modos; comparação de início tardio com pyRing; conferência do GWTC-3 sem duplicar eventos; sensibilidade restante de priors e remanescente.
- C4: procedência da fusão do weighted_posterior e binário original pyRing não reconstruída; 2.7.0 está fixado no ambiente publicado de figuras. Controle secundário fica condicionado a isso.
- C5: PSD fora da fonte, injeções com duas famílias IMR e N>=50 por célula; viés/cobertura sob ruído empírico; completar distribuições de evidência calibradas, além de Fisher.
- C6: entregar registro com hash antes de ler strain na janela; executar rota escolhida validada, incluindo cinco tempos de início e controles.
- C7: pacote independente em inglês, comandos e teste de reprodução integral; só declarar completo após auditoria do objetivo inteiro.


# Ordem 013 — ruído empírico e primeira rodada registrada em strain

UTC: 2026-09-22T01:07:35.184955+00:00

[REAL — análises computacionais condicionais; objetivo integral ATIVO]

A C6 foi executada após o registro verificável no túnel. Foram lidos os arquivos públicos H1/L1 do evento, preservando as janelas e os três priors de amplitude registrados. Massa e spin foram integrados com priors próprios uniformes, sem usar o posterior do mesmo evento como prior.

Registro C6: `ded00f09b5010d622b67b4ea4e559a216818f578440a0f60772130174ececf14`. O erro máximo entre grades nos log-fatores de Bayes foi 4.96819297e-06.

| Leitura | ln B na janela primária 10 tM |
|---|---:|
| R-GLOBAL | 0.000000000 |
| R-B | -0.002595070 |
| R-RAIZ-0 | -0.043068118 |
| R-LIN | -0.090862677 |
| R-MOD | -0.251294964 |

Esses números são razões condicionadas ao modelo 220+440 com amplitudes por detector. Todas as janelas recebem INCONCLUSIVE_SYSTEMATICS por regra registrada: os controles com duas famílias IMR não passaram o critério completo de viés/cobertura. Não há sigma de descoberta nem exclusão física.

A integral analítica das amplitudes foi conferida por covariância gaussiana independente e quadratura numérica. O ruído simulado diretamente no domínio de Fourier reproduziu a covariância projetada. Ruído real: 256 intervalos por detector; flutuações dos filtros entre 0,94 e 1,07 da escala prevista. Foram preservadas três tentativas numericamente instáveis antes da seleção de amostras e projeção estável.

C5: 480 células × 50 avaliações pareadas, cinco tempos, três SNRs, oito leituras e duas famílias (SEOBNRv4HM e IMRPhenomXPHM). Contagem: {'UNIDENTIFIABLE_AT_NUMERICAL_AND_OBSERVATIONAL_PRECISION': 240, 'INCONCLUSIVE_SYSTEMATICS': 240}. O mesmo ruído é reutilizado entre hipóteses para controle; não somar como eventos independentes.

A comparação com oito posteriores Kerr publicados em 6, 8, 10 e 12 tM foi realizada. Há diferenças de modos, priors, processamento e referência de tempo (0,0001095 s), explicitadas no JSON. Não existe posterior de 10,5 tM no índice inspecionado. Não foi declarada reprodução da análise pyRing.

A análise conjunta anterior 220+440 permanece em C4_JOINT_MODES.json; não foi multiplicada por esta nova análise do mesmo evento. O consumidor Bilby e a extensão angular multimodo passaram controles independentes com LAL.

**O que falta no objetivo integral**

- C0: três fontes integrais continuam com falhas 403/406 documentadas; não anunciar leitura integral.
- C2/C3: finalizar interfaces reutilizáveis de Cauchy e Poisson coerente no pacote; escolha física de desenrolamento e partição continuam hipóteses explícitas.
- C4: conferir release GWTC-3 sem duplicar eventos; procedência integral da fusão de posteriores/binário pyRing permanece ressalva. A comparação de quatro tempos foi realizada; 10,5M não existe no índice do release.
- C5: completar injeções com outras PSDs (O5/ET/CE) por recoloração validada; medir distribuição calibrada de evidência, não apenas Fisher.
- C5/C6: modelo fundamental 220+440 falhou no critério de viés/cobertura para duas famílias IMR; localizar e tratar a discrepância de modos/overtones e de priors. Qualquer novo acesso orientado pelo resultado exige adendo NÃO-CEGO, preservando o registro C6 e seus resultados.
- C6: a rodada registrada em H1/L1 foi executada em cinco inícios e três priors, com massa/spin marginalizados e convergência. Ainda não é uma verossimilhança coerente completa nem uma réplica pyRing; não promover INCONCLUSIVE_SYSTEMATICS a exclusão.
- C7: concluir pacote independente em inglês, tabela de escopos, comandos e teste de reprodução; auditar objetivo integral antes de marcar completo.

**Artefatos e hashes medidos**

- `C4_JOINT_MODES.json` — `8b2e0fea734caed23f05c3a9f9a2f3f7aaa8f19ed71d2f9d9a841129739e742f`
- `C3_MULTIMODE_TEMPLATE.json` — `20ada0cc440388aa636cd78e40a1330433137d7fd5bd7d10ce689a40f40bd7f1`
- `C3_BILBY_CONSUMER.json` — `993b705cebf2cc3449fc473ab9cac185d58096e8a6a8f26bc1a2d01280821aad`
- `C2_TEMPLATE_CHECKS.json` — `b43fa517a37f9b41b8aa2d4f699571a4e24c7da5f6027266e55a86b6ffbe579a`
- `C5_EMPIRICAL_NOISE.json` — `a748e279a04f08e0218bcda347ff9d2750068e53b2cefed35a6b36935199e3ef`
- `C5_IMR_CONTROLS.json` — `1fe989525c3c9cff7059caa748eea541f94d01f9d416840117072c1f094fe2c1`
- `C5_EMPIRICAL_IMR.json` — `f5ea9f58ec31b75079b20caf9a891e26bea2dfb7414ae1035e65278b2a7a34fc`
- `C5_EMPIRICAL_IMR_STARTS.json` — `220117a57b178018de94ae212a7a8f2afaceff07585ea30ad3b394336ed0c145`
- `C5_LIKELIHOOD_VALIDATION.json` — `49f36dc63a2193a92e7f0be66395c9d802e4b1ab5c88f346d046665c288ebfaf`
- `C5_FISHER_EMPIRICAL.json` — `00fbe67f5aa5b38212e8b6c4e6654d09e6cbc23b9e0e5306ee3d7cb77a3bc508`
- `C6_RESULTS.json` — `781a3741a68875eba0fcef02d596dab7d36103d9e926edc6bec18fb485a055e8`
- `REGISTRO_C6.json` — `ded00f09b5010d622b67b4ea4e559a216818f578440a0f60772130174ececf14`
- `C6_DOWNLOADS.json` — `188ecebffcdeabc819b5f3e852da5d2670a95475299d6177bf479f54d86483aa`
- `C6_PYRING_START_COMPARISON.json` — `59dfef3554288c6117debec7827a8b7cd56c6422ff3710a8a39deb4470645a18`
- `C6_SYNTHETIC_GRID_0.json` — `467d3c3fc2663a034ecc2ed399956b7ef9009c43da7562a54453597a7a71591b`
- `C6_SYNTHETIC_GRID_1.json` — `0ec71b78873dcbed1326db580dcb6c5a04fee5c74302357031c370c511ae1909`
- `tgl_ringdown_prediction.py` — `fd0fc446e1c732f3d782210c6effa7cb7faeaeb7a51a434d4f397f1da89bd652`
- `tgl_ringdown_template.py` — `16d7fbc25e94b0351e7050aa5055db421365953782cec1a668d68f11e5cc5132`
- `tgl_ringdown_likelihood.py` — `f16517e62fca96cc348aac17369e75e1fb9b07f1e95fef06f7630c8b94153bca`
- `prepare_empirical_noise.py` — `5683b5324c2d099060a1b236b6babd2c35be31e9a3a168f64740742bde7cdffd`
- `prepare_imr_controls.py` — `5139864946af88ee0f4f3c52f85edba0acd690ab1249489068bb4677004f3e19`
- `empirical_imr_recovery.py` — `b4ea2d0e2326b229aa1b3913f65aeb16b5bcd3892bd489e61dd99bab8a6a071f`
- `verify_likelihood_and_noise.py` — `f91100fecaa2e6842042760ad2103de951ec800f3804888d21185b77763ae8d2`
- `c6_engine.py` — `94c724c4cb1764b7a62209da08c37a40d7936c98b344da714d1bd7733352de3c`
- `run_c6_grid.py` — `d3aa76afdc419ff3ac73321fc11bb405ae762cd0d219411be16affe8c7f347c1`
- `cache/MANIFESTO_DOWNLOADS.json` — `727ff51684585428840915d8460f21236f307656d32351031b4c5ba1b1c34b3c`

Manifesto atualizado: 92 arquivos de aquisição/derivação conferidos. Não foram alterados um.py, kernel, Atlas ou memórias canônicas; a gerência recebe esta entrega para incorporação.


---

[REAL — medições e reprodução; DERIVED/INPUT/CONJECTURE nos modelos; não confirmação física]

# Ordem 013 — distribuição de evidência, interfaces e pacote independente

Data UTC: 2026-09-22T01:45:36.344883+00:00. Axiomas: N/A — sem Lean. Nenhuma edição do um.py, do kernel,
de memórias canônicas ou do gate. Registro C6 conferido: `ded00f09b5010d622b67b4ea4e559a216818f578440a0f60772130174ececf14`.

## O que mudou

- **PAGO — diagnóstico da discrepância:** a falha já existe no harmônico 22 isolado.
  Overtones reduzem o resíduo, mas amplitudes livres absorvem informação sobre a.
  No ruído O4 medido, SNR40, família SEOB: resíduo² 41,6301 com 220+440, 0,12646
  com quatro modos e 0,001435 com oito; poder Fisher local otimista cai de 0,4039
  para 0,1346 e 0,0430. São controles em SNR fixo, não eventos diferentes.
- **PAGO — recoloração validada:** quatro curvas O4/O5/ET/CE, 256 resíduos disponíveis
  por detector; primeiras 50 janelas em cada célula. Projeção polinomial no intervalo,
  convenção Cholesky explícita e controles independentes de ruído Gaussiano.
  Continuação abaixo da tabela por f^(-4), controles f^(-2)/f^(-6); sensibilidade
  máxima do norm do filtro de aproximadamente 1,31%. Não são observações futuras.
- **PAGO — matriz C5:** 4608 células, duas famílias, oito leituras,
  três modelos, seis SNRs e a=0/1; controles FULL_IMR e MATCHED_RINGDOWN separados.
  Contagens globais: `{'UNIDENTIFIABLE_AT_NUMERICAL_AND_OBSERVATIONAL_PRECISION': 2304, 'INCONCLUSIVE_SYSTEMATICS': 1780, 'CALIBRATED_CONDITIONAL_CELL': 524}`; FULL_IMR: `{'UNIDENTIFIABLE_AT_NUMERICAL_AND_OBSERVATIONAL_PRECISION': 1152, 'INCONCLUSIVE_SYSTEMATICS': 1052, 'CALIBRATED_CONDITIONAL_CELL': 100}`.
  **Nenhum grupo passou simultaneamente nas duas famílias e nas duas injeções.**
  As 100 células FULL_IMR aprovadas isoladamente não permitem escolher a posteriori
  uma família favorável. Matriz completa e amostras preservadas.
- **PAGO — oráculo independente:** 96 células conferidas por SVD, maior diferença
  em ln B `1.30967e-09`;
  refinamento contínuo do MLE mudou no máximo
  `2.56241e-05`.
- **PAGO — interfaces C3:** Cauchy de fase e Poisson coerente finito reutilizáveis,
  com sementes, controles de cauda, recusa de N macroscópico como soma exata,
  oráculo de matriz densidade N=4/64/256 e três consumidores Bilby reais.
  Template antigo e C6 congelado preservados.
- **PAGO — recusa adversarial C6:** cópias com registro, código ou QNM adulterados
  são recusadas; cópias íntegras passam. Nenhuma janela real lida neste teste.
- **PAGO — pacote independente v1:** 8715214 bytes no ZIP, 54
  membros. Manifesto e demo NumPy passaram numa extração limpa no Windows.
  A reprodução em nova pasta WSL recalculou todas as cinco janelas a partir do
  strain público, sem saídas existentes: 75 linhas, diferença máxima em ln B
  `0.0`.
- **NÃO PAGO — automação portátil de todo o acervo:** v1 inclui interfaces,
  evidências e reprodução C6; a regeneração completa de posteriores/injeções e a
  comparação separada GWTC-3 continuam por fazer. Objetivo continua ativo.

## Exemplo O5/A+ — ramo B, SNR40, família SEOBNRv4HM

| modelo de recuperação | a injetado | média ln B | dispersão ln B | viés absoluto | cobertura90 | intervalos na borda |
|---|---:|---:|---:|---:|---:|---:|
| 220_440 | 0 | -0.131420 | 0.427068 | 1.9028 | 0.68 | 11 |
| 220_440 | 1 | 0.015430 | 0.426759 | 1.8516 | 0.72 | 8 |
| 220_221_222_440 | 0 | 0.424963 | 0.176966 | 1.7495 | 0.88 | 27 |
| 220_221_222_440 | 1 | 0.448675 | 0.172582 | 1.4948 | 0.88 | 31 |
| eight_modes | 0 | 0.850875 | 0.107350 | 2.6171 | 0.86 | 49 |
| eight_modes | 1 | 0.855725 | 0.105602 | 3.6500 | 0.86 | 49 |

O modelo com oito modos tem ln B médio ~0,851 mesmo no **ruído sem sinal**.
O pequeno favorecimento não distingue a=0 de a=1: o volume do prior de amplitudes
explica o deslocamento. Não converter isso em sigma, nem chamar de dephasing.
As distribuições das mesmas 50 janelas são pareadas; não são milhares de eventos.
A figura `C5_O5_DISTRIBUTIONS.png` foi renderizada e inspecionada.

## Pacote e reprodução

[README em inglês](../../ORDEM_013_RINGDOWN/C7_INDEPENDENT/README.md)
· [ZIP verificado](../../ORDEM_013_RINGDOWN/cache/TGL_RINGDOWN_INDEPENDENT_v1.zip)
· [validação do pacote](../../ORDEM_013_RINGDOWN/C7_PACKAGE_VALIDATION.json).

```sh
python -m pip install -r requirements-minimal.txt
python verify_manifest.py
python run_demo.py --output
python -m pip install -r requirements-reproduction.txt
python reproduce_c6.py --run --download
```

Para refazer a nova bancada no ambiente científico local, scripts principais:
`prepare_recolored_noise.py`, `forecast_recolored_imr.py`,
`verify_recolored_forecast.py`, `verify_unravelings.py`.
Os geradores recusam sobrescrever caches; usar cópia nova para repetir.
O pacote inclui tabela de 264 combinações evento/leitura, 33 eventos únicos.
Não combina múltiplas análises de GW250114 como observações independentes.

## Ficha de aproveitamento

Reutilizados: v369 congelada (não executada), `QNM_GRID.json`, dois IMRs já
construídos, 256 janelas fora da fonte por detector, `linear_statistics`,
`mode_basis` e registro/engine C6. Novos artefatos têm consumidores: ruído
recolorido → matriz → oráculo/figura; interfaces → Bilby/demo; engine congelado
→ reprodução independente. Nenhuma função adicionada ao programa canônico.
Não há nova execução do evento orientada pela escolha de modelos extras.

## Próximos itens e limites

- C0: três tentativas de leitura integral da literatura falharam (403/406); resolver por fontes primárias alternativas ou manter explicitamente a limitação na auditoria final.
- C4: conferir o release GWTC-3 e reconciliar eventos sem contagem dupla; a versão integral da inferência/fusão pyRing segue limitada ao que o release documenta.
- C5/C6: discrepância de modos e volume de prior agora medidos. Nenhum grupo PSD/modelo/leitura/SNR passou nas duas famílias e nas duas injeções simultaneamente. Não promover células isoladas ou maior SNR a calibração universal. Qualquer modelo novo para o strain exige adendo NÃO-CEGO, mantendo C6 intacto.
- C7: v1 independente entregue e C6 reproduzido a partir do strain; completar automação de regeneração dos posteriores/injeções e auditoria de cobertura do objetivo integral.
- Limite físico explícito: a seleção da partição, relógio, quantização/excitação e desenrolamento não foi determinada pelos dados. Não inventar uma escolha para encerrar o objetivo.

Falhas anteriores preservadas. Esta entrega não apaga os diagnósticos de matriz
de covariância ou do modelo fundamental. O viés/cobertura negativo é resultado;
não se exige obter um número favorável para concluir uma medição honesta.

## Custódia lida nesta rodada

| arquivo | SHA-256 |
|---|---|
| `C5_BIAS_ABLATION.json` | `6fd926f371e38aa7fec9c0782e48230dc169087086ea3d0a76a309e14a5ea54f` |
| `C5_EXTRA_QNMS.json` | `be9f839dcb69814baca963f97c997dae259aa2a7bf2e83de004228869f9d1297` |
| `C5_OVERTONE_ABLATION.json` | `21b28ee843422f68d1c63a12f1d74736807f8d0bc99b424fb5ae5d92897ea8bd` |
| `C5_RECOLORED_NOISE.json` | `088fe6927b17e8461df6a05c0d129da28654cf001e3833df24713cfe0d3ec477` |
| `C5_RECOLORED_FORECAST.json` | `0825d9e83c57155496b552cb8e806c2245cc1f66dc86c27b4e68b3a551011a0c` |
| `C5_RECOLORED_VALIDATION.json` | `cd4e58c2aecb3e374a3fdfcf5dd8877591db07e42a1b13e021cd1e7c18ce58a2` |
| `C3_UNRAVELING_API.json` | `e280b73ccbdeece3ee051e2ffa32fd963e85ff81717a9df8881a04f5f5c6ed24` |
| `C6_GUARD_TEST.json` | `46aa5d66b7db186b19c4148149b6ebe9a3ec8ffeb75c78530641a1fbc46a5c4e` |
| `C7_PACKAGE_VALIDATION.json` | `9b333c7859c1c5b9ea60076e84fc173c88b7cbe96c6cdff50bf0a307511989c1` |
| `tgl_ringdown_unravelings.py` | `2858efdbf0e1f8ba2b8419e9f2a987c340ae02e2e5825495f0d3381b2d26e830` |
| `prepare_recolored_noise.py` | `c7a454a4faaa110ecd9cad3b2210736e779458a22577e62f655c31d740c9da06` |
| `forecast_recolored_imr.py` | `02e09d1f8b29217b60ee8b72ef1b94e9fe3a2adba92972f8d6cfe2d9a6cabc6e` |
| `verify_recolored_forecast.py` | `72454a50c6583cfa2e7ece7282f558ac4486b21b52e19c4bdbbc8d2520f2ca21` |
| `verify_unravelings.py` | `e696a6f768dd9a4eae1c09a7d6d9ff7664ccf531b44d8d9c69c5dbe5b5f0a965` |
| `verify_c6_guard.py` | `ca700bf9440d24c919605fa25aeb9730c613ae0524959b82d0857cd19b7fd790` |
| `build_independent_package.py` | `a0cb6e21326128e39a7af3ea0cc389053aafff8067f9afe089a7e677255a39d5` |
| `package_demo.py` | `63d299e5be9bd659f5c140c4a8216f04b10ecd930e7858a8274b67cd12e09c2b` |
| `package_reproduce_c6.py` | `916b812ed3b359c42a5929ca7355083ed8229fc563b715ac8b7827753204cc72` |
| `verify_package_release.py` | `ca1dcbdccc7b411ff51887fceb4c2de064f8943fdcd92a1582b5df9617b58c30` |
| `C5_O5_DISTRIBUTIONS.png` | `1ef68ce754e696a56fbb6d1bd7725941830d56bac2ba6ad16b118fd25cc767bc` |
| `C5_O5_DISTRIBUTIONS.svg` | `ee83deca11b6983daebefc5cd6daaf802d64fb3681a202a1fe66e63474c80f0b` |
| `C7_INDEPENDENT/MANIFEST.json` | `29d36d2e921344ee2a2d3ea69f95c962b538c5f042b7c70a16942414f096279c` |
| `C7_INDEPENDENT/README.md` | `4b8f73158cae5c7231725ec2d4c8dd12a62db3720e26b4b189d3ae898468272b` |
| `C7_INDEPENDENT/C6_REPRODUCTION_RESULT.json` | `0ed044f5db8d47cc845fc2de0b78da9e70250f6f4cfcbe3a1ac282b32b2e61a4` |
| `cache/TGL_RINGDOWN_INDEPENDENT_v1.zip` | `c03563c8ecc1b0efb76ffa20ea3a1615e2e12965058121204dac4e166d2ed436` |
| `cache/MANIFESTO_DOWNLOADS.json` | `4f21bedd862f7a1a3deddbc2da663af1857f8ce196db5059d93577875248bf5f` |


[REAL — medido e conferido; predições condicionais DERIVED/INPUT/CONJECTURE; NÃO-CEGO]

# Ordem 013 — GWTC-3 e reprodução dos posteriores/injeções

Data UTC: 2026-09-22T02:37:52.756708+00:00. Axiomas: N/A — sem Lean.

## Critérios e resultados

- **PAGO:** 18 HDF5 pSEOB220, 844880 amostras; ZIP conferido contra MD5 oficial e SHA medido. Convenções de prior e amortecimento documentadas com fontes versionadas.
- **PAGO:** 12 sobreposições com o catálogo corrente e seis produtos antigos adicionais. A união nominal tem 39 eventos; nenhuma evidência foi multiplicada entre releases.
- **PAGO:** seleção primária recuperada da Tabela 13 e das duas exclusões explícitas: dez eventos. O controle de todos os 18 arquivos permanece separado.
- **PAGO:** cinco reproduções em pastas novas, desde os posteriores ou ruído bruto; 88563 campos numéricos coincidem, sem diferença nos campos conferidos. Isso conta campos, não medições independentes. Manifestos, arquivos e resultados recalculados foram reconferidos nesta rodada.
- **PAGO:** integridade do registro C6 e de todos os seus insumos. Nenhuma nova leitura do strain nesta entrega.
- **NÃO PAGO:** empacotar o acréscimo GWTC-3 e terminar a auditoria integral C0-C7. Objetivo ativo.

## Seleção publicada do GWTC-3

| leitura | ln B condicional contra RG | veredito |
|---|---:|---|
| R-A | 0 | INCONCLUSIVE_SYSTEMATICS |
| R-B | -0.82083377 | INCONCLUSIVE_SYSTEMATICS |
| R-RAIZ-0 | -1.5687495 | INCONCLUSIVE_SYSTEMATICS |
| R-RAIZ-EP4 | 0 | INCONCLUSIVE_SYSTEMATICS |
| R-RAIZ-REST | 0 | INCONCLUSIVE_SYSTEMATICS |
| R-LIN | -3.3906752 | INCONCLUSIVE_SYSTEMATICS |
| R-MOD | -1.4915603 | INCONCLUSIVE_SYSTEMATICS |
| R-GLOBAL | 0 | INCONCLUSIVE_SYSTEMATICS |

Controle central: 8192 pontos, ESS=2357.48; conteúdo HPD no ponto RG=0.969096. As quatro verificações deixam RG fora de 95%. A regra relativa impede exclusão da TGL com esse diagnóstico. A incerteza Monte Carlo não cobre viés de KDE ou sistemáticas; não convertê-la em sigma.

A soma do controle de 18 tem pouco suporte local em dois produtos e não reproduz a seleção do artigo. As razões são do setor 220 sob priors uniformes condicionais; não representam uma teoria TGL completa. Versões originais do binário/fits não recuperadas.

Seleção conferida em [LVK, VIII.1.2 e Tabela 13](https://arxiv.org/html/2112.06861v3#S8.SS1.SSS2), com leitura do Apêndice A.3. Não se declara leitura integral nem se substituem amostras por números do artigo.

## Reprodução e entrega

Na bancada: `python -B gwtc3_posterior_readout.py`, `python -B read_gwtc3_selection.py`, `python -B combine_gwtc3.py`. Os dois últimos recusam sobrescrita; repetir em pasta nova com os insumos relativos. O backup ALL18_ONLY preserva o gerador do controle anterior.

Os suplementos já testados estão em `cache/C7_POSTERIOR_REPRODUCTION_v1.zip` e `cache/C7_INJECTION_REPRODUCTION_v1.zip`. Cada um contém README em inglês, manifesto, scripts e recibos. No primeiro: `python reproduce.py primary|joint|free_clock|catalog --source-root /path/to/ORDEM_013_RINGDOWN` (escolher um estágio). No segundo: `python reproduce.py full --source-root /path/to/ORDEM_013_RINGDOWN --imr-python /path/to/pycbc/python`.

`--download` é a alternativa pública documentada; essa via de rede não foi novamente exercitada na reprodução local. Samplers LVK não foram rerodados. Tabela adicional: `C7_GWTC3_EVENT_READINGS.csv`, 144 linhas, com indicação da seleção publicada e de sobreposição.

## Memória, limites e aproveitamento

A automação de posteriores/injeções já foi entregue e não deve ser refeita. O adendo C0 corrige o rótulo antigo de três leituras integrais falhadas. STATUS e PROGRESSO recebem backups byte a byte; nenhuma memória canônica ou programa de outra casa foi alterado.

Reutilizados ratio_pair, local_support, weighted_quantile, registro C4 e grade QNM. Acrescentados os posteriores antigos e sua seleção documental. Nenhuma função nova no um.py. Falhas de URL, codificação e patch ficam no STATUS; não viraram dados científicos.

A calibração de duas famílias continua negativa. A partição, relógio e desenrolamento físico não foram escolhidos. O objetivo não exige números favoráveis, nem permite transformar NOT_EXCLUDED em confirmação.

## Custódia medida

| arquivo | SHA-256 |
|---|---|
| `C0_ADENDO_ESCOPO_LITERATURA.md` | `15ff3b8fd2e82484f0fe2e1bdd4d916cb859ad8ffadbef714cac660373341775` |
| `C4_GWTC3_220.json` | `d9dc9b09a8d91dc7f85c5e849091db619b1c22a633b09c97d82bcf434e9c6053` |
| `C4_GWTC3_SCHEMA.json` | `59570d2dd11e6077198dffb39f9d8addcc06945c07f88c822905bebbaa7b7a7e` |
| `C4_GWTC3_COMBINATION.json` | `f88c2aa84f98891734f6dc67229a97777bd201ffca40bc479c86bc2fd4fd1f4e` |
| `C4_GWTC3_PUBLISHED_COMBINATION.json` | `f6dbd853223b803984d352aebe3fd64f786b3f26458988cbb4b37a752f8b1ddd` |
| `C4_GWTC3_SELECTION.json` | `ef18f3b0495d58bffc5f968f86ca860eefd3becb570cd75bfc9f88fa8fee5dd3` |
| `C4_GWTC3_CONVENTIONS.json` | `01205e018dc407304194cc18d04b9d9ad42b3b01cc42659b7c8cbd950770bfe1` |
| `C4_GWTC3_SOURCE_DOCS.json` | `134de77ce9a820455d50de9c73ec5c95e48b04fd816bbb3690502e4468ae0c0a` |
| `C4_GWTC3_PAPER_RECEIPT.json` | `a3087776d05a48cb166f649593686a7e6cb876484abf91ceda724e886fbe29dd` |
| `gwtc3_posterior_readout.py` | `f1e876b1d41a318030613d3c09ef9e882103d2ff2d98dbc12151987694abfe6b` |
| `combine_gwtc3.py` | `b1f13be86cba773e58801a846f0fd3c1aa080f3ece5de0f0886581d22d0c6db1` |
| `combine_gwtc3.py.bak_ALL18_ONLY` | `4181b278a4fa27cd2e6d0d9b9697c08dd7563a90984b54ab570174eae03f77c6` |
| `read_gwtc3_selection.py` | `139cdcbedb2dfe2f14423a060b84b55f2da5acf91aee44562ec3298446dd6d7f` |
| `record_gwtc3_conventions.py` | `16997d65eaf6bde312fff79a9eef706cc3ba227608296165cedada0a34c01816` |
| `C7_GWTC3_EVENT_READINGS.csv` | `d48eca4106876c068e1bf01acb0be7d112e9303436b77f6d8597c54a90b1dddb` |
| `C7_SUPPLEMENTS_VALIDATION.json` | `da1b54fcd7e40dc76b3218f11acfdd6942315beb52077484adcea655e3a92f17` |
| `cache/C7_POSTERIOR_REPRODUCTION_v1.zip` | `194a0a02b703d6ae49723d435a06fd73144bc1b9a138dbcb604c8cc3fbb8eecc` |
| `cache/C7_INJECTION_REPRODUCTION_v1.zip` | `0e94898309569440f3aab339f3c2b1c2e1eac41a96ace904bb5d7d23c05a4492` |
| `cache/MANIFESTO_DOWNLOADS.json` | `f3e8103571721e6712b68ab99013a97d6baba396e8b11535469e9e915febe495` |


[REAL — reprodução e custódia verificadas; predições DERIVED/INPUT/CONJECTURE; interpretação NÃO-CEGA]

# Ordem 013 — pacote unificado e auditoria de cobertura

UTC: 2026-09-22T03:00:40.904623+00:00. Axiomas: N/A — sem Lean novo.

## Critérios pagos

- **PAGO:** GWTC-3 recalculado em pasta limpa, com nova extração dos 18 HDF5 do ZIP público já conferido. 6598 campos numéricos coincidiram exatamente; identidades, seleção e vereditos também. A seleção de dez eventos foi novamente extraída da Tabela 13 e das exclusões do artigo.
- **PAGO:** oito controles adversariais recusaram arquivo adulterado, caminhos inválidos, identidade, veredito, contagem e medida alterados.
- **PAGO:** quatro pacotes prévios reunidos em `cache/TGL_RINGDOWN_DELIVERY_v1.zip` (10583656 bytes; 183 entradas). Extração nova validou 182 arquivos do manifesto. Os bytes das entregas anteriores foram preservados.
- **PAGO:** `C7_DELIVERY_OVERVIEW.md`, resumo científico em inglês com as quatro respostas, taxas por leitura, exemplo de distribuição de ln B, dados reais, comandos de reprodução e limitações.
- **PAGO:** `C7_REQUIREMENTS_AUDIT.json/.md`, inspeção de 14 grupos de requisitos e 51 artefatos com hashes. Separação explícita entre cálculo concluído e critério científico reprovado.

## Critérios não pagos e escopo

- **NÃO PAGO — aceitação científica C5:** nenhum grupo FULL_IMR testado passa conjuntamente os critérios de viés/cobertura nas duas famílias e nas duas amplitudes injetadas. Não é consertado por escolher só células favoráveis.
- **PARCIAL — comparação externa C6:** oito posteriores pyRing comparados, mas não reprodução idêntica de modelos/priors; não há produto 10,5 tM no release inspecionado. O próprio C6 foi integralmente reproduzido.
- **ABERTO por escopo:** identificação física de partição, relógio e desenrolamento; a bancada não fez essa escolha. A realização finita condicional não demonstra um estado global de Kerr.
- **PENDENTE de revisão final:** conferir cada exigência granular contra a matriz consolidada, especialmente colunas C1 e alcance de validação externa. O objetivo permanece ativo; não se declara integralmente concluído.

## Resultado que pode ser comunicado

No ramo B, no GW250114 de referência: Gamma ≈ 4,95 s⁻¹, Gamma/omega ≈ 0,00316 e delta_tau ≈ −0,01985, sob o relógio de massa assumido. A medida primária de strain dá ln B ≈ −0,002595. Os catálogos corrente e GWTC-3 dão −1,80828 e −0,820834 em seus respectivos recortes. Não multiplicar esses resultados: há dados sobrepostos. Os vereditos continuam INCONCLUSIVE_SYSTEMATICS; nenhum desses números é sigma.

## Reprodução

Descompactar `TGL_RINGDOWN_DELIVERY_v1.zip`, ler `README.md` e executar `python verify_delivery.py`. Cada uma das quatro subpastas tem manifesto e instruções próprias. Para o GWTC-3: `python reproduce.py full --archive-cache /path/to/public` ou `--download`; o teste desta rodada usou o ZIP local verificado, não repetiu a transferência.

## Aproveitamento e memória

Reaproveitados os três scripts científicos GWTC-3 sem alteração. Acrescentados um leitor de ZIP com hash/CRC, comparação exata de identidades e empacotamento. Nenhuma função nova em um.py, nenhuma fonte canônica modificada. O registro C6 e seus insumos continuam íntegros. STATUS, PROGRESSO e manifesto local recebem backups imediatos byte a byte.
Notas antigas de pendência foram corrigidas por adendo e índice: a recuperação de trajetórias, os posteriores, as injeções, o strain e o GWTC-3 já têm execução e reprodução. Não é necessário refazê-los. Falhas de acesso WSL, codificação de saída e tabela Markdown estão preservadas no STATUS; não alteraram resultados científicos.

## Custódia medida

| Artefato | SHA-256 |
|---|---|
| `package_reproduce_gwtc3.py` | `710624fc1fee81ec462ea0e7ae95db6f33fe391caf1e7bf6a23c9b5712a14bf6` |
| `build_gwtc3_reproduction.py` | `b4ad14233f9cf912bc92317765f3d62d06b542d4a0d3a337d3e3ab04f771ea18` |
| `verify_gwtc3_reproduction.py` | `5910ad8cb99ab56766d3daa4622603abf78e9bfba57b50f79f862237756a987e` |
| `C7_GWTC3_REPRODUCTION/MANIFEST.json` | `77f9f8883837fcc34899f962991560a92b19e9a9e1fefa9804f7c1f9eada99b5` |
| `C7_GWTC3_REPRODUCTION_VALIDATION.json` | `900df79b4aa68bd80cb0b555d823c739e3beb726de2aa844dbf0deb0c0f8299e` |
| `cache/C7_GWTC3_REPRODUCTION_v1.zip` | `8b0c8fcffa7ce36616c7dab39b963c1f343c9e770c620471f0ddc46aabe70407` |
| `build_delivery_audit.py` | `3d75364fce3a7cbe40280a7cec95035639da1794ebb2812ca037bec1f1833a62` |
| `C7_REQUIREMENTS_AUDIT.json` | `f84ac921fad188b21ae0c8a9b65b4295740196d9341efaf04b5d42e93071b591` |
| `C7_REQUIREMENTS_AUDIT.md` | `9646a2f0bbd25dac918e9962d692708db32c7b279633635003dbbe2d6ce078e8` |
| `C7_DELIVERY_OVERVIEW.md` | `218a3de59715c9b1c610a1fd6e59143fe347eaf088cac5b3b1cfbc5ae7f48066` |
| `build_delivery_bundle.py` | `0c66c23cc304edbe266bc1e8193d53be1f892a0ada76e606faf498e9e76f5ae4` |
| `C7_DELIVERY_BUNDLE_VALIDATION.json` | `f557751d3f9a82bce3f70eeab551771aa9849e71f3b79035ee0dae3bed53952b` |
| `cache/TGL_RINGDOWN_DELIVERY_v1.zip` | `45c561e1bde379d577b55abc7684b5fdce33ab1008d6b1eba1e092f147eb4cf0` |
| `cache/MANIFESTO_DOWNLOADS.json` | `de12d0611043dfd2d0d6d9db1bbedf3d8e2cd54c23bdb10e466b60ec5efc80d0` |


[REAL — controle de implementação e custódia; DERIVED/INPUT/CONJECTURE nas leituras físicas; NÃO-CEGO]

# Ordem 013 — C1 completa e oráculo original do pyRing

UTC: 2026-09-22T03:28:09.205354+00:00. Axiomas: N/A — sem Lean novo.

## Critérios, um a um

- **PAGO — C1 documental:** dez leituras, nove âncoras, dezoito linhas numéricas e dez verificações de unidade. `C1_LEITURAS.json/.md` reúne operador, relógio/estatuto, FP-5, fonte/novidade, universalidade e dependência em distância. Conferidos hashes e textos das âncoras. A escolha e a relação com as falas do operador permanecem `null`.
- **PAGO — implementação gaussiana de C6:** executado pyRing 2.7.0 original, compilado somente em cache. Fonte likelihood.pyx instalada idêntica à distribuição pública. Nove casos Toeplitz, seis vetores de ruído fora do evento e 270 integrais. Erro máximo em log-evidência: 7.09974301571e-11; em log-densidade projetada: 1.830369456e-08. A omissão intencional do determinante produz diferença 2.46136609387, recusada.
- **PAGO — reprodução em pasta limpa:** todos os valores do novo oráculo coincidiram exatamente. Foi reutilizado o binário compilado e conferido; não chamar isso de nova compilação independente. O teste não leu novamente o strain do evento.
- **PAGO — pacote v2:** `cache/TGL_RINGDOWN_DELIVERY_v2.zip`, 10626560 bytes; 194 arquivos do manifesto verificados após extração nova. O v1 permanece intacto, inclusive seus resultados e reproduções.
- **NÃO PAGO — calibração científica C5:** continua reprovada conjuntamente nas duas famílias/duas amplitudes. O oráculo elimina uma suspeita aritmética específica; não elimina o viés do modelo de forma de onda.
- **PARCIAL — validação pelo posterior publicado:** a comparação pyRing continua com modos/priors/pré-processamento distintos; o release inspecionado não tem 10,5 tM. O oráculo verifica a implementação gaussiana, não a equivalência desses problemas inferenciais.
- **ABERTO — ponte física:** nenhuma partição, relógio ou desenrolamento foi escolhido. A realização KMS finita e as predições continuam condicionais; Kay-Wald/Milburn somente no escopo dos resumos efetivamente lidos.

## Aproveitamento

Foram reutilizados a matriz C1, os relógios da v369 congelada, a covariância e o ruído off-source de C5, o registro C6 e os quatro pacotes já reproduzidos. Não houve nova função em um.py, nova pedra Lean, nova PE de posterior ou repetição do catálogo. A instalação do pyRing usa o tarball público já existente e dependências somente sob cache/pyring_oracle.

Também foi conferida a suspeita de atribuição de remanescente: SEOBNRv4HM já usa a função SEOB correspondente; IMRPhenomXPHM já usa suas funções FinalMass2017/FinalSpin2017. Não há correção a fazer nessa atribuição, e ela não explica o viés.

## Próxima ação científica

C5: resolver o viés de recuperação da forma de onda. Os 4608 cálculos e sua reprodução já terminaram; nenhum grupo FULL_IMR passa as duas famílias e as duas amplitudes. Próxima ação científica: avaliar recuperação com formas IMR completas (rota b), em estudo não-cego separado, preservando o C6 e os critérios originais. Não repetir a grade QNM já reprovada nem ajustar critérios para obter aprovação.

Nenhum resultado de strain foi promovido: INCONCLUSIVE_SYSTEMATICS permanece. Não multiplicar os posteriores do mesmo evento nem tratar estes controles numéricos como observações. O objetivo continua ativo, sem reivindicação de precisão integral já alcançada.

## Reprodução

Descompactar o v2, executar `python verify_delivery.py`, entrar em `C1_C6_ADDENDUM` e executar `python -B reproduce.py --download` no ambiente científico da entrega. Para reutilizar a distribuição conferida: `--source-archive /path/to/pyRingGW-2.7.0.tar.gz`. A opção `--vendor-cache /path/to/vendor` registra explicitamente o reaproveitamento de binário.

O recibo separado `C7_C1_C6_REPLAY_VALIDATION.json` paga a pendência histórica `independent_directory_oracle_replay=PENDING` do recibo imutável do empacotamento. Não sobrescrever o histórico para esconder a sequência.

## Tentativas e memória

A primeira tentativa do gerador C1 falhou por pedir x à leitura coerente não exponencial; código anterior preservado e tipagem corrigida antes da entrega. Avisos do pyRing e a recusa inicial de acesso WSL estão no STATUS. STATUS, PROGRESSO e manifesto local recebem backup imediato dos bytes anteriores. Nenhuma memória canônica de outra casa foi tocada.

## Custódia

| Artefato | SHA-256 lido |
|---|---|
| `C1_LEITURAS.json` | `333a9d8b7d650affb21e63564a399fa3048e407de71f7b9d57ec4d2cd2e583b3` |
| `C1_LEITURAS.md` | `a640e0c9ab336dabf99b7f0bf6423abd4684f60942f3384395eac54028daf6be` |
| `complete_c1_contract.py` | `91d80e48f451fe92c7434f914582d066b3f9dd6440e9ee3dff6a97fcc78ed8aa` |
| `C6_PYRING_IMPLEMENTATION_ORACLE.json` | `bb75157f8f4edd4d3bda7e4607970d1ec77d04820c393c718b1ab9ede8a429aa` |
| `verify_pyring_likelihood.py` | `ca979eb8a0f20d69d679cedb9244d7ab7e0ff89a90ec32de2f014e02736a2a03` |
| `prepare_pyring_oracle.py` | `70986e5a16fcb3440db6879ce5c47ed62d4f9bd0b3810f8f11ad30a39345f8e0` |
| `package_reproduce_pyring_oracle.py` | `db315f1a4436f35573e4af2120f4b9bf1a39071d75882e73dda29f4ed1811acc` |
| `build_c1_c6_addendum.py` | `204be0777e17a46104de7ff5cb2522404c61583df9601ffb9d520d1d45287f26` |
| `C7_C1_C6_ADDENDUM.json` | `81045fa87271028d1e92af3a1cf64c6cd4590753a12da587fb2b96df19f62e3f` |
| `C7_C1_C6_ADDENDUM.md` | `5a9dd40b05480f784b3b325b5fb0d238f5ff067778f002d55702894950f1357e` |
| `C7_C1_C6_ADDENDUM_VALIDATION.json` | `c4488521944af97c8ebf9cef43d95b425c650f95f62cb900f1005013f6332c5b` |
| `C7_C1_C6_REPLAY_VALIDATION.json` | `dd4b6b113ab9df6a53888129eebe7d8756c9960314c7885000daf339c7d37613` |
| `cache/pyring_oracle/PREPARATION.json` | `c29a57a854957598ee748dab5ede93f910e546578a211065cd0e92a61f3c170c` |
| `cache/TGL_RINGDOWN_DELIVERY_v2.zip` | `3c1ae84211f81a46309c44f41035eeb926b31350336be22da4d16ca0953a0bbe` |
| `cache/MANIFESTO_DOWNLOADS.json` | `4320a6bd4ebfeb816a6a096d497650ad0ad3dc9d3df1d8a5121b31ea0a009a1f` |


[REAL — injeções, cálculo e custódia; DERIVED condicional nas taxas; NÃO-CEGO; sem promoção a confirmação física]

# Ordem 013 — recuperação com formas IMR completas

UTC: 2026-09-22T03:44:40.108419+00:00. Axiomas: N/A — sem Lean.

## Resultado

As formas IMR completas substituíram a base curta de QNMs somente neste novo estudo. Foram preservadas as duas famílias, oito leituras, β calculado em runtime e os critérios viés≤0,2, cobertura de 90% em [0,80;0,97], sem borda.

**19 de 24 grupos identificáveis passaram** conjuntamente nas duas famílias e nas duas amplitudes com a mesma verossimilhança de mistura. Total: 576 células, 206 intervalos de ruído por célula, O4/O5 e SNR de ringdown 40/200/600. Os intervalos 50:256 eram externos ao treinamento da PSD e não foram usados no forecast anterior de 50 injeções; são reutilizados entre cenários, não 118.656 eventos independentes.

Há 78 células individuais aprovadas na mistura e 76 na recuperação pela própria família. **Nenhuma das 96 células identificáveis recuperadas somente pela família oposta passou.** Metade das 576 células é sub-resolução e não recebe um selo de calibração.

| PSD | Leitura | SNR de ringdown | Duas famílias × a=0/1, mistura |
|---|---|---:|---|
| O4 | R-B | 40 | NÃO PAGO |
| O4 | R-B | 200 | PAGO neste conjunto |
| O4 | R-B | 600 | PAGO neste conjunto |
| O4 | R-RAIZ-0 | 40 | PAGO neste conjunto |
| O4 | R-RAIZ-0 | 200 | PAGO neste conjunto |
| O4 | R-RAIZ-0 | 600 | PAGO neste conjunto |
| O4 | R-LIN | 40 | PAGO neste conjunto |
| O4 | R-LIN | 200 | PAGO neste conjunto |
| O4 | R-LIN | 600 | PAGO neste conjunto |
| O4 | R-MOD | 40 | NÃO PAGO |
| O4 | R-MOD | 200 | PAGO neste conjunto |
| O4 | R-MOD | 600 | PAGO neste conjunto |
| O5 | R-B | 40 | NÃO PAGO |
| O5 | R-B | 200 | PAGO neste conjunto |
| O5 | R-B | 600 | PAGO neste conjunto |
| O5 | R-RAIZ-0 | 40 | NÃO PAGO |
| O5 | R-RAIZ-0 | 200 | PAGO neste conjunto |
| O5 | R-RAIZ-0 | 600 | PAGO neste conjunto |
| O5 | R-LIN | 40 | PAGO neste conjunto |
| O5 | R-LIN | 200 | PAGO neste conjunto |
| O5 | R-LIN | 600 | PAGO neste conjunto |
| O5 | R-MOD | 40 | NÃO PAGO |
| O5 | R-MOD | 200 | PAGO neste conjunto |
| O5 | R-MOD | 600 | PAGO neste conjunto |

## O limite que impede promover o resultado

O gerador verdadeiro está contido na mistura, e a fonte é um único binário com massas, spins, inclinação e fase fixados. O teste paga calibração **dentro desse conjunto fechado**, não robustez para uma fonte arbitrária ou estimação dos parâmetros desconhecidos. A análise por família oposta torna esse limite mensurável.

**R-B em SNR40 continua NÃO PAGO**: viés entre 0.0469238 e 0.918529; cobertura entre 0.752427 e 0.84466. O sucesso de SNR200/600 não se transporta para a sensibilidade atual. Uma razão de Bayes média positiva também aparece sob a=0 em baixo SNR; não convertê-la em sigma.

As taxas são aplicadas a todo o conteúdo dos harmônicos 22/44, cada qual com sua taxa fundamental; outros harmônicos permanecem como no controle. Essa transposição continua condicional. A mistura bayesiana tem prior 1/2 para cada família e soma evidências; o máximo entre famílias é usado apenas no perfil diagnóstico. Não se seleciona a família que produz a frase desejada.

## Verificação e reprodução

- **PAGO:** registro separado antes da execução, código e entradas conferidos por hash; nenhum novo strain on-source lido.
- **PAGO:** critérios recalculados de todas as 288 células identificáveis a partir dos sorteios gravados.
- **PAGO:** 96 células e 288 sorteios conferidos por integral SVD independente; maior diferença de ln B = 1.0768417269e-09. A base da própria família contém exatamente a injeção sem ruído, controle explícito que não é robustez externa.
- **PAGO:** reprodução em pasta nova: 9247 campos numéricos, identidades e estatutos conferidos; todas as diferenças nos arrays de sorteios foram zero.
- **PAGO:** pacote `cache/C7_IMR_RECOVERY_REPRODUCTION_v1.zip`, 15583002 bytes. Começa de matrizes IMR/ruído derivadas e conferidas. A produção dessas entradas desde strain público/PyCBC/LAL já está no pacote anterior C7_INJECTION_REPRODUCTION; não foi repetida.
- **NÃO PAGO:** marginalização de parâmetros da fonte e validação fora do conjunto finito contendo o gerador da própria injeção.
- **INALTERADO:** C5 anterior, C6 congelado, veredito INCONCLUSIVE_SYSTEMATICS, escolha física da partição/relógio/leitura e gate canônico.

## Próximo passo

A recuperação IMR resolve a discrepância apenas no conjunto fechado testado: 19/24 grupos passam, mas o gerador verdadeiro está entre os candidatos e massas/spins/extrínsecos estão fixados. Para PE astrofísica, estudar a marginalização dos parâmetros da fonte e validação fora dessa identidade injeção-recuperação, com registro não-cego separado.

## Comando e aproveitamento

Descompactar C7_IMR_RECOVERY_REPRODUCTION_v1.zip e executar `python -B reproduce.py` com NumPy/SciPy. Ambiente efetivamente testado: Python 3.12, NumPy 2.5.3 e SciPy 1.18.1. A reprodução verifica o manifesto antes de executar e cria uma nova pasta de trabalho.

Reaproveitados os dois arquivos IMR, as PSDs, o ruído, as taxas e os QNMs já calculados. Nenhum pacote de sistema, um.py, kernel ou memória de outra casa foi alterado. STATUS, PROGRESSO e manifesto local atualizados com backups imediatos byte a byte. Nenhuma falha de execução nesta rodada; os negativos científicos permanecem nos arquivos.

## Custódia lida nesta execução

| Artefato | SHA-256 |
|---|---|
| `REGISTRO_C5_IMR_RECOVERY.json` | `804af656c37fef53cfd09abdec6745677efc7087551dd53f8cb95c66e00d7898` |
| `calibrate_imr_recovery.py` | `d409fa2225cc25a2eda8591b57f5e2e789c44b5eee647b2a6d525a69aab8c45a` |
| `C5_IMR_RECOVERY.json` | `bda4441856c23a643be6dc467b65059c4fc968d54971a73490710ffc67568cb6` |
| `verify_imr_recovery.py` | `8fed4447ecb57aa18aa0d5c5c6f80b7638a47d195c658f5caee35890891ab0f3` |
| `C5_IMR_RECOVERY_VALIDATION.json` | `0f40a767502a627ab68dcb801e44486d446c0f3d2582f6e668ab719766a2c8c7` |
| `package_reproduce_imr_recovery.py` | `c2f862223d0c333355dbf460fa79675dc497078cb250134d7986715f8ca84094` |
| `build_imr_recovery_package.py` | `080db29e02c925d8f08865bc5ab09d6da913e3a55c6edf818bc10b9d6b2e8a7f` |
| `C7_IMR_RECOVERY_PACKAGE.json` | `0bba01dba8cff4881e8e59d718b3396b96878115bc3447e2b4a8a7526fcb376a` |
| `C7_IMR_RECOVERY_REPLAY_VALIDATION.json` | `2553f7baa9848da82baf9eaa5d02a5554cfa84ccdd9c2581faafbd80238543a9` |
| `cache/C7_IMR_RECOVERY_REPRODUCTION_v1.zip` | `7dd26dad74ce5fc101c9183654af33394f62a3cb06e261704aa7ef3a64a98c22` |
| `cache/imr_recovery/O4_draws.npz` | `a79ab602d4b9fa2a1c9cf30de3cdf0ad663703a557ea88574473ec45e646c487` |
| `cache/imr_recovery/O5_draws.npz` | `1feacc7bf0f4e668a9afd8249778f21bc201c92e4e2f22dddc38f88bc3410434` |
| `cache/MANIFESTO_DOWNLOADS.json` | `580128a3ba513ebdac66effa64125b91f9c0d39f2cc9933af10c78073ac69b97` |


[REAL — diagnóstico local e integrais verificadas; INPUT nos priors e na transposição física; inferência astrofísica completa OPEN]

# Ordem 013 — incerteza da fonte e limites do resultado com fonte fixa

UTC: 2026-09-22T04:04:14.582949+00:00. Axiomas: N/A — sem Lean. Nenhuma mudança do gate, do um.py ou do C6.

## Resultado e interpretação

A rodada anterior de recuperação IMR fixava massas, spins, fase e inclinação. Esta extensão mede a informação que resta ao acrescentar, à mesma liberdade de amplitudes por detector, o instante do pico e quatro parâmetros intrínsecos: log da massa total, log da razão de massas, deslocamento comum dos spins alinhados e deslocamento oposto dos spins. A inclinação e o céu ainda são fixos. São duas famílias, O4/O5 de referência, quatro leituras observáveis, a=0/1 e uma única fonte representativa.

**Na família Phenom, o ramo B conserva cerca de 0.842% a 2.66% da informação local disponível após ajustar amplitudes, ao liberar também tempo e parâmetros da fonte.** O resultado é estável sob refinamento. Isso mede degenerescência neste modelo; não é exclusão da leitura B e não mede significância de um evento.

Na SEOB, a derivada da razão de massas e a dos spins continuam sensíveis à resolução. As estimativas estão preservadas e marcadas **NUMERICAL_SENSITIVITY_UNRESOLVED**. Não escolhemos o refinamento que produziria um resultado desejado. Passaram 16/32 controles em cada rodada: os 16 da Phenom. Essa contagem não representa uma aprovação física por maioria.

| Família | PSD | a de referência | z local, fonte fixa, SNR40 | z local, fonte livre, SNR40 | Informação restante | Controle |
|---|---|---:|---:|---:|---:|---|
| SEOBNRv4HM | O4 | 0 | 0.416009 | 0.057146 | 1.887% | NUMERICAL_SENSITIVITY_UNRESOLVED |
| SEOBNRv4HM | O4 | 1 | 0.390952 | 0.0492061 | 1.584% | NUMERICAL_SENSITIVITY_UNRESOLVED |
| SEOBNRv4HM | O5 | 0 | 0.417451 | 0.0566804 | 1.844% | NUMERICAL_SENSITIVITY_UNRESOLVED |
| SEOBNRv4HM | O5 | 1 | 0.392498 | 0.048926 | 1.554% | NUMERICAL_SENSITIVITY_UNRESOLVED |
| IMRPhenomXPHM | O4 | 0 | 0.399913 | 0.0438374 | 1.202% | STABLE_LOCAL_DIAGNOSTIC |
| IMRPhenomXPHM | O4 | 1 | 0.377102 | 0.0346032 | 0.842% | STABLE_LOCAL_DIAGNOSTIC |
| IMRPhenomXPHM | O5 | 0 | 0.403772 | 0.0658769 | 2.662% | STABLE_LOCAL_DIAGNOSTIC |
| IMRPhenomXPHM | O5 | 1 | 0.379117 | 0.0427879 | 1.274% | STABLE_LOCAL_DIAGNOSTIC |

O símbolo z nesta tabela é a norma local da derivada projetada, em unidades de ruído ideal, para Δa=1. É um diagnóstico de Fisher. Não é sigma observado nem conversão de fator de Bayes. O SNR é referido ao sinal nominal a=0 neste novo teste; não é exatamente a renormalização de cada injeção da rodada anterior.

## Construção e controle da conta

Escrevendo d=∂h/∂a e A para as colunas de parâmetros indesejados após branqueamento, calculamos d_perp=(I−AA⁺)d e I_a=||d_perp||². Os ranks são conferidos com três tolerâncias. As derivadas intrínsecas vêm de formas IMR novas, geradas por PyCBC/LAL, com o remanescente próprio de cada família; não de uma alteração arbitrária da frequência do QNM.

O pico é o máximo contínuo, por spline, da amplitude do harmônico 22. Todos os harmônicos compartilham esse pico. A janela de dados fica fixa em 10 tM do remanescente nominal enquanto variamos a fonte. Isso evita transformar mudança de janela em informação de massa.

Foram geradas 68 formas por rodada: nominal e diferenças centrais, mais controles de resolução. A segunda rodada divide os passos por quatro; a terceira dobra as taxas de geração para 16384/32768 Hz. As duas anteriores, seus registros e resultados continuam intactos. Total 204 formas de controle, não 204 eventos físicos independentes.

## Distribuições de razão de Bayes: escopo estritamente afim

Cada rodada também calcula 288 distribuições de ln B, com 206 intervalos de ruído por célula, usando os mesmos intervalos externos 50:256 já conhecidos. São reutilizados entre cenários e rodadas. A integral é a de um modelo afim h=h_a+J_a·u, com prior gaussiano normalizado em u. Assim C_a=I+J_a Σ J_aᵀ e log Z_a=−(r_aᵀC_a⁻¹r_a+log det C_a)/2, fora a constante comum.

Os três priors da fonte são: fixo, σ=0,002 e σ=0,02 em cada uma das quatro coordenadas declaradas. Eles são **INPUT diagnóstico**, centrados na fonte simulada. Não são informação do evento nem derivação da TGL. As amplitudes têm prior próprio, idêntico em definição entre hipóteses; a integração inclui o determinante. Também calculamos média e variância analíticas para ruído gaussiano ideal no centro do prior, mantendo-as separadas do ruído empírico.

Esses resultados não substituem uma integral sobre formas de onda não lineares. Uma média positiva sob a=0, que continua possível por efeito do prior, não é detecção. Os números completos de ambos a=0/1 estão no resumo JSON, sem selecionar somente a hipótese favorável.

## Critérios e evidências

- **PAGO:** registro e hashes antes de cada rodada; parâmetros físicos e regras de aceitação declarados; nenhum novo strain do evento lido.
- **PAGO:** integral afim conferida por Cholesky da covariância completa, independente da implementação SVD de produção: 648 comparações, maior diferença de ln B=2.06739514397e-10.
- **PAGO no escopo local:** convergência das derivadas e informação projetada na Phenom, nas quatro leituras/duas PSDs/duas amplitudes.
- **NÃO PAGO:** convergência da SEOB pelo critério pré-fixado; derivadas sensíveis preservadas como tal.
- **NÃO PAGO:** cobertura/viés sob variação não linear de fontes, marginalização astrofísica completa e rede com polarizações coerentes. As 12 amplitudes independentes por detector são uma flexibilidade fenomenológica, não uma inferência física de orientação.
- **INALTERADO:** C6, seus hashes, o veredito INCONCLUSIVE_SYSTEMATICS, as leituras físicas abertas e os pacotes anteriores.

## Próximo passo e aproveitamento

O diagnóstico local da fonte está calculado, mas não substitui marginalização não linear. Phenom mantém só 0,8–2,7% da informação local do ramo B depois dos parâmetros livres testados. A família SEOB falha nos controles de derivada mesmo com refinamento; avançar com avaliação não linear/coerente de fonte, sem trocar isso por mais rodadas de Fisher ou aceitar números instáveis.

Reaproveitados PSDs, ruído externo, QNMs, leis condicionais e geradores já instalados. Nada foi instalado em /opt. Para reproduzir o cálculo de uma rodada já gerada, entrar em sua pasta e executar `python -B analyze_source_tangents.py` seguido de `python -B verify_source_tangents.py` **em uma cópia nova com as saídas removidas da cópia**, preservando as entradas/registro; os scripts recusam sobrescrever resultados. A análise exige NumPy/SciPy; gerar fontes exige PyCBC/LAL. `verify_source_tangents_extended.py` confere as três rodadas sem repetir a geração. A geração usa só fontes públicas e o ruído derivado já custodiado. Não se entrega um novo ZIP duplicando os pacotes anteriores nesta etapa diagnóstica.

As falhas desta rodada são os controles numéricos da SEOB, registrados nos três resultados; as execuções terminaram com código zero. Não há processo em curso. STATUS, PROGRESSO e manifesto foram atualizados com backup imediato de bytes. Memórias canônicas são somente leitura nesta ordem.

## Custódia lida nesta execução

| Arquivo | SHA-256 |
|---|---|
| `REGISTRO_C5_SOURCE_TANGENTS.json` | `fb8a5728d8a1c0652e2f0ec7c38b1982c60e1c1bf51338dba84978d42e285eba` |
| `C5_SOURCE_TANGENTS_INPUTS.json` | `228a66d054e2e24726ab8edd030757e4649c44bec9f1a5c229d3edfa9df84853` |
| `C5_SOURCE_TANGENTS.json` | `2a5d4f63d26839ceab195b82e57fe08850d1b63405334f140da83c84723d4610` |
| `C5_SOURCE_TANGENTS_VALIDATION.json` | `e97a01c7943702c22ec16d1ddd3158b633edc5c3553142c5d36af17f93292bd2` |
| `cache/source_tangents_refinement/REGISTRO_C5_SOURCE_TANGENTS.json` | `704589ad5e13592fd18342db92c35b9bda6c6052e371d7348943027fec5b9d6f` |
| `cache/source_tangents_refinement/C5_SOURCE_TANGENTS_INPUTS.json` | `c33f91f1e5e489c400d437cef1fe75f679b79f564ab461e1adfc24829eec406e` |
| `cache/source_tangents_refinement/C5_SOURCE_TANGENTS.json` | `6b503e6b157e4a8d824ed4669d353efe0b1ade4317b37172259cc2fbc6674f22` |
| `cache/source_tangents_refinement/C5_SOURCE_TANGENTS_VALIDATION.json` | `4acf43f9c5438f90c86f6ac76b0524cc62e4d3e65f8371d2e1a6232d87511f4a` |
| `cache/source_tangents_highrate/REGISTRO_C5_SOURCE_TANGENTS.json` | `a658d193051cedaf6da2273bae70127fdb36757d28d2ddb515b45e342004f800` |
| `cache/source_tangents_highrate/C5_SOURCE_TANGENTS_INPUTS.json` | `bdce3d3b7ab07711aed46491e3b2ead0bb725ddee78bee9f51061438a9d15be5` |
| `cache/source_tangents_highrate/C5_SOURCE_TANGENTS.json` | `5effc64bf2dcb648145a1b002c62c6da027e6f685eeb68c7a56fd64d59eb9380` |
| `cache/source_tangents_highrate/C5_SOURCE_TANGENTS_VALIDATION.json` | `1e129e553bd02d4db0e140807e379ff24f101ca2715e1c5ecc0e3c9bef409214` |
| `prepare_source_tangents.py` | `54a823eb4ec3ade6c1bdbdd10a471d1b0594da40adff8229a13b3e183517535e` |
| `analyze_source_tangents.py` | `3b7b425e3f81f38b5c2cb5cafe182bf38daa46c89ef99cf1cd7c7b5647b5b77f` |
| `verify_source_tangents.py` | `59a868489a50fd6a57f0af4b3ffc0c1846a00ca12369a286f17e882f9b3d1944` |
| `refine_source_tangents.py` | `1d4ed9e22727b10872e3a2014b0c3dc74c919a9e141e17bea99933fca57f5d8f` |
| `refine_source_tangents_highrate.py` | `c7145796539b5410c5d81eec1614140a7e368a952bdb0b6014c9c47e811ec5a9` |
| `verify_source_tangents_extended.py` | `cdb7a9d38780fddffe52d0d6a4fa5dbf16e88fd9db2b615738a5552a9ce3e07b` |
| `C5_SOURCE_TANGENTS_EXTENDED_VALIDATION.json` | `c87363d62ddf2553f01716095859e89b5aa27144d9e224c007ec27812407781f` |
| `C5_SOURCE_UNCERTAINTY_SUMMARY.json` | `45e0d7aa63c591b29c4ad1cea9b4da8d3e16c77f2821df7f8ef5e93e1fd894f9` |
| `record_source_tangents.py` | `80d451503505d157c9af0a2058fbd78dc88fa2748c2a7752232283c72539fe86` |
| `cache/MANIFESTO_DOWNLOADS.json` | `6dd8ed1504bc0d18927a611fcf4ea6640740e7a8e16a642cc4e47d21a51a8d84` |


[REAL — candidatos de fonte física e verificação numérica; DERIVED condicional no limite de poder; marginalização completa OPEN]

# Ordem 013 — fonte não linear, polarização coerente e correção do pico

UTC: 2026-09-22T04:36:38.574849+00:00. Axiomas: N/A — sem Lean. O C6 e o programa canônico permanecem intactos.

## Resultado

Foram feitas 12 buscas com a convenção antiga de pico e 12 numa rodada corrigida, reaproveitando os candidatos anteriores. Três binários alinhados, duas famílias de injeção e duas de recuperação. A injeção tem a=1 no ramo B; a recuperação busca uma fonte GR, a=0, variando massa total, razão de massas, ambos os spins, inclinação, fase e instante do pico. Distância e uma polarização são compartilhadas pela rede.

**As seis recuperações pela própria família admitem candidatos sem dephasing com resíduo de 0.1449 a 0.5979 em unidades da métrica de ruído, para SNR de ringdown 40**, nas PSDs O4/O5 de referência. Verificados com geradores a 16384 e 32768 Hz. A busca é local: um candidato válido dá uma cota superior para o melhor resíduo, mesmo quando o otimizador esgota seu orçamento. Não é garantia de ótimo global, cobertura, posterior ou fator de Bayes.

As trocas de família têm resíduos entre 0.6606 e 4.857. Portanto a incerteza do gerador precisa permanecer no modelo. Não se seleciona apenas o ajuste favorável.

| Candidato | PSD | Resíduo a 16384 Hz | Resíduo a 32768 Hz | Ambos abaixo de um |
|---|---|---:|---:|---|
| reference_IMRPhenomXPHM_to_IMRPhenomXPHM | O4 | 0.144953 | 0.144873 | sim |
| reference_IMRPhenomXPHM_to_IMRPhenomXPHM | O5 | 0.147022 | 0.14695 | sim |
| reference_IMRPhenomXPHM_to_SEOBNRv4HM | O4 | 0.668337 | 0.668495 | sim |
| reference_IMRPhenomXPHM_to_SEOBNRv4HM | O5 | 0.660434 | 0.660626 | sim |
| reference_SEOBNRv4HM_to_IMRPhenomXPHM | O4 | 0.905949 | 0.905899 | sim |
| reference_SEOBNRv4HM_to_IMRPhenomXPHM | O5 | 0.899861 | 0.89981 | sim |
| reference_SEOBNRv4HM_to_SEOBNRv4HM | O4 | 0.317586 | 0.317225 | sim |
| reference_SEOBNRv4HM_to_SEOBNRv4HM | O5 | 0.320533 | 0.319987 | sim |
| source_64_IMRPhenomXPHM_to_IMRPhenomXPHM | O4 | 0.517437 | 0.517421 | sim |
| source_64_IMRPhenomXPHM_to_IMRPhenomXPHM | O5 | 0.512796 | 0.512781 | sim |
| source_64_IMRPhenomXPHM_to_SEOBNRv4HM | O4 | 4.25326 | 4.2621 | não |
| source_64_IMRPhenomXPHM_to_SEOBNRv4HM | O5 | 4.22815 | 4.23706 | não |
| source_64_SEOBNRv4HM_to_IMRPhenomXPHM | O4 | 3.3484 | 3.3504 | não |
| source_64_SEOBNRv4HM_to_IMRPhenomXPHM | O5 | 3.33365 | 3.33568 | não |
| source_64_SEOBNRv4HM_to_SEOBNRv4HM | O4 | 0.563785 | 0.564073 | sim |
| source_64_SEOBNRv4HM_to_SEOBNRv4HM | O5 | 0.559458 | 0.559775 | sim |
| source_90_IMRPhenomXPHM_to_IMRPhenomXPHM | O4 | 0.416988 | 0.416953 | sim |
| source_90_IMRPhenomXPHM_to_IMRPhenomXPHM | O5 | 0.42127 | 0.421241 | sim |
| source_90_IMRPhenomXPHM_to_SEOBNRv4HM | O4 | 2.85584 | 2.85783 | não |
| source_90_IMRPhenomXPHM_to_SEOBNRv4HM | O5 | 2.8844 | 2.88636 | não |
| source_90_SEOBNRv4HM_to_IMRPhenomXPHM | O4 | 4.85355 | 4.85718 | não |
| source_90_SEOBNRv4HM_to_IMRPhenomXPHM | O5 | 4.83488 | 4.83925 | não |
| source_90_SEOBNRv4HM_to_SEOBNRv4HM | O4 | 0.598038 | 0.59792 | sim |
| source_90_SEOBNRv4HM_to_SEOBNRv4HM | O5 | 0.592194 | 0.592087 | sim |

## A falha identificada e corrigida

Para o par alinhado ±22, h+ é proporcional a (1+cos²i)/2 vezes uma quadratura e h× a cos i vezes a outra. Assim h+²+h×² pode oscilar com a fase quando a fonte é inclinada: seu máximo não é a amplitude intrínseca do modo complexo. No candidato problemático, o pico projetado saltou **2.60065 ms** ao mudar a resolução. O pico intrínseco variou **12.6872 μs** no mesmo diagnóstico.

A rodada nova usa o máximo da amplitude do 22 visto face-on, antes da projeção para a orientação da fonte, e mantém um único instante para todos os harmônicos. Trata-se de uma convenção nova, registrada separadamente: não alteramos o início ou o resultado do C6. A taxa do modelo continua aplicada ao tempo desde o pico declarado; nenhuma identificação física única de início/desenrolamento é inferida disso. O pico e as buscas antigos permanecem como evidência do erro.

## O que o limite gaussiano permite dizer

Para dois templates fixos h0 e h1, branqueados por uma covariância conhecida, r=||h1−h0||. O estatístico S=⟨h1−h0,Y−h0⟩/r tem distribuição N(0,1) sob h0 e N(r,1) sob h1. Um teste que controle o falso alarme do nulo composto GR também precisa controlá-lo no candidato h0 encontrado. No modelo gaussiano, o melhor poder desse par a um limiar unilateral de cinco sigmas é Φ(r−5).

Nos pares da própria família, isso dá cotas de poder entre 6.01547e-07 e 5.36089e-06 em SNR40. **É uma derivação condicional para os templates e ruído gaussiano, não uma medição da cauda do ruído real, nem uma conversão de ln B para sigma.** Uma fonte sem dephasing quase idêntica impede alto poder uniforme nesse cenário; não exclui a TGL nem elimina a necessidade da inferência.

## Likelihood que fica disponível

`coherent_imr_likelihood.py` reaproveita a integral linear existente com somente dois coeficientes comuns de rede: c=A cos(2ψ), d=A sin(2ψ). Eles representam distância e rotação de polarização, em vez de amplitudes independentes para cada modo/detector. O prior isotrópico gaussiano desses coeficientes equivale a ψ uniforme módulo π e p(D)=403²/(s²D³) exp[−403²/(2s²D²)], D em Mpc. É normalizado e marcado INPUT; não é prior uniforme em volume.

A integral de distância/polarização é exata, inclusive determinante; o maior erro contra a covariância completa foi 2.75122147286e-11. **Os sete parâmetros não lineares da fonte ainda não foram integrados.** O código não normaliza a forma de onda a um SNR escolhido dentro da likelihood. O SNR40 é apenas a normalização declarada das injeções de controle.

## Critérios, reprodução e aproveitamento

- **PAGO:** modelos físicos de rede com polarização comum; três fontes; ambas as famílias; resultados negativos incluídos.
- **PAGO:** pico intrínseco corrigido por diagnóstico explícito; nova rodada registrada; hashes e C6 original conferidos.
- **PAGO:** regeneração dos 12 candidatos e projeção QR independente, diferença máxima 8.881784197e-16; controle em 32768 Hz.
- **PAGO:** pacote inglês `cache/C7_COHERENT_SOURCE_REPRODUCTION_v1.zip`, 13662627 bytes; reprodução em pasta nova regenerou os candidatos, com diferença máxima de resíduo 0. O otimizador não foi repetido na reprodução; isso está expresso.
- **NÃO PAGO:** marginalização dos sete parâmetros, distribuição de evidência de fonte completa, calibração de ruído não gaussiano e cobertura sob população de fontes.
- **INALTERADO:** C6 INCONCLUSIVE_SYSTEMATICS, leituras físicas condicionais, escolha de relógio/partição e gate.

Descompactar o pacote e executar `python -B reproduce.py` num Python com PyCBC/LAL/NumPy/SciPy. Versões testadas constam no README e nos recibos. Os arquivos de forma de onda usam dados e geradores públicos; não há programa canônico ou acervo privado no pacote.

Há agora uma likelihood de fonte não linear com distância/polarização comuns integradas exatamente. Falta integrar os sete parâmetros de fonte e medir distribuições O4/O5 e cobertura sob fontes variadas; candidatos de Powell não são posteriores nem fatores de Bayes. Usar o módulo corrigido em cache/nonlinear_intrinsic_peak (ou C7_COHERENT_SOURCE_REPRODUCTION), não a versão histórica de pico projetado.

As buscas são não cegas, partem das fontes simuladas e de candidatos anteriores, e têm orçamentos limitados. Saídas de orçamento não foram renomeadas como sucesso. Nenhum evento real foi relido. As memórias locais receberam backups imediatos de bytes; a gerência mantém a incorporação canônica.

## Custódia lida nesta execução

| Arquivo | SHA-256 |
|---|---|
| `coherent_imr_model.py` | `3ee4c88b7c719f3a67f41dda4e67462cbb576ea8fcf191d8abe5480aba3f3d38` |
| `coherent_imr_likelihood.py` | `883613f37e7861c95ec43790c18ce7e790f7c708de776a75cb5496bc5fb3d74e` |
| `nonlinear_coherent_recovery.py` | `f426318a1f4cd2502cd71bed20377fa710fa78bd51425d8496059f294999d64a` |
| `validate_coherent_model.py` | `7c46f0c5ebef98dd936c9a4706815a7ffe867435a8c2cb22e826de143677a89e` |
| `validate_coherent_likelihood.py` | `375c839ef517c94db9f67a5548ac4f95573db877bc269636e1c764bd77e624dc` |
| `REGISTRO_C5_NONLINEAR_COHERENT.json` | `af458f8d7f283652fafea35c0fd1d31eb3578da31b9791c059448869f956203a` |
| `C5_COHERENT_MODEL_VALIDATION.json` | `646ac965b17089596e238af16af747919d4b2e1c5c391130b83ab9bd6eb62f1a` |
| `C5_COHERENT_LIKELIHOOD_VALIDATION.json` | `8fd147497ac2100e95da95aaa3328068aa22df590469dd8008fc0ed5a355368d` |
| `C5_NONLINEAR_COHERENT.json` | `ceeb3fda937f0d2b4b0dd4922868c81d72adff94775bf4f091400e2a72879ab3` |
| `C5_COHERENT_PEAK_DIAGNOSTIC.json` | `6a56b29f75bf1388d09c46c61fbfa9d361649a71ed8833e102844bfbfc22b8a2` |
| `diagnose_coherent_peak.py` | `55993e9eb781e142c7ebc2e0e9f1315b48014f14235613d962b959b8c5af20df` |
| `prepare_intrinsic_peak_run.py` | `2343c8199acaf3442717ed682eae1307d9b1c09bab7f1d4e228afa6e9cc4145d` |
| `verify_nonlinear_coherent.py` | `99e15f571626c28ab3ea32bfc1783414c3a8f9958d722f80b691f651b23dd107` |
| `build_coherent_source_package.py` | `24b1df2a9db1d258b40cb0976fa95174bcbbefcb35ccaf0176a3884f55a5d249` |
| `C7_COHERENT_SOURCE_PACKAGE.json` | `7b8a50c120c2533cdbc62be960fdeb8dee76a84bf621a33a261f6102072264ca` |
| `C7_COHERENT_SOURCE_REPLAY_VALIDATION.json` | `b6ed52324d189e52c9838fcbf0b4f74f1c1259f49bed44181d5f801acbee248b` |
| `C5_NONLINEAR_SOURCE_SUMMARY.json` | `e51a7faeda45d16f674986a1d5fdf55ac5da885d2d6fa67212ef586b92157b27` |
| `record_nonlinear_coherent.py` | `33b455a061013345665d18aa98210a1487dbc56ddd3d6a4a1ef839ae028d36aa` |
| `cache/C7_COHERENT_SOURCE_REPRODUCTION_v1.zip` | `19be994825bb76618dcfd1edcf3a819141a66a07999dc1324b41d1f7fb8efc3e` |
| `cache/nonlinear_intrinsic_peak/REGISTRO_C5_NONLINEAR_COHERENT.json` | `81f223445b02c1c313a8efe939b72cb7a6696adaaf80baa166b913555ff1a27c` |
| `cache/nonlinear_intrinsic_peak/C5_NONLINEAR_COHERENT.json` | `ded69e9a63371a6cfb2ed83beaaa653741d2177b9c43ddc2309cd7365be5a426` |
| `cache/nonlinear_intrinsic_peak/C5_NONLINEAR_COHERENT_VALIDATION.json` | `dbcc05451b948c77a3e495b353405ac77c91003b7811396a6ddb1b0f447fb28d` |
| `cache/nonlinear_intrinsic_peak/C5_COHERENT_MODEL_VALIDATION.json` | `11c2f0fa1a8a3d7f30c6dbb3819b67c48865fe7e8fd7a970abc2f2a2930e6ee8` |
| `cache/nonlinear_intrinsic_peak/C5_COHERENT_LIKELIHOOD_VALIDATION.json` | `cc292f917d0cba3be45df414ecb581eb51a547ae97f11a1684a138db025efc1a` |
| `cache/nonlinear_intrinsic_peak/PEAK_CORRECTION_PROVENANCE.json` | `13d603832d634774182c056a60ac29e821e172ebe402b76093a1f811650be78b` |
| `cache/nonlinear_intrinsic_peak/coherent_imr_model.py` | `4d9e568816c3b47e8e59b2401334a1a66541247fa80ed36495949aa4f5bca497` |
| `cache/nonlinear_intrinsic_peak/nonlinear_coherent_recovery.py` | `8c05dfa7d5e71fb17634ce4514290710a5208c1486472034e368161f8fb4dfa4` |
| `cache/MANIFESTO_DOWNLOADS.json` | `07c45d18d92ca3541625d76548eb0e1ff29ed82d34ed1388a4118fd39ed9efd7` |


---
[REAL — implementação verificada e processo iniciado; OPEN — evidência científica ainda não concluída]

# ORDEM 013 — Integração não linear da fonte

Registro: 2026-09-22T04:56:01.697307+00:00.

**PAGO:** a likelihood direta das formas de onda agora integra sete coordenadas físicas
(massa total, razão de massas, dois spins, inclinação, fase orbital e deslocamento do pico),
com distância/polarização comuns integradas analiticamente. O pico usa a correção intrínseca
22 previamente demonstrada. Priors uniformes declarados, sem reutilizar o posterior do
próprio evento. O prior de distância continua inverso-Rayleigh, não uniforme em volume.

**PAGO:** entradas congeladas: três fontes × duas famílias de injeção × a=0/1 × O4/O5 ×
50 intervalos = 1200 conjuntos simulados. São os mesmos 50 intervalos reutilizados e
pareados; não são 1200 eventos independentes. Cada conjunto recebe duas hipóteses:
2400 componentes de likelihood, reconstruídas SEPARADAMENTE. A média usada pelo
integrador é um recurso de cálculo, nunca o produto dessas simulações.

**PAGO:** equivalência da implementação com a API anterior: erro máximo
1.1368683772161603e-13; identidade de reconstrução de evidência conferida por
quadratura independente: 6.6613381477509392e-16.

**NÃO PAGO:** convergência astrofísica, distribuição final de ln B, posterior contínuo de a,
viés/cobertura, demais SNR e leituras. A primeira família de recuperação, IMRPhenomXPHM,
está em execução. SEOBNRv4HM continua na matriz, mas sua integração ainda não foi iniciada.
256 pontos vivos, orçamento piloto de 24000 avaliações, semente 130522 e checkpoints.
Não executar outra cópia enquanto a sessão 79591 continuar viva.

## O alerta que o controle produziu

O controle analítico usa gaussianas em sete dimensões. A componente com menor evidência
ficou com ESS de [19.1910390504424, 21.65496872447128] e erros em ln Z de
[-0.6151549186382663, -0.7644486530485732]. Portanto, a etiqueta PASS do teste de consistência
ampla **não satisfaz a precisão pretendida**. A auditoria astrofísica exigirá ESS≥100,
peso máximo≤0,05, estabilidade ao dobrar a amostragem temporal e repetição independente
com mais pontos vivos; a convergência global sozinha não basta. Se necessário, a rodada
piloto poderá orientar balanceamento computacional, preservando os priors e reconstruindo
as integrais por componente. O erro medido não será escondido por médias.

## Comandos

No WSL, diretório `cache/source_evidence`:

```text
/opt/pycbc_env/bin/python -B source_evidence.py run
/opt/pycbc_env/bin/python -B analyze_source_evidence.py IMRPhenomXPHM_seed130522_nlive256
```

O primeiro comando já está rodando: NÃO duplicar. A auditoria só pode rodar quando existir
RESULT.json. `--resume` é reservado a processo comprovadamente interrompido e checkpoint
existente; um timeout de observação não demonstra interrupção.

O pacote dynesty3.1.0 e sua licença foram COPIADOS de instalação existente para `vendor`;
nenhuma instalação de /opt foi alterada. A interface foi conferida na documentação primária
<https://dynesty.readthedocs.io/en/latest/quickstart.html> e no código local. A documentação
adverte que poucos pontos vivos podem perder modos; isso é uma limitação relevante aqui.

Não houve leitura nova da janela do evento, alteração de C6, seleção física de relógio,
partição ou desenrolamento, alteração do um.py, kernel, Atlas ou gate. C6 preserva
INCONCLUSIVE_SYSTEMATICS. Axiomas: N/A — sem Lean.

## Custódia dos insumos e scripts

| arquivo relativo à bancada | SHA256 medido |
|---|---|
| `prepare_source_evidence.py` | `acad4b6fcdda52b6a5c9ff3b6c5b091a9329ae4115871cbf4d1536099ce488c1` |
| `record_source_evidence_start.py` | `64461f6aa5996248d6fb2a24c46fba7625934be903fe63e3c5cc4d601d13b6e0` |
| `cache/source_evidence/source_evidence.py` | `0590f8e15bd508e525d2911fc570615671fdcdbc328399f4d7d8cb05d9816f7a` |
| `cache/source_evidence/validate_source_evidence.py` | `e2e81c1891c8d6c6253cd987f2aec25b4c1d787b5188d2a2f8587436928f2379` |
| `cache/source_evidence/validate_nested_mixture.py` | `22b441da13b79f8ec36fe0cedc9a329a10e983b2aeac55bc8b9a9c7a3f767fb2` |
| `cache/source_evidence/analyze_source_evidence.py` | `6723ed2ff58e409c7b47ed54e91929291f1f4d68879a842d658e4b8340aab12c` |
| `cache/source_evidence/REGISTRATION.json` | `cfde6683725ae3613cca2f3b46f55b7fd3ca9b0aac4443e297bb72cc7d2b7e6e` |
| `cache/source_evidence/PROVENANCE.json` | `ba6b1f184d7b789a9752a0941722bf378a8d6a4282ad0b76370fec70efef245e` |
| `cache/source_evidence/INJECTIONS.json` | `98a62aac521938955ac90c7a8a19e884ffd2bfc468d9a436164bf26d48299631` |
| `cache/source_evidence/INJECTIONS.npz` | `27dfc5fa47342efbaab30d32d915a7f0afd151f1cbae493bc44a813112472265` |
| `cache/source_evidence/VALIDATION.json` | `88119eee23a569f8d4781611b85659765fa31cd819b776cfe328fc4ba50fa4c0` |
| `cache/source_evidence/NESTED_ORACLE.json` | `7c817552578819589fa364211434abb34b5307f8d1a28efeda39c1637f6e2586` |
| `cache/source_evidence/vendor/MANIFEST.json` | `862341565cd495341e3bfef5912c6da9145e17d2af94ffa3c9caf0f920a25b3f` |


---
[REAL — resultados numéricos e auditoria; OPEN — aceitação científica da fonte não linear]

# ORDEM 013 — Auditoria da integração de fonte

2026-09-22T05:23:34.904279+00:00

O piloto de amostragem aninhada terminou com 24267 chamadas e sem atingir a
meta de convergência. ESS das componentes: [1.004503652320579, 20.188395533331473]; componentes
aprovadas no critério de pesos: 0 de 2400.
Esses fatores de Bayes NÃO são uma entrega científica aceita. Dobrar a taxa da forma
de onda passou no controle dos pontos relevantes; a integração estatística falhou.

No oráculo analítico, balancear componentes melhorou os pesos, mas duas sementes ainda
diferiram 0.398763109 em ln B (critério: 0,2). A etiqueta
de consistência ampla do teste não substitui essa exigência. A alternativa de amostragem
independente obteve erro máximo 0.0132514732 em quatro
controles de integrais conhecidas; isso valida seu mecanismo, não o modelo astrofísico.

## Integração independente no problema real

| rodada | propostas | avaliações dentro do prior | conjuntos com precisão mínima |
|---|---:|---:|---:|
| inicial | 4096 | 2303 | 0 / 1200 |
| adaptada | 16384 | 13021 | 0 / 1200 |

A rodada adaptada usou 24 componentes Student-t aprendidas de TODOS os pesos do piloto.
Dez por cento das propostas vêm do prior original completo; pontos fora do cubo têm
integrando zero e continuam no denominador. O prior físico, os parâmetros, o modelo e
os intervalos de ruído não foram reduzidos para conseguir passar. Aprender uma proposta
não é restringir o prior; a integral usa o quociente pela densidade da proposta.

Pior ESS na rodada adaptada: 1.00000004;
maior peso individual: 0.999999981;
maior erro estimado de Monte Carlo em ln B: 0.760440425.
Auditoria aritmética/taxa: PASS_ARITHMETIC_AND_RATE. Critérios completos de precisão:
False. Uma repetição independente da proposta final
e a calibração contínua do parâmetro de dephasing ainda faltam.

Cada conjunto simulado é analisado separadamente. Os 1200 conjuntos reutilizam 50
intervalos pareados por detector; não são eventos independentes. O4/O5 são sensibilidades
de cenário. Não houve leitura nova do evento, alteração da C6, do um.py ou do gate.
SEOBNRv4HM continua na matriz de injeções e controles; sua integração como família de
recuperação ainda está pendente. A confirmação física e qualquer significância nova
permanecem não estabelecidas. N/A — sem Lean.

Falhas operacionais preservadas: ordem de importação do dynesty local no oráculo
balanceado; booleano NumPy não serializável no primeiro registro do oráculo independente.
As cópias de bytes estão ao lado dos scripts corrigidos. Nenhuma delas foi falha de física.

## Reprodução

## Causa numérica localizada e próximo passo

A fase 22 no pico gira 35.7757518 rad na varredura de massa
60–100 massas solares e 12.2003879 rad na varredura
do spin comum −0,25 a 0,25. A fase de referência, portanto, pode criar muitas curvas
estreitas no posterior. Isso é um diagnóstico do gerador, não uma identificação física.
`PEAK_PHASE_COORDINATES.md` deriva uma mudança EXATA de variável que conserva o prior:
fase no pico uniforme em [0,π), somando as duas pré-imagens orbitais com pesos 1/2.
É essencial conservar ambos os ramos e todas as harmônicas, inclusive ímpares. A soma
é invariante à troca de ramo do argumento complexo. Implementação e validação de
quadratura ainda não foram feitas. Essa é a próxima ação justificada pelo diagnóstico;
não repetir as integrações anteriores apenas aumentando o número de amostras.

## Reprodução dos artefatos existentes

Scripts e resultados ficam em `cache/source_evidence`. Scripts create-once recusam
sobrescrever rodadas. Para nova integração usar semente/nome distintos; preservar os
priors e verificar o registro. `audit_importance_source.py <nome_da_rodada>` confere
custódia, somas diretas em precisão estendida e taxa duplicada nos pontos dominantes.
Os cálculos desta entrega terminaram; não retomar as sessões históricas como se estivessem vivas.

## Custódia

| arquivo relativo à bancada | SHA256 medido |
|---|---|
| `cache/source_evidence/source_evidence.py` | `0590f8e15bd508e525d2911fc570615671fdcdbc328399f4d7d8cb05d9816f7a` |
| `cache/source_evidence/importance_source_evidence.py` | `4671a7c402349e65f9c570527cd81a9f9a8608489a39f789e3288760ca654990` |
| `cache/source_evidence/validate_balanced_mixture.py` | `52982057783c0a717e65d540067a59505f05455b410937579f32f62e52f77578` |
| `cache/source_evidence/validate_importance_mixture.py` | `b81c4f354e390b3984c13f9e89ab7f33d016de20c4af36081547e995400bbd76` |
| `cache/source_evidence/refine_importance_proposal.py` | `510f1d5861314fe791dd1f9ae8257598f751acb55512965c2d2fd86afb7d2129` |
| `cache/source_evidence/audit_importance_source.py` | `643b54166cfcc6f6bcda56f9c2aa04efc350d7465a8322d55674cf1921696db2` |
| `cache/source_evidence/analyze_source_evidence.py` | `6723ed2ff58e409c7b47ed54e91929291f1f4d68879a842d658e4b8340aab12c` |
| `cache/source_evidence/BALANCED_ORACLE.json` | `44df2c65009e9dae001fb9b4cfcc46855d9e1e035bcc78bb36c2b4465d8802dc` |
| `cache/source_evidence/IMPORTANCE_ORACLE.json` | `ea907680a91a2238ee13e394f3cfe3add43e3eac22f17ff9321691ada31fb386` |
| `cache/source_evidence/validate_balanced_mixture.py.import_order_failed_bytes` | `5886bd625838d6b0325ca17998a4aa926e88f3e5ac2f5015f7cc17cb25e3a199` |
| `cache/source_evidence/validate_importance_mixture.py.numpy_bool_failed_bytes` | `db826f2981565726541088cefac98466cbb0ab166f37fc1b95fb3ae46e94c4e0` |
| `cache/source_evidence/REGISTRATION.json` | `cfde6683725ae3613cca2f3b46f55b7fd3ca9b0aac4443e297bb72cc7d2b7e6e` |
| `cache/source_evidence/runs/IMRPhenomXPHM_adapted_130701/IMPORTANCE_PROPOSAL.json` | `35b718570705bbbd78865d07913933116ff80efa8b41a32e4109fda12859098f` |
| `cache/source_evidence/diagnose_peak_phase.py` | `2bab71e781e00415a3f84f96bbbe4fa249b98d8a5d0bfbc0f250734509769602` |
| `cache/source_evidence/PEAK_PHASE_DIAGNOSTIC.json` | `a306a23c96d43d9c0badec6fd170b2474aabfacedc065757263220908cde6788` |
| `cache/source_evidence/PEAK_PHASE_COORDINATES.md` | `13809c80d2515421b5f3c447596a3fc7c887e53c28e8471bb07d6d7688b0aecd` |
| `cache/source_evidence/runs/IMRPhenomXPHM_seed130522_nlive256/RESULT.json` | `3f015cbd503dcf16e75797dcb9072588608689bfd84696f3ffbddea6e0aa00dd` |
| `cache/source_evidence/runs/IMRPhenomXPHM_seed130522_nlive256/AUDIT.json` | `fb4a420bd9fc1dd4e7694afc89c1d871f14dcc497e005014e59ac27d82958a23` |
| `cache/source_evidence/runs/IMRPhenomXPHM_seed130522_nlive256/samples.npz` | `b250011235394741bb0c52c6241fd901ed5a3ed0eadc8fd8ab9c9dcd3531a361` |
| `cache/source_evidence/runs/IMRPhenomXPHM_seed130522_nlive256/IMPORTANCE_PROPOSAL.json` | `4f3c2b885d8b41a2a648d70fe5072fbbe756004f1df80b3ffa81d35f8d5904f5` |
| `cache/source_evidence/importance_runs/IMRPhenomXPHM_seed130522_nlive256_seed130701_N4096/RESULT.json` | `55791e8658ea2fd519b1da722c189ba864b52b8b758cf88aba2ee1d1a26ba87c` |
| `cache/source_evidence/importance_runs/IMRPhenomXPHM_seed130522_nlive256_seed130701_N4096/RESULT_ARRAYS.npz` | `db085326c9ab220b987f3c27e6f1e26fb335d8dfff69bd0611be0d2a229b76ce` |
| `cache/source_evidence/importance_runs/IMRPhenomXPHM_seed130522_nlive256_seed130701_N4096/START.json` | `b4bf2033bfa6fcb507ce75c26cd38f3d7613c235e1f41f354357895c1a3085c3` |
| `cache/source_evidence/importance_runs/IMRPhenomXPHM_adapted_130701_seed130707_N16384/RESULT.json` | `8b198ff8a8822427601a0882757021ed0dc41f62492b36a801ee4d5148039a85` |
| `cache/source_evidence/importance_runs/IMRPhenomXPHM_adapted_130701_seed130707_N16384/RESULT_ARRAYS.npz` | `4002a5182e3e7259deac745c28b76d72c5822e7274a79db98500f35059be39db` |
| `cache/source_evidence/importance_runs/IMRPhenomXPHM_adapted_130701_seed130707_N16384/AUDIT.json` | `af6124acb779b40d71861015c44e5cd70b8f4db2034bab59ce5fd6ce6ede722f` |
| `cache/source_evidence/importance_runs/IMRPhenomXPHM_adapted_130701_seed130707_N16384/START.json` | `6e3ac0f1f9fd4d28c0761e8ba9940e33cedf572ab0f5aabebcb4776dcbec3963` |
| `record_source_evidence_audit.py` | `0201643bf53b4d05f1fa53c67a19f08654129a1102f86b8abe3ca4add1c48bda` |


---
[REAL — 2026-09-22T05:40:08.555646+00:00] Mudança para fase no pico validada em duas famílias e dois pontos de fonte por família. Erro máximo de integral ao mudar coordenadas: 3.4106051316484809e-13; erro máximo ao omitir um ramo: 73.675049210612428. Marginal da proposta conferida por quadratura: 8.4127149690971237e-12. Rodada phase_runs/IMRPhenomXPHM_seed130801_N1024 em execução na sessão85465; sete parâmetros integrados, fase em quadratura e seis em amostragem. Evidência científica ainda não aceita. Ver C5_PHASE_INTEGRATION_START.json.


---
[REAL — controles numéricos executados; OPEN — precisão da evidência e calibração da fonte]

# ORDEM 013 — fase inteira, auditoria e intensidade contínua

Registro: 2026-09-22T05:58:28.079650+00:00. N/A — sem Lean. Nenhuma edição no um.py/kernel/casas canônicas.

## Critérios desta etapa

- **PAGO:** o piloto de fase integral terminou (1024 propostas;843 dentro do prior). As181 externas têm integrando zero e contam no denominador. São1200 dados simulados, com50 intervalos de ruído por detector reutilizados entre células; não1200 observações independentes.
- **PAGO:** soma alternativa em precisão estendida, erro máximo 4.0856207306205761e-14; taxas8192→16384Hz nos35 pontos dominantes, mudança relevante máxima 0.016328971882330734, limite0,1. Esses testes verificam a implementação, não a suficiência das amostras.
- **NÃO PAGO:** precisão da evidência. ZERO/1200 comparações passou; ESS entre1.0012363 e14.35321, contra mínimo100. Não usar os lnB desse piloto como resultado físico aceito. Fase explícita não resolveu sozinha a exploração das demais coordenadas.
- **PAGO:** proposta computacional adaptada usando igualmente todos os2400 alvos.70% mistura ajustada,20% mistura anterior,10% prior inteiro. Priors físicos, likelihood e critérios inalterados. Nova integração com2048 propostas independentes: sessão38040, último registro1008/1656 avaliações internas. Conferir o handle; este documento não promete que continuará viva.
- **PAGO:** leitura contínua de a implementada e comparada à geração direta em480 controles (32 células; duas famílias, duas fontes, quatro leituras, O4/O5; a=-0,25;0;0,37;1;2). Erro relativo máximo da onda=2.1327560997955204e-07; logL=2.1337889847927727e-05. O controle negativo de a é extensão fenomenológica de diagnóstico, não gerador GKLS físico.
- **PAGO:** em a=0/1 a nova integral recupera a anterior, diferença máxima3.4106051316484809e-13.
- **NÃO PAGO:** repetição independente, precisão suficiente da fonte, recuperação SEOB integrada, demais SNR/leituras e viés/cobertura de a contínuo. Nenhum prior de a foi escolhido pelo simples teste da nova função.

## O que se integra

Na realização condicional inteira de harmônicos já usada, h_a = h_all + (exp(-a Γ_220 t)-1) h_22 + (exp(-a Γ_440 t)-1) h_44. Cada termo usa a mesma fonte, o pico intrínseco22 e distância/polarização comuns. O amortecimento ocorre ANTES do branqueamento pela covariância do detector. Demais harmônicos ficam como estavam; não é uma derivação da taxa de cada overtone.

A integral de fase é da **verossimilhança**, (1/2π)∫L(d|η,φ,a)dφ, não uma média da forma de onda. Marginalizar uma fase orbital desconhecida não é aplicar dephasing físico nem escolher um desenrolamento quântico. As duas ramificações orbitais e todos os harmônicos gerados continuam incluídos. A força contínua altera apenas a mesma lei de amortecimento explicitamente condicional.

## Reprodução e continuação

Scripts em `cache/source_evidence`, Python WSL `/opt/pycbc_env/bin/python -B`:

```text
audit_phase_source.py IMRPhenomXPHM_seed130801_N1024 --rate --processes 6
validate_continuous_phase.py
adapt_phase_source.py fit
adapt_phase_source.py run --draws 2048 --seed 130811 --processes 6
```

Comandos acima JÁ executados/iniciados. Arquivos create-once recusam sobrescrita; reproduzir numa cópia preservada ou usar nova semente/pasta quando aplicável. Não iniciar outra cópia da sessão38040. As sessões85465 (piloto),40076 (auditoria) e45570 (validação contínua) foram observadas terminais, código0. Após a nova rodada, conferir RESULT, somas, ESS, peso máximo e erro MC antes de interpretar lnB. C6 original permanece congelada. Nenhum número foi convertido em sigma, e nenhum gate foi movido.

## Custódia medida

| arquivo relativo à bancada | SHA256 |
|---|---|
| `cache/source_evidence/audit_phase_source.py` | `43f4c78aec69f141c7c2a1bd860ed728fcbfb32ece6a7d0327cb872a1d9418bb` |
| `cache/source_evidence/adapt_phase_source.py` | `8ffc29bd4fc48d4ba622db26f6f40822a7cc9ab0e1d7dda0c5daff56e0ae5cfb` |
| `cache/source_evidence/continuous_phase_source.py` | `fe6b60367fd66c7b4f11d84b6e5922f9c0e76f19777ff0bacb323ddd17d95bed` |
| `cache/source_evidence/validate_continuous_phase.py` | `8036ac3c0210621174a5526b6dc44dc28fa4801b00d9fc00d9977e047be8d762` |
| `cache/source_evidence/CONTINUOUS_PHASE_VALIDATION.json` | `d44a0a99b02b1bb152d9b99f6b5151b8de4084fc5a15cdb2ef1af3712057e3cc` |
| `cache/source_evidence/phase_runs/REGISTRATION.json` | `a47a203a5a794048d5d71f1e6b4db7f37b7187a5cea0cb8e1a8c51960275a3fc` |
| `cache/source_evidence/phase_runs/PROPOSAL.json` | `9e58d2b73d9f7c1c8f34dbd5367020fb2abf5f148bff0595732b366710557b7d` |
| `cache/source_evidence/phase_adapted_130801/ADAPTATION.json` | `4a8524918c38193580d51bee2629949d203da576f9fc3eddce0ea304c29d37f6` |
| `cache/source_evidence/phase_adapted_130801/PROPOSAL.json` | `1aea79fc4d34bd438a9372ad48cb7ec448ffb7f4d1304cfc38d90396414717b0` |
| `cache/source_evidence/phase_runs/IMRPhenomXPHM_seed130801_N1024/RESULT.json` | `5bb92343f7b8d44e9895515c47514d079a6291e3f18d5414c2e87dcfdf6780b5` |
| `cache/source_evidence/phase_runs/IMRPhenomXPHM_seed130801_N1024/RESULT_ARRAYS.npz` | `fde2b08494ac0bb663086d5b116581841786b67763719fae3f41fee94ffeb10d` |
| `cache/source_evidence/phase_runs/IMRPhenomXPHM_seed130801_N1024/PROPOSALS.npz` | `028029d0551a5b0a34eefd4fea6ab7fadaaf2f1dbb7b7ab26f077b8b20c925b7` |
| `cache/source_evidence/phase_runs/IMRPhenomXPHM_seed130801_N1024/AUDIT.json` | `70d0b45a5e271ac0bd77c2679d8ef0d117c7816a33aae6c6a2afcafdf9145f39` |
| `cache/source_evidence/phase_runs/IMRPhenomXPHM_seed130801_N1024/AUDIT_RATE.json` | `360c2e8ab157d0f01476719ec8216e519f15e6d0c8e36e81b602ad6cf331bf09` |
| `cache/source_evidence/phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048/START.json` | `bd6f037680e1b3677c19b3c4f992f8fa069bb3cf0968cb390a61c766363c8d30` |
| `record_phase_source_progress.py` | `d9dfe36fd5a546d397dfe69bb276898c95353e3d57e5569b2012070f18c06846` |


---
[REAL — resultados numéricos; OPEN — precisão científica da fonte e calibração]

# ORDEM 013 — coordenadas de ringdown e resolução

2026-09-22T06:16:54.151116+00:00. N/A — sem Lean. O objetivo permanece a confrontação precisa, sem selecionar relógio/partição e sem mover gate.

## O que a nova rodada efetivamente mediu

**PAGO:** a rodada adaptada2048 terminou (1656 propostas no domínio); a auditoria independente de soma deu diferença máxima6.9277916736609768e-14. O controle de geração8192→16384Hz nos54 pontos dominantes deu variação relevante máxima0.015403299371428147, abaixo de0,1.

**NÃO PAGO:** ZERO/1200 comparações passou a precisão. A ESS mediana passou de2.34379764 para3.30563467 com o DOBRO de propostas; eficiência por proposta caiu de0.00228886488 para0.00161407943. 672/1200 razões mudaram mais de0,2; mudança máxima2.89545111. A média favorável de uma célula não é evidência aceita. Não repetir essa proposta inalterada como solução da precisão. Nenhuma média dos dois pilotos foi fabricada.

## Resolução em SNR alto

**PAGO:** controles em duas famílias de recuperação, três fontes, O4/O5, a=0;0,37;1, ambas as famílias/amplitudes injetadas,50 ruídos pareados por célula. A tabela conta avaliações em pontos de fonte fixados, não posteriores integrados. Critério: alteração de logL≤0,1.

| SNR | 8192→16384 passa | 16384→32768 passa | maior alteração inicial | maior alteração seguinte |
|---:|---:|---:|---:|---:|
| 40 | 144/144 | 144/144 | 0.0924766589 | 0.0640261167 |
| 200 | 83/144 | 101/144 | 0.381504837 | 0.381252705 |
| 600 | 42/144 | 69/144 | 1.92511931 | 2.0697562 |

**NÃO PAGO:** precisão uniforme para SNR200/600. As injeções8192Hz foram conservadas e apenas reescaladas em amplitude: isso isola a resolução da recuperação, mas não valida a resolução da própria injeção em SNR600. Algumas avaliações fora da região posterior podem falhar sem dominar evidência; isto deve ser medido, não presumido. Não converter essas falhas em exclusão física.

## A mudança de coordenadas e o prior

**PAGO numericamente:** a mesma fonte é agora parametrizada para a proposta por

`y = (log(f220/250Hz), log(tau220/0.004s), u_q, u_spin2, u_cosi, u_t0)`.

Os parâmetros físicos originais continuam variando.250Hz e0,004s são somente unidades de coordenada e não relógios de dephasing. A forma de onda continua sendo gerada integralmente com os parâmetros binários recuperados pela inversa; a fase orbital continua integrada sobre0..2π.

Se `M_f = M_total * F(q,s1,s2)` e `chi = chi(q,s1,s2)`, então

`log f = log omega_R(chi) - log M_total - log F + const`,
`log tau = log M_total + log F - log abs(omega_I(chi)) + const`.

A derivada de F cancela no determinante. Nas coordenadas uniformes originais, a largura de M é60 e a de s1 é0,8. Portanto:

`J = |det(dy/du)| = (48/M_total) * (dchi/ds1) * d[log(omega_R/abs(omega_I))]/dchi`.

> [nota operacional do operador — omitida no retrato público]

Verificações: 512 idas/voltas em duas famílias, erro máximo1.2234657731369225e-13; determinante por diferenças finitas independente, erro relativo3.3702774127064572e-08; 18 integrais condicionais de normalização/momentos, erro máximo6.8746619508175399e-10; grade de monotonicidade com5202 pontos. São verificações numéricas do ajuste e da spline; não se intitulam prova formal global. Controles locais continuam ativos na inferência.

O oráculo da proposta sorteou32768 pontos independentes. Normalização estimada1.02106715±0.0159460624 (erro Monte Carlo); maior desvio padronizado entre13 momentos=1.54879464. Isso testa a distribuição computacional; não é significância física.

## Execução e pendências

**EM EXECUÇÃO:** `phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048`, sessão73887; registro observado304/1473. Revalidar o handle. Não duplicar por timeout. Sessões38040,85447 e75295 foram observadas terminais com código0.

Scripts em `cache/source_evidence`, Python `/opt/pycbc_env/bin/python -B`:

```text
compare_phase_runs.py phase_runs/IMRPhenomXPHM_seed130801_N1024 phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048
audit_phase_source.py ../phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048 --rate --processes 6
check_phase_high_snr.py
validate_ringdown_coordinates.py
transport_phase_source.py fit
transport_phase_source.py oracle
transport_phase_source.py run --draws 2048 --seed 130841 --processes 6
```

Todos esses comandos já executados ou iniciados; artefatos create-once recusam sobrescrita. Reproduzir em cópia preservada. Primeiro conferir precisão da nova rodada, densidade/jacobiano, amostras externas e resolução nos pontos relevantes. Permanecem repetição, recuperação SEOB integrada, outras leituras, calibração contínua de a e resolução em SNR alto. C6 e o programa canônico não foram alterados. Nenhum lnB destes pilotos foi promovido a resultado aceito ou a sigma.

## Custódia medida

| arquivo relativo à bancada | SHA256 |
|---|---|
| `cache/source_evidence/check_phase_high_snr.py` | `4e91281611aea23ee4c3a2cdbf2cc5eddf1777f8305a2bae497157e5930b2b29` |
| `cache/source_evidence/PHASE_HIGH_SNR_CONTROLS.json` | `a1eb1dc15fdff83e6a633178aa787153d53258382014e804a941e3cf8d98fd82` |
| `cache/source_evidence/compare_phase_runs.py` | `0d75c49a79ce21ee90231994e8ed7673ca81debb201e94bb8fb9a09dd852741f` |
| `cache/source_evidence/ringdown_source_coordinates.py` | `361c7b919374325878c553d712655b74edf40ffeef23401df98c5151f76e226f` |
| `cache/source_evidence/validate_ringdown_coordinates.py` | `d0203622412eef46eaafe40a25dd64c7c9a23d084379f1be16489ca145cda4b4` |
| `cache/source_evidence/RINGDOWN_COORDINATES_VALIDATION.json` | `766b7cdb1b73084281c255ce114094354a6061a0d2fe499c867d90ecfece60ed` |
| `cache/source_evidence/transport_phase_source.py` | `5efc1eb9881a785c7ba48b3099f0005729b19cc4d5a7e38770407a1c9b560fa9` |
| `cache/source_evidence/phase_ringdown_transport/REGISTRATION.json` | `882e1e548c56e553541420ae507837f69c76b114ebc5fcb6d65a099cb6e52524` |
| `cache/source_evidence/phase_ringdown_transport/PROPOSAL.json` | `8a6243e1c11156220ee7a8a6e89cce23d9443f163165686c619ced97ca747f56` |
| `cache/source_evidence/phase_ringdown_transport/PROPOSAL_ORACLE.json` | `6ae1e34150bf08d297a7b9bf82d7924575434907abdd563f4d79bc54a2dbd4a2` |
| `cache/source_evidence/phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048/RESULT.json` | `c9ffc43fc377cc32f1e04068808fb8008c37b175b373ab58b425bdfc7b33d57c` |
| `cache/source_evidence/phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048/RESULT_ARRAYS.npz` | `4cd54d0eb221e66b91f6a1728d445e7cfa4d1eb65fb6dac83b1c2ee3e8294034` |
| `cache/source_evidence/phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048/PROPOSAL_COMPARISON.json` | `db1fa5b678b3a15d17f93cbab4f6c5019213a98f28144cd65c8ea71f6ab93d5a` |
| `cache/source_evidence/phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048/AUDIT_RATE.json` | `a9cd2026589112bc823f9766dd3e32f571cb7999faed1173c021d0a0edb37029` |
| `cache/source_evidence/phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048/START.json` | `4b6aff10f635d78da25000f980e4745901a8a71f0f131a92039804ae09a2bfe5` |
| `record_ringdown_coordinates_progress.py` | `e6d0bb547dfab6e7c8b8d340aa5457b9ee70162fd2336e73c6b5903aa64eb65f` |


---
[REAL — implementação auditada e déficits medidos; OPEN — precisão/calibração científica]

# ORDEM 013 — auditoria do transporte e resolução

2026-09-22T06:44:00.335469+00:00. N/A — sem Lean. Originais canônicos e C6 preservados.

**PAGO:** piloto em coordenadas de ringdown concluído:2048 propostas,1473 no domínio,575 com integrando zero contadas no denominador. Densidade conferida por soma direta das PDFs, erro log máximo3.5527136788005009e-15; jacobiano por diferenças finitas nos pontos dominantes, erro relativo máximo1.6648771250515892e-10. Ida/volta e suporte verificados para todas as propostas.

**PAGO:** auditoria das somas e resolução8192→16384Hz nos92 pontos dominantes, alteração relevante máxima0.015367115598905912, abaixo de0,1.

**NÃO PAGO:** ZERO/1200 razões atingiu os critérios. ESS mediana5.79428676; eficiência por proposta multiplicada por1.75285152, mas ainda insuficiente. 508/1200 razões mudaram mais de0,2 contra o piloto anterior; máximo1.4457595. Nenhuma foi promovida a evidência física ou sigma.

## Resolução estendida

**PAGO:** controles adicionais32768/65536/131072Hz, mesmas fontes/ruídos/hipóteses. Os dados injetados continuam os8192Hz originais: não se demonstrou adequação da resolução das injeções a SNR600. A tabela é de avaliações em pontos de fonte, não da região posterior.

| SNR | 32768→65536 passa | 65536→131072 passa | maior delta logL inicial | maior delta logL seguinte |
|---:|---:|---:|---:|---:|
| 40 | 144/144 | 144/144 | 0.02755232 | 0.0579619254 |
| 200 | 123/144 | 123/144 | 0.286959443 | 0.371107506 |
| 600 | 72/144 | 74/144 | 2.15906119 | 2.65821002 |

**NÃO PAGO:** resolução uniforme em alta sensibilidade. Phenom melhora no controle entre taxas, mas SEOB permanece instável em parte dos casos; não basta continuar duplicando taxa sem diagnosticar o gerador/alinhamento. Além disso, 32/144 controles locais de interpolação falharam algum SNR, máximo delta logL=0.00286003001. Interpolação, quadratura, resolução do gerador e região posterior são controles diferentes; passar um não quita os outros. A falha numérica não é exclusão da TGL.

## Próxima integração, efetivamente iniciada

**EM EXECUÇÃO:** `phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192`, sessão41895, observado1136/4299. O conjunto anterior ganhou ESS agregada49.4901384. Hipótese computacional: poucos pontos efetivos podem ajustar em excesso uma mistura6D de12 componentes. O próximo piloto usa3 componentes e8192 novas propostas; não elimina nenhum dos sete parâmetros físicos nem altera seu prior. A hipótese de melhora ainda será medida.

O oráculo de32768 amostras da proposta passou: maior desvio padronizado dos momentos=1.49896051. Isso verifica normalização/momentos computacionais, não significância astrofísica. Dez por cento da proposta continua sendo o prior original integral.

**Continuar:** revalidar sessão41895; não reiniciar por timeout. Sessões73887,95183 e81510 terminaram com código0. Após o RESULT:

```text
audit_registered_transport.py IMRPhenomXPHM_seed130861_N8192 --stage phase_ringdown_regularized
audit_phase_source.py ../phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192 --rate --processes 6
compare_phase_runs.py phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048 phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192
```

O auditor parametrizável é cópia do auditor anterior, com seleção explícita de pasta e contagem dinâmica; o original foi preservado. Os comandos de auditoria desta nova rodada ainda não foram executados, pois ela está viva. A descrição em inglês `SOURCE_INTEGRATION_METHODS.md` registra integral, priors, jacobiano, propostas externas, intensidade contínua e limites dos testes, para a entrega independente.

Faltam precisão/repetição dos fatores de Bayes, SEOB como recuperação integrada, demais leituras/SNR e calibração contínua de a. Nos SNR altos, diagnosticar as falhas persistentes antes de usar a inferência. Nenhum resultado recente move gate nem altera a C6 congelada.

## Custódia medida

| arquivo relativo à bancada | SHA256 |
|---|---|
| `cache/source_evidence/audit_transport_density.py` | `f0b95959f89510173f851cd6353888fba5dcd4994a9dd30a4f231cda81a47597` |
| `cache/source_evidence/audit_registered_transport.py` | `0f4d3c39f9f3e54aee316141daec0a66a4ad8b0e1194149469c0e9023b56c23c` |
| `cache/source_evidence/SOURCE_INTEGRATION_METHODS.md` | `7e9aaf225bb1aadba591978d9c2b9dc6b368c93616b3ec80defcc099220b937a` |
| `cache/source_evidence/refine_phase_resolution.py` | `d2968807ab5ecd7829c7ba0a32cda836a3a6a3177167b7ac9c98a649a5b3bb16` |
| `cache/source_evidence/resolution_refinement/REGISTRATION.json` | `adb18e0500f13625c68e3a560d3e3c9912a0dc7dcf7b2724476ef6e7453b29e5` |
| `cache/source_evidence/resolution_refinement/RESULT.json` | `45722efbe4c22dc22977d73cd3d4f0b594c8ee960683b5f6eeb7c14e2c82fd51` |
| `cache/source_evidence/refine_ringdown_proposal.py` | `c788e3a4c4bb4d94886a7c8fa182ee43333db539311d1922abe82fffe344e8fa` |
| `cache/source_evidence/phase_ringdown_regularized/REGISTRATION.json` | `6c167d0b6839a63cf14c6b0635079d538b14e7107d7519627e379b5341f4dd89` |
| `cache/source_evidence/phase_ringdown_regularized/PROPOSAL.json` | `8af9f27a680c1c0ef86a6a7abf48389a22ed6aac593dbc9a6b4ddbad28a0572f` |
| `cache/source_evidence/phase_ringdown_regularized/PROPOSAL_ORACLE.json` | `40d045cb4c14ec6c1791878c03b4b34865c4d2f314d81e8172a495cfbe6cbf85` |
| `cache/source_evidence/phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048/RESULT.json` | `698fea056fff1830b135dba6eb2acb6985a36a377927b946c7977741e674f04c` |
| `cache/source_evidence/phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048/RESULT_ARRAYS.npz` | `3671bfd7e0fe6d6c9bd14325d184159f31f6d2c0f3cfa82548d6a34125c95a13` |
| `cache/source_evidence/phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048/PROPOSAL_COMPARISON.json` | `e5d86fea78109a767359d4c35ab6f7ebcce5085fc56c4ea0d7b514ec23e42d9a` |
| `cache/source_evidence/phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048/DENSITY_AUDIT.json` | `068a89facdd181f47326dc731226c102b5bc58ce871e11282aef76fac6e99bba` |
| `cache/source_evidence/phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048/AUDIT_RATE.json` | `eee54c1256b17b6067e6723855b82d8ddf8ed1d1104f13c203fe3639bbafb0d0` |
| `cache/source_evidence/phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/START.json` | `c67a0c7af8ea26be5fd3dc6e4c5a4af5a950b5fc96f92313035042b9080478a9` |
| `record_transport_audit_progress.py` | `5a060a3dfdb8b259dc32e045ac7322960ff1acb014759aa439fb3097789ab9de` |


---
[REAL — correção numérica medida em cópia; OPEN — evidência integrada/calibração]

# ORDEM 013 — correção do pico de fase e diagnóstico da resolução

2026-09-22T06:58:12.989179+00:00. N/A — sem Lean. Nenhum original canônico alterado.

**PAGO:** localizada a origem das falhas de interpolação em fase no caso source90.
O pico intrínseco do modo22 deve ser independente da fase orbital, mas sua
reotimização para cada fase criava dispersão de aproximadamente10⁻¹⁰s. Usar o
mesmo pico medido em fase zero levou os controles de44 falhas em72 para zero
falhas em72. Fontes: duas famílias, três taxas32/64/128kHz, duas PSDs, duas
intensidades e três fases fora da malha; SNR40/200/600.

**PAGO:** a correção entrou somente na cópia `stable_peak_imr_model.py`.
O gerador original e a integração já registrada continuam intactos. A cópia
foi conferida contra o banco de fase com alinhamento comum: erro relativo
máximo de forma de onda=2.4754042885334018e-15; erro máximo na
log-verossimilhança=4.9476511776447296e-10, em72 controles.
Isso não atesta ainda a região inteira do prior/posterior.

**NÃO PAGO:** o erro SEOB entre resoluções não desaparece com essa correção.
Um diagnóstico adicional ajustou apenas as direções já presentes de
amplitude/polarização, fase e tempo, em SNR600 sem ruído. A coluna final foi
conferida gerando novamente a forma de onda com o deslocamento calculado.

| família | taxas (Hz) | maior resíduo após amplitude/polarização | após também fase/tempo, avaliação direta |
|---|---:|---:|---:|
| IMRPhenomXPHM | 32768 → 65536 | 0.000794202572 | 5.77101729e-06 |
| IMRPhenomXPHM | 65536 → 131072 | 0.000106419289 | 7.49973865e-07 |
| SEOBNRv4HM | 32768 → 65536 | 0.0743562681 | 0.0703238485 |
| SEOBNRv4HM | 65536 → 131072 | 0.355460383 | 0.100084503 |

Esses números são normas na métrica do ruído, não sigmas de detecção. Ajustar
fase e tempo reduz parte da diferença SEOB, mas sobra erro de forma. O teste
é pontual e não substitui integração do prior, estabilidade de evidências,
controle da resolução das injeções nem cobertura dos posteriores.

**EM EXECUÇÃO:** sessão41895, rodada8192 propostas
`phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192`, observada em
2752/4299 avaliações dentro do suporte.
Propostas externas ao suporte físico continuam contadas com integrando zero.
O diagnóstico46894 e a validação71668 terminaram com código0.

**Continuar:** revalidar sessão41895; não reiniciar por timeout.
Após RESULT, executar `audit_registered_transport.py` com
`--stage phase_ringdown_regularized`, `audit_phase_source.py` com `--rate` e
comparar com o piloto anterior via `compare_phase_runs.py` conforme o recibo
`C5_TRANSPORT_AUDIT_PROGRESS.json`. Não usar a nova cópia retroativamente.
Faltam precisão/repetição, recuperação SEOB integrada, demais leituras/SNR e
calibração contínua de a. A causa de fase foi resolvida no escopo medido;
a precisão física/estatística não foi declarada por consequência.

Descrição técnica em inglês: `cache/source_evidence/PHASE_ALIGNMENT_NUMERICS.md`.
Nenhum resultado novo é confirmação física ou conversão para5σ. C6 preservada.

## Custódia medida

| arquivo relativo à bancada | SHA256 |
|---|---|
| `cache/source_evidence/diagnose_generator_alignment.py` | `2a9e48f1481c7dedd2772ffc52e74358d71b43e665fe556507c18002e4e2b915` |
| `cache/source_evidence/generator_alignment_diagnostic/REGISTRATION.json` | `2b5b2c42ac3788b92b0e4f66a76f860606857526834620de49428c0400cd55f7` |
| `cache/source_evidence/generator_alignment_diagnostic/RESULT.json` | `8aff37d96c6089ae395133e0701b70dc56c48f03d366a4277b4c009d58958e44` |
| `cache/source_evidence/stable_peak_imr_model.py` | `378eb1aa410ded4e00f33008e878095d71561dc559119ee7bcf6da659fa4ed25` |
| `cache/source_evidence/STABLE_PEAK_MODEL_PROVENANCE.json` | `f30a9e92b8fb9fcf358880dcd7dc6e768aa4d3e1a56a836d64be4540a862905d` |
| `cache/source_evidence/validate_stable_peak_and_rate.py` | `06135e58c5fd0db0ef6b83a91ed4456a49a5861e4d2264f80368f181ef891001` |
| `cache/source_evidence/stable_peak_validation/REGISTRATION.json` | `2f86ee6ec82406b4319b11a632a04db381714388179df8d3fb398bd86b55f21f` |
| `cache/source_evidence/stable_peak_validation/RESULT.json` | `78ff213a2a001fb02221c6b27578da8270bc35ad9aa9e780b5dda87a92b73ba7` |
| `cache/source_evidence/PHASE_ALIGNMENT_NUMERICS.md` | `96ad94fa9b65121f701d9df4d6f9ebaf4ff268fc2fd842fdf4645629f78a2ed3` |
| `cache/source_evidence/coherent_imr_model.py` | `4d9e568816c3b47e8e59b2401334a1a66541247fa80ed36495949aa4f5bca497` |
| `cache/source_evidence/phase_ringdown_regularized/REGISTRATION.json` | `6c167d0b6839a63cf14c6b0635079d538b14e7107d7519627e379b5341f4dd89` |
| `record_phase_alignment_refinement.py` | `ed8f2e5cf4f1150c7a9de046f49e72240046e759ff89cf5d42bdc667127eea91` |


---
[REAL — resultados e implementação conferidos; OPEN — precisão da evidência integrada]

# ORDEM 013 — Encerramento da rodada8192 e modos nativos

Registro: 2026-09-22T07:30:29.851494+00:00. Axiomas: N/A — sem Lean.

**PAGO:** rodada8192 concluída, 4299 avaliações no suporte; as demais
propostas têm integrando zero e continuam no denominador. Auditorias de densidade e
aritmética concluídas. O controle8192→16384Hz em pontos dominantes deu máximo
|ΔlogL|=0.015231062348448177; não é cota uniforme do posterior.

**NÃO PAGO:** zero das1200 razões atinge a precisão registrada. Quantis ESS:
[1.0881740365454493, 8.282652919492387, 15.31115697461153, 25.68379858214803, 73.57686504006874]. A eficiência mediana por proposta passou de
0.0028292416 para 0.0018690377.
Portanto a mistura de três componentes não resolveu a eficiência. Em
300 casos |ΔlnB|>0,2 contra o piloto2048;
máximo=1.0942384. Erros Monte Carlo de baixa ESS
podem ser subestimados; não promover médias/quantis a resultado científico.

**PAGO:** correção do pico comum testada em504 controles, zero falhas;
erro máximo de logL em SNR40/600=[3.183231456205249e-12, 6.693881005048752e-10].
São três fontes de referência e quatro pontos do prior, não prova uniforme.

**PAGO:** reconstrução direta dos modos SEOB verificada em18 casos,
erro relativo máximo=1.5814399506254759e-16, fonte90/8192Hz.
A tentativa anterior falhou e está preservada. A cópia corrigida usa a rotação
de polarização explícita no LAL e as mesmas conversões SI do PyCBC.

**DIAGNÓSTICO:** fonte oficial da versão instalada mostra que, para fonte90,
8192 até131072Hz mantêm a mesma malha interna. A taxa262144 realmente a refina.
Isso motiva o próximo controle, mas ainda não demonstra a causa única do erro.
Código consultado: https://git.ligo.org/lscsoft/lalsuite/-/raw/2c00d8c200308422036d0a23b7c0394f7c73faad/lalsimulation/lib/LALSimIMRSpinAlignedEOB.c (commit e SHA conferidos).

**CONTINUAR:** validar um adaptador de banco de fase via modos nativos contra a
API original; então testar131072/262144/524288Hz com malha interna medida.
Não repetir a mistura8192 sem diagnóstico/adaptação. Faltam precisão/repetições,
recuperação SEOB integrada, demais leituras/SNR, viés/cobertura de intensidade
contínua e atualização do pacote. C6 e fontes canônicas preservados.

O identificador41895 deixou de existir; não há processo vivo registrado aqui.
Comandos já concluídos: refine_ringdown_proposal.py; audit_registered_transport.py
--stage phase_ringdown_regularized; audit_phase_source.py com --rate;
compare_phase_runs.py; validate_stable_phase_prior.py; direct_seob_modes.py.
Arquivos/resultados são create-once; reprodução deve usar diretório separado.

## Custódia medida

| arquivo relativo | SHA256 |
|---|---|
| cache/source_evidence/phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/RESULT.json | 240e6e53bb0451ba7bafdc9fd24f661cb5c3e01310d005422894c52ae85f885a |
| cache/source_evidence/phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/RESULT_ARRAYS.npz | 1b05254d33eb1a57c3983f012d5b1eb0b838a69455ca43d5896cca709f0dd6b0 |
| cache/source_evidence/phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/PROPOSALS.npz | 2d4303d3b5bb9524149c3dca765917154ccce5d46db7378dae6d917ffd8b02ab |
| cache/source_evidence/phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/DENSITY_AUDIT.json | 9bd3d7d9946f0884a48963f4b220a8120f460bf67c0e60efa7f13fd81fcf9b17 |
| cache/source_evidence/phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/AUDIT_RATE.json | d8acd65b6bcf40754e4e2e68476d6c0e14d2801bb99dd8912af90ee776b74b64 |
| cache/source_evidence/phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/PROPOSAL_COMPARISON.json | e04e919f7f2721ae3fc15efe0a3f88c61c2c61cc03da56e33547b423b67882a1 |
| cache/source_evidence/stable_phase_prior_controls/REGISTRATION.json | 33b4b8b58f14f0aa39fac4a809da61e40300693f6ca5bbdb2d1d07e9539504b6 |
| cache/source_evidence/stable_phase_prior_controls/RESULT.json | 5c18212d2435a7fd005ac3d1d0367458753aab4569566cfdb3b24cdebec01dcf |
| cache/source_evidence/DIRECT_SEOB_MODES_VALIDATION.json | 741fafedbbc29cf6cfe2a951aac1137c5dd10db17c033ed9153ffb162a80d410 |
| cache/source_evidence/DIRECT_SEOB_MODES_CORRECTED_VALIDATION.json | ea05dc1dbe614b54961062c302ad97b9a5cd852a969de8fbf4addfa349b1438e |
| cache/source_evidence/direct_seob_modes.py | 7cb9fd39298dd8f6dbedbf436ae42137d54a44287003a01b0e342456c8187415 |
| cache/source_evidence/LAL_INTERNAL_MESH_AUDIT.json | 95d4533c3ac5c30cd43635541dce3b2ac4b59b0d9622564e1e36af1ff2af88d9 |
| cache/source_evidence/lal_generator_source_gitlab/LALSimIMRSpinAlignedEOB.c | 6b7969bb7cbe714c4937a691838b0b82a7fcc2a199c03ee2bf5215738f1ce1b3 |
| cache/source_evidence/lal_generator_source_gitlab_LALSimInspiralGeneratorLegacy/LALSimInspiralGeneratorLegacy.c | 87a5562ec7c1c411e068e96fc31c5214049b7b3cdecd350aeb68ea33b24bfdc9 |
| record_completed_source_and_modes.py | d37520a2125989f43b5ed397136b4ec14650d82605b4336d002c94aed04011be |


---
[REAL — controles numéricos; OPEN — evidência integrada e calibração científica]

# ORDEM 013 — Malha interna medida e nova amostragem

Registro: 2026-09-22T07:45:16.709680+00:00. Axiomas: N/A — sem Lean.

**PAGO:** o adaptador de modos nativos reproduziu a API anterior em180
controles: três fontes de referência e dois pontos de prior,8192/16384Hz,
deslocamentos de pico de ambos os sinais, três fases externas ao banco,
a=0/0,37/1, O4/O5. Erro relativo máximo=6.2210712098656472e-16;
erro de logL máximo em SNR40/600=[2.9558577807620168e-12, 6.402842700481415e-10].
O pico é exatamente o da API anterior nos casos testados. Não houve troca
de família SEOB, perda de modos nem alteração do prior.

**PAGO:** na fonte90, a malha interna foi de fato refinada com taxas de saída
131072/262144/524288Hz. Razões dos passos medidos=[2.0, 1.9999999999735776].
Doze controles adicionais da API de alta taxa passaram. O banco131072 também
reproduziu os16 pontos de fase anteriores, erro relativo
6.8070632624902974e-16.

**NÃO PAGO:** convergência suficiente em alta SNR. A mudança da log-likelihood
integrada sobre fase/amplitudes, neste ponto de fonte, foi:

| taxas (Hz) | PSD | SNR40 | SNR200 | SNR600 |
|---|---|---:|---:|---:|
| 131072→262144 | O4 | 0.018844314 | 0.10277967 | 0.4291108 |
| 131072→262144 | O5 | 0.034200796 | 0.16937048 | 0.55572549 |
| 262144→524288 | O4 | 0.035898243 | 0.25244507 | 1.6064155 |
| 262144→524288 | O5 | 0.060014584 | 0.23731355 | 1.6252408 |

O limite registrado é0,1. SNR40 passa neste controle;200/600 falham.
A malha interna fixa explicava a ausência de refinamento anterior, mas refiná-la
não resolveu a precisão: não é demonstração de causa única nem justificativa
para continuar dobrando taxas cegamente. As injeções continuam congeladas
em8192Hz; este ensaio não valida sua precisão intrínseca em alta SNR.

**PAGO COMO DIAGNÓSTICO:** a rodada8192 anterior é terminal e permanece
não aceita. Usamos suas likelihoods para comparar propostas, sem recalculá-las.
Primeiro:36 alternativas em duas metades. Depois: treinamento pela média e
pela raiz da média quadrática das densidades-alvo, com3/6/12 componentes.
Pela desigualdade de Cauchy-Schwarz, a segunda forma é a proposta ideal para
reduzir o segundo momento médio se as densidades-alvo forem conhecidas.
Aqui elas são estimadas com baixa ESS: a motivação não é prova de eficiência.

Selecionada:rms_K6, pelo maior ganho previsto
no décimo percentil, no pior dos dois grupos de validação. Esse ganho ainda é
0.8267695<1; nenhuma melhora
uniforme foi demonstrada. Ganho mediano mínimo previsto:
3.0301197, diagnóstico apenas.
Proposta:seis componentes Student-t,df30,mais10% do prior completo.
As sete coordenadas físicas continuam integradas; fase por quadratura,
distância/polarização comuns por integral analítica.

**PAGO:** teste independente de normalização/momentos32768draws:
integral=1.0111631 ±0.01577368;
maior desvio padronizado=1.2838414; erro da
densidade por fórmula independente=8.8817841970012523e-16.
Normalização aprovada não é precisão dos fatores de Bayes.

**EM EXECUÇÃO:** sessão62818,16384propostas,seed130892,
288/8554avaliações no suporte no último
registro observado. Fora do suporte:integrando zero, contado no denominador.
Não há resultado final desta rodada. O modelo/likelihood congelado não mudou;
a nova extração SEOB é instrumento de controle e não foi injetada na rodada Phenom.

**CONTINUAR:** revalidar a sessão62818; não reiniciar por timeout.
Depois de RESULT:auditar todas as densidades com `audit_registered_transport.py
--stage phase_ringdown_balanced`, auditar pesos e taxa com `audit_phase_source.py
../phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384 --rate --processes 6`,
comparar com a rodada8192. Repetição independente continua necessária, assim
como recuperação SEOB integrada, outras leituras/SNR, posterior contínuo de a,
viés/cobertura e pacote para reprodução. C6 preservada; nenhuma confirmação ou5σ.

Reprodução dos novos controles:create-once `validate_native_seob_phase.py`,
`refine_native_internal_mesh.py`, `diagnose_proposal_efficiency.py`,
`diagnose_balanced_proposal.py`. Proposta:`refine_balanced_source_proposal.py`
nas etapas fit,oracle,run --draws 16384 --seed 130892 --processes 6.
Para repetir resultados concluídos, usar diretório separado; não sobrescrever.

## Custódia medida

| arquivo relativo à bancada | SHA256 |
|---|---|
| record_native_mesh_and_balanced_start.py | 4c55fb0c342bbfc3c3a62207b7e1fda52f144b423b9e9affd83d408b8ee8ce6e |
| cache/source_evidence/native_seob_phase_source.py | bb2db74e009d014dcdffa50ac6e4368ea88deff2e3f86f2a5e9fc467570ccd5b |
| cache/source_evidence/validate_native_seob_phase.py | 8f7d80665a37e847fa7d5dfc342caa67ae38448414420c67838b9322dcdc9313 |
| cache/source_evidence/refine_native_internal_mesh.py | 7f152a8472e05adfe3056927e4b0402b569ff2f086d8483cc33cde27327414a3 |
| cache/source_evidence/diagnose_proposal_efficiency.py | ea4174d9a4a0bc221511e5ed7ced43b0f3809afaedf588b5abf72f4d97da2e5a |
| cache/source_evidence/diagnose_balanced_proposal.py | 79d46b2a6a125012469a8bc094f19d819a5ced4c8c6c18fbde934f04bc96c4d0 |
| cache/source_evidence/refine_balanced_source_proposal.py | af03ff79b21a73fd6554ff36c6da6a0b5274b00e57d82c3f422cee0d6a918d2b |
| cache/source_evidence/direct_seob_modes.py | 7cb9fd39298dd8f6dbedbf436ae42137d54a44287003a01b0e342456c8187415 |
| cache/source_evidence/native_seob_phase_validation/REGISTRATION.json | 64f44d5096f6278ec1e72957faea14b0214fc3ebb4a8ca530c7b7afaa914dc28 |
| cache/source_evidence/native_seob_phase_validation/RESULT.json | 106704c909943a3001dacba8fa6f393fd77a1081c550e47afa6f94de3ea4fba3 |
| cache/source_evidence/native_internal_mesh_refinement/REGISTRATION.json | 182314fc0178e28d91a2e4ce031b8630430a8e4e73005da7f25d2ded51503262 |
| cache/source_evidence/native_internal_mesh_refinement/RESULT.json | e63ea3023e30245f70d02f08411d16a47f7a04417bc0a56edbdbd99acafb4f1d |
| cache/source_evidence/proposal_efficiency_diagnostic/REGISTRATION.json | 5114891072a37d8f01b4c4f37fe058850edbb3fa2666dd9a8228168607b4d920 |
| cache/source_evidence/proposal_efficiency_diagnostic/RESULT.json | 5dc050c75b225edb18257ce4436b364cfaf6d34d716c07cbe13b9bfb3b10d4bc |
| cache/source_evidence/balanced_proposal_diagnostic/REGISTRATION.json | 14e07d4405203e9d05a210f162d33a9feaac6b2b3f6fb8b3014c3d42eb5a9488 |
| cache/source_evidence/balanced_proposal_diagnostic/RESULT.json | 981ff3affc26a0953841dbe0b4c8404f03e68a16e47de74f486628ddcac5b68d |
| cache/source_evidence/phase_ringdown_balanced/PROPOSAL.json | bce89a73bcbd5ff4c003d7032e066b27976cf67c7d119fd1cf8323d1591e663a |
| cache/source_evidence/phase_ringdown_balanced/REGISTRATION.json | 4c3464405e77139fa96198a7027e91256534fce6f80d2b7da7a09360262ed805 |
| cache/source_evidence/phase_ringdown_balanced/PROPOSAL_ORACLE.json | 5d877d41a7a9393a7ff3f5698f24572ef7229fa247f65d6b0c3abce074d211f3 |
| cache/source_evidence/phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384/START.json | 31af068d5fe43da8dc27d3171df47188ab4c1b8459c35fb84d4b9bf73405cf6a |
| cache/source_evidence/phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384/PROPOSALS.npz | ac5074d31ea48466bda6f7fd85dfaa8f9d5a3dc1a9015e783bee3373fc05c322 |
| cache/source_evidence/native_internal_mesh_refinement/integrals_131072_O4.npz | 430544b983bdd112b0659ec1716de6274827ca240333e665a643400f344ec1c7 |
| cache/source_evidence/native_internal_mesh_refinement/integrals_131072_O5.npz | 772fc81deb9b9e6c693bef6c81411fa4569aa57f4f9cce37d68e5d6b6bb197bc |
| cache/source_evidence/native_internal_mesh_refinement/integrals_262144_O4.npz | 2b5f2f43deaff55e2f222522fc305f7ce22cbf22aa726d699fa7e3d30c221989 |
| cache/source_evidence/native_internal_mesh_refinement/integrals_262144_O5.npz | 0a65dca3d1741616f4015234a5880c9916106e86a1cad98d46c7df2ac56e6c9d |
| cache/source_evidence/native_internal_mesh_refinement/integrals_524288_O4.npz | 555e2f8e25a643f27c77b7321d9f33a6919285cb6667fd526a9be25c6aee1d2a |
| cache/source_evidence/native_internal_mesh_refinement/integrals_524288_O5.npz | a37db2f191479ed8de6d7429d3c000b861822117f7171226efa0d14474074b4b |
| cache/source_evidence/native_internal_mesh_refinement/raw_131072.npz | 86e19f882752f84226759e945ab7320cb6aa8a2d56e4cca92196e2b1fb3069b3 |
| cache/source_evidence/native_internal_mesh_refinement/raw_262144.npz | 97ba8225b715a1681795ad7d65c6bacf798e0b3136d27027d28e1a9bbae4032e |
| cache/source_evidence/native_internal_mesh_refinement/raw_524288.npz | 2c2054868456678b4ba74667d22fc485cc58e74fc0b2faab0c98e7bd942b3ac2 |


---
[REAL — forma de onda reproduzida; OPEN — evidência integrada e calibração]

# ORDEM 013 — Forma de onda portátil e recuperação da segunda família

Registro: 2026-09-22T08:07:42.169719+00:00. Axiomas: N/A — sem Lean.

**PAGO:** a integral de fase/amplitudes via modos nativos SEOB reproduz a
implementação original em quatro pontos fonte/taxa,2400 componentes por ponto,
erro máximo |ΔlogL|=1.1434362306772528e-05, abaixo de0,001.
Os tempos do teste têm cache aquecido: não são benchmark independente de velocidade.
Cada ponto da nova inferência continua comparado com o gerador COMPLETO original
em três fases externas à malha, sem dispensar os critérios anteriores.

**PAGO:** proposta SEOB usa mapa de remanescente e jacobiano próprios; o aprendizado
Phenom fornece apenas uma distribuição computacional inicial. Não foi usado como
prior físico. As sete coordenadas da fonte, a fase inteira e as amplitudes comuns
continuam integradas. Normalização em32768 amostras:
0.99595461 ±0.015648269; maior desvio dos13
momentos=0.9946938. A eficiência para SEOB ainda não é conhecida.

**PAGO — C7:** pacote standalone `cache/C7_NATIVE_SEOB_WAVEFORM_v1.zip`, 64766bytes,
10arquivos de conteúdo e manifesto. Dispensa memória/contexto da
bancada e dados privados. `prepare_ringdown` gera todos os modos SEOB41;
`polarizations` aplica a leitura condicional explícita, intensidade, distância e
polarização comuns, retornando strain adimensional. Não escolhe relógio físico.
As demais harmônicas ficam preservadas. β vem do cálculo em runtime.

Reprodução real em `python -I -B`:144 comparações passaram,
erro relativo máximo=4.0127806320932996e-16. Três fontes, duas taxas,
quatro leituras condicionais, três intensidades, duas escolhas de distância/rotação.
Seis entradas inválidas foram recusadas. A leitura de estado coerente é recusada
como exponencial completa porque só fornece a inclinação inicial nessa API.

**PAGO:** arquivo ZIP conferido byte a byte contra o pacote testado. Uma cópia
descartável adulterada foi recusada pelo consumidor antes dos imports científicos.
Os originais continuam intactos. Isso é controle de integridade, não aprovação
externa independente da teoria. Resultado do replay:`C7_NATIVE_SEOB_WAVEFORM/cache/replay_20260922_080209_864989/RESULT.json`.

**EM EXECUÇÃO, observado antes deste registro:**
- IMRPhenomXPHM:sessão62818, 2928/8554avaliações no suporte, `cache/source_evidence/phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384`.
- SEOBNRv4HM:sessão61984, 320/1024avaliações no suporte, `cache/source_evidence/phase_native_seob/SEOBNRv4HM_seed130901_N2048`.

Não há resultado final dessas rodadas. A primeira integra16384 propostas; a
segunda é piloto2048. Propostas fora do suporte têm integrando zero e continuam
no denominador. Os50 intervalos de ruído são reutilizados/pareados; não são1200
eventos independentes.

**NÃO PAGO:** convergência/replicação das duas famílias, viés/cobertura da intensidade
contínua, demais leituras/SNR e aceitação científica dos fatores de Bayes. Os
controles prévios de alta SNR continuam falhando; a entrega portátil não os apaga.
Dados/C6/cânone preservados. Nenhuma declaração de confirmação ou5σ.

**PRÓXIMA AÇÃO:** revalidar os dois handles acima. Só após RESULT, executar
`audit_registered_transport.py <nome_da_rodada> --stage <fase>`; a fase é
`phase_ringdown_balanced` ou `phase_native_seob`. `audit_phase_source.py
../<fase>/<nome_da_rodada> --rate --processes 2` usa o gerador original para
controle independente de taxa (SEOB é mais caro). Comparação de Phenom contra
8192 em `compare_phase_runs.py`; não comparar famílias como se fossem repetições
do mesmo estimador. Repetições por seed da mesma família permanecem necessárias.

Comandos da etapa: `run_native_seob_source.py register`, `oracle`, `run --draws
2048 --seed 130901 --processes 2`. Artefatos concluídos são create-once; reproduzir
em cópia separada, nunca sobrescrever resultados. Pacote: `python -I -B
C7_NATIVE_SEOB_WAVEFORM/reproduce.py` cria diretório de replay próprio.

## Custódia medida

| arquivo relativo | SHA256 |
|---|---|
| record_native_package_and_seob_start.py | 4eb23cc51cae962337d5a3fbf306178fea21e53d909cef32e5873efb2def2050 |
| build_native_waveform_package.py | 456643f2582fbaa20da5f6b6e1f4015f8f3ef8f8ffa8ce4d2069e494865ced72 |
| verify_native_package_integrity.py | 9747c5688e21ff0f9a290dc0de2aee0c68ada94f25b7afd87a180070fc1ff372 |
| C7_NATIVE_SEOB_WAVEFORM_PACKAGE.json | 9e68a2d2f4153c29d99a2bfbef3e9de2c8df7f25cd29b8ad83676e570d57b08c |
| C7_NATIVE_SEOB_INTEGRITY_VALIDATION.json | 3fb3c27c6671e66247a439ca6a8e437606dd4a5a4c09e168fb08a7a56b12e51d |
| C7_NATIVE_SEOB_REPLAY_VALIDATION.json | 054937a524d8a7187d661130b29d148c20903c59e6af8181283353d8f47f3288 |
| C7_NATIVE_SEOB_WAVEFORM/cache/replay_20260922_080209_864989/RESULT.json | 8262b938587c554916130fc337132fd9012541a6c7f8ad5e2516de534dd5982d |
| cache/C7_NATIVE_SEOB_WAVEFORM_v1.zip | a368ae336532096297ceb4a7a9554dbb13dc648b8024f770b94183433a1eb09d |
| C7_NATIVE_SEOB_WAVEFORM/MANIFEST.json | a8d8ab561d1b96f3826a89b458943efafdd51a092e712c2c1bdbde8036721913 |
| cache/source_evidence/native_seob_source_likelihood.py | 942000641f1c1f096319857b340357a1606df3e4b040be32e6a67e30c13a345d |
| cache/source_evidence/validate_native_source_integral.py | 2b1906606c2a037c9647a3bce182111368f61ec5c791f69b9867b3e389f80818 |
| cache/source_evidence/run_native_seob_source.py | 8255927ce5991fbad1d3817105daeba703250a0edf5a3f964d72636b5e28e7e4 |
| cache/source_evidence/native_source_integral_validation/REGISTRATION.json | 0a45412c4283b5bbac84859d0d8ebc6447234880c6e30f495ac5e0d778d77775 |
| cache/source_evidence/native_source_integral_validation/RESULT.json | e1caf33c4878a99fea1c27a1450b4c2528afc8b677fb35e7a370cb10eb32b830 |
| cache/source_evidence/phase_native_seob/REGISTRATION.json | b6ef3665b895959ecd8480434170c373bff16a7cc6502c2eb21bb1ee87acb69b |
| cache/source_evidence/phase_native_seob/PROPOSAL.json | efd8f63d0b7a7215b7f42d01a9c682cbaa69fc9fdf490eac110d5881d6da1763 |
| cache/source_evidence/phase_native_seob/PROPOSAL_ORACLE.json | d01b269df9d50f7524b41149fd58b22abd856cf9df8b7b6ac1dfda81074faf0a |
| cache/source_evidence/phase_native_seob/SEOBNRv4HM_seed130901_N2048/START.json | c68bc077955892d62533db56bb01c88b645894e90c20fa31713a81fb6cc86cd5 |
| cache/source_evidence/phase_native_seob/SEOBNRv4HM_seed130901_N2048/PROPOSALS.npz | 29df29259777dac8cab89082f85ba771bb3d1a6dfd22820808dd4f1f278183d9 |


---
[REAL — controle estatístico implementado; OPEN — precisão e calibração astrofísicas]

# ORDEM 013 — Combinação preparada das famílias de recuperação

Registro: 2026-09-22T08:29:45.984156+00:00. N/A — sem Lean novo.

**Avanço:** a mistura de evidências das duas famílias está implementada e
registrada, com prior explícito 1/2 para cada família sob ambas as hipóteses.
As simulações permanecem separadas. A mistura não faz média de ln B nem
seleciona a família mais favorável a cada hipótese.

**Resultado do controle:** em 4000 repetições de integrais analíticas,
a razão entre variância observada e prevista foi
1.02005200893. O erro de Monte Carlo
preserva o pareamento das hipóteses dentro de cada família e centra sua
influência, pois as probabilidades posteriores das famílias podem mudar.
No controle com integrandos constantes, o erro correto foi
6.8051349e-17; omitir o centramento
produziria erro espúrio 0.22999506.
Isso é teste do estimador, não resultado de ondas gravitacionais.

**Recusas verificadas:** quatro entradas inválidas; componente com ESS baixo
mesmo com erro pareado cancelado; tentativa de consumir uma rodada incompleta.
Esta última terminou com código 1 e nenhum resultado da mistura foi gravado.

**Rodadas ainda ativas, observadas via handles antes deste registro:**
- IMRPhenomXPHM: sessão 62818, 5552/8554 avaliações no suporte.
- SEOBNRv4HM: sessão 61984, 832/1024 avaliações no suporte.

**O que falta:** terminar as integrações, auditar densidade/taxa, comparar
repetições e recuperar a intensidade contínua com viés/cobertura medidos.
A mistura não apaga falhas de precisão dos componentes. Não há resultado
aceito novo de ln B ou sigma nesta etapa. Os 50 intervalos de ruído continuam
reutilizados e pareados; O4/O5 estão normalizados separadamente a SNR40.

**Próximo passo:** após os RESULT.json, executar as auditorias existentes
`audit_registered_transport.py` com as respectivas fases, e então
`combine_source_families.py run`. O registro já existe: não repetir `register`.
Não reiniciar processos vivos. A nota `cache/source_evidence/FAMILY_MIXTURE_METHOD.md`
contém derivação, limitações e comandos exatos. C6 e originais preservados.

## Custódia medida

| arquivo relativo | SHA256 |
|---|---|
| cache/source_evidence/source_family_mixture.py | 8e12185b8dc954cb9f4e3a35c9f1cd83498051c6b6735cef77a009b2c3d3dadc |
| cache/source_evidence/validate_source_family_mixture.py | 7a961051b17b1ba699c24087e9b71b51decb64580bfbec5cc700aee6f6aba237 |
| cache/source_evidence/combine_source_families.py | c70a7ad786e7bba9aa46d265ecc5035653a74fce92abe9f53f49564116028f01 |
| cache/source_evidence/FAMILY_MIXTURE_METHOD.md | 7076ceb22988140acf5dc1d214f00f6f026548c8a102ecae24b6b23089dbee14 |
| cache/source_evidence/source_family_mixture_validation/REGISTRATION.json | a6ed14c611f771c7562760f86b1f6a403583fbb9ab1d4b914035e97b7d5dd569 |
| cache/source_evidence/source_family_mixture_validation/RESULT.json | 7be90060fbe49573cbe5002532c338b1c435a573676424d50f371411bd388a15 |
| cache/source_evidence/source_family_mixture_validation/TOY_REPETITIONS.npz | efa9ebcb8b617c331ba3bd70359bbe4621bc4533dd75022400b19ff201fec763 |
| cache/source_evidence/source_family_combination/REGISTRATION.json | 86c4a6c21f5961f6d723fc1f090e8b86d654db7ab987c68d078624d12e4d8730 |
| record_family_mixture_progress.py | fa991cfb0da4786148d2ba2aecb3cc80f2a97ab2fddfffcff48153fdb7ed9e15 |


---
[REAL — piloto concluído e auditado; OPEN — precisão e calibração]

# ORDEM 013 — Piloto SEOB, adaptações recusadas e repetição registrada

Registro: 2026-09-22T08:50:58.855733+00:00. N/A — sem Lean novo.

**O piloto terminou:** processo61984, código0; 2048 propostas,
1024 avaliações dentro do suporte. As propostas restantes
têm integrando zero e permanecem no denominador. A auditoria independente
da densidade/suporte/jacobiano e aritmética passou. Erro logarítmico da
densidade=1.776356839e-15; discrepância das somas
=1.776356839e-13.

**A precisão não passou:** 0/1200 conjuntos.
ESS mínimo/mediano/máximo=1.1899212/16.242518/56.649199.
Maior peso normalizado=0.91627143. A pequena incerteza
delta de certos quocientes não vence essa reprovação. Os ln B do arquivo são
pilotos, não resultados aceitos nem significância física.

**Diagnóstico que mudou a próxima ação:** treinar no próprio piloto SEOB não
melhorou a generalização. Melhor ganho no décimo percentil, pior metade:
0.42742316 em seis dimensões e
0.39286709 no produto espectral. Ambos abaixo
de1. Foram recusadas 52 alternativas;
nenhuma rodada física usa esses ajustes. Os diagnósticos reutilizam amostras
do piloto e não são validação científica independente.

**Repetição registrada, ainda não iniciada:**16384 propostas, seed130942,
`phase_native_repeat`. A proposta é cópia byte a byte da anterior. Seu oráculo
de normalização foi reutilizado com proveniência explícita; não foi anunciado
um teste novo. `repeat_native_source.py run --processes 4` usa novas amostras
e os mesmos critérios. Iniciar quando a rodada Phenom liberar os trabalhadores.

**Ativos, confirmados via handles:**62818 (Phenom16384) e15254 (controle SEOB
com gerador original a16384Hz,196 pontos dominantes;33 tinham sido conferidos
na observação desta sessão). Não duplicar. Revalidar na próxima continuação.
O controle de taxa completo ainda não produziu resultado.

**Bibliografia:** o texto HTML posterior do próprio Milburn foi lido e
arquivado; ver `C0_MILBURN_FONTE_COMPLEMENTAR.md`. O acesso ao artigo original
de1991 e a Kay–Wald continua limitado como antes. Esse registro não altera
a partição física ou os templates em execução.

**Próxima sequência:** após Phenom terminar, auditoria da densidade e da taxa;
comparação com sua rodada8192; `combine_source_families.py run` sobre os dois
pilotos originais. A mistura continuará não aceita enquanto os componentes
falharem. A repetição SEOB nova deverá ser auditada e comparada ao piloto; não
substituir silenciosamente os caminhos já congelados no registro da mistura.
Viés/cobertura da intensidade contínua continuam pendentes. C6 e cânone intactos.

## Custódia medida

| arquivo relativo | SHA256 |
|---|---|
| cache/source_evidence/adapt_native_source_proposal.py | 48c73ef09c70d9624062788ec8cbb748a9ddba6b1ce90b3c9b05311d59f4f0f0 |
| cache/source_evidence/diagnose_native_product_proposal.py | 9980b4c852ccc07e324deff90cc95dda4b239804d9a0c609789bb8665770cc35 |
| cache/source_evidence/repeat_native_source.py | 2d04a83532735660cbdc0ad75a86f9c7208baa361c77c02dfecc537f20fbdffb |
| cache/source_evidence/phase_native_seob/SEOBNRv4HM_seed130901_N2048/RESULT.json | a6ffb35010e611439fae5e63f6e679fa3fc2c55daf6905779e78efc92b4b1529 |
| cache/source_evidence/phase_native_seob/SEOBNRv4HM_seed130901_N2048/RESULT_ARRAYS.npz | e9dd52da1e8c84fec4b54b6d6a45bfd5d178f02f66065fdd0d6c1bb75bf2037b |
| cache/source_evidence/phase_native_seob/SEOBNRv4HM_seed130901_N2048/DENSITY_AUDIT.json | de9077ff589b3ae195d8acb33a73e86f5c0cef0eb7061604d1c91c76f4ab0ec6 |
| cache/source_evidence/native_proposal_crossfit/REGISTRATION.json | 889cec30db19bb69be6c0086cbe9f4dccd47dbbdc494e52528e6b4a4fe428efd |
| cache/source_evidence/native_proposal_crossfit/RESULT.json | 524370f6f9074eaf04301bea86cec98fcfe7367cc60a409919f8017f5c6315d5 |
| cache/source_evidence/native_product_proposal_diagnostic/REGISTRATION.json | 104cfc336a8310a67e40bfb71d88df00ccfeff44dc6d5791d126ca25e6d2cd99 |
| cache/source_evidence/native_product_proposal_diagnostic/RESULT.json | 0a75c546a00c02960093ab3e7d98a3ed82a5597d0a7ac0a01bf651f71833f62a |
| cache/source_evidence/phase_native_repeat/REGISTRATION.json | f83231ac5ea421ad357f57be6e34a91c4e4e868a6a76d8bc415ed35c3ecf6dde |
| cache/source_evidence/phase_native_repeat/PROPOSAL.json | efd8f63d0b7a7215b7f42d01a9c682cbaa69fc9fdf490eac110d5881d6da1763 |
| cache/source_evidence/phase_native_repeat/PROPOSAL_ORACLE.json | f96ef558c161e5f64853b644d5b2960ee53e7d74792cfdcff09fa02d75b269c9 |
| fetch_milburn_followup.py | dee3b7b06bf4b58ccc21f450a49026a339a794066f9959ee6a3f301a90dc601e |
| C0_MILBURN_FONTE_COMPLEMENTAR.md | 1cce3f28c1e93fdddd896e1a3593f60dcd885982f0646ffef9d9773f5d5d05f9 |
| cache/literature_milburn_followup/PROVENANCE.json | a21b72d0c2e0f7a0796bfb4d72b11afc38609b7038ec42a535b028ef7e6ddb35 |
| cache/literature_milburn_followup/milburn_grqc0308021.html | 5c4d09b270bbe6b39c4505c3a24db8d09293d8deb3266f7f83509184bebbc376 |
| record_seob_pilot_and_followup.py | 16ed0f91b79ccce7ce443536cec50a6c03e2c60c3adb626950a7edaeb1d95be9 |


---
[REAL — correção numérica verificada; OPEN — convergência científica]

# ORDEM 013 — Recuperação da interpolação real

Registro: 2026-09-22T09:18:50.829512+00:00. N/A — sem alteração de Lean, um.py, Atlas ou C6.

O processo Phenom62818 terminou com código1. Foram preservados8128 vetores
completos em508 blocos;426 avaliações ainda faltavam. O diagnóstico80765
reproduziu a falha somente no índice15627 entre32 pontos: os outros31 passaram.
Os arquivos da rodada original continuam intactos e sem RESULT.json.

## Causa e correção verificadas

Para dados reais com N par, o coeficiente de Nyquist real deve multiplicar
cos(Nφ/2). O leitor antigo usava a exponencial complexa isolada e recusava
sua parte imaginária, embora devolvesse apenas a parte real. Substituir
essa exponencial pelo cosseno preserva a interpolação real anterior.
O novo leitor verifica dados/coeficientes, simetria conjugada e resíduo
imaginário. Os limites contra a forma de onda completa e a quadratura
permaneceram1e-6 relativo,0.001 em logL e1e-5 na integração de fase.

O primeiro teste da correção falhou por um erro próprio de broadcasting:
comparou matrizes(34,1,9) e(34,9), cruzando fases diferentes. Ele e seu
registro foram preservados. O teste corrigido compara formatos iguais;
erro máximo da integral gaussiana independente=2.13162820728e-14.
Oráculos cardinais N16/N17 e cosseno puro passaram; três entradas adulteradas
foram recusadas. Em dois pontos já aprovados, diferença da integral=0.
No ponto15627: erro relativo de forma de onda
5.76302935514e-08;
erro máximo logL=1.0821500922e-05;
erro de quadratura=4.10052075495e-06.
Os bancos16/32/64 concordaram dentro de0.001. Validador58463 terminou código0.

## Continuação sem apagar o ponto difícil

`phase_ringdown_real_continuation`: cópia byte a byte das16384 propostas e
dos8128 resultados anteriores, mais32 pontos recuperados;394 avaliações
novas. Denominador16384 preservado, inclusive integrandos zero fora do suporte.
As novas avaliações guardam os controles em arquivos junto aos blocos.
**Limitação:** os valores exatos dos controles dos8128 pontos antigos estavam
somente na RAM; não foram recuperados. O caminho original só escrevia um
resultado depois de seus controles passarem, mas isso não recupera seus máximos.

Ativos conferidos nesta sessão:54722(continuação Phenom,2 trabalhadores),
40860(repetição SEOB16384,4 trabalhadores),15254(auditoria SEOB original,
2 trabalhadores,135/196 na consulta). Revalidar os três handles.
O auditor da continuação recusou corretamente a ausência do resultado final.

## Sequência necessária

1. Quando54722 terminar: `audit_registered_transport.py IMRPhenomXPHM_seed130892_N16384 --stage phase_ringdown_real_continuation`;
   `audit_real_phase_continuation.py --rate --processes 2`;
   `compare_phase_runs.py phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192 phase_ringdown_real_continuation/IMRPhenomXPHM_seed130892_N16384`.
2. Quando40860 terminar: auditar densidade/taxa e comparar com o piloto SEOB2048.
   Não duplicar o processo enquanto seu handle estiver vivo.
3. A nova combinação já está registrada em `source_family_combination_real_repeat`:
   `combine_continuation_families.py run` espera ambos RESULT e DENSITY_AUDIT.
   Ela utiliza a continuação Phenom e a repetição SEOB16384, com os mesmos pesos
   das famílias e fórmulas verificadas. O registro anterior não foi alterado.
4. Precisão componente a componente, repetição independente e viés/cobertura
   de intensidade contínua ainda são necessários. Nenhum resultado desta
   correção estabelece significância física ou seleciona relógio/partição.


---
[REAL — rodada e auditorias aritméticas concluídas; OPEN — convergência e calibração]

# ORDEM 013 — Piloto Phenom completo, precisão parcial e próxima proposta

Registro: 2026-09-22T09:33:57.591395+00:00. N/A — sem mudança no cânone, no Lean ou em C6.

**Terminou:**54722,código0. Foram contabilizadas todas as16384 propostas:
8554 vetores válidos e7830 integrandos zero fora do suporte. Nenhum ponto
difícil foi descartado. O original62818 permanece falho e preservado.

**Auditorias passaram:** densidade logarítmica com erro
1.7763568394e-15; jacobiano relativo
2.00942151807e-10; erro máximo de
soma independente (inclui ESS)=2.67164068646e-12.
Erro no próprio lnB=8.71525074331e-15.

**Precisão local:**512/1200 conjuntos,
contra0/1200 na rodada8192. ESS mínimo/mediano/máximo:
2.01271029/106.811129/422.661465.
Isso não é aceitação física nem calibração:688 conjuntos continuam falhando,
e120 mudaram mais de0.2 em lnB na comparação
com8192. Maior mudança=0.9111832448.
Não combinar as simulações como eventos nem converter esses lnB em sigma.

**Controles antigos:** máximos numéricos disponíveis para426 pontos; para8128
somente o fato de terem atravessado os testes antes da gravação, conforme
implementação preservada. Essa limitação segue explícita. Os próximos blocos
guardam os controles dentro do mesmo NPZ, junto com os vetores.

**Diagnóstico da próxima amostragem:**12 candidatos comparados em duas metades,
com seleção pela eficiência prevista, nunca pelo sinal da evidência.
Venceu `rms_K6_scale1`: pior-metade, décimo percentil de ganho
1.05218204; ganho mediano
1.58857409. É previsão incerta, não precisão
conquistada. A hipótese de envelope foi testada e não venceu.

**Registrada, ainda não iniciada:**32768 propostas,seed130972,
`phase_real_refined`. Mesmos priors físicos e likelihood;70% mistura ajustada,
20% mistura anterior e10% prior completo. Oráculo independente32768/seed130850:
normalização1.0189618 ±0.0159708441;
maior desvio padronizado dos13 momentos=1.45705351.
O novo amostrador reaproveita o código existente, altera o leitor já validado
e acrescenta apenas a persistência dos controles aos blocos.

**Ativos:**40860(SEOB16384);15254(controle de resolução SEOB,186/196);
57200(controle de resolução Phenom,169/347). Revalidar os handles.
Os controles de resolução são nos pontos dominantes, não um limite global
de erro do posterior. Antes de lançar `run_real_phase_importance.py --processes 4`,
ler seus resultados; se algum reprovar, tratar a falha primeiro.

**Demais próximos passos:** concluir/auditar/comparar SEOB; executar a combinação
já registrada `combine_continuation_families.py run` somente após os dois
resultados e auditorias de densidade. Esse registro usa a continuação Phenom
16384 e SEOB16384; a nova proposta32768 não substitui esse caminho em silêncio.
Precisão integral, repetição, posterior contínuo e viés/cobertura continuam abertos.
Não repetir as cadeias C1-C4/C6/C7 já verificadas.


## Adendo 2026-09-22T09:35:04.375010+00:00 — controle SEOB concluído

[REAL]15254 terminou com código0. Controle8192→16384Hz nos196 pontos dominantes: máximo |ΔlogL|=0.080030965721221037, abaixo de0.1. PASS no escopo pontual; não é um limite global do posterior. O piloto SEOB continua0/1200 em precisão. Ativos revalidados:40860(repetição SEOB) e57200(controle Phenom,233/347). A nova rodada Phenom32768 permanece registrada, não iniciada, aguardando o controle Phenom.


---
[REAL — controles numéricos passaram; OPEN — precisão integral e calibração]

# ORDEM 013 — Refinamento iniciado e API contínua verificada

Registro: 2026-09-22T09:47:39.740096+00:00. N/A — sem alteração do cânone, Lean, Atlas ou C6.

**Controle de resolução Phenom:**57200 terminou código0;347 pontos dominantes,
8192→16384Hz. Maior |ΔlogL|=0.0136696520976<0.1.
O controle SEOB196 pontos já havia passado. São controles pontuais, não limites
globais de erro do posterior nem provas de precisão da integração de fonte.

**Nova rodada começou:**34860,quatro trabalhadores;32768 propostas,seed130972,
`phase_real_refined/IMRPhenomXPHM_seed130972_N32768`. Mesmos priors e likelihood;
a proposta numérica foi ajustada e registrada na etapa anterior. O instantâneo
de36 blocos conferiu576 vetores completos
e seus controles guardados atomicamente dentro dos NPZ. Não reiniciar o processo.
A repetição SEOB16384/seed130942 continua no handle40860,quatro trabalhadores.

**API contínua:** a função de integração de fase já existente recebeu somente
o leitor real de Nyquist, em cópia separada. Foram examinados os pontos reais
Phenom15627(o que havia interrompido a rodada) e SEOB1002(dominante no piloto),
com intensidades[-2,0,0.37,1,4],três fases fora da grade e O4/O5.
São60 controles diretos: máximo erro relativo
1.24055410548e-07; máximo erro logL
1.17639992538e-05. Os extremos a=0/1 concordaram
exatamente nas duas famílias. Intensidade negativa é extensão diagnóstica,
não afirmação de dinâmica GKLS física. Nenhum prior sobre a foi escolhido.

**O que continua faltando:** as curvas de fonte marginalizadas Z(a), além dos
dois extremos, e a calibração por injeções. Esta validação de API não entrega
viés/cobertura. Reutilizar os leitores de intervalos existentes quando houver
curvas completas; dois pontos não determinam um máximo ou um intervalo.
Intervalo truncado pelo domínio, curva sem identificação ou integração sem
precisão devem permanecer falhas visíveis, sem fabricar erro/sigma.

**Sequência:** revalidar34860 e40860. Quando terminarem, auditar densidades e
somas, conferir controles completos e comparar com as rodadas anteriores.
O controle de resolução da nova proposta deve abranger seus próprios pontos
dominantes; não herda automaticamente a aprovação dos pontos antigos.
`combine_continuation_families.py run` mantém os caminhos já registrados
(Phenom16384 + SEOB16384); não trocar pelo novo32768 sem registro separado.
A rodada Phenom16384 segue512/1200 em precisão local e120 diferençaslnB>0.2.
Não anunciar nova significância física. Restam convergência e viés/cobertura
da intensidade contínua no escopo completo.


---
[REAL — leitor e avaliador contínuos verificados; OPEN — integral/calibração físicas]

# ORDEM 013 — Curvas contínuas iniciadas

Registro:2026-09-22T10:07:23.151865+00:00. N/A — sem Lean. Cânone, Atlas e C6 preservados.

## Critérios e evidências

- **PAGO, aritmética:** `continuous_source_calibration.py` reutiliza a função
  de importância pareada existente. O erro máximo contra quadratura de
  Gauss–Legendre foi 0.726097662 erros MC;
  a covariância foi conferida por somas independentes em long double, erro
  7.94203502e-17. Propostas de integrando
  zero continuam no denominador. Não se multiplicam mocks.
- **PAGO, geometria do leitor:** reutiliza `profile_intervals`. No oráculo
  gaussiano, erro MLE=2.77555756e-16 e erro de limites
  =0.00152112919. Os nove controles recusados
  incluem curva plana, borda, ilhas desconexas, fonte dominante, NaN e ruído
  duplicado. Mock com falha não é removido para melhorar a cobertura.
- **PAGO, avaliador de forma de onda:** 3 pontos reais,
  306 comparações diretas, 17 intensidades de −4 a4
  com passo0,5. Máximo erro relativo=1.05977555e-07,
  logL=1.17639993e-05, quadratura de fase
  =4.47066679e-06. Os extremos a=0/1 reproduzem os
  checkpoints anteriores com erro 0.
  Os dois critérios de seleção SEOB apontaram ao mesmo ponto1002: por isso
  são TRÊS pontos distintos, não quatro. Não extrapolar este controle pontual
  para todo o domínio; cada ponto novo enfrenta os controles completos.
- **INICIADO, ainda NÃO PAGO:** curvas SEOB para16384 propostas,8520 válidas,
  handle19681,dois trabalhadores. Primeiros48 pontos
  completos conferidos com seus controles embutidos. O conjunto inclui todos
  os1200 mocks congelados; reutiliza as mesmas coordenadas de fonte da rodada
  binária. São novas intensidades, não novas observações independentes.
- **REGISTRADO, NÃO INICIADO:** extensão Phenom32768/22384 válidas. A rodada
  binária Phenom34860 e a SEOB40860 continuam com quatro trabalhadores cada.
- **NÃO PAGO:** viés/cobertura físicos, repetição independente das curvas,
  controle de resolução nos pontos dominantes dessas novas curvas, mistura
  das famílias e demais leituras/SNR exigidos no objetivo completo.

## Tipagem estatística

Não foi escolhido prior para a, nem alterado β. O leitor calcula intervalos
de razão de verossimilhança sobre Z(a) marginalizado nos parâmetros da fonte.
Não os chama de intervalos bayesianos nem presume cobertura por Wilks: a
cobertura precisa ser medida nas injeções. Curva plana, ilha desconexa,
intervalo truncado, grade sem resolução ou fonte sem precisão deixam a
cobertura calibrada como nula/indisponível; diagnósticos brutos permanecem.
Intensidade negativa é controle numérico, não dinâmica GKLS física.
Uma comparação passo0,5/1,0 é necessária, mas não prova resolução final:
domínio/grade maiores podem ser exigidos. O máximo deslocamento aceito do
MLE e das duas bordas nessa comparação foi registrado em0,05unidades de a.

## Continuação e reprodução

Em `cache/source_evidence`, no Python WSL `/opt/pycbc_env/bin/python -B`:

1. Revalidar os handles34860,40860,19681. Não duplicar execução viva.
2. Quando19681 terminar, conferir `EVALUATIONS_COMPLETE.json` e rodar
   `run_continuous_source_curves.py analyze --family SEOBNRv4HM`.
3. Para Phenom, registro pronto; iniciar
   `run_continuous_source_curves.py run --family IMRPhenomXPHM --workers 2`
   quando houver capacidade, e depois seu `analyze`.
4. Comparar os extremos integrados das curvas às integrais binárias respectivas
   (mesmas propostas) e fazer auditoria independente; preservam-se as exigências
   de densidade, repetição e resolução. O runner emite diagnóstico, nunca
   aceitação científica automática.
5. A mistura binária já registrada continua Phenom16384+SEOB16384. Não trocar
   silenciosamente o primeiro pelo novo32768.

Nenhum teste de natureza moveu gate; nenhum resultado novo em sigma.
Tentativas anteriores e registros congelados mantidos. Ficha de aproveitamento:
reutilizados estimador de importância, leitor de intervalos, geradores completos,
adaptador SEOB nativo, leitor Fourier real, priors, propostas e ruídos existentes.
Acrescentadas apenas a ligação para curvas contínuas, controles e execução.

## Custódia

Hashes SHA256 lidos por script:

- `cache/source_evidence/continuous_source_calibration.py`: `f206fa9237654a1369eea9c3ddd966fa2f2f1d5bfa464e4ff10ec9d252cef0fb`
- `cache/source_evidence/validate_continuous_calibration.py`: `64ea0a49fdc80ec4cd56dbfdbef8a315b2fc5bbb87afcea942e5221390431ad7`
- `cache/source_evidence/controlled_continuous_source.py`: `3373a580390ca51a7953667ed2055e83c8d58a9220119e0deb9d3a32ed0aa3c8`
- `cache/source_evidence/validate_controlled_continuous_source.py`: `3aeb109b923cf7929a9f41f7254243fde6f9b78dfcea19494cdee409bfb9cf91`
- `cache/source_evidence/run_continuous_source_curves.py`: `7473bda8e5c5a306589159c80866ea469efae9b49a98f168b91d02303062497c`
- `cache/source_evidence/continuous_calibration_validation/REGISTRATION.json`: `1b2e60cc0d886b945e3ac30f323f60cf95b12924bf2a0dda0cd2a6c063d8fbe0`
- `cache/source_evidence/continuous_calibration_validation/RESULT.json`: `9d60fdee82bcdc85f5991489121210063f7371e78fa2e1add0486b689262b455`
- `cache/source_evidence/controlled_continuous_validation/REGISTRATION.json`: `b15519af4f3d5fb139135bd8cb093402c8e619f49808bbe55db71172bff0b941`
- `cache/source_evidence/controlled_continuous_validation/RESULT.json`: `00751b1f30161d224f7a27dd8c37cbdd9f2e9d0d2a4a4f83af01e06c8cb961f9`
- `cache/source_evidence/continuous_source_curves\SEOBNRv4HM_seed130942_N16384\REGISTRATION.json`: `93ba610c6889e804952190f9b6a6e000bf7cbf86f1906cede9f951798fe94064`
- `cache/source_evidence/continuous_source_curves\IMRPhenomXPHM_seed130972_N32768\REGISTRATION.json`: `fc82a1ba786a0e0d16175d0962f26b3757e1c725ac4a051c10eb57be1b9b96c2`
- `cache/source_evidence/continuous_source_curves\SEOBNRv4HM_seed130942_N16384\START.json`: `5751d1f460859af461390b7b6835fa7f1c176486609ccf193d1877532527be7e`
- `record_continuous_curve_start.py`: `f3c63aac91ab2718ad91c67acfb6897d8727a04eb8d4b11fe871118a3f7d70d1`


---
[REAL - extremos numericos conferidos; OPEN - integrais e calibracao fisica]

# ORDEM 013 - Duas familias continuas em execucao

Registro:2026-09-22T10:16:35.443924+00:00. N/A - sem Lean. Canone, Atlas e C6 preservados.

**PAGO no escopo parcial:**96 pontos SEOB e192 Phenom confrontados com os
checkpoints binarios das mesmas coordenadas e mesmas propostas. Para cada
ponto, a=0 e a=1 nos1200 mocks:691200 comparacoes de logL, discrepancia maxima
zero. Os arquivos foram lidos em bytes uma vez, com SHA256 do mesmo conteudo.
Isto confere identidade numerica de leitores; nao cria eventos independentes
nem demonstra a precisao da integral ainda incompleta.

**PAGO, recusa:**a auditoria com --require-complete recusou ambas as rodadas
incompletas. Os retratos parciais tem full_comparison_complete=false e nao
promovem a aceitacao cientifica. Nenhuma soma parcial substituiu o N registrado.

**INICIADO:**Phenom continuo32768/22384 validas,17 intensidades,handle43367,
12 trabalhadores. Antes da partida, WSL informou48 CPUs acessiveis,carga1min
10.09 e114651380KiB de memoria disponivel. SEOB continuo19681 permanece com
2 trabalhadores; binarios34860 e40860 permanecem com4 cada. Todos revalidados
vivos na mesma rodada de registro. Nenhuma execucao duplicada ou reiniciada.

**NAO PAGO:**concluir integrais, conferir densidades e covariancia, repetir
independentemente as curvas, controlar resolucao e medir vies/cobertura.
Continuam os demais SNR/leituras do objetivo completo e os limites da C6.
Sem novo sigma e sem aceitacao fisica. A extensao nao escolhe relogio fisico,
prior sobre a ou novo beta. Negativos sao diagnosticos, nao GKLS fisica.

## Continuacao

- Revalidar34860,40860,19681,43367, usando os handles existentes.
- A auditoria util de encerramento e `audit_continuous_endpoints.py --family
  SEOBNRv4HM --require-complete` (analogamente IMRPhenomXPHM), depois de ambos
  os resultados respectivos estarem completos. Evitar repetir retratos
  parciais apenas para produzir novos arquivos.
- Ao fim de cada corrida continua, executar `run_continuous_source_curves.py
  analyze --family <familia>`. E diagnostico, nao aceitacao automatica.
- Integrais binarias concluidas exigem auditoria de densidade, comparacao de
  repeticoes e seus proprios pontos de controle de resolucao.
- Mistura binaria ja registrada continua Phenom16384+SEOB16384; nao substituir
  silenciosamente o Phenom por32768. Mistura de curvas continuas requer
  evidencia por familia com prior comum, nunca media de log-fatores.

Ficha de aproveitamento:mesmas propostas,indices,ruidos,amplitudes e geradores;
acrescentada apenas a comparacao entre checkpoints das duas leituras numericas.
Tentativas anteriores preservadas.

## Custodia - SHA256 lidos dos artefatos

- `cache\source_evidence\continuous_source_curves\SEOBNRv4HM_seed130942_N16384\endpoint_audits\20260922T101217_966853Z\RESULT.json`: `f39192a57096dfef90926ae1b6359db6b09acb79e171a73dab0dbd1eff43fd75`
- `cache\source_evidence\continuous_source_curves\IMRPhenomXPHM_seed130972_N32768\endpoint_audits\20260922T101245_712920Z\RESULT.json`: `6a2c2fdf24d66443395d2b8d2450c4f59356984f955752c1612d5bf0e717f7e0`
- `cache\source_evidence\continuous_source_curves\INCOMPLETE_GUARD_CHECK.json`: `c46aca6fd5d7e2dbfd6d0a116ff18b39c6a06b433e7cf78867301b7715b97c1c`
- `cache\source_evidence\continuous_source_curves\IMRPhenomXPHM_seed130972_N32768\START.json`: `ed47027bb6535823886093d6c44af17246c8478aadb237100506fd9196f59749`
- `cache\source_evidence\audit_continuous_endpoints.py`: `75baac0f50510952c9fb46aa7fa05073b632be6851f1ba9e3ef7f3aea406219c`


---
[REAL - aritmetica verificada; OPEN - resultados fisicos da mistura]

# ORDEM 013 - Mistura continua registrada

Registro: 2026-09-22T10:25:20.384098+00:00. N/A - sem Lean. Canone, Atlas e C6 preservados.

**PAGO:** `continuous_family_mixture.py` reaproveita `mix_statistics`, ja
validada, para cada intensidade contra a=0. O prior de familia e o mesmo em
toda a curva: metade Phenom, metade SEOB; nao foi introduzido prior sobre a.
Misturam-se Z_f(a), nunca os logaritmos e nunca os mocks.

O oraculo independente usa somas em long double, numeros diferentes de
amostras por familia, tres alvos e 17 intensidades. Maximos erros:
logZ=1.61741280091e-15, razao logaritmica=
1.884451796e-15, erro MC pareado=
8.29954645455e-18. A media incorreta de logaritmos
erra em 0.67830685282 nesse controle.
Integrandos constantes devolvem erro MC=2.64018065658e-16,
compativel com zero. A familia com precisao insuficiente continua recusada
mesmo com prior1e-10; uma bandeira otimista que contradiz o ESS e recusada.
Nao repetimos o ensaio binario de4000 realizacoes: o reaproveitamento e explicito.

**REGISTRADO / NAO EXECUTADO:** `continuous_source_family_combination` exige
os dois resultados completos, os cubos/estatisticas sob hash, as auditorias
integrais dos extremos e as auditorias de densidade das propostas respectivas.
O comando `combine_continuous_source_curves.py run` recusou corretamente os
resultados ainda ausentes. Registro separado da mistura binaria antiga:
na continua entram Phenom32768 e SEOB16384; na binaria previamente registrada
continuam Phenom16384 e SEOB16384. Nao houve substituicao silenciosa.

**NAO PAGO:** integrar as curvas em execucao, auditar, medir vies e cobertura;
repeticao continua independente e controle de resolucao dos novos dominantes;
outros SNR/leituras do objetivo completo. A combinacao preserva todas essas
pendencias. Intervalo LR90 de Z(a) marginalizado nao vira intervalo bayesiano,
e a cobertura sera aferida por celula com os50 ruidos reutilizados.

## Execucoes e proximo passo

Os handles34860,40860,19681,43367 foram revalidados vivos. Nao repetir esses
jobs nem abrir nova rodada apenas porque estao demorando. Aguardar conclusoes
para auditoria de densidade/binarios, `run_continuous_source_curves.py analyze`
e `audit_continuous_endpoints.py --family <familia> --require-complete`.
So entao rodar `combine_continuous_source_curves.py run`.
A saida combinada permanece diagnostica ate passar repeticao, resolucao e
calibracao: o codigo nao aceita fisica automaticamente.

Ficha de aproveitamento: mesmas evidencias, priors, dados e estimador centrado
de covariancia; apenas a indexacao por intensidade e a verificacao conjunta
foram acrescentadas. Sem novos sinais experimentais ou conversao para sigma.
Tentativas anteriores preservadas.

## Custodia - SHA256 lidos por script

- `cache\source_evidence\continuous_family_mixture_validation\RESULT.json`: `37342e279f0e61e94e6657ff59bdee729e9306eeeaf23247abaf30393e72074b`
- `cache\source_evidence\continuous_family_mixture_validation\REGISTRATION.json`: `d0914ba7c9e283666f51575d90a46b0dcf88a027cf76d53d6f2709271934558d`
- `cache\source_evidence\continuous_source_family_combination\REGISTRATION.json`: `d8f521ffadeb4a40b8322e92a673d1d02a698ac9c39d6af3450e761274bda22a`
- `cache\source_evidence\continuous_source_family_combination\INCOMPLETE_GUARD_CHECK.json`: `3ed94ea20e24d37823b505f7ad3603b9445d4264ed23c767fbdac87634a0136d`
- `cache\source_evidence\continuous_family_mixture.py`: `a76a8001afb21ed76a7dbac016eaa939c36c00b01c25324e03000e21a483b978`
- `cache\source_evidence\validate_continuous_family_mixture.py`: `0ddee4d4c6d14b2bd80f188635c961df68c44d594fdda359a454906587931116`
- `cache\source_evidence\combine_continuous_source_curves.py`: `b74aa70c305c66e80c3c2b9857f80c44fc7962c57f8e096366b3eab3c9c3e7b9`


2026-09-22T10:29:02.813065+00:00 [VERIFIED_WAIT] 34860: 2896/22384; 40860: 4160/8520; 19681: 240/8520; 43367: 1104/22384. Todos revalidados vivos; criterios e escopo preservados. Nenhuma estimativa cientifica parcial, novo teste ou reinicio. Proximo passo depende dos resultados completos, como registrado.


2026-09-22T10:38:50.473505+00:00 [VERIFIED_WAIT] [{"handle": 34860, "completed": 3152, "total_valid": 22384}, {"handle": 40860, "completed": 4480, "total_valid": 8520}, {"handle": 19681, "completed": 320, "total_valid": 8520}, {"handle": 43367, "completed": 1616, "total_valid": 22384}]; processos revalidados vivos, sem falha observada. Nenhum novo experimento, reinicio ou estimativa parcial de evidencia. Aguardando conclusoes para as auditorias ja registradas.


2026-09-22T10:49:44.700828+00:00 [VERIFIED_WAIT] [{"handle": 34860, "completed": 3440, "valid_draws": 22384}, {"handle": 40860, "completed": 4832, "valid_draws": 8520}, {"handle": 19681, "completed": 416, "valid_draws": 8520}, {"handle": 43367, "completed": 2176, "valid_draws": 22384}]; quatro handles revalidados vivos e em avanço. Objetivo e ORDEM 013 reconferidos. As análises registradas dependem das entradas completas; sem novo teste, reinício, estimativa parcial ou edição do cânone.


2026-09-22T10:59:02.764002+00:00 [VERIFIED_WAIT] [{"handle": 34860, "completed": 3696, "valid_draws": 22384}, {"handle": 40860, "completed": 5168, "valid_draws": 8520}, {"handle": 19681, "completed": 496, "valid_draws": 8520}, {"handle": 43367, "completed": 2688, "valid_draws": 22384}]; quatro handles vivos em cinco consultas limitadas. Interfaces dos auditores existentes conferidas; controle de resolução das novas amostras depende dos resultados completos. Sem novos scripts, testes, reinícios ou alterações no cânone.


2026-09-22T11:07:19.902651+00:00 [VERIFIED_WAIT] [{"handle": 34860, "completed": 3904, "valid_draws": 22384}, {"handle": 40860, "completed": 5424, "valid_draws": 8520}, {"handle": 19681, "completed": 560, "valid_draws": 8520}, {"handle": 43367, "completed": 3088, "valid_draws": 22384}]; seis rodadas de consulta aos handles confirmaram execuções ativas. Nenhum término ou erro observado. Aguardar resultados completos para auditorias já previstas; nenhuma nova rodada nem alteração de critérios.


2026-09-22T11:16:15.056056+00:00 [VERIFIED_WAIT] [{"handle": 34860, "completed": 4096, "valid_draws": 22384}, {"handle": 40860, "completed": 5712, "valid_draws": 8520}, {"handle": 19681, "completed": 624, "valid_draws": 8520}, {"handle": 43367, "completed": 3472, "valid_draws": 22384}]; oito consultas aos quatro handles confirmaram execuções vivas; nenhum término ou erro observado. Auditorias dependentes aguardam os resultados completos. Sem reinício, experimento adicional, estimativa científica parcial ou mudança de escopo.


2026-09-22T11:25:22.002510+00:00 [VERIFIED_WAIT] [{"handle": 34860, "completed": 4288, "valid_draws": 22384}, {"handle": 40860, "completed": 5984, "valid_draws": 8520}, {"handle": 19681, "completed": 688, "valid_draws": 8520}, {"handle": 43367, "completed": 3872, "valid_draws": 22384}]; oito consultas confirmaram os quatro handles vivos. Nenhum término ou falha observado. Mesmas integrações em andamento, sem experimento adicional nem alteração dos critérios. Auditorias dependem das entradas completas.


2026-09-22T11:34:23.253118+00:00 [VERIFIED_WAIT] [{"handle": 34860, "completed": 4480, "valid_draws": 22384}, {"handle": 40860, "completed": 6256, "valid_draws": 8520}, {"handle": 19681, "completed": 752, "valid_draws": 8520}, {"handle": 43367, "completed": 4256, "valid_draws": 22384}]; oito consultas confirmaram quatro handles vivos. Sem término ou falha observados. Mantidas as execuções, o escopo integral e as análises dependentes já previstas; nenhuma estimativa parcial de evidência científica.


2026-09-22T11:43:28.197248+00:00 [VERIFIED_WAIT] [{"handle": 34860, "completed": 4704, "valid_draws": 22384}, {"handle": 40860, "completed": 6544, "valid_draws": 8520}, {"handle": 19681, "completed": 832, "valid_draws": 8520}, {"handle": 43367, "completed": 4672, "valid_draws": 22384}]; oito consultas confirmaram os quatro handles vivos, sem término ou falha observados. Aguardando entradas completas para as auditorias previstas. Nenhum novo experimento, reinício ou movimento de critério.


2026-09-22T11:52:25.080593+00:00 [VERIFIED_WAIT] [{"handle": 34860, "completed": 4896, "valid_draws": 22384}, {"handle": 40860, "completed": 6816, "valid_draws": 8520}, {"handle": 19681, "completed": 896, "valid_draws": 8520}, {"handle": 43367, "completed": 5072, "valid_draws": 22384}]; oito consultas confirmaram os quatro handles vivos. Sem término ou falha observados. Mantidas as integrações e os critérios; as auditorias registradas aguardam entradas completas.


2026-09-22T12:01:02.710761+00:00 [VERIFIED_WAIT] [{"handle": 34860, "completed": 5072, "valid_draws": 22384}, {"handle": 40860, "completed": 7056, "valid_draws": 8520}, {"handle": 19681, "completed": 960, "valid_draws": 8520}, {"handle": 43367, "completed": 5408, "valid_draws": 22384}]; sete consultas aos quatro handles confirmaram execuções vivas. Sem término ou falha observados. Aguardar resultados completos para auditorias já registradas; nenhuma nova rodada, estimativa científica parcial ou alteração de escopo.


2026-09-22T12:38:02.750776+00:00 [VERIFIED_WAIT] [{"handle": 34860, "completed": 5904, "valid_draws": 22384}, {"handle": 40860, "completed": 8192, "valid_draws": 8520}, {"handle": 19681, "completed": 1232, "valid_draws": 8520}, {"handle": 43367, "completed": 7024, "valid_draws": 22384}]; quatro handles revalidados vivos. Nenhum término ou falha observado. Auditores existentes de densidade e comparação conferidos para a conclusão da rodada SEOB; não foram rodados sobre resultados incompletos.


---
[REAL — execução e aritmética verificadas; OPEN — precisão e calibração física]

# ORDEM 013 — Repetição SEOB concluída e mistura das famílias

Data UTC: 2026-09-22T13:04:13.360393+00:00. Axiomas: N/A — sem Lean.

## Critérios e alcance

- **PAGO — execução SEOB:** 16384 propostas, 8520 avaliações dentro do suporte e 7864 integrandos nulos fora dele. O denominador preserva todas as propostas. Priors físicos mantidos.
- **PAGO — auditoria independente de densidade e somas:** erro em log-densidade 1.7763568394e-15; erro máximo de aritmética 1.98951966013e-12. Isto verifica o cálculo, não sua convergência.
- **NÃO PAGO — precisão SEOB:** 444/1200 conjuntos passam; 756 falham. ESS entre 1.23205944318 e 344.205441085. A ampliação de 2048 para 16384 propostas deixou 49 conjuntos com mudança de ln B acima de 0,2; máximo 0.535889212199.
- **PAGO — mistura registrada:** combina Z, com prior 1/2 por família em ambas as hipóteses. Entradas: Phenom16384 seed130892 (continuação real) e SEOB16384 seed130942. Não substitui a primeira entrada pela Phenom32768 ainda em execução.
- **NÃO PAGO — precisão conjunta:** 238/1200 passam simultaneamente precisão de ambas as famílias e erro MC da mistura; nenhuma das 24 células tem todos os 50 conjuntos aprovados. Nenhum conjunto recusado foi excluído do denominador.
- **NÃO PAGO — calibração contínua, viés, cobertura, repetição e resolução completa:** permanecem requisitos. scientific_acceptance=false nos dois resultados. Não há conversão de ln B para sigma.

São 1200 conjuntos simulados que reutilizam 50 intervalos de ruído, não 1200 eventos independentes. Escopo: leitura R-B, SNR40 normalizado separadamente para O4 e O5; não é comparação a distância fixa. Não foi escolhida a partição, o relógio físico ou o desenrolamento. C6 e arquivos canônicos permaneceram intactos.

## Execuções revalidadas e dependências

- 34860: Phenom32768 binária; aguardar resultado completo para auditoria de densidade, comparação e resolução com leitor de Fourier real.
- 19681 e 43367: curvas contínuas SEOB16384 e Phenom32768; aguardar EVALUATIONS_COMPLETE.json.
- 58182: controle de resolução SEOB dos 302 pontos dominantes, original PyCBC a 16384 Hz. Ao consultar: 18 concluídos; processo vivo. Só o resultado final decide o controle. O auditor não grava PROGRESS.json.

O processo 40860 terminou; não reiniciar. A mistura binária terminou; não executar de novo. A mistura contínua é outro registro e ainda aguarda suas entradas completas.

Depois das curvas completas, usar os scripts existentes:

```text
run_continuous_source_curves.py analyze --family SEOBNRv4HM
run_continuous_source_curves.py analyze --family IMRPhenomXPHM
audit_continuous_endpoints.py --family SEOBNRv4HM --require-complete
audit_continuous_endpoints.py --family IMRPhenomXPHM --require-complete
combine_continuous_source_curves.py run
```

A última operação exige também auditorias de densidade das entradas binárias correspondentes. O auditor antigo audit_phase_source.py usa o leitor complexo: não aplicar sem adaptação aos novos casos Phenom com Nyquist real. O controle SEOB em execução mantém seu leitor já validado.

## Reprodução e aproveitamento

Resultados e registros são preservados. Scripts já usados: repeat_native_source.py, audit_registered_transport.py, compare_phase_runs.py e combine_continuation_families.py. Para nova reprodução usar diretório separado e os registros/priors congelados; não sobrescrever esta rodada. As tentativas e falhas anteriores permanecem.

Ficha de aproveitamento: reutilizadas as formas de onda, injeções, propostas registradas, somas independentes e mistura validada. Esta entrega consolida resultados existentes; não acrescenta camada ao um.py, não altera teoremas e não move o gate. Outros SNR/leituras do objetivo integral ainda estão pendentes.

## Custódia — hashes SHA256 lidos nesta rodada

- `cache\source_evidence\phase_native_repeat\SEOBNRv4HM_seed130942_N16384\RESULT.json`: `edf7270513171e3e15f2c2bf2674149112a9c76da7b89890402104a7b04ac043`
- `cache\source_evidence\phase_native_repeat\SEOBNRv4HM_seed130942_N16384\RESULT_ARRAYS.npz`: `8411f30d8bbbad96c63989f7eebb62ea609af3d1ca1cd75308e5dd75f90ba0ff`
- `cache\source_evidence\phase_native_repeat\SEOBNRv4HM_seed130942_N16384\DENSITY_AUDIT.json`: `ec124d173cf28fc3edaf51113575f6f26ae86d02634b6c1be1be9d49e607d1c8`
- `cache\source_evidence\phase_native_repeat\SEOBNRv4HM_seed130942_N16384\PROPOSAL_COMPARISON.json`: `2b20c08d7a87516a3bd4a145b0227bb72248b3915a8ed0596c1913590cea9f2b`
- `cache\source_evidence\source_family_combination_real_repeat\RESULT.json`: `016daeb721a618e7c4bfc32e6049ab26652b28581e24d55d611e5560d5044186`
- `cache\source_evidence\source_family_combination_real_repeat\RESULT_ARRAYS.npz`: `b6e25892a1e5649c0d4abc371a611b6198d0f84ae70a20770a4e5fda202de613`
- `cache\source_evidence\source_family_combination_real_repeat\REGISTRATION.json`: `343ac83372ca1ded6e66bbbc143e0b973027b26eddc235408c360ae5eba53fbd`
- `cache\source_evidence\audit_phase_source.py`: `43f4c78aec69f141c7c2a1bd860ed728fcbfb32ece6a7d0327cb872a1d9418bb`
- `cache\source_evidence\combine_continuation_families.py`: `4d5bf82f749e5bb553cb9c6f5a085d8a85ee60c4c0717fad415f33a33fcfb335`
