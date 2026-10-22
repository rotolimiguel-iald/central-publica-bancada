# Ordem 013 — ruído empírico e primeira rodada registrada em strain

UTC: 2026-09-22T01:07:35.184955+00:00

[REAL — análises computacionais condicionais; objetivo integral ATIVO]

A C6 foi executada após o registro verificável no túnel. Foram lidos os arquivos públicos H1/L1 do evento, preservando as janelas e os três priors de amplitude registrados. Massa e spin foram integrados com priors próprios uniformes, sem usar o posterior do mesmo evento como prior.

Registro C6: `ded00f09b5010d622b67b4ea4e559a216818f578440a0f60772130174ececf14`. O erro máximo entre grades nos log-fatores de Bayes foi 4.96819297e-06.

| Leitura | ln B na janela primária 10 tM |
|---|---:|
| R-GLOBAL | 0.000000000 |
| R-B | -0.002595070 |
| R-RAIZ-0 | -0.043068118 |
| R-LIN | -0.090862677 |
| R-MOD | -0.251294964 |

Esses números são razões condicionadas ao modelo 220+440 com amplitudes por detector. Todas as janelas recebem INCONCLUSIVE_SYSTEMATICS por regra registrada: os controles com duas famílias IMR não passaram o critério completo de viés/cobertura. Não há sigma de descoberta nem exclusão física.

A integral analítica das amplitudes foi conferida por covariância gaussiana independente e quadratura numérica. O ruído simulado diretamente no domínio de Fourier reproduziu a covariância projetada. Ruído real: 256 intervalos por detector; flutuações dos filtros entre 0,94 e 1,07 da escala prevista. Foram preservadas três tentativas numericamente instáveis antes da seleção de amostras e projeção estável.

C5: 480 células × 50 avaliações pareadas, cinco tempos, três SNRs, oito leituras e duas famílias (SEOBNRv4HM e IMRPhenomXPHM). Contagem: {'UNIDENTIFIABLE_AT_NUMERICAL_AND_OBSERVATIONAL_PRECISION': 240, 'INCONCLUSIVE_SYSTEMATICS': 240}. O mesmo ruído é reutilizado entre hipóteses para controle; não somar como eventos independentes.

A comparação com oito posteriores Kerr publicados em 6, 8, 10 e 12 tM foi realizada. Há diferenças de modos, priors, processamento e referência de tempo (0,0001095 s), explicitadas no JSON. Não existe posterior de 10,5 tM no índice inspecionado. Não foi declarada reprodução da análise pyRing.

A análise conjunta anterior 220+440 permanece em C4_JOINT_MODES.json; não foi multiplicada por esta nova análise do mesmo evento. O consumidor Bilby e a extensão angular multimodo passaram controles independentes com LAL.

**O que falta no objetivo integral**

- C0: três fontes integrais continuam com falhas 403/406 documentadas; não anunciar leitura integral.
- C2/C3: finalizar interfaces reutilizáveis de Cauchy e Poisson coerente no pacote; escolha física de desenrolamento e partição continuam hipóteses explícitas.
- C4: conferir release GWTC-3 sem duplicar eventos; procedência integral da fusão de posteriores/binário pyRing permanece ressalva. A comparação de quatro tempos foi realizada; 10,5M não existe no índice do release.
- C5: completar injeções com outras PSDs (O5/ET/CE) por recoloração validada; medir distribuição calibrada de evidência, não apenas Fisher.
- C5/C6: modelo fundamental 220+440 falhou no critério de viés/cobertura para duas famílias IMR; localizar e tratar a discrepância de modos/overtones e de priors. Qualquer novo acesso orientado pelo resultado exige adendo NÃO-CEGO, preservando o registro C6 e seus resultados.
- C6: a rodada registrada em H1/L1 foi executada em cinco inícios e três priors, com massa/spin marginalizados e convergência. Ainda não é uma verossimilhança coerente completa nem uma réplica pyRing; não promover INCONCLUSIVE_SYSTEMATICS a exclusão.
- C7: concluir pacote independente em inglês, tabela de escopos, comandos e teste de reprodução; auditar objetivo integral antes de marcar completo.

**Artefatos e hashes medidos**

- `C4_JOINT_MODES.json` — `8b2e0fea734caed23f05c3a9f9a2f3f7aaa8f19ed71d2f9d9a841129739e742f`
- `C3_MULTIMODE_TEMPLATE.json` — `20ada0cc440388aa636cd78e40a1330433137d7fd5bd7d10ce689a40f40bd7f1`
- `C3_BILBY_CONSUMER.json` — `993b705cebf2cc3449fc473ab9cac185d58096e8a6a8f26bc1a2d01280821aad`
- `C2_TEMPLATE_CHECKS.json` — `b43fa517a37f9b41b8aa2d4f699571a4e24c7da5f6027266e55a86b6ffbe579a`
- `C5_EMPIRICAL_NOISE.json` — `a748e279a04f08e0218bcda347ff9d2750068e53b2cefed35a6b36935199e3ef`
- `C5_IMR_CONTROLS.json` — `1fe989525c3c9cff7059caa748eea541f94d01f9d416840117072c1f094fe2c1`
- `C5_EMPIRICAL_IMR.json` — `f5ea9f58ec31b75079b20caf9a891e26bea2dfb7414ae1035e65278b2a7a34fc`
- `C5_EMPIRICAL_IMR_STARTS.json` — `220117a57b178018de94ae212a7a8f2afaceff07585ea30ad3b394336ed0c145`
- `C5_LIKELIHOOD_VALIDATION.json` — `49f36dc63a2193a92e7f0be66395c9d802e4b1ab5c88f346d046665c288ebfaf`
- `C5_FISHER_EMPIRICAL.json` — `00fbe67f5aa5b38212e8b6c4e6654d09e6cbc23b9e0e5306ee3d7cb77a3bc508`
- `C6_RESULTS.json` — `781a3741a68875eba0fcef02d596dab7d36103d9e926edc6bec18fb485a055e8`
- `REGISTRO_C6.json` — `ded00f09b5010d622b67b4ea4e559a216818f578440a0f60772130174ececf14`
- `C6_DOWNLOADS.json` — `188ecebffcdeabc819b5f3e852da5d2670a95475299d6177bf479f54d86483aa`
- `C6_PYRING_START_COMPARISON.json` — `59dfef3554288c6117debec7827a8b7cd56c6422ff3710a8a39deb4470645a18`
- `C6_SYNTHETIC_GRID_0.json` — `467d3c3fc2663a034ecc2ed399956b7ef9009c43da7562a54453597a7a71591b`
- `C6_SYNTHETIC_GRID_1.json` — `0ec71b78873dcbed1326db580dcb6c5a04fee5c74302357031c370c511ae1909`
- `tgl_ringdown_prediction.py` — `fd0fc446e1c732f3d782210c6effa7cb7faeaeb7a51a434d4f397f1da89bd652`
- `tgl_ringdown_template.py` — `16d7fbc25e94b0351e7050aa5055db421365953782cec1a668d68f11e5cc5132`
- `tgl_ringdown_likelihood.py` — `f16517e62fca96cc348aac17369e75e1fb9b07f1e95fef06f7630c8b94153bca`
- `prepare_empirical_noise.py` — `5683b5324c2d099060a1b236b6babd2c35be31e9a3a168f64740742bde7cdffd`
- `prepare_imr_controls.py` — `5139864946af88ee0f4f3c52f85edba0acd690ab1249489068bb4677004f3e19`
- `empirical_imr_recovery.py` — `b4ea2d0e2326b229aa1b3913f65aeb16b5bcd3892bd489e61dd99bab8a6a071f`
- `verify_likelihood_and_noise.py` — `f91100fecaa2e6842042760ad2103de951ec800f3804888d21185b77763ae8d2`
- `c6_engine.py` — `94c724c4cb1764b7a62209da08c37a40d7936c98b344da714d1bd7733352de3c`
- `run_c6_grid.py` — `d3aa76afdc419ff3ac73321fc11bb405ae762cd0d219411be16affe8c7f347c1`
- `cache/MANIFESTO_DOWNLOADS.json` — `727ff51684585428840915d8460f21236f307656d32351031b4c5ba1b1c34b3c`

Manifesto atualizado: 92 arquivos de aquisição/derivação conferidos. Não foram alterados um.py, kernel, Atlas ou memórias canônicas; a gerência recebe esta entrega para incorporação.
