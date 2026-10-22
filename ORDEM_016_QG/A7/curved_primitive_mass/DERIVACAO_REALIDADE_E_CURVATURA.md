[DERIVED — realidade e parcela algébrica de curvatura da primitiva; REAL — CAS; OPEN — laços curvos/normalização causal]
# A7.b — conservar realidade e explicitar o termo inferior em K
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T00:42:58.822103+00:00.

O dicionário069 fixa h*=h,c*=c,b*=b,barc*=-barc para conjugação (não confundir
este * com o rótulo de antifield). Uma extensão compatível é

    (phi^ddagger)*=-epsilon_phi phi^ddagger,
    (sF)*=(-1)^paridade(F) s(F*),   phi*=epsilon_phi phi.

O star é antilinear e reverte os produtos. A identidade confere nos oito
geradores livres e estende-se aos produtos pelo Leibniz graduado. sc=c partial c
também a satisfaz. Assim h^ddagger,b^ddagger,c^ddagger são anti-reais e
barc^ddagger real; a ação BV escrita na069 permanece real. A combinação
u=4kappa(h^ddagger+C*barc) é anti-real para qualquer kappa real não nulo.

Os monômios de gerador A2,Z,u B c nabla u e u D1(nabla c)u, com coeficientes
reais, são ímpares e anti-reais. Portanto seu sF é real. Não se deve acrescentar
um i para 'tornar F real': isso tornaria sF não real. Os fatores i de Fourier
dos vértices são restaurados separadamente, como antes. Teste:20checks,
3negativos,rc0. É uma extensão explícita de convenção, não prova de toda a
hierarquia causal ou de um gerador não linear ainda não comparado aos laços.

Dos operadores livres já conferidos e C*=-Itr K_gauge/2 segue

    E=4kappa H= -box Itr + Itr K_gauge C +2K id+K g trace.

H é físico ANTES de eliminar b. Mantemos essa ORDEM de derivadas, sem
comutá-las silenciosamente. Escreva M(H)=2KH+Kg trH. Então
B(M)=-K(H/3+2g trH/3) e
D1(M;r,v)=K[sym(r,Hv)-sym(v_flat,H r_sharp)]. A contribuição algébrica dessa
curvatura à candidata marcada, retirado4iκA0, é

    -K{ [(p+r/2)·v](H/3+2g trH/3)
         +[sym(r,Hv)-sym(v_flat,H r_sharp)]/3 }.

A compatibilidade métrica e K constante justificam B paralelo. A mesma
identidade foi conferida nas fibras euclidiana e Lorentziana(+---):260checks,
80polarizações não nulas,4negativos. Não é cálculo do laço curvo. Os termos
gerados ao reordenar derivadas covariantes e os termos finitos permanecem
separados. A identidade covariante da parcela B continua

    delta Psi_B + (1/2)nabla_mu J^mu
      = u B[c.nabla E+(div c)E/2], J^mu=u B c^mu E.

Com cutoff chi, integral chi deltaPsi_B tem ainda
+(1/2)integral(nabla_mu chi)J^mu. A parcelaD1 não exige integração por partes
nessa representação. Os termos com antighost provenientes de u são conservados.
CPU realidade0.03125s;curvatura0.28125s.
O lado da primitiva fica mais determinado; sua igualdade ao coeficiente causal
real, s1F e a hierarquia multilinear ainda não foram demonstrados.
