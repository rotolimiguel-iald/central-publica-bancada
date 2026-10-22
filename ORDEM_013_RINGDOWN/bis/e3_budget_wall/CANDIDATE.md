# E3.2 — candidato de orçamento por parede instrumental

**INATIVO, para revisão independente antes de qualquer ativação.** Nova PE=0; novas injeções=0; downloads=0; rebuild/workaround=0. Encerra esta tentativa E3.1 IMR por falha nativa medida, sem afirmar impossibilidade geral. Custo por posterior IMR convergido=null, não11s. Kerr não substitui qualificação da recuperação de deformações.

Relógio em 2026-09-22T23:02:56.988802+00:00: 3.939774h decorridas; 36.060226h restantes. Reserva final máxima2h, encerrando em 2026-09-23T01:02:56.988802+00:00; 34.060226h de ciência não alocadas/devolvidas, **não gastas**. Deadline global 2026-09-24T11:06:33.802143+00:00 intacto. A reserva não reinicia na ativação; atraso de revisão consome-a. Contabilidade contínua inclui orquestração e todos os trabalhos; não somar novamente custos dos jobs abaixo.

Kerr V1 394.298829s +V2 641.003189s de controladores = 1035.302019s; CPU 1026.449371s. São calibração não cega, equivalent_reproduction_paid=false. Piloto IMR falhou em 11.011140s. Diagnóstico nativo: 13.168752s wall somado, 10.400864s CPU,10processos/16chamadas. Diagnóstico Welch consta separado no JSON. Tempos de launcher/runner/componentes se sobrepõem; não somar com total do controlador.

## Cinco alternativas exigidas (ORDEM:194)

i. **Calibrar apenas pisos R-LIN/R-MOD** — Coeficientes recalculados abaixo; nenhum sigma_inj/custo de recuperação qualificada medido. Piso mais largo não corrige falha nativa. Alocação0; custo de programa qualificado=null/NÃO PAGO.

ii. **Calibrar somente bins de SNR alto** — Menor largura é expectativa condicional; viés abaixo do piso não demonstrado. Nenhum bin ou evento admitido por este candidato. Alocação0; custo de programa qualificado=null/NÃO PAGO.

iii. **PE reduzida com amplitude marginalizada** — Alternativa metodológica da ordem; instrumento diferente, sem implementação/custo/convergência validados neste escopo. Nenhum workaround executado. Alocação0; custo de programa qualificado=null/NÃO PAGO.

iv. **Reutilizar injeções públicas LVK** — Diagnóstico F2 existente revisado pode ser reutilizado descritivamente; duas recuperações com/sem44 não são curva c(SNR), cobertura repetida nem sigma_sys calibrado. Zero PE nova. Alocação0; custo de programa qualificado=null/NÃO PAGO.

v. **pSEOBNRv5PHM via pyseobnr em venv próprio** — Instalabilidade, custo e qualificação não medidos aqui; sem instalação, rebuild ou troca de runtime. Custo permanece null. Alocação0; custo de programa qualificado=null/NÃO PAGO.

##14 candidatos,10 sem hold e4 com hold

Ausência de publicação é limitada ao censo auditado; elegibilidade documental não é admissão. Cada entrada conserva fonte SNR/path/linha/hash, reviews e flags. Nenhum hold removido. Pesos abaixo: **proxy / E[I]**, respectivamente exp(−2μ) e exp(−2μ+2s²). Ajustes31/33 não são somados entre si; covariância dos coeficientes e intervalos preservados no JSON. Erros de seleção/transferência, s, SNR e nova família permanecem abertos. Sem leitura de posterior candidato.

| Evento | SNR | Flag | Ajuste31 proxy/E[I] | Ajuste33 proxy/E[I] |
|---|---:|---|---:|---:|
| GW230919_215712 | 16.8 | sem hold | 12.173 / 13.471 | 12.663 / 13.996 |
| GW241111_111552 | 16.3 | sem hold | 11.497 / 12.723 | 11.987 / 13.249 |
| GW240930_035959 | 16.1 | HOLD | 11.232 / 12.430 | 11.721 / 12.956 |
| GW240513_183302 | 14.5 | sem hold | 9.216 / 10.199 | 9.692 / 10.713 |
| GW240920_073424 | 14.0 | sem hold | 8.624 / 9.544 | 9.094 / 10.052 |
| GW250118_170523 | 13.9 | sem hold | 8.508 / 9.416 | 8.977 / 9.922 |
| GW241130_034908 | 13.8 | sem hold | 8.393 / 9.288 | 8.860 / 9.793 |
| GW240923_204006 | 13.6 | sem hold | 8.165 / 9.035 | 8.628 / 9.537 |
| GW241210_060606 | 13.4 | sem hold | 7.939 / 8.786 | 8.399 / 9.284 |
| GW240615_160735 | 13.1 | HOLD | 7.607 / 8.418 | 8.061 / 8.910 |
| GW250109_010541 | 13.1 | sem hold | 7.607 / 8.418 | 8.061 / 8.910 |
| GW240515_005301 | 12.8 | HOLD | 7.281 / 8.057 | 7.729 / 8.543 |
| GW241102_144729 | 12.7 | HOLD | 7.174 / 7.939 | 7.619 / 8.422 |
| GW250104_015122 | 12.1 | sem hold | 6.547 / 7.245 | 6.978 / 7.713 |

Somas condicionais e frações dos alvos E0 constam do JSON por ajuste, separando10/4/14. Não são poder, ganho realizado ou evidência física. A incerteza conjunta não é a soma de erros independentes. Não há ranking por custo/hora.

## Ncalib e alcance

N=(k²/δ²)σ_inj², k5/15. Coeficientes das10 leituras recalculados dos deltas E0; σ=.0497/.058/.24 são INPUTs ilustrativos da ordem, não resultados deste piloto. Cinco bins×duas famílias é desenho mínimo, não matriz paga. Contas pressupõem média sem viés de replicações independentes de variância finita; não pagam cauda5σ ou viés desconhecido. Leituras subresolução ficam com N_target_operational=null e coeficientes analíticos separados. Nenhum N ilustrativo vira job/alocação.

GR nas duas famílias, TGL por leitura, c(SNR), sigma_sys(df), cobertura e440 não foram calibrados por nova PE: NÃO PAGO. dtau livre na recuperação não equivale a injeção TGL; família alternativa nãoGR permanece não implementada. Gate não verde.

## Esquema, preservação e revisão

`ORCAMENTO_40H_CANDIDATE.json` usa esquema documental próprio; registered_utc/witness=null tornam-no deliberadamente não ativável. `ZERO_JOBS_V2_CANDIDATE.json` tem contrato E2_PE_JOBS_V2 com jobs={} e downloads={} e parentE2 pinado. **Empty jobs não revoga o piloto estático nem downloads originais**: o guard agrega. Não relançar piloto. O principal integra o fechamento documental após revisão independente; nenhum registro, testemunha ou ORCAMENTO ativo foi escrito aqui. Serializer opcional anterior não foi usado/importado.

`frozen_inputs/` contém cópias byte a byte dos metadados/fontes selecionados; `FROZEN_INPUTS.json` dá pins e origens. Nenhum posterior/strain/pickle. Fontes limitadas25MB. `FINITE_CHECKS.json`: 136 controles positivos/negativos, sem experiências. Todos os arquivos escritos enumerados em `MANIFEST.json` (auto-hash omitido para evitar circularidade).

Verificação somente leitura:

```powershell
C:\Python314\python.exe -B "C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\e3_budget_wall\build_budget_wall.py" --verify
```
