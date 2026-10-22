[DERIVED — fórmula preservada, argumento corrigido; REAL — CAS; OPEN — amplitude]
# A7.b — revisão DeepSeek dos contatos logarítmicos
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T07:11:27.051220+00:00. Job `1f45d6da-5abe-47e5-ae5b-6387733f0aad`.
Uso {'prompt_tokens': 233109, 'completion_tokens': 49466, 'total_tokens': 282575, 'prompt_tokens_details': {'cached_tokens': 226304}, 'completion_tokens_details': {'reasoning_tokens': 46541}, 'prompt_cache_hit_tokens': 226304, 'prompt_cache_miss_tokens': 6805}. Custo estimado informado ['0.031379262', '0.062758524']USD,
tarifa de pico como teto da estimativa, não fatura. Nenhuma repetição.

A fórmula recebida para R(D[z^-n L^ell])-D R(z^-n L^ell) coincide com
a fórmula da bancada sob a hipótese de polo simples da família base.
Mas a frase de que apenas t0,t1 da soma de Leibniz contribuem é falsa:

    ell=2, c(a)=a³, T(a)=rho/a:
    parcelas = [-6rho,+6rho,-2rho], soma=-2rho.

O corte t<=1 daria0. A forma final correta resulta da soma completa.
Para c=a^m, o termo m=ell+1 usa
sum_t binomial(ell,t)(-1)^t/(t+1)=1/(ell+1); o termo m=ell>=1 usa
sum_(t>=1) binomial(ell,t)(-1)^t=-1. A exceção ell=m=0 dá0.
O resto analítico da família não contribui para esse comutador local.

Conferimos graus ell0..6,m0..8 com e sem resto analítico. Também foram
conferidas as três contas do perfil: -3K/32, -37K/384 e -K/3072.
São 131 controles, rc0, CPU0.296875s.
O termo u0 citado é raiz de Van Vleck; chamar apenas de determinante
sem a raiz pode reproduzir a confusão corrigida na revisão Kimi.

A concordância vale para a álgebra do perfil sob R fixada. Não preenche
por si só existência distributiva, bitensores, soma causal ou Q2.
