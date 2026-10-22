# F0.3.B2 — revisão limitada da implantação e manifesto

Autor: nu2_theory_sources. [REAL — leitura de código e helpers em fixture sintética] Nenhum --apply, gerador de manifesto, processo instalado ou arquivo original científico foi executado/alterado nesta revisão. As cópias exatas dos scripts examinados estão em DEPLOY_REVIEW_SNAPSHOT, com SHA256 em SNAPSHOT_AND_PROBES.json. A coordenação corrigiu parte dos achados durante esta revisão; as linhas abaixo pertencem à fotografia custodiada.

## Contenção e custódia

- deploy_candidate.py:19–23 recusa caminho absoluto, .. e destino resolvido fora da raiz Bancada. A lista de implantação :25–28 inclui apenas entradas relativas de código/fontes e o manifesto; as referências absolutas a um.py, selo, pipeline e outras fontes externas não viram destinos de escrita. O builder escreve somente no candidate e lê os originais. Não localizei destino de escrita no Nós/kernel/um.py original.
- :30–39 verifica bytes do candidato e baseline instalado; recusa overwrite não listado. :44–45 compara plano e hash do manifesto. :54–59 reconfere destino e preserva backup byte a byte. :60 usa o buffer candidato já pinado. :62–63 verifica os pins instalados.
- :9–18 escreve temporário exclusivo, fsync, tamanho e os.replace; limpa seu temporário no finally. Nas sondas, caminho válido permaneceu contido, absoluto/.. foram recusados, falha simulada no replace preservou o original e removeu o temporário.
- :65–74 tenta cada restauração mesmo após outra falhar e grava recibo de falha. Backups sobrevivem. Isso supera a versão inicialmente lida, cujo rollback podia parar sem recibo e cujo temporário sobrava.
- build_manifest.py:40–44 agora deriva versão, hash do programa e hash do selo dos mesmos buffers lidos, conferindo ligação e versão do selo. Fontes externas são pinadas, com check_each_call=true e estatuto de custódia, não admissão do operador. Tabela/JSON/PDF copiados permanecem bytes idênticos, ou o conflito é recusado.

## Ajustes residuais comunicados à coordenação

1. deploy:25 e :27 leem o manifesto duas vezes. Ler mraw uma vez e fazer json.loads(mraw); assim o plano e o pin referem-se à mesma geração.
2. deploy:54 verifica current, mas :57 relê old para backup. Guardar current já conferido. A exclusão de escritores durante implantação continua necessária: uma leitura dupla não constitui lock.
3. builder:23–24 lê e copia novamente o contrato NU; :27–28 valida a extração e a relê em copy_same. Copiar exatamente os buffers cuja identidade foi conferida, e confrontar esse buffer com extraction_sha256.
4. deploy:70–72 marca restored=True depois da operação, sem confrontar o hash restaurado com old_sha256. Acrescentar conferência e registrar ausência no caso de arquivo novo removido. O backup em si não prova restauração bem sucedida.

Esses pontos são de consistência de bytes e recuperação; não foram simulados como edição adversarial no diretório real. Helpers apenas foram extraídos via AST e executados no temporário. Não foi executado o caminho --apply nem o builder, nem em cópia.

## Critério para reinício do legado

Um 404 em /api/atividades não demonstra ociosidade. CPU/GPU baixos tampouco demonstram ausência de tarefas assíncronas. Antes de encerrar o PID legado, impedir novos despachos e ter evidência de conclusão das chamadas/tarefas do processo identificado, ou uma alternativa cooperativa que preserve as tarefas conhecidas. Não registrar idle verificado quando o inventário é inacessível. Depois da parada, conferir o PID e listener encerrados antes de anunciar a substituição. A subida do novo processo deve conferir identidade, prontidão e recibo; não exige rodar um ajuste observado. Esta é a recomendação operacional pedida; execução/reinício competem à coordenação.

## Regressão após rotas de neutrinos

31/31 testes core aprovados, EXIT 0, fontes estáveis antes/depois. CORE_RECEIPT_R3_neutrino_routes.json (SHA256 11d4f9c1909d1bef0304ac6f50fbf1164a195713436b0ca9b6247f34b42c29d6) e CORE_TEST_R3_neutrino_routes.log preservam comando, tempos e pins. Essa regressão reaplica a suíte de identidade/HTTP/GW; não é um ensaio empírico ou teste científico dos endpoints novos de neutrinos.

Nenhum gate mudou. Não há declaração de implantação concluída nesta revisão.
