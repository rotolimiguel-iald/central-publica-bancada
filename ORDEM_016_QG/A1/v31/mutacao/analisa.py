# analisa.py — a matriz de MORDIDA e CONSUMO da v3.1 (rodada 2).
# mordida  = erro presente na BASE de um probe NEGATIVO que DESAPARECE sob a mutação (o dente era o campo);
# consumo  = teorema DERIVADO (Teoremas/Paredes/FlagNet/Residual) que passa a errar ou a depender de sorryAx.
# A Ponte v3<->v3.1 NÃO conta como consumidor (transporte campo a campo = tautológico por construção).
# Um estágio BLOQUEADO (Teoremas não compilou) conta como consumo por Teoremas (a quebra já está medida lá).
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'resultado_mutacao.json'), encoding='utf-8'))
base = next(r for r in R if r['name'] == 'BASE')
NEG = ['ProbeToyV31.lean', 'ProbeLegacyV31.lean', 'ProbeVacuousImportV31.lean', 'ProbeTrivialH3v31.lean',
       'ProbeAjustadorV31.lean', 'ProbeRekappaV31.lean']
DER = ['ContratoQG_v31_Teoremas.lean', 'ContratoQG_v31_Paredes.lean', 'FlagNetV31.lean', 'ProbeResidualH3v31.lean']
TAUT = ['PonteV3V31.lean']
linhas = []; kt = set(); oom = 0
for r in R:
    kt.add(r.get('kernel_newer_than_R2_start'))
    for f in r:
        if isinstance(r[f], dict) and 'oom' in r[f]:
            oom += int(r[f]['oom'])
    if r['name'] == 'BASE':
        continue
    row = {'campo': f"{r['struct']}.{r['field']}", 'core_rc': r['ContratoQG_v31.lean']['rc'], 'stage2': r.get('stage2')}
    row['mordida'] = {f[:-5]: sorted(set(base[f]['sitios']) - set(r[f]['sitios'])) for f in NEG
                      if r[f]['rc'] is not None and set(base[f]['sitios']) - set(r[f]['sitios'])}
    row['novos_erros_neg'] = {f[:-5]: sorted(set(r[f]['sitios']) - set(base[f]['sitios'])) for f in NEG
                              if r[f]['rc'] is not None and set(r[f]['sitios']) - set(base[f]['sitios'])}
    q = {}
    for f in DER:
        if r[f]['rc'] is None:
            continue
        e = sorted(set(r[f]['sitios']) - set(base[f]['sitios']))
        s = sorted(set(x.split('.')[-1] for x in r[f]['sorryAx']) - set(x.split('.')[-1] for x in base[f]['sorryAx']))
        if e or s:
            q[f[:-5]] = {'erros': e, 'sorryAx': s}
    row['consumo'] = q
    row['ponte_tautologica_quebra'] = bool(r['PonteV3V31.lean']['rc'] not in (None, 0))
    linhas.append(row)
mord = [x['campo'] for x in linhas if x['mordida']]
cons = [x['campo'] for x in linhas if x['consumo']]
nada = [x['campo'] for x in linhas if not x['mordida'] and not x['consumo']]
res = {'n_campos': len(linhas), 'mordidos_por_probe_negativo': mord, 'consumidos_por_teorema_derivado': cons,
       'sem_mordida_nem_consumo': nada, 'kernel_newer_than_R2_start': sorted(kt), 'oom_logs': oom,
       'core_rc_nao_zero': [x['campo'] for x in linhas if x['core_rc'] != 0], 'linhas': linhas}
json.dump(res, open(os.path.join(HERE, 'matriz_mutacao.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('campos', len(linhas), '| core_rc!=0', res['core_rc_nao_zero'], '| kernel', sorted(kt), '| oom', oom)
print('MORDIDOS (%d):' % len(mord), mord)
print('CONSUMIDOS (%d):' % len(cons))
print('NEM MORDIDA NEM CONSUMO (%d):' % len(nada), nada)
for x in linhas:
    print(x['campo'], '| mordida:', x['mordida'], '| novos:', x['novos_erros_neg'], '| consumo:',
          {k: (v['erros'][:4] + v['sorryAx'][:4]) for k, v in x['consumo'].items()})

# ---- REFINAMENTO (rodada 2): consumo GENUÍNO exclui (i) os sítios de CONSTRUÇÃO do próprio campo mutado
# (`decl.<campo> := ...` cujo alvo virou True — artefato de tipo) e (ii) a propagação de sorryAx (herdada).
gen = {}
for x in linhas:
    fld = x['campo'].split('.')[-1]
    g = {}
    for k, v in x['consumo'].items():
        e = [s for s in v['erros'] if not s.endswith('.' + fld)]
        if e:
            g[k] = e
    x['consumo_genuino'] = g
    gen[x['campo']] = g
res['consumo_genuino_por_campo'] = gen
res['consumidos_genuinamente'] = [c for c, g in gen.items() if g]
res['sem_mordida_nem_consumo_genuino'] = [x['campo'] for x in linhas if not x['mordida'] and not x['consumo_genuino']]
json.dump(res, open(os.path.join(HERE, 'matriz_mutacao.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('---- REFINADO ----')
print('CONSUMIDOS GENUINAMENTE (%d)' % len(res['consumidos_genuinamente']))
print('SEM MORDIDA NEM CONSUMO GENUINO (%d):' % len(res['sem_mordida_nem_consumo_genuino']), res['sem_mordida_nem_consumo_genuino'])
for c, g in gen.items():
    print(c, '->', {k: v[:5] for k, v in g.items()})
