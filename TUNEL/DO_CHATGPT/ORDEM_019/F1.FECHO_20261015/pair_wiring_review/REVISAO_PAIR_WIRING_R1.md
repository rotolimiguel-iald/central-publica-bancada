# Revisão independente — fluxo da cunha e Tomita do par

[REAL] **PASSA COM ESCOPO DE COMPONENTES**. Nenhum achado material; claim 845. O aceite da gerência permanece distinto.

## Builds independentes

| Fonte | EXIT | Segundos | #print axioms | .olean idêntico |
|---|---:|---:|---:|---|
| CanonicalWeylAssemblyR5.lean | 0 | 65.159 | 5 | False |
| CanonicalWedgeFlowR2.lean | 0 | 61.528 | 5 | True |
| PairTomitaClosabilityR2.lean | 0 | 16.242 | 5 | True |
| PairClosedTomitaR2.lean | 0 | 13.699 | 6 | True |
| OneParticleSymplecticR2.lean | 0 | 37.632 | 2 | True |
| WedgePairTomitaR2.lean | 0 | 55.900 | 7 | True |
| WeylAntiunitaryR4.lean | 0 | 51.798 | 4 | False |

Checker separado: EXIT 0, 181 declarações locais/geradas dos seis namespaces; todas no trio, nenhum axioma local, zero sorry nos aceites. Inclui importados via `env.constants.toList`. Cada recibo guarda início/fim/segundos, toolchain, comando, LEAN_PATH literal e pinos antes/depois.

A R3 histórica foi recompilada antes da mudança de escopo. A R4 do construtor falhou e foi excluída; somente a montagem final é importada no checker. As diferenças de .olean indicadas na tabela não são ocultadas e sua causa não foi estabelecida.

## Matemática

- **CanonicalWeylAssembly — PASSA.** A versão final fornece dez campos por termos: R, monotonia, localidade, covariância, fluxo e suas três leis, ciclicidade e separação. Os últimos dois usam KWR concreto e D.wedge_glue. O tipo RemainingWeylInput continua premissa não habitada por este arquivo; não é construção de certificado completo.
- **CanonicalWedgeFlowR2 — PASSA.** A reflexão-conjugação comuta com o multiplicador de fase. O grafo do operador TW é preservado pelo boost, logo o espaço real fixo KWR é preservado. A volta usa B0(-s); a covariância concreta permite restringir Ad Gamma(B0(-2*pi*t)) à álgebra da cunha. Não se inventa a rede global nem se prova que esse fluxo é modular/KMS.
- **PairTomitaClosabilityR2 — PASSA.** O grafo usado é exatamente pairTomitaGraph(M,Omega). A identidade de emparelhamento segue do adjunto e da comutação M/N; estende-se à clausura por continuidade. A ciclicidade de N fornece funcionalidade da clausura, e a ciclicidade de M dá domínio denso. Essas são hipóteses explícitas no lema genérico, não conclusões assumidas no consumidor.
- **PairClosedTomitaR2 — PASSA.** O domínio é a projeção da clausura real do grafo, fechado por soma e multiplicação escalar com conjugação na segunda coordenada. Escolha de valor torna-se unívoca pela funcionalidade; constrói S semilinear, grafo fechado igual à clausura, domínio denso, invariância do domínio e involutividade. S(a*Omega)=a-star*Omega. Não se afirma S limitado em todo F.
- **OneParticleSymplecticR2 — PASSA.** TW f=Jcandidate f em KWR é deduzido da fixação de Jcandidate TW e Jcandidate^2=1. A simetria de TW no domínio efetivo, mais antiunitariedade, torna real inner(f,Jcandidate g), provando Jcandidate(KWR) contido no complemento simplético. Só inclusão é provada; não igualdade ou dualidade de Haag.
- **WedgePairTomitaR2 — PASSA.** Compõe as duas álgebras concretas R(K) e R(K-prime), cuja comutação e ciclicidade já foram provadas. Não há campos de ciclicidade, separação ou fechabilidade. Produz S fechado/densamente definido/involutivo do PAR concreto e sua ação nos vetores de Weyl. Standardness é a hipótese geral, com aplicação ao KWR construído.
- **WeylAntiunitaryR4 — PASSA.** Conjugação Gamma(j) D(f) Gamma(j)=D(jf) vem da fórmula nos exponenciais totais, conjugação da amplitude e j^2=1. Para o campo W(f)=D(if), antilinearidade muda o rótulo para -j f. A hipótese j involutiva é explícita. Trata-se de covariância antiunitária algébrica, sem identificar Gamma(j) com a polar do S do par.

## Alcance

- S é o Tomita fechado do par da álgebra concreta/vácuo no sentido da clausura do grafo; não há identificação das suas polares com Gamma(J) ou Gamma(Delta).
- Invariância de uma cunha e restrição do fluxo não provam BW/KMS nem a rede física global.
- RemainingWeylInput mantém condições analíticas/core importadas; não se reivindica habitante do FockCertificate completo, Maxwell ou H3.
- As hipóteses do consumidor do par são habitadas pelo KWR e Fock concretos já construídos, com vácuo de norma um.
- Integração no candidato um.py e rito integral são etapas distintas desta revisão.

Fontes, recibos e compilações estão pinados no JSON. Originais, memória, produção e gate intactos; nenhuma chamada externa.
