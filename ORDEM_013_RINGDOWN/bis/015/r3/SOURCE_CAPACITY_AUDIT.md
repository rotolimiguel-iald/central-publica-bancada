[REAL — leitura da fonte custodiada; OPEN — efeito do patch e equivalência com o binário]

Fonte lida, sem edição: `ORDEM_013_RINGDOWN/cache/source_evidence/lal_generator_source_gitlab/LALSimIMRSpinAlignedEOB.c`, SHA256 `6b7969bb7cbe714c4937a691838b0b82a7fcc2a199c03ee2bf5215738f1ce1b3`. O registro de proveniência aponta lalsuite `2c00d8c200308422036d0a23b7c0394f7c73faad`; a reprodução byte a byte do binário instalado ainda não foi estabelecida.

- Linhas 2060–2097: `sigReHi`, `sigImHi`, `omegaHi` e `vPhiVecHi` recebem `length = retLen + ceil(20*(1+dtau220)/(cimag(modeFreq)*deltaTHigh))` no ramo `dtau220 > 0`; o outro ramo usa fator 1. `dtau440` é lido na linha 2051, mas não entra nessa dimensão.
- Linha 2428: `hLMAllHi` é dimensionado com `sigReHi->length * nModes`.
- Linhas 2990–2996: os vetores são preenchidos até `retLen` e zerados até `sigReHi->length`.
- Linhas 3070–3083: os vetores inteiros são passados a `XLALSimIMREOBAttachFitRingdown`, juntamente com `dtau440`.
- Linhas 3128–3130: a cópia dos modos percorre `sigReHi->length`.
- Linhas 3192–3204 e 3631–3634: alocação e reamostragem posteriores também usam esse comprimento.

Consequência limitada ao texto da fonte: `REAL8Vector.length` exerce o papel de capacidade e de extensão usada pelo cálculo. Portanto, **trocar apenas as quatro expressões de alocação não é, por si, demonstravelmente um patch de capacidade que conserva a forma de onda**. Pode corrigir o aborto, mas também estende o domínio da saída e o custo. Antes de qualificar R3, é necessário auditar os maiores índices escritos/lidos em `XLALSimIMREOBAttachFitRingdown`, os limites inteiros (`UINT4`, `INT4`, `size_t`) e comparar waveform/likelihood com o binário original nas regiões em que ele é finito. O teste de 122 pontos mede robustez no conjunto registrado; não prova sozinho equivalência física.

Nenhum patch, build, ensaio científico ou gate foi movido nesta leitura. A resposta DeepSeek sobre R3 tem estatuto `[DECLARADO]` e não recebeu esta fonte; este apontamento deriva da fonte local lida diretamente.
