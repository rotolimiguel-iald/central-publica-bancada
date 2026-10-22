"""Document finite MC results with their explicit Gaussian scenario limits."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
B=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((B/n).read_bytes())
a=read('bis/E0_ROUTE_IV_POWER_v2.json');v=read('bis/E0_ROUTE_IV_VALIDATION.json')
if v['source_result_sha256']!=sha(B/'bis/E0_ROUTE_IV_POWER_v2.json'):raise ValueError('Source mismatch')
s='''[DERIVED sobre larguras REAL — NÃO-CEGO; cenário gaussiano, não sensibilidade física calibrada; AGUARDA REVISÃO INDEPENDENTE]

# E0 — poder da rota IV

O limiar é LRT>25. A simulação perfila a média comum nas hipóteses nula e alternativa; a alternativa adiciona variância não negativa. Os sigma de medição são DP amostrais dos posteriores completos existentes (ddof=1), usados somente como aproximação gaussiana para planejamento. A mistura prospectiva sorteia classes de qualidade com probabilidade uniforme entre os eventos existentes; não seleciona eventos de teste pela largura posterior.

O cálculo usa estatísticas suficientes gaussianas por classe: contagens multinomiais, soma normal e soma de quadrados centrados qui-quadrado. Isso permite calcular N grande sem materializar cada observação, com a mesma distribuição. Há controle por otimização escalar independente em 16 casos e comparação da potência homogênea com a cauda qui-quadrado exata. Esses controles verificam implementação, não natureza.

| População de qualidade | sigma_jit INPUT | N50 exploratório | N90 exploratório | N90 com validação nova | Poder na validação | Limite inferior simultâneo |
|---|---:|---:|---:|---:|---:|---:|
'''
for r in a['results']:
    chosen=next(x for x in v['selected'] if x['population']==r['population'] and x['sigma_jit']==r['sigma_jit'])
    n=chosen['N90_validated']
    row=next(x for x in v['cells'] if x['population']==r['population'] and x['sigma_jit']==r['sigma_jit'] and x['N']==n) if n is not None else None
    s+=f"| {r['population']} | {r['sigma_jit']:.4g} | {r['targets']['0.5']['at_or_above']['N']} | {r['targets']['0.9']['at_or_above']['N']} | {n} | {row['power'] if row else None} | {row['simultaneous_lower'] if row else None} |\n"
s+='''
A busca inicial usa 4.000 repetições por N. Seu alvo não é certificado com o mesmo intervalo usado para escolhê-lo. Uma segunda grade finita foi gravada antes de novos sorteios: três N por cenário, 27 células, 20.000 repetições por célula. Cada célula recebe alfa=0,05/27 no limite unilateral exato Clopper–Pearson; selecionar uma célula aprovada dessa grade conserva o controle simultâneo. Os novos sorteios usam sementes separadas; o algoritmo estatístico é o mesmo, portanto não se trata de um segundo estimador independente. N50 permanece busca exploratória com erro MC, não inteiro mínimo exato. A grade N90 também não prova minimalidade.

Dois alvos exploratórios da mistura de 33 não passaram o limite inferior de 90% na validação: foram mantidos no resultado e o alvo reportado subiu na grade predefinida. Não se apagou o fracasso nem se usou apenas a potência pontual. As diferenças contra 59/38/21 da gerência para o caso de alta precisão decorrem da largura real, média perfilada e da exigência adicional de incerteza MC explícita; isso será confrontado na integração E0.

Todos estes N são **limites de planejamento condicionados a sigma_sys=0 e à transferência perfeita do jitter ao estimador IMR**. Essas duas condições não foram medidas aqui. Não autorizam resultado de 5sigma, escolha de desenrolamento ou gate verde. O limiar nominal ainda exige calibração do nulo heterogêneo em E2. A inferência dos posteriores completos da rota IV é E5; esta tabela não a substitui. Não houve posterior novo, PE ou forma de onda.

'''
s+='Equivalentes de informação local em delta-f (soma de (sigma_GW250114/sigma_i)^4; não informação de delta-tau): `'+json.dumps(a['information_df_fourth_power_equivalents'])+'`.\n\n'
s+=f"Tempo medido da busca: {a['elapsed_seconds']:.6f}s; validação: {v['elapsed_seconds']:.6f}s. Uma thread; a parede contínua do orçamento inclui também coordenação e controles. UTC deste adendo {datetime.now(timezone.utc).isoformat()}.\n\n"
for name in ['refeito/e0_route_iv_power_013bis.py','refeito/e0_route_iv_power_013bis_v2.py','refeito/validate_e0_mc_targets_013bis.py','bis/E0_ROUTE_IV_SMOKE.json','bis/E0_ROUTE_IV_POWER_v2.json','bis/E0_ROUTE_IV_VALIDATION_PLAN.json','bis/E0_ROUTE_IV_VALIDATION.json','bis/PART_B_BUDGET_START.json']:
    p=B/name;s+=f'- [{name}](<{p.as_posix()}>) SHA256 `{sha(p)}`.\n'
s+='\nReprodução: WSL /opt/lal_env/bin/python -B nos scripts indicados, em cópia isolada com saídas ausentes; os destinos existentes são recusados. Axiomas: N/A — sem Lean. Não é entrega de B1 nem aceite do portão completo.\n'
p=B/'bis/E0_ROUTE_IV_POWER_NOTE.md'
with p.open('xb') as f:f.write(s.encode('utf-8'))
print(p,sha(p))
