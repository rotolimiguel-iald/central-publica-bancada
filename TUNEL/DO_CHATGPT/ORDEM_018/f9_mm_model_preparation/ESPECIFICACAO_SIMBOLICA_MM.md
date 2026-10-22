# F9 — os cinco termos MM: contrato estatístico e propagação

Pedido `98a42877-3879-43a7-841c-8bb662be3d06`, 06/10/2026. Preparação documental/simbólica para ROOT, sem ratificação. O script de custódia confere os pins das fontes admitidas e exporta somente identidades, erros autorizados, configurações e fórmulas; nenhum catálogo bruto é aberto.

## 1. Duas alternativas, antes de escolher a preparação

**A — experimento gaussiano de trabalho com erros publicados fixados.** Manter exatamente a transformação e a receita de erros upstream, congelar suas escalas de referência e explicitar uma lei gaussiana comum aos cinco modelos. É a opção mais diretamente implementável na arquitetura linear existente. Sua cota é válida no experimento estipulado quando suas hipóteses são satisfeitas; não demonstra cobertura para o estimador físico original.

**B — distribuição primitiva e transformação não linear.** Especificar a lei conjunta de distâncias, velocidades corrigidas e calibração, inclusive assimetrias/dependências, e transportar essa lei. Tem maior fidelidade potencial ao processo de medição, mas erros marginais e nomes de galáxias não determinam essa distribuição. Pode exigir nova calibração de caudas; não herda automaticamente a cota gaussiana já derivada.

**Recomendação concreta:** preparar A, fiel à receita upstream e explicitamente rotulada como experimento de trabalho condicional. Manter B como alternativa especificada, sem inserir sua derivada completa ou novos parâmetros na receita A. A escolha científica continua não ratificada. Nenhum dos cinco modelos, das267linhas locais, dos priors, de alpha, da exclusão de MM ou da abertura sob§6 é alterado por esta unidade.

## 2. Identidade das cinco linhas e fontes

**[REAL — metadados/código]** As identidades provêm de `METADADOS_ERROS_NAO_ESTELARES_V01.json`, cruzadas com `ESPECIFICACAO_LINEAR.json`. O arquivo `megamaser.dat` não foi reaberto. As larguras abaixo são copiadas de metadados já admitidos; não são valores centrais nem novas estimativas.

| Termo | Identidade | ID estável | Largura inferior D(Mpc) | Superior D(Mpc) | s_D upstream(Mpc) | s_v publicado(km/s) |
|---|---|---|---:|---:|---:|---:|
| MM1 | UGC_3789 | data/megamaser.dat:L5 | −4,0 | +4,5 | 4,25 | 0,8 |
| MM2 | NGC_6264 | data/megamaser.dat:L6 | −17 | +21 | 19 | 0,8 |
| MM3 | NGC_6323 | data/megamaser.dat:L7 | −23 | +34 | 28,5 | 1,5 |
| MM4 | NGC_5765b | data/megamaser.dat:L8 | −5,1 | +5,4 | 5,25 | 0,7 |
| MM5 | CGCG_074-064 | data/megamaser.dat:L9 | −7,2 | +7,9 | 7,55 | 1,9 |

N4258 permanece âncora da rede; não entra como sexto maser de fluxo. Em cada linha nativa, `X_i=0`, `a_h,i=1`, `c_C,i=0`: a média é o mesmo h do modelo físico já escolhido, sem nuisance próprio de galáxia. A escala de magnitude discutida abaixo transforma esses coeficientes junto com os dados.

Fontes de implementação, verificadas por SHA256: `data_loader.py:528–592` (especialmente559–585), `equations.py:324,630–643`; a notação linear está no projeto já pinado. `intercept.py:53–74` contém outro fator cosmográfico, do intercepto SN: não substituir o fator MM por ele por semelhança de nome. Os caminhos, hashes e trechos exatos constam de `FONTES_E_FORMULAS.json`.

Configuração admitida: `mm_dz=True`, correção `2M++`, q0=−0,55, j0=1 e orçamento `vpec_error=240 km/s`. São configurações fixadas da redução upstream, não parâmetros novos ajustados nesta unidade. O valor240 é um orçamento da receita, não prova de uma dispersão populacional medida. A derivação não troca a convenção `z=v_corr/c` pela conversão relativística usada em outros setores.

## 3. Transformação e variâncias upstream: especificação executável em símbolos

Defina, para cada uma das cinco linhas:

\[
\ell=\ln10,\quad z_i=v_i/c,\quad A=(q_0+3)/2,\quad B=(11+7q_0+3q_0^2-j_0)/6,
\]
\[
F(z)=1-Az+Bz^2,\qquad U(v)=vF(v/c).
\]

Aqui D_i é a distância em Mpc e v_i a coluna de velocidade corrigida2M++ em km/s. **Ambos os valores centrais permanecem não interpretados/não expostos nesta unidade.** Com D_unit=1Mpc, v_unit=1km/s e H_unit=v_unit/D_unit:

\[
y_i=\log_{10}\!\left[\frac{U(v_i)/v_{unit}}{D_i/D_{unit}}\right],
\qquad h=\log_{10}(H_0/H_{unit}).
\]

Isso é a redução algébrica exata de `cz_term−0.2*mu+5`, com `mu=5 log10(D/Mpc)+25`. Não foi calculado nenhum y_i. Exige D_i>0 e U(v_i)>0; falha não autoriza descartar a galáxia ou substituir seus campos.

Escreva d_i^- e d_i^+ para os módulos das duas larguras de distância e s_i para o erro de velocidade publicado. A receita efetivamente implementada é

\[
\bar s_{D,i}=\frac{d_i^-+d_i^+}{2},\quad
s_{V,i}^2=s_i^2+s_{pec}^2,\quad
V_i^{up}=\frac1{\ell^2}\left[\frac{\bar s_{D,i}^2}{D_i^2}+\frac{s_i^2+s_{pec}^2}{v_i^2}\right].
\]

**[REAL na fonte]** Os valores de s_D da tabela já estavam nos metadados; não foram recalculados de catálogos. `equations.py` inicia C em zero e preenche esses cinco elementos diagonais com `logh_error**2`. A independência assim representada é uma hipótese de trabalho do código, não uma medição de todas as correlações reais.

As cinco expressões individuais, com nomes/IDs e os numeradores provenientes da tabela, estão no contrato JSON. Os denominadores D_i e v_i ficam simbólicos. Não basta possuir s_D em Mpc para obter V_i em dex². O campo `v_corr_2mpp_km_s` que existe nos metadados não foi exposto nem convertido; somente sua existência é referenciada.

Unidades: y,h em dex; V em dex². Se uma matriz diagonal fixa T multiplica por5 as linhas originalmente logarítmicas para colocá-las na convenção de magnitude, transformar simultaneamente `y'=Ty`, `X'=TX`, `a_h'=Ta_h`, `c_C'=Tc_C`, `C'=TCTᵀ`. Assim, para MM, V'_i=25V_i e a'_h,i=5. Covariância cruzada com uma linha não escalada recebe fator5, não25. Não confundir esse Jacobiano fixo de unidades com o Jacobiano não linear de distâncias.

## 4. A derivada completa é outra receita

**[DERIVED — cálculo simbólico]** A derivada do mesmo y, mantendo q0/j0 fixos, é

\[
a_i=\frac{\partial y_i}{\partial D_i}=-\frac1{\ell D_i},\qquad
b_i=\frac{\partial y_i}{\partial v_i}
=\frac1\ell\left[\frac1{v_i}+\frac{F'(z_i)}{cF(z_i)}\right]
=\frac{1+z_iF'(z_i)/F(z_i)}{\ell v_i},
\]
\[
F'(z)=-A+2Bz,\quad U'(v)=F+zF',\quad U''(v)=(2F'+zF'')/c.
\]

O loader usa **b_i^up=1/(ell*v_i)** na incerteza, embora use F na transformação central. Portanto V_up não é a propagação diferencial completa daquela transformação. Isso é uma identificação de receitas, não uma troca automática nem uma conclusão sobre o tamanho da diferença nos dados não abertos.

Para a distribuição primitiva, no limite diferencial:

\[
C^{delta}_{ij}=a_ia_j\Sigma^{DD}_{ij}+a_ib_j\Sigma^{DV}_{ij}
+b_ia_j\Sigma^{VD}_{ij}+b_ib_j\Sigma^{VV}_{ij}.
\]

Em particular, `V_delta,i=a_i² Var(D_i)+b_i² Var(v_i)+2a_i b_i Cov(D_i,v_i)`. O sinal do termo misto vem dos Jacobianos; não se podem substituir derivadas por módulos. Se v_i deriva de várias primitivas, aplicar a regra da cadeia à correção efetiva. Selecionar uma coluna2M++ não documenta por si só a lei de erro dessa correção.

Qualquer componente de calibração comum exige os seus Jacobianos e covariância. O mesmo orçamento240 em duas linhas não significa nem uma variável comum de240 nem variáveis independentes demonstradas. Se a covariância primitiva já inclui velocidade peculiar, não somar o mesmo orçamento novamente. Covariâncias com os interceptos SN/SBF e com âncoras/calibrações permanecem não determinadas pelas larguras marginais; usar a mesma reconstrução de fluxo pode produzir dependências que devem ser modeladas ou assumidas explicitamente.

Como verificação algébrica de convenção, o polinômio MM satisfaz `F(z)=K_L(z)/(1+z)^2+O(z^3)`, para `K_L=1+(1−q0)z/2−(1−q0−3q0²+j0)z²/6`. Isso é compatível com uma expansão do tipo distância angular. Não demonstra, sem documentação adicional da medição, o tipo físico da distância de cada linha; Mpc é a unidade admitida. Não substituir silenciosamente D_A por D_L.

## 5. Assimetria e estimativas de erro

As larguras inferior/superior são distintas; seu promedio upstream perde essa informação. Metadados e código não demonstram que os intervalos originais sejam desvios padrão de uma gaussiana, nem identificam seu nível de credibilidade ou correlações de posterior. O campo chamado erro não resolve essa questão sem uma lei amostral.

Mantendo v fixo, a transformação exata dos extremos de distância seria

\[
\Delta y_- =\log_{10}(1+d_i^+/D_i),\qquad
\Delta y_+ =-\log_{10}(1-d_i^-/D_i),
\]

com D_i>d_i^- para o segundo extremo. O aumento de D corresponde à cauda inferior de y. Essas expressões transportam extremos; não os promovem automaticamente a probabilidades de uma sigma. Extremos de velocidade exigem `log10[U(v±s)/U(v)]` e domínio positivo, não uma troca de sinal no mesmo erro relativo.

Nem uma distância posterior publicada nem seu intervalo são automaticamente uma likelihood. Caso B venha a usar posteriors de ajustes de discos, identificar a likelihood, prior e seleção de origem; não contar o prior de publicação como evidência nova. Sem essas informações, a alternativa B permanece incompleta, embora matematicamente especificada.

## 6. Contrato A recomendado: o que significa condicional

Preparar uma ficha de referência R* com erros publicados, D_ref/v_ref, unidades, correção, fonte e hash, obtida somente na etapa de leitura autorizada. Neste momento D_ref/v_ref e V_i* ficam null. Fixar a receita upstream e usar `V_i*=V_up(R*)` sem recalcular durante a varredura de parâmetros ou para cada hipótese.

O experimento estipulado é

\[
Y^*\mid\mathcal R^*\sim N_{\mathcal A_s}\big(\mu_i(\theta)+X\eta,C_s^*(\mathcal R^*)\big),
\]

com C_s* comum aos cinco modelos em cada cenário s. A proposta mais simples, fiel à montagem upstream MM, usa cinco variâncias positivas na diagonal e covariâncias MM–resto nulas, declaradas como **INPUT do experimento de trabalho**, não como descoberta de independência. O contrato mantém essa proposta sem adotá-la. Se forem escolhidas dependências não nulas, precisam de fonte/parametrização e de uma matriz conjunta PSD com suporte compatível; larguras sozinhas não as determinam.

**Distinção essencial:** R* é uma ficha fixa usada para definir esse experimento de trabalho. Se R* for obtida das mesmas D/v observadas, congelá-la não prova que a lei condicional real seja a gaussiana acima. Condicionar literalmente nos próprios D e v torna y=f(D,v) determinado; não sobra automaticamente ruído gaussiano com V_up. Mesmo um estimador de covariância independente não é a covariância verdadeira conhecida sem uma hipótese/distribuição adicional. Registrar a proveniência endógena/exógena de R*, sem reinterpretar uma flag como prova.

O aceite operacional deverá separar `working_experiment_ratified`, `common_covariance_artifact_verified` e `physical_sampling_law_adequacy`. Nenhum desses campos pode atribuir verdade física ao outro. Hash/PSD/posto certificam propriedades do artefato e do modelo; não certificam a lei real de medição.

## 7. Consequências para suporte e cota F9

**[DERIVED, condicional ao experimento A]** Se `R_s X=0`, `R_s C_s* R_sᵀ=I_nu`, o verdadeiro parâmetro pertence ao domínio nulo e os suportes/normalizações são comuns, então `||R_s(Y*−mu_null)||²` tem lei qui-quadrado_nu. A cota residual e a cota de ganho pelo span global do documento `CALIBRATION_BOUND_CANDIDATE.json` permanecem utilizáveis sob suas demais condições. São envelopes superiores das caudas, não distribuições exatas das estatísticas ajustadas.

A receita mantém a resposta MM proporcional a a_h, sem uma nova coluna física. Por isso não acrescenta direção à inclusão global17/18 já candidata. Isso não mede o posto após branqueamento: R_s e o suporte precisam ser qualificados em cada matriz conjunta. Não usar uma tangente local no lugar da inclusão global.

Se o bloco MM é independente e estritamente positivo, acrescenta cinco dimensões de ruído ao bloco sem MM; X tem cinco novas linhas zero e conserva seu posto suportado. Sob as hipóteses herdadas, a cadeia condicional é:262linhas locais sem MM →267com MM;283coordenadas com o fundo;72vínculos exatos; posto conjunto no máximo211; posto nuisance63; dimensão residual no máximo148. São limites condicionais da fonte, **não um posto medido aqui**. Correlações cruzadas ou singularidades exigem verificar novamente suporte/posto; não transferir automaticamente a conta143 do preflight sem MM.

Transformação fixa de unidades não altera a lei do quociente se todos os objetos forem transportados. Na densidade singular, o Jacobiano é o da transformação restrita ao suporte; não aplicar cegamente det(T) do espaço ambiente inteiro. Cancelamento de normalização entre modelos requer a mesma medida, suporte e fatores independentes de todos os parâmetros integrados. Bayes e calibração frequentista continuam separados.

Um C comum escolhido com base nos dados, mas diferente da covariância verdadeira, não garante esse pivô. Uma possível extensão gaussiana exige uma desigualdade uniforme comprovada `Sigma_true <= a C_work`, com suporte compatível e controle do centro; então cabe a extensão dominada já mencionada na cota, não a cota original sem fator. Nenhum a foi calculado ou proposto numericamente aqui. Não renovar alpha, multiplicidade, priors ou mínimos certificados por causa desta especificação.

## 8. Contrato B: transporte exato e calibração própria

Definir uma distribuição conjunta `p(D,V,cal | theta,eta)` e seus domínios. Uma gaussiana em D pode atribuir massa a D≤0; truncamento, lognormal ou outra lei positiva precisa de especificação e normalização, não descarte posterior de simulações. Corrigir v por fluxo e modelar o mesmo fluxo novamente na covariância é dupla contagem se ambos representam a mesma incerteza.

Para as cinco medidas, escrevendo f(D,V)=(y1,...,y5), o transporte exato é `p_Y(y)=integral delta(y−f(w)) p_W(w) dw`. Não existe determinante quadrado de um Jacobiano5×10 que dispense essa integração. Uma mudança bijetiva válida é `(D,V) -> (Y,V)`, com

\[
D_i(y_i,v_i)=U(v_i)/(H_{unit}10^{y_i}),\qquad
\left|\frac{\partial D_i}{\partial y_i}\right|=\ell D_i,
\]
\[
p_Y(y\mid\theta,\eta)=\int_{\mathcal V(y)} p_{D,V}(D(y,v),v\mid\theta,\eta)
\prod_{i=1}^5(\ell D_i(y_i,v_i))\,d^5v.
\]

Manter v como observação em vez de marginalizá-lo define outra representação estatística, cujo espaço de dados/normalização tem de ser declarado; não contar y e D novamente como dados independentes. Calibração latente requer a distribuição conjunta ou sua marginalização explícita; não inventar novos priors nesta unidade.

A aproximação diferencial da seção4 é somente a primeira ordem. Mesmo com primitivas centradas, em geral `E[f(W)] != f(E[W])`. Para duas primitivas de uma linha, o viés de segunda ordem contém

\[
\tfrac1{2\ell}\left[\Sigma_{DD}/D^2+
\big(U''/U-(U'/U)^2\big)\Sigma_{VV}\right],
\]

pois a derivada mista D–v de f é zero. Essa expressão local não substitui uma distribuição nem foi avaliada nos dados. Assimetria, viés e covariâncias dependentes dos parâmetros podem invalidar o C comum e a inclusão simples das médias exigidos pela cota atual.

Consequência: B precisa demonstrar uma dominação válida ou calibrar suas estatísticas uniformemente nos nulos, inclusive parâmetros de perturbação e incerteza de Monte Carlo. Um bootstrap no melhor ajuste observado, uma gaussiana aproximada pelo Jacobiano ou uma simulação pontual não certificam automaticamente uma cauda global5sigma. Manter os cinco modelos físicos e os priors atuais não dispensa essa especificação do modelo de medição.

## 9. Preparação entregue e lacunas delimitadas

`CONTRATO_MM_CANDIDATO.json` fornece nomes/IDs, fórmulas por linha, unidades, referências protegidas, receita recomendada, pressupostos de dependência e guardas. `PLANO_CONTROLES_SINTETICOS_MM.json` descreve controles novos e independentes **não executados**; C01–C08 consumidos não são repetidos. `FONTES_E_FORMULAS.json` fixa proveniência, pins e trechos. `VALIDACAO_DOCUMENTAL.json` verifica apenas consistência documental/custódia, sem solver ou propagação numérica.

Está resolvido o que implementar e sob qual interpretação. Faltam, para uso científico: ratificação do experimento, preenchimento autorizado e pinado das referências, matriz conjunta/supporte qualificados e condições restantes da cota. O contrato não transforma erros publicados em C verdadeira por uma flag. Não foi calculado F9, likelihood, ajuste, variância observada MM, y, S, g, H0 ou sigma. Originais, gate e memórias permanecem intactos.
