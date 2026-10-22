[NÃO-CEGO — E0 PAGO como portão de planejamento; calibração sistemática NÃO PAGA; nenhum teste físico]

# Portão da ampliação V1

Todos os números abaixo são cálculos condicionais de planejamento. Offset fixo em zero: **PROIBIDA_COMO_TESTE**. Dez leituras em paralelo; nenhuma escolhida. RG permanece limite clássico.

Fonte de largura: DP dos posteriores completos, ddof=1. Previsão E0 em medianas separadas; a marginalização conjunta pertence a E1. Controle q90 e QNM exato preservado no JSON.

N90/N50 = 1.57831560282; I = Σ1/σ². I90 depende da distribuição conjunta de δ e σ. A referência 1/0,058² é unidade fixa de informação, não corte de seleção.

| Leitura | z de sinal, 31, calibração | I90 condicional | N90 mistura ilustrativa | z tendência, intercepto livre |
|---|---:|---:|---:|---:|
| R-A | 1.0514e-40 | OPEN/nulo/subresolução | OPEN/nulo/subresolução | 2.09946e-41 |
| R-B | 0.606334 | 95216 | 3327.15 | 0.0484826 |
| R-MOD | 1.07645 | 30209.4 | 1055.61 | 0.158487 |
| R-RAIZ-0 | 1.11998 | 27907.2 | 975.164 | 0.0540716 |
| R-RAIZ-EP4 | 1.0514e-40 | OPEN/nulo/subresolução | OPEN/nulo/subresolução | 2.09946e-41 |
| R-RAIZ-REST | 4.85657e-81 | OPEN/nulo/subresolução | OPEN/nulo/subresolução | 1.89281e-81 |
| R-RAIZ-COHERENT | OPEN/nulo/subresolução | OPEN/nulo/subresolução | OPEN/nulo/subresolução | OPEN/nulo/subresolução |
| R-LIN | 2.1585 | 7513.27 | 262.537 | 0.100126 |
| R-GLOBAL | 0 | OPEN/nulo/subresolução | OPEN/nulo/subresolução | 0 |
| R-PROP | OPEN/nulo/subresolução | OPEN/nulo/subresolução | OPEN/nulo/subresolução | OPEN/nulo/subresolução |

Os conjuntos 33, 39 únicos e GWTC3 18/10, o falsificador espúrio inclusive RG e os controles constam integralmente do JSON. N astronômicos de efeitos subresolvidos ficam como aritmética histórica; alvos operacionais permanecem null.

**Qualidade [INPUT adotado nesta etapa]:** SNR de rede GWOSC ≥12, mediana GR Mf,det ≥40 M☉ e 0≤χf<0,98; prioridade SNR≥30. Nenhuma largura de posterior decide admissão. GR full-IMR é anterior ao teste de deformação, não inspiral-only. χ_eff não substitui χf. Ausências aguardam metadados sob a mesma regra.

Na cobertura atual, O4b: 45 com SNR≥12; 44 têm Mf/χf na tabela GR; 27 passam o INPUT, 17 ficam abaixo, um aguarda. O4a e O4c precisam completar metadados. Não se afirma que todos são elegíveis nem que strain foi baixado.

Ajuste: mediana σ = 4.12311785 SNR^(-0.944999805); dispersão ln=0.225092187. E[1/σ²]=exp(−2μ+2s²), diferente do inverso da mediana². As diferenças contra 3,03/−0,86 vêm de fonte do SNR **e** definição de largura; tabela 2×2 no parecer independente.

**Condição sistemática:** FALSA para admissão em todas as leituras com efeito definido: σ(c_calibrado) ainda não medido na pipeline exigida. Pisos |δ|/5 e |δ|/15 separados; null não é zero. A matriz recalculada de controles C5 e a revisão independente estão vinculadas por hash.

**Rota IV:** poder condicional ≥90% nos candidatos aprovados por IC simultâneo: N=61/39/22 para largura GW250114; 1588/996/524 na mistura31; 1696/1144/594 na mistura33, para jitter 0,019/0,0228/0,030. Menor aprovado de três candidatos, não mínimo inteiro. As duas tentativas falhas da mistura33 sobrevivem. Cauda nula de 5σ, transferência e σ_sys continuam OPEN.

**Taxas/cenários:** Poisson central90 condicionado ao universo publicado e à exposição declarada. SNR≥78 é proxy de metadado, não precisão garantida. O5 tem bandas históricas BBH, controle de PSD e teto BNS distinto. Ganho de qualidade mais volume é hipótese otimista; controle de qualidade invariante separado. ET/CE são cronogramas e populações projetadas, não promessa de anos.

C4 permanece herdada, NÃO-CEGA, com correção/σ e veto relativo à RG. Nenhum número de planejamento muda seu veredito ou o gate. E0 não é o registro E2, e nenhum posterior de teste foi lido.

Reprodução: executar os produtores documentados em cada recibo apenas em novo destino; este assemblador recusa substituir arquivos. N/A — sem Lean; zero teoremas. Tentativas e revisões preservadas.

## Fontes e recibos

JSON desta entrega: `710028a7d2af7b649511afe369d88462d2add95c5fecbb1fb03c517fc91fe8a0`.
- `bis/e0_core/E0_CORE.json` — `ce5fa2f3bfc985138e5c3a20116b93791a84f8034df3c42ce3ce2781fb7e26be` (592549 B)
- `bis/e0_core/DATASET.json` — `89d39541bd9a43f00720bda7b76886a0ee97658749c360682cb6e671c38ec7c0` (462205 B)
- `bis/e0_core/SYSTEMATICS_ADENDO.json` — `d1ed739909f00e1dba2e39474fccc46fc92480d6e27e5c74c91f3853bf677df0` (2246537 B)
- `bis/E0_SYSTEMATICS_REVIEW.json` — `2c001d14ce7a117bfab31f2d848eaf9954f2828bf888a068e9a3a951dd8980c7` (1179 B)
- `bis/E0_CORE_SCALAR_REVIEW.json` — `14c1f136ba351ddcb4dc8432ad7d06c96dc65adb0b60fbe583a03528a2a0e3d5` (6615 B)
- `bis/E0_SNR_INFORMATION_FIT.json` — `98bc0408e7fec14a6a6c0ad0ef232b859ff277c408e581cbe6206aac8cb2f0f6` (48947 B)
- `bis/E0_SNR_FIT_REVIEW.md` — `df95b7567c2f07dfcaabbd5b38b1c4a1a7cbeae510c37d011c7252ef0a3cfc0e` (5727 B)
- `bis/E0_ROUTE_IV_POWER_v2.json` — `ae457e82c8c18b5cccf47d60c785d82b3ec3888db7975f2184666c558e4ddd93` (71029 B)
- `bis/E0_ROUTE_IV_VALIDATION.json` — `047554eb39c332a9b19190d241a5c34de2e16293074c5aca500ae00f4e3d1c42` (10683 B)
- `bis/E0_ROUTE_IV_VALIDATION_PLAN.json` — `908727da18cb48a28fcb12f07c9578764af2f266aa08d8ba406735fb18c7fc55` (4978 B)
- `bis/E0_ROUTE_IV_PROVENANCE.json` — `99ace27f2cc10527a52d50230a91fe7fc110d9545365503dbe720340922ef215` (3564 B)
- `bis/E0_MC_GUARD_CLOSURE.json` — `3bcb7b435b971df182116f6037fcd5ea96c3c514d31a2256e599ad491947809b` (6786 B)
- `bis/E0_ROUTE_IV_INDEPENDENT_REVIEW.md` — `64f76106e7e207c96188cec3c7bd46d157c43a0b2b91804eae0ce24c07fc6dde` (10164 B)
- `bis/e0_metadata/GWOSC_INVENTORY.json` — `b5860044f456d5d5332801803c188be09ab7d6d1c231c0a6aaeacce17f8750ce` (897502 B)
- `bis/e0_metadata/GR_METADATA_DRAFT_REVIEW.json` — `edd3193f3c1256f495d1b31c43619fcdcfaee5bbca3002d90f138a60ac7dfb7a` (183510 B)
- `bis/e0_metadata/GR_METADATA_DRAFT_REVIEW.md` — `d2a469219caba17fcd9e862f7f21bdc7654856b4f4fdb0a8c511dbba4a05dd96` (3629 B)
- `bis/e0_metadata/SCENARIOS_AND_SCHEDULES.json` — `130eac06dbd38b0665cd98b9861212ae8a8fc60a4b1c6d8835d6d6a47639bf4c` (6510 B)
- `bis/e0_metadata/SOURCE_LEDGER.json` — `1ee18d3facb6ea238d1d9e776393778b54a771c03cc9fa5037fa302ef544818d` (22000 B)
- `bis/E0_RATE_O5_SCENARIOS.json` — `416b45cd9db34709cef6e33a85c3c78a2a4dc147166f62cf24e824198fdc02d1` (103836 B)
- `bis/E0_RATE_O5_INDEPENDENT_REVIEW.md` — `f95a94e8ef838d00b7d637af918ee0ca39c2517cca50c527f51aa37fe41f6bb8` (5632 B)
- `bis/PART_B_BUDGET_START.json` — `2b3cfefd17cb8f3df845172a3b41f6e457b92b2c5bb164128aa0b40e8919355f` (1536 B)
- `C1_LEITURAS_v4.json` — `126270a896d8589870954b209155f26a8b08295839b31e0e9a6e28e512621980` (35419 B)
