# Revisão independente I02 — admissão antes do background

[REAL — revisão estática, 2026-10-06T15:29:22.675008+00:00] Aceito o reparo 99e2bfa7-36b8-4e0f-92e7-1a6918e80591 no recorte de fonte. ROOT conferiu 26 pins únicos, o delta exato e a equivalência da AST após retirar exclusivamente a nova identidade e as duas verificações documentadas. O store preserva os mesmos bytes.

A igualdade entre prediction_admission_sha256 e assembly_admission_sha256 é exigida na construção de NodeContext (linhas48–49) e novamente em descriptor (104–105). O callback durável chama descriptor na linha187, antes da primeira aquisição na192, da consulta de cache na194, da aquisição de background na209 e do fornecedor na214. _require levanta ConsumerError quando a igualdade falha. A validação posterior do consumidor permanece.

Esse resultado fecha o defeito local de ordem das verificações sob módulos pinados e objetos confiáveis. Não demonstra execução real nem resistência a mutação concorrente/hostil. A criação prévia de DurableStore pode validar/sincronizar o diretório; não se afirma ausência de toda operação de filesystem antes da verificação.

O sucessor científico deve usar a nova identidade e os bytes revisados, com guard externo, operações POSIX exatas, quota agregada, objetos carregados, pipes/ACK/watchdog e recibo externo. Essas qualificações continuam abertas. Nenhum candidato foi importado ou executado, nenhum observado aberto e nenhuma chamada de provedor feita. O aceite não cria AUTH, CLAIM ou ROOT_DECISION, não fecha F1/F3 nem emite veredito físico.

Alternativas conferidas: A — comparação apenas posterior/externa; B — comparação antecipada interna com validação posterior preservada. B resolve o defeito descrito sem mudar fórmulas.
