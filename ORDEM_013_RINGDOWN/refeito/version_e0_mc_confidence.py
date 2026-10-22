"""Version the power stopping rule before the full MC, retaining the smoke source."""
from pathlib import Path
import ast,hashlib
B=Path(__file__).resolve().parents[1]
source=B/'refeito/e0_route_iv_power_013bis.py';target=B/'refeito/e0_route_iv_power_013bis_v2.py'
s=source.read_text(encoding='utf-8')
s=s.replace("'bis/E0_ROUTE_IV_SMOKE.json' if args.smoke else 'bis/E0_ROUTE_IV_POWER.json'","'bis/E0_ROUTE_IV_SMOKE_v2.json' if args.smoke else 'bis/E0_ROUTE_IV_POWER_v2.json'")
s=s.replace("while evaluate(hi)['power']<goal:","while (evaluate(hi)['binomial_95'][0] if goal==.9 else evaluate(hi)['power'])<goal:")
s=s.replace("if evaluate(mid)['power']>=goal:hi=mid","if (evaluate(mid)['binomial_95'][0] if goal==.9 else evaluate(mid)['power'])>=goal:hi=mid")
s=s.replace("meaning='Monte Carlo bracket, not exact minimal integer; confidence interval reported'","meaning='Monte Carlo bracket, not exact minimal integer; N50 uses point power, N90 requires Wilson95 lower bound >=0.90; uncertainty and mean profiling make it differ from simple reference counts'")
ast.parse(s)
with target.open('xb') as f:f.write(s.encode('utf-8'))
print(target,hashlib.sha256(target.read_bytes()).hexdigest())
