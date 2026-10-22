[REAL — lema funcional compilado; A3.4 em curso]

# ORDEM 016 — ausência de autovetores com fibra transversal

UTC 2026-09-24T15:32:06.251346+00:00. ABERTURA sha256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

Para qualquer espaço normado complexo E, seja D(s) em L²(R;E) a composição
f(ξ)↦f(ξ−s). Foi verificado:

`(∀s, ∃c∈C, ‖c‖=1 ∧ D(s)f=c•f) → f=0`.

O argumento reutiliza RetaDeLuzEspectro.D_no_eigen: a energia ‖f‖² fica
periódica sob translações inteiras; cada intervalo [n,n+1) tem a mesma
integral. Como a integral total é finita, todas são zero. A adaptação troca
valores escalares por E e enorm_mul por enorm_smul. O deslocamento é um
operador linear isométrico real, construído pela preservação de Lebesgue.

**Evidência:** primeira compilação rc0, duas declarações auditadas no trio,
sem sorry/axiom novo. 15.138003s parede;
14.906250s CPU.
Fonte, log, recibo, origem e hashes em A3/vector_rapidity_manifest.json e
A3/vector_rapidity_provenance.json. Nenhum original/kernel alterado.

**Ainda não pago:** identificar unitariamente a medida d³p/p⁰ de cada órbita
com a descrição por rapidez e fibra transversal; conferir o conjunto excluído
de medida zero no cone e o transporte das helicidades. Não há, aqui, um
teorema sobre a representação física inteira por simples renomeação de D.
O mesmo argumento funcional pode ser reutilizado nos três ramos quando
essas ligações forem fornecidas. O gate não muda.

Próximo trabalho local A3.4: parametrização
p=(m⊥ cosh ξ,m⊥ sinh ξ,q₂,q₃), m⊥²=m²+q₂²+q₃²;
conferir domínio, jacobiano e medida, e então transportar o lema acima.
Para m=0, q⊥=0 requer tratamento a.e.; não assumir chart global bijetivo.
Para helicidade, não substituir o cociclo por 1 sem prova de equivalência.
