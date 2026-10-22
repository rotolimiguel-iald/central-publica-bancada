"""Append this measured delivery to every affected local memory, with byte backups."""
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from record_universe_delivery import append, HERE, CANON, CENTRAL


def main():
    receipt = Path(sys.argv[1]).resolve()
    assert receipt.parent == (HERE / 'state').resolve()
    record = json.loads(receipt.read_text(encoding='utf-8'))
    assert record['status'] == 'PASS' and record['gw_unchanged']
    for name, pin in record['installed_sha256'].items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == pin
        assert hashlib.sha256((CANON / name).read_bytes()).hexdigest() == pin
    generation = hashlib.sha256((HERE / 'static/universe-map.js').read_bytes()).hexdigest()
    marker = 'TGL_UNIVERSE_EDUCATIONAL_MAP_' + generation[:16]
    body = f'''## {datetime.now():%d/%m/%Y %H:%M} — Universo educativo, mapa livre + percurso guiado

[INPUT] O operador pediu que o sistema funcione como um programa de curso astrofísico/cosmológico, mostrando matéria bariônica, matéria escura, energia escura, CMB, expansão e estruturas, para facilitar a interação. Escolheu explicitamente “Mapa livre + percurso guiado”.

[REAL — interface instalada] Entrada http://127.0.0.1:18766/explore, oito temas com questões, explicações, experiências, fontes primárias e links aos laboratórios existentes. Navegação livre, Anterior/Próximo, marcação explícita de leitura e progresso no navegador. O atalho TGL conserva seu alvo launch.py e passa a abrir o mapa se Cosmos responder; fallback para GW preservado. Menus Cosmos/GW retornam ao mapa. Apenas Cosmos reiniciou; banco GW não reiniciado.

[REAL / DIDÁTICO] Diagrama interativo de frações de densidade, histórico logarítmico em 1+z, presets de época e controles Ωb/Ωc/Ωr; ΩΛ por fechamento. Modelo FLRW plano idealizado: matéria a^-3, radiação a^-4, Λ constante. Valores arredondados de ensino, domínio z0..100000, sem idade física, formação, perturbações ou recombinação calculada. Frações não são regiões espaciais. Fonte matemática WMAP e demais fontes primárias em EDUCACAO_FONTES.md/static/cosmos-lessons.js. Este módulo não redefine a Ωm agregada do V3 nem fornece espectros TGL. Sem novo sigma ou mudança do gate.

[REAL — verificação] 67 testes Python e 7 testes Node aprovados; rotas instaladas conferidas byte a byte, geração científica preservada {record['scientific_generation_unchanged']}, cálculo V3 padrão idêntico ao recibo anterior. UI conferida: oito temas, percurso/progresso após reload, z1100 e z10000, recusa de composição inválida e recuperação. Revisão independente achou e foram corrigidos dois bugs: histórico velho após sequência redshift inválido→alterar composição→redshift válido; link interno recarregando e perdendo cenário. Fluxo corrigido conferido no navegador. Valores pequenos positivos são mostrados como <0,0001%, sem anunciar zero exato.

[REAL — preservação] GW {record['gw']['loaded_files']}/{record['gw']['total_files']} arquivos, {record['gw']['resident_bytes']} bytes, mesmo load_id {record['gw']['load_id']} e hashes. Memórias com backup imediato de bytes e append atômico. App local TGL somente; conversa pública/iOS/Android não modificados, builds não aplicáveis. Código por agentes locais: modelo didático/testes, roteamento/launcher, fontes primárias; coordenação: integração visual, correções, instalação e verificação. Nenhuma nova chamada externa Kimi/MiMo/DeepSeek nesta entrega.

[OPEN] Temas CMB/estruturas estão organizados para ensino; mapas e Cℓ CMB, catálogos 3D, crescimento/lentes ainda não foram conectados a essa interface. BAO e GW usam os laboratórios reais já existentes. Voz, integração de todas as sondas e teste global D10 seguem no planejamento anterior.

Guia: `{CANON / 'MAPA_EDUCATIVO.md'}`. Recibo: `{CANON / 'state' / receipt.name}`, SHA256 {hashlib.sha256(receipt.read_bytes()).hexdigest()}. Originais científicos intactos.
'''
    for root in (HERE, CANON):
        for name in ('MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'PLANO_UNIVERSO_RESIDENTE.md', 'DESENHO_DO_COCKPIT.md'):
            append(root / name, body, marker)
    for name in ('TGL_ATLAS.md', 'TGL_INDICE_VIVO.md', 'TGL_CORE_MEMORY.md'):
        append(CENTRAL / 'memory' / name, body, marker)
    print(marker)


if __name__ == '__main__':
    main()
