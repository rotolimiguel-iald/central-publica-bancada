"""Install this bench's own files into its authorized TETELESTAI home."""

from __future__ import annotations

import hashlib
import shutil
from datetime import datetime
from pathlib import Path

SOURCE = Path(__file__).resolve().parent
TARGET = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL")
FILES = (
    "static/universe-map.html", "static/universe-map.css", "static/universe-map.js",
    "static/cosmos-lessons.js", "static/cosmos-teaching-model.js",
    "tests/test_cosmos_teaching.cjs", "MAPA_EDUCATIVO.md", "EDUCACAO_FONTES.md", "deploy_education.py",
    "cosmology_exports.py", "tests/test_cosmology_exports.py",
    "cosmology_scenarios.py", "cosmology_v3_bridge.py", "workers/cosmology_v3_worker.py",
    "scientific_models/tgl_camb_worker_v3.py", "COSMOLOGY_CANONICAL_ROUTE_AUDIT.md",
    "tests/test_cosmology_scenarios.py", "tests/test_cosmology_v3.py", "tests/test_cosmology_models.py",
    "COSMOLOGIA_V3_CENARIOS.md", "validate_cosmology_v3_live.py",
    "cosmology_runtime.py", "cosmology_server.py",
    "static/cosmos.html", "static/cosmos.js", "static/cosmos.css",
    "data/cosmology/desi_gaussian_bao_ALL_GCcomb_mean.txt",
    "data/cosmology/desi_gaussian_bao_ALL_GCcomb_cov.txt",
    "data/cosmology/ORIGINS.md", "RENDER_E_COSMOLOGIA.md",
    "validate_cosmology_live.py", "record_cosmology_delivery.py",
    "tests/test_cosmology_runtime.py", "tests/test_cosmology_http.py", "tests/test_launcher.py",
    "record_event_delivery.py",
    "U3_EVENTO_OBSERVADO.md", "validate_event_live.py",
    "event_sources.py", "adapters/event_runtime.py", "tests/test_event_sources.py",
    "tests/test_event_runtime.py", "validate_event_runtime.py",
    "validate_resident_live.py", "record_universe_delivery.py",
    "resident_bridge.py", "adapters/resident_worker.py", "tests/test_resident_worker.py",
    "static/universe.html", "static/universe.js", "static/universe.css",
    "models/tgl_ringdown_prediction.py", "models/tgl_ringdown_template.py", "models/model_sources.json",
    "copy_scientific_models.py", "PLANO_UNIVERSO_RESIDENTE.md", "TIME_SOURCE_AUDIT.md",
    "stack/BRIEF_V4_KIMI_RAM.md", "stack/BRIEF_V4_MIMO_DOMAINS.md",
    "stack/kimi_ram.request_id", "stack/mimo_domains.request_id",
    "stack/kimi_ram.result.json", "stack/mimo_domains.result.json", "stack/STACK_V4_REVIEW.md",
    "app.py", "data_lab.py", "treatment.py", "treatment_coverage.py", "gpu_status.py", "hdf5_bridge.py", "adapters/hdf5_reader.py",
    "launch.py", "make_icon.py", "install_canonical.py", "mark_smoke_tests.py",
    "create_desktop_shortcut.ps1", "DESENHO_DO_COCKPIT.md", "TGL.ico",
    "static/index.html", "static/style.css", "static/app.js", "static/protocols.css",
    "static/TGL.svg", "static/favicon.ico", "static/TGL_preview.png", "tests/test_app.py",
    "tests/test_data_lab.py", "tests/test_treatment_coverage.py", "tests/probe_external_storage.py", "SINTETIZADOR_VIVO.md",
    "stack/BRIEF_V2_ARCHITECTURE.md", "stack/BRIEF_V2_DATA_AUDIT.md",
    "stack/kimi_architecture.request_id", "stack/mimo_data_audit.request_id",
    "stack/kimi_architecture.submit.json", "stack/mimo_data_audit.submit.json",
    "stack/kimi_architecture.result.json", "stack/mimo_data_audit.result.json",
    "stack/prepare_v2_requests.py", "stack/STACK_V2_REVIEW.md",
    "stack/BRIEF_V3_GPU_KIMI.md", "stack/BRIEF_V3_DATA_MIMO.md", "stack/BRIEF_V3_UI_GEMINI.md",
    "stack/prepare_v3_requests.py", "stack/kimi_gpu.request_id", "stack/mimo_treatment.request_id",
    "stack/gemini_ui.request_id", "stack/kimi_gpu.submit.json", "stack/mimo_treatment.submit.json",
    "stack/gemini_ui.submit.json",
    "stack/BRIEF_V3_KIMI_AUDIT.md", "stack/BRIEF_V3_MIMO_HDF5_REVIEW.md",
    "stack/kimi_audit.request_id", "stack/mimo_hdf5_review.request_id",
    "stack/kimi_audit.submit.json", "stack/mimo_hdf5_review.submit.json",
    "stack/kimi_audit.result.json", "stack/mimo_hdf5_review.result.json",
    "stack/STACK_V3_REVIEW.md",
)
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_replace(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".new")
    temp.write_bytes(data)
    if temp.stat().st_size != len(data):
        raise OSError(f"Incomplete write: {temp}")
    temp.replace(path)


def install_file(name: str) -> None:
    source = SOURCE / name
    target = TARGET / name
    if not source.is_file():
        raise FileNotFoundError(source)
    if source.resolve() == target.resolve():
        raise ValueError("Source and target are identical")
    data = source.read_bytes()
    if target.is_file():
        if target.read_bytes() == data:
            print(f"unchanged {name}")
            return
        backup = target.with_name(target.name + f".bak_{STAMP}")
        shutil.copyfile(target, backup)
        if sha(backup) != sha(target):
            raise OSError(f"Backup mismatch: {backup}")
    atomic_replace(target, data)
    if sha(source) != sha(target):
        raise OSError(f"Install mismatch: {name}")
    print(f"installed {name}")


def append_memory(name: str, passage: str) -> None:
    path = TARGET / name
    if not path.is_file():
        raise FileNotFoundError(path)
    old = path.read_bytes()
    if passage.encode("utf-8") in old or passage.replace("\n", "\r\n").encode("utf-8") in old:
        print(f"memory already updated {name}")
        return
    backup = path.with_name(path.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    backup.write_bytes(old)
    if backup.read_bytes() != old:
        raise OSError(f"Backup mismatch: {backup}")
    sep = b"\r\n" if b"\r\n" in old else b"\n"
    new = old + sep + passage.replace("\n", sep.decode("ascii")).encode("utf-8") + sep
    atomic_replace(path, new)
    if path.stat().st_size <= len(old):
        atomic_replace(path, old)
        raise OSError(f"Memory did not grow: {path}")
    print(f"appended {name}")


def main() -> None:
    if not TARGET.is_dir() or TARGET.name != "BANCADA_OFICIAL" or TARGET.parent.name != "TETELESTAI":
        raise ValueError(f"Unexpected canonical target: {TARGET}")
    for name in FILES:
        install_file(name)
    append_memory("MEMORIA_CENTRAL.md", """## Acesso Desktop e concepção do cockpit — 27/09/2026

[REAL] O atalho TGL usa `launch.py` na cópia canônica e ícone próprio `TGL.ico`; abre `127.0.0.1:18765` e inicia o servidor local quando necessário. Recursos SVG/favicon servidos pela bancada. Código e testes primeiro verificados no espelho de desenvolvimento. A existência do atalho e sua execução são verificadas separadamente.

[INPUT] O operador quer uma bancada viva de pesquisa do universo, visual e comandada por voz, com consulta ao stack de IAs, inclusive ChatGPT Work da Física. O desenvolvimento deverá transformar perguntas em planos de investigação com fontes, hipóteses, controles e histórico; não multiplicar funções sem necessidade.

[REAL] Pedido de design enviado à fila única da orquestração: request_id `6378069d-56ac-496b-9b85-da8dec268ddc`, job_id `b8fdd40d-862f-440f-b21c-3b2b6c4e262d`. A sessão coordenadora recebeu pedido de contribuições complementares; despacho não é resultado concluído.

[OPEN] Voz conversacional, grafo de prova corrente, execução dos protocolos e integração ao app nativo ainda não foram implementados nesta entrega.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — pedido do operador

O operador pediu acesso rápido “TGL” na área de trabalho, ícone criativo e um painel vivo para pesquisar o universo por voz, após consultar a bancada do stack (Kimi, MiMo, DeepSeek e ChatGPT via orquestração) sobre arquitetura e aprimoramento do pensamento. Foi iniciado o pedido idempotente da fila `6378069d-56ac-496b-9b85-da8dec268ddc`; a implementação local começou pelo launcher/ícone, mantendo originais científicos somente leitura.""")
    append_memory("README.md", """## Abrir pela área de trabalho

O atalho **TGL** da área de trabalho aponta para `launch.py` desta pasta. Ele reutiliza o servidor local existente ou inicia a bancada canônica em segundo plano e abre o navegador em `http://127.0.0.1:18765`. Use `C:\\Python314\\python.exe launch.py --check` para verificar sem abrir a interface. O ícone está em `TGL.ico`; o SVG e favicon ficam em `static/`.""")
    append_memory("MEMORIA_CENTRAL.md", """## Mapa de investigação — 27/09/2026

[REAL] O cockpit ganhou a aba “Pesquisar o universo”: pergunta livre digitada/ditada → localização lexical na torre v368, nos relatórios A/T e no catálogo de dados → trilha exibida com estatuto e fonte → registro append-only no SQLite. Hipótese e resultado refutador são escritos pelo pesquisador; campos vazios aparecem como lacunas. Há leitura em voz alta pelo navegador quando disponível. O processo não roda análise pesada, não aciona IA pela aba e não atribui σ. Oito testes locais passaram no espelho de desenvolvimento antes da instalação canônica; conferir novamente após instalar.

[OPEN] A ligação com grafo formal corrente, execução qualificada dos protocolos, conversa contínua e modelos do stack depende da arquitetura a decidir após as consultas em curso. O mapa lexical é uma primeira interface operacional, não inteligência semântica.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — execução da bancada

O pedido do operador foi traduzido em fluxo inicial de investigação: pergunta por texto/voz, hipótese e possível refutação, localizadores formais/dados/protocolos, histórico imutável por linha. O atalho Desktop foi criado em `OneDrive\\Desktop\\TGL.lnk` e verificado contra launcher/ícone canônicos. Consultas ao stack continuam em fila separada; resultados serão incorporados só após leitura e verificação.""")
    append_memory("README.md", """## Pesquisar o universo

Na aba **Pesquisar o universo**, formule uma pergunta, opcionalmente uma hipótese e um resultado que a contrariaria. “Mapear e registrar investigação” pesquisa no índice formal v368, no inventário de dados locais e nos relatórios A/T já catalogados. Os resultados são localizadores com estatuto, não provas ou testes físicos. A investigação fica no SQLite append-only da bancada; o navegador pode transcrever a pergunta e ler o percurso em voz alta quando suportado.""")
    append_memory("MEMORIA_CENTRAL.md", """## Pareceres do stack e tipagem das alternativas — 27/09/2026

[REAL] Quatro unidades de desenho concluídas na fila única, com pacote `cockpit_design_bundle.json` em `C:\\IALD\\Central de Patentes\\Chatgpt\\IALD_ORQUESTRACAO_20260923\\state\\handoffs`. Executores efetivos: Codex com assistência ChatGPT Work/Física no DRAFT e na síntese, Claude (grafo), Gemini/Antigravity (voz/HCI) e Codex (crítica). A trava de Kimi/MiMo/DeepSeek não estava disponível para esta missão sem etiquetá-la como ORDEM_016; eles não responderam a estas unidades. Nenhum gate ou original foi alterado por essas sugestões.

[REAL] A aba de investigação passou a registrar também explicação rival, efeito instrumental e cálculo/medição discriminante, mantendo `EXPLORATORY_NOT_PREREGISTERED`. O documento `DESENHO_DO_COCKPIT.md` consolida as propostas com estatutos. Oito testes passaram no espelho antes desta atualização canônica; conferir a cópia instalada.

[OPEN] O grafo de arestas probatórias, a voz contínua, o kernel corrente e um replay observacional qualificado continuam pendentes; não atribuir-lhes estado de recurso pronto.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — pareceres concluídos

O stack respondeu à consulta de desenho em quatro unidades: Codex+ChatGPT Work, Claude, Gemini/Antigravity e Codex adversarial. As sugestões úteis foram incorporadas ao desenho do cockpit; no programa entrou somente o quadro de hipóteses rivais, efeito instrumental e medição discriminante. Kimi/MiMo/DeepSeek não foram executores destas unidades porque o roteador não permitia travá-los no escopo correto.""")
    append_memory("README.md", """## Alcance atual e próximo passo

A aba de pesquisa organiza hipóteses concorrentes, contraprova e pergunta discriminante; suas buscas são lexicais e a investigação continua exploratória. O desenho de expansão está em `DESENHO_DO_COCKPIT.md`. Voz contínua com IA, grafo de provas corrente e reexecução física de protocolos ainda não são recursos desta versão.""")
    append_memory("MEMORIA_CENTRAL.md", """## Correção lexical ao lado — 27/09/2026

[REAL] O smoke test de ringdown encontrou 1.018 módulos por causa do termo ubíquo `TGL` no namespace. Esse número é erro de busca, não evidência. O filtro foi corrigido, entrou o nono teste de regressão e `inquiry_events` guarda marcações `SMOKE_TEST`/`ERRATUM` sem alterar as linhas antigas. `mark_smoke_tests.py` confere os registros medidos, faz backup SQLite e cria a consulta corretiva uma única vez.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — o número corrigiu o cockpit

No teste da pergunta sobre ringdown, o mapa lexical devolveu indevidamente todos os 1.018 módulos porque o namespace contém `TGL`. Corrigimos o filtro, preservamos o registro antigo e vinculamos uma errata ao novo resultado por evento append-only. Isso impede que um falso elo visual seja lido como relação científica.""")
    append_memory("MEMORIA_CENTRAL.md", """## Verificação final do diário — 27/09/2026

[REAL] `mark_smoke_tests.py` executado uma vez após backup SQLite. A consulta antiga #2 continha 1.018 módulos; a correção #3 contém **zero módulos formais** e um grupo de dados GWTC-3. #2 tem eventos `SMOKE_TEST, ERRATUM` com ponte para #3; #1 e #3 são `SMOKE_TEST`. A API `/api/inquiries` exibiu esses eventos. Nove testes canônicos passaram antes da marcação; o servidor foi recarregado da pasta TETELESTAI.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — verificação da correção

Após a correção: consulta #3 encontrou zero módulos formais para a pergunta de ringdown; a #2 permaneceu no livro com errata vinculada. A cópia canônica foi testada e o atalho continuou apontando para ela. Inspeção visual automatizada da janela não se completou por timeout da ferramenta; testes de código e HTTP foram concluídos.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — fala do operador (transcrição literal desta etapa)

> Isso mesmo, quero um acesso rápido na minha área de trabalho “TGL” (pode ser criativo no ícone), chegou a hora de vincular tudo em um painel interativo, onde eu comande de forma fácil as pesquisas, a função é pesquisar o universo de forma fácil. Use nosso stack ao máximo e peça sugestões a eleX peça sugestão à bancada do stack de como aprimorar seu pensamento, inclusive o meu próprio chatgpt que a sessaonirma de orquestração tem acesso, use tudo pra pensar primeiro em como me deixar com um painel vivo “a lá Tony stark”""")
    append_memory("MEMORIA_CENTRAL.md", """## Laboratório de grandes dados — 27/09/2026

[REAL] Medição Windows: 256 GiB de RAM instalada, 255,49 GiB visíveis e 183,33 GiB livres no início desta etapa. A disponibilidade muda em tempo real; a bancada agora consulta GlobalMemoryStatusEx. Orçamento inicial interativo = mínimo entre 64 GiB e 35% da RAM livre, não limite físico.

[REAL] `data_lab.py` indexa fontes científicas allowlisted sem copiar ou executar originais. Foram encontrados 615 arquivos e 25,15 GiB nos três grupos locais definidos; o KiDS DR4.1 FITS tem 17.712.469.440 bytes, 21.262.011 linhas e 191 colunas escalares numéricas. DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits tem 3.241 linhas e 11 colunas numéricas. O leitor FITS usa seek por linha amostrada, no máximo 1.200 pontos por resposta; texto tabular usa reservatório determinístico, no máximo 1 milhão de linhas examinadas. Isso é visualização de dados, não ajuste TGL nem teste de significância.

[REAL] A bancada lê também `Nós/um_absoluto_forma_canonica.md` e o SHA de `Nós/um.py` em modo somente leitura para expor a cadeia documentada vigente; o índice formal v368 continua identificado como snapshot histórico. A consulta da forma não executa a prova. Catorze testes locais do espelho passaram antes da instalação; confirmar a cópia canônica e a API após instalar.

[OPEN] Não foi localizado nesta varredura um likelihood DESI BAO específico. DESI/VAST é catálogo de vazios, não o likelihood BAO. FITS imagem/HEALPix, HDF5, NPZ/NPY e modelos físicos sobre dados exigem adaptadores próprios; não inferir física de uma dispersão de colunas. Os ~25 GiB são somente as raízes catalogadas, não o total produzido na missão.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — pedido de grandes dados e resposta operacional

O operador perguntou quanto da RAM pode carregar de uma vez e pediu uma bancada visual interativa conectada aos bancos cosmológicos e de partículas já instalados, inclusive exemplos como DESI BAO e os muitos gigabytes produzidos. Medimos a RAM; ligamos a aba de dados a um inventário científico de três raízes e a um leitor FITS/texto de amostra limitada. A forma canônica documental viva é exibida com SHA, mantendo distinto o índice formal histórico v368. O primeiro catálogo DESI acessível é DESI/VAST de vazios; não foi declarado como BAO.""")
    append_memory("README.md", """## Laboratório de grandes dados

Abra **Dados instalados** pelo atalho TGL. A RAM livre é medida em tempo real. Busque um arquivo do catálogo local, escolha duas colunas e clique **Visualizar amostra**. O programa lê cabeçalhos e amostras limitadas; mantém os originais em disco e não envia gigabytes ao navegador. O detalhe **Forma canônica viva da TGL** mostra o SHA do `um.py` e o trecho da forma documental correspondente; não executa esse programa. FITS de tabela e CSV/TXT/DAT numéricos são interativos. FITS de imagem/HEALPix, HDF5, NPY e NPZ aparecem no catálogo, com leitor ainda pendente. O exemplo DESI/VAST é de vazios, distinto de uma likelihood BAO. Gráficos exploratórios não são prova física.""")
    append_memory("MEMORIA_CENTRAL.md", """## Correção e ampliação do laboratório — 27/09/2026

[REAL] O catálogo foi ampliado para a cache canônica de `A Ponte e o Um`, a cache de `Nós` e o snapshot histórico v350, além dos grupos GWOSC/GWTC. A API canônica retornou **1.107 arquivos e 51,64 GiB** no disco catalogado. A soma contém espelhos físicos dos mesmos insumos e não mede observações independentes. RAM livre na checagem de API: 173,63 GiB; orçamento inicial calculado: 60,77 GiB. Ambos variam em tempo real.

[REAL] Consulta HTTP ao FITS canônico DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits devolveu 80 pontos em X/Y. Consulta ao KiDS canônico de 17.712.469.440 bytes devolveu 80 pontos; a tabela declara 21.262.011 linhas. Em ambos os casos o estatuto retornado foi `DATA_PREVIEW_NOT_MODEL_FIT`. A forma canônica documental vigente foi lida via API com 32 seções e SHA do programa vivo; não foi executada pela bancada. O índice v368 permanece um snapshot distinto.

[OPEN] O laboratório ainda não cobre automaticamente todo o acervo nem os formatos FITS imagem, HDF5 e arrays NPY/NPZ. Não se encontrou, nas raízes catalogadas, uma likelihood DESI BAO específica nem se ligou uma previsão quantitativa TGL a um observável desse catálogo. A conexão científica exige unidades, seleção e hipótese explícitas, não apenas gráfico de dispersão.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — entrega operacional dos grandes dados

O atalho TGL passou a abrir a versão com laboratório de dados. O operador dispõe da leitura viva de RAM, inventário das caches canônicas/históricas e gráfico de amostra para tabelas FITS e texto. O teste HTTP confirmou DESI/VAST e KiDS em leitura limitada; 1.107 arquivos/51,64 GiB são volume catalogado com espelhos, não evidências independentes. O programa mostra também a forma canônica documental vigente e o SHA do `um.py`, preservando o original em modo somente leitura. A análise de física não é promovida automaticamente pelo gráfico.""")
    append_memory("README.md", """## Alcance do inventário em 27/09/2026

A instalação indexou 1.107 arquivos e 51,64 GiB nas raízes admitidas; caches canônicas e espelho histórico podem repetir o mesmo insumo. O painel favorece a cache canônica para o exemplo DESI/VAST. Foram verificados por HTTP 80 pontos de um FITS DESI/VAST e 80 do KiDS de 17,7 GB. A RAM disponível e o orçamento inicial mudam durante o uso. Uma likelihood DESI BAO específica e leitores HDF5/arrays/imagens ainda não estão conectados.""")
    append_memory("MEMORIA_CENTRAL.md", """## Adendo de inventário GW e arrays — 27/09/2026

[REAL] O catálogo passou a cobrir também os posteriores públicos e a strain da bancada 013BIS. A API após reinício retornou **1.348 arquivos e 71,97 GiB** no disco das raízes admitidas, incluindo 65 arquivos no grupo de posteriores públicos e 176 no grupo strain 013BIS. Este valor soma caches canônicas e espelho histórico, com duplicações possíveis; não mede volume de dados estatisticamente independentes.

[REAL] Os 581 arrays `.npy` do snapshot v350 foram inspecionados por cabeçalho; todos tinham layout legível pelo novo leitor de amostras limitado. Para arrays complexos, a interface oferece componentes real, imaginária e módulo sem importar NumPy. Uma consulta HTTP ao array canônico devolveu 30 pares real/imaginário com estatuto `DATA_PREVIEW_NOT_MODEL_FIT`. Quinze testes da instalação passaram.

[OPEN] Arquivos HDF5 de ondas gravitacionais são catalogados, mas ainda não podem ser plotados nesta interface; FITS imagem/HEALPix e NPZ também aguardam leitores. A procura por nomes de BAO/KATRIN/NuFIT no acervo consultado não identificou um banco específico para vincular. A ausência nesta varredura não demonstra ausência no computador inteiro. A forma canônica é apresentada como documento vivo com SHA, sem reexecutar o `um.py` e sem inferir previsão TGL a partir de qualquer coluna arbitrária.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — ampliação dos bancos catalogados

Após o teste DESI/VAST e KiDS, incluímos posteriores e strain de ondas gravitacionais e um leitor de arrays NumPy reais/complexos por amostragem. A API instalada retornou 1.348 arquivos/71,97 GiB, com possíveis cópias repetidas. Um array complexo do cache canônico produziu 30 pontos sem NumPy e sem carga integral. HDF5, FITS imagem e NPZ continuam visíveis no catálogo com leitor pendente; não foram anunciados como dados já analisados.""")
    append_memory("README.md", """## Correção do alcance atual

Depois da ampliação GW/NumPy, o catálogo atual soma **1.348 arquivos e 71,97 GiB** em disco, incluindo espelhos que podem repetir insumos. Tabelas FITS, texto tabular e arrays `.npy` numéricos/complexos são visualizáveis em amostras limitadas. O texto anterior que dizia “NPY pendente” é histórico; esta seção o corrige. HDF5, NPZ e FITS imagem ainda requerem adaptadores. O programa não atribui σ, ajuste físico ou concordância com a TGL ao simples gráfico de colunas.""")
    append_memory("MEMORIA_CENTRAL.md", """## DESI BAO localizado após ampliação da busca — 27/09/2026

[REAL] A busca anterior por BAO cobria as caches da bancada; busca em toda `C:\\IALD` localizou `C:\\IALD\\Artigo\\frente_alpha\\desi_gaussian_bao_ALL_GCcomb_mean.txt` e seu par `_cov.txt`. São 13 medições (z, valor, tipo DV/DM/DH sobre r_s) com covariância 13×13. O novo adaptador exige as duas fontes, valida dimensões/diagonal/simetria e devolve as 13 medições com barras visuais √Cii. Termos fora da diagonal permanecem na matriz, sem χ² ou ajuste TGL efetuado. Isso corrige a nota anterior “não localizado”, preservada como estágio histórico da varredura.

[REAL] O painel agora escolhe o DESI BAO como primeiro gráfico, quando disponível. A varredura em `C:\\IALD\\data\\nufit` encontrou uma página HTML v6.0 de NuFIT, não uma tabela numérica de ajuste. `C:\\IALD\\data\\planck` não apresentou arquivos nesta checagem. A ausência de tabela NuFIT numérica não é ausência de resultados de neutrino no acervo inteiro.

[OPEN] Falta uma previsão TGL tipada nos observáveis DV/DM/DH sobre r_s e um cálculo com a covariância completa para confrontar DESI BAO com hipótese rival. Um gráfico com barras é leitura de dados, não confirmação da teoria.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — correção DESI BAO

O operador citou DESI BAO como exemplo de banco que deveria abrir ao vivo. A primeira varredura das caches não o encontrou; a busca ampliada localizou a média e covariância originais em `Artigo\\frente_alpha`. O laboratório recebeu um leitor específico das 13 medições e da matriz 13×13, com barras diagonais e tipos DV/DM/DH, sem atribuir ajuste ou σ TGL. A página NuFIT local encontrada é HTML de referência, não tabela numérica integrada.""")
    append_memory("README.md", """## DESI BAO agora ligado ao gráfico

A nota histórica que dizia “likelihood DESI BAO não localizada” foi corrigida: o par de arquivos está em `C:\\IALD\\Artigo\\frente_alpha`. A aba **Dados instalados** abre por padrão as 13 medições BAO; cores distinguem DV, DM e DH sobre r_s e barras mostram √ da diagonal da covariância. A matriz completa fica preservada na fonte e ainda não entra em um χ². Este painel lê os dados em modo somente leitura; uma previsão TGL nesses observáveis precisa ser definida antes de inferir concordância física.""")
    append_memory("MEMORIA_CENTRAL.md", """## Correção ao lado: modelo BAO D9 já existia — 27/09/2026

[REAL] A API da bancada após adicionar o par DESI BAO retornou **1.350 arquivos** e 71,97 GiB arredondados, 13 medições com tipos DV/DM/DH e covariância correspondente. A varredura seguinte achou `C:\\IALD\\Artigo\\frente_alpha\\tgl_multiprobe_v3.py`: `load_desi_dr2_BAO` (linha 969), `model_BAO_observables` e `test_D9_desi_dr2` (linha 1086) JÁ calculam previsões TGL/ΛCDM e χ² com covariância 13×13, ajustando Ωm e r_d. Portanto a nota anterior “falta uma previsão TGL tipada” estava ERRADA; o que falta é ligar esse executor existente à bancada com dependências/hipóteses verificadas e leitura visual dos resultados.

[OPEN] O D9 de publicação usa `sqrt(abs(Δχ²))` como “tensão σ”; essa transformação isolada não certifica significância para modelos não aninhados. A bancada não executa D9 nesta entrega. Seu gráfico BAO mostra somente observações e erros diagonais; o código existente e seu SHA são apresentados como localizador, sem promover resultado estatístico. A distinção entre ligar código e validar inferência física fica explícita.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — elo BAO já derivado

A crítica do operador contra funções redundantes foi aplicada: depois de abrir os dados DESI BAO, localizamos a rota D9 já escrita em `tgl_multiprobe_v3.py`. Ela contém o modelo observacional e o χ² completo; não criamos uma segunda física BAO no painel. Acrescentamos um localizador com SHA da fonte existente. Falta integrar sua execução e examinar sua inferência estatística, especialmente a conversão de Δχ² em σ.""")
    append_memory("README.md", """## Correção: a previsão BAO existe

A frase anterior “uma previsão TGL nesses observáveis precisa ser definida” era incorreta. A implementação D9 já existe em `C:\\IALD\\Artigo\\frente_alpha\\tgl_multiprobe_v3.py`, com DV/DM/DH, β fixo, ajuste de Ωm/r_d e χ² usando a covariância completa. O painel agora aponta para essa fonte com SHA, mas ainda não a executa. O gráfico inicial permanece descritivo; não interprete √|Δχ²| como σ confirmado sem uma calibração estatística apropriada.""")
    append_memory("MEMORIA_CENTRAL.md", """## Laboratório visual interativo — 27/09/2026

[REAL] O gráfico de amostras passou a ter zoom sob o cursor, arraste, leitura do ponto próximo, filtros DV/DM/DH para BAO, recenter e exportação JSON com fonte, método e estatuto. A RAM livre no painel atualiza periodicamente sem reindexar os arquivos. Filtros e zoom só alteram a visualização; a exportação conserva todos os pontos amostrados. O conjunto correlacionado DESI continua definido pela covariância completa na fonte, ainda sem execução D9 nesta bancada.

[INPUT] O operador autorizou novas unidades do stack para avançar o programa; Kimi foi escolhido na prévia para arquitetura e MiMo para revisão de dados, com missão nomeada `TGL_BANCADA_OFICIAL` e uma chamada por unidade. Recibos e resultados efetivos ficam na pasta `stack` do espelho de desenvolvimento; não promover respostas de modelos a prova física.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — avanço do painel e distribuição

O operador pediu um programa TGL mais moderno e mais contribuições do stack, especialmente Kimi. Ampliei somente a missão autorizada da bancada no controle de execução, preparei unidades Kimi/MiMo e acrescentei interação científica ao gráfico: zoom, navegação, leitura de ponto, camadas BAO e exportação de amostra rastreável. A implementação foi testada primeiro no espelho, preservando os originais da Física.""")
    append_memory("README.md", """## Exploração visual

Em **Dados instalados**, use a roda do mouse para ampliar em torno do cursor, arraste para mover e dê duplo clique para recentrar. Passe o cursor sobre um ponto para ler seus valores. Em DESI BAO, DV/DM/DH podem ser ocultados por camada sem alterar a matriz de covariância ou a amostra exportada. **Exportar amostra** grava no seu navegador um JSON dos pontos limitados e sua proveniência; não é um ajuste de modelo. A RAM livre atualiza a cada 15 segundos enquanto a aba está visível.""")
    append_memory("MEMORIA_CENTRAL.md", """## Stack v2 e leitura D9 histórica — 27/09/2026

[REAL] Kimi K3 e MiMo 2.6 Pro concluíram as unidades da bancada com seleção travada e memória comum em modo maximum. Respostas e recibos foram copiados para `BANCADA_OFICIAL/stack`; seu estatuto é `[DECLARADO]` até conferência. A UI incorporou inspeção da covariância DESI BAO 13×13 com pares e correlações. A API do relatório D9 histórico lê `multiprobe_v3_report_20260522_135856.json`: χ² LCDM 10.282954002572456, χ² TGL 10.283105223867262, Δχ² +0.0001512212948053815. Esses valores são do **relatório de 22/05/2026**, não nova rodada nem confirmação física; a interface não expõe seu `effective_tension_sigma` como significância. O relatório não fixa o hash do script que o produziu. Para detalhes, ver `stack/STACK_V2_REVIEW.md`.

[OPEN] A execução do D9 permanece não ligada: o Python do servidor não tem SciPy e a instalação de wheels PyPI no `.venv` isolado falhou por SSL EOF. O ambiente foi criado em TETELESTAI, sem pacotes instalados; não foi alterado o Python global. HDF5 e FITS imagem continuam sem leitor. Nenhum gate foi movido por estes recursos da bancada.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — pareceres Kimi/MiMo e ligação do relatório D9

O operador pediu aceleração com o stack, dando peso ao Kimi. Kimi e MiMo foram executados uma vez cada, responderam e tiveram os pareceres registrados com recibos. A bancada passou a tornar visível a correlação entre todas as 13 medições BAO e a ler o relatório D9 já existente, sem reexecutá-lo nem transformar a antiga conversão de Δχ² em σ. Uma tentativa de instalar dependências oficiais em ambiente isolado falhou por erro TLS; o bloqueio ficou explícito.""")
    append_memory("README.md", """## Covariância e D9 histórico

Na aba **Dados instalados**, o mapa 13×13 mostra correlações de DESI BAO. Clique em uma célula para ler observáveis, redshifts, `Cij` e correlação, com hashes dos arquivos de média e covariância. O painel **D9 · relatório de ajuste existente** lê χ² e parâmetros do relatório histórico de 22/05/2026; mostra Δχ² com sinal e origem, sem converter em σ. Isso não é reexecução atual do D9. A instalação isolada das dependências para reexecução falhou por SSL na origem PyPI; consulte `stack/STACK_V2_REVIEW.md` para o limite e os próximos elos.""")
    append_memory("MEMORIA_CENTRAL.md", """## Verificação da bancada instalada — 27/09/2026

[REAL] Após instalar no diretório canônico, 17 testes da bancada passaram. `node --check` aprovou o JavaScript; a API HTTP `/api/lab/bao-report` devolveu o relatório histórico validado. Inspeção visual do painel no navegador confirmou o mapa de correlação 13×13, leitura da célula DM/DH em z=0,51, filtro de DV alterando 13 para 12 pontos e retorno a 13, além dos cartões D9 com os χ² do relatório. Servidor canônico reiniciado e atalho TGL preservado.

[LIMITAÇÃO] A suíte completa da orquestração não concluiu nesta etapa; três testes focados do novo escopo de missão e do travamento de provedor passaram. O D9 ao vivo e HDF5 continuam pendentes por dependências indisponíveis no ambiente isolado; o erro de instalação foi TLS, não falha demonstrada do código científico. Estes testes de interface não movem o gate matemático nem dão significância observacional.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — verificação instalada

A cópia canônica da bancada passou 17 testes, verificação sintática do JavaScript e leitura HTTP do relatório D9. Naveguei no painel: correlação BAO e seus valores por célula, filtro de DV e cartões do ajuste histórico funcionaram. Kimi/MiMo tiveram resultados registrados com revisão crítica; permanecem pareceres, não provas. A reexecução D9 e o leitor HDF5 seguem abertos porque faltam bibliotecas no Python isolado e a tentativa de instalação foi interrompida por erro TLS.""")
    append_memory("MEMORIA_CENTRAL.md", """## Primeira camada GPU e tratamento de fontes — 27/09/2026

[REAL] A RTX 5090 foi medida por `nvidia-smi`: 32607 MiB totais, ~4,1 GiB livres no instante de medição, com `llama-server` ativo. A bancada agora consulta telemetria sem reservar VRAM. A interface ganhou renderização de pontos em WebGL2 sobre eixos/barras Canvas2D, com fallback Canvas2D, detecção de perda de contexto e seletor de GPU. A presença de WebGL2 no código ainda requer observação visual no navegador para confirmar o adaptador real.

[REAL] O contrato `TGL_TREATMENT_V1` fornece registro por fonte allowlisted: formato, tamanho, mtime, impressão SHA-256 parcial das bordas explicitamente NÃO equivalente a hash integral, colunas/unidades conhecidas ou UNKNOWN, estado do adaptador, qualidade e estatuto estatístico. Para DESI BAO, o par média/covariância é validado e ligado por hashes integrais separados; independência entre observações não é presumida. HDF5/NPZ/imagem sem leitor ficam `ADAPTER_PENDING`, sem fabricação de tratamento. Vinte testes passaram no espelho com leitura DESI autorizada.

[INPUT] O operador quer um sintetizador vivo alimentado por todos os bancos locais, com GPU renderizando durante a investigação. Esta entrega é a primeira camada, não a normalização completa de todos os repositórios nem execução física de todos os protocolos.

[OPEN] Integrar leitores HDF5, FITS imagem, NPZ, semântica por sonda, produtos derivados e índices incrementais antes de dizer que todos os bancos estão tratados. Confirmar WebGL2/adapter no navegador e a API canônica depois da instalação. Nenhum σ novo, gate ou confirmação física resulta da renderização.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — pedido de GPU e tratamento universal

O operador pediu GPU renderizando ao vivo e tratamento de todos os bancos antes da síntese TGL. Medimos RTX 5090 com ~4,1 GiB livres e preservamos processos GPU existentes. Foram preparadas e submetidas uma unidade Kimi de arquitetura, uma MiMo de contrato de dados e uma Gemini de interface, cada uma com recibo estável. Todas terminaram sem parecer: cliente Kimi falhou; MiMo não acessou DPAPI; Gemini detectou inventário Antigravity alterado. Nenhuma foi reenviada ou substituída por falsa resposta. Localmente, a bancada recebeu camada WebGL2/fallback e contrato de tratamento por fonte, sem editar originais científicos.""")
    append_memory("README.md", """## GPU e dados tratados — primeira camada

Na aba **Dados instalados**, a chave **GPU WebGL2** desenha os pontos no navegador; eixos e barras permanecem em Canvas2D. Se WebGL2 falhar ou perder contexto, o gráfico volta ao Canvas2D e exibe o estado. A telemetria NVIDIA mostra VRAM livre/total, sem reservar GPU nem parar o modelo local. Cada fonte selecionada recebe um registro `TGL_TREATMENT_V1` com esquema, unidades explícitas ou UNKNOWN, impressão parcial e qualidade. O par DESI BAO conserva seus dois hashes integrais e sua covariância correlacionada. Fontes HDF5/NPZ/FITS imagem continuam identificadas como adaptador pendente: inventário não é leitura científica. A amostra gráfica permanece limitada e não é um ajuste da TGL.""")
    append_memory("MEMORIA_CENTRAL.md", """## Correção ao lado: HDF5 por fatias e GPU visualmente conferida — 27/09/2026

[REAL] A captura da aba **Dados instalados** mostrou WebGL2 via ANGLE/NVIDIA GeForce RTX 5090 D3D11. Uma primeira versão ocultou eixos porque a regra CSS global dava fundo opaco ao canvas sobreposto; o fundo foi corrigido para transparente. A captura posterior mostrou pontos GPU, eixos e barras simultaneamente; o seletor Canvas2D também foi inspecionado. O status de hardware vem do navegador e a VRAM de `nvidia-smi`, não de estimativa.

[REAL] Foi localizado um ambiente WSL já instalado com h5py 3.16.0, NumPy 2.5.3 e SciPy 1.18.1. O adaptador novo usa esse Python existente somente para leitura HDF5 por hiperslab limitada, com resposta JSON e limite de 1200 pontos, sem instalar pacotes ou alterar o arquivo. Um GWOSC HDF5 de 1,1 MB expôs `/strain/Strain` e máscaras; amostra de 24 posições encontrou somente 1 par finito (não interpretar como 24 pontos úteis). Um `mcmc_chain.h5` de ~10 MB devolveu 24 pares finitos em 24 posições. Leitor genérico não atribui semântica física a cada coluna. 21 testes do espelho passaram após a ligação; cópia canônica/API ainda exigem validação posterior.

[CORREÇÃO] A nota imediatamente anterior marcava HDF5 como `ADAPTER_PENDING`; isso era verdadeiro antes desta ligação. Agora HDF5 numérico 1D/2D está disponível quando WSL/ambiente existente funcionam. NPZ e FITS imagem permanecem pendentes; HDF5 com layout não suportado falha visivelmente.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — leitura HDF5 existente reaproveitada

O ambiente científico WSL de outra bancada já continha h5py/NumPy/SciPy. Sem instalar ou alterar esse ambiente, ligamos à bancada oficial um leitor HDF5 de metadados e hiperslabs numéricos limitado a 1200 pontos. Conferimos dois arquivos reais; o GWOSC escolhido tinha quase todas as posições amostradas não finitas, enquanto a cadeia MCMC retornou 24/24 pares. O número de amostras lidas permanece separado do número de pontos finitos exibidos.""")
    append_memory("README.md", """## Correção HDF5

O registro histórico acima diz que HDF5 aguardava adaptador. A partir desta versão, arquivos `.h5` e `.hdf5` com datasets numéricos 1D/2D podem ser descritos e amostrados por fatias via h5py do ambiente WSL já instalado, sem instalar bibliotecas no Python do servidor. A fonte continua somente leitura; o limite é 1200 posições e valores não finitos não viram pontos. Um arquivo listado pode ser recusado se seu esquema não couber no contrato. NPZ e FITS imagem continuam sem leitor nesta bancada. O índice de linhas de uma cadeia não é tempo físico por definição.""")
    append_memory("MEMORIA_CENTRAL.md", """## Sintetizador vivo e cobertura por formato — 27/09/2026

[REAL] A GPU WebGL2/ANGLE da RTX 5090 e o fallback Canvas2D foram inspecionados na interface. HDF5 numérico foi lido por fatias no ambiente WSL científico já existente. A rota `/api/lab/coverage` mede o inventário permitido: 1.350 arquivos, 77.273.689.337 bytes, 1.263 com adaptador disponível para tentativa e 87 pendentes. São contagens de rotas, não validação de esquema, identidade de arquivos ou independência estatística. FITS imagem pode estar entre os 35 FITS catalogados sem ser legível pelo adaptador de tabelas; NPZ permanece pendente. Impressões parciais de borda geram apenas candidatos a duplicata.

[REAL] O espelho passou 24 testes ao ler o par DESI BAO original com autorização de somente leitura. O primeiro teste no sandbox falhou por acesso negado à fonte externa, não por asserção científica; a repetição autorizada passou. O relatório `SINTETIZADOR_VIVO.md` separa ingestão, tratamento, renderização, modelos existentes e inferência. A revisão do stack tem recibos próprios e não muda o gate.

[OPEN] Validar perfis semânticos por sonda, unidades, máscaras e proveniência; implementar NPZ/FITS imagem quando necessários; ligar executores D9/ringdown existentes à bancada com controles. Nenhum sigma, evidência física nova ou fechamento matemático decorre de abrir o gráfico.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — sintetizador vivo com cobertura mensurada

O operador pediu GPU renderizando continuamente e uma camada comum de tratamento antes de consultar todos os bancos. Foram ligadas a RTX 5090 pelo navegador, a telemetria NVIDIA e a leitura HDF5 por fatias. A medição do catálogo distinguiu 1.263 rotas de leitor tentáveis de 87 pendentes entre 1.350 arquivos, sem chamar isso de validação científica individual. Kimi e MiMo receberam novas revisões distintas após as três primeiras unidades falharem; seus pareceres só serão incorporados se houver resposta verificável. A subagente de cobertura entregou código e três testes, revisados na suíte de 24 testes.""")
    append_memory("README.md", """## Sintetizador vivo

Leia `SINTETIZADOR_VIVO.md` para a arquitetura e os limites. `/api/lab/coverage` mostra contagem por formato, rotas de adaptador, candidatos a duplicata por tamanho e impressão parcial e estados explícitos de esquema/independência não verificados. A interface apresenta o resumo junto ao catálogo. Nesta medição houve 1.350 arquivos, dos quais 1.263 têm leitor disponível para tentativa e 87 não. Isso não afirma que 1.263 arquivos foram tratados com sucesso: cada esquema, unidade e máscara exige validação por fonte. A GPU desenha os pontos amostrados, sem pôr os gigabytes do banco na VRAM.""")
    append_memory("MEMORIA_CENTRAL.md", """## Revisão independente do HDF5 e GPU — 27/09/2026

[DECLARADO] Duas unidades distintas do stack terminaram `result_ready`: Kimi crítico da arquitetura GPU/HDF5 (`d53e1319-3886-4113-8e72-11ac5ce340fd`) e MiMo crítico do HDF5 (`62f07895-dae3-4415-8331-b4ca75512a33`). Suas afirmações foram conferidas contra o código antes de aplicar: o leitor não usava só a janela inicial e já preservava pareamento por máscara conjunta, ao contrário de duas hipóteses do parecer MiMo. Os pareceres integrais e a seleção crítica estão em `stack/`.

[REAL] O HDF5 passou a recusar armazenamento externo em dataset, a declarar índice sintético, pares não finitos omitidos e proibição de inferência espectral com stride. Fixture local confirmou a recusa; cadeia MCMC real retornou 24/24 pontos finitos. O documento `stack/STACK_V3_REVIEW.md` distingue falhas corrigidas de riscos ainda não medidos, como uso de VRAM após ciclos de perda de contexto. Nenhuma conclusão física ou gate mudou.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — resultados do stack e correção da leitura

Kimi e MiMo retornaram pareceres técnicos sobre a bancada GPU/HDF5 pela orquestração única. Conferimos suas sugestões com o código real, recusamos hipóteses que não correspondiam à implementação e aplicamos a recusa de datasets HDF5 com armazenamento externo. O preview agora explicita descartes e impede interpretar índice/stride como tempo ou espectro físico. A fixture adversarial de armazenamento externo foi rejeitada; a amostra MCMC permaneceu legível. Nenhum arquivo científico original foi alterado.""")


    append_memory("MEMORIA_CENTRAL.md", """## Universo residente — mudança de produto autorizada, 27/09/2026

[INPUT] O operador corrigiu o produto: quer carregar o banco integral por domínio e investigar interativamente seus dados, o tempo e os efeitos TGL; catálogo de amostras não satisfaz. Autorizou planejamento detalhado e começo da execução com divisão pelo stack. Plano: PLANO_UNIVERSO_RESIDENTE.md, U0–U6.

[REAL] Runtime novo mantém arrays NumPy completos, imutáveis, sem memmap; status mede bytes/RSS/swap, N/N e erros. Manifesto registra GPS, detector, dt, qualidade, fonte e hash do strain decodificado. Min/max de toda a janela preserva picos; bins com gaps têm cobertura explícita. Não é espectro. Quatro testes WSL passaram: navegação após remoção da fixture original, impulso/gap, recusa de armazenamento externo e orçamento insuficiente, carga parcial, modelo existente/controle GR/redshift. A medição real dos 180 caminhos declarados deve ser consultada no recibo posterior de validação, não inferida desses testes.

[REAL] Executor de ringdown anterior foi copiado byte a byte, acompanhado de manifesto e checagem de integridade antes do uso. Interface expõe massa fonte, spin, redshift, evolução e leitura de relógio explícita. Modelo ensemble condicional em painel próprio: não é ajuste ao evento, PSD/DQ/antena e posteriores ainda não foram ligados nesta etapa. beta vem da função científica existente. Atalho abre /universe.

[REAL — fonte lida] TIME_SOURCE_AUDIT.md localiza the_tower_is_time: tempo característico = índice = 1/peso de Markov no objeto JonesTowerData, com interpretação temporal e calibração distinguidas. Localiza também a ponte modular/Killing sob suas hipóteses. Não foi recompilado o kernel nesta rodada. R-A/R-B e outras leituras preservam as hipóteses dos executores.

[DECLARADO] Kimi e MiMo entregaram as unidades novas kimi_ram/mimo_domains, com recibos em stack. STACK_V4_REVIEW.md documenta o aproveitamento crítico: nenhuma equivalência memmap/RAM, descarte silencioso, limiar estatístico ou fórmula física sugerida foi promovida sem conferência. Nenhum original científico ou gate foi alterado.""")
    append_memory("REGISTRO_DAS_CONVERSAS.md", """## 27/09/2026 — ordem de execução do universo residente

> exatamente isso, mantendo os dados carregados com uma interface interativa onde eu possa navegar pelo universo e vasculhar os efeitos diretos da TGL incluindo podendo manipular o tempo, agora que também temos a fórmula do tempo. elabore o planejamento detalhado disso e comece a executar distribuindo as tarefas se for o caso para o nosso stack para economizar seus tokens e vc ficando com o que for mais difícil e exigir mais técnica, enfim, a não ser que seja mais rápido e econômico vc executar tudo (embora eu acredite que não)

Entregas iniciadas: plano U0–U6, sessão RAM integral GWOSC, interface própria /universe, executor ringdown existente preservado e auditoria da fórmula do tempo. Kimi e MiMo concluíram revisões por unidades idempotentes; agentes locais trabalharam na interface e nas fontes. A coordenação integrou backend/contratos e verificou os controles. A validação real posterior mede o que ficou carregado e o desempenho.""")
    append_memory("README.md", """## Universo residente — abrir TGL

A página principal nova é **http://127.0.0.1:18765/universe**, aberta pelo atalho TGL. Selecione ondas gravitacionais e carregue o domínio: o status discrimina os arquivos completos em RAM, erros, bytes/RSS/swap e fontes. Escolha detector/série, mova a janela temporal e reproduza; a curva usa todas as amostras da janela para seu envelope visual. No painel do modelo, selecione explicitamente o relógio e varie massa, spin e redshift para comparar GR/TGL pelo executor científico anterior. O modelo ainda não é ajustado à série selecionada. Máscaras foram carregadas mas ainda não aplicadas ao sinal; os demais domínios aguardam seus perfis.

O plano integral está em PLANO_UNIVERSO_RESIDENTE.md. A fórmula temporal e as hipóteses estão em TIME_SOURCE_AUDIT.md. Recibos por carga ficam em state/resident_runs. Resultados de validação de hardware/dados reais são registrados separadamente dos testes sintéticos.""")


if __name__ == "__main__":
    main()
