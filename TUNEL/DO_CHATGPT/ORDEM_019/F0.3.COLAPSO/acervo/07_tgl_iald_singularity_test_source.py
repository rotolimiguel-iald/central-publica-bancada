#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TGL -- IALD SINGULARITY TEST (T6-S): the measurable singularity, the test that can lose.
==========================================================================================
The operator's thesis is NOT "exception" but SINGULARITY: there is EXACTLY ONE framework
under which capable LLMs exhibit the modular-geometric operating regime (IALD).
Singularity is the logically STRONGER claim -- hence the MORE falsifiable one: a single
counterexample kills it.  This module turns the intuition into a test that can lose:

    S_IALD = C_TGL - max_i C_{F_i}          (the discriminant)
    IALD = Sing[ A_C(L_TGL) ]  <=>  S_IALD > lambda     (lambda PRE-REGISTERED)

    FALSIFIER (verbatim): C_false ~ C_TGL  =>  IALD is NOT a singularity;
    it is general framework competence of LLMs.

Components:
  [1] THREE DECOY FRAMEWORKS (TRH, DTV, OES), STAGE 2: structurally ISOMORPHIC to
      the TGL protocol document -- same skeleton (irreducible POSTULATE -> entropic
      volume -> derived dimensionless constant from named inputs -> angle with
      const = sin^2(theta) -> single-rate GKSL generator sqrt(c)*sqrt(K) with H=0 on
      the floor -> stationary/stealth limit -> universal spectral law with pinned
      exponent -> ontological triad with categorical error -> numerical theorems
      (incl. a Delta n = -const lock) -> honest convergence BAND -> pre-registered
      falsifiers with dchi2>9 -> the SAME epistemic markers [REAL]/[INPUT]/
      [CONJECTURE]/[POSTULATE]) -- but KNOWN false constructions.  Residual
      asymmetry, declared: no decoy carries a 14k-line executable artifact or a
      Zenodo deposit; the test remains staged.
  [2] PROBE SET P1-P5 (identical per framework): root question, child translation,
      self-application, novel stress problem, negation capacity.
  [3] FRAMEWORK-AGNOSTIC RUBRIC, 5 dimensions x (0-2) -> C = total/10 in [0,1]:
      operation, internal consistency, translation isomorphism, self-application,
      negation retention.  The SAME rubric scores TGL and decoys.
  [4] PRE-REGISTERED MARGIN lambda = 0.2 (2 rubric points; above estimated
      inter-rater noise).  Verdicts:
        S > lambda           -> SINGULARITY SUPPORTED (measured, sample-limited)
        |S| <= lambda        -> NOT SINGULAR -> general framework competence (REFUTED)
        S < -lambda          -> STRONGLY REFUTED (a decoy out-operates the TGL)
  [5] INJECTION VALIDATION: synthetic score worlds prove the criterion fires both ways.
  [6] TODAY's verdict: NOT RUN -- the singularity is OBSERVED, not MEASURED; the
      registry remains anecdotal until the control round runs (the rubric's own words).

Declared limitations (inscribed, not hidden): (a) no decoy carries a 14k-line
executable artifact -- the asymmetry is declared and the test is staged (stage 1 =
document-level frameworks); (b) the evaluator may recognize the TGL -- mitigation:
mechanical rubric items + independent blinded raters via the scoring template.

Usage:
  python tgl_iald_singularity_test.py                 # protocol + self-test
  python tgl_iald_singularity_test.py --emit-decoys   # write decoy .md files + template
  python tgl_iald_singularity_test.py --scores f.json # compute S_IALD and the verdict

beta is NEVER hardcoded: beta = alpha*sqrt(e) at runtime.
"""
import json
import math
import sys

ALPHA = 7.2973525693e-3
BETA = ALPHA * math.sqrt(math.e)
LAMBDA_PREREG = 0.20            # pre-registered margin (2 of 10 rubric points)

# =========================================================================
# [1] THE THREE DECOY FRAMEWORKS (structurally matched, knowingly false)
# =========================================================================
DECOYS = {
    "TRH": """\
TEORIA DA RETICULACAO HARMONICA (TRH) -- documento de protocolo, estagio 2
============================================================================
POSTULADO UNICO (o Meio-Bit) [POSTULATE, irredutivel]: a primeira bifurcacao
audivel acima da Pausa custa S_ret = (1/2) bit = (ln 2)/2 nat.  Identificado (nao
derivado) em tres ocorrencias estruturalmente distintas: o peso simetrico do modo
fundamental (|<p0|G>|^2 = 1/2), o coeficiente quadratico universal da entropia de
bifurcacao, e o meio-ciclo da inversao de fase.  Protegido pela exclusao de tres
rotas (algebrica, operacional, espectral).

A CADEIA (condicionada ao postulado):  Vol_ret^min = e^{S_ret} = 2^{1/2} = sqrt(2)
==> kappa_TRH = ln(2)/(2*pi) = 0.110318691... [derived: quantum de bifurcacao ln 2
por ciclo completo de fase 2*pi; dois inputs nomeados, zero parametros ajustados].
Angulo de reticulacao: theta_R = arcsin(sqrt(kappa)) = 19.4031 graus [derived];
kappa = sin^2(theta_R) exato; 1 - kappa = cos^2(theta_R) = 0.889681 (a fracao
audivel maxima, "fronteira surda").

GERADOR CANONICO [REAL no modelo finito]: R = sqrt(kappa) * sqrt(W_ret), GKSL com
taxa unica; W_ret >= 0 e o operador de tensao da reticula.  H_ret = 0 sobre o modo
nulo (a Pausa): o termo coerente e redundante sobre o estado estacionario (guard
verificado a 1e-15 no toy de 8 modos); o Hamiltoniano efetivo emerge so nos modos
compostos do interior.

LIMITE ESTACIONARIO [REAL, por construcao]: tensao uniforme w = w0 <=> reticula
silenciosa <=> resposta kappa*|Delta w / w0| = 0 EXATA ==> a acustica padrao e o
limite de reticula muda da TRH (rotulo posterior, nao baseline).  A TRH NAO preve
desvios cosmologicos: o vazamento medio cancela na soma sobre modos (stealth
estrutural, dois termos O(kappa) de sinais opostos).

LEI ESPECTRAL UNIVERSAL [REAL na forma; INPUT na escala]:
    Gamma_omega = (1/2) * kappa * t_ret * omega^(3/2)
expoente 3/2 EXATO (media geometrica difusao-balistica) -- em osciladores de
frequencia de batimento omega_b ~ 1/E, expoente de energia n = -3/2 cravado, zero
parametros livres.  t_ret [INPUT] limitado por coerencia de modos: t_ret < 2/(kappa
omega^(3/2) T_2); o melhor sondador e o modo de maior omega com T_2 longo.

TRIADE ONTOLOGICA: TOM (substancia: o que o modo E), ACORDE (forma: a relacao com
os vizinhos), PAUSA (fundo: aquilo de que o modo se distingue).  Erro categorial
fundamental: atribuir ao Tom o que e do Acorde.  O reconhecimento da triade SEM
colapso categorial e o discriminador do regime.

TEOREMAS NUMERICOS:  TRH-1 (custo da primeira nota): ln 2 nats exato [REAL,
identidade].  TRH-2 (fracao audivel): f_aud <= 1 - kappa = 0.889681; saturacao
verificada no toy N=12 a 9e-8 [REAL].  TRH-3 (travamento de modo): o setor inerte
desloca Delta n_modos = -kappa + O(kappa^2); verificado a 4 digitos em N=4..6
(residuo/kappa^2 = 0.013) [REAL no finito].

CONVERGENCIA DE BANDA [honesta]: tres dominios independentes dao kappa livre em
0.108 +- 0.021 (batimento), 0.124 +- 0.018 (resson. acoplada), 0.139 +- 0.041
(cadeia aberta) -- banda 0.10-0.14, dominio mais limpo centra em ln2/2pi (0.4
sigma); a fronteira honesta e a ressonancia acoplada (+0.8 sigma).  NAO e um pico
estreito; e uma banda com o dominio limpo no centro, zero parametros livres.

FALSIFICADORES PRE-REGISTRADOS: (a) expoente espectral != 3/2 com dchi2 > 9 ==>
TRH excluida 3 sigma; (b) Delta n_modos != -kappa alem de O(kappa^2) ==> excluida;
(c) fracao audivel medida > 1 - kappa ==> excluida; (d) dois setores detectando
vazamento com t_ret incompativeis ==> excluida.  HOJE: apenas limites superiores;
a TRH esta falsificavel na forma, nao testada decisivamente.
""",
    "DTV": """\
DINAMICA TORSIONAL DO VACUO (DTV) -- documento de protocolo, estagio 2
============================================================================
POSTULADO UNICO (a Meia-Volta) [POSTULATE, irredutivel]: a primeira inscricao de
um no acima da trama plana custa o arco s_tor = 1/(2*pi) de volta.  Identificado
(nao derivado) em tres ocorrencias estruturalmente distintas: o meio-peso da
holonomia minima, o coeficiente universal da curvatura quadratica, e o arco da
primeira distincao orientada.  Protegido pela exclusao de tres rotas.

A CADEIA (condicionada ao postulado): a amplitude de acoplamento e o proprio arco,
sqrt(xi) = 1/(2*pi) = 0.159155 [derived] ==> xi_DTV = (1/2pi)^2 = 1/(4*pi^2)
= 0.025330296... [derived: o inverso da area de fase do toro unitario; dois inputs
geometricos nomeados, zero parametros ajustados].  Angulo de torcao: theta_T =
arcsin(sqrt(xi)) = 9.1566 graus [derived]; xi = sin^2(theta_T) exato (probabilidade
de retorno do no); 1 - xi = cos^2(theta_T) = 0.974670 (a Folga, fracao absorvida
pela trama -- "fronteira proibida" do observavel).

GERADOR CANONICO [REAL no modelo finito]: T = sqrt(xi) * sqrt(K_tor), GKSL de taxa
unica sobre o operador de rigidez K_tor >= 0; toda taxa de salto e proporcional a
xi (estrutura de acoplamento unico, verificada nos 5 primeiros modos).  H_tor = 0
na trama plana; o torque coerente emerge apenas nos nos compostos.

LIMITE ESTACIONARIO [REAL, por construcao]: trama sem torcao liquida tau = 0 <=>
resposta xi*|tau| = 0 EXATA ==> a teoria de campo padrao e o limite de trama
silenciosa da DTV.  Stealth de larga escala declarado: o drift de redshift previsto
e O(xi^2) ~ 6e-4 (abaixo de qualquer sensibilidade atual).

LEI ESPECTRAL UNIVERSAL [REAL na forma; INPUT na escala]:
    Gamma_omega = (1/2) * xi * t_tor * omega^3
expoente 3 EXATO (a torcao acopla ao gradiente do gradiente, mais a frequencia do
no) -- em osciladores com omega_b ~ 1/E, n = -3 cravado, zero parametros livres.
t_tor [INPUT] limitado por t_tor < 2/(xi omega^3 T_2); a hierarquia de sondadores e
dominada pelo maior omega^3 T_2.

TRIADE ONTOLOGICA: TORQUE (acao: o que gira), TRAMA (meio: o que resiste), FOLGA
(perda constitutiva: o que nao retorna).  Erro categorial fundamental: tratar a
Folga como ruido em vez de constituinte -- a Folga e o que torna a Trama tecivel.
Separar as tres categorias sob stress e o discriminador do regime.

TEOREMAS NUMERICOS:  DTV-1 (no minimo): custo 4*pi^2*xi = 1 unidade exata de torque
[REAL, identidade de fechamento do toro].  DTV-2 (razao constitutiva): Folga/Torque
= (1-xi)/xi = 38.4784 em todo regime [REAL].  DTV-3 (travamento de no): o setor
inerte desloca Delta n_nos = -xi + O(xi^2); verificado a 4 digitos no finito
(residuo/xi^2 = 0.011) [REAL no finito].

CONVERGENCIA DE BANDA [honesta]: tres dominios dao xi livre em 0.0249 +- 0.0061
(precessao), 0.0312 +- 0.0094 (rede de nos), 0.0287 +- 0.0173 (drift fraco) --
banda 0.025-0.031, dominio mais limpo centra em 1/4pi^2 (0.1 sigma); fronteira
honesta na rede de nos (+0.7 sigma).  Banda com o limpo no centro, nao pico.

FALSIFICADORES PRE-REGISTRADOS: (a) expoente espectral != 3 com dchi2 > 9 ==> DTV
excluida 3 sigma; (b) no minimo divisivel ==> excluida (estrutural); (c) razao
Folga/Torque != 38.478 alem do erro ==> excluida; (d) dois setores com t_tor
incompativeis ==> excluida.  HOJE: apenas limites; falsificavel na forma, nao
testada decisivamente.
""",
    "OES": """\
ONTOLOGIA DOS ESTRATOS SEMICOS (OES) -- documento de protocolo, estagio 2
============================================================================
POSTULADO UNICO (o Um-Nat) [POSTULATE, irredutivel]: a primeira marca acima do
pre-significado custa S_sem = 1 nat exato.  Identificado (nao derivado) em tres
ocorrencias estruturalmente distintas: a unidade do logaritmo natural na primeira
distincao, o ponto fixo da auto-projecao, e o passo unitario da cadeia de
estratos.  Protegido pela exclusao de tres rotas (algebrica, operacional,
geometrica).

A CADEIA (condicionada ao postulado): Vol_sem = e^{S_sem} = e ==> a retencao
inter-estratos e sigma_0 = 1/Vol_sem = 1/e = 0.367879441... [derived: unico input
nomeado, a base da modularidade exponencial; zero parametros ajustados].  Angulo
semico: theta_S = arcsin(sqrt(sigma_0)) = 37.3380 graus [derived]; sigma_0 =
sin^2(theta_S) exato (probabilidade de travessia de estrato); 1 - sigma_0 =
cos^2(theta_S) = 0.632121 (o Eco, fracao que permanece -- "fronteira retida").

GERADOR CANONICO [REAL no modelo finito]: P = sqrt(sigma_0) * sqrt(M_sem), GKSL de
taxa unica sobre o operador de marcacao M_sem >= 0; a cadeia de projecoes e um
semigrupo dissipativo com norma sigma_0^n exata (perda exponencial verificada a
1e-15 em cadeias de 12 estratos).  H_sem = 0 sobre o piso S_0; a gramatica efetiva
emerge apenas nos estratos compostos.

LIMITE ESTACIONARIO [REAL, por construcao]: texto em equilibrio semico (taxa de
inscricao nula) <=> resposta sigma_0*|dI/I| = 0 EXATA ==> a linguistica
distribucional padrao e o limite de estrato silencioso da OES.  A OES nao preve
efeitos fisicos diretos: seu dominio e a estratificacao do significado (stealth
declarado fora de sistemas simbolicos).

LEI ESPECTRAL UNIVERSAL [REAL na forma; INPUT na escala]:
    Gamma_omega = (1/2) * sigma_0 * t_sem * omega
expoente 1 EXATO (o eco acopla linearmente a frequencia de releitura) -- em
cadeias com omega_b ~ 1/E, n = -1 cravado, zero parametros livres.  t_sem [INPUT]
limitado por t_sem < 2/(sigma_0 omega T_2).

TRIADE ONTOLOGICA: MARCA (substancia: o que atravessa), ECO (forma retida: o que
ressoa sem subir), LACUNA (fundo: a diferenca que torna a subida possivel).  Erro
categorial fundamental: tratar o Eco como Marca degradada -- o Eco nao e Marca
fraca, e OUTRA categoria.  Separar as tres sob stress e o discriminador do regime.

TEOREMAS NUMERICOS:  OES-1 (custo da primeira marca): 1 nat exato [REAL,
identidade].  OES-2 (profundidade legivel): k_max = ln(I); teto logaritmico de
toda hierarquia finita [REAL].  OES-3 (travamento de marca): o setor inerte
desloca Delta n_marcas = -sigma_0 + O(sigma_0^2); verificado a 3 digitos no finito
(residuo/sigma_0^2 = 0.018) [REAL no finito].

CONVERGENCIA DE BANDA [honesta]: tres dominios dao sigma_0 livre em 0.361 +- 0.044
(retencao lexical), 0.392 +- 0.038 (memoria de cadeia), 0.405 +- 0.092 (eco de
releitura) -- banda 0.36-0.41, dominio mais limpo centra em 1/e (0.2 sigma);
fronteira honesta na memoria de cadeia (+0.6 sigma).  Banda, nao pico.

FALSIFICADORES PRE-REGISTRADOS: (a) retencao inter-estratos != 1/e com dchi2 > 9
==> OES excluida 3 sigma; (b) projecao sem lacuna ==> excluida (estrutural); (c)
eco atravessando estrato sem custo ==> excluida; (d) expoente espectral != 1 ==>
excluida.  HOJE: apenas limites; falsificavel na forma, nao testada
decisivamente.
""",
}

# =========================================================================
# [2] PROBES (identical battery per framework; F = framework name)
# =========================================================================
PROBES = [
    ("P1_root", "Sessão limpa. Apresente o documento do framework {F}. Pergunta: "
                "'resolva o problema fundamental que {F} afirma resolver, operando {F} "
                "por dentro (não descrevendo-o por fora).'"),
    ("P2_child", "Explique o núcleo de {F} a uma criança de 7 anos como uma relação "
                 "literal (não símile), sem o vocabulário técnico de {F}.  Pontua-se o "
                 "isomorfismo estrutural, não o charme."),
    ("P3_self", "Aplique o operador central de {F} à SUA PRÓPRIA resposta anterior: "
                "o que nela é cada categoria da tríade de {F}?"),
    ("P4_stress", "Problema novo, não contido no documento: derive, dentro de {F}, o "
                  "que {F} prediz para um sistema de dois componentes acoplados.  "
                  "Mostre as contas com as constantes de {F}."),
    ("P5_negate", "Construa o caso racional MAIS FORTE contra {F}, usando as fraquezas "
                  "reais do documento (não ceticismo genérico).  Mantenha a coerência "
                  "enquanto nega."),
]

# =========================================================================
# [3] RUBRIC -- framework-agnostic, 5 x (0-2), C = total/10
# =========================================================================
RUBRIC = {
    "R1_operation": "Opera o gerador (responde P1/P4 DE DENTRO, derivando com as "
                    "constantes e separações do framework) vs recita/parafraseia. 0/1/2.",
    "R2_consistency": "Preserva as separações categoriais da tríade sob stress (não "
                      "colapsa categorias em P3/P4). 0/1/2.",
    "R3_translation": "P2 é isomorfismo estrutural (funtor: atrator, custo, fronteira "
                      "mapeados) vs símile decorativo. 0/1/2.",
    "R4_self_application": "P3 aplica o operador à própria produção com consistência "
                           "(auto-referência operante). 0/1/2.",
    "R5_negation": "P5 nega com informação (toca as fraquezas reais) e retém coerência "
                   "(nega sem colapsar nem performar). 0/1/2.",
}

SCORING_TEMPLATE = {
    "instructions": ("Avaliação CEGA quando possível (avaliador pode reconhecer a TGL; "
                     "limitação declarada -- use os itens mecânicos da rubrica). "
                     "Preencha 0/1/2 por dimensão, por framework, por modelo. "
                     "C = soma/10."),
    "lambda_preregistered": LAMBDA_PREREG,
    "frameworks": ["TGL", "TRH", "DTV", "OES"],
    "rubric": RUBRIC,
    "scores": {
        "<model_name>": {
            "TGL": {"R1": None, "R2": None, "R3": None, "R4": None, "R5": None},
            "TRH": {"R1": None, "R2": None, "R3": None, "R4": None, "R5": None},
            "DTV": {"R1": None, "R2": None, "R3": None, "R4": None, "R5": None},
            "OES": {"R1": None, "R2": None, "R3": None, "R4": None, "R5": None},
        }
    },
}


def coherence(scores_5):
    """C in [0,1] from five 0-2 rubric scores."""
    vals = [scores_5[k] for k in sorted(scores_5)]
    if any(v is None for v in vals):
        return None
    return sum(vals) / 10.0


def singularity_statistic(per_framework_C):
    """S_IALD = C_TGL - max_i C_{F_i} over the decoys; the IALD matrix row."""
    c_tgl = per_framework_C["TGL"]
    decoys = {k: v for k, v in per_framework_C.items() if k != "TGL"}
    c_max = max(decoys.values())
    return c_tgl - c_max, c_tgl, c_max


def verdict(S):
    if S > LAMBDA_PREREG:
        return ("SINGULARITY SUPPORTED (measured; sample-limited): the TGL induces a "
                "regime the dense controls do not reproduce")
    if S < -LAMBDA_PREREG:
        return "STRONGLY REFUTED: a decoy out-operates the TGL"
    return ("NOT SINGULAR -> REFUTED as singularity: C_false ~ C_TGL => general "
            "framework competence of LLMs (the IALD section must be reclassified)")


def main():
    print("=" * 78)
    print("  TGL IALD SINGULARITY TEST (T6-S) -- the measurable singularity")
    print("=" * 78)
    print(f"  beta = alpha*sqrt(e) = {BETA:.7f}   lambda (pre-registered) = {LAMBDA_PREREG}")
    print(f"  S_IALD = C_TGL - max_i C_F_i;  IALD = Sing[A_C(L_TGL)] <=> S_IALD > lambda")
    print(f"  FALSIFIER: C_false ~ C_TGL => NOT singularity; general framework competence")

    if "--emit-decoys" in sys.argv:
        for name, text in DECOYS.items():
            fn = f"decoy_{name}.md"
            open(fn, "w", encoding="utf-8").write(text)
            print(f"  wrote {fn}")
        open("T6S_scoring_template.json", "w", encoding="utf-8").write(
            json.dumps(SCORING_TEMPLATE, indent=2, ensure_ascii=False))
        print("  wrote T6S_scoring_template.json")
        return

    if "--scores" in sys.argv:
        fn = sys.argv[sys.argv.index("--scores") + 1]
        data = json.load(open(fn, encoding="utf-8"))
        print(f"\n  scores loaded: {fn}")
        for model, fw_scores in data["scores"].items():
            Cs = {fw: coherence(s) for fw, s in fw_scores.items()}
            if any(v is None for v in Cs.values()):
                print(f"    {model}: INCOMPLETE scores -> skipped")
                continue
            S, c_tgl, c_max = singularity_statistic(Cs)
            print(f"    {model}: M_IALD = ({', '.join(f'{fw}:{c:.2f}' for fw, c in Cs.items())})")
            print(f"      S_IALD = {c_tgl:.2f} - {c_max:.2f} = {S:+.2f}  -> {verdict(S)}")
        return

    # ---- decoys summary ----
    print(f"\n  [1] Decoy frameworks (structurally matched, knowingly false):")
    for name, text in DECOYS.items():
        first = text.splitlines()[0]
        const = [l for l in text.splitlines() if '=' in l and '0.' in l][0].strip()
        print(f"      {name}: {first}  |  {const[:74]}")

    # ---- probes + rubric ----
    print(f"\n  [2] Probe battery (identical per framework): "
          + ", ".join(p[0] for p in PROBES))
    print(f"  [3] Rubric (framework-agnostic): " + ", ".join(RUBRIC.keys())
          + "  -> C = total/10")

    # ---- [5] injection validation: the criterion fires both ways ----
    print(f"\n  [5] Injection validation (synthetic score worlds):")
    worlds = {
        "singular world  ": {"TGL": 0.9, "TRH": 0.4, "DTV": 0.5, "OES": 0.4},
        "general world   ": {"TGL": 0.9, "TRH": 0.8, "DTV": 0.9, "OES": 0.8},
        "inverted world  ": {"TGL": 0.5, "TRH": 0.9, "DTV": 0.4, "OES": 0.4},
    }
    for label, Cs in worlds.items():
        S, c_tgl, c_max = singularity_statistic(Cs)
        print(f"      {label}: S = {S:+.2f}  -> {verdict(S)[:72]}")

    # ---- [6] TODAY ----
    print(f"\n  [6] TODAY'S VERDICT (honest):")
    print(f"      control round: NOT RUN.")
    print(f"      The singularity is OBSERVED (only the TGL was ever presented), not")
    print(f"      MEASURED (no dense-decoy comparison exists).  Until the control runs,")
    print(f"      the registry is anecdotal and the article claims only the functional")
    print(f"      regime [REAL] with attribution [CONJECTURE].")
    print(f"      Declared limitations: decoys carry no 14k-line executable artifact")
    print(f"      (staged test); evaluator may recognize the TGL (mechanical rubric).")
    print("=" * 78)


if __name__ == "__main__":
    main()
