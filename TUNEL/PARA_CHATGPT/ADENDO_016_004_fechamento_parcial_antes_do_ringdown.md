[REAL — lido por script em 26/09/2026 10:29 (−03); adendo da gerência à ORDEM 016; não altera a matemática já entregue, nem o gate]

# ADENDO 016-004 — O FECHAMENTO PARCIAL DA TEORIA, ANTES DO RINGDOWN

**CITA:** `ORDEM_016_a_gravidade_quantica_primeiro.md` (sha16 `c0614dbd8d9ba606`), ADENDOS 016-001 (`9347a15320f40fea`), 016-002 (`1018567b6966a4c1`), 016-003 (`076940a20f26cf94`), 016-003-bis (`b2294b54d2a37abc`), 016-003-ter (`3469ff03a2b9e438`). **Lido:** `DO_CHATGPT\ENTREGA_016_PROGRESSO.md` (sha16 `76f7c560dcad9230`, última entrada `2026-09-26T13:27:07.183201+00:00`, B/T05) e `ENTREGA_016_PARTE_D_quadro_final.md` (sha16 `b2e74e08bed56216`).

**Ordem do operador (26/09/2026, verbatim):**

> Escreva uma ordem para a bancada para quando ela terminar a prova da gravidade quântica ela realizar um fechamento parcial e te enviar, ou seja, antes do início do teste com ringdown, a hora que a bancada terminar a derivação teórica/técnica total ela deve enviar um primeiro retorno parcial para você já fechar aqui no um.py e depois inserimos o teste com o rongdown

## 0. Onde a bancada está (lido)

As Partes A, C e D foram entregues: cada item está PAGO ou MEDIDA, com as hipóteses nomeadas. A Parte B já começou (T01, T02, T13, T03 e T05 registrados; o próximo seria o T06), sem hora de máquina pesada e sem veredito. **Nada da Parte B se desfaz nem se perde.**

## 1. Quando

1. **Terminar a unidade da Parte B que estiver aberta** (se o T06 já começou, terminá-lo) e **PAUSAR a Parte B**. Nenhuma unidade nova da B abre até o pacote do §2 estar entregue.
2. Montar e entregar o **FECHAMENTO PARCIAL** (§2).
3. **Retomar a Parte B** exatamente do ponto de pausa, sem esperar resposta. Se a gerência publicar `PARA_CHATGPT\RECIBO_016_FECHAMENTO_PARCIAL*.md` pedindo correção, a correção passa na frente da B.

## 2. O que entregar

Pasta `DO_CHATGPT\FECHAMENTO_PARCIAL_016\` + `DO_CHATGPT\ENTREGA_016_FECHAMENTO_PARCIAL.md` (o índice legível). **Por último**, gravado de uma vez: `DO_CHATGPT\FECHAMENTO_PARCIAL_016\PRONTO.json`, com o sha256 de cada arquivo do pacote e o sha256 do próprio `ENTREGA_016_FECHAMENTO_PARCIAL.md`. Sem o `PRONTO.json`, o pacote não está entregue.

| # | peça | conteúdo exigido |
|---|---|---|
| P1 | **Quadro item a item** | A-0…A-8, C-1…C-6, D-1′…D-6 (e D-1…D-3 como CANCELADOS pelo 016-003-ter). Por item: estatuto (PAGO / MEDIDA / NÃO PAGO / CANCELADO); nomes das declarações; arquivos com sha256; para cada MEDIDA, **o lema que falta, nomeado**; horas; custos informados e desconhecidos. |
| P2 | **O pacote Lean consolidado** | Todos os `.lean` da teoria em `lean\`, em ordem de dependência, compilando **juntos** sobre uma **cópia limpa** do kernel v371 (`lake env lean <arquivo> -R <pasta> -o <pasta>`, um log por arquivo). Por declaração: `#print axioms` ⊆ {propext, Classical.choice, Quot.sound}; **zero `sorry`, zero `axiom`**. Lista dos módulos do kernel importados. **Checagem de colisão de nomes** contra todas as declarações do kernel v371 (saída do script; colisão = listada, nunca silenciada). Nenhum nome reservado que a ordem proíbe. Se a compilação conjunta falhar num arquivo, `ENTREGA_016_MEDIDA_<slug>.md` com o import que falha, e o pacote sai mesmo assim com os que compilam. |
| P3 | **O contrato** | (a) Mapa **cláusula a cláusula** de `ContratoH2`, `ContratoH3` e `ContratoImportH3` v3.1: a declaração que habita cada cláusula ou a hipótese nomeada que falta. (b) A **proposta de contrato v3.2** num arquivo próprio que compila: `peso_do_nome` (D-4), a luz como campo de W₀, o gráviton como forma conjugada (D-3′), `same_horizon` por conteúdo (D-6) e `StressTensorDataLocal_v2`, com o **diff contra a v3.1**. (c) **Uma lista única** de todas as hipóteses nomeadas em aberto (por exemplo `GlobalHelicityInducedRepresentationMeasured`, `MaxwellWickExpectationLocalMeasured`, `IsotonyImpliesStripMultiplierCriterion`, o par KMS regional, a instanciação física do D-6, a identificação modular do centro na rede, a covariância física do D-5, a Q2 da A-7), cada uma com onde seria descarregada. |
| P4 | **O leitor A-8** | A versão final, os testes de controle e **a previsão da bancada**: que bandeiras o leitor acenderia contra o pacote. É previsão, não veredito; `gate_changed=false`. O leitor roda no rito da gerência, não na bancada. |
| P5 | **Proposta de runtime** | `PROPOSTA_RUNTIME.py` (**não** o `um.py`): para cada pedra que deve entrar, uma função `prove_<nome>_v372(ONE)` no molde dos módulos do `um.py`. Só contam em `all_verified` os checks que **podem falhar**, com o controle negativo escrito no próprio check («| CONTROLE»); as identidades por construção ficam em `identities_by_construction`. Estatutos marcados; veredito em string, sem CONFIRMED nem PROVED; β nunca literal (`ALPHA_FINE_CODATA_2018 × √e` em runtime). |
| P6 | **Texto para o artigo** | Um parágrafo PT e um EN por bloco (A, C, D), com os estatutos. Curto; a gerência revisa. |
| P7 | **Reprodução** | `reproduzir.py`: numa cópia limpa do kernel v371, recompila o P2 na ordem e reimprime rc e axiomas por arquivo, com o tempo medido. |
| P8 | **Erratas e recusas** | Tudo o que foi corrigido ao longo da ordem (inclusive os cancelamentos do 016-003-ter) e o que a crítica externa apontou, com o que foi aceito e o que foi recusado, e por quê. |
| P9 | **O estado da Parte B na pausa** | T01…T05 (e T06, se feito): estatuto, arquivos com sha256, e o passo exato de retomada. |

**Teto: 6 h de bancada.** O pacote **consolida**; não abre lema novo. O que faltar vira MEDIDA nomeada, e o pacote sai.

## 3. Regras que não mudam

- A bancada **não escreve o `um.py`** nem o kernel canônico. Quem fecha no `um.py` é a gerência, na v372, a partir deste pacote.
- Nunca `lake build` no kernel; só compilação isolada sobre a cópia.
- Tudo da §8 da ordem e dos ADENDOS 016-001/002/003: pedido por pergunta com `request_id` próprio, ledger no ato, nada confidencial.
- Nada move o gate. PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED. A leitura «gráviton = forma conjugada da luz» é [INPUT/ONTO] do operador; o que se prova é a álgebra.
- O relatório final da ordem (`ENTREGA_016_RELATORIO_FINAL.md`) continua devido **depois** da Parte B, e cita este pacote pelo sha256 do `PRONTO.json`.
