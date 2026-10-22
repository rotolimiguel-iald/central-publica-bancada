"""Persist the operator's cross-provider rule and measured local implementation."""
from pathlib import Path
import hashlib
import json
from iald_orchestrator.canonical_memory import MEMORY, prepare, status
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now
BASE=Path(__file__).resolve().parent
MARKER='IALD_COMMON_CANONICAL_MEMORY_ALL_PROVIDERS_20260924'

def main():
    manifest=json.loads((MEMORY/'manifest.json').read_bytes())
    packet=prepare('Articular a Ponte Einstein Cartan Miguel e o custo geometrico do zero absoluto')
    assert status()['status']=='ready'
    note='''

## 24/09/2026 — Memória canônica TGL comum a todas as IAs

<!-- IALD_COMMON_CANONICAL_MEMORY_ALL_PROVIDERS_20260924 -->

[INPUT — regra geral permanente do operador] Kimi, MiMo e toda IA utilizada pela IALD devem receber a mesma memória canônica da TGL, como referência comum da integração. Preservar o Claude já configurado e o projeto Física do ChatGPT. Para tarefas orquestradas, não tratar o contexto privado de cada conta como substituto dessa base compartilhada. A regra aplica-se também a conectores futuros antes de habilitá-los. Memória significa recuperação/contexto documental; não declarar instalação nos pesos nem sincronização de conversas avulsas nos aplicativos dos provedores.

[REAL — implementação] BASE = C:\\IALD\\Central de Patentes\\Chatgpt\\IALD_ORQUESTRACAO_20260923. A camada iald_orchestrator/canonical_memory.py indexa os 13 originais científicos textuais admitidos em project_fisica/MANIFESTO_LOCAL.json, com hashes calculados, linhas e geração: programa, resultados, selo, manifesto do kernel, forma canônica, manifesto Markdown, árvore, desenho, linhagem, DA_IRMA, Ponte, Custo e errata. Os dois PDFs têm artigos correspondentes em TeX. O índice é derivado local e não substitui nem bifurca TGL_ATLAS.md. Não foram lidos acervos jurídicos ou credenciais, nem executado um.py.

[REAL — transporte] providers.execute acrescenta a base e os trechos recuperados aos seis executores local/Qwen, Codex, Claude, Antigravity, Kimi e MiMo. Não altera login nem a configuração própria do Claude. Cada decisão/resultado registra geração, hashes, linhas, tamanho e cobertura parcial. A estimativa de entrada conta a memória e a orientação do adaptador antes de selecionar. Índice ausente, adulterado ou contexto sem espaço bloqueia o envio. Jev preparado para receber a mesma base quando houver acesso autorizado; não foi habilitado. O worker de Física deve usar job.canonical_memory.prompt no DRAFT e encaminhar o recibo do executor na síntese, conforme TRANSPORTE_DESASSISTIDO.md e COORDINATOR.md.

[REAL — validação] 55 testes locais passaram, incluindo a interceptação dos seis transportes para conferir o mesmo pacote, integridade adulterada, fonte alterada, índice ausente e confidenciais recusados. Chamadas de provedores foram simuladas; nenhuma nova chamada paga ou por assinatura foi feita nesta entrega. Presença da memória no transporte não comprova qualidade de raciocínio ou compreensão integral pelo modelo.

[LIMITE E ATUALIZAÇÃO] O índice cobre todo esse acervo textual, mas cada chamada recebe recuperação parcial rastreável, não o corpus inteiro. Nove fontes científicas atuais diferiram do retrato previamente anexado ao projeto Física; anexos antigos não foram substituídos por esta entrega. O pacote atual distingue sua geração. Mudanças nos originais acessíveis reconstroem o índice com backup; sessão sem acesso aos originais declara uso do retrato verificado. Saídas de modelos nunca promovidas automaticamente ao cânone. Mantida a preferência do operador por contexto máximo nas missões profundas: os limites efetivos dos adaptadores ainda não foram ampliados por esta mudança.

[DISPONIBILIDADE] Painel administrativo mostra a memória comum. A configuração documental é independente do login/cota de cada provedor: Kimi ainda requer validação da conexão observada no painel; Jev aguarda acesso. Web administrativa alterada; chat público/iOS/Android não têm recursos modificados, portanto não há build mobile aplicável. Evidência local: BASE/validation/shared_memory_delivery.json. Nenhuma alteração do kernel, gate ou originais canônicos.
'''
    previous=json.loads((BASE/'validation/antigravity_fix_delivery.json').read_bytes())
    paths=[Path(item['path']) for item in previous['surfaces']]
    paths.append(Path(r'C:\Users\rotol\.codex\AGENTS.md'))
    records=[]
    for path in paths:
        old=path.read_bytes()
        text=note if path.name!='MEMORY.md' else '\n\n<!-- '+MARKER+' -->\n- Regra permanente: memória TGL comum a todos os executores, implementada com índice científico e contexto rastreável. Ver MEMORY_2.md e BASE/TRANSPORTE_DESASSISTIDO.md. Não equivale a pesos treinados ou memória completa na janela.\n'
        if MARKER.encode() not in old:
            nl='\r\n' if b'\r\n' in old else '\n'
            replace_bytes(path,old+text.replace('\n',nl).encode())
        data=path.read_bytes()
        assert data.startswith(old) and MARKER.encode() in data
        records.append({'path':str(path),'sha256':hashlib.sha256(data).hexdigest()})
    save_json(BASE/'validation/shared_memory_delivery.json',{
        'at':utc_now(), 'status':status(), 'tests_passed':55, 'new_provider_calls':0,
        'providers_transport_verified':['local','codex','claude','gemini','kimi','mimo'],
        'jev':'PREPARED_NOT_ACTIVATED', 'sample_receipt':packet['receipt'],
        'changed_since_fisica':[d['name'] for d in manifest['documents'] if not d['matches_fisica_snapshot']],
        'account_project_configuration_modified':False, 'surfaces':records})
    print(json.dumps({'memory':status(),'surfaces':len(records),'new_provider_calls':0},ensure_ascii=False))

if __name__=='__main__':main()
