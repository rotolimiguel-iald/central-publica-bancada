# E45A — aceleração exata validada; grades pendentes

[REAL] A validação passou. Nenhuma evidência observacional, integral de grade ou MCMC foi executada. A ordem desta unidade autoriza preparar/validar e devolver custo/controles antes do lote. A leitura acumulada permanece separada e o acelerador recusa essa configuração.

## Derivação e invariantes

[DERIVED] Para fundo fixo theta=(H0,omega_b,omega_c), I* é constante. Em P/F4, chi2(beta)=chi2_Planck+BAO+[H0 exp(beta I*)−H_SH]^2/sigma_SH^2. Um cálculo do fundo serve a todos os nós beta; o exponencial não é linearizado.

Em P/F5 sombra, seja q o vetor indicador das SN não-calibradoras e a=5/ln(10). Então mu(beta)=mu0−a beta I* q, enquanto calibradores mantêm CEPH_DIST; logo r(beta)=r0+a beta I* q. Para C=LLᵀ, u=L⁻¹1 e P=Id−uuᵀ/(uᵀu), defina x=P L⁻¹r0 e y=P L⁻¹q. Segue:

chi2_SN(beta)=xᵀx+2a I* (xᵀy) beta+(a I*)²(yᵀy) beta².

Mhat(beta)=Mhat0+a I* beta [uᵀL⁻¹q/(uᵀu)].

Todos os coeficientes preservam a matriz STAT+SYS completa, inclusive covariâncias calibrador/não-calibrador. A projeção é do intercepto M; não é leitura angular da face canônica e não altera qualquer construção formal. Face/projeção da teoria permanecem com seus tipos próprios.

A igualdade é algébrica no contrato histórico de sombra, não uma aproximação de beta pequeno. A integral sobre beta continua sendo a mesma soma dos mesmos nós retangulares25/35. A única mudança é organizar contas comuns uma vez por fundo e usar vetor beta. Priors, máscara CAMB, contagem de nós inválidos, perfil M e estatísticas históricas E45 são preservados. Beta_TGL é computado de alpha_CODATA2018*sqrt(e) em runtime.

## Controle e congelamento

Protocolo congelado em 2026-10-06T01:54:47.133652+00:00, registro prévio seq420 confirmado antes de validate. Protocolo SHA-256 5b443690528f3abe1da1cdcb4e468119a081cbd82f3aadde6e0585b1ad107a0c; código bc36447efe48a10bd918f5dc5868e5cf2dcddfd2e56dfcd4c8eece3dd93333f3; validação aefaab9e4c822993cb7d8579ef3699a4f416e510c0d22a13400be938c41b8a90.

Fundos: os três theta verificados P45 de cada família. Betas de controle fixados antes: −0,04;−0,015;0;0,005;0,01;0,02;0,04; beta_TGL runtime. Esses são pontos paramétricos de engenharia com os mesmos dados congelados, não novas observações sintéticas nem um ajuste. Foram48 comparações acelerado/escalar e seis conferências dos resultados P45 conhecidos. Os endpoints−0,05/+0,05 deram infinito como exige a máscara estrita histórica.

Maior |Δchi2| acelerado/escalar: 7.27595761418e-12, limite1e−8. Maior |ΔM|: 1.42108547152e-14mag, limite1e−10. Contra os recibos P45: |Δchi2|≤2.72848410532e-12 e |ΔM|≤1.06581410364e-14mag. Conferências dos recibos também verificadas por leitura posterior do JSON, sem repetir cálculos.

Benchmark: cinco rodadas de quatro ciclos dos três fundos, vetor35 construído repetindo os betas de controle, sem novos pontos ou integral.174 chamadas de likelihood incluindo controles/coeficientes/benchmark. Wall2.9150s; CPU1.5938s; pico164.383MiB. Uma thread, sem GPU.

## Custo projetado, não duração medida de grade

| Família | ms por fundo com vetor35 | Total25+35, três modelos | Margem2x |
|---|---:|---:|---:|
| P4_d1b | 0.1666 | 0.49min | 1.01min |
| P5_sombra | 4.9559 | 14.50min | 29.08min |

Total P/F4+P/F5 sombra: 14.98min, margem agregada30.09min. Cada modelo usa15625 fundos em n25 e42875 em n35, inclusive o modelo livre; sua quantidade de nós científicos continua390625 e1500625 respectivamente. Nenhuma integral analítica substitui a soma de beta.

Todas as12 unidades únicas projetadas cabem isoladamente em600s com margem2x da maior taxa medida. O programa limita uma unidade por invocação, streaming,512MiB e600s; falha conserva saída parcial sem logZ concluído e não amplia lote. Projeção não garante duração: loops, domínio e carga do host podem variar. O modo de grade foi preparado por revisão de código, mas ainda não foi invocado; os controles acima validam os valores e o perfil algébrico.

A implementação escalar E45 permanece como referência preservada. Sua projeção P/F5 sombra era2,59h; a redução medida por custo de bloco é uma estimativa de execução futura, não benchmark completo entre duas grades. A leitura acumulada não ganhou esta aceleração e mantém seu custo/contrato separado.

## Sequência e comando para a coordenação

Proposta: primeiro uma unidade fixa P/F4 pequena; conferir seu recibo, normalização e comparação com o alvo histórico antes de ampliar. Em seguida, somente conforme continuação da coordenação, o par25/35 e demais modelos, mantendo cada unidade limitada. Depois P/F5 sombra. Nenhum lote automático é lançado por esta nota.

~~~powershell
& 'C:\Python314\python.exe' -X utf8 'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\reproducao_fase45_conjunta\E45A_aceleracao_exata.py' grid P4_d1b tgl 25 --max-seconds 600
~~~

O comando é concreto e preparado, ainda NÃO executado. E45A_CONTROLES_CUSTO_COMANDOS.json contém custos e comandos individuais. Ao comparar, conservar logZ25/logZ35; tolerâncias E45 de0,01 em logZ e0,02 em logB; diferença35−25 acima0,01 sinaliza não resolvido, sem ajuste de alvo ou extensão automática.

Os limites estatísticos do contrato E45 não foram corrigidos pela aceleração: constantes de normalização ausentes, cancelamento de M comum apenas em comparações compatíveis, caixa±6sigma com caudas não certificadas, máscara CAMB de origem numérica, covariância cruzada ausente e marginal/SD discretizadas. Diagonal-Laplace continua diagnóstico; nunca substituir o Bayes de grade por ele. F4/F5 compartilham dados e não são réplicas independentes.

[REAL] Validação computacional e benchmark. [DERIVED] Identidade algébrica sob o mapa sombra. [INPUT] Contrato histórico. Nenhum novo veredito científico, fit, gate, original ou hipótese física foi alterado.
