"""Install admin visibility and coordinator instructions with byte backups."""
from pathlib import Path
from iald_orchestrator.safe_files import replace_bytes
BASE=Path(__file__).resolve().parent

def change(relative, old, new):
    path=BASE/relative
    data=path.read_bytes()
    newline='\r\n' if b'\r\n' in data else '\n'
    text=data.decode().replace('\r\n','\n')
    assert text.count(old)==1, relative
    replace_bytes(path,text.replace(old,new).replace('\n',newline).encode())

change('iald_orchestrator/panel.html', '<div id="providers" class="cards"></div>',
       '<div id="memory-status" class="notice">Conferindo a memória canônica da TGL…</div>\n<div id="providers" class="cards"></div>')
change('iald_orchestrator/panel.js', "async function refresh(){try{const s=await api('/status');",
       "async function refresh(){try{const s=await api('/status');const m=s.canonical_memory;const memoryEl=$('memory-status');if(memoryEl)memoryEl.textContent=m?.status==='ready'?'Memória TGL comum ativa · '+m.documents+' fontes científicas indexadas. Cada executor recebe a mesma base e trechos pertinentes; as fontes carregadas ficam registradas na tarefa.':'Memória TGL indisponível ou desatualizada · novos envios exigem verificação.';")
change('iald_orchestrator/jev.py', '    body = {"model": "jev-latest", "state": {"task": prompt},',
       '    from .canonical_memory import prepare\n    memory = prepare(prompt)\n    body = {"model": "jev-latest", "state": {"task": prompt, "canonical_memory": memory["prompt"]},')

note='''

## 24/09/2026 — Memória científica comum em todas as etapas

<!-- IALD_SHARED_TGL_MEMORY_PROTOCOL_20260924 -->

[INPUT — regra permanente do operador] Toda IA utilizada na orquestração deve receber a mesma base canônica da TGL. Preservar a configuração própria já existente no Claude e o projeto Física do ChatGPT. Contexto documental não altera os pesos nem equivale à memória nativa da conta.

[REGRA DO WORKER] Ao obter um pedido não terminal, `job.canonical_memory` contém `prompt` (pedido original com a memória científica recuperada) e `receipt` (geração, hashes, fontes e linhas). Na criação da tarefa Work, transportar esse campo `prompt` integralmente junto do marcador DRAFT e das instruções de preparação. Não reduzi-lo a uma referência a caminho local: Work não lê esse disco. Conservar o recibo no registro de handoff. O resumo preparado por Work não precisa repetir o pacote: o executor recebe novamente a memória pelo adaptador comum. Na síntese, incluir `execution.result.canonical_memory`, para distinguir geração/fontes efetivamente recebidas pelo executor das fontes antigas do projeto. Uma atualização do acervo entre etapas fica visível nesses recibos; não misturar evidências como se fossem a mesma rodada.

[IMPLEMENTAÇÃO] Os seis executores atuais — local/Qwen, Codex, Claude, Antigravity, Kimi e MiMo — passam pela mesma montagem de contexto antes do transporte. Jev, se vier a ser habilitado, também recebe a base no estado da classificação; continua sem acesso neste momento. A estimativa de entrada inclui a memória e a orientação do adaptador; overhead interno do cliente continua desconhecido. Falha de integridade, índice ausente ou espaço insuficiente interrompe o envio. Não remover memória silenciosamente para caber, não aumentar orçamento e não habilitar fornecedor por esta regra.

[ESCOPO] O índice derivado lê somente os 13 arquivos científicos textuais do catálogo já autorizado para Física: programa, resultados, selo, manifesto, forma canônica, árvore, desenho, linhagem, DA_IRMA, os dois artigos em TeX e errata. Os dois PDFs têm os mesmos artigos em TeX. Não copia nem bifurca o Atlas canônico, não inclui acervo jurídico, credenciais ou arquivos confidenciais. Não executa um.py. Mudanças detectadas nos originais acessíveis reconstroem o índice com backups; se os originais não puderem ser consultados pela sessão, o pacote declara uso do retrato verificado, sem afirmar atualidade dos originais. Saídas dos modelos não viram memória canônica automaticamente.

[LIMITE EXPLÍCITO] A recuperação é parcial por tarefa; indexar o acervo inteiro não significa carregá-lo inteiro na janela. O limite operacional atual dos adaptadores continua registrado, sem promessa de contexto máximo ou equivalência à memória nativa das contas. O catálogo completo e os trechos enviados são rastreáveis em cada recibo. Configuração da API/CLI não configura automaticamente conversas avulsas nos sites ou aplicativos dos provedores.
'''
for name in ('TRANSPORTE_DESASSISTIDO.md','COORDINATOR.md'):
    path=BASE/name
    data=path.read_bytes()
    nl='\r\n' if b'\r\n' in data else '\n'
    replace_bytes(path,data+note.replace('\n',nl).encode())
