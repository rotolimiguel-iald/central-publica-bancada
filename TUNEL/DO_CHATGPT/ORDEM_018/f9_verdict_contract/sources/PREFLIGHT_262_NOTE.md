# Preflight condicional das primeiras 262 equações H0DN V01

Identidade: chatgpt-codex/ordem-018/derivacoes. Unidade ORDEM018_PREFLIGHT_262_ERROR_ONLY_001. Pré-registro no mapa 458, anterior à execução; protocolo e fontes pinados. Uma execução local, sem repetição.

[REAL — engenharia por erros] As duas variantes concluíram e passaram o guard existente. Os 27 controles de integridade/recibos finais passaram; essa auditoria não reexecutou a álgebra. A parede do launcher foi 0.395544499857 s, dentro do teto duro de 120 s; worker 0.269663700135 s, CPU 0.25 s. Runtime efetivo: Python 3.14.3, NumPy 2.4.3, executável C:\Python314\python.exe; quatro variáveis de thread fixadas em 1 antes de importar NumPy. SciPy não foi usado.

## Escopo congelado

Foram consideradas duas alternativas antes de medir: conservar as 267 equações com cinco variâncias MM simbólicas; ou executar um diagnóstico numérico limitado às primeiras 262. Esta unidade escolheu somente a segunda. Não modifica seleção V01, contrato V1 nem substitui o teste científico completo.

Foram excluídas exatamente as cinco linhas finais de megamasers: data/megamaser.dat:L5, data/megamaser.dat:L6, data/megamaser.dat:L7, data/megamaser.dat:L8, data/megamaser.dat:L9. Suas variâncias requerem distâncias centrais; nenhum valor foi inventado ou aberto. Nenhum vetor y/b, centro de intercepto, ajuste, S/g, H0, evidência, ln B, poder global ou detecção foi calculado.

O baseline estelar foi extraído por AST das instruções ak…baseline do código próprio qualify_stellar_family.py, com hash do fonte. Foram usados somente seus erros/IDs pinados. O main e a família de 300 casos não foram executados. O guard singular_gaussian_v2 e FlatNuisanceGaussian foram importados sem alteração. Não houve jitter, reparo de matriz, rede, Work, modelo remoto ou instalação.

Os 178 registros estelares foram combinados com 13 dispersões de grupo, 55 variâncias calibradoras SN, 14 calibradoras SBF e dois erros de intercepto do recibo FLOW. A independência entre blocos e a receita diagonal não estelar permanecem INPUT upstream; não são afirmações de independência física medida.

Variantes predefinidas: SBF upstream com erro de m110; SBF com acréscimo independente de e(M110), estritamente condicional e não adotado como decomposição física. As duas preservam as mesmas linhas e todos os demais erros.

## Transporte e suporte

Os dois interceptos em log10 foram multiplicados por 5. A transformação T foi aplicada a C como TCTᵀ e a X, a_h e c_C como TX, Ta_h e Tc_C. As linhas ficam em magnitude; os parâmetros continuam h=log10 H0 em dex e δ_C em magnitude. O coeficiente de magnitude dos interceptos passa de −1/5 para −1, e a resposta h passa de 1 para 5. Nenhum centro foi necessário.

A eliminação racional no subset, sem recorrer à testemunha dos MM, encontrou postos X=63, [X,a_h]=64 e [X,a_h,c_C]=65. O h continua identificável algebricamente: as distâncias/grupos e calibradores fixam as magnitudes no argumento de núcleo, e os dois interceptos então fixam h. A testemunha diferencial Cefeida/TRGB permanece dentro das primeiras 262 linhas.

Nas duas variantes, C262 possui posto 190 e nulidade 72; X tem posto whitened 63. O máximo ||NᵀX_col|| foi 2.89961324058e-14, ||Nᵀa_h||=0 e ||Nᵀc_C||=9.70357609629e-15, abaixo da tolerância congelada de 1e−10. Corte relativo de C e do desenho: 1e−12; corte absoluto de C: zero. As respostas estão no suporte numérico exigido pelo módulo.

Isso qualifica somente a matriz condicional especificada e a resposta por erros. Não verifica Ly observado, completude dos sistemáticos, dependências ausentes ou validade física do mapa R-A.

## Informação projetada e erros ideais

[REAL condicional] Foi calculada apenas a informação 2×2 solicitada, após projetar os 63 nuisance comuns: I=AᵀPA, com A=(a_h,c_C). A ordem de parâmetros é (h em dex, δ_C em mag). Os autovalores abaixo dependem dessa convenção de coordenadas; não são uma métrica invariante entre unidades de parâmetros.

SBF upstream:
I = [[41298.8137152, -6065.20188028], [-6065.20188028, 2186.18216272]]
Autovalores = 1267.24066125, 42217.7552167.

SBF + e(M110) independente, condicional:
I = [[41155.9339724, -6063.82432838], [-6063.82432838, 2186.16888128]]
Autovalores = 1264.41982582, 42077.6830279.

| Variante | σ(h), dex | σ(δ_C), mag | Correlação dos parâmetros |
|---|---:|---:|---:|
| SBF_UPSTREAM_M_ONLY | 0.00639243108635 | 0.0277838016608 | 0.638312426415 |
| SBF_INDEPENDENT_M_ADDITION_CONDITIONAL | 0.00641018106161 | 0.0278127974879 | 0.639276185326 |

Esses erros são sqrt(diag(I⁻¹)), com ambas as respostas livres e os 63 nuisance projetados pela mesma medida plana. Não são posterior ajustada nem erro de H0 observado. O recibo também conserva os erros condicionais com a outra resposta fixa, discriminados por nome; não misturá-los com a tabela conjunta.

O pequeno efeito da segunda variante caracteriza somente esse acréscimo independente de erro sob o baseline. Não estabelece irrelevância de correlações SBF, não resolve a partição sistemática pendente e não escolhe uma variante científica.

## Entrega

PREFLIGHT_262_RESULT.json contém precisão integral, runtime, hashes de entradas, ranks, normas de suporte e hashes das duas C262 transformadas. Os hashes de C são identificação das matrizes montadas pelo worker, não uma validação independente delas. CLAIM.json e PREFLIGHT_262_LAUNCH.json preservam a execução única; AUDITORIA_PREFLIGHT_262.json registra a conferência posterior sem rerodada.

Próximo uso: preparação do contrato e revisão deste instrumento parcial. A rede 267, o tratamento MM, a covariância residual e as decisões físicas continuam distintos. Nenhum gate ou veredito científico foi alterado.
