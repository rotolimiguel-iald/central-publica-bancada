# Revisão independente — fechamento do delta APP-01

[REAL — inspeção local de bytes/AST] APP-01 está corrigido. O suplemento foi examinado sem instalar, importar ou executar o candidato, os testes ou os provedores. O manifesto permaneceu estável entre a abertura e o fechamento; os onze vínculos de membros, backup, manifesto original, prefixo e COUNT_PLAN conferiram.

A atribuição de '_verified_source_scope' ocorre somente depois da validação completa de '_load'. 'search' e 'fetch' recarregam esse estado validado; a busca retorna LOCAL_SEALED_DOCUMENTS ou PUBLISHED_DOCUMENTS, informa source_scope no envelope e em cada resultado, e conserva a distinção mesmo sem resultados. 'fetch' acrescenta a proveniência ao documento. Falhas de leitura/validação propagam; nenhuma exceção passa a sucesso.

[REAL — comparação estática] Mudaram somente '_load', 'search' e 'fetch'. 'context' e as definições das ferramentas têm AST idêntica. Prefixo e COUNT_PLAN continuam com os bytes pinados. [DECLARADO — ensaio do autor conferido por fonte/recibo] Os 30 testes locais passaram, incluindo os oito casos do delta; o autor mediu igualdade do contexto e metadados. Não repeti esses testes. Os sete esquemas do payload de contagem permanecem como no pacote original revisado; não foi produzido outro payload remoto nesta revisão.

O plano sucessor conserva 1.239 entradas e troca somente a origem/hash/tamanho de 'iald_core_indexado.py', com destino e baseline iguais. O campo suplementar identifica a correção. O finalizador mudou apenas a raiz, a localização do plano sucessor e o caminho de import local necessário: conserva contagem efetiva, conferência do prefixo, limites, baselines e manifesto por último. Não instala por si e mantém a revisão final ROOT. Nenhum arquivo de contas, autenticação, modelos ou limites foi incluído pelo delta.

[DERIVED — decisão de engenharia] Aceite da PREPARAÇÃO ESTÁTICA do pacote original mais suplemento APP-01. Não há bloqueador concreto restante neste delta. A alternativa A escolhida preserva o regime público e explicita o snapshot local; a alternativa B de um rótulo neutro seria possível, mas não é necessária.

Permanecem qualificações documentais não bloqueantes já registradas: APP-02 conserva um texto genérico histórico no 'method', enquanto a fonte específica tem proveniência LOCAL_SEALED sem commit/URL fictícios. APP-03 conserva a projeção compacta e a referência ao recálculo: afirmações de precisão/convergência exigem a fonte integral. A descrição genérica antiga da ferramenta não suplanta a proveniência concreta agora devolvida.

[OPEN — entrega operacional] Este aceite não autoriza contagem, instalação, ativação, reload nem declara v388 carregada em produção. A contagem nativa continua dependente da autorização específica antes recusada e de recibo efetivo; não a executei. Após ela, ROOT ainda deve conferir o plano final e a versão efetivamente carregada. O snapshot científico aprovado é v388 selado, sem absorção automática do drift do 'um.py' vivo.

Nenhum arquivo do autor ou produção foi alterado. O mapa MCP não foi chamado, preservando a recusa anterior; ROOT coordena a memória compartilhada. Evidência detalhada: EVIDENCIA_DELTA_APP01.json. O parecer inicial é preservado como história do achado.
