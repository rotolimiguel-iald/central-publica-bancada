"""Official Google successor login, interacted with by the operator only."""
from pathlib import Path
import subprocess
from iald_orchestrator.profiles import client_environment

base=Path(__file__).resolve().parent
work=base/'state/login/antigravity';(work/'.git').mkdir(exist_ok=True)
print('IALD — Google Antigravity (sucessor oficial do Gemini CLI)',flush=True)
print('Conclua o login Google no navegador aberto pelo cliente. Não copie códigos ou senhas na conversa.',flush=True)
print('Use o perfil iald-text; ao chegar ao campo de conversa, encerre com Ctrl+C. Nenhum prompt de teste foi enviado por este inicializador.',flush=True)
code=subprocess.call([str(base/'clients/antigravity/agy.exe'),'--agent','iald-text'],cwd=work,env=client_environment('antigravity'))
print('Cliente encerrado; código '+str(code),flush=True)
