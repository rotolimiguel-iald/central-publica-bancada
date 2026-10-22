[DERIVED — diferencial livre e deslocamento do antifield; REAL — CAS finito; OPEN — contratermo completo]
# A7.b — manter b e cancelá-lo pela combinação correta

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-24T23:55:29.094229+00:00.

A069 escreve S0=Sgf+<h*,Kc>-<barc*,b>. Para tornar explícita sua frase
«antibracket escolhido para gerar(7)», usamos sF=(S0,F)_σ, com
σ_A=(-1)^paridade(phi_A) multiplicando cada par canônico(phi_A,phi_A*).
Equivale às coordenadas Darboux tilde(phi_A*)=σ_A phi_A*; não é alteração
da teoria. Derivadas direita/esquerda e essa identificação são mantidas
juntas. Nesse dicionário, a ação escrita na069 dá

    s h=Kc; s barc=-b; s b=s c=0;
    s h*=Hh+C*b;
    s b*=Ch-ell^-1 b-barc*;
    s c*=-Q barc-K*h*; s barc*=Qc.

H é a Hessiana física livre ANTES de eliminar b, não a mínima gauge-fixada.
HK=0 e CK=Q garantem s²=0, usando adjuntos e coeficientes de fundo fixos.
Por exemplo s²c*=Qb-K*C*b=0 e s²b*=Q c-Q c=0. Não se pode misturar
esse dicionário com outro sinal canônico para os mesmos símbolos de antifields.

Segue, sem descartar b,

    hat_h*=h*+C*barc,
    s hat_h*=Hh+C*b-C*b=Hh.

O deslocamento tem paridade ímpar e gh=-1. Na normalização principal
Euclidiana usada no cálculo dos vértices, E=4κH e u=4κ hat_h* dão su=Eh.
Aplicamos então a identidade graduada já derivada à candidata

    F=A0/2 integral u_A B_AB c^μ partial_μu_B,
    B(A)=-A/6-I trA/12, A0=1/(8π²).

O coeficiente linear em h* de sF é4κA0 B[c·∂E+(div c)E/2]. Com
c constante e a convenção Fourier+i, a parte transversal reproduz a
forma4iκA0[-(p·v)(E/6+P_T trE/12)] anteriormente medida. Esse fator
é calculado, não uma identificação entre H e E sem normalização.

O CAS conferiu um bloco com um modo de gauge e outro físico independente,
H=diag(0,m/(4κ)), CK=Q=1: nilpotência10×10, números fantasma, deslocamento
e coeficiente;4checks+2negativos, rc0,CPU0.09375s. A prova
geral acima é por identidades de operadores; o bloco é controle de sinais,
não substituto da prova. Não houve compilação Lean nem chamada remota.

Ao expandir u aparecem também antighosts: esses termos são parte do gerador,
nunca omitidos. Para cutoffχ, a identidade módulo divergência traz
+(A0/2) integral(partial_μχ)J^μ após integração por partes. Não apagamos
esse contato. A realidade na involução escolhida, os demais momentos,
componentes longitudinais, contribuição não linear s1F, curvatura e anomalia
causal finita ainda precisam ser conferidos. O gerador completo não está
identificado com esta única parcela. Nenhum kernel, original ou gate alterado.
