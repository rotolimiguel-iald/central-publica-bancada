# Conexões existentes — verificação de 19/09/2026

[REAL — compilação de adaptadores] `ConexoesExistentes.lean` compilou com Lean 4.31.0, retorno 0. As 90 fontes locais da dependência transitiva no cache usado foram comparadas com as extraídas da v368, com igualdade de texto após normalização de fins de linha e espaços externos. Os hashes de ambos os lados estão em resultado.json. Usaram-se dependências previamente compiladas; não foi recompilado o kernel inteiro.

## Encaixes confirmados

| Fornecedor existente | Consumidor | Resultado desta rodada |
|---|---|---|
| `qgStrongCertificate_frame.1` | `SmoothFrameData` | aceita diretamente |
| `qgStrongCertificate_frame.2` | não constância do mesmo frame | aceita diretamente |
| `existingSmoothFrame.det_unit x` | `four_frame_gives_lorentz_metric` | coframe dual e métrica lorentziana em cada ponto |
| `theHorizon` | `HorizonEquilibriumData` | aceita diretamente |
| `the_master_fires.2.2.2` | coeficiente térmico do mesmo horizonte | aceita diretamente |

Os três teoremas-adaptadores consultados por `#print axioms` retornaram somente `propext`, `Classical.choice`, `Quot.sound`. São reaproveitamento de provas existentes, não novas derivações físicas. A presença da tríade construída foi confirmada também pelo tipo de `the_master_fires` impresso pelo Lean.

## Controle que recusou a troca de contrato

`ControleContrato.lean` tentou fornecer `towerEquilibriumInput 1 ... 1` diretamente a `HorizonEquilibriumData`. O Lean retornou código 1 com `Type mismatch` entre:

- `EquilibriumInput (Matrix (chainIdx 1) (chainIdx 1) ℂ)`;
- `HorizonEquilibriumData`.

O primeiro objeto contém fluxo, estado, unidade preservada e relação KMS. O segundo contém kappa, G positivo, variações de área/entropia/calor e suas relações. A recusa demonstra que essa substituição direta não funciona; não demonstra impossibilidade de um adaptador nem ausência dele no restante do acervo.

## Onde os leitores se separam

Os nomes `qgPrice_H2_smoothModularFourFrame_discharged`, `qgPrice_H3_localHorizonEquilibrium_discharged` e `qgImport_H3_horizonEquilibriumData_produced` não foram localizados nas fontes TGL/TGLExt extraídas da v368, nem por busca literal. Seus nomes constam nos mapas Python. O leitor em torno da linha 134824 procura presença no relatório de axiomas e ausência de axiomas proibidos.

Esse leitor, isoladamente, NÃO estabelece um tipo esperado para o termo reservado. Logo, não é seguro ocupar esses nomes com qualquer fato verdadeiro apenas para mudar a bandeira. Também não é correto inferir da ausência desses nomes que inexiste frame ou horizonte: os fornecedores da tabela acima estão compilados e presentes.

O contrato efetivamente pago por esta rodada é explícito: frame suave não constante, coframe dual e Lorentz em cada ponto; horizonte concreto e seu coeficiente térmico. A identificação de todos esses dados com uma realização física comum não está incluída na assinatura desses adaptadores. Não foi declarada inexistente; sua rota deve ser localizada e comparada separadamente.

## Preparação, Einstein e colagem já localizados

`ChatgptAudit.UnifiedRecorded.unified_einstein_from_area` já chama `record_einstein_from_area` e usa `unified_area_matching_iff`: conserva explicitamente `hd` (divergência da fonte) e `harea` (compatibilidade de área), além dos dados de região e telas.

`ChatgptAudit.SmoothAtlasGluing.connected_smooth_atlas_einstein` já consome `AreaChart`, cobertura e transições, encaminhando `transition_supplies_tensor_match` ao teorema de colagem. Essas conexões já estão escritas; não precisam de um novo wrapper equivalente. A próxima consulta deve perseguir os produtores das instâncias e argumentos concretos.

## Decisão de implementação

Nenhum original ou gate foi alterado. Os adaptadores são instrumentos de auditoria, sem novos nomes reservados. Não foi criado outro reconhecedor. Antes de qualquer mudança de leitor, fixar o contrato que ele pretende medir e comparar esse contrato com os fornecedores existentes; conservar em separado o que já está ligado e o que depende de instâncias adicionais.

Arquivos: `../ConexoesExistentes.lean`, `../ControleContrato.lean`, `resultado.json`, `ConexoesExistentes.txt`, `ControleContrato.txt`.
