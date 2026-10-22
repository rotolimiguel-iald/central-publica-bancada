"""Append the read-only Codex archive finding to the Fase 9 handoff."""

import importlib.util
from pathlib import Path

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019")
helper = BASE / "F7.2" / "append_memoria_v2.py"
spec = importlib.util.spec_from_file_location("append_memoria_v2", helper)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.MARKER = b"<!-- FASE9_D72_TAREFA_ANTIGA_ARQUIVADA_20261008 -->"
mod.ENTRY = """

**[REAL — localização da interface]** A listagem de tarefas arquivadas do Codex retornou a tarefa antiga com o mesmo ID `01a070fc-9484-7e13-a654-c6b5f61093a4` e título “Resolver problema da gravidade quântica”. Para localizar o pedido d72, o operador deve entrar em **Tarefas arquivadas**, restaurar essa tarefa e abrir nela o pedido de aprovação pendente. A leitura da lista não comprova que o cartão de aprovação ainda esteja disponível; caso não esteja, a gerência deve recuperar a identidade do pedido, sem executar nem gerar outro ID por inferência.

<!-- FASE9_D72_TAREFA_ANTIGA_ARQUIVADA_20261008 -->
""".encode("utf-8")
target = BASE / "F3.1" / "NOTA_GERENCIA_FASE9_INICIO_20261008.md"
if mod.MARKER in target.read_bytes():
    print({"path": str(target), "status": "already_appended"})
else:
    print(mod.append_one(target))
