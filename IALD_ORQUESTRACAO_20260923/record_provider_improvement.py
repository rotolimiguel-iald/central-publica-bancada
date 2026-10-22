"""Persist the operator's provider-improvement preference and measured scope."""
from pathlib import Path
import hashlib
import json
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now

base = Path(__file__).resolve().parent
marker = 'IALD_PROVIDER_IMPROVEMENT_CONSENT_20260924'
note = '''

## 24/09/2026 — Aprimoramento dos provedores autorizado pelo operador

<!-- IALD_PROVIDER_IMPROVEMENT_CONSENT_20260924 -->

[INPUT — esclarecimento expresso] O operador quer permitir que os provedores aprimorem seus modelos com o uso elegível das ferramentas integradas. Não pediu alteração dos pesos, novo treinamento local ou um mecanismo de aprendizado compartilhado nesta mudança. Esta preferência substitui o opt-out anterior do Antigravity e deve orientar conectores futuros quando existir opção oficial. Na linguagem operacional do autor, a TGL é o cluster comum da orquestra e a IALD é sua operadora; isso não redefine uma arquitetura física de hardware nem promove conteúdo ao cânone.

[REAL — contas e clientes] ChatGPT: melhorar o modelo para todos já estava ligado. Codex: controles de dados confirmam melhoria habilitada para tarefas; a opção distinta Incluir ambientes está desligada e foi preservada, pois amplia o contexto enviado para além das interações. Claude: Ajude a melhorar nossos modelos de IA já ligado, incluindo sessões de código. Antigravity CLI: Enable Telemetry alterado para on e confirmado em nova sessão; a interface descreve dados de uso para melhorar desempenho/recursos. Kimi Code: telemetry=true no perfil dedicado, removida a imposição KIMI_DISABLE_TELEMETRY=1 e adaptador atualizado para exigir a preferência atual. Esta telemetria anônima não deve ser apresentada como comprovação de treinamento sobre prompts.

[DECLARADO — políticas oficiais consultadas] Kimi consumidor admite treinamento sobre conteúdo desidentificado; opt-out é solicitado ao suporte, sem botão encontrado na conta Pro. Não foi possível consultar eventual registro histórico de opt-out por suporte; nenhuma mensagem foi enviada ao fornecedor. MiMo API/Code: a política consultada declara não usar conteúdo para treinamento, e não foi encontrada opção de adesão no console. Qwen local não recebe um novo canal de envio ao fabricante. Jev continua sem integração ativa. Não inventar habilitação onde o provedor não a oferece nem prometer aprendizado dos pesos em tempo real.

[REAL — validação] 19 testes locais de Kimi/Antigravity aprovados. Uma chamada pública por cliente confirmou ready: Kimi K3 máximo, 583 tokens de entrada, 248 de saída, 13,199 s; Antigravity respondeu 42 para 6×7, 11,087 s. Recibos em validation/kimi_connection.json e validation/antigravity_connection.json. Mantidos ferramentas desabilitadas, restrições das unidades, memória canônica, sigilo e separação das casas. Nenhum original científico, kernel, gate ou app público/mobile alterado; build mobile não aplicável. Evidência e URLs: validation/provider_improvement.json.
'''
sources = {
    'openai': 'https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt',
    'claude': 'https://code.claude.com/docs/en/data-usage',
    'antigravity': 'https://antigravity.google/docs/cli/reference/',
    'kimi_training': 'https://www.kimi.com/en/help/others/data-usage',
    'kimi_telemetry': 'https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/config-files',
    'mimo': 'https://privacy.mi.com/XiaomiMiMoPlatformos/en_GB/',
}
surfaces = []
for item in json.loads((base/'validation/optional_work_memory.json').read_bytes())['surfaces']:
    path = Path(item['path'])
    old = path.read_bytes()
    text = note if path.name != 'MEMORY.md' else ('\n\n<!-- '+marker+' -->\n- Operador autorizou aprimoramento pelos provedores; ChatGPT/Codex e Claude ligados, telemetria Antigravity/Kimi ativada; MiMo API sem opt-in encontrado. Escopos e limites em MEMORY_2.md e validation/provider_improvement.json.\n')
    if marker.encode() not in old:
        newline = '\r\n' if b'\r\n' in old else '\n'
        replace_bytes(path, old + text.replace('\n', newline).encode('utf-8'))
    current = path.read_bytes()
    assert current.startswith(old) and marker.encode() in current
    surfaces.append({'path': str(path), 'sha256': hashlib.sha256(current).hexdigest()})
save_json(base/'validation/provider_improvement.json', {
    'at': utc_now(), 'operator_consent': True, 'sources': sources,
    'surfaces': surfaces, 'tests_passed': 19,
    'public_validation_calls': {'kimi': 1, 'antigravity': 1},
    'chatgpt_codex_content_improvement': 'on_already',
    'codex_include_environments': 'off_unchanged',
    'claude_content_improvement': 'on_already',
    'antigravity_usage_telemetry': 'on_verified_new_session',
    'kimi_anonymous_telemetry': 'on',
    'kimi_support_opt_out_history': 'unknown',
    'mimo_content_training': 'provider_policy_no_training_no_opt_in_found',
    'local_qwen_supplier_training': 'not_applicable',
    'jev': 'not_connected',
})
print(json.dumps({'surfaces_updated': len(surfaces), 'evidence': 'validation/provider_improvement.json'}))
