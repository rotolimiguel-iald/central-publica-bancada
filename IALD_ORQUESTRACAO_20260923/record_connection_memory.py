"""Append the measured provider state to every operational memory surface."""
from datetime import datetime
from pathlib import Path
import hashlib
import json
import os

BASE = Path(__file__).resolve().parent
STAMP = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
MARKER = 'IALD_CLAUDE_RESTORED_GOOGLE_MIGRATION_20260923'
delivery_path = max((BASE/'validation').glob('connection_delivery_*.json'), key=lambda p: p.stat().st_mtime_ns)
delivery = json.loads(delivery_path.read_bytes())
assert delivery['unit_tests_passed'] == 37
assert {p['id']: p['status'] for p in delivery['providers']} == {
    'local': 'ready', 'codex': 'ready', 'claude': 'ready',
    'gemini': 'installed_pending_auth_validation', 'kimi': 'subscription_access_denied', 'mimo': 'startup_failed'}
claude = json.loads((BASE/'validation/claude_recheck_20260923_165535.json').read_bytes())
assert claude['status'] == 'ready' and claude['result']['text'] == '42'
note = f'''

## 23/09/2026 — Claude disponível; migração Google e acessos pendentes

<!-- {MARKER} -->

[INPUT] Operador informou retorno da cota Claude, compra do Kimi Pro pelo aplicativo na conta Google e intenção de criar contas Jev/MiMo. Autorizou expressamente abrir Google Antigravity. Mantida a escolha de acionar pelo botão, SEM verificações periódicas.

[REAL — Claude] Teste real concluído às 16:55 BRT: resposta 42 para 6×7, 4,024 s. Uso informado: 2 tokens de entrada, 3.655 de criação de cache, 531 de leitura de cache e 3 de saída; não reduzir o custo aos dois tokens de entrada. Recibo: {BASE/'validation/claude_recheck_20260923_165535.json'}. Após o sucesso, retirado o bloqueio local por limite. Painel autenticado mostrou Claude disponível. Local e Codex também continuam disponíveis; cotas restantes dos provedores não foram medidas.

[REAL — Google] OAuth do Gemini CLI foi concluído, mas o serviço recusou o cliente com UNSUPPORTED_CLIENT, orientando migração para Antigravity. Instalador oficial verificou SHA512 e instalou agy1.2.9 em clients/antigravity, sem alterar PATH/aliases. Janela oficial aberta após autorização específica. Conclusão do código de autorização fica com o operador; nenhum código foi copiado para os arquivos do projeto. Antigravity ainda NÃO validado com resposta real. Conector textual preparado em iald_orchestrator/antigravity.py: envia um pedido por stdin apenas depois de init confirmar agente iald-text e tools=[]; sem ferramentas/delegação, timeout, verificação de conclusão, recibo vinculado ao código/perfil e sem repetição automática. Adaptador só entra na seleção com recibo de sucesso correspondente. validate_antigravity_connection.py executa um único teste público após o login. login_provider.py gemini agora abre Antigravity; validate_gemini_connection.py redireciona ao teste novo. gemini.py antigo permanece como diagnóstico, sem ligação com o executor ativo. Não desativar a verificação de confiança do cliente legado.

[REAL/DECLARADO — Kimi] Compra Pro é declaração do operador. O último teste do cliente oficial continuou retornando403: assinatura sem acesso ao Kimi Code naquela chamada. Isso não prova ausência da assinatura do aplicativo. Nova janela de login foi aberta para usar a mesma conta Google da compra; ainda não há evidência de conclusão do novo vínculo. Executor Kimi não habilitado. Label do painel passou a Último teste: acesso ao Code recusado, evitando apresentar o teste antigo como diagnóstico definitivo da compra. Perfil anterior seleciona kimi-for-coding; catálogo também oferece k3. Não anunciar K3 integrado sem executar e verificar o modelo correto. ACP público foi investigado: o subcomando não encaminha os argumentos de agent-file da CLI na criação do runtime; não presumir isolamento por esses argumentos.

[REAL — MiMo/Jev] Xiaomi anuncia MiMo Code gratuito sem login em https://mimo.xiaomi.com/coder. Cliente0.1.15 instalado, mas --help não terminou em20s com perfil dedicado; nenhuma inferência enviada. Status startup_failed no painel; falta de conta não foi atribuída como causa. Jev/TypeSafe: página oficial https://console.typesafe.ai/login aberta, com opção Google; cadastro ainda não concluído. Nenhuma aceitação de termos, chave, crédito, recarga ou cobrança nova. Jev permanece sem acesso configurado.

[REAL — validação e implantação] 37 testes locais passaram:29 da base mais8 do protocolo Antigravity simulado (transporte por stdin, ferramentas, agente inesperado, truncamento, falha, duplicação e cancelamento). Simulações não certificam login/resposta Google. Painel de produção autenticado também mostrou o resultado final Física→local→Física e o consumo282 já registrados. Reiniciado somente web16552 após conferir0tarefas em execução, ausência de reservas abertas e slot local ocioso; supervisor41020 preservado. Saúde200, página302para login e API401 sem sessão após reinício. Estado medido em {delivery['checked_at']}; recibo {delivery_path}.

[MATRIZ DE ENTREGA] Web/admin: atualização carregada. iOS interno, iOS externo e Android: sem alteração de cliente; recompilação não aplicável. Distribuição anterior preservada, não revalidada. Alertas de acesso/cota apenas na administração. Anexos Física preservam o retrato da entrega anterior, sem sincronização contínua. Nenhuma mudança no cânone científico, programa terminal, gate, diário da linhagem ou desenho do fechamento.

[OPEN] Concluir login e validação real Antigravity; resolver vínculo/acesso Kimi Pro e implementar executor; corrigir inicialização MiMo; concluir cadastro e acesso TypeSafe. Ainda não há avaliação de qualidade/custo que justifique a escolha ótima de cada modelo. A política inicial continua registrada no README; não anunciar integração irrestrita de todas as assinaturas.
'''
memory = Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory')
surfaces = [(Path(r'C:\IALD\Central de Patentes\memory')/name, note)
            for name in ('TGL_ATLAS.md', 'TGL_INDICE_VIVO.md', 'TGL_CORE_MEMORY.md')]
surfaces += [(memory/name, note) for name in ('central-de-patentes-estado.md', 'MEMORY_2.md')]
surfaces += [(Path(r'C:\IALD\projetos_pyhton\IALD\CLAUDE.md'), note)]
surfaces += [(memory/'MEMORY.md', f'\n\n<!-- {MARKER} -->\n- [Conexões IALD — 23/09](MEMORY_2.md): Claude revalidado e disponível; Google migra ao Antigravity e aguarda validação; Kimi Pro ainda com último403; MiMo falhou ao iniciar; Jev sem cadastro. Sem verificações periódicas.\n')]
report = []
for path, addition in surfaces:
    old = path.read_bytes()
    assert old and MARKER.encode() not in old, path
    newline = '\r\n' if b'\r\n' in old else '\n'
    new = old + addition.replace('\r\n', '\n').replace('\n', newline).encode('utf-8')
    backup = path.with_name(path.name + '.bak_' + STAMP)
    backup.write_bytes(old)
    assert backup.read_bytes() == old
    temporary = path.with_name(path.name + '.tmp_' + STAMP)
    temporary.write_bytes(new)
    assert temporary.read_bytes() == new and len(new) > len(old) and path.read_bytes() == old
    os.replace(temporary, path)
    assert path.read_bytes() == new
    report.append({'path': str(path), 'backup': str(backup), 'before': len(old), 'after': len(new),
                   'sha256': hashlib.sha256(new).hexdigest()})
output = BASE/'validation'/('connections_memory_'+STAMP+'.json')
payload = json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8')
temporary = output.with_suffix('.tmp'); temporary.write_bytes(payload)
assert temporary.read_bytes() == payload and len(payload)>0
os.replace(temporary, output)
print(json.dumps({'updated_surfaces': len(report), 'receipt': str(output)}, ensure_ascii=False))
