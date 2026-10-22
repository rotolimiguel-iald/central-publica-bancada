"""Record measured mail integration progress, without claiming live availability."""
from pathlib import Path
import hashlib
import json
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
MARKER = 'IALD_MAIL_LOCAL_BRIDGE_PROGRESS_20260923'
note = '''

## 23/09/2026 — Correio integrado: cadastro conferido, ponte instalada, bloqueios visíveis

<!-- IALD_MAIL_LOCAL_BRIDGE_PROGRESS_20260923 -->

[REAL — correção ao lado] O operador autenticou a Locaweb nesta sessão. Todas as quatro caixas profissionais JA EXISTEM: [dado pessoal removido], contato@iald.ia.br, tgl@teoriadagravitacaoluminodinamica.com e [dado pessoal removido]. O registro antigo de Convim inexistente foi superado pelo painel do provedor. Nenhuma caixa foi criada ou contratada. Servidor oficial conferido no painel: email-ssl.com.br, IMAP TLS 993, SMTP TLS 465. Configurações de IALD/TGL/Convim no Lar atualizadas com backups; senhas não foram extraídas do painel nem alteradas.

[REAL — testes] Conexão IMAP e autenticação SMTP do Escritório passaram, SEM envio/leitura de mensagens. DNS consultado: IALD/TGL têm MX Locaweb; rmiguel.adv.br e convim.com.br sem MX. NS desses dois domínios são Cloudflare. Painel Cloudflare aberto, aguardando login; não houve alteração DNS. Perfil Outlook contém os dois Hotmail [dado pessoal removido] e [dado pessoal removido]; ainda falta confirmar se são os dois pessoais pretendidos.

[REAL — diagnóstico Outlook] Erro reproduzido: esgotamento de recursos compartilhados ao carregar perfil. Reinício da instância de diagnóstico e do componente iCloudOutlookConfig64 não resolveu. Modo seguro também apresentou erro. Memória física livre superior a 160 GiB e arquivos OST observados menores que 1 GB, portanto não foi demonstrada falta de RAM ou tamanho excessivo de caixa. Word mantém OLMAPI32.DLL/MSPST32.DLL carregadas; fechamento após salvar documentos foi solicitado como teste, não é causa provada. Não apagar/recriar perfil/PST/OST, nem encerrar Word com documentos sem salvar. A sincronização iCloud da agenda tem falhas recentes registradas; tarefa preexistente preservada.

[REAL — engenharia parcial] Ponte C:\\LAR_MIGUEL\\correio_outlook.py instalada: status de contas da sessão ativa, rascunho na conta exata, envio somente de rascunho autorizado com verificação de remetente/destinatários/conteúdo. Journal por remetente em correio/outlook, sem corpos. Recusa remetente ausente/ambíguo, mudança de rascunho e repetição após tentativa incerta; submissão ao Outlook NÃO prova entrega. 11 testes isolados com objetos simulados passaram; nenhum teste real de envio foi executado. Anexos ainda não suportados pela ponte. Manifesto operacional: C:\\LAR_MIGUEL\\correio\\outlook_accounts.json.

[REAL — ligação ao coordenador] Fonte MCP recebeu iald_email_status, iald_email_prepare e iald_email_send; transporte local com timeout, sem repetição e sem segredos em argumentos. COORDINATOR.md descreve a rota, separada do projeto Física para não enviar correio jurídico a modelos externos. Recarregamento das novas ferramentas MCP no cliente NÃO foi confirmado. Código instalado é diferente de disponibilidade validada. Sem cron/monitor, mensagens lidas=0, mensagens enviadas=0.

[OPEN] Pendentes: login Cloudflare e correção dos MX; conclusão do diagnóstico Outlook após salvar/fechar Word; conexão das caixas IALD/TGL/Convim no Outlook com credenciais pelo operador; confirmação das contas pessoais; validação real da sessão/remetentes/rascunho e carregamento MCP. Não declarar integração total concluída. Web/iOS/Android do app de conversa não foram alterados nesta entrega de ponte local.
'''

central = ROOT / 'memory'
claude = Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory')
targets = [central/n for n in ('TGL_ATLAS.md', 'TGL_INDICE_VIVO.md', 'TGL_CORE_MEMORY.md')]
targets += [claude/n for n in ('central-de-patentes-estado.md', 'MEMORY_2.md', 'atlas-lar-miguel.md')]
targets += [Path(r'C:\IALD\projetos_pyhton\IALD\CLAUDE.md'), Path(r'C:\LAR_MIGUEL\ATLAS.md')]
entries = [(p, note) for p in targets]
entries.append((claude/'MEMORY.md', '\n\n<!-- '+MARKER+' -->\n- [Correio local 23/09](MEMORY_2.md): quatro caixas Locaweb já existem; ponte Outlook instalada e 11 testes simulados, validação real bloqueada pelo erro do aplicativo. Cloudflare/DNS e conexão das caixas pendentes. Zero mensagens enviadas.\n'))
states = [(p, text, p.read_bytes()) for p,text in entries]
records = []
for p,text,old in states:
    if MARKER.encode() not in old:
        assert old and p.read_bytes() == old
        nl = '\r\n' if b'\r\n' in old else '\n'
        replace_bytes(p, old + text.replace('\n',nl).encode('utf-8'))
    current = p.read_bytes()
    assert current.startswith(old) and MARKER.encode() in current
    records.append({'path': str(p), 'sha256': hashlib.sha256(current).hexdigest()})
manifest_path = BASE/'validation/mail_initial_delivery.json'
manifest = json.loads(manifest_path.read_bytes())
manifest.update(mcp_source_tools_added=3, mcp_loaded=False,
                adapter_sha256=hashlib.sha256(Path(r'C:\LAR_MIGUEL\correio_outlook.py').read_bytes()).hexdigest())
save_json(manifest_path, manifest)
save_json(BASE/'validation/mail_progress_memory.json', {'at':utc_now(), 'marker':MARKER,'surfaces':records})
print(json.dumps({'surfaces_verified':len(records), 'messages_sent':0, 'live_validation':'pending'}))
