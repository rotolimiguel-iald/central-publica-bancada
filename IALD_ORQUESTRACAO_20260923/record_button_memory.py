"""Append the button delivery and explicit no-schedule preference, byte-for-byte backups."""
from pathlib import Path
from datetime import datetime
import hashlib,json,os,urllib.request,urllib.error
base=Path(__file__).resolve().parent
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
marker='IALD_BUTTON_COORDINATION_NO_POLLING_20260923'
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*a,**kw):return None
checks={};opener=urllib.request.build_opener(NoRedirect())
for route in ['/health','/admin/agi/orquestracao','/admin/api/orchestrator/status','/admin/api/orchestrator/coordination/4d1fcd7c-a03d-41a5-b07a-edad9d3581a4']:
    try:
        with opener.open('http://127.0.0.1:8082'+route,timeout=8) as r:checks[route]=r.status
    except urllib.error.HTTPError as e:checks[route]=e.code
assert list(checks.values())==[200,302,401,401],checks
from iald_orchestrator.coordination import Coordination
job=Coordination().get('4d1fcd7c-a03d-41a5-b07a-edad9d3581a4')
assert job['stage']=='completed'
note=f'''

## 23/09/2026 — Acionamento por botão e percurso Física → executor → Física

<!-- {marker} -->

[INPUT — preferência explícita] Luiz escolheu acionar a coordenação pelo botão, SEM verificações periódicas. Não criar heartbeat, cron nem chamadas recorrentes de modelos para a fila. Autorizou concluir logins oficiais de Gemini/Kimi; senhas e credenciais permanecem nos clientes oficiais.

[REAL — engenharia] Painel administrativo /admin/agi/orquestracao agora registra pedido, oferece Abrir Codex e enviar pedido e guarda as etapas da coordenação no SQLite. O deep link oficial preenche a mensagem; o operador ainda clica Enviar no Codex. Depois desse envio, o roteiro COORDINATOR.md orienta a criação de uma tarefa Work em Física por pedido, preparação do prompt, seleção do executor e síntese final no mesmo projeto. Sem conversa global fixa, API privada do ChatGPT ou monitor. Alternativa: copiar a instrução do painel. A abertura real do protocolo do Windows pelo clique depende do cliente; nesta rodada o link foi conferido na prévia, sem criar tarefa adicional para só testar a abertura.

[REAL — teste integrado] Pedido {job['id']} concluído: a tarefa Work de teste já autorizada foi reutilizada somente para a validação, preparou o prompt, o seletor escolheu local e o resultado voltou ao projeto para síntese, gravada no painel. Executor informou 243 tokens de entrada +39 de saída=282, 1,426 s. Código de soma foi gerado como texto, NÃO executado. Recibo integral: {base / 'validation/button_roundtrip_completed.json'}. Consumo de Codex coordenador/ChatGPT Work é separado e não medido pelo painel.

[REAL — verificações] 29 testes passaram, incluindo exclusão mútua entre runtimes, idempotência, transições, cancelamento durante envio, preservação do pedido original e classificação sem interferência da preparação. Prévia isolada: clique repetido preservou um único pedido; cancelamento verificado; sem erros no console. MCP real enumerou quatro ferramentas: estado, prévia, leitura de coordenação e ação explícita sobre pedido existente. A ação execute pode chamar o executor; o MCP deixou de ser exclusivamente leitura. Recarregar o cliente para ver ferramentas novas; bridge.py por stdin funciona como alternativa. Reiniciado apenas o web ocioso, supervisor preservado. Saúde200, página302/login, APIs de estado e coordenação401 sem sessão na implantação final. Teste visual autenticado da produção continua pendente; não foi forjada sessão.

[REAL — acesso] Kimi Code oficial 2.0.2 respondeu HTTP403: assinatura atual sem acesso ao Kimi Code. Isso não afirma ausência de assinatura/acesso ao chat Kimi. Status subscription_access_denied exclui o cliente da seleção, sem upgrade ou novas tentativas automáticas. Gemini: janela de login aberta, OAuth ainda ausente no perfil dedicado na última conferência, executor não habilitado. Claude conserva bloqueio por limite já informado. MiMo instalado, mas inicialização/acesso não validados. Jev continua sem acesso TypeSafe. Local e Codex permanecem as conexões validadas. Seleção ainda é política inicial, sem benchmark de qualidade ou garantia de menor custo total.

[MATRIZ DE ENTREGA] Web/admin: módulo novo carregado e rotas protegidas. iOS interno, iOS externo e Android: sem mudança de cliente, recompilação não aplicável; distribuição anterior preservada e não revalidada aqui. Alertas de acesso/cota ficam somente na administração. Os 16 anexos do projeto Física da entrega anterior permanecem; não foram reenviados ou alegados como sincronização contínua.

[OPEN] Finalizar acessos e implementar/validar executores pendentes; comparar qualidade/custo em tarefas representativas; execução geral de ações/arquivos. O fluxo por botão já foi demonstrado no teste acima; integração irrestrita de todas as assinaturas não está concluída. Cânone científico, gate e originais intocados. Guia atualizado: {base / 'README.md'}.
'''
claude=Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory')
surfaces=[(Path(r'C:\IALD\Central de Patentes\memory')/name,note) for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md']]
surfaces += [(claude/name,note) for name in ['central-de-patentes-estado.md','MEMORY_2.md']]
surfaces += [(Path(r'C:\IALD\projetos_pyhton\IALD\CLAUDE.md'),note),(claude/'MEMORY.md',f'\n\n<!-- {marker} -->\n- [Orquestração por botão — 23/09](MEMORY_2.md): Física → local → Física validado; preferência permanente sem verificações periódicas; Gemini pendente e Kimi Code recusado por acesso da assinatura.\n')]
report=[]
for p,addition in surfaces:
    old=p.read_bytes();assert old and marker.encode() not in old,p
    newline='\r\n' if b'\r\n' in old else '\n'
    new=old+addition.replace('\r\n','\n').replace('\n',newline).encode('utf-8')
    bak=p.with_name(p.name+'.bak_'+stamp);bak.write_bytes(old);assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+stamp);tmp.write_bytes(new)
    assert tmp.read_bytes()==new and len(new)>len(old) and p.read_bytes()==old
    os.replace(tmp,p);assert p.read_bytes()==new
    report.append({'path':str(p),'backup':str(bak),'before':len(old),'after':len(new),'sha256':hashlib.sha256(new).hexdigest()})
out=base/'validation'/('button_delivery_'+stamp+'.json');tmp=out.with_suffix('.tmp')
tmp.write_bytes(json.dumps({'http_checks':checks,'tests_passed':29,'mcp_tools':4,'surfaces':report,'automatic_polling':False},ensure_ascii=False,indent=2).encode())
assert tmp.stat().st_size>0;os.replace(tmp,out)
print(json.dumps({'updated_memories':len(report),'record':str(out),'http_checks':checks},ensure_ascii=False))
