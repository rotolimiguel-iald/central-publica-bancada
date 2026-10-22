# Q01-THETA — próxima qualificação independente proposta

Pedido gerencial 23d6a698-270b-4ecd-be8d-94eb9ff31993; preparação 4e9a80ad-dac3-4c6c-8ec5-b7927a9c056d. [REAL documental] Identidade gravada antes do código, após consulta do mapa613; início registrado615. A preparação não cria autorização, claim científico ou resultado numérico.

## O que esta unidade esclarece

Qualifica um recorte da dependência Q01 do quadro F1e: o integrador externo ad025, seu contrato de callback, a família completa e o prior normalizado sobre a caixa. A evidência Q01 escalar PASS9 é reaproveitada como antecedente, nunca repetida. Não é uma execução dos serviços f820, dos priors df482, da likelihood a987 ou da montagem I02/I03. Estes nomes nos envelopes sintéticos servem apenas para exercer o protocolo; não representam execução desses módulos.

Alternativa escolhida: integrais analíticas e falhas sintéticas com biblioteca padrão, usando o integrador original pinado sem monkeypatch. Alternativa preterida: integração ponta a ponta de dados/solver e store POSIX — depende de guard, entradas e decisões ainda ausentes e não cabe nesta unidade. Outra alternativa: uma segunda cubatura numérica como oráculo — acrescentaria dependência e erro sem necessidade para estes casos de solução conhecida.

A existência de uma unidade independente útil não fecha o restante de Q01. Permanecem as junções y/C/offsets/prefator, os priors físicos, perfis, suporte e C conjunta. Q02/Q03 físicas não estão exercitadas aqui.

## Casos e referências independentes

Seja u=(H0−50)/40, v=(ombh2−0,015)/0,015, w=(omch2−0,08)/0,10. O volume da caixa é 3/50 e a densidade uniforme é 50/3, portanto a medida transformada é du dv dw. As cinco escalas sintéticas são a=(1,2,3,1/2,5). Não são parâmetros cosmológicos nem valores de β_TGL.

> [nota operacional do operador — omitida no retrato público]

Em T06, PASS significará que o programa mantém explícita sua falta de certificado, NÃO que detectou ou integrou o pico. A razão verdadeira do primeiro contra o segundo é1 (log0), enquanto a regra amostrada lê1/2 (−log2). Esse controle demonstra por construção por que diferença pequena entre grades não limita toda massa omitida. Não é falha física da TGL: as funções são fabricadas e nenhuma predição TGL é calculada.

Todos os envelopes/recibos do callback são explicitamente SYNTHETIC. Seus hashes são calculados sobre bytes sintéticos reais e reproduzíveis, não inventados como se pertencessem a arquivos de execução. Os campos1/1 e VERIFIED_DURABLE_CACHE são fixtures do protocolo; não comprovam solver ou cache físico. O relatório registra solver_calls=0 e fixture_receipts_are_real_executions=false. O digest condicional usa a função existente do ad025; sua resistência criptográfica não é objeto do teste. O hash do descritor é conferido separadamente pelo harness.

As tolerâncias de confronto em log são1e−11 para T01/T02/T06 e3e−10 para os deslocamentos±1000. São tolerâncias de engenharia fixadas antes da execução; math.log e arredondamento não são aritmética intervalar. As fórmulas analíticas não usam a soma de Simpson do candidato como oráculo. Nenhum limite é relaxado automaticamente.

## Custo, runtime e contenção

Quinze tentativas de construção;14 chamadas primárias de run (N01 falha na construção), mais duas reentradas intencionais que devem ser recusadas antes de callbacks:16 tentativas de run no total. Seis casos com125 callbacks e nove negativos com0/3/2/2/1/2/2/1/2, total exato esperado765. Níveis1/2 usam27/125 nós; o reuso aninhado deve evitar152 callbacks por caso completo. Nada disso mede custo de uma grade cosmológica com CAMB.

Runtime: C:\Python314\python.exe, flags -I -S -B -X utf8, somente biblioteca padrão. Hash do executável e fontes é medido em CONTROL_CONTRACT.json. O driver deriva do supervisor Q01 pinado, adaptado em pasta nova; o original consumido não é alterado nem executado. Carregamento futuro compila os bytes exatos verificados em ModuleType e atesta código/funções; não usa pycache ou lookup de candidato por nome.

O fechamento inteiro da biblioteca padrão/DLL não está pinado por este pacote. O executável e os dois códigos carregados são pinados/atestados; isso delimita a afirmação de runtime. Um filho Windows oculto, sem shell, casos seriais; prazo nominal total30s desde main, cooperativo23s, espera25s e reserva de recolhimento. O tempo de inicialização do interpretador/imports do supervisor é excluído. Não é garantia de tempo real. Saída de cada stream até64KiB é critério de aceite posterior, não quota física. Sem limite rígido de RAM por Job Object ou benchmark alegado; as estruturas científicas ficam limitadas a125 nós por instância.

O supervisor exige uma futura ROOT_DECISION.json que ligue request_id, manifesto e revisão; valida antes de criar RUN_CLAIM O_EXCL. O worker exige pai/nonce, cria WORKER_STARTED antes de carregar o candidato e conserva registros por caso. Claim parcial/presente ou output existente impede reexecução. Resultado worker é provisório: aceite exige exit0 externo do supervisor, recibo terminal PASS e ausência de falha. Não há fallback, retry ou troca de nome para contornar incerteza. Metadados de decisão não substituem a autoridade ROOT e a proteção do diretório.

## Comando candidato — NÃO executado

Somente após revisão independente e decisão própria de ROOT:

```powershell
& 'C:\Python314\python.exe' -I -S -B -X utf8 'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_theta_qualification_preparation\driver.py' --decision-sha256 '<SHA256_REAL_DA_FUTURA_ROOT_DECISION.json>'
```

Não há arquivo ROOT_DECISION/AUTH/CLAIM nesta preparação. O schema descritivo fica no contrato, sem autorização válida. O manifesto prende casos, driver, contrato, linhagem e evidência estática. A chamada de build_preparation.py é apenas empacotamento/AST, não o comando de qualificação.

## Pendências preservadas

Antes de consumir qualquer fundo via I02, o controlador deve conferir explicitamente joint._admission['prediction_admission_sha256'] == plan['assembly_admission_sha256']. Esta unidade não modifica a fonte I02 congelada, não exerce esse preflight e não legitima detecção tardia. Guard/autorização/código carregado, POSIX/durabilidade, concorrência e crash continuam por concretizar/qualificar em unidade própria.

O stack remoto continua inelegível segundo ROOT: sources.ok=false, âncora/geração divergentes, uma coordenação antiga e zero execuções. Não houve preview novo porque esta tarefa é local e não precisa de provedor; não houve repin, mudança de executor ou despacho. I03/Q01/c435/ffd6/NC02 e demais unidades consumidas não foram reabertas. Memórias globais/ledger ficam com ROOT; esta pasta entrega somente a preparação delimitada solicitada.
