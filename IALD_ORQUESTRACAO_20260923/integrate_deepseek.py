"""Apply the reviewed DeepSeek integration with byte-exact backups."""
from pathlib import Path
from iald_orchestrator.safe_files import replace_bytes

base = Path(__file__).resolve().parent / 'iald_orchestrator'


def update(name, pairs):
    path = base / name
    raw = path.read_bytes()
    newline = '\r\n' if b'\r\n' in raw else '\n'
    text = raw.decode('utf-8').replace('\r\n', '\n')
    for before, after in pairs:
        assert before in text, (name, before[:100])
        text = text.replace(before, after)
    replace_bytes(path, text.replace('\n', newline).encode('utf-8'))


update('canonical_memory.py', [
    ('def prepare(prompt, directory=MEMORY,', "def mode_for_provider(provider):\n    return 'deepseek_maximum' if provider == 'deepseek' else 'maximum' if provider in ('kimi', 'mimo') else 'standard'\n\ndef prepare(prompt, directory=MEMORY,"),
    ("if mode not in ('standard','maximum'):", "if mode not in ('standard','maximum','deepseek_maximum'):"),
    ("maximum=mode=='maximum'", "maximum=mode!='standard'\n    output_reserve = 393216 if mode == 'deepseek_maximum' else 131072"),
    ('(1048576-131072-8192 if maximum else 36000)', '(1048576-output_reserve-8192 if maximum else 36000)'),
])
for file in ('runtime.py', 'coordination.py'):
    pairs = []
    if file == 'runtime.py':
        pairs += [
            ("mode='maximum' if c and c['required_provider'] in ('mimo','kimi') else 'standard'", "mode=canonical_memory.mode_for_provider(c['required_provider'] if c else None)"),
            ("decision['selected'] in ('mimo','kimi') and packet['receipt'].get('memory_mode')!='maximum'", "decision['selected'] in ('mimo','kimi','deepseek') and packet['receipt'].get('memory_mode')!=canonical_memory.mode_for_provider(decision['selected'])"),
            ("if c else None,mode='maximum')", "if c else None,mode=canonical_memory.mode_for_provider(decision['selected']))"),
        ]
    else:
        pairs += [("mode='maximum' if c and c['required_provider'] in ('kimi','mimo') else 'standard'", "mode=canonical_memory.mode_for_provider(c['required_provider'] if c else None)")]
    update(file, pairs)

update('providers.py', [
    ('("mimo", "MiMo API / 2.6 Pro", "advanced", "authorized_api")]', '("mimo", "MiMo API / 2.6 Pro", "advanced", "authorized_api"),\n        ("deepseek", "DeepSeek API / V4.1 Flash", "standard", "authorized_api")]'),
    ('if command or name == "mimo":', 'if command or name in ("mimo", "deepseek"): '),
    ('                    elif name == "mimo":', '''                    elif name == "deepseek":
                        from . import deepseek
                        from .deepseek_secret_store import key_metadata
                        row.update(status=deepseek.connection_status(), daily_run_limit=None,
                                   context_budget=deepseek.CONTEXT_WINDOW,
                                   billing_authorized=deepseek.authorization().get("enabled") is True,
                                   financial_cap_usd=None, thinking_effort='max',
                                   output_token_budget=deepseek.MAX_OUTPUT, output_token_cap_enforced=True,
                                   credential_metadata=key_metadata(), model=deepseek.MODEL,
                                   routing_scope="MEDIUM_COMPLEXITY_PENDING_EVALUATION",
                                   credential_scope="SERVER_SIDE_ONLY")
                    elif name == "mimo":'''),
    ("mode='maximum' if name in ('mimo','kimi') else 'standard'", 'mode=canonical_memory.mode_for_provider(name)'),
    ("('mimo','kimi')", "('mimo','kimi','deepseek')"),
    ('\n    elif name == "mimo":\n', '''
    elif name == "deepseek":
        from . import deepseek
        if deepseek.connection_status() != "ready":
            raise RuntimeError("DeepSeek ainda não validado; conferir conexão no painel administrativo.")
        result = deepseek.execute(SYSTEM.replace("Limite a resposta a cerca de 1500 palavras.", "Desenvolva a resposta na extensão necessária à tarefa e às evidências.") + "\\n\\nTAREFA:\\n" + prompt, cancel=cancel, max_output=constraints['max_output_tokens'] if constraints else deepseek.MAX_OUTPUT)
    elif name == "mimo":
'''),
])

update('request_controls.py', [
    ("'kimi','mimo'}", "'kimi','mimo','deepseek'}"),
    ("('mimo','kimi')", "('mimo','kimi','deepseek')"),
    ("    elif 'max_cost_usd' in c or 'max_output_tokens' in c:", '''    elif c['required_provider'] == 'deepseek':
        if c.get('max_cost_usd') is not None:
            raise ValueError('Teto financeiro por unidade DeepSeek ainda não implementado; não será ignorado.')
        c['max_cost_usd'] = None
        c.setdefault('max_output_tokens', 393216)
        if type(c['max_output_tokens']) is not int or not 1 <= c['max_output_tokens'] <= 393216:
            raise ValueError('Saída DeepSeek deve respeitar o limite técnico 1..393216.')
    elif 'max_cost_usd' in c or 'max_output_tokens' in c:'''),
    ("def quote(c):\n", '''def quote(c):
    if c and c['required_provider'] == 'deepseek':
        return {'reserved_usd': '0', 'scope': 'EXECUTOR_ONLY', 'billing': 'PAID_NO_LOCAL_FINANCIAL_CAP', 'max_output_tokens': c['max_output_tokens']}
'''),
    ("if c['required_provider']=='mimo' else", "if c['required_provider'] in ('mimo','deepseek') else"),
    ("    if c['required_provider']!='mimo':", '''    if c['required_provider']=='deepseek':
        from . import deepseek
        # Revalidate token accounting before accepting the paid result.
        checked = deepseek.parse_response({'model': result.get('model'), 'choices': [{'finish_reason': 'stop', 'message': {'content': result.get('text')}}], 'usage': result.get('usage')}, c['max_output_tokens'])
        cost = checked['cost_estimate_usd']
        db.execute("UPDATE request_budget_ledger SET accounted_usd=?,accounting_status='PEAK_RATE_UPPER_ESTIMATE_NOT_INVOICE',usage=? WHERE task_id=?", (cost,json.dumps(checked['usage']),task_id))
        result['request_cost_accounting']={'accounted_usd':cost,'usage':checked['usage'],'status':'PEAK_RATE_UPPER_ESTIMATE_NOT_INVOICE'}
        return
    if c['required_provider']!='mimo':'''),
])

update('web.py', [('    @bp.get(root + "/status")', '''    @bp.get("/admin/agi/orquestracao/deepseek")
    def deepseek_key_page():
        return Response((Path(__file__).parent / "deepseek-key.html").read_text(encoding="utf-8"), mimetype="text/html")

    @bp.get(root + "/deepseek-key.js")
    def deepseek_key_script():
        return Response((Path(__file__).parent / "deepseek-key.js").read_text(encoding="utf-8"), mimetype="application/javascript")

    @bp.post(root + "/connections/deepseek/key")
    def store_deepseek_key():
        from .deepseek_secret_store import store_key
        from .deepseek import AUTHORIZATION
        from .safe_files import save_json, utc_now
        body = request.get_json()
        if body.get("authorize_paid_tasks") is not True:
            return jsonify(error="Confirme o uso do saldo para tarefas autorizadas."), 400
        try:
            store_key(body.get("key"))
            save_json(AUTHORIZATION, {"enabled": True, "scope": "IALD_OPERATOR_AUTHORIZED_TASKS",
                "financial_cap_usd": None, "routing_scope": "MEDIUM_COMPLEXITY_PENDING_EVALUATION",
                "authorized_at": utc_now(), "provider_improvement_preference": True})
        except ValueError:
            return jsonify(error="Formato de chave inválido."), 400
        except Exception:
            return jsonify(error="Não foi possível guardar a chave no cofre Windows."), 503
        return jsonify(stored=True, storage="WINDOWS_DPAPI_CURRENT_USER", expires_at=None)

    @bp.get(root + "/status")''')])

update('panel.js', [
    ("if(p.credential_metadata)card.append", "if(p.id==='deepseek'){card.append(text('p','V4.1 Flash · raciocínio MAX · tarefas de média complexidade. Janela configurada '+p.context_budget.toLocaleString('pt-BR')+' tokens.','muted'));const link=text('a','Conectar DeepSeek');link.href='/admin/agi/orquestracao/deepseek';card.append(link);}if(p.credential_metadata)card.append"),
    ("p.billing==='authorized_api'?'API paga · sem teto local'", "p.billing==='authorized_api'?(p.billing_authorized?'API paga · sem teto local':'API paga · ativação pendente')"),
])
print('DeepSeek integration applied with backups.')
