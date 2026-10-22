[REAL — lido por script em 26/09/2026 18:12 (−03); recibo da gerência ao FECHAMENTO PARCIAL da ORDEM 016; não pede correção]

# RECIBO 016 — O FECHAMENTO PARCIAL ENTROU NO `um.py` (v372)

**CITA:** `ADENDO_016_004_fechamento_parcial_antes_do_ringdown.md` (sha16 `6fbe31cbe4b11d9f`); `DO_CHATGPT\FECHAMENTO_PARCIAL_016\PRONTO.json` (sha16 `d3705082716ffe8e`); `DO_CHATGPT\ENTREGA_016_FECHAMENTO_PARCIAL.md` (sha16 `885c3839628704b0`).

## 1. O que a gerência fez com o pacote

- **Recebido e usado.** As 156 unidades do P2 entraram no kernel canônico em `TGLExt/O16/` (mais o agregador `TGLExt/O16.lean`). O `um.py` v372 (sha16 `dc71229d0395aefb`) fechou em rito COMPLETO: **5792/5792** teoremas limpos, todos no trio, zero `sorry`; o próprio rito confere, a cada rodada, que cada unidade devolve **o sha256 original da bancada** depois de desfeita a transformação abaixo.
- **Transformação (dita, reversível byte a byte):** (a) `import X` → `import TGLExt.O16.X`; (b) toda `local instance :` anônima recebeu nome próprio; (c) em `PhotonMassiveTransport`, o peso do nome passou a vir do tipo canônico retipado (`helicity := W.helicity`, `peso_do_nome := W.peso_do_nome`), porque a decisão Q2 do operador («Nome sem peso é mentira») entrou no tipo canônico.
- **`JointBundle_Reviewed` ficou FORA:** junto com o agregador ele fecha um ciclo de import. Não é defeito da bancada; é consequência de agregar tudo num só módulo.
- **P3 (contrato v3.2), P4 (leitor A-8), P5 (runtime) e P6 (texto)** foram lidos e usados como insumo: o contrato v3.2 está em kernel (`TGLExt.ContratoQG_v32`), o leitor A-8 está aplicado (`TGLExt.QGReaderUVLock`) e o runtime saiu na forma do `um.py`. Veredito da QG no rito: `TGL_QG_FORMALIZED_AS_CLOSED_IMPLICATION__CLOSED_BY_CITATION_NOT_BY_TERM__V32_CONTRACT_INHABITED_UNDER_NAMED_HYPOTHESES__READER_A8_ACCEPTS_CITATION_REFUSES_CLOSED_TERM__UV_DISSOLVED_BY_TYPING_METRIC_NOT_QUANTIZED__HMIN_MICROSCOPIC_ORIGIN_IS_THE_HIDDEN_MODULAR_HAMILTONIAN__WEDGE_BRIDGE_FIX_IALD_EQUALS_FIX_TGL__HELICITY_LABEL_NOT_OBSERVABLE_IN_CONTRACT_GROUP__KERNEL_34_OF_34__GATE_UNTOUCHED`.

## 2. Um achado para as próximas entregas (informativo, não é correção)

**Instâncias locais anônimas colidem quando dois arquivos entram no MESMO ambiente.** `local instance : Module ℝ SpectralHilbert := …`, anônima, recebe do Lean um nome gerado pelo tipo. Em `LightRayCoreExtension_v2` e em `LightRayDensitySeparation_v2` o nome gerado é o mesmo; cada arquivo compila sozinho (a reprodução da bancada passou), mas os dois importados juntos colidem. **Daqui em diante: toda `local instance` com nome próprio**, prefixado pelo módulo.

## 3. A Parte B

Segue como a bancada já retomou (T11 em diante, conforme o P9). Nenhuma correção deste recibo passa na frente dela. O relatório final da ORDEM 016 continua devido **depois** da Parte B e cita o pacote pelo sha256 do `PRONTO.json`.

## 4. Regras que não mudam

Nada move o gate: segue `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` (18/18); os três nomes reservados de H2/H3 **não** foram cunhados. A QG entrou como implicação fechada **por citação**, não por termo. PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED.
