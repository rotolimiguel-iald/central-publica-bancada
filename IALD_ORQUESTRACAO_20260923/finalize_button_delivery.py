from pathlib import Path
from datetime import datetime
import os,json
base=Path(__file__).resolve().parent
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def save(p,text):
    original=p.read_bytes();data=text.encode('utf-8')
    if original==data:return
    backup=p.with_name(p.name+'.bak_'+stamp);backup.write_bytes(original);assert backup.read_bytes()==original
    temporary=p.with_name(p.name+'.tmp_'+stamp);temporary.write_bytes(data)
    assert temporary.stat().st_size==len(data)>0 and p.read_bytes()==original
    os.replace(temporary,p);assert p.read_bytes()==data
p=base/'iald_orchestrator/coordination.py';s=p.read_text(encoding='utf-8')
s=s.replace('prompt=validate_prompt(prompt);uuid.UUID(request_id)',"prompt=validate_prompt(prompt)\n        if not isinstance(request_id,str):raise ValueError('Identificador inválido.')\n        uuid.UUID(request_id)")
s=s.replace("payload=payload or {}", "payload={} if payload is None else payload")
s=s.replace("thread_id=payload.get('thread_id','');uuid.UUID(thread_id)","thread_id=payload.get('thread_id','')\n            if not isinstance(thread_id,str):raise ValueError('Identificador de tarefa inválido.')\n            uuid.UUID(thread_id)")
s=s.replace("f'Processe a coordenação IALD {job_id}. Leia COORDINATOR.md neste diretório e siga o fluxo '","f'Processe a coordenação IALD {job_id}. Leia {BASE / \"COORDINATOR.md\"} e siga o fluxo '")
save(p,s)
p=base/'iald_orchestrator/panel.js';s=p.read_text(encoding='utf-8')
s=s.replace("$('cancel').hidden=['completed','failed','cancelled'].includes(job.stage);await refresh();", "$('cancel').hidden=['completed','failed','cancelled'].includes(job.stage);if($('cancel').hidden){coordinationRequestId=null;coordinationPrompt=null;}await refresh();")
save(p,s)
p=base/'COORDINATOR.md';s=p.read_text(encoding='utf-8').replace('"project_id":"g-p-..."','"project_id":"g-p-6804cf9af0cc81918b3bd8915b7579c3"');save(p,s)
p=base/'coordinator.json';data=json.loads(p.read_text(encoding='utf-8'))
data.update(button_roundtrip_validated=True,button_roundtrip_record='validation/button_roundtrip_completed.json',validation_job_id='4d1fcd7c-a03d-41a5-b07a-edad9d3581a4')
save(p,json.dumps(data,ensure_ascii=False,indent=2)+'\n')
p=base/'README.md';s=p.read_text(encoding='utf-8')
s=s.replace('Base administrativa instalada; integração integral ainda em andamento.','Fluxo por botão instalado e validado com o projeto Física e executor local. Conexões externas pendentes descritas abaixo.')
s=s.replace('**Ver seleção sem executar**', '**Preparar pedido com Física** registra o pedido. Clique em **Abrir Codex e enviar pedido** e envie a mensagem já preenchida no Codex. A partir desse envio, o agente segue `COORDINATOR.md`: Física prepara o prompt, a IALD seleciona e chama um executor, e Física compõe a resposta final. O link oficial preenche a mensagem, sem enviá-la automaticamente. Cada novo pedido deve abrir uma tarefa própria em Física; a mesma tarefa é retomada dentro do pedido. Use **Atualizar disponibilidade** para consultar o resultado no painel. **Não foi criado monitor, heartbeat ou verificação periódica.**\n\n**Ver seleção sem executar**',1)
s=s.replace('O painel local ainda não encaminha automaticamente tarefas ao projeto; não existe aqui uma API privada do ChatGPT nem um daemon de navegador.','O painel aciona esse transporte pelo botão e pelo envio da mensagem no Codex; não existe aqui uma API privada do ChatGPT nem um daemon de navegador. O teste da fila persistente reutilizou a tarefa de teste já autorizada: seleção local, resposta real com 243 tokens de entrada e 39 de saída, síntese final no projeto e gravação no painel. Recibo: `validation/button_roundtrip_completed.json`. A abertura do deep link depende do protocolo Codex registrado no Windows; a alternativa é copiar a instrução mostrada no painel e enviá-la no Codex.')
s=s.replace('| Gemini, Kimi, MiMo | Clientes instalados; autenticação e execução ainda não validadas. Executores não habilitados. |','| Gemini CLI | Janela oficial de login aberta. Credencial OAuth ainda ausente no perfil dedicado na última conferência; executor não habilitado. |\n| Kimi Code | Login registrado, mas o cliente oficial devolveu HTTP 403: a assinatura atual não dá acesso ao Kimi Code. Excluído da seleção; não equivale a dizer que a assinatura do chat Kimi não funciona. |\n| MiMoCode | Cliente instalado; inicialização do executável não concluiu nos testes limitados. Acesso e condições de uso ainda não validados; excluído da seleção. |')
s=s.replace('com duas ferramentas: `iald_orchestration_status` e `iald_selection_preview`. São consultas: não executam modelos.', 'com quatro ferramentas: `iald_orchestration_status` e `iald_selection_preview` são consultas sem execução; `iald_coordination_get` lê um pedido; `iald_coordination_action` avança um pedido existente e sua ação `execute` pode consumir a conexão selecionada. Nenhuma ferramenta cria pedidos indiscriminadamente ou agendas. `bridge.py` é alternativa por JSON em stdin enquanto o cliente MCP não tiver sido recarregado.')
s=s.replace('23 testes passaram:', '29 testes passaram:').replace('fila, autenticação e origem das requisições.', 'fila, autenticação, origem das requisições, transições da coordenação, cancelamento durante envio, preservação do pedido original e exclusão mútua entre dois runtimes. Clique repetido no botão produziu um único pedido na prévia; cancelamento verificado; quatro ferramentas MCP enumeradas pelo protocolo real.')
s=s.replace('comparar qualidade/custo com tarefas representativas; conectar o fluxo automático painel → projeto Física → executor → síntese.', 'comparar qualidade/custo com tarefas representativas. O percurso por botão Física → executor → Física já foi validado, mas depende do aplicativo Codex disponível e do envio inicial pelo operador. O consumo do coordenador Codex/ChatGPT Work é separado do consumo registrado pelo executor; ainda não é medido pelo painel.')
s+='\nReferências do acionamento: [links oficiais do Codex](https://learn.chatgpt.com/docs/reference/commands) e [perfis de ferramentas do Kimi Code](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/agents.html). Login local: `C:\\Python314\\python.exe login_provider.py gemini` ou `kimi`, executado nesta pasta. Não enviar credenciais na conversa.\n'
save(p,s)
print('Final delivery documentation and button handling updated with byte backups.')
