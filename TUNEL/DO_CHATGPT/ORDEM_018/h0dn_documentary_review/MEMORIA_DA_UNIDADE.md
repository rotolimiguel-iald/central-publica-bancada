# Memória da unidade — revisão H0DN

## 05/10/2026 — ORDEM018: rede H0DN e identificação por método

[INPUT] Coordenação pediu revisão pública H0DN/ACT/CMB-S4 sem novos ajustes, modelos ou alteração do V1. [REAL] Fontes H0DN fixadas em cc0a4b9f36e65470d514f254a3c5cffa463fbd94, 24 arquivos verificados por blob Git; código apenas lido. Matriz SN fornecida 277x277 finita, simétrica, diagonal positiva; não confundir com C da rede, gerada por seleção. Localizados 20 hosts Ceph/TRGB antes do matching final de calibradores; seleção preliminar, não número de medidas independentes. Nenhum espectro/rank de C global ou resultado de ajuste reproduzido.

[DERIVED] Extensão da revisão SPD anterior: C singular exige consistência do suporte além da pseudoinversa. Deslocamento universal é absorvido por H0 livre; comparação requer âncora independente ou outra previsão. Viés diferencial Cefeida deve ser definido nas distâncias e propagado; não é qualquer offset fotométrico comum. H0DN e seus componentes/variantes são dependentes. A insuficiência do H0 comprimido para testar efeito de método aponta o uso da rede completa.

[KNOWN — fontes primárias lidas] ACT v2 distingue P-ACT-LB sigma .13, D-He .11 e DR2 .12, com sobreposição e hipóteses diferentes; não somar. Site CMB-S4 informa retirada DOE/NSF em 09/07/2025 e encerramento organizado, invalidando cronograma antigo. Nenhuma previsão de poder foi recalculada.

Relatório: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\h0dn_documentary_review\REVISAO_H0DN_ACT.md`; SHA256 88f804c6ac00242fa3fd0d0d39c6bb9310a8c07d00b9de743ced392ab7f4af96. Recibos: UPSTREAM_MANIFEST.json, STRUCTURE_AUDIT.json, MANIFESTO_ENTREGA.json. Mapa: anotação seq399 em hubble.fase9_razao_discriminante. V1 composto continua a cargo da coordenação, a ratificar antes de executar. Sem chamada a modelo, fit, veredito novo, alteração de interface/runtime, originais, kernel ou gate.


<!-- ORDEM018_JAGB_METADATA_20261005_a094da87d6b0 -->
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



<!-- ORDEM018_F1_LINEAR_DESIGN_EC4872EC -->
## 05/10/2026 23:49 — Projeto linear V01 e medida nuisance F1/F9

[INPUT — delegação delimitada] Unidade ec4872ec-82f0-4236-a76c-1e10f89aefe5, solicitada pela coordenação 01a0ce2b-8c2f-71b0-a9a8-91b17715a569: explicitar X, h, nuisance e desvio Cefeida, vínculos por âncora e medida comum aos cinco modelos. Sem centros novos, ajuste, S/g/H0/lnB, upstream, D ou modelos remotos.

[REAL documental / DERIVED] Projeto esparso por chaves:267linhas; eta63=(59hospedeiras,2grupos,MB,M110offset), h64ªcoluna. As53hospedeiras anteriores eram as medidas diretamente; seis extras entram pelos grupos. a_h=1 em7linhas de fluxo; c_C=1 em119linhas Cefeida, conferido com candidato anterior. 104HMS,11MAS ativos,14referências disponíveis (três inativas),9componentes. Componente R22 tem37hosts×3âncoras:72ciclos independentes, posto de incidência106 no bloco inteiro. Verificadas identidades exatas LX=La_h=Lc_C=0; Ly permanece não examinado. X pleno63 por conectividade; [X,h]64 e [X,h,c_C]65 por testemunhas estruturais. Nenhuma covariância numérica montada.

[DERIVED condicional] Entregues opções de prior próprio (gaussiano ou domínio uniforme finito) e razão plana com mesma medida em R^63; explicitadas normalizações, suporte, jacobianos e condições de cancelamento. Determinantes dependentes de lambda/theta não saem automaticamente das integrais. Parâmetros específicos beta livre/delta_C/r_drag precisam de priors próprios. Âncora/MAS/HMS já em C não duplicados como nuisance. Compressão cinemática q0/j0 fixa do upstream deve ser preservada no recorte ou requalificada com a normalização completa.

[REAL — custódia] Falha inicial detectou pin antigo do candidato V1. Dono resolveu apontando para backup com hash original; snapshot e nota conferidos, sem repin de conteúdo novo e sem repetir análise. 13artefatos da entrega verificados por hash/tamanho. Relatório `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\h0dn_documentary_review\linear_design\PROJETO_LINEAR_E_MEDIDA.md`; SHA256 `66616993e30427b41b7fb3c64caef71a2cc444e7cf61b890ca25c14ffbda13dc`. Manifesto `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\h0dn_documentary_review\linear_design\MANIFESTO_ENTREGA.json`; SHA256 `04cc8b0a45b63cb64f034c9c004bb681c1d6750305c2a5cb146fe294d3b24343`. Mapa antes438, registro posterior444.

[OPEN] Revisão independente, escolha da medida nuisance e contrato físico/V1 continuam com a coordenação. Não há nova evidência observada, sigma, ajuste ou mudança de gate. Reutilizar guard de suporte e seleção existentes; não criar camada de física repetida. Provedores bloqueados e suspensões preservados.

