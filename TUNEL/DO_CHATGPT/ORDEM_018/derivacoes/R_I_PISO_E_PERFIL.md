# R-I — piso dos vazios e forma do perfil
[REAL da leitura documental / DERIVED na distinção matemática / OPEN no perfil predito] 06/10/2026 UTC. Autor: chatgpt-codex/ordem-018/derivacoes.

**Nas funções canônicas examinadas, o piso fixa uma desigualdade para a densidade média total no núcleo; não determina uma forma radial nem uma distribuição de perfis.** Há templates de perfil na instrumentação do teste, porém identificados como externos e acrescidos de um piso imposto. Não foram propostos novos estatísticos de perfil, abertos dados ou repetidos ritos.

## Consulta do mapa e falha de índice
A consulta oficial precedeu o exame. A rota vazios.piso.cadeia_v78_v92 tem título sobre a cadeia do piso e campo onde apontando a prove_void_floor_v41_calibrated, mas a nota do seq158 trata de prove_neff_channel, prove_rho_plus_p_closure e N_eff. Isso é uma **incongruência documental de escopo no registro** [REAL da leitura]. Não foi identificada aqui sua causa, nem para onde o texto deveria ser transferido.

Consequência limitada: essa nota não sustenta a cronologia v78→v92 do piso. Ela tampouco refuta ou confirma a previsão do piso. A cadeia histórica permanece por verificar no recorte próprio; nenhuma conclusão sobre N_eff foi transportada aos vazios. A correção no mapa é ao lado, preservando o seq158.

A rota vazios.piso.v11, seq3 com anotações75/83/84 e errata82, registra limitações anteriores do desenho e da leitura do traçador. Foram reconhecidas para não repetir o rito; suas contas não foram refeitas. Os registros não foram tratados como evidência de uma distribuição radial.

## Fontes primárias nomeadas e alcance
O hash do um.py e os recortes literais com linhas foram lidos por script em R_I_FONTES_E_TRECHOS.json. Só foram examinadas funções nomeadas do piso e seus templates pertinentes, sem importação/execução. O verbete “Piso dos vazios” do Atlas foi consultado como índice com remissão, não como substituto da fonte.

| Função/trecho do um.py | O que efetivamente especifica | Alcance |
|---|---|---|
| prove_void_floor_margin,2652–2671 | prediction: rho_void/rho_bar >= beta; perfil empilhado como via de estimação; mínimo típico de literatura marcado EXT | A palavra perfil nomeia o estimador/endereço; não aparece uma função radial derivada de beta. |
| _void_floor_protocol_record,145363–145413 | central_total_matter_density_ratio; núcleo x_c=0,25; densidade total e reconstrução por lente; galaxy_density_only_is_not_matter_density | Limite da quantidade central média, não equação de forma. |
| prove_void_floor_protocol,145525–145533 | Define expressamente r_v como densidade TOTAL média no quarto central dividida pela média no mesmo z | Não autoriza trocar média volumétrica por densidade pontual. |
| evaluate_void_floor_test,145416–145441 | Compara limite superior corrigido por família com beta e usa controle/poder como entradas | Avaliador da desigualdade; não fornece gerador de perfis ou probabilidade própria da TGL. |
| prove_void_floor_power_pilot,145540–145558/145618–145623 | Mock LCDM lognormal de densidades centrais, calibrado externamente; mock TGL com piso IMPOSTO | Distribuição auxiliar de piloto, não derivação da distribuição TGL a partir do piso. |
| prove_void_floor_v3_kappa,146317–146345/146442–146457 | Modelo HSW explicitamente EXT, parâmetros delta_c e s1 perfilados; prof = maximum(prof,rstar) antes da projeção | Shape importado mais truncamento; não uma lei radial fixada por beta. |
| prove_void_floor_v41_calibrated,147679–147715/147790–147855 | Conta dentro de Rc=x_c Rv, divide contagem por volume e calibra pela referência aleatória | Razão escalar do núcleo; a calibração de contagem não cria previsão de perfil de matéria. |
| prove_void_floor_v11_sdss_independent,151587–151645 | Herda estimador V4.1; canal de traçador unilateral, matéria bilateral por shear/kappa | Reconstrução/observação e previsão continuam objetos distintos. |

O uso de perfis auxiliares pode sustentar um teste **condicional** às hipóteses do template, seleção e calibração. Não transforma a escolha do template em consequência da desigualdade. Não se julgou novamente o veredito histórico, nem o fundamento completo da derivação do piso.

## O objeto matemático que o piso restringe
Defina f_i(x,z)=rho_i(x Rv,z)/rhobar(z), com x=r/Rv, como perfil radial médio angular de matéria de um vazio já definido. Para uma média esférica volumétrica, o núcleo da fonte corresponde ao funcional
T_c[f_i] = (3/x_c^3) integral_0^x_c f_i(x,z) x^2 dx, com x_c=0,25.
Esta fórmula explicita o significado de densidade média no núcleo; **não é uma proposta de novo estatístico nem de forma radial**. Na análise de conjuntos, a ponderação entre vazios e a seleção ainda precisam permanecer as do protocolo.

O piso operacional impõe T_c[f_i] >= beta, onde beta=alpha_CODATA2018 sqrt(e) em runtime. A desigualdade não impõe T_c=beta, f_i(0)=beta, saturação do piso, inclinação, curvatura, parede de compensação, raio de transição ou dependência em redshift.

[DERIVED] Um único funcional integral limitado inferiormente não determina seus integrandos. Mesmo se o piso fosse adicionalmente imposto ponto a ponto, f_i(x,z)>=beta, isso só restringiria o conjunto admissível: continuariam livres a variação radial e a distribuição entre objetos. A condição média da fonte, por si, não implica essa condição pontual mais forte.

Se Y=T_c[f] for tratado como variável latente de uma população à qual se aplica universalmente o piso, a consequência é P(Y<beta)=0 no nível físico ideal. Não se obtém P(Y<=y) para y>=beta, nem média/variância, abundância perto do piso ou covariância entre raios. Ruído de reconstrução não tem suporte necessariamente igual ao de Y. O limite permanece uma previsão falsificável; sua força não é uma especificação da população inteira.

## Duas leituras avaliadas, sem medir novamente
1. **Piso como desigualdade:** conserva apenas o conjunto de perfis admitidos pelo limite central. Esta é a informação explícita da prediction e do avaliador lidos.
2. **Piso mais template externo:** escolhe um perfil HSW ou uma lei de densidades centrais e aplica clipping. A fonte marca a forma como EXT/auxiliar; portanto há premissas além do piso. Não foram selecionados novos parâmetros, formas ou famílias.

O fato algébrico do clipping também delimita seu alcance: se uma entrada já satisfaz f>=beta em todo ponto, max(f,beta)=f. Logo impor o piso não garante uma diferença de forma em relação a todo perfil concorrente. Isso é uma identidade da operação, não execução do template, análise de dados ou veredito.

## Objeto faltante e decisão sobre estatísticos
Para prever um perfil distinto seria necessário localizar ou derivar **ao menos um** destes objetos, com domínio e condições declarados:
- uma solução radial F_beta(x;Rv,z,ambiente) de equações de evolução/fechamento e condições iniciais/de contorno que a tornem determinada; ou
- uma lei de probabilidade Pi_beta[df | Rv,z,seleção] sobre perfis, que fixe ao menos a expectativa funcional e a dispersão necessárias ao contraste escolhido.

Em qualquer caso, a ligação aos observáveis requer também o operador declarado de matéria→lenteamento/traçador, sua janela/projeção e os parâmetros auxiliares admissíveis. Uma previsão concorrente e a mesma definição de vazio devem permitir um contraste que sobreviva a essas liberdades. Esses objetos não foram encontrados como derivados nas funções restritas examinadas; a afirmação não é uma busca exaustiva de todo o acervo.

**Estatísticos novos de perfil propostos: zero.** Não há aqui uma forma TGL distinta sustentada a partir apenas do piso para justificar a escolha de um filtro, inclinação ou contraste entre raios. O teste de violação do piso já registrado é preservado; não será renomeado como novo teste de perfil. A tarefa útil seguinte é explicitar o objeto matemático faltante antes de propor estatístico ou abrir dados.

## Registro e limites da entrega
Sem cálculo de beta numérico, simulação, fit, consulta a catálogo, novo poder, rito ou chamada de executor. Somente leitura de código/índice e derivação funcional; não houve execução de um.py, abertura de caches observacionais ou alteração de originais, kernel ou gate. Os números e resultados históricos presentes no texto-fonte foram lidos como documentação, não recalculados nem usados como novo veredito.

R_I_MAPAS_ANTES.json guarda o extrato identificado das rotas consultadas. R_I_FONTES_E_TRECHOS.json traz hashes atuais, linhas e recortes. R_I_PISO_E_PERFIL.md é esta nota. O recibo e o manifesto R-I guardam a correção do índice e a anotação de escopo ao mapa. A incorporação às memórias centrais cabe à coordenação/gerência, com o estatuto OPEN do perfil preservado.
