# E0 — revisão independente das taxas e cenários O5

[REAL de contas leves; cenários INPUT/DERIVED; NÃO-CEGO]

UTC 2026-09-22T19:38:03.781577+00:00. **Sem erro aritmético ou bloqueante novo encontrado no recorte solicitado.** As ressalvas presentes impedem tratar as projeções como taxa observacional corrigida, previsão física aceita ou data de alcance5σ. Conferi hashes das cinco entradas/código, intervalos e conjuntos, Poisson e todas as80 linhas (dez leituras × quatro fatores × duas exposições), sem executar o builder, refazer OLS, MC, Fisher ou PE. Controle próprio: 0.0253s, uma thread.

## Poisson e exposição

Reobtive os limites centrais Garwood90% por **inversão direta da CDF Poisson**, sem usar os quantis chi-quadrado do construtor. Para N>0: CDF(N−1,lambda_lo)=0,95; CDF(N,lambda_hi)=0,05; divide-se por T. Para N=0: [0,−ln(0,05)/T]. Essa é inferência sobre taxa com exposição tratada como conhecida, compatível com a definição de [intervalo de taxa Poisson](https://www.stat.math.ethz.ch/R-manual/R-patched/RHOME/library/stats/html/poisson.test.html).

| exposição | N | taxa/ano | IC90 da taxa |
|---|---:|---:|---|
| 1.450000000 anos | 1 | 0.689655172 | [0.035374686, 3.271630702] |
| 1.450000000 anos | 21 | 14.482758621 | [9.704844654, 20.855478132] |
| 1.488153915 anos | 1 | 0.671973503 | [0.034467735, 3.187751260] |
| 1.488153915 anos | 21 | 14.111443570 | [9.456027769, 20.320776620] |

O conjunto raro tem1 evento, GW250114_082203, pelo corte SNR_GWOSC≥78 em O4a+b; não inclui a discovery O4c. Isso não certifica larguraδτ=0,058 para qualquer evento de mesma SNR. O conjunto calibrador contém21 eventos O4 dentre os31 produtos históricos; conferi todos os nomes com as linhas do fit e o inventário.

A soma GPS é **46962566 s = 543.548217593 dias = 1.488153915380 anos julianos**, contra o INPUT nominal1,45. O uso de1,45 eleva as taxas em **2.631305%** relativamente ao denominador GPS. As duas alternativas estão identificadas corretamente. Limites de arquivo podem incluir engineering e **não são live time**. Poisson estacionário para esse universo publicado é hipótese; falta função de seleção/exposição efetiva para inferir taxa física. Não se adicionou O4c ao numerador com denominador O4a+b.

## Ganhos, qualidade e volume

As contas usam g=2500/1600, 2500/1400, fator C5 arquivado e330/160. O5_C5_PSD continua um resultado de fonte/projeção e PSD individual, não fator medido de toda a população. BNS_ONLY_UPPER_CONTROL está explicitamente marcado como **controle, não forecast BBH**. Os três anos são duração de cenário, sem data de início prometida.

N_esperado=3 R g³ e banda=3 IC(R) g³ conferem. `count_CI90_from_Poisson_rate` é intervalo para a **média esperada** induzido pela incerteza da taxa: não é intervalo preditivo para a futura contagem, nem inclui incerteza em g, seleção, duty cycle ou população.

O cenário otimista dá z=z_base g sqrt(N_esperado/31), assumindo tanto volume g³ quanto qualidade das novas fontes igual à qualidade melhorada de fontes fixas. A hipótese forte está escrita no próprio JSON; não é uma identidade física. O controle de qualidade invariante retira o fator g de z e representa o caso idealizado em que mais detecções vêm de fontes mais distantes, junto ao limiar. As duas expressões conferem. Não aplicar novamente g aos números já escalados. N90/g² é diagnóstico do cenário de fonte fixa, não o N90 heteroscedástico da rotaIV MC.

As dez leituras estão presentes; R-RAIZ-COHERENT e R-PROP mantêm z/N90 nulos, R-GLOBAL mantém z0/N90null, e os regimes pequenos mantêm o diagnóstico sub-resolução via N90 operacional nulo. Nenhuma leitura escolhida, nenhum test_verdict preenchido, todos os gates permanecem NOT_CALIBRATED_RED. `operational_information_target` é transportado do core, cuja hipótese de efeito/população precisa acompanhar o uso.

## Cuidados de transporte documental, sem novo bloqueio

1. As projeções usam a mistura de qualidade das31 fontes, mas a taxa das21 O4. Isso está declarado; não rotular tudo “amostra O4 homogênea”. As larguras calibradoras não podem virar inclusão de eventos de teste.
2. Na ficha pública conservar a origem **calibração com offset zero PROIBIDA_COMO_TESTE**, que está no core e não reaparece literalmente em cada linha de forecast. Os z são diagnósticos de separação com sistemáticas ainda abertas, não significância observada.
3. Conservar os estatutos próprios das leituras, especialmente R-MOD conjectural e os nulos sem observável único. O gate genérico vermelho não substitui esse contexto.
4. Não usar a coluna com tetoBNS para anunciar BBH, nem as bandas da taxa como previsão de contagem realizada. Não há integração da incerteza do fit sigma(SNR) neste escalonamento; tampouco é afirmada.

Este parecer fecha a revisão **das contas e dos escopos declarados neste artefato**, não o portão E0.7 inteiro. SYSTEMATICS_ADENDO é revisão distinta; E1 não foi executado por mim nem pressuposto aqui. CritérioMf/chi_f continua no rascunho separado aguardando revisão do principal.

## Custódia

Artefato: `416b45cd9db34709cef6e33a85c3c78a2a4dc147166f62cf24e824198fdc02d1`. Builder lido: `2f5d33b9c663231aec06c3b196e7dff1e42d1d7fdfdfc1b662c9795737af0a32`. Controle independente: `2b8276c0c356e5c80a3e34bdf1ee2010d4808dc383d46e0538afa418f97edc5f`. Resultado: `53e06bfed373351a5db28b45cd6a8db0bcbe4c0a357339158e330d8b64124236`. Hashes de cada entrada e contas em `bis/c1_review/e0_rate_independent_results.json`. Nenhum arquivo de produção alterado.

## Adendo documental — adoção e selo

O texto acima é preservado da revisão independente anterior (SHA256 f95a94e8ef838d00b7d637af918ee0ca39c2517cca50c527f51aa37fe41f6bb8). A referência histórica a aguardar revisão do critério foi superada pela ordem expressa do usuário: [INPUT] SNR de rede GWOSC ≥12, mediana Mf_det ≥40 M☉, 0≤mediana chi_f<0,98; prioridade SNR≥30. Ausências permanecem AWAITING_GR_METADATA. Não é corte por largura de posterior nem estimativa de eficiência de seleção. E0 foi depois declarado selado pelo agente principal; a nova frente E1 não executa E2/E3.
