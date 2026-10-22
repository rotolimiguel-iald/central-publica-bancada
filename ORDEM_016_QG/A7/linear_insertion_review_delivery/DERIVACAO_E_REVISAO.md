[DERIVED — inserções lineares identificadas e identidade auxiliar fechada; Q2 completa OPEN]

# Duas inserções de A1 entram na identidade de aridade2

Mantemos Tc2=(i/hbar)(T2-S2), com S2 simetrizado graduadamente. A condição
de concordância perturbativa para uma entrada linear, escrita nas equações
158a/b de Fröb1803.10235v3, fornece os produtos com Green avançado/retardado.
Usá-la é uma condição explícita de normalização, não consequência automática
do finite part radial aplicado aos grafos com duas linhas internas.
Fonte primária consultada: https://arxiv.org/pdf/1803.10235v3, p37.

Mediando as duas ordens e usando GD=(Gret+Gadv)/2, derivamos

 Tc2(V,phiK(x))=-int GD_LK(y,x) T1(dR V/dphiL(y))dy.

No único canal que contrai com c, Vghost=chi barc C Lie_c h. A derivada
DIREITA em barc vale -chi C Lie_c h, e G_barc,c=-GQ. Assim

 Tc2(Vchi,c_i(x))=-int GQ_D,ji(y,x) chi(y)(C Lie_c h)^j(y)dy.

As parcelas métrica e antifield de V1 não têm barc e não contribuem a essa
contração linear. O produto restante h*c não tem contração interna permitida.
Escrevendo A1(Vchi)=i hbar alpha int chi div(c), com alpha contendo a
normalização física ainda explícita, o par de termos subtraídos em A2 é

 -i hbar alpha [int dchi(x) GQ_D(y,x) eta(y) C Lie_c h(y)
              +int deta(x) GQ_D(y,x) chi(y) C Lie_c h(y)].

Para chi=eta há fator2. Omitir uma das duas entradas perde esse fator.
Essas parcelas tomadas sozinhas contêm Green e são não locais. Devem ser
combinadas com os outros termos da Ward para obter a quebra local; não
podem ser renomeadas como contato já calculado. Um controle de coeficientes
constantes deixa resto -4m²lambda ao dividir4lambda³ por lambda²+m².
Esse controle detecta a não localidade do inverso, sem pretender calcular
o propagador curvo. São11controles, CPU0.015625s,rc0.

# A identidade linear fecha com o termo de Euler presente

Ponha w=c.nabla c. A nilpotência clássica polarizada dá
C Lie_c Kg c=Qw. A derivada direita do vértice s0Vchi em barc tem DUAS
parcelas: chi Qw, vinda do vértice ghost, e -Q(chi w), vinda do termo
qcdag=-Qbarc-Kg*hdag. Portanto

 dR(s0 Vchi)/dbarc=chi Qw-Q(chi w)=-[Q,chi]w,
 [Q,chi]w=2nabla chi.nabla w+(box chi)w.

A identidade com uma entrada c torna-se exatamente

 s0 Tc2(Vchi,c)-Tc2(s0Vchi,c)-(Vchi,c)
 =GD chi Qw-GD(chi Q-Qchi)w-chi w=0.

Usa-se GD Q=I no domínio dos testes declarado. Tc2(A1(Vchi),c)=0 por
ausência de contração c*c. Se omitirmos -Q(chi w), a mesma expressão dá
-chi w, não zero. São10controles exatos, CPU0.171875s,
com matrizes finitas que testam a ordem dos operadores e a regra de produto
diferencial nas assinaturas euclidiana/lorentziana. Os controles não constroem
um Green global. O resultado é A2(Vchi,c)=0 sob o contrato; não é
A2(Vchi,Veta)=0.

# Auditoria da revisão DeepSeek6945

Resposta original e recibo preservados. O revisor reconstruiu a aritmética
99/4+179/20=337/10 e C*S a partir do primeiro jato fornecido. Essa parte
confere com o CAS da bancada. Não forneceu reconstrução independente de
toda a identidade de transporte do calor: sua aprovação é condicional.
Corrigimos sua nomenclatura: jato misto do calor e jato logarítmico de Green
são OBJETOS diferentes, não convenções intercambiáveis. Estado global e
entrelaçamento formal local também são obrigações diferentes.

Próximo passo: verificar a normalização da entrada linear na MESMA família
T2 e reunir as duas parcelas acima ao subtotal de duas inserções já medido,
conservando a parte de curvatura e os termos de cutoff. O coeficiente337/10
é auxiliar euclidiano; realidade/continuação não foram inferidas do voto do
revisor. MiMo57e está executando a revisão de coordenadas BV; Kimi mantém
três pedidos aguardando recuperação efetiva da quota. Nenhuma nova chamada
nesta entrega. Originais e gate intactos. AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
