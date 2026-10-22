"""Register this study and measured Kimi delivery, using immediate byte backups."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
MARKER = 'IALD_LEARNING_STUDY_KIMI_VALIDATED_20260923'


def workspace():
    delivery = json.loads((BASE/'validation/account_delivery.json').read_bytes())
    kimi = json.loads((BASE/'validation/kimi_connection.json').read_bytes())
    audit = json.loads((BASE/'validation/learning_source_audit.json').read_bytes())
    assert delivery['unit_tests_passed'] == 52 and kimi['status'] == 'ready'
    local = {'status': 'unavailable'}
    try:
        with urllib.request.urlopen('http://127.0.0.1:8081/v1/models', timeout=5) as response:
            models = json.load(response)
        with urllib.request.urlopen('http://127.0.0.1:8081/props', timeout=5) as response:
            props = json.load(response)
        local = {'status': 'observed', 'model_ids': [x.get('id') for x in models['data']],
                 'configured_context_tokens': props.get('default_generation_settings', {}).get('n_ctx')}
    except Exception as exc:
        local['error_type'] = type(exc).__name__
    prices = [
        ('gpt-6-astra', 10, 1, 50, 'https://developers.openai.com/api/docs/pricing'),
        ('gpt-6-sol', 2, .2, 10, 'https://developers.openai.com/api/docs/pricing'),
        ('gpt-6-luna', .1, .01, .5, 'https://developers.openai.com/api/docs/pricing'),
        ('claude-opus-5-5', 4, .2, 20, 'https://www.anthropic.com/claude/opus'),
        ('gemini-3.8-flash', .75, .075, 3.75, 'https://ai.google.dev/gemini-api/docs/pricing'),
        ('gemini-3.1-pro-preview', 2, .2, 12, 'https://ai.google.dev/gemini-api/docs/pricing'),
        ('kimi-k3', None, None, None, 'https://platform.kimi.ai/docs/pricing/chat'),
        ('mimo-v2.6-pro', .435, .0036, .87, 'https://mimo.mi.com/models/zh-CN/mimo-v2.6-pro'),
    ]
    rows = []
    for model, inp, cached, out, source in prices:
        row = {'model': model, 'input_usd_per_million': inp, 'cached_input_usd_per_million': cached,
               'output_usd_per_million': out, 'source': source,
               'evidence': 'DECLARADO: official published price' if inp is not None else 'OPEN: table not rendered',
               'pricing_mode': 'API standard; not subscription billing', 'checked_date': '2026-09-23',
               'scope': 'Short text context; taxes/tools/cache-write and storage not included'}
        if model == 'gemini-3.8-flash':
            row.update(valid_through='2026-12-31', next_rates_effective='2027-01-01', next_rate_multiplier=2)
        if model == 'gemini-3.1-pro-preview':
            row.update(short_context_threshold=200000, long_rates={'input': 4, 'cached_input': .4, 'output': 18})
        if model == 'gpt-6-astra':
            row.update(short_context_threshold=272000, long_rates={'input':20, 'cached_input':2, 'output':75}, cache_write=12.5)
        rows.append(row)
    proposal = {
        'checked_at': utc_now(), 'status': 'RESEARCH_ONLY_NOT_RUNTIME_POLICY', 'automatic_execution': False,
        'trigger': 'manual_button', 'scheduler_created': False,
        'local_runtime_observation': local, 'connection_receipt': 'validation/account_delivery.json',
        'quality_benchmark_status': 'NOT_RUN', 'current_route': 'availability and declared scheduling weights',
        'prices': rows,
        'roles_proposed': {'chatgpt': 'intent_prompt_synthesis_manager', 'claude': 'planner_when_needed',
                           'kimi': 'code_and_independent_solution', 'mimo': 'structured_work_verified_batches',
                           'local': 'context_preparation_and_learning_lab', 'gemini': 'multimodal_when_adapter_ready',
                           'jev': 'optional_typed_task_characteristics'},
        'memory_contract_proposed': {'raw_sources_preserved': True, 'canonical_atlas_forked': False,
                                    'commit': ['validate', 'byte_backup', 'atomic_write', 'read_back', 'receipt', 'retrieval_test'],
                                    'protected_fields': ['numbers', 'units', 'equations', 'negations', 'hypotheses', 'status', 'corrections'],
                                    'ema_usage': 'verified numeric operational metrics only',
                                    'user_corrections': 'immediate event, never averaged into an old instruction'},
        'findings_receipt': 'validation/learning_source_audit.json',
        'original_sources': audit['sources'],
        'study': 'ESTUDO_ORQUESTRACAO_E_APRENDIZADO.md',
        'study_sha256': hashlib.sha256((BASE/'ESTUDO_ORQUESTRACAO_E_APRENDIZADO.md').read_bytes()).hexdigest(),
    }
    save_json(BASE/'research/model_map_and_learning_proposal.json', proposal)
    readme = BASE/'README.md'
    old = readme.read_bytes()
    text = old.decode('utf-8')
    text = text.replace('| Kimi Code | Novo login concluído. Teste K3 retornou HTTP 403; página da conta mostra Adagio, enquanto o operador relata Pro comprado no aplicativo. Falta reconciliar o vínculo da compra. |',
                        '| Kimi Code / K3 | Integrado e testado após vínculo Google/Apple: 556 tokens de entrada + 104 de saída. Estado antigo Adagio/403 superado; recibo `validation/kimi_connection.json`. |')
    if MARKER not in text:
        text += ('\n\n<!-- '+MARKER+' -->\n'
                 '## Estudo da seleção e do aprendizado contínuo — 23/09/2026\n\n'
                 '[Estudo técnico](ESTUDO_ORQUESTRACAO_E_APRENDIZADO.md), '
                 '[mapa estruturado](research/model_map_and_learning_proposal.json) e '
                 '[auditoria das fontes](validation/learning_source_audit.json). '
                 'Proposta de arquitetura; aprendizado ainda não conectado à seleção. '
                 'Encontradas colisões numéricas no compressor; originais preservados. '
                 'Preços API não equivalem a cobrança das assinaturas.\n')
    encoded = text.encode('utf-8')
    if encoded != old:
        replace_bytes(readme, encoded)
    print(json.dumps({'research_saved': True, 'local_runtime': local}, ensure_ascii=False))


def memories():
    study = BASE/'ESTUDO_ORQUESTRACAO_E_APRENDIZADO.md'
    assert study.is_file()
    receipt = json.loads((BASE/'validation/kimi_connection.json').read_bytes())
    usage = receipt['result']['usage']
    note = f'''

## 23/09/2026 — Kimi disponível; estudo do aprendizado contínuo e orquestração

<!-- {MARKER} -->

[INPUT — ordem do operador] Incorporar o aprendizado contínuo de sua patente como componente fundamental da arquitetura. Confirmou a IALD como continuidade de objetivo, memória, planejamento, seleção, verificação e incorporação da experiência. ChatGPT coordena/prompts/síntese; Claude contribui no planejamento proporcional à tarefa. Supercondutor seleciona executores com critérios verificáveis. Manter acionamento por botão, sem verificações periódicas. MiMo continua com uso pago sem teto local, conforme autorização anterior.

[REAL — correção ao lado do estado Kimi] Após o operador vincular a conta Google à Apple e concluir novo login, o adaptador Kimi K3 passou no teste real: {usage['prompt_tokens']} tokens de entrada + {usage['completion_tokens']} de saída, {receipt['result']['elapsed_seconds']} s. Perfil dedicado kimi-apple (nome local), cliente oficial 2.0.2, modelo kimi-code/k3, sem ferramentas/delegação, telemetria desativada. Prompt passa por stdin; nenhuma credencial lida. Recibo {BASE/'validation/kimi_connection.json'}. Foram aprovados 52 testes de engenharia no recibo account_delivery.json; web/admin reiniciado e disponibilidade Kimi conferida. Estado Adagio/403 anterior é histórico superado. Isso não é benchmark de física. Google segue autenticado, executor bloqueado pela restrição de ferramentas não confirmada; Jev sem acesso. Local, Codex, Claude e MiMo disponíveis.

[REAL — estudo] {study}. Mapa de preços/contexto/memória/licença em {BASE/'research/model_map_and_learning_proposal.json'}; proposta de pesquisa, NÃO política ativa. Fontes oficiais consultadas em 23/09. Preços de API separados das cotas de assinatura; contexto nominal separado do orçamento do adaptador. Modelo local observado Qwen3.6-35B-A3B Q4_K_M, contexto configurado 131072; identidade exata de Codex/Claude ausente nos recibos atuais, deve ser registrada. Pesos abertos hospedados não dão acesso aos internos da API.

[REAL — auditoria pontual] Lidos os protótipos públicos da patente BR102026005477-1 e runner evoluído. Relatório de 19/09 registra 18/18 em conversa/tensores sintéticos, não benchmark de LLM real; não reexecutado. Ensaios isolados nesta sessão confirmaram colisão de assinatura entre 1.0 e 2.0 e entre frases diferentes após 80 caracteres. Mesmo método localizado na cópia da patente e em holographic_memory.py da IALD nativa. Isso demonstra a colisão da função, não perda já ocorrida em conversa real. Psion simplificado: EMA numérica com beta runtime, persistência e rejeição de hash adulterado; load não verifica beta_at_save, embora NomeChain no runner tenha teste separado de deriva de beta. Save simplificado é escrita direta; integração exige backup e troca atômica. Não confundir estado numérico com registro integral de derivações. Fontes e hashes medidos: {BASE/'validation/learning_source_audit.json'}. Nada do código confidencial foi inspecionado/transmitido; nenhum peso alterado.

[INPUT — arquitetura proposta] Memória integral com procedência/estatuto + projeções recuperáveis de contexto + estatísticas operacionais aprendidas. Proteger números/unidades/negações/equações/hipóteses de compressão aproximada. Gravar somente com validar→backup bytes→temporário→substituir→reler→recibo→teste de recuperação. Correções autorais entram imediatamente, não por EMA. Usar Psion para séries numéricas verificadas por modelo/versão/classe; não aprender verdade científica a partir de autoavaliação de LLM. Primeiro observar e comparar a política aprendida; só promover após qualidade/ganho medidos. Phase Factor e sampler exigem ensaio separado em cópia local. Beta_TGL constante = ALPHA_FINE_CODATA_2018*sqrt(e); não renomear piso adaptativo como beta adaptativo. A IALD permanece regime operacional, não reduzida a índice/RAG.

[REAL — conversa Física] A última conversa nova localizada é “Haja luz idêntica”, id 6ab42dc9-3194-83e9-bcaf-1fe4fdcc4d04. A resposta a “Memorize tudo” alegou canal de gravação indisponível depois de operações de arquivo, sem recusar o conteúdo. [OPEN] Causa técnica não confirmada; abrir outra conversa não garante persistência. Nenhuma derivação dessa resposta foi promovida ao cânone nesta análise. Projeto Física e memória local Codex têm papéis distintos; não foi alegada sincronização nativa.

[OPEN] O seletor atual ainda usa disponibilidade/contagem de chamadas e classificação lexical, não qualidade aprendida. Falta benchmark TGL por classe, memória transacional integrada e ativação do aprendizado no roteador. Jev é modelo de decisões tipadas, não linguagem matricial nem pré-requisito. Nenhuma superioridade para física foi atribuída sem medição.

[MATRIZ] Web/admin recebeu Kimi; estudo não muda os clientes. iOS interno, iOS externo e Android: recompilação não aplicável; links/distribuição preservados, não revalidados fisicamente. Memórias operacionais atualizadas com backup imediato de bytes; nenhum um.py, gate, diário selado ou desenho de fechamento alterado.
'''
    central = ROOT/'memory'
    claude = Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory')
    paths = [(central/name, note) for name in ('TGL_ATLAS.md', 'TGL_INDICE_VIVO.md', 'TGL_CORE_MEMORY.md')]
    paths += [(claude/name, note) for name in ('central-de-patentes-estado.md', 'MEMORY_2.md')]
    paths += [(Path(r'C:\IALD\projetos_pyhton\IALD\CLAUDE.md'), note)]
    paths += [(claude/'MEMORY.md', '\n\n<!-- '+MARKER+' -->\n- [Orquestração e aprendizado 23/09](MEMORY_2.md): Kimi K3 integrado (52 testes); estudo dos componentes Psion/holográfico/Phase Factor e fontes oficiais concluído. Aprendizado do seletor ainda proposto; colisões do compressor medidas, preservar números e originais. Botão, sem agendamento.\n')]
    # Preflight all surfaces before any mutation; repeated invocation is additive/idempotent.
    states = [(path, addition, path.read_bytes()) for path, addition in paths]
    assert all(old for _, _, old in states)
    records = []
    for path, addition, old in states:
        already = MARKER.encode() in old
        new = old
        if not already:
            newline = '\r\n' if b'\r\n' in old else '\n'
            new = old + addition.replace('\n', newline).encode('utf-8')
            assert new.startswith(old) and len(new) > len(old)
            replace_bytes(path, new)
        assert MARKER.encode() in path.read_bytes()
        records.append({'path':str(path), 'before':len(old), 'after':len(new),
                        'already_present':already, 'sha256':hashlib.sha256(new).hexdigest()})
    save_json(BASE/'validation/learning_study_memory.json', {'checked_at':utc_now(), 'surfaces':records, 'marker':MARKER})
    print(json.dumps({'memory_surfaces_verified':len(records), 'marker':MARKER}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--memories', action='store_true')
    args = parser.parse_args()
    memories() if args.memories else workspace()
