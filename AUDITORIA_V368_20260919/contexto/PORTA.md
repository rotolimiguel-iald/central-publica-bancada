# Porta da consolidação v368

## Finalidade e regra de retomada

Consulta por dependências e contratos, sem carregar o monólito na conversa. Antes de declarar uma lacuna, localizar fornecedores neste índice e no índice IALD existente. Uma bandeira falsa ou um nome reservado sem declaração é uma falha de fornecimento ao leitor, não uma demonstração de inexistência de prova equivalente em outro módulo.

Esta consolidação é uma ferramenta de leitura, não novo motor de prova. Não altera gate, programa, parâmetros, dados ou teoremas. Fontes, recibos e hipóteses continuam acessíveis. O Atlas permanece fonte documental única; não foi bifurcado.

## Conteúdo medido

- Fonte: SHA256 `4a34fbf36f3ae0d8bf56249d30bb1185cdee01767ec6e4f0a20433a4ac2d261e`.
- 1018 módulos TGL/TGLExt extraídos; 426 funções Python catalogadas.
- 11066 localizadores sintáticos de declarações; NÃO é contagem de teoremas auditados.
- 2956 documentos únicos, 9027 trechos pesquisáveis, 327 caminhos duplicados por bytes.
- Os 11 termos do gate são encontrados em 5 módulos; o fecho de imports locais contém 99 módulos. Isso não é prova de minimalidade lógica.

## Caminhos de consulta

- `rotas.json`: bandeira → termo consumido → módulo e linha candidatos.
- `modulos.json`: fonte, hash, imports e declarações por módulo.
- `funcoes.json`: função Python → linha, docstring e chamadas sintáticas.
- `evidencia_rodada.json`: valores de qgc/qgp/gpf/gpi lidos da rodada v368, com hash do JSON de origem.
- `lean/`: fontes extraídas integralmente da cópia v368, sem execução.
- `busca.sqlite`: pesquisa textual de fontes, funções e documentos da bancada.
- `manifesto.json`: cobertura, exclusões e hash da versão.

Execute `consultar_contexto.py search '"the_master_fires"'`, `consultar_contexto.py route H2` ou `consultar_contexto.py module UnifiedRecordedPreparation`, no diretório acima. Resultados de funções Python dão o início absoluto da função e a linha relativa do trecho; somar os dois menos um para obter a linha no monólito.

## Rota principal já ligada

| Bandeira | Termo | Fonte extraída | Valor da rodada |
|---|---|---|---|
| concrete_aqft_core_constructed | `TGLExt.qgStrongCertificate_core` | [TGLExt.StrongAssembly](<C:/IALD/Central de Patentes/Chatgpt/AUDITORIA_V368_20260919/contexto/lean/TGLExt/StrongAssembly.lean:127>) | True |
| concrete_breuer_corner_constructed | `TGLExt.qgStrongCertificate_corner` | [TGLExt.StrongAssembly](<C:/IALD/Central de Patentes/Chatgpt/AUDITORIA_V368_20260919/contexto/lean/TGLExt/StrongAssembly.lean:135>) | True |
| concrete_modular_four_frame_constructed | `TGLExt.qgStrongCertificate_frame` | [TGLExt.StrongAssembly](<C:/IALD/Central de Patentes/Chatgpt/AUDITORIA_V368_20260919/contexto/lean/TGLExt/StrongAssembly.lean:143>) | True |
| concrete_solder_field_constructed | `TGLExt.qgStrongCertificate_solder` | [TGLExt.SolderField](<C:/IALD/Central de Patentes/Chatgpt/AUDITORIA_V368_20260919/contexto/lean/TGLExt/SolderField.lean:155>) | True |
| concrete_emergent_einstein_proved | `TGLExt.qgStrongCertificate_einstein` | [TGLExt.EmergentEinstein](<C:/IALD/Central de Patentes/Chatgpt/AUDITORIA_V368_20260919/contexto/lean/TGLExt/EmergentEinstein.lean:340>) | True |
| canonical_boundary_transport_witness_constructed | `TGLExt.qgClosureCertificateV2` | [TGLExt.TheCoinage](<C:/IALD/Central de Patentes/Chatgpt/AUDITORIA_V368_20260919/contexto/lean/TGLExt/TheCoinage.lean:50>) | True |
| massless_spin2_proved | `TGLExt.qgPhysicsCertificate_massless` | [TGLExt.PhysicsCertificates](<C:/IALD/Central de Patentes/Chatgpt/AUDITORIA_V368_20260919/contexto/lean/TGLExt/PhysicsCertificates.lean:109>) | True |
| exactly_two_helicities_proved | `TGLExt.qgPhysicsCertificate_helicities` | [TGLExt.PhysicsCertificates](<C:/IALD/Central de Patentes/Chatgpt/AUDITORIA_V368_20260919/contexto/lean/TGLExt/PhysicsCertificates.lean:212>) | True |
| ghost_free_proved | `TGLExt.qgPhysicsCertificate_ghostfree` | [TGLExt.PhysicsCertificates](<C:/IALD/Central de Patentes/Chatgpt/AUDITORIA_V368_20260919/contexto/lean/TGLExt/PhysicsCertificates.lean:231>) | True |
| stress_energy_conserved | `TGLExt.qgPhysicsCertificate_conservation` | [TGLExt.PhysicsCertificates](<C:/IALD/Central de Patentes/Chatgpt/AUDITORIA_V368_20260919/contexto/lean/TGLExt/PhysicsCertificates.lean:259>) | True |
| relevant_anomalies_absent | `TGLExt.qgPhysicsCertificate_anomaly` | [TGLExt.PhysicsCertificates](<C:/IALD/Central de Patentes/Chatgpt/AUDITORIA_V368_20260919/contexto/lean/TGLExt/PhysicsCertificates.lean:292>) | True |

## Rotas recuperadas que não devem ser rederivadas

1. `TheMasterFires`: `ellTwoSusy` + `modularFrame` + `theHorizon` → `the_master_fires`. A tríade tem instância construída; não dizer simplesmente que H1/H2/H3 não existem. `theHorizon` especifica dados normalizados; conferir o contrato do destinatário antes de substituí-lo por outro horizonte.
2. `StrongAssembly` → `SolderField` → `EmergentEinstein` → gate. O frame suave não constante já é fornecedor do gate principal. Um consumidor geométrico adicional pode exigir mais; deve-se comparar os tipos, não recomeçar a construção de um frame.
3. `UnifiedRecordedPreparation` → `SelectedGravitationalAtlas` → `SmoothSelectedAtlasGluing`. A preparação, respostas e transporte de Einstein já estão formalizados. Área, conservação e compatibilidade de cartas aparecem nas assinaturas; procurar quem as fornece antes de chamar a rota de aberta.
4. `TheImportedEquilibrium`: a torre fornece `EquilibriumInput`; `the_trio_is_a_pair` compõe uma implicação fornecida. A rota existe, mas seu objeto deve ser comparado ao `HorizonEquilibriumData` exigido, sem composição de homônimos.
5. `UmPostoInscription` e `UmPostoRelacao`: leitura/injetividade/covariância/evento medido já existem. Não criar outro reconhecedor.
6. `TracialDissipativeTorsion`, `TorsionShearDecay`, `OrientedBoundaryFace`: ler os fornecedores atuais de torção, dinâmica condicional e orientação, não apenas comentários de versões antigas.

## Correção à auditoria anterior

`full_plan_complete=False` é um literal: não mede falta de provas. A auditoria de 13/09 já documentava esse risco. A leitura anterior do resultado foi fiel ao JSON, mas sua utilização como indício autônomo de pendência foi inadequada. O diagnóstico de pendências físicas permanece PROVISÓRIO até comparar fornecedores e consumidores nesta malha.

O programa distingue modelos e contratos: não está demonstrado por esta indexação que todas as interfaces físicas se compõem, nem que sejam impossíveis. A hipótese do operador — restam conexões — será testada por assinaturas, instâncias e compilação dos adaptadores que forem necessários, aproveitando as provas existentes.

## Limites de cobertura e testes

Imports Lean e chamadas Python são arestas sintáticas, não dependências lógicas completas. O parser de declarações é um localizador, não o elaborador Lean. Seis funções grandes tiveram seu corpo excluído da busca textual (nomes e chamadas preservados no catálogo); a lista está no manifesto. Bibliotecas de terceiros, material privado e backups foram excluídos. Os arquivos Lean externos à cópia não foram inventariados integralmente; os documentos da bancada permitem localizar suas entregas. Não foi reexecutado Lean nesta consolidação.

Seis verificações automáticas: hashes de todas as fontes extraídas, localização única dos 11 termos do gate e recuperação de quatro fornecedores conhecidos. Todas passaram. Não são testes de verdade física.
