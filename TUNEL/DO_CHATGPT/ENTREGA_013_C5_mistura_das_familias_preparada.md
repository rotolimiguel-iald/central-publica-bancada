[REAL — controle estatístico implementado; OPEN — precisão e calibração astrofísicas]

# ORDEM 013 — Combinação preparada das famílias de recuperação

Registro: 2026-09-22T08:29:45.984156+00:00. N/A — sem Lean novo.

**Avanço:** a mistura de evidências das duas famílias está implementada e
registrada, com prior explícito 1/2 para cada família sob ambas as hipóteses.
As simulações permanecem separadas. A mistura não faz média de ln B nem
seleciona a família mais favorável a cada hipótese.

**Resultado do controle:** em 4000 repetições de integrais analíticas,
a razão entre variância observada e prevista foi
1.02005200893. O erro de Monte Carlo
preserva o pareamento das hipóteses dentro de cada família e centra sua
influência, pois as probabilidades posteriores das famílias podem mudar.
No controle com integrandos constantes, o erro correto foi
6.8051349e-17; omitir o centramento
produziria erro espúrio 0.22999506.
Isso é teste do estimador, não resultado de ondas gravitacionais.

**Recusas verificadas:** quatro entradas inválidas; componente com ESS baixo
mesmo com erro pareado cancelado; tentativa de consumir uma rodada incompleta.
Esta última terminou com código 1 e nenhum resultado da mistura foi gravado.

**Rodadas ainda ativas, observadas via handles antes deste registro:**
- IMRPhenomXPHM: sessão 62818, 5552/8554 avaliações no suporte.
- SEOBNRv4HM: sessão 61984, 832/1024 avaliações no suporte.

**O que falta:** terminar as integrações, auditar densidade/taxa, comparar
repetições e recuperar a intensidade contínua com viés/cobertura medidos.
A mistura não apaga falhas de precisão dos componentes. Não há resultado
aceito novo de ln B ou sigma nesta etapa. Os 50 intervalos de ruído continuam
reutilizados e pareados; O4/O5 estão normalizados separadamente a SNR40.

**Próximo passo:** após os RESULT.json, executar as auditorias existentes
`audit_registered_transport.py` com as respectivas fases, e então
`combine_source_families.py run`. O registro já existe: não repetir `register`.
Não reiniciar processos vivos. A nota `cache/source_evidence/FAMILY_MIXTURE_METHOD.md`
contém derivação, limitações e comandos exatos. C6 e originais preservados.

## Custódia medida

| arquivo relativo | SHA256 |
|---|---|
| cache/source_evidence/source_family_mixture.py | 8e12185b8dc954cb9f4e3a35c9f1cd83498051c6b6735cef77a009b2c3d3dadc |
| cache/source_evidence/validate_source_family_mixture.py | 7a961051b17b1ba699c24087e9b71b51decb64580bfbec5cc700aee6f6aba237 |
| cache/source_evidence/combine_source_families.py | c70a7ad786e7bba9aa46d265ecc5035653a74fce92abe9f53f49564116028f01 |
| cache/source_evidence/FAMILY_MIXTURE_METHOD.md | 7076ceb22988140acf5dc1d214f00f6f026548c8a102ecae24b6b23089dbee14 |
| cache/source_evidence/source_family_mixture_validation/REGISTRATION.json | a6ed14c611f771c7562760f86b1f6a403583fbb9ab1d4b914035e97b7d5dd569 |
| cache/source_evidence/source_family_mixture_validation/RESULT.json | 7be90060fbe49573cbe5002532c338b1c435a573676424d50f371411bd388a15 |
| cache/source_evidence/source_family_mixture_validation/TOY_REPETITIONS.npz | efa9ebcb8b617c331ba3bd70359bbe4621bc4533dd75022400b19ff201fec763 |
| cache/source_evidence/source_family_combination/REGISTRATION.json | 86c4a6c21f5961f6d723fc1f090e8b86d654db7ab987c68d078624d12e4d8730 |
| record_family_mixture_progress.py | fa991cfb0da4786148d2ba2aecb3cc80f2a97ab2fddfffcff48153fdb7ed9e15 |
