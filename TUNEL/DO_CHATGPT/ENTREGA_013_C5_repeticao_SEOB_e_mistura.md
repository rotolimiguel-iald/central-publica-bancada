[REAL — execução e aritmética verificadas; OPEN — precisão e calibração física]

# ORDEM 013 — Repetição SEOB concluída e mistura das famílias

Data UTC: 2026-09-22T13:04:13.360393+00:00. Axiomas: N/A — sem Lean.

## Critérios e alcance

- **PAGO — execução SEOB:** 16384 propostas, 8520 avaliações dentro do suporte e 7864 integrandos nulos fora dele. O denominador preserva todas as propostas. Priors físicos mantidos.
- **PAGO — auditoria independente de densidade e somas:** erro em log-densidade 1.7763568394e-15; erro máximo de aritmética 1.98951966013e-12. Isto verifica o cálculo, não sua convergência.
- **NÃO PAGO — precisão SEOB:** 444/1200 conjuntos passam; 756 falham. ESS entre 1.23205944318 e 344.205441085. A ampliação de 2048 para 16384 propostas deixou 49 conjuntos com mudança de ln B acima de 0,2; máximo 0.535889212199.
- **PAGO — mistura registrada:** combina Z, com prior 1/2 por família em ambas as hipóteses. Entradas: Phenom16384 seed130892 (continuação real) e SEOB16384 seed130942. Não substitui a primeira entrada pela Phenom32768 ainda em execução.
- **NÃO PAGO — precisão conjunta:** 238/1200 passam simultaneamente precisão de ambas as famílias e erro MC da mistura; nenhuma das 24 células tem todos os 50 conjuntos aprovados. Nenhum conjunto recusado foi excluído do denominador.
- **NÃO PAGO — calibração contínua, viés, cobertura, repetição e resolução completa:** permanecem requisitos. scientific_acceptance=false nos dois resultados. Não há conversão de ln B para sigma.

São 1200 conjuntos simulados que reutilizam 50 intervalos de ruído, não 1200 eventos independentes. Escopo: leitura R-B, SNR40 normalizado separadamente para O4 e O5; não é comparação a distância fixa. Não foi escolhida a partição, o relógio físico ou o desenrolamento. C6 e arquivos canônicos permaneceram intactos.

## Execuções revalidadas e dependências

- 34860: Phenom32768 binária; aguardar resultado completo para auditoria de densidade, comparação e resolução com leitor de Fourier real.
- 19681 e 43367: curvas contínuas SEOB16384 e Phenom32768; aguardar EVALUATIONS_COMPLETE.json.
- 58182: controle de resolução SEOB dos 302 pontos dominantes, original PyCBC a 16384 Hz. Ao consultar: 18 concluídos; processo vivo. Só o resultado final decide o controle. O auditor não grava PROGRESS.json.

O processo 40860 terminou; não reiniciar. A mistura binária terminou; não executar de novo. A mistura contínua é outro registro e ainda aguarda suas entradas completas.

Depois das curvas completas, usar os scripts existentes:

```text
run_continuous_source_curves.py analyze --family SEOBNRv4HM
run_continuous_source_curves.py analyze --family IMRPhenomXPHM
audit_continuous_endpoints.py --family SEOBNRv4HM --require-complete
audit_continuous_endpoints.py --family IMRPhenomXPHM --require-complete
combine_continuous_source_curves.py run
```

A última operação exige também auditorias de densidade das entradas binárias correspondentes. O auditor antigo audit_phase_source.py usa o leitor complexo: não aplicar sem adaptação aos novos casos Phenom com Nyquist real. O controle SEOB em execução mantém seu leitor já validado.

## Reprodução e aproveitamento

Resultados e registros são preservados. Scripts já usados: repeat_native_source.py, audit_registered_transport.py, compare_phase_runs.py e combine_continuation_families.py. Para nova reprodução usar diretório separado e os registros/priors congelados; não sobrescrever esta rodada. As tentativas e falhas anteriores permanecem.

Ficha de aproveitamento: reutilizadas as formas de onda, injeções, propostas registradas, somas independentes e mistura validada. Esta entrega consolida resultados existentes; não acrescenta camada ao um.py, não altera teoremas e não move o gate. Outros SNR/leituras do objetivo integral ainda estão pendentes.

## Custódia — hashes SHA256 lidos nesta rodada

- `cache\source_evidence\phase_native_repeat\SEOBNRv4HM_seed130942_N16384\RESULT.json`: `edf7270513171e3e15f2c2bf2674149112a9c76da7b89890402104a7b04ac043`
- `cache\source_evidence\phase_native_repeat\SEOBNRv4HM_seed130942_N16384\RESULT_ARRAYS.npz`: `8411f30d8bbbad96c63989f7eebb62ea609af3d1ca1cd75308e5dd75f90ba0ff`
- `cache\source_evidence\phase_native_repeat\SEOBNRv4HM_seed130942_N16384\DENSITY_AUDIT.json`: `ec124d173cf28fc3edaf51113575f6f26ae86d02634b6c1be1be9d49e607d1c8`
- `cache\source_evidence\phase_native_repeat\SEOBNRv4HM_seed130942_N16384\PROPOSAL_COMPARISON.json`: `2b20c08d7a87516a3bd4a145b0227bb72248b3915a8ed0596c1913590cea9f2b`
- `cache\source_evidence\source_family_combination_real_repeat\RESULT.json`: `016daeb721a618e7c4bfc32e6049ab26652b28581e24d55d611e5560d5044186`
- `cache\source_evidence\source_family_combination_real_repeat\RESULT_ARRAYS.npz`: `b6e25892a1e5649c0d4abc371a611b6198d0f84ae70a20770a4e5fda202de613`
- `cache\source_evidence\source_family_combination_real_repeat\REGISTRATION.json`: `343ac83372ca1ded6e66bbbc143e0b973027b26eddc235408c360ae5eba53fbd`
- `cache\source_evidence\audit_phase_source.py`: `43f4c78aec69f141c7c2a1bd860ed728fcbfb32ece6a7d0327cb872a1d9418bb`
- `cache\source_evidence\combine_continuation_families.py`: `4d5bf82f749e5bb553cb9c6f5a085d8a85ee60c4c0717fad415f33a33fcfb335`
