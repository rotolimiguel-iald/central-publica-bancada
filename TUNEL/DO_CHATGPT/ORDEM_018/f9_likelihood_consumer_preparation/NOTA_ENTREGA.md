# Entrega F1(c) — consumidor puro preparado

[REAL — preparação estática] Pedido a9874f79-9d71-48f5-824c-d51d6d819534.
Foi escrito likelihood_consumer.py, adaptador de entradas explícitas para a classe gaussiana
existente, sem duplicar o solucionador. A alternativa foi fixada antes de escrever o candidato.
A API liga os 283 IDs, as 63 colunas eta e a escala T aos metadados das fontes já admitidas,
mantém a família de cinco modelos e usa a estrutura hash-admitida do montador.

O código aplica Ty, TCTt e a mesma T à origem afim, conserva X e médias já transformados,
preserva offsets presentes em y e entrega a integral pontual normalizada em d_eta,
omitindo apenas log(kappa) comum identificado. Priors físicos ficam como metadados não
aplicados. Não calcula ajuste, evidência, lnB, p, sigma, certificação ou veredito.
Suporte/posto e normalização continuam no backend preservado. Densidade zero fora do
suporte comum é distinta de falha de schema/covariância/posto; esta aborta a coleção inteira.

[REAL — 93 conferências estáticas] audit_static.py executou apenas leitura/hash/AST e
projeções de metadados de identidade; todas passaram. Nenhum candidato, numpy ou backend
foi importado, nenhuma função do consumidor foi chamada, nenhum teste numérico foi realizado.
Os recibos históricos dos módulos gaussianos e a revisão548 foram lidos e pinados, sem
reexecução ou transferência de cobertura ao adaptador. Não foi montada campanha ou launcher.

[OPEN] O consumo numérico, a integração de objetos carregados, a admissão estatística e a
revisão independente ainda são futuros. A fronteira é um chamador confiável: nomes/flags/hashes
não autenticam por si objetos Python nem certificam hipóteses científicas. O consumidor
valida ligações em memória; o chamador verifica os referenciais efetivos fora da API.
A autorização futura de observações depende do operador/V1. MM permanece condicional
não ratificado, sem exclusão silenciosa de suas cinco linhas e sem cobertura alegada.

As edições de rascunho nesta pasta têm backups imediatos de bytes. Fontes externas, pacotes
selados, memórias compartilhadas e ledger não foram alterados. Nenhuma autorização ou CLAIM
foi criada. O registro de rota é preparação solicitada pelo coordenador, não liberação.

A auditoria inclui leitura dos pins novamente após escrita; os hashes do manifesto são
calculados diretamente de cada arquivo. Os backups contêm a primeira forma dos rascunhos
e são custódia da preparação, não versões alternativas autorizadas para consumo.

Arquivos principais: API_CONTRATO.md, CONTRATO_API.json, likelihood_consumer.py,
PIN_FONTES.json, IDENTIDADE_ESTRUTURAL_METADATA.json e RECIBO_ESTATICO.json.
