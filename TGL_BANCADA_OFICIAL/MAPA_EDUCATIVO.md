# Universo: mapa livre e percurso guiado

Entrada local: http://127.0.0.1:18766/explore. O atalho TGL passa a abrir essa página quando o serviço Cosmos estiver disponível, preservando a abertura do laboratório GW como alternativa se Cosmos falhar.

## Experiência

Oito temas conectam composição, evolução e observação: matéria bariônica, matéria escura, energia escura, CMB, expansão, estruturas, BAO e ondas gravitacionais. É possível escolher qualquer tema ou usar Anterior/Próximo no percurso guiado. Marcar um tema como lido é uma ação explícita; a leitura não é presumida por uma visita. O progresso fica neste navegador, com mensagem visível quando o armazenamento falhar.

Cada tema apresenta uma explicação, uma pergunta de pesquisa, o que observar, uma experiência, a ligação possível à TGL, disponibilidade do laboratório e fontes primárias. Os links levam aos executores existentes; nenhum resultado é recalculado por uma segunda implementação da TGL.

## Experiência didática calculada

O gráfico de composição e o histórico usam um modelo FLRW plano independente, com bárions e matéria escura fria não relativísticos, radiação idealizada e constante cosmológica. As entradas são Ωb, Ωc e Ωr atuais; ΩΛ fecha a soma. As frações na época selecionada são densidades normalizadas por sua soma. São frações de densidade, não fatias espaciais.

E²(z) = (Ωb + Ωc)(1+z)³ + Ωr(1+z)⁴ + ΩΛ.

Parâmetros iniciais arredondados para ensino; não são um posterior Planck, ajuste ou previsão TGL. Radiação idealizada não modela transições de espécies massivas. O domínio didático é 0 ≤ z ≤ 100000; z é redshift, não idade ou tempo de reprodução. O marcador z≈1100 localiza uma referência educativa, sem calcular a recombinação. Valores inválidos produzem erro visível e esmaecem o último gráfico válido.

Este modelo não altera os parâmetros, fontes, estado ou geração do motor V3 de pesquisa. A matéria agregada do V3 não foi convertida artificialmente em um cálculo de matéria bariônica e escura separadas.

## Laboratórios relacionados

- `/cosmos`: distâncias BAO, covariância, comparações e cenários do executor V3 condicional existente; domínio de pesquisa z≤3, rd como entrada.
- `http://127.0.0.1:18765/universe`: sinais e cenários de ondas gravitacionais; conserva o worker residente.
- CMB em mapas/espectros, lentes, catálogos 3D e simulações de formação são temas educativos, ainda sem seus produtos científicos integrados a esta entrada.

As fontes estão em `static/cosmos-lessons.js` e `EDUCACAO_FONTES.md`. Textos e desenhos didáticos não são produtos observacionais. O SVG do diagrama calcula relações; a renderização GPU dos laboratórios existentes permanece disponível. Nenhum novo experimento, ajuste, significância estatística ou mudança do gate resulta da navegação.

## Validação e operação

`node --test tests/test_cosmos_teaching.cjs` verifica conservação das frações, leis de escala, regimes, limites, discretização e entradas inválidas. Os testes HTTP e launcher conferem rotas, MIME, caminhos restritos, mutex e alternativa GW. A UI é conferida no navegador, incluindo percurso, persistência, redshift, composição inválida e navegação.

Somente o serviço Cosmos precisa reiniciar para novas rotas. Não reiniciar o serviço principal GW para essa entrega. Scripts de registro usam backup imediato byte a byte e append atômico das memórias próprias.
