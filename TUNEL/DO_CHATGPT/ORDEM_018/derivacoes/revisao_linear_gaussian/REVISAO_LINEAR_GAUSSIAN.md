# Revisão independente de linear_gaussian.py

Identidade: chatgpt-codex/ordem-018/derivacoes. Mapa prévio: 451, rota hubble.fase9_razao_discriminante. Escopo: implementação da integral nuisance plana sobre suporte comum; nenhuma adoção de hipótese física ou abertura da F9.

[REAL — leitura e integridade] Não encontrei defeito material no módulo examinado. A revisão estática é suficiente para conferir a implementação desta álgebra e os limites declarados, em conjunto com os controles já registrados. Não houve motivo concreto para repetir os 16 controles sintéticos; eles não foram reexecutados.

Foram conferidos os três pins do protocolo, o pin do protocolo no resultado, os 16 nomes de controles contra o código, todos os estados e erros/tolerâncias arquivados, o tempo interno registrado e a leitura AST dos três scripts. As 12 verificações de integridade passaram. Isso verifica a coerência do recibo existente, não declara uma segunda execução independente. O guard singular_gaussian_v2 permaneceu inalterado.

## Correspondência matemática

[DERIVED] Para C efetiva de posto r, escreva W=Λ₊^(-1/2)U₊ᵀ. A implementação armazena esse whitener. Se WX=Q diag(s) Vᵀ tem p colunas independentes, QᵀQ=I_p e

F=XᵀC⁺X=V diag(s²)Vᵀ, portanto log det(F)=2Σ log(s).

O código usa precisamente essa identidade, sem formar ou inverter as equações normais. O resíduo projetado é t=(I−QQᵀ)Wb, de modo que ||t||²=bᵀPb, onde P=C⁺−C⁺X F⁻¹XᵀC⁺. A normalização implementada é

log ∫ L(b|η,C)dη = −½[(r−p)log(2π)+log pdet(C)+log det(F)+||t||²].

Logo o fator nuisance e a normalização do suporte estão preservados. Não se trata apenas de likelihood perfilada: o determinante da integral está presente.

Para matriz de respostas A, residualize devolve T=(I−QQᵀ)WA e response_information devolve TᵀT=AᵀPA. A saída é informação positiva semidefinida calculada exclusivamente com erros/projeto/respostas; não consome resíduos observados. Uma resposta no espaço nuisance tem informação nula em aritmética exata. O pequeno resíduo numérico documentado no controle correspondente não constitui identificação dessa direção.

## API e limites pertinentes à F9

[REAL — inspeção de código] O construtor exige projeto finito, bidimensional e com o número correto de linhas. Recusa mais colunas nuisance que direções suportadas, colunas fora do suporte e perda de posto/condicionamento pela tolerância de SVD congelada. O corte de desenho precisa ser escalar finito em [0,1). A normalização não finita é recusada.

residualize exige respostas finitas, bidimensionais e no mesmo suporte. response_information também recusa saída não finita. log_integral delega a validação de forma e finitude ao guard existente; resíduo incompatível com o núcleo retorna −infinito, e resultado não finito dentro do suporte é recusado. Assim o caminho não aceita silenciosamente o χ² da pseudoinversa para um resíduo determinístico incompatível.

Permanecem limites explícitos, e não defeitos novos:

- Os postos e o suporte são os da covariância efetiva após os cortes. Unidades, tolerâncias e medida nuisance comuns precisam ser congelados pelo chamador. O módulo não declara invariância sob mudanças de unidades sem transportar o contrato.
- A classe verifica suporte para um objeto. A igualdade do suporte afim e da medida entre modelos pertence à montagem externa já exigida. Construtores separados não certificam essa igualdade por si mesmos.
- A integral implementada usa a mesma medida plana em todo R^p. Não substitui a integral de um prior próprio ou de uma caixa finita: normalização e truncamento dessas alternativas continuam fora desta API.
- response_information devolve uma matriz PSD; não promete sua invertibilidade nem produz veredito de identificabilidade estatística, poder, ajuste ou evidência. Nenhuma inversão automática foi acrescentada.
- Se C, X ou a transformação de medida dependerem de parâmetros, a normalização correspondente deve ser recalculada e mantida dentro da integral externa. O módulo entrega o fator calculável; não decide que ele pode cancelar.

Essas condições já constam do escopo e do projeto documental revisado. Não identifiquei necessidade de acrescentar um requisito científico ou repetir PSD/seleção para aceitar este componente.

## Recibo e conclusão

[REAL — evidência anterior conferida] O resultado registra 16/16 controles aprovados: contraste analítico e quadratura escalar, incorporação singular, recusas de suporte/posto/finitude, jacobianos de coordenadas e unidades, informação projetada e comparação densa de Schur/normalização. O maior erro das comparações registradas é 1,7763568394002505e−15 para tolerância 1e−10. A estimativa de erro da quadratura é 4,137001223127387e−12; não é erro observado do módulo. O tempo interno registrado é 0,01574639999307692 s.

Aceite técnico do componente no escopo matemático declarado. A revisão não importa o módulo nem NumPy/SciPy, não lê catálogos ou centros, não monta C real, não calcula S/g/H0/ln B e não repete E45/P3/PSD. Não altera arquivos do autor. A aplicação científica permanece sujeita à escolha documental de medida e ao contrato físico comum; este parecer não autoriza composto nem transforma controles sintéticos em evidência observada.

Fontes e hashes: REVISAO_LINEAR_GAUSSIAN_RECIBO.json. Custódia desta revisão: MANIFESTO_REVISAO_LINEAR_GAUSSIAN.json.
