"""Fix Google agent discovery and retain the newly authorized Kimi profile."""
from iald_orchestrator.profiles import BASE
from iald_orchestrator.safe_files import replace_bytes

old_agent = BASE/'state/login/antigravity/.agents/agents/iald-text.md'
new_agent = old_agent.parent/'iald-text/agent.md'
replace_bytes(new_agent, old_agent.read_bytes())
adapter = BASE/'iald_orchestrator/antigravity.py'
data = adapter.read_bytes()
replace_bytes(adapter, data.replace(b".agents/agents/iald-text.md", b".agents/agents/iald-text/agent.md"))
profiles = BASE/'iald_orchestrator/profiles.py'
data = profiles.read_bytes()
assert b'profile=PROFILES/provider' in data
replace_bytes(profiles, data.replace(b'profile=PROFILES/provider', b'profile=PROFILES/("kimi-pro" if provider == "kimi" else provider)'))
print('Agent discovery path corrected; Kimi uses newly authenticated dedicated profile.')
