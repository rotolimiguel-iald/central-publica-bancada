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
