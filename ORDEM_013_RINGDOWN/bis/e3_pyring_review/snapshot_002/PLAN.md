# Kerr22010M — preparação independente para E3.1

[REAL — fontes e código preparados; INPUT — desenho; OPEN — execução, convergência e equivalência da reprodução]

Calibração NÃO CEGA de GW250114. Nenhum registro E2 é criado ou alterado. Seis fontes E2 congeladas são dependências somente de leitura quando necessárias. Este pacote não leu séries de strain, não gerou sinais e não executou inferência. A execução depende da revisão independente deste código/manifesto e de autorização própria pinada. Não instalar pyRing nem modificar `/opt`.

## Modelo e legalidade dos priors

Fonte primária local: `cache/pyring_oracle/vendor/pyRing` versão 2.7.0, conferida contra o sdist existente. O INI publicado é `cache/public/17018009/selected/26f158d16a946d97.ini`. O cabeçalho do posterior `selected/b0e560a83a0d3d5f.dat:1` contém `psi Mf af cosiota A2220_1 A2220_2 phi2220_1 phi2220_2 logL`. Apenas esse cabeçalho foi interpretado nesta preparação; o arquivo é hashado sem calcular novas estatísticas.

**Achado contra o uso automático dos defaults atuais:** a documentação atual permite absorver harmônicos nas amplitudes quando a simetria não precessante está desativada. A fonte 2.7.0 (`pyRing.py:677`, `:745`, `:1060`, `:1182`; `waveform.pyx:1084`) mantém `cosiota` e harmônicos explícitos. O cabeçalho efetivo confirma a inclinação amostrada. Usar a variante absorvida mudaria o prior efetivo. A versão exata do executável da release permanece OPEN; a fonte 2.7.0 e o cabeçalho são as âncoras disponíveis, não prova de identidade de versão. [Documentação atual](https://lscsoft.docs.ligo.org/pyring/model_inputs/).

O desenho retém oito parâmetros livres: Mf uniforme [10,500] M☉ no **referencial do detector**; af uniforme [0,0.99]; cosiota uniforme [−1,1]; ψ uniforme [0,π]; cada A uniforme [0,50]; cada fase uniforme [0,2π]. `reference-amplitude=1e−21`, azimute global φ=0, razão máxima de amplitudes desativada. As amplitudes são complexas independentes dos ramos ±, compartilhadas pelos detectores, com raio uniforme; não são gaussianas cartesianas nem amplitudes independentes por detector. ψ continua livre, portanto não se precisa invocar uma equivalência por remoção de degenerescência.

Para φ=0: Y₊=√(5/(64π))(1+cosiota)² e Y₋=√(5/(64π))(1−cosiota)². Em convenção pyRing, h₊+i h×=10⁻²¹ exp(−u/τ)[Y₊ A₁ exp(iφ₁+i2πfu)+Y₋ A₂ exp(iφ₂−i2πfu)]. Nenhuma reflexão/conjugação entre A₁/A₂ é imposta. Fonte: `waveform.pyx:851` e `:1190–1228`.

Frequência e amortecimento usam **o fit Berti da fonte**, default `qnm-fit=1` (`initialise.py:232`), com os seis coeficientes extraídos do texto `data/NR_data/berti_qnm_fits.txt:2` e fórmulas `waveform.pyx:244–246`. Assim o domínio af≤0.99 não é extrapolação da antiga QNM_GRID limitada a0.98. Massas de componentes e cosmologia não entram. Não usar o novo helper remnant GR do PE IMR aqui: Mf/af são parâmetros diretamente inferidos e livres.

## Tempo, projeção e ruído

INI: trigger H1 1420878141.2190118; RA2.3332345218980706; dec0.19024356075903648; atraso fixo t0=0.003369s. “10M” usa o deslocamento fixado na release, não dez massas do Mf amostrado. A escala de massa usada no prior temporal original é68.40897469707073M☉, mas não se recalcula t0 durante inferência.

H1 e L1 recebem o mesmo modelo de polarizações. `lal.ArrivalTimeDiff(detector, H1, RA, dec, trigger)` define cada atraso; `ComputeDetAMResponse` é avaliada no tempo trigger+t0+atraso, conforme `likelihood.pyx:425–448` e `pyRing.py:335`. Os tempos relativos preservam a parte fracionária. A seleção usa a primeira amostra nativa com tempo relativo≥t0, sem arredondar o atraso/modelo a uma amostra inteira. Reporta-se o resto temporal de cada detector. 4096Hz, N=int(0.2×4096)=819, N/fs=0.199951171875s; a duração nominal não é escondida.

Segmento acolchoado de8s a partir de GPS1420878137; filtro Butterworth de quarta ordem20–2043Hz, `filtfilt`, sem taper no trecho final. Modelo não filtrado, conforme implementação pyRing2.7.0; a diferença para filtragem consistente também do modelo é limitação explícita em bordas de banda, não equivalência presumida. O buffer de ≥1s é verificado. Não se reamostra implicitamente.

Likelihood gaussiana temporal normalizada com covariância **Toeplitz819×819 por detector**, fator Cholesky e escala numérica10⁻²¹. Matrizes de detectores independentes são uma hipótese INPUT. Sem jitter, clipping ou piso adaptativo: não positividade, condição>10¹² ou Cholesky inválida causam falha visível. Não há projeção/marginalização analítica das amplitudes.

Ramo principal **Welch off-source**: primeiro bloco256s aprovado por qualidade/finitude, segmentos4s Hann, sobreposição50%, mediana corrigida SciPy, PSD unilateral. Seleção não usa nível de ruído ou posterior. ACF=(fs/2)irfft(PSD×|H|⁴), representando o filtro `filtfilt` aplicado à série. É controle próprio, não o PSD exato da release.

Ramo de robustez público: por complemento explícito do principal, foram extraídos somente os dois membros `bilby-NRSur7dq4_prod_[H1,L1]_psd.dat` para `cache/E3_KERR220_PSD_INPUTS`. O hash completo do tar confere com o índice, e os arquivos de819218bytes cada têm pins calculados em `PSD_EXTRACTION.json`. Cabeçalho `#Frequency Strain`, duas colunas numéricas; a coluna Strain é tratada como PSD pelo contrato de origem `pesummary/psds`, não como ASD. A identidade de unidades exatas do arquivo externo original permanece uma diferença documental. Ambos os ramos ficam **habilitados em ordem fixa: Welch → PSD público**, sem selecionar por melhor acordo posterior. O algoritmo externo2.7.0 usa intervalo estrito20–2038Hz, interpolação linear/extrapolação e ACF=(fs/2)irfft(PSD); recusa extrapolação não positiva. **Nada prova identidade com H1_PSD.txt/L1_PSD.txt do INI**. Os arquivos GWF C00_AR citados também diferem dos GWOSC disponíveis. Esses limites impedem declarar reprodução equivalente paga, mesmo que as medianas concordem.

## Posterior e critério de relato

Nested sampling Bilby/dynesty, oito parâmetros livres,512live, rwalk50, dlogz0.1, maxcall nominal1milhão, um processo/BLAS1, seed1234 INPUT de calibração. É amostrador diferente do publicado4096live; a alteração é documentada e não pode ser usada para escolher o resultado mais próximo. Reusa o adaptador pinado E2 que captura delta_logz antes de adicionar live points. Só emite comparação após delta_logz atingido, sem plateau/maxcall, ESS≥100 e posterior≥1000; parcial nunca aceito. Critérios de convergência não demonstram ausência de multimodalidade perdida.

Saída pareada NPZ (sem pickle lido), covariância amostral Mf/af e quantis5/50/95. Comparação com o posterior publicado existente: diferenças de medianas, std ddof1, sobreposição dos intervalos90%, distância KS marginal e diferença normalizada por larguras em quadratura. Todos **descritivos**; z calibrado=null, sem BF, teste de equivalência ou evidência independente do mesmo evento. Interpretação igual-peso do posterior publicado preserva limitação da origem de merging. Alvo documental em `C6_PYRING_START_COMPARISON.json`, entrada “Fundamental220”/10M: Mf73.5052871323 [66.7354520371,79.9022405266], af0.7519521363 [0.6264694358,0.8347185993]; números herdados, não recalculados nesta preparação. `aud_2_C6.txt:42` resume o alvo; não usar os números do220+440 como se fossem Kerr220.

## Custo, autorização e execução futura

Teto conjunto **7200s**, limitado também pelo deadline real de `PART_B_BUDGET_START.json` e validade da autorização. Primário≤4800s, robustez≤1800s, resto para inicialização/revisão de saída. Relógio iniciado antes das verificações de custódia. Sem extensão automática, retries ou retomada de diretório. Reserva15s para limpeza de grupo e recibos. O controlador inicia grupo próprio, captura logs e limpa descendentes mesmo após saída do líder; reaproveita o helper E2 pinado sem editar sua fonte. Uma execução interrompida não ganha novo teto ao reiniciar: o diretório global exclusivo permanece.

**Estimativa ainda não medida:** duas fatorações819³ no preparo; por avaliação dois modelos819 e duas soluções triangulares, ordem10⁶ operações. Dependendo de tempo real0.5–5ms por avaliação,10⁶ avaliações custariam aproximadamente500–5000s além da preparação; essa faixa é planejamento INPUT, não benchmark. O máximo nominal não garante convergência. Logs/custo finais distinguem chamadas reais da likelihood, ncall interno e parede/CPU. Só o futuro piloto mede o custo. Não executar benchmark de waveform agora.

O principal/revisor deve ler código e `MANIFEST.json`, confirmar as limitações e emitir JSON próprio contendo `status: CALIBRATION_ONLY_REVIEWED`, `manifest_sha256` calculado, `reviewer`, `approved_utc`, `valid_until_utc` suficientemente longa para a janela escolhida. Não há autorização fabricada neste pacote. Comando futuro, **não executado**:

```text
wsl -- /opt/lal_env/bin/python -B "/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_pyring_preparation/controller.py" --authorization "<caminho WSL do JSON revisado>"
```

`build_preparation.py` apenas lê metadados/fontes, verifica sdist, extrai coeficientes textuais, cria CONFIG/SOURCE_REVIEW/MANIFEST e verifica sintaxe estática. Essa preparação inicial foi preservada byte a byte em `snapshots/pre_public_psd_001`. `extract_public_psds.py` extrai somente os dois membros nomeados, sem executar nada do tar, e registra a leitura de46,884s. `finalize_preparation.py` incorpora pins e esquema PSD, atualiza as dependências E2 para a guarda final de ativação e emite o manifesto final. Somente stdlib nessas etapas; não importam os módulos científicos preparados. Não constituem registro, autorização ou ensaio. Axiomas: N/A; teoremas novos:0. A aceitação inferencial E3.1 permanece **NÃO PAGA** até execução/revisão, e equivalência de PSD/strain/versão permanece OPEN separadamente.
