[REAL — fechamento somente de F2-R1; suporte da cauda permanece inconclusivo]

# Fechamento F2-R1

2026-09-22T18:15:00.589429+00:00. **Achado encerrado.** A v2 transporta o ESS e distingue estabilidade da quadratura de validade da densidade. Não há bloqueante remanescente da omissão nomeada; isso não transforma a cauda em suporte suficiente nem aprova limites físicos.

Conferi os 2.403 valores da grade quanto a dimensão, finitude e faixa [1,N]; reavaliei independentemente 51 pontos reportados/quantis/cruzamentos com scipy KDE e whitening por Cholesky, sem chamar o corretor. Maior diferença relativa de ESS: 3.10862e-15. As entradas coincidentes na grade concordam. Não recalculei a grade inteira nem a curva de densidade.

As nove frações de massa KDE em regiões de baixo suporte conferem por soma própria de trapézios. No teto 20:

| Banda | Massa KDE na grade com ESS < 100 |
|---|---:|
| 0.7 | 5.51319751% |
| 1 | 2.03889390% |
| 1.4 | 0.85050084% |

Essas frações são diagnósticos da aproximação KDE na grade, não probabilidades calibradas de erro. O limiar descontínuo não ganhou controle próprio de convergência; não se deve atribuir precisão física aos decimais impressos.

Os três cruzamentos brutos foram preservados e marcados INCONCLUSIVE_DENSITY_SUPPORT; data_supported_cut é null. Os quantis têm seu ESS; os nove posteriores mantêm quadrature_converged separado de density_validation_status, que explicita a cauda da normalização. Não houve recorte, renormalização em teto menor, apagamento de cauda ou mudança de prior: curvas, quantis, integrais, dois priors originais e demais campos antigos permanecem iguais.

Hashes de supersedes, builder e parecer conferem; original preservado. O status global é NONBLIND_RAW_CLOCK_DENSITY__INCONCLUSIVE_DENSITY_SUPPORT_FOR_CUT. Continua aberta a sustentação estatística da cauda, agora honestamente registrada.

Controle: `bis/c1_review/close_f2_support.py`, executado com `/opt/lal_env/bin/python -B` em WSL. Evidência: `bis/c1_review/f2_closing_results.json`, SHA256 `cf69273485cdd56b3039b1a6d4307c3bda1940df296282f809db874f3197ac99`; script SHA256 `e5eda912355e035107ea4be9b32bf63249e66f8d7f8b41448608b695ccb6eefb`. Reprodução em cópia isolada, pois as saídas recusam sobrescrita. Sem PE, novos posteriores, strain, C5 ou código de produção executado. Insumos intactos. Axiomas: N/A — sem Lean.

| Caminho relativo a ORDEM_013_RINGDOWN | SHA256 lido |
|---|---|
| `bis/F2_FREE_CLOCK_EXTENDED.json` | `5c2929bd4e7352227b7f573c9511abe9742ce5ba5526e3171aec6a014ff3e188` |
| `bis/F2_FREE_CLOCK_EXTENDED_v2.json` | `6443db084c8fad29db425914eb77a3238648cd069c3bff535f5851f557225d7d` |
| `refeito/correct_f2_clock_support_013bis.py` | `0e1fc61d2bd47d9c621341e2e326106ec7f3a2d7ec8c7cf774cfeeeb896b4aa9` |
| `bis/F2_DENSITY_CLOCK_REVIEW.md` | `b879f1468e9b09e2f144d8be3bc33424b74f1e9e4eeda83864bf1bbbb0e129a6` |
