[DERIVED — símbolo sob transporte Taylor declarado; REAL — CAS; OPEN — adjunção bilocal completa]
# A7.b — correção da orientação Taylor da fonte
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T07:34:11.146853+00:00.


Tentativa preservada: source_full_fourier_engine.py passou no controle
plano, mas usou o polinômio P_j(x) junto da exponencial exp(-ipx).
A primeira curvatura divergiu do log covariante local já medido.
Separar a soma por grau externo localizou o erro exatamente em j=1.

A reversão do deslocamento exige P_j(-x)=(-1)^j P_j(x), além da troca
da exponencial. Em v2, apenas esse fator foi corrigido; kernels,
prescrição, medidas e multiplicadores meromórficos permanecem iguais.
Não se ajustou um coeficiente para zerar Ward. O predecessor fica no disco.

Na base [Tpv, (pTp)(pv)/p², trT(pv)], para p²>0 e retirados C_E, i e K,
o símbolo candidato de primeira curvatura tem coeficientes (1,L,L²):
- ['421/144', '71/24', '0']
- ['-35/24', '0', '0']
- ['-191/288', '-19/48', '0']


Três amostras determinam os coeficientes; o caso independente
p=(1,2,-1,1), v=(2,-1,1,3), T=e11 reproduz os três componentes.
O termo racional com 1/p² permanece: ausência de contato não é ausência
de kernel. As amostras de ajuste não são contadas como prova independente.

Após a correção, a parte sem log(z) explícito reproduz o log covariante
local anterior, na normalização -1/4. Os kernels com log(z) acrescentam
ao coeficiente de FourierLog exatamente Tpv/2+trT(pv)/4 nos controles,
incluindo o não axial. Portanto o log local UV sozinho não determina
todo o multiplicador de Fourier da fonte.

LIMITAÇÃO: esta é a soma do símbolo na ordenação Taylor especificada.
A identificação da adjunção bilocal, sua imagem pelo operador Einstein
curvo e a soma com os pares/tadpoles/W ainda não foram demonstradas.
Não é Q2. O Kimi recebeu separadamente a pergunta sobre adjunção, sem
estes números, preservando a independência da revisão.

Comandos: python -X utf8 -B source_firstK_symbol_check.py e
source_firstK_log_partition_check.py; depois source_firstK_symbol_check_v2.py,
todos no Python simbólico de A4. rc0, mas o primeiro resultado NÃO satisfez
a comparação matemática: os rc0 significam execução e ajuste, não aceitação
da hipótese. Logs e SHA constam do manifesto desta entrega.
Próximo: concluir o controle não axial do par e construir E da fonte sem
comutar indevidamente funções não locais de Box. Gate e originais intactos.
