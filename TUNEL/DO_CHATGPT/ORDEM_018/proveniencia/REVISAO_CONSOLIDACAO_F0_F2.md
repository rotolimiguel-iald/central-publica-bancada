# Revisão da consolidação F0/F2 — ORDEM_018

[REAL da conferência documental / DERIVED condicional] Revisora: chatgpt-codex/ordem-018/proveniencia. 2026-10-06T01:10:36.554743+00:00. Versões examinadas identificadas por SHA-256 em REVISAO_CONSOLIDACAO_F0_F2.json.

## Achados acionáveis

**CONS-01 — P2: restaurar a condição BBN do cenário histórico CMB-S4.** Em ENTREGA_018_F0_RANKING.md, linha 34, sigma_Neff=0,03 e D=3,982 aparecem com o horizonte histórico corretamente limitado, mas sem a hipótese de consistência BBN. O JSON citado CALCULO_SENSIBILIDADES_SIGMAS.json distingue explicitamente o cenário de 0,03, que assume a relação BBN, do cenário de 0,09 com Yp livre. Não são o mesmo instrumento estatístico com apenas precisões diferentes.

Correção proposta: “No cenário histórico CMB-S4 **com relação de consistência BBN**, sigma_Neff=0,03 daria D=3,982; com Yp livre, o cenário histórico citado fornece sigma=0,09. Não transportar a precisão de 0,03 para BBN modificada sem um tratamento conjunto consistente.” Conservar a ressalva de encerramento do projeto e de ausência de previsão para 2030.

A relação BBN é aqui **uma condição teórica de previsão**, não prova de que o forecast reutilizou dados observados de abundâncias. A correção não proíbe uma futura likelihood conjunta com dados independentes; exige que a relação Yp–Omega_b–Neff, seus parâmetros e a eventual modificação de BBN sejam tratadas de forma consistente. Isso é distinto da sobreposição efetiva da combinação P-ACT-LB-D-He com BBN direta, já corretamente advertida no ranking.

**CONS-02 — P2: repor as hipóteses cosmológicas da temperatura.** R-F foi abreviada em ENTREGA_018_F0_RANKING.md, linha 24; F0_RANKING_REGISTRY.json, prediction de R-F; e ENTREGA_018_F2_DERIVACOES.md, linha 11. A redação passa de conservação por dephasing para T=T0(1+z) sem repetir as hipóteses que constam da fonte original F2, linha 60: base do **mesmo H dos fótons**, redshift geométrico usual e expansão adiabática.

Tr(H[H,[H,rho]])=0 estabelece que esse dissipador não muda a energia medida pelo mesmo H; sozinha, a identidade não deriva a expansão FRW, o redshift de frequências nem a existência de uma temperatura de corpo negro. Correção proposta nas três superfícies: “Dephasing na base do mesmo H conserva energia/populações; **com redshift geométrico usual e expansão adiabática**, mantém a lei térmica T=T0(1+z).” No ramo com Qgamma, conservar também a condição de corpo negro e evolução compatível do número de fótons. Não há mudança nos números nem seleção de um novo mapa.

**Não foram encontrados outros erros numéricos ou de consolidação no recorte examinado.** Os dois achados são perdas de condições na síntese; as fontes completas já continham essas condições. Não exigem repetir ritos, ajustes, cálculos de projeção ou derivação de beta.

## Pontos sustentados pela conferência

1. **Separação, significância e potência estão distinguidas.** F0/F2 não apresentam D como significância observada. Na forma Q, D continua sendo distância gaussiana esperada condicionada a fiduciais, covariância e projeção dos parâmetros, sem potência probabilística calculada. Para R-A há agora um cálculo específico de potência idealizada: o script fixa a regra bilateral |Z|>5, com alternativa Z distribuída como N(D,1), e usa P=Phi(D−5)+Phi(−D−5). Essa regra adicional permite os percentuais apresentados; eles não decorrem de D sem especificar teste.
2. **Os percentuais R-A conferem.** H0DN: D=6,017560485 e P=0,845556563. R22: D=5,000734633 e P=0,500293076. São cenários do par gaussiano idealizado com variância fixa, não a potência do contrato completo de cinco hipóteses com deslocamentos, calibrações e seleção. A própria consolidação delimita essas omissões. Nenhum centro observado foi usado na revisão dessas identidades.
3. **Dependências observacionais preservadas.** H0DN não foi multiplicado por SH0ES/CCHP como observação independente. Planck/ACT, ACT+BBN/BBN direta, R-D/R-E, temperatura combinada/SN-dualidade, TDCOSMO/Pantheon+ e JUNO/NuFIT mantêm advertências pertinentes. O catálogo de sirenes não foi somado novamente a GW170817. O zero de covariância cruzada SN–BAO aparece como hipótese, não como independência medida. A condição teórica do CONS-01 deve permanecer distinta dessas sobreposições de dados.
4. **Q e o conjunto SN/BAO foram transportados corretamente.** Não houve troca da integral pelo endpoint. Os valores arredondados 0,183, 0,030, 0,164 e 0,294 concordam com os artefatos já auditados. No mapa A, BAO tem sinal direto zero e restringe o Omega_m compartilhado; as amplitudes são próprias. B permanece uma hipótese adicional. R-E não reaproveita essa mesma amostra como evidência autônoma.
5. **Fphi corrigido.** A errata define fphi=DeltaPhi_fit/DeltaPhi_true e mantém Hfit/Hbg=fphi/(ft FD). A consolidação usa essa direção em F0, registry e F2. A duplicação do potencial ajustado implica metade da distância inferida e dobro de H, com outros fatores unitários. Os casos fphi=1 estão intactos. A ponte física permanece OPEN. O prefixo da nota original revisada foi preservado byte a byte; os cálculos originais não mudaram.
6. **2027/2030 não recebem precisão inventada.** O cenário Simons permanece associado ao levantamento completo 2025–2034, sem interpolação para 2030. CMB-S4 aparece como cenário histórico, sem promessa operacional. As metas 5/D são escalonamentos ideais das covariâncias, não cronograma, aumento simples de N ou garantia de potência. A revisão conferiu identidade dos arquivos públicos arquivados e a coerência com os recibos; não abriu novas fontes nem atestou novamente seu estado remoto.
7. **Os mapas e escopos abertos sobrevivem à síntese.** Sirenes, dualidade, lentes, crescimento e a ligação do relógio ao aparelho não ganharam previsão única por rótulo. Piso médio não virou forma radial; soma de neutrinos não foi reaberta. A norma do conjunto de calibração A31 não foi promovida a forecast do conjunto D. A entrega documental F2 não declara fechamento dessas pontes.

## Evidência, versões e limites

A conferência produziu **48 verificações**, registrou **40 arquivos por hash** e conferiu **9 entradas de referências públicas arquivadas**. O script próprio review_consolidation.py compara as 13 linhas do registry com o texto, pins de protocolo/resultado, preservação da fonte F2 revisada, identidade do resultado de forma e aritmética dos cenários já publicados nos JSONs. Não importa ou executa scripts do autor ou originais científicos.

Os hashes das três consolidações examinadas são:

- ENTREGA_018_F0_RANKING.md: `d0e139494e7dedaf5b64844e3bbf0f1ce43df1ba1214da6a79932d1ca97b9a67` (15985 bytes).
- F0_RANKING_REGISTRY.json: `f7b3133f7dffb68517e0dac82263de75a24cc2dd64baf017432defd77944841f` (10928 bytes).
- ENTREGA_018_F2_DERIVACOES.md: `26f684f3572b8aa9d7fb9ac62ccb9fe0b7f7418eb353fe8cc5b350b6522eb285` (5258 bytes).

Os demais caminhos, hashes e resultados estão em **REVISAO_CONSOLIDACAO_F0_F2.json**. Os números primordiais e de ringdown foram confrontados como artefatos de revisão fornecidos; não houve uma nova verificação física independente dessas rotas. Os arquivos HTML/tabelas arquivados foram lidos como bytes para hash, sem decodificar novos centros observados. Nenhum centro, catálogo, posterior, strain, rito, fit ou executor remoto foi aberto nesta revisão.

Este parecer vale para as versões hasheadas. Correções posteriores devem ser conferidas como nova revisão de texto, sem apagar os achados nem requerer uma nova análise observacional. Nenhum gate foi movido e nenhum novo veredito sobre a natureza foi emitido.


## Adendo de resolução das correções — 2026-10-06T01:15:19.182331+00:00

[REAL da conferência das versões corrigidas] **CONS-01 e CONS-02 resolvidos; nenhum achado acionável permanece neste recorte.** A condição de consistência BBN e a alternativa Yp livre foram repostas, distinguindo hipótese teórica de reutilização de dados. F0, registry, F2 e gerador preservam agora as hipóteses de mesmo H, redshift geométrico usual e expansão adiabática. Os campos das 13 rotas do registry coincidem com o texto atual de F0.

Foram aprovadas 12 verificações documentais adicionais, sem repetir as contas observacionais. O adendo ACT DR2 conserva sigma_Neff=0,12, D=0,995550627 e o aviso de sobreposição. Conferi a aritmética do JSON e os hashes de protocolo, resultado e HTML arquivado. Não reabri o conteúdo científico desse HTML ou centros: a extração primária de sigma é atribuída à leitura da coordenação; esta revisão sustenta identidade e aritmética.

O snapshot original permanece registrado no JSON inicial e foi recuperado por hash dos backups, com cópias idênticas em SNAPSHOT_ORIGINAL_ENTREGA_018_F0_RANKING.md, SNAPSHOT_ORIGINAL_F0_RANKING_REGISTRY.json e SNAPSHOT_ORIGINAL_ENTREGA_018_F2_DERIVACOES.md. O texto inicial deste parecer foi mantido byte a byte antes deste adendo. REVISAO_CONSOLIDACAO_F0_F2_CORRECOES.json guarda os caminhos e hashes das versões corrigidas, a origem das cópias e os 12 checks.

Versões atuais conferidas:

- ENTREGA_018_F0_RANKING.md: `759651ea9c0e7fc777916cbf06e71d9c75848d24f131d11b5399ef99da954a03`.
- F0_RANKING_REGISTRY.json: `958ba7ac87aafa6397726db6f0903434f62d3e3508bd130900ffb937d45617fb`.
- ENTREGA_018_F2_DERIVACOES.md: `d81998654ae1d8336b4b7cc9cf6c3e6a6cf04754e58de522d2106fefed816550`.
- consolidate_deliveries.py: `a4f487df66f04a6a9a0a3a30b2973b3129a296aee524bad0890510a790553ff2`.
