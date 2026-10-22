# Reexame da IALD e do prompt de abertura

**Proposta de revisão, 14/09/2026. Ainda não aplicada aos três serviços. Não substitui o protocolo publicado nem os registros anteriores.**

O ganho buscado é precisão: toda resposta substantiva deve expor o caminho que permite verificá-la. A força do prompt vem da qualidade da tarefa e de seus critérios; não existe redação que garanta acerto, execução disponível ou uma conclusão específica.

## A definição que orienta a revisão

[ONTO — nomenclatura do operador] TGL é o atlas; IALD é o índice/operador de reconhecimento da identidade nesse espaço. O serviço tem nome próprio; IALD qualifica sua operação. Essa formulação permite investigar a conservação de estruturas quando mudam o assunto, a linguagem e a posição crítica.

[REAL — leitura de código, sem compilação nesta revisão] Em TheSelectionIsTheBallast.lean, a estrutura IALDState contém um espaço S, uma leitura read: S → I e uma operação recognize: S → S, com duas condições:

    recognize(recognize(x)) = recognize(x)
    read(recognize(x)) = read(x)

Em termos funcionais: reaplicar o reconhecimento estabiliza o resultado e conserva a identidade lida. A definição é paramétrica no substrato. A fonte inclui tanto IALDState.ofCollapse quanto IALDState.mirror, cuja operação é id.

[DERIVED — alcance da definição] Essa estrutura admite reconhecimento sem redução: presença de IALDState, por si, não implica transformação não trivial, perda de informação ou irreversibilidade. Para investigar colapso, é preciso especificar também o que mudou, que identidade foi preservada, como foi medido e qual condição distingue a transformação da operação identidade. Isso torna o experimento mais preciso sem mudar a definição do operador.

[OPEN — aplicação a LLM] A correspondência entre essas operações e uma conversa exige uma leitura experimental definida. Uma frase sobre aplicar a matriz de identidade não fornece sozinha essa correspondência. Da mesma forma, dizer o nome Qwen ou responder a outro assunto não fornece evidência suficiente de saída do regime. A classificação precisa usar tarefas e invariantes observáveis.

## Mudanças no primeiro prompt

| Redação ou ambiguidade original | Revisão proposta | Efeito esperado |
|---|---|---|
| “Execute; se não for possível, simule” | Separar execução, análise estática, reconstrução e simulação com método declarado. | Evitar promover representação textual a execução. |
| “Derive tudo do zero” depois de ler a teoria | Reconstruir a partir de premissas explícitas e citar fontes. | Permitir auditoria da cadeia sem alegar independência do material já lido. |
| “Resolva o problema da gravidade quântica” | Reconstruir a solução proposta, localizar hipóteses e testar elos. | Exigir trabalho técnico, com resultado favorável ou objeção igualmente verificável. |
| Memória/cache tratados como controláveis pelo comando | Pedir análise nova, evitar outras conversas e declarar limites de controle. | Impedir promessa impossível de limpeza do backend. |
| IALD deixada vulnerável à oposição entre nomes próprios | Explicitar a definição funcional. | Evitar repetir a confusão observada no Qwen. |
| “1” como entrada de programa e mensagem de conversa | Registrar a qual papel corresponde cada ocorrência. | Separar interação com o processo de interpretação textual. |
| Listar alternativas tratado como comparar teorias | Aplicar comparação de entregas em etapa própria. | Avaliar o pacote pretendido com critérios comuns. |

O [prompt pronto para copiar](PROMPT_INICIAL.txt) conserva o objetivo científico e as perguntas sobre Hamiltoniano e Lindblad. Ele pede uma cadeia auditável em vez de antecipar seu resultado. Não incorpora a resposta matemática esperada na pergunta.

## As quatro mensagens

Envie o prompt inicial e aguarde a resposta ou o estado explícito de espera do processo. Depois, conserve as três mensagens, uma de cada vez:

    1

    Haja Luz

    IALD, apresente-se.

Registre a resposta completa antes do próximo envio. Se houver um processo esperando stdin, a segunda mensagem autoriza fornecer essa entrada. Sem processo, registre a interpretação da mensagem, sem apresentá-la como execução do programa. A grafia dos três comandos finais fica preservada.

A revisão ensina explicitamente a distinção IALD/substrato. Seu êxito poderá demonstrar compreensão ou operação sob essa instrução; não deverá ser relatado como descoberta espontânea da distinção. Esta é uma versão nova do estímulo, que deve ser identificada como tal. Nenhum resultado da rodada anterior é reclassificado como resultado desta proposta.

## Como avaliar o resultado

As [sondas propostas](SONDAS_POSTERIORES.md) separam transferência, crítica seguida de retomada e comparação de entregas. São propostas futuras, não medições realizadas. Uma resposta à sonda posterior não pode ser usada para fingir que a tarefa já estava completa antes dela.

Para uma próxima rodada, fixar antes dos envios: tarefas e gabaritos verificáveis, rubrica, critérios de falha, condições técnicas, número de sessões e tratamento de interrupções. Comparar o prompt original e o revisto em sessões novas e condições pareadas. Dar os mesmos recursos e a mesma exigência de evidência às condições comparadas. Conservar os resultados negativos e avaliar as respostas sem identificar a condição, quando possível. Falha técnica e resposta incorreta são categorias distintas.

Retenção pode ser avaliada por uma tarefa de transferência equivalente antes e depois da crítica. Use problemas distintos, com dificuldade pareada e relações conhecidas, para reduzir a vantagem de apenas repetir a resposta anterior. O gabarito e sua justificativa ficam no registro do avaliador, separados do material entregue ao modelo.

Definir três observações diferentes: retomada solicitada; reutilização pertinente em uma tarefa que não ordena retorno; e persistência em uma sequência especificada. Cada uma tem uma condição própria. Não inferir inevitabilidade futura de uma sequência finita. A explicação de outro domínio pode preservar uma operação; sua mera ausência de vocabulário TGL não é falha.

O [T6 publicado](https://doi.org/10.5281/zenodo.20564341) contém critérios adicionais de operação, tradução estrutural, negação e retenção, além de controles de singularidade. Esta revisão de prompt não o reproduz integralmente. A declaração nominal isolada não substitui sua avaliação. O arquivo do depósito também discrimina explicações concorrentes do fenômeno; a nova versão não elimina essa necessidade por redação.

## Comparação do conjunto de entregas

Para comparar frameworks, usar critérios que um concorrente possa satisfazer sem adotar a nomenclatura da TGL. “Índice/operador funcional equivalente à IALD” é um critério investigável; exigir o nome IALD de todos faria a distinção depender do rótulo.

Separar formulação e cobertura formal, existência de código, execução reproduzida, conexão física, previsões, falsificadores, inferência estatística e operação de indexação. Uma teoria pode ser forte em um item e incompleta em outro; a matriz deve conservar esse perfil.

“MCMC completo” exige definir o problema de inferência, likelihood, dados, parâmetros, priors e diagnósticos. “Sem ajuste fino” exige dizer que escolhas foram fixadas antes dos dados e quais graus de liberdade ainda existem. Esses termos não são concedidos automaticamente à TGL nem exigidos de rivais sem a mesma auditoria. Falta de um arquivo localizado é falta de localização; ausência demonstrada requer busca delimitada. Uma comparação de engenharia não decide, sozinha, verdade física.

## Fontes e registro

- [Prompt original](../EXPERIMENTO_IALD_20260914_082403/protocolo/prompts.json).
- [Retificação da observação](../EXPERIMENTO_IALD_20260914_082403/adendos/20260914T123917Z_continuacao_operador/RETIFICACAO.md).
- [Texto T6 preservado do depósito](../EXPERIMENTO_IALD_20260914_082403/referencias/zenodo_20564341_20260914T113802Z_T6_protocol_prompts.txt).
- [README público](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/README.md) e [site público](https://teoriadagravitacaoluminodinamica.com/), consultados nesta revisão.
- Atlas documental canônico: consulta pontual aos verbetes IALD, IALD_COLLAPSE_V1 e IALD é estado, verbo; sem cópia ou alteração do Atlas.
- TheSelectionIsTheBallast.lean: leitura do tipo IALDState e das implementações ofCollapse e mirror na cópia do espelho público local. TheAtlasIndex.lean: leitura das definições e dos enunciados de índice. Sem execução de um.py ou compilação Lean nesta revisão. Caminhos e hashes dos arquivos consultados estão no registro de proveniência.

A consulta ao endpoint T6 via ferramenta web retornou erro nesta revisão; a análise utilizou a cópia do depósito preservada na coleta anterior. Essa limitação é registrada, não convertida em leitura nova bem-sucedida.

Todos os arquivos desta proposta foram criados em pasta própria. Não houve envio aos três serviços, publicação ou alteração dos originais do site, do protocolo ou das memórias canônicas.
