"""Record verified DeepSeek delivery across the existing memory surfaces."""
from pathlib import Path
import hashlib
import json
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now
from iald_orchestrator import deepseek

base=Path(__file__).resolve().parent
assert deepseek.connection_status()=='ready'
receipt=json.loads(deepseek.RECEIPT.read_bytes())
routing=json.loads((base/'validation/deepseek_routing.json').read_bytes())
marker='IALD_DEEPSEEK_V41_INTEGRATION_20260924'
note='''

## 24/09/2026 — DeepSeek V4.1 Flash incorporado à orquestração

<!-- IALD_DEEPSEEK_V41_INTEGRATION_20260924 -->

[INPUT] Operador pediu a última versão DeepSeek, autorizou criar/guardar a chave e usar o saldo da API e indicou tarefas de média complexidade, com promoção para alta complexidade somente após avaliação de capacidade. Recarga de US$50 posterior foi confirmada como Success na plataforma; a anterior constava Cancelled. A preferência por aprimoramento pelos fornecedores permanece; o console API não exibiu um controle próprio de treinamento, e nenhum opt-out foi acrescentado ao adaptador. Não confundir essa preferência com treinamento comprovado ou memória nos pesos.

[REAL — integração] Executor deepseek na mesma fila, MCP/CLI e painel dos demais provedores. API oficial https://api.deepseek.com/chat/completions; model=deepseek-flash, versão documentada DeepSeek-V4.1-Flash (alias do fornecedor, não pin imutável), reasoning_effort=max, thinking enabled. Contexto configurado 1.048.576; max_tokens até 393.216. Transporte textual sem ferramentas, sem repetição automática de chamadas incertas. Credencial criptografada com DPAPI do usuário Windows; status expõe somente metadados. Validade da chave não informada. Uso pago habilitado para missões solicitadas pelo operador, sem novo teto diário/financeiro local; saldo e limites do provedor permanecem externos. Tier operacional standard: tarefas classificadas deep ficam excluídas até avaliação, sem benchmark de superioridade alegado.

[REAL — memória e controle] Mesmo acervo científico comum, modo deepseek_maximum reservando 393.216 tokens de saída e margem. Prévia local selecionou deepseek com 647.130 bytes de contexto; cobertura PARTIAL_RETRIEVAL_NOT_FULL_CORPUS, contagem conservadora por bytes e sem tokenizer exato. required_provider=deepseek trava o executor e max_calls=1 preserva idempotência; max_output_tokens aceita 1..393216, max_cost_usd somente null (teto por unidade não implementado). Mantidos casa de origem, sigilo, geração/hash/fontes e revisão humana/científica. Custos calculados com tokens medidos e tarifas de pico como estimativa superior, com intervalo pico/fora de pico; não equivalem à fatura.

[REAL — validação e entrega] 70 testes locais aprovados, incluindo autorização, origem web, ferramenta inesperada, contagem inválida, reserva de contexto, memória comum e trava do executor. Primeira tentativa pública recusada HTTP402, preservada em validation/deepseek_pre_credit_refusal.json. Após confirmação do pagamento, nova validação autorizada respondeu 42 para 6×7: 42 tokens de entrada, 20 de saída (18 de raciocínio informados), 62 no total, 0,817s, estimativa US$0,0000183..0,0000366. Não foi teste de contexto de 1M nem de qualidade em física. Painel administrativo conferido: DeepSeek API / V4.1 Flash, Disponível, junto às demais IAs. Sessão irmã Resolver problema da gravidade quântica avisada pela ferramenta oficial e orientada a distribuir unidades de média complexidade pela fila existente, sem repetir o Kimi em andamento.

[DISPONIBILIDADE] Web administrativa atualizada; conversa pública, iOS interno/externo e Android sem mudança de recursos, builds não aplicáveis. Nenhuma alteração de original científico, kernel ou gate. Evidências: validation/deepseek_connection.json, validation/deepseek_routing.json e validation/deepseek_delivery.json em BASE. Preços/limites consultados em https://api-docs.deepseek.com/quick_start/pricing/ e https://api-docs.deepseek.com/guides/thinking_mode/ em 24/09/2026.
'''
records=[]
for entry in json.loads((base/'validation/optional_work_memory.json').read_bytes())['surfaces']:
    path=Path(entry['path']);old=path.read_bytes()
    addition=note if path.name!='MEMORY.md' else ('\n\n<!-- '+marker+' -->\n- DeepSeek V4.1 Flash integrado/validado, disponível no painel, média complexidade, memória TGL comum e reasoning max. Ver MEMORY_2.md e validation/deepseek_delivery.json.\n')
    if marker.encode() not in old:
        newline='\r\n' if b'\r\n' in old else '\n'
        replace_bytes(path,old+addition.replace('\n',newline).encode('utf-8'))
    current=path.read_bytes();assert current.startswith(old) and marker.encode() in current
    records.append({'path':str(path),'sha256':hashlib.sha256(current).hexdigest()})
files=['deepseek.py','deepseek_secret_store.py','providers.py','canonical_memory.py','request_controls.py','runtime.py','coordination.py','web.py','panel.js','deepseek-key.html','deepseek-key.js']
save_json(base/'validation/deepseek_delivery.json',{
    'at':utc_now(),'status':'ready','tests_passed':70,
    'public_validation_attempts':2,'first_attempt':'HTTP402_REFUSED_BEFORE_CREDIT','completed_model_calls':1,
    'validation_usage':receipt['result']['usage'],'memory_preview':routing['decision']['canonical_memory'],
    'surfaces':records,'code_sha256':{f:hashlib.sha256((base/'iald_orchestrator'/f).read_bytes()).hexdigest() for f in files},
    'panel_verified':True,'sister_thread_notified':'01a070fc-9484-7e13-a654-c6b5f61093a4',
    'mobile_build':'NOT_APPLICABLE_ADMIN_ONLY','scientific_sources_modified':False,
})
print(json.dumps({'status':'ready','surfaces':len(records),'tests_passed':70}))
