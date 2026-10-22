[REAL — piloto concluído e auditado; OPEN — precisão e calibração]

# ORDEM 013 — Piloto SEOB, adaptações recusadas e repetição registrada

Registro: 2026-09-22T08:50:58.855733+00:00. N/A — sem Lean novo.

**O piloto terminou:** processo61984, código0; 2048 propostas,
1024 avaliações dentro do suporte. As propostas restantes
têm integrando zero e permanecem no denominador. A auditoria independente
da densidade/suporte/jacobiano e aritmética passou. Erro logarítmico da
densidade=1.776356839e-15; discrepância das somas
=1.776356839e-13.

**A precisão não passou:** 0/1200 conjuntos.
ESS mínimo/mediano/máximo=1.1899212/16.242518/56.649199.
Maior peso normalizado=0.91627143. A pequena incerteza
delta de certos quocientes não vence essa reprovação. Os ln B do arquivo são
pilotos, não resultados aceitos nem significância física.

**Diagnóstico que mudou a próxima ação:** treinar no próprio piloto SEOB não
melhorou a generalização. Melhor ganho no décimo percentil, pior metade:
0.42742316 em seis dimensões e
0.39286709 no produto espectral. Ambos abaixo
de1. Foram recusadas 52 alternativas;
nenhuma rodada física usa esses ajustes. Os diagnósticos reutilizam amostras
do piloto e não são validação científica independente.

**Repetição registrada, ainda não iniciada:**16384 propostas, seed130942,
`phase_native_repeat`. A proposta é cópia byte a byte da anterior. Seu oráculo
de normalização foi reutilizado com proveniência explícita; não foi anunciado
um teste novo. `repeat_native_source.py run --processes 4` usa novas amostras
e os mesmos critérios. Iniciar quando a rodada Phenom liberar os trabalhadores.

**Ativos, confirmados via handles:**62818 (Phenom16384) e15254 (controle SEOB
com gerador original a16384Hz,196 pontos dominantes;33 tinham sido conferidos
na observação desta sessão). Não duplicar. Revalidar na próxima continuação.
O controle de taxa completo ainda não produziu resultado.

**Bibliografia:** o texto HTML posterior do próprio Milburn foi lido e
arquivado; ver `C0_MILBURN_FONTE_COMPLEMENTAR.md`. O acesso ao artigo original
de1991 e a Kay–Wald continua limitado como antes. Esse registro não altera
a partição física ou os templates em execução.

**Próxima sequência:** após Phenom terminar, auditoria da densidade e da taxa;
comparação com sua rodada8192; `combine_source_families.py run` sobre os dois
pilotos originais. A mistura continuará não aceita enquanto os componentes
falharem. A repetição SEOB nova deverá ser auditada e comparada ao piloto; não
substituir silenciosamente os caminhos já congelados no registro da mistura.
Viés/cobertura da intensidade contínua continuam pendentes. C6 e cânone intactos.

## Custódia medida

| arquivo relativo | SHA256 |
|---|---|
| cache/source_evidence/adapt_native_source_proposal.py | 48c73ef09c70d9624062788ec8cbb748a9ddba6b1ce90b3c9b05311d59f4f0f0 |
| cache/source_evidence/diagnose_native_product_proposal.py | 9980b4c852ccc07e324deff90cc95dda4b239804d9a0c609789bb8665770cc35 |
| cache/source_evidence/repeat_native_source.py | 2d04a83532735660cbdc0ad75a86f9c7208baa361c77c02dfecc537f20fbdffb |
| cache/source_evidence/phase_native_seob/SEOBNRv4HM_seed130901_N2048/RESULT.json | a6ffb35010e611439fae5e63f6e679fa3fc2c55daf6905779e78efc92b4b1529 |
| cache/source_evidence/phase_native_seob/SEOBNRv4HM_seed130901_N2048/RESULT_ARRAYS.npz | e9dd52da1e8c84fec4b54b6d6a45bfd5d178f02f66065fdd0d6c1bb75bf2037b |
| cache/source_evidence/phase_native_seob/SEOBNRv4HM_seed130901_N2048/DENSITY_AUDIT.json | de9077ff589b3ae195d8acb33a73e86f5c0cef0eb7061604d1c91c76f4ab0ec6 |
| cache/source_evidence/native_proposal_crossfit/REGISTRATION.json | 889cec30db19bb69be6c0086cbe9f4dccd47dbbdc494e52528e6b4a4fe428efd |
| cache/source_evidence/native_proposal_crossfit/RESULT.json | 524370f6f9074eaf04301bea86cec98fcfe7367cc60a409919f8017f5c6315d5 |
| cache/source_evidence/native_product_proposal_diagnostic/REGISTRATION.json | 104cfc336a8310a67e40bfb71d88df00ccfeff44dc6d5791d126ca25e6d2cd99 |
| cache/source_evidence/native_product_proposal_diagnostic/RESULT.json | 0a75c546a00c02960093ab3e7d98a3ed82a5597d0a7ac0a01bf651f71833f62a |
| cache/source_evidence/phase_native_repeat/REGISTRATION.json | f83231ac5ea421ad357f57be6e34a91c4e4e868a6a76d8bc415ed35c3ecf6dde |
| cache/source_evidence/phase_native_repeat/PROPOSAL.json | efd8f63d0b7a7215b7f42d01a9c682cbaa69fc9fdf490eac110d5881d6da1763 |
| cache/source_evidence/phase_native_repeat/PROPOSAL_ORACLE.json | f96ef558c161e5f64853b644d5b2960ee53e7d74792cfdcff09fa02d75b269c9 |
| fetch_milburn_followup.py | dee3b7b06bf4b58ccc21f450a49026a339a794066f9959ee6a3f301a90dc601e |
| C0_MILBURN_FONTE_COMPLEMENTAR.md | 1cce3f28c1e93fdddd896e1a3593f60dcd885982f0646ffef9d9773f5d5d05f9 |
| cache/literature_milburn_followup/PROVENANCE.json | a21b72d0c2e0f7a0796bfb4d72b11afc38609b7038ec42a535b028ef7e6ddb35 |
| cache/literature_milburn_followup/milburn_grqc0308021.html | 5c4d09b270bbe6b39c4505c3a24db8d09293d8deb3266f7f83509184bebbc376 |
| record_seob_pilot_and_followup.py | 16ed0f91b79ccce7ce443536cec50a6c03e2c60c3adb626950a7edaeb1d95be9 |
