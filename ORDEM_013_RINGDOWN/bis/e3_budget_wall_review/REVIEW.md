# B3 — revisão estática finita

**Alterações necessárias antes da entrega/ativação; nenhum script de produção executado.** Custos/contagens e números Kerr conferem com candidato e recibos.

- **B3-R1 (P1_DEPENDENCY_BEFORE_ACTIVATION)**, `refeito/activate_wall_budget_013bis.py:47; bis/e2_code/registration_guard.py:157,196`: Activation witness draft has prose but omits exact allocation_sha256: and registered_utc: lines required by frozen check_witness. Receipt alone does not make load_jobs accept it. Correção proposta: Before activation, append exactly one machine hash line for the active budget bytes and one registered UTC line. Test those regexes against a finite mock witness; do not change guard. This review does not execute or activate anything.

- **B3-R2 (P2_PIN_AND_ACTIVATION_PREFLIGHT)**, `refeito/deliver_b3_wall_013bis.py:20-29,107`: Before first output the delivery checks only budget hash and review approved flag. It neither validates complete activation receipt/witness/parent/candidate bindings nor compares COMPARISON to the independently reviewed Kerr pin. Later listing hashes records current bytes but does not enforce reviewed identity. Correção proposta: Preflight all named sources and destinations before new(fiche): activation status and parent/candidate/review/witness pins; approved review candidate binding; Kerr review hash and its input_hashes COMPARISON pin; empty new jobs/counts and bounded reserve. No scientific imports required. Use a snapshot of verified bytes for rendering.

## Linguagem e escopo

- `refeito/deliver_b3_wall_013bis.py:42-51`: Print mass_frame explicitly: Mf detector-frame Msun, af dimensionless. Replace razão de larguras by diferença de medianas dividida pela largura em quadratura.

- `refeito/deliver_b3_wall_013bis.py:51`: A revisão conferiu os dados completos is too broad: B checked complete posterior samples and metadata/pins, not strain bytes or reconstructed covariance. Say posteriores completos e metadados/pins no escopo do parecer.

- `refeito/deliver_b3_wall_013bis.py:98`: Cost totals agree. Add separate Welch diagnostic3.402371976s if claiming complete itemized E3 costs; otherwise explicitly say its receipt is in budget. Do not add launcher/runner totals twice.

- `refeito/deliver_b3_wall_013bis.py:101-103`: Commands shown contain ellipses or omit actual WSL/Python prefix; label as abbreviated locators rather than exact replay commands. No rerun authorized by reproduction prose.

## Integridade e symlink

Recibo:217 insumos +31 fontes +47 entregas ParteA =295 comparações registradas, todas com hashes esperado/real iguais. Isto é conferência interna do recibo, **não nova rehash dos295 originais**. Cache não foi varrido; não há alegação de integridade universal.

A única exceção WinError1920 é o symlink da fixture negativa `finding_symlink_output_escape`. `readlink` retornou `/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_allocation_review/fixtures_001/finding_symlink_output_escape/escaped_sidecar`, lexicalmente dentro da própria fixture, coerente com audit_fixtures.py:218 e FIXTURE_RESULTS_001.json. Nenhum conteúdo do destino foi lido; não remover a exceção histórica nem declarar o destino auditado. Classificação separada em SYMLINK_CLASSIFICATION.json.

356 verificações finitas passaram. `REVIEW.json` traz hashes lidos e detalhes; `snapshot/` preserva os bytes efetivamente revisados. Reavaliação necessária se o principal alterar os drafts. Não executado deliver_b3, activate, ciência, strain ou posterior. A revisão independente do próprio candidato continua sendo de B. Todos os arquivos escritos estão em MANIFEST.json.
