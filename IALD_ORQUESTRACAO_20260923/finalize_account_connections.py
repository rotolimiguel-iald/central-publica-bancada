"""Record measured account states and update the admin-only explanation."""
from iald_orchestrator.profiles import BASE
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now
import json

observed = {
    'recorded_at': utc_now(),
    'mimo': {'balance_observed_usd': '100.72', 'cash_observed_usd': '100.00',
             'bonus_observed_usd': '0.72', 'source': 'Authenticated official balance page',
             'observation_phase': 'Before single API smoke test', 'balance_is_live': False,
             'key_name': 'IALD Orquestracao Local', 'key_created_at_displayed': '2026-09-23 18:15:25',
             'expires_at': None, 'expiry_status': 'NOT_REPORTED_BY_PROVIDER'},
    'kimi': {'login_completed': True, 'profile': 'kimi-pro', 'region': 'global',
             'subscription_displayed': 'Adagio', 'subscription_reported_by_operator': 'Pro purchased in mobile app',
             'source': 'https://www.kimi.ai/settings/subscription', 'code_access': 'HTTP_403'},
    'google': {'login_completed': True, 'plan_displayed': 'Google AI Pro',
               'optional_interaction_sharing_enabled': False,
               'consent_source': 'Official CLI checkbox disabled then Done, explicitly authorized by operator',
               'executor_status': 'TOOLS_FILTER_NOT_CONFIRMED', 'inference_prompt_sent': False},
    'jev': {'signup_status': 'TEMPORARILY_CLOSED', 'source': 'https://console.typesafe.ai/login?error=signups_disabled'}
}
save_json(BASE/'validation/account_connections_observed.json', observed)
save_json(BASE/'validation/antigravity_auth.json', dict(observed['google'], checked_at=utc_now()))

def replace(relative, old, new):
    path = BASE/relative
    data = path.read_bytes(); content = data.decode('utf-8').replace('\r\n','\n')
    assert content.count(old) == 1, relative
    output = content.replace(old,new)
    if b'\r\n' in data: output=output.replace('\n','\r\n')
    replace_bytes(path,output.encode())

replace('iald_orchestrator/providers.py', '                if command:', '                if command or name == "mimo":')
replace('iald_orchestrator/policy.py', '(?:sk-ant-|sk-proj-|sk-kimi-|AIza)', '(?:sk-|AIza)')
replace('iald_orchestrator/panel.js', "$('providers').append(card);", "if(p.credential_metadata)card.append(text('p','Validade da chave: não informada pelo provedor.','muted'));$('providers').append(card);")
replace('iald_orchestrator/panel.js', "+task.result.elapsed_seconds+' s':''", "+task.result.elapsed_seconds+' s'+(task.result.cost_estimate_usd?' · custo estimado: US$ '+task.result.cost_estimate_usd:''):''")
replace('validate_kimi_login.py', (BASE/'validate_kimi_login.py').read_text(encoding='utf-8').replace('\r\n','\n'), '''"""Compatibility entry point: validate the newly authenticated Kimi K3 profile."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('check_kimi_pro.py')), run_name='__main__')
''')
readme = BASE/'README.md'
old = readme.read_bytes()
note = '''

## Estado conferido em 23/09/2026, após os logins

- **MiMo API / 2.6 Pro: disponível.** Conta criada e recarga de US$100 realizadas pelo operador. Página oficial mostrou US$100,72 (US$100 pagos + US$0,72 de bônus) antes do teste; isso é um retrato, não saldo em tempo real. Criada a chave exclusiva `IALD Orquestracao Local` e guardada por DPAPI do usuário Windows. Sem chave em código, resposta, prompt ou histórico de tarefas. Validade não informada pelo provedor, exibida assim na administração.
- **Uso MiMo sem teto financeiro local**, por ordem expressa do operador. Sem limite local diário de chamadas para esse provedor. Acionamento manual, sem recarga automática. Limites técnicos de entrada e saída continuam aplicados. API oficial direta, sem ferramentas, sem redirecionar credencial, sem tentativa repetida automática. Modelo `mimo-v2.6-pro`, até4096tokens de resposta+raciocínio por chamada normal. Consumo e estimativa pela tabela oficial são registrados; custo estimado não substitui a fatura.
- Teste real MiMo: resposta42,23tokens de entrada +3de saída=26;2,521s; estimativaUS$0,000012615. Recibo `validation/mimo_connection.json`. Tarifas internacionais consultadas em https://mimo.mi.com/docs/en-US/price/pay-as-you-go: US$0,435entrada não cacheada,US$0,0036cacheada eUS$0,87saída por milhão. Não chamar um teste aritmético de avaliação geral da qualidade.
- **Kimi: login concluído, acesso ao Code recusado.** Novo perfil oficial `kimi-pro`, região global, autenticado na conta Google do operador. Teste explícito `kimi-code/k3` voltouHTTP403. A página autenticada https://www.kimi.ai/settings/subscription mostra **Adagio**; o operador relata Pro comprado no app. Necessário reconciliar o vínculo/restaurar compra no app ou com o suporte do Kimi. Não comprar outra assinatura automaticamente. Evidência `validation/kimi_pro_recheck.json`; chave ou API alternativa paga não configuradas. Executor continua excluído do seletor.
- **Google Antigravity: autenticado.** Conta reconhecida comoGoogleAIPro. Termos concluídos com envio opcional de interações desmarcado, conforme autorização. O perfil `tools: []` não foi confirmado pelo cliente1.2.9, inclusive nos locais de descoberta documentados. O adaptador recusou antes de enviar qualquer pergunta. Autenticação concluída é diferente de executor automático validado. Não desativar essa verificação para anunciar disponibilidade. Perfil dedicado também registrado em `~/.gemini/config/agents/iald-text/agent.md`; nenhum outro agente ou permissão global alterado.
- **Jev/TypeSafe:** página oficial informa novos cadastros temporariamente fechados (`signups_disabled`). Integração permanece pendente de acesso do provedor.
- Local, Codex e Claude seguem as conexões já validadas. A seleção usa uma política inicial de engenharia, sem benchmark que demonstre escolha ótima. O MiMo participa quando elegível; não foi forçada uma escolha nem acionada tarefa privada para testá-lo.

Administração: `/admin/agi/orquestracao`; chaveMiMo: `/admin/agi/orquestracao/mimo`. As rotas exigem administrador; alterações exigem mesma origem. Nenhum aviso de saldo/prazo inserido no app de conversa. Web/admin atualizado; iOSinterno/externo eAndroid não exigem nova compilação para esta alteração de servidor. Distribuições e links existentes preservados, sem nova inspeção física.

Verificação desta entrega:44testes passaram, incluindo sete testes MiMo (DPAPI real com chave fictícia, proteção da rota, transporte, rejeição de respostas incompletas, contabilização e autorização daAPI). Os44testes são complementados pelo teste realMiMo acima. As falhas iniciais no sandbox foram dependências/DPAPI do perfil isolado; suíte passou no usuário do servidor. Evidências de contas em `validation/account_connections_observed.json`. Permanecem pendentes Googleexecutor, vínculoKimiPro e acessoJev.
'''
newline = '\r\n' if b'\r\n' in old else '\n'
replace_bytes(readme, old+note.replace('\n', newline).encode())
print('Observed states, admin labels, and README updated with immediate backups.')
