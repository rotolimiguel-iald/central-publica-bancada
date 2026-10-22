# Auditoria das fontes do tempo — bancada TGL

27/09/2026. **[REAL — leitura de fontes e conferência documental]**. Skill `tgl-atlas` consultada focalmente; buscas com `rg --max-columns 250 --max-columns-preview`. Nenhum original editado, nenhum `um.py` executado/importado, nenhuma compilação nova ou chamada a modelos. Este é o único arquivo entregue.

**Resultado:** há três fórmulas pertinentes, com papéis diferentes. O candidato recente mais diretamente chamado “TEMPO” é `the_tower_is_time` (v371); a ponte formal físico/modular usa BW/KMS; a escala `τ*` da lei de dephasing exige identificação física adicional. Não foi localizada uma definição literal `theta_t`/`thermal_time` no `um.py` e no TGLExt consultados. Não há base nesta auditoria para escolher silenciosamente uma delas como a única fórmula pretendida pelo operador.

Âncora: [índice vivo](<C:/IALD/Central de Patentes/memory/TGL_INDICE_VIVO.md:1>) registra v375. SHA-256 do `um.py`, calculado dos bytes nesta leitura: `ba234a6d384cb3f59ced49c94b643a71a002f65d284b01307cb088bbace5e2e0`. As linhas abaixo pertencem a esse arquivo e às fontes lidas nesta sessão; presença em fonte não equivale a recompilação aqui.

## 1. Fórmulas exatas e estatutos

**A. Torre de Jones como tempo — candidato recente explícito.**

```text
r = 1 / T.indexVal = T.markovWeight
1 / (1 / T.indexVal) = T.indexVal
T.indexVal = 1 / T.markovWeight
T.upper.E T.eJones = (((1 / T.indexVal : ℝ)) : ℂ) • (1 : M)
```

`TGLExt.IALDGraviton.the_tower_is_time`, [IALDGraviton.lean:116](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/IALDGraviton.lean:116>), linhas 116–125. Hipótese: `T : JonesTowerData N M Ext`, com as estruturas de anel/*-anel/álgebra declaradas nas linhas 111–114; peso positivo fornecido por T. **[KERNEL — enunciado/prova lidos]** para a álgebra; interpretar `1/r` como tempo é **[ONTO/INPUT]**, e identificar o peso genérico `w` com `β_TGL` é **[CONJ]**, expressamente nas linhas 116–117. A torre da luz mencionada nas linhas 34–37 tem peso 1/2, índice 2 e taxa 1/2: não substituir seu peso por β_TGL.

O [Atlas:27069](<C:/IALD/Central de Patentes/memory/TGL_ATLAS.md:27069>), adendo de 25/09, liga essa construção ao rito v7 e abrevia a linha 27075 como `tempo característico = índice = 1/β`. **A fonte Lean atual explicita o peso genérico e restringe essa identificação.** No rito numérico, [um.py:2493](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py:2493>) declara exatamente `Tempo caracteristico = 1/beta`, com estatuto `FINITE_DIM_SANITY_NOT_III1_PROOF`; [forma canônica:50](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um_absoluto_forma_canonica.md:50>) reproduz a leitura. É escala do parâmetro do modelo, sem calibração automática em segundos.

**B. Tempo modular e tempo de Killing — ponte condicional explícita.**

```text
Δit(t) = V(−2πt)
killingFlow(τ) = V(κτ)
T_Unruh = κ/(2π)
β_Killing = 2π/κ
β_Killing · κ = 2π
```

Fontes: [ContratoQG_v31.lean:229](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/ContratoQG_v31.lean:229>), campos `kms` e `bw`, linhas 229–234; [definições:260](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/ContratoQG_v31.lean:260>), linhas 260–265; [unruh_is_kms:407](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/ContratoQG_v31_Teoremas.lean:407>), linhas 407–438. **[DERIVED, condicional ao ContratoH2 W R N]**. `β_Killing` é período/inverso de temperatura KMS; não é β_TGL.

**[DERIVED — substituição dessas equações, sem novo lema compilado]**: para avançar no fluxo físico positivo, `s = κτ/(2π)` e `killingFlow(τ) = Δit(−s)`. Logo, se o painel usar o parâmetro de `Δ^{it}`, `t_mod = −κτ/(2π)`; se usar o fluxo KMS `Δ^{-is}`, `s = +κτ/(2π)`. Fixar a convenção evita inverter o fluxo. A rapidez do boost é `κτ`; não é o ângulo compacto θ_M.

`κ > 0`; `N : KillingNormalization` é **[INPUT externo]**, ponto do observador na cunha: [contrato:203](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/ContratoQG_v31.lean:203>). `kappa_eq_inv_radius` (teoremas:461), `kappa_fixed` (469) e `kappa_is_input` (520) distinguem κ fixo dado N de κ não escolhido pelo par. A normalização assintótica de um buraco negro fica fora desse tipo plano (208–209). Não restaurar unidades SI nem trocar κ espectral, κ da cunha e κ_H de Kerr por homonímia.

Evidência recente: [KMSStripConditional.lean:72](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_016_QG/A4/KMSStripConditional.lean:72>), `killing_kms_from_modular`, assume explicitamente `0 < kappa`, `H_regional_modular_strip` e `H_modular_equals_geometric`. O círculo periódico sozinho não fornece essas hipóteses (50–51). **[REAL — recibo anterior conferido]** [kms_strip_manifest.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_016_QG/A4/kms_strip_manifest.json>) registra rc=0; hashes de fonte e log recalculados e correspondentes; o log contém três declarações com `[propext, Classical.choice, Quot.sound]`. Isso verifica a evidência anterior, não uma execução nova.

**C. Escala de dephasing `τ*` — não é a coordenada temporal.**

```text
Γ_ω = (1/2) β_TGL τ* ω²
(dρ/dt)_diss = −(β_TGL τ*/(2ℏ²)) [H,[H,ρ]]
C(t)/C(0) = exp(−Γ_ω t)       [coerência no modelo exponencial]
β_TGL = ALPHA_FINE_CODATA_2018 × sqrt(e)  [runtime]
```

[um.py:193782](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py:193782>), `prove_clock_test_protocol_v369`: `τ*=t_Planck [PRINCIPLED IDENTIFICATION]`; o Hamiltoniano/partição física permanece escolha explícita nas linhas 193777–193812. **[DERIVED na forma; INPUT na identificação]**. A hipótese `τ* = 2π/κ_H` não foi derivada pela álgebra das dez leituras: [ten_readings_checked.json:21](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_016_QG/A4/ten_readings_checked.json:21>) registra `hypothesis_derived_here: false`; [tabela:5](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_016_QG/A4/ten_readings_table.md:5>) exige o mesmo horizonte e referencial. A fonte v375 ainda recebe `N : KillingNormalization` como argumento, [TetelestaiOneObject.lean:121](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/TetelestaiOneObject.lean:121>); não foi localizada uma quitação posterior dessa identificação de τ*.

## 2. Relógios que o painel deve distinguir

| Grandeza | Fórmula/papel | Requisito e estatuto |
|---|---|---|
| Reprodução da UI | posição/velocidade de navegação na série | Parâmetro operacional; não é tempo físico nem duração de execução do programa. |
| GPS do detector | `GPS_i = GPSstart + i·Xspacing` | Metadados reais do arquivo; índice isolado não basta. |
| Tempo relativo do detector | `t_det = GPS_i − GPS_ref,det` | Origem e detector nomeados; preservar deslocamento entre detectores. |
| Tempo da fonte | `Δt_src = Δt_det/(1+z)` | [DERIVED condicional] z informado e mesma referência de evento; não dividir a época GPS absoluta por `1+z`. |
| Tempo modular | `σ_s(A)=ρ^{is} A ρ^{−is}` ou `Ad(Δ^{is})` | Estado/álgebra e convenção explicitados; segundos requerem ponte/calibração. |
| `τ*` | parâmetro em segundos da lei Γ, distinto da variável t | Escolha de relógio, referencial e partição explícitos. `τ*_det=(1+z)τ*_src`. |

Fonte detector: [c6_engine.py:35](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/c6_engine.py:35>), `observed_windows`, lê `meta/GPSstart`, `strain/Strain.attrs['Xspacing']`, DQ/Injmask e produz GPS das amostras (44–64). Fonte transformação: [C1_LEITURAS_E_RELOGIOS.md:9](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C1_LEITURAS_E_RELOGIOS.md:9>), que também explicita: uma taxa modular exige `ds/dt`; β isolado não define segundos.

## 3. Executores locais já encontrados

**[REAL — implementação lida; não executada aqui]**. São rotinas científicas, sem despacho a provedores.

| Executor e localização | Uso possível e limite |
|---|---|
| [app.py:150](<C:/IALD/Central de Patentes/Chatgpt/TGL_BANCADA_OFICIAL/app.py:150>), `calculate`, operação `dephasing` (165–181) | Já recebe `omega_rad_s`, `tau_s`, `duration_s`; calcula Γ e 51 pontos de `exp(−Γt)`. Retorna `CONDITIONAL_MODEL_CALCULATION`. Não identifica τ* fisicamente. |
| [tgl_ringdown_prediction.py:64](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/tgl_ringdown_prediction.py:64>), `prediction` | Massa no detector, spin, leitura obrigatória, redshift e QNM. Retorna Γ, τ_GR, τ*_det e estatuto. R-A: `(1+z)t_P`; R-B: `GM_det/c³`; R-MOD: `2π/κ_H`, exige QNM exato e `ω−mΩ_H>0`, com `CONJECTURE_RESTRICTED_KMS_AND_MODULAR_CLOCK__NO_GLOBAL_KERR_HARTLE_HAWKING` (108–119). |
| [tgl_ringdown_template.py:27](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/tgl_ringdown_template.py:27>), `ringdown` | Array temporal em segundos, `t_start`, parâmetros físicos; devolve plus/cross. `elapsed=time−t_start`, fase `ω·elapsed+phase`, envelope `exp[−(1/τ_GR+Γ)elapsed]` no ensemble (58–72). Realização Browniana exige semente e não recebe a mesma supressão de envelope. |
| [c6_engine.py:35](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/c6_engine.py:35>), `observed_windows` | Referência existente para janelas GWOSC com hashes, GPS e máscaras. Está vinculada ao registro C6 e a 4096 Hz; não é leitor universal. |
| [um.py:7517](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py:7517>), `prove_cocycle_to_einstein`; internas `_pit`, `sigma` (7534–7547) | Avaliação finita de `ρ^{it}=V diag(exp(it log w)) V†` e conjugação modular. Exige densidade fiel positiva; a rotina cria exemplos n=4. Base para adaptação em cópia, não API independente nem motor de tempo físico. Correspondente formal: [ModularFlow.lean:32](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/ModularFlow.lean:32>), `logRho/modPow/sigma`, seção `noncomputable`. |
| [um.py:2493](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py:2493>), `prove_fiat_lux_flow`; interna `rho_at` (2520) | Evolução `unvec(expm(t·Lsuper)·vec(rho0))`, horizonte `3/β`; controle finito n=4. Escala 1/β sem conversão em segundos. Não importar o programa original para extrair a rotina. |

## 4. Adendos e ambiguidades a preservar

- [ADENDO_016_003:15](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ADENDO_016_003_decisoes_do_operador_e_parte_D.md:15>): “agora”/“relógio fractalizado” recebem leitura `[INPUT/ONTO]`, N₀ com κ=1 como convenção; κ/T=2π é o invariante. Não fornece z nem calibração de segundos. O adendo 003c cancela D1–D3 da construção física proposta, preservando D4–D6; não transforma “fractalizado” em fórmula numérica de tempo.
- [ORDEM_016:510](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_016_a_gravidade_quantica_primeiro.md:510>) separa a derivação do 2π da hipótese sobre τ*. A-4 registra álgebra paga e identificação física não paga. Os adendos posteriores consultados não forneceram `theta_t` nem uma conversão universal GPS→modular.
- `θ_M=arcsin(sqrt(β_TGL))`, [forma canônica:145](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um_absoluto_forma_canonica.md:145>), é ângulo de leitura da fronteira. Não acrescentar dependência temporal por nome; a fase `ωt+φ` do template é outra grandeza. Boost hiperbólico, órbita compacta e parâmetro modular permanecem distintos.
- Para o runtime: usar GPS/tempo relativo com metadados; tempo fonte somente com z; eixo modular somente com estado/gerador e normalização declarados; conservar a leitura escolhida de τ* e seu estatuto. Ausência de ponte deve permanecer visível, sem substituição por `1/β` ou por uma posição de reprodução.
