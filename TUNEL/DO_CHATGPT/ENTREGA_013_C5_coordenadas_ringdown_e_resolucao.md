[REAL — resultados numéricos; OPEN — precisão científica da fonte e calibração]

# ORDEM 013 — coordenadas de ringdown e resolução

2026-09-22T06:16:54.151116+00:00. N/A — sem Lean. O objetivo permanece a confrontação precisa, sem selecionar relógio/partição e sem mover gate.

## O que a nova rodada efetivamente mediu

**PAGO:** a rodada adaptada2048 terminou (1656 propostas no domínio); a auditoria independente de soma deu diferença máxima6.9277916736609768e-14. O controle de geração8192→16384Hz nos54 pontos dominantes deu variação relevante máxima0.015403299371428147, abaixo de0,1.

**NÃO PAGO:** ZERO/1200 comparações passou a precisão. A ESS mediana passou de2.34379764 para3.30563467 com o DOBRO de propostas; eficiência por proposta caiu de0.00228886488 para0.00161407943. 672/1200 razões mudaram mais de0,2; mudança máxima2.89545111. A média favorável de uma célula não é evidência aceita. Não repetir essa proposta inalterada como solução da precisão. Nenhuma média dos dois pilotos foi fabricada.

## Resolução em SNR alto

**PAGO:** controles em duas famílias de recuperação, três fontes, O4/O5, a=0;0,37;1, ambas as famílias/amplitudes injetadas,50 ruídos pareados por célula. A tabela conta avaliações em pontos de fonte fixados, não posteriores integrados. Critério: alteração de logL≤0,1.

| SNR | 8192→16384 passa | 16384→32768 passa | maior alteração inicial | maior alteração seguinte |
|---:|---:|---:|---:|---:|
| 40 | 144/144 | 144/144 | 0.0924766589 | 0.0640261167 |
| 200 | 83/144 | 101/144 | 0.381504837 | 0.381252705 |
| 600 | 42/144 | 69/144 | 1.92511931 | 2.0697562 |

**NÃO PAGO:** precisão uniforme para SNR200/600. As injeções8192Hz foram conservadas e apenas reescaladas em amplitude: isso isola a resolução da recuperação, mas não valida a resolução da própria injeção em SNR600. Algumas avaliações fora da região posterior podem falhar sem dominar evidência; isto deve ser medido, não presumido. Não converter essas falhas em exclusão física.

## A mudança de coordenadas e o prior

**PAGO numericamente:** a mesma fonte é agora parametrizada para a proposta por

`y = (log(f220/250Hz), log(tau220/0.004s), u_q, u_spin2, u_cosi, u_t0)`.

Os parâmetros físicos originais continuam variando.250Hz e0,004s são somente unidades de coordenada e não relógios de dephasing. A forma de onda continua sendo gerada integralmente com os parâmetros binários recuperados pela inversa; a fase orbital continua integrada sobre0..2π.

Se `M_f = M_total * F(q,s1,s2)` e `chi = chi(q,s1,s2)`, então

`log f = log omega_R(chi) - log M_total - log F + const`,
`log tau = log M_total + log F - log abs(omega_I(chi)) + const`.

A derivada de F cancela no determinante. Nas coordenadas uniformes originais, a largura de M é60 e a de s1 é0,8. Portanto:

`J = |det(dy/du)| = (48/M_total) * (dchi/ds1) * d[log(omega_R/abs(omega_I))]/dchi`.

> [nota operacional do operador — omitida no retrato público]

Verificações: 512 idas/voltas em duas famílias, erro máximo1.2234657731369225e-13; determinante por diferenças finitas independente, erro relativo3.3702774127064572e-08; 18 integrais condicionais de normalização/momentos, erro máximo6.8746619508175399e-10; grade de monotonicidade com5202 pontos. São verificações numéricas do ajuste e da spline; não se intitulam prova formal global. Controles locais continuam ativos na inferência.

O oráculo da proposta sorteou32768 pontos independentes. Normalização estimada1.02106715±0.0159460624 (erro Monte Carlo); maior desvio padronizado entre13 momentos=1.54879464. Isso testa a distribuição computacional; não é significância física.

## Execução e pendências

**EM EXECUÇÃO:** `phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048`, sessão73887; registro observado304/1473. Revalidar o handle. Não duplicar por timeout. Sessões38040,85447 e75295 foram observadas terminais com código0.

Scripts em `cache/source_evidence`, Python `/opt/pycbc_env/bin/python -B`:

```text
compare_phase_runs.py phase_runs/IMRPhenomXPHM_seed130801_N1024 phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048
audit_phase_source.py ../phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048 --rate --processes 6
check_phase_high_snr.py
validate_ringdown_coordinates.py
transport_phase_source.py fit
transport_phase_source.py oracle
transport_phase_source.py run --draws 2048 --seed 130841 --processes 6
```

Todos esses comandos já executados ou iniciados; artefatos create-once recusam sobrescrita. Reproduzir em cópia preservada. Primeiro conferir precisão da nova rodada, densidade/jacobiano, amostras externas e resolução nos pontos relevantes. Permanecem repetição, recuperação SEOB integrada, outras leituras, calibração contínua de a e resolução em SNR alto. C6 e o programa canônico não foram alterados. Nenhum lnB destes pilotos foi promovido a resultado aceito ou a sigma.

## Custódia medida

| arquivo relativo à bancada | SHA256 |
|---|---|
| `cache/source_evidence/check_phase_high_snr.py` | `4e91281611aea23ee4c3a2cdbf2cc5eddf1777f8305a2bae497157e5930b2b29` |
| `cache/source_evidence/PHASE_HIGH_SNR_CONTROLS.json` | `a1eb1dc15fdff83e6a633178aa787153d53258382014e804a941e3cf8d98fd82` |
| `cache/source_evidence/compare_phase_runs.py` | `0d75c49a79ce21ee90231994e8ed7673ca81debb201e94bb8fb9a09dd852741f` |
| `cache/source_evidence/ringdown_source_coordinates.py` | `361c7b919374325878c553d712655b74edf40ffeef23401df98c5151f76e226f` |
| `cache/source_evidence/validate_ringdown_coordinates.py` | `d0203622412eef46eaafe40a25dd64c7c9a23d084379f1be16489ca145cda4b4` |
| `cache/source_evidence/RINGDOWN_COORDINATES_VALIDATION.json` | `766b7cdb1b73084281c255ce114094354a6061a0d2fe499c867d90ecfece60ed` |
| `cache/source_evidence/transport_phase_source.py` | `5efc1eb9881a785c7ba48b3099f0005729b19cc4d5a7e38770407a1c9b560fa9` |
| `cache/source_evidence/phase_ringdown_transport/REGISTRATION.json` | `882e1e548c56e553541420ae507837f69c76b114ebc5fcb6d65a099cb6e52524` |
| `cache/source_evidence/phase_ringdown_transport/PROPOSAL.json` | `8a6243e1c11156220ee7a8a6e89cce23d9443f163165686c619ced97ca747f56` |
| `cache/source_evidence/phase_ringdown_transport/PROPOSAL_ORACLE.json` | `6ae1e34150bf08d297a7b9bf82d7924575434907abdd563f4d79bc54a2dbd4a2` |
| `cache/source_evidence/phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048/RESULT.json` | `c9ffc43fc377cc32f1e04068808fb8008c37b175b373ab58b425bdfc7b33d57c` |
| `cache/source_evidence/phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048/RESULT_ARRAYS.npz` | `4cd54d0eb221e66b91f6a1728d445e7cfa4d1eb65fb6dac83b1c2ee3e8294034` |
| `cache/source_evidence/phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048/PROPOSAL_COMPARISON.json` | `db1fa5b678b3a15d17f93cbab4f6c5019213a98f28144cd65c8ea71f6ab93d5a` |
| `cache/source_evidence/phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048/AUDIT_RATE.json` | `a9cd2026589112bc823f9766dd3e32f571cb7999faed1173c021d0a0edb37029` |
| `cache/source_evidence/phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048/START.json` | `4b6aff10f635d78da25000f980e4745901a8a71f0f131a92039804ae09a2bfe5` |
| `record_ringdown_coordinates_progress.py` | `e6d0bb547dfab6e7c8b8d340aa5457b9ee70162fd2336e73c6b5903aa64eb65f` |
