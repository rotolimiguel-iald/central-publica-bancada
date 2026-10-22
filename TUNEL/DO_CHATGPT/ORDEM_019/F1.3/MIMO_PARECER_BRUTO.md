# REVISÃO CÉTICA INDEPENDENTE — F1.3 (ORDEM 019)

**Régua desta revisão.** Atuei somente sobre os artefatos textuais recuperados (`CONCILIACAO_F11_V376.md`, `GRAFO_DEGRAUS.md`, hit `TGLExt.Commutant.lean`, `ENTREGA_016_…` e a memória canônica). Não executei compilação, não li disco, não verifiquei hash, não movo gate, não afirmo prova física. Onde digo "verificar por script", é pendência local do verificador, não resultado meu. `NOT_FALSIFIED ≠ CONFIRMED`; nada aqui confirma a TGL.

---

## 1. Veredito

**Nenhum P0.** **8 P1** (bloqueiam ENTREGUE) · **7 P2** (correção de precisão/lexico). **Escopo aprovado condicionalmente** às correções P1, com a ressalva de que o "primeiro degrau factível" entregue é uma **auditoria**, não o descarregamento de um nó construtivo do grafo.

A separação de eixos F1.1×v376 está correta e é o mérito real do documento: as linhas `PkerK-rhoStar-PF`, `trace_tracial` e `core regular × core físico` estão **classificadas honestamente** e a frase *"não há identidade automática com `PF` físico"* está no ponto exato. Os defeitos são de **proveniência, de completude do grafo e de lexico**, não de conclusão indevida.

---

## 2. Os três pontos pedidos pelo operador

### 2.1 `P_kerK` — `ρ*` — `P_F` (cadeia de TRÊS elos, não de um)

A conciliação separa `P_kerK=ρ*_IALD` (por termo) de `ρ*↔PF_Takesaki` (SABIDO) — correto. O que falta é dizer que **a composição transitiva não está licenciada**: o elo 1 é `[REAL, termo]` *no objeto-luz*; o elo 2 é `[KNOWN, não tipado]`; logo `P_kerK → P_F` **não é teorema**. Acrescente-se o risco de homônimo, que é o cerne da pergunta do operador: **`P_F` aparece em dois registros distintos** — o canto dos Three Locks *finito* (v10, `τ(P_F)=1`, provado na face finita) e a projeção do *core* de Takesaki sobre II_∞ (semifinito, sem escala fixada). São objetos diferentes com o mesmo símbolo.

> **P1-1.** Trecho: *"não há identidade automática com `PF` físico"* (CONCILIACAO) e *"Transportar v351 somente por morfismo demonstrado"* (GRAFO).
> **Problema:** os dois `P_F` não são renomeados; a cadeia `P_kerK→ρ*→P_F` pode ser lida como fechada.
> **Correção mínima:** nomear `P_F^fin` (canto dos Three Locks, kernel, finito) e `P_F^core` (projeção do core físico, OPEN), e inserir no grafo o nó **"identificação ρ* ↔ P_F^core [OPEN]"** como obrigação explícita, não como corolário do degrau 6.

### 2.2 `trace_tracial`

A conciliação diz: *"A v376 mediu `trace_tracial` total sem consumidor"* e *"F1.2 instanciou `DualScalingData` no subcone finito v351, sem morfismo para o core Fock."* Correto e essencial. Dois ajustes: (i) a **tracialidade** do core regular (`scalarInverseLimitWeight_tracial`, na memória) está **provada na face finita**, enquanto a **escala de Takesaki** `Tr(θ_s x)=e^{-s}Tr(x)` entra como **DADO** (`DualScalingData`) — provado e dado não podem partilhar rótulo; (ii) `trace_tracial` sem consumidor **não pode ser consumido retroativamente** por nenhum nó deste grafo.

> **P1-2.** Trecho: *"Core, traço e escala | VINCULADO no `FockCertificate`; FECHADO no core regular v351"*.
> **Problema:** colapsa três estatutos (campo nomeado / tracialidade provada finita / escala importada como dado).
> **Correção mínima:** três linhas separadas, cada uma com o seu modo de quitação (`KERNEL`/`IMPORTED`/`OPEN`), e a cláusula *"nenhum consumidor downstream pode usar `trace_tracial`"*.

### 2.3 `core regular v351` versus `core físico` — **descompasso de rótulo**

> **P1-3.** Trechos: *"FECHADO no core regular v351"*; *"DualScalingData` no subcone finito v351"*; *"Transportar v351 somente por morfismo demonstrado"*.
> **Problema:** na memória canônica recuperada, **v351 é a oitava cláusula (`J M J = M′` na torre-produto)**; o **core regular** com traço e `DualScalingData` aparece em **A1(b)/A2 (v354–v355)** — `scalarInverseLimitTraceData : RegularCoreTraceData`, `regularLegacyCore : ContinuousCoreData`, `ContinuousCoreData` com ação dual e escala de Takesaki. O rótulo `v351` não casa.
> **Correção mínima:** não renumerar por memória; **reler por script** o ledger de F1.2 e citar o **hash do artefato** que sustenta "v351". Se não houver, corrigir para A1(b)/A2 (v354–v355). Proveniência errada em peça que o operador nomeou é bloqueio de ENTREGUE.

---

## 3. P1 restantes

**P1-4 — O "primeiro degrau" não descarrega nó nenhum.**
> *"Conferir, por compilação numa cópia, a fiação de `LightOneParticleByTerm.U1_continuous/null_no_eigen` a `LightNetData.toLightOneParticle`; declarar os demais campos ainda como entradas."*
É **auditoria de fiação**, não construção da rede/Fock/Tomita. O critério da unidade pede "o primeiro degrau factível" do grafo de dependências; este é factível, mas **não é nó do grafo**.
*Correção:* rotular como **D0.5 — auditoria (não descarrega nó)** e declarar **degrau 1 construtivo = instanciamento da rede padrão física**, mesmo que o custo seja meses.

**P1-5 — "declarar os demais campos ainda como entradas" é ambíguo e perigoso.**
Sob a regra do modo de quitação (v253) e a lição v292 (`ConverseClauseContract`: tipo sem habitante ≠ assunção consumível), "entradas" pode virar premissa silenciosa.
*Correção:* *"contratos tipados sem habitante, bandeira `gpf_`/`gpi_` **apagada**, nenhum consumidor downstream os trata como provados"*.

**P1-6 — Ausência de citação na face.**
A regra v253 exige *"autor, ano, periódico"* para tudo que é importado/citado. A tabela inteira usa nomes de flag (`PhysicalPhotonNetContractMeasured`, `PairTomitaAnalyticRealizationMeasured`, `H_modular_equals_geometric`) **sem uma única referência bibliográfica** (BW 1975/76 *JMP*; Reeh–Schlieder 1961; Tomita; Takesaki 1970 *LNM* 128 / 1973 *JFA*; Connes 1973; Araki–Woods 1968 *Publ. RIMS* 4). *Correção:* uma citação por linha IMPORTADA.

**P1-7 — Grafo omite o bicomutante/`J A J = A′` e o tijolo já existente.**
O `TGLExt.Commutant.lean` (hit vivo) declara-se *"o primeiro tijolo do bicomutante finito (Degrau 1) e, adiante, do Tomita-Takesaki finito (Degrau 0)"* — e a **oitava cláusula é justamente a versão-torre de `J M J = M′`**. O grafo de dependências passa direto de "Tomita físico" para "BW" sem nó para `JAJ=A′`/bicomutante, nem para a parede conhecida da oitava cláusula (distributividade falsa em geral). *Correção:* inserir o nó e reaproveitar `TGLExt.Commutant` como base.

**P1-8 — Custo: dois registros inconsistentes, e lexiço `[INPUT]` usado para prazo.**
> *"[INPUT — ORDEM 016] A gerência estimou ≥400 h…"* contra a tabela (*"dias"*, *"meses"*, *"meses mais semanas"*, *"semanas a meses"*).
≥400 h ≈ 50 dias úteis; a soma dos passos é ordens de grandeza maior. Além disso `[INPUT]` no lexicão da casa designa **valor científico declarado** (α, τ★, G), não prazo de trabalho.
*Correção:* reconciliar (400 h é piso já excedido? esforço ou tempo de calendário?) e usar `[ESTIMATIVA/GESTÃO]` para prazos, reservando `[INPUT]` aos valores.

---

## 4. P2

1. **Definição de classe heterogênea.** *"VINCULADO = campo Lean nomeado sem habitante físico"* mistura dois bits. Um campo nomeado pode **não ter habitante nem formal**. Separar `habitação formal?` × `habitação física?`.
2. **Colisão de numeração de degraus.** `Commutant.lean` já fala em "Degrau 1/Degrau 0" com outro sentido; prefixar `F1.3.D#`.
3. **"Tomita VINCULADO (`J`, `tomita`, `flow`)"** deve dizer: *contrato da casa; Mathlib não fornece* (`StandardSubspace.lean:42` TODO). Senão o leitor lê que o Mathlib dá Tomita.
4. **Passo 4 omite a parede analítica nomeada da casa**: `[OPEN, ANALÍTICO]` — `S` fechável e `Δ` auto-adjunto positivo como operadores **não limitados**. É sub-obrigação do degrau de Tomita e deve estar no grafo.
5. **Passo 6 funde "construir/importar"** — modos de quitação distintos (v253). Separar 6a (`IMPORTED`, `gpi_`, com ponte nossa + citação) e 6b (`KERNEL`, `gpf_`).
6. **"Reaproveitar A1/A3/D4 do inventário"** — itens não presentes nos trechos recuperados; **lacuna declarada**: não posso conferir o que sustentam. Exigir hash/linha do `INVENTARIO_BANCADA` §3–§4.
7. **"A integração de 12 fontes em 12 GiB não satisfaz retroativamente a meta histórica de 8 GiB"** — semântica ambígua (12 GiB *excede* 8 GiB). Citar a frase-fonte da ORDEM 016 ou cortar.

---

## 5. Factibilidade do primeiro passo no Mathlib pinado

**Sim, factível — e por motivo que precisa ser dito**: o passo 1 **não consome Mathlib**; é checagem de compilação de termos da casa (`TGLExt`). O `Commutant.lean` recuperado já é algébrico (`Ring A`), sem `sorry`/`axiom`. Os pinos declarados (*"Lean `leanprover/lean4:v4.31.0`, Mathlib `fabf563…`"*) e o TODO de `StandardSubspace.lean:42` **não pude verificar nesta sessão** — devem ser relidos por script no rev pinado antes do selo; se o TODO já tiver sido preenchido nesse rev, o custo do degrau 4 cai e a estimativa muda. Nomes (`LightNetData.toLightOneParticle`) exigem grep antes de qualquer alegação de fiação.

---

## 6. Escopo aprovado (condicional)

Aprovo, **após** as correções P1-1…P1-8: (a) o eixo duplo F1.1×v376 como retrato conciliatório; (b) a separação `P_kerK` / `ρ*` / `P_F` e a recusa de identidade automática; (c) a recusa de transportar o core regular ao core físico sem morfismo demonstrado; (d) a ordem das dependências rede→Fock→RS→Tomita→BW/KMS→core→P_F, **acrescida** dos nós em falta (bicomutante/`JAJ=A′`; identificação `ρ*↔P_F^core`; parede analítica de `S`/Δ; tipagem III₁/Connes como obrigação nomeada — hoje `TGL_BOUNDARY_TYPE_UNDECIDED_IN_KERNEL`); (e) a estimativa de risco, dita como estimativa.

**F1.3 não deve ser marcada ENTREGUE como está.**

---

## 7. Pendências (sem execução aqui)

Reler por script e anexar: hash dos pins; linha exata do TODO de Tomita; existência dos nomes `LightNetData.*`; artefato/hash que sustenta "v351" para o core regular; conteúdo da ressalva **O16** (ausente dos trechos — não avaliável); texto-fonte de ORDEM 016 (≥400 h e a cláusula 8/12 GiB); itens A1/A3/D4 do inventário. Definir, por decisão do operador, se a numeração de degraus do plano convive com a do `Commutant.lean`.

*Não afirmo prova física, não movo gate, não houve execução nem verificação local por esta revisão.*