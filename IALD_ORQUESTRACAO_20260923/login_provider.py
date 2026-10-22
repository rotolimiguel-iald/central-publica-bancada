"""Open an official login in the operator's terminal; never capture credentials."""
import argparse
import subprocess
from iald_orchestrator.profiles import client_environment, login_workspace
from iald_orchestrator.providers import client_command

parser = argparse.ArgumentParser()
parser.add_argument('provider', choices=['gemini', 'kimi'])
name = parser.parse_args().provider
command = client_command(name)
if not command:
    raise SystemExit('Cliente oficial não localizado.')
profile = 'antigravity' if name == 'gemini' else name
print('IALD — conexão oficial de ' + profile, flush=True)
print('Conclua o login no próprio cliente. Insira códigos apenas na janela oficial.', flush=True)
args = command + (['--agent', 'iald-text'] if name == 'gemini' else ['login', '--region', 'global'])
result = subprocess.run(args, cwd=login_workspace(profile), env=client_environment(profile))
print('Cliente encerrado; código ' + str(result.returncode), flush=True)
