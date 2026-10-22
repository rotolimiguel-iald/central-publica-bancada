[REAL — R5 da fonte qualificada; T03 ainda parcial; nenhum teste físico]

Abertura015SHA256: dbd0a307438dda2969a21baf64665d54e8b70fb84c3fe10f8c233ddeac736610
Abertura016SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a

Na cópia irmã, pe_runner/pseob_source separam banda20–1024 da geração. O gerador usa fmax4096/fs8192 e devolve os bins exatos da grade de dados fs4096. A asserção de overflow precede o LAL. Retornos None/EDOM são escritos em EDOM_LOG.jsonl com massa/spin/hora, contados e cruzados com o hiper-retângulo posterior0,5%–99,5%; EDOM dentro dele impede aceitação. Quinze controles locais e quatro chamadas nativas de comparação passaram; erro máximo entre wrapper e referência na mesma grade =0. Não se comparou uma amostragem com outra como se fossem idênticas.

R5 executada source-only:1.000sorteios pelo build_priors emendado,3casos históricos(DRAW8,16,20) com440fixoRG e12cantos dentro da prior. A2048:1.013finitos+2EDOM,0aborto ⇒ NÃO QUALIFICADO. Ambos EDOM têm massas15/10 e spins0,99. f550RG nesse canto=2833.736716073Hz. A4096/8192 nos MESMOS1.015casos:1.015finitos,0EDOM,0aborto ⇒ R5 da fonte qualificada. Essa amostragem finita não prova ausência universal de erro no contínuo da prior.

Proveniência C04: quatro scripts e draws400 copiados com hashes, originais preservados. O supervisor conserva PRECALL/RETURN e recibos por filho; falha não vira rejeição física do prior. Os testes não leram strain, posterior cego ou semente real e não iniciaram PE. A V1 ainda retorna TimeoutError esperado após verificar seu contrato/runtime.

Guarda: funções de cadeia adicionadas ao módulo existente,18controles passaram, incluindo sub-objeto estatístico imutável, célula V1 reutilizada, pai errado, testemunha alterada, lacuna ordinal, job substituído e promoção antes da primeira testemunha. A primeira implementação presumiu lista para nulls.cells; a fonte é dicionário por ID, corrigido antes dos controles, tentativa preservada. Pins históricos vêm dos bytes. As funções AINDA NÃO estão ligadas a checked_registration: não há registro/testemunha V1.1 nem liberação de execução. A qualificação R5 cobre fonte/build_priors/validação/contrato temporal, não a ativação futura. Helpers de cadeia mudaram depois do import do filho; fonte e runner ficaram idênticos e os utilitários importados preservaram o AST, registrados no recibo de fechamento.

CPU medida dos recibos de fonte/controles=168.686s; parede=178.162s; CPU de testes locais de cadeia não medida. Intervalo desde cópiaT03=0.3569h. Máquina pesada0h. Chamadas externas novas0; soma parcial deduplicada do ledgerUS$3.0821417664, sem converter assinaturas/falhas de uso desconhecido em zero.

Próximo: ligar cadeia/ativação/alocações/relógioR7, novos nulos e descegamento por leitura, concluir desenho e probes, só então emitir testemunha. A geração4096 já está selecionada pela regraR4, sem mudar a prior. Ainda falta garantir relatório EDOM também em saída excepcional da PE e integrar geração explícita às injeções no ramo autorizado correspondente.
