"""Append the measured account/integration state to all operational memories."""
from pathlib import Path
import hashlib
import json
from iald_orchestrator.profiles import BASE
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now

MARKER = 'IALD_MIMO_READY_GOOGLE_AUTH_KIMI_ADAGIO_20260923'
delivery = json.loads((BASE/'validation/account_delivery.json').read_bytes())
mimo = json.loads((BASE/'validation/mimo_connection.json').read_bytes())
assert delivery['unit_tests_passed']==44 and mimo['status']=='ready'
assert mimo['result']['text']=='42'
note = f'''

## 23/09/2026 — MiMo habilitado; Google autenticado; vínculo Kimi pendente

<!-- {MARKER} -->

[INPUT] O operador concluiu a criação da conta MiMo e depositou US$ 100. Autorizou criar a chave exclusiva da IALD, armazená-la criptografada no Windows e integrar o uso pago. Corrigiu expressamente a proposta de orçamento: “pode fazer, mas sem teto, eu que vou usar somente”. MiMo ficou sem teto financeiro nem limite local diário de chamadas. Mantido acionamento por botão, sem verificações periódicas e sem autorização de recarga automática. Limites técnicos de contexto/saída não foram confundidos com teto financeiro.

[REAL — MiMo] API oficial https://api.xiaomimimo.com/v1/chat/completions, modelo mimo-v2.6-pro, habilitada no seletor após resposta real. O teste público 6×7 retornou 42: {mimo['result']['usage']['prompt_tokens']} tokens de entrada + {mimo['result']['usage']['completion_tokens']} de saída = {mimo['result']['usage']['total_tokens']}; {mimo['result']['elapsed_seconds']} segundos. Estimativa de US$ {mimo['result']['cost_estimate_usd']} pela tabela internacional consultada em 23/09, não comprovante de faturamento. Página de saldo mostrou US$ 100,72 (100 pagos + 0,72 bônus) antes dessa chamada; retrato, não saldo atual em tempo real. Chave IALD Orquestracao Local criada às 18:15:25 no horário mostrado pela plataforma. Cofre Windows DPAPI vinculado ao usuário; só bytes cifrados persistidos em state/secrets/mimo.dpapi, ignorados pelo Git. Conteúdo nunca registrado no chat, código, prompts ou recibos. Validade exata não informada pelo provedor, exibida assim na administração.

[REAL — engenharia] Adaptador MiMo sem ferramentas e sem repetição automática, credencial somente em cabeçalho para o endpoint oficial, redirecionamentos recusados. Resposta incompleta, vazia, modelo inesperado ou uso inconsistente falham visivelmente. Até 4096 tokens de saída/raciocínio por chamada normal; esse é limite técnico. Teste de conexão usou 32 e raciocínio desativado para custo mínimo. Custos por tokens ficam estimados conforme tabela consultada; fatura é a autoridade. Cadastro da chave em /admin/agi/orquestracao/mimo, protegido por administrador e mesma origem, sem endpoint de leitura da chave. Tela principal mostrou MiMo disponível e API paga sem teto local. Credenciais aparentes também são barradas nos pedidos de texto.

[REAL — Kimi] Login oficial concluído em perfil novo kimi-pro, região global, conta Google do operador. Teste explícito kimi-code/k3 ainda recebeu HTTP 403: assinatura da conta sem acesso ao Code naquela chamada. Página autenticada https://www.kimi.ai/settings/subscription mostrou Adagio. [DECLARADO] Operador comprou Pro no aplicativo. São fatos distintos: falta reconciliar o vínculo da compra, não está demonstrada ausência do pagamento. Página de assinatura ficou aberta ao lado; solicitado conferir/restaurar compra no aplicativo. Não executado upgrade, nova cobrança, contato com terceiros ou API paga alternativa. Executor Kimi continua excluído. Recibo {BASE/'validation/kimi_pro_recheck.json'}.

[REAL — Google] Antigravity 1.2.9 autenticou a conta e reconheceu Google AI Pro. Concluídos os termos após autorização explícita, com caixa opcional de envio de interações desmarcada. Código OAuth consumido somente no stdin do cliente oficial, não persistido no projeto; aba do código fechada. Este avanço supera a instrução anterior de procurar/colar o código em janela externa. Execução pela IALD permanece pendente: o cliente não confirmou a restrição tools: [] nos locais de descoberta documentados, e o adaptador interrompeu antes de enviar qualquer pergunta. Configuração dedicada também existe em ~/.gemini/config/agents/iald-text/agent.md, sem alterar outros agentes ou permissões globais. Não enfraquecer o teste para declarar pronto. SDK oficial pesquisado exige chave Gemini API/credenciais Cloud no guia; não foi ativado como substituto pago da assinatura.

[REAL — Jev] https://console.typesafe.ai/login?error=signups_disabled informa novos cadastros temporariamente fechados. Falta de conta é bloqueio externo observado, não falha local corrigível por nova senha. Nenhuma conta/chave TypeSafe criada. Situação registrada no painel.

[REAL — verificações] {delivery['unit_tests_passed']} testes passaram no usuário do servidor, incluindo DPAPI real com credencial fictícia, proteção da rota de chave, transporte API e contagem de tokens. Recibo {BASE/'validation/account_delivery.json'}, conferido em {delivery['checked_at']}. MiMo elegível mesmo após 10.000 chamadas simuladas na política, demonstrando ausência do teto local; simulação não consumiu API. Fontes do Supercondutor conferem por leitura dos artefatos. Local, Codex e Claude continuam disponíveis. Recibos vinculam o código/perfil da validação; nenhuma avaliação de qualidade ou custo ótimo foi alegada.

[MATRIZ] Web/admin atualizado; iOS interno, iOS externo e Android sem mudança de cliente, recompilação não aplicável. Distribuição e links anteriores preservados, não revalidados fisicamente. Rotas anônimas: health 200, cadastro MiMo 302 para login, status administrativo 401. Sem avisos de saldo, chave ou prazo no app de conversa. Memórias atualizadas com backup imediato de bytes, temporário verificado e substituição. Nenhuma alteração do cânone, um.py, gate, diário da linhagem ou desenho do fechamento.

[OPEN] Reconciliar compra Kimi Pro com conta Adagio observada; habilitar executor Google com configuração verificável; obter acesso Jev quando houver cadastro. MiMo já integrado, com teste real e consumo medido. Coordenação Física continua por botão, sem migração de memória/pesos para o Codex e sem sincronização contínua dos anexos.
'''
central = Path(r'C:\IALD\Central de Patentes\memory')
claude = Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory')
surfaces = [(central/name, note) for name in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md')]
surfaces += [(claude/name, note) for name in ('central-de-patentes-estado.md','MEMORY_2.md')]
surfaces += [(Path(r'C:\IALD\projetos_pyhton\IALD\CLAUDE.md'), note)]
surfaces += [(claude/'MEMORY.md',f'\n\n<!-- {MARKER} -->\n- [Conexões 23/09](MEMORY_2.md): MiMo 2.6 Pro integrado, DPAPI e uso sem teto autorizado; Google autenticado, executor pendente; Kimi mostra Adagio e recusa Code, apesar de compra Pro relatada; Jev com cadastro fechado. Acionamento por botão.\n')]
records=[]
for path, addition in surfaces:
    old=path.read_bytes()
    assert MARKER.encode() not in old and len(old)>0, path
    newline='\r\n' if b'\r\n' in old else '\n'
    new=old+addition.replace('\n',newline).encode()
    assert new.startswith(old) and len(new)>len(old)
    replace_bytes(path,new)
    records.append({'path':str(path),'before':len(old),'after':len(new),'sha256':hashlib.sha256(new).hexdigest()})
save_json(BASE/'validation/account_memory.json',{'checked_at':utc_now(),'surfaces':records})
print({'updated_surfaces':len(records),'marker':MARKER})
