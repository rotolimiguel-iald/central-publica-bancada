"""Use Outlook's supported Application automation after ROT lookup failed live."""
from pathlib import Path
from iald_orchestrator.safe_files import replace_bytes

base = Path(__file__).resolve().parent
for path in (base / 'mail_stage/correio_outlook.py', Path(r'C:\LAR_MIGUEL\correio_outlook.py')):
    old = path.read_bytes()
    text = old.decode('utf-8')
    text = text.replace('Never launches Outlook or retries sending. JSON requests arrive only through stdin.',
                        'Explicit calls may initialize the existing Outlook profile. Never retries sending.\nJSON requests arrive only through stdin.')
    before = "        # GetActiveObject never creates a hidden instance or a new login prompt.\n        obj = pythoncom.GetActiveObject('Outlook.Application')\n        app = dynamic.Dispatch(obj)"
    after = "        # Outlook can be running without an entry in the Running Object Table.\n        # The official Application class connects to the current default profile.\n        # This explicit call may start Outlook; the caller bounds its execution.\n        app = dynamic.Dispatch('Outlook.Application')"
    normalized = text.replace('\r\n', '\n')
    if before in normalized:
        normalized = normalized.replace(before, after)
        if b'\r\n' in old:
            normalized = normalized.replace('\n', '\r\n')
        replace_bytes(path, normalized.encode('utf-8'))
    elif after not in normalized:
        raise RuntimeError(f'Unexpected source: {path}')
path = base / 'mcp_server.py'
old = path.read_bytes()
new = old.decode('utf-8').replace('Lista remetentes da sessão aberta do Outlook, sem ler mensagens ou senhas.',
    'Lista remetentes do perfil Outlook existente, sem ler mensagens ou senhas.\n\n    Esta chamada explícita pode inicializar o Outlook se necessário.')
if new.encode('utf-8') != old:
    replace_bytes(path, new.encode('utf-8'))
print('Outlook Application activation installed; send guards unchanged.')
