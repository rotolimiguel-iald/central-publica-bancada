[REAL] A-1.c — extensão tipada e rejeição do tensor forjado.

Abertura SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a

[DERIVED — proposta compilada, fora do kernel] StressTensorDataLocal W B estende exatamente StressTensorData W, acrescentando simetria, conservação em teste e covariância sob B:WedgeBoostRep W. Na convenção (+---), exige para todo teste suave compacto f a integrabilidade de cada T_mu,nu * sinal_mu * derivada_mu(f), e a soma das quatro integrais igual a zero. A condição de integrabilidade evita que a integral totalizada esconda divergência. A transformação dos índices covariantes usa o boost inverso e seu transposto.

Preservação: os corpos originais de 22 lemas de janela/controle foram recompilados literalmente em dois recortes, sem substituir suas provas. O primeiro tem 21 declarações; o segundo reutiliza o lema existente de TriadMaster para o coeficiente 8πG. Oito corolários da extensão compilaram: primeira lei, Bekenstein–Hawking, Clausius, coeficiente 8πG, cancelamento de κ, controles afim/exponencial e rejeição do tensor forjado. A aplicação ocorre sobre o MESMO ContratoH3, lendo L.toStressTensorData, sem construir um substituto.

O controle b2 é recusado precisamente por symmetric: o H3 inicial não trivial e a simetria da fonte inicial implicam um ponto admissível onde o tensor forjado não é simétrico. Logo não existe extensão local proposta cuja projeção seja esse tensor. Isto não prova existência do H3 inicial ou da extensão.

[OPEN — alcance] Local no nome segue a ordem; o tipo ainda fala de EXPECTATIVAS. Não constrói distribuição de operadores, afiliação à rede, domínio comum, sesquilinearidade ou microcausalidade. B é índice explícito: numa aplicação física deve ser o boost do mesmo H2; os corolários de janela não usam essa identificação. Conservação/covariância são exigências novas, não derivadas gratuitamente do H3. As paredes H2 não dependem de T; as paredes H3 afim/exponencial foram efetivamente especializadas. Não foi recompilado aqui todo o arquivo agregado de paredes legadas, cuja reprodução A-1.a permanece com MEDIDA de memória.

Auditoria: 30 declarações, trio permitido, zero sorry/axioma novo, rc 0 em todos os três recibos. Fonte v1 e suas evidências preservadas; v2 amplia somente os corolários, não corrige falha. Recursos dos três passes: 71.187000s parede, 69.968750s CPU. B pesada 0h. Nenhuma chamada externa nesta entrega. Comandos integrais e limites de cada passe nos recibos.

- C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\minimal_imports\WindowLemmasVerbatim.lean, SHA256 444e0111488f43ed357bcc032919db8e4c57a6d1ae9b5bf8be91c496654972a5
  Log C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\minimal_imports\window_lemmas_01.log, SHA256 84c0e360b77b362b33df67837e80eff27c00edd9dee45663832a0e0a10119c5f
  Comando/recibo C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\minimal_imports\window_lemmas_01.json, SHA256 d59caa8367ed7e7d963dcb898318c3c706591d830e75d526c91b883b1bc789d3
- C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\minimal_imports\WindowCoefficientVerbatim.lean, SHA256 e53d82b5c6127ba1fd938fb0318173f9fd393d9fe6f7d590284d8eb192f4d003
  Log C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\minimal_imports\window_coefficient_01.log, SHA256 5019ba2c3337da1d5a6755b830fe6d7bc245fa139b5081c82dc77d85f7690823
  Comando/recibo C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\minimal_imports\window_coefficient_01.json, SHA256 292d134523b575d611d56892a4b7cedbe708782dc552aef67cd4a3d76864d509
- C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\StressTensorDataLocal_v2.lean, SHA256 06a32c20bd03c96c97ca8b193cbdcf6730c2246835d1f071693d66459c9b8879
  Log C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\local_stress_02.log, SHA256 099be59901a4bbb3d637d49e99b473012f7be9324e3a975c7d19d2d12318ad49
  Comando/recibo C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\local_stress_02.json, SHA256 8451b58395e09ba3a25d339a476bd950adaa1ae73b9ad75b80254553a8e2d63e

Manifesto: A1/local_extension_manifest.json SHA256 c934492ef02ce153347511889091877f03497c2969c1bed85d2ec27427e942fe.
Auditoria: A1/local_extension_axioms.json SHA256 d3a29460c4044581b341ee586c0a1cebbae6aa87aea6b9830819f244a5c05c85.

Não move H2/H3/import-H3 ou gate. A adoção do refinamento continua com a gerência. Próximo: finalizar A-1.b1 com a rota orquestrada e consolidar A-1.
