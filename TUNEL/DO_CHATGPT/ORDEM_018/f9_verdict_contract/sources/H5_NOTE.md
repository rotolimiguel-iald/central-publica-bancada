# Fase 9 — especificação do rival de fundo e escalas acústicas

[REAL documental / DERIVED / OPEN] O quinto rival ainda não está definido para execução. A proposta `r_d livre` precisa dizer o que acontece com o horizonte no desacoplamento, com a compressão CMB e com a medida comum usada nas evidências. Esta nota não escolhe modelo físico, não muda o V1 e não calcula ajuste.

## Duas escalas presentes no instrumento histórico

O código independente `T4_reproduzir.py`, linhas100–101, conserva duas quantidades da tabela CAMB: BAO divide DM, DH ou DV por `r_drag`; o vetor CMB usa R=sqrt(Omega_m) H0 DM_star/c, lA=pi DM_star/r_star e omega_b. Portanto r_drag e r_star não são nomes intercambiáveis. Ambos foram obtidos sob o mesmo modelo de fundo tabelado; nenhum deles é uma observação direta independente do CMB.

[KNOWN] Chen, Huang e Wang definem lA com o horizonte no desacoplamento e verificam sua compressão em LCDM, wCDM e CPL. Esse recorte de validação não demonstra automaticamente validade para uma alteração arbitrária do horizonte primordial. [Fonte primária, equações1–3 e resumo](https://arxiv.org/html/1808.05724).

[KNOWN] Zhai et al. mostram que a compressão depende de hipóteses do modelo; ao variar parâmetros de neutrinos, ampliar o vetor com omega_c e Neff foi necessário nos casos examinados. Isso não é uma certificação nem uma proibição universal de outros modelos. [Resumo primário](https://arxiv.org/abs/1912.04921).

As duas páginas foram arquivadas integralmente por GET e hash em `SOURCES.json`. O HTML de Chen foi convertido posteriormente ao artigo; a data de conversão não foi tratada como data da publicação original. A leitura dessas fontes contém números publicados, mas nenhum deles foi usado para escolher prior ou calcular evidência nesta unidade.

## Alternativas explícitas para decisão científica

**A — fator fenomenológico apenas na régua BAO.** Definir r_d^eff=q_d r_d^CAMB(theta), com q_d>0 e prior normalizado próprio. Usar DM/r_d^eff, DH/r_d^eff, DV/r_d^eff no mesmo vetor BAO. CMB continua com r_star e DM_star padrão, e a rede local usa H0, sem fator K. Isso cria um rival estatístico preciso de inconsistência entre réguas, com os mesmos dados; não implementa EDE nem autoriza chamar H0 de completamente livre, pois o bloco CMB ainda o restringe. O modelo adicional não nasce da mera troca de uma variável no código: a compressão e o estatuto fenomenológico precisam ser aceitos antes do composto.

**B — alteração primordial física.** Escolher uma dinâmica concreta que compute H(a), recombinação, z_star/z_drag, ambos os horizontes e, quando necessário, perturbações. Então usar a likelihood CMB completa ou uma compressão especificamente qualificada para esse domínio, com os mesmos dados observacionais na comparação. Libertar dois números acústicos sem essa dinâmica seria outra extensão fenomenológica, não a realização física da alternativa. Nenhum modelo primordial foi selecionado nesta nota.

**C — quinto rival apenas de uma discrepância de calibração de fundo.** Se o modelo multiplica somente H0_local=b exp(eta), enquanto o restante depende de theta como no diagnóstico beta livre, eta=I(theta) beta é uma reparametrização. Com I não zero no domínio, o Jacobiano condicional e o domínio transformado precisam acompanhar o prior. Essa alternativa não acrescenta uma assinatura de dados à de beta livre, mesmo que o nome mude. Só alteraria a evidência por um prior diferente se este fosse escolhido explicitamente. Não é uma quinta explicação identificável por si só.

Uma análise auxiliar sem CMB também é possível, desde que TODOS os modelos dessa comparação usem exatamente o mesmo conjunto reduzido. O Bayes factor desse experimento auxiliar não pode ser colocado na mesma tabela como se fosse evidência calculada sobre o conjunto CMB+BAO+rede. Nenhuma alternativa foi adotada por esta preparação.

## Prior: r_d livre não equivale automaticamente a q_d livre

[DERIVED] Para theta fixo, r_d=q_d r_d^CAMB(theta). Se se preservar a proposta anterior r_d uniforme em[130,160] Mpc, então o suporte de q_d é[130/r_d^CAMB(theta),160/r_d^CAMB(theta)] e sua densidade condicional é r_d^CAMB(theta)/30. Um prior uniforme em q_d com limites fixos seria outro prior conjunto. A dependência em theta impede transformar só os limites no melhor ajuste e reutilizá-los em toda a integral. Este cálculo é mudança de variáveis, sem escolha de valores observados ou adoção desse prior.

## Condições para tornar a proposta executável

- Escolher uma das interpretações e nomeá-la exatamente pelo que prevê.
- Fixar vetor de observações, fatores de likelihood e respostas locais comuns aos cinco modelos; nenhuma duplicação de Planck/BAO/escada.
- Verificar se a compressão CMB admite o domínio proposto; quando não qualificada, manter o resultado condicional explícito ou empregar o instrumento apropriado.
- Fixar prior conjunto normalizado, domínio, mapeamento de escalas e nuisance; transportar todos os Jacobianos.
- Conferir identidades/nesting em controles sintéticos antes de solicitar abertura para veredito.

[OPEN] Não foi localizada nesta preparação uma ratificação do quinto rival, do prior ou da compressão para a extensão. Isso não prova ausência de uma solução no acervo. A ambiguidade foi convertida em opções revisáveis, sem declarar parede. A reprodução histórica T4/P45 conserva seus contratos e não foi alterada.
