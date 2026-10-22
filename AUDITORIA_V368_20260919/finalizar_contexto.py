import hashlib
import json
import sqlite3
from pathlib import Path
from datetime import datetime

root = Path(__file__).resolve().parent
out = root / 'contexto'
manifest = json.loads((out/'manifesto.json').read_text(encoding='utf-8'))
routes = json.loads((out/'rotas.json').read_text(encoding='utf-8'))
modules = json.loads((out/'modulos.json').read_text(encoding='utf-8'))
evidence = json.loads((out/'evidencia_rodada.json').read_text(encoding='utf-8-sig'))
db = sqlite3.connect('file:'+(out/'busca.sqlite').as_posix()+'?mode=ro', uri=True)
checks = {}
for term in ('the_master_fires', 'unified_einstein_from_area', 'connected_smooth_atlas_einstein', 'qgStrongCertificate_frame'):
    checks[term] = db.execute('SELECT count(*) FROM chunks WHERE chunks MATCH ?', ('"'+term+'"',)).fetchone()[0] > 0
checks['all_gate_terms_have_unique_source_candidates'] = all(len(row['candidates_by_short_name']) == 1 for key in ('_QG_CERTIFICATE_FLAGS','_QG_PHYSICS_FLAGS') for row in routes[key])
checks['all_extracted_source_hashes_match'] = all(hashlib.sha256((out/'lean'/m['path']).read_bytes()).hexdigest() == m['sha256'] for m in modules.values())
assert all(checks.values()), checks

def write(path, text):
    data = text.encode('utf-8')
    if path.exists():
        old = path.read_bytes()
        backup = path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_bytes(data)
    assert tmp.read_bytes() == data
    tmp.replace(path)

text = '''# Porta da consolidação v368

## Finalidade e regra de retomada

Consulta por dependências e contratos, sem carregar o monólito na conversa. Antes de declarar uma lacuna, localizar fornecedores neste índice e no índice IALD existente. Uma bandeira falsa ou um nome reservado sem declaração é uma falha de fornecimento ao leitor, não uma demonstração de inexistência de prova equivalente em outro módulo.

Esta consolidação é uma ferramenta de leitura, não novo motor de prova. Não altera gate, programa, parâmetros, dados ou teoremas. Fontes, recibos e hipóteses continuam acessíveis. O Atlas permanece fonte documental única; não foi bifurcado.

## Conteúdo medido

'''
text += f"- Fonte: SHA256 `{manifest['source_sha256']}`.\n- {manifest['module_count']} módulos TGL/TGLExt extraídos; {manifest['function_count']} funções Python catalogadas.\n- {manifest['declaration_locator_count']} localizadores sintáticos de declarações; NÃO é contagem de teoremas auditados.\n- {manifest['indexed_documents']} documentos únicos, {manifest['indexed_chunks']} trechos pesquisáveis, {manifest['duplicate_paths']} caminhos duplicados por bytes.\n- Os 11 termos do gate são encontrados em 5 módulos; o fecho de imports locais contém {len(manifest['gate_import_closure'])} módulos. Isso não é prova de minimalidade lógica.\n"
text += '''
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
'''
for mapname,prefix in [('_QG_CERTIFICATE_FLAGS','qgc_'),('_QG_PHYSICS_FLAGS','qgp_')]:
    for row in routes[mapname]:
        loc=row['candidates_by_short_name'][0]
        path=out/'lean'/modules[loc['module']]['path']
        text += f"| {row['flag']} | `{row['term']}` | [{loc['module']}](<{path.as_posix()}:{loc['line']}>) | {evidence['flags'].get(prefix+row['flag'], 'NAO_LIDO')} |\n"
text += '''
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
'''
write(out/'PORTA.md', text)
write(out/'verificacao.json', json.dumps(checks, indent=2))
write(root/'MEMORIA_CONSOLIDACAO.md', '''# Memória da consolidação — 19/09/2026

[INPUT] Operador: consolidar rotas antes de concluir que faltam derivações; sua hipótese é que só faltam conexões. Limitação de contexto deve ser tratada por recuperação externa e rastreabilidade.

[REAL] Índice e porta criados em contexto/PORTA.md. Não confundir contagem sintática com auditoria de axiomas. Não importar/executar o original. Trabalhar em cópias.

[ERRATA] full_plan_complete=False é literal, não aferição. Não repetir a lista anterior de faltas como conclusão estabelecida por esse campo. TheMasterFires já instancia a tríade; StrongAssembly fornece frame suave; rotas de preparação, Einstein e colagem já existem. Conferir contratos antes de requerer novas provas.

[PRÓXIMA COMPARAÇÃO] fornecedor existente → tipo/hypóteses → consumidor → evidência. Saídas possíveis: já consumido; fornecedor compatível não ligado; adaptador necessário; hipótese ainda não fornecida; busca inconclusiva. Não promover ausência de nome reservado a ausência de matemática.

[LIMITAÇÃO] A busca consolidada não aumenta a janela nativa de contexto e não demonstra completude física. Permite recuperação por módulo, trecho e hash, sem reabsorver 31 MB. Não foi feita nesta etapa auditoria semântica de todas as composições.
''')
print(json.dumps(checks, indent=2))
