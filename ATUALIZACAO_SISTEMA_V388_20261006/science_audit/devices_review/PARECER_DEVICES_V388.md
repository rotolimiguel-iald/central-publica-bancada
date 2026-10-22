# Revisão independente — dispositivos v388

[REAL — leitura, AST, bytes e ZIP em memória] Aceite estático delimitado do snapshot v388 selado. Nenhum bloqueador concreto remanescente foi encontrado no recorte examinado. Não instalei, importei candidatos, executei runners, funções científicas ou refiz controles.

A comparação AST do módulo inteiro, removendo apenas as seis funções novas, a constante de pin e a chave adendo_v388, coincide com a base. Todas as funções antigas preservam seu AST, inclusive beta() = ALPHA_FINE_CODATA_2018*sqrt(e), fatores D1a/D1b e formula_runtime. A camada mantém versão-base v386 e identifica o adendo v388 separadamente; não rebatiza os resultados antigos.

[DERIVED — inspeção algébrica] A implementação 2t/(1+t²), t=exp(−χ/2), corresponde a sech(χ/2). A API requer χ finito, não negativo, e 0≤χ≤χsup para a leitura de piso. Ela recusa bool, não finitos e apagamento da positividade por underflow. O piso é β(χsup), explicitamente não identificado com β0; χ=0 dá sqrt(e), não Thomson. μ e χ(μ) continuam OPEN e beta_of_mu_v388 lança NotImplementedError. O domínio de couplingOfAlpha é apenas diagnóstico binary64. Nenhuma dessas observações certifica precisão uniforme, escala física ou dispositivo empírico.

Os pins obrigatórios ligam programa, selo, resultado, proof manifest e pedra nova ao mesmo snapshot. A leitura do adendo falha quando o cofre selecionado não é exatamente v388 ou quando metadado/pins divergem. A futura presença de outro cofre requer vínculo próprio: não é migração automática.

[REAL] Conferi os16 ZIPs embutidos por AST/base64, sem extrair arquivos nem executar código. Nomes seguros/únicos, conjunto exato de membros, hashes e tamanhos, bytes do stage e identidades combinadas conferem. Em todos, a única alteração é tgl_formula_completa.py; a única adição é ADENDO_V388_METADATA.json; nenhum membro foi removido. Os16 runners são byte a byte os anteriores. A compatibilidade aqui é estrutural; os bundles continuam dependendo do cofre externo da Central e não são certificados de runtime fora dela.

Achei o campo final_bytes calculado sobre LF antes da gravação CRLF nos16 manifestos, comportamento também presente nos16 anteriores. O autor corrigiu somente os manifestos, acrescentou final_sha256 e preservou ZIPs/FINALs. A revisão do delta confirmou os16 tamanhos e hashes finais e a estabilidade de todos os FINALs. Não há pendência desse achado.

[REAL] Os1823 membros do manifesto final conferem por bytes. O plano único é exatamente a união dos planos examinados:1233 arquivos de custódia,2 da camada e32 dos FINALs. Todos os1267 pins de instalação conferem. Destinos são únicos e contidos nas raízes previstas. Para novas custódias o plano exige ausência/reconciliação; para existentes exige backup de bytes, temporário verificado, substituição atômica e leitura final. A inspeção anterior confirmou os hashes das34 destinações já existentes e ausência dos dois diretóriosv388. Essas pré-condições precisam ser reconferidas no momento da instalação, que não foi feita nesta revisão.

A origem viva um.py mudou após a cópia; o recibo do autor e a confirmação ROOT distinguem isso do snapshot. Aceito somente v388 cujo programa e64b… coincide com o selo preservado. Não avaliei nem aceitei a nova fonte viva como parte deste pacote. Os37 testes isolados AST/fixtures foram lidos como recibo do autor, sem repetição; isso não é demonstração dos16 dispositivos.

Alternativas: (A) transportar o snapshot/adendo tipado preservando β0 e resultados, como preparado; (B) trocar β0 por uma leitura de escala, que não foi adotada e depende de identificação física própria. Não é necessário resolver μ para a atualização documental A. Não há avanço empírico ou confirmação física inferido; gate e contratos científicos permanecem fora desta alteração.

EVIDENCIA_REVISAO.json preserva a inspeção anterior à correção; REVISAO_DELTA_FINAL.json ancora a versão final e seus1823 pins. PLANO.md e planos intermediários mudaram de modo declarado e com backups, sem corrupção dos bytes científicos. O mapa MCP não foi chamado novamente, preservando sua recusa anterior de egress.
