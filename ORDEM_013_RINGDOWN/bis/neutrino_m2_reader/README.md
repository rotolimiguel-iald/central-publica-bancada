[REAL — T11, ferramenta de bancada; não altera registro nem gate]

# Leitor do neutrino

Lê EXTRACTED_RULES.json mediante hash externo. O extrator leu apenas bytes e nós literais AST da cópia do um.py; nunca o importou/executou. O hash congelado reproduz o registro: `e24877751ad810225412cc294c06b83eefeaedc67e4c5cabc7779ac01e4b19c3`.

Baseline: 8.507414099900329 meV, tensão 2.9528540277344604σ CONTRA a escala 1 eV [NORM], veredito TGL_NU_M2_ARMED_CONSISTENT. São os números do registro legado, sem nova conferência independente dos artigos experimentais.

Uso: `python -X utf8 -B reader.py --snapshot-sha256 d0a679c49026d204fa4d920a858cd55a40de158b7a36f557ea3aab9a426496c1`. Para novo JSON, acrescentar `--release <arquivo> --release-sha256 <hash obtido da fonte de custódia>`. A fonte primária exige URL, citação, cópia local e SHA256; o programa confere os bytes, não certifica a transcrição dos números nem a autonomia dos experimentos. Esses dados devem ser verificados pelo operador/gerência.

Fixture exige `fixture:true` e `--allow-fixtures`; resultado marcado FIXTURE_NOT_DATA. Nunca substituir dado experimental por fixture. A regra preserva os grupos autônomos e não conta uma combinação global como segundo experimento. Não emite MATCHED_PROSPECTIVELY porque esse ramo não existe na implementação congelada, embora o texto o liste entre os vereditos permitidos.

Uma medição isolada ≥5σ produz no máximo TENSION e a bandeira; duas determinações autônomas ≥5σ podem satisfazer a kill_rule. O veredito do registro só muda por incorporação pela gerência e novo rito ratificado.

19 testes PASS: TEST_RECEIPT.json e TESTS.log. Sem hora de máquina pesada; sem chamada remota.
