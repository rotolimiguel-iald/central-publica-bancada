[REAL — inspeção independente completa dos produtos RD; DERIVED — decisão de aplicabilidade; 22/09/2026] **NÃO É APLICÁVEL RODAR DIRETAMENTE O MESMO ln B DE DEFORMAÇÃO LIVRE DO 220 CONTRA GR NESTES RD.** Não foi encontrado posterior físico livre do 220. O valor de ln B permanece NÃO CALCULADO (`null`), não zero, −∞ ou exclusão. A alternativa de F2 “ou justificar por escrito” recebe esta justificativa documental; o controle numérico RD não foi realizado nem simulado como sucesso.

O resultado vale para o RD.tar.gz identificado abaixo. Não afirma inexistência de outro produto público ou impossibilidade de uma análise reformulada. A correção C2 v2 informada pelo operador não foi reaberta nesta tarefa. Nenhum trabalho gaussianindependent/freeclock foi duplicado.

## Cobertura integral, não inferência pelos seis primeiros arquivos

Foram lidos **372 configs**, **341 esquemas NetCDF** e o README: **714/714 hashes extraídos conferem**, sem arquivo ausente, extra ou falha de leitura. A hash do próprio tar também confere. Há **31 famílias de modelo/varredura**, cinco supereventos e 14 esquemas distintos. Cada família tem 12 configs (um mestre e 11 locais) e 11 posteriores, cada um com 4 cadeias × 1000 draws. Os seis NC do recibo amostral eram uma amostra de Kerr220+330; não fundamentaram sozinhos a conclusão.

Classificação: **297 posteriores Kerr**, **44 com desvios livres somente do 221**, **zero com 220 livre**. São 209 resultados sobre eventos observados e 132 controles de injeção; janelas e modelos do mesmo evento não são evidências independentes. Os diretórios `noise0`/`noise6` são controles, não eventos adicionais.

O inventário do tar foi percorrido integralmente, sem extração ou execução adicional. Além dos 714 arquivos auditados, há somente 10 arquivos regulares: cinco scripts de figuras, pyproject.toml, uv.lock e três PDFs de figuras. Não há outro posterior NetCDF/HDF5 nem pickle no inventário deste tar. Os corpos desses dez arquivos não foram lidos; seus nomes e tamanhos estão no inventário. Não foi seguido link HDF5 externo ou simbólico (nenhum encontrado).

## Evidência decisiva: qual modo é livre

No caso com maior suporte de desvios, [config do evento S240621dy, linhas 1–10](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/220+delta221_start0M_stop20M_step2M_T0.3s_ds4_broaddfdg/config.ini:1>), a ordem dos modos é `(1,-2,2,2,0)` e `(1,-2,2,2,1)`, isto é, **220 primeiro, 221 segundo**. Os limites são:

```text
df_min = [0., -0.8]    df_max = [0., 1.1]
dg_min = [0., -2]      dg_max = [0., 0.8]
```

No [NetCDF correspondente](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/220+delta221_start0M_stop20M_step2M_T0.3s_ds4_broaddfdg/engine/1403034677.448923/result.nc>), os localizadores são `posterior/mode`, `posterior/df` e `posterior/dg`. Os dois últimos têm forma `(4,1000,2)`; o eixo final segue os rótulos de `posterior/mode`. Em **todos os 44 arquivos com desvios**, os 176.000 valores de `df[...,0]` e os 176.000 valores de `dg[...,0]` são exatamente zero. Min=max=0, contagem não zero=0. A segunda coluna varia. O JSON do parecer contém caminhos exatos, hashes e min/max por família; o inventário contém o esquema de cada arquivo.

**Armadilha adicional verificada:** `posterior/df_unit` e `posterior/dg_unit` têm amostras variáveis inclusive no primeiro modo. São coordenadas auxiliares; não são os desvios físicos. Com limites inferior e superior iguais a zero, uma coordenada unitária variável não abre suporte em df220/dg220. Trocar os campos físicos pelos auxiliares fabricaria uma distribuição de deformação.

Nos 297 produtos Kerr não há `posterior/df`/`posterior/dg` físicos livres. Há `posterior/m`, `posterior/chi`, `posterior/f` e `posterior/g`: frequência e taxa variam com massa/spin, não com um parâmetro 220 independente. Não se pode converter essa variação em df220 pela comparação com Kerr em parâmetros arbitrariamente fixos. Os configs de cada NC e seus atributos `config` coincidem semanticamente; as diferenças textuais encontradas eram somente formatação de arrays numéricos. Todos declaram a versão `ringdown 1.0.1.dev312+gdee4418`.

## Fonte primária e priors: logaritmo não é desvio fracionário

A seção 7.1 do [artigo GWTC-5.0 local, linhas 3648–3662](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/../TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/gwtc5_tgr.txt:3648>) explica que as frequências e taxas Kerr são funções da massa final no referencial do detector e do spin; o 220 ancora esses parâmetros, enquanto o modo subdominante pode se desviar. A Eq. (16) usa `f=f_Kerr exp(df)` e `gamma=gamma_Kerr exp(dg)`. As [linhas 3726–3728](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/../TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/gwtc5_tgr.txt:3726>) declaram priors planos U(−0,8;0,8), estendidos quando necessário. As [linhas 3938–3944](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/../TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/gwtc5_tgr.txt:3938>) identificam explicitamente o teste de desvios do **221**. Texto primário efetivamente lido nessas passagens; não alego leitura integral do artigo. Numeração por quebras LF, não por form feeds de página.

Os priors de deformação efetivamente configurados são:

| Produtos | df220 / dg220 físicos | df221 logarítmico | dg221 logarítmico |
|---|---|---|---|
| Kerr, 297 NC | fixos em 0; coordenadas de desvio ausentes | fixo/ausente | fixo/ausente |
| S240621dy, evento, broaddfdg, 11 NC | ambos fixos em 0 | U(−0,8;1,1) | U(−2;0,8) |
| S240621dy, injeção zero, 11 NC | ambos fixos em 0 | U(−0,8;0,8) | U(−0,8;0,8) |
| S240621dy, noise0 e noise6, 22 NC | ambos fixos em 0 | U(−0,8;0,8) | U(−0,8;0,8) |

A forma plana vem da declaração do artigo; os limites acima vêm dos configs lidos. Para a injeção: [config:7–10](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/220+delta221_start0M_stop20M_step2M_T0.3s_ds4_INJ/config.ini:7>). Massa é declarada plana no artigo e seus limites por evento estão na tabela de modelos JSON. Os configs não explicitam os limites numéricos do prior de spin; não os inferi de defaults de biblioteca nem certifiquei um contrato completo de priors de nuisance. Esse desconhecimento é secundário à ausência comprovada de suporte livre no 220.

[DERIVED] Converter os parâmetros logarítmicos em desvios fracionários daria `delta_f=exp(df)−1` e `delta_tau=exp(−dg)−1`, não `delta_tau=dg` nem `−dg` exatamente. Um prior uniforme em df,dg induz densidade proporcional a `1/[(1+delta_f)(1+delta_tau)]` no suporte transformado; não vira automaticamente o prior uniforme fracionário usado no código C4. Isso diz respeito ao **221 disponível**, não cria um 220 livre.

## Por que a rotina existente não pode receber esses RD

A rotina [posterior_220_readout.py:3–7](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/posterior_220_readout.py:3>) define a razão de densidades `p(df220,dtau220−g(chi)|d)(0,0) / p(df220,dtau220|d)(0,0)`, sob priors de deformação uniformes independentes e compatibilidade dos priors restantes. A função [uniform_prior:25–44](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/posterior_220_readout.py:25>) exige esse contrato; [catalog_220_readout.py:57–75](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/catalog_220_readout.py:57>) lê `domega220`, `dtau220` e parâmetros conjuntos do remanescente. A transformação cisalhante tem Jacobiano um nesse espaço, mas isso pressupõe que tal posterior livre exista. Esses fontes foram lidos, não importados ou executados.

O RD fornece um posterior restrito ao 220 Kerr e, em 44 casos, uma extensão em **outras coordenadas modais**. Uma KDE sobre zeros físicos teria covariância singular; adicionar jitter ou aproveitar `*_unit` criaria suporte artificial. Avaliar a curva sobre o posterior Kerr de massa/spin tampouco recupera a verossimilhança fora da superfície Kerr. Não há argumento para atribuir ln B=0 ou −∞ aos ramos de efeito não nulo com esses produtos.

“Priors comuns” significa priors compatíveis entre as duas hipóteses comparadas no mesmo modelo amplo; não exige que todo método público tenha priors numericamente idênticos aos do pSEOB. Um outro posterior poderia permitir correção explícita de priors/Jacobianos. Aqui essa correção não resolve a direção 220 que não foi amostrada. Uma reparametrização não trivial que reancorasse massa/spin em outro modo exigiria nova demonstração de bijeção, suporte, priors induzidos e hipóteses de modos superiores; não foi construída nem autorizada como reutilização direta do MESMO estimador.

Para um produto futuro ser diretamente utilizável, seriam necessários draws conjuntos de desvios **físicos** livres do 220 e parâmetros do remanescente; significado, suporte e densidade dos priors; compatibilidade de nuisance/modos superiores entre curva e GR; convenções de pesos e início de janela. Nenhum caminho/field/prior desse tipo foi encontrado neste RD. **Lista de posteriores livre220 utilizáveis: vazia.**

## Tabela completa de modelos e regimes

Cada linha representa uma família com 11 NC e 12 configs, cobrindo a varredura de início registrada. O link aponta ao config mestre lido, linha 1. Todos mantêm o 220 Kerr. “Evento” é o identificador do pacote, sem inventar novas observações para cada janela.

| Evento | Regime | Modelo/config | NC | Desvios livres físicos |
|---|---|---|---:|---|
| S240615dg | evento | [220+210](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240615dg/production/220+210_start0M_stop20M_step2M_T0.2s_ds4/config.ini:1>) | 11 | nenhum |
| S240615dg | evento | [220+221](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240615dg/production/220+221_start0M_stop20M_step2M_T0.2s_ds4/config.ini:1>) | 11 | nenhum |
| S240615dg | evento | [220](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240615dg/production/220_start0M_stop20M_step2M_T0.2s_ds4/config.ini:1>) | 11 | nenhum |
| S240621dy | evento | [220+210](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/220+210_start0M_stop20M_step2M_T0.3s_ds4/config.ini:1>) | 11 | nenhum |
| S240621dy | evento | [220+221+440](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/220+221+440_start0M_stop20M_step2M_T0.3s_ds4/config.ini:1>) | 11 | nenhum |
| S240621dy | injeção zero | [220+221+440](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/220+221+440_start0M_stop20M_step2M_T0.3s_ds4_INJ/config.ini:1>) | 11 | nenhum |
| S240621dy | evento | [220+221](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/220+221_start0M_stop20M_step2M_T0.3s_ds4/config.ini:1>) | 11 | nenhum |
| S240621dy | injeção zero | [220+221](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/220+221_start0M_stop20M_step2M_T0.3s_ds4_INJ/config.ini:1>) | 11 | nenhum |
| S240621dy | injeção zero | [220+delta221](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/220+delta221_start0M_stop20M_step2M_T0.3s_ds4_INJ/config.ini:1>) | 11 | 221 |
| S240621dy | evento | [220+delta221](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/220+delta221_start0M_stop20M_step2M_T0.3s_ds4_broaddfdg/config.ini:1>) | 11 | 221 |
| S240621dy | evento | [220](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/220_start0M_stop20M_step2M_T0.3s_ds4/config.ini:1>) | 11 | nenhum |
| S240621dy | injeção zero | [220](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/220_start0M_stop20M_step2M_T0.3s_ds4_INJ/config.ini:1>) | 11 | nenhum |
| S240621dy | injeção noise0 | [220+221+440](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/noisy_data/noise0/220+221+440_start0M_stop20M_step2M_T0.3s_ds4/config.ini:1>) | 11 | nenhum |
| S240621dy | injeção noise0 | [220+221](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/noisy_data/noise0/220+221_start0M_stop20M_step2M_T0.3s_ds4/config.ini:1>) | 11 | nenhum |
| S240621dy | injeção noise0 | [220+delta221](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/noisy_data/noise0/220+delta221_start0M_stop20M_step2M_T0.3s_ds4/config.ini:1>) | 11 | 221 |
| S240621dy | injeção noise0 | [220](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/noisy_data/noise0/220_start0M_stop20M_step2M_T0.3s_ds4/config.ini:1>) | 11 | nenhum |
| S240621dy | injeção noise6 | [220+221+440](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/noisy_data/noise6/220+221+440_start0M_stop20M_step2M_T0.3s_ds4/config.ini:1>) | 11 | nenhum |
| S240621dy | injeção noise6 | [220+221](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/noisy_data/noise6/220+221_start0M_stop20M_step2M_T0.3s_ds4/config.ini:1>) | 11 | nenhum |
| S240621dy | injeção noise6 | [220+delta221](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/noisy_data/noise6/220+delta221_start0M_stop20M_step2M_T0.3s_ds4/config.ini:1>) | 11 | 221 |
| S240621dy | injeção noise6 | [220](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240621dy/production/noisy_data/noise6/220_start0M_stop20M_step2M_T0.3s_ds4/config.ini:1>) | 11 | nenhum |
| S240920dw | evento | [220+210](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240920dw/production/220+210_start0M_stop20M_step2M_T0.35s_ds4/config.ini:1>) | 11 | nenhum |
| S240920dw | evento | [220+221](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240920dw/production/220+221_start0M_stop20M_step2M_T0.35s_ds4/config.ini:1>) | 11 | nenhum |
| S240920dw | evento | [220](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S240920dw/production/220_start0M_stop20M_step2M_T0.35s_ds4/config.ini:1>) | 11 | nenhum |
| S241127aj | evento | [220+210](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S241127aj/production/220+210_start0M_stop20M_step2M_T0.5s_ds4/config.ini:1>) | 11 | nenhum |
| S241127aj | evento | [220+221](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S241127aj/production/220+221_start0M_stop20M_step2M_T0.5s_ds4/config.ini:1>) | 11 | nenhum |
| S241127aj | evento | [220+330](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S241127aj/production/220+330_start0M_stop20M_step2M_T0.5s_ds4/config.ini:1>) | 11 | nenhum |
| S241127aj | evento | [220](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S241127aj/production/220_start0M_stop20M_step2M_T0.5s_ds4/config.ini:1>) | 11 | nenhum |
| S241225v | evento | [220+210](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S241225v/production/220+210_start0M_stop20M_step2M_T0.25s_ds4/config.ini:1>) | 11 | nenhum |
| S241225v | evento | [220+221](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S241225v/production/220+221_start0M_stop20M_step2M_T0.25s_ds4/config.ini:1>) | 11 | nenhum |
| S241225v | evento | [220+330](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S241225v/production/220+330_start0M_stop20M_step2M_T0.25s_ds4/config.ini:1>) | 11 | nenhum |
| S241225v | evento | [220](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/controls_extracted/ringdown/S241225v/production/220_start0M_stop20M_step2M_T0.25s_ds4/config.ini:1>) | 11 | nenhum |

## Custódia e alcance da decisão F2

A [ORDEM_013BIS:85](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/../TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md:85>) pede o mesmo ln B no RD **ou justificativa por escrito**, sem multiplicá-lo ao pSEOB. A ausência de posterior livre220 é uma justificativa concreta de não execução direta. O pedido de inspeção/aplicabilidade está cumprido; o resultado científico de robustez não foi produzido. Não substitui a conclusão dos outros itens F2, o marco formal de entrega ou a decisão da gerência.

| Fonte/recibo | SHA-256 calculado |
|---|---|
| RD.tar.gz, 415283962 bytes | `9810e0e45cd35824d29044d13474520b0a576dc6a3c3bb71160e0b328e72e47a` |
| bis/F2_CONTROL_EXTRACTION.json | `88384c3eb4240dc159f0aa3b16d9353b5b63bdb990415e8d1073f9507d366e97` |
| bis/F2_CONTROL_SCHEMAS.json | `e54e648e06625cc6f96094c7c16d4b89cd40001498d1f4fd5cd9c7f30f417dbf` |
| ../TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/gwtc5_tgr.txt | `d523ae94f23f40b55e7688702b444cf35fb2c2dc90610a6d03bfbd2ef8eefccf` |
| ../TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md | `a907d07bc484b53cc6db237dc5972f4dcc47be03ad084c832201bb648981454b` |
| catalog_220_readout.py | `c2b43d633b39195a086a7961cdcc9842ec90fb4d5b25cf5114641b33191707de` |
| posterior_220_readout.py | `f5cccda67b341785cc5101cd7c3447cd6d945ef7e0f0703aa4da1b031ff72279` |
| bis/f2_review/inspect_rd.py | `4988c8d50d688cc4d469edb018881a9233400dbcd09d09ece94a5c253accd933` |
| bis/f2_review/rd_inventory.json | `7745a49b005df4f4c0556f1c05e71c5f468efab4507e672c495ddff865f2cd1e` |
| NC exemplar com desvios 221 | `ce3a60c915c13fd9e83a0675e9fc8988ee20de16c72eb77628d47da9ec96a198` |
| Parecer JSON completo | `2076f9fc296b30063dbe1272f834c0135e33dcd015fc948d50362a0a84daa5b3` |

Os hashes de todos os 714 produtos estão no JSON e no inventário; o JSON inclui todos os caminhos de resultados, campos e limites por modelo. Os insumos com barras Windows foram normalizados para leitura no WSL, com verificação de confinamento na raiz autorizada. Leitura de HDF5 em modo `r`, sem interpretação de pickle. Nenhum código do tar foi executado e nenhum script de produção alterado. A varredura de metadados e hashes levou aproximadamente 217,53 s; não foi inferência ou grande rerun.

Não lidos: valores dos datasets de strain, posteriores primários pSEOB para refazer análises, corpos dos scripts/lock/figuras omitidos da extração, defaults internos do pacote ringdown ou artigo completo. Os valores numéricos lidos dos NC foram somente coordenadas de modos e campos de desvios/auxiliares relevantes; os demais datasets foram inspecionados por nome, forma e dtype. O HDF5 de injeção do outro tar (17018009) não foi usado para alegar disponibilidade em RD. Sem consulta web: a fonte primária local bastou para identificar as convenções.

Reprodução da inspeção (recusa sobrescrever o inventário já existente):

```powershell
wsl -e /opt/lal_env/bin/python -B "/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_review/inspect_rd.py"
```

Arquivos escritos nesta revisão, somente estes:

1. `bis/f2_review/inspect_rd.py`
2. `bis/f2_review/rd_inventory.json`
3. `bis/f2_review/write_review.py`
4. `bis/F2_RD_APPLICABILITY_REVIEW.json`
5. `bis/F2_RD_APPLICABILITY_REVIEW.md`

Raiz B: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN`. Temporários exclusivos foram substituídos por seus destinos; nenhuma escrita em dados, código de produção, C2, memória ou canônico. Axiomas N/A; nenhum gate ou veredito físico alterado.
