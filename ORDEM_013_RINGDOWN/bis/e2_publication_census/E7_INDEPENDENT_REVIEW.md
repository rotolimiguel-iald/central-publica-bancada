# E7 — parecer independente sobre produtor, extrator e HANDOFF FINAL v2

**Resultado: REQUEST_CHANGES_BEFORE_INTEGRATION_OR_EXTRACTION.** A aritmética condicional revisada está coerente com a fonte pinada; há duas falhas de validação/custódia a corrigir e um pin operacional desatualizado. Isso não é reprovação da hipótese física, nem execução ou liberação de E2/E7.

[REAL — observação de código, hashes e execução de mocks] · [DERIVED — identidades algébricas condicionais] · [INPUT/CONJECTURE — hipóteses das leituras] · [DECLARADO — proveniência anterior dos produtos] · [OPEN — likelihood, priors normalizados, seleção, calibração física, cegamento e integração real]

Data da conferência dos pins: **2026-09-22T20:40:33.182646+00:00**. Revisão solicitada pelo operador depois do censo de publicações. A autoria desta revisão é distinta da produção E7/Wegener. Os **31 testes do autor não foram tratados como revisão independente nem repetidos**: executei controles novos, descritos e reproduzíveis abaixo.

## Achados que exigem correção

### F1 — [P2] Conferir o contrato completo do payload contra o plano antes dos diagnósticos

**[REAL — reproduzido com mocks]** Em [tgl_ringdown_ampliacao.py:428](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/tgl_ringdown_ampliacao.py:428>) e [tgl_ringdown_ampliacao.py:431](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/tgl_ringdown_ampliacao.py:431>), a comparação com o plano cobre identidade, papel, caminhos, hashes e dataset. Não compara `N_source`, mapeamento de campos, modelo, referencial/unidade da massa ou proveniência dos priors. [tgl_ringdown_ampliacao.py:172](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/tgl_ringdown_ampliacao.py:172>) valida o comprimento apenas contra o próprio `N` recebido; [tgl_ringdown_ampliacao.py:184](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/tgl_ringdown_ampliacao.py:184>) confronta `N_source` apenas com esse mesmo número. Assim, um payload autoconsistente, mas diferente do plano registrado, é aceito.

| Sonda independente, plano sintético com 8 draws | Expectativa do contrato | Observado |
|---|---|---|
| Cortar as cinco colunas para 2 draws e declarar N=N_source=2, mantendo o plano em 8 | Recusar perda de amostras | Aceito; saída informa N=2 e FULLSAMPLE |
| Trocar mass_frame para source e mass_unit para kilogram | Recusar referencial/unidade divergentes | Aceito |
| Trocar source_field_mapping de df220 e model | Recusar mapeamento/modelo divergentes | Aceito |
| Priors com status arbitrário e declarations=null, inclusive df220/dtau220 | Recusar proveniência malformada | Aceito |
| Retirar authorization_sha256 e usar schema alheio | Recusar payload sem o contrato de produção | Aceito |

A primeira sonda basta para demonstrar o defeito: a saída mantém `NONBLIND_FULLSAMPLE_CONDITIONAL_DESCRIPTIVE_ONLY` apesar de não conter o número integral registrado. As demais mostram a mesma lacuna contratual e a falta de encadeamento do recibo de autorização no consumo.

**Limite da reprodução:** guarda E2 e I/O foram substituídos por mocks; nenhum hash criptográfico foi “quebrado”. Os testes isolam a validação do consumidor **depois** da autenticação de transporte. Um SHA correto fixa os bytes entregues, mas não prova que seu conteúdo satisfaz o plano. Não foi demonstrado que o extrator atual produza esses payloads defeituosos; o problema é o consumidor aceitá-los quando chegam de uma etapa externa.

**Correção mínima sugerida:** validar schema e campos de proveniência exigidos; exigir `N == N_source == planned.N_source`; comparar `source_field_mapping == planned.fields`, modelo, frame e unidade; validar a estrutura dos priors, os caminhos contra `planned.prior_paths` e declarações textuais não vazias para os dois deltas. Manter os priors derivados como OPEN. Encadear o recibo de autorização ao artefato consumido, sem inventar assinatura/autorização a partir de um hash declarado. Fazer as recusas antes de `fullsample_diagnostics` e `reading_diagnostics`.

### F2 — [P2] Aplicar a barreira de armazenamento externo também aos priors

**[REAL — inspeção AST e sondas de predicado, sem executar o extrator]** [extrai_posteriores_pseob.py:24](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/extrai_posteriores_pseob.py:24>) verifica HardLink nos caminhos dos priors, mas [extrai_posteriores_pseob.py:29](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/extrai_posteriores_pseob.py:29>) verifica somente tipo Dataset, quantidade de elementos e `dtype.kind`. Em seguida, [extrai_posteriores_pseob.py:31](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/extrai_posteriores_pseob.py:31>) lê `node[()]`. A barreira `ds.is_virtual or ds.external`, existente para as amostras em [extrai_posteriores_pseob.py:61](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/extrai_posteriores_pseob.py:61>), não existe para esses nós de metadados.

Um link duro no arquivo pinado não estabelece que o armazenamento de um dataset virtual/externo esteja no mesmo arquivo. O predicado real da linha 29, avaliado isoladamente em AST com objetos simulados, **não recusou**:

- Dataset textual S com `is_virtual=True`;
- Dataset textual S com `external` não vazio;
- Dataset de kind O sem demonstração de que se trata de string HDF5.

O terceiro caso é complementar: kind O, sozinho, não é validação de texto; converter qualquer valor com `str(v)` não estabelece que haja uma declaração de prior válida. O limite de caracteres também é aplicado somente depois da leitura.

**Impacto:** a garantia de “priors dentro do HDF5 pinado” não cobre todos os caminhos de leitura implementados. O hash do arquivo recipiente não fixa bytes armazenados externamente. **Não afirmo que qualquer um dos 33 arquivos reais tenha essa estrutura**; eles não foram abertos nesta revisão.

**Correção mínima sugerida:** recusar `node.is_virtual` e `node.external` antes de qualquer leitura, como no posterior; verificar o tipo string real, incluindo vlen de texto, e recusar referências/objetos não textuais; preservar os limites de tamanho e conferir os caminhos declarados. Acrescentar um teste negativo específico por variante. Não é necessário normalizar ou avaliar código de prior para corrigir a custódia.

## Bloqueio operacional já previsto pelo handoff

**[REAL] O pin da guarda não coincide com a guarda atual.**

- Pin em E2_INCLUDE_FINAL_v2: `276a2e31acbcc2f82b87238ac8ed58ae413ee9da25ae7738656f99cdf7c0adbb`.
- SHA medido de [registration_guard.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/registration_guard.py>): `32b2d6cc43325ac2caa16cc9040df6ebcaa550758f291e34c993a9cc57c69733`.

O handoff avisa expressamente que esse pin é provisório. Portanto, isto é uma **pendência de integração conhecida**, não evidência de um bypass: `checked_context` verifica o pin antes de importar a guarda e deve recusar a combinação atual. Consolidar a versão final, rever a guarda e regenerar os vínculos na preparação **antes** do registro. Não alterar um registro já publicado para fazê-lo passar.

A integração real de `checked_registration()`, testemunha, orçamento, runtime e autorização pós-E2 **não foi executada**. O contrato foi lido; as sondas do consumidor não substituem essa integração. A guarda observada nesta revisão já contém funcionalidades posteriores ao pin provisório.

## O que passou — fórmulas, unidades e domínio

**[REAL — testes numéricos; DERIVED — álgebra dentro das hipóteses da fonte]** A fonte [tgl_ringdown_prediction.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/tgl_ringdown_prediction.py>) coincide com o pin de E7 e com `prediction_module_sha256` do DATASET E0. O consumidor não importa essa fonte em produção: copia sua implementação vetorizada e confere a âncora de código. Nos testes independentes, carreguei somente o consumidor e a fonte, depois de conferir seus hashes, com bytecode desativado.

Defina T = GM_det/c³, u = Re(ωT), v = −Im(ωT) > 0, r = √(1−a²), e β = ALPHA_FINE_CODATA_2018 × √e calculado em runtime. Então ω = u/T e τ_GR = T/v. A soma de taxas de decaimento da **amplitude** dá:

`τ_eff = 1/(1/τ_GR + Γ)`, `x = Γ τ_GR`, `δτ = −x/(1+x)`.

Não encontrei troca entre amortecimento da amplitude e da energia nem um fator 2 espúrio. Com Γ ≥ 0, a correção é não positiva; R-GLOBAL produz zero. Trata-se de previsão ensemble condicional, não da leitura universal de uma realização observacional.

| Leitura | Identidade de x conferida / escopo | Estatuto físico conservado |
|---|---|---|
| R-A | β (1+z)tP u²/(2Tv) | INPUT: relógio de Planck e ponte fonte→detector |
| R-B | βu²/(2v) | INPUT: relógio de massa |
| R-RAIZ-0 | βu/(2v) | INPUT: coerência vácuo→um quantum |
| R-RAIZ-EP4 | Γ com offset ω₀=1/[4tP(1+z)]; denominador racionalizado | INPUT: energia de base |
| R-RAIZ-REST | ω₀=T/[tP²(1+z)²]; mesma forma racionalizada | CONJECTURE: energia de repouso do remanescente |
| R-LIN | βu/v | CONJECTURE: ponte física linear |
| R-MOD | 2πβ(1+r)[u−a/(1+r)]²/(rv), somente gap positivo e QNM explícito | CONJECTURE: identificação modular restrita |
| R-GLOBAL | 0 sob a partição declarada | INPUT: observável relacional |
| R-RAIZ-COHERENT | OPEN; ocupação/janela não fornecidas | CONJECTURE |
| R-PROP | OPEN; expoente de propagação não promovido a taxa local | CONJECTURE |

A forma para R-MOD usa m=2 e não foi estendida ao 440. As duas formas de offset conservam os fatores de redshift da fonte. O teste dimensional verificou: x_A ∝ (1+z)/M_det; x_B, x_RAIZ0, x_LIN e x_MOD independentes de massa/redshift a spin e QNM dimensionless fixos; o limite de grande offset REST ∝ (1+z)²/M_det²; EP4 coincide assintoticamente com R-A no domínio sintético astrofísico testado.

A regressão nova usou **8 triplas diferentes** das 4 do autor, em 7 leituras, com tolerância relativa 2×10⁻¹⁴ e absoluta zero. Maior erro relativo observado: **3,4678746308606614×10⁻¹⁶**. Além da regressão contra a fonte, derivei um oráculo dimensionless separado para seis leituras, incluindo R-MOD com spins negativos e QNM sintético admissível. Isso reduz, mas não elimina, a possibilidade de erro compartilhado entre fonte e cópia.

BCW não é extrapolado para spin negativo. QNM instável ou gap corrotante não positivo é recusado. R-MOD sem QNM por draw permanece OPEN no pipeline de cinco campos. PROP, COHERENT e 440 também permanecem OPEN. Um QNM fornecido à função continua INPUT com proveniência requerida; o teste não certifica sua obtenção física.

## Pareamento, priors e nuisance

**[REAL] Pareamento numérico:** a leitura estática mostra seleção das cinco colunas em uma única operação `ds.fields(columns)[()]`, sem ordenação individual ou thinning, em [extrai_posteriores_pseob.py:70](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/extrai_posteriores_pseob.py:70>). Não foi executada essa leitura. No consumidor, os mocks verificaram a identidade

`Var(dtau−delta) = Var(dtau)+Var(delta)−2Cov(dtau,delta)`.

Uma permutação conjunta das linhas conserva o resultado; embaralhar somente dtau altera a covariância, como deve ocorrer. **Comprimentos iguais não certificam a identidade dos pares**: a garantia depende da extração conjunta e da custódia do payload, razão adicional para F1.

**[REAL/OPEN] Priors:** a implementação não divide posteriores por priors desconhecidos, não inventa fatorização e não calcula normalização da likelihood restrita. Priors de Mfdet/af/z continuam derivados/OPEN; os de deformação são texto DECLARADO, não densidades pagas. Isso é apropriado para diagnóstico descritivo e insuficiente para BF/inferência física. F1/F2 dizem respeito à validade e custódia desse texto, não exigem implementar a likelihood nesta revisão.

**[REAL] Nuisance:** a projeção por SVD coincidiu com a solução fechada do intercepto ponderado, com informação sintética **0,39171686364533526**. Intercepto absorve uma correção constante; desenho singular é recusado. Um efeito reescalado por 10⁻⁴⁰ preservou informação **4,003726573754519×10⁻⁷⁹**, sem zeragem por limiar absoluto. A geometria usa média das previsões dos draws e largura posterior de dtau. Ela não marginaliza conjuntamente a incerteza do modelo/nuisance e é corretamente apresentada como planejamento gaussiano condicional.

Mesmo com um gate falsamente declarado pago, as 20 células mantiveram lnB/z físicos nulos: sem testes, AWAITING_DATA; com contagem sintética positiva, INCONCLUSIVE_SYSTEMATICS. **Não apareceu CONFIRMED**, nem promoção de NOT_FALSIFIED.

Há uma observação de robustez: [tgl_ringdown_ampliacao.py:390](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/tgl_ringdown_ampliacao.py:390>) testa a presença de valores de nuisance, não seus domínios numéricos. Valores negativos, string ou objeto não nulo produziram `UNVERIFIED`, em vez de red/erro. Isso **não abriu o gate nem criou significância** na versão revisada; antes de implementar qualquer ramo green, validar tipos, finitude e domínios cientificamente definidos. Não classifiquei essa lacuna como bypass físico atual.

## Forecast, estatutos e dependências

**[REAL] Forecast sob controle de fonte:** as **50 linhas**, cinco populações para cada uma das dez leituras, em `conditional_E0_targets` são cópias exatas de `planning_targets` do PORTAO_DA_AMPLIACAO_V1 pinado. Todas conservam `operational_target_paid=false` e `systematic_gate_green=false`; os dez `N_target_information` continuam null. Conferi também a correspondência dos estatutos INPUT/CONJECTURE com C1 v4.

Os forecasts herdados são históricos/condicionais; o DATASET E0 explicita avaliação nos remanescentes medianos, distinta da nova média de previsão por draw. A cópia E7 não transforma forecasts em nova medição nem atualiza suas hipóteses. Não fiz novo forecast, seleção de leitura, cálculo de posterior ou inferência sobre natureza.

**[REAL] NumPy-only tem alcance delimitado:** os imports científicos do consumidor são apenas NumPy, sem scipy/h5py, e ele não importa o extrator. O extrator depende de h5py por projeto. A **CLI registrada completa**, porém, chama uma guarda que exige o ambiente /opt/lal_env e verifica a disponibilidade/origem pinada de scipy, bilby, dynesty, lal, lalsimulation, gwpy e h5py. Portanto, “consumidor científico NumPy-only” está correto; “CLI executável numa instalação apenas com NumPy” não foi demonstrado e não é o contrato efetivo da guarda atual.

**[REAL/DECLARADO] Escopo de dados:** o plano contém 33 identidades únicas, todas calibration. Nenhuma das nove novas exclusões do censo de publicação entra por esse plano. Isso não dispensa transportar o censo para a seleção E2 externa a E7. Os pins de HDF5/tar permanecem DECLARADOS a partir da custódia anterior; não foram medidos novamente nesta revisão.

## Conferências executadas e limites

| Grupo independente | Resultado |
|---|---|
| T01 — Fonte pinada, grade vetorizada nova, sete leituras | PASS |
| T02 — Oráculo dimensionless separado, seis leituras, spin assinado | PASS |
| T03 — Escalas de massa/redshift e limites dos offsets | PASS |
| T04 — Soma de taxas, sinal e convenção de amplitude | PASS |
| T05 — Projeção vs solução fechada ponderada | PASS |
| T06 — Efeito minúsculo, constante absorvida, desenho singular | PASS |
| T07 — Covariância pareada, variância residual, permutações | PASS |
| T08 — NaN/domínio/comprimento/duplicatas | PASS |
| T09 — Canais OPEN, spin/QNM/gap, 440 ausente | PASS |
| T10 — Claims de nuisance não promovem veredito físico | PASS, com observação UNVERIFIED acima |
| T11 — Hash errado/ausente, chave JSON duplicada, escape de caminho | PASS |
| T12 — Imports científicos do consumidor | PASS |
| T13 — Contrato básico com payload sintético válido | PASS |
| T14 — Plano blind recusado antes de ler payload simulado | PASS |
| Cinco sondas negativas F1 | **REJECT esperado; ACCEPT observado nas cinco** |
| Predicado AST de prior virtual/externo/O | **Não recusou os três objetos simulados** |

Runtime numérico: **Python 3.12.3, NumPy 2.5.3**, já existentes em WSL /opt/lal_env. Não foi feita instalação. O Python Windows não tinha NumPy; a primeira chamada WSL no sandbox retornou E_ACCESSDENIED. A execução seguinte foi autorizada pelo mecanismo de permissões e funcionou. Isso não foi rejeição de aprovação automática.

Nenhum extrator foi importado/chamado; nenhum extract_one/extract/main foi executado, nem com fixture. Não criei HDF5 sintético. As sondas do extrator apenas analisam AST e avaliam seu predicado de guarda em objetos simulados. Não abri posterior de teste ou de calibração, strain, tar ou novo extrato. Não executei PE, campanha, importação/execução de um.py ou alteração canônica.

Mocks de I/O e guarda limitam a conclusão das sondas à lógica do consumidor. Não executei testes de integração real da cadeia de autorização, nem certifico os produtos reais. O resultado de 14 controles positivos **não apaga** as cinco recusas ausentes e não equivale a “suíte inteira aprovada”.

## Pins medidos

Os **19/19 arquivos** listados no MANIFEST_FINAL_v2 coincidem em hash e tamanho. Os **17/17 pins de entrada** do fragmento v2 também coincidem. O pin provisório da guarda é a divergência separada já descrita. Hashes abaixo foram calculados dos bytes em disco, não recuperados de memória.

| Arquivo relativo a Chatgpt | Bytes | SHA256 medido |
|---|---:|---|
| ORDEM_013_RINGDOWN/bis/e7_prepare/producer/tgl_ringdown_ampliacao.py | 24853 | `a636cf53891c771d4c427dd6e12eaca25e398ddc73d6428ffb74717d028dbaa6` |
| ORDEM_013_RINGDOWN/bis/e7_prepare/producer/extrai_posteriores_pseob.py | 7525 | `a188874000c5b357925b9b664f5e8609b0fda9886386ce8c09663608dcaec0ad` |
| ORDEM_013_RINGDOWN/tgl_ringdown_prediction.py | 8382 | `fd0fc446e1c732f3d782210c6effa7cb7faeaeb7a51a434d4f397f1da89bd652` |
| ORDEM_013_RINGDOWN/bis/e7_prepare/HANDOFF_FINAL_v2.md | 4661 | `33c8bde0e3057462ff3b26966bee8c4bb899f55d3c5268840fc59a5e1c1c43ef` |
| ORDEM_013_RINGDOWN/bis/e7_prepare/REVIEW_AND_HANDOFF.md | 7698 | `d6122d6f1c978f6bca5fa60709bfed1d52ce95b550dc1df6f466343cac982a02` |
| ORDEM_013_RINGDOWN/bis/e7_prepare/MANIFEST_FINAL_v2.json | 3496 | `7aaced9f85b9f8b33b04ccbfbaf1cb85f1de949f6356aa5a2e6e780d068ae20c` |
| ORDEM_013_RINGDOWN/bis/e7_prepare/E2_INCLUDE_FINAL_v2.json | 47987 | `eed58e6d6b635208b47557fe8e1e22aa6a81867bd8b2171104ff362cdb376f8a` |
| ORDEM_013_RINGDOWN/bis/e7_prepare/EXTRACTION_PLAN.json | 47760 | `7dc138a1690d45d381fc36d6e5cb54967b028741158f625ac814fb92159a7335` |
| ORDEM_013_RINGDOWN/bis/e2_code/registration_guard.py | 11555 | `32b2d6cc43325ac2caa16cc9040df6ebcaa550758f291e34c993a9cc57c69733` |
| ORDEM_013_RINGDOWN/C1_LEITURAS_v4.json | 35419 | `126270a896d8589870954b209155f26a8b08295839b31e0e9a6e28e512621980` |
| ORDEM_013_RINGDOWN/PORTAO_DA_AMPLIACAO_V1.json | 903525 | `710028a7d2af7b649511afe369d88462d2add95c5fecbb1fb03c517fc91fe8a0` |
| ORDEM_013_RINGDOWN/NUISANCE_V1.json | 1437250 | `83f860bbfa904c0048005c8b0f1b367814032052f352e780af7d77ed1f257b85` |
| ORDEM_013_RINGDOWN/bis/e0_core/DATASET.json | 462205 | `89d39541bd9a43f00720bda7b76886a0ee97658749c360682cb6e671c38ec7c0` |

## Disposição para o principal

**Não integrar/liberar extração com este parecer como PASS irrestrito.** Corrigir F1/F2, acrescentar as respectivas recusas negativas e consolidar o pin final da guarda. Então conferir novamente os hashes e a cadeia E2/autorização. As hipóteses e fórmulas condicionais revisadas podem ser mantidas; não é necessário reabrir posteriores para corrigir essas falhas.

A likelihood física normalizada, priors conjuntos, seleção, covariância/sistemática física e liberação cega seguem OPEN por projeto. Esse trabalho pendente não foi disfarçado como implementação paga nem tratado como defeito novo onde já está explicitamente fora do escopo.

Única escrita desta revisão: **bis/e2_publication_census/E7_INDEPENDENT_REVIEW.md**. Nenhuma mudança em produtor, extrator, handoff, manifestos ou memórias. **NOT_FALSIFIED nunca significa CONFIRMED.**

## Apêndice — código dos controles independentes em memória

O bloco abaixo é o script efetivamente executado por stdin com `/opt/lal_env/bin/python -B -`. Ele não é a suíte do autor. Lê somente código/metadados locais e usa mocks para as sondas de consumo. Não salvar/executar automaticamente: fica aqui para reprodutibilidade da revisão.

```python
from pathlib import Path
import ast, copy, hashlib, json, math, sys, types
import numpy as np
sys.dont_write_bytecode = True
B=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN')
P=B/'bis/e7_prepare'
include=json.loads((P/'E2_INCLUDE_FINAL_v2.json').read_bytes())
manifest=json.loads((P/'MANIFEST_FINAL_v2.json').read_bytes())
def load_code(name,path,wanted):
    raw=path.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==wanted
    mod=types.ModuleType(name);mod.__file__=str(path)
    exec(compile(raw,str(path),'exec'),mod.__dict__)
    return mod
m=load_code('e7_independent_consumer',P/'producer/tgl_ringdown_ampliacao.py',manifest['producer_tree_sha256']['tgl_ringdown_ampliacao.py'])
oracle=load_code('e7_independent_source',B/'tgl_ringdown_prediction.py',include['e7']['prediction_source_sha256'])
records=[]
def check(name,fn):
    try:
        detail=fn();records.append(dict(name=name,status='PASS',detail=detail))
    except Exception as exc:
        records.append(dict(name=name,status='FAIL',error=repr(exc)))
def must_raise(fn):
    try:fn()
    except (ValueError,FileNotFoundError):return True
    raise AssertionError('Expected rejection absent')
M=np.array([13.,27.,41.,65.,90.,130.,250.,700.])
A=np.array([0.,.11,.27,.43,.61,.79,.9,.97])
Z=np.array([0.,.03,.17,.4,.8,1.7,2.4,4.])
readings=('R-A','R-B','R-RAIZ-0','R-RAIZ-EP4','R-RAIZ-REST','R-LIN','R-GLOBAL')
def scalar_grid():
    errors={}
    for r in readings:
        actual=m.prediction_draws(M,A,Z,r)['delta_tau']
        expected=np.array([oracle.prediction(float(mm),float(aa),r,redshift=float(zz))['delta_tau'] for mm,aa,zz in zip(M,A,Z)])
        np.testing.assert_allclose(actual,expected,rtol=2e-14,atol=0)
        errors[r]=float(np.max(np.abs((actual-expected)/expected))) if np.any(expected) else 0.
    return {'draws_per_reading':len(M),'max_relative_errors':errors}
check('T01 scalar source pin and vector regression on new grid',scalar_grid)
def independent_qnm():
    masses=np.array([17.,45.,120.,300.]);spins=np.array([-.7,-.1,.2,.75]);zs=np.array([0.,.4,1.,3.])
    q=np.array([.6-.08j,.65-.07j,.7-.06j,.9-.04j])
    b=7.2973525693e-3*math.exp(.5);c=299792458.;G=6.67430e-11;HB=6.62607015e-34/(2*math.pi)
    tm=masses*1.3271244e20/c**3;tp=math.sqrt(HB*G/c**5)
    u=q.real;v=-q.imag;z1=1+zs
    base={'R-A':b*tp*z1*u*u/(2*tm*v),'R-B':b*u*u/(2*v),'R-RAIZ-0':b*u/(2*v),'R-LIN':b*u/v,'R-GLOBAL':np.zeros(4)}
    root=np.sqrt(1-spins*spins)
    base['R-MOD']=b*2*math.pi*(1+root)*(u-spins/(1+root))**2/(root*v)
    for r,x in base.items():
        got=m.prediction_draws(masses,spins,zs,r,q)['delta_tau']
        want=-x/(1+x)
        np.testing.assert_allclose(got,want,rtol=2e-14,atol=0)
    return {'dimensionless_x_derivations':list(base),'signed_spins_checked':True}
check('T02 independent dimensionless formula oracle including signed R-MOD',independent_qnm)
def dimensions():
    q=np.full(4,.65-.07j);a=np.full(4,.4);mass=np.array([30.,60.,30.,60.]);z=np.array([0.,0.,1.,1.])
    def x(r):
        d=m.prediction_draws(mass,a,z,r,q)['delta_tau'];return -d/(1+d)
    xa=x('R-A');np.testing.assert_allclose(xa/xa[0],[1,.5,2,1],rtol=2e-14,atol=0)
    for r in ['R-B','R-RAIZ-0','R-LIN','R-MOD']:np.testing.assert_allclose(x(r)/x(r)[0],np.ones(4),rtol=2e-14,atol=0)
    rest=x('R-RAIZ-REST');np.testing.assert_allclose(rest/rest[0],[1,.25,4,1],rtol=2e-14,atol=0)
    np.testing.assert_allclose(x('R-RAIZ-EP4'),xa,rtol=2e-14,atol=0)
    return 'Mass/redshift scalings and EP/4 large-offset asymptote hold for synthetic astrophysical domain.'
check('T03 dimensional scaling and redshift controls',dimensions)
def lifetime():
    q=np.full(8,.8-.06j);b=m.beta_runtime();tm=M*1.3271244e20/299792458.**3
    tau=tm/.06;gam=b*.8/tm
    got=m.prediction_draws(M,A,Z,'R-LIN',q)['delta_tau']
    np.testing.assert_allclose(got,1/(1/tau+gam)/tau-1,rtol=2e-14,atol=0)
    assert np.all((got>-1)&(got<0))
    return 'Independent sum of decay rates, amplitude convention, no extra energy factor.'
check('T04 harmonic lifetime identity and sign',lifetime)
def closed_projection():
    d=np.array([-.25,.13,-.11,.41]);sig=np.array([.7,1.1,.4,.9]);weights=1/sig**2
    avg=np.sum(weights*d)/weights.sum();want=np.sum(weights*(d-avg)**2)
    got=m.conditional_projection(d,sig,np.ones((4,1)))
    np.testing.assert_allclose(got['projected_information'],want,rtol=2e-14,atol=0)
    assert got['z_physical'] is None and got['lnB'] is None
    return {'information':got['projected_information'],'closed_form':float(want)}
check('T05 independent weighted-intercept closed form',closed_projection)
def projection_scales():
    d=np.array([1.,2.,4.,8.]);sig=np.array([.7,1.,1.3,.9]);design=np.ones((4,1))
    info=m.conditional_projection(d,sig,design)['projected_information']
    tiny=m.conditional_projection(d*1e-40,sig,design)['projected_information']
    np.testing.assert_allclose(tiny/info,1e-80,rtol=2e-14,atol=0)
    assert m.conditional_projection(np.ones(4)*.01,sig,design)['projected_information']==0
    must_raise(lambda:m.conditional_projection(d,sig,np.ones((4,2))))
    return {'tiny_information':tiny,'constant_absorbed':True,'singular_refused':True}
check('T06 tiny effects and degenerate nuisance controls',projection_scales)
def fixture():
    return dict(event_id='MOCK_ONLY',role='calibration',N=8,N_source=8,source_path='fake/source.h5',source_sha256='a'*64,tar_path='fake/source.tar',tar_sha256='b'*64,dataset='samples',model='MOCK_ONLY',mass_frame='detector',mass_unit='solar_mass',source_field_mapping={k:k for k in m.FIELDS},samples=dict(df220=[.1,.2,.3,.1,-.2,-.4,.5,.6],dtau220=[.5,.4,.3,.1,-.1,-.3,-.5,-.7],Mfdet=M.tolist(),af=A.tolist(),z=Z.tolist()),priors={k:dict(status='DECLARADO_TEXT_NOT_NORMALIZED' if k in ('df220','dtau220') else 'OPEN_DERIVED_PRIOR_NOT_DECLARED',declarations=[{'path':'mock/'+k,'text':['Uniform(-1,1)']}] if k in ('df220','dtau220') else [],density=None,joint_factorization='OPEN') for k in m.FIELDS},thinning={'factor':1,'seed':None,'method':'none'},sample_weights='equal_as_stored')
def pairing():
    e=fixture();got=m.reading_diagnostics([e])['R-B']['events'][0];d=m.prediction_draws(M,A,Z,'R-B')['delta_tau'];t=np.array(e['samples']['dtau220'])
    cov=float(np.sum((t-t.mean())*(d-d.mean()))/(len(t)-1))
    np.testing.assert_allclose(got['cov_dtau_prediction'],cov,rtol=2e-14,atol=0)
    v=np.var(t,ddof=1)+np.var(d,ddof=1)-2*cov
    np.testing.assert_allclose(got['residual_std_ddof1']**2,v,rtol=2e-14,atol=0)
    ee=copy.deepcopy(e)
    for k in m.FIELDS:ee['samples'][k]=ee['samples'][k][::-1]
    perm=m.reading_diagnostics([ee])['R-B']['events'][0]
    np.testing.assert_allclose(perm['residual_mean'],got['residual_mean'],rtol=2e-14,atol=0)
    ee['samples']['dtau220']=ee['samples']['dtau220'][::-1]
    shuffled=m.reading_diagnostics([ee])['R-B']['events'][0]
    assert not math.isclose(shuffled['cov_dtau_prediction'],cov,rel_tol=1e-3)
    return {'paired_covariance':cov,'row_permutation_invariant':True,'single_column_shuffle_changes_covariance':True,'equal_length_alone_does_not_prove_pair_identity':True}
check('T07 pair covariance and residual variance identities',pairing)
def invalids():
    for field,value in [('z',float('nan')),('Mfdet',0.),('af',1.)]:
        e=fixture();e['samples'][field][0]=value;must_raise(lambda:m.validate_events([e]))
    e=fixture();e['samples']['z'].pop();must_raise(lambda:m.validate_events([e]))
    must_raise(lambda:m.validate_events([fixture(),fixture()]))
    e=fixture();e['event_id']='ALIAS';must_raise(lambda:m.validate_events([fixture(),e]))
    return 'nonfinite, domains, unequal length, duplicate event/product refused'
check('T08 invalid samples and duplicate controls',invalids)
def open_channels():
    for r in ['R-MOD','R-PROP','R-RAIZ-COHERENT']:
        got=m.prediction_draws(M,A,Z,r);assert got['delta_tau'] is None and got['status']=='OPEN'
    assert m.prediction_draws([20.,30.],[-.1,.3],[0.,1.],'R-B')['status']=='OPEN'
    must_raise(lambda:m.prediction_draws([20.,30.],[.9,.9],[0.,1.],'R-MOD',[.1-.1j,.1-.1j]))
    must_raise(lambda:m.prediction_draws([20.,30.],[.1,.2],[0.,1.],'R-MOD',[.6+.1j,.7-.1j]))
    diag=m.reading_diagnostics([fixture()]);assert all(r['mode_440']['status'].startswith('OPEN') for r in diag.values())
    return 'Missing QNM, negative-spin BCW, forbidden corotation, unstable QNM and absent 440 fail closed.'
check('T09 OPEN channels and exact-QNM domain guards',open_channels)
reg={'e7':{'readings':{r:{'N_target_information':None,'status':'OPEN'} for r in m.READINGS}}}
def conservative_gate():
    variants=[{},dict(systematic_calibration_paid=True,physical_likelihood_paid=True,sigma_c_physically_calibrated=.1,selection_efficiency=.9,global_restricted_prior_normalization=1.),dict(systematic_calibration_paid=True,physical_likelihood_paid=True,sigma_c_physically_calibrated=-1,selection_efficiency='bad',global_restricted_prior_normalization={})]
    states=[]
    for gate in variants:
        for count in (0,1):
            rows=m.verdict_matrix(reg,{'gate':gate},count)
            assert len(rows)==20 and all(r['z_physical'] is None and r['lnB'] is None for r in rows)
            assert set(r['verdict'] for r in rows)=={'AWAITING_DATA' if count==0 else 'INCONCLUSIVE_SYSTEMATICS'}
            states.append(rows[0]['systematic_gate'])
    return {'gate_labels':states,'malformed_nonnull_gate_labeled_UNVERIFIED_not_red':True,'never_green_or_confirmed':True}
check('T10 adversarial nuisance claims cannot create physical verdict',conservative_gate)
def hashes_and_json():
    must_raise(lambda:m.require_pin(P/'producer/tgl_ringdown_ampliacao.py','0'*64))
    must_raise(lambda:m.require_pin(P/'producer/tgl_ringdown_ampliacao.py',None))
    must_raise(lambda:m.unique_object([('x',1),('x',2)]))
    must_raise(lambda:m.contained(B,'../escape'))
    return 'Wrong/missing hash, duplicate JSON key and path escape refused, all read-only.'
check('T11 pins JSON and path controls',hashes_and_json)
def imports():
    tree=ast.parse((P/'producer/tgl_ringdown_ampliacao.py').read_bytes())
    names={a.name.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names}
    names|={n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)}
    assert not names & {'scipy','h5py','bilby','extrai_posteriores_pseob'}
    return {'imports':sorted(names),'extractor_imported':False}
check('T12 consumer scientific imports NumPy only',imports)
# Consumer contract probes use a guard/IO mock. No extractor imported or called.
def consumer_probe(mutate=None, blind_plan=False):
    event=fixture();planned={k:copy.deepcopy(v) for k,v in event.items() if k not in ('samples','priors','N','source_field_mapping','thinning','sample_weights')}
    planned['fields']={k:k for k in m.FIELDS};planned['prior_paths']={k:['mock/'+k] if k in ('df220','dtau220') else [] for k in m.FIELDS}
    if blind_plan:planned['role']='blind_test'
    rr=copy.deepcopy(reg);rr['statistics']={'maximum_information_weight_INPUT':.2,'split_null_seed':123}
    rr['e7'].update(nuisance_path='fake/nuisance.json',plan_path='fake/plan.json',plan_sha256='c'*64,nuisance_sha256='d'*64,prediction_source_sha256=include['e7']['prediction_source_sha256'],producer_tree_sha256=manifest['producer_tree_sha256'])
    pay={'registration_sha256':'e'*64,'plan_sha256':'c'*64,'producer_tree_sha256':manifest['producer_tree_sha256'],'events':[event],'authorization_sha256':'f'*64,'schema':'POSTERIORES_PSEOB_V1'}
    if mutate:mutate(event,pay)
    accesses=[]
    def reader(path):
        n=Path(path).name;accesses.append(n)
        if n=='nuisance.json':return {'gate':{}}
        if n=='plan.json':return {'events':[planned]}
        if n=='payload.json':return pay
        raise AssertionError('Unplanned mock read '+n)
    old=(m.checked_context,m.read_json,m.require_pin)
    m.checked_context=lambda *args:(rr,types.SimpleNamespace(authorize_event=lambda *args:True))
    m.read_json=reader;m.require_pin=lambda *args:None
    try:
        result=m.run(B,'mock-registration','e'*64,'payload.json','f'*64)
        return {'accepted':True,'reported_N':result['fullsample_diagnostics']['events'][0]['N'],'status':result['fullsample_diagnostics']['status'],'reads':accesses}
    except ValueError as exc:
        return {'accepted':False,'error':str(exc),'reads':accesses}
    finally:m.checked_context,m.read_json,m.require_pin=old
check('T13 mock consumer valid baseline',lambda:consumer_probe())
def blind_gate():
    r=consumer_probe(blind_plan=True);assert not r['accepted'] and 'payload.json' not in r['reads'];return r
check('T14 blind plan rejected before mock payload read',blind_gate)
probes=[]
def probe(name,mutator):
    r=consumer_probe(mutator)
    probes.append({'name':name,'expected':'REJECT','actual':'ACCEPT' if r['accepted'] else 'REJECT','evidence':r})
def trunc(e,p):
    for k in m.FIELDS:e['samples'][k]=e['samples'][k][:2]
    e['N']=e['N_source']=2
probe('F1a truncated draws despite registered N_source=8',trunc)
def frame(e,p):e['mass_frame']='source';e['mass_unit']='kilogram'
probe('F1b wrong frame and unit',frame)
def mapping(e,p):e['source_field_mapping']['df220']='dtau220';e['model']='WRONG_MODEL'
probe('F1c changed mapping/model',mapping)
def prior(e,p):
    for k in m.FIELDS:e['priors'][k]={'status':'ANY_STRING','declarations':None}
probe('F1d malformed/absent deformation prior declarations',prior)
def authorization(e,p):del p['authorization_sha256'];p['schema']='UNRELATED_SCHEMA'
probe('F1e missing authorization and wrong payload schema',authorization)
# Static extractor checks, never loading/executing extractor functions.
tree=ast.parse((P/'producer/extrai_posteriores_pseob.py').read_bytes())
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='prior_metadata')
attrs=sorted({n.attr for n in ast.walk(node) if isinstance(n,ast.Attribute)})
static={'prior_metadata_attribute_checks':attrs,'rejects_virtual_prior_dataset':'is_virtual' in attrs,'rejects_external_storage_prior_dataset':'external' in attrs,'extractor_execution':False,'prior_dataset_read_line':[n.lineno for n in ast.walk(node) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='node']}
print(json.dumps({'runtime':{'python':sys.version.split()[0],'numpy':np.__version__},'tests':records,'test_count':len(records),'test_failures':sum(r['status']=='FAIL' for r in records),'consumer_negative_probes':probes,'static_extractor_custody':static,'no_files_written':True,'extractor_imported_or_executed':False,'no_real_posterior_or_strain_access':True},ensure_ascii=False,indent=2))

```

A conferência complementar de F2 avaliou somente o AST do `if` da linha 29 de `prior_metadata`, com `h5py.Dataset` substituído por uma classe vazia de teste. Para os três objetos (S/virtual, S/armazenamento externo, O), o predicado de rejeição retornou False. Nenhuma função do extrator foi executada. O apêndice principal conserva também a inspeção AST que registra a ausência de `is_virtual` e `external` na função.

