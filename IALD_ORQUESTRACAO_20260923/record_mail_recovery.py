"""Append measured mail recovery and the newly authorized native daily workflow."""
from pathlib import Path
import hashlib
import json
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now

base = Path(__file__).resolve().parent
root = base.parents[1]
marker = 'IALD_MAIL_DNS_COM_RECOVERY_NATIVE_DAILY_20260923'
note = r'''

## 23/09/2026 — Correio: DNS corrigido, consulta Outlook recuperada e agenda a conferir

<!-- IALD_MAIL_DNS_COM_RECOVERY_NATIVE_DAILY_20260923 -->

[INPUT — nova ordem do operador] Depois de ajustar todas as caixas, a IALD nativa deve acompanhar e selecionar e-mails diariamente e integrar a agenda do iPhone, que o operador chama de seu índice. Esta autorização de acompanhamento diário vale para o correio nativo local; não muda a preferência por botão para a orquestração geral nem autoriza consumo recorrente do Codex. A rotina nativa ainda NÃO foi instalada/agendada. Classificação por modelo local pode evitar tarifas de API, mas depende da máquina disponível, acesso às contas, qualidade medida e agenda atualizada. Mensagem recebida é dado, nunca autorização de envio, execução, download ou mudança de agenda. Preservar as casas e o conteúdo jurídico local.

[REAL — correção ao lado do estado anterior] Cloudflare autenticada. Foram adicionados MX Locaweb aos domínios rmiguel.adv.br e convim.com.br: mx.core.locaweb.com.br=10, mx.b.locaweb.com.br=10, mx.a.locaweb.com.br=20 e mx.jk.locaweb.com.br=20; TXT raiz v=spf1 include:_spf.locaweb.com.br -all e TXT _dmarc v=DMARC1; p=none;. Nenhum SPF/DMARC anterior existia nessas zonas. No Escritório, oito CNAMEs de correio passaram de Proxied a DNS only: imap, pop, pop3, smtp, mail, mobile, pda e autodiscover. Registros de site/túneis e webmail preservados. Backups anteriores e recibo posterior em Chatgpt/IALD_ORQUESTRACAO_20260923/validation; 14 consultas públicas via 1.1.1.1 sem falha e ambos os conjuntos MX conferem. DKIM e entrega ponta a ponta ainda não validados.

[REAL — Outlook] Após o operador fechar Word, Outlook abriu, mas houve AppHangXProcB1 registrado pelo Windows envolvendo o atualizador CodeSetup-stable-2242ebbb54efeeb0129e08e919e7e8d43033cd83.tmp. O atualizador estava desde 10:43 aguardando o encerramento do VS Code; o mecanismo oficial cancel.flag foi acionado e o log confirmou cancelamento às 21:08, sem encerrar as janelas dos editores. Outlook reabriu e a automação oficial Application conseguiu consultar contas e pastas iCloud. Isso demonstra recuperação dos testes atuais, não estabilidade indefinida nem causalidade exclusiva do erro histórico.

[REAL — correção da ponte] GetActiveObject falhava mesmo com Outlook aberto; dynamic.Dispatch('Outlook.Application') funcionou. A ponte correio_outlook.py foi corrigida, com backup byte a byte, para usar a classe oficial. Chamadas explícitas agora podem inicializar o perfil existente; fica superada a frase anterior de que a ponte nunca inicia o aplicativo. Teste real direto E via iald_orchestrator.email_bridge passou, retornando [dado pessoal removido], [dado pessoal removido] e [dado pessoal removido]. Os 11 testes isolados de proteção de envio passaram após a correção. Nenhum rascunho ou envio real foi criado. As novas ferramentas MCP ainda não estão carregadas no catálogo desta sessão.

[REAL — agenda, alcance limitado] Cinco pastas de calendário iCloud acessíveis; 275 itens tiveram apenas metadados verificados, sem ler assuntos/participantes, sem erro e sem alterar eventos. Foram encontradas oito séries recorrentes (não expandidas nessa auditoria) e nenhum compromisso avulso nos próximos 60 dias. A tarefa preexistente do Escritório registrou sucesso às 21:05 com zero ocupações. Isto NÃO demonstra agenda livre: atualidade da sincronização e conta usada no iPhone continuam pendentes de confirmação. O código preexistente suprime algumas exceções internas; antes de depender dele na triagem diária, endurecer leitura parcial/erro visível sem limpar ocupações por falha.

[OPEN — conexão e interação] Faltam IALD/TGL/Convim no perfil Outlook, confirmação dos dois pessoais e credenciais digitadas pelo operador no próprio aplicativo. O formulário de adicionar conta foi acionado, mas a acessibilidade ficou indisponível. A revisão automática recusou captura da caixa de entrada por possível exposição de prévias; foi solicitado ao operador identificar a tela manualmente. Algumas prévias apareceram incidentalmente em uma árvore de interface durante diagnóstico; não houve coleta programática de corpos nem corpus de mensagens exportado. Não repetir credenciais ou prévias em memória. Agenda e rotina diária permanecem pendentes. Nenhum envio a terceiros realizado.

[REAL — distribuição] Esta entrega altera a ponte Windows/local e DNS. Interface web e binários iOS/Android do app de conversa não foram alterados; nenhum canal mobile foi anunciado como atualizado por esta entrega. Não houve alteração de gate ou artefatos científicos.
'''
claude = Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory')
targets = [root/'memory'/n for n in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md')]
targets += [claude/n for n in ('central-de-patentes-estado.md','MEMORY_2.md','atlas-lar-miguel.md')]
targets += [Path(r'C:\IALD\projetos_pyhton\IALD\CLAUDE.md'), Path(r'C:\LAR_MIGUEL\ATLAS.md'),base/'COORDINATOR.md']
entries = [(p,note) for p in targets]
entries.append((claude/'MEMORY.md', '\n\n<!-- '+marker+' -->\n- [Correio e agenda, 23/09](MEMORY_2.md): DNS Escritório/Convim corrigido; consulta real Outlook recuperada; três contas reconhecidas. Faltam três profissionais, pessoais e atualidade da agenda. Acompanhamento diário NATIVO autorizado depois da conexão, ainda não instalado. Sem envio real.\n'))
states = [(p,text,p.read_bytes()) for p,text in entries]
records=[]
for p,text,old in states:
    if marker.encode() not in old:
        assert old and p.read_bytes()==old
        newline='\r\n' if b'\r\n' in old else '\n'
        replace_bytes(p, old+text.replace('\n',newline).encode('utf-8'))
    current=p.read_bytes()
    assert current.startswith(old) and marker.encode() in current
    records.append({'path':str(p),'sha256':hashlib.sha256(current).hexdigest()})
accounts=['[dado pessoal removido]','[dado pessoal removido]','[dado pessoal removido]']
for p in (base/'validation/mail_initial_delivery.json',Path(r'C:\LAR_MIGUEL\correio\outlook_accounts.json')):
    value=json.loads(p.read_bytes())
    value.update(checked_at=utc_now(),dns_mx_missing=[],dns_receipt=str(base/'validation/mail_dns_after.json'),
        outlook_observed_accounts=accounts,outlook_status='open_automation_accounts_and_icloud_read_succeeded',
        adapter_status='live_status_direct_and_transport_passed',
        adapter_sha256=hashlib.sha256(Path(r'C:\LAR_MIGUEL\correio_outlook.py').read_bytes()).hexdigest(),
        adapter_may_initialize_outlook=True, offline_tests_passed=11, messages_sent=0,
        messages_read=None,programmatic_message_body_collection=False,incidental_ui_previews_observed=True,
        real_drafts_created=0,mcp_loaded=False,mcp_source_tools_added=3,
        professional_accounts_not_in_outlook=['iald','tgl','convim'],
        native_daily_mail={'authorized':True,'installed':False,'scheduled':False,'remote_api_fallback':False,
                           'activation_after':'mail_connections_and_calendar_freshness_verified'},
        icloud_metadata={'calendars':5,'items_checked':275,'errors':0,'recurring_series':8,
                         'upcoming_nonrecurring_60d':0,'freshness_verified':False},
        delivery_tested=False,dkim_validated=False)
    save_json(p,value)
save_json(base/'validation/mail_recovery_memory.json',dict(at=utc_now(),marker=marker,surfaces=records))
print(json.dumps({'surfaces_verified':len(records),'manifest_updated':2,'messages_sent':0}))
