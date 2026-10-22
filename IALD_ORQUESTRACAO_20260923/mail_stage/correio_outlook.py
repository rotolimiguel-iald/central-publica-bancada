"""Local Outlook bridge: exact sender, separate drafts, explicit reviewed sends.

Reads no mailbox bodies. Uses the current Windows user's existing Outlook session.
Explicit calls may initialize the existing Outlook profile. Never retries sending.
JSON requests arrive only through stdin.
Deploy in C:\\LAR_MIGUEL, where correio/ is excluded from plain cloud mirrors and Git.
"""
from __future__ import annotations
import contextlib
import hashlib
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / 'correio' / 'outlook'


def address(value):
    if not isinstance(value, str) or not re.fullmatch(r'[^\s<>@,;]+@[^\s<>@,;]+\.[^\s<>@,;]+', value):
        raise ValueError('Informe um endereço completo e único.')
    return value.casefold()


def recipients(value):
    if not isinstance(value, list) or not value or len(value) > 50:
        raise ValueError('Informe de 1 a 50 destinatários explícitos.')
    return [address(x) for x in value]


def choose_account(accounts, sender):
    sender = address(sender)
    matches = [a for a in accounts if str(a.SmtpAddress).casefold() == sender]
    if len(matches) != 1:
        raise ValueError('Remetente ausente ou duplicado no Outlook; sem troca automática de conta.')
    return matches[0]


@contextlib.contextmanager
def active_outlook():
    import pythoncom
    from win32com.client import dynamic
    pythoncom.CoInitialize()
    try:
        # Outlook can be running without an entry in the Running Object Table.
        # The official Application class connects to the current default profile.
        # This explicit call may start Outlook; the caller bounds its execution.
        app = dynamic.Dispatch('Outlook.Application')
        yield app
    finally:
        pythoncom.CoUninitialize()


def atomic_json(path, value):
    data = json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_bytes() if path.exists() else None
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    if old is not None:
        backup = path.with_name(path.name + '.bak_' + stamp)
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temp = path.with_name(path.name + '.tmp_' + stamp)
    temp.write_bytes(data)
    assert temp.read_bytes() == data
    assert (path.read_bytes() if path.exists() else None) == old
    temp.replace(path)
    assert path.read_bytes() == data


def journal_path(sender, draft_id):
    sender = address(sender)
    if str(uuid.UUID(draft_id)) != draft_id:
        raise ValueError('Identificador inválido.')
    return STATE / hashlib.sha256(sender.encode()).hexdigest() / (draft_id + '.json')


def fingerprint(mail, sender):
    actual = str(mail.SendUsingAccount.SmtpAddress).casefold()
    if actual != address(sender):
        raise ValueError('O Outlook não confirmou a conta remetente solicitada.')
    # Display strings and body are hashed locally; they are not logged or returned.
    resolved = [(int(r.Type), str(r.Address)) for r in mail.Recipients]
    fields = [actual, resolved, str(mail.To), str(mail.CC), str(mail.BCC), str(mail.Subject), str(mail.Body)]
    if int(mail.Attachments.Count):
        raise ValueError('Anexos exigem revisão específica; esta versão aceita texto simples.')
    return hashlib.sha256(json.dumps(fields, ensure_ascii=False).encode()).hexdigest()


def status():
    with active_outlook() as app:
        rows = []
        for a in app.Session.Accounts:
            rows.append({'sender': str(a.SmtpAddress), 'display_name': str(a.DisplayName),
                         'account_type': int(a.AccountType)})
        return {'ok': True, 'accounts': rows, 'evidence': 'OUTLOOK_SESSION',
                'delivery_tested': False, 'reads_message_bodies': False}


def prepare(request):
    sender = address(request['sender'])
    to = recipients(request['to'])
    subject, body = request['subject'], request['body']
    if not isinstance(subject, str) or not subject or '\n' in subject or '\r' in subject:
        raise ValueError('Assunto inválido.')
    if not isinstance(body, str) or not body:
        raise ValueError('Texto da mensagem ausente.')
    if request.get('attachments'):
        raise ValueError('Anexos ainda não suportados por este fluxo.')
    with active_outlook() as app:
        account = choose_account(app.Session.Accounts, sender)
        folder = account.DeliveryStore.GetDefaultFolder(16)  # olFolderDrafts
        mail = folder.Items.Add('IPM.Note')
        mail.SendUsingAccount = account
        mail.To = '; '.join(to)
        mail.Subject, mail.Body = subject, body
        if not mail.Recipients.ResolveAll():
            raise ValueError('Destinatário não resolvido pelo Outlook.')
        digest = fingerprint(mail, sender)
        mail.Save()
        draft_id = str(uuid.uuid4())
        receipt = {'draft_id': draft_id, 'sender': sender, 'to': to,
                   'state': 'DRAFT_REVIEW_REQUIRED', 'sha256': digest,
                   'entry_id': str(mail.EntryID), 'store_id': str(folder.StoreID),
                   'created_at': datetime.now(timezone.utc).isoformat()}
        atomic_json(journal_path(sender, draft_id), receipt)
        return {'ok': True, 'draft_id': draft_id, 'sender': sender,
                'to': to, 'sha256': digest, 'state': receipt['state'], 'sent': False}


@contextlib.contextmanager
def exclusive(path):
    with path.open('x'):
        pass
    try:
        yield
    finally:
        path.unlink()


def send(request):
    if request.get('confirmed') is not True:
        raise ValueError('Falta a ordem explícita do operador para enviar este rascunho.')
    path = journal_path(request['sender'], request['draft_id'])
    # One worker at a time for this reviewed draft, even across local processes.
    lock = path.with_suffix('.lock')
    with exclusive(lock):
            receipt = json.loads(path.read_bytes())
            if receipt['state'] != 'DRAFT_REVIEW_REQUIRED':
                raise ValueError('Envio já iniciado ou concluído; repetição automática recusada.')
            if request.get('expected_sha256') != receipt['sha256']:
                raise ValueError('A confirmação não corresponde ao rascunho revisado.')
            with active_outlook() as app:
                choose_account(app.Session.Accounts, receipt['sender'])
                mail = app.Session.GetItemFromID(receipt['entry_id'], receipt['store_id'])
                if fingerprint(mail, receipt['sender']) != receipt['sha256']:
                    raise ValueError('O rascunho mudou; revise novamente antes de enviar.')
                receipt['state'] = 'SUBMISSION_STARTED_UNCERTAIN'
                atomic_json(path, receipt)
                # A failure after this point must never trigger an automatic retry.
                mail.Send()
                receipt['state'] = 'SUBMITTED_TO_OUTLOOK_NOT_DELIVERY_CONFIRMED'
                atomic_json(path, receipt)
                return {'ok': True, 'state': receipt['state'], 'sender': receipt['sender'],
                        'draft_id': receipt['draft_id'], 'delivery_confirmed': False}


def main():
    request = json.load(sys.stdin)
    op = request.get('operation')
    try:
        if op == 'status':
            result = status()
        elif op == 'prepare':
            result = prepare(request)
        elif op == 'send':
            result = send(request)
        else:
            raise ValueError('Operação inválida.')
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as exc:
        # Do not serialize COM/server errors that might echo content or credentials.
        text = str(exc) if isinstance(exc, (ValueError, FileExistsError)) else 'Outlook indisponível; confira a janela e o perfil.'
        print(json.dumps({'ok': False, 'error_type': type(exc).__name__, 'error': text}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    sys.exit(main())
