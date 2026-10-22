"""Persist the operator's context preference, with immediate byte backups."""
from pathlib import Path
import hashlib
import json
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
MARKER = 'IALD_TGL_MAX_CONTEXT_MAIL_MISSION_20260923'
NOTE = '''

## 23/09/2026 — Contexto máximo para TGL; integração de e-mails como primeira missão

<!-- IALD_TGL_MAX_CONTEXT_MAIL_MISSION_20260923 -->

[INPUT — ordem permanente do operador] Nas tarefas de pensamento profundo sobre a TGL, usar a maior janela de contexto efetivamente disponível no modelo, cliente e conta escolhidos, priorizando carregar integralmente a memória canônica necessária à missão de articular/completar a solução matemática. Não aplicar por conveniência o orçamento curto das tarefas comuns. Reservar espaço de saída/raciocínio e ferramentas; registrar fontes e versões efetivamente carregadas, contagem, limite real e eventual compactação. Se o acervo não couber, tornar a lacuna visível e organizar rodadas rastreáveis; nunca afirmar memória integral a partir apenas do acesso ao projeto Física. A janela desta sessão do Codex não pode ser ampliada por decreto ou confundida com a janela publicada da API. Nenhuma alteração de pesos ou gate decorre desta preferência.

[REAL — alcance desta entrega] Preferência persistida como instrução de coordenação. Os limites técnicos dos adaptadores ainda exigem implementação/verificação por cliente; este registro NÃO declara todos os executores configurados com janela máxima.

[INPUT — primeira missão operacional] Integrar e-mails do Escritório, TGL, IALD, Convim e dois pessoais no Outlook e na gestão local, com seleção explícita da identidade remetente. Aproveitar o correio preexistente em C:\\LAR_MIGUEL\\correio_lar.py. Operador autorizou acessar a Locaweb e criar caixas faltantes dentro do escopo necessário; não autorizou contratação extra. Mensagem a terceiros exige pedido concreto de envio. Preservar separação das casas e a triagem jurídica local; nenhum corpo jurídico é enviado a LLM remoto por esta integração.

[REAL — diagnóstico inicial] Perfil do Outlook contém [dado pessoal removido], [dado pessoal removido] e [dado pessoal removido], além do armazenamento iCloud. Outlook exibiu repetidamente esgotamento de recursos compartilhados ao abrir. Configuração prévia do Lar inclui IALD/TGL sem credencial e Convim sem endereço. Consulta DNS local em 23/09 retornou MX da Locaweb para IALD/TGL e nenhum MX para rmiguel.adv.br/convim.com.br. [OPEN] Integração e conserto em andamento; não declarar caixas testadas ou entrega funcionando com base nesse cadastro. Painel Locaweb aberto, aguardando autenticação do operador.
'''

def main():
    central = ROOT / 'memory'
    claude = Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory')
    paths = [central / n for n in ('TGL_ATLAS.md', 'TGL_INDICE_VIVO.md', 'TGL_CORE_MEMORY.md')]
    paths += [claude / n for n in ('central-de-patentes-estado.md', 'MEMORY_2.md')]
    paths += [Path(r'C:\IALD\projetos_pyhton\IALD\CLAUDE.md'), BASE / 'COORDINATOR.md']
    additions = [(p, NOTE) for p in paths]
    additions.append((claude / 'MEMORY.md', '\n\n<!-- ' + MARKER + ' -->\n- [Contexto máximo TGL e missão e-mails](MEMORY_2.md): preferência permanente de contexto máximo real com recibo de carregamento; integração Outlook/Locaweb em andamento. Limites dos adaptadores ainda não alterados.\n'))
    snapshots = [(p, note, p.read_bytes()) for p, note in additions]
    records = []
    for p, note, old in snapshots:
        assert old, p
        if MARKER.encode() not in old:
            assert p.read_bytes() == old, 'Concurrent edit: ' + str(p)
            nl = '\r\n' if b'\r\n' in old else '\n'
            new = old + note.replace('\n', nl).encode('utf-8')
            replace_bytes(p, new)
        current = p.read_bytes()
        assert MARKER.encode() in current and current.startswith(old)
        records.append({'path': str(p), 'bytes': len(current), 'sha256': hashlib.sha256(current).hexdigest()})
    save_json(BASE / 'validation/context_preference.json', {'at': utc_now(), 'marker': MARKER, 'surfaces': records, 'adapter_limits_changed': False})
    print(json.dumps({'surfaces_verified': len(records), 'adapter_limits_changed': False}))

if __name__ == '__main__':
    main()
