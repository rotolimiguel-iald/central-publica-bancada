"""Record measured Antigravity readiness and preserve historical failures."""
from pathlib import Path
import hashlib
import json
from iald_orchestrator import antigravity
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
MARKER='IALD_ANTIGRAVITY_TEXT_EXECUTOR_READY_20260924'

def main():
    assert antigravity.connection_status()=='ready'
    receipt=json.loads(antigravity.RECEIPT.read_bytes())
    assert receipt['result']['text'].strip()=='42'
    runtime=Runtime(recover=False)
    preview=runtime.preview('Explicar hipotese e evidencia em fisica.')
    candidate=next(p for p in preview['candidates'] if p['id']=='gemini')
    assert candidate['status']=='ready' and candidate['eligible']
    comparison=json.loads((BASE/'validation/antigravity_capability_comparison.json').read_bytes())
    assert comparison['same_advertised_inventory']
    assert set(comparison['positive']['tool_events'])=={'view_file'}
    assert not comparison['negative']['tool_events']
    note=r'''

## 24/09/2026 — Antigravity integrado como executor textual disponível

<!-- IALD_ANTIGRAVITY_TEXT_EXECUTOR_READY_20260924 -->

[INPUT] O operador determinou corrigir e fazer funcionar a integração Antigravity.

[REAL — diagnóstico e correção] A autenticação já permitia respostas. O conector exigia init.tools=[]; o CLI anunciou a mesma lista de 57 ferramentas para dois agentes com capacidades distintas. No controle com view_file habilitado houve tentativa de ferramenta (a leitura do arquivo público foi NEGADA independentemente pela política headless); no controle sem ferramentas não houve evento de ferramenta e a resposta foi SEM_FERRAMENTAS. Não se afirma que a leitura do controle positivo foi concluída: o campo effective_tools_differ=false do relatório refere-se ao critério mais forte que exigia recuperar o conteúdo. A diferença de invocação foi observada.

[REAL — perfil final] Sincronizados os perfis global e locais iald-text, com tools=[], excludeDefaultComponents=true, inheritCustomizations=false, comandos off, sem MCP/skills/plugins/regras/hooks. A validação agora confere esses campos e a igualdade de bytes dos perfis antes de iniciar o processo; aceita somente o inventário previamente observado ou vazio e continua rejeitando eventos de ferramenta, agente errado, truncamento, cancelamento e resultados inconsistentes. A assinatura de prontidão inclui os perfis, adaptador, binário e inventário. Hooks experimentais não carregaram corretamente nesta versão e foram desativados; NÃO são alegados como mecanismo de proteção ativo.

[REAL — resultado] Onze testes de regressão passaram. Uma chamada real pelo adaptador IALD devolveu 42 para 6×7, terminou normalmente e gravou status=ready em validation/antigravity_connection.json. Runtime/seleção também reportaram gemini (Google / Antigravity) ready e eligible=true. O teste aritmético final informou 849 tokens totais; houve outras chamadas públicas de diagnóstico, portanto 849 NÃO é o consumo total desta manutenção. Nenhum corpo jurídico, credencial ou acervo confidencial foi enviado.

[REAL — alcance] Executor de respostas e código textual via assinatura Google; não comprova execução de código produzido, qualidade superior ou confirmação física. Limites/contexto da política permanecem como antes. Jev ainda depende de acesso. Integração de correio/agenda continua pendente. Nenhuma modificação em um.py, kernel, gate ou artigos. Web administrativa usa o conector corrigido; nenhum recurso de cliente iOS/Android foi alterado, portanto não há nova build aplicável.

[FONTES] Recursos oficiais consultados: https://antigravity.google/changelog/ (excludeDefaultComponents, versão 1.2.1); https://antigravity.google/docs/subagents?tab=cli (configuração de agentes); https://www.antigravity.google/docs/cli/headless/ (protocolo e permissões). Evidências locais: validation/antigravity_fix_delivery.json e relatórios ali referidos. A enumeração inicial do CLI é distinguida das capacidades testadas, sem alegar garantia universal a partir destes testes limitados.
'''
    claude=Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory')
    targets=[ROOT/'memory'/n for n in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md')]
    targets += [claude/n for n in ('central-de-patentes-estado.md','MEMORY_2.md','atlas-lar-miguel.md')]
    targets += [Path(r'C:\IALD\projetos_pyhton\IALD\CLAUDE.md'),Path(r'C:\LAR_MIGUEL\ATLAS.md'),BASE/'README.md']
    entries=[(p,note) for p in targets]
    entries.append((claude/'MEMORY.md','\n\n<!-- '+MARKER+' -->\n- [Antigravity corrigido 24/09](MEMORY_2.md): executor textual ready/eligible, chamada real 6×7=42 e 11 testes. Perfil restrito global/local verificado; lista init do CLI distinguida das ferramentas efetivas. Jev segue pendente.\n'))
    records=[]
    for path,text in entries:
        old=path.read_bytes()
        if MARKER.encode() not in old:
            previous=set(path.parent.glob(path.name+'.bak_*'))
            nl='\r\n' if b'\r\n' in old else '\n'
            replace_bytes(path,old+text.replace('\n',nl).encode('utf-8'))
            backups=set(path.parent.glob(path.name+'.bak_*'))-previous
            assert len(backups)==1 and backups.pop().read_bytes()==old
        current=path.read_bytes()
        assert current.startswith(old) and MARKER.encode() in current
        records.append({'path':str(path),'sha256':hashlib.sha256(current).hexdigest()})
    save_json(BASE/'validation/antigravity_fix_delivery.json',{
        'at':utc_now(), 'connection':receipt, 'candidate':candidate, 'regression_tests_passed':11,
        'comparison':'validation/antigravity_capability_comparison.json',
        'effective_tool_invocations_differ':True, 'positive_read_succeeded':False,
        'experimental_hooks_active':False, 'surfaces':records})
    print(json.dumps({'status':candidate['status'],'eligible':candidate['eligible'],
                      'memory_surfaces_verified':len(records)},ensure_ascii=False))

if __name__=='__main__':main()
