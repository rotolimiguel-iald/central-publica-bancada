# Memória — JAGB

## 05/10/2026 — H0DN/JAGB: seleção ampliada e compartilhamento de dados

[INPUT] Unidade documental solicitada pela coordenação para completar TRGB/JAGB no contrato do discriminante, sem fits, centros observados para inferência, upstream ou chamadas remotas.

[REAL — metadados] Variante H0DN V01 confirmada em variants.ini:6-7 e IDL vars.pro:68-80: retira apenas exclusão JAGB. Seleção de nomes/filtros/matching reimplementada localmente: hosts166→178, referências12→14,53hospedeiras nas duas; preservadas55linhas SN,14SBF,13grupos. JAGB adiciona12registros (7CCHP+5SH0ES) em11hosts, todos também Ceph/TRGB, âncora N4258. N5643 aparece nas duas fontes. Os13IDs SN associados já eram compartilhados. Fluxo277linhas/238nomes preservado; desigualdade de nomes não comprova independência sistemática.

[DERIVED/OPEN] Coluna candidata c_C por row_id,119entradas1 entre178hosts, representa viés positivo no módulo publicado Cefeida. Propagação no sistema comum: dxhat/dδ_C=−(AᵀC⁺A)^−1 AᵀC⁺c_C, sob consistência do suporte e identificabilidade. Coeficiente NÃO calculado nem C global montada. Código quantifica âncora/MAS/HMS, não todos os termos residuais cruzados entre métodos/fontes; ausência permanece não quantificada, jamais independência presumida. Candidato exige fontes ou análise PSD de sensibilidade e ratificação do contrato. H0DN V01 não é V1 do nosso pré-registro.

Relatório `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\h0dn_documentary_review\jagb_extension\ENTREGA_JAGB.md`, SHA256 a094da87d6b03b2647b441a90460c1840c58edcc78b7a7f3044ed65fbffd2376; SOURCES.json + SELECTION_V01_IDENTIFIERS.json + CEPHEID_RESPONSE_CANDIDATE.json + CONTRATO_JAGB_CANDIDATO.json + MANIFESTO_ENTREGA.json. Sete novas fontes públicas,31verificadas no conjunto. Mapa seq421. Sem inferência/veredito novo, upstream, chamadas pagas/remotas, alterações do pré-registro, runtime, originais, kernel ou gate.


<!-- ORDEM018_F1_RESIDUAL_PSD_54FEB986 -->
## 05/10/2026 23:26 — ORDEM018 F1: covariâncias residuais concretas

[INPUT — resumo da delegação] Coordenação pediu qualificar N4258, JAGB CCHP/SH0ES e as 11 hospedeiras de V01; duas alternativas e família PSD caso não houvesse matriz publicada, sem centros para ajuste, S/g/H0/lnB, upstream ou novos modelos remotos. Request `54feb986-d927-4ff9-aa69-3c07680ee78b`.

[REAL] Cinco fontes primárias HTML arquivadas com SHA/linhas derivadas. 47 caminhos/hash conferidos; seis artefatos JAGB anteriores intactos. Auditoria somente de erros/identificadores: 178 equações, 104 HMS, erros exatamente iguais dentro de cada HMS, nenhuma referência MAS ausente. A distância geométrica N4258 (0,032 mag) já é comum; MAS JAGB de cada fonte (0,05 mag) são termos separados. N5643 tem campos e estrelas sobrepostos documentados. Matriz residual conjunta não localizada no recorte lido, sem afirmar ausência universal.

[DERIVED] Família C=D0+C_anchor+B Dm Rm Dm B.T+H Dh Rh Dh H.T: R PSD com diagonal 1 preserva marginais. Misturas convexas de blocos assinados definem grupos concretos; grade interior R>=I/4 preserva o núcleo do C baseline. É prova algébrica de admissibilidade, não medição da correlação física. D0=0 nesta seleção de erros. Alternativa A reconstrói componentes/jacobiano/reamostragem conjunta; alternativa B usa envelope PSD pré-especificado. Não somar erros agregados novamente; efeitos cruzados entre níveis MAS/HMS exigem realocação com resposta host−âncora.

[OPEN] Escolher e congelar alternativa, grupos, sinais e regra de robustez no contrato científico da coordenação, sem escolher pelo resultado. Reutilizar o guard de suporte já entregue; não criar camada repetida. Nenhum novo ajuste, C global, S, g, H0, lnB, sigma ou veredito foi calculado. Fontes contêm tabelas observadas; não alegar cegamento. Executor MiMo com âncora bloqueada preservado, nenhuma nova chamada. Originais/kernel/gate intactos.

Relatório: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\h0dn_documentary_review\jagb_extension\residual_systematics\REVISAO_RESIDUAIS.md`; SHA256 `9d91a8435d099146c3a6c402718fe974ffa46e1faa360c1af9fe93b78fe11eb7`. Contrato: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\h0dn_documentary_review\jagb_extension\residual_systematics\CONTRATO_PSD_CANDIDATO.json`. Manifesto: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\h0dn_documentary_review\jagb_extension\residual_systematics\MANIFESTO_ENTREGA.json`; SHA256 `e9bdc7d5e428225b6d9d55c9d385af06beb5dd1c7410ee5e3f2f1930512e809f`. Mapa antes consultado; ANOTACAO posterior **seq 435**, rota `hubble.fase9_razao_discriminante`. Estatuto da rota segue EM_CURSO.

