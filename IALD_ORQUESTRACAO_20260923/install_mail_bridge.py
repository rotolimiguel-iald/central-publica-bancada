"""Install the neutral-house mail adapter without opening mailbox contents."""
import hashlib
import json
from pathlib import Path
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now

BASE = Path(__file__).resolve().parent
LAR = Path(r'C:\LAR_MIGUEL')
source = BASE / 'mail_stage/correio_outlook.py'
target = LAR / 'correio_outlook.py'
replace_bytes(target, source.read_bytes())
assert target.read_bytes() == source.read_bytes()

addresses = {
    'escritorio': '[dado pessoal removido]',
    'iald': 'contato@iald.ia.br',
    'tgl': 'tgl@teoriadagravitacaoluminodinamica.com',
    'convim': '[dado pessoal removido]',
}
for house in ('iald', 'tgl', 'convim'):
    path = LAR / 'correio' / (house + '.json')
    cfg = json.loads(path.read_bytes().decode('utf-8-sig'))
    cfg.update(conta=addresses[house], usuario=addresses[house], de=addresses[house])
    cfg['imap'] = {'servidor': 'email-ssl.com.br', 'porta': 993}
    cfg['smtp'] = {'servidor': 'email-ssl.com.br', 'porta': 465, 'seguranca': 'ssl'}
    cfg['nota'] = ('Caixa existente conferida no painel Locaweb em 23/09/2026. '
                   'Autenticacao local ainda pendente; nao e necessario recriar a caixa. '
                   'Integracao Outlook usa o perfil do usuario, sem extrair senhas.')
    save_json(path, cfg)

manifest = {'checked_at': utc_now(), 'professional_accounts': addresses,
            'outlook_observed_accounts': ['[dado pessoal removido]', '[dado pessoal removido]',
                                          '[dado pessoal removido]'],
            'personal_identity_confirmation': 'pending_operator',
            'locaweb_accounts': 'all_four_exist',
            'dns_mx_missing': ['rmiguel.adv.br', 'convim.com.br'],
            'office_protocol_auth_test': {'imap': True, 'smtp': True, 'messages_sent': 0},
            'outlook_status': 'startup_shared_resources_error_under_diagnosis',
            'adapter': str(target), 'adapter_status': 'offline_guards_passed_live_test_pending',
            'offline_tests_passed': 11, 'messages_read': 0, 'messages_sent': 0}
save_json(LAR / 'correio/outlook_accounts.json', manifest)
save_json(BASE / 'validation/mail_initial_delivery.json', {
    **manifest, 'adapter_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
    'native_ui_modified': False, 'mcp_loaded': False,
})
coord = BASE / 'COORDINATOR.md'
marker = 'IALD_OUTLOOK_LOCAL_BRIDGE_20260923'
if marker.encode() not in coord.read_bytes():
    note = '''

## Correio — roteamento local separado do projeto Física

<!-- IALD_OUTLOOK_LOCAL_BRIDGE_20260923 -->

Pedidos de integração/redação/envio de e-mail usam a ponte local `C:\\LAR_MIGUEL\\correio_outlook.py`, com JSON por stdin e Python C:\\Python314\\python.exe. Não encaminhar automaticamente correspondência do Escritório ao projeto Física ou a provedores remotos. O manifesto sem senhas é `C:\\LAR_MIGUEL\\correio\\outlook_accounts.json`; seu estado pode estar pendente e deve ser medido novamente.

- `{"operation":"status"}` lê somente as contas da sessão aberta do Outlook. Não inicia o aplicativo, não lê mensagens e não comprova entrega.
- `prepare` exige `sender` completo, `to` como lista de endereços, `subject` e `body` explicitamente autorizados. Salva em Rascunhos da conta escolhida e retorna `draft_id` e `sha256`. Anexos ainda exigem outro fluxo revisado; não são aceitos silenciosamente.
- `send` exige `sender`, `draft_id`, `expected_sha256` e `confirmed:true` SOMENTE após ordem concreta do operador para aquele conteúdo e destinatários. Conta ausente/ambígua, conteúdo alterado ou tentativa anterior bloqueiam o envio. Não substituir remetente. `SUBMITTED_TO_OUTLOOK_NOT_DELIVERY_CONFIRMED` significa submetido à caixa de saída, nunca prova de entrega. Após estado incerto, verificar manualmente; não repetir automaticamente.

Nesta entrega, 11 testes com objetos simulados passaram, sem envio real. Outlook ainda em diagnóstico; o código instalado não torna as contas ausentes disponíveis por si só. Não criar cron/monitor para esta ponte.
'''
    replace_bytes(coord, coord.read_bytes() + note.encode('utf-8'))
print(json.dumps({'installed': str(target), 'configurations_updated': 3,
                  'locaweb_mailboxes_created': 0, 'live_outlook_test': 'pending'}))
