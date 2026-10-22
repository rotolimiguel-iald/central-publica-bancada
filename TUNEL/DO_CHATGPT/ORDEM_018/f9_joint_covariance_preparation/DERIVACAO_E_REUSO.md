# Derivação e inventário da montagem I03

[REAL — leitura/AST/pins] Request f200dee1-0ecf-4a51-9b38-4c32d7eb0696. Esta nota é preparação local, com zero chamada científica. Fontes por bytes em FONTES_PINADAS.json. Não há números de C, centros ou resíduos observados nesta entrega.

## Alternativas anteriores ao código

ALTERNATIVAS_ANTES_DO_CODIGO.json foi gravado antes do módulo. A alternativa A apenas receberia 600 C prontas e verificaria metadados; ela deixaria a montagem que faltava a cargo de terceiros. B, escolhida, monta blocos explícitos e reutiliza a primitiva estelar já qualificada, mantendo o solver gaussiano único. Para deduplicação, comparar C+respostas+suporte+normalização seria possível depois de qualificar tudo; agora preservar todos600 é mais simples e não confunde coincidência de matrizes primitivas com equivalência de experimentos completos.

## Inventário e reaproveitamento exatos

| Fonte | Parte reutilizada | Limite |
|---|---|---|
| covariance_support/qualify_stellar_family.py | block_correlation, ordem de chaves, fórmula de incidências e laço cenário/frações | main é um controle consumido com IO e guard; não é biblioteca de montagem conjunta, não é chamado |
| derivacoes/preflight_262/baseline_stellar.py | referência da extração AST de ak…baseline | função só reproduz baseline, não a família correlacionada; não duplicada como solver |
| covariance_support/qualify_flow_errors.py | receita documentada SN e dois SBF; recibos existentes podem ser referidos explicitamente | main não é callable pura de compressão; nenhum centro/fluxo é carregado agora |
| h0dn_documentary_review/linear_design/ESPECIFICACAO_LINEAR.json | IDs, grafo, eta63, X/a_h/c_C nativos, ordem das linhas | prova estrutural não mede suporte da C com cross-blocos arbitrários |
| covariance_support/singular_gaussian_v2.py | guard futuro único de simetria/PSD/posto/suporte | nenhum eigensolver novo ou chamada nesta entrega |
| covariance_support/linear_gaussian.py | FlatNuisanceGaussian futuro, com normalização e medida plana | nenhum ajuste, integral ou informação avaliada aqui |
| f9_likelihood_consumer_preparation/likelihood_consumer.py | dono de Ty/TCTᵀ, origem afim e ligação ao mesmo guard | o builder devolve C nativa e pin; não aplica T |
| f9_five_model_assembly_preparation/five_model_assembly.py | fonte da estrutura/respostas das cinco hipóteses | builder não gera média nem muda modelo |

Não foi encontrada função pura existente que monte os nove blocos de 283 linhas para todos600 mantendo5MM. O preflight de262 excluiu5MM explicitamente por ausência das escalas de referência e incluiu só o baseline estelar. A extensão nova monta a família completa, mas não inventa aquelas cinco variâncias.

## Construção estelar

[DERIVED — sob a receita condicionada] Para cada rótulo ε e tupla (u,v,p,q), a primitiva da fonte constrói E_ref,E_J,E_host,E_5643 como blocos εεᵀ e identidade fora dos grupos. Então:
`Rm=(1-u-v)I+u E_ref+v E_J`;
`Rh=(1-p-q)I+p E_host+q E_5643`.
A grade pinada tem u,v,p,q≥0 e u+v,p+q≤3/4, portanto Rm,Rh≽I/4. As matrizes têm diagonal1. Com incidências A/B/H:
`Cstar=A diag(a²) Aᵀ + B Dm Rm Dm Bᵀ + H Dh Rh Dh Hᵀ`.
D0=0 é **INPUT explícito** da receita de baseline; não estimativa de erro omitido. O núcleo de Cstar é a interseção dos núcleos dos fatores, sob erros positivos. Diagonal e nulidade estrutural são preservadas dentro desta família restrita. Isso não prova completude física da decomposição, nem torna verdadeiros os coeficientes de correlação propostos.

O histórico achou menos desenhos primitivos distintos que rótulos. Não se transfere esse número para covariâncias/respostas/normalizações conjuntas. Todos os 300 rótulos estelares são mantidos, cada um com duas receitasSBF.

## Construção conjunta e unidades

[DERIVED] Particione a linha em nove blocos r_a. Para cada bloco diagonal admitido C_aa e cada par a<b com C_ab explicitamente informado, preencha C[r_a,r_b]=C_ab e C[r_b,r_a]=C_abᵀ. Iniciar com NaN, e exigir cobertura/finiteza final, torna buracos visíveis. Zeros de cross-blocos precisam de valores e declaração explícita. C_aa≽0 separadamente não basta: um C_ab arbitrário pode tornar C indefinida ou mudar seu suporte. O guard de suporte já existente decide isso numericamente sob contrato de tolerâncias, e pode recusar; o builder não corrige a matriz.

[DERIVED] T é diagonal com fator5 exatamente nas duas linhas de interceptos e cincoMM, e1 nas demais. O consumidor realiza C'=TCTᵀ, incluindo cross-blocos. Logo MM/intercepto×mag ganha fator5; dois eixos dex ganham25. Não se pode transportar só a diagonal. A multiplicação de todos os vetores e origem pela mesma T conserva a equação; X e médias vindos do montador já estão no espaço de saída.

Floating products podem produzir assimetria de arredondamento. O builder conserva os bytes, sem tolerância nem média interna. SupportGaussian existente compara com Cᵀ no limiar explícito relativo à escala e então diagonaliza sua parte simétrica; o eventual efeito numérico e seus limites pertencem à qualificação, não à presente prova algébrica.

## MM, compressões e ausências fechadas na interface

[OPEN] CONTRATO_MM_CANDIDATO.json#/alternatives/A/reference_binding, /reference_endogeneity e /shared_covariance_support/no_silent_failure exigem referências fixas D_ref,v_ref, receita e lei de trabalho. Seus campos numerical_variances/protected_references permanecem nulos. A interface recebe os valores/variâncias com proveniência; não os busca, deduz de H0(theta) ou estima de um centro. O código implementa apenas A diagonal com crossMMzero explícito; alternativaB primitiva não herda o pivô gaussiano e é ausência de componente suportado, não um caso aproximado silenciosamente.

[INPUT] A receita upstream simétrica é `V_i=[(σD_i/D_ref_i)²+(σv_i²+s_pec²)/v_ref_i²]/ln(10)²`. O termo b_up=1/(ln10 v) é a receita declarada, não o Jacobiano cosmográfico completo de U(v). Esta candidata não efetua essa conta: exige V_i e o recibo da receita, preservando o problema de adequação/endogeneidade. Positividade de uma matriz diagonal só prova sua PSD matemática; não prova lei de amostragem condicional adequada.

[OPEN] As duas receitas SBF do preflight usam m apenas ou m mais M independente condicionado. Ao alterar a variância usada em pesos de intercepto, o y comprimido e C cruzada também podem mudar. A família fixa uma compressão por receita e exige suas referências. A interface não supõe que adicionar σM² só mude um número de C mantendo todos os demais objetos automaticamente válidos.

[OPEN] RESOLUTOR_F9.json#/resolved_contract/data/block_factorization marca independência entre blocos como INPUT. A API exige os36pares e proíbe None→0. Os oito paresMM obedecem especificamente a propostaA. Demais cross-blocos não são inferidos nem lidos nesta preparação.

## Suporte, respostas e normalização

[DERIVED — condicionado] Seja r=rank(C'), X' de posto63 dentro do suporte e origem afim fixa o'. Com a mesma medida κdη:
`∫ L(y|θ,η,C') κdη = κ (2π)^(-(r-63)/2) [pdet(C') det(X'ᵀ C'⁺ X')]^(-1/2) exp[-bᵀPb/2]`,
onde `P=C'⁺−C'⁺X'(X'ᵀC'⁺X')^(-1)X'ᵀC'⁺`, b=y'−μ(θ), e as condições afins pertinentes são verificadas pelo backend. Diferentes normalizações não desaparecem só porque há63nuisances ou283IDs. Usos relativos requerem a mesma constante κ, medidas, dimensões e finitude; não se anuncia evidência absoluta.

O builder liga cada rótulo à receita das cinco respostas, à estrutura do consumidor e às referências de suporte/normalização, mas seus recibos numéricos continuam null. Cross-blocos podem invalidar nulidades, posto ou suporte das respostas. Só após qualificação do C conjunto e dessas respostas será legítimo preencher recibos separados; esta entrega não falsifica esse passo com um booleano.

Falha computacional/schema/PSD/posto não é probabilidade zero. Residual que legitimamente sai do suporte afim fixo pode ter densidade0 conforme o contrato do backend. Nenhum modelo é eliminado por exceção; nenhum veredito é produzido.

## Alcance e mínimo restante

[REAL] Código puro proposto e metadados; não teste numérico. [OPEN] Revisão independente da montagem; ligação técnica ao controlador; qualificação nova dessa ligação em escopo autorizado; referências/variânciasMM e receitas físicas O01/O02; C e suporte reais após abertura autorizada. A falta de certificado uniforme não impede esta entrega ENGINEERING_ONLY: limita inferências científicas futuras. Não são criados controles redundantes, launcher, AUTH, CLAIM ou pedidos artificiais.
