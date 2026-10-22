# Preparação do builder NC02-RAT-01

[REAL — fontes lidas, arquivos escritos e AST analisada; INPUT — código candidato ainda não executado] Foram preparados apenas builder.py e codec_adapter.py. Nenhum desses arquivos, codec antigo ou Fraction foi importado/executado nesta preparação. Não há verificador, worker, supervisor, request de execução, CLAIM ou autorização produzidos por esta entrega. Registro prévio no mapa532.

## Interface acordada

build_case(payload, case, rational_parser) devolve somente primitivas JSON com campos estáveis:
case_id, status, reason, annihilation_residual, dual_affine_constant, dual_affine_slope, lower, upper e witness.
Um racional é {numerator: string, denominator: string}; campo não emitido permanece null. witness, quando presente, contém u, eta e residual (duas coordenadas encoded).

O worker exterior, construído independentemente por ROOT, deve vincular payload_sha256, hashes das dependências/fontes, identidade de execução e resultados do verificador. O builder não faz I/O ou verificação de bytes. A função rational_parser é dependência injetada; deve ser a _rational da fonte tail V2 pinada no manifesto, com retorno (int,int). O adaptador não importa tail_envelope nem chama cauda, agregador ou controle antigo. O futuro worker precisa carregar/pinar essa dependência somente dentro da autorização própria.

Os valores de expected_analytic_not_run não são acessados. A chave é apenas permitida como anotação opcional no schema dos casos. O worker pode removê-la, assim como required_checks, metadados, pins e provas esperadas, antes de passar a projeção de entrada. Os campos matemáticos/identificadores exigidos permanecem os do payload. A projeção e sua relação com os bytes de origem devem ser vinculadas pelo envelope exterior.

## Recorte e cálculo

C=I2, X=(1,1), domínio fechado u em[0,1/2], b(u)=(1,u), nuisance real e os dois IDs/ordem, duais e testemunha são conferidos como a fixture fixa admitida. Alterações de geometria, dimensão, caixa, coeficientes, caso, dual ou testemunha são INVALID_INPUT; não é gerador de fixtures gerais.

As constantes de entrada que fixam esse recorte não são constantes de saída. A partir dos racionais decodificados, o construtor calcula:
- Xᵀv por produto interno;
- constante dual 2vᵀb0−vᵀCv e coeficiente 2vᵀb1;
- valores da expressão afim nos dois extremos, mínimo deles e máximo com zero;
- viabilidade da testemunha na caixa, b(u)−Xη e sua norma ao quadrado (C é exatamente I2);
- coerência lower≤upper e igualdade exata, quando houver.

Não lê a fórmula esperada nem o mínimo analítico no payload. O caso não anulante retorna INVALID_DUAL_ANNIHILATION imediatamente após Xᵀv≠0, com o residual de anulamento encoded e todos os coeficientes/bounds/witness null. Não avalia a expressão dual nem a testemunha para esse caso. Sem tolerância, otimização, float, exp/log ou solver.

Status de construção possíveis: CERTIFIED_TOY_MINIMUM, CERTIFIED_TOY_MINIMUM_INTERVAL, INVALID_DUAL_ANNIHILATION, INVALID_INPUT e RESOURCE_LIMIT. A palavra CERTIFIED nos rótulos é do contrato sintético proposto; um rótulo emitido pelo builder não substitui o verificador independente. Nenhum desses resultados foi emitido por execução agora.

## Codec e orçamento exato

codec_adapter.py usa Fraction somente a partir de inteiros retornados pelo parser injetado. Aplica primeiro tamanho/shape da entrada; o parser original faz o parsing canônico de512bits. O adaptador confere retorno tuple de dois int exatos (bool recusado),512bits, denominador positivo, ausência de redução pendente e correspondência às strings canônicas originais. É pós-condição da dependência, não cópia do parser.

As operações necessárias são soma, subtração, negação, produto e comparação. Não é preciso uma API de divisão racional para esta fixture. Numeradores e denominadores intermediários têm limite4096bits. Produtos são pré-recursados pelo limite conservador bitlen(a)+bitlen(b) antes da multiplicação; somas não triviais por max(bitlen(a),bitlen(b))+1 antes da adição. Toda formação de Fraction recebe inteiros já limitados; normalização por gcd/divisão não aumenta seus módulos. Comparações por produtos cruzados passam pelas mesmas guardas. Negação/abs não aumentam bit_length. A codificação decimal fica abaixo do limite padrão de conversão de inteiros do runtime neste orçamento.

As guardas conservadoras podem recusar uma operação cujo resultado reduzido caberia, sobretudo por cancelamento. Isso gera RESOURCE_LIMIT com bounds null; não arredonda nem converte para float. A garantia é sobre os intermediários explícitos da aritmética exata, não um teto duro de RAM/tempo do SO. Python/Fraction e a função codec são fronteiras de confiança pinadas, não código formalmente provado. A identidade real da função injetada não pode ser certificada por ser callable: deve ser ligada pelo worker.

## Alternativas e limites

A seleção documentada comparou: (A) inteiros/Fraction exatos, adotados apenas para NC02; (B) mpmath.iv, disponível por metadados mas não qualificado para todo domínio/função; (C) Decimal com envoltórias específicas ainda ausentes. A evita dependência transcendental desnecessária nesta unidade mínima. Outra opção operacional seria copiar um codec local; foi rejeitada para preservar a dependência read-only já pinada e evitar divergência de gramática.

As duas recusas reais têm caminhos distintos: escopo/codec inválido retorna INVALID_INPUT; excesso prévio de bits retorna RESOURCE_LIMIT. O negativo autorizado é uma terceira condição matemática explícita, INVALID_DUAL_ANNIHILATION. Não existe fallback aproximado, retry, novo ID ou reparo de dados.

O arquivo de validação estática registra somente AST, imports declarados, ausência de chamadas diretas proibidas/float e ausência de leitura dos resultados esperados. Isso não é teste dos dois casos, benchmark ou confirmação do runtime. Os limites operacionais, carregamento de dependências, verificador e supervisão ficarão na unidade separada de ROOT, após revisão independente. Nenhum backend cosmológico/global, integral F9, significância, original ou memória compartilhada foi alterado.
