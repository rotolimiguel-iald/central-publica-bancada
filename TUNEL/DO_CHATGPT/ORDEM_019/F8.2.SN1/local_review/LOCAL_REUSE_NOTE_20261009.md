# F8.2.SN1 — reaproveitamento local para o reexame SN Ia / Chandrasekhar

Autor: codex/sn_tgl_readonly, por delegação de codex-gerente-tgl; unidade reivindicada pelo coordenador (evento 610). Consulta em 09/10/2026. Estatuto desta nota: levantamento documental e inferências explicitadas, sem cálculo observacional.

## O que já existe e muda o desenho

A consulta ao Nós Vivo F8.2 e à rota `outro.grande_atrator_e_chandrasekhar` reencontrou a rota 164, PROPOSTA: deslocamento de massa nunca testado. O grafo localiza; as fontes abaixo foram abertas. A fonte `um.py` atual, 193300–193302, mantém o item `sn_ia_chandrasekhar` em `A9_SEM_INCERTEZA`: há aritmética de `(1-beta)^(3/2)`, sem massa observada nem sigma. Isso permite reexaminar a proposta, mas não usar esse item como medida pronta.

A mudança v388 é real na fonte: `alphaOfChi=sech(chi/2)`, `betaOfChi=alphaOfChi*exp(1/2)`, monotonia e piso em intervalo limitado de profundidade; a identificação de chi com escala física continua distinta. O `um.py` (713–717, 752–762, 194681–194689) deriva a forma e lê o valor físico de alfa. `ALPHA_FINE_CODATA_2018` e a multiplicação runtime estão em 5557–5559. A pedra TheWholeIsOne liga beta a alfa e à raiz de e, mas sua docstring 105–106 explicita a justaposição da cadeia com o certificado da luz. A consulta não transforma uma lacuna desses arquivos em impossibilidade geral.

A regra X6 registrada em 07/10 preserva beta0=alpha(0)*sqrt(e) para os ritos e para o dephasing. O Teorema da Escala do artigo Ponte (1301–1343) é condicional à identificação da fronteira com o infravermelho; distingue corrida do bulk e constante da fronteira. A energia relevante para matéria densa precisa vir do processo (por exemplo, momento/energia de Fermi ou transferência), com esquema de renormalização e matching definidos. A existência da escala eletrofraca não determina por si uma escolha de mu=MZ para uma anã branca.

## A rota histórica e o limite que permanece

`tgl_paper_unified.py`, 7518–7543, define a massa por multiplicação por `(1-beta)^(3/2)`; não resolve hidrostática modificada. O stress 7546–7599 usa mu_e=2 e não modela Coulomb. A atribuição do resíduo a Coulomb está escrita no comentário, mas não é uma correção EOS calculada. O trecho 7674–7714 importa expoente luminoso 1,8 e reconhece a degenerescência do deslocamento global com o offset GLS. A linha que mede essa degenerescência chama novamente a mesma função: prova do encanamento daquele modelo, não dado independente.

O snapshot v369 contém a pergunta quase literal (2585–2596), a resposta de massa/luminosidade (2647–2706) e sua própria correção de rota (2977–2992 e 3315). É história preservada. A correção antiga impede reaproveitar o número como previsão validada; não encerra a nova pergunta sobre um mecanismo de pressão ou taxas fracas vindo da TGL atual.

## Material da teoria que merece reaproveitamento

O Tratado, Fundamentos 327–330, escreve tensor do campo escalar com termo não mínimo; 421 traz uma equação de campo; 575–586 escreve o candidato `beta/Mp² R_mu_nu F^mu_rho F^nu_rho`. Esses são candidatos documentais para uma fonte efetiva, com alcance [DECLARADO na fonte / OPEN como modelo estelar nesta revisão]. Antes de usar, reconciliar versão, sinal, normalização e regime com o cânone e suas erratas. O nome TheNonMinimalCoupling, isoladamente, não faz essa ligação: a pedra lida é sobre não minimalidade de canto algébrico.

Fundamentos 797 contém `beta²=alpha² e`, uma identidade algébrica; a interpretação em dois vértices na linha 803 não fornece, sozinha, uma taxa ou pressão. Partículas 457–461 usa `beta sin45 * 1eV` e chama 1eV de escala eletrofraca: isso não é uma derivação de captura eletrônica em matéria densa. Não foi localizada equação superfluida relevante nas seções examinadas.

## Próxima pergunta operacional sustentada por este levantamento

Construir primeiro o mapa condicional **termo TGL admitido -> energia livre/tensor total ou taxa fraca -> P(rho,T,Ye), evolução de Ye -> hidrostática/limiar -> níquel/transferência radiativa -> observável diferencial**. Cada seta deve carregar sua hipótese e incerteza. O termo é distintivo somente se sobreviver à comparação com correções eletromagnéticas/eletrofracas padrão e à projeção dos parâmetros de calibração. Nenhum 5 sigma é calculável sem amplitude física e covariância do observável. A rota pode ser proposta com resultado nulo; este levantamento não escolhe o resultado.

## Alcance e custódia

Foram pinadas 13 fontes centrais, com SHA-256 dos bytes e de cada faixa de linhas no JSON ao lado. Os artigos/Lean/programas foram lidos, sem importar nem executar programas científicos; nenhum catálogo, curva de luz, espectro ou arquivo de observações foi aberto. Literais e resultados históricos contidos nas fontes permanecem declarações dessas fontes; não foram usados para medir significância. Nenhum original, memória, quadro, mapa, Bancada ou gate foi alterado por esta subtarefa. As saídas são novas e limitadas a `local_review`.

A busca lexical no kernel e nas duas seções do Tratado é delimitada. **Não encontrar uma ponte aqui não prova que ela não exista no acervo inteiro.** Nenhum resultado anterior de laboratório ou estatística foi promovido ao escopo estelar.

## Pinos das fontes

| Fonte | SHA-256 lido dos bytes | Bytes |
|---|---|---:|
| runtime_current | `8e7b9927ceae64b8b6812019f77cca24c08296222ae7968af41baf2fe7a67dc6` | 33910631 |
| historical_sn_code | `29c92b66b2fd6b4d589adbef4de86a67f979e03964b3f7ae892732a40ab395cd` | 1216423 |
| kernel_running | `702d7352c053060ae3f2ba7602c0fcf75762b796ed7617ac6ea29248a4d3fa2f` | 6375 |
| kernel_beta_chain | `097236427302ae42857b1cfc3e89711b45f7bc34fe02e5374bc0903a34d1a608` | 12231 |
| kernel_scale | `0ed72186957c2a8a60e23499b12b259b1e90c2db9c10845eb0b9e48a79d54462` | 6891 |
| kernel_alpha | `3ed12b22f7b1bfd3ddd3017af2fad0dbe592676a75ec0d2c436bd99f97e5a4d0` | 11107 |
| kernel_action_controls | `7be4b6cf1726d3e068fa7bc515901ce8e6b4873de7f6775c05f5bb67cb6876e1` | 4010 |
| ponte_current | `98ec3d808d51e694098ae216500ab853584cb89f9eb23661128ddc1829c1b657` | 129435 |
| tratado_fundamentos | `64e9a0ed5fb17c1aa8aa6640097b63e58457b82a6ed631ee35ba72bcab213530` | 65881 |
| tratado_particulas | `5584ac8f4ce04bfd54521ea36b6b1e35a71e197691a89d32edd6bc01c2dba0b0` | 45195 |
| historical_question_erratum | `559d79fb81b0af6c0fb8c47549a0e21e3b29f4173a5b5a642f9464611b4fa217` | 286095 |
| atlas_current_reference | `43d624bf8a158e0e1617be0b53111142b522afd50661874a0cd4830f761022e5` | 8742627 |
| index_current_reference | `0b540cff38b760daf0528f0920f4123c5ac804704f1369ab3b4a7b1b2b2a6458` | 872658 |
