# Revisão independente do preflight 262

Identidade: chatgpt-codex/ordem-018/preregistros. Consulta prévia à rota hubble.fase9_razao_discriminante, registros 458 (pré-registro) e 459 (resultado). Escopo delegado: revisão documental, de integridade e estática; nenhuma reexecução científica.

[REAL — revisão limitada] Não localizei defeito bloqueante na montagem ou na interpretação do preflight pinado. Este parecer vale junto ao RECIBO_REVISAO_PREFLIGHT_262_V2.json e seus controles explícitos, não como aprovação da covariância física completa, de um composto ou de veredito. O revisor leu o código e os recibos, sem importar módulos científicos, reconstruir C, recalcular ranks, autovalores, inversas ou informação. O script de revisão usa somente a biblioteca padrão.

## Identidade, custódia e execução registrada

O protocolo ORDEM018_PREFLIGHT_262_ERROR_ONLY_001 antecede o CLAIM, e o resultado repete o mesmo ID, protocolo e entradas. O manifesto cobre os nove artefatos da entrega; o protocolo fixa doze entradas. As dependências FLOW/estelar compartilhadas são cruzadas por hash e tamanho. O launcher pinado cria CLAIM, recusa artefato terminal ou CLAIM existente, fixa as quatro variáveis de threads em 1 e faz uma única chamada ao worker, com timeout de 120 s e sem repetição. Seu stdout reproduz os campos correspondentes do resultado, com returncode 0 e stderr vazio.

[REAL — recibo lido, não medição repetida] Parede registrada do launcher: 0,3955444998573512 s; worker: 0,26966370013542473 s; CPU do worker: 0,25 s. Python 3.14.3, NumPy 2.4.3 constam do recibo. A auditoria do produtor registra 27 controles. A presente revisão tem identidade, custo e controles próprios. Não certifica toda leitura de runtime por um sandbox de sistema operacional, nem transforma o launcher em API inviolável contra entradas alternativas.

## Montagem das 262 equações

A seleção é o prefixo de 262 linhas da especificação de 267, com identidade única de linhas: 178 host, 13 group, 55 SN_calibrator, 14 SBF_calibrator e dois interceptos SN_HF/SBF_HF. As cinco linhas excluídas são exatamente data/megamaser.dat:L5 a L9, todas e somente as megamasers. O subconjunto não altera a lista V01/V1 nem inventa as variâncias dos cinco MM.

A identidade dos 178 host é cruzada com os grafos MAS/HMS e grupos primitivos. O helper estelar contém as mesmas quinze instruções AST das linhas 54–68 de qualify_stellar_family.py, seguidas apenas por return baseline. As dependências compartilhadas de âncora, MAS e HMS entram por produtos de fatores, preservando covariância entre linhas. O main original e a grade de 300 casos não são chamados.

O bloco host ocupa as primeiras 178 linhas. Os 82 IDs de erros não estelares correspondem precisamente aos 13 grupos e 69 calibradores; suas variâncias positivas entram na diagonal. Os dois interceptos usam o recibo FLOW. A variante SBF muda somente sua variância diagonal, pelo quadrado do sigma indicado no protocolo. O resto parte do mesmo common. A independência entre blocos e os termos não estelares diagonais continuam hipóteses INPUT; a revisão de implementação não mede independência física nem completude de sistemáticos.

## Transporte por 5 e medida comum

[DERIVED — inspeção algébrica] T tem valor 5 somente nas linhas SN_HF/SBF_HF e 1 nas demais. O código aplica C_t=T C Tᵀ, X_t=T X e A_t=T A, A=(a_h,c_C). Nas duas linhas de intercepto, X contém −1/5, a_h=1 e c_C=0: o transporte é, portanto, −1, 5 e 0. A unidade da observação torna-se magnitude; h permanece em dex e δ_C em magnitude. Transportar o intercepto significa transportar sua equação e seu erro; não foi necessário materializar seu centro.

No suporte de C_t, o módulo forma W=Λ₊⁻¹ᐟ² V₊ᵀ, usa SVD de W X_t e exige posto completo dos 63 nuisance. Denotando Q a base ortonormal obtida, R_A=(I−QQᵀ) W A_t e I₂=R_AᵀR_A. Isso equivale ao complemento de Schur

P=C_t⁺−C_t⁺ X_t (X_tᵀ C_t⁺ X_t)⁻¹ X_tᵀ C_t⁺,
I₂=A_tᵀ P A_t,

sob o suporte e o posto exigidos pelo módulo. A verificação de suporte é aplicada tanto a X_t como às duas respostas. A pseudoinversa é a do suporte numérico com cortes congelados; não existe inversão de C_t completa por esse caminho.

A mesma medida plana de nuisance é usada para ambas as respostas. O normalizador do módulo depende de C_t e X_t, sem vetor observado; response_information não chama log_integral nem evaluate. A medida plana não fornece por si só evidência bayesiana absoluta ou prior de modelos. Um futuro cálculo de evidência requer seu contrato próprio, suporte/medida coerentes e priors apropriados; nenhum foi realizado aqui.

## Rótulos e limites dos números

[REAL — números lidos, não recalculados] O resultado registra postos racionais X=63, [X,a_h]=64, [X,a_h,c_C]=65, posto C=190, nulidade 72 e normas de suporte abaixo de 1e−10 nas duas variantes. A revisão verifica esses registros contra o protocolo e os recibos; não os recomputa e não regenera os hashes internos das matrizes C.

A expressão dos erros conjuntos no worker é sqrt(diag(I₂⁻¹)); portanto considera as duas respostas livres após projeção nuisance. A expressão 1/sqrt(diag(I₂)) aparece em campo separado com a outra resposta fixa. A nota distingue corretamente essas duas quantidades e preserva a ordem de parâmetros (h em dex, δ_C em mag). Os autovalores dependem das coordenadas/unidades, como declarado.

Os erros ideais conjuntos registrados são (0,0063924310863533815 dex; 0,027783801660828767 mag) no SBF upstream e (0,006410181061613873 dex; 0,02781279748786292 mag) no acréscimo independente e(M110). São condicionais à matriz, à rede parcial e às hipóteses adotadas. Não são erro de H0 observado, ajuste posterior, significância global, poder ou detecção. A segunda variante é sensibilidade condicional, sem adoção de uma decomposição física de erros.

## Conclusão restrita

O instrumento está coerente com o preflight parcial por erros especificado. Permanecem abertos o tratamento dos cinco MM, a covariância física residual/completa e as decisões científicas da rede integral. Próximo passo admissível: a coordenação pode usar esta revisão para preparar contratos e separar pendências; nenhuma nova execução é concedida pelo parecer. Não houve leitura de centros y/b, dados D, cálculo de H0 observado, S/g ou lnB, chamada remota ou mudança de código/pacote. O controle de inicialização sintética P3 continua apenas preparado e sem execução.

Correção local do revisor: a primeira auditoria passou 101/102 controles; o controle restante exigia tipo JSON numérico, mas as 82 variâncias upstream são strings decimais. O worker já as converte explicitamente por float. O revisor corrigiu apenas seu teste para a conversão finita e positiva correspondente. Recibo inicial e backup de bytes do script foram preservados; nenhum pacote científico foi alterado ou executado por esta correção.
