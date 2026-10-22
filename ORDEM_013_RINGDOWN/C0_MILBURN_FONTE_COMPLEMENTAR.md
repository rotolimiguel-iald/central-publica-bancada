[KNOWN — fonte primária consultada; DERIVED — separação espectral]

# Milburn: gerador exato e limite quadrático

No [texto posterior do próprio Milburn](https://arxiv.org/html/gr-qc/0308021),
as equações 23, 35 e 36 distinguem saltos unitários de Poisson e expansão
quadrática. O corpo HTML foi lido; arquivo e hash estão em
`cache/literature_milburn_followup/PROVENANCE.json`. Isso não equivale à leitura
integral do artigo de 1991, que continua inacessível nesta rodada.

Escrevendo `omega=(E_i-E_j)/hbar`, a equação espectral consultada tem autovalor

    lambda = (exp(-i nu omega)-1)/nu.

[DERIVED] Separar partes real e imaginária fornece

    Gamma_exact = 2 sin²(nu omega/2)/nu >= 0,
    omega_effective = sin(nu omega)/nu.

Para `|nu omega| << 1`, a taxa é `nu omega²/2 + O(nu³ omega⁴)`.
O sinal dissipativo acima segue do gerador; evita importar o sinal inconsistente
exibido na equação 61 do HTML sem conferência do PDF.

[ESCOPO] A dinâmica quadrática implementada na bancada é exata **para seu
gerador declarado**. Identificá-la com a dinâmica integral de saltos seria
outra hipótese. A fonte não determina `nu=beta*tau_star` para a TGL.
Nenhum relógio, template, resultado de strain ou gate foi alterado. Kay–Wald
e Milburn 1991 mantêm o escopo de acesso registrado no adendo anterior.
