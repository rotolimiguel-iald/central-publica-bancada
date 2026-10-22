# F4.3 — errata ao lado: relógio do Fisher B2 e relógio do V1

**08/10/2026 · auditoria cética documental.** Esta nota complementa `PLANO_E_PREREGISTRO.md` sem alterar seus bytes, o pré-registro JSON, o resultado, o mapa ou o quadro. Nenhum strain foi aberto e nenhum poder foi medido aqui.

| Peça | Relógio efetivamente usado | Alcance |
|---|---|---|
| Fisher E4.1/B2, leitura `R-B` histórica | `tau_star = G M_f,det / c³`, isto é, **k = 1** | [REAL — fonte e tabela] `delta_tau_440 = -0,0821606`, `z_local = 0,409281`, `N90 = 235,554` no recorte O4 com SNR isolado do 440 igual a 10, massa/spin/fonte fixos. |
| Hipótese primária do `PREREGISTRO_RAMO_B_RINGDOWN_V1.json` retomada pela F4.3 | `tau_star = k(chi_f) G M_f / c³`, **k(chi_f) = 2π / kappa_hat(chi_f)** | [INPUT] Relógio modular/KMS local do remanescente; a deformação adicional do 440 também é [INPUT]. |

**Correção de leitura:** a linha B2 da seção 4 do plano F4.3 é uma referência *histórica k=1*. Ela não fornece Fisher, z, N90 ou poder para o par atual `k(chi_f)=2π/kappa_hat(chi_f)` com 220+440 e massa/spin compartilhados e livres. Mesmo para k=1, B2 não paga a degenerescência da fonte livre nem a amplitude física do 440 por evento. O valor atual do poder do conjunto D permanece **NÃO MEDIDO / `AWAITING_POWER`**. A próxima etapa deve implementar o relógio V1 pinado em cópia e medir a projeção, os nulos e as injeções antes de qualquer abertura autorizada.

## Fontes conferidas por SHA-256 dos bytes

| Papel | Arquivo | Bytes | SHA-256 |
|---|---|---:|---|
| E4.1 chama `prediction.prediction(..., reading, mode=(4,4,0))` | `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\e4_e5_prepare\deterministic_e4_e5.py` | 24013 | `c5f8576c76a32f668580aac2386264e719ee8e1c425360d75c1551335063b694` |
| `R-B` histórico fixa `star = tm`, e `tm = M_f,det G/c³` | `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\tgl_ringdown_prediction.py` | 8382 | `fd0fc446e1c732f3d782210c6effa7cb7faeaeb7a51a434d4f397f1da89bd652` |
| Tabela B2/E4.1 com valor e hipóteses condicionais | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ENTREGA_013BIS_B2_registro_e_440.md` | 20687 | `06345093b5fca7b250f9360f66cf40bfc0becbd54b6e4cce4505f828f96fa8d7` |
| V1 nomeia `k = 2π/kappa_hat(chi_f)` | `C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_05out\PREREGISTRO_RAMO_B_RINGDOWN_V1.json` | 138727 | `86f98fcc124dd9cae04fdb06bd10c14175893253d5b139496bd4c05f109feee0` |
| Plano F4.3 preservado | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F4.3\PLANO_E_PREREGISTRO.md` | 8753 | `10c80b981c22df24a826cc454f746df2f0cb493acacd2358e2ca6b21182dbf46` |

Nenhum dos números do Fisher B2 foi recalculado nesta errata. O hash V1 atesta a fonte lida; a hipótese do 440 continua condicional, sem termo correspondente demonstrado no kernel.
