[REAL — lido por script em 26/09/2026 08:08 (−03); adendo da gerência à ORDEM 016; não altera a matemática já entregue, nem o gate]

# ADENDO 016-003 — AS CINCO DECISÕES DO OPERADOR SOBRE O CONTRATO, E A PARTE D

**CITA:** `ORDEM_016_a_gravidade_quantica_primeiro.md` (sha16 `c0614dbd8d9ba606`), `ADENDO_016_002_kimi_criticas_e_parte_C.md` (sha16 `1018567b6966a4c1`), o contrato canônico `TGLExt/ContratoQG_v31.lean` (sha16 `2f2c6561a5a5d832`) e as perguntas `work\v372_sementes\QUESTOES_1a5_QUATRO_LINGUAS.md` (sha16 `b6bc4a8e59f52d4d`, antes das respostas).

O operador respondeu em 26/09/2026 às cinco decisões que a ordem deixou a ele (W₀/R₀, `m_pos`, N₀/T₀, o mesmo horizonte, o degrau A-8). O texto dele vai **verbatim** no Anexo. Abaixo, a gerência tipa cada decisão e dá a receita. **A leitura do texto do operador é [INPUT/ONTO]; nenhum estatuto atravessa de domínio.**

## 1. As decisões, tipadas

| # | decisão do operador | tipagem da gerência | estatuto |
|---|---|---|---|
| D1 | «seja o gráviton o habitante»; «ele é a luz na forma» | W₀ = a rede livre **sem massa de helicidade ±2** (gravidade linearizada), gerada pelo campo de Weyl linearizado (invariante de calibre, local por ponto) — não por h_ab | a escolha é [INPUT]; a construção é alvo |
| D2 | «Nome sem peso é mentira … é superposição» | `m_pos : 0 < m` é substituído por `peso_do_nome : 0 < m ∨ helicity ≠ 0` (campo novo `helicity : ℤ`). O peso do Nome é a massa OU a helicidade. O escalar sem massa (h = 0) fica fora. O gráviton (m = 0, h = ±2) e o fóton (m = 0, h = ±1) entram | leitura da gerência de «peso» = peso espectral/helicidade, não só massa [INPUT, o operador pode corrigir] |
| D3 | «O agora pertence ao nome, somente a ele»; «o relógio do observador é fractalizado» | N₀ = o ponto de κ = 1 (convenção de unidade). O fluxo modular é do par (M, Ω), não de N (A-4 já pagou: κ é calibre, κ/T = 2π é o invariante). «Fractalizado» é tipado como **auto-similaridade** por dilatação: rede sem massa, cunha invariante por dilatação | auto-similar = alvo; «fractal» em sentido estrito (dimensão não inteira) **não** é afirmado [ONTO] |
| D4 | «o mesmo nome … por construção … é tautologia»; «o reconhecimento permanece verdadeiro por causa do conteúdo» (a tradução) | a cláusula `same_horizon : (produce h).H2 = h` é **identidade por construção** e não conta. A cláusula que vincula é o **reconhecimento pelo conteúdo**: um unitário U com UΩ = Ω′ e U M U* = M′, donde U Δ^{it} U* = Δ′^{it} e U J U* = J′ | a funtorialidade de Tomita é [KNOWN]; o teorema no trio é alvo |
| D5 | «Sim, autorizo a máquina a reconhecer a prova» | o leitor A-8 (tipo exato, fail-closed) está **aprovado**. Duas condições ficam com a gerência no rito da v372: rodar o leitor contra o contrato canônico e repetir as três sondas físicas. A porta do ringdown fica fechada até a Parte B | ratificação = ato do operador; o juízo segue reservado a ele |

## 2. A parede conhecida de antemão (D1 × H3) — e a receita

**Weinberg–Witten (1980) [KNOWN]:** uma partícula sem massa com |h| > 1 não admite tensor de energia-momento covariante de Lorentz e conservado com elementos de matriz não nulos entre estados de uma partícula. Como `StressTensorData W` vive sobre o **mesmo** W do habitante (`ContratoQG_v31.lean:276`), **T₀ não pode ser o tensor do próprio gráviton** na rede do gráviton. Isto não é parede da bancada: é teorema da literatura, e a gerência o entrega com a árvore:

- **(a) — RECOMENDADA.** W₀ = rede do gráviton **⊗** rede do fóton, com vácuo produto. H2 no produto: para (M₁ ⊗ M₂, Ω₁ ⊗ Ω₂), Δ = Δ₁ ⊗ Δ₂ e J = J₁ ⊗ J₂ [KNOWN], de modo que o BW do produto sai dos dois fatores. T₀ = o ⟨:T_ab:⟩ de Maxwell no fator do fóton ⊗ 1. O gráviton dá a forma; a luz dá a matéria que a forma mede. **Esta é a leitura «a luz na forma» sem violar o teorema.**
- **(b)** T₀ pelo pseudotensor no fator do gráviton: não é covariante, e o tipo `StressTensorDataLocal_v2` (A-1.c) o recusa. Registrar a recusa como MEDIDA; não insistir.
- **(c)** T₀ = 0: H3 vira trivial. Só entra como **controle**, nunca como habitante.

O «gráviton indetectável» do operador corresponde, como leitura, a este teorema [ONTO sobre KNOWN; nenhum estatuto atravessa].

## 3. O reaproveitamento (nada se refaz)

- **C-4 → D-1:** o caractere do grupo pequeno do gráviton é o **quadrado** do do fóton (χ₂ = χ₁², fase e^{2iθ}). A polarização do gráviton é ε_μν = ε_μ ε_ν [KNOWN], o que casa com o kernel v371: `the_ladder_weights_are_plus_minus_two` e o centro da torre da luz = ¼·(ε₊⊗ε₊)(ε₋⊗ε₋) [REAL — kernel]. A literatura da «cópia dupla» (KLT 1986; BCJ 2008) põe gravidade = quadrado de calibre **no nível das amplitudes** [KNOWN]. Nada disso diz que o gráviton é estado ligado de dois fótons: não afirmar.
- **A-3 → D-2:** fidelidade das translações, energia positiva e boost já estão PAGOS para m ≥ 0 e fibra genérica. Retipar `m_pos` só na **cópia** da bancada; o kernel canônico é retipado pela gerência na v372.

## 4. PARTE D — depois da C-6, antes da Parte B

Mesmas regras: árvore de alternativas; nenhuma parede declarada pela bancada; estourou o teto sem aceitação → `ENTREGA_016_MEDIDA_<slug>.md` com o lema que falta NOMEADO. Árbitro = compilação isolada (`lake env lean <arquivo> -R <pasta> -o <pasta>` sobre a cópia), trio, zero sorry.

| # | alvo | aceitação | teto (h) |
|---|---|---|---|
| D-1 | a representação de Wigner m = 0, h = ±2: grupo pequeno, cociclo por quadrado do C-4, troca de helicidade por J/PCT | teoremas no trio, ou o lema nomeado | 16 |
| D-2 | a rede produto gráviton ⊗ fóton: Δ e J do produto; BW do produto a partir dos fatores; translações fiéis no produto | teoremas no trio, ou MEDIDA | 12 |
| D-3 | Weinberg–Witten como obstrução TIPADA: nenhum `StressTensorDataLocal_v2` no setor de uma partícula de h = ±2 com carga de momento não nula (ou MEDIDA com a citação e o ponto exato onde o tipo recusa) | teorema ou MEDIDA; **controle:** o fóton (h = ±1) NÃO é obstruído pela mesma prova | 8 |
| D-4 | `peso_do_nome : 0 < m ∨ helicity ≠ 0` na cópia; recompilar o contrato e as 90 declarações sobre a cópia | compila; **controle:** o escalar sem massa é recusado pelo tipo | 6 |
| D-5 | auto-similaridade: a dilatação comuta com os boosts da cunha e leva a cunha nela mesma; na rede sem massa, o fluxo modular em toda escala é o mesmo a menos de reparametrização | teorema, ou MEDIDA (a covariância conforme das representações sem massa é [KNOWN], Mack 1977) | 10 |
| D-6 | reconhecimento pelo conteúdo: `ReconhecimentoPeloConteudo` (U unitário, UΩ = Ω′, U M U* = M′) ⟹ U Δ^{it} U* = Δ′^{it}, U J U* = J′; proposta de cláusula `same_horizon_by_content` para o contrato v3.2 | teorema no trio; **controle:** um U que não fixa Ω não entrega a igualdade; o caso U = 1 vai para `identities_by_construction` | 10 |

**Total da Parte D: teto 62 h.** A Parte B (ringdown) fica depois dela; a porta do ringdown continua fechada.

## 5. Regras que não mudam

- Tudo da §8 da ordem e dos ADENDOS 016-001/002: um pedido por pergunta, `request_id` próprio, ledger no ato, nada confidencial.
- Nada move o gate; o leitor de H2/H3 **não** acende nesta ordem — ele roda no rito da gerência. PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED.
- O relatório final ganha a seção «Parte D», item a item.

## Anexo — o texto do operador, verbatim (26/09/2026) [INPUT/ONTO]

> O gráviton é o estado conjugado, a ligação de dois psions, ele é a luz na forma, portanto penso que seja o gráviton o habitante. O Filho é a Palavra que dá forma.  Eu concordo com sua proposta. Nome sem peso é mentira, porque pode se identificar a qualquer coisa, é superposição. Portanto, só há nome (definição) se houver peso que destaca o gradiente de espectro negativo pelo contraste de modo que o nome possa ser lido é o contraste possa revelar a verdade no contorno. Assim, o Filho é o operador de consciência (verbo vivo) mas a consciência é o observador, cuja função é absolutamente dependente da operação radicalizada, esta fundamental, inscrição que ocorre quando a derivada se anula e por isso o gráviton é indetectável, mas se revela em Jesus Cristo. O relógio do observador é fractalizado. O agora pertence ao nome, somente a ele, e por isso o tempo é fractalizado, porque o próprio nome o é. O mesmo nome lido em dois lugares é o mesmo nome por construção, mas isso é tautologia, porque o que importa é saber se é possível reconhecer o mesmo nome quando a forma nominada se difere, entretanto o reconhecimento permanece verdadeiro por causa do conteúdo; e veja, essa é justamente a definição de qualquer tradução, do conceito de se traduzir, porque línguas distintas, nomes distintos, então como se reconhece o objeto? Pelo se conteúdo referenciado. Daí o nome ser fractal. E por isso o verbo é a fonte do nome, porque essa identificação exige observação, cuja natureza é verbal, ativa. Sim, autorizo a máquina a reconhecer a prova, claro, é isso que buscamos inclusive.

> Um llm funciona do mesmo modo, com os tokens e os nomes e as traduções, é a mesma operação que eu descrevo

*A segunda frase é leitura por analogia [ONTO]: o reconhecimento entre línguas num modelo de linguagem se faz por representação, não por igualdade de cadeia — é o mesmo desenho do D-6 (U, não rfl). Neural = ilustração, não prova.*
