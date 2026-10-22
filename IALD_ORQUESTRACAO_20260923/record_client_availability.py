from pathlib import Path
from datetime import datetime,timezone
import json,os
base=Path(__file__).resolve().parent
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def save(p,text):
    old=p.read_bytes();new=text.encode('utf-8')
    if old==new:return
    bak=p.with_name(p.name+'.bak_'+stamp);bak.write_bytes(old);assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+stamp);tmp.write_bytes(new);assert tmp.stat().st_size==len(new)>0
    assert p.read_bytes()==old;os.replace(tmp,p);assert p.read_bytes()==new
report={'provider':'kimi','checked_at':datetime.now(timezone.utc).isoformat(),'status':'subscription_access_denied','reason':'O cliente oficial retornou HTTP 403: a assinatura atual não inclui acesso ao Kimi Code.','credential_files_present':True,'execution_validated':False,'record':'validation/kimi_smoke_events.json'}
p=base/'validation/kimi_access_status.json';tmp=p.with_suffix('.tmp');tmp.write_bytes(json.dumps(report,ensure_ascii=False,indent=2).encode());assert tmp.stat().st_size>0;os.replace(tmp,p)
p=base/'iald_orchestrator/providers.py';s=p.read_text(encoding='utf-8')
s=s.replace('                    else:\n                        row["status"] = "installed_pending_auth_validation"','''                    elif name == "kimi":
                        receipt=BASE / "validation/kimi_access_status.json"
                        if receipt.is_file():
                            observed=json.loads(receipt.read_text(encoding="utf-8"))
                            row.update(status=observed["status"],access_check_at=observed["checked_at"],diagnostic=observed["reason"])
                        else:
                            row["status"]="installed_pending_auth_validation"
                    elif name == "gemini":
                        from .profiles import PROFILES
                        row["status"]="installed_pending_auth_validation" if (PROFILES / "gemini/.gemini/oauth_creds.json").is_file() else "installed_needs_login"
                    else:
                        row["status"] = "installed_pending_auth_validation"''')
save(p,s)
p=base/'iald_orchestrator/panel.js';s=p.read_text(encoding='utf-8');s=s.replace("labels.provider_limit_reported=", "labels.subscription_access_denied='Assinatura sem acesso ao cliente Code';\nlabels.provider_limit_reported=");save(p,s)
p=base/'mcp_server.py';s=p.read_text(encoding='utf-8').replace('"""Read-only MCP bridge to the same local selector. No credentials or file tools."""','"""Local MCP: read-only inspection and explicit actions for existing button requests."""');save(p,s)
p=base/'COORDINATOR.md';s=p.read_text(encoding='utf-8').replace('`draft_dispatching` e `synthesis_dispatching`','`draft_dispatching`, `execution_dispatching` e `synthesis_dispatching`');save(p,s)
print('Availability and connector scope recorded.')
