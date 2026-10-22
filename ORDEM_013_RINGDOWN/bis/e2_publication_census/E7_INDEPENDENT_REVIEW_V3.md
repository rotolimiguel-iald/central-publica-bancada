# E7 v3 — fechamento independente de F1/F2

[REAL] Data da conferência complementar: 2026-09-22T21:02:44.967178+00:00. Fontes: HANDOFF_FINAL_v3.md, MANIFEST_FINAL_v3.json, E2_INCLUDE_FINAL_v3.json, UNIT_TESTS_V3.json, árvore producer e fonte escalar pinada.

**Veredito: F1/F2 corrigidos nos bytes v3 revisados. F3 (cronologia da autorização) permanece OPEN. Não é aprovação irrestrita para extração/ativação.** A integração como candidato de revisão pode prosseguir; corrigir ou tratar explicitamente F3 antes do uso operacional da autorização. Nenhuma autorização final do operador é inferida deste parecer.

[REAL] E7_INDEPENDENT_REVIEW.md permanece intacto. Este é um parecer novo, independente dos 46 testes relatados pelo autor. Nenhum produtor, registro, guarda, manifesto ou input foi alterado por este revisor.

## Evidência independente

[REAL] Executei somente controles finitos em memória: **13 grupos de regressão passaram; 26 negativos de contrato foram recusados antes dos diagnósticos; 11 controles dos predicados AST de metadados passaram**. Uma sonda adicional de cronologia foi aceita indevidamente, descrita em F3. Portanto não rotulo toda a revisão como “todos os negativos passaram”.

[REAL] Ambiente dos controles: Python 3.12.3, NumPy 2.5.3, WSL /opt/lal_env. Primeira tentativa de selecionar distribuição “Ubuntu” falhou porque esse nome não existe; não executou o script. A execução bem-sucedida usou a distribuição padrão. Scripts passados por stdin, -B, sem arquivos temporários de testes. O consumidor e a fonte escalar foram carregados em módulos de teste após conferir seus pins. Guard/IO do consumidor substituídos por mocks: os resultados de contrato não certificam integração real com E2.

[REAL] **O extrator não foi importado nem executado.** Para F2, somente os predicados de rejeição extraídos de sua AST foram avaliados sobre objetos falsos. h5py foi usado apenas para construir/identificar tipos NumPy de metadados, sem h5py.File, dataset real ou leitura de valores. Nenhum HDF, posterior real, strain, seed privada, extração, PE, waveform ou MC foi acessado/executado. A suíte do autor cria fixtures HDF locais e importa o extrator: foi lida, não reexecutada por este revisor.

[REAL] Custódia: **9/9 arquivos do manifesto** conferem em SHA256 e tamanho; **18/18 pins de entrada** conferem. A leitura desses inputs foi apenas de bytes de arquivos de metadados/código já autorizados, para hashing, sem imprimir valores científicos. MANIFEST_FINAL_v3 e E7_ASSEMBLY_V3 também tiveram hashes medidos. Árvores no manifesto, no fragmento e no diretório produtor concordam, com exatamente os dois módulos esperados.

[DECLARADO] UNIT_TESTS_V3 registra 46 testes, zero falhas e 1,608 s. Conferi os bytes e li os testes, mas não trato o recibo do autor como execução independente minha.

## F1 — CLOSED no contrato semântico de payload

[REAL] [validate_payload_contract](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/tgl_ringdown_ampliacao.py:211>) vincula schema, catálogo, registro, plano, árvore e SHA da autorização; exige ordem/membros do plano, N=N_source=N_source planejado, fonte/tar/dataset/modelo, mapeamento, massa detector em solar_mass e priors com caminhos/estatuto/estrutura esperados. Declarações de deformação são obrigatórias; textos precisam ser não vazios e limitados; densidade segue null e fatorização OPEN. Priors derivados sem declaração permanecem OPEN.

[REAL] A função [run](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/tgl_ringdown_ampliacao.py:487>) verifica papel calibration de todo o plano antes de ler o payload, exige autorização por caminho/hash independente do JSON posterior e valida o contrato antes dos diagnósticos. Os cinco cenários antes aceitos na v2 agora recusam; ampliei para 26 casos discriminados no apêndice.

[REAL] A nova interface exige authorization e authorization_sha256 quando há posterior. A autorização tem que vir do principal por canal já autorizado; copiar o hash autodeclarado no payload não satisfaz a independência da autorização. O hash fixa bytes, não autentica uma pessoa. Sem payload, preview continua permitido apenas no contexto registrado.

[OPEN] Igualdade de comprimentos/mapping não prova que uma origem maliciosa preservou o pairing. O pairing depende do produtor pinado: leitura conjunta dos campos/mesma ordem de linhas, sem thinning. O diagnóstico de covariância reage a permutação de uma coluna, enquanto permutação conjunta preserva a identidade estatística; teste independente conferido. Nenhum pairing real foi inspecionado.

## F2 — CLOSED para armazenamento externo/VDS e objeto não textual

[REAL] [prior_metadata](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/extrai_posteriores_pseob.py:18>) recusa links não duros, dataset virtual, external storage, tamanho zero/excessivo e dtype que h5py não reconhece como string **antes de node[()]**. A alocação de texto fixo é limitada antes da leitura. Referências e vlen numérico recusaram nos predicados; strings fixas e vlen textuais válidas passaram.

[REAL] Ordem AST: predicado de metadados nas linhas 30–32; alocação fixa 35–36; leitura somente na linha 37. Nove formas inválidas recusadas e duas formas textuais admitidas nos 11 controles. O extrator completo não foi invocado.

[OPEN] Para string vlen, o tamanho lógico é limitado depois da leitura; isso é explicitamente assumido no handoff, não uma garantia de memória metadata-only. Validação de valores vazios/UTF-8 permanece suportada pela leitura estática e testes declarados do autor, não por abrir HDF nesta revisão. Fechamento limitado ao defeito de custódia F2 e seus predicados, sem inventar prova de toda a implementação h5py.

## F3 — P2, OPEN: autorização futura é aceita

Evidência: [checked_authorization](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/tgl_ringdown_ampliacao.py:190>), especialmente linhas 206–208.

[REAL] A função só compara authorization.registered_utc >= reg.registered_utc. Não exige authorization.registered_utc <= agora. Sonda independente com data fictícia **2999-01-01T00:00:00+00:00** foi aceita, chegando aos diagnósticos; data anterior ao registro foi corretamente recusada. O teste usa guard.utc simulado e IO/pins simulados: identifica a comparação ausente, sem afirmar quebra criptográfica, autorização real ou acesso real a dados.

[DERIVED] Um recibo pós-datado ainda não representa um ato de autorização ocorrido no momento de uso. A existência de um hash fornecido pelo principal não corrige uma data futura. F1/F2 históricos estão fechados, mas a nova alegação de cronologia do handoff é mais ampla que a verificação feita.

Correção mínima recomendada: tempo UTC com timezone obrigatório e comparação E2 <= autorização <= agora, no ponto de uso, usando relógio controlável no teste. Adicionar negativos para futuro, timezone ausente e data malformada, sem abrir payload quando recusados. Conferir prazo pela guarda do registro, mantendo-o distinto da data de autorização. Se o produtor mudar, emitir pins/manifesto novos e fazer fechamento focado; não editar os artefatos v3 congelados silenciosamente.

## Fórmulas, estatutos, forecasting e limites preservados

[REAL] Comparação AST entre snapshot v2 e v3: no consumidor só mudaram run e main; acrescentadas checked_authorization e validate_payload_contract. Funções científicas mantêm AST idêntica. No extrator mudaram extract e prior_metadata. Isso não substitui os controles: os 13 grupos independentes também passaram.

[REAL] Fonte escalar tgl_ringdown_prediction.py: SHA256 **fd0fc446e1c732f3d782210c6effa7cb7faeaeb7a51a434d4f397f1da89bd652**, lido/conferido por script. Comparação escalar-vetorial em sete leituras × oito pontos sintéticos: maior erro relativo 3.4678746308606614e-16. Oráculo adimensional independente inclui R-MOD com QNM fornecido, spins assinados e identidade de soma de taxas de amplitude; controles de escala M/z e projeção de intercepto mantidos.

[REAL] Dez leituras e matriz de targets do fragmento v3 são idênticas às da v2. Plano preserva 33 identidades únicas, todas calibration. Não foram introduzidos eventos de teste cego. Forecast permanece condicionado aos inputs da fonte; nuisance física, seleção/normalização e covariância física não foram pagas. Gate alegado “pago” ou campos inválidos não produziram lnB/z físicos; outputs permanecem null e vereditos conservadores. R-MOD sem QNM, PROP, COHERENT e 440 permanecem OPEN.

[INPUT/CONJECTURE] Estatutos por leitura são os declarados na fonte, não evidência experimental. Fórmula/nome não recebe interpretação estrutural por esta revisão. NOT_FALSIFIED nunca CONFIRMED; nenhum gate do núcleo é movido.

## Guarda e montagem final

[REAL] Na conferência de 2026-09-22T21:02:44.967178+00:00, o pin de guarda no fragmento era `7fbb74837d8d56b33690c09b0a6f0ca186ee8d1b1c948f5dec28825316f20133` e o arquivo vivo mediu `9576db51615627c1264ef51ba228c47a12f162c6c62f68b939306135e1ae3743`. Conforme ordem explícita do operador, **a guarda será recalculada no assembly depois de A final**. Não reabro o achado v2 por essa mudança esperada nem exijo congelar a guarda antiga.

[OPEN] O candidato final deve citar E2_INCLUDE_FINAL_v3 (ou sucessor necessário por F3), recalcular coerentemente a guarda, preservar outras raízes e receber as revisões e autorização do operador. Este fechamento cobre os produtores pinados abaixo; não certifica registro futuro, witness, seed, runtime ativo integral ou execução. Divergências posteriores exigem nova conferência, nunca bypass do pin.

## Pins medidos

| Artefato em e7_prepare | Bytes | SHA256 |
|---|---:|---|
| `producer/extrai_posteriores_pseob.py` | 7673 | `3e896bd014db610c9b83c6171de2b3b98db506e597b068da20617e189734e330` |
| `producer/tgl_ringdown_ampliacao.py` | 29360 | `6293d8cb4980b16637f6cde1991cc6b3aa25b7c2a14bff2103f81dc67ab48d2d` |
| `HANDOFF_FINAL_v3.md` | 4248 | `e7433bfa040e1ccc3b272300e73e89b935f2af2621eb76f28fa32aab1ed96b7d` |
| `E2_INCLUDE_FINAL_v3.json` | 48349 | `af656a6c6fcf4efc29f94997c27b19ce5707f9a4121863cfba0b2eb31e242d71` |
| `UNIT_TESTS_V3.json` | 685 | `a038b719d3604b0eebd86d671eb4157ce19b0ee42c7a0bc5a27fbfdab46c2e88` |
| `EXTRACTION_PLAN.json` | 47760 | `7dc138a1690d45d381fc36d6e5cb54967b028741158f625ac814fb92159a7335` |
| `tests/test_e7.py` | 10481 | `e8556579074575fb9eb4e38f3133c89162e12095acacbb1738f8b991cffc93bb` |
| `tests/test_review_fixes_v3.py` | 11312 | `03d30781cfdeeb1dc767929b2db2dda14c73afa83ea6d4c8ff2cf44b993ea265` |
| `tests/finalize_review_v3.py` | 4163 | `dedf638db3faeb7e7c3f7a501fc2e2940d25286171fafeacbc39b15c305dc897` |
| `MANIFEST_FINAL_v3.json` | 2144 | `8a88538dfb0067f9ea56205d3772f4f8de4f7afae0764489d3797ff9b0c764f7` |
| `E7_ASSEMBLY_V3.json` | 740 | `6d578043ade69659cc6f7e6c46b65faeeb626f9085e2c25e78f3ade38d05d12f` |

## Apêndice A — resultados independentes completos

[REAL] Registros abaixo são da execução em memória desta revisão. “accepted” em future_authorization_residual é a falha F3; não é autorização concedida.

```json
{
  "runtime": {
    "python": "3.12.3",
    "numpy": "2.5.3"
  },
  "tests": [
    {
      "name": "T01 scalar source pin and vector regression on new grid",
      "status": "PASS",
      "detail": {
        "draws_per_reading": 8,
        "max_relative_errors": {
          "R-A": 3.4678746308606614e-16,
          "R-B": 1.9736978141857145e-16,
          "R-RAIZ-0": 0,
          "R-RAIZ-EP4": 1.7339373154303304e-16,
          "R-RAIZ-REST": 2.0392116151805147e-16,
          "R-LIN": 0,
          "R-GLOBAL": 0
        }
      }
    },
    {
      "name": "T02 independent dimensionless formula oracle including signed R-MOD",
      "status": "PASS",
      "detail": {
        "dimensionless_x_derivations": [
          "R-A",
          "R-B",
          "R-RAIZ-0",
          "R-LIN",
          "R-GLOBAL",
          "R-MOD"
        ],
        "signed_spins_checked": true
      }
    },
    {
      "name": "T03 dimensional scaling and redshift controls",
      "status": "PASS",
      "detail": "Mass/redshift scalings and EP/4 large-offset asymptote hold for synthetic astrophysical domain."
    },
    {
      "name": "T04 harmonic lifetime identity and sign",
      "status": "PASS",
      "detail": "Independent sum of decay rates, amplitude convention, no extra energy factor."
    },
    {
      "name": "T05 independent weighted-intercept closed form",
      "status": "PASS",
      "detail": {
        "information": 0.39171686364533526,
        "closed_form": 0.39171686364533526
      }
    },
    {
      "name": "T06 tiny effects and degenerate nuisance controls",
      "status": "PASS",
      "detail": {
        "tiny_information": 4.003726573754519e-79,
        "constant_absorbed": true,
        "singular_refused": true
      }
    },
    {
      "name": "T07 pair covariance and residual variance identities",
      "status": "PASS",
      "detail": {
        "paired_covariance": 0.00892681106415199,
        "row_permutation_invariant": true,
        "single_column_shuffle_changes_covariance": true,
        "equal_length_alone_does_not_prove_pair_identity": true
      }
    },
    {
      "name": "T08 invalid samples and duplicate controls",
      "status": "PASS",
      "detail": "nonfinite, domains, unequal length, duplicate event/product refused"
    },
    {
      "name": "T09 OPEN channels and exact-QNM domain guards",
      "status": "PASS",
      "detail": "Missing QNM, negative-spin BCW, forbidden corotation, unstable QNM and absent 440 fail closed."
    },
    {
      "name": "T10 adversarial nuisance claims cannot create physical verdict",
      "status": "PASS",
      "detail": {
        "gate_labels": [
          "red",
          "red",
          "UNVERIFIED",
          "UNVERIFIED",
          "UNVERIFIED",
          "UNVERIFIED"
        ],
        "malformed_nonnull_gate_labeled_UNVERIFIED_not_red": true,
        "never_green_or_confirmed": true
      }
    },
    {
      "name": "T11 pins JSON and path controls",
      "status": "PASS",
      "detail": "Wrong/missing hash, duplicate JSON key and path escape refused, all read-only."
    },
    {
      "name": "T12 consumer scientific imports NumPy only",
      "status": "PASS",
      "detail": {
        "imports": [
          "argparse",
          "hashlib",
          "importlib",
          "json",
          "math",
          "numpy",
          "os",
          "pathlib",
          "re",
          "sys",
          "tempfile"
        ],
        "extractor_imported": false
      }
    },
    {
      "name": "T13 v3 mock full consumer valid baseline",
      "status": "PASS",
      "detail": {
        "accepted": true,
        "reported_N": 8,
        "physical_lnB": null,
        "physical_z": null,
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": [
          "reached"
        ]
      }
    }
  ],
  "test_count": 13,
  "test_failures": 0,
  "negative_probes": [
    {
      "name": "F1a self-consistent truncation",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Full sample count differs from registered plan",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1b mass_frame",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Posterior source not registered: mass_frame",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1b mass_unit",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Posterior source not registered: mass_unit",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1b model",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Posterior source not registered: model",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1b source_field_mapping",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Registered mapping or detector mass units differ",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1c malformed priors",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Prior declarations/paths must be lists",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1d mismatch schema",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Posterior schema/production/authorization contract differs",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1d mismatch authorization_sha256",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Posterior schema/production/authorization contract differs",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1d mismatch catalogue",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Posterior schema/production/authorization contract differs",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1d mismatch registration_sha256",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Posterior schema/production/authorization contract differs",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1d mismatch plan_sha256",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Posterior schema/production/authorization contract differs",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1d mismatch producer_tree_sha256",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Posterior schema/production/authorization contract differs",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1e missing authorization payload pin",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Posterior schema/production/authorization contract differs",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1f missing independent authorization",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Principal post-E2 authorization path and SHA256 required",
        "reads": [
          "nuisance.json",
          "plan.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1g early authorization",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Principal authorization predates E2",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1h authorization status",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Missing/mismatched principal post-E2 authorization",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1h authorization registration_sha256",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Missing/mismatched principal post-E2 authorization",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1h authorization plan_sha256",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Missing/mismatched principal post-E2 authorization",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1h authorization producer_tree_sha256",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Missing/mismatched principal post-E2 authorization",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1i prior path",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Prior paths differ from registered plan",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1i prior empty-text",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Prior declaration must contain bounded nonempty text",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1i prior nontext",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Prior declaration must contain bounded nonempty text",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1i prior too-long",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Prior declaration must contain bounded nonempty text",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1i prior density-paid",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Prior status/density is not the declared OPEN contract",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1i prior factorization-paid",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Prior status/density is not the declared OPEN contract",
        "reads": [
          "nuisance.json",
          "plan.json",
          "auth.json",
          "payload.json"
        ],
        "diagnostics": []
      }
    },
    {
      "name": "F1j blind plan blocked before payload",
      "expected": "REJECT_BEFORE_DIAGNOSTICS",
      "passed": true,
      "evidence": {
        "accepted": false,
        "error": "Blind-release adapter OPEN; refuse before opening posterior JSON",
        "reads": [
          "nuisance.json",
          "plan.json"
        ],
        "diagnostics": []
      }
    }
  ],
  "negative_passed": 26,
  "F2_AST_predicates": [
    {
      "name": "virtual_text",
      "rejected": true,
      "expected_rejected": true,
      "passed": true
    },
    {
      "name": "external_text",
      "rejected": true,
      "expected_rejected": true,
      "passed": true
    },
    {
      "name": "object_reference",
      "rejected": true,
      "expected_rejected": true,
      "passed": true
    },
    {
      "name": "numeric_vlen",
      "rejected": true,
      "expected_rejected": true,
      "passed": true
    },
    {
      "name": "plain_object",
      "rejected": true,
      "expected_rejected": true,
      "passed": true
    },
    {
      "name": "numeric",
      "rejected": true,
      "expected_rejected": true,
      "passed": true
    },
    {
      "name": "zero_elements",
      "rejected": true,
      "expected_rejected": true,
      "passed": true
    },
    {
      "name": "too_many_elements",
      "rejected": true,
      "expected_rejected": true,
      "passed": true
    },
    {
      "name": "oversize_fixed",
      "rejected": true,
      "expected_rejected": true,
      "passed": true
    },
    {
      "name": "fixed_text",
      "rejected": false,
      "expected_rejected": false,
      "passed": true
    },
    {
      "name": "vlen_text",
      "rejected": false,
      "expected_rejected": false,
      "passed": true
    }
  ],
  "F2_metadata_before_read": true,
  "future_authorization_residual": {
    "accepted": true,
    "reported_N": 8,
    "physical_lnB": null,
    "physical_z": null,
    "reads": [
      "nuisance.json",
      "plan.json",
      "auth.json",
      "payload.json"
    ],
    "diagnostics": [
      "reached"
    ]
  },
  "manifest_audit": {
    "producer/extrai_posteriores_pseob.py": {
      "hash_matches": true,
      "size_matches": true,
      "sha256": "3e896bd014db610c9b83c6171de2b3b98db506e597b068da20617e189734e330",
      "bytes": 7673
    },
    "producer/tgl_ringdown_ampliacao.py": {
      "hash_matches": true,
      "size_matches": true,
      "sha256": "6293d8cb4980b16637f6cde1991cc6b3aa25b7c2a14bff2103f81dc67ab48d2d",
      "bytes": 29360
    },
    "HANDOFF_FINAL_v3.md": {
      "hash_matches": true,
      "size_matches": true,
      "sha256": "e7433bfa040e1ccc3b272300e73e89b935f2af2621eb76f28fa32aab1ed96b7d",
      "bytes": 4248
    },
    "E2_INCLUDE_FINAL_v3.json": {
      "hash_matches": true,
      "size_matches": true,
      "sha256": "af656a6c6fcf4efc29f94997c27b19ce5707f9a4121863cfba0b2eb31e242d71",
      "bytes": 48349
    },
    "UNIT_TESTS_V3.json": {
      "hash_matches": true,
      "size_matches": true,
      "sha256": "a038b719d3604b0eebd86d671eb4157ce19b0ee42c7a0bc5a27fbfdab46c2e88",
      "bytes": 685
    },
    "EXTRACTION_PLAN.json": {
      "hash_matches": true,
      "size_matches": true,
      "sha256": "7dc138a1690d45d381fc36d6e5cb54967b028741158f625ac814fb92159a7335",
      "bytes": 47760
    },
    "tests/test_e7.py": {
      "hash_matches": true,
      "size_matches": true,
      "sha256": "e8556579074575fb9eb4e38f3133c89162e12095acacbb1738f8b991cffc93bb",
      "bytes": 10481
    },
    "tests/test_review_fixes_v3.py": {
      "hash_matches": true,
      "size_matches": true,
      "sha256": "03d30781cfdeeb1dc767929b2db2dda14c73afa83ea6d4c8ff2cf44b993ea265",
      "bytes": 11312
    },
    "tests/finalize_review_v3.py": {
      "hash_matches": true,
      "size_matches": true,
      "sha256": "dedf638db3faeb7e7c3f7a501fc2e2940d25286171fafeacbc39b15c305dc897",
      "bytes": 4163
    },
    "MANIFEST_FINAL_v3.json": {
      "sha256": "8a88538dfb0067f9ea56205d3772f4f8de4f7afae0764489d3797ff9b0c764f7",
      "bytes": 2144
    },
    "E7_ASSEMBLY_V3.json": {
      "sha256": "6d578043ade69659cc6f7e6c46b65faeeb626f9085e2c25e78f3ade38d05d12f",
      "bytes": 740
    }
  },
  "input_pins_audit": [
    {
      "path": "ORDEM_013_RINGDOWN/C1_LEITURAS_v4.json",
      "passed": true
    },
    {
      "path": "ORDEM_013_RINGDOWN/C4_SCHEMA.json",
      "passed": true
    },
    {
      "path": "ORDEM_013_RINGDOWN/C4_CATALOG_SCHEMA.json",
      "passed": true
    },
    {
      "path": "ORDEM_013_RINGDOWN/C4_GWTC3_SCHEMA.json",
      "passed": true
    },
    {
      "path": "ORDEM_013_RINGDOWN/bis/e0_core/DATASET.json",
      "passed": true
    },
    {
      "path": "ORDEM_013_RINGDOWN/NUISANCE_V1.json",
      "passed": true
    },
    {
      "path": "ORDEM_013_RINGDOWN/PORTAO_DA_AMPLIACAO_V1.json",
      "passed": true
    },
    {
      "path": "ORDEM_013_RINGDOWN/bis/F2_CONTROL_SCHEMAS.json",
      "passed": true
    },
    {
      "path": "ORDEM_013_RINGDOWN/bis/e1_selection/SELECTION_AND_CONTROLS.json",
      "passed": true
    },
    {
      "path": "TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md",
      "passed": true
    },
    {
      "path": "ORDEM_013_RINGDOWN/cache/public/21454847/pSEOB.tar.gz.receipt.json",
      "passed": true
    },
    {
      "path": "ORDEM_013_RINGDOWN/cache/public/17018009/TGR_companion_S250114ax_results.tar.gz.receipt.json",
      "passed": true
    },
    {
      "path": "ORDEM_013_RINGDOWN/bis/e7_prepare/EXTRACTION_PLAN.json",
      "passed": true
    },
    {
      "path": "ORDEM_013_RINGDOWN/bis/e7_prepare/PLAN.md",
      "passed": true
    },
    {
      "path": "ORDEM_013_RINGDOWN/tgl_ringdown_prediction.py",
      "passed": true
    },
    {
      "path": "ORDEM_013_RINGDOWN/bis/e7_prepare/HANDOFF_FINAL_v3.md",
      "passed": true
    },
    {
      "path": "ORDEM_013_RINGDOWN/bis/E2_DESIGN_DRAFT_003.json",
      "passed": true
    },
    {
      "path": "ORDEM_013_RINGDOWN/bis/e2_publication_census/E7_INDEPENDENT_REVIEW.md",
      "passed": true
    }
  ],
  "consumer_functions_changed": [
    "main",
    "run"
  ],
  "consumer_functions_added": [
    "checked_authorization",
    "validate_payload_contract"
  ],
  "no_files_written": true,
  "extractor_imported_or_executed": false,
  "no_HDF_or_real_posterior_or_strain_access": true
}
```

## Apêndice B — script independente executado via stdin

[REAL] Conservado para reprodução sob autorização e ambiente isolado. Não é instrução para executar extração nem campanha. Não importa produtor extrator; os mocks substituem transporte/guarda para testar o contrato científico isolado.

```python
from pathlib import Path
import ast, copy, hashlib, json, math, sys, types
import numpy as np
sys.dont_write_bytecode = True
B=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN')
P=B/'bis/e7_prepare'
include=json.loads((P/'E2_INCLUDE_FINAL_v3.json').read_bytes())
manifest=json.loads((P/'MANIFEST_FINAL_v3.json').read_bytes())
def load_code(name,path,wanted):
    raw=path.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==wanted
    mod=types.ModuleType(name);mod.__file__=str(path)
    exec(compile(raw,str(path),'exec'),mod.__dict__)
    return mod
m=load_code('e7_independent_consumer',P/'producer/tgl_ringdown_ampliacao.py',manifest['producer_tree_sha256']['tgl_ringdown_ampliacao.py'])
oracle=load_code('e7_independent_source',B/'tgl_ringdown_prediction.py',include['e7']['prediction_source_sha256'])
records=[]
def check(name,fn):
    try:
        detail=fn();records.append(dict(name=name,status='PASS',detail=detail))
    except Exception as exc:
        records.append(dict(name=name,status='FAIL',error=repr(exc)))
def must_raise(fn):
    try:fn()
    except (ValueError,FileNotFoundError):return True
    raise AssertionError('Expected rejection absent')
M=np.array([13.,27.,41.,65.,90.,130.,250.,700.])
A=np.array([0.,.11,.27,.43,.61,.79,.9,.97])
Z=np.array([0.,.03,.17,.4,.8,1.7,2.4,4.])
readings=('R-A','R-B','R-RAIZ-0','R-RAIZ-EP4','R-RAIZ-REST','R-LIN','R-GLOBAL')
def scalar_grid():
    errors={}
    for r in readings:
        actual=m.prediction_draws(M,A,Z,r)['delta_tau']
        expected=np.array([oracle.prediction(float(mm),float(aa),r,redshift=float(zz))['delta_tau'] for mm,aa,zz in zip(M,A,Z)])
        np.testing.assert_allclose(actual,expected,rtol=2e-14,atol=0)
        errors[r]=float(np.max(np.abs((actual-expected)/expected))) if np.any(expected) else 0.
    return {'draws_per_reading':len(M),'max_relative_errors':errors}
check('T01 scalar source pin and vector regression on new grid',scalar_grid)
def independent_qnm():
    masses=np.array([17.,45.,120.,300.]);spins=np.array([-.7,-.1,.2,.75]);zs=np.array([0.,.4,1.,3.])
    q=np.array([.6-.08j,.65-.07j,.7-.06j,.9-.04j])
    b=7.2973525693e-3*math.exp(.5);c=299792458.;G=6.67430e-11;HB=6.62607015e-34/(2*math.pi)
    tm=masses*1.3271244e20/c**3;tp=math.sqrt(HB*G/c**5)
    u=q.real;v=-q.imag;z1=1+zs
    base={'R-A':b*tp*z1*u*u/(2*tm*v),'R-B':b*u*u/(2*v),'R-RAIZ-0':b*u/(2*v),'R-LIN':b*u/v,'R-GLOBAL':np.zeros(4)}
    root=np.sqrt(1-spins*spins)
    base['R-MOD']=b*2*math.pi*(1+root)*(u-spins/(1+root))**2/(root*v)
    for r,x in base.items():
        got=m.prediction_draws(masses,spins,zs,r,q)['delta_tau']
        want=-x/(1+x)
        np.testing.assert_allclose(got,want,rtol=2e-14,atol=0)
    return {'dimensionless_x_derivations':list(base),'signed_spins_checked':True}
check('T02 independent dimensionless formula oracle including signed R-MOD',independent_qnm)
def dimensions():
    q=np.full(4,.65-.07j);a=np.full(4,.4);mass=np.array([30.,60.,30.,60.]);z=np.array([0.,0.,1.,1.])
    def x(r):
        d=m.prediction_draws(mass,a,z,r,q)['delta_tau'];return -d/(1+d)
    xa=x('R-A');np.testing.assert_allclose(xa/xa[0],[1,.5,2,1],rtol=2e-14,atol=0)
    for r in ['R-B','R-RAIZ-0','R-LIN','R-MOD']:np.testing.assert_allclose(x(r)/x(r)[0],np.ones(4),rtol=2e-14,atol=0)
    rest=x('R-RAIZ-REST');np.testing.assert_allclose(rest/rest[0],[1,.25,4,1],rtol=2e-14,atol=0)
    np.testing.assert_allclose(x('R-RAIZ-EP4'),xa,rtol=2e-14,atol=0)
    return 'Mass/redshift scalings and EP/4 large-offset asymptote hold for synthetic astrophysical domain.'
check('T03 dimensional scaling and redshift controls',dimensions)
def lifetime():
    q=np.full(8,.8-.06j);b=m.beta_runtime();tm=M*1.3271244e20/299792458.**3
    tau=tm/.06;gam=b*.8/tm
    got=m.prediction_draws(M,A,Z,'R-LIN',q)['delta_tau']
    np.testing.assert_allclose(got,1/(1/tau+gam)/tau-1,rtol=2e-14,atol=0)
    assert np.all((got>-1)&(got<0))
    return 'Independent sum of decay rates, amplitude convention, no extra energy factor.'
check('T04 harmonic lifetime identity and sign',lifetime)
def closed_projection():
    d=np.array([-.25,.13,-.11,.41]);sig=np.array([.7,1.1,.4,.9]);weights=1/sig**2
    avg=np.sum(weights*d)/weights.sum();want=np.sum(weights*(d-avg)**2)
    got=m.conditional_projection(d,sig,np.ones((4,1)))
    np.testing.assert_allclose(got['projected_information'],want,rtol=2e-14,atol=0)
    assert got['z_physical'] is None and got['lnB'] is None
    return {'information':got['projected_information'],'closed_form':float(want)}
check('T05 independent weighted-intercept closed form',closed_projection)
def projection_scales():
    d=np.array([1.,2.,4.,8.]);sig=np.array([.7,1.,1.3,.9]);design=np.ones((4,1))
    info=m.conditional_projection(d,sig,design)['projected_information']
    tiny=m.conditional_projection(d*1e-40,sig,design)['projected_information']
    np.testing.assert_allclose(tiny/info,1e-80,rtol=2e-14,atol=0)
    assert m.conditional_projection(np.ones(4)*.01,sig,design)['projected_information']==0
    must_raise(lambda:m.conditional_projection(d,sig,np.ones((4,2))))
    return {'tiny_information':tiny,'constant_absorbed':True,'singular_refused':True}
check('T06 tiny effects and degenerate nuisance controls',projection_scales)
def fixture():
    return dict(event_id='MOCK_ONLY',role='calibration',N=8,N_source=8,source_path='fake/source.h5',source_sha256='a'*64,tar_path='fake/source.tar',tar_sha256='b'*64,dataset='samples',model='MOCK_ONLY',mass_frame='detector',mass_unit='solar_mass',source_field_mapping={k:k for k in m.FIELDS},samples=dict(df220=[.1,.2,.3,.1,-.2,-.4,.5,.6],dtau220=[.5,.4,.3,.1,-.1,-.3,-.5,-.7],Mfdet=M.tolist(),af=A.tolist(),z=Z.tolist()),priors={k:dict(status='DECLARADO_TEXT_NOT_NORMALIZED' if k in ('df220','dtau220') else 'OPEN_DERIVED_PRIOR_NOT_DECLARED',declarations=[{'path':'mock/'+k,'text':['Uniform(-1,1)']}] if k in ('df220','dtau220') else [],density=None,joint_factorization='OPEN') for k in m.FIELDS},thinning={'factor':1,'seed':None,'method':'none'},sample_weights='equal_as_stored')
def pairing():
    e=fixture();got=m.reading_diagnostics([e])['R-B']['events'][0];d=m.prediction_draws(M,A,Z,'R-B')['delta_tau'];t=np.array(e['samples']['dtau220'])
    cov=float(np.sum((t-t.mean())*(d-d.mean()))/(len(t)-1))
    np.testing.assert_allclose(got['cov_dtau_prediction'],cov,rtol=2e-14,atol=0)
    v=np.var(t,ddof=1)+np.var(d,ddof=1)-2*cov
    np.testing.assert_allclose(got['residual_std_ddof1']**2,v,rtol=2e-14,atol=0)
    ee=copy.deepcopy(e)
    for k in m.FIELDS:ee['samples'][k]=ee['samples'][k][::-1]
    perm=m.reading_diagnostics([ee])['R-B']['events'][0]
    np.testing.assert_allclose(perm['residual_mean'],got['residual_mean'],rtol=2e-14,atol=0)
    ee['samples']['dtau220']=ee['samples']['dtau220'][::-1]
    shuffled=m.reading_diagnostics([ee])['R-B']['events'][0]
    assert not math.isclose(shuffled['cov_dtau_prediction'],cov,rel_tol=1e-3)
    return {'paired_covariance':cov,'row_permutation_invariant':True,'single_column_shuffle_changes_covariance':True,'equal_length_alone_does_not_prove_pair_identity':True}
check('T07 pair covariance and residual variance identities',pairing)
def invalids():
    for field,value in [('z',float('nan')),('Mfdet',0.),('af',1.)]:
        e=fixture();e['samples'][field][0]=value;must_raise(lambda:m.validate_events([e]))
    e=fixture();e['samples']['z'].pop();must_raise(lambda:m.validate_events([e]))
    must_raise(lambda:m.validate_events([fixture(),fixture()]))
    e=fixture();e['event_id']='ALIAS';must_raise(lambda:m.validate_events([fixture(),e]))
    return 'nonfinite, domains, unequal length, duplicate event/product refused'
check('T08 invalid samples and duplicate controls',invalids)
def open_channels():
    for r in ['R-MOD','R-PROP','R-RAIZ-COHERENT']:
        got=m.prediction_draws(M,A,Z,r);assert got['delta_tau'] is None and got['status']=='OPEN'
    assert m.prediction_draws([20.,30.],[-.1,.3],[0.,1.],'R-B')['status']=='OPEN'
    must_raise(lambda:m.prediction_draws([20.,30.],[.9,.9],[0.,1.],'R-MOD',[.1-.1j,.1-.1j]))
    must_raise(lambda:m.prediction_draws([20.,30.],[.1,.2],[0.,1.],'R-MOD',[.6+.1j,.7-.1j]))
    diag=m.reading_diagnostics([fixture()]);assert all(r['mode_440']['status'].startswith('OPEN') for r in diag.values())
    return 'Missing QNM, negative-spin BCW, forbidden corotation, unstable QNM and absent 440 fail closed.'
check('T09 OPEN channels and exact-QNM domain guards',open_channels)
reg={'e7':{'readings':{r:{'N_target_information':None,'status':'OPEN'} for r in m.READINGS}}}
def conservative_gate():
    variants=[{},dict(systematic_calibration_paid=True,physical_likelihood_paid=True,sigma_c_physically_calibrated=.1,selection_efficiency=.9,global_restricted_prior_normalization=1.),dict(systematic_calibration_paid=True,physical_likelihood_paid=True,sigma_c_physically_calibrated=-1,selection_efficiency='bad',global_restricted_prior_normalization={})]
    states=[]
    for gate in variants:
        for count in (0,1):
            rows=m.verdict_matrix(reg,{'gate':gate},count)
            assert len(rows)==20 and all(r['z_physical'] is None and r['lnB'] is None for r in rows)
            assert set(r['verdict'] for r in rows)=={'AWAITING_DATA' if count==0 else 'INCONCLUSIVE_SYSTEMATICS'}
            states.append(rows[0]['systematic_gate'])
    return {'gate_labels':states,'malformed_nonnull_gate_labeled_UNVERIFIED_not_red':True,'never_green_or_confirmed':True}
check('T10 adversarial nuisance claims cannot create physical verdict',conservative_gate)
def hashes_and_json():
    must_raise(lambda:m.require_pin(P/'producer/tgl_ringdown_ampliacao.py','0'*64))
    must_raise(lambda:m.require_pin(P/'producer/tgl_ringdown_ampliacao.py',None))
    must_raise(lambda:m.unique_object([('x',1),('x',2)]))
    must_raise(lambda:m.contained(B,'../escape'))
    return 'Wrong/missing hash, duplicate JSON key and path escape refused, all read-only.'
check('T11 pins JSON and path controls',hashes_and_json)
def imports():
    tree=ast.parse((P/'producer/tgl_ringdown_ampliacao.py').read_bytes())
    names={a.name.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names}
    names|={n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)}
    assert not names & {'scipy','h5py','bilby','extrai_posteriores_pseob'}
    return {'imports':sorted(names),'extractor_imported':False}
check('T12 consumer scientific imports NumPy only',imports)

from datetime import datetime,timezone
def consumer_probe(mutate=None, auth_mutate=None, blind_plan=False, missing_auth=False):
    event=fixture()
    planned={k:copy.deepcopy(v) for k,v in event.items() if k not in ('samples','priors','N','source_field_mapping','thinning','sample_weights')}
    planned['fields']={k:k for k in m.FIELDS}
    planned['prior_paths']={k:['mock/'+k] if k in ('df220','dtau220') else [] for k in m.FIELDS}
    if blind_plan:planned['role']='blind_test'
    rr=copy.deepcopy(reg);rr['registered_utc']='2026-01-01T00:00:00+00:00'
    rr['statistics']={'maximum_information_weight_INPUT':.2,'split_null_seed':123}
    rr['e7'].update(nuisance_path='fake/nuisance.json',plan_path='fake/plan.json',plan_sha256='c'*64,nuisance_sha256='d'*64,prediction_source_sha256=include['e7']['prediction_source_sha256'],producer_tree_sha256=manifest['producer_tree_sha256'])
    plan={'catalogue':'MOCK_ONLY','status':'READY_FOR_REGISTERED_CALIBRATION_EXTRACTION','events':[planned]}
    pay={'catalogue':'MOCK_ONLY','registration_sha256':'e'*64,'plan_sha256':'c'*64,'producer_tree_sha256':manifest['producer_tree_sha256'],'events':[event],'authorization_sha256':'f'*64,'schema':'POSTERIORES_PSEOB_V1'}
    auth={'status':'AUTHORIZED_BY_PRINCIPAL_AFTER_E2','registration_sha256':'e'*64,'plan_sha256':'c'*64,'producer_tree_sha256':manifest['producer_tree_sha256'],'registered_utc':'2026-01-02T00:00:00+00:00'}
    if mutate:mutate(event,pay)
    if auth_mutate:auth_mutate(auth)
    accesses=[];diagnostics=[]
    def reader(path):
        n=Path(path).name;accesses.append(n)
        return {'nuisance.json':{'gate':{}},'plan.json':plan,'payload.json':pay,'auth.json':auth}[n]
    old=(m.checked_context,m.read_json,m.require_pin,m.fullsample_diagnostics)
    m.checked_context=lambda *args:(rr,types.SimpleNamespace(authorize_event=lambda *args:True,utc=datetime.fromisoformat))
    m.read_json=reader
    m.require_pin=lambda *args:None
    def diag(*args):diagnostics.append('reached');return old[3](*args)
    m.fullsample_diagnostics=diag
    try:
        result=m.run(B,'mock-registration','e'*64,'payload.json','0'*64,None if missing_auth else 'auth.json',None if missing_auth else 'f'*64)
        return {'accepted':True,'reported_N':result['fullsample_diagnostics']['events'][0]['N'],'physical_lnB':result['lnB'],'physical_z':result['z_physical'],'reads':accesses,'diagnostics':diagnostics}
    except (ValueError,KeyError,TypeError) as exc:
        return {'accepted':False,'error':str(exc),'reads':accesses,'diagnostics':diagnostics}
    finally:m.checked_context,m.read_json,m.require_pin,m.fullsample_diagnostics=old
def valid():
    r=consumer_probe();assert r['accepted'] and r['reported_N']==8 and r['physical_lnB'] is None and r['physical_z'] is None;return r
check('T13 v3 mock full consumer valid baseline',valid)
probes=[]
def negative(name,mutator=None,**kwargs):
    r=consumer_probe(mutator,**kwargs)
    probes.append({'name':name,'expected':'REJECT_BEFORE_DIAGNOSTICS','passed':not r['accepted'] and not r['diagnostics'],'evidence':r})
def trunc(e,p):
    for k in m.FIELDS:e['samples'][k]=e['samples'][k][:2]
    e['N']=e['N_source']=2
negative('F1a self-consistent truncation',trunc)
for key,value in [('mass_frame','source'),('mass_unit','kilogram'),('model','wrong'),('source_field_mapping',{k:'wrong' for k in m.FIELDS})]:
    negative('F1b '+key,lambda e,p,k=key,v=value:e.update({k:v}))
negative('F1c malformed priors',lambda e,p:e.update(priors={k:{'status':'ANY_STRING','declarations':None} for k in m.FIELDS}))
for key in ('schema','authorization_sha256','catalogue','registration_sha256','plan_sha256','producer_tree_sha256'):
    negative('F1d mismatch '+key,lambda e,p,k=key:p.update({k:'WRONG'}))
negative('F1e missing authorization payload pin',lambda e,p:p.pop('authorization_sha256'))
negative('F1f missing independent authorization',missing_auth=True)
negative('F1g early authorization',auth_mutate=lambda a:a.update(registered_utc='2025-01-01T00:00:00+00:00'))
for key in ('status','registration_sha256','plan_sha256','producer_tree_sha256'):
    negative('F1h authorization '+key,auth_mutate=lambda a,k=key:a.update({k:'WRONG'}))
prior_mutations=[
 ('path',lambda d:d['declarations'][0].update(path='wrong')),
 ('empty-text',lambda d:d['declarations'][0].update(text=[''])),
 ('nontext',lambda d:d['declarations'][0].update(text=[1])),
 ('too-long',lambda d:d['declarations'][0].update(text=['x'*100001])),
 ('density-paid',lambda d:d.update(density=1)),
 ('factorization-paid',lambda d:d.update(joint_factorization='PAID'))]
for name,fn in prior_mutations:
    negative('F1i prior '+name,lambda e,p,f=fn:f(e['priors']['dtau220']))
negative('F1j blind plan blocked before payload',blind_plan=True)
assert 'payload.json' not in probes[-1]['evidence']['reads']
future=consumer_probe(auth_mutate=lambda a:a.update(registered_utc='2999-01-01T00:00:00+00:00'))
# Parse extractor only; evaluate its rejection predicates on fake nodes.
# No extractor module/function, HDF file, dataset or prior values are opened.
import h5py
etree=ast.parse((P/'producer/extrai_posteriores_pseob.py').read_bytes())
priorfn=next(n for n in etree.body if isinstance(n,ast.FunctionDef) and n.name=='prior_metadata')
conditions=[n for n in ast.walk(priorfn) if isinstance(n,ast.If)]
meta=next(n for n in conditions if any(isinstance(z,ast.Attribute) and z.attr=='is_virtual' for z in ast.walk(n.test)))
alloc=next(n for n in conditions if any(isinstance(z,ast.Attribute) and z.attr=='itemsize' for z in ast.walk(n.test)))
metacode=compile(ast.Expression(meta.test),'extractor_metadata_guard_ast','eval')
alloccode=compile(ast.Expression(alloc.test),'extractor_allocation_guard_ast','eval')
class Dataset:pass
fakeh5=types.SimpleNamespace(Dataset=Dataset,check_string_dtype=h5py.check_string_dtype)
f2=[]
for label,dtype,virtual,external,size,want in [
 ('virtual_text',np.dtype('S10'),True,None,1,True),
 ('external_text',np.dtype('S10'),False,[('fake',0,10)],1,True),
 ('object_reference',h5py.ref_dtype,False,None,1,True),
 ('numeric_vlen',h5py.vlen_dtype(np.dtype('i4')),False,None,1,True),
 ('plain_object',np.dtype('O'),False,None,1,True),
 ('numeric',np.dtype('f8'),False,None,1,True),
 ('zero_elements',np.dtype('S10'),False,None,0,True),
 ('too_many_elements',np.dtype('S10'),False,None,257,True),
 ('oversize_fixed',np.dtype('S100001'),False,None,1,True),
 ('fixed_text',np.dtype('S10'),False,None,1,False),
 ('vlen_text',h5py.string_dtype(),False,None,1,False)]:
    node=Dataset();node.dtype=dtype;node.is_virtual=virtual;node.external=external;node.size=size
    env={'node':node,'h5py':fakeh5}
    rejected=bool(eval(metacode,env) or eval(alloccode,env))
    f2.append({'name':label,'rejected':rejected,'expected_rejected':want,'passed':rejected==want})
readline=min(n.lineno for n in ast.walk(priorfn) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='node')
assert meta.lineno<readline and alloc.lineno<readline
# Verify custody using metadata/code bytes only.
audit={}
for name,entry in manifest['files'].items():
    raw=(P/name).read_bytes()
    audit[name]={'hash_matches':hashlib.sha256(raw).hexdigest()==entry['sha256'],'size_matches':len(raw)==entry['bytes'],'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
for name in ('MANIFEST_FINAL_v3.json','E7_ASSEMBLY_V3.json'):
    raw=(P/name).read_bytes();audit[name]={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
inputpins=[]
for name,pin in include['input_pins_relative_to_Chatgpt'].items():
    # Only previously declared metadata/code inputs; refuse unexpected data extensions.
    path=B.parent/name
    if path.suffix.lower() not in ('.json','.md','.py','.txt'):raise AssertionError('Unexpected input type; no read permitted: '+name)
    raw=path.read_bytes();inputpins.append({'path':name,'passed':hashlib.sha256(raw).hexdigest()==pin})
def fns(raw):
    t=ast.parse(raw);return {n.name:ast.dump(n,include_attributes=False) for n in t.body if isinstance(n,ast.FunctionDef)}
old=fns((P/'snapshot_v2_before_review_fixes/producer/tgl_ringdown_ampliacao.py').read_bytes())
new=fns((P/'producer/tgl_ringdown_ampliacao.py').read_bytes())
changed=sorted(k for k in old.keys()&new.keys() if old[k]!=new[k])
added=sorted(new.keys()-old.keys())
output={'runtime':{'python':sys.version.split()[0],'numpy':np.__version__},'tests':records,'test_count':len(records),'test_failures':sum(r['status']=='FAIL' for r in records),'negative_probes':probes,'negative_passed':sum(r['passed'] for r in probes),'F2_AST_predicates':f2,'F2_metadata_before_read':True,'future_authorization_residual':future,'manifest_audit':audit,'input_pins_audit':inputpins,'consumer_functions_changed':changed,'consumer_functions_added':added,'no_files_written':True,'extractor_imported_or_executed':False,'no_HDF_or_real_posterior_or_strain_access':True}
print(json.dumps(output,ensure_ascii=False))
```

