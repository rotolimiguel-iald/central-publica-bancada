# Revisões V4 — aproveitamento crítico

27/09/2026. Kimi: request e670c4d3-67d3-4f00-8911-237d1afe9a89, job 55c5db0e-a5dc-4758-b8a7-c2447b66c3ba. MiMo: request 55737f44-fb07-4c3c-aead-21a435bf1c21, job 4c40e941-fc31-4bd9-9527-97855edfcecd. Ambos result_ready, conferidos nos arquivos result.json. Pareceres são DECLARADO e não executaram os testes locais.

## Incorporado

- Arrays completos em processo persistente, propriedade/imutabilidade, orçamento pela memória disponível, RSS e swap visíveis.
- N/N e erro explícito; PARTIAL não vira READY. Fontes fechadas após leitura; teste continua navegando depois de remover somente a fixture.
- Tempo GPU em coordenada normalizada da janela, jamais GPS absoluto float32.
- Envelopes mínimo/máximo de todos os pontos da janela; cobertura por bin e gaps; não usados como espectro.
- Relógio explícito, hipóteses das leituras preservadas, modelo existente com hash, GR de controle e relação de redshift.
- Manifesto por carga, geração, identificadores de requisição; respostas obsoletas separadas.
- Plano por domínio e reprodução dos executores, com controles e ensaios múltiplos antes de significância.

## Não adotado / corrigido

- MiMo sugeriu memmap como alternativa a RAM: não cumpre a carga integral pedida; não usado.
- MiMo sugeriu descartar silenciosamente duplicatas por hash parcial: recusado. Impressão parcial só sugere igualdade; os caminhos continuam identificados e não são tratados como evidência independente.
- A pendência de localizar a fórmula de tempo foi superada pela auditoria local TIME_SOURCE_AUDIT.md. Isso não converte automaticamente índice modular em segundos nem escolhe tau*.
- Kimi sugeriu tornar obrigatório transporte binário: mantido JSON limitado a envelopes/curvas, sem transferir arrays completos. Mediremos latência antes de substituir o transporte; não é uma lei de arquitetura.
- FDR não é, por si, probabilidade global de falso positivo de 5sigma; contagem de testes não é automaticamente N efetivo. Nenhum limiar estatístico sugerido entrou no motor sem o protocolo correspondente.
- Fórmulas de outros domínios mencionadas pelo MiMo são localizadores a conferir, não física implementada. Tempos fonte/detector são intervalos relativos, não divisão do timestamp GPS absoluto por 1+z.

## Próximo após U1/U2

Integrar evento/PSD/DQ/antena/posteriores e likelihoods existentes. Medir desempenho, concorrência e integridade; LOD hierárquico/binário só se os números exigirem. Todos os dados de domínio residentes não significam todos os repositórios ou todos os domínios tratados.
