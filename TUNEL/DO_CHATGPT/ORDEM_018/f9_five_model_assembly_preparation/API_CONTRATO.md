# Montagem pura F9: cinco médias e um desenho nuisance comum

[REAL — fonte preparada e inspeção estática] Unidade `8e017d91-f3bb-4ec6-9236-5b2c327d1b98`. O arquivo `five_model_assembly.py` contém a montagem aritmética, sem solver novo. Não foi importado, chamado ou testado numericamente nesta unidade. O recibo documental distingue parsing AST de execução. A leitura das fontes não qualifica um resultado cosmológico.

## API e separação de responsabilidades

`assemble_five(model_parameters, *, design_json, layout_json, background_json, admission_json, admission_sha256)` recebe somente objetos em memória. Os quatro argumentos `_json` são bytes UTF-8; o último é o SHA-256 do documento de admissão congelado por uma instância externa. A biblioteca não lê discos, importa o motor, inicia processos ou consulta provedores. Não contém observações ou realiza ajuste.

O chamador fornece as cinco chaves `H1_TGL`, `H2_LCDM`, `H3_beta_free`, `H4_Cepheid`, `H5_rd_free`. Cada valor contém `H0`, `ombh2`, `omch2`; H3 acrescenta `beta`, H4 acrescenta `s`, H5 acrescenta `rd_Mpc`. Chaves extras são erro. Os cinco fundos têm o mesmo theta nesta chamada para compartilhar uma avaliação do motor. Ajustadores distintos podem chamar o adaptador em pontos theta distintos; **não há imposição de igual melhor ajuste entre modelos**.

Domínios fechados: H0[50,90] km/s/Mpc; ombh2[0,015;0,030]; omch2[0,08;0,18]; beta diagnóstico[−0,05;0,05]; s[−0,15;0,15]; rd[130,160] Mpc. São os priors candidatos do resolutor, não novas decisões físicas. O retorno conserva as coordenadas originais e as densidades racionais; não integra priors ou likelihoods.

## Fórmulas ligadas às fontes

Se I=(2/3)ln E_standard(1089,95;theta) e h0=log10(H0/(km/s/Mpc)):

| Hipótese | h local (dex) | delta_C (mag) | Denominador BAO |
|---|---|---|---|
| H1 | h0+I beta_TGL/ln10 | 0 | rdrag CAMB |
| H2 | h0 | 0 | rdrag CAMB |
| H3 | h0+I beta/ln10 | 0 | rdrag CAMB |
| H4 | h0 | −5log10(1+s) | rdrag CAMB |
| H5 | h0 | 0 | rd livre |

beta_TGL é calculado por `alpha_value * math.sqrt(math.e)` a cada chamada. Seu valor decimal não é congelado como beta. A constante `ALPHA_FINE_CODATA_2018` deve provir do layout estrutural pinado descrito abaixo, nunca de um ajuste. `math.log1p(s)` implementa a mesma transformação de H4 sem subtrair números próximos. **O prior de H4 continua uniforme em s**, não em delta_C. H5 continua uniforme em rd, não em q. A lA injetada foi calculada com rstar padrão pelo motor; H5 não a recalcula com rd livre.

O resultado do motor é reutilizado: `R`, `lA`, `E_law`, `I_law`, `rdrag_Mpc`, `rstar_Mpc` e distâncias de `low_z`. Não se refaz CAMB, recombinação, integral de distância ou fórmula de maser. A terceira coordenada CMB é ombh2 do mesmo theta. As três coordenadas CMB seguem **a ordem do layout admitido**, e não uma ordem suposta nesta biblioteca.

Fonte do resultado: `background_controls.py:130–186`, em especial 155–170 e 177–184; priors/configuração: `PROTOCOL.json`; fórmulas H1–H5: `RESOLUTOR_F9.json:resolved_contract.models/definitions/physical_priors`; unidades: `resolved_contract.units`. A especificação local já contém as cinco linhas de masers e não é reconstruída a partir de seus centros.

## Desenho local, ordem e unidades

`design_json` deve ser a cópia exata dos bytes de `ESPECIFICACAO_LINEAR.json` pinados. Reaproveitam-se suas 267 linhas, 63 colunas eta e coeficientes racionais. Os row_ids e a ordem de eta não são inferidos de nomes de arquivos. Não se avalia eta, não se integra eta e não se duplica intercepto ou calibração como parâmetro cosmológico.

O vetor completo contém 16 componentes de fundo seguidos pelas 267 linhas locais. A média local é `a_h*h + c_C*delta_C`; X eta fica separado, com 16 linhas nulas de X no fundo. No desenho nativo, a_h atua somente nas sete linhas SN_HF/SBF_HF/megamaser e c_C nas 119 linhas Cefeida já identificadas. O modelo H4 não desloca todas as 267 linhas nem SN/SBF novamente.

Segue-se a convenção all-magnitude do resolutor: sete linhas dex multiplicadas por 5; as outras 260 mantidas. O mesmo fator multiplica X, a_h e c_C. Os coeficientes de X e das duas colunas ficam como **strings racionais exatas**, inclusive `-1/5` convertido em `-1` nos interceptos. As previsões são floats de engenharia. Nuisance conserva sua medida comum em magnitudes, sem reparametrizar suas 63 coordenadas.

O retorno inclui `native_to_output_row_scale`, `row_units`, `row_ids`, X esparsa e as colunas de resposta. O consumidor tem de usar **y_out=T y_native e C_out=T C_native T^T**. Este adaptador não recebe y ou C e não pode certificar que outro consumidor aplicou a transformação. Essa obrigação não é satisfeita apenas por uma frase no JSON; deverá ser conferida na integração posterior com a likelihood. Vínculos determinísticos, rank e suporte também pertencem à integração posterior. Não foi recalculado rank nesta unidade.

## Layout existente recebido e consumido diretamente

A coordenação entregou `f9_structural_layout_preparation/LAYOUT_ESTRUTURAL_3CMB_13BAO.json` sob manifesto conferido. A API recebe **os próprios bytes desse arquivo em layout_json**, sem segunda extração e sem criar um formato paralelo para alpha. Schema F9_BACKGROUND_STRUCTURAL_LAYOUT_V1; status STRUCTURAL_PROJECTION_NO_OBSERVED_CENTRES. O hash fica materializado em SOURCE_PINS junto às cinco fontes originais da montagem.

O arquivo contém 16 components, primeiro R/l_A/omega_b_h2, depois as13BAO. O código apenas mapeia os nomes do manifesto para campos do motor: l_A→lA, omega_b_h2→ombh2 e *_over_rdrag→*_over_rd. Não troca rdrag por rstar. Os IDs derivados para a API são `source_path:Lsource_line#observable`, usando valores do próprio manifesto; o sufixo distingue as três expressões CMB presentes na mesma linha101. São chaves de referência geradas, não identificadores novos de objetos observados.

A ordem BAO é DV em0,295; DM/DH em0,510;0,706;0,934;1,321;1,484; e DH/DM em2,33. Os tokens decimais preservados na fonte são convertidos para float somente ao usar a API. Nesta preparação não se chamou a conversão do candidato. O z_lei1089,95 permanece separado de zstar/zdrag térmicos. O mesmo SHA do layout protege a estrutura de ordem, os metadados de redshift e a origem alpha.

Alpha vem de `alpha.decimal_token` dentro desse arquivo, com símbolo ALPHA_FINE_CODATA_2018, origem pinada e source_line25. A coordenação/extrator conferiu a declaração no pipeline histórico e o token no T4. Nesta unidade se conferiram o manifesto e seus três artefatos por bytes/hash; **os originais observados e a fonte externa alpha não foram reabertos**. A proveniência transcrita do extrator conserva essa distinção. O candidato converte esse token e calcula alpha*sqrt(e) em runtime; não contém beta decimal.

## Admissão estrutural e resultado injetado

`admission_json` contém exatamente schema F9_ASSEMBLY_ADMISSION_V1, status ENGINEERING_STRUCTURAL_ADMISSION, layout_sha256, sources, engine_configuration_sha256, runtime_sha256. Sources deve ser exatamente SOURCE_PINS materializado na biblioteca por bytes verificados (resolutor, layout, desenho, engine, protocolo, contratoMM).

Os pins de engine/protocolo identificam **a implementação e o protocolo de origem**. `engine_configuration_sha256` identifica separadamente a configuração efetiva da avaliação: theta, grade, perfil e parâmetros efetivos devem estar registrados em recibo associado; mudanças físicas precisam de outra revisão. O protocolo original tem seis redshifts de controle e cinco pontos theta; ele não é declarado uma execução geral nos redshifts BAO. Não rotular configuração modificada como os bytes do protocolo original.

`runtime_sha256` identifica o manifesto de runtime; `execution_receipt_sha256`, exigido no pacote de previsão, identifica a avaliação efetiva. A biblioteca compara pins e mantém sua proveniência. **A verificação do conteúdo desses artefatos compete ao chamador/revisor de integração**. O SHA da admissão recebido pelo argumento vem do registro confiável do supervisor; recebê-lo do próprio pacote seria autodeclaração circular. Não se criou uma admissão preenchida para fingir que uma avaliação geral do motor já existe.

`background_json` contém exatamente schema F9_BACKGROUND_PACKET_V1, status ENGINEERING_RESULT, identity, result e error null. Result é a estrutura existente do motor, incluindo physics_status STANDARD_BACKGROUND_THEORY_CONTROL_NOT_OBSERVATION. Metadados adicionais próprios de result permanecem protegidos pelo hash do pacote. Erro upstream interrompe a montagem e deve ser preservado pelo chamador.

Identity contém exatamente engine_sha256, protocol_sha256, engine_configuration_sha256, runtime_sha256, theta (lista de três coordenadas), z_law (1089,95), units e execution_receipt_sha256. O contrato units está declarado literalmente como BACKGROUND_UNITS na biblioteca: theta em km/s/Mpc,1,1; R/lA/E_law/I_law/z_law adimensionais; rstar/rdrag emMpc; low_z com z adimensional e DM/DH/DV emMpc.

Low_z precisa conter as distâncias nos redshifts **exatos do layout**, sem aproximação ao vizinho nem interpolação nova. A tolerância relativa1e-12/absoluta1e-14 compara apenas I_law recebido com (2/3)lnE_law: coerência aritmética de engenharia, não cota teórica uniforme ou alteração de um limiar científico.

## Retorno, falhas e certificação

Retorno: schema F9_FIVE_MODEL_PREDICTIONS_V1, status ENGINEERING_ONLY, cinco vetores mean_without_nuisance de comprimento283, uma matriz esparsa X com283linhas/63colunas declaradas, unidades/ordem/transformação, coeficientes e proveniência.

AssemblyError conserva code/detail. Ausência de entrada, JSON duplicado, pin diferente, parâmetros fora do domínio, theta incompatível, redshift faltante ou resultado upstream falho interrompem a montagem. Não se retorna vetor zero, likelihood zero, recorte do prior ou hipótese parcialmente completada. O supervisor deve conservar também o pacote upstream para sua causa detalhada; o adaptador não imprime o conteúdo de exceções remotas.

Por construção toda saída contém `certified=false`, `uniform_error_bound=null`, `numerical_certificate=null`, status UNBOUNDED_THEORY_ERROR; chi2/p/sigma/lnB null. Um certificado fornecido como flag não é aceito como substituto. Os valores de engenharia permanecem disponíveis para a análise quando as entradas estão presentes. A falta de cota teórica uniforme **não invalida sua utilidade de engenharia**, mas impede promovê-los a mínimos globais certificados ou a significância calibrada. Interfaces de certificação numérica já existentes não são reimplementadas aqui.

## Lacunas exatas e menor revisão seguinte

1. **Resolvido nesta preparação:** layout3+13, redshifts/ordem e origem alpha recebidos da coordenação e pinados, consumidos diretamente pelo candidato. As lacunas documentais iniciais não permanecem abertas.
2. **Ainda não materializado:** o envelope/admissão com configuração efetiva, runtime e recibo de uma avaliação nos redshiftsBAO exatos. O motor existente ainda está documentado no piloto de seis redshifts de controle; o adaptador não fabrica as sete distâncias de levantamento.
3. **Fora desta unidade:** revisão/execução da montagem, acoplamento à covariância e qualificação de erro. Não se exigem novos teoremas para preencher o layout recebido; esses são trabalhos de integração e validação de implementação.

A próxima ação mínima é **uma revisão estática de integração**: layout/alpha recebidos e pinados, mapeamento do envelope para o result existente, ordem/unidades contra o consumidor e inspeção da fonte preparada. Não é pedido de nova execução, controles, abertura dos dados ou orçamento. Eventuais ensaios posteriores deverão ter unidade própria; não se repetem CAMB/C01–C08/tail/guard/INIT003/4f5d nesta entrega.

## Alternativas examinadas

A — adaptador puro sobre resultado injetado (selecionada): reutiliza o cálculo do motor, mantém formas físicas e permite cache do mesmo fundo nas cinco hipóteses. O custo é explicitar o envelope de proveniência e fechar o layout antes da montagem concreta.

B — nova implementação que chama solver a partir do montador (não selecionada): mistura cálculo, execução e leitura; repete funções existentes e torna a revisão de falhas/consumo mais difícil. Não é necessária para montar médias.

C — injetar callback de avaliador (adiada): permitiria consumo sob demanda, mas adiciona uma chamada de efeito externo à API. O chamador pode realizar essa função fora do adaptador e entregar o mesmo resultado pinado. A alternativa passiva satisfaz a preparação atual com menor superfície de execução.

Não foram alterados um.py, modelos, priors, V1, §6, kernel, gate, acervos canônicos ou memórias compartilhadas. Esta ligação implementa o candidato restrito R-A; não afirma que todo o modelo cosmológico TGL foi executado nem que houve resultado5sigma.
