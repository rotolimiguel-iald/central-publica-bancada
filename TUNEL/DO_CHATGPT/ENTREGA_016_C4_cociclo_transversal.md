[REAL — 26 teoremas no trio; DERIVED — diagnóstico; OPEN — representação induzida completa]

AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.

C4 entrega uma base transversal concreta e mensurável no cone regular
q≠0. O transporte usa o wedgeBoostMap do contrato. As duas polarizações
circulares são conjugadas e distintas; a fase do boost nesta base é zero.
A decomposição nula é provada, não presumida. Para transformações lineares
com transporte do momento e preservação métrica explicitados, o Lean prova
C(g∘h;x,z)=C(g;y,z) C(h;x,y), onde Cij=-⟨ei(z),g ej(x)⟩.
A componente proporcional ao momento nulo desaparece na próxima leitura.

Cinco fontes finais, 26 declarações auditadas, todas rc0 e somente o trio.
As tentativas falhas foram preservadas: álgebra polinomial exigiu multiplicar
as identidades hiperbólica/radial; o rewrite final foi substituído por
normalização explícita do pareamento. Nenhum axioma foi acrescentado.

**Crítica C2.3 parcialmente aceita e corrigida.** O teorema espectral A3 já
usa fibra isométrica genérica; não precisa de outro motor. A afirmação Kimi
«fase zero em qualquer trivialização» é falsa: χ(x)=x produz o cobordo
exp(i s), igual a−1 em s=π (Lean). A fase é U(1); não se pressupôs argumento
real global aditivo. O boost orbital não constrói sozinho uma rede ou BW.

A resposta1265 antiga também foi confrontada: sua seção levava k a p/r,
e sua inversa atanh(p1/r) estava errada. A seção corrigida
L=Bx(ξ)Rx(a,b)By(log r), a²+b²=1,r>0, leva k=(1,0,1,0) a p,
é Lorentz/det1 e é equivariante para Bx;46 verificações CAS exatas.
Isso é CAS, não uma prova Lean do grupo de Lorentz inteiro.

Outra correção: a lei de cociclo quase em toda parte para cada s,t fixos
não autoriza substituir t=x−s. A prova Lean de cobordo é PONTUAL.
Exemplo explícito [DERIVED]: C(s,x)=exp(ix²) se x=s, e1 fora disso.
Para s,t fixos a lei vale fora de {s,s+t}, mas a diagonal dá
b(x)=exp(ix²); b(x)/b(x−s)=exp(i(2sx−s²)), diferente de1 em geral.
Logo a extração daquela diagonal não prova a equivalência de representantes
a.e.; exige versão estrita. A revisão Kimi8c terminou por timeout, sem
resultado validado; esse diagnóstico local não é atribuído ao modelo.

**MEDIDA: GlobalHelicityInducedRepresentationMeasured permanece nomeado**
(especificação em RESULTS.json): quociente orientado SO(2), cartas/exceções
e ação unitária fortemente contínua de Lorentz inteiro no L² do cone, com
caracteres ±1. A composição finita acima reduz essa dívida; não a renomeia
como paga. Duas polarizações e um boost não substituem essa representação.
Não se selecionou partição nem se criou habitante regional/vácuo/Fock.

MiMo46f falhou por resposta SSE sem finalização; Kimi8c por timeout.
Não repetidos, uso/custo desconhecidos. DeepSeekaa respondeu à crítica KMS,
que será auditada em C5; custo medido USD0.03249732. Kimi b175, objetivo
distinto de crítica final C3, segue pelo coordenador. Nenhum voto é prova.

Recursos C4: 10 compilações, parede186.335s,
CPU184.609s, bancada0.3709h/teto16h.
Custo remoto conhecido parcial da missão USD2.7237508140; desconhecidos não são zero.
Aceitação «teorema ou lema nomeado» atendida com o alcance acima.
Sem edição de kernel/um.py/gate. Próximo:C5, KMS de faixa e crítica C2.4.
