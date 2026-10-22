[REAL — controles numéricos; OPEN — evidência integrada e calibração científica]

# ORDEM 013 — Malha interna medida e nova amostragem

Registro: 2026-09-22T07:45:16.709680+00:00. Axiomas: N/A — sem Lean.

**PAGO:** o adaptador de modos nativos reproduziu a API anterior em180
controles: três fontes de referência e dois pontos de prior,8192/16384Hz,
deslocamentos de pico de ambos os sinais, três fases externas ao banco,
a=0/0,37/1, O4/O5. Erro relativo máximo=6.2210712098656472e-16;
erro de logL máximo em SNR40/600=[2.9558577807620168e-12, 6.402842700481415e-10].
O pico é exatamente o da API anterior nos casos testados. Não houve troca
de família SEOB, perda de modos nem alteração do prior.

**PAGO:** na fonte90, a malha interna foi de fato refinada com taxas de saída
131072/262144/524288Hz. Razões dos passos medidos=[2.0, 1.9999999999735776].
Doze controles adicionais da API de alta taxa passaram. O banco131072 também
reproduziu os16 pontos de fase anteriores, erro relativo
6.8070632624902974e-16.

**NÃO PAGO:** convergência suficiente em alta SNR. A mudança da log-likelihood
integrada sobre fase/amplitudes, neste ponto de fonte, foi:

| taxas (Hz) | PSD | SNR40 | SNR200 | SNR600 |
|---|---|---:|---:|---:|
| 131072→262144 | O4 | 0.018844314 | 0.10277967 | 0.4291108 |
| 131072→262144 | O5 | 0.034200796 | 0.16937048 | 0.55572549 |
| 262144→524288 | O4 | 0.035898243 | 0.25244507 | 1.6064155 |
| 262144→524288 | O5 | 0.060014584 | 0.23731355 | 1.6252408 |

O limite registrado é0,1. SNR40 passa neste controle;200/600 falham.
A malha interna fixa explicava a ausência de refinamento anterior, mas refiná-la
não resolveu a precisão: não é demonstração de causa única nem justificativa
para continuar dobrando taxas cegamente. As injeções continuam congeladas
em8192Hz; este ensaio não valida sua precisão intrínseca em alta SNR.

**PAGO COMO DIAGNÓSTICO:** a rodada8192 anterior é terminal e permanece
não aceita. Usamos suas likelihoods para comparar propostas, sem recalculá-las.
Primeiro:36 alternativas em duas metades. Depois: treinamento pela média e
pela raiz da média quadrática das densidades-alvo, com3/6/12 componentes.
Pela desigualdade de Cauchy-Schwarz, a segunda forma é a proposta ideal para
reduzir o segundo momento médio se as densidades-alvo forem conhecidas.
Aqui elas são estimadas com baixa ESS: a motivação não é prova de eficiência.

Selecionada:rms_K6, pelo maior ganho previsto
no décimo percentil, no pior dos dois grupos de validação. Esse ganho ainda é
0.8267695<1; nenhuma melhora
uniforme foi demonstrada. Ganho mediano mínimo previsto:
3.0301197, diagnóstico apenas.
Proposta:seis componentes Student-t,df30,mais10% do prior completo.
As sete coordenadas físicas continuam integradas; fase por quadratura,
distância/polarização comuns por integral analítica.

**PAGO:** teste independente de normalização/momentos32768draws:
integral=1.0111631 ±0.01577368;
maior desvio padronizado=1.2838414; erro da
densidade por fórmula independente=8.8817841970012523e-16.
Normalização aprovada não é precisão dos fatores de Bayes.

**EM EXECUÇÃO:** sessão62818,16384propostas,seed130892,
288/8554avaliações no suporte no último
registro observado. Fora do suporte:integrando zero, contado no denominador.
Não há resultado final desta rodada. O modelo/likelihood congelado não mudou;
a nova extração SEOB é instrumento de controle e não foi injetada na rodada Phenom.

**CONTINUAR:** revalidar a sessão62818; não reiniciar por timeout.
Depois de RESULT:auditar todas as densidades com `audit_registered_transport.py
--stage phase_ringdown_balanced`, auditar pesos e taxa com `audit_phase_source.py
../phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384 --rate --processes 6`,
comparar com a rodada8192. Repetição independente continua necessária, assim
como recuperação SEOB integrada, outras leituras/SNR, posterior contínuo de a,
viés/cobertura e pacote para reprodução. C6 preservada; nenhuma confirmação ou5σ.

Reprodução dos novos controles:create-once `validate_native_seob_phase.py`,
`refine_native_internal_mesh.py`, `diagnose_proposal_efficiency.py`,
`diagnose_balanced_proposal.py`. Proposta:`refine_balanced_source_proposal.py`
nas etapas fit,oracle,run --draws 16384 --seed 130892 --processes 6.
Para repetir resultados concluídos, usar diretório separado; não sobrescrever.

## Custódia medida

| arquivo relativo à bancada | SHA256 |
|---|---|
| record_native_mesh_and_balanced_start.py | 4c55fb0c342bbfc3c3a62207b7e1fda52f144b423b9e9affd83d408b8ee8ce6e |
| cache/source_evidence/native_seob_phase_source.py | bb2db74e009d014dcdffa50ac6e4368ea88deff2e3f86f2a5e9fc467570ccd5b |
| cache/source_evidence/validate_native_seob_phase.py | 8f7d80665a37e847fa7d5dfc342caa67ae38448414420c67838b9322dcdc9313 |
| cache/source_evidence/refine_native_internal_mesh.py | 7f152a8472e05adfe3056927e4b0402b569ff2f086d8483cc33cde27327414a3 |
| cache/source_evidence/diagnose_proposal_efficiency.py | ea4174d9a4a0bc221511e5ed7ced43b0f3809afaedf588b5abf72f4d97da2e5a |
| cache/source_evidence/diagnose_balanced_proposal.py | 79d46b2a6a125012469a8bc094f19d819a5ced4c8c6c18fbde934f04bc96c4d0 |
| cache/source_evidence/refine_balanced_source_proposal.py | af03ff79b21a73fd6554ff36c6da6a0b5274b00e57d82c3f422cee0d6a918d2b |
| cache/source_evidence/direct_seob_modes.py | 7cb9fd39298dd8f6dbedbf436ae42137d54a44287003a01b0e342456c8187415 |
| cache/source_evidence/native_seob_phase_validation/REGISTRATION.json | 64f44d5096f6278ec1e72957faea14b0214fc3ebb4a8ca530c7b7afaa914dc28 |
| cache/source_evidence/native_seob_phase_validation/RESULT.json | 106704c909943a3001dacba8fa6f393fd77a1081c550e47afa6f94de3ea4fba3 |
| cache/source_evidence/native_internal_mesh_refinement/REGISTRATION.json | 182314fc0178e28d91a2e4ce031b8630430a8e4e73005da7f25d2ded51503262 |
| cache/source_evidence/native_internal_mesh_refinement/RESULT.json | e63ea3023e30245f70d02f08411d16a47f7a04417bc0a56edbdbd99acafb4f1d |
| cache/source_evidence/proposal_efficiency_diagnostic/REGISTRATION.json | 5114891072a37d8f01b4c4f37fe058850edbb3fa2666dd9a8228168607b4d920 |
| cache/source_evidence/proposal_efficiency_diagnostic/RESULT.json | 5dc050c75b225edb18257ce4436b364cfaf6d34d716c07cbe13b9bfb3b10d4bc |
| cache/source_evidence/balanced_proposal_diagnostic/REGISTRATION.json | 14e07d4405203e9d05a210f162d33a9feaac6b2b3f6fb8b3014c3d42eb5a9488 |
| cache/source_evidence/balanced_proposal_diagnostic/RESULT.json | 981ff3affc26a0953841dbe0b4c8404f03e68a16e47de74f486628ddcac5b68d |
| cache/source_evidence/phase_ringdown_balanced/PROPOSAL.json | bce89a73bcbd5ff4c003d7032e066b27976cf67c7d119fd1cf8323d1591e663a |
| cache/source_evidence/phase_ringdown_balanced/REGISTRATION.json | 4c3464405e77139fa96198a7027e91256534fce6f80d2b7da7a09360262ed805 |
| cache/source_evidence/phase_ringdown_balanced/PROPOSAL_ORACLE.json | 5d877d41a7a9393a7ff3f5698f24572ef7229fa247f65d6b0c3abce074d211f3 |
| cache/source_evidence/phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384/START.json | 31af068d5fe43da8dc27d3171df47188ab4c1b8459c35fb84d4b9bf73405cf6a |
| cache/source_evidence/phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384/PROPOSALS.npz | ac5074d31ea48466bda6f7fd85dfaa8f9d5a3dc1a9015e783bee3373fc05c322 |
| cache/source_evidence/native_internal_mesh_refinement/integrals_131072_O4.npz | 430544b983bdd112b0659ec1716de6274827ca240333e665a643400f344ec1c7 |
| cache/source_evidence/native_internal_mesh_refinement/integrals_131072_O5.npz | 772fc81deb9b9e6c693bef6c81411fa4569aa57f4f9cce37d68e5d6b6bb197bc |
| cache/source_evidence/native_internal_mesh_refinement/integrals_262144_O4.npz | 2b5f2f43deaff55e2f222522fc305f7ce22cbf22aa726d699fa7e3d30c221989 |
| cache/source_evidence/native_internal_mesh_refinement/integrals_262144_O5.npz | 0a65dca3d1741616f4015234a5880c9916106e86a1cad98d46c7df2ac56e6c9d |
| cache/source_evidence/native_internal_mesh_refinement/integrals_524288_O4.npz | 555e2f8e25a643f27c77b7321d9f33a6919285cb6667fd526a9be25c6aee1d2a |
| cache/source_evidence/native_internal_mesh_refinement/integrals_524288_O5.npz | a37db2f191479ed8de6d7429d3c000b861822117f7171226efa0d14474074b4b |
| cache/source_evidence/native_internal_mesh_refinement/raw_131072.npz | 86e19f882752f84226759e945ab7320cb6aa8a2d56e4cca92196e2b1fb3069b3 |
| cache/source_evidence/native_internal_mesh_refinement/raw_262144.npz | 97ba8225b715a1681795ad7d65c6bacf798e0b3136d27027d28e1a9bbae4032e |
| cache/source_evidence/native_internal_mesh_refinement/raw_524288.npz | 2c2054868456678b4ba74667d22fc485cc58e74fc0b2faab0c98e7bd942b3ac2 |
