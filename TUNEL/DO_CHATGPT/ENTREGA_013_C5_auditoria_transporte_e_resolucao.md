[REAL — implementação auditada e déficits medidos; OPEN — precisão/calibração científica]

# ORDEM 013 — auditoria do transporte e resolução

2026-09-22T06:44:00.335469+00:00. N/A — sem Lean. Originais canônicos e C6 preservados.

**PAGO:** piloto em coordenadas de ringdown concluído:2048 propostas,1473 no domínio,575 com integrando zero contadas no denominador. Densidade conferida por soma direta das PDFs, erro log máximo3.5527136788005009e-15; jacobiano por diferenças finitas nos pontos dominantes, erro relativo máximo1.6648771250515892e-10. Ida/volta e suporte verificados para todas as propostas.

**PAGO:** auditoria das somas e resolução8192→16384Hz nos92 pontos dominantes, alteração relevante máxima0.015367115598905912, abaixo de0,1.

**NÃO PAGO:** ZERO/1200 razões atingiu os critérios. ESS mediana5.79428676; eficiência por proposta multiplicada por1.75285152, mas ainda insuficiente. 508/1200 razões mudaram mais de0,2 contra o piloto anterior; máximo1.4457595. Nenhuma foi promovida a evidência física ou sigma.

## Resolução estendida

**PAGO:** controles adicionais32768/65536/131072Hz, mesmas fontes/ruídos/hipóteses. Os dados injetados continuam os8192Hz originais: não se demonstrou adequação da resolução das injeções a SNR600. A tabela é de avaliações em pontos de fonte, não da região posterior.

| SNR | 32768→65536 passa | 65536→131072 passa | maior delta logL inicial | maior delta logL seguinte |
|---:|---:|---:|---:|---:|
| 40 | 144/144 | 144/144 | 0.02755232 | 0.0579619254 |
| 200 | 123/144 | 123/144 | 0.286959443 | 0.371107506 |
| 600 | 72/144 | 74/144 | 2.15906119 | 2.65821002 |

**NÃO PAGO:** resolução uniforme em alta sensibilidade. Phenom melhora no controle entre taxas, mas SEOB permanece instável em parte dos casos; não basta continuar duplicando taxa sem diagnosticar o gerador/alinhamento. Além disso, 32/144 controles locais de interpolação falharam algum SNR, máximo delta logL=0.00286003001. Interpolação, quadratura, resolução do gerador e região posterior são controles diferentes; passar um não quita os outros. A falha numérica não é exclusão da TGL.

## Próxima integração, efetivamente iniciada

**EM EXECUÇÃO:** `phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192`, sessão41895, observado1136/4299. O conjunto anterior ganhou ESS agregada49.4901384. Hipótese computacional: poucos pontos efetivos podem ajustar em excesso uma mistura6D de12 componentes. O próximo piloto usa3 componentes e8192 novas propostas; não elimina nenhum dos sete parâmetros físicos nem altera seu prior. A hipótese de melhora ainda será medida.

O oráculo de32768 amostras da proposta passou: maior desvio padronizado dos momentos=1.49896051. Isso verifica normalização/momentos computacionais, não significância astrofísica. Dez por cento da proposta continua sendo o prior original integral.

**Continuar:** revalidar sessão41895; não reiniciar por timeout. Sessões73887,95183 e81510 terminaram com código0. Após o RESULT:

```text
audit_registered_transport.py IMRPhenomXPHM_seed130861_N8192 --stage phase_ringdown_regularized
audit_phase_source.py ../phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192 --rate --processes 6
compare_phase_runs.py phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048 phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192
```

O auditor parametrizável é cópia do auditor anterior, com seleção explícita de pasta e contagem dinâmica; o original foi preservado. Os comandos de auditoria desta nova rodada ainda não foram executados, pois ela está viva. A descrição em inglês `SOURCE_INTEGRATION_METHODS.md` registra integral, priors, jacobiano, propostas externas, intensidade contínua e limites dos testes, para a entrega independente.

Faltam precisão/repetição dos fatores de Bayes, SEOB como recuperação integrada, demais leituras/SNR e calibração contínua de a. Nos SNR altos, diagnosticar as falhas persistentes antes de usar a inferência. Nenhum resultado recente move gate nem altera a C6 congelada.

## Custódia medida

| arquivo relativo à bancada | SHA256 |
|---|---|
| `cache/source_evidence/audit_transport_density.py` | `f0b95959f89510173f851cd6353888fba5dcd4994a9dd30a4f231cda81a47597` |
| `cache/source_evidence/audit_registered_transport.py` | `0f4d3c39f9f3e54aee316141daec0a66a4ad8b0e1194149469c0e9023b56c23c` |
| `cache/source_evidence/SOURCE_INTEGRATION_METHODS.md` | `7e9aaf225bb1aadba591978d9c2b9dc6b368c93616b3ec80defcc099220b937a` |
| `cache/source_evidence/refine_phase_resolution.py` | `d2968807ab5ecd7829c7ba0a32cda836a3a6a3177167b7ac9c98a649a5b3bb16` |
| `cache/source_evidence/resolution_refinement/REGISTRATION.json` | `adb18e0500f13625c68e3a560d3e3c9912a0dc7dcf7b2724476ef6e7453b29e5` |
| `cache/source_evidence/resolution_refinement/RESULT.json` | `45722efbe4c22dc22977d73cd3d4f0b594c8ee960683b5f6eeb7c14e2c82fd51` |
| `cache/source_evidence/refine_ringdown_proposal.py` | `c788e3a4c4bb4d94886a7c8fa182ee43333db539311d1922abe82fffe344e8fa` |
| `cache/source_evidence/phase_ringdown_regularized/REGISTRATION.json` | `6c167d0b6839a63cf14c6b0635079d538b14e7107d7519627e379b5341f4dd89` |
| `cache/source_evidence/phase_ringdown_regularized/PROPOSAL.json` | `8af9f27a680c1c0ef86a6a7abf48389a22ed6aac593dbc9a6b4ddbad28a0572f` |
| `cache/source_evidence/phase_ringdown_regularized/PROPOSAL_ORACLE.json` | `40d045cb4c14ec6c1791878c03b4b34865c4d2f314d81e8172a495cfbe6cbf85` |
| `cache/source_evidence/phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048/RESULT.json` | `698fea056fff1830b135dba6eb2acb6985a36a377927b946c7977741e674f04c` |
| `cache/source_evidence/phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048/RESULT_ARRAYS.npz` | `3671bfd7e0fe6d6c9bd14325d184159f31f6d2c0f3cfa82548d6a34125c95a13` |
| `cache/source_evidence/phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048/PROPOSAL_COMPARISON.json` | `e5d86fea78109a767359d4c35ab6f7ebcce5085fc56c4ea0d7b514ec23e42d9a` |
| `cache/source_evidence/phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048/DENSITY_AUDIT.json` | `068a89facdd181f47326dc731226c102b5bc58ce871e11282aef76fac6e99bba` |
| `cache/source_evidence/phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048/AUDIT_RATE.json` | `eee54c1256b17b6067e6723855b82d8ddf8ed1d1104f13c203fe3639bbafb0d0` |
| `cache/source_evidence/phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/START.json` | `c67a0c7af8ea26be5fd3dc6e4c5a4af5a950b5fc96f92313035042b9080478a9` |
| `record_transport_audit_progress.py` | `5a060a3dfdb8b259dc32e045ac7322960ff1acb014759aa439fb3097789ab9de` |
