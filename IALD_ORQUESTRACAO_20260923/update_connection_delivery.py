"""Persist measured connection states with byte backups and atomic replacement."""
from datetime import datetime, timezone
from pathlib import Path
import json
import os

BASE = Path(__file__).resolve().parent
STAMP = datetime.now().strftime('%Y%m%d_%H%M%S_%f')


def replace(path, content):
    old = path.read_bytes() if path.exists() else None
    new = content.encode('utf-8')
    if old == new:
        return
    if old is not None:
        backup = path.with_name(path.name + '.bak_' + STAMP)
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temporary = path.with_name(path.name + '.tmp_' + STAMP)
    temporary.write_bytes(new)
    assert temporary.read_bytes() == new and len(new) > 0
    assert (path.read_bytes() if path.exists() else None) == old
    os.replace(temporary, path)
    assert path.read_bytes() == new


p = BASE/'iald_orchestrator/providers.py'
s = p.read_text(encoding='utf-8')
target = '''                    else:
                        row["status"] = "installed_pending_auth_validation"
'''
replacement = '''                    elif name == "mimo":
                        receipt = BASE / "validation/mimo_access_status.json"
                        if receipt.is_file():
                            observed = json.loads(receipt.read_bytes())
                            row.update(status=observed["status"], access_check_at=observed["checked_at"], diagnostic=observed["reason"])
                        else:
                            row["status"] = "installed_pending_auth_validation"
                    else:
                        row["status"] = "installed_pending_auth_validation"
'''
assert s.count(target) == 1
replace(p, s.replace(target, replacement))

p = BASE/'iald_orchestrator/panel.js'
s = p.read_text(encoding='utf-8')
s = s.replace("labels.subscription_access_denied='Assinatura sem acesso ao cliente Code';", "labels.subscription_access_denied='Último teste: acesso ao Code recusado';\nlabels.startup_failed='Cliente não concluiu a inicialização';\nlabels.migration_required='Migrar para Antigravity';")
replace(p, s)

replace(BASE/'validation/mimo_access_status.json', json.dumps({
    'checked_at': datetime.now(timezone.utc).isoformat(), 'status': 'startup_failed',
    'reason': 'MiMo Code 0.1.15 não concluiu --help em 20 segundos no perfil dedicado; nenhuma inferência foi enviada.',
    'execution_validated': False, 'account_required': 'NOT_REQUIRED_FOR_ADVERTISED_FREE_MODE',
    'source': 'https://mimo.xiaomi.com/coder'
}, ensure_ascii=False, indent=2))

replace(BASE/'login_provider.py', '''"""Open an official login in the operator's terminal; never capture credentials."""
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
''')
replace(BASE/'validate_gemini_connection.py', '''"""Compatibility entry point: Google moved personal subscriptions to Antigravity."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('validate_antigravity_connection.py')), run_name='__main__')
''')

p = BASE/'README.md'; s = p.read_text(encoding='utf-8')
s = s.replace('| Claude Code | Login reconhecido; teste recusado por limite informado pelo provedor. Bloqueado no seletor até o operador conferir a cota e permitir outra tentativa. |', '| Claude Code | Revalidado em 23/09 às 16:55 BRT: resposta 42, 4,024 s; consumo de entrada, cache e saída registrado. Bloqueio anterior retirado após o sucesso. Disponível no painel autenticado. |')
s = s.replace('| Gemini CLI | Janela oficial de login aberta. Credencial OAuth ainda ausente no perfil dedicado na última conferência; executor não habilitado. |', '| Google / Antigravity | Gemini CLI recebeu OAuth, mas o serviço devolveu UNSUPPORTED_CLIENT. Antigravity oficial 1.2.9 instalado, login aberto com autorização expressa. Conector por stdin preparado; aguarda conclusão do login e validação real antes de entrar na seleção. |')
s = s.replace('| Kimi Code | Login registrado, mas o cliente oficial devolveu HTTP 403: a assinatura atual não dá acesso ao Kimi Code. Excluído da seleção; não equivale a dizer que a assinatura do chat Kimi não funciona. |', '| Kimi Code | Operador informou compra do Pro pelo aplicativo na conta Google. Último teste continuou com HTTP 403; novo login foi aberto para vincular a mesma conta. Acesso ainda não validado; não inferir ausência da assinatura do aplicativo. |')
s = s.replace('| MiMoCode | Cliente instalado; inicialização do executável não concluiu nos testes limitados. Acesso e condições de uso ainda não validados; excluído da seleção. |', '| MiMoCode | A Xiaomi anuncia uso gratuito sem login. Cliente 0.1.15 instalado, mas --help não concluiu em 20 s no perfil dedicado. Nenhuma inferência feita; excluído da seleção por falha de inicialização, não por falta de conta. |')
s = s.replace('29 testes passaram:', '37 testes passaram (incluindo oito casos do protocolo Antigravity, com processos simulados):')
s = s.replace('O teste visual autenticado da implantação fica pendente; não foi forjada sessão administrativa.', 'Painel de produção autenticado verificado: resposta final do percurso Física, consumo de 282 tokens e Claude disponível. A sessão administrativa é a do operador.')
s += '''

## Atualização das conexões — 23/09/2026

[REAL — engenharia] Antigravity recebe o pedido por stdin somente depois de anunciar o perfil `iald-text` e lista vazia de ferramentas. Falha, truncamento, duplicação de resultado, evento de ferramenta, cancelamento e mudança de configuração impedem aceitar sucesso. O recibo de validação é necessário para habilitar o conector. Os 37 testes locais não equivalem a uma chamada Google autenticada; esta permanece pendente.

Finalize o código Google na janela do Antigravity. Depois, execute `C:\\Python314\\python.exe -X utf8 validate_antigravity_connection.py` nesta pasta para uma única chamada pública de validação (6×7). Atualize a disponibilidade no painel. O cliente anterior Gemini CLI não é mais usado. `gemini.py` conserva somente o diagnóstico do caminho anterior, sem conexão com o executor ativo.

[Jev: cadastro oficial](https://console.typesafe.ai/login) aberto para o operador; não foram aceitos termos, criada conta, gerada chave ou ativada cobrança. [MiMo Code oficial](https://mimo.xiaomi.com/coder) anuncia modalidade sem login; sua disponibilidade efetiva nesta máquina ainda precisa de correção da inicialização. Nenhum código de autorização foi copiado para arquivos do projeto.

Web/admin recebeu os ajustes. iOS interno, iOS externo e Android não têm mudanças de cliente nesta entrega; recompilação não aplicável. Mantidos acionamento por botão e ausência de verificações periódicas.
'''
replace(p, s)
print('Connection status, login commands and README updated with byte backups.')
