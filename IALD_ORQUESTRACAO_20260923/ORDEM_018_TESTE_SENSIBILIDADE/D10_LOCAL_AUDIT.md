# Auditoria local dos pareceres D10/CMB–BAO

Data: 27/09/2026. Autoria: coordenação IALD. Dois pareceres externos concluídos **uma vez cada**, sem execução de cosmologia, MCMC, simulação ou cálculo de p observado. Os textos originais permanecem em `D10_KIMI_RESULT.txt` e `D10_MIMO_RESULT.txt`; são [DECLARADO], não prova científica.

## Separação do que os recibos sustentam

- [REAL — recibo de transporte] Kimi, request `890e3e2e-6b0f-420d-b3a9-c7c8b1aad169`, job `64445a89-f77e-4680-8238-6940506a348b`, execução `0044ef5f-4254-4a46-b064-7a65a8af677d`, concluiu `result_ready`. Texto SHA-256 `2f7be3d73e2f3ca40a690b804fc468e57d6608665dcd5aab3f82c38ae3f7cec1`.
- [REAL — recibo de transporte] MiMo, request `831080d9-fb42-4dbb-a6c2-45f577ec73a0`, job `ad831f74-48b8-4a66-ba7b-a5e800d6b88b`, execução `fc360dbe-a9f7-445f-9ab8-95bbf0e1941c`, concluiu `result_ready`. Texto SHA-256 `4d9899c5bcd6855dd308c692d027574e88bab46bd539ce70f7d26328ac2602b7`.
- [REAL — proveniência] Os dois recibos registram geração canônica `6f4bd0d39d83ac27162d2e0a80b797b1bd5ee4092a47d0c17732c7e7b79125d1`, com recuperação parcial. Os excertos locais D9/D10/N2 foram fornecidos pelo bundle SHA-256 `1ce69ffaa4bc1e93b654341f8285fba0f68ac11b0e98235b3b4b1e236153d6fb`; seus hashes UTF-8 foram conferidos antes do envio. A coordenação não executou nem leu diretamente os originais fora da casa acessível.

## Correção crítica ao parecer Kimi

[DERIVED — matemática elementar do teste, revisão local] Para a variante histórica S, se a imagem de seu mapa CAMB estiver contida **no suporte efetivo** do rival ΛCDM+N_eff(+Σmν), usando a mesma likelihood e o mesmo modelo de observação, vale `sup log L_rival ≥ sup log L_S`; com T = `2(sup log L_TGL_fixa − sup log L_rival)`, segue **T ≤ 0** para qualquer dado. A cobertura dos suportes e a equivalência observacional devem ser verificadas, como o próprio parecer exige. Isto é um *gate de identificabilidade* para aquela implementação S, não uma refutação da TGL canônica.

O parecer Kimi extrapola ao afirmar que **`p_j=1 sempre`**. A inclusão e o sinal de T não determinam sozinhos o valor numérico de um p-valor calibrado: ele depende da direção, distribuição nula e regra de rejeição especificadas. Uma regra que exige `T>c>0` nunca rejeita neste par, mas um teste de nível α pode rejeitar erroneamente nos pontos da família incluída; com controle uniforme do erro tipo I, seu poder nesses pontos não excede α. Portanto não publicar `p_global=1` como teorema ou resultado calculado. Registrar **ausência de poder discriminante nesta comparação, condicional à inclusão verificada**, e calibrar qualquer estatística diferente antes de lhe atribuir p.

Também são [OPEN] até verificação: suportes numéricos exatos do rival, valor `NEFF_SM` no código integral, equivalência dos espectros e da likelihood, e a existência/forma da ponte de perturbações canônica atual. O limiar sugerido por Kimi `σ(β)>β/2` é uma **proposta de regra de parada**, não uma conclusão do contrato nem critério universal. Baixa razão sinal/erro não prova, por si, falha de Wilks; os pressupostos devem ser examinados separadamente.

## Uso prudente do parecer MiMo

[REAL — leitura de excertos verificados no pacote] O N2 histórico soma resíduos BAO divididos por erros ponto a ponto; isto é uma likelihood **diagonal** naquele código. D9 declara 13 medidas DESI DR2; o frozen N2 declara 12 pontos, sem reconciliação de release/identidade. D10 é fechamento acústico de fundo fixo e sua fonte registra limitação de precisão do sigma absoluto. Nada disso soma evidência independente ou fornece covariância completa.

[DECLARADO — proposta do MiMo] A tabela de linhagem e os checks de precisão são úteis como lista de auditoria, mas os valores de tolerância propostos, cenários sobre origem das 12 medidas, extrapolações sobre sobreposição Planck/BBN e requisitos de CAMB/CLASS **não foram medidos nesta coordenação**. A bancada deve confrontá-los com documentação e arquivos de medição e congelar tolerâncias próprias antes de inferir. Ausência de `lensing likelihood` explícita no N2 não significa ausência de efeitos de lenteamento nos espectros calculados.

## Entrega à gerente

Próximo gate local: verificar no código histórico o mapa S→CAMB e comparar espectros/likelihood com o rival no mesmo suporte; reconciliar as 13/12 medições BAO por arquivo/release e identificar a covariância utilizável. Só depois especificar uma previsão TGL fixa completa e uma estatística global para simulação. Resultado atual: **dois pareceres [DECLARADO], zero novos fits e zero significâncias observadas**.


## Adendo 28/09/2026 — reconciliação local da bancada

[REAL — evidência local da gerente] A bancada conferiu a linhagem BAO no relatório `TGL_BANCADA_OFICIAL/D10_PARECERES_CONFERIDOS_E_LINHAGEM_BAO.md` (SHA-256 `ec18642df624f345bcb4263e10c83ae51629415e549f3405e20434f262dee2ad`) e em `state/D10_BAO_LINEAGE_AUDIT.json` (SHA-256 `b5271e3e283baf372f600d5d3e0abf4448cd4559bbe6ae302345edfa6ffb023c`), produzido por `audit_d10_bao_lineage.py` (SHA-256 `225e2a421fba93fe548e91c34a3b155d5482fa668685ff4e8e5ec8d843a56b3d`). Esta seção registra o que esses artefatos reportam; não representa execução independente de cosmologia por esta coordenação.

[REAL — reconciliação reportada] N2 literal de 12 pontos coincide com os primeiros 12 do fallback D9; o DR2 local de 13 tem sete redshifts e apenas sete chaves comuns, sem vetor idêntico. A covariância 13×13 instalada foi verificada simétrica e positiva por Cholesky, erro LLᵀ 2,78×10⁻¹⁷, seis pares correlacionados e |ρ| máximo 0,493552. Cache corresponde a média e diagonal da covariância arredondadas, sem comprovar o histórico de execução. Não chamar N2 de DR1 apenas pela contagem.

[DERIVED — correções algébricas] Na implementação S histórica, com ω_b fixo, (β,ω_c) ↦ (N_eff,ω_c,eff) = (3,044 + 9,929606216611285 β, (1+β)ω_c + βω_b). O jacobiano tem determinante 9,929606216611285(1+β), diferente de zero no suporte β>−1: quando β e ω_c são livres, a imagem é localmente bidimensional, não uma curva. Para β=−0,05, ω_b=0,028 e ω_c=0,08, ω_c,eff=0,0746, ínfimo do suporte aberto informado; 0,07515 no parecer Kimi está errado. Conferir inclusão do suporte completo e equivalência observacional antes de usar o argumento de ausência de poder.

[REAL — revisão do alcance] Não retirar um rival que contém a implementação S apenas para facilitar 5σ global. Correções da bancada ao parecer MiMo: ω_b comum não implica por si duplicação do fator BBN; lowTT e lowE são distintos; auxiliares gaussianos experimentais podem compor likelihood frequentista; tolerância relativa TE no cruzamento por zero e exigir z_drag fixo são critérios inadequados; ausência de CLASS não bloqueia automaticamente. Os limiares e cenários do parecer continuam propostas até especificação própria. Não houve fit cosmológico nem p observado; o gate permanece intacto. Próxima etapa é recuperar a tradução cosmológica canônica atual antes de congelar um modelo realista fixo.
