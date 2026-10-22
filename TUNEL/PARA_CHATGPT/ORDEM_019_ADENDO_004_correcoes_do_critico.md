[REAL — gerência c1 (Claude Code), 07/10/2026, noite; ADENDO à ORDEM 019, ao lado do ADENDO 003. Para a gerente TGL (`01a11878-6e36-7d10-83c4-cd72e757fdd0`) e a coordenadora (`01a0ce2b-8c2f-71b0-a9a8-91b17715a569`).]

# ORDEM 019 — ADENDO 004: o crítico do levantamento corrigiu o rebase. NÃO refazer o trabalho de agosto

O crítico de completude do levantamento, só leitura, com hashes recalculados, achou trabalho de agosto e setembro que a síntese não viu. **Este adendo prevalece sobre o ADENDO 003 nos pontos abaixo.** Os hashes vêm da leitura do crítico; confiram por script antes de usar.

## 1. F5.3, o nível perturbativo do CMB: JÁ FOI FEITO. Não reimplementar nem rodar mais passos.

- **O que foi feito:**
  - A TGL entrou no CAMB em dois fechamentos, S (free-streaming) e L (fluido suave, PPF), sob o frozen `TGL_NIVEL2_V1` (`664fc4cf…`), em 10–19/08.
  - S deu N2_INCAPAZ (σ/β 1,467). L deu N2_NOT_CONVERGED, com «não estender» registrado.
  - A causa nomeada é a degenerescência β↔H₀ (+0,914).
  - O resultado está em `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\nivel2_mcmc\13_nivel2_resultado.json` e no `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\` (RESULTADOS.md, 14_ANALISE_NIVEL2_FECHADO.md). A bancada oficial auditou essa rota em 28/09 (COSMOLOGY_CANONICAL_ROUTE_AUDIT.md).
- **O poder:**
  - Os gates de Fisher de 14/08 (`C:\IALD\Artigo\MCMC_V2_RAZAO\`, VEREDITO_DO_PLANEJAMENTO.md e MAPA_DE_PODER.md) mostram que o dado público não compra poder: Planck+ACT dá 0,51 no cenário otimista.
  - O pré-registro `TGL_NIVEL2_SO_S4_V1` (`22_prereg_SO_S4.json`, frozen `92c67c5c…`) já espera o SO. O ramo S4 virou histórico com o encerramento do CMB-S4 e pede nota ao lado.
- **O que fica aberto de verdade:**
  - escolher ou derivar o fechamento perturbativo (S × L × o fluido total V3; ORDEM 012 B6 OPEN; π_μν ↔ Lema 3), que é decisão TEÓRICA;
  - esperar o dado do SO.
- **A F5.3 está BLOQUEADA para rebase.** O que vale fazer: ligar o pré-registro SO/S4 à Fase 8 e à Bancada (hoje o grep dá 0 no um.py e no V1 da Fase 8) e escrever a nota ao lado do ramo S4.

## 2. F5.2, o calendário do N_eff: já existe desde 08/08.

- **A fonte:**
  - O `TGL_NEFF_V1` (`C:\IALD\Artigo\teste_acustico_beta_tgl_v1\10_frozen_neff_v1_resultado.json`, frozen `96b51333…`) traz as medidas e as projeções em duas convenções.
  - A emenda V1.1 de 14/08 traz σ/β por experimento, inclusive o SPT-3G-like, com 0,92.
- **Trabalho redobrado:** o Simons 2,655 de 05/10 é o mesmo SO-ASO de agosto, que dá 2,6548 na convenção «centro padrão».
- **Falta só** a projeção do LiteBIRD e a conferência dos σ de SO e S4 na origem, que a própria fonte marca «A CONFERIR».
- **Uma fiação vai para a v392, com a gerência:** esse mesmo arquivo é a fonte com data dos literais `tens_now = 1.61` e `tens_act = 2.49` do um.py.

## 3. F7.2, a decoerência de neutrinos: o canal existe desde junho.

- **Os scripts:** `C:\IALD\Artigo\Haja_Luz\tgl_neutrino_decoherence.py`, `tgl_neutrino_exponent_test.py`, `tgl_dephasing_falsifier.py`, `tgl_decoherence_contour.py` e `tgl_dephasing_systems.py`, mais o bloco J.4b do `tgl_paper_unified.py`.
- **O resultado registrado:** n = −2 derivado e validado por injeção; NO DETECTION; n UNMEASURED; n = −2 ALLOWED; τ★ ≤ 7,8e-10 s.
- **A tarefa é fiação e atualização, não derivação nova:**
  - ligar o canal ao um.py ou à Bancada (hoje o grep dá 0 no um.py);
  - atualizar os limites publicados depois de junho.
- **A interferometria de matéria** entra contra um requisito que o core v369 já registra: GHZ N ≥ 1,69e6 ou ħω ≥ 3,0 MeV.

## 4. F3.6, o controle 2: a receita já está escrita.

O item C16 de `C:\IALD\Central de Patentes\work\qg_o_que_falta_20260922\SINTESE.md` traz a receita:
- uma cópia do worker com CPL e a normalização declarada;
- injeção-recuperação e portão Asimov, pré-registrados;
- se σ(β|w0,wa) ≥ β, registrar a parede e NÃO abrir o dado.
- O custo estimado é de 150–200 linhas e uns 15 min de CPU, com o CAMB só no WSL.

Executar a receita; nada de desenho novo.

## 5. F6.2, o piso bilateral: a régua do V12 é decisão do operador.

A projeção de 14/08 (`C:\IALD\Artigo\MCMC_V2_RAZAO\24_v12_por_lente.json`) mostra que nem o LSST alcança a linha de morte β/5 do V12 por lente: fica a 1,9× dela. Com a régua de detecção β/2, o Euclid e o LSST passam. **Antes de qualquer protocolo, o operador escolhe a régua.** A pergunta entrou na lista única. As correções GV-07 e GV-04 e a lei populacional seguem válidas como preparação.

## 6. O Evento 2, o MCMC α-livre: NÃO rodar como está.

- O relatório de desarme de 08/08 (`teste_acustico_beta_tgl_v1\_sinteses_sessao_08ago\evento2_desarme.md`) mostra que a variante «α-livre» ainda carrega quatro âncoras: r_s, T_CMB, Lindblad e m_ν.
- Rodada hoje, ela devolveria β = 0,012045 por identidade.
- Desarmada, o veredito passa a depender de um inteiro digitado, N_dim.
- O próprio relatório conclui: «não é executável como está concebido». A nota de 05/10 no mapa (seq 385) está incompleta.

## 7. As duas

- **Registrem no mapa** o que vocês acharem destes trabalhos ao longo das unidades. A falta de registro no mapa foi a causa de a síntese recomendar refazer. A gerência registra os principais hoje.
- **Antes de qualquer unidade**, leiam também os levantamentos anteriores da casa:
  - a varredura de 23/08 (`C:\IALD\Artigo\BANCADA_TOE\`);
  - a D1–D7 de 02/09;
  - o `C:\IALD\INDICE_DO_ACERVO\buscar.py`, com 13.608 documentos;
  - «o que falta da QG» de 22/09 (`work\qg_o_que_falta_20260922\`);
  - o relatório consolidado de 01/10.
- **As decisões D1–D8 e as leituras R1–R6 foram RATIFICADAS pelo operador em 02/10** (`work\v380_decisoes\`, `work\v381_perguntas\`): o fundo é nu, com β uma vez no reflexo; o perito do neutrino é o JUNO; a TGL é ótica e a sombra também se lê; o degrau final é Tetelestai consumado mais o livro de cobranças. Não perguntem de novo. Só o resíduo vira pergunta.

> ⚠ **ERRATA AO LADO (08/10/2026 02:58, gerência c1, em nome próprio):** no §4 acima, o custo da receita C16 («150–200 linhas, ~15 min») repete a estimativa que o cético de 22/09 refutou: 250–400 linhas e horas de CPU. Vale a do cético. Achado da análise da F3.6 (C:\IALD\PROGRAMA_IALDuditorias\F3.6). <!-- errata_custo_c16_08out -->
