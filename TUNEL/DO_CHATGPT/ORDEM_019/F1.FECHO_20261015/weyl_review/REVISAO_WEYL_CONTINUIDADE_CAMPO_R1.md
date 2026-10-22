# Revisão independente: continuidade e convenção de campo

[REAL] PASSA nos enunciados revisados. A correção de fase atende à ressalva anterior; a identificação Tomita continua fora do escopo.

| Fonte | EXIT | Segundos | Declarações/impressões | .olean idêntico |
|---|---:|---:|---:|---|
| ConcreteWeylContinuityR2.lean | 0 | 140.303952 | 5 | True |
| FieldWeylR3.lean | 0 | 871.103233 | 31 | True |

Somente o trio propext/Classical.choice/Quot.sound; zero sorry.

- **exponential_continuity — PASSA:** A norma da diferença entre exponenciais deriva da expansão do produto interno e da identidade exp(inner). A continuidade resulta de funções escalares contínuas e limite zero; não é hipótese.
- **strong_continuity — PASSA:** A órbita W(f)e(g) é contínua pela amplitude e pelo mapa exponencial. O subespaço de órbitas contínuas é fechado por convergência uniforme decorrente de ||D(f)||=1; sua inclusão do span total dos exponenciais permite alcançar todo vetor. O argumento reutiliza continuousOrbitSpace_closed, sem assumir regularidade da família D.
- **continuity_topology — PASSA_COM_ESCOPO:** O enunciado prova continuidade forte, f↦W(f)ψ para cada ψ, e regularidade t↦W(tf)ψ. Não prova continuidade na norma de operador ou diferenciabilidade/geradores.
- **phase_rotation — PASSA:** rotate(f)=i*f preserva inner e a forma simplética. W_field(f)=D(i*f) conserva exatamente o cociclo exp(-i Im inner(f,g)), sem 1/sqrt(2) adicional. A lei de adjunto e a covariância unitária são transportadas com sinais consistentes.
- **field_net — PASSA:** A álgebra de campo é gerada por D(i*f) para f em K, no mesmo Fock e vácuo. R_mono/R_local/R_cov e o fluxo restrito são derivados dessas leis. A identidade wedgeFlow_is_Ad tem o sinal -(2*pi*t) previsto na assinatura.
- **previous_integration_finding — CORRECAO_DE_FASE_ATENDIDA__IDENTIFICACAO_TOMITA_ABERTA:** A ressalva de convenção do parecer R1 foi tratada por um módulo novo e separado. A órbita agora é proporcional a e(i*k), compatível com a antilinearidade de S_K quando S_K k=k. Esta compatibilidade de fase não demonstra que o Tomita da álgebra seja Gamma(S_K); nenhuma identificação Tomita, ciclicidade/separação de cunha ou KMS é afirmada por estas fontes.

## Alcance

- Rodada material limitada às duas fontes novas; os quatro Weyl antigos aprovados não foram recompilados novamente.
- Recompilações em sandbox próprio com Lean 4.31.0, cópias exatas, dependências independentes quando disponíveis e hashes conferidos antes/depois. Logs registram comando, início/fim/segundos/exit e LEAN_PATH literal.
- As tentativas FieldWeyl R1/R2 recusadas não integram o aceite. Nenhuma fonte do construtor foi alterada pelo revisor.
- LightNetData continua hipótese de localização do fluxo. Nenhum FockCertificate completo ou habitante físico foi produzido por esta revisão.
- Originais, memória, produção e gate preservados; AUDITADA/FECHADA pertence à gerência.

Recibo, hashes e linhas: REVISAO_WEYL_CONTINUIDADE_CAMPO_R1.json.
