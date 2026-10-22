[REAL — correção numérica medida em cópia; OPEN — evidência integrada/calibração]

# ORDEM 013 — correção do pico de fase e diagnóstico da resolução

2026-09-22T06:58:12.989179+00:00. N/A — sem Lean. Nenhum original canônico alterado.

**PAGO:** localizada a origem das falhas de interpolação em fase no caso source90.
O pico intrínseco do modo22 deve ser independente da fase orbital, mas sua
reotimização para cada fase criava dispersão de aproximadamente10⁻¹⁰s. Usar o
mesmo pico medido em fase zero levou os controles de44 falhas em72 para zero
falhas em72. Fontes: duas famílias, três taxas32/64/128kHz, duas PSDs, duas
intensidades e três fases fora da malha; SNR40/200/600.

**PAGO:** a correção entrou somente na cópia `stable_peak_imr_model.py`.
O gerador original e a integração já registrada continuam intactos. A cópia
foi conferida contra o banco de fase com alinhamento comum: erro relativo
máximo de forma de onda=2.4754042885334018e-15; erro máximo na
log-verossimilhança=4.9476511776447296e-10, em72 controles.
Isso não atesta ainda a região inteira do prior/posterior.

**NÃO PAGO:** o erro SEOB entre resoluções não desaparece com essa correção.
Um diagnóstico adicional ajustou apenas as direções já presentes de
amplitude/polarização, fase e tempo, em SNR600 sem ruído. A coluna final foi
conferida gerando novamente a forma de onda com o deslocamento calculado.

| família | taxas (Hz) | maior resíduo após amplitude/polarização | após também fase/tempo, avaliação direta |
|---|---:|---:|---:|
| IMRPhenomXPHM | 32768 → 65536 | 0.000794202572 | 5.77101729e-06 |
| IMRPhenomXPHM | 65536 → 131072 | 0.000106419289 | 7.49973865e-07 |
| SEOBNRv4HM | 32768 → 65536 | 0.0743562681 | 0.0703238485 |
| SEOBNRv4HM | 65536 → 131072 | 0.355460383 | 0.100084503 |

Esses números são normas na métrica do ruído, não sigmas de detecção. Ajustar
fase e tempo reduz parte da diferença SEOB, mas sobra erro de forma. O teste
é pontual e não substitui integração do prior, estabilidade de evidências,
controle da resolução das injeções nem cobertura dos posteriores.

**EM EXECUÇÃO:** sessão41895, rodada8192 propostas
`phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192`, observada em
2752/4299 avaliações dentro do suporte.
Propostas externas ao suporte físico continuam contadas com integrando zero.
O diagnóstico46894 e a validação71668 terminaram com código0.

**Continuar:** revalidar sessão41895; não reiniciar por timeout.
Após RESULT, executar `audit_registered_transport.py` com
`--stage phase_ringdown_regularized`, `audit_phase_source.py` com `--rate` e
comparar com o piloto anterior via `compare_phase_runs.py` conforme o recibo
`C5_TRANSPORT_AUDIT_PROGRESS.json`. Não usar a nova cópia retroativamente.
Faltam precisão/repetição, recuperação SEOB integrada, demais leituras/SNR e
calibração contínua de a. A causa de fase foi resolvida no escopo medido;
a precisão física/estatística não foi declarada por consequência.

Descrição técnica em inglês: `cache/source_evidence/PHASE_ALIGNMENT_NUMERICS.md`.
Nenhum resultado novo é confirmação física ou conversão para5σ. C6 preservada.

## Custódia medida

| arquivo relativo à bancada | SHA256 |
|---|---|
| `cache/source_evidence/diagnose_generator_alignment.py` | `2a9e48f1481c7dedd2772ffc52e74358d71b43e665fe556507c18002e4e2b915` |
| `cache/source_evidence/generator_alignment_diagnostic/REGISTRATION.json` | `2b5b2c42ac3788b92b0e4f66a76f860606857526834620de49428c0400cd55f7` |
| `cache/source_evidence/generator_alignment_diagnostic/RESULT.json` | `8aff37d96c6089ae395133e0701b70dc56c48f03d366a4277b4c009d58958e44` |
| `cache/source_evidence/stable_peak_imr_model.py` | `378eb1aa410ded4e00f33008e878095d71561dc559119ee7bcf6da659fa4ed25` |
| `cache/source_evidence/STABLE_PEAK_MODEL_PROVENANCE.json` | `f30a9e92b8fb9fcf358880dcd7dc6e768aa4d3e1a56a836d64be4540a862905d` |
| `cache/source_evidence/validate_stable_peak_and_rate.py` | `06135e58c5fd0db0ef6b83a91ed4456a49a5861e4d2264f80368f181ef891001` |
| `cache/source_evidence/stable_peak_validation/REGISTRATION.json` | `2f86ee6ec82406b4319b11a632a04db381714388179df8d3fb398bd86b55f21f` |
| `cache/source_evidence/stable_peak_validation/RESULT.json` | `78ff213a2a001fb02221c6b27578da8270bc35ad9aa9e780b5dda87a92b73ba7` |
| `cache/source_evidence/PHASE_ALIGNMENT_NUMERICS.md` | `96ad94fa9b65121f701d9df4d6f9ebaf4ff268fc2fd842fdf4645629f78a2ed3` |
| `cache/source_evidence/coherent_imr_model.py` | `4d9e568816c3b47e8e59b2401334a1a66541247fa80ed36495949aa4f5bca497` |
| `cache/source_evidence/phase_ringdown_regularized/REGISTRATION.json` | `6c167d0b6839a63cf14c6b0635079d538b14e7107d7519627e379b5341f4dd89` |
| `record_phase_alignment_refinement.py` | `ed8f2e5cf4f1150c7a9de046f49e72240046e759ff89cf5d42bdc667127eea91` |
