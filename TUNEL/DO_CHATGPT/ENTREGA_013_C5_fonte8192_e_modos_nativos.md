[REAL — resultados e implementação conferidos; OPEN — precisão da evidência integrada]

# ORDEM 013 — Encerramento da rodada8192 e modos nativos

Registro: 2026-09-22T07:30:29.851494+00:00. Axiomas: N/A — sem Lean.

**PAGO:** rodada8192 concluída, 4299 avaliações no suporte; as demais
propostas têm integrando zero e continuam no denominador. Auditorias de densidade e
aritmética concluídas. O controle8192→16384Hz em pontos dominantes deu máximo
|ΔlogL|=0.015231062348448177; não é cota uniforme do posterior.

**NÃO PAGO:** zero das1200 razões atinge a precisão registrada. Quantis ESS:
[1.0881740365454493, 8.282652919492387, 15.31115697461153, 25.68379858214803, 73.57686504006874]. A eficiência mediana por proposta passou de
0.0028292416 para 0.0018690377.
Portanto a mistura de três componentes não resolveu a eficiência. Em
300 casos |ΔlnB|>0,2 contra o piloto2048;
máximo=1.0942384. Erros Monte Carlo de baixa ESS
podem ser subestimados; não promover médias/quantis a resultado científico.

**PAGO:** correção do pico comum testada em504 controles, zero falhas;
erro máximo de logL em SNR40/600=[3.183231456205249e-12, 6.693881005048752e-10].
São três fontes de referência e quatro pontos do prior, não prova uniforme.

**PAGO:** reconstrução direta dos modos SEOB verificada em18 casos,
erro relativo máximo=1.5814399506254759e-16, fonte90/8192Hz.
A tentativa anterior falhou e está preservada. A cópia corrigida usa a rotação
de polarização explícita no LAL e as mesmas conversões SI do PyCBC.

**DIAGNÓSTICO:** fonte oficial da versão instalada mostra que, para fonte90,
8192 até131072Hz mantêm a mesma malha interna. A taxa262144 realmente a refina.
Isso motiva o próximo controle, mas ainda não demonstra a causa única do erro.
Código consultado: https://git.ligo.org/lscsoft/lalsuite/-/raw/2c00d8c200308422036d0a23b7c0394f7c73faad/lalsimulation/lib/LALSimIMRSpinAlignedEOB.c (commit e SHA conferidos).

**CONTINUAR:** validar um adaptador de banco de fase via modos nativos contra a
API original; então testar131072/262144/524288Hz com malha interna medida.
Não repetir a mistura8192 sem diagnóstico/adaptação. Faltam precisão/repetições,
recuperação SEOB integrada, demais leituras/SNR, viés/cobertura de intensidade
contínua e atualização do pacote. C6 e fontes canônicas preservados.

O identificador41895 deixou de existir; não há processo vivo registrado aqui.
Comandos já concluídos: refine_ringdown_proposal.py; audit_registered_transport.py
--stage phase_ringdown_regularized; audit_phase_source.py com --rate;
compare_phase_runs.py; validate_stable_phase_prior.py; direct_seob_modes.py.
Arquivos/resultados são create-once; reprodução deve usar diretório separado.

## Custódia medida

| arquivo relativo | SHA256 |
|---|---|
| cache/source_evidence/phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/RESULT.json | 240e6e53bb0451ba7bafdc9fd24f661cb5c3e01310d005422894c52ae85f885a |
| cache/source_evidence/phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/RESULT_ARRAYS.npz | 1b05254d33eb1a57c3983f012d5b1eb0b838a69455ca43d5896cca709f0dd6b0 |
| cache/source_evidence/phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/PROPOSALS.npz | 2d4303d3b5bb9524149c3dca765917154ccce5d46db7378dae6d917ffd8b02ab |
| cache/source_evidence/phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/DENSITY_AUDIT.json | 9bd3d7d9946f0884a48963f4b220a8120f460bf67c0e60efa7f13fd81fcf9b17 |
| cache/source_evidence/phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/AUDIT_RATE.json | d8acd65b6bcf40754e4e2e68476d6c0e14d2801bb99dd8912af90ee776b74b64 |
| cache/source_evidence/phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/PROPOSAL_COMPARISON.json | e04e919f7f2721ae3fc15efe0a3f88c61c2c61cc03da56e33547b423b67882a1 |
| cache/source_evidence/stable_phase_prior_controls/REGISTRATION.json | 33b4b8b58f14f0aa39fac4a809da61e40300693f6ca5bbdb2d1d07e9539504b6 |
| cache/source_evidence/stable_phase_prior_controls/RESULT.json | 5c18212d2435a7fd005ac3d1d0367458753aab4569566cfdb3b24cdebec01dcf |
| cache/source_evidence/DIRECT_SEOB_MODES_VALIDATION.json | 741fafedbbc29cf6cfe2a951aac1137c5dd10db17c033ed9153ffb162a80d410 |
| cache/source_evidence/DIRECT_SEOB_MODES_CORRECTED_VALIDATION.json | ea05dc1dbe614b54961062c302ad97b9a5cd852a969de8fbf4addfa349b1438e |
| cache/source_evidence/direct_seob_modes.py | 7cb9fd39298dd8f6dbedbf436ae42137d54a44287003a01b0e342456c8187415 |
| cache/source_evidence/LAL_INTERNAL_MESH_AUDIT.json | 95d4533c3ac5c30cd43635541dce3b2ac4b59b0d9622564e1e36af1ff2af88d9 |
| cache/source_evidence/lal_generator_source_gitlab/LALSimIMRSpinAlignedEOB.c | 6b7969bb7cbe714c4937a691838b0b82a7fcc2a199c03ee2bf5215738f1ce1b3 |
| cache/source_evidence/lal_generator_source_gitlab_LALSimInspiralGeneratorLegacy/LALSimInspiralGeneratorLegacy.c | 87a5562ec7c1c411e068e96fc31c5214049b7b3cdecd350aeb68ea33b24bfdc9 |
| record_completed_source_and_modes.py | d37520a2125989f43b5ed397136b4ec14650d82605b4336d002c94aed04011be |
