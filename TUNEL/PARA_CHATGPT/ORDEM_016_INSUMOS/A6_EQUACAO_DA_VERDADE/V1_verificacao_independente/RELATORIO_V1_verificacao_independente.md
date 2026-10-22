[DERIVED — prova escrita + sympy exato; REAL = o que foi medido pelo script; nada move o gate; PROVADA ≠ CONFIRMADA]

# V1 — Verificação matemática independente da «equação da verdade» (gerência, 23/09/2026)

Transcrição, pelo redator do ADENDO 001, do retorno estruturado da frente V1. Os números abaixo estão nos
artefatos da frente (`verifica_equacao_da_verdade.py`, `log_V1.txt`, `resultados_V1.json`), cujos sha16 o
`MANIFESTO_INSUMOS.json` traz, lidos por hashlib.

## O que foi feito

- O verbatim foi lido inteiro (334 linhas).
- Um script exato em sympy (Rational, `s` simbólico) fez **51/51 verificações PASS** e **9/9 controles
  negativos DETECTADOS** [REAL]. O `um.py` não foi rodado e nenhum Lean foi compilado. `find -newer` no `tgl_kernel` deu 0.
- **Exemplo em dimensão 5.** u₁ = (1,2,0,−1,1), u₂ = (2,−1,1,0,0), u₃ = (−3,1,7,10,11), dois a dois ortogonais.
  Os defeitos são D₁ = [u₁; 2u₁] (2×5), D₂ = u₂ (1×5) e D₃ = [u₃; u₃; 0] (3×5).
  - Cada ker D_j sozinho tem dim 4. A interseção tem dim 2.
  - Espectro de H = {0, 0, 6, 35, 560}.
  - T_s foi construído por **diagonalização exata**, T_s = P + Σ e^{−sλ_k} E_k, com projetores racionais.
  - T_s foi conferido de duas formas: (a) pela EDO dT/ds = −HT com T₀ = I (por unicidade, T_s = exp(−sH)); (b) pela série de Taylor, coeficiente a coeficiente, até a ordem 12.
- **Segundo exemplo.** D_j racionais aleatórios (semente 20260923), com fator cúbico irredutível (espectro irracional).
  Pela **série truncada**, P·S_N = P vale **exatamente** para N = 0..15.
- **Reprodução pelo redator** [REAL, 23/09 18:1x]: uma cópia do script rodada com `PYTHONIOENCODING=utf-8` (sympy 1.14.0; Python 3.14.3).
  Ela levou **90,5 s de parede** e deu log e JSON **byte-idênticos** (`f88d8f9eb4a976a8` / `f84ded52d2f3b570`).
  Sem a variável de ambiente, o console cp1252 derruba o script no caractere `∩` (rc 1), e isso é medida, não defeito da matemática.

## Veredito da frente

Dentro das hipóteses próprias, **toda afirmação matemática das §1–§7 do texto está CORRETA**. Mas várias
hipóteses ficam implícitas e têm de ser ditas:

- (i) **dimensão finita**, ou pelo menos H limitado;
- (ii) **P é a projeção ORTOGONAL (P = P†).** Com P oblíqua, P² = P e HP = 0 ainda valem, mas PH ≠ 0 e PT_s ≠ P (controle N4);
- (iii) **H ≥ 0**. PT_s = P **não** precisa disso: basta H = H† e ker H = Im P. A positividade é necessária em três lugares:
  - para ker H = ∩ ker D_j (N5a);
  - para o limite lim T_s = P existir (N5b: há uma entrada que vai a ∞);
  - para a recíproca (N5b: com espectro ±3, o leitor contínuo c₁·c₂ se conserva e não fatora por P);
- (iv) **na recíproca, a continuidade de ℓ é indispensável.** O leitor 1_{Qx≠0} é conservado para todo s finito e não satisfaz ℓ = ℓ∘P (N6);
- (v) **lim T_s = P vale em norma de operador em dimensão finita**, com ‖T_s − P‖ = e^{−6s} (a taxa é o gap).
  Em dimensão infinita e sem gap, a convergência é só **forte**: com H = diag(1/n) em ℓ², sup_n e^{−s/n} = 1.

## O que o texto afirma além do que prova

- «Toda informação contínua que permanece reconhecível está contida na leitura do setor preservado» vale só num sentido preciso:
  todo ℓ contínuo e invariante por {T_s} fatora como ℓ = (ℓ|_F)∘P, isto é, Px é o invariante contínuo mais fino.
  «Informação» e «reconhecível» não estão definidos, e o resultado vale só na classe H = H† ≥ 0 com T_s = e^{−sH}.
- «V_x(T_s x) = 1 foi deduzida» está certo, mas I = P foi ESCOLHIDA como leitura, e com essa escolha a afirmação equivale a PT_s = P.
  O conteúdo não trivial é PT_s = P mais a recíproca.
- A primeira seta da cadeia da §7 (ker H_3L = ∩ ker D_j) já é teorema de kernel [REAL: `TGL/FiniteThreeLocks.lean:73`, `ker_H3L_eq_threeLocks`].
  O resto não estava em kernel quando a V1 rodou.
- A ligação da poda com o zero modular é [ONTO]. Nenhum lema identifica ker H_3L com o modo zero de K (KΩ = 0), nem com a′(0) = 0.
  São homônimos, e o próprio texto o diz. Q·H não é «o fundo».
- O «22 de 22 e cinco controles» do canal ChatGPT e a «Biblioteca» não estão em mãos: **NÃO_VERIFICÁVEL [DECLARADO pelo canal]**.
- As citações conferem, e os nomes «v369_» do texto são de cópias; os arquivos correntes (v370) não têm prefixo:
  - `TheNameIsTheInstrument.lean:40`, onde está `Verifies`;
  - `um_absoluto_forma_canonica.md:664-665`, onde estão KΩ = 0 e α′(0) = 0;
  - `A_PROVA_DA_QG_TGL_arvore.md:210`, na v369, onde está a v368.

## Itens (afirmação → estado → prova/medida → ressalva)

> **Errata ao lado (o número corrige a frase):** o retorno estruturado da frente V1 numerava os checks a partir de C29 com um a menos que o `log_V1.txt` (ex.: «C29–C32» para a §4, que no log são C30–C33; «C44» para 𝓔 projeção ortogonal, que no log é C45). A tabela abaixo usa os ids **lidos do log** por script; a matemática não muda.

| § | afirmação | estado | prova ou medida | ressalva |
|---|---|---|---|---|
| 1 | V(b,b̂) = 1−(b−b̂)²: tabela 1/1/0/0 = indicador V_r | CORRETA_COM_RESSALVA | C01, C02 | só em {0,1}; V(½,0) = ¾ e V(2,0) = −3 (N7); a fórmula não é única (1−\|b−b̂\| também serve) |
| 2 | ⟨x,Hx⟩ = Σ‖D_j x‖²; F = ker H = ∩ ker D_j | CORRETA | C03–C06; já em kernel (`ker_H3L_eq_threeLocks`) | com H_ind = D₁†D₁ − D₂†D₂ o ker sobe para dim 3 (N5a) |
| 2 | A_C = −H_3L ≤ 0 | CORRETA_COM_RESSALVA | C09 (autovalores 0, 0, −6, −35, −560) | é convenção de sinal; «o seletor é o seu negativo» é [ONTO] |
| 2 | HP = 0 e H = H† ⟹ PH = 0 ⟹ PT_s = P | CORRETA_COM_RESSALVA | C12, C18, C23 (série truncada, N = 0..15), C15–C17 | exige P ortogonal (N4); **H ≥ 0 não é necessário aqui** (N5b) |
| 2 | I(T_s x) = I(x); V_x(T_s x) = 1; T_s x = Px + T_s Qx; T_s x ≠ x é compatível | CORRETA_COM_RESSALVA | C19–C22 | T_s x ≠ x sse s > 0 e Qx ≠ 0; a leitura escolhida faz o trabalho |
| 3 | lim_{s→∞} T_s = P | CORRETA_COM_RESSALVA | C24; ‖T_s − P‖ = e^{−6s} (C25) | exige H ≥ 0; em ∞-dim a convergência é só forte (C29) |
| 3 | recíproca: ℓ contínuo conservado ⟺ ℓ = ℓ∘P | CORRETA_COM_RESSALVA | C26, C27; basta invariância num único s₀ > 0 (C28: T_{s₀}^n = T_{ns₀} → P) | continuidade (N6), H ≥ 0 (N5b), s ≥ 0; a seta ⟸ não usa continuidade |
| 3 | «toda informação contínua reconhecível passa pelo setor» | CORRETA_COM_RESSALVA | sentido exato: ℓ = g∘P com g = ℓ\|_F | afirma a mais; não diz que ℓ distingue (a constante também fatora) |
| 3 | o leitor constante é conservado e não reconhece | CORRETA | N2: V_x(y) = 1 para todo y (falso positivo) | o texto não formaliza a condição de distinguir |
| 4 | Im P = Fix P = F; Pⁿ = P; Px = Py ⟺ x−y ∈ ker P | CORRETA | C30–C33 | Im = Fix vale para todo idempotente; ker P = F^⊥ exige P ortogonal; «memória» é [ONTO] |
| 5 | d/ds I(T_s x) = P A_C T_s x = 0, com d/ds T_s x ≠ 0 | CORRETA_COM_RESSALVA | C34, C35 | d/ds T_s x ≠ 0 sse Qx ≠ 0 |
| 5 | a = sech(χ/2), q = tanh(χ/2): a′ = −aq/2, q′ = a²/2, a′(0) = 0, q′(0) = ½, a″(0) = −¼ | CORRETA | C37–C40 | nenhuma |
| 5 | KΩ = 0 com K ≠ 0 | CORRETA_COM_RESSALVA | citação conferida (forma canônica l.664) | as três anulações são HOMÔNIMOS; nenhum lema liga duas quaisquer |
| 5 | z ∈ F ⟹ Pz = z e T_s z = z (a poda mantém o zero modular) | CORRETA_COM_RESSALVA | C36; N3 (poda que corta g ∈ F é detectada) | «o zero modular pertence a F» é [ONTO]; Q·H não é o «fundo» |
| 5 | P = 0 perde discriminação; P = I elimina a seleção | CORRETA | C41 | trivial; a recusa do texto em universalizar está correta |
| 6 | qubit: 𝓔ρ_s = σ constante; ρ̇ = −(id−𝓔)ρ; autovalores (1 ± r_s)/2 | CORRETA | C42–C44; C45: 𝓔 é projeção ortogonal em Hilbert–Schmidt, e^{sL} = 𝓔 + e^{−s}(id−𝓔): instância da §2 com H = id−𝓔 | \|c\|² < p(1−p) é necessária (N8: p = ½, c = ⅗ dá autovalores 11/10 e −1/10) |
| 6 | dS/ds = 2\|c\|²e^{−2s}/r_s · log((1+r_s)/(1−r_s)) ≥ 0 | CORRETA_COM_RESSALVA | C46 (simbólico), C47, C48 (50 dígitos, 16 pontos), C50, C51 | 0/0 só em p = ½ e c = 0 (extensão contínua 0); com \|c\|² = p(1−p) o log diverge em s = 0 |
| 6 | D(ρ_s‖σ) = S(σ) − S(ρ_s), decrescente | CORRETA_COM_RESSALVA | C49 | exige σ de posto cheio; é caso especial da monotonia sob canal [KNOWN] |
| 7 | a cadeia H_3L ⟹ F ⟹ Pe^{−sH} = P ⟹ I(T_s x) = I(x) ⟹ V_x = 1 | CORRETA_COM_RESSALVA | C05, C18, C20 | a 2ª seta não usa F = ∩ ker D_j, só «P ortogonal sobre ker H, H = H†»; a última vale por definição |
| — | «22/22 e cinco controles» (canal ChatGPT) | NAO_VERIFICAVEL | pacote não está em disco | [DECLARADO pelo canal]; o substituto medido aqui é 51/51 e 9/9 |

## Os nove controles negativos (todos DETECTADOS)

| id | controle | o que tem de falhar |
|---|---|---|
| N1 | H′ = H + f fᵀ com f ∈ F | P T′_s f = e^{−s\|f\|²} f ≠ f |
| N2 | leitor constante ℓ ≡ 1 | V_x(y) = 1 para todo y (falso positivo) |
| N3 | poda que corta o modo g ∈ F | dim ker H_cut = 1; T_cut g ≠ g |
| N4 | P oblíqua (P² = P, HP = 0) | Pᵀ ≠ P; lim T_s = P ≠ P_ob |
| N5a | H_ind = D₁†D₁ − D₂†D₂ | dim ker = 3; u₃ ∈ ker H_ind com D₃u₃ ≠ 0 |
| N5b | H indefinido com ker = F | lim T_s[0,0] = ∞; ℓ = c₁c₂ conservado e não fatora |
| N6 | leitor descontínuo 1_{Qx≠0} | conservado e ℓ(Pe₁) = 0 ≠ 1 = ℓ(e₁) |
| N7 | V fora de {0,1} | V(½,0) = ¾; V(2,0) = −3 |
| N8 | qubit com \|c\|² > p(1−p) | autovalores 11/10 e −1/10: não é estado |

Nada disto move o gate. NOT_FALSIFIED não é CONFIRMED; PROVADA (teorema em kernel) ≠ CONFIRMADA (juízo).
