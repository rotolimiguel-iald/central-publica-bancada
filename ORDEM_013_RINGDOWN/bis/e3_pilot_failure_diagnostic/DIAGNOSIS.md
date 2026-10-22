# Diagnóstico finito do piloto pSEOB — encerrado

**Reparo não implementado nem aprovado.** [REAL] Foram10 processos (9 de fonte +1 replay),16 chamadas/15 retornos: 13.168752s de wall somado e 10.400864s CPU dos filhos. Último término: 2026-09-22T22:44:02.890043+00:00, 192.043s após o plano; limite original 2026-09-22T22:50:50.847418+00:00. O supervisor conta também o replay no teto10 (`run_diagnostics.py:22`). Não houve filho adicional. Tempo documental posterior não reiniciou a janela de execução.

## Causas distintas

1. [REAL — fonte + execução] O condicionador toma fmax como Nyquist interno (`sources/LALSimInspiralGeneratorConditioning.c:536`,545). fmax1024 e deltaF1/16 dão fs interno2048, embora o grid dos dados seja4096. O teste que emite EDOM usa GR550 no ramo HM (`sources/LALSimIMRSpinAlignedEOB.c:1250`,1256,1279). Essa checagem não lê TGRParams; **não atribuir automaticamente o EDOM a domega**. LOW_GR também recusou em1024.
2. [REAL] As massas dos dois erros originais coincidem com draws2/8. A sequência desses oito em1024 retornou sem crash. **Tuple/índice do SIGSEGV original−11 permanecem OPEN**; um próximo draw não foi executado. Não reproduzimos a inicialização completa nem sua likelihood/dados. Bilby verifica parâmetros e depois faz100 temporizações (`sources/bilby_base_sampler.py:267`,447); isso não identifica o primeiro crash.
3. [REAL] DRAW8_2048 abortou−6 com `free(): invalid next size (normal)`. `cases/DRAW8_2048.CALL_1.json` contém a entrada completa persistida antes da chamada. Comparação por script com DRAW8_1024 confirma que **só generation_fmax mudou**; a falha alterada não é o SIGSEGV original. Elevar fmax sozinho não é reparo estabelecido.
4. [CONJECTURE — hipótese específica, não causa provada] O buffer de alta resolução é ampliado por dtau220 (`sources/LALSimIMRSpinAlignedEOB.c:2060`), sem dtau440. pSEOB4112 liga TGRflag (`:649`); o attach modifica Im(omega440) por /(1+dtau440) (`sources/LALSimIMREOBHybridRingdown.c:1081`), dimensiona Nrdwave por esse modo (`:1263`) e escreve signal[i+indAmax] sem checagem local (`:1393`). No draw8 dtau220<0 e dtau440>0. É uma hipótese concreta de capacidade insuficiente; **não medimos retLen, indAmax, Nrdwave nem demonstramos a desigualdade no caso**. `free()` não prova double-free ou identifica a instrução corruptora.

## Evidência completa e alcance

`DIAGNOSIS.json` inclui configuração original, todos os casos, tuples e retornos/pins. DRAW8: massas detector40.70912464765123/20.237781889510657 Msun; chi1/2 .9196233876975504/.2055129322455731; dtau220/440 −.6157519631492032/1.7780455359890353; domega220/440 −.42647193412015016/.7808349673597068. Distância, ângulos e GPS constam integralmente do precall. Não houve gravação de arrays de onda nem stack nativo/faulthandler; controles de fase/overlap/epoch continuam OPEN.

| Caso | rc | Chamadas | Retornos |
|---|---:|---:|---|
| DRAW2_1024 | 0 | 1 | DOMAIN_RETURNED_NONE |
| DRAW2_2048 | 0 | 1 | FINITE_WAVEFORM |
| DRAW2_8192 | 0 | 1 | FINITE_WAVEFORM |
| DRAW8_1024 | 0 | 1 | DOMAIN_RETURNED_NONE |
| DRAW8_2048 | -6 | 1 |  |
| LOW_DEFORMED_8192 | 0 | 1 | FINITE_WAVEFORM |
| LOW_GR_1024 | 0 | 1 | DOMAIN_RETURNED_NONE |
| LOW_GR_2048 | 0 | 1 | FINITE_WAVEFORM |
| PRIOR_REPLAY | 0 | 0 |  |
| SEQUENCE_8_ORIGINAL | 0 | 8 | FINITE_WAVEFORM, DOMAIN_RETURNED_NONE, FINITE_WAVEFORM, FINITE_WAVEFORM, FINITE_WAVEFORM, FINITE_WAVEFORM, FINITE_WAVEFORM, DOMAIN_RETURNED_NONE |

## Desenho de reparo para revisão, sem implementação

Separar geração interna da banda científica20–1024, conservando fs4096, deltaF1/16, epoch/fase, todos os modos, PSD/dados e priors. Uma frequência interna maior precisa passar pelo **draw8 exato**, controles complexos na banda comum com tolerância prévia e limites temporais/custo; normas escalares semelhantes no draw2 não pagam isso. Auditar capacidade nativa por máximo de todos os comprimentos/offsets realmente requeridos, com checagens explícitas de limites e overflow. Alterar tamanho de buffer exige validação, não clipping de dtau ou remoção de modos.

Persistência pré-call e isolamento tornam falhas visíveis, mas não fornecem likelihood válida para o ponto. EDOM numérico não deve ser transformado em rejeição física do prior. Reparo concreto exige versão própria, pins de fonte/binário/imports, parentE2/testemunha, saída exclusiva e revisão independente. **Stop original 2026-09-23T06:35:19.847427+00:00 preservado**; não renovar8h. A causa nativa universal não é pré-requisito abstrato adicional: vale a qualificação NF-R1 de B, com demonstração concreta de suporte e falha visível.

## Custódia e lacunas

NF-R4 corrigido **ao lado** em `SOURCE_HASH_ADDENDUM.json`: três entradas do plano apontavam texto C com hash/tamanho do HTML. Reextração byte a byte conferida; ambos os hashes estão no adendo. Plano original preservado. Fontes C adicionais e header VCS estão em `STATIC_SOURCE_ADDITION.json`; header:39/42 concorda com commit/tag instalado, mas compilação reprodutível não foi feita. Leitura primária: https://lscsoft.docs.ligo.org/lalsuite/7.26/lalsimulation/_l_a_l_sim_i_m_r_e_o_b_hybrid_ringdown_8c_source.html . Nenhum código dessa página foi executado.

Os14 fontes E2 conferem com registro. 96 verificações documentais/escalares passaram, sem ciência nova. Revisão B lida: `PILOT_NATIVE_DIAGNOSTIC_INDEPENDENT_REVIEW.json`, SHA256 `3d170b546abe6d3d438c17d6402b95ab8209f90ef4f2a63f9f597aab4dcd8e9a`. NF-R2/R3 continuam dependentes do reparo concreto; NF-R4 recebe este adendo para revisão. Não foi medido group_absent dos diagnósticos nem número real de threads; há wait/return e caps de ambiente. E2/runtime e resultados originais intactos. Sem strain, posterior, PE ou seed cego. `MANIFEST.json` lista todos os arquivos deste diretório e hashes; o próprio manifesto é listado sem auto-hash circular.
