# Revisão independente — totalidade na cunha e vácuo cíclico/separante

[REAL] **PASSA COM ESCOPO**, sem achado material. Claim 845; decisão AUDITADA/FECHADA continua da gerência.

## Recompilação independente

| Módulo | EXIT | Segundos | Impressões de axiomas | .olean idêntico |
|---|---:|---:|---:|---|
| WedgeAnalyticR2.lean | 0 | 47.350 | 4 | True |
| StandardComplexSpanR1.lean | 0 | 13.617 | 1 | True |
| RealSubspaceTotalityR5.lean | 0 | 49.211 | 7 | True |
| WedgeCyclicR3.lean | 0 | 59.755 | 5 | True |

21 teoremas nas fontes, 17 impressões de axiomas: somente propext, Classical.choice e Quot.sound; zero sorry. Logs/recibos guardam início, fim, duração, comando, toolchain e LEAN_PATH literal. Os quatro .olean são byte a byte os aceitos.

## Conferência matemática

- **WedgeAnalyticR2.lean:27-49** — Ortogonalidade aos exponenciais de K implica que cada coeficiente setorial é zero, restringindo a série inteira a t real com t*x em K. O peso 1/sqrt(n!) é estritamente positivo. Totalidade não é premissa.
- **WedgeAnalyticR2.lean:51-80** — Analiticidade dos tensores puros vem do produto tensorial bilinear contínuo e da inclusão na completude. A sequência real 1/(n+1) dá zeros distintos acumulando em 0; aplica-se o teorema de identidade no domínio complexo conexo inteiro.
- **StandardComplexSpanR1.lean:12-33** — K+iK é denso pelo campo IsCyclic de StandardSubspace; a clausura do span complexo contém K e iK. Só a metade cíclica da standardness é necessária para esta conclusão; não se assume densidade exponencial.
- **RealSubspaceTotalityR5.lean:16-68** — A complexificação algébrica K+iK é provada igual ao span complexo. Para x,y em K, o polinômio P(c)=inner(v_n,(x+c*y)^tensor n) anula na reta real; continuação analítica dá P(i)=0. O inner é linear no segundo argumento.
- **RealSubspaceTotalityR5.lean:70-111** — A densidade do span complexo e a continuidade estendem a anulação a todo H1; a totalidade dos tensores puros em cada setor e lp.ext dão v=0. O complemento ortogonal nulo entrega a totalidade exponencial. A aplicação a spectralOutput.KWR usa um habitante já construído.
- **WedgeCyclicR3.lean:23-49** — Na convenção W(f)=D(i*f), W(k)Omega é amplitude não nula vezes e(i*k). A totalidade é aplicada a K.mulI. Isso prova a ciclicidade de R(K), não só ciclicidade global para K=top.
- **WedgeCyclicR3.lean:51-83** — O complemento simplético K-prime é standard pela biblioteca. Localidade força a comutar com todo b de R(K-prime); a*Omega=0 implica a*b*Omega=0. Ciclicidade de K-prime e continuidade de a dão a=0. Não se assume separação da álgebra.

## Alcance e não vacuidade

O consumidor usa spectralOutput.KWR concreto. F é o mesmo Fock já construído e Omega tem norma 1 (BosonicFock.lean:25), não espaço nulo. Não se exige como campo o resultado a provar.

- Para K real de span complexo denso, exp(K) é total no Fock canônico.
- Para K standard, Omega é cíclico e separante de R(K) na convenção W(f)=D(i*f); aplica-se à cunha canônica existente.
- Não identifica o Tomita da álgebra-vácuo, nem estabelece KMS/BW, Maxwell, H3, Takesaki ou realização física.
- Standardness é hipótese nos teoremas gerais, habitada pelo consumidor KWR; nenhuma rede completa com todos os certificados é reivindicada.
- Não foi repetida a compilação dos exponenciais/Weyl já revisados: reutilizaram-se seus artefatos independentes.
- A execução elevada segue a autorização desta unidade; tempo menor não prova a causa da latência anterior.

Os hashes das duas entregas e de seus 37 pinos foram relidos. Fontes do construtor permaneceram intactas; a revisão copiou os bytes para subpastas próprias e recompilou com caches somente de leitura. O JSON guarda os pinos individuais, evidências e fontes reutilizadas. Nenhuma alteração de memória, produção ou gate.
