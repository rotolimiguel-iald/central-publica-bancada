[DERIVED — identidade fora da diagonal até primeira ordem em K; Q2 completa OPEN]

# Soma bilocal na mesma orientação

O cálculo usa o espaço-forma euclidiano 4D, a referência singular e as
normalizações já fixadas nos motores anteriores. Não escolhe coeficientes
para impor Ward. A prescrição distribucional anterior continua reservada
para a extensão; esta demonstração é em X diferente de Y, até O(K).

## 1. Domínio de jatos externos

Depois da integração das derivadas do ghost externo em Y, cada laço tem

    integral dvolX dvolY [h_ab(X) C0^{ab}_r(X,Y)
                         + D_i h_ab(X) C1^{iab}_r(X,Y)] c^r(Y).

Portanto seu coeficiente forte é B=C0-divX C1. Pôr Dh=0 antes dessa
integração calcula outro objeto. A divisão por dois dos testes fora da
diagonal a!=b vem de testar com o tensor simétrico e_ab+e_ba.

Em Y=0, todos os índices são de frame ortonormal. A covariância O(4) e a
ausência de epsilon nos vértices reduzem C0 a três estruturas e C1 a sete:

    C0: delta_ab Xr; delta_ar Xb+delta_br Xa; Xa Xb Xr.

    C1: delta_ir delta_ab; delta_ia delta_br+delta_ib delta_ar;
        delta_ab Xi Xr; delta_ir Xa Xb;
        delta_ia Xb Xr+delta_ib Xa Xr;
        delta_ar Xi Xb+delta_br Xi Xa; Xi Xa Xb Xr.

Para C1, as potências de z=X² são, respectivamente, 4,4,5,5,5,5,6
na ordem K0 e uma a menos na ordem K1. Para C0 são 5,5,6 e uma a menos.
As três leituras 110,011,000 separam a base de posto três na direção e0.
As sete leituras registradas no script separam a base de posto quatro.
Todos os coeficientes logarítmicos foram mantidos até a extração; os
coeficientes finais medidos neste recorte não dependem de L.

## 2. A derivada no extremo X

A divergência inclui a conversão do frame para coordenadas, a conexão
dos três índices em X e a reconversão dos dois índices restantes:

    e_i^mu = delta_i^mu + K(z delta_i^mu-Xi Xmu)/6,
    omega^a_{c,i} = K(Xa delta_ic-delta_ia Xc)/2.

O índice r está em Y; não recebe conexão em X. A sua transformação sob
rotação simultânea entra, contudo, na reconstrução O(4). O script de
auditoria independente usa divergência em coordenadas com Christoffel;
confere todas as sete estruturas, incluindo coeficientes lineares em L
(84 igualdades). Omitir a correção do frame produz resíduo -1 num controle.

## 3. Fonte e soma sem ajuste

A fonte C é calculada primeiro como A-divY B, antes de Y=0. Sua
decomposição em gauge mais resto curvo está demonstrada em
../source_einstein_radial_aux/DERIVACAO.md, com 128 verificações locais.
A aplicação do operador Einstein E dá

    (EC)0 = 0,
    (EC)1_ab,r = -144 delta_ab Xr/z4
                -48(delta_ar Xb+delta_br Xa)/z4
                +384 Xa Xb Xr/z5.

Separadamente, a combinação fixa dos laços, -metrico/2+ghost, dá

    B0 = 0,
    B1_ab,r = +144 delta_ab Xr/z4
               +48(delta_ar Xb+delta_br Xa)/z4
               -384 Xa Xb Xr/z5.

Logo, na referência, truncamento e normalização usados,

    -B_metrico/2 + B_ghost + EC = O(K²),  X != Y.

O script de junção lê os resultados dos motores separados e calcula a
divergência covariante em X simbolicamente, sem ajustar nenhum número.
Verifica todos os 4x4x4 componentes em K0 e K1: 128 identidades racionais
modulo z=X². As correções de conversão dos índices da fonte não mudam
esta comparação em K1 porque (EC)0 já é zero.

Os três controles detectam: omissão da integração DhX; retirada de EC;
inversão do sinal de EC. Os resíduos não nulos estão no results.json.

## 4. O que isso localiza

O resíduo anterior, calculado com DhX=0, não era uma quebra de Ward forte.
A soma agora paga o setor não coincidente até primeira curvatura. Uma
eventual quebra desse setor após extensão deve estar na diagonal; a
anulação fora dela NÃO estabelece o coeficiente dos contatos.

Não estão demonstrados aqui: extensão temporal lorentziana, contatos da
prescrição R, parte suave W geral, todos os tadpoles, ordem K², aridades
restantes, condição Wess–Zumino completa ou classe nula da Q2 completa.
As reconstruções usam a covariância e homogeneidade dos kernels da
bancada; a revisão independente dos jatos bilocais permanece solicitada.
Nenhuma alteração de vértice original, kernel Lean ou gate.
