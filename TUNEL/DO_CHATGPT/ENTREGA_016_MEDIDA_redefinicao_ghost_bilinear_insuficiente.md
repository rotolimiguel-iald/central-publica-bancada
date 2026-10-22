[REAL — triângulo principal sem peso global; MEDIDA — redefinição bilinear não basta]
# A7.b — c* c c: próximo vértice marcado calculado

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-24T22:51:36.330146+00:00.

A fonte é c*_ρ c^μ∂_μc^ρ. Seu vértice de duas pernas ghost, retirando i,
é T_ab=(l_a Y_b-k_b Y_a), onde Y é a polarização de c* e k,l são os dois
momentos ghost. O diagrama1PI usa essa fonte e dois vértices barc C(L_c h).
Uma linha métrica une esses dois vértices; duas linhas ghost os ligam à fonte.
Para externos c(p)=v,c(r)=w,c*(-p-r)=Y, fixamos k=q+p,l=r-q. O numerador é

    Σ S0_ij [ (l·V(E_i,q,p)v)(Y·V(E_j,-q,r)w)
             -(Y·V(E_i,q,p)v)(k·V(E_j,-q,r)w) ],

com denominadores q²(q+p)²(q-r)². Fatores globais4κ,i e pesos Grassmann/ação
estão separados: o resultado é um kernel numérico sem peso global completo.

Controles: troca das duas pernas ghost inverte o sinal depois de q→-q,
diretamente no numerador e após a extração. Uma integração independente por
Feynman usa x,y>=0,x+y<=1, shift=xp-yr e Δ=x p²+y r²-(xp-yr)². Para termo
l^(2a) em três denominadores, a≥1, seu log UV tem fator
2(-1)^(a-1) binomial(a+1,2) Δ^(a-1), incluindo o peso simplex2; momentos
angulares Dirichlet reproduzem seis casos de eixo e um caso não axial.

## Medida que limita a simplificação

Com p=e0,r=e1,Y=e0,v=e0,w=e1, o coeficiente sobreA0 é7/24. A extensão por
coordenadas δ_F B derivada da bolha h*c dá ZERO no mesmo caso. Logo nem um
fator global resolve a diferença. No teste não axial o triângulo deu1165/24
e a candidata de coordenadas -27/4. As sete componentes estão em results.json.

Não é uma anomalia demonstrada. A bolha h*c sozinha não determina as correções
quânticas de todos os vértices da álgebra de gauge. A Ward superior envolve
também fontes dependentes de h; impô-la a c*cc isoladamente é truncá-la.
Próximo elo do A7.b: h*hc e suas relações com estes termos, mantendo curvatura,
cutoff e contatos finitos visíveis. O triângulo não foi apagado nem ajustado
para concordar com a candidata bilinear.

Comando A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/ghost_antifield_triangle_check.py; rc0,20checks,1controle não nulo;
wall 4.595295699953567s,CPU 4.59375s. Plano anterior, código,
resultados e log no manifesto. Não há QME/gate novo nem prova da teoria física.
