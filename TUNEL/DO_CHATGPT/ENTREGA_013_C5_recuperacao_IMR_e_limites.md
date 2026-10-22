[REAL — injeções, cálculo e custódia; DERIVED condicional nas taxas; NÃO-CEGO; sem promoção a confirmação física]

# Ordem 013 — recuperação com formas IMR completas

UTC: 2026-09-22T03:44:40.108419+00:00. Axiomas: N/A — sem Lean.

## Resultado

As formas IMR completas substituíram a base curta de QNMs somente neste novo estudo. Foram preservadas as duas famílias, oito leituras, β calculado em runtime e os critérios viés≤0,2, cobertura de 90% em [0,80;0,97], sem borda.

**19 de 24 grupos identificáveis passaram** conjuntamente nas duas famílias e nas duas amplitudes com a mesma verossimilhança de mistura. Total: 576 células, 206 intervalos de ruído por célula, O4/O5 e SNR de ringdown 40/200/600. Os intervalos 50:256 eram externos ao treinamento da PSD e não foram usados no forecast anterior de 50 injeções; são reutilizados entre cenários, não 118.656 eventos independentes.

Há 78 células individuais aprovadas na mistura e 76 na recuperação pela própria família. **Nenhuma das 96 células identificáveis recuperadas somente pela família oposta passou.** Metade das 576 células é sub-resolução e não recebe um selo de calibração.

| PSD | Leitura | SNR de ringdown | Duas famílias × a=0/1, mistura |
|---|---|---:|---|
| O4 | R-B | 40 | NÃO PAGO |
| O4 | R-B | 200 | PAGO neste conjunto |
| O4 | R-B | 600 | PAGO neste conjunto |
| O4 | R-RAIZ-0 | 40 | PAGO neste conjunto |
| O4 | R-RAIZ-0 | 200 | PAGO neste conjunto |
| O4 | R-RAIZ-0 | 600 | PAGO neste conjunto |
| O4 | R-LIN | 40 | PAGO neste conjunto |
| O4 | R-LIN | 200 | PAGO neste conjunto |
| O4 | R-LIN | 600 | PAGO neste conjunto |
| O4 | R-MOD | 40 | NÃO PAGO |
| O4 | R-MOD | 200 | PAGO neste conjunto |
| O4 | R-MOD | 600 | PAGO neste conjunto |
| O5 | R-B | 40 | NÃO PAGO |
| O5 | R-B | 200 | PAGO neste conjunto |
| O5 | R-B | 600 | PAGO neste conjunto |
| O5 | R-RAIZ-0 | 40 | NÃO PAGO |
| O5 | R-RAIZ-0 | 200 | PAGO neste conjunto |
| O5 | R-RAIZ-0 | 600 | PAGO neste conjunto |
| O5 | R-LIN | 40 | PAGO neste conjunto |
| O5 | R-LIN | 200 | PAGO neste conjunto |
| O5 | R-LIN | 600 | PAGO neste conjunto |
| O5 | R-MOD | 40 | NÃO PAGO |
| O5 | R-MOD | 200 | PAGO neste conjunto |
| O5 | R-MOD | 600 | PAGO neste conjunto |

## O limite que impede promover o resultado

O gerador verdadeiro está contido na mistura, e a fonte é um único binário com massas, spins, inclinação e fase fixados. O teste paga calibração **dentro desse conjunto fechado**, não robustez para uma fonte arbitrária ou estimação dos parâmetros desconhecidos. A análise por família oposta torna esse limite mensurável.

**R-B em SNR40 continua NÃO PAGO**: viés entre 0.0469238 e 0.918529; cobertura entre 0.752427 e 0.84466. O sucesso de SNR200/600 não se transporta para a sensibilidade atual. Uma razão de Bayes média positiva também aparece sob a=0 em baixo SNR; não convertê-la em sigma.

As taxas são aplicadas a todo o conteúdo dos harmônicos 22/44, cada qual com sua taxa fundamental; outros harmônicos permanecem como no controle. Essa transposição continua condicional. A mistura bayesiana tem prior 1/2 para cada família e soma evidências; o máximo entre famílias é usado apenas no perfil diagnóstico. Não se seleciona a família que produz a frase desejada.

## Verificação e reprodução

- **PAGO:** registro separado antes da execução, código e entradas conferidos por hash; nenhum novo strain on-source lido.
- **PAGO:** critérios recalculados de todas as 288 células identificáveis a partir dos sorteios gravados.
- **PAGO:** 96 células e 288 sorteios conferidos por integral SVD independente; maior diferença de ln B = 1.0768417269e-09. A base da própria família contém exatamente a injeção sem ruído, controle explícito que não é robustez externa.
- **PAGO:** reprodução em pasta nova: 9247 campos numéricos, identidades e estatutos conferidos; todas as diferenças nos arrays de sorteios foram zero.
- **PAGO:** pacote `cache/C7_IMR_RECOVERY_REPRODUCTION_v1.zip`, 15583002 bytes. Começa de matrizes IMR/ruído derivadas e conferidas. A produção dessas entradas desde strain público/PyCBC/LAL já está no pacote anterior C7_INJECTION_REPRODUCTION; não foi repetida.
- **NÃO PAGO:** marginalização de parâmetros da fonte e validação fora do conjunto finito contendo o gerador da própria injeção.
- **INALTERADO:** C5 anterior, C6 congelado, veredito INCONCLUSIVE_SYSTEMATICS, escolha física da partição/relógio/leitura e gate canônico.

## Próximo passo

A recuperação IMR resolve a discrepância apenas no conjunto fechado testado: 19/24 grupos passam, mas o gerador verdadeiro está entre os candidatos e massas/spins/extrínsecos estão fixados. Para PE astrofísica, estudar a marginalização dos parâmetros da fonte e validação fora dessa identidade injeção-recuperação, com registro não-cego separado.

## Comando e aproveitamento

Descompactar C7_IMR_RECOVERY_REPRODUCTION_v1.zip e executar `python -B reproduce.py` com NumPy/SciPy. Ambiente efetivamente testado: Python 3.12, NumPy 2.5.3 e SciPy 1.18.1. A reprodução verifica o manifesto antes de executar e cria uma nova pasta de trabalho.

Reaproveitados os dois arquivos IMR, as PSDs, o ruído, as taxas e os QNMs já calculados. Nenhum pacote de sistema, um.py, kernel ou memória de outra casa foi alterado. STATUS, PROGRESSO e manifesto local atualizados com backups imediatos byte a byte. Nenhuma falha de execução nesta rodada; os negativos científicos permanecem nos arquivos.

## Custódia lida nesta execução

| Artefato | SHA-256 |
|---|---|
| `REGISTRO_C5_IMR_RECOVERY.json` | `804af656c37fef53cfd09abdec6745677efc7087551dd53f8cb95c66e00d7898` |
| `calibrate_imr_recovery.py` | `d409fa2225cc25a2eda8591b57f5e2e789c44b5eee647b2a6d525a69aab8c45a` |
| `C5_IMR_RECOVERY.json` | `bda4441856c23a643be6dc467b65059c4fc968d54971a73490710ffc67568cb6` |
| `verify_imr_recovery.py` | `8fed4447ecb57aa18aa0d5c5c6f80b7638a47d195c658f5caee35890891ab0f3` |
| `C5_IMR_RECOVERY_VALIDATION.json` | `0f40a767502a627ab68dcb801e44486d446c0f3d2582f6e668ab719766a2c8c7` |
| `package_reproduce_imr_recovery.py` | `c2f862223d0c333355dbf460fa79675dc497078cb250134d7986715f8ca84094` |
| `build_imr_recovery_package.py` | `080db29e02c925d8f08865bc5ab09d6da913e3a55c6edf818bc10b9d6b2e8a7f` |
| `C7_IMR_RECOVERY_PACKAGE.json` | `0bba01dba8cff4881e8e59d718b3396b96878115bc3447e2b4a8a7526fcb376a` |
| `C7_IMR_RECOVERY_REPLAY_VALIDATION.json` | `2553f7baa9848da82baf9eaa5d02a5554cfa84ccdd9c2581faafbd80238543a9` |
| `cache/C7_IMR_RECOVERY_REPRODUCTION_v1.zip` | `7dd26dad74ce5fc101c9183654af33394f62a3cb06e261704aa7ef3a64a98c22` |
| `cache/imr_recovery/O4_draws.npz` | `a79ab602d4b9fa2a1c9cf30de3cdf0ad663703a557ea88574473ec45e646c487` |
| `cache/imr_recovery/O5_draws.npz` | `1feacc7bf0f4e668a9afd8249778f21bc201c92e4e2f22dddc38f88bc3410434` |
| `cache/MANIFESTO_DOWNLOADS.json` | `580128a3ba513ebdac66effa64125b91f9c0d39f2cc9933af10c78073ac69b97` |
