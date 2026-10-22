[DERIVED+CAS — revisão Kimi51c recebida e auditada; Q2 OPEN]

O Kimi preservou corretamente a ausência de propagadores de antifields e
a distinção entre autocontração normal-ordenada e contato Euler entre
vértices. Seu censo completo, porém, não foi adotado.

Em C=(Qbarc)_i c^j d_j c^i contra Vghost=barc h c, há DUAS duplas:
barc_X--c_Y e uma das duas c_X--barc_Y. Sobra c_X,h_Y. A enumeração
independente retorna2, com sinais Wick+ e-. C×C admite4 duplas antes
da soma de sinais. A exclusão de C na tabela e na receita R5 é falsa.
Além da contagem, o cálculo tensorial anterior em R_bal contém testemunha
não nula: célula(0,0), valor exato
-85645/512 na substituição registrada em AUDIT.json. Não
se infere contribuição não nula só da existência de um emparelhamento.

A identidade de cutoff impressa na seção5 repete o membro esquerdo e
acrescenta -I. A identidade correta, modulo divergência, é

 s0 int chi E_h Z = I - int (G* E_h) chi w,
 I=int E_h [G,chi]w.

Com o setor auxiliar completo, E_h=H0h+C*b, H0G=0,
G*E_h=Q*b. Este termo NÃO pode ser apagado por Bianchi. O controle
polinomial verifica a igualdade pontual incluindo a divergência. Após
substituir b=ell C h, manter qbarc=-ell C h dá q²barc=-ell Qc:
igualdade gaussiana livre não autoriza eliminar o auxiliar na cadeia
off-shell sem transformar a estrutura BV. Nenhum novo sinal foi ajustado.

36 controles locais, CPU0.09375s. Original e
recibo preservados, consumo registrado uma vez pelo ID de execução.
Os resultados do Kimi permanecem DECLARADO onde não conferidos; esta
auditoria não reconstrói toda A2 nem sua família lorentziana. Gate intacto.
AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
