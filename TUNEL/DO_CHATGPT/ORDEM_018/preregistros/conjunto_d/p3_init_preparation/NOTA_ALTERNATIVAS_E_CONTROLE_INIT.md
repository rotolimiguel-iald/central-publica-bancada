# Inicialização P3 — alternativas e controle isolado preparados

[REAL — somente preparação] Consultado mapa450. Foram lidas e pinadas 16 fontes/configurações instaladas do runtime; as cópias ficam em sources/. Foram preparados dois deltas e um controle exclusivamente de inicialização. Nenhuma alternativa, controle científico ou campanha P3 foi executada. Pastas V2, candidato e CODEC_002 permanecem intactas. Não foram criados autorização, CLAIM ou novos jobs científicos.

## Causa e fronteira conhecida

[REAL] A falha450 ocorre antes de waveform/likelihood. A factory `InterferometerList(["H1","L1"])` chama `get_empty_interferometer`, que abre a configuração fixa de cada detector. `networks.py:449–460` avalia seus valores; ambos os arquivos indicam `PowerSpectralDensity(asd_file='aLIGO_O4_high_asd.txt')`. `psd.py:263–268,297–338` procura o arquivo local ou instalado e o lê por `np.genfromtxt`, construindo PSD e cache antes de devolver o detector. A leitura foi negada pelo hook. `networks.py:443–446` captura `OSError` — classe ancestral de `PermissionError` — e converte a causa em “Interferometer H1 not implemented”. Isso explica a mensagem sem inferir ausência real de H1.

O driver só substituiria a PSD após a factory retornar. Portanto, o ASD padrão não deveria entrar na likelihood, mas é uma dependência real de inicialização da factory instalada. Não é strain ou posterior D; é uma curva de referência do pacote Bilby. Seu conteúdo não será usado para escolher a hipótese nem para regenerar/ajustar a PSD qualificada.

## Alternativas concretas

| Aspecto | A — construção direta | B — factory oficial com dependência exata |
|---|---|---|
| Código | `init_detectors.build_A`; `DELTA_ALTERNATIVA_A.patch` | `init_detectors.build_B`; `DELTA_ALTERNATIVA_B.patch` |
| Geometria | Valores dos arquivos H1/L1 extraídos por AST aritmética restrita; nenhum eval/chamada da configuração | Mesmas configurações e factory instaladas, verificadas por hash |
| Leitura do ASD default | Dispensada | Exatamente um arquivo instalado, comum a H1 e L1; sem wildcard |
| PSD final | Objeto analítico criado diretamente dos arrays sintéticos pinados | Objeto default descartado; objeto analítico novo assume seu lugar |
| Vantagem | Remove dependência de ruído irrelevante à análise final e eval da configuração | Menor alteração no caminho já usado: preserva construção oficial, defaults e geometria |
| Custo de revisão | Extração/transcrição da geometria e equivalência completa ao construtor oficial | Comprovar leitura exata e que nenhum valor/cache default sobrevive à substituição |

[DERIVED — recomendação] B é a primeira proposta para o controle isolado, pela menor mudança validável. A razão não é contornar a guarda: a dependência foi localizada na fonte instalada, pinada, e fica restrita à inicialização. A guarda exata continua ativa; qualquer leitura desconhecida ou erro silenciado pela biblioteca falha o controle. A alternativa A permanece disponível para revisão, sem ter sido executada ou adotada.

## O que o controle preparado verifica

`control_init.py` exige hash do contrato e decisão específica ROOT `QUALIFY_INITIALIZATION_ONLY`, ainda inexistente. Não cria autorização nem CLAIM. Cria somente uma pasta independente `CONTROL_INIT_001` com identidade de processo e resultado; se ela já existir, recusa nova execução. Não importa/usa Dynesty por seu próprio código e não contém chamada de sampler.

Após conferir pins, usa somente o NPZ sintético P0–P2 RUN_002, com `allow_pickle=False`. Percorre os dois rótulos existentes GR_GAUSS/RB_GAUSS, sem novos jobs: confere hashes de ruído/sinal/injetado, grade, normalização e SNR calculado dos arrays congelados. Não gera ruído, PSD ou sinal novos.

Na alternativa B, verifica o pin do ASD instalado, recusa arquivo homônimo no cwd e confere o caminho efetivamente usado. Antes da construção da likelihood, exige novo objeto PSD; campos `asd_file`/`psd_file` iguais a None; arrays crus e PSD efetiva exatamente iguais à PSD analítica do NPZ. Repete essa prova depois do construtor da likelihood. Geometria, vértices/braços/tensor, banda final20–1024Hz, duração32s, fs4096 e início999999984 são conferidos. Preserva o `roll_off=0.2` nativo do objeto strain e `window_factor=1`; o `roll_off=0.4` do contrato temporal da fonte continua separado, sem corrigir defaults por conveniência.

WaveformGenerator e GravitationalWaveTransient podem ser construídos, conforme esclarecimento da coordenação. Todos os métodos relevantes de avaliação, a fonte efetivamente vinculada e `bilby.run_sampler` recebem guardas que contam tentativa e abortam. Sucesso exige zero tentativas e contador nativo da fonte zero, caches de waveform/ruído não avaliados, mesma assinatura e mesmos parâmetros inferidos. A inspeção encontrou `inspect.getfullargspec` no Bilby; o wrapper define `__signature__` explicitamente. A equivalência de assinatura foi verificada só em função stand-in com Python314, sem importar código científico ou o controle preparado.

Limites próprios propostos: 60s parede, CPU45/50s, 8GiB, um thread, sem retry. Esses limites são do controle sem PE e não alteram qualquer teto do contrato científico anterior. Falha mantém recibo e para; sucesso não autoriza nova campanha P3.

## Leituras conhecidas até a fronteira

O mapa completo por fases/pins está em `MAPA_LEITURAS_E_SUBSTITUICOES.json`. Antes do hook: entradas exatas, manifesto do interpretador/runtime, imports fixos já existentes e preload cp437. O manifesto existente enumera 1.162 arquivos; o futuro controle verificará cada hash, sem ampliar diretórios. Das 16 fontes específicas examinadas agora, 15 já constam desse manifesto e apenas o ASD é adicional.

Após o hook: NPZ sintético; na B, H1.interferometer, L1.interferometer e o ASD exato. Construção de grade, PSD analítica em memória, strain, geometria e inspeção da assinatura são os passos seguintes. O construtor GWT configurado usa objetos existentes: marginalizações falsas, quadro sky e tempo geocêntrico desativam tabelas de distância/calibração e a criação de detector de referência. Não foi localizado outro arquivo de dados nessas ramificações. Isso é análise estática, não garantia de completude dinâmica; lazy imports e leituras inesperadas continuam recusados e deverão aparecer no controle.

A auditoria Python começa depois dos imports fixos e não é confinamento de syscalls nativas. Cálculos geométricos auxiliares não são waveform; o contador da fonte não inventaria toda função C. Avaliação científica, custos de PE, convergência, cobertura e D continuam OPEN.

## Evidência e próxima decisão

[REAL] 78 verificações estáticas/integridade passaram; 24 entradas pinadas, 16 snapshots de fontes e um único caminho extra proposto. O custo do controle é desconhecido porque ele não foi executado. Os deltas são propostas textuais; não foram aplicados ao driver antigo.

Arquivo adicional: /opt/lal_env/lib/python3.12/site-packages/bilby/gw/detector/noise_curves/aLIGO_O4_high_asd.txt
SHA256: eb5ec9b081c3d86d2f4257b9aff6a57566d168b8a95e5e57b7909eebad021780
Bytes: 71136

Contrato de controle SHA256: ec8ca95137da8f27ffeb1636cbe6fe779463286d62b341387a23b33649ced6a9

Próximo passo: ROOT revisar o contrato, os deltas e a recomendação; decidir se autoriza apenas o controle isolado. Não há permissão de nova PE nesta entrega.
