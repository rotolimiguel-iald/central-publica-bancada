# Estágio interno v388 — cofre e 16 dispositivos

[REAL — cópia e inspeção estática] Foram preparados 1.233 arquivos com identidade de bytes verificada em stage/vault/originals_copy: os 14 artefatos nomeados pelo selo v388, o próprio selo, o handoff e o stdout histórico, além dos 1.215 arquivos listados no manifesto formal e de uma cópia desse manifesto na raiz do kernel. Os 1.215 incluem 1.211 arquivos .lean; esse é o recorte do manifesto lido, não uma nova contagem de teoremas ou um novo build. Nenhum rito, runner, Lean, um.py ou import integral de candidato foi executado. Após autorização específica de ROOT, sete definições de função foram extraídas por AST (as seis novas e beta() preservada): 37/37 verificações de software passaram em 0,021 s, incluindo fixtures sintéticas do caminho de metadados. Isso não é validação física nem execução de dispositivo.

O destino é somente o estágio Chatgpt/ATUALIZACAO_SISTEMA_V388_20261006/devices. Os cofres de produção v386 e o módulo comum de produção permanecem intactos. Os dois destinos de produção v388 não existiam na inspeção. As cópias são dos arquivos selados exatos, sem reparação de originais.

## O que a atualização torna disponível

[INPUT — candidato] A camada compartilhada preserva a base v386 e acrescenta um campo adendo_v388 com a forma alpha(chi)=sech(chi/2), beta(chi)=alpha(chi)*sqrt(e), os estatutos e a lacuna de mu. Ela oferece também funções novas, explicitamente separadas, para leituras numéricas futuras de chi. O texto do núcleo v388 foi transportado como metadado, não recalculado nem promovido a prova nova.

[REAL — comparação estática] Os nove sub-blocos históricos que a camada v386 consulta são iguais, campo a campo, nos cores v386 e v388. O AST de beta(), formula_runtime(), fator_D1a(), fator_D1b(), axioma_e_verbo_runtime() e de todas as outras funções antigas permanece igual; somente camada() ganha uma chave no dicionário retornado. Removida essa única chave, seu AST também coincide com o original. VERSAO_DA_CAMADA permanece v386 como versão da base; adendo_v388 identifica a informação nova. Isso evita rebatizar cálculos antigos como recalculados na v388.

Os 16 runners foram lidos e analisados por AST. Todos carregam patents/_formula_completa/tgl_formula_completa.py e gravam seu resultado antes do selo do dispositivo. Os 16 manifestos FINAL declaram o mesmo hash dessa camada v386, conferido contra seus bytes atuais. Na etapa posterior desta mesma preparação, os 16 bundles antigos foram lidos por AST/base64 e os membros dos ZIPs conferidos contra seus manifestos. As 507 dependências únicas foram preservadas por bytes, sem interpretar os metadados opacos. Os 16 FINALs foram regenerados pelo empacotador oficial idêntico na raiz de estágio e todos os seus membros foram conferidos contra estágio, runners e camada. A única alteração de membro foi a camada comum; o único membro adicionado foi ADENDO_V388_METADATA.json. Nenhum FINAL ou runner foi executado.

Os vereditos de engenharia e physical_verdict_allowed=False permanecem. Resultados e selos antigos não são editados. Não se afirma avanço empírico de dispositivo, patente já implementando beta variável ou melhoria de desempenho por causa da nova fórmula.

## Duas alternativas de atualização

**A — proposta adotada no estágio:** transportar o cofre v388 por identidade de bytes e acrescentar informação tipada/retrieval e API explícita à camada comum. Os cálculos correntes continuam usando beta()=ALPHA_FINE_CODATA_2018*sqrt(e). A camada consulta o cofre v388 exato; os pins do programa, selo, core, manifesto e pedra nova são conferidos pelo candidato antes de expor o adendo. Se a versão corrente do cofre for outra, ou algum pin divergir, o adendo falha de forma visível.

**B — não adotada:** substituir automaticamente beta() por beta(chi(mu)) em todos os dispositivos e regenerar os resultados como se houvesse uma escala definida. Não existe mu por dispositivo/rito nem chi(mu) ratificados nas fontes consultadas. Essa substituição confundiria forma matemática com identificação física e mudaria cálculos/vereditos anteriores. Não está preparada nem implicitamente autorizada pela atualização de versão.

A atualização interna solicitada pelo operador não depende de ratificar B. É possível disponibilizar A e manter as identificações físicas abertas.

## Domínio e API adicionada

- alpha_of_chi_v388(chi): chi adimensional, finito e não negativo; cálculo binary64 pela forma estável 2*exp(-chi/2)/(1+exp(-chi)). Bool e valores não reais/finitos são recusados; underflow que apagaria a positividade levanta erro, sem devolver falso zero.
- beta_of_chi_v388(chi): a função anterior vezes sqrt(e), sempre em runtime. Não substitui a função beta() já usada.
- scale_reading_v388(chi, chi_sup): exige 0≤chi≤chi_sup e devolve a leitura e o piso beta(chi_sup), mais beta0 antigo para referência. Não presume beta(chi_sup)=beta0.
- beta_of_mu_v388(mu): levanta NotImplementedError, pois mu por dispositivo e a função chi(mu) continuam OPEN.
- camada(runner_path): assinatura preservada; apenas adiciona adendo_v388 após os controles antigos. O adendo é documental e não chama as funções novas de chi.

[KERNEL — fonte lida, não recompilada aqui] TheCouplingRunsBoundedBelow prova a monotonia em chi≥0 e o piso condicionado a 0≤chi≤chi_sup. chi=0 dá alpha=1 e beta=sqrt(e), não a constante Thomson. A identificação de alpha físico com essa coordenada é INPUT/ONTO; a corrida QED é literatura externa, e mu por rito é OPEN.

O vínculo a couplingOfAlpha tem a hipótese alpha<exp(-1/2), equivalente a beta<1 na forma exata. A API retorna um diagnóstico float desse domínio, não uma prova intervalar. Não alimentar automaticamente a matriz-S antiga ou theta_M com beta_chi: a forma global pode exceder 1, enquanto a rotina antiga usa beta0. Arredondamento binary64 não certifica desigualdade estrita nem precisão uniforme. Amostras de domínio/limites/forma foram avaliadas somente nos testes de software autorizados, sem escolher mu ou medir fenômeno físico. Esses testes não certificam erro uniforme.

## Fluxo oficial e plano de instalação para revisão ROOT

As referências reais são os HANDOFF_v386_CUSTODIA.md e HANDOFF_v388_CUSTODIA.md do Nós, o CUSTODY_MANIFEST.json v386 e tools/build_final_code.py. O handoff v388 indica site+cofre+runner+16 dispositivos e reserva commit/push ao operador. A remissão memory/handoff-v386-custodia.md na Central estava ausente; o handoff do Nós foi encontrado e lido.

1. ROOT revisa o manifesto do estágio, o delta mínimo e a separação entre base v386 e adendo v388. Nenhuma decisão científica de mu, ramo B ou Fase9 é requerida para transportar a informação com seus estatutos. O plano de v389 relatado por outra coordenação diz respeito a correções futuras de texto/rótulo, não a uma suspensão encontrada da atualização interna v388 solicitada agora.
2. Antes de instalar, reconferir os pins de entrada e do estágio. Os dois diretórios de destino v388 devem continuar ausentes; se aparecerem, parar e reconciliar com a coordenação que os criou. Não sobrepor custódias concorrentes nem substituir v386. A lista de mapeamentos exatos está em PLANO_INSTALACAO.json.
3. Após liberação de ROOT, copiar o par um_unificado_v388/tgl_kernel_v388 para o cofre interno e persistir recibo de instalação que identifique as cópias e a limitação de cobertura. O estágio contém o conjunto selado atual e as fontes do manifesto formal, mas não toda a cadeia histórica de ensaios v383–v388, cache/ambiente Mathlib ou publicação. Não chamar esse escopo de custódia pública integral.
4. Instalar os dois arquivos da camada compartilhada com backup imediato de bytes do arquivo existente, temporário verificado e substituição atômica. Preserve o hash do módulo v386 e seus resultados antigos. O adendo passa a estar disponível aos 16 runners por sua dependência comum; nenhuma execução ou resultado novo é presumido por instalar.
5. Os 16 FINALs já foram reempacotados no estágio nesta preparação. O oficial build_final_code.py foi copiado byte a byte para stage/tools, de onde deriva sua raiz isolada; não precisou de adaptação. Os 16 ZIPs contêm exatamente os membros antigos mais o ADENDO; apenas a camada comum mudou. RECIBO_BUNDLES_V388.json contém os pins e verificações. A instalação deve trocar os 32 arquivos FINAL.py/FINAL.manifest.json com backup imediato dos atuais, temporário verificado e atomicidade, conforme PLANO_INSTALACAO_COMPLETO.json. O empacotador não será executado em produção. Nenhum resultado ou selo histórico será regravado.
6. A execução dos 16 runners e a demonstração dos FINAL ficam explicitamente fora desta unidade. Os testes autorizados foram apenas das funções novas extraídas por AST e do caminho de metadados sob fixtures sintéticas. Resultado: 37/37 software checks. Não houve import de módulo de dispositivo nem leitura do cofre real por código candidato. Resultados antigos preservados não contam como validação física do novo adendo.
7. Publicação, PORTAs, README/site e commit/push não foram iniciados nem realizados por esta preparação. Não alegamos que estejam em atualização paralela. Nenhuma sincronização de Atlas ou ledger foi feita por este agente; ROOT cuida da consolidação das memórias da entrega.

A seleção automática de maior cofre do módulo original foi preservada, mas o adendo v388 exige a identidade exata revisada. Uma futura v389 precisará de seu próprio vínculo de proveniência antes de esta camada expor dados dessa versão.

## Coordenação e lacunas honestas

O mapa já registra outra coordenação da Central responsável pelo selo/exame v388 e proposta de v389. Há também estágios app, inventário e orquestrador na pasta de atualização; foram preservados. Não havia pasta devices no início. Não se deduz dessas informações que v388 esteja publicada ou instalada nos dispositivos.

O resultado desta unidade é um estágio revisável: bytes selados, inventário dos 16 vínculos, candidato aditivo e roteiro exato de instalação. Import/runtime do módulo completo, execução de dispositivos, implantação e publicação permanecem não realizados. Reempacotamento e 37 testes isolados de software foram realizados e têm recibos próprios, sem ensaio científico. O número de arquivos copiados não prova nova compilação, novo resultado experimental nem confirmação física.


## Cronologia dos recibos

VALIDACAO_ESTATICA.json, INVENTARIO_DISPOSITIVOS.json e o campo status de ADENDO_V388_METADATA.json são retratos da preparação anterior aos testes de software/reempacotamento. Foram preservados por hash: o rótulo CANDIDATE_NOT_INSTALLED_NOT_NUMERICALLY_EXECUTED não é um recibo permanente de disponibilidade. O estado atualizado está nos RECIBO_BUNDLES_V388.json, RECIBO_TESTES_SOFTWARE_V388.json e no recibo final desta entrega. O campo não é apresentado pelo adendo retornado ao runner; não muda β0 ou estatutos científicos. Nenhum desses documentos é autorização de instalação.


## Fonte viva alterada durante o fechamento

[REAL — reconferência de bytes] A checagem final encontrou o um.py vivo alterado depois da cópia. RECIBO_DIVERGENCIA_FONTE_VIVA.json registra os dois pins lidos. O estágio mantém o programa e64b00f4…46739 que o selo v388 transportado identifica; as demais 1.232 origens continuaram idênticas. A asserção interrompeu o fechamento antes de instalar; a divergência foi investigada somente por leitura. Não se deduz a versão ou validade do arquivo novo nem se substitui o snapshot selado. ROOT deve distinguir explicitamente “v388 selado” de “programa vivo posterior” ao decidir instalação/relato de atualidade. Esta é uma diferença de proveniência temporal, não alteração do estágio.


## Correções finais de metadados e escopo do snapshot

[REAL — bytes] O empacotador oficial calculava final_bytes sobre texto LF antes da gravação CRLF no Windows. Por solicitação de ROOT e achado independente, os 16 manifestos de estágio foram corrigidos para o tamanho real do FINAL e receberam final_sha256 lido do arquivo. Backups preservam os manifests anteriores; ZIPs e FINAL.py não foram regravados. Todos os membros foram novamente conferidos por leitura AST/base64, sem executar o código embutido. RECIBO_CORRECAO_FINAL_BYTES.json registra cada diferença.

[INPUT — coordenação ROOT] O escopo selecionado é instalar somente o snapshot v388 selado após revisão final; não importar os bytes posteriores do um.py vivo. Essa orientação resolve a escolha de versão do estágio, sem declarar instalação já feita nem promover a versão viva. A aprovação final de instalação continua com ROOT.
