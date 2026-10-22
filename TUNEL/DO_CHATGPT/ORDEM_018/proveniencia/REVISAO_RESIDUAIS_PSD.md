# ORDEM_018 — revisão independente dos residuais e da família PSD

**Aceite limitado, sem achado matemático ou de correspondência que exija correção no pacote revisto.** A família é uma escolha de sensibilidade admissível, ainda não ratificada; não é estimativa das correlações físicas, demonstração de independência dos indicadores ou autorização de V1. O incidente de acesso descrito ao final integra o parecer.

[REAL documental] Unidade da gerência request_id 54feb986-d927-4ff9-aa69-3c07680ee78b, mapa consultado seq435; complemento da coordenação consultado seq439. Foram conferidos REVISAO_RESIDUAIS.md, CONTRATO_PSD_CANDIDATO.json, erros/identificadores, manifestos e código pertinente em modo leitura. Os scripts do autor e o upstream não foram executados pelo revisor.

## Conferências e prova

A auditoria independente de custódia conferiu os 47 caminhos herdados declarados e 58 caminhos pinados no recorte documental completo, incluindo os oito artefatos da entrega e as seis peças anteriores JAGB. Conferiu os pins da seq435. As 178 linhas selecionadas correspondem a 14 referências MAS e 104 primitivas HMS. Cada identidade foi comparada com os campos host/method/anchor/source da linha original, e somente a coluna de erro foi convertida. Os grupos propostos contêm 48 chaves HMS disjuntas nas 11 hospedeiras; os pares JAGB e os dois grupos MAS de três métodos existem com os nomes e erros indicados. As 12 linhas JAGB e o par N5643 conferem.

[REAL] Os erros são exatamente iguais dentro de cada HMS: D₀,ii=sᵢ²−h(HMSᵢ)²=0 nesta seleção. Isso justifica a transcrição particular do baseline. Não é uma regra geral que permita eliminar D₀ em outro conjunto; D₀ negativo deve falhar, não ser corrigido por clipping.

[DERIVED, condicional] Para os fatores A, B e H da nota, a soma

C(θ)=D₀+A diag(a²)Aᵀ+B DₘRₘDₘBᵀ+H DₕRₕDₕHᵀ

é PSD quando D₀≥0 e Rₘ,Rₕ são PSD. Cada E é uma soma direta de blocos εεᵀ e identidades: PSD e diagonal unitária. Grupos de diferentes componentes podem se sobrepor; a soma convexa dos componentes continua PSD, sem exigir compatibilidade par a par fora dessa construção.

Cada linha tem exatamente uma chave MAS e uma HMS. Logo a diagonal de C é D₀,ii+aᵢ²+mᵢ²+hᵢ²=sᵢ²+aᵢ²+mᵢ². A repetição do mesmo HMS compartilha a mesma variável primitiva, não um novo erro independente. Rₘ=Rₕ=I reproduz os termos de âncora/MAS/HMS do código equations.py:334–376, à luz dos erros desta seleção. O uso das chaves em data_loader.py:328–400 e 450–505 é consistente com a nota.

A grade foi conferida com frações exatas: são 100 tuplas ordenadas, três cenários de sinais, e 1−u−v,1−p−q≥1/4. Portanto Rₘ,Rₕ≥I/4. Mais precisamente, C(θ)≥C₀/4 e todo x∈ker C₀ anula cada fator primitivo que compõe C(θ). As duas inclusões dão ker C(θ)=ker C₀. Essa prova é sobre o bloco de erro definido; não assegura que os resíduos dos cinco modelos de média pertençam ao suporte afim. O guard existente continua necessário.

Os extremos com soma 1 podem perder o limite inferior e alterar o núcleo; é correta sua separação como diagnóstico. Uma dimensão igual do suporte, isoladamente, também não garante medida ou suporte afim comum em comparação de evidências.

[REAL] Os produtos de erros foram recalculados em Decimal: âncora N4258 0,001024 mag², referências JAGB cruzadas 0,0025 mag² e HMS JAGB cruzadas em N5643 0,00152 mag². São coeficientes multiplicando escolhas de correlação, não covariâncias medidas. Não se acrescentam outra vez 0,032, 0,05 ou a provisão metodológica 0,06 mag.

## Implementação estelar da coordenação

O protocolo STELLAR_FAMILY_PROTOCOL.json, o script qualify_stellar_family.py e o recibo STELLAR_FAMILY_RESULT.json foram lidos e pinados. A fonte só monta o bloco estelar a partir dos JSONs de erros/identificadores, usa o guard V2 já revisto e não lê os catálogos com centros. A omissão de D₀ é válida neste retrato, pela igualdade exata acima; não qualifica automaticamente outros erros.

Foi feito um controle independente restrito à correspondência entre grupos/sinais e os hashes primitivos emitidos: uma construção entrada a entrada, em quartos exatos e biblioteca padrão, sem NumPy, sem importar o autor e sem reconstruir C estelar ou global. Todos os 300 hashes Rₘ/Rₕ coincidiram; os 17 vínculos de duplicação e os 283 desenhos primitivos distintos conferem. “Desenhos primitivos distintos” não promete que o mapa para C seja injetivo, nem significa 283 evidências independentes.

[REAL documental do recibo; não reexecutado pelo revisor] A execução da coordenação registra posto 106/nulidade 72 para 178 linhas, erro de marginais zero, máximo desvio do projetor nulo 2,985347421800767e−13 e posto 106 nos três cortes relativos 1e−10/1e−12/1e−14. O erro da transcrição por pares é zero; duração registrada 1,4577025999315083 s. Esses valores foram conferidos no recibo e sua consistência estrutural, sem repetir a diagonalização. Não demonstram precisão de evidência, suporte da rede completa ou correlação física.

## Limites preservados

- [INPUT/OPEN] Grupos, sinais, pesos e regra de robustez continuam escolhas a congelar. Não otimizar pelos resíduos nem apresentar o cenário mais favorável como resultado único; marginalizar exigiria um prior e normalização declarados.
- [OPEN] A família exclui covariância primitiva MAS↔HMS. Um mecanismo comum pode cancelar parcialmente na diferença hospedeira−referência; precisa do jacobiano diferencial e realocação do orçamento da alternativa A. A alternativa B é limitada, sem exigir independência absoluta de tudo o que não modela.
- [OPEN documental] A divergência 0,03/0,02 mag para correção de abertura permanece exposta na nota da gerência. Esta revisão não escolheu um dos valores, não reescreveu os erros V01 e não fez reauditoria integral dos cinco artigos. Os HTML/TXT foram pinados; ausência de matriz publicada continua restrita ao recorte descrito pela gerência.
- [OPEN] V01 é variante de seleção upstream, não ratificação do pré-registro V1. Permanecem separadas a montagem global SN/rede/fundo, as cinco médias físicas, H5, priors e a regra final de evidência. Nenhum S, g, H0, likelihood, Bayes factor, ajuste, teste de natureza ou gate foi calculado/movido nesta revisão.

## Incidente de acesso do revisor

[REAL — falha de escopo registrada] Uma busca rg ampla por termos de erro nos dois TXT públicos JAGB retornou incidentalmente um parágrafo com módulos de distância e fragmentos numéricos de tabelas. Isso ultrapassou a intenção de não expor centros; a busca foi interrompida e a coordenação avisada imediatamente. Não alego cegamento. Nenhum centro foi convertido ou usado nos scripts, na escolha da grade, na construção de matrizes ou na conclusão. As verificações posteriores usaram os campos explicitamente permitidos e os recibos. Esse incidente não é evidência a favor ou contra uma hipótese física.

Custódia: REVISAO_RESIDUAIS_PSD.json contém as identidades, verificações e hashes; REVISAO_IMPLEMENTACAO_PSD_ESTELAR.json contém pins e a conferência dos 300 desenhos. Scripts próprios e protocolo do complemento ficam nesta pasta. Snapshots conservam a entrega original em residual_psd_snapshot. Fontes do autor preservadas.

