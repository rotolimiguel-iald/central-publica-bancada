# F3.6 — Asimov Λ: controle 2 C16

**Estatuto:** [REAL numérico local] Fisher tangente no ponto Λ; [OPEN] worker CPL fora de Λ. Não é ajuste a dados observados nem altera o veredito V3.

O código congelado antes do recibo final (`FREEZE_PRE_RUN.json`) foi executado no WSL com CAMB 2.0.4. O mesmo vetor de resultados apareceu no ensaio exploratório e no recibo após o congelamento. O fiducial é `(H₀,ω_b,ω_c,β,w₀,wₐ)=(67,5;0,02237;0,1200;0;−1;0)`, com mν=0,06 eV, sem SH0ES. O Fisher tem 15 observáveis sintéticos e 6 parâmetros livres. O valor central é a previsão CAMB no fiducial.

| Base de R | Covariância | σβ A | σβ B′ | σβ/β | Leitura |
|---|---:|---:|---:|---:|---|
| nu V3 | corrigida D1F-01/03 | 0.01804348 | 0.01804348 | 1.4997 | UNDERPOWERED_DO_NOT_OPEN_DATA |
| nu V3 | matriz histórica V3 | 0.02179079 | igual | 1.8112 | sensibilidade histórica |
| efetivo do operador | corrigida | 24.386 | igual | >1 | quase degenerado; número fora do alcance local |

β foi calculado em runtime por `ALPHA_FINE_CODATA_2018 × √e` = 0.012031300400803. No caso principal, posto=6 e condição da Jacobiana branqueada=743.90. A diferença máxima entre as Jacobianas β de A e B′ foi 0.0e+00. Como a entalpia CPL é zero em Λ, o portão dispensa a escolha entre A/B′, o cruzamento phantom e a âncora futura **somente neste tangente**.

**Precisão:** o teste exigente de estabilidade a 0,5% falhou. Passos escalados 0,005/0,01/0,02 dão σβ no intervalo 0.01790070–0.01836213; o mínimo é 1.4878β. Todos excedem β; a parada por falta de poder é robusta ao passo testado. A derivada em β variou no máximo 1.28e-06 absoluto nos passos 5×10⁻⁵ a 2×10⁻⁴. Não atribuir precisão subpercentual ao σ pontual.

**Erratas aplicadas:** D1F-01 usa os cinco blocos correlacionados D_M–D_H da [Tabela 1 DESI DR1](https://arxiv.org/html/2404.03002); D1F-03 usa a matriz inversa do [Apêndice A de Chen, Huang & Wang](https://arxiv.org/html/1808.05724). Para D1F-V1, a resposta β usa `E_CAMB²` e sua derivada, incluindo a evolução de neutrino massivo, no lugar da dupla contagem do FundoV3. O controle mν=0 dá σβ=0.01814239. D1F-04 (convenção de l_A) não foi reconstruída separadamente.

**Limites de custódia:** a função `_dados_reais()` do pipeline V3 apareceu incidentalmente numa leitura de linhas, e a Tabela 1 DESI exibiu médias ao lado das correlações. Nenhuma média observada foi passada ao código, processada ou ajustada. Não houve injeção-recuperação com ruído, ajuste real, worker CPL fora de Λ, alteração dos originais, do `um.py` ou do gate. O selftest de precisão falhou e está preservado no recibo; as demais verificações passaram. O portão de poder recomenda **não abrir o dado**.

**Hashes lidos do artefato:** código congelado `86bae1f6a9cd31a271dc409b0b009e26cc2025e071f2182624db82aa84e60ddb`; resultado `d6fe92487ac667d0e59288df0aa6e7cc594fb0e6c9e257031741ef065af16912`; congelamento `349e8acf4407bfe9ac9642cce3d0ec3ae340f192e5e953387c8e7b843e40aaa2`; auditoria e originais em `FREEZE_PRE_RUN.json`.
