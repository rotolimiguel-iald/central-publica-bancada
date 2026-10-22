[REAL — fechamento independente de S2 e seleção/bytes do ZIP final; sem nova ciência]

# C7 suplementos v3_2 — fechamento S2 / M6

Data UTC: 2026-09-22T19:06:12.127927+00:00.

**S2 fechado nos três suplementos v3_2. Seleção e integridade do ZIP final aprovadas neste recorte.** Não resta bloqueante dos achados S1/S2 examinados; R1–R4 do pacote principal têm os fechamentos próprios v3_2/v3_3. Este parecer é novo e não substitui os anteriores.

POSTERIOR/GWTC3/INJECTION resolvem e recusam work/output internos antes de qualquer mkdir. Reexecutei o bloco real em memória sob optimize=1: seis recusas independentes (duas por wrapper), zero mkdir/mkdtemp/subprocess. Mais nove sondas preservam S1 e exercitam finally: falha de criação do destino ocorre antes de mkdtemp; cleanup normal e cleanup após falha de escrita do recibo removem somente o filho validado. Nenhuma remoção real foi feita pelos mocks.

As três negativas por fonte ausente, executadas pelo **agente principal autorizado**, conferem nos logs/intenções/recibos; seus temporários estão ausentes e eram descendentes próprios das raízes declaradas. Tamanhos/hashes/ZIPs dos três pacotes conferem. Apenas README e reproduce.py mudaram versus v3_1, além do manifesto; assets científicos permanecem idênticos. Não houve nova campanha por esta revisão.

O ZIP `cache/TGL_RINGDOWN_DELIVERY_v3_1.zip` contém **231 arquivos listados + MANIFEST.json = 232 membros**, sem ausências/duplicatas/extras. Conferi por leitura direta todos os tamanhos/hashes e os bytes dos subpacotes contra as pastas/manifestos de origem. CRC passa. Builder hasheado no manifesto é `build_final_bundle_v3_1_013bis.py`. A seleção efetiva no ZIP, no manifesto/recibo e no builder coincide:

- `C7_INDEPENDENT_v3_3`
- `C7_POSTERIOR_REPRODUCTION_v3_2`
- `C7_GWTC3_REPRODUCTION_v3_2`
- `C7_INJECTION_REPRODUCTION_v3_2`
- `C7_IMR_RECOVERY_REPRODUCTION_v3`
- `C7_COHERENT_SOURCE_REPRODUCTION_v3`
- `C7_NATIVE_SEOB_WAVEFORM_v3`

Recibos embarcados coincidem com os originais, incluindo C7_SUPPLEMENTS_V3_2_BUILD. README/OVERVIEW coincidem, listam as versões corretas e preservam a marca literal R-MOD. O log do verificador contém PASS/231 e coincide com C7_FINAL_BUNDLE_V3_1_VALIDATION. Essa extração foi executada pelo agente principal autorizado; minha verificação do ZIP é direta, independente e sem nova extração. O recibo final registra temporary_removed=true mas não informa o caminho: a ausência física desse temporário específico fica [DECLARADO], distinta das três remoções dos suplementos efetivamente reconstatadas. Isso não impede fechar S2 e a seleção pedida.

**Erratas de proveniência dos pareceres anteriores:** “replay do operador” deve ser lido como **replay do agente principal autorizado pelo operador**, não execução pessoal do humano. Além disso, a observação anterior de seleção v3 referia-se ao arquivo build_final_bundle_v3_3_013bis.py efetivamente lido; o builder então vigente informado pelo agente principal era build_final_bundle_v3_final_013bis.py, que conferi agora e seleciona v3_1. Não imputo ao builder efetivo anterior a seleção do arquivo antigo. A nova entrega v3_1 seleciona os suplementos v3_2, como comprovado acima.

O fechamento é de engenharia documental/confinamento e integridade para M6, não certificação global da ciência ou de todos os requisitos de entrega. As raízes externas à entrega composta seguem a instrução do README; a guarda dos wrappers é relativa a cada pacote próprio. Ciência congelada, C5/PE, injeção A e a ressalva operacional F2-INJ-R1 são assuntos separados. Sem alteração de produção, manifests, memórias ou parecer anterior.

Controle próprio: `bis/c1_review/c7_supplement_v3_2_final_checks.py`, Python bundled −B −O; resultados em `c7_supplement_v3_2_final_results.json`.

| Caminho relativo à raiz | SHA256 lido |
|---|---|
| `refeito/close_supplement_confinement_013bis.py` | `9e94b8aa9cf6798d0688c43611a8dca5d6b6be3ad75f5299c431868269ee96aa` |
| `bis/C7_SUPPLEMENTS_V3_2_BUILD.json` | `6513b82b52f7f6cfe0a90b82c7c4ca60f1a1101b227e2e14a04226e91424cf4e` |
| `refeito/build_final_bundle_v3_1_013bis.py` | `c8121e8f32fa2d2458f63369a038e77d2ae87bdac2022a645e1c1e85ab70f517` |
| `cache/TGL_RINGDOWN_DELIVERY_v3_1.zip` | `67af7fdd0ff3ed07d20b70702467eab9a97e3d0bd843a93aa08c703cb0ccf20f` |
| `bis/C7_FINAL_BUNDLE_V3_1_VALIDATION.json` | `f6b27d649f48047d4994fab1f78cc4e0c5f144c5b6549e22caa7383ca4ed5050` |
| `bis/C7_FINAL_BUNDLE_V3_1_VERIFY.log` | `9d585b55e26fb1561f85de88f6779628fd9e8a33fc0e490cd398c059ae4e0e37` |
| `bis/c1_review/c7_supplement_v3_2_final_checks.py` | `b555c448a6dee6db0b5623b734204c84276b3ab741e52096ce953b82363cada8` |
| `bis/c1_review/c7_supplement_v3_2_final_results.json` | `0e67df2f569eca6fca5e0a7a942cdb886677cdd2abf397e4633d20cfea2d1d4d` |
