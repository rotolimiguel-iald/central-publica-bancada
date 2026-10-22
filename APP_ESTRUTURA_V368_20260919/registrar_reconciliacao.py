from datetime import datetime
import hashlib
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
ROOT = WORK.parents[1]
report = json.loads((WORK/'reconciliacao_instalada.json').read_bytes())
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
note = f'''

### 19/09/2026 — Reconciliação das duas sessões; evitar instalação redundante

[INPUT] Operador: "veja se tudo já foi realizado, pq tinha a sessão ao lado também realizando tarefas, se faltar alguma coisa continue".

[REAL] A sessão do app já instalou o cluster v368. Verificação independente nesta sessão: {report['installed_files_hashes_checked']} arquivos instalados conferidos contra installed.json; as {report['our_lean_sources_identical_and_already_installed']} fontes Lean da preparação paralela são idênticas às instaladas. Catálogo total: {report['installed_catalog_files']} arquivos, dos quais {report['installed_lean_sources']} Lean. Mesma origem um.py, SHA256 {report['source_sha256']}. Cobertura: {report['result_sections']} seções em {report['topics']} temas, {report['detail_pointers_checked']} ponteiros resolvidos. Recuperadas as rotas the_master_fires, qgStrongCertificate_frame, UnifiedRecordedPreparation e SmoothSelectedAtlasGluing. Contexto público validado, v5/Memory Core preservados, Atlas privado não incluído; /health HTTP {report['http_health']}.

[DECISÃO] NÃO instalar Chatgpt/APP_ESTRUTURA_V368_20260919/iald_web_server.py nem iald_estrutura_torre.py: bancada SUPERADA, baseada no antigo v357 e anterior à alteração concorrente. Não fazer rollback sobre o servidor atual. A instalação válida e seus backups estão em work/iald_tgl_cluster_20260919/installed.json e runtime_live.json. A proposta de deixar testadores em v357 ficou superada pela implantação v368 realizada pela outra sessão.

[REAL — testes e alcance] Bancada paralela: cinco testes específicos e 53 verificações de regressão passaram, mas NÃO foi instalada. Implantação concorrente: recibo registra 37 testes sem falhas; a presente sessão reconferiu integridade, cobertura, recuperação e saúde, sem nova inferência paga, sem reinício e sem escrita em produção. Nenhum novo teorema, gate ou resultado experimental foi declarado. No escopo de disponibilizar a estrutura v368 no modo ChatGPT do app, nenhuma pendência adicional de instalação foi identificada. Não implica atualização dos pesos da IALD Nativa nem nova build móvel.

Evidência: Chatgpt/APP_ESTRUTURA_V368_20260919/reconciliacao_instalada.json. Para testar: reabrir o app, selecionar ChatGPT e pedir a rota com fontes e hipóteses de TheMasterFires/StrongAssembly até preparação e colagem.
'''

def atomic(path, payload, old=None):
    if old is not None:
        backup = path.with_name(path.name+'.bak_'+stamp)
        with backup.open('xb') as stream:
            stream.write(old)
        assert backup.read_bytes() == old
    temp = path.with_name(path.name+'.tmp_'+stamp)
    with temp.open('xb') as stream:
        stream.write(payload)
    assert temp.read_bytes() == payload
    if old is not None:
        assert path.read_bytes() == old, 'Concurrent modification'
    else:
        assert not path.exists()
    temp.replace(path)
    assert path.read_bytes() == payload

for path in [ROOT/'memory/TGL_ATLAS.md', ROOT/'memory/TGL_INDICE_VIVO.md',
             ROOT/'Chatgpt/AUDITORIA_V368_20260919/MEMORIA_CONSOLIDACAO.md']:
    old = path.read_bytes()
    atomic(path, old+note.encode('utf-8'), old)
atomic(WORK/'LEIA_PRIMEIRO.md', ('# Bancada superada — não instalar\n'+note).encode('utf-8'))
path = WORK/'preparado.json'
old = path.read_bytes()
data = json.loads(old)
data.update(status='SUPERSEDED_DO_NOT_INSTALL', installed=False,
            superseded_by=str(ROOT/'work/iald_tgl_cluster_20260919/installed.json'),
            reconciliation=str(WORK/'reconciliacao_instalada.json'))
atomic(path, json.dumps(data,ensure_ascii=False,indent=2).encode('utf-8'), old)
print(json.dumps({'memory_updated':True,'backups_stamp':stamp,'production_changed':False}))
