# Entrega F1(c) — priors físicos extras em theta fixo

[REAL — preparação] Unidade df482198-56c4-4169-ae5e-3908f5d12f2c. physical_prior.py propõe
um adaptador puro acoplado por pin ao consumidor a987 e ao backend Gaussian existente.
Não há segundo solver, nova chamada CAMB por extra, leitura implícita de arquivo ou execução.

[DERIVED — hipóteses explicitadas] H3 é uma média de janela gaussiana em beta uniforme.
H4 transporta exatamente o prior uniforme em s para delta, com lambda=ln10/5 e densidade
(lambda/0,30) exp(-lambda*delta); o deslocamento B-lambda vale somente para o integrando.
H5 usa q=1/rd, limites invertidos e densidade 1/(30*q^2), com quadratura1D escalada.
A derivação cobre a=0/subidentificação, suporte afim/C cruzada integral, prefator/medida
comum e estabilidade. A fórmula do mínimo condicional da likelihood usa B/A sem o prior.

[REAL — auditoria própria] 98 conferências de AST/custódia/metadados passaram; não são
controles numéricos. Zero imports de candidato/NumPy/SciPy/backend, zero funções especiais,
quadraturas, mínimos, controles sintéticos, WSL, rede, provedores ou dados observados.
O erro auxiliar de separadores no primeiro writer ocorreu antes das gravações e está no
recibo; nenhuma unidade científica foi lançada. Fontes e todos os14 membros do consumidor
revisado foram relidos por hash e permanecem intactos.

[OPEN — dependências declaradas] As duas funções de precisão são injetadas por um chamador
confiável: log_exp_quad_interval e positive_quad_1d. Esta entrega fixa seus alvos, contratos
de recibo/erro/orçamento e uso, mas não fornece/instala/importa/qualifica suas implementações.
É uma dependência explícita de integração futura, não uma exigência de cota uniforme CAMB
para permitir estimativas ENGINEERING_ONLY. Erros locais estimados não cobrem automaticamente
geometria, reconstrução BAO ou teoria. Nem métodos/flags/nomes/pins fazem certificado físico.

[OPEN] Revisão independente e decisão ROOT antes de consumo. O theta de fundo não foi
integrado: densidade comum50/3 permanece como metadado não aplicado. MM continua condicional
não ratificado; V1 e liberação de observações não mudam. Não há evidência, lnB, p, sigma,
veredito, AUTH, CLAIM ou proposta de campanha nesta pasta. Backups de rascunho são bytes
exatos locais; nenhum pacote congelado, memória compartilhada ou ledger foi alterado.
