# Levantamento A5/A6 — F1.ATRATOR, ADENDO1

Autor: codex-gerente-tgl/atrator_lean. Reivindicação668 comunicada pela coordenação. Protocolo ACOM próprio recuperado, revisão7. [REAL] Fontes lidas, hashes medidos em SOURCE_HASHES_R1.json. Não se compilou candidata nem se executaram números nesta etapa.

## 1. O J e o K que realmente existem

Todos os identificadores abaixo pertencem ao namespace TGLExt.

| Fonte:linha | Declaração e tipo | Conteúdo |
|---|---|---|
| ConjugateAct.lean:60 | conjJ : Pair n → Pair n, Pair n=((Fin n→ℝ)×(Fin n→ℝ)) | Troca literal dos dois vetores: (p.2,p.1). É função real pareada; não se presume o J antiunitário contínuo. |
| ConjugateAct.lean:79 | J_squared_is_one (p : Pair n) | conjJ(conjJ p)=p. O composto J∘J é id, não J. |
| ConjugateAct.lean:84 | J_preserves_identity | pairEnergy(conjJ p)=pairEnergy p. |
| ConjugateAct.lean:99 | J_invariant_iff_diagonal | conjJ p=p ↔ p.1=p.2. |
| DecisionCommutation.lean:142 | pairK (d : Fin n→ℝ) : Pair n→Pair n | (d*p.1,−d*p.2). |
| DecisionCommutation.lean:149 | JKJ_eq_neg_K d p | conjJ(pairK d(conjJ p))=−pairK d p; usa o mesmo conjJ, sem homônimo. |
| LightIsJ.lean:60 | light_crosses_without_loss | Empacota J²=id e conservação de pairEnergy. |
| LightIsJ.lean:68 | light_inverts_the_gradient_preserving_structure | Empacota JKJ=−K com conservação da energia de K. A nomenclatura J=Luz é [ONTO], explícita na fonte. |
| TheTwoPairings.lean:72 | J_and_K_anticommute | conjJ(pairK d p)=−pairK d(conjJ p), no mesmo espaço. |
| TheLivingWord.lean:85 | identity_survives_the_mirroring | Se p.1≠p.2, então conjJ p≠p, mas conjJ(conjJ p)=p. Evita identificar involução com projeção. |

## 2. A leitura angular é outro operador

TheAngleIsTheProjection.lean:76 define genK=!![0,1;−1,0] em Matrix (Fin2)(Fin2) ℂ; :79–85 define projPlus, projMinus e angFamily. TheObserverReadsTheAngle.lean:79 prova projPlus*angFamily θ=exp(iθ)•projPlus; :114 prova observing_adds_nothing, projPlus*(projPlus*angFamily θ)=projPlus*angFamily θ.

Esse teorema é releitura de uma projeção espectral angular. Não é o operador conjJ da função real pareada; não se pode encadear os nomes. Não fornece um limite angular, uma dinâmica ou uma projeção E_J sem nova ponte tipada.

## 3. Proposta tipada A5 — o que falta construir

[DERIVED — desenho, ainda não compilado] Permanecer no próprio Pair n:

- AdJ(F)(p) := conjJ(F(conjJ p)), para F : Pair n→Pair n.
- E_J(F)(p) := (1/2:ℝ) • (F p + conjJ(F(conjJ p))).
- Reutilizar J_squared_is_one e JKJ_eq_neg_K; provar distribuição de conjJ sobre soma e escala pelos seus dois componentes.
- Saídas exatas: AdJ(conjJ)=conjJ; E_J(conjJ)=conjJ; E_J(E_J(F))=E_J(F); E_J(pairK d)=0; E_J(id)=id; imagem de E_J coincide com os F invariantes por AdJ.
- A igualdade literal de termos não contém argumento de fonte externa. Isso é o sentido verificável de “sem termo externo”, não uma conclusão de fechamento físico.

A5 deve escolher a OPERAÇÃO de leitura. Se leitura significa composição simples, J∘J=id e a tese J∘J=J é falsa para o espelho não trivial. Se significa conjugação, J∘J∘J=J; a conjugação é uma involução em F, não uma projeção. Se significa a média E_J, ela é idempotente e fixa J. Essas três sentenças são distintas.

E_J fixa também id. Na face n=1, id e conjJ são operadores distintos e linearmente independentes; por isso essa leitura sobre operadores NÃO tem imagem de dimensão1. Não identificar E_J com a leitura R de A4 ou concluir unicidade de Luz do mero fato E_J(J)=J. O R anterior atua em estados/populações; E_J atua em operadores.

Busca pelos usos reais de conjJ no TGLExt não localizou a média E_J. As esperanças condicionais de outros módulos têm dados/tipos próprios e não foram tratadas como essa média por homonímia.

## 4. A6 — ablação com conclusão nomeada

[DERIVED — desenho, ainda não compilado] A minimalidade universal dos três rótulos não segue de A1–A3:

1. Dinâmica nula como GERADOR zero dá T=id. Se R for recalculado como projeção do novo espaço fixo, R=id, então A1 (trajetória constante), A2 e A3 continuam verdadeiras. A4 falha na face de dimensão2. Se for mantido o R rank1 do primário, A1 falha para x fora da sua imagem. Pré-registro precisa dizer qual leitura mantém; não trocar uma pela outra após o resultado.
2. beta=0 implica transmissão total e T(0)=id: zero_beta_control já compilado em OpticalPopulationBridgeR2.lean:83. O mesmo contraexemplo refuta indispensabilidade irrestrita da dissipação para A1–A3, mas não para atração a um único estado normalizado.
3. “Sem ponto fixo” não existe para mapa linear homogêneo em espaço vetorial: 0 sempre é fixo. O controle afim x↦x+1 tem ausência de ponto fixo já provada em OpticalPopulationBridgeR2.lean:87, fora do contrato homogêneo/CPTP. Não apresentá-lo como ablação física da própria classe.
4. “Sem suporte” pode significar espaço zero. Nele A1–A3 podem sobreviver por vacuidade, mas e≠0 e dimensão fixa1 falham. Isso é controle de não vacuidade, não evidência que todas as identidades exigem suporte não trivial.
5. “Sem leitura” precisa ser operacional: R ausente deixa A2/A3 sem enunciado; R=0 mantém idempotência e ambos produtos zero, mas falha A3 como projeção de Fix(T) quando há e≠0. A1 também falha para o estado fixo não zero. Não confundir ausência com operador zero sem declarar a escolha.
6. Sem fase angular não equivale a beta=0: um canal de populações dissipativo já pode ser real e sem fase complexa. Remover fase global de S pode deixar |S|² intacto. Portanto a fase só é indispensável se o observável nomeado a consumir.

## 5. Ressalva encontrada na fonte existente

TheTwoPairings.lean:102–110 define flatK=0 e demonstra J²=id e J flatK J=flatK. A docstring diz que isso demonstra a não redundância da anticomutação. Entretanto, com K=0, também J K J=−K, pois −0=0. O enunciado Lean está correto; a leitura de exclusão na docstring não é demonstrada por esse exemplo. Não reutilizar esse caso como prova de necessidade da hipótese. Nenhum original foi corrigido neste levantamento; a ressalva fica ao lado aqui.

## 6. Reaproveitamento da entrega anterior

TheSingularityReadsTheAttractor.lean:27,46,52,58 contêm A1 Cesàro, A2, A3; :64 a hipótese estrita no complemento; :95 dimensão1; :190 o contraexemplo identidade com dimensão2. A formulação A6 deve distinguir identidades A1–A3, não trivialidade, dissipação e unicidade A4. Fonte anterior permanece intacta.