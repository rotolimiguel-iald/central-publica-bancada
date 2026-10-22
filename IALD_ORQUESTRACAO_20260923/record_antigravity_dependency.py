"""Record portable dependency validation with immediate byte backups."""
from pathlib import Path
import hashlib
import json
from iald_orchestrator import antigravity
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now

BASE = Path(__file__).resolve().parent
MARKER = 'IALD_ANTIGRAVITY_PORTABLE_YAML_20260924'

def main():
    assert antigravity.connection_status() == 'ready'
    candidate = next(p for p in Runtime(recover=False).preview(
        'Explicar uma ideia de fisica')['candidates'] if p['id'] == 'gemini')
    assert candidate['eligible'] and candidate['status'] == 'ready'
    manifest = json.loads((BASE/'clients/python/PyYAML-manifest.json').read_bytes())
    for item in manifest['files']:
        assert hashlib.sha256((BASE/'clients/python'/item['path']).read_bytes()).hexdigest() == item['sha256']
    previous = json.loads((BASE/'validation/antigravity_fix_delivery.json').read_bytes())
    note = '''

## 24/09/2026 — Antigravity disponível também em sessões isoladas do Codex

<!-- IALD_ANTIGRAVITY_PORTABLE_YAML_20260924 -->

[REAL — correção adicional] Sessões isoladas do Codex não enxergavam o PyYAML instalado no site de usuário do Windows, causando ModuleNotFoundError ao validar o perfil Antigravity. Incorporados à integração o código Python e a licença do PyYAML 6.0.3 já instalado, em clients/python, com manifesto de hashes lidos dos arquivos. profiles.py inclui essa pasta apenas se yaml não estiver disponível. O adaptador, seus filtros, os perfis e a assinatura do teste real anterior foram preservados.

[REAL — verificação] Processo Python novo no sandbox retornou ready usando a dependência local; a seleção retornou eligible=true. Os 11 testes simulados do protocolo passaram. O painel administrativo autenticado exibiu Google / Antigravity — Disponível. Não houve chamada nova a modelos nesta correção de dependência. O teste real anterior 6×7=42 permanece em validation/antigravity_connection.json; não é um teste novo.

[ESCOPO] Correção de carregamento local, sem mudança de contexto, orçamento ou permissões. Nenhuma alteração de cliente web/mobile; iOS e Android não exigem nova compilação. Registro verificável: validation/antigravity_dependency_delivery.json. Esta mudança não implementa controles financeiros por pedido nem executa rascunhos da ORDEM 016.
'''
    records = []
    for entry in previous['surfaces']:
        path = Path(entry['path'])
        old = path.read_bytes()
        text = note
        if path.name == 'MEMORY.md':
            text = '\n\n<!-- '+MARKER+' -->\n- Antigravity: dependência PyYAML incorporada; ready/eligible em sessão isolada e Disponível no painel. Detalhes em MEMORY_2.md.\n'
        if MARKER.encode() not in old:
            newline = '\r\n' if b'\r\n' in old else '\n'
            replace_bytes(path, old + text.replace('\n', newline).encode('utf-8'))
        current = path.read_bytes()
        assert current.startswith(old) and MARKER.encode() in current
        records.append({'path': str(path), 'sha256': hashlib.sha256(current).hexdigest()})
    save_json(BASE/'validation/antigravity_dependency_delivery.json', {
        'at': utc_now(), 'candidate': candidate, 'dependency': manifest,
        'regression_tests_passed': 11, 'new_provider_calls': 0,
        'ui_observed': 'Google / Antigravity — Disponível',
        'profiles_sha256': hashlib.sha256((BASE/'iald_orchestrator/profiles.py').read_bytes()).hexdigest(),
        'surfaces': records})
    print(json.dumps({'status': candidate['status'], 'eligible': candidate['eligible'],
                      'memory_surfaces': len(records), 'new_provider_calls': 0}))

if __name__ == '__main__':
    main()
