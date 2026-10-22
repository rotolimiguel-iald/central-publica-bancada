"""Install the operator-authorized MiMo API integration without exposing secrets."""
from iald_orchestrator.profiles import BASE
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now


def change(relative, old, new):
    path = BASE/relative
    data = path.read_bytes()
    text = data.decode('utf-8').replace('\r\n', '\n')
    assert text.count(old) == 1, relative
    updated = text.replace(old, new)
    if b'\r\n' in data:
        updated = updated.replace('\n', '\r\n')
    replace_bytes(path, updated.encode('utf-8'))


change('iald_orchestrator/web.py', '    @bp.get(root + "/status")', '''    @bp.get("/admin/agi/orquestracao/mimo")
    def mimo_key_page():
        return Response((Path(__file__).parent / "mimo-key.html").read_text(encoding="utf-8"), mimetype="text/html")

    @bp.get(root + "/mimo-key.js")
    def mimo_key_script():
        return Response((Path(__file__).parent / "mimo-key.js").read_text(encoding="utf-8"), mimetype="application/javascript")

    @bp.post(root + "/connections/mimo/key")
    def store_mimo_key():
        from .secret_store import store_mimo
        try:
            store_mimo(request.get_json().get("key"))
        except ValueError:
            return jsonify(error="Formato de chave inválido."), 400
        except Exception:
            return jsonify(error="Não foi possível guardar a chave no cofre Windows."), 503
        return jsonify(stored=True, storage="WINDOWS_DPAPI_CURRENT_USER", expires_at=None)

    @bp.get(root + "/status")''')
change('iald_orchestrator/providers.py', '("mimo", "MiMoCode", "advanced", "unverified")', '("mimo", "MiMo API / 2.6 Pro", "advanced", "authorized_api")')
old = '''                        receipt = BASE / "validation/mimo_access_status.json"
                        if receipt.is_file():
                            observed = json.loads(receipt.read_bytes())
                            row.update(status=observed["status"], access_check_at=observed["checked_at"], diagnostic=observed["reason"])
                        else:
                            row["status"] = "installed_pending_auth_validation"'''
new = '''                        from . import mimo
                        from .secret_store import key_metadata
                        row.update(status=mimo.connection_status(), daily_run_limit=None,
                                   billing_authorized=mimo.authorization().get("enabled") is True,
                                   financial_cap_usd=None, output_token_budget=mimo.MAX_OUTPUT,
                                   output_token_cap_enforced=True, credential_metadata=key_metadata(),
                                   model=mimo.MODEL, credential_scope="SERVER_SIDE_ONLY")'''
change('iald_orchestrator/providers.py', old, new)
change('iald_orchestrator/providers.py', '    elif name in ("codex", "claude"):', '''    elif name == "mimo":
        from . import mimo
        if mimo.connection_status() != "ready":
            raise RuntimeError("MiMo ainda não validado; conferir conexão no painel administrativo.")
        result = mimo.execute(SYSTEM + "\\n\\nTAREFA:\\n" + prompt, cancel=cancel)
    elif name in ("codex", "claude"):''')
change('iald_orchestrator/policy.py', '        if p.get("billing") not in ("local", "subscription"):', '        if p.get("billing") not in ("local", "subscription") and not (p.get("billing") == "authorized_api" and p.get("billing_authorized") is True):')
change('iald_orchestrator/policy.py', '        if counts.get(p["id"], 0) >= p.get("daily_run_limit", 10):', '        if p.get("daily_run_limit", 10) is not None and counts.get(p["id"], 0) >= p.get("daily_run_limit", 10):')
change('iald_orchestrator/policy.py', 'task["estimated_input_tokens"] + 2048', 'task["estimated_input_tokens"] + p.get("output_token_budget", 2048)')
change('iald_orchestrator/panel.html', '<h2>Conexões</h2>', '<h2>Conexões</h2><p><a href="/admin/agi/orquestracao/mimo">Configurar chave MiMo</a></p>')
change('iald_orchestrator/panel.js', "p.billing==='subscription'?'Assinatura · limite operacional':'Condição de uso a conferir'", "p.billing==='subscription'?'Assinatura · limite operacional':p.billing==='authorized_api'?'API paga · sem teto local':'Condição de uso a conferir'")
change('iald_orchestrator/panel.js', "+' / '+p.daily_run_limit", "+' / '+(p.daily_run_limit??'sem teto local')")
change('iald_orchestrator/panel.js', "labels.provider_limit_reported=", "labels.api_key_required='Aguardando chave da API';\nlabels.tools_filter_unavailable='Login concluído · executor pendente';\nlabels.provider_limit_reported=")
change('iald_orchestrator/panel.js', "'Jev: aguardando sua conta e acesso à API.'", "'Jev: novos cadastros temporariamente fechados pela TypeSafe (conferido em 23/09).'")
change('iald_orchestrator/antigravity.py', "            return 'ready'\n    return 'installed_pending_auth_validation'", "            return 'ready'\n        if record.get('signature') == signature() and 'perfil sem ferramentas' in record.get('reason', ''):\n            return 'tools_filter_unavailable'\n    return 'installed_pending_auth_validation'")
save_json(BASE/'state/mimo_authorization.json', {
    'enabled': True, 'financial_cap_usd': None, 'scope': 'IALD_LOCAL_MANUAL_TASKS',
    'authorized_at': utc_now(), 'source': 'Explicit operator instruction in current Codex task',
    'instruction': 'pode fazer, mas sem teto, eu que vou usar somente',
    'auto_recharge_authorized': False, 'periodic_model_calls': False})
check = __import__('json').loads((BASE/'validation/kimi_pro_recheck.json').read_bytes())
assert check['returncode'] == 1 and '403' in check['diagnostic']
save_json(BASE/'validation/kimi_access_status.json', {
    'status': 'subscription_access_denied', 'checked_at': check['checked_at'],
    'reason': 'Novo login Google concluído no perfil kimi-pro. Teste explícito K3 recusado HTTP 403: assinatura desta conta sem acesso ao Kimi Code nesta chamada.',
    'model_requested': 'kimi-code/k3', 'profile': 'kimi-pro'})
print('MiMo integration installed in protected extension; Kimi evidence updated.')
