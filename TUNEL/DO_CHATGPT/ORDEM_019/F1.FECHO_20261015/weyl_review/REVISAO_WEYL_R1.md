# Revisão independente dos operadores de Weyl

[REAL] PASSA nos teoremas enunciados, com ressalva material para a integração modular futura.

## Ressalva de integração

O W atual é D(f), cuja órbita do vácuo é proporcional a e(f). Para f em K, a regra de Tomita na órbita é S e(f)=e(-f). Se S_K fixa K, identificar diretamente esse S com Gamma(S_K) tem sinal incompatível para f não nulo. Não se deve promover R_D(K) e Gamma(J_K) à identificação modular sem uma ponte de fase.

[DECLARADO — decisão do root] Root aceitou a ressalva e planejou FieldWeylR1 com W_field(f)=D(i*f), sem 1/sqrt(2) nesta convenção, e R_field(K)=R_D(iK). A rotação i preserva inner e o cociclo; a conjugação antilinear envia i*f a -i*f quando S_K fixa f.

Esta revisão só verifica as quatro fontes listadas. O módulo futuro e sua integração não são considerados compilados ou aprovados por este recibo.

## Recompilação independente

| Fonte | EXIT | Segundos | Declarações/impressões | .olean idêntico |
|---|---:|---:|---:|---|
| WeylCoefficientsR4.lean | 0 | 26.764216 | 19 | False |
| WeylOperatorsGenericR2.lean | 0 | 27.850234 | 18 | False |
| WeylCovarianceR1.lean | 0 | 27.558168 | 2 | False |
| ConcreteWeylR1.lean | 0 | 150.926825 | 27 | True |

## Conferência matemática

- **cocycle — PASSA:** A convenção D(f)e(g)=exp(-<f,f>/2-<f,g>)e(g+f) preserva Gram com o produto interno antilinear à esquerda. A composição deriva D(f)D(g)=exp(-i Im<f,g>)D(f+g). Não há um fator 1/2 omitido: o parâmetro simplético desta convenção é 2 Im<f,g>.
- **extension — PASSA:** O módulo genérico assume apenas a família exponencial, seu kernel e totalidade. A imagem deslocada é total por translação sobrejetiva e amplitude não nula. GramTotalExtension constrói a isometria/equivalência; nenhum Weyl, CCR, inverso ou covariância é um campo assumido. A revisão independente do Gram é do root, pinada abaixo.
- **star_locality — PASSA:** W(-f)W(f)=1 deriva do cociclo; a equivalência unitária identifica o inverso com adjunto, produzindo W(f)*=W(-f). Localidade usa Im<f,g>=0 nas duas ordens, com conjugação explícita.
- **covariance — PASSA:** A covariância genérica deriva da ação V e(g)=e(ug) e da invariância da amplitude. Na instanciação concreta essa hipótese é descarregada por gamma_exponential. As hipóteses de operador Weyl/kernel/totalidade desaparecem do enunciado concreto.
- **same_fock — PASSA:** ConcreteWeylR1 usa F1Rede.BosonicFock.F, o vacuum e exponential já construídos. W_vacuum e a característica gaussiana são derivados. Não há novo Hilbert, vácuo substituto ou densidade postulada.
- **net_and_cyclicity — PASSA:** R é a álgebra bicomutante dos W(K); monotonia/localidade/covariância consomem leis agora concretas. vacuum_orbit_total e global_vacuum_cyclic usam todos f:H1 e K=top. Não estabelecem ciclicidade ou separação de uma cunha.
- **flow_scope — PASSA_COM_HIPOTESE_EXPLICITA:** wedgeFlow continua recebendo LightNetData como dado de localização. As leis zero/add são algébricas; não são identificação modular, KMS ou construção de um habitante físico desse registro.

## Alcance

- Recompilação independente uma vez de cada fonte aceita, Lean 4.31.0, fonte copiada byte a byte, dependências pinadas antes/depois, LEAN_PATH literal nos recibos.
- Os três módulos seguintes importaram os módulos precedentes recompilados pelo revisor; Concrete importou também ExponentialVectors/Totality recompilados independentemente.
- 66 declarações/impressões, incluindo auxiliares gerados, somente no trio propext/Classical.choice/Quot.sound; zero sorry.
- Os .olean podem diferir: caminhos absolutos distintos estão serializados e as dependências foram recompiladas. Não se alega identidade binária nem que o caminho seja a única causa de cada diferença.
- Não houve revisão própria do Gram: consume-se o parecer independente do root. Não se afirma continuidade forte de W, ciclicidade/separação de cunha, KMS/BW, certificado Fock completo ou confirmação física.
- Nenhum original, memória, produção, Nós ou gate foi modificado. AUDITADA/FECHADA é ato da gerência.

Recibos, hashes, linhas e evidência de comparação: REVISAO_WEYL_R1.json.
