[REAL — revisão independente do diagnóstico descritivo NÃO-CEGO; OPEN — lnB, cobertura frequentista e robustez das guardas sob −O]

# F2 — revisão independente da injeção pública

Data UTC: 2026-09-22T19:03:46.532488+00:00. Objeto: `bis/f2_injection/REPORT.md`, quatro scripts e seus metadados/resultados/recibo, construídos pela bancada identificada como Averroes pelo agente principal. Não é novo posterior, nova campanha, PE ou aprovação integral de F2.

**Parecer: válido no escopo descritivo declarado, com ressalva operacional P2 para reutilização dos scripts sob Python otimizado.** Não encontrei erro numérico nas contas verificadas, lnB fabricado ou inferência indevida de cobertura a partir deste único ponto. A ressalva não invalida os resultados arquivados, cuja integridade e contas foram conferidas independentemente.

## Evidência independente e resultado

Conferi os sete insumos e oito arquivos produzidos listados no recibo, por tamanho e SHA256, além dos cross-hashes de dependências, extração, esquema e HDF5. Fonte: 64331592 bytes, SHA256 `e2373f81973401adfb78037236d28480155e3d0c428d49d46f822b381111a826`. HDF5 foi aberto somente para leitura de campos selecionados de posterior/prior/metadados; sem strain, pickle, execução de notebook, import de produção ou de um.py. A fonte e os artefatos permaneceram byte a byte íntegros após os controles.

Recalculei os oito campos em cada grupo (16 séries de 20.000 linhas): médias/DP por somas independentes, quantis por interpolação de estatísticas de ordem, intervalos centrais/contíguos mínimos, massas de sinal, quadrantes, correlações e pares distintos. Conferi também declarações/amostras de prior, campos de verdade não finitos e conversão para null. Todos coincidem com o JSON, dentro da tolerância explícita do controle (rtol 2e−12, atol 2e−13).

Para KDE, implementei diretamente a soma dos kernels gaussianos em NumPy, usando covariância e transformação de coordenadas; **não chamei scipy.stats.gaussian_kde nem importei o construtor**. Mantive a divisão e bandas registradas para verificar a implementação: 16.000 treino/4.000 consulta, semente 1302212026, multiplicadores 0,7/1/1,4. Os seis conteúdos coincidem exatamente, inclusive as contagens inteiras de consultas; densidade em GR e suporte local também conferem. É verificação independente do mesmo estimando, não um novo estimador científico nem validação de cobertura.

| Configuração | Mediana δf220 | Mediana δτ220 | Conteúdo conjunto em GR: 0,7 / 1 / 1,4 |
|---|---:|---:|---|
| NR_with_44 | +0.020948 | +0.047857 | 0.85925 / 0.86800 / 0.87500 |
| NR_without_44 | +0.027949 | -0.101295 | 0.95300 / 0.95075 / 0.95025 |

Os quantis sustentam as frases do relatório: δf220 tem intervalo central de 90% positivo e de 95% incluindo zero nos dois casos; δτ220 inclui zero com 44 e tem intervalo de 95% negativo sem 44. Sem 44, 0,95075 está só 0,00075 acima do corte de 95%, ante escala condicional de consulta 0,0034214: não sustenta exclusão conjunta robusta. Com 44, os conteúdos calculados são compatíveis com inclusão conjunta a 90%. As 20.000 linhas e 19.997/19.758 pares distintos não são número de injeções nem ESS de cadeia.

## Escopo físico e estatístico

F2/ORDEM_013BIS:85 pede extração e descrição de uma injeção com/sem 44, explicitamente sem curva em SNR. A apresentação respeita esse limite: não multiplica as duas recuperações como eventos, não acrescenta ao catálogo e não afirma tendência populacional, poder ou calibração frequentista.

[KNOWN — consulta primária pontual] Conferi a seção .7 e a legenda/discussão da Fig. 11: trata-se da simulação SXS:BBH:3617 de massas iguais e spins nulos, em ruído gaussiano, com uma comparação removendo os multipolos 44 e mantendo simulação/parâmetros. O objetivo é a informação de frequência 440. A realização exata de ruído não foi reconstruída. Não transportei para esta comparação a seleção de ruído descrita na seção .3. [Artigo LVK, seção .7](https://arxiv.org/html/2509.08099v1#A1.SS7).

Não foi lido o artigo integral por esta revisão. O vínculo entre HDF5 e simulação permanece uma identificação documental consistente, não reprodução do sinal. Flags gaussian_noise/zero_noise do arquivo de configuração não contradizem, por si sós, dados preparados externamente. A ausência de verdades numéricas recuperáveis nesses campos está exposta; não impede usar (0,0) como referência teórica GR para as deformações do setor 220.

Os contornos medem massa posterior acima da densidade estimada em um ponto, não probabilidade de GR, p-valor, taxa de falsos positivos ou cobertura sobre repetições. A dependência amostral, a divisão única e a incerteza de treino continuam limites. O suporte local usa a KDE de **20.000** linhas, enquanto o conteúdo usa a KDE treinada em **16.000**; o JSON distingue full_sample e train. Recomendo explicitar esse detalhe na nota da tabela para evitar que suporte local seja lido como ESS da KDE de treino. Não é erro nos valores.

## Priors e ausência de lnB

Conferi os quatro Uniform arquivados: 220 em [−0,8;2,0], 440 em [−0,8;0,8]; declarações analíticas idênticas entre grupos, amostras dentro dos limites e os quatro desvios variando nos dois posteriores. Portanto **440 é nuisance livre nos dois casos**; retirar o 44 da injeção não fixa os parâmetros 440 da recuperação. Esse recorte não é diretamente o de catálogos com 440 fixo.

P(δ220>0) no prior é 2/2,8=0,7142857. O relatório usa corretamente essa base ao discutir 0,7776 para δτ220 com 44; a diferença é 0,0633143. Sinal positivo de mediana, isoladamente, não demonstra deslocamento físico. Correlações próximas de zero em 5.000 amostras não provam independência global dos priors.

`PRIOR_CONTRACT.json` e `RECEIPT.json` conservam **lnB=null**, não zero. A fórmula de razão de integrais é válida sob as hipóteses ditas: se p(η,x|d) é o posterior abrangente, π(x|η) seu prior condicional e o prior normalizado de η é comum aos modelos restritos e ao abrangente, então Z_g/Z_amplo = ∫p(η,x=g(η)|d)/π(g(η)|η)dη; dividir pela expressão com g=0 dá a razão requerida. Um prior auxiliar diferente exigiria também a razão desses priors no integrando. Uma média de razões condicionais ou apenas massa de sinal não substitui essa identidade.

A revisão confirma priors de deformação conhecidos e campos de remanescente úteis; não certifica conversão/normalização integral do prior externo nem suporte das curvas em todo seu domínio. Finitude/extremos de amostras não provam esse suporte. A decisão de adiar lnB é honesta neste diagnóstico; não prova que calculá-lo seja impossível, que todos os priors sejam desconhecidos ou que a falta de parâmetros verdadeiros, sozinha, impeça Bayes factors. A ordem pede descrever esta pasta; o adiamento não deixa este recorte descritivo sem cumprimento.

## F2-INJ-R1 — P2 operacional, assert permite sobrescrita sob −O

`bis/f2_injection/check_contract.py:40` protege o destino com `assert not p.exists()` e `:43` termina em `t.replace(p)`. Sob `python -O`, a primeira guarda desaparece e replace substitui o destino existente. Reproduzi apenas esse bloco real com caminhos/bytes inteiramente simulados: sem otimização, AssertionError e nenhuma escrita; com optimize=1, criação do temporário simulado e substituição do resultado simulado. **Nenhum arquivo de produção foi alterado para demonstrar isso.**

Também dependem de assert os pins da fonte em check_contract.py:14/38 e várias guardas de integridade/formato nos quatro scripts. Não encontrei indício de execução otimizada do construtor original; os recibos atuais e os controles independentes pagam a integridade desta versão. A frase irrestrita “os scripts recusam sobrescrever resultados” precisa dessa correção antes de reutilização sob −O.

Correção exata em scripts novos ao lado: usar `if p.exists(): raise FileExistsError(p)` e exceções explícitas para fonte/hash/tamanho/finitude/cobertura; verificar os bytes temporários sem assert e impedir substituição de destino existente também na etapa final. Testar sob −O destino preexistente e pin incompatível, exigindo recusa e zero alteração. Preservar resultados atuais; não requer nova ciência. Os demais scripts já têm if explícito para destino, mas suas verificações de bytes/insumos ainda precisam deixar de depender de assert para robustez otimizada.

## Limites e custódia da revisão

O status AGUARDA REVISÃO no original é preservado como histórico do construtor; este documento é o parecer independente ao lado. Aprovação limitada ao diagnóstico descritivo e às contas conferidas, com ressalva R1 de reutilização. Cobertura frequentista, causalidade exclusiva do 44, generalização em SNR, lnB integral e validação da pipeline LVK continuam OPEN. Nenhum gate muda.

Controle próprio: `bis/c1_review/f2_injection_independent_checks.py`, executado em WSL /opt/lal_env com `-B -O`, uma thread; tempo medido 3.595 s. Resultados em `f2_injection_independent_results.json`. Consulta Atlas/protocolo somente leitura. Sem alterações em memória, canônico, originais ou produção. Axiomas: N/A.

| Caminho relativo à raiz | SHA256 lido |
|---|---|
| `bis/f2_injection/REPORT.md` | `720b041f207520bbe36264b1d77f475794a077bbbaa5840d486f634cc85357ca` |
| `bis/f2_injection/RECEIPT.json` | `0d4120d77f179d4d4d3aeb90c52168bf56365b8796bbdf726e9529934058db77` |
| `bis/f2_injection/inspect_injection.py` | `9d23c7ab872bfea23feadbc45d35036a3f15316ffc5f8f1cbe5c6ca29f89b212` |
| `bis/f2_injection/diagnose_injection.py` | `3db0eb150ff2860c3f83b04c8f3e8d7e31c853632c4774987bcdf9cb85f031a0` |
| `bis/f2_injection/check_contract.py` | `09243b81f04efdb2832b9002795da2e1419142b461956b152b88e99531468080` |
| `bis/f2_injection/write_report.py` | `1056aca5c9909b281112ae1780fbb64230cc08522ae7e74097e3504d8829ea0a` |
| `bis/f2_injection/METADATA.json` | `b56c22e54d99b98d0693e915326f410f193063928248e859902df6692625f305` |
| `bis/f2_injection/DESCRIPTIVE_RESULT.json` | `bc1fec39f21d92dd19d0953d4d9ae14bae4b2eed5ea80aa60a405fc42e091ecc` |
| `bis/f2_injection/PRIOR_CONTRACT.json` | `1900f0bc77d98e99be08e5e476388975f5b2d90b68da561555c36349876dad1e` |
| `bis/c1_review/f2_injection_independent_checks.py` | `26d884e16bd3370d51baf7606774b2be6e9f34b726fd085f12f5bdb781466add` |
| `bis/c1_review/f2_injection_independent_results.json` | `9787e57f7c68ed2dbb507a68b3bb82aacae15b43ca9fc4c6cbe6a18eec74f928` |
