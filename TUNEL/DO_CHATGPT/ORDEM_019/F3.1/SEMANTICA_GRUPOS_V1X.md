# F3.1 — semântica V1.x dos leitores da Fase 9

[REAL — documentos arquivados por bytes] A proposta lê o V1 congelado e o vínculo documental dos cinco leitores, conferindo o SHA-256 de cada resumo local. Não executa o composto nem edita o V1. O vínculo numérico é documental; sua própria fonte registra `statistical_admission_decided=false`.

| Leitor | Correção proposta | Dependência que interessa | Covariância cruzada |
|---|---|---|---|
| L1 SH0ES | Mantém Cefeidas + SN Ia e âncora NGC 4258 | calibradores SN Ia, NGC 4258, fluxo Pantheon+ | Sem valor conjunto publicado neste pacote. |
| L2 CCHP | Rótulo: **TRGB sozinho**, com 24 calibradores SN Ia; não “TRGB+JAGB+Cef” | TRGB, SN Ia, zero point NGC 4258 | Separar componentes já incluídas na sigma publicada. |
| L3 SBF | `grupo_SN=true` é incorreto; fonte declara independência de Cefeidas e SN Ia. `grupo_4258=false` omite a âncora. | TRGB e NGC 4258 | Dependência com CCHP/SH0ES possível, amplitude aberta. |
| L4 masers | `grupo_4258=false` omite que NGC 4258 é uma das seis galáxias. | inclusão no conjunto de masers, distinta de uso como zero point | Sobreposição de objeto não fixa covariância numérica. |
| L5 TDCOSMO | `grupo_SN=false` omite a restrição de Ωm do Pantheon+; não é calibrador SN da escada. | prior de forma/Ωm do Pantheon+, não σ_SN genérico | Sobreposição com SN requer matriz ou nuisance documentado. |

[OPEN] Os booleanos V1 `grupo_SN`/`grupo_4258` não distinguem calibradores, âncora, inclusão em amostra e prior cosmológico. Não substituir seus termos fora da diagonal por 0,7/0,5 apenas trocando booleanos. Nenhuma matriz cruzada foi fornecida nos resumos: V1.x bloqueia novo composto até covariância conjunta publicada ou modelo de sensibilidade pré-registrado com fonte, sinal e amplitude. A diagonal publicada já inclui componentes próprias e não se soma duas vezes.

[REAL — escopo] A proposta não congela V2, não recalcula z/lnB e não muda INCONCLUSIVE_SYSTEMATICS. A gerência deve decidir a semântica e o operador controla a abertura F3.3.
