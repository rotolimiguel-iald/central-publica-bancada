[REAL — código e metadados conferidos; observável físico OPEN]

# C3.1 — README de convenções e lacunas (013BIS)

O módulo prediction(..., observable="realization") não fornece uma previsão universal de δτ̂ médio ou dp(δf̂): **NÃO PAGO** como distribuição física calibrada. Os estimadores condicionais de C2 estão em C2_ADENDO_OBSERVAVEL.md e no JSON de mil trajetórias, com seus desenrolamentos nomeados; não preenchem esse campo por identidade de nomes.

## Relógio, regressão e constantes

A chave que reproduz o v346 é delta_tau_linear=−x, x=ΓτGR. A expressão de ensemble exata é delta_tau_ensemble_exact=−x/(1+x). LEGACY_V346 mantém constantes históricas e não é CODATA2018/IAU2015. As diferenças medidas do perfil completo, em z=0, e as 264 linhas de compatibilidade estão em C1_ADENDO_CORRECOES_013BIS_v2.md; o controle atualizado recusa cobertura parcial, duplicatas, NaN e dependências alteradas.

## t_start, pico e t0

tgl_ringdown_template.py:58–59 usa time>=t_start e elapsed=time−t_start, em segundos no referencial do detector. Se time contém GPS, t_start deve conter GPS; se time já mede tempo desde um pico, t_start é um deslocamento nessa mesma origem. O template não identifica o pico automaticamente e sua amplitude/fase são definidas no início declarado.
Na C6-pre, requested=reference_peak_GPS[detector]+n×reference_tM_seconds; seleciona-se o primeiro sample original a 4096 Hz não anterior ao pedido e depois stride=2. A base de c6_engine.py:82 recomeça em zero no primeiro sample retido; portanto o início realizado pode diferir de n tM. Massa de referência do corte é fixa, não a massa corrente de cada ponto do posterior. São hipóteses e convenções do diagnóstico antigo, não um novo ajuste.

| n nominal | detector | GPS pedido | GPS primeiro sample | arredondamento (µs) | n realizado |
|---:|---|---:|---:|---:|---:|
| 6 | H1 | 1420878141.2209241 | 1420878141.2209473 | 23.1266 | 6.0689408 |
| 6 | L1 | 1420878141.2184286 | 1420878141.2185059 | 77.2476 | 6.2295621 |
| 8 | H1 | 1420878141.2215979 | 1420878141.2216797 | 81.7776 | 8.2426362 |
| 8 | L1 | 1420878141.2191024 | 1420878141.2192383 | 135.899 | 8.4032576 |
| 10 | H1 | 1420878141.2222719 | 1420878141.2224121 | 140.19 | 10.416332 |
| 10 | L1 | 1420878141.2197764 | 1420878141.2199707 | 194.311 | 10.576953 |
| 10.5 | H1 | 1420878141.2224402 | 1420878141.2226562 | 216.007 | 11.140897 |
| 10.5 | L1 | 1420878141.2199447 | 1420878141.2199707 | 25.9876 | 10.576953 |
| 12 | H1 | 1420878141.2229457 | 1420878141.2231445 | 198.841 | 12.590027 |
| 12 | L1 | 1420878141.2204502 | 1420878141.2204590 | 8.82149 | 12.026083 |

C6_PYRING_START_COMPARISON.json registra pico H1 de Kerr pyRing 1420878141,2190118 e referência TEOB da bancada 1420878141,2189023: origens distintas, diferença aproximada 109,5 µs. Esse número é lido do controle arquivado; a presente conferência não reextraiu as configurações primárias. Kerr220/221 a 6,8,10,12 tM têm posteriores liberados; não há 10,5 tM nesse índice. A comparação de pipelines não é reprodução da mesma likelihood: modos, priors, banda, PSD e origem temporal diferem.

## Γ e overtones

O template geral calcula Γ por mode=(l,m,n) e QNM exato fornecido. A chamada para um overtone pode produzir uma taxa diferente da fundamental. Os controles C5 em diagnose_overtones.py:40–47 impõem outra hipótese: todos os overtones 22 recebem Γ220; os 44 recebem Γ440; os demais harmônicos ficam sem modificação. Isso acompanha a injeção fabricada que amortece o harmônico inteiro. Não são a mesma lei multimodo, nem uma escolha física inferida dos dados. O Fisher original usa só 220 e não resolve essa ponte.

PAGO: documentação das convenções, diferenças de constantes, chave de regressão e início realizado a partir do registro. NÃO PAGO: observável de realização universal, identificação física da lei dos overtones e reprodução completa da PE pyRing (reservada a E3.1). Nenhum strain foi relido.

Evidência JSON SHA256 56906841f92020988defa1dd774b02add88c34e6d18e9617375aab0323abcc1b. Reprodução: `python -B -X utf8 refeito/record_c3_and_f7_013bis.py` (saídas únicas; usar cópia de bancada para repetição). Fontes/hashes no JSON. Abertura SHA256 0118a54b7a806a0a5ef5572afc8349c223cc3da4bec62ff18a9cd1b07433f9f0. Axiomas: N/A — sem Lean.
