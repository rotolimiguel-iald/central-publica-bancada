[REAL — release e textos primários localizados/lidos; DERIVED — aplicabilidade limitada; 22/09/2026] **Corrigir “não localizado”: o release DCC P2600130-v1 existe e foi arquivado. O pacote pSEOBNR examinado não demonstra disponibilidade do posterior conjunto por evento (df220, dtau220, spin) necessário para reutilizar diretamente o mesmo ln B dependente do spin.** Nenhum ln B foi calculado. Ausência de comprovação neste pacote não é inexistência de um release utilizável em outro local.

Esta revisão complementa `bis/F2_RD_APPLICABILITY_REVIEW.md/json`; o RD já foi concluído separadamente. Não foi duplicado trabalho gaussianindependent/freeclock.

## Fonte e cobertura

A [página DCC arquivada:71](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/DCC_P2600130_v1/release.html:71>) identifica GWTC-4.0 TGR III. A linha 116 liga o tar pSEOBNR; as linhas 115–119 mostram outros pacotes do release, que **não foram auditados aqui**. URL primária: [DCC P2600130-v1](https://dcc.ligo.org/LIGO-P2600130/public). A licença CC-BY-4.0 é declarada na página:105.

Conferi o SHA-256 do tar de **14.923.249 bytes**, o inventário completo de **49 membros** contra o recibo e extraí somente textos em `bis/f2_review/dcc_text/`. Recusei nomes absolutos, `..` e links; verifiquei confinamento e tamanho. Os três notebooks foram analisados como JSON/texto; suas células fonte foram numeradas em arquivos `.cells.txt`. Nenhuma célula foi executada e seus outputs não foram usados como prova. O utilitário Python foi apenas lido como texto. Não foi feito `pickle.load`, import de código do tar, `np.load` ou leitura de valores `.dat.gz`.

O header HTTP arquivado traz `Last-Modified: Wed, 18 Mar 2026 15:17:05 GMT`. Isso não certifica a data de publicação nem prova retroativamente em que dia o produto ficou disponível. A correção de localização é atual e documental.

## O que dizem README e notebooks

1. [README:3–5](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_review/dcc_text/pSEOB/README.md:3>) caracteriza o material como dados auxiliares/notebooks de figuras e manda obter as amostras individuais no release Zenodo associado. Não fornece nessa linha um identificador Zenodo; esta revisão não o adivinha.
2. [Notebook principal, células 5–6, linhas 117–135](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_review/dcc_text/pSEOB/pSEOBNR_main_figure.cells.txt:117>) tenta ler `pSEOB_{event_map[event]}_Prod0.h5`, com `pesummary.io.read`, e depois `samples_dict["pSEOBNRv5PHM-reweighted"][param]` para `domega220` e `dtau220`. Esses HDF5 não constam dos 49 membros. O caminho de computador do autor não é um arquivo disponível localmente.
3. [Linhas 76–92](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_review/dcc_text/pSEOB/pSEOBNR_main_figure.cells.txt:76>) declaram limites [−0,8;2] para ambos os desvios, estendidos a [−0,8;4] em S191109d e S200208q. São limites descritos no notebook, não priors analíticos lidos dos HDF5 nem comprovação de independência dos priors/nuisance. O notebook não identifica campos de spin/massa do remanescente para a curva.
4. [Linhas 147–158](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_review/dcc_text/pSEOB/pSEOBNR_main_figure.cells.txt:147>) carregam produtos combinados `joint/` e `hierarchical/`. As [linhas 220–249](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_review/dcc_text/pSEOB/pSEOBNR_main_figure.cells.txt:220>) passam as duas colunas combinadas a uma KDE/contorno 2D. Portanto, **não é correto declarar apenas pelo nome dos arquivos que sejam marginais independentes**. O código sugere uso pareado de um produto combinado 2D; o pareamento dos valores não foi conferido. Mesmo se confirmado, falta a dimensão de spin e a correspondência por evento para a curva g(chi).
5. [Notebook hierárquico:18–31](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_review/dcc_text/pSEOB/hierarchical_2D_figure.cells.txt:18>) referencia `mu_domega_220`, `mu_dtau_220`, `sigma_domega_220`, `sigma_dtau_220`, `rho`; o principal referencia `pop_domega_220` e `pop_dtau_220`. São parâmetros/amostras populacionais segundo o uso documentado, não o spin do remanescente de cada evento. Os campos foram identificados no texto, não verificados dentro dos NPZ.
6. [Notebook mock:45–55](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_review/dcc_text/pSEOB/mock_catalog_figure.cells.txt:45>) também exige dados externos do Zenodo: Q0 e resultados de 1000 catálogos simulados. Não roda nem fornece a ponte entre os produtos resumidos e os draws conjuntos reais por evento.
7. [utils_o3b.py:169–203](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_review/dcc_text/pSEOB/aux_data/utils_o3b.py:169>) lê pickles como propriedades auxiliares de catálogos e mapeia nomes como `CHIF→final_spin`. A existência dessa string **não é evidência de posterior conjunto**: os pickles ficaram opacos. O [dict_det_masses.json:1](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_review/dcc_text/pSEOB/aux_data/dict_det_masses.json:1>) guarda números escalares de massa total para cores, conforme o notebook:61–67; não são draws de massa final/spin correlacionados com deformações.

## Matriz de aplicabilidade

| Produto | Evidência textual | Serve ao mesmo ln B por curva em spin? |
|---|---|---|
| HDF5 individuais pSEOB_*_Prod0.h5 | Referenciados; ausentes deste tar | Potencial rota futura, não verificada: faltam arquivos, esquema conjunto e priors completos. |
| joint/*/domega_220_comb.dat.gz e dtau_220_comb.dat.gz | Produtos combinados; notebook usa pares em 2D | Não sustentam a integração por evento com spin. Não separar ou fabricar pareamento. |
| hierarchical/*/pseob_hier*.npz | Hiperparâmetros/população no texto | Não substituem o posterior por evento da curva determinística. |
| aux_data/*.pkl | Propriedades auxiliares; conteúdo não lido | Não certificado; não desserializado. |
| aux_data/dict_det_masses.json | Massas totais escalares para cores | Não contém a distribuição conjunta necessária. |
| Mock catalogs | Dados externos referenciados | Simulações e resumos não são novos eventos nem ln B dos dados reais. |

O mesmo estimador em `posterior_220_readout.py:3–7,25–53` exige o posterior conjunto livre e correlação com g(chi), além do contrato de priors. Agregar eventos antes da avaliação da curva geralmente perde a informação de qual spin está associado a qual deformação; um resumo 2D não a recria. Não usar uma mediana de spin, a massa escalar de cores ou propriedades pickle não lidas para preencher a lacuna. A inexistência de HDF5 por si só não seria impedimento — outro formato seguro poderia conter os mesmos draws —, mas este README e os fluxos de leitura deixam a dependência externa explícita.

**Disposição F2:** localização PAGA; disponibilidade direta neste pacote do joint df/dtau/spin por evento NÃO DEMONSTRADA; ln B NÃO CALCULADO (`null`). É necessário localizar o Zenodo associado e inspecionar seus dados/priors em tarefa autorizada antes de mudar essa conclusão. Este parecer não afirma que essa rota esteja bloqueada para sempre, nem que o restante do release DCC seja inutilizável.

## Hashes e arquivos escritos

| Fonte | SHA-256 |
|---|---|
| pSEOBNR.tar.gz | `946f0ec0052d935f68ddfee03327b777ce2386595108dde1eaf1bc782997b114` |
| bis\f2_review\dcc_text\pSEOB\pSEOBNR_main_figure.ipynb | `a12ee294230f9e5a6770c08516497748230f787f560d5767a73e94d629d6451a` |
| bis\f2_review\dcc_text\pSEOB\README.md | `d963288039a780b0b5786f4bacdf920de6e35c999a484a5479aba4100cb79728` |
| bis\f2_review\dcc_text\pSEOB\aux_data\utils_o3b.py | `59248804f2c6f7d871c78f4e77b25f77ea616ee747a6c60806bc0b0343ee123f` |
| bis\f2_review\dcc_text\pSEOB\aux_data\dict_det_masses.json | `580a52c36cd055ec5b372e552f1ef200e6a8bdcbea0d72cb258b23df511e2d31` |
| bis\f2_review\dcc_text\pSEOB\hierarchical_2D_figure.ipynb | `5ce2432d9b23a95ca3202c2eca4805a7cff454049ebb16e09ab7ac3939e1c321` |
| bis\f2_review\dcc_text\pSEOB\mock_catalog_figure.ipynb | `4a5dffa0f1f21895b435612888888e9b390439495c87ceb1f1143c3a1bf7ccc1` |
| bis\f2_review\dcc_text\pSEOB\pSEOBNR_main_figure.cells.txt | `cd97f5334e8732e9cd0d92a06954cab60c07290e4e58b6b53fa404ebcfa7ae18` |
| bis\f2_review\dcc_text\pSEOB\hierarchical_2D_figure.cells.txt | `675024cf3afeb60985dd07a7aa63d1535ad38caef215d8136c81b57e7e39cbe2` |
| bis\f2_review\dcc_text\pSEOB\mock_catalog_figure.cells.txt | `5907d70589049ebcf581f56612ff0723491b681b97efc82a558f61c761485bca` |
| cache/public/DCC_P2600130_v1/release.html | `ab802d007ea49f6d921c807bc2c259186c0e0f1377352b3a0c9b9c7f8e3f10a6` |
| bis/F2_GWTC4_RELEASE_SEARCH.json | `ecef9bbaee6f66923ae43cfd4c2b187500bc6c8673de668703216453faff4c56` |
| bis/f2_review/dcc_text_inventory.json | `3b545086968842e513e6dac9aea4c9268a702a0573fbfb0ba34f477d94f2b4de` |
| Parecer JSON | `a406d33b88b717dd32f1271b50c3432ddabb375bf6f6c92a03561805b13ee6d7` |

Escritos apenas os seguintes arquivos deste complemento:

- `bis/f2_review/inspect_dcc_text.py`
- `bis/f2_review/dcc_text_inventory.json`
- `bis/f2_review/write_dcc_review.py`
- `bis/f2_review/GWTC4_DCC_APPLICABILITY_REVIEW.json`
- `bis/f2_review/GWTC4_DCC_APPLICABILITY_REVIEW.md`
- `bis\f2_review\dcc_text\pSEOB\pSEOBNR_main_figure.ipynb`
- `bis\f2_review\dcc_text\pSEOB\README.md`
- `bis\f2_review\dcc_text\pSEOB\aux_data\utils_o3b.py`
- `bis\f2_review\dcc_text\pSEOB\aux_data\dict_det_masses.json`
- `bis\f2_review\dcc_text\pSEOB\hierarchical_2D_figure.ipynb`
- `bis\f2_review\dcc_text\pSEOB\mock_catalog_figure.ipynb`
- `bis\f2_review\dcc_text\pSEOB\pSEOBNR_main_figure.cells.txt`
- `bis\f2_review\dcc_text\pSEOB\hierarchical_2D_figure.cells.txt`
- `bis\f2_review\dcc_text\pSEOB\mock_catalog_figure.cells.txt`

Raiz B: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN`. Dados de origem, notebooks no tar e produção permaneceram intactos. Todos os nomes de fields de NPZ citados são referências textuais, não resultados de abertura dos bins. Nenhuma conclusão física, publicação, comunicação externa ou alteração de gate.
