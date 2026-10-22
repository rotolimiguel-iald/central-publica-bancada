"""Install a user-scoped skill over the existing shared orchestration service."""
from pathlib import Path
import hashlib
import json
import tomllib
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now

BASE = Path(__file__).resolve().parent
SKILL = Path(r'C:\Users\rotol\.agents\skills\iald-orquestrar')
GLOBAL = Path(r'C:\Users\rotol\.codex\AGENTS.md')
MARKER = 'IALD_GLOBAL_ORCHESTRATION_ENTRY_20260924'

SKILL_TEXT = r'''---
name: iald-orquestrar
description: Orquestrar as IAs integradas à IALD/Supercondutor por pedido do operador, em qualquer sessão local do Codex nesta máquina. Use quando pedir para orquestrar, coordenar várias IAs, escolher executores pelo sistema IALD ou acompanhar/retomar um pedido dessa fila. Não acionar provedores só por uma menção à IALD ou por uma pergunta geral sobre modelos.
---

# Orquestração IALD entre sessões

Esta habilidade usa a instalação existente de Luiz Antonio Rotoli Miguel neste Windows. A sessão atual pode registrar e acompanhar pedidos na fila compartilhada, independentemente de sua pasta. Não criar outro servidor, fila ou automação para cada sessão.

## Fonte operacional

BASE = `C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923`

Leia `TRANSPORTE_DESASSISTIDO.md` em BASE antes de registrar/retomar trabalho. As configurações efetivas são `transport.json`, `coordinator.json` e a resposta de estado do serviço; não presumir disponibilidade pelos nomes dos modelos. Para conteúdo TGL, consultar também a habilidade `tgl-atlas` e as fontes pertinentes. Não importar/executar um.py para recuperar contexto.

## Entrada de qualquer sessão

1. Reconhecer o pedido do operador, a casa de origem e o resultado esperado. Uma ordem para orquestrar autoriza utilizar os conectores já autorizados, dentro daquele escopo. Registrar somente o contexto necessário e permitido; não copiar o histórico inteiro da sessão. Conteúdo jurídico, credenciais e arquivos confidenciais não entram na fila remota/projeto Física. Pedidos desses domínios exigem tratamento local separado.
2. Descobrir as ferramentas do servidor global `iald-orchestrator`. Consultar `iald_orchestration_status`; usar `iald_selection_preview` para conferir a rota sem chamar modelos. Escolher etapas e provedores pelo trabalho e pelas conexões disponíveis: “todas as IAs” significa dispor do conjunto, não consumir cada provedor sem finalidade. A seleção atual não demonstra qualidade superior por benchmark. Não anunciar Jev/Antigravity como executores ativos sem evidência.
3. Para uma nova unidade de trabalho, gerar um UUID `request_id` e preservá-lo ANTES da submissão em um recibo local. Usar `BASE\state\session_requests\<request_id>.json`, com pedido permitido, casa/pasta de origem, data e identificador REAL da sessão, se disponível (nunca inventá-lo). Gravar por arquivo temporário/backup de bytes. Se já houver pedido desta missão, recuperar seu ID em vez de gerar outro. Cada etapa deve ter objetivo explícito; não replicar o pedido para todos os modelos.
4. Chamar `iald_coordination_submit(prompt, request_id)` uma vez. Registrar `job_id` retornado no recibo, junto do mesmo request_id. Em resultado incerto, repetir APENAS o mesmo request_id e o mesmo prompt: a criação é idempotente. Nunca gerar UUID novo para contornar um timeout. O worker oficial cria uma tarefa ChatGPT Work no projeto Física por pedido; o operador já autorizou esse comportamento.
5. Acompanhar por `iald_coordination_get(job_id)`. A fila é comum; outras sessões podem consultar o mesmo ID. Apresentar resultado concluído com executor/uso/evidência e depois realizar apenas as ações locais autorizadas na casa de origem. Enquanto pendente, distinguir “registrado” de “concluído”. A síntese fica na fila/painel e na tarefa Work vinculada; o acompanhamento desassistido continua na tarefa coordenadora, não há promessa de notificação automática em todas as sessões de origem.

## Um único responsável pelas transições

O worker habitual é o heartbeat `iald-transporte-autom-tico-entre-ias`, da tarefa `01a0ce2b-8c2f-71b0-a9a8-91b17715a569`. A ordem do operador de 24/09/2026 autorizou o transporte desassistido e uma tarefa Work por pedido. Sessões de origem submetem/acompanham; não começam a executar as mesmas transições em paralelo ao worker. Não criar outra automação nem alterar o alvo da existente.

Se houver necessidade real de recuperação, conferir estado da automação pelas ferramentas oficiais e estado persistente da fila antes de assumir trabalho. Não assumir abandono pela passagem de alguns minutos. Em `draft_dispatching`, `execution_dispatching` ou `synthesis_dispatching`, resultado pode ser incerto: procurar a evidência/marker existente e seguir o guia; não repetir chamada externa às cegas. Esta habilidade não autoriza iniciar missões sem pedido nem alterar limites/contas/filtros.

## Fallback local quando o MCP não estiver no catálogo

O registro MCP global pode existir sem estar carregado na sessão. Usar os CLIs existentes com Python `C:\Python314\python.exe -X utf8` e caminho absoluto; não fingir ter chamado uma ferramenta ausente. Eles funcionam fora de BASE.

- `transport_cli.py`: JSON stdin `{"operation":"next"}`; ou `{"operation":"submit","prompt":"...","request_id":"UUID"}`.
- `bridge.py`: JSON stdin `{"operation":"get","job_id":"UUID"}` ou `{"operation":"list"}`. A listagem retorna metadados; não abrir outros pedidos sem relação com a missão.
- Para inspeção do seletor sem MCP, usar `Runtime(recover=False).status()` / `.preview(prompt)` do pacote em BASE; nunca `recover=True` numa sessão cliente.

Comandos PowerShell de consulta (sem chamar modelos):

```powershell
'{"operation":"next"}' | & 'C:\Python314\python.exe' -X utf8 'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\transport_cli.py'
'{"operation":"list"}' | & 'C:\Python314\python.exe' -X utf8 'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\bridge.py'
```

Para prompts arbitrários, criar um JSON UTF-8 por ferramenta de arquivo. Passar seu conteúdo como stdin, nunca interpolá-lo como código shell. No PowerShell, definir `$OutputEncoding = [System.Text.UTF8Encoding]::new($false)` antes de `Get-Content -Raw -Encoding UTF8 -LiteralPath '<arquivo JSON real>' | & '<python>' -X utf8 '<CLI absoluto>'`. Manter o recibo de origem separado do JSON de chamada; não mandar caminhos privados ao modelo sem necessidade.

## Limites que acompanham a capacidade

- A fila delega geração de texto/artefatos textuais; a sessão que gere a missão verifica e executa ações de sistema pelas ferramentas apropriadas. Uma resposta de modelo não prova execução de código, envio, implantação ou correção física.
- Memória do projeto Física continua no ChatGPT Work. Não alegar acesso automático a toda a memória privada, aos pesos ou à janela máxima. Conferir limites efetivos por tarefa.
- Separar Central, Física, IALD Nativa, Lar e Escritório. A fila compartilhada não permite misturar seus acervos ou faturamento. Usar orçamento/política vigentes; a autorização MiMo sem teto não autoriza missões novas.
- O acesso global é para este usuário neste computador com arquivos/contas disponíveis. Uma sessão remota/nuvem sem o host local não ganha acesso por ler a habilidade.
- Se a habilidade nova não aparecer, uma nova sessão/reabertura pode carregar o catálogo atualizado. A leitura deste arquivo e o CLI absoluto continuam sendo a rota verificável; não reiniciar o aplicativo ou interromper outras tarefas automaticamente.
'''

YAML_TEXT = '''interface:
  display_name: "IALD — Orquestrar IAs"
  short_description: "Coordene as IAs da IALD em qualquer sessão local"
  default_prompt: "Use $iald-orquestrar para coordenar esta tarefa com as IAs disponíveis na IALD."
policy:
  allow_implicit_invocation: true
'''

GLOBAL_NOTE = r'''

## 24/09/2026 — Orquestração IALD disponível entre sessões locais

<!-- IALD_GLOBAL_ORCHESTRATION_ENTRY_20260924 -->

[INPUT — ordem permanente] Quando o operador pedir uma tarefa “orquestrando as IAs”, usar a habilidade global `iald-orquestrar`: `C:\Users\rotol\.agents\skills\iald-orquestrar\SKILL.md`. Ela vale em qualquer pasta desta máquina. Ler o arquivo se o catálogo da sessão ainda não o mostrar. Não exigir que o operador volte à conversa de instalação.

[REAL — entrada operacional] Servidor MCP global `iald-orchestrator`; fallback JSON em stdin para `C:\Python314\python.exe -X utf8 C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\transport_cli.py`. O guia completo está em `TRANSPORTE_DESASSISTIDO.md` nessa pasta. Há UMA fila e UM heartbeat já configurados: não duplicá-los por sessão. Preservar request_id/job_id e a casa de origem. Sessões clientes registram/acompanham; o worker existente conduz as transições e cria a tarefa Work em Física conforme autorização já dada.

Registrar pedido não é concluir execução. Verificar ferramentas/modelos realmente disponíveis, retomar sem duplicar chamadas incertas, proteger confidenciais e manter separação das casas. A capacidade global não transfere toda a memória do ChatGPT nem concede acesso ao host em sessões remotas. Detalhes e recuperação ficam na habilidade, sem depender do histórico desta conversa.
'''

GUIDE_NOTE = r'''

## 24/09/2026 — Entrada global por outras sessões

<!-- IALD_GLOBAL_ORCHESTRATION_ENTRY_20260924 -->

A habilidade `C:\Users\rotol\.agents\skills\iald-orquestrar\SKILL.md` permite que qualquer sessão local registre/acompanhe trabalho na mesma fila. Essas sessões não criam novos heartbeats nem disputam as transições com o worker desta tarefa. Recibos de origem ficam em `state/session_requests/`, com request_id estável e job_id para retomada; são contexto local, não novos pedidos nem autorização adicional. A síntese permanece acessível pela fila e pela tarefa Work vinculada; não foi instalado envio automático de mensagens às sessões de origem. O operador pode invocar `$iald-orquestrar` ou pedir em linguagem natural que orquestre uma tarefa.
'''

def append_once(path, note):
    old = path.read_bytes()
    if MARKER.encode() in old:
        return
    newline = '\r\n' if b'\r\n' in old else '\n'
    updated = old + note.replace('\n', newline).encode('utf-8')
    replace_bytes(path, updated)
    assert path.read_bytes().startswith(old)

def main():
    config = tomllib.loads((GLOBAL.parent/'config.toml').read_text(encoding='utf-8'))
    mcp = config['mcp_servers']['iald-orchestrator']
    assert Path(mcp['command']).is_file()
    assert str(BASE/'mcp_server.py') in mcp['args']
    for path, body in ((SKILL/'SKILL.md', SKILL_TEXT), (SKILL/'agents/openai.yaml', YAML_TEXT)):
        data = body.encode('utf-8')
        if not path.exists() or path.read_bytes() != data:
            replace_bytes(path, data)
        assert path.read_bytes() == data
    append_once(GLOBAL, GLOBAL_NOTE)
    assert GLOBAL.stat().st_size < 32768, 'Global guidance exceeds default 32 KiB budget'
    append_once(BASE/'TRANSPORTE_DESASSISTIDO.md', GUIDE_NOTE)
    files = [GLOBAL, SKILL/'SKILL.md', SKILL/'agents/openai.yaml', BASE/'TRANSPORTE_DESASSISTIDO.md']
    receipt = {'at': utc_now(), 'skill': str(SKILL), 'global_instructions_bytes': GLOBAL.stat().st_size,
               'mcp_config_preserved': True, 'queue_reused': True, 'automation_created': False,
               'files': [{'path':str(p), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
    save_json(BASE/'validation/global_skill_install.json', receipt)
    print(json.dumps(receipt, ensure_ascii=False))

if __name__ == '__main__':
    main()
