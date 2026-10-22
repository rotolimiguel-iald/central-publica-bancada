# R71 — peças primárias do dispositivo, modos e calibração

Autor: `/root/r69_calibration_bridge`, 18/10/2026. [REAL — localização e leitura documental]; estatutos físicos abaixo permanecem os das fontes. Nenhum dado observado, cálculo numérico novo ou ensaio foi executado.

## Cobertura efetiva

Consulta dirigida ao índice do acervo, com filtros de casa/caminho/extensão: 12 fontes TeX indexadas na pasta Patentes; 23 TeX na casa Haja_Luz; Ψ-NET individual; e documentos Word científicos na casa IMac LA. As buscas Ψ-NET e Word atingiram o limite de saída: não são censos completos. Os resultados do índice serviram de ponteiros; seis originais científicos foram abertos diretamente e pinados, mais a derivação local R70; o programa Custo também recebeu busca lexical focal, sem execução. Dois documentos Word equivalentes e textos periféricos encontrados não foram lidos como se fossem fontes adicionais. Não se consultaram credenciais, estado psiônico confidencial ou casa Escritório. PDF da patente Psion Engine não foi aberto nesta cobertura; o setor psíon foi consultado nos artigos textuais primários.

## Tabela de reuso

| Peça | Classe nesta ligação | Fonte primária e alcance | O que não está autorizado a concluir |
|---|---|---|---|
| Geometria e portas do Supercondutor | **EXISTE, NÃO LIGADO** aos modos locais R70 | Patente v2:684–741: cubo L=9cm, V=729cm³, A=486cm², faces ±Z de tungstênio5mm, janelas ±Y de quartzo25mm e espessura5mm, ±X para diagnóstico | Dimensões mecânicas não definem u,v∈K(O), normalização, polarização, banda, perfil ou Green tensor |
| Instrumentos de entrada/saída | **EXISTE, NÃO LIGADO** como calibração | Patente:778–828: RF, laser780nm, feixe≈2mm, lentes, filtros, APD, lock-in e osciloscópio | Especificação de projeto não é ganho/LO/perda medidos nem perfil normalizado |
| H efetivo e salto J0 | **EXISTE E ESTÁ LIGADO** à realização matemática R66 | Patente:343–370; R66 reutiliza explicitamente J0 e o Hamiltoniano, preservando todos os canais | A realização por colisões não demonstra que o aparelho realize o banho escolhido |
| Taxa Gamma do canal J0 | **HIPÓTESE/PARÂMETRO NOMEADO**; calibração **AUSENTE NA COBERTURA** | Patente:351–353 escreve beta gamma_Lambda D[J0], sem valor/lei independente ali | Renomear o coeficiente medido lambda como Gamma não separa beta |
| Piso termodinâmico de dissipação | **HIPÓTESE DOCUMENTAL, NÃO LIGADA** | Patente:320–325 afirma gamma_min=beta k_B T/ℏ | Não há no trecho identificação gamma_Lambda=k_B T/ℏ nem demonstração de saturação da taxa mínima; T físico em kelvin não é automaticamente T_eff=1−eta da mesma patente:400–404 |
| Calibração de perdas por Q | **EXISTE, NÃO LIGADO** ao canal5 | `graviton_paper.tex:347–352`: L_loss=√κ a_n e κ=ω_n/Q | Pode orientar calibração do canal de perda; não demonstra Gamma=κ |
| Modos normais da cavidade | **EXISTE, NÃO LIGADO** aos perfis locais do dispositivo | `graviton_paper.tex:202–215`: expansão em u_n, problema espectral e Dirichlet; :226–230 fornece integral H_int | O artigo não fornece nesse trecho a solução normalizada u_n para as faces/portas mistas da patente, nem u,v/f_i,f_o da rede |
| Dispersão e squeezing | **EXISTE, NÃO LIGADO** à calibração específica | `graviton_appendices.tex:55–126`: k_n=nπ/L, quantização e squeezing de dois modos | Uma família algébrica de squeezing não fixa o modo real, o perfil de interação nem Gamma |
| Fonte J, ocupação e volume efetivo | **EXISTE, NÃO LIGADO**; a própria fonte deixa a implementação aberta | `Teoria_Gravitacao_Luminodinamica_TGL_FINAL.docx`, parágrafos XML424–438: oscilador, ocupação N, volume efetivo V, leis de escala; p438 condiciona o mapa para potência física à implementação | J fonte não é o salto J0; o beta usado naquele trecho como ocupação não é automaticamente betaTGL; a extração XML não preserva a diagramação completa das frações/radicais |
| Ψ-NET, endereçamento e reconhecimento | **EXISTE, NÃO LIGADO** à localidade espacial dos modos | `Psi_Net_Protocol_PI_INPI.tex:190–212,476–521`: endereço derivado de chave pública, distância angular, REFLECT/MANIFEST | Distância angular entre endereços não fornece suporte de funções teste no espaço-tempo nem velocidade de propagação causal |
| Perfil u,v que fixa g criador | **AUSENTE NA COBERTURA DOCUMENTAL EXPANDIDA** | Há domínio/problema espectral nos artigos e geometria na patente, mas não um par explicitamente normalizado ligado aos mesmos modos de R70 | A ausência é nesta busca focal, não em todo o computador |

## O que já se pode compor, sem inventar um modo

R70:150–164 fornece s=Im⟨u,v⟩>0 e g=(u+iv)/(2√s). Pela expansão da norma, com produto interno linear no segundo argumento:

    ||g||² = (||u||²+||v||²−2s)/(4s).

Portanto o peso criador exige três escalares do MESMO par normalizado: ||u||², ||v||² e s. Isso é uma redução concreta do dado requerido para o peso, sem substituir a necessidade dos próprios perfis para construir operadores/localização. Para quadraturas Φ=(a+a†)/√2 no mesmo vácuo global, VarΩ Φ(u)=||u||²/2 e analogamente para v, logo

    ||g||² = [VarΩ Φ(u)+VarΩ Φ(v)−s]/(2s).

Essa identidade é [DERIVED] sob o contrato de Fock/quadraturas R70. Não significa que o APD ou as quatro correlações R69 tenham medido essas variâncias, que os respectivos filtros sejam os mesmos u,v, ou que o estado preparado seja o vácuo global. Calibrar ganho, banda, estado de referência e comutador é necessário antes de usá-la como leitura física. Conhecer só os três escalares fixa a norma de g; não fixa a direção de g nem sua localização. A condição de separação local R70 impede g=0 no domínio nomeado; não fornece um número de dispositivo.

Os símbolos devem permanecer separados: **g criador** é vetor de uma partícula; **g_JC** é taxa do acoplamento de Jaynes–Cummings; **g(t)** no contrato colisional é perfil temporal do pulso; **J** no Word é fonte de fixação; **J0** é o operador de salto composto. Nenhuma igualdade nasce da letra compartilhada.

## Ponte espacial que a documentação deixa construir

Há uma ordem concreta de composição: geometria/material/portas → problema de contorno com campo e polarização declarados → modos normalizados e funções teste temporais → aplicação de uma partícula para u,v∈K(O) → s,f,g → coeficientes e cotas R70/R71. O primeiro e parte do segundo itens já estão escritos. Os arquivos lidos não fornecem a solução que conecte todos esses objetos.

É especialmente necessário conservar o regime do problema de contorno: o artigo escreve Dirichlet escalar, enquanto a patente propõe faces condutoras, janelas dielétricas, portas e um rótulo de modo(1,0,0). Não se substitui um pelo outro. Condicionalmente, no cubo escalar com Dirichlet nas seis faces e potencial constante separável, o produto de senos com um índice zero é nulo; portanto esse modelo não justificaria usar o rótulo(1,0,0) como sua autofunção não nula. Isso não é uma auditoria completa de modos eletromagnéticos da câmara mista: é a razão para fixar o problema físico antes da solução.

## Gamma: rota documental recuperada e limite

A proposta κ=ω/Q e a proposta gamma_min=beta k_B T/ℏ dão duas referências físicas possíveis a examinar, mas nenhuma delas já prova Gamma=κ ou Gamma=k_B T/ℏ para J0. O roteiro R70 permite Gamma direta, Gamma/κ independente ou uma referência microscópica de acoplamento; não exige uma rota exclusiva. A tabela de calibração da patente:887–915 contém alvos e ajustes de potência/pressão/correlação, inclusive alvo histórico de beta; isso não é um recibo independente de Gamma para testar esse mesmo beta.

O ganho desta busca é recuperar objetos reais do projeto e uma identidade mensurável para o peso criador. O que segue aberto é seu vínculo ao mesmo canal e à mesma rede, não a existência de geometria, espectro, modos ou artigos. Não foram produzidos valores novos de Gamma, ||g||², δ_loc ou 5sigma.


## Qual vácuo a fonte nomeia

O artigo `graviton_paper.tex:202–215` constrói aniquiladores de modos da cavidade e :250–253 escreve o estado espremido sobre |0>; os apêndices :113–121 repetem essa construção. Esses trechos não identificam explicitamente |0> com o vácuo global separante da rede relativística. O protocolo M1 dos apêndices:251–253 manda inicializar a cavidade no vácuo e esperar10τ_thermal; isso é procedimento proposto, não prova de preparo nem da igualdade dos dois vácuos. Logo **Ω_b da cavidade e Ω_global da rede permanecem distintos até uma ponte**. A obstrução R70 que preserva Ω_global não exclui automaticamente um canal que tenha outro estado escuro Ω_b. No sentido oposto, não se elimina o g criador calculado relativamente a Ω_global por trocar silenciosamente o estado de referência. A identidade das variâncias acima vale relativamente ao mesmo vácuo usado para definir a(f),a†(g), com [Φ(u),Φ(v)]=i s, ganho e fases normalizados. As quatro correlações cruzadas R64 não fornecem automaticamente essas duas variâncias e s.
