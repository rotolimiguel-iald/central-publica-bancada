[REAL — cálculo exato e compilação; DERIVED no modelo de cargas especificado]
# A5.d — Primeira ordem unilateral versus bilateral
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

Reutilizados literalmente três lemas da v3.1: Δit_vac, inner_vac_Δit e
bilateral_no_first_order. Eles demonstram, sob H2 e derivada de φ, energia
bilateral ε² kφ para Ω+εφ. O novo lema de normalização mantém derivada
zero em ε=0 para kφ ε²/(1+r ε²). Não foi substituído o contrato físico.

**Testemunho exato de dois corpos:** pacote f(k)=2√k exp(−k), k>0,
normalizado; Φ(k₁,k₂)=f(k₁)f(k₂) é simétrico e normalizado. Na compressão
aos setores |0>, |1_f>, |2_f>, N|2_f>=2|2_f>. O campo quadrático
normal ordenado foi definido explicitamente por
Q(u)=g(u)²a²+conj(g(u))²(a†)²+2|g(u)|²N,
g(u)=1/[√π(1+iu)²]. Essa convenção de carga é INPUT do harness.

As integrais convergentes dão ∫₀∞u g(u)²du=−1/(6π) e
∫₀∞u|g(u)|²du=1/(2π). Para H₊=2π∫₀∞uQ(u)du,
H₋=−2π∫₋∞⁰uQ(u)du, ψε=(|0>+ε|2_f>)/√(1+ε²),

    <H₊>ψε = (−2√2 ε/3 + 4ε²)/(1+ε²)
    d<H₊>/dε|₀ = −2√2/3 ≠ 0
    d<H₊−H₋>/dε|₀ = 0.

A segunda igualdade é geral no lema bilateral reutilizado; neste pacote
simétrico a compressão H₊−H₋ inteira zera. Isso NÃO diz que o boost
completo da teoria seja zero. O estado perturbado não é coerente para ε≠0:
o menor que testa proporcionalidade entre aψε e ψε é √2ε/(1+ε²).

**Controles:** fase relativa i ou retirada do termo de pares anulam a
derivada unilateral; trocar ε por −ε inverte seu sinal; normalizar não
muda o termo linear. Matriz hermitiana, vácuo subtraído e primeiro momento
absoluto das caudas conferidos. O abaixador é truncado e não foi anunciado
como representação completa de CCR. Não construímos Fock da rede, T₀ local
da TGL, covariância espacial completa nem derivada de entropia física.

**Estado A5.d:** PAGO como harness exato do mecanismo e reuso do teorema
bilateral; aplicação ao T₀ do mesmo par continua condicionada ao elo A5.c.
São 9 entradas Lean auditadas (3 reutilizadas, 6 locais), finais rc0/trio,
e 33 controles exatos no harness final. Tentativas anteriores preservadas;
as duas falhas do módulo novo decorreram de API de soma não importada e
conversão de instâncias, corrigidas sem hipóteses adicionais.
Máquina 64.608609s parede/64.812500s CPU; bancada não exclusiva.
Custos remotos explícitos acumulados US$0.2662637382, incompletos; sem nova chamada.
Não move gate. Segue A5.e.

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A5\first_order_manifest.json`
SHA256: `2557d27c94bb49622c7f4f612907860954b272eeed77464dd9af7ac73a93d822`.
