# analisa.py — lê resultado_mutacao.json e emite a matriz de mutação (frente contrato_v3, 23/09/2026)
import json, os, sys
V3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open(os.path.join(V3, 'mutacao', 'resultado_mutacao.json'), encoding='utf-8'))
base = [r for r in R if r['name'] == 'BASE'][0]
files = ['GuardasV3.lean', 'ContratoQG_v3_Teoremas.lean', 'ProbeToyV3.lean', 'ProbeLegacyV3.lean',
         'ProbeVacuousImportV3.lean', 'ProbeTrivialH3v3.lean']
out = {'base': {f: base[f] for f in files}, 'mutantes': [], 'criterio': None}
ok_all = True
kt = set()
for r in R:
    for f in ['core'] + files:
        if r.get(f) and r[f].get('kernel_touched'):
            kt.update(r[f]['kernel_touched'])
    if r['name'] == 'BASE':
        continue
    row = {'estrutura': r['struct'], 'campo': r['field'], 'linhas': r['span'], 'core_rc': r['core']['rc']}
    for f in files:
        b = set(base[f]['errors']); m = set(r[f]['errors'])
        row[f] = {'rc_base': base[f]['rc'], 'rc_mut': r[f]['rc'], 'novos_erros': sorted(m - b), 'erros_removidos': sorted(b - m)}
    dedicated = f"guard_{r['struct']}_{r['field']}"
    row['guarda_dedicada'] = dedicated
    row['guarda_dedicada_mudou'] = any(e == dedicated or e.startswith(dedicated + '.') for e in row['GuardasV3.lean']['novos_erros'])
    row['medida_invalida_oom'] = any((r[f] or {}).get('invalid_oom') for f in ['core'] + files)
    row['algum_probe_mudou'] = any(row[f]['novos_erros'] or row[f]['erros_removidos'] for f in files)
    ok_all = ok_all and row['guarda_dedicada_mudou'] and row['core_rc'] == 0 and not row['medida_invalida_oom']
    out['mutantes'].append(row)
out['criterio'] = {'todo_campo_muda_sua_guarda_dedicada': ok_all,
                   'base_invalida_oom': any((base[f] or {}).get('invalid_oom') for f in files),
                   'n_invalidos_oom': sum(1 for x in out['mutantes'] if x['medida_invalida_oom']), 'n_mutantes': len(out['mutantes']),
                   'kernel_touched_valores': sorted(kt)}
json.dump(out, open(os.path.join(V3, 'mutacao', 'matriz_mutacao.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# tabela legível
print('criterio:', out['criterio'])
for row in out['mutantes']:
    t = row['ContratoQG_v3_Teoremas.lean']['novos_erros']
    neg = []
    for f in ['ProbeToyV3.lean', 'ProbeLegacyV3.lean', 'ProbeVacuousImportV3.lean', 'ProbeTrivialH3v3.lean']:
        if row[f]['erros_removidos'] or row[f]['novos_erros']:
            neg.append(f"{f.replace('.lean','')}: -{row[f]['erros_removidos']} +{row[f]['novos_erros']}")
    print(f"{'[OOM] ' if row['medida_invalida_oom'] else ''}{row['estrutura']}.{row['campo']}: core rc={row['core_rc']} guarda={'SIM' if row['guarda_dedicada_mudou'] else 'NAO'} "
          f"guardas+={row['GuardasV3.lean']['novos_erros']} | teoremas quebrados ({len(t)}): {t} | negativos: {neg}")
