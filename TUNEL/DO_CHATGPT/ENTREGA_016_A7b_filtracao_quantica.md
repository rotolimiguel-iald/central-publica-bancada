[DERIVED — filtração perturbativa; REAL — CAS exato; OPEN — quebra quântica]
# A7.b — contrair antes de truncar a valência externa

Abertura da ORDEM016: sha256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

## O cálculo que muda a preparação

A087 define C_N pela valência clássica e prova que s não a reduz (linhas11–13).
Essa afirmação não diz que a mesma projeção comuta com contrações quânticas.
Num par bosônico com contração formal ħ C, para monômios não normalizados,

    q^(N+1) ⋆ q = q^(N+2) + (N+1) ħ C q^N.

O primeiro fator é zero em C_N, mas o segundo termo do produto não é. A idealidade
clássica não se transfere ao produto deformado. A identidade é algébrica para todo
N>=0; o CAS verifica N=2,...,8. C denota um pareamento de contração, não um número
de amplitude física. Não é necessário tomar um valor singular de propagador em x=x.

Para duas inserções distintas a conta de Wick dá

    [(ħ C)^2/2!] (d_x^2 x^7)(d_y^2 y^3) = 126 ħ² C² x^5 y.

São seis pernas externas, duas linhas internas e dois vértices: L=I−V+1=1.
O poder ħ² do produto temporal NÃO é o número de laços; os fatores de vértice e a
normalização da ação efetiva precisam ser incluídos. Nenhuma distribuição foi
estendida, nenhum índice métrico/ghost foi contraído e nenhum coeficiente Ward foi obtido.

## Corte compatível

Uma contração de ordem r leva ħ^p A_m e ħ^q A_n a
ħ^(p+q+r) A_(m+n−2r). O peso E+2p é aditivo: a perda de dois campos é compensada
pelo peso dois de ħ. Portanto a filtração conjunta, com potências não negativas de
ħ, é compatível com esse produto formal. A expansão de S contém ħ inversos;
para a ação efetiva conectada usa-se separadamente a identidade da fonte069:

    Σ_v (v−2) = E+2L−2.

Com vértices de interação v>=3 e L=1, V<=E e cada v<=E+3−V.
Para E<=6, isso requer considerar vértices até8; em grafos com V>=2, até7.
O exemplo (7,3) mostra por que C6 aplicado ANTES dos produtos não basta.
Se uma ordenação elimina tadpoles de um único vértice, isso não elimina por si a
família (7,3). A identidade vale para a contagem topológica; contatos, antifields
externos, graduação e inserções marcadas exigem a análise própria da Ward.

O CAS enumera29 PARTIÇÕES DE VALÊNCIAS para E=1,...,6 e L=1, das quais11 têm E=6.
Três famílias contêm vértice>6. Não são29 grafos nem29 amplitudes não nulas.
O termo cosmológico admite coeficientes de grau7/8: na direção local de posto1,
sqrt(det(1+q e_00))=sqrt(1+q), com coeficientes33/2048 e−429/32768.
Isso verifica disponibilidade de vértices, sem excluir cancelamentos da ação completa.

## Consequência e verificação

Registrar a projeção EXTERNA após as contrações e a graduação por ħ/pernas antes
de fixar a prescrição temporal. O C6 clássico continua válido em seu domínio.
Esta é uma obrigação de implementação, não obstrução à existência da teoria.
A prescrição completa e o coeficiente a_1 em H^(1,4)(s|d_H) continuam pendentes.
Não se escolhe a_1=0 por definição nem se transporta H4 clássico para esse grupo.

Comando executado: `A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/quantum_filtration_check.py`.
rc0 observado pela ferramenta exec_command; 27 checks e
11 negativos; 0.051683600002434105s de cálculo,
0.046875s CPU. A saída estruturada foi gravada diretamente pelo script;
não foi capturado um arquivo stdout independente. Reprodução não sobrescreve o plano.
Plano, fonte e resultado têm hashes no manifesto associado. Sem Lean novo/original/gate.

Fontes locais: A087 linhas11–13,69–71; Q2_069 §§4–6; contrato072 §5 (hashes no plano).
Leitura primária delimitada: BFR, §3.4, equações52–54, distingue o produto fora da
diagonal e as extensões com liberdade local. Não fornece o coeficiente deste cálculo.
https://arxiv.org/html/1306.1058v4
