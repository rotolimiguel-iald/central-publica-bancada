# F3.2 — camada R4 do gate e runner sintético

[REAL — consulta] O Nós Vivo F3.2 aponta para o gate R3 e para a rota d1.fase9.f3_2_r1_hash_gate; a auditoria c1 AUDITORIA_F3_2_C1_a543370e.md mostrou que a janela curta do SBF «istical) $\pm 2.3» aparece três vezes na fonte pinada e era aceita. Reaproveitei o vínculo e os seis leitores documentais por hash; L1b e L6 continuam [DECLARADO_UNVERIFIED].

[REAL — G2] f9_reader_gate_v1x_r4.py exige que cada janela H0 ou componente de sigma, depois de conferir número e presença nos bytes da fonte ou projeção pinada, ocorra exatamente uma vez nesses bytes. Esta é a alternativa de unicidade pedida pela c1. As 18 janelas do vínculo atual são únicas. No teste adversarial, a R3 aceita a janela curta com três ocorrências e a R4 a recusa com ReaderGateError; a janela completa vigente é aceita. O gate não interpreta uma fonte repetida como identificada só por letras genéricas.

[REAL — integração sintética] O vínculo R4 pinou o rascunho F3.1 V2 R4 (SHA-256 3f4017bf3229903106d2c85388bde9ebfd57e076428e48af5be33c873d5c2d00, lido do arquivo). Preflight e staged R4 importam o gate R4; staged exige a função proposta veredito_fase9_v2_r4_proposta pelo hash da fonte 98ba17095fc8f84d053f8b7ab18f8c0125db323aba930e487bcb49bea924c14d, passa n_local=5 e aceita só o token sintético R4. O fixture R3 continua pinado e é apenas sintético. O teste final deu 8/8, EXIT 0, incluindo recusa do modo real.

[DERIVED — alcance do mock] synthetic_free_background toma a verossimilhança local ΛCDM do fixture e acrescenta um fator escalar de quadratura sobre um r_d gaussiano fabricado. Isso testa o encanamento da integração e da quadratura, não discrimina a TGL contra um fundo livre cosmológico. Não usa CAMB nem dado observado.

[OPEN — admissão] required_sources_admitted continua fixo em False no runner sintético porque não há ato D-H pinado. A função R4 proposta contém os limiares de dispersão χ²/(n−1)>2 ou p<0,01 em qualquer ponta; a legenda antiga NO_VERDICT_THRESHOLD_NOT_PINNED dos arquivos históricos R2/R3 não descreve a R4. O campo R4 diz explicitamente SYNTHETIC_ONLY; o veredito observado segue nulo.

[INPUT — limites vigentes] Nada foi congelado ou aberto. F3.4 e X13 precedem congelar a V2; D-H precede abrir; D-J nomeia o token. Não se gravou ALVOS_FASE9_LIDOS.json, nem se tocou Bancada, kernel ou gate.
