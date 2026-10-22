# Avaliação local de contexto maior — v388

A recomendação é avaliar **Sonnet 5.5 com a montagem pública ampla já preparada**, mantendo Haiku público e Sonnet interno até decisão explícita posterior. O perfil Sonnet já existe, mas o caminho de produção ainda passa pela montagem e pelo orçamento legados. Esta entrega contém inventário, plano e dois corpos exatos de contagem futura; não implementa nem ativa a migração.

## Objeto científico disponível

[REAL — bytes conferidos] O prefixo público amplo tem **1.029.394 bytes**, SHA256 **a2a42ef56895d17b08ba1b433898bbb6e3160a9254b74f644f3f5a7fff39ef37**. Contém literalmente a mãe v5 (31.972 B), o núcleo operacional (25.623 B), o cluster v388 (885.241 B) e as cinco fontes formais completas H1/H2/H3/mestre/rota importada (26.564 B). Os 377 tópicos correspondem exatamente às chaves do resultado selado; 15 são novos. O catálogo tem 1.215 arquivos, somando 9.239.393 B; seus hashes e os 1.231 membros do snapshot foram conferidos. Não houve compilação Lean ou execução do programa.

Esta é a **montagem pública ampla existente**, não o corpus inteiro dentro do contexto. O cluster mantém remissões declaradas para coleções de detalhe; o rol redundante de 341 vereditos é recuperável na forma canônica. Os oito documentos admitidos, catálogo integral e prova selada continuam disponíveis pelas ferramentas. Mãe, núcleo, hipóteses e fontes formais não foram cortados. Não se promete que 1M comporte todos os 33,8 MB do programa, todos os JSONs e todos os fontes Lean simultaneamente.

O metadado auxiliar public_metadata.json registra **329.581 tokens de proxy o200k**, sem nova contagem local nesta rodada. Isso não é medida Sonnet. O prefixo corrente já está abaixo do antigo guard340k desse proxy; o diagnóstico355.963 era de montagem anterior. O metadado auxiliar conserva um sub-pin antigo do LOCAL_SEALED_MANIFEST. O manifesto staged atual e todos seus membros conferem; nenhum dos dois sub-pins aparece no prefixo. Um sucessor deve reancorar seu próprio metadado; **não é alegação de falha da produção ou do plano APP01 revisto**. Os pacotes anteriores foram preservados.

## Alternativas e viabilidade

1. **Sonnet5.5 / montagem ampla**, recomendado para avaliação: janela documentada1M e perfil local existente. Mantém mais conteúdo diretamente que a projeção Haiku, sem outra variante seletiva. Plausibilidade não certifica encaixe: tokens nativos permanecem null.
2. **Opus5.5:** mesma janela1M e tarifas de entrada/saída maiores. Não compra contexto adicional; exigiria outro critério de qualidade, ainda não medido.
3. **Permanecer Haiku:** mantém política, mas v388 de210.177 tokens permanentes medidos não cabe no pacote200k. B reversível e A seletiva ficam selados, sem nova alteração ou contagem.

Segundo as fontes oficiais verificadas pela ROOT em06/10/2026, Sonnet5.5 usa ID claude-sonnet-5-5, contexto1M e saída máxima128K. Tarifa normal: US$2/MTok entrada, US$10 saída, US$2,50 escrita cache5m, US$4 escrita1h e US$0,20 leitura. [Modelo](https://platform.claude.com/docs/en/models/sonnet-5-5/overview), [preços](https://platform.claude.com/docs/en/about-claude/pricing).

[INPUT — cenário, não medição] Para **600 mil tokens de entrada e4.096 de saída**, extremos Sonnet: US$1,24096 sem cache; US$1,54096 escrita5m; US$2,44096 escrita1h; US$0,16096 leitura integral do cache. Isso não atribui600mil tokens ao pacote, não é custo medido e não prevê cache hit. Acesso, cota, latência e qualidade não aferidos.

## Duas futuras contagens concretas

FUTURE_COUNT_MINIMAL.json: prefixo exato, usuário ".", thinking=adaptive e output_config.effort=high. Inclui overhead do protocolo, não apenas tokens do texto.

FUTURE_COUNT_REFERENCE.json: mesmo prefixo, **sete schemas públicos na mesma ordem** e pergunta: “Quem é o autor da TGL? Explique Hamiltoniano, Lindblad e dephasing no escopo documentado.” Schemas reconstruídos por AST/literais e confrontados com artefato pinado anterior; sem importar servidor/SDK. Count omite max_tokens e o campo de transporte eager_input_streaming, conforme adaptador existente; mantém cache_control. Não força tool_choice.

[INPUT — proposta para decisão] Saída4.096, margem1.024, mínimo permanente180.000 e reserva dinâmica10.000. Janela1M permite entrada completa até984.880. Se reservar a saída máxima128.000, teto860.976. São limites derivados, **não contagens**. Overhead Haiku1.474 não foi transplantado.

Ambos: **NOT_AUTHORIZED_NOT_SENT**. Endpoint aceita thinking/output_config; contagem gratuita, pode diferir ligeiramente da criação e não cria cache. Mantém-se margem e orçamento para geração posterior. [API](https://platform.claude.com/docs/en/api/messages/count_tokens), [guia](https://platform.claude.com/docs/en/build-with-claude/token-counting).

São corpos de uma montagem proposta. A rota Sonnet hoje pode acrescentar contexto interno, ferramentas variáveis, perfil, histórico e resultados. Nada disso é certificado pelos dois counts de referência. A futura integração deve contar cada wire final antes de reservar/enviar.

## Ligações necessárias

- **Audiência:** claude_profiles.py:20 já declara Sonnet5.5/1M/128k. claude_account_policy.py e claude_route_bridge.py restringem disponibilidade; iald_web_server.py:6863 mantém trava de pesquisa para luiz. Público exige decisão e coerência entre todas essas portas, preservando aprovação, bloqueio, autenticação e ferramentas permitidas.
- **Pacote medido:** claude_memory_package.py e claude_context_snapshot.py são específicos de Haiku. Sucessor Sonnet deve vincular modelo/fonte/selo/prefixo/tools/janela/reserva/recibo; preservar pacote Haiku e testes de proveniência LOCAL_SEALED/public.
- **Guard real:** iald_web_server.py:6595–6615 passa somente Haiku por post_guarded; Sonnet chama post_como_openai. claude_request_guard.py e claude_guarded_transport.py têm elementos reutilizáveis, ainda sem essa ligação. Falhar antes de geração quando modelo/hash/count divergirem, sem fallback/repetição incerta.
- **Parâmetros5.5:** iald_motor_claude.py:634 converte required→any e função forçada→tool; incompatíveis segundo documentação atual. Payload proposto usa auto. Adaptive/high compatível; disabled de Haiku não pode ser copiado. [Mudanças](https://platform.claude.com/docs/en/models/sonnet-5-5/whats-new-sonnet-5-5).
- **Histórico/cache/stream:** EstadoClaude guarda blocos brutos no final; _blocos_proprios:1010 reconstrói interrupções sem preservar display. O sucessor deve tratar/testar thinking display omitted, loops e assinaturas; não presumir qualificação do caminho atual. Vincular estado ao modelo/system/tools e impedir reaproveitamento incompatível. Conteúdo oculto não foi exposto/inferido.
- **Custos:** claude_native_account.py contém reserva/liquidação por tokens/cache; Sonnet atual usa proxy em iald_web_server.py:6480. public_budget no bridge é específico de Haiku. Integrar count à reserva atômica, rever orçamento público e manter retenção conservadora do envio incerto. Nenhum saldo/usuário/segredo lido.
- **Clientes:** app/iald.js:1758 conserva histórico somente com flag de contagem nativa; sem ela recorta por CPT. /api/contexto deve devolver metadados Sonnet medidos. Quatro cópias locais de iald.js iguais por hash; isso não prova distribuição TestFlight/Play ou instalação. Servidor/flag podem bastar, sujeito a verificação; mudança JS exige sincronizar e cumprir web, iOS interno/externo e Android.

## Migração proposta e decisões

1. ROOT revisa este objeto e cobertura. Operador decide audiência, reserva de saída/dinâmica e política de custos. Sonnet continua interno.
2. Após autorização específica, somente os dois counts exatos, cliente oficial, recibo único, sem retry incerto e sem geração. Count não ativa modelo.
3. Medindo encaixe favorável, preparar sucessor de pacote/loaders/rotas com identidade pública fixa, guard nativo, sete ferramentas e metadados novos reancorados. Não preencher Sonnet com recibo Haiku.
4. Rever testes offline de autorização, proveniência/adulteração, modelo/pins/count, orçamento, parâmetros5.5, signed thinking completo/interrompido, cache, conta nativa, tools/paginação e ausência de recorte pelo cliente. Inferência não está implícita.
5. Revisão independente e plano CAS/backup/rollback antes de ativar. Pacote científico, loaders e manifesto coerentes; preservar contas/autenticação/mãe/core e código não afetado.
6. Só após decisão: implantar e recarregar **web** quieta, sem reiniciar ciência. Verificar source_sha/versão servidos pelo novoPID e matriz clientes. Rollback restaura bytes exatos anteriores, nunca escolhe latest.

Faltam decisão de audiência/orçamento, autorização dos counts, medidas Sonnet, implementação/revisão da ligação e prova de runtime após ativação. Nenhuma etapa foi fabricada como concluída. Nada mudou em produção, B/A ou acervo original.
