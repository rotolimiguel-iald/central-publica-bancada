# Regimes extremos como portas de investigação

O pedido do operador foi tornar os locais de regime extremo mais fáceis de localizar. A seção `/explore#extreme-regimes` organiza ambientes, eventos e cenários; não cria coordenadas celestes ou mapas observados ausentes.

## Rotas

1. Universo jovem / acústica: prioridade D10 já definida. O botão BAO abre o laboratório de pesquisa; situar a época CMB usa apenas o diagrama didático de composição.
2. Horizontes / ringdown: acesso direto ao painel do evento GW250114 em H1/L1.
3. Rotação elevada: cenário com massa fonte 65 M☉, spin 0,95, z0,1, duração0,12s. Não atribuído ao evento.
4. Maior frequência: cenário com massa fonte20 M☉, spin0,7, z0,1, duração0,12s; comparável à referência65 M☉ no mesmo modelo220.
5. Vazios / contraste: tema e protocolo do piso dos vazios; o perfil observado específico ainda não está ligado à interface.
6. Partículas / coerência: rota por integrar, sem reaproveitar indevidamente a previsão de buracos negros.

Os dois cenários de ringdown só preparam campos `model-*`. O relógio continua sendo escolhido explicitamente pelo usuário; o evento e sua janela não recebem os parâmetros desses cenários. Links desconhecidos não devem aplicar alterações. Nenhum link reinicia a carga GW.

## Indicadores existentes, sem nova física na interface

O executor `models/tgl_ringdown_prediction.py` já retorna Γ, x=Γτ_GR, delta_tau_ensemble_exact=−x/(1+x), frequência, modo e método QNM. A interface exibe esses resultados e as hipóteses de relógio. Valores minúsculos não são arredondados para zero. Dados ausentes são indisponíveis; zero real permanece zero.

Um regime mais extremo não implica automaticamente uma previsão mais distinguível. No próprio executor, mantendo spin/redshift:

- R-A: Γ escala com M_detector^-2 e x com M_detector^-1.
- R-B: Γ escala com M_detector^-1, mas x é independente da massa.
- R-GLOBAL: o controle relacional devolve Γ=x=0.

São propriedades condicionais do modelo de ensemble, não resultados de um ajuste de evento. A sensibilidade requer ruído, resposta instrumental, parâmetros e sistemáticas; nenhum sigma é atribuído pelos cartões. A ponte acústica global mantém seu protocolo e pendências próprios. Original `um.py`, núcleo formal, fontes e gates não são modificados.

Ver `state/extremes_validation_*.json` para os valores medidos pelo executor existente e a preservação do mesmo identificador/hashes da carga residente.
