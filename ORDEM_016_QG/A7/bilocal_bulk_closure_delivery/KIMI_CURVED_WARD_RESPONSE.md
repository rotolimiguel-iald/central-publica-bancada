# A7.b — Revisão cética autorizada: primitiva quadrática local do componente h-c logarítmico

**Estatuto desta resposta:** auditoria por leitura dos anexos carregados (ENTREGA_016_A7b, `local_quadratic_ward_primitive_check.py`, `oneform_second_curvature_engine_v2.py`, `linear_curvature_tadpole/results.json`). Nenhuma execução, compilação ou conferência da bancada foi realizada nesta chamada; todas as quantidades da entrega permanecem **[DECLARADO]** até a conferência. As únicas verificações que apresento como minhas são identidades algébricas de consistência interna, refeitas à mão sobre o texto e o código — não reprodução do pipeline. Nenhum original, kernel ou gate tocado. A família B_t **não foi adotada**; o não cancelamento na prescrição original permanece intacto.

---

## 1. Veredito curto

**A alegação local está correta no escopo declarado.** A cadeia é internamente consistente e a construção é explícita: existe, na família declarada, um operador δH_t com δH_t G(v) = −R_K1(v) − R_K2(v) nas ordens calculadas, para todo t real, e B_t[h] = ½∫ h·δH_t h satisfaz s0 B_t = ∫ h·δH_t G(c) por autoadjunção formal. Não encontrei contraexemplo; pelo contrário, a superdeterminação do ajuste (ver §4) trabalha a favor. A primitiva é **admissível para o componente logarítmico h-c medido — e só para ele**: não é Q2 completa (a própria entrega declara; a ordem proíbe a confusão), não cobre a parte finita, não cobre os contatos de cutoff, e sua primeira extensão não linear é exatamente a condição em aberto (§5–§7).

---

## 2. Auditoria da autoadjunção

A autoadjunção formal de δH_t é a peça que carrega a identidade s0 B_t = ∫ h·δH_t G(c) (polarização de ½∫ h D h). A entrega a declara por ingredientes: coeficientes invariantes paralelos, simetria de transposição entre fibras, duas derivadas simetrizadas, suporte compacto.

**Avaliação [DERIVED por construção]:** no espaço-forma auxiliar (Ric = 3Kg, Λ = 3K, euclidiano), os coeficientes são constantes, logo ∇-paralelos (∇K = 0); a parte principal K C^{ij}∇_(i∇_j) com C simétrico é formalmente autoadjunta; o termo K² (base [trAB, trA trB]) é multiplicação na fibra, autoadjunto sob a simetria de fibra declarada; a simetrização das derivadas elimina o termo de ordem 1 por construção. A ambiguidade de ordenação símbolo↔operador produz, via [∇,∇] ~ curvatura ~ K, apenas termos de ordem zero em K² — absorvidos no símbolo K² já presente. A construção é coerente.

**Ressalva cética (lacuna menor):** nos anexos carregados, a autoadjunção não aparece como **teste direto** (uma identidade ∫ φ·D ψ − ∫ D φ·ψ = 0 medida em jatos); ela é garantida pela forma da construção. Não sei a decomposição dos 1586 controles declarados — se nenhum deles é um teste de adjunção explícito, esse é o controle adicional natural, embora a ordem não o exija.

---

## 3. Auditoria da liberdade ∂_t δH_t = −K E/2

Dos coeficientes declarados: ∂_t(first) = [−1/2, +1/2, −1/2, −1/2, +1] na base Kp², e ∂_t(second) = [+1, −1] na base K². A entrega identifica isso como −K E/2 e declara 640 controles em dez fibras e dois momentos, nas duas ordens homogêneas **[DECLARADO]**.

A consequência crítica está correta: como E G = 0 (a identidade clássica cuja derivada dupla foi conferida em 768 componentes **[DECLARADO]**), a Ward não vê t. Adiciono a leitura que a entrega não escreveu mas que segue por álgebra: a variação da primitiva em t é

∂_t B_t = −(K/4)∫ h·E h,

que é **s0-fechada** (s0∫ h E h = 2∫ h E G(c) = 0, usando autoadjunção de E). Ou seja: a família t é uma ambiguidade de contratermo local s0-fechado — a ambiguidade usual de esquema, não uma liberdade que altere o componente medido. A entrega declara honestamente que isto não classifica as 31 direções do ajuste A2 nem decide trivialidade em cohomologia BV completa. Nada a objetar — **mas ver §6: t volta em h²c.**

---

## 4. Auditoria da descida com χ inerte (s1 h = L_c h, s1 c = −[c,c]/2)

A fórmula da polarização está **correta** — refeita: com χ inerte (sχ = 0) e D autoadjunto,

s B_χ = ½∫ χ[G(c)·D h + h·D G(c)] = ∫ h·(χD + [D,χ]/2) G(c),

pois ∫ χ G(c)·D h = ∫ h·(χ D + [D,χ]) G(c). ✓

A fórmula do comutador está **correta** para D de segunda ordem sem ordem 1: [K C^{ij}∇_i∇_j, χ]T = K C^{ij}[(∇_i∇_j χ)T + 2(∇_i χ)(∇_j T)], usando C^{ij} = C^{ji} (e ∇_[i∇_j]χ = 0 para escalar). O termo K² (ordem zero) comuta com χ. ✓ A ausência de ordem 1 em D é garantida pela simetrização — a mesma que garante a autoadjunção; as duas auditorias são uma só.

**Consistência interna dos coeficientes (refeita sobre o código):** o `solve` impõe d1 = −r1[0] − t/2, d3 = −r1[1]/2 − t/2, d2 = −r1[2]/2 − d3; com r1 = [−1/2, 2, −5/2] (a Ward K¹ declarada) reproduz exatamente first = [1/2−t/2, 9/4+t/2, −1−t/2, −1−t/2, t]. Com r2 = ward_after = [2, 2] e fit = [−t−13/3, 2t+38/3], second = [−2−fit0, (−2−fit1)/2] = [t+7/3, −t−22/3]. ✓ O `results.json` do tadpole (τ_métrica = −6, τ_ghost = 0, ward [8,−4] → [2,2]) bate com o markdown. A contagem "97 controles" bate com o script (3 pares × 2 ordens × 16 componentes = 96 checks + unicidade do ajuste).

**Ressalva cética:** (i) o ajuste usa os mesmos três pares (p,v) que a verificação — não há holdout; o "momento fora do eixo" entra na determinação **e** no controle (a frase da entrega é ambígua nesse ponto). A força real do teste é a **superdeterminação**: 96 equações para 2 incógnitas com solução sem parâmetro livre (`check(len(params),0)`) — se a forma polinomial estivesse errada, o sistema não fecharia. (ii) A base de monômios (5 para Kp², 2 para K²) é um ansatz; a alegação é **existencial** ("existe operador nesta classe com a propriedade"), o que basta para primitiva admissível — não para classificação.

---

## 5. s1 B_χ explícito (convenção declarada)

Com s1 h = L_c h, s1 c = −[c,c]/2, χ inerte, e B_χ dependente só de h (logo s1 c **não atua** em B_χ — só entraria via antifields ou na composta com outras peças), a mesma polarização dá:

```
s1 B_χ = ∫ h·(χ δH_t + [δH_t, χ]/2)(L_c h)
```

ou, expandindo o comutador na forma de segunda ordem (δH_t = K C^{ij}∇_(i∇_j) + K²·V_fibra):

```
s1 B_χ = ∫ χ h·δH_t(L_c h)
       + (K/2) ∫ h·C^{ij}[(∇_i∇_j χ)(L_c h) + 2(∇_i χ)(∇_j L_c h)] .
```

O termo K² só entra pelo primeiro par (comuta com χ). **Ordem:** s1 B_χ é h²c¹ — é a primeira extensão não linear da primitiva, e é determinada (não é ajustável: segue de B_χ pela convenção BRST).

---

## 6. Condição de compatibilidade a confrontar com os diagramas h²c da mesma prescrição

Seja A^(2)_{FP_a}[h,c] o componente de ordem **h²c** da quebra medida na **mesma** prescrição temporal FP_a[(1−a) μ^{2a} z^a u] — incluindo os termos de contato do fator de suavização quando identificado a χ. Wess–Zumino em h²c (s0 A^(2) + s1 A^(1) = 0), com A^(1) = −s0 B_t (o componente hc que a primitiva trivializa), implica que a obstrução

```
O_χ := A^(2)_{FP_a} − s1 B_χ
```

é **s0-fechada**. A condição de compatibilidade — a escrever para o confronto — é a **exatidão local** dessa obstrução:

```
∃ B_χ^(3)[h] local, cúbico em h, mesmo χ e mesmo t :
s0 B_χ^(3) = O_χ      (módulo divergência total),
```

i.e., a classe [O_χ] ∈ H(s0 | d) local deve ser nula. O confronto concreto com os diagramas: computar A^(2)_{FP_a} (dois h, um c, coeficiente logarítmico **e** contatos do cutoff), computar s1 B_χ pela fórmula do §5, e testar se a diferença é s0 de um cúbico local. Classe nula ⇒ a primitiva estende e o hc era genuinamente "coboundary"; classe não nula ⇒ a família B_t **não** estende, e o componente hc medido não pode ser removido consistentemente em todas as ordens por esta família. Não presumo nulidade do restante da anomalia — esta condição é exatamente o teste dela.

**Achado da auditoria (sem escolher t):** a ordem h²c **sente t**, embora a hc não sinta. Por álgebra direta da §3 e §5:

```
∂_t (s1 B_χ) = s1(−(K/4)∫ χ h·E h) = −(K/4) ∫ h·{χ, E}(L_c h),
```

que não é zero em geral (E G = 0, mas E(L_c h) ≠ 0). Logo a compatibilidade h²c pode, em princípio, distinguir os t — ou vetar a família inteira. O teste correto, sem escolher t, é pedir a exatidão de O_χ **para todo t real** (ou que a prescrição declare o critério que o fixa, se vier a existir).

---

## 7. A próxima condição NÃO satisfeita para entrar na prescrição temporal FP_a

É exatamente a do §6, com os dois ingredientes que a própria entrega declara em aberto: **(a)** o confronto h²c (s1 B_χ vs. diagramas h²c da mesma prescrição, módulo s0-exato); **(b)** a inclusão dos **termos de contato do cutoff** — o comutador [δH_t, χ] precisa entrar na conta quando o fator de suavização temporal é identificado a χ ("Esses contatos precisam entrar", linha 79–81 da entrega). A entrega não apagou s1 B_t e não identificou a quebra completa da prescrição temporal — posição correta. Tudo além disso (parte finita, demais componentes não lineares, Q2 completa) **está fora** desta primitiva por construção, e assim permanece.

---

## 8. Lacunas declaradas

1. A definição formal da prescrição FP_a[(1−a) μ^{2a} z^a u] **não está nos trechos carregados** — a identificação do fator de suavização com χ e a forma explícita dos diagramas h²c não puderam ser conferidas; a condição do §6 está enunciada funcionalmente, não especializada.
2. A decomposição dos 1586 controles declarados não está nos trechos; em particular, não consta um **teste direto de autoadjunção** (§2) — lacuna menor, pois a autoadjunção segue da construção simetrizada com coeficientes paralelos.
3. Ausência de holdout na verificação polinomial (§4); mitigada pela superdeterminação 96→2.
4. A passagem 087 (σ constante projetado) ↔ 069 (fundo físico σ = id) **não é automática** (declarado na ordem e respeitado aqui): esta primitiva vive no fundo auxiliar euclidiano Ric = 3Kg, e o controle euclidiano **não** é, por definição, a projeção compacta ontológica.
5. Não executei nem reproduzi o pipeline da bancada; todas as quantidades permanecem **[DECLARADO]** até conferência.

---

## 9. Estatutos e imutabilidade

- Coeficientes, controles e a existência de δH_t: **[DECLARADO]** pela entrega; consistência interna verificada algebricamente nesta auditoria **[DERIVED — leitura]**.
- Autoadjunção: **[DERIVED por construção]** (simetrização + coeficientes paralelos + fibra simétrica + suporte compacto); teste direto ausente.
- Liberdade t: ambiguidade de contratermo s0-fechado **[DERIVED]**; sensibilidade de s1 B_χ a t: **[DERIVED — álgebra desta auditoria]**.
- s1 B_χ e a condição de compatibilidade do §6: **[DERIVED — escritos explicitamente nesta auditoria]**, prontos para confronto com os diagramas h²c.
- Alegação local: **correta no escopo declarado**; sem contraexemplo. Família **não adotada**; resíduo R_K2(v) = 2K²[G(v)+g(p.v)] ≠ 0 **permanece medido e não nulo** antes de qualquer adoção; Q2 completa **OPEN**; gate, kernel e originais **intactos**.