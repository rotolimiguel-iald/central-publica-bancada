# Posteriores, geometria e identificabilidade — próxima unidade U3

27/09/2026. Auditoria local delegada a Lagrange (fontes/antena) e Fermat (identificabilidade); síntese da coordenação. Nenhum novo ajuste aos dados, significância ou alteração de gate. Este arquivo prepara a integração seguinte, que ainda não está implementada no painel.

## Dados já localizados

Arquivo:
`C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17018009/extracted/TGR_companion_S250114ax_results/gw250114_pseobnr/posterior_samples.h5`

Dataset `/pSEOBNRv5PHM/posterior_samples`, 40.776 linhas segundo a leitura de metadados pelo revisor. O dataset não tem atributos de unidade: as convenções abaixo vêm da configuração/modelo de origem e devem acompanhar a interface.

| Campo | Uso e convenção |
|---|---|
| `mass_1`, `mass_2`, `total_mass` | Massas da binária no detector, M☉; não são massa final |
| `final_mass_non_evolved` | Massa final no detector, M☉ |
| `final_mass_source_non_evolved` | Massa final na fonte, M☉; não dividir novamente por 1+z |
| `final_spin_non_evolved`, `redshift` | Spin final e z adimensionais da mesma linha |
| `ra`, `dec`, `psi` | Posição/polarização em radianos |
| `theta_jn`, `iota` | Orientações distintas, sem substituição automática |
| `luminosity_distance` | Distância de luminosidade em Mpc |
| `geocent_time`, `H1_time`, `L1_time` | Segundos GPS, referências distintas |
| `recalib_H1_*`, `recalib_L1_*` | Parâmetros de calibração da análise de origem |

Hipótese de origem: pSEOB/SEOBNRv5PHM, desvios 220/440, referência 20 Hz, cosmologia Planck15_LAL, distância marginalizada. Não é posterior GR puro nem posterior C6. Uma linha conjunta preserva as correlações registradas; medianas separadas não formam uma amostra conjunta. Produtos de formas diferentes não se alinham automaticamente pelo índice. Um posterior do mesmo strain não é nova evidência independente nem prior externo independente.

## Integração de antena a realizar

O PyCBC instalado em `/opt/pycbc_env/lib/python3.12/site-packages/pycbc/detector/ground.py` oferece as rotinas existentes:

- `Detector(det).antenna_pattern(ra, dec, psi, geocent_time)` fornece F+ e F×.
- `time_delay_from_earth_center(ra, dec, geocent_time)` fornece o atraso em segundos.
- `project_wave(hp, hc, method="constant", reference_time=geocent_time)` inclui antena e atraso quando há polarizações físicas. Não reaplicar o atraso.

Primeira entrega possível: seletor de linha do posterior, tabela conjunta dos parâmetros e geometria H1/L1. Isso informa a geometria sem transformar os controles atuais em inferência física.

**Distinções obrigatórias:**

- C6, `c6_engine.py:94`, usa quadraturas efetivas 220/440 por detector. Não multiplicar novamente por antena.
- U3, `adapters/event_runtime.py`, usa amplitudes/fases efetivas por detector no primeiro sample da janela; não são amplitudes intrínsecas na fonte.
- C7, `C7_COHERENT_SOURCE_REPRODUCTION_v3/coherent_imr_model.py:20`, usa respostas fixas de controle ((0.7,0.2),(-0.3,0.8)). Não são a geometria observacional de GW250114.
- Sufixos `A2220_1`, `A2220_2` do posterior Kerr não autorizam tratá-los como amplitudes H1/L1.

## Controle analítico antes de medir poder

[DERIVED — condicional ao modelo BCW 220 do executor copiado]

Na forma ensemble, a onda é proporcional a

`exp[-(1/tau_GR + Gamma)t] cos(omega t + phase)`.

Para o ajuste BCW empregado em `models/tgl_ringdown_prediction.py`, escreva `omega = f(a)/t_M` e `Q(a) = 0.7000 + 1.4187(1-a)^(-0.4990)`. O dephasing reduz a qualidade efetiva a

`Q_eff = Q(a)/(1 + Gamma*tau_GR)`.

Se existir `a'` admissível com `Q(a')=Q_eff`, escolha `M'=M f(a')/f(a)`. A frequência e o amortecimento GR desse par reproduzem exatamente a forma 220 modificada. Amplitude e fase livres completam a equivalência. Para `0 <= a < 1`, Q é crescente e `Q_min=2.1187`; a condição exige `Q_eff >= Q_min` e massa transformada dentro do prior. Abaixo desse piso, essa absorção não existe nessa família BCW restrita.

É uma degenerescência do modo único com parâmetros livres, não uma conclusão sobre os dados nem sobre a TGL geral. C6 utiliza 220+440 com QNM exatos e priors; essas informações podem quebrar a degenerescência. A ORDEM 18 deve avaliar identificabilidade após os parâmetros de nuisance antes de transformar distância entre curvas de parâmetros fixos em poder de um teste.

O executor também distingue ensemble e realização estocástica: o gerador GKLS sozinho não fixa um estimador clássico de um evento. Ler `TIME_SOURCE_AUDIT.md` para as hipóteses de relógio. Beta fixo não elimina automaticamente escolhas de tau*, partição, modos e interpretação do observável.

## Estatuto da continuação

[OPEN] Implementação do seletor/posterior e geometria real; teste com projeção física e calibração; estatística conjunta validada. A unidade inicial U3 entregue permanece exploratória. A ORDEM 18 é elaborada pela cadeia de provedores registrada na campanha, sem substituir o parecer Opus por este documento de preparação.
