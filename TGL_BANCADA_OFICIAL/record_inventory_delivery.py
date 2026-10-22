"""Preserve the event inventory and append its scope to bench memories."""
import hashlib
import json
from datetime import datetime
from pathlib import Path

from record_universe_delivery import append, CANON

HERE = Path(__file__).resolve().parent
CENTRAL = HERE.parent.parent


def copy_verified(source, target):
    raw = source.read_bytes()
    if target.exists():
        old = target.read_bytes()
        if old == raw:
            return
        backup = target.with_name(target.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as stream:
            stream.write(old)
        if backup.read_bytes() != old:
            raise OSError('Backup failed')
    else:
        old = None
    temp = target.with_name(target.name + '.new_inventory')
    with temp.open('xb') as stream:
        stream.write(raw)
    if temp.read_bytes() != raw:
        raise OSError('Incomplete copy')
    if old is not None and target.read_bytes() != old:
        raise OSError('Concurrent change')
    temp.replace(target)


def main():
    inventory_path = HERE / 'state/EVENT_INVENTORY_018.json'
    inventory = json.loads(inventory_path.read_text(encoding='utf-8'))
    binding_path = HERE / 'state/EVENT_INVENTORY_018_BINDING_8560b710-3ad7-402b-a12e-9a0b1fdf1ad3.json'
    binding = json.loads(binding_path.read_text(encoding='utf-8'))
    digest = hashlib.sha256(inventory_path.read_bytes()).hexdigest()
    if binding['inventory']['sha256'] != digest:
        raise ValueError('Inventory changed after verification')
    counts = binding['recomputed_counts']
    for source in (inventory_path, inventory_path.with_suffix('.md'), binding_path):
        copy_verified(source, CANON / 'state' / source.name)
    marker = 'TGL_EVENT_INVENTORY_018_' + digest
    text = f'''## {datetime.now():%d/%m/%Y %H:%M} — Eventos do perfil residente, ORDEM 018

[REAL — cruzamento documental e reconciliação] Os {counts['resident_files']} arquivos strain do perfil GWOSC correspondem a {counts['resident_event_ids']} identidades de eventos com strain, {counts['distinct_strain_array_hashes']} hashes distintos de arrays e {counts['unique_onsource_detector_interval_pairs']} pares detector×intervalo onsource. Papéis: {counts['files_by_role']}. O inventário original ancora a carga anterior; o recibo de vínculo conferiu {binding['field_comparisons']} campos contra a carga {binding['resident']['load_id']}, sem diferenças. Os hashes grandes são herdados dos recibos, não reprocessados nesta verificação.

[REAL — alcance dos metadados] Há 33 eventos ancorados em metadados GWOSC; GW190910_112807 tem metadados/posterior, sem strain neste perfil. Os 18 produtos posteriores GWTC-3 sobrepõem 12 rótulos; seis adicionais são rótulos de timestamp sem identidade oficial resolvida neste inventário. A união de 39 rótulos não é número de eventos independentes. O JSON também registra produtos posteriores e configurações, que não foram incluídos nos 180 arquivos strain.

[OPEN] Independência científica, seleção/DQ aceitável e poder conjunto exigem o protocolo registrado. INCONCLUSIVE_SYSTEMATICS permanece na análise C6. Inventário, memória, índice e interface não produzem sigma nem movem gate. Nenhum dado original foi modificado.

Artefatos: `{CANON / 'state' / inventory_path.name}` (SHA256 {digest}), relatório de mesmo nome .md e `{CANON / 'state' / binding_path.name}`. São mapas derivados, sem bifurcar o Atlas ou substituir os manifestos científicos originais. A ORDEM 018 é redigida na cadeia Kimi/MiMo/DeepSeek → ChatGPT/Física → Claude Opus, conforme a campanha na Central; sua conclusão não é inferida deste inventário.
'''
    for root in (HERE, CANON):
        for name in ('MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md'):
            append(root / name, text, marker)
    for name in ('TGL_ATLAS.md', 'TGL_INDICE_VIVO.md', 'TGL_CORE_MEMORY.md'):
        append(CENTRAL / 'memory' / name, text, marker)
    print(json.dumps({'marker': marker, 'inventory_sha256': digest}))


if __name__ == '__main__':
    main()
