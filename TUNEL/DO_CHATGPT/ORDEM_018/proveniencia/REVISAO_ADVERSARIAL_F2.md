# Revisão adversarial F2 — ORDEM_018

[REAL da revisão documental / DERIVED condicional / OPEN nas pontes observacionais] Revisora: chatgpt-codex/ordem-018/proveniencia. Data UTC: 2026-10-06T00:35:25.973664+00:00.

## Achado primeiro

**F2-REV-01 — P2 antes de uso quantitativo em lentes: falta definir a direção de f_phi.** Na NOTA_DERIVACOES_F2.md, linhas 74–76 e resumo 132, a expressão “a reconstrução do potencial um fator f_phi” não define uma razão. A nota escreve D_fit/D_bg = f_t f_phi f_l f_s/f_ls. Essa multiplicação é válida com uma convenção específica; com a outra convenção usual, a dependência se inverte.

Para tornar o ponto verificável, defina F_D = f_l f_s/f_ls, Delta_t_obs = f_t D_phys Delta_phi_true/c, D_phys = F_D D_bg e a equação do ajuste Delta_t_obs = D_fit Delta_phi_fit/c. Então:

- Se f_phi = Delta_phi_fit/Delta_phi_true, **D_fit/D_bg = f_t F_D/f_phi** e **H_fit/H_bg = f_phi/(f_t F_D)**, mantendo o restante da cosmologia fixo.
- Se f_phi = Delta_phi_true/Delta_phi_fit, o **produto escrito na nota é correto** e a razão de H é seu inverso.

[DERIVED] Não é possível decidir pelo nome isolado qual convenção foi pretendida. A correção necessária é definir a razão e a equação da leitura temporal antes de transportar esse fator para uma inferência. Por exemplo, com os demais fatores iguais a 1 e potencial reconstruído duas vezes o verdadeiro, a distância inferida é metade da física. A convenção omitida poderia inverter essa resposta.

**Impacto delimitado:** as duas alternativas explícitas da nota usam f_phi=1; os proxies endpoint do JSON também não variam esse fator. Esses números não são afetados. Permanece sustentada a conclusão de que K sozinho não seleciona o mapa de lentes. A revisora não alterou a nota original nem escolheu uma ponte física no lugar do autor.

**Não foram encontrados outros erros aritméticos ou de direção no escopo examinado.** Isso não certifica pontes marcadas OPEN, o rito observacional, a cadeia histórica de pré-registro ou previsões posteriores à versão examinada.

## Conferências e limites

| Objeto | Conferência | Estatuto e limite |
|---|---|---|
| R-D: Q integral | Q = integral(k/E)/integral(1/E), e não k no endpoint. O fator comum K* e c/H0 cancelam. Para E crescente e beta positivo, 1 <= Q <= k. | DERIVED sob o fundo e as hipóteses indicados. O módulo em I exige rho+p >= 0 para reduzi-lo a (2/3)lnE. |
| R-D: pequeno z | Para a fiducial plana, matéria mais Lambda e radiação nula, k−1 ~ beta Omega_m z; Q−1 ~ beta Omega_m z/2. | A diferença de fator 2 é real. Não transferir esse coeficiente sem trocar a expansão E(z) para outros fundos. |
| R-D: unidades e sinal | E, k e Q são adimensionais; c/H0 dá Mpc; 5 log10 Q é a diferença de magnitude ac/sombra e é positiva. | BAO continua no fundo nu no motor citado; Q não fornece automaticamente uma alteração de D_H/r_d. |
| R-E: dualidade | eta_obs = f_L/f_A; fator comum cancela. Somente luminosidade modificada permite eta = Q/K* no cenário acumulado. | DERIVED condicional à reciprocidade da geometria de referência. O limite eta(0) normaliza a forma. K não seleciona f_L/f_A. OPEN. |
| R-F: temperatura | rho_dot + 4H rho = Q_gamma e rho proporcional a T^4 dão T_dot/T = −H + Q_gamma/(4rho). | Q_gamma tem unidade de densidade de energia/tempo. O expoente gamma_T = Q_gamma/(4Hrho) só é constante sob hipótese adicional. Não igualar gamma_T a beta por nome. |
| R-L: S8 | Com sigma8 fixo e somente Omega_m multiplicado por 1+beta, a mudança de S8 é positiva: sqrt(1+beta)−1 = 0,599766%. | DERIVED de uma troca de parâmetro declarada, não uma previsão de supressão do crescimento ou do shear. A dinâmica perturbativa continua OPEN. |
| R-J: relógio | Gamma = beta tau* omega²/2 tem unidade s^-1; f=100 Hz exige omega=2 pi f. Com tau*=tP, o JSON reproduz 1,280358e−40 s^-1. | Identidade condicional. T(t)²=T(2t) duplica o tempo, não deriva nova massa/escala. P²=P tampouco amplifica sinal. |
| R-K: massas | m2 = beta sin45 graus vezes 1 eV = 8,507414 meV. Com m1=0 e NO: Delta_m21² = 7,23760947e−5 eV². | sin45 graus é POSTULATE, 1 eV é NORM/INPUT. São condições da previsão; não estão demonstradas só pelo valor de beta. |

[DERIVED — direção de m2] Mantendo m2 fixo, Delta_m21² = m2² − m1² **diminui** quando m1 aumenta. Admitir m1>0 não poderia elevar essa previsão para encontrar um splitting observado maior. Este é um controle de direção para usos posteriores, não uma alegação de que a nota tenha feito a manobra contrária. Não foi calculado novo pull ou veredito.

[OPEN preservado] A nota separa corretamente a escala de massas da soma que já foi aposentada como discriminante; não a reabre. O erro de JUNO não fornece, sozinho, separação entre TGL e uma previsão única de LambdaCDM para esse splitting. Uma combinação NuFIT que contém JUNO não constitui uma segunda determinação autônoma. A formulação respeita a novidade de uso sem exigir ignorância temporal dos dados.

## Verificação independente registrada

[REAL] review_f2.py leu os bytes da entrega e dos originais necessários. São **18 arquivos registrados por SHA-256**: seis arquivos da entrega, três fontes científicas primárias locais, três arquivos de recortes e seis páginas primárias públicas já arquivadas pela entrega. Os hashes dos três originais e dos seis arquivos HTML coincidiram com o manifesto do autor. Sete recortes foram comparados literalmente às linhas dos originais e coincidiram. O Atlas, sujeito a atualizações simultâneas, não foi usado como substituto desses originais nem incluído nessa afirmação de imutabilidade.

[REAL] Uma implementação própria de Simpson adaptativo conferiu os 18 valores de Q do JSON, com diferença absoluta máxima **1,7763568394002505e−15**; para 5 log10 Q, **3,8565613376395635e−15**. Endpoint, m2, Delta_m21², razão algébrica de S8 e Gamma concordaram à precisão de ponto flutuante usada. Beta foi reconstruído a partir de ALPHA_FINE_CODATA_2018 lida no um.py e sqrt(e), sem literal de beta. A integração foi conferência do exemplo sintético, sem ler novamente dados de rito, ajustar parâmetros ou avaliar uma nova hipótese contra observações.

As seis páginas arquivadas foram examinadas pelos abstracts: sustentam as barras e as ressalvas de combinação citadas na entrega, inclusive 0,021 para KiDS, 3,9 km/s/Mpc para TDCOSMO com Pantheon+, 0,018 para o teste direto de temperatura e 0,008 para a combinação direta/indireta, além de 0,12e−5 eV² em JUNO. Não foram baixadas versões novas nem recalculados centros/pulls. A revisão não afirma cegueira: os abstracts contêm centros publicados. Essas barras são insumos de resolução, não validação de um mapa TGL.

Os “54 testes” da entrega correspondem a verificações numéricas internas de refinamento, beta=0 e desigualdade; não equivalem a 54 testes independentes da natureza. O presente exame sustenta sua aritmética e a separação de estatutos, com a ressalva F2-REV-01. Não certifica a cronologia de criação do plano apenas pelo texto ou mtime.

## Identidade e artefatos

Versão congelada examinada: derivacoes/NOTA_DERIVACOES_F2.md, 15767 bytes; SHA-256 lido: `4282e0d6125e862fc225f9e8d82ecc5e55089500048cab9c0272eb690a0a458c`.

- `REVISAO_ADVERSARIAL_F2_FONTES.json`: caminhos absolutos, SHA-256, recortes, diferenças numéricas, achado e escopo.
- `REVISAO_ADVERSARIAL_F2_ABSTRACTS.json`: extração dos abstracts das seis páginas já arquivadas, sem requisição externa.
- `review_f2.py`: conferência independente; não executa/importa o código científico original nem o script do autor.

Não foi executado um.py, motor.py, fundo_gpu.py ou f2_analysis.py. Não foram examinados poder_forma ou novos forecasts. Nenhum original foi alterado, nenhum provedor foi chamado, nenhum rito foi repetido e nenhum gate foi movido. NOT_FALSIFIED não foi convertido em CONFIRMED.
