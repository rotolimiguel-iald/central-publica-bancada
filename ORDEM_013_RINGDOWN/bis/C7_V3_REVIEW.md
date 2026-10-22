[REAL — revisão lateral F6/F7; replay do operador conferido por recibos; OPEN — guardas, limpeza e documentação]

# Revisão C7 v3_1

Data UTC: 2026-09-22T18:37:11.905530+00:00. Raiz: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN`. O pacote efetivo está em `C7_INDEPENDENT_v3_1/`; B é a variável de raiz nos construtores, não uma subpasta existente.

**Parecer: reprodução ordinária registrada como PASS, mas pacote ainda não aprovado sem ressalvas.** A comparação numérica aceita silenciosamente NaN em uma posição não inicial; há uma falha de limpeza antes do try; a marca Unicode exata de R-MOD continua corrompida. O README também promete rastreabilidade de licenças que não está embarcada no manifesto. Os achados F2/C6 encerrados não foram reabertos.

## O que confere

- 73/73 arquivos de cada manifesto v3 e v3_1 conferem por tamanho/hash. Os dois ZIPs contêm exatamente os 73 arquivos mais MANIFEST, com bytes idênticos às pastas. A v3 anterior está preservada. Da v3 para v3_1 mudaram apenas README, OVERVIEW, reading_scope.json/csv e o módulo público de predição; a árvore congelada reproduction permanece idêntica.
- A tabela possui dez leituras × seis conjuntos, 60 chaves únicas. Números, estatutos, nulls, vereditos condicionais, contexto de sigma/z e marcas analíticas conferem com F2 fechado. Os campos novos C1_scope, EXCLUDED_IF_UNIVERSAL e C6_pre_lnB conferem com as fontes hasheadas. CSV conserva a projeção de todos os campos, sem promover zeros analíticos a medições.
- Fixture é exatamente per_series[2] do arquivo declarado, com hash correto. Executei apenas `python -B -O unit_checks.py` do pacote com o Python bundled: PASS, cinco recusas de entrada; regressões A/B com erros relativos 3,951998679763808e−16 e 3,4760409478204096e−16. Conversão exata da taxa, a=0/a=1 e onset passam. Não houve replay C6 por esta revisão.
- O wrapper recusa output dentro do pacote e resultado preexistente, usa temporário filho do work-root resolvido, verifica hashes do strain antes/depois da cópia e recusa grids/resultados C6 previamente presentes na área de execução. O finally normal confere o alvo como descendente próprio antes de removê-lo; não houve exclusão real na sonda adversarial.
- Downgrade não é token fixo: a sonda aceita NOT_VERIFIED e os estados inconclusivos previstos e recusa CONFIRMED, EXCLUDED_IN_READING, PASS e string vazia. Falta/duplicata de linha e erro finito 0,1 são recusados. A aprovação numérica permanece distinta do estatuto físico.
- README/OVERVIEW têm escopo 220/440, ensemble versus realização OPEN, paredes Kerr/laboratório, contraste entre gerador positivo-raiz e postulado modular, tensão R-RAIZ-0, BCW/exato, perfis de constantes, delta_tau_linear legado, onset/fase/overtones, Occam e aviso MAX_PATH. São correções substantivas presentes; os defeitos editoriais abaixo não apagam isso.

**Execução iniciada pelo operador (session49378):** ao fim desta revisão existiam C7_V3_1_CLEAN_VALIDATION.json e C7_V3_1_C6_REPLAY.json, com PASS_BYTE_UNIT_AND_C6_NUMERICAL_REPRODUCTION e PASS_NUMERICAL_REPRODUCTION, 75 linhas, diferença máxima 0, estatuto científico INCONCLUSIVE_SYSTEMATICS. Conferi hashes do ZIP, manifesto, wrapper, registro, referência congelada e cinco logs; os dois diretórios temporários informados já não existem. É conferência independente dos recibos dessa execução, não uma segunda execução minha. O defeito de NaN é demonstrado por mutação, não detectado nesse replay ordinário.

## Achados e correções exatas

**C7-R1 — P1, falso aceite de não finito.** Em `refeito/reproduce_c6_v3.py:67`, max(abs(actual−reference)) seguido de `error > 1e-5` não recusa NaN. Isolei o bloco real por AST sob optimize=1 e alterei apenas lnB_vs_GR da segunda linha para NaN: a guarda aceitou com max_error=0,0. O relatório resumido pode ser serializado com allow_nan=False porque o NaN ficou apenas na entrada, não no resumo; essa opção de escrita não corrige a falha.

Correção: leitura JSON estrita com rejeição de NaN/Infinity e validação explícita de finitude/tipo de todos os números comparados (incluindo chaves numéricas) antes de diferenças/max. Manter cobertura e unicidade e validar também finitude do erro final. Usar ValueError explícito, operante sob −O. Aceitação: NaN/±Infinity em qualquer posição devem recusar; amostra íntegra e downgrade legítimo devem continuar passando. Não exige nova ciência para testar a guarda.

**C7-R2 — P2, limpeza não cobre toda criação.** `validate_package_v3_013bis.py:9` cria o temporário; `:12` pode lançar FileExistsError por recibo já existente; o try/finally só começa em `:15`. Simulei esse caminho com objetos em memória: um diretório criado, zero remoções. É falha reproduzível ao tentar validar novamente com recibo existente. No wrapper há a mesma janela estrutural: chmod em `reproduce_c6_v3.py:43` fica depois da criação e antes do try.

Correção: verificar saídas já existentes antes de mkdtemp e colocar todo o ciclo após a criação (incluindo chmod/preparação/hash suscetível a erro) sob finally, preservando a validação do alvo descendente resolvido. Não resolver com remoção ampla do work-root. Testar falhas logo após criação e nas precondições sem tocar diretórios reais da campanha. A remoção no caminho ordinário do replay atual confere; a promessa “incluindo falhas” ainda não vale para esses caminhos.

**C7-R3 — P2 editorial, string exata de R-MOD.** A atribuição a scope existe agora em `tgl_ringdown_prediction.py:119` e contém as palavras e duas paredes requeridas. Contudo, o separador é a sequência Unicode U+00E2/U+20AC/U+201D, não o travessão U+2014. O teste literal `CONJECTURE — management hypothesis, not TGL canon` falha no scope, README, OVERVIEW e nas seis linhas R-MOD. Há também corrupção em “5–95%”. Isso foi conferido por codepoints, não pela aparência do terminal.

Correção em novo builder/pacote: gerar texto UTF-8 correto (pode usar escape Python `\u2014` para a constante), centralizar a marca e testá-la integralmente nas quatro superfícies; manter as paredes completas no scope/README. Testar o valor retornado para R-MOD com QNM fornecido, além da recusa sem QNM. Não editar os arquivos/manifests deste pacote selado para corrigir a codificação.

**C7-R4 — P2 documental, licença afirmada sem recibo embarcado.** README:49 afirma que cada licença upstream foi preservada separadamente e que recibos identificam os releases. No universo de 73 arquivos do manifesto, somente README e OVERVIEW contêm menção a licença; não há manifesto/recibo de licenças por arquivo nem textos de licença embarcados. A lista narrativa de quatro releases não é o vínculo de proveniência exigido em F7.

Correção: incluir na próxima versão o recorte verificável do manifesto de downloads/atribuições aplicável ao bundle, vinculando caminhos/hashes embarcados à origem e à licença documentada, sem inferir licença para o código de pesquisa. Preservar textos upstream aplicáveis ou declarar precisamente o que é somente referência externa. Até lá, reformular a frase para não afirmar preservação dentro do pacote. Não foi feita análise jurídica nem nova consulta aos provedores nesta revisão; o achado é a ausência da evidência documental prometida.

**Ajustes menores do README:** os intervalos por evento do catálogo estão em `evidence/C4_CATALOG_220.json`, não no agregado de `current_evidence/F2_ALL_READING_TABLES_v2.json`; corrigir o ponteiro da linha 11. A entrada é inglesa, mas current_evidence ainda contém quatro adendos Markdown em português: se o critério “bundle em inglês” for literal para toda documentação corrente, falta versão inglesa ao lado; preservar os originais como fontes históricas. Nenhuma leitura deve virar preferida nessa edição.

## Limites, reprodução e integridade

O foco foi o pacote e os três construtores pedidos. Não auditei novamente ciência F2/C6, calibração C5, nem a limpeza de todas as outras pastas C7 da casa. Não há arquivo >25 MB entre os 73 membros examinados; isso não quita sozinho o critério global F7. A aceitação em extração limpa tem o recibo lido acima; pasta profunda não foi testada, estando pago apenas o aviso MAX_PATH permitido pela ordem.

Controle próprio: `bis/c1_review/c7_v3_checks.py`, executado com Python bundled `-B -O`; hashes/ZIP/tabela/fixture, unidades leves e sondas AST/mock sem subprocesso C6. Resultado em c7_v3_results.json. Conferência dos recibos da execução do operador: c7_replay_receipt_check.json. Nenhum pacote, manifesto ou produção foi escrito; nenhuma C6 concorrente foi criada, interrompida ou aguardada por ferramenta. Axiomas: N/A — sem Lean. Repetir controles em cópia isolada, pois as saídas recusam sobrescrita.

| Caminho relativo à raiz | SHA256 lido |
|---|---|
| `refeito/build_independent_v3_1_013bis.py` | `d996a35be9318de6071646c57c3397a6a7d01830ef758ebf985016b34e1d7cbe` |
| `refeito/reproduce_c6_v3.py` | `09c9189a887348bdd7a10dc4506033c1e22f3d69fc67bfede203dd424067290e` |
| `refeito/validate_package_v3_013bis.py` | `d0e450c11baeb9f9249eb7b20bf1c84a13d51cb9532aafe92e686893caadeb60` |
| `C7_INDEPENDENT_v3_1/MANIFEST.json` | `3100982b19ae1620a1a02f3badbf7685377d9bd291eaa128ac08815cb15bf574` |
| `cache/C7_INDEPENDENT_v3_1.zip` | `2c72c21a56278be9533065b2d2ec7a59ffe629afd4ef703119fe8150d5cce51d` |
| `C7_INDEPENDENT_v3/MANIFEST.json` | `71a3a56bbe6c94a9545dabadb4c701702d8d8239912266875610bcbe8a6c5b14` |
| `cache/C7_INDEPENDENT_v3.zip` | `ae8832e1e3d20986cc73c864a16d0da26a6c85e6b6abbe7f1e1925112ffce01f` |
| `bis/C7_V3_1_C6_REPLAY.json` | `533c84345ef2bfefff0ea87fe3ac588e3508ca9a401953b8bdcc64840e66f505` |
| `bis/C7_V3_1_CLEAN_VALIDATION.json` | `9c6e17d81047c9bd8c9d91538ec2249facf14ac39050ea4acbb6e4fa8166396b` |
| `bis/c1_review/c7_v3_checks.py` | `810e45481d528412bbf95034ce6025197a727dd1e36bbb07f25c94c630c7edac` |
| `bis/c1_review/c7_v3_results.json` | `9a6770f7b4cb7c1fe05c7c5eefdb426153a93eedcc31fc042fe3648cf1a31b5e` |
| `bis/c1_review/c7_replay_receipt_check.json` | `9f92d59517f0f1a34c621ff5cb101210213fbe91766db31515b634357f0d20f2` |


---

## Adendo — seis wrappers e fechamento parcial dos suplementos

[REAL — auditoria de bytes, recibos e controles em memória; OPEN — confinamento antes de mkdir dos três suplementos]

Data UTC: 2026-09-22T18:53:57.099088+00:00. O parecer v3_1 acima é histórico. **No pacote principal, C7-R1–R3 estão fechados pelo C7_V3_2_CLOSING_REVIEW.md e C7-R4 está fechado pelo C7_V3_3_CLOSING_REVIEW.md.** Este adendo trata somente do desenho de execução/cleanup dos suplementos. Não reabre ciência C5, PE, injeções, F2/C6 ou o diagnóstico de injeção A, reservado a outro revisor.

| Pacote efetivamente revisto | Arquivos no manifesto | Recibo do operador | Resultado da revisão |
|---|---:|---|---|
| `C7_POSTERIOR_REPRODUCTION_v3_1` | 20 | negativa fonte ausente, removido | janela fechada; mkdir antes da guarda permanece |
| `C7_GWTC3_REPRODUCTION_v3_1` | 26 | negativa fonte ausente, removido | janela fechada; mkdir antes da guarda permanece |
| `C7_INJECTION_REPRODUCTION_v3_1` | 26 | negativa fonte ausente, removido | janela fechada; mkdir antes da guarda permanece |
| `C7_COHERENT_SOURCE_REPRODUCTION_v3` | 25 | prepare-only sem ciência, removido | desenho/controles leves aprovados |
| `C7_IMR_RECOVERY_REPRODUCTION_v3` | 25 | prepare-only sem ciência, removido | desenho/controles leves aprovados |
| `C7_NATIVE_SEOB_WAVEFORM_v3` | 12 | prepare-only sem ciência, removido | desenho/controles leves aprovados |

### Três suplementos POSTERIOR/GWTC3/INJECTION

Verifiquei as v3 e v3_1, os manifestos/ZIPs e a igualdade dos assets científicos. A v3_1 altera somente README e reproduce.py entre os arquivos embarcados; manifests mudam como esperado. Os ZIPs v1 permanecem disponíveis, com os membros científicos coincidentes com seus manifestos e os recibos históricos extras identificados nos controles. Não foi executado programa científico nem nova preparação pela auditoria.

As seis negativas do operador (três v3, três v3_1) são FileNotFoundError por ausência de fonte; os logs, intenções e recibos foram lidos e hasheados, o manifesto indicado confere e cada temporário é filho próprio do work-root e está ausente. Isso demonstra aqueles caminhos de falha, não todos os caminhos possíveis.

**C7-S1 — janela anterior ao try, corrigida na v3_1.** Na v3, preserved.mkdir podia falhar depois de mkdtemp, deixando o filho criado; reproduzi por mock nos três wrappers. Na v3_1, preserved.mkdir antecede mkdtemp e a preparação fica sob finally. As mesmas sondas agora mostram zero temporários criados nesse erro. O finally normal remove o filho validado; o finally interno também é executado se falha a escrita de CLEANUP_INTENT. Foram cinco casos por wrapper em cada versão, 30 sondas em memória sob optimize=1; nenhum diretório real foi criado/removido por elas.

**C7-S2 — P2, ainda aberto na v3_1: escrita anterior à checagem de confinamento.** POSTERIOR reproduce.py:127–130, GWTC3:130–133 e INJECTION:128–131 executam workroot.mkdir e outputroot.mkdir antes de perguntar se esses caminhos estão dentro de ROOT. Ao fornecer ROOT/new_work ou ROOT/new_output, a sonda registra mkdir interno antes do ValueError. A execução científica não chega a começar, mas o pacote que se declara imutável já recebeu um diretório.

Correção exata: resolver ambos os caminhos, comparar ambos com ROOT resolvido e recusar os internos **antes de qualquer mkdir**; somente então criar raízes externas/destino, e finalmente o temporário sob try/finally. Em nova versão, testar separadamente work-root e output-root internos: ValueError, zero mkdir, zero mkdtemp, zero subprocess. Preservar a correção S1 e os assets. Nenhuma campanha é necessária para testar isso.

### Três suplementos COHERENT_SOURCE/IMR_RECOVERY/NATIVE_SEOB

**Sem bloqueante encontrado no recorte de execução/cleanup examinado.** Os 25, 25 e 12 arquivos conferem com os manifestos e ZIPs. reproduce_legacy.py é byte a byte igual ao reproduce.py original de cada pacote, e todos os demais arquivos históricos têm cópia idêntica (README renomeado como histórico). Os três wrappers novos são exatamente o script genérico hasheado. Os ZIPs v1 continuam legíveis e coincidem com os arquivos/manifestos antigos.

O wrapper exige opção explícita para preparar/rodar; modo padrão apenas confere hashes. work/output internos são recusados antes de mkdir; destino é criado antes do temporário; cópia, subprocesso e coleta de resultados ficam sob finally, com alvo de remoção validado como filho próprio. O subprocesso explicitamente autorizado apontaria para reproduce_legacy.py da cópia, com cwd nessa cópia. O estatuto emitido é LEGACY_REPLAY_EXIT_ZERO, não calibração científica, e scientific_calibration fica false.

Oito controles do main real em memória sob optimize=1: default, prepare-only, subprocesso **simulado** com retorno zero e um, falha de cópia, cada raiz interna e falha do destino externo. Confirmados: nenhum subprocesso em default/prepare-only; remoção e propagação nos erros de cópia/execução; zero mkdir nas raízes internas; zero temporários no erro de destino. Não houve subprocesso científico real. Os três recibos prepare-only já produzidos pelo operador coincidem com C7_OTHER_V3_BUILD; temporários estão ausentes. A compatibilidade científica completa do replay legado permanece fora desta revisão.

### Integração final ainda não executada pela revisão

Na leitura de `refeito\build_final_bundle_v3_3_013bis.py`, SHA256 `2d352ce062a73d1806e526b156004a88c1be13fba3b0caef67392aa0df173406`, a lista de packages ainda selecionava POSTERIOR/GWTC3/INJECTION **v3**, não v3_1. Antes de gerar o bundle, apontar aos três suplementos finalmente corrigidos e transportar seus recibos correspondentes. Conferir essa seleção por script, além dos hashes internos, para não empacotar uma versão anterior que é íntegra mas conserva o defeito. O builder final não foi executado; nenhuma extração final é certificada aqui. A checagem de raiz dos wrappers analisados se refere ao seu pacote próprio; não foi demonstrada proteção automática do diretório-pai de uma entrega composta.

O adendo não promove NOT_FALSIFIED/PASS numérico a CONFIRMED. Escritas desta revisão limitadas a pareceres e controles próprios. Backup imediato byte a byte deste parecer: `C7_V3_REVIEW.md.bak_20260922_185357`, SHA256 `7166768d74034998c615e769a47a5704a06863117f94090595220ae65f85356d`.

| Caminho relativo à raiz | SHA256 lido |
|---|---|
| `refeito/build_supplements_v3_013bis.py` | `34e13ec2124dc07b089a7b5f2df14000e96dfd7d91e678e1a1c58f14cea03ade` |
| `refeito/close_supplement_creation_window_013bis.py` | `8427dfbb39aae431699350c7eae23fb47391f40860768d6d4bb9a11ad0d0ae3f` |
| `refeito/replay_legacy_in_temporary_v3.py` | `b0ad7cfc75aad16be66c0eb6093b417d8e9cd3ba2bc165bda9f486fb20cf3dd6` |
| `refeito/build_other_packages_v3_013bis.py` | `98178c2e7808cba64ca337d3a915d15d625786b4aed9dc466db0125b714a6788` |
| `bis/C7_SUPPLEMENTS_V3_CLEANUP_CONTROLS.json` | `f3b5412fe7c9f0d43e8920002b81240d8542cf5af1105b855f6ae2d8c6a364d1` |
| `bis/C7_SUPPLEMENTS_V3_1_BUILD.json` | `5ea7169a0b6d3a7f1de0e143342c5c62bc10645fc2adfb4df4b5501e35c0879a` |
| `bis/C7_OTHER_V3_BUILD.json` | `7c1178492093d70a8a6c137303cd86f5f6a9cdd456565981f1ea04afd3c49551` |
| `bis/c1_review/c7_supplement_cleanup_checks.py` | `fdb09dad3827f17e2668996f9079466ff7a55d70994682df5a37b2fc8fef709d` |
| `bis/c1_review/c7_supplement_cleanup_results.json` | `26954def09d85f4cbb449952d62d03d5cb8b2ff259276ce6ecfa3547aeb5de2d` |
| `bis/c1_review/c7_supplement_v3_1_checks.py` | `6dda8b114e274af09cac346e0da54c2e4263aaa0aa232d40919dd0b4a429f4e5` |
| `bis/c1_review/c7_supplement_v3_1_results.json` | `9cc5f5eb05d46dc51db195e2fc6bbb55e672df4b050ea6e91a080ec731147d3e` |
| `bis/c1_review/c7_other_wrapper_checks.py` | `eed2f019fbc265fd7ac81e576597c8b779e0ff179516534c55dd9b4cc4aa8a38` |
| `bis/c1_review/c7_other_wrapper_results.json` | `7ac6b523be955b9ffce213b8f28e731dab7921472b3df914d18424561bd8971d` |
